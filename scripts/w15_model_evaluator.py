#!/usr/bin/env python3
"""W15 Model Evaluator -- REAL implementation (post Fix S61).

Reads pre-computed model snapshots from ``state/model_snapshots/*.json``
refreshed locally by Gonzalo via ``scripts/refresh_model_snapshots.py`` to
comply with Chile's Ley 19.628 -- patient data never leaves the local PC.

Compares each snapshot vs ``state/canonical_facts.json``, computes
per-metric delta (percent) and a drift flag, and optionally invokes a
Claude sub-agent to propose improvements for drifty models.

Modes:
  * ``evaluate`` (default, used in CI): read snapshots + compare + alert
  * ``improve``  (``--improve`` flag, manual only): invoke Claude improver

Output: ``state/model_evaluation.json`` (schema version 2).

Exit codes:
  0  normal (even if drift > 0 -- alert is sent via ntfy)
  1  snapshots dir missing, empty, or canonical_facts unreadable

Design notes (Fix-2, S61):
  * Snapshots are static JSON -- no R execution in CI.
  * Patient-level raw data NEVER touches this script; only aggregated
    metrics shipped in the committed snapshots do.
  * Drift tolerance is 5% (configurable via DRIFT_TOLERANCE_PCT).
  * CANONICAL_MAP routes each ``model_id`` to a section of
    ``canonical_facts.json`` (or ``None`` for models that have no
    canonical reference yet, e.g. Ward clustering).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api, ntfy, state  # noqa: E402
from scripts.lib.claude_live import (  # noqa: E402
    error as live_error,
    finalize,
    heartbeat,
)

SNAPSHOTS_DIR = REPO_ROOT / "state" / "model_snapshots"
CANONICAL_FILE = REPO_ROOT / "state" / "canonical_facts.json"
EVAL_OUTPUT = "model_evaluation.json"

# Any metric whose |snapshot - canonical| / canonical * 100 exceeds
# this threshold raises drift=True for that metric.
DRIFT_TOLERANCE_PCT = 5.0

# Map snapshot ``model_id`` -> section of canonical_facts.json to compare
# against. ``None`` means the model has no canonical reference (we still
# record its snapshot metrics, but every comparison gets delta=None).
CANONICAL_MAP: dict[str, str | None] = {
    "s29k": "facts_model_S29K",
    "walk_forward": "facts_model_S29K",  # same coefficients, OOS variant
    "ward_clustering": None,
    "trilogia_firth": None,
    "fire_scph": None,
    "cluster_2023": None,
    "framework_seremi": None,
    "decision_curve": None,
}


def _now_iso_z() -> str:
    """Return current UTC time as ISO-8601 with trailing ``Z``."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def parse_numeric(value: Any) -> float | None:
    """Extract the first float from a value.

    Handles plain numbers (``0.734``) and strings that embed numbers with
    units or confidence intervals (``'68.1% [61.7, 74.0]'``, ``'IRR=1.28'``).

    Args:
        value: Anything that might contain a number.

    Returns:
        The first float found, or ``None`` if no number can be parsed.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    match = re.search(r"-?\d+\.?\d*", value)
    return float(match.group(0)) if match else None


def compare_metric(snapshot_val: Any, canonical_val: Any) -> dict[str, Any]:
    """Compare a snapshot metric vs its canonical reference.

    Args:
        snapshot_val: Value extracted from the live snapshot JSON.
        canonical_val: Value extracted from canonical_facts.json.

    Returns:
        Dict with ``snapshot``, ``canonical``, ``delta_pct`` (or ``None`` if
        either side could not be parsed or canonical is zero) and
        ``drift`` (bool).
    """
    sv = parse_numeric(snapshot_val)
    cv = parse_numeric(canonical_val)
    if sv is None or cv is None or cv == 0:
        return {
            "snapshot": snapshot_val,
            "canonical": canonical_val,
            "delta_pct": None,
            "drift": False,
        }
    delta_pct = abs((sv - cv) / cv) * 100.0
    return {
        "snapshot": snapshot_val,
        "canonical": canonical_val,
        "delta_pct": round(delta_pct, 3),
        "drift": delta_pct > DRIFT_TOLERANCE_PCT,
    }


def evaluate_snapshot(snap_path: Path, canonical: dict) -> dict[str, Any]:
    """Read a single snapshot JSON file and compare each metric vs canonical.

    Args:
        snap_path: Path to a ``*.json`` file under ``state/model_snapshots/``.
        canonical: Full parsed canonical_facts.json dict.

    Returns:
        Per-model evaluation dict with ``model_id``, ``metric_comparisons``,
        ``drift_count`` and ``overall_drift_flag``.
    """
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    model_id = snap.get("model_id", snap_path.stem)

    canon_section_key = CANONICAL_MAP.get(model_id)
    canon_section: dict[str, Any] = (
        canonical.get(canon_section_key, {}) if canon_section_key else {}
    )

    metrics = snap.get("metrics", {}) or {}
    metric_comparisons: dict[str, Any] = {}
    drift_count = 0
    for metric_key, snap_val in metrics.items():
        if canon_section_key and metric_key in canon_section:
            cmp = compare_metric(snap_val, canon_section[metric_key])
        else:
            cmp = {
                "snapshot": snap_val,
                "canonical": None,
                "delta_pct": None,
                "drift": False,
                "note": "no canonical reference",
            }
        metric_comparisons[metric_key] = cmp
        if cmp.get("drift"):
            drift_count += 1

    if drift_count > 2:
        overall_flag = "high"
    elif drift_count > 0:
        overall_flag = "medium"
    else:
        overall_flag = "low"

    return {
        "model_id": model_id,
        "snapshot_status": snap.get("status", "UNKNOWN"),
        "blindaje_status": snap.get("blindaje_status", "UNKNOWN"),
        "m14_index": snap.get("m14_index", ""),
        "snapshot_generated_at": snap.get("generated_at")
        or snap.get("refreshed_at")
        or snap.get("timestamp"),
        "canonical_section": canon_section_key,
        "metric_comparisons": metric_comparisons,
        "drift_count": drift_count,
        "overall_drift_flag": overall_flag,
        "n_metrics_evaluated": len(metric_comparisons),
    }


def call_improver(
    model_evals: list[dict[str, Any]], canonical: dict
) -> list[dict[str, Any]]:
    """Invoke a Claude sub-agent to propose improvements for drifty models.

    Args:
        model_evals: Full list of per-model evaluation dicts.
        canonical: Parsed canonical_facts.json dict.

    Returns:
        List of improvement proposals (possibly empty) as emitted by Claude.
        Network/parse errors are caught by the caller.
    """
    drifty = [m for m in model_evals if m["overall_drift_flag"] != "low"]
    if not drifty:
        return []

    canon_s29k = canonical.get("facts_model_S29K", {}) or {}
    canon_key_subset = {
        k: v
        for k, v in canon_s29k.items()
        if any(tag in k for tag in ("BSS", "IRR", "EPV", "ICC", "AUC"))
    }

    prompt = (
        "You are 'model-improver', an expert in epidemiological modeling for "
        "Q1 publication.\n\n"
        "Below are evaluation results for ecological models in a Hantavirus "
        "Nuble manuscript about to be submitted to Emerging Infectious "
        "Diseases.\n\n"
        "Your task: for each model with drift_flag != 'low', propose UP TO 3 "
        "concrete improvements to the underlying R script (or method) that "
        "would (a) reduce drift, (b) increase Q1 robustness, (c) elevate "
        "P(accept EID).\n\n"
        f"EVAL DATA:\n{json.dumps(drifty[:5], indent=2, ensure_ascii=False)}\n\n"
        f"CANONICAL EXPECTED METRICS (S29-K):\n"
        f"{json.dumps(canon_key_subset, indent=2, ensure_ascii=False)}\n\n"
        "Output JSON only, no prose:\n"
        "{\n"
        '  "improvements": [\n'
        "    {\n"
        '      "model_id": "...",\n'
        '      "issue": "...",\n'
        '      "proposal": "...",\n'
        '      "expected_lift_pct": 0.0,\n'
        '      "risk": "low|medium|high",\n'
        '      "script_to_modify": "R/...R",\n'
        '      "diff_sketch": "..."\n'
        "    }\n"
        "  ]\n"
        "}"
    )
    resp = claude_api.call_sonnet(prompt, max_tokens=3000)
    parsed = claude_api.extract_json(resp) or {}
    improvements = parsed.get("improvements", [])
    if not isinstance(improvements, list):
        return []
    return improvements


def _load_canonical() -> dict | None:
    """Load canonical_facts.json or return ``None`` on failure."""
    try:
        return json.loads(CANONICAL_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[W15] failed to load canonical_facts.json: {exc}", flush=True)
        return None


def _build_summary(model_evals: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute the ``summary`` block attached to the output JSON."""
    total = len(model_evals)
    n_high = sum(1 for m in model_evals if m["overall_drift_flag"] == "high")
    n_med = sum(1 for m in model_evals if m["overall_drift_flag"] == "medium")
    n_low = sum(1 for m in model_evals if m["overall_drift_flag"] == "low")
    n_blindados = sum(1 for m in model_evals if m["blindaje_status"] == "BLINDADO")
    n_parciales = sum(1 for m in model_evals if m["blindaje_status"] == "PARCIAL")
    n_pendientes = sum(
        1 for m in model_evals if m["blindaje_status"] == "PENDIENTE"
    )
    health_pct = round(100.0 * n_low / max(total, 1), 1)
    return {
        "total_models_evaluated": total,
        "n_high_drift": n_high,
        "n_medium_drift": n_med,
        "n_low_drift": n_low,
        "n_blindados": n_blindados,
        "n_parciales": n_parciales,
        "n_pendientes": n_pendientes,
        "overall_health_pct": health_pct,
    }


