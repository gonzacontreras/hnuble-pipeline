"""Claude Live heartbeat helper.

Thin helper layer over ``state/claude_live.json`` used by the main Claude Code
instance (manual heartbeats during pipeline construction) and by future workers
W11/W12/W13/W14 to report progress. The ``docs/live.html`` dashboard polls the
written JSON every ~3s via fetch.

All reads/writes go through :mod:`scripts.lib.state` so the atomic
``save_json`` semantics (tmp file + ``os.replace``) are preserved.

Schema contract (mirrored by ``state/schemas/claude_live.schema.json``):

- ``version`` (int): schema version.
- ``heartbeat_sequence`` (int): monotonic, auto-incremented.
- ``updated_at`` (str): ISO-8601 UTC, ``Z`` suffix.
- ``session`` (str): session code, e.g. ``"S61"``.
- ``session_deadline`` (str): ISO-8601 UTC.
- ``current_block`` / ``current_block_label`` (str).
- ``overall_status`` (enum): ``running | idle | blocked | done | error``.
- ``agent`` / ``methodology`` (str).
- ``sub_blocks`` (list[dict]): each has ``id``, ``label``, ``status``,
  ``agent_type``, optional ``output_path`` / ``output_refs`` /
  ``error_message`` / ``traceback`` / ``duration_s`` / ``detail``.
- ``current_findings`` (list[str]).
- ``next_planned`` (list[str]).
- ``tool_calls_total`` (int).
- ``files_touched`` (list[str]).
- ``eta_estimate`` (dict): ``optimistic_wall_time_min``,
  ``pessimistic_wall_time_min``, ``current_block_eta_min``.
- ``m14_preflight`` (dict): ``catalog_consulted``, ``catalog_path``,
  ``findings_classified``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from scripts.lib.state import load_json, save_json

STATE_FILE = "claude_live.json"


def _now_iso_z() -> str:
    """Return current UTC time as ISO-8601 with trailing ``Z``.

    Returns:
        Timestamp string compatible with the dashboard fetch contract,
        e.g. ``"2026-04-11T13:31:54Z"``.
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def _skeleton() -> dict[str, Any]:
    """Return the initial skeleton used when ``claude_live.json`` is absent.

    Returns:
        A fresh state dict with ``heartbeat_sequence=0`` and ``overall_status='idle'``.
        Caller is expected to mutate and persist it via the public helpers.
    """
    return {
        "version": 1,
        "heartbeat_sequence": 0,
        "updated_at": "1970-01-01T00:00:00Z",
        "session": "S61",
        "session_deadline": "2026-04-14T06:00:00Z",
        "current_block": "none",
        "current_block_label": "idle",
        "overall_status": "idle",
        "agent": "Claude Code",
        "methodology": "5-fase anti-bypass + M14",
        "sub_blocks": [],
        "current_findings": [],
        "next_planned": [],
        "tool_calls_total": 0,
        "files_touched": [],
        "eta_estimate": {
            "optimistic_wall_time_min": 0,
            "pessimistic_wall_time_min": 0,
            "current_block_eta_min": 0,
        },
        "m14_preflight": {
            "catalog_consulted": False,
            "catalog_path": "memory/CANONICAL_BLINDAJES_INDEX.md",
            "findings_classified": False,
        },
    }


def _load_state() -> dict[str, Any]:
    """Load ``claude_live.json`` or a fresh skeleton if missing.

    Returns:
        The current persisted state dict, or :func:`_skeleton` output when the
        file does not exist.
    """
    return load_json(STATE_FILE, _skeleton())


def _write_state(data: dict[str, Any]) -> dict[str, Any]:
    """Persist ``data`` atomically and return it.

    Args:
        data: The full state dict to write.

    Returns:
        The same dict that was written (for chaining).
    """
    save_json(STATE_FILE, data)
    return data


