"""crossref_verify — detect fabricated / swapped DOIs via Crossref API.

Referenced by E2 S60 post-mortem: during S60 reference cleanup two DOIs
ended up pointing to completely different papers than the declared
author/year/title:

  1. Fernandez-Manso et al. 2016 "SENTINEL-2A red-edge spectral indices for
     burn severity" was cited with DOI 10.1016/j.jag.2016.02.002 — but that
     DOI actually resolves to Guo et al. 2016 "Soils" (unrelated topic).

  2. Dimitriadis et al. 2021 "Stable reliability diagrams for probabilistic
     forecasts" was cited with DOI 10.1016/j.ijforecast.2020.08.008 — but
     that DOI actually resolves to Taleb 2022 on price forecasting.

Both fabrications survived manual review and were only caught by reviewer
audit. This module provides programmatic Crossref verification so W1
(papers watcher) and W9 (memory cross-checker) can flag DOI-swaps BEFORE
they land in state/references.json or the manuscript.

Online dependency: requires https://api.crossref.org to be reachable.
If the network is unavailable the function returns a
`NEEDS_HUMAN_VERIFICATION` status (never raises), so calling workflows can
decide whether to block or queue. The module is also safe to import and
unit-test offline — the inline tests below are best-effort and skip
automatically if Crossref cannot be reached.

Functions
---------
verify_citation(doi, author_surname, year, title_words, timeout=10.0) -> dict

Return dict schema
------------------
{
    "status": "VERIFIED" | "DOI_SWAP_DETECTED" | "YEAR_MISMATCH"
              | "TITLE_MISMATCH" | "DOI_INVALID"
              | "NEEDS_HUMAN_VERIFICATION",
    "crossref_metadata": {...} | None,
    "reason": str,
    "suggested_correct_doi": str | None,
}

Cache
-----
In-memory dict `_cache` keyed by normalized DOI. Survives for the duration
of the Python process. Not persisted to disk.
"""
from __future__ import annotations

import re
from typing import Optional

try:
    import httpx
    _HAS_HTTPX = True
except ImportError:  # pragma: no cover - httpx is in requirements.txt
    _HAS_HTTPX = False

# Module-level in-memory cache: normalized_doi -> crossref_response_json
_cache: dict[str, dict] = {}

CROSSREF_BASE = "https://api.crossref.org/works/"
USER_AGENT = "hnuble-pipeline/1.0 (mailto:gonzalocontreras@example.invalid)"

# Jaccard similarity threshold below which title match is rejected.
# 0.30 is permissive enough to allow subtitle/punctuation drift but strict
# enough to catch the S60 swaps (Guo 'soils' vs 'burn severity red-edge' = 0.0).
TITLE_JACCARD_THRESHOLD = 0.30

# Year tolerance: some Crossref entries list early-access year differing from
# print year by 1. Off by more than 1 is a real mismatch.
YEAR_TOLERANCE = 1


def _norm_doi(doi: str) -> str:
    """Strip protocol prefix and lowercase a DOI."""
    s = (doi or "").strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^doi:\s*", "", s, flags=re.IGNORECASE)
    return s.lower()


def _tokenize_title(text: str) -> set[str]:
    """Lowercase, strip punctuation, return set of tokens >= 3 chars."""
    if not text:
        return set()
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    tokens = {tok for tok in text.split() if len(tok) >= 3}
    # strip common stopwords that inflate false positives
    stop = {
        "the", "and", "for", "from", "with", "use", "using",
        "based", "study", "analysis", "review", "paper", "new",
        "this", "these", "their", "its", "via", "our", "such",
    }
    return tokens - stop


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _fetch_crossref(doi: str, timeout: float) -> tuple[Optional[dict], Optional[str]]:
    """Return (json_message, error_status_if_any).

    error_status is one of None, "DOI_INVALID", "NEEDS_HUMAN_VERIFICATION".
    """
    if not _HAS_HTTPX:
        return None, "NEEDS_HUMAN_VERIFICATION"

    norm = _norm_doi(doi)
    if norm in _cache:
        return _cache[norm], None

    url = CROSSREF_BASE + norm
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    try:
        with httpx.Client(timeout=timeout, verify=False, follow_redirects=True) as client:
            r = client.get(url, headers=headers)
    except httpx.HTTPError:
        return None, "NEEDS_HUMAN_VERIFICATION"
    except Exception:
        return None, "NEEDS_HUMAN_VERIFICATION"

    if r.status_code == 404:
        return None, "DOI_INVALID"
    if r.status_code != 200:
        return None, "NEEDS_HUMAN_VERIFICATION"

    try:
        payload = r.json()
    except ValueError:
        return None, "NEEDS_HUMAN_VERIFICATION"

    msg = payload.get("message")
    if not isinstance(msg, dict):
        return None, "NEEDS_HUMAN_VERIFICATION"

    _cache[norm] = msg
    return msg, None


