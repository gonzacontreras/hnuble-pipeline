#!/usr/bin/env python3
"""
build_manuscript_from_baseline.py
==================================
Sub-tarea S61 post-rotation fix: rebuild manuscript_v5_condensed.json from the
**S61 BASELINE MASTER CONTROL** (post-contamination-fix v5_v3 CLEAN).

Why this script exists
----------------------
B4 (sub-agent) used the wrong source: MANUSCRITO_EID_v5_CONDENSED_S60.md, which
predates the S61 contamination fix that removed 23 legacy paragraphs (#173-#195)
containing inline cover letter, PAHO 2023 hallucination, "End of assembled
manuscript", and "Next step for Gonzalo" markers.

The CANONICAL source post-S61 is the **section 5 of BASELINE_S61_MASTER_CONTROL.md**
(SHA256 d10d564e..., 949 lines, 9714 words), which contains the v5_v3 CLEAN
manuscript inline in clean Markdown with explicit hierarchical structure
(5.1 → 5.8, sub-sections 5.5.1–5.5.9, 5.6.1–5.6.7).

Equivalent .docx file: MANUSCRITO_EID_v5_v3_CLEAN_S61_BASELINE.docx
(SHA256 9ca07741..., 5106 words total docx, 3469 words main text — INVARIANT
versus pre-contamination versions).

Input
-----
C:/Proyectos/Hantavirus_Nuble/BASELINE_S61_MASTER_CONTROL.md
   Section 5 between "## 5. CONTENIDO COMPLETO DEL MANUSCRITO" (line 554)
   and "## 6. BIBLIOGRAFÍA COMPLETA" (line 722).

Output
------
pipeline/repo/state/manuscript_v5_condensed.json
   Same path as B4 wrote (kept stable so the frontend HTMLs do not break).
   Schema: same as before but `version` upgraded to "v5_v3_CLEAN_S61_BASELINE"
   and `source_path` updated to BASELINE.

Algorithm
---------
1. Read BASELINE_S61_MASTER_CONTROL.md.
2. Extract the section 5 slice (between "## 5." and "## 6.").
3. Parse hierarchical structure:
   - Main sections at "### 5.X" headings (Title/metadata, Abstract, Article
     Summary, Introduction, Methods, Results, Discussion, Conclusions).
   - Sub-sections at "**5.X.Y**" or "**5.X.Y NAME**" markers.
4. Split into paragraphs (blank-line separated, blockquote `>` recognised).
5. Enumerate para_id 1..N.
6. Word count per paragraph (whitespace split, markdown stripped).
7. Extract refs: author-year `(Author 2024)` / `(Author et al. 2024)` /
   `Author et al. 2024` patterns + the Methods code block annotated.
8. Compute total_words and total_paragraphs; declare main text vs metadata.
9. Persist `state/manuscript_v5_condensed.json`.

This script is idempotent and read-only on the source.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Source: BASELINE master control (mirror raíz preferida; obsidian mirror también válido)
BASELINE_SRC = Path(r"C:/Proyectos/Hantavirus_Nuble/BASELINE_S61_MASTER_CONTROL.md")
DOCX_CANONICAL = Path(
    r"C:/Proyectos/Hantavirus_Nuble/resultados/S49_ALERTAS/BLINDAJE_Q1/"
    r"submission/MANUSCRITO_EID_v5_v3_CLEAN_S61_BASELINE.docx"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = REPO_ROOT / "state" / "manuscript_v5_condensed.json"

# SHA256 expected for integrity verification
EXPECTED_DOCX_SHA = (
    "9ca07741799ddb3fa2567e4ba8ddfa1d895ab878a52b1d80bd4c35f4da4d02a9"
)
EXPECTED_BASELINE_SHA = (
    "d10d564ebb6b43c4db501d03d45d5fb1b72a09a013ee997b3683c8ef21387d49"
)

# Section 5 slice markers in the BASELINE markdown
SECTION_5_START = "## 5. CONTENIDO COMPLETO DEL MANUSCRITO"
SECTION_5_END = "## 6. BIBLIOGRAFÍA COMPLETA"

# Regex for ref extraction inside paragraphs
REF_PATTERNS = [
    re.compile(r"\(([A-Z][A-Za-z\-\u00C0-\u017F]+(?:\s+et\s+al\.?)?,?\s+\d{4}[a-z]?)\)"),
    re.compile(r"\b([A-Z][A-Za-z\-\u00C0-\u017F]+(?:\s+&\s+[A-Z][A-Za-z\-\u00C0-\u017F]+)?\s+\d{4}[a-z]?)\b"),
]

# Hierarchical heading regex
HEADING_3 = re.compile(r"^### (5\.\d+)\s+(.+)$")
SUBSECTION_BOLD = re.compile(r"^\*\*(5\.\d+\.\d+)\s*(.*?)\*\*\s*$")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_markdown(text: str) -> str:
    """Conservatively strip markdown for word counting."""
    # Remove blockquote prefix
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # Remove inline code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def count_words(text: str) -> int:
    return len(strip_markdown(text).split())


def extract_refs(text: str) -> list[str]:
    """Extract author-year refs found in the text. Dedupe preserving order."""
    found: list[str] = []
    seen: set[str] = set()
    for rx in REF_PATTERNS:
        for m in rx.finditer(text):
            ref = m.group(1).strip()
            # Filter out obvious non-refs (e.g. "1.21 per 100,000")
            if any(ch.isdigit() for ch in ref.split()[0]):
                continue
            if ref not in seen:
                seen.add(ref)
                found.append(ref)
    return found


def slice_section_5(full_text: str) -> str:
    start_idx = full_text.find(SECTION_5_START)
    end_idx = full_text.find(SECTION_5_END)
    if start_idx == -1 or end_idx == -1:
        raise ValueError(
            f"Could not locate section 5 markers in {BASELINE_SRC}. "
            f"start={start_idx} end={end_idx}"
        )
    return full_text[start_idx:end_idx]


def parse_section_5(slice_text: str) -> tuple[list[dict], list[dict]]:
    """Parse the section 5 markdown into (paragraphs, sections) lists."""
    lines = slice_text.splitlines()
    blocks: list[dict] = []
    current_section = "Pre-section"
    current_subsection: str | None = None
    buffer: list[str] = []

    def flush_buffer():
        nonlocal buffer
        if not buffer:
            return
        joined = "\n".join(buffer).strip()
        if joined and not joined.startswith("---"):
            blocks.append(
                {
                    "section": current_section,
                    "subsection": current_subsection,
                    "raw": joined,
                }
            )
        buffer = []

    for line in lines:
        # Section header (### 5.X NAME)
        m = HEADING_3.match(line)
        if m:
            flush_buffer()
            current_section = m.group(2).strip()
            current_subsection = None
            continue
        # Subsection (**5.X.Y NAME**) — only if it appears alone on a line
        ms = SUBSECTION_BOLD.match(line.strip())
        if ms:
            flush_buffer()
            current_subsection = ms.group(2).strip() or ms.group(1)
            continue
        # Heading 2 marker — section 5 root, skip
        if line.startswith("## "):
            flush_buffer()
            continue
        # Blank line: paragraph boundary
        if line.strip() == "":
            flush_buffer()
            continue
        buffer.append(line)
    flush_buffer()

    # Convert blocks into paragraphs with ids and metrics
    paragraphs: list[dict] = []
    for idx, blk in enumerate(blocks, start=1):
        text = blk["raw"]
        wc = count_words(text)
        refs = extract_refs(text)
        paragraphs.append(
            {
                "id": idx,
                "section": blk["section"],
                "subsection": blk["subsection"],
                "text": text,
                "words": wc,
                "char_length": len(text),
                "refs_cited": refs,
                "is_main_text": _is_main_text(blk["section"]),
            }
        )

    # Aggregated sections array
    sections: list[dict] = []
    if paragraphs:
        cur_name = paragraphs[0]["section"]
        cur_start = 1
        cur_words = 0
        for p in paragraphs:
            if p["section"] != cur_name:
                sections.append(
                    {
                        "name": cur_name,
                        "para_start": cur_start,
                        "para_end": p["id"] - 1,
                        "words": cur_words,
                    }
                )
                cur_name = p["section"]
                cur_start = p["id"]
                cur_words = 0
            cur_words += p["words"]
        sections.append(
            {
                "name": cur_name,
                "para_start": cur_start,
                "para_end": paragraphs[-1]["id"],
                "words": cur_words,
            }
        )

    return paragraphs, sections


def _is_main_text(section_name: str) -> bool:
    """Tag whether the section counts toward EID's 3500-word main text limit."""
    name = section_name.lower()
    if name.startswith("title"):
        return False
    if name.startswith("article summary"):
        return False
    return True


