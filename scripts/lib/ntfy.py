"""ntfy.sh wrapper for HIL notifications."""

from __future__ import annotations

import os
from typing import Iterable, Optional

import httpx


def _topic_url() -> str:
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        raise RuntimeError("NTFY_TOPIC env var missing")
    if topic.startswith("http"):
        return topic
    return f"https://ntfy.sh/{topic}"


PRIORITY_MAP = {
    "min": "1",
    "low": "2",
    "default": "3",
    "high": "4",
    "urgent": "5",
    "max": "5",
}


def send(
    title: str,
    message: str,
    priority: str = "default",
    tags: Optional[Iterable[str]] = None,
    click_url: Optional[str] = None,
    actions: Optional[str] = None,
) -> bool:
    """Send a notification.

    actions: raw ntfy "Actions" header value. Example:
      'view, Approve, https://.../approve, clear=true; view, Reject, https://.../reject'
    """
    headers = {
        "Title": title.encode("ascii", "replace").decode("ascii"),
        "Priority": PRIORITY_MAP.get(priority, "3"),
    }
    if tags:
        headers["Tags"] = ",".join(tags)
    if click_url:
        headers["Click"] = click_url
    if actions:
        headers["Actions"] = actions
    try:
        with httpx.Client(timeout=30.0, verify=False) as client:
            r = client.post(_topic_url(), headers=headers, content=message.encode("utf-8"))
        return r.status_code == 200
    except httpx.HTTPError as exc:
        print(f"[ntfy] send failed: {exc}", flush=True)
        return False


def send_alert(severity: str, title: str, body: str) -> bool:
    severity = severity.upper()
    priority = {
        "HIGH": "high",
        "URGENT": "urgent",
        "MED": "default",
        "MEDIUM": "default",
        "LOW": "low",
    }.get(severity, "default")
    tags_map = {
        "HIGH": ["warning"],
        "URGENT": ["rotating_light"],
        "MED": ["mag"],
        "MEDIUM": ["mag"],
        "LOW": ["information_source"],
    }
    return send(
        title=f"[{severity}] {title}",
        message=body,
        priority=priority,
        tags=tags_map.get(severity, []),
    )


def send_approval_request(
    title: str,
    body: str,
    approve_url: str,
    reject_url: str,
    click_url: Optional[str] = None,
) -> bool:
    actions = (
        f"view, Approve, {approve_url}, clear=true; "
        f"view, Reject, {reject_url}, clear=true"
    )
    return send(
        title=title,
        message=body,
        priority="high",
        tags=["question"],
        click_url=click_url,
        actions=actions,
    )
