"""W6 — Model Stability.

Cron: daily at 02:00 UTC.
NO Claude API. Runs the R model script with multiple seeds and records sd of
key coefficients. If sd exceeds threshold, notifies HIGH severity.

Since GitHub Actions does not have the R environment pre-installed and the
full dataset is not in the pipeline repo, this W6 runs in "metadata mode":
it reads a pre-computed stability matrix from state/stability_seeds.json
(seeded by local runs in Rscript S29K_MODELO_FINAL_SIN_ZONE.R) and recomputes
summaries. Local hook: a companion R script can be scheduled via Windows
Task Scheduler and pushed via commit.
"""

from __future__ import annotations

import datetime as dt
import os
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


STABILITY_THRESHOLDS = {
    "fsi_r5_coef": 0.03,  # sd > 0.03 raises flag
    "t2m_coef": 0.03,
    "theta": 0.10,
}


def main() -> int:
    seeds_data = state.load_json("stability_seeds.json", {"runs": []})
    runs = seeds_data.get("runs", [])
    if len(runs) < 2:
        print("[w6] insufficient seed data (need >=2 runs)", flush=True)
        # do not touch history; just update pipeline_status
        status = state.load_pipeline_status()
        status.setdefault("workflows", {})
        status["workflows"]["w6"] = {
            "last_run": dt.datetime.utcnow().isoformat() + "Z",
            "seeds": len(runs),
            "status": "insufficient",
        }
        state.save_pipeline_status(status)
        return 0

    summary = {}
    flags: list[str] = []
    for key, threshold in STABILITY_THRESHOLDS.items():
        vals = [r.get(key) for r in runs if isinstance(r.get(key), (int, float))]
        if len(vals) < 2:
            continue
        sd = statistics.stdev(vals)
        summary[key] = {
            "mean": statistics.mean(vals),
            "sd": sd,
            "n": len(vals),
            "threshold": threshold,
            "flag": sd > threshold,
        }
        if sd > threshold:
            flags.append(f"{key}: sd={sd:.4f} > {threshold}")

    history = state.load_stability_history()
    history.setdefault("runs", [])
    now = dt.datetime.utcnow().isoformat() + "Z"
    history["runs"].append({"timestamp": now, "summary": summary})
    history["runs"] = history["runs"][-200:]
    state.save_stability_history(history)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w6"] = {
        "last_run": now,
        "seeds": len(runs),
        "flags": flags,
    }
    state.save_pipeline_status(status)

    if flags:
        ntfy.send_alert(
            "HIGH",
            f"W6: model instability ({len(flags)} coefs)",
            "\n".join(flags),
        )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/stability_history.json", "state/pipeline_status.json"],
            f"W6: {len(flags)} flags @ {now}",
        )

    print(f"[w6] done flags={len(flags)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