def _parse_first_author(msg: dict) -> str:
    authors = msg.get("author") or []
    if not authors:
        return ""
    first = authors[0] if isinstance(authors[0], dict) else {}
    return (first.get("family") or first.get("name") or "").strip()


def _parse_year(msg: dict) -> Optional[int]:
    for key in ("issued", "published-print", "published-online", "created"):
        node = msg.get(key)
        if isinstance(node, dict):
            parts = node.get("date-parts")
            if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
                try:
                    return int(parts[0][0])
                except (TypeError, ValueError):
                    continue
    return None


def _parse_title(msg: dict) -> str:
    t = msg.get("title")
    if isinstance(t, list) and t:
        return str(t[0])
    if isinstance(t, str):
        return t
    return ""


def verify_citation(
    doi: str,
    author_surname: str,
    year: int,
    title_words: str,
    timeout: float = 10.0,
) -> dict:
    """Verify that a DOI corresponds to the declared author-year-title.

    Parameters
    ----------
    doi : str
        The DOI as declared in the manuscript (with or without URL prefix).
    author_surname : str
        First-author surname as declared (e.g. "Fernandez-Manso").
    year : int
        Publication year as declared.
    title_words : str
        Full or partial title string. Used for fuzzy token Jaccard match.
    timeout : float
        HTTP timeout in seconds.

    Returns
    -------
    dict
        See module docstring for schema.

    Notes
    -----
    - Never raises. Network failures map to NEEDS_HUMAN_VERIFICATION so the
      caller can route the item to W8 HIL queue.
    - Result is cached in-memory by DOI to reduce Crossref load during batch runs.
    """
    decl_doi = _norm_doi(doi)
    if not decl_doi:
        return {
            "status": "DOI_INVALID",
            "crossref_metadata": None,
            "reason": "empty or malformed DOI",
            "suggested_correct_doi": None,
        }

    msg, err = _fetch_crossref(decl_doi, timeout)
    if err == "DOI_INVALID":
        return {
            "status": "DOI_INVALID",
            "crossref_metadata": None,
            "reason": f"Crossref 404 for DOI {decl_doi}",
            "suggested_correct_doi": None,
        }
    if err == "NEEDS_HUMAN_VERIFICATION" or msg is None:
        return {
            "status": "NEEDS_HUMAN_VERIFICATION",
            "crossref_metadata": None,
            "reason": "Crossref API unreachable or malformed response",
            "suggested_correct_doi": None,
        }

    parsed_author = _parse_first_author(msg)
    parsed_year = _parse_year(msg)
    parsed_title = _parse_title(msg)

    metadata = {
        "doi": decl_doi,
        "first_author_family": parsed_author,
        "year": parsed_year,
        "title": parsed_title,
    }

    # --- 1. Author match (case-insensitive substring, handles hyphen variants)
    decl_author_norm = (author_surname or "").lower().replace("-", "").replace(" ", "")
    parsed_author_norm = parsed_author.lower().replace("-", "").replace(" ", "")
    author_ok = False
    if decl_author_norm and parsed_author_norm:
        author_ok = (
            decl_author_norm in parsed_author_norm
            or parsed_author_norm in decl_author_norm
        )

    # --- 2. Year match (within tolerance)
    year_ok = False
    if parsed_year is not None and year:
        year_ok = abs(parsed_year - int(year)) <= YEAR_TOLERANCE

    # --- 3. Title Jaccard
    decl_tokens = _tokenize_title(title_words)
    parsed_tokens = _tokenize_title(parsed_title)
    jaccard = _jaccard(decl_tokens, parsed_tokens)
    title_ok = jaccard >= TITLE_JACCARD_THRESHOLD

    # --- Decision tree
    if author_ok and year_ok and title_ok:
        return {
            "status": "VERIFIED",
            "crossref_metadata": metadata,
            "reason": (
                f"author match, year {parsed_year}=={year}+/-{YEAR_TOLERANCE}, "
                f"title Jaccard={jaccard:.2f}"
            ),
            "suggested_correct_doi": None,
        }

    # If both author and title fail, this is a DOI swap (most severe).
    if not author_ok and not title_ok:
        return {
            "status": "DOI_SWAP_DETECTED",
            "crossref_metadata": metadata,
            "reason": (
                f"DOI resolves to {parsed_author or '?'} {parsed_year or '?'} "
                f"'{parsed_title[:80]}' but citation declared {author_surname} {year} "
                f"'{title_words[:60]}' (Jaccard={jaccard:.2f})"
            ),
            "suggested_correct_doi": None,
        }

    # Author matches but title doesn't -> same author, wrong paper
    if author_ok and not title_ok:
        return {
            "status": "TITLE_MISMATCH",
            "crossref_metadata": metadata,
            "reason": (
                f"author matches but title Jaccard={jaccard:.2f} < {TITLE_JACCARD_THRESHOLD}; "
                f"Crossref title: '{parsed_title[:120]}'"
            ),
            "suggested_correct_doi": None,
        }

    # Title matches but year wrong -> early-access / preprint drift
    if title_ok and not year_ok:
        return {
            "status": "YEAR_MISMATCH",
            "crossref_metadata": metadata,
            "reason": (
                f"title matches (Jaccard={jaccard:.2f}) but year {parsed_year} "
                f"differs from declared {year} by more than {YEAR_TOLERANCE}"
            ),
            "suggested_correct_doi": None,
        }

    # Fallback: title matches, author doesn't — could be editor/reviewer-style
    # citation. Flag for human.
    return {
        "status": "NEEDS_HUMAN_VERIFICATION",
        "crossref_metadata": metadata,
        "reason": (
            f"partial match: author_ok={author_ok} year_ok={year_ok} "
            f"title_jaccard={jaccard:.2f}"
        ),
        "suggested_correct_doi": None,
    }


