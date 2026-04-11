"""W0 — Weekly Reconnaissance.

Cron: Monday 06:00 UTC.
Summarizes what changed over the past 7 days across:
 - findings.json
 - objections.json
 - paper_candidates.json
 - pending_approvals.json
 - pipeline_status.json

Produces state/weekly_recon.json and a single ntfy digest.
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


RECON_SYSTEM = """You are a weekly recon summarizer. Given JSON dumps of the pipeline state, produce a concise Spanish digest (~250 words) with:
- Top 3 findings of the week
- New papers of interest
- HIL approvals pending
- Any HIGH severity items needing attention
Return plain text, no markdown fences."""


def _week_ago() -> str:
    return (dt.datetime.utcnow() - dt.timedelta(days=7)).isoformat() + "Z"


def _recent(items: list[dict], since: str, ts_key: str) -> list[dict]:
    return [i for i in items if (i.get(ts_key) or "") >= since]


def main() -> int:
    since = _week_ago()
    findings = state.load_findings().get("items", [])
    objections = state.load_objections().get("items", [])
    candidates = state.load_paper_candidates().get("items", [])
    approvals = state.load_pending_approvals().get("items", [])

    digest_data = {
        "window_start": since,
        "window_end": dt.datetime.utcnow().isoformat() + "Z",
        "new_findings": _recent(findings, since, "discovered_at"),
        "new_objections": _recent(objections, since, "discovered_at"),
        "new_candidates": _recent(candidates, since, "discovered_at"),
        "pending_approvals": [a for a in approvals if a.get("status") == "PENDING_HIL"],
    }

    state.save_json("weekly_recon.json", digest_data)

    # Compose a short digest with Claude
    try:
        summary = claude_api.call_sonnet(
            json.dumps(
                {
                    "new_findings_count": len(digest_data["new_findings"]),
                    "new_objections_count": len(digest_data["new_objections"]),
                    "new_candidates_count": len(digest_data["new_candidates"]),
                    "pending_approvals_count": len(digest_data["pending_approvals"]),
                    "top_findings": digest_data["new_findings"][:3],
                    "top_candidates": digest_data["new_candidates"][:3],
                },
                ensure_ascii=False,
            ),
            max_tokens=800,
            system=RECON_SYSTEM,
        )
    except claude_api.ClaudeAPIError as exc:
        summary = f"W0 summarizer unavailable ({exc}). Raw counts: {len(digest_data['new_findings'])} findings, {len(digest_data['pending_approvals'])} pending HIL."

    ntfy.send(
        title="W0 Weekly Digest",
        message=summary[:2000],
        priority="default",
        tags=["calendar"],
    )

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w0"] = {
        "last_run": digest_data["window_end"],
        "new_findings": len(digest_data["new_findings"]),
        "pending_approvals": len(digest_data["pending_approvals"]),
    }
    state.save_pipeline_status(status)

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/weekly_recon.json", "state/pipeline_status.json"],
            f"W0: weekly digest @ {digest_data['window_end']}",
        )

    print(f"[w0] done findings_w={len(digest_data['new_findings'])}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