def main() -> int:
    """Orchestrate: read snapshots, compare, optionally improve, write output."""
    heartbeat(
        "W15",
        sub_block_id="W15.evaluate",
        status="running",
        detail="reading snapshots",
    )

    if not SNAPSHOTS_DIR.exists():
        ntfy.send_alert(
            "HIGH",
            "W15: no snapshots dir",
            "Run scripts/refresh_model_snapshots.py locally first and commit "
            "state/model_snapshots/*.json",
        )
        live_error("W15", "W15.evaluate", "snapshots dir missing")
        return 1

    snap_files = sorted(SNAPSHOTS_DIR.glob("*.json"))
    if not snap_files:
        ntfy.send_alert(
            "HIGH",
            "W15: empty snapshots",
            "0 model snapshots found in state/model_snapshots/",
        )
        live_error("W15", "W15.evaluate", "snapshots dir empty")
        return 1

    canonical = _load_canonical()
    if canonical is None:
        ntfy.send_alert(
            "HIGH",
            "W15: canonical_facts unreadable",
            "state/canonical_facts.json missing or invalid JSON",
        )
        live_error("W15", "W15.evaluate", "canonical_facts.json unreadable")
        return 1

    model_evals: list[dict[str, Any]] = []
    for sf in snap_files:
        try:
            model_evals.append(evaluate_snapshot(sf, canonical))
        except Exception as exc:  # noqa: BLE001 - best-effort per-file
            print(f"[W15] error evaluating {sf.name}: {exc}", flush=True)

    summary = _build_summary(model_evals)
    total_drift = summary["n_high_drift"] + summary["n_medium_drift"]

    improvements: list[dict[str, Any]] = []
    if "--improve" in sys.argv:
        heartbeat(
            "W15",
            sub_block_id="W15.evaluate",
            status="running",
            detail=f"invoking improver ({total_drift} drifty)",
        )
        try:
            improvements = call_improver(model_evals, canonical)
        except Exception as exc:  # noqa: BLE001
            print(f"[W15] improver failed: {exc}", flush=True)

    payload = {
        "version": 2,
        "evaluated_at": _now_iso_z(),
        "mode": "snapshots_static",
        "drift_tolerance_pct": DRIFT_TOLERANCE_PCT,
        "models": model_evals,
        "summary": summary,
        "improvements": improvements,
    }
    state.save_json(EVAL_OUTPUT, payload)

    if total_drift > 0:
        severity = "HIGH" if summary["n_high_drift"] > 0 else "MED"
        ntfy.send_alert(
            severity,
            f"W15: {total_drift} models drifty",
            (
                f"{summary['n_high_drift']} high, "
                f"{summary['n_medium_drift']} medium. "
                "Run W15 with --improve for Claude-proposed fixes."
            ),
        )

    finalize("W15", [f"state/{EVAL_OUTPUT}"], sub_block_id="W15.evaluate")
    print(
        f"[W15] evaluated {len(model_evals)} models, "
        f"{total_drift} drifty, health {summary['overall_health_pct']}%",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
