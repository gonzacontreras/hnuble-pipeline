#!/usr/bin/env python3
"""refresh_model_snapshots.py -- orchestrate R wrappers + write local snapshots.

Run by Gonzalo locally (1x/day, ~1 min wall time). Output goes to
``state/model_snapshots/*.json``. Gonzalo then ``git commit + git push``
the snapshots. W15 in CI reads those committed JSON files and compares
them vs ``state/canonical_facts.json``.

Raw patient data never leaves the local PC -- this script only re-computes
aggregated metrics (already-published summary statistics) from the R
scripts under ``C:/Proyectos/Hantavirus_Nuble/R/``.

Complies with:
  * Chile Ley 19.628 (proteccion datos personales) -- patient-level data
    stays local, commits contain only aggregate metrics.
  * Helsinki Declaration -- no individual re-identification risk in repo.
  * ICMJE authorship transparency -- all figures reproducible from R.

Windows note: ``RSCRIPT`` env var may override the default Rscript path.
The default (``C:/Program Files/R/R-4.5.3/bin/Rscript.exe``) contains
spaces, which is why the subprocess call uses a list of args, not a shell
string.

Usage:
    python scripts/refresh_model_snapshots.py
    # then:
    git add state/model_snapshots/
    git commit -m "refresh model snapshots $(date -I)"
    git push
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
RWRAPPERS_DIR = REPO_ROOT / "scripts" / "r_wrappers"
SNAPSHOTS_DIR = REPO_ROOT / "state" / "model_snapshots"

# Default Rscript path for Gonzalo's Windows 11 box (R 4.5.3 installed
# system-wide). Override via ``set RSCRIPT=...`` in PowerShell if needed.
DEFAULT_RSCRIPT = r"C:/Program Files/R/R-4.5.3/bin/Rscript.exe"
RSCRIPT_BIN = os.environ.get("RSCRIPT", DEFAULT_RSCRIPT)

# Wrappers produced by Fix-1 sub-agent. Each wrapper must print a single
# JSON object to stdout with keys: model_id, metrics, status,
# blindaje_status, generated_at, (optional m14_index).
R_WRAPPERS_TO_RUN: list[tuple[str, str]] = [
    ("s29k", "run_s29k_metrics.R"),
    ("walk_forward", "run_walkforward_metrics.R"),
    ("ward_clustering", "run_ward_metrics.R"),
]

R_TIMEOUT_SECONDS = 600  # 10 min hard cap per wrapper


def _now_iso_z() -> str:
    """Return current UTC time as ISO-8601 with trailing ``Z``."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def run_r_wrapper(model_id: str, script_name: str) -> dict[str, Any] | None:
    """Invoke an R wrapper and return the parsed JSON it prints on stdout.

    Args:
        model_id: Canonical model id (used for logging + missing-file guard).
        script_name: Basename of the wrapper inside ``scripts/r_wrappers/``.

    Returns:
        Parsed JSON dict on success (augmented with ``refreshed_at`` and
        ``mode``), or ``None`` if the wrapper is missing, times out, exits
        non-zero, or emits unparsable stdout.
    """
    script = RWRAPPERS_DIR / script_name
    if not script.exists():
        print(
            f"[refresh] SKIP {model_id}: wrapper not found at {script}",
            flush=True,
        )
        return None

    print(f"[refresh] running {model_id} ({script_name})...", flush=True)
    try:
        result = subprocess.run(
            [RSCRIPT_BIN, "--vanilla", str(script)],
            capture_output=True,
            text=True,
            timeout=R_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        print(
            f"[refresh] FAIL {model_id}: Rscript binary not found at "
            f"{RSCRIPT_BIN}. Set RSCRIPT env var.",
            flush=True,
        )
        return None
    except subprocess.TimeoutExpired:
        print(
            f"[refresh] TIMEOUT {model_id} after {R_TIMEOUT_SECONDS}s",
            flush=True,
        )
        return None

    if result.returncode != 0:
        stderr_tail = (result.stderr or "")[-400:]
        print(
            f"[refresh] FAIL {model_id} (exit {result.returncode}): "
            f"{stderr_tail}",
            flush=True,
        )
        return None

    stdout = (result.stdout or "").strip()
    if not stdout:
        print(f"[refresh] FAIL {model_id}: empty stdout", flush=True)
        return None

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        print(
            f"[refresh] FAIL {model_id} JSON parse: {exc}; "
            f"stdout head={stdout[:200]!r}",
            flush=True,
        )
        return None

    if not isinstance(data, dict):
        print(
            f"[refresh] FAIL {model_id}: top-level JSON is not an object",
            flush=True,
        )
        return None

    data.setdefault("model_id", model_id)
    data["refreshed_at"] = _now_iso_z()
    data["mode"] = "live_R_execution"
    return data


def write_snapshot(model_id: str, data: dict[str, Any]) -> Path:
    """Write ``data`` to ``state/model_snapshots/<model_id>.json`` (pretty)."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    out = SNAPSHOTS_DIR / f"{model_id}.json"
    out.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[refresh] wrote {out}", flush=True)
    return out


def main() -> int:
    """Run every R wrapper, write snapshots, print summary, return exit code."""
    print(f"[refresh] starting at {_now_iso_z()}", flush=True)
    print(f"[refresh] Rscript bin : {RSCRIPT_BIN}", flush=True)
    print(f"[refresh] wrappers dir: {RWRAPPERS_DIR}", flush=True)
    print(f"[refresh] output dir  : {SNAPSHOTS_DIR}", flush=True)

    n_ok = 0
    n_fail = 0
    for model_id, script_name in R_WRAPPERS_TO_RUN:
        data = run_r_wrapper(model_id, script_name)
        if data is None:
            n_fail += 1
            continue
        try:
            write_snapshot(model_id, data)
            n_ok += 1
        except OSError as exc:
            print(
                f"[refresh] FAIL {model_id}: cannot write snapshot: {exc}",
                flush=True,
            )
            n_fail += 1

    print(
        f"[refresh] R wrappers summary: {n_ok} ok, {n_fail} fail "
        f"(of {len(R_WRAPPERS_TO_RUN)} total)",
        flush=True,
    )
    print(
        "[refresh] static snapshots (ward, trilogia, fire, cluster_2023, "
        "framework_seremi, decision_curve) are maintained by the Fix-1 "
        "sub-agent and kept as-is here.",
        flush=True,
    )
    print(
        "[refresh] DONE. Next steps:\n"
        "  git add state/model_snapshots/\n"
        "  git commit -m 'refresh model snapshots'\n"
        "  git push",
        flush=True,
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