def _find_sub_block(
    data: dict[str, Any], sub_block_id: str
) -> Optional[dict[str, Any]]:
    """Locate a sub-block by id within ``data['sub_blocks']``.

    Args:
        data: Current state dict.
        sub_block_id: Target sub-block id, e.g. ``"B2.1"``.

    Returns:
        The mutable sub-block dict, or ``None`` if not found.
    """
    for sb in data.get("sub_blocks", []):
        if sb.get("id") == sub_block_id:
            return sb
    return None


def _dedupe_append(target: list[str], items: list[str]) -> None:
    """Append items to ``target`` skipping exact-string duplicates.

    Args:
        target: List mutated in place.
        items: Candidate strings to add.
    """
    seen = set(target)
    for it in items:
        if it not in seen:
            target.append(it)
            seen.add(it)


def heartbeat(
    block_id: str,
    sub_block_id: Optional[str] = None,
    status: str = "running",
    detail: Optional[str] = None,
    findings: Optional[list[str]] = None,
    next_planned: Optional[list[str]] = None,
    files_touched_add: Optional[list[str]] = None,
    tool_calls_delta: int = 1,
) -> dict[str, Any]:
    """Write a progress heartbeat to ``state/claude_live.json``.

    Increments ``heartbeat_sequence`` and ``tool_calls_total``, refreshes
    ``updated_at``, optionally updates a sub-block's status/detail and appends
    new findings / next-planned / files-touched entries with simple dedupe.

    Args:
        block_id: Current top-level block id (e.g. ``"B2"``). Written to
            ``current_block`` when it changes.
        sub_block_id: Optional sub-block id (e.g. ``"B2.1"``). If provided and
            found, its ``status`` is updated and ``detail`` is attached.
        status: New status for the sub-block. Enum-free at this layer, but
            downstream consumers expect ``pending | dispatched | running |
            done | error | blocked``.
        detail: Free-form note appended to the sub-block.
        findings: Strings to append to ``current_findings`` (dedupe by value).
        next_planned: Replaces ``next_planned`` entirely when provided.
        files_touched_add: Paths to extend ``files_touched`` with (dedupe).
        tool_calls_delta: Amount to add to ``tool_calls_total``. Default 1.

    Returns:
        The full state dict that was persisted.
    """
    data = _load_state()

    data["heartbeat_sequence"] = int(data.get("heartbeat_sequence", 0)) + 1
    data["updated_at"] = _now_iso_z()

    if data.get("current_block") != block_id:
        data["current_block"] = block_id

    if sub_block_id is not None:
        sb = _find_sub_block(data, sub_block_id)
        if sb is not None:
            sb["status"] = status
            if detail is not None:
                sb["detail"] = detail

    if findings:
        _dedupe_append(data.setdefault("current_findings", []), findings)

    if next_planned is not None:
        data["next_planned"] = list(next_planned)

    if files_touched_add:
        _dedupe_append(data.setdefault("files_touched", []), files_touched_add)

    data["tool_calls_total"] = int(data.get("tool_calls_total", 0)) + int(
        tool_calls_delta
    )

    return _write_state(data)


def start_block(
    block_id: str,
    block_label: str,
    sub_blocks: list[dict[str, Any]],
    eta_min: Optional[int] = None,
) -> dict[str, Any]:
    """Begin a new top-level block, replacing the sub-block roster.

    Args:
        block_id: New ``current_block`` id (e.g. ``"B2"``).
        block_label: Human-readable label for the block.
        sub_blocks: Complete list of sub-blocks for this block. Each entry
            missing a ``status`` is defaulted to ``"pending"``.
        eta_min: Optional ETA in minutes; written to
            ``eta_estimate.current_block_eta_min`` when provided.

    Returns:
        The persisted state dict.
    """
    data = _load_state()

    data["current_block"] = block_id
    data["current_block_label"] = block_label
    data["overall_status"] = "running"

    normalized: list[dict[str, Any]] = []
    for sb in sub_blocks:
        entry = dict(sb)
        entry.setdefault("status", "pending")
        normalized.append(entry)
    data["sub_blocks"] = normalized

    if eta_min is not None:
        eta = data.setdefault(
            "eta_estimate",
            {
                "optimistic_wall_time_min": 0,
                "pessimistic_wall_time_min": 0,
                "current_block_eta_min": 0,
            },
        )
        eta["current_block_eta_min"] = int(eta_min)

    data["heartbeat_sequence"] = int(data.get("heartbeat_sequence", 0)) + 1
    data["updated_at"] = _now_iso_z()

    return _write_state(data)