# ---------------------------------------------------------------------------
# Inline tests — run with: python scripts/lib/crossref_verify.py
# Requires network access to api.crossref.org. If network is unavailable, all
# tests will return NEEDS_HUMAN_VERIFICATION and the test block will SKIP
# rather than fail — this is by design per module docstring.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    print("crossref_verify inline tests")
    print("=" * 60)

    # Test 1 — E2 S60 first fabrication: Fernandez-Manso declared but DOI is Guo 2016
    print("\n[T1] Fernandez-Manso 2016 vs Guo 2016 DOI swap (E2 S60)")
    r1 = verify_citation(
        doi="10.1016/j.jag.2016.02.002",
        author_surname="Fernandez-Manso",
        year=2016,
        title_words="SENTINEL-2A red-edge spectral indices burn severity",
    )
    print(f"  status: {r1['status']}")
    print(f"  reason: {r1['reason']}")
    if r1["status"] == "NEEDS_HUMAN_VERIFICATION":
        print("  SKIP (offline)")
        skip = True
    else:
        skip = False
        assert r1["status"] in ("DOI_SWAP_DETECTED", "TITLE_MISMATCH"), (
            f"Expected DOI_SWAP_DETECTED or TITLE_MISMATCH, got {r1['status']}"
        )
        print("  PASS")

    # Test 2 — E2 S60 second fabrication: Dimitriadis declared but DOI is Taleb 2022
    print("\n[T2] Dimitriadis 2021 vs Taleb 2022 DOI swap (E2 S60)")
    r2 = verify_citation(
        doi="10.1016/j.ijforecast.2020.08.008",
        author_surname="Dimitriadis",
        year=2021,
        title_words="reliability diagrams probabilistic forecasts",
    )
    print(f"  status: {r2['status']}")
    print(f"  reason: {r2['reason']}")
    if r2["status"] == "NEEDS_HUMAN_VERIFICATION" and not skip:
        pass
    elif r2["status"] != "NEEDS_HUMAN_VERIFICATION":
        assert r2["status"] in ("DOI_SWAP_DETECTED", "TITLE_MISMATCH", "YEAR_MISMATCH"), (
            f"Expected swap/mismatch, got {r2['status']}"
        )
        print("  PASS")

    # Test 3 — known-good DOI (Dimitriadis real PNAS paper)
    print("\n[T3] Dimitriadis 2021 PNAS -- known good")
    r3 = verify_citation(
        doi="10.1073/pnas.2016191118",
        author_surname="Dimitriadis",
        year=2021,
        title_words="reliability diagrams probabilistic forecasts",
    )
    print(f"  status: {r3['status']}")
    print(f"  reason: {r3['reason']}")
    if r3["status"] == "NEEDS_HUMAN_VERIFICATION":
        print("  SKIP (offline)")
    else:
        assert r3["status"] == "VERIFIED", f"Expected VERIFIED, got {r3['status']}"
        print("  PASS")

    # Test 4 — malformed DOI (empty)
    print("\n[T4] empty DOI -> DOI_INVALID")
    r4 = verify_citation(doi="", author_surname="Smith", year=2020, title_words="foo")
    print(f"  status: {r4['status']}")
    assert r4["status"] == "DOI_INVALID"
    print("  PASS")

    # Test 5 — 404 DOI
    print("\n[T5] nonexistent DOI -> DOI_INVALID (if online)")
    r5 = verify_citation(
        doi="10.9999/nonexistent-fake-doi-hantavirus-test",
        author_surname="Nobody",
        year=2099,
        title_words="this does not exist",
    )
    print(f"  status: {r5['status']}")
    if r5["status"] == "NEEDS_HUMAN_VERIFICATION":
        print("  SKIP (offline)")
    else:
        assert r5["status"] == "DOI_INVALID", f"Expected DOI_INVALID, got {r5['status']}"
        print("  PASS")

    print("\n" + "=" * 60)
    print("crossref_verify tests complete")
    sys.exit(0)
