"""Memory + vault search for V1 MCC.

When running on GitHub Actions, memory/ and obsidian_vault/ are not available by
default. The W9 script supports two modes:

1. Bundled-excerpts mode (default for CI): state/memory_bundle.json contains
   key verbatim excerpts from memory/ and obsidian_vault/ pre-extracted locally
   and committed. grep_* helpers read from this bundle.

2. Local mode: set HNUBLE_PROJECT_ROOT to a filesystem path with memory/ and
   obsidian_vault/ subdirs. Helpers then grep the live filesystem.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterable

from . import state as state_lib

BUNDLE_NAME = "memory_bundle.json"


def _load_bundle() -> dict:
    return state_lib.load_json(BUNDLE_NAME, {"memory": [], "vault": [], "audit": []})


def _local_root() -> Path | None:
    root = os.environ.get("HNUBLE_PROJECT_ROOT")
    return Path(root) if root and Path(root).exists() else None


def _grep_files(root: Path, keywords: Iterable[str], max_hits: int = 30) -> list[dict]:
    hits: list[dict] = []
    patterns = [re.compile(re.escape(k), re.IGNORECASE) for k in keywords]
    if not patterns:
        return hits
    for path in root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if any(p.search(line) for p in patterns):
                lo, hi = max(0, i - 3), min(len(lines), i + 4)
                hits.append(
                    {
                        "file": str(path.relative_to(root)),
                        "line": i + 1,
                        "snippet": "\n".join(lines[lo:hi]),
                    }
                )
                if len(hits) >= max_hits:
                    return hits
                break
    return hits


def _grep_bundle(section: str, keywords: Iterable[str], max_hits: int = 30) -> list[dict]:
    bundle = _load_bundle()
    items = bundle.get(section, [])
    patterns = [re.compile(re.escape(k), re.IGNORECASE) for k in keywords]
    hits: list[dict] = []
    for item in items:
        text = item.get("text", "") if isinstance(item, dict) else str(item)
        if any(p.search(text) for p in patterns):
            hits.append(item if isinstance(item, dict) else {"text": text})
            if len(hits) >= max_hits:
                break
    return hits


def grep_memory(keywords: Iterable[str]) -> list[dict]:
    local = _local_root()
    if local:
        mem_dir = local / "memory"
        if mem_dir.exists():
            return _grep_files(mem_dir, keywords)
    return _grep_bundle("memory", keywords)


def grep_vault(keywords: Iterable[str]) -> list[dict]:
    local = _local_root()
    if local:
        vault_dir = local / "obsidian_vault"
        if vault_dir.exists():
            return _grep_files(vault_dir, keywords)
    return _grep_bundle("vault", keywords)


def grep_audit_findings(keywords: Iterable[str]) -> list[dict]:
    local = _local_root()
    if local:
        # common audit file locations
        candidates = [
            local / "audit_findings.md",
            local / "submission" / "audit_findings.md",
            local / "04_sesgos_vacios.md",
        ]
        for c in candidates:
            if c.exists():
                patterns = [re.compile(re.escape(k), re.IGNORECASE) for k in keywords]
                try:
                    text = c.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                lines = text.splitlines()
                hits: list[dict] = []
                for i, line in enumerate(lines):
                    if any(p.search(line) for p in patterns):
                        lo, hi = max(0, i - 3), min(len(lines), i + 4)
                        hits.append(
                            {
                                "file": c.name,
                                "line": i + 1,
                                "snippet": "\n".join(lines[lo:hi]),
                            }
                        )
                        if len(hits) >= 20:
                            break
                if hits:
                    return hits
    return _grep_bundle("audit", keywords)