def finalize(
    block_id: str,
    output_refs: list[str],
    sub_block_id: Optional[str] = None,
    duration_s: Optional[float] = None,
) -> dict[str, Any]:
    """Mark a sub-block as ``done`` and attach its outputs.

    Args:
        block_id: The block id the sub-block belongs to. Used for logging and
            to guard the "all sub-blocks done" roll-up check.
        output_refs: List of output paths/URLs produced by the sub-block.
        sub_block_id: Sub-block to mark ``done``. If omitted, the first
            non-done sub-block belonging to ``block_id`` is used as a best
            effort, preserving ergonomics for callers that only track one
            sub-block at a time.
        duration_s: Optional wall-time in seconds attached to the sub-block.

    Returns:
        The persisted state dict. When every sub-block is ``done``,
        ``overall_status`` is set to ``"done"``. The caller is responsible for
        choosing the next ``current_block``.
    """
    data = _load_state()

    target: Optional[dict[str, Any]] = None
    if sub_block_id is not None:
        target = _find_sub_block(data, sub_block_id)
    if target is None:
        for sb in data.get("sub_blocks", []):
            if sb.get("status") != "done":
                target = sb
                break

    if target is not None:
        target["status"] = "done"
        target["output_refs"] = list(output_refs)
        if duration_s is not None:
            target["duration_s"] = float(duration_s)

    all_done = bool(data.get("sub_blocks")) and all(
        sb.get("status") == "done" for sb in data.get("sub_blocks", [])
    )
    if all_done:
        data["overall_status"] = "done"

    data["heartbeat_sequence"] = int(data.get("heartbeat_sequence", 0)) + 1
    data["updated_at"] = _now_iso_z()

    return _write_state(data)


def error(
    block_id: str,
    sub_block_id: str,
    error_message: str,
    traceback_str: Optional[str] = None,
) -> dict[str, Any]:
    """Mark a sub-block as failed and flip ``overall_status`` to ``"error"``.

    Args:
        block_id: The parent block id (used for the finding label).
        sub_block_id: Sub-block to mark ``error``.
        error_message: Short message stored on the sub-block and mirrored
            (truncated to 150 chars) into ``current_findings``.
        traceback_str: Optional full traceback attached to the sub-block.

    Returns:
        The persisted state dict.
    """
    data = _load_state()

    sb = _find_sub_block(data, sub_block_id)
    if sb is not None:
        sb["status"] = "error"
        sb["error_message"] = error_message
        if traceback_str is not None:
            sb["traceback"] = traceback_str

    finding = f"ERROR in {sub_block_id}: {error_message[:150]}"
    _dedupe_append(data.setdefault("current_findings", []), [finding])

    data["overall_status"] = "error"
    data["heartbeat_sequence"] = int(data.get("heartbeat_sequence", 0)) + 1
    data["updated_at"] = _now_iso_z()

    return _write_state(data)


if __name__ == "__main__":
    # Smoke test: write a heartbeat for B0.1 and read it back.
    # NOTE: requires repo root on sys.path so that `scripts.lib.state` resolves.
    # If invoked directly as `python scripts/lib/claude_live.py`, add repo root
    # to sys.path before running. This block is for manual verification only.
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    written = heartbeat(
        "B0",
        sub_block_id="B0.1",
        status="running",
        detail="smoke test",
    )
    print(
        f"[claude_live smoke] heartbeat_sequence={written['heartbeat_sequence']} "
        f"current_block={written['current_block']} "
        f"updated_at={written['updated_at']}"
    )
    readback = _load_state()
    print(
        f"[claude_live smoke] readback_sequence={readback['heartbeat_sequence']} "
        f"tool_calls_total={readback['tool_calls_total']}"
    )
