"""text_cleanup — whitespace/unicode normalization for batch edits.

Referenced by E7 S60 post-mortem: during S60 manuscript condensation a batch
of string.replace() operations silently failed because the source manuscript
contained 61 NBSP (U+00A0) characters. Claude had produced the old_string
with a regular ASCII 0x20 space, so the replacements never matched and the
edit pipeline reported zero changes without surfacing the mismatch.

This module provides deterministic text preprocessing so that any workflow
that performs literal string replacement (W2 language polish, W9 MCC
auto-patch, W10 blindaje upgrader) first NFC-normalizes and strips
non-breaking/narrow whitespace to plain ASCII spaces.

Typical use::

    from lib.text_cleanup import preprocess_for_edit
    manuscript = preprocess_for_edit(manuscript_raw)
    # safe to do manuscript.replace(old, new) afterwards

Functions
---------
- strip_nbsp(text)         -> replaces NBSP, NNBSP, thin space, tab with space
- normalize_whitespace(text) -> collapses runs of whitespace to single space
                                (preserves newlines)
- nfc_normalize(text)      -> unicodedata.normalize("NFC", text)
- preprocess_for_edit(text) -> nfc -> strip_nbsp -> preserve newlines pipeline
"""
from __future__ import annotations

import unicodedata

# Characters that look like space but break str.replace / str.split
# U+00A0 NO-BREAK SPACE       (latin1, very common in Word/Google Docs exports)
# U+202F NARROW NO-BREAK SPACE (French thin spaces around punct)
# U+2009 THIN SPACE            (typographic)
# U+200A HAIR SPACE
# U+2007 FIGURE SPACE
# U+2008 PUNCTUATION SPACE
# U+205F MEDIUM MATHEMATICAL SPACE
# U+3000 IDEOGRAPHIC SPACE
# \t     TAB
_SPACE_LOOKALIKES = [
    "\u00a0",
    "\u202f",
    "\u2009",
    "\u200a",
    "\u2007",
    "\u2008",
    "\u205f",
    "\u3000",
    "\t",
]


def strip_nbsp(text: str) -> str:
    """Replace NBSP and other space-lookalike chars (incl. tab) with ASCII space.

    Does NOT touch newlines. This is the single operation that fixes E7 S60.
    """
    if not text:
        return text
    for ch in _SPACE_LOOKALIKES:
        if ch in text:
            text = text.replace(ch, " ")
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse runs of spaces/tabs to a single space, preserving newlines.

    Implementation: split on newline, collapse intra-line whitespace, rejoin.
    Leading/trailing whitespace on each line is stripped.
    """
    if not text:
        return text
    out_lines = []
    for line in text.split("\n"):
        # collapse any run of space/tab/NBSP/etc to single ASCII space
        collapsed = []
        prev_space = False
        for ch in line:
            if ch.isspace() and ch != "\n":
                if not prev_space:
                    collapsed.append(" ")
                prev_space = True
            else:
                collapsed.append(ch)
                prev_space = False
        out_lines.append("".join(collapsed).strip())
    return "\n".join(out_lines)


def nfc_normalize(text: str) -> str:
    """Apply Unicode NFC canonical composition.

    Important for combining accents: 'a' + COMBINING ACUTE (U+0301) becomes 'á'
    (U+00E1). Without NFC, copy/paste from PDFs can produce decomposed forms
    that break literal string matching.
    """
    if not text:
        return text
    return unicodedata.normalize("NFC", text)


def preprocess_for_edit(text: str) -> str:
    """Full preprocessing pipeline for batch str.replace safety.

    Steps:
      1. NFC-normalize (unicode canonical form)
      2. strip_nbsp (replace space-lookalikes with ASCII space, keep newlines)
      3. Preserve original newline structure (no collapsing of multi-line)

    This pipeline is idempotent: preprocess_for_edit(preprocess_for_edit(x)) == preprocess_for_edit(x).

    Use this BEFORE any str.replace() chain over a manuscript or prompt
    loaded from disk or received from Claude API.
    """
    if not text:
        return text
    text = nfc_normalize(text)
    text = strip_nbsp(text)
    return text


# ---------------------------------------------------------------------------
# Inline tests — run with:  python scripts/lib/text_cleanup.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    failures: list[str] = []

    def check(label: str, got, expected) -> None:
        if got == expected:
            print(f"  OK   {label}")
        else:
            failures.append(label)
            print(f"  FAIL {label}")
            print(f"       got:      {got!r}")
            print(f"       expected: {expected!r}")

    print("text_cleanup inline tests")
    print("=" * 60)

    # Test 1 — real NBSP from S60 manuscript (the exact character that broke
    # E7). Example: "Tier 1" with NBSP between Tier and 1.
    t1_input = "Tier\u00a01 68.2%"
    t1_expected = "Tier 1 68.2%"
    check("1. real NBSP (E7 S60)", strip_nbsp(t1_input), t1_expected)

    # Test 2 — narrow NBSP from French-style thin space around units
    t2_input = "3\u202f500 words"
    t2_expected = "3 500 words"
    check("2. narrow NBSP", strip_nbsp(t2_input), t2_expected)

    # Test 3 — mixed: NBSP + thin space + tab
    t3_input = "Tier\u00a01\u2009=\t0.682"
    t3_expected = "Tier 1 = 0.682"
    check("3. mixed space lookalikes", strip_nbsp(t3_input), t3_expected)

    # Test 4 — newlines preserved by strip_nbsp
    t4_input = "line1\u00a0A\nline2\u00a0B"
    t4_expected = "line1 A\nline2 B"
    check("4. newlines preserved", strip_nbsp(t4_input), t4_expected)

    # Test 5 — NFC normalization: decomposed 'á' (a + U+0301) -> composed
    t5_input = "Nu\u0301ble"
    t5_expected_nfc = "Nuble".replace("u", "\u00fa")  # 'Núble'
    check("5. NFC decomposed -> composed", nfc_normalize(t5_input), t5_expected_nfc)

    # Test 6 — full pipeline preserves newlines but normalizes NBSP + NFC
    t6_input = "Nu\u0301ble\u00a0region\nTier\u00a01"
    t6_expected = "N\u00fable region\nTier 1"
    check("6. preprocess_for_edit full pipeline", preprocess_for_edit(t6_input), t6_expected)

    # Test 7 — normalize_whitespace collapses multiple spaces but keeps newlines
    t7_input = "a    b\n  c   d  "
    t7_expected = "a b\nc d"
    check("7. normalize_whitespace collapse", normalize_whitespace(t7_input), t7_expected)

    # Test 8 — idempotence
    t8_input = "Tier\u00a01\nNu\u0301ble"
    once = preprocess_for_edit(t8_input)
    twice = preprocess_for_edit(once)
    check("8. idempotence preprocess_for_edit", once, twice)

    # Test 9 — empty / None guard
    check("9. empty string", preprocess_for_edit(""), "")

    # Test 10 — real-world: literal str.replace that E7 would have broken
    manuscript = "Tier\u00a01 achieved BSS 68.2% (95% CI 61.7-74.0)."
    manuscript = preprocess_for_edit(manuscript)
    patched = manuscript.replace("Tier 1 achieved BSS 68.2%", "Tier 1 achieved BSS 68.1%")
    t10_expected = "Tier 1 achieved BSS 68.1% (95% CI 61.7-74.0)."
    check("10. post-preprocess str.replace (E7 fix)", patched, t10_expected)

    print("=" * 60)
    if failures:
        print(f"FAILED: {len(failures)} test(s): {failures}")
        sys.exit(1)
    print(f"PASSED: 10/10 tests")
    sys.exit(0)
