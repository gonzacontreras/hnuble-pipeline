"""W5 — Reviewer Virtuals.

Cron: daily at 04:00 UTC.
Runs 3 virtual reviewers (Stats, EpiEco, Editorial) against the current
manuscript, produces top objections, dedupes against existing baseline, and
pushes new objections into state/objections.json. Triggers W9 MCC on new items.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api  # noqa: E402
from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


REVIEWERS = {
    "stats": """You are a senior statistical reviewer in the style of Harrell / VanderWeele / Gelman.
Focus on: model mis-specification, CI coverage, calibration, overfitting, bootstrap propagation, confounding, temporal leakage.
Be blunt. Return JSON with a list `objections` of up to 5 items: {id, severity (HIGH/MED/LOW), title, critique (<=400 chars), suggested_response (<=400 chars)}.""",
    "epieco": """You are an eco-epidemiology reviewer in the style of Torres-Perez / Polop / Padula / Luis.
Focus on: reservoir ecology plausibility, lag biology (bamboo masting vs operational lag), DAG structure, case definition drift, ascertainment bias, climate-vegetation causality.
Return JSON with `objections` (same schema as Stats).""",
    "editorial": """You are an EID editorial reviewer (CDC EID style).
Focus on: novelty framing, scope appropriateness, replicability, overstatement of claims, missing limitation disclosures, supplementary completeness, word count compliance.
Return JSON with `objections` (same schema as Stats).""",
}


def load_manuscript_excerpt() -> str:
    candidates = [
        REPO_ROOT / "state" / "manuscript_improved.md",
        REPO_ROOT / "state" / "manuscript_control.md",
    ]
    for c in candidates:
        if c.exists():
            return c.read_text(encoding="utf-8", errors="ignore")[:22000]
    return ""


def run_reviewer(role: str, system: str, manuscript: str, prior_objections: list[dict]) -> list[dict]:
    prior_compact = [
        {"id": o.get("id"), "title": o.get("title")} for o in prior_objections[:50]
    ]
    prompt = (
        "PRIOR OBJECTIONS (already logged, do not repeat):\n"
        + json.dumps(prior_compact, ensure_ascii=False)
        + "\n\nMANUSCRIPT EXCERPT:\n"
        + manuscript
        + "\n\nReturn strict JSON only."
    )
    try:
        resp = claude_api.call_sonnet(prompt, max_tokens=2500, system=system)
    except claude_api.ClaudeAPIError as exc:
        print(f"[w5:{role}] claude error: {exc}", flush=True)
        return []
    parsed = claude_api.extract_json(resp) or {}
    items = parsed.get("objections", []) if isinstance(parsed, dict) else []
    for i, item in enumerate(items):
        item.setdefault("id", f"W5-{role}-{dt.datetime.utcnow().strftime('%Y%m%d')}-{i+1:02d}")
        item["role"] = role
    return items


def main() -> int:
    manuscript = load_manuscript_excerpt()
    if not manuscript:
        print("[w5] no manuscript", flush=True)
        return 0

    objections = state.load_objections()
    objections.setdefault("items", [])
    prior = objections["items"]

    all_new: list[dict] = []
    for role, system in REVIEWERS.items():
        new = run_reviewer(role, system, manuscript, prior)
        all_new.extend(new)

    now = dt.datetime.utcnow().isoformat() + "Z"
    existing_ids = {o.get("id") for o in prior}
    added: list[dict] = []
    for o in all_new:
        if o.get("id") in existing_ids:
            continue
        o["discovered_at"] = now
        o["status"] = "PENDING_MCC"
        objections["items"].append(o)
        added.append(o)

    objections["last_w5_run"] = now
    state.save_objections(objections)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w5"] = {
        "last_run": now,
        "new_objections": len(added),
    }
    state.save_pipeline_status(status)

    if added:
        high = [o for o in added if o.get("severity") == "HIGH"]
        ntfy.send_alert(
            "HIGH" if high else "MED",
            f"W5: +{len(added)} reviewer objections",
            f"{len(high)} HIGH severity. Flowing to W9 MCC.",
        )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/objections.json", "state/pipeline_status.json"],
            f"W5: +{len(added)} objections @ {now}",
        )

    print(f"[w5] done added={len(added)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
