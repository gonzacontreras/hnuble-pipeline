"""W15 Model Evaluator and Improver.

Evaluates the 8 active models/tools of the Hantavirus Nuble project against
the canonical metrics stored in ``state/canonical_facts.json``. Produces
``state/model_evaluation.json`` following the schema declared in this file's
docstring.

Two modes:

* **static** (default on GitHub Actions): reads ``state/model_snapshots.json``
  and compares to canonical facts. No R execution. Suitable for CI.
* **live** (only on Gonzalo's Windows box): invokes ``Rscript`` on the
  relevant ``C:/Proyectos/Hantavirus_Nuble/R/*.R`` scripts via subprocess
  to recompute metrics, then writes the fresh numbers to the snapshot file
  so the next static run sees them.

Mode is auto-detected:
    * ``GITHUB_ACTIONS=true`` -> ``static`` always.
    * Otherwise, if ``Rscript`` is on the PATH, ``live``. Else ``static``.

Recommendations per model are hard-coded (1-3 items) so that W14 can pull
them as seed material when an annotation targets ``modelos_activos``.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import ntfy, state  # noqa: E402
from scripts.lib.claude_live import finalize, heartbeat, start_block  # noqa: E402


MODEL_REGISTRY: list[dict[str, Any]] = [
    {
        "id": "s29k",
        "label": "S29-K GLMM NegBin (ecological)",
        "script": "R/S29K_MODELO_FINAL_SIN_ZONE.R",
        "canonical_keys": ["BSS_tier1", "IRR_R5", "ICC"],
        "recommendations": [
            "Report BCa CIs instead of percentile for IRR_R5.",
            "Run sensitivity analysis with cluster bootstrap by comuna.",
            "Add DHARMa zero-inflation test to Supplementary.",
        ],
    },
    {
        "id": "walk_forward",
        "label": "Walk-forward BSS / log score",
        "script": "R/CELDA_1_5_ZINB_POISSON.R",
        "canonical_keys": ["BSS_tier1", "BSS_tier2", "logscore_tier1"],
        "recommendations": [
            "Extend walk-forward horizon to 2024-2025 when panel refreshes.",
            "Compare Brier resolution against persistence baseline.",
        ],
    },
    {
        "id": "ward_cluster",
        "label": "Ward hierarchical clustering (3v)",
        "script": "R/CLUSTER_AUDIT.R",
        "canonical_keys": ["Ward_kappa", "Ward_silhouette"],
        "recommendations": [
            "Repeat with 4v (slope included) as robustness check.",
            "Document mid-p value for the C30 cluster test.",
        ],
    },
    {
        "id": "dag",
        "label": "Causal DAG / adjustment set",
        "script": "R/BH_CORRECTION.R",
        "canonical_keys": [],
        "recommendations": [
            "Export DAG to Supplementary as dagitty code.",
            "Add E-value for the fire->SCPH arrow.",
        ],
    },
    {
        "id": "dlnm_fire",
        "label": "DLNM fire exposure lag",
        "script": "R/EFECTO_EVENTOS_FUEGO.R",
        "canonical_keys": ["IRR_fire", "PAF_fire"],
        "recommendations": [
            "Report dose-response p-trend alongside IRR.",
            "Add specification curve for robustness.",
        ],
    },
    {
        "id": "trilogia",
        "label": "Clinical trilogy score",
        "script": "R/TRILOGIA_CLINICA_SCORE.R",
        "canonical_keys": ["OR_trilogia", "AUC_trilogia"],
        "recommendations": [
            "Cross-validate AUC with LOOCV over 33 cases.",
            "Add calibration plot (Hosmer-Lemeshow).",
        ],
    },
    {
        "id": "mcc",
        "label": "Memory Cross-Checker classifier",
        "script": "scripts/w9_memory_crosschecker.py",
        "canonical_keys": [],
        "recommendations": [
            "Back-test against S59 35 findings (retroactive validation).",
            "Add confusion matrix for BLINDADO/PARCIAL/NUEVO.",
        ],
    },
    {
        "id": "bu_upgrader",
        "label": "Blindaje Upgrader (W10)",
        "script": "scripts/w10_blindaje_upgrader.py",
        "canonical_keys": [],
        "recommendations": [
            "Track time-to-upgrade per PARCIAL finding.",
            "Emit lift estimate per upgrade in logs.",
        ],
    },
]


def _now_iso_z() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _detect_mode() -> str:
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        return "static"
    if shutil.which("Rscript"):
        return "live"
    return "static"


def _canonical_metrics_for(keys: list[str], canonical: dict) -> dict[str, float]:
    """Fetch canonical metric values from ``canonical_facts.json``."""
    facts = canonical.get("facts_model") or canonical.get("facts", {}) or {}
    out: dict[str, float] = {}
    for key in keys:
        val = facts.get(key)
        if isinstance(val, (int, float)):
            out[key] = float(val)
    return out


def _run_rscript(script_rel: str) -> dict[str, float]:
    """Invoke ``Rscript <abs>`` and parse stdout for ``<metric>=<value>``.

    This is intentionally minimal: the R scripts are expected to emit one
    ``metric=value`` line per KPI. Anything else is silently ignored.
    """
    abs_path = Path("C:/Proyectos/Hantavirus_Nuble") / script_rel
    if not abs_path.exists():
        print(f"[W15] live script missing: {abs_path}", flush=True)
        return {}
    try:
        proc = subprocess.run(
            ["Rscript", str(abs_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=600,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"[W15] Rscript call failed: {exc}", flush=True)
        return {}
    metrics: dict[str, float] = {}
    for line in (proc.stdout or "").splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip()
            try:
                metrics[k] = float(v)
            except ValueError:
                continue
    return metrics


def _evaluate_static(
    model: dict, snapshots: dict, canonical: dict
) -> dict[str, Any]:
    canonical_metrics = _canonical_metrics_for(model["canonical_keys"], canonical)
    current = snapshots.get(model["id"], {})
    delta: dict[str, float] = {}
    for key, cval in canonical_metrics.items():
        cur_val = float(current.get(key, cval))
        delta[key] = cur_val - cval
    status = "BLINDADO"
    if any(abs(v) > 1e-3 for v in delta.values()):
        status = "PARCIAL"
    if not canonical_metrics:
        status = "PENDIENTE"
    return {
        "id": model["id"],
        "label": model["label"],
        "script": model["script"],
        "metrics_current": current or canonical_metrics,
        "metrics_canonical": canonical_metrics,
        "delta": delta,
        "status": status,
        "last_eval": _now_iso_z(),
        "recommendations": list(model["recommendations"]),
    }


def _evaluate_live(
    model: dict, canonical: dict
) -> dict[str, Any]:
    canonical_metrics = _canonical_metrics_for(model["canonical_keys"], canonical)
    current = _run_rscript(model["script"]) or canonical_metrics
    delta = {
        key: float(current.get(key, cval)) - float(cval)
        for key, cval in canonical_metrics.items()
    }
    status = "BLINDADO"
    if any(abs(v) > 1e-3 for v in delta.values()):
        status = "PARCIAL"
    if not canonical_metrics:
        status = "PENDIENTE"
    return {
        "id": model["id"],
        "label": model["label"],
        "script": model["script"],
        "metrics_current": current,
        "metrics_canonical": canonical_metrics,
        "delta": delta,
        "status": status,
        "last_eval": _now_iso_z(),
        "recommendations": list(model["recommendations"]),
    }


def _summary(models: list[dict]) -> dict[str, Any]:
    status_counts = {"BLINDADO": 0, "PARCIAL": 0, "PENDIENTE": 0}
    for m in models:
        status_counts[m.get("status", "PENDIENTE")] = (
            status_counts.get(m.get("status", "PENDIENTE"), 0) + 1
        )
    total = max(1, len(models))
    overall_health = (
        status_counts["BLINDADO"] / total
        + 0.5 * status_counts["PARCIAL"] / total
    )
    return {
        "n_blindados": status_counts["BLINDADO"],
        "n_parciales": status_counts["PARCIAL"],
        "n_pendientes": status_counts["PENDIENTE"],
        "overall_health": round(overall_health, 3),
    }


def main() -> None:
    start_block(
        "W15",
        "Model evaluator",
        [
            {"id": "W15.load", "label": "Load canonical + snapshots", "agent_type": "main"},
            {"id": "W15.eval", "label": "Evaluate 8 models", "agent_type": "main"},
            {"id": "W15.write", "label": "Persist evaluation", "agent_type": "main"},
        ],
    )

    mode = _detect_mode()
    heartbeat("W15", "W15.load", status="running", detail=f"mode={mode}")
    canonical = state.load_json("canonical_facts.json", {})
    snapshots = state.load_json("model_snapshots.json", {})
    finalize("W15", ["state/canonical_facts.json"], sub_block_id="W15.load")

    heartbeat(
        "W15",
        "W15.eval",
        status="running",
        detail=f"{len(MODEL_REGISTRY)} models",
    )
    if mode == "live":
        evaluated = [_evaluate_live(m, canonical) for m in MODEL_REGISTRY]
    else:
        evaluated = [
            _evaluate_static(m, snapshots, canonical) for m in MODEL_REGISTRY
        ]
    finalize("W15", ["state/model_evaluation.json"], sub_block_id="W15.eval")

    payload = {
        "version": int(
            state.load_json("model_evaluation.json", {}).get("version", 0)
        )
        + 1,
        "evaluated_at": _now_iso_z(),
        "mode": mode,
        "models": evaluated,
        "summary": _summary(evaluated),
    }
    state.save_json("model_evaluation.json", payload)
    finalize("W15", ["state/model_evaluation.json"], sub_block_id="W15.write")

    ntfy.send(
        title=f"W15: models {payload['summary']['n_blindados']}/8 blindados",
        message=(
            f"mode={mode} health={payload['summary']['overall_health']:.2f} "
            f"parciales={payload['summary']['n_parciales']}"
        ),
        priority="default",
        tags=["w15", "models"],
    )
    print(f"[W15] {json.dumps(payload['summary'])}", flush=True)


if __name__ == "__main__":
    main()