def main() -> int:
    if not BASELINE_SRC.exists():
        sys.stderr.write(f"FATAL: BASELINE not found: {BASELINE_SRC}\n")
        return 1
    if not DOCX_CANONICAL.exists():
        sys.stderr.write(
            f"WARNING: canonical docx not found at {DOCX_CANONICAL} "
            f"(continuing with markdown source only)\n"
        )

    baseline_sha = sha256_file(BASELINE_SRC)
    baseline_match = baseline_sha == EXPECTED_BASELINE_SHA
    docx_sha = sha256_file(DOCX_CANONICAL) if DOCX_CANONICAL.exists() else "missing"
    docx_match = docx_sha == EXPECTED_DOCX_SHA

    full_text = BASELINE_SRC.read_text(encoding="utf-8")
    slice_text = slice_section_5(full_text)
    paragraphs, sections = parse_section_5(slice_text)

    main_text_words = sum(p["words"] for p in paragraphs if p["is_main_text"])
    total_words = sum(p["words"] for p in paragraphs)

    payload = {
        "version": "v5_v3_CLEAN_S61_BASELINE",
        "source_path": str(BASELINE_SRC).replace("\\", "/"),
        "source_section": "5. CONTENIDO COMPLETO DEL MANUSCRITO",
        "docx_canonical": str(DOCX_CANONICAL).replace("\\", "/"),
        "parsed_at": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "integrity": {
            "baseline_sha256_expected": EXPECTED_BASELINE_SHA,
            "baseline_sha256_actual": baseline_sha,
            "baseline_sha_match": baseline_match,
            "docx_sha256_expected": EXPECTED_DOCX_SHA,
            "docx_sha256_actual": docx_sha,
            "docx_sha_match": docx_match,
        },
        "metadata": {
            "title": (
                "A Three-Tier Probabilistic Early Warning System for "
                "Andes Virus Hantavirus Cardiopulmonary Syndrome in "
                "South-Central Chile (2002-2024)"
            ),
            "running_title": (
                "Hantavirus three-tier ecological alert system - "
                "Nuble, Chile"
            ),
            "target_journal": "Emerging Infectious Diseases (CDC)",
            "article_type": "Research article",
            "word_count_target_main_text": 3500,
            "word_count_actual_main_text": main_text_words,
            "word_count_actual_total": total_words,
            "word_count_official_main_text": 3469,  # per Word COM, S60 + S61
            "word_count_official_total_docx": 5106,  # per Word COM v5_v3 CLEAN
            "refs_target": 50,
            "refs_actual": 50,  # canonical, declared
            "pre_specification_lock": "2026-04-04",
            "zenodo_doi": "10.5281/zenodo.19425753",
            "submission_deadline": "2026-04-14T06:00:00Z",
            "author": (
                "Gonzalo Contreras, MD - Hospital Clinico Herminda Martin, "
                "Chillan, Nuble, Chile"
            ),
            "keywords": [
                "hantavirus",
                "Andes virus",
                "early warning system",
                "walk-forward validation",
                "logarithmic score",
                "ecological forecasting",
                "Chile",
                "One Health",
                "pre-registration",
                "anti-HARKing",
            ],
        },
        "stats": {
            "total_paragraphs": len(paragraphs),
            "total_sections": len(sections),
            "main_text_paragraphs": sum(1 for p in paragraphs if p["is_main_text"]),
            "main_text_words_parsed": main_text_words,
            "total_words_parsed": total_words,
            "total_refs_in_text": len(
                {ref for p in paragraphs for ref in p["refs_cited"]}
            ),
        },
        "sections": sections,
        "paragraphs": paragraphs,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[OK] wrote {OUTPUT_JSON}")
    print(f"  baseline SHA match: {baseline_match}")
    print(f"  docx SHA match:     {docx_match}")
    print(f"  paragraphs:         {len(paragraphs)}")
    print(f"  sections:           {len(sections)}")
    print(f"  main text words:    {main_text_words} (vs official 3469)")
    print(f"  total words parsed: {total_words}")
    print(f"  unique refs found:  {len({r for p in paragraphs for r in p['refs_cited']})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
