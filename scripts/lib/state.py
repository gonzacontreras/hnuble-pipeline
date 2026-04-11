"""Atomic JSON state file load/save."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "state"


def _path(name: str) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / name


def load_json(name: str, default: Any) -> Any:
    p = _path(name)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(name: str, data: Any) -> Path:
    """Atomic write: tmp then replace."""
    p = _path(name)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=STATE_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)
        os.replace(tmp_path, p)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return p


# Convenience wrappers for known state files
def load_findings() -> dict:
    return load_json("findings.json", {"items": [], "version": 0})


def save_findings(data: dict) -> Path:
    return save_json("findings.json", data)


def load_references() -> dict:
    return load_json("references.json", {"items": []})


def save_references(data: dict) -> Path:
    return save_json("references.json", data)


def load_decisions() -> dict:
    return load_json("decisions.json", {"items": []})


def save_decisions(data: dict) -> Path:
    return save_json("decisions.json", data)


def load_objections() -> dict:
    return load_json("objections.json", {"items": []})


def save_objections(data: dict) -> Path:
    return save_json("objections.json", data)


def load_paper_candidates() -> dict:
    return load_json("paper_candidates.json", {"items": []})


def save_paper_candidates(data: dict) -> Path:
    return save_json("paper_candidates.json", data)


def load_stability_history() -> dict:
    return load_json("stability_history.json", {"runs": []})


def save_stability_history(data: dict) -> Path:
    return save_json("stability_history.json", data)


def load_pending_approvals() -> dict:
    return load_json("pending_approvals.json", {"items": []})


def save_pending_approvals(data: dict) -> Path:
    return save_json("pending_approvals.json", data)


def load_pipeline_status() -> dict:
    return load_json("pipeline_status.json", {"workflows": {}})


def save_pipeline_status(data: dict) -> Path:
    return save_json("pipeline_status.json", data)
