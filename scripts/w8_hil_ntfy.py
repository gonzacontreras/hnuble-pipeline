"""W8 — HIL ntfy dispatcher.

Continuous / manual. Reads state/pending_approvals.json and for any items with
status == 'PENDING_HIL' and no notification_sent flag, sends an ntfy alert with
approve/reject action buttons pointing at GitHub Actions workflow_dispatch URLs.
Marks items as notified.

Note: approve/reject endpoints are GitHub Pages approval forms that open a
GitHub Actions run manually. Gonzalo will approve via the iPhone app by
clicking through to docs/approvals.html which is easiest.
"""

from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


def main() -> int:
    approvals = state.load_pending_approvals()
    items = approvals.get("items", [])
    repo = os.environ.get("GITHUB_REPOSITORY", "gonzacontreras/hnuble-pipeline")
    pages_url = f"https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}"
    sent_count = 0
    now = dt.datetime.utcnow().isoformat() + "Z"

    for item in items:
        if item.get("status") != "PENDING_HIL":
            continue
        if item.get("notification_sent"):
            continue
        item_id = item.get("id", "unknown")
        click_url = f"{pages_url}/approvals.html#{item_id}"
        title = f"HIL: {item.get('type','approval')[:40]}"
        body_parts = [
            f"Finding: {item.get('finding_id','?')}",
            f"Confidence: {item.get('confidence','?')}",
            f"Missing: {item.get('missing','?')}",
        ]
        if item.get("after_text"):
            body_parts.append(f"Proposal: {item['after_text'][:220]}")
        ok = ntfy.send(
            title=title,
            message="\n".join(body_parts),
            priority="high",
            tags=["question"],
            click_url=click_url,
        )
        if ok:
            item["notification_sent"] = now
            sent_count += 1

    state.save_pending_approvals(approvals)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w8"] = {"last_run": now, "notifications_sent": sent_count}
    state.save_pipeline_status(status)

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/pending_approvals.json", "state/pipeline_status.json"],
            f"W8: {sent_count} HIL notifications @ {now}",
        )

    print(f"[w8] done sent={sent_count}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
