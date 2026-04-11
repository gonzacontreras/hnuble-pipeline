"""Annotation parser, validator and utilities (stub).

This module handles the annotations that Gonzalo emits from Obsidian via
ntfy. Each annotation is a JSON payload embedded in the ``message`` field of
a raw ntfy message. The schema source of truth lives at
``state/schemas/annotation_message_v1.schema.json`` (created by B1.1).

Responsibilities:
    * ``parse_ntfy_message`` decodes the JSON payload from the raw ntfy dict.
    * ``validate`` checks required fields, color enum, string lengths,
      paragraph id, and selection range sanity.
    * ``dedupe`` removes duplicates by ``annotation_id`` while preserving
      arrival order.
    * ``mark_received`` / ``mark_processed`` stamp lifecycle timestamps and
      worker metadata.

This file is a STUB: the real downstream consumer
``scripts/w14_annotation_applier.py`` will import these helpers to feed the
annotation-driven editing loop.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION: str = "v1"
VALID_COLORS: set[str] = {"yellow", "green", "red"}
MAX_COMMENT_LEN: int = 2000
MAX_SELECTED_LEN: int = 2000

_REQUIRED_FIELDS: tuple[str, ...] = (
    "annotation_id",
    "para_id",
    "selection_start",
    "selection_end",
    "selected_text",
    "color",
    "comment",
    "ts",
    "schema_version",
)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_ntfy_message(ntfy_raw: dict) -> dict | None:
    """Parse a raw ntfy message into an annotation dict.

    The expected ntfy wire format (as returned by ``/json?poll=1``) is::

        {
            "id": "...",
            "time": 1712846400,
            "event": "message",
            "topic": "...",
            "message": "<json-encoded annotation payload>",
            "title": "...",
            "tags": [...]
        }

    The ``message`` field must itself be a JSON-encoded annotation payload
    with ``schema_version == "v1"``.

    Args:
        ntfy_raw: Raw dict decoded from the ntfy polling endpoint.

    Returns:
        The parsed annotation dict on success, or ``None`` if the message
        body is missing, not valid JSON, or has a mismatched schema version.
    """
    try:
        msg_body = ntfy_raw.get("message", "")
        if not msg_body:
            return None
        data = json.loads(msg_body)
        if not isinstance(data, dict):
            return None
        if data.get("schema_version") != SCHEMA_VERSION:
            return None
        return data
    except (json.JSONDecodeError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(annotation: dict) -> tuple[bool, str | None]:
    """Validate an annotation dict against schema v1.

    Checks:
        * all required fields present,
        * ``color`` in the allowed enum,
        * ``schema_version`` matches,
        * ``para_id`` is a positive int,
        * ``selection_end > selection_start``,
        * ``selected_text`` and ``comment`` within length limits.

    Args:
        annotation: Annotation dict to validate.

    Returns:
        Tuple ``(is_valid, error_message)``. ``error_message`` is ``None``
        when the annotation is valid.
    """
    for field in _REQUIRED_FIELDS:
        if field not in annotation:
            return False, f"missing field: {field}"

    if annotation["color"] not in VALID_COLORS:
        return False, f"invalid color: {annotation['color']}"

    if annotation["schema_version"] != SCHEMA_VERSION:
        return False, (
            f"schema version mismatch: {annotation['schema_version']}"
        )

    if (
        not isinstance(annotation["para_id"], int)
        or isinstance(annotation["para_id"], bool)
        or annotation["para_id"] < 1
    ):
        return False, "para_id must be positive integer"

    if annotation["selection_end"] <= annotation["selection_start"]:
        return False, "selection_end must be > selection_start"

    if len(annotation["selected_text"]) > MAX_SELECTED_LEN:
        return False, f"selected_text > {MAX_SELECTED_LEN} chars"

    if len(annotation["comment"]) > MAX_COMMENT_LEN:
        return False, f"comment > {MAX_COMMENT_LEN} chars"

    return True, None


# ---------------------------------------------------------------------------
# Dedupe
# ---------------------------------------------------------------------------


def dedupe(items: list[dict]) -> list[dict]:
    """Remove duplicate annotations by ``annotation_id``.

    The first occurrence of each ``annotation_id`` is kept; subsequent
    duplicates are dropped. Items without an ``annotation_id`` are skipped
    entirely (they should have been filtered out by :func:`validate`).

    Args:
        items: List of annotation dicts, possibly containing duplicates.

    Returns:
        Deduplicated list in original arrival order.
    """
    seen: set[str] = set()
    result: list[dict] = []
    for item in items:
        aid = item.get("annotation_id")
        if aid and aid not in seen:
            seen.add(aid)
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# Lifecycle stamps
# ---------------------------------------------------------------------------


def _now_iso_z() -> str:
    """Return the current UTC time as an ISO-8601 string ending in ``Z``."""
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def mark_received(annotation: dict) -> dict:
    """Stamp an annotation as received by the pipeline.

    Adds ``received_at`` (ISO-8601 UTC, trailing ``Z``) and ``processed =
    False``. Does not mutate the input dict.

    Args:
        annotation: Annotation dict.

    Returns:
        A shallow copy with the lifecycle fields added.
    """
    annotation = dict(annotation)
    annotation["received_at"] = _now_iso_z()
    annotation["processed"] = False
    return annotation


def mark_processed(
    annotation: dict,
    w14_run_id: str,
    edit_applied: bool,
) -> dict:
    """Stamp an annotation as processed by w14.

    Adds ``processed = True``, ``processed_at``, ``w14_run_id`` and
    ``edit_applied``. Does not mutate the input dict.

    Args:
        annotation: Annotation dict.
        w14_run_id: Identifier of the ``w14_annotation_applier`` run that
            handled this annotation.
        edit_applied: ``True`` if w14 actually modified the manuscript as
            a result of this annotation, ``False`` otherwise.

    Returns:
        A shallow copy with the lifecycle fields added.
    """
    annotation = dict(annotation)
    annotation["processed"] = True
    annotation["processed_at"] = _now_iso_z()
    annotation["w14_run_id"] = w14_run_id
    annotation["edit_applied"] = edit_applied
    return annotation


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    sample: dict[str, Any] = {
        "annotation_id": "test-001",
        "para_id": 12,
        "selection_start": 0,
        "selection_end": 50,
        "selected_text": "HCPS incidence 1.21/100k hab-year",
        "color": "yellow",
        "comment": "verificar que este numero es correcto",
        "ts": "2026-04-11T13:00:00Z",
        "schema_version": "v1",
    }
    ok, err = validate(sample)
    print(f"validate: {ok}, {err}")
    print(f"mark_received: {mark_received(sample)}")
