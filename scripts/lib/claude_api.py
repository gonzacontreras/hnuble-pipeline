"""Claude API wrapper with retry, model selection, usage tracking.

Models:
- call_sonnet (claude-sonnet-4-5) -> W1, W3, W5, W9, W10 (default workhorse)
- call_haiku (claude-haiku-4-5) -> W7 (cheap retraction scoring)
- call_opus (claude-opus-4-5) -> emergency only

Note: model IDs are pinned explicitly. Update here if Anthropic rotates model aliases.
"""

from __future__ import annotations

import os
import time
import json
from typing import Optional

import httpx

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"

# Pinned model IDs (2026-04 stable). Update if necessary.
MODEL_SONNET = os.environ.get("CLAUDE_MODEL_SONNET", "claude-sonnet-4-5")
MODEL_HAIKU = os.environ.get("CLAUDE_MODEL_HAIKU", "claude-haiku-4-5")
MODEL_OPUS = os.environ.get("CLAUDE_MODEL_OPUS", "claude-opus-4-5")


class ClaudeAPIError(RuntimeError):
    pass


def _get_key() -> str:
    key = os.environ.get("CLAUDE_API_KEY")
    if not key:
        raise ClaudeAPIError("CLAUDE_API_KEY env var missing")
    return key


def _call(
    model: str,
    prompt: str,
    max_tokens: int,
    system: Optional[str] = None,
    max_retries: int = 4,
) -> dict:
    """Low-level call with exponential backoff on 429/5xx."""
    headers = {
        "x-api-key": _get_key(),
        "anthropic-version": API_VERSION,
        "content-type": "application/json",
    }
    body: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        body["system"] = system

    delay = 2.0
    last_err: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=180.0) as client:
                r = client.post(API_URL, headers=headers, json=body)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                last_err = ClaudeAPIError(f"HTTP {r.status_code}: {r.text[:300]}")
                time.sleep(delay)
                delay *= 2
                continue
            raise ClaudeAPIError(f"HTTP {r.status_code}: {r.text[:500]}")
        except httpx.HTTPError as exc:
            last_err = exc
            time.sleep(delay)
            delay *= 2
    raise ClaudeAPIError(f"Exhausted retries: {last_err}")


def _extract_text(resp: dict) -> str:
    chunks = resp.get("content", [])
    return "".join(c.get("text", "") for c in chunks if c.get("type") == "text")


def _log_usage(model: str, resp: dict) -> None:
    usage = resp.get("usage", {})
    print(
        f"[claude_api] model={model} "
        f"in={usage.get('input_tokens', 0)} out={usage.get('output_tokens', 0)}",
        flush=True,
    )


def call_sonnet(
    prompt: str, max_tokens: int = 4000, system: Optional[str] = None
) -> str:
    resp = _call(MODEL_SONNET, prompt, max_tokens, system)
    _log_usage(MODEL_SONNET, resp)
    return _extract_text(resp)


def call_haiku(
    prompt: str, max_tokens: int = 400, system: Optional[str] = None
) -> str:
    resp = _call(MODEL_HAIKU, prompt, max_tokens, system)
    _log_usage(MODEL_HAIKU, resp)
    return _extract_text(resp)


def call_opus(
    prompt: str, max_tokens: int = 8000, system: Optional[str] = None
) -> str:
    resp = _call(MODEL_OPUS, prompt, max_tokens, system)
    _log_usage(MODEL_OPUS, resp)
    return _extract_text(resp)


def extract_json(text: str) -> Optional[dict]:
    """Best-effort JSON extraction from Claude response (handles ```json ... ``` fences)."""
    text = text.strip()
    if text.startswith("```"):
        # strip first fence line
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    # try direct
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # try to find first balanced { } block
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None
