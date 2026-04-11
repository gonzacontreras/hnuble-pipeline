"""W10 — Blindaje Upgrader (BU, V2).

Consumes state/w10_queue.json (PARCIAL findings from W9) and produces upgrade
proposals for each: a suggested citation (Q1 2023-2026), a calculation recipe
and/or a ready-to-integrate sentence. Pushes each proposal to HIL via W8.
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


BU_SYSTEM = """You are the Blindaje Upgrader for the Hantavirus Nuble EID manuscript.

Given a PARCIAL finding (missing citation, calculation, or phrase), produce a
ready-to-integrate upgrade. Use Q1 literature from 2023-2026 when you know it.
Never fabricate DOIs or author names; set null when unknown and mark confidence LOW.

Return strict valid JSON (no comments, no trailing commas, no pseudo-code):

{"upgrades": [{"finding_id": "S59-TOP5-01", "missing": "CITATION", "before_text": "current fragment", "after_text": "proposed 30-80 word replacement", "citation": {"authors": "Smith et al.", "year": 2024, "venue": "Lancet Planet Health", "doi": "10.1016/xxx", "relevance": "<=150 chars"}, "calc_recipe": null, "rationale": "<=200 chars", "confidence": "MED"}]}

Rules:
- missing MUST be one of: CITATION, CALC, PHRASE
- confidence MUST be one of: HIGH, MED, LOW
- If no real Q1 paper is known, set citation.doi to null and confidence to LOW
- calc_recipe can be an R code string or null
- Return only the JSON, no prose
"""


def main() -> int:
    queue = state.load_json("w10_queue.json", {"items": []})
    items = queue.get("items", [])
    if not items:
        print("[w10] queue empty", flush=True)
        return 0

    # Process oldest first, batch of up to 6
    batch = items[:6]
    payload = [
        {
            "finding_id": f.get("id"),
            "title": f.get("title"),
            "severity": f.get("severity"),
            "missing": f.get("mcc_missing"),
            "rationale": f.get("mcc_rationale"),
            "evidence": (f.get("evidence") or "")[:400],
            "fix_hint": f.get("fix_hint", ""),
        }
        for f in batch
    ]

    prompt = (
        "Produce upgrade proposals for these PARCIAL findings. Return JSON only.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    try:
        resp = claude_api.call_sonnet(prompt, max_tokens=4000, system=BU_SYSTEM)
    except claude_api.ClaudeAPIError as exc:
        print(f"[w10] claude error: {exc}", flush=True)
        return 1

    parsed = claude_api.extract_json(resp) or {}
    upgrades = parsed.get("upgrades", []) if isinstance(parsed, dict) else []

    now = dt.datetime.utcnow().isoformat() + "Z"
    approvals = state.load_pending_approvals()
    approvals.setdefault("items", [])
    added = 0
    for u in upgrades:
        app = {
            "id": f"W10-{u.get('finding_id','?')}-{now[:19]}",
            "type": "BLINDAJE_UPGRADE",
            "finding_id": u.get("finding_id"),
            "missing": u.get("missing"),
            "before_text": u.get("before_text"),
            "after_text": u.get("after_text"),
            "citation": u.get("citation"),
            "calc_recipe": u.get("calc_recipe"),
            "rationale": u.get("rationale"),
            "confidence": u.get("confidence", "LOW"),
            "created_at": now,
            "status": "PENDING_HIL",
        }
        approvals["items"].append(app)
        added += 1

    state.save_pending_approvals(approvals)

    # Drop processed items from the queue
    queue["items"] = items[6:]
    state.save_json("w10_queue.json", queue)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w10"] = {
        "last_run": now,
        "upgrades": added,
        "queue_remaining": len(queue["items"]),
    }
    state.save_pipeline_status(status)

    # HIL notification
    if added:
        titles = "\n".join(
            f"- [{u.get('confidence','?')}] {u.get('finding_id')}: "
            f"{(u.get('after_text') or '')[:80]}"
            for u in upgrades
        )
        ntfy.send_alert(
            "HIGH",
            f"W10: {added} blindaje upgrades pending HIL",
            f"{titles}\n\nReview in docs/approvals.html",
        )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            [
                "state/pending_approvals.json",
                "state/w10_queue.json",
                "state/pipeline_status.json",
            ],
            f"W10: +{added} upgrades @ {now}",
        )

    print(f"[w10] done upgrades={added}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
