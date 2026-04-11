#!/usr/bin/env python3
"""
build_manuscript_json.py
========================
Sub-tarea B4.1 del pipeline Hantavirus Nuble (S61).

One-shot parser (NOT a recurring workflow). Reads the v5 CONDENSED
manuscript markdown and emits a structured JSON that the paper-current.html
and paper-improved.html frontends consume.

Input
-----
C:/Proyectos/Hantavirus_Nuble/resultados/S49_ALERTAS/BLINDAJE_Q1/
    MANUSCRITO_EID_v5_CONDENSED_S60.md

Output
------
pipeline/repo/state/manuscript_v5_condensed.json

Algorithm
---------
1. Read the markdown file.
2. Split into blocks by blank-line pairs (`\n\n`).
3. Skip horizontal rule separators (`------`) and the title H1.
4. Track the active section (last `## ` heading) and subsection
   (last `### ` heading) for every block.
5. Enumerate paragraphs 1..N (target ~40).
6. Compute word count per paragraph (naive whitespace split).
7. Extract refs cited via two regexes: numeric `[n]` and author-year
   `(Author et al., YYYY)` / `(Author YYYY)`.
8. Derive an aggregated sections array with para_start, para_end, words.
9. Dump JSON with metadata block.

This script is idempotent. It never mutates the source manuscript.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Absolute paths (Windows-aware but platform neutral).
MANUSCRIPT_SRC = Path(
    r"C:/Proyectos/Hantavirus_Nuble/resultados/"
    r"S49_ALERTAS/BLINDAJE_Q1/MANUSCRITO_EID_v5_CONDENSED_S60.md"
)
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "state" / "manuscript_v5_condensed.json"

# Citation regexes.
RE_NUMERIC_CITE = re.compile(r"\[(\d{1,3})\]")
RE_AUTHOR_YEAR = re.compile(
    r"\(([A-ZÁÉÍÓÚÑ][\w\-]+(?:\s(?:&|et\s+al\.?|and)\s+[A-ZÁÉÍÓÚÑ]?[\w\-]*)?),?\s*(\d{4})[a-z]?\)"
)
RE_HR = re.compile(r"^-{3,}$")
RE_H1 = re.compile(r"^#\s+")
RE_H2 = re.compile(r"^##\s+(.+)$")
RE_H3 = re.compile(r"^###\s+(.+)$")

REFS_TARGET = 50
WORDS_TARGET = 3500

# Main text sections (those that count toward the EID 3,500-word cap).
# Order matters for rendering. Anything outside this set is still captured
# in the JSON (for completeness) but gets is_main_text=False and is not
# assigned a main-text para_id.
MAIN_TEXT_SECTIONS = {
    "Abstract",
    "Introduction",
    "Methods",
    "Results",
    "Discussion",
    "Conclusions",
}


def clean_section_name(raw: str) -> str:
    """Normalize a section heading by stripping trailing metadata."""
    name = raw.strip()
    # Drop parentheticals like "Abstract (target <=150 words...)".
    name = re.sub(r"\s*\(.*$", "", name).strip()
    return name


def _looks_like_table_fragment(block: str) -> bool:
    """Detect a block that is actually a fragment of a pandoc-style grid table.

    The v5 CONDENSED manuscript renders tables via pandoc in a multi-line
    layout where row continuations and separators become standalone blocks
    once we split on blank lines. Those fragments start with a horizontal
    rule of dashes, or contain the characteristic pattern of many runs of
    two or more spaces without a terminal period."""
    stripped = block.strip()
    if stripped.startswith("----"):
        return True
    first_line = stripped.splitlines()[0].strip() if stripped else ""
    # Fragments commonly start with a tier label followed by big runs of
    # whitespace (column alignment) and do not end with a period.
    if re.match(r"^(Tier\s*\d|BSS\s*95%|Tier-?1|Tier-?2|Tier-?3)", first_line):
        if "  " in first_line:
            return True
    return False


def parse_manuscript(md_text: str) -> dict:
    # Split into blocks by blank lines.
    raw_blocks = re.split(r"\n\s*\n", md_text)
    blocks_initial = [b.strip() for b in raw_blocks if b.strip()]

    # Post-process: merge pandoc table fragments back into the paragraph
    # that introduced the table. We deliberately skip headings (##, ###)
    # when locating the anchor so the merged content survives the main
    # iteration (where headings are consumed, not rendered as paragraphs).
    blocks: list[str] = []

    def _is_heading(b: str) -> bool:
        first = b.split("\n", 1)[0].strip()
        return bool(RE_H1.match(first) or RE_H2.match(first) or RE_H3.match(first))

    for block in blocks_initial:
        if _looks_like_table_fragment(block):
            # Walk back to find the most recent paragraph-like block.
            anchor_idx = len(blocks) - 1
            while anchor_idx >= 0 and _is_heading(blocks[anchor_idx]):
                anchor_idx -= 1
            if anchor_idx >= 0:
                blocks[anchor_idx] = blocks[anchor_idx] + "\n\n" + block
                continue
        blocks.append(block)

    paragraphs: list[dict] = []
    sections: list[dict] = []  # aggregated section metadata
    current_section = "Front matter"
    current_subsection: str | None = None
    para_id = 0  # only increments for main-text paragraphs
    extra_block_id = 0  # for non-main-text content
    sections_map: dict[str, dict] = {}
    total_words = 0  # main text only
    total_words_all = 0  # entire file

    for block in blocks:
        # Horizontal rule separator.
        if RE_HR.match(block):
            continue

        # Heading detection first. A heading line is the whole block.
        lines = block.split("\n")
        first = lines[0].strip()

        if RE_H1.match(first):
            # Title — do not count as a paragraph.
            continue

        h2_match = RE_H2.match(first)
        if h2_match:
            current_section = clean_section_name(h2_match.group(1))
            current_subsection = None
            # Do not emit a paragraph for the heading itself.
            continue

        h3_match = RE_H3.match(first)
        if h3_match:
            current_subsection = clean_section_name(h3_match.group(1))
            continue

        # Otherwise this is a paragraph-level block.
        text = block
        is_main = current_section in MAIN_TEXT_SECTIONS

        # Word count (simple whitespace tokenization).
        words = len(text.split())
        total_words_all += words

        # Citation extraction.
        numeric_refs = sorted({int(m) for m in RE_NUMERIC_CITE.findall(text)})
        author_year_refs = sorted(
            {f"{a} {y}" for a, y in RE_AUTHOR_YEAR.findall(text)}
        )
        refs_cited = {
            "numeric": numeric_refs,
            "author_year": author_year_refs,
        }

        if is_main:
            para_id += 1
            block_id = para_id
            total_words += words
        else:
            extra_block_id += 1
            # Use negative-ish ids so main-text para_id stays in [1, 40].
            block_id = 1000 + extra_block_id

        paragraphs.append(
            {
                "id": block_id,
                "section": current_section,
                "subsection": current_subsection,
                "is_main_text": is_main,
                "text": text,
                "words": words,
                "refs_cited": refs_cited,
                "char_length": len(text),
            }
        )

        bucket = sections_map.setdefault(
            current_section,
            {
                "name": current_section,
                "para_start": block_id,
                "para_end": block_id,
                "words": 0,
                "is_main_text": is_main,
            },
        )
        bucket["para_end"] = block_id
        bucket["words"] += words

    sections = list(sections_map.values())

    # Extract title from the H1 line.
    title_match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    # Count references by scanning the References block: lines like `1. Author ...`.
    refs_block_match = re.search(
        r"## References\s*(.*?)(?=\n## |$)",
        md_text,
        re.DOTALL,
    )
    refs_actual = 0
    if refs_block_match:
        refs_text = refs_block_match.group(1)
        refs_actual = len(re.findall(r"^\s*\d{1,3}\.\s", refs_text, re.MULTILINE))

    main_paragraph_count = sum(1 for p in paragraphs if p["is_main_text"])

    out = {
        "version": "v5_CONDENSED_S60",
        "source_path": (
            "resultados/S49_ALERTAS/BLINDAJE_Q1/MANUSCRITO_EID_v5_CONDENSED_S60.md"
        ),
        "parsed_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "total_words": total_words,
        "total_words_full_file": total_words_all,
        "total_paragraphs": main_paragraph_count,
        "total_blocks": len(paragraphs),
        "total_refs": refs_actual,
        "sections": sections,
        "paragraphs": paragraphs,
        "metadata": {
            "title": title,
            "word_count_target": WORDS_TARGET,
            "word_count_actual": total_words,
            "refs_target": REFS_TARGET,
            "refs_actual": refs_actual,
            "main_text_sections": sorted(MAIN_TEXT_SECTIONS),
            "parser_version": "b4.1-1.0",
        },
    }
    return out


def main() -> int:
    if not MANUSCRIPT_SRC.exists():
        sys.stderr.write(
            f"ERROR: manuscript source not found at {MANUSCRIPT_SRC}\n"
        )
        return 1

    md_text = MANUSCRIPT_SRC.read_text(encoding="utf-8")
    parsed = parse_manuscript(md_text)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        f"[build_manuscript_json] wrote {OUT_PATH.relative_to(REPO_ROOT)}  "
        f"paragraphs={parsed['total_paragraphs']}  "
        f"words={parsed['total_words']}  refs={parsed['total_refs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
