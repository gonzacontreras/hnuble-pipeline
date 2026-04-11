"""W4 — Figure Iterator (stub).

On-demand. Low priority in S60 build: produces a short text analysis of a
figure's caption and suggests improvements. Does NOT generate images yet
(requires multimodal capacity + local R pipeline). Placeholder that logs and
emits a ntfy info message.
"""

from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


SYSTEM = """You review scientific figure captions for a Q1 journal. Given a caption, produce:
- 3 concrete improvements (clarity, data honesty, axis labels, CI)
- 1 red-team objection
- A revised caption (<=120 words)
Return plain text."""


def main() -> int:
    caption = os.environ.get("W4_CAPTION", "")
    if not caption:
        print("[w4] W4_CAPTION env var missing", flush=True)
        return 1
    try:
        resp = claude_api.call_sonnet(caption, max_tokens=1200, system=SYSTEM)
    except claude_api.ClaudeAPIError as exc:
        print(f"[w4] claude error: {exc}", flush=True)
        return 1

    now = dt.datetime.utcnow().isoformat() + "Z"
    out = state.load_json("w4_reviews.json", {"items": []})
    out.setdefault("items", []).append(
        {"timestamp": now, "caption": caption, "review": resp}
    )
    state.save_json("w4_reviews.json", out)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w4"] = {"last_run": now}
    state.save_pipeline_status(status)

    ntfy.send(
        title="W4 caption review",
        message=resp[:1000],
        priority="low",
        tags=["art"],
    )
    print("[w4] done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
