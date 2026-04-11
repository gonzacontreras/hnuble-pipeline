"""W12 Annotation Listener.

Polls the ntfy topic dedicated to manuscript annotations, parses any new
messages using :mod:`scripts.lib.annotations`, dedupes them against the
existing ``state/annotations.json`` queue, persists the merged list, and
fires off :mod:`w14_master_orchestrator` via ``gh workflow run`` with the
freshly received ``annotation_id`` values.

Execution model:
    * GitHub Actions cron every 5 minutes (see ``.github/workflows/w12-annotation.yml``).
    * A 10-minute ``since`` window is used to absorb the previous slot with
      overlap, so a single miss does not lose annotations.

The listener is intentionally dumb: it never mutates annotation content, it
only stamps ``received_at`` via :func:`annotations.mark_received` and leaves
``processed = False``. The real editing pipeline lives in W14.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import httpx

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import annotations, ntfy, state  # noqa: E402
from scripts.lib.claude_live import finalize, heartbeat  # noqa: E402

NTFY_TOPIC_ANN: str = os.environ.get(
    "NTFY_TOPIC_ANNOTATIONS", "hnuble-annot-test-demo"
)
POLL_WINDOW_SEC: int = 600  # 10 min overlap
STATE_FILE: str = "annotations.json"


def poll_ntfy(topic: str, since_sec: int = POLL_WINDOW_SEC) -> list[dict[str, Any]]:
    """Fetch recent ntfy messages via ``/json?poll=1&since=<sec>s``.

    Args:
        topic: ntfy topic name (no leading slash, no scheme).
        since_sec: How far back to look, in seconds.

    Returns:
        List of raw ntfy message dicts. Empty on any transport error.
    """
    url = f"https://ntfy.sh/{topic}/json?poll=1&since={since_sec}s"
    try:
        with httpx.Client(timeout=30.0, verify=False) as client:
            resp = client.get(url)
    except httpx.HTTPError as exc:
        print(f"[W12] ntfy transport error: {exc}", flush=True)
        return []

    if resp.status_code != 200:
        print(f"[W12] ntfy HTTP {resp.status_code}: {resp.text[:200]}", flush=True)
        return []

    msgs: list[dict[str, Any]] = []
    for line in resp.text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            msgs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return msgs


def dispatch_w14(new_ids: list[str]) -> bool:
    """Fire ``gh workflow run w14-master.yml`` for the new annotation ids.

    Args:
        new_ids: Annotation ids to pass as ``--field annotation_ids=<csv>``.

    Returns:
        ``True`` on success, ``False`` otherwise. Also sends a ntfy alert
        on HIGH severity when the dispatch fails.
    """
    if not new_ids:
        return True

    csv = ",".join(new_ids)
    try:
        subprocess.run(
            [
                "gh",
                "workflow",
                "run",
                "w14-master.yml",
                "--field",
                f"annotation_ids={csv}",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        ntfy.send_alert("HIGH", "W12 dispatch failed", f"gh CLI missing: {exc}")
        return False
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc))[:200]
        ntfy.send_alert("HIGH", "W12 dispatch failed", detail)
        return False

    ntfy.send(
        title=f"W12: {len(new_ids)} annotations -> W14",
        message=f"Dispatched W14 for IDs: {csv[:100]}",
        priority="default",
        tags=["w12", "dispatch"],
    )
    return True


def main() -> None:
    heartbeat(
        "W12",
        sub_block_id="W12.poll",
        status="running",
        detail=f"polling {NTFY_TOPIC_ANN}",
    )

    current = state.load_json(
        STATE_FILE,
        {"version": 1, "last_poll_at": "1970-01-01T00:00:00Z", "items": []},
    )

    raw_msgs = poll_ntfy(NTFY_TOPIC_ANN)
    parsed: list[dict[str, Any]] = []
    for raw in raw_msgs:
        ann = annotations.parse_ntfy_message(raw)
        if ann is None:
            continue
        ok, err = annotations.validate(ann)
        if not ok:
            print(f"[W12] invalid annotation: {err}", flush=True)
            continue
        parsed.append(annotations.mark_received(ann))

    existing_ids: set[str] = {
        it.get("annotation_id", "") for it in current.get("items", [])
    }
    new_items = [p for p in parsed if p.get("annotation_id") not in existing_ids]

    if new_items:
        merged = list(current.get("items", [])) + new_items
        current["items"] = annotations.dedupe(merged)
        current["last_poll_at"] = new_items[-1]["received_at"]
        current["version"] = int(current.get("version", 0)) + 1
        state.save_json(STATE_FILE, current)

        new_ids = [n["annotation_id"] for n in new_items]
        dispatch_w14(new_ids)

    finalize("W12", [f"state/{STATE_FILE}"], sub_block_id="W12.poll")
    print(
        f"[W12] new={len(new_items)} total={len(current.get('items', []))}",
        flush=True,
    )


if __name__ == "__main__":
    main()
