"""Git helpers to commit state from GitHub Actions.

Designed to be safe no-ops when run locally without git config set.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=check
    )


def ensure_git_identity() -> None:
    """Configure git identity if running in GitHub Actions without one."""
    try:
        _run(["git", "config", "user.name"], check=True)
    except subprocess.CalledProcessError:
        _run(["git", "config", "user.name", "hnuble-bot"], check=False)
    try:
        _run(["git", "config", "user.email"], check=True)
    except subprocess.CalledProcessError:
        _run(["git", "config", "user.email", "bot@hnuble.io"], check=False)


def commit_state(files: Iterable[str], message: str) -> bool:
    """Stage + commit + push given files. Returns True if a commit was created."""
    ensure_git_identity()
    add_list = [str(f) for f in files]
    if not add_list:
        return False
    _run(["git", "add", *add_list], check=False)
    # Check if there's anything staged
    status = _run(["git", "status", "--porcelain"], check=False)
    if not status.stdout.strip():
        return False
    _run(["git", "commit", "-m", message], check=False)
    # Push only if a remote exists and we're in a CI context
    if os.environ.get("GITHUB_ACTIONS"):
        _run(["git", "push"], check=False)
    return True
