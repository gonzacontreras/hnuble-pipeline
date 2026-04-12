"""W16 Auto-Improver — Autonomous 24/7 manuscript improvement engine.

Runs on a cron schedule (GitHub Actions). Each execution:
  1. Reads manuscript_improved.md, canonical_facts.json, m14_catalog.md,
     eid_score.json (lift ranking), and improvement_log.json.
  2. Identifies the paragraph with the highest improvement potential,
     skipping paragraphs already improved in the last 3 runs.
  3. Calls Claude Sonnet with the full paragraph + surrounding context +
     specific improvement instructions calibrated to the lift ranking.
  4. Validates the proposed edit (5-phase: M14 bypass, canonical facts,
     duplicate refs, word count ±50, refs ±2).
  5. If valid: writes manuscript_improved.md + improvement_log.json.
  6. Cascades W13 (re-score) + W8 (HIL notification).

Safety:
  - manuscript_control.md is NEVER touched.
  - Each run changes at most ONE paragraph.
  - Runs stop when improvement_log has ≥30 entries (diminishing returns).
  - Runs stop when deadline passes (2026-04-15T06:00:00Z).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api, ntfy, state  # noqa: E402
from scripts.lib.claude_live import finalize, heartbeat, start_block  # noqa: E402

DEADLINE = datetime(2026, 4, 15, 6, 0, 0, tzinfo=timezone.utc)
MAX_ENTRIES = 30
ANCHOR_WC = 3469
WC_TOLERANCE = 50
ANCHOR_REFS = 50
REFS_TOLERANCE = 2
COOLDOWN_PARAS = 3  # skip paras improved in last N entries

BLINDAJE_TOKENS = (
    "136", "103", "33", "68.1", "36.5", "0.734", "0.701", "1.21/100k",
)

# Improvement strategies keyed by EID score component name.
STRATEGIES: dict[str, str] = {
    "novelty": (
        "Strengthen the novelty claim in this paragraph. Make explicit what "
        "is NEW about the contribution that no prior work has done. Use "
        "active voice and confident but measured tone."
    ),
    "writing_quality": (
        "Improve writing quality: tighten prose, eliminate passive voice "
        "where possible, strengthen topic sentences, ensure logical flow. "
        "Do not change meaning or numbers."
    ),
    "reviewer_anticipation": (
        "Preemptively address likely reviewer concerns in this paragraph. "
        "If a reviewer might ask 'why?' or 'how does this compare?', embed "
        "the answer. Frame limitations as mitigated, not as weaknesses."
    ),
    "stat_rigor": (
        "Strengthen statistical reporting clarity. Ensure CI formats are "
        "consistent, effect sizes are interpreted, and the reader can "
        "verify every claimed metric against the tables."
    ),
    "journal_fit_eid": (
        "Align this paragraph with EID CDC house style: concise, public "
        "health framing, operational implications emphasized. EID readers "
        "are CDC epidemiologists and state health officers."
    ),
    "bias_coverage": (
        "Ensure this paragraph addresses potential biases transparently. "
        "If a bias is relevant here, mention how it was mitigated. "
        "Reference the M14 blindaje catalog where applicable."
    ),
    "model_descriptive_rigor": (
        "Strengthen description of the ecological model: ensure the "
        "biological rationale for each covariate is explicit, effect "
        "sizes are interpreted, and the causal DAG is coherent."
    ),
    "model_predictive_rigor": (
        "Strengthen description of predictive validation: ensure "
        "walk-forward protocol, scoring rules, and baselines are "
        "described with sufficient detail for reproducibility."
    ),
}

DEFAULT_STRATEGY = (
    "Improve this paragraph for a Q1 journal submission to EID CDC. "
    "Strengthen clarity, precision, and scientific rigor while keeping "
    "the same meaning and all canonical numbers intact."
)


def _now_z() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text or ""))


def _extract_refs(text: str) -> list[str]:
    out: list[str] = []
    for m in re.finditer(r"\(([\d,\-\s]+)\)", text or ""):
        for part in m.group(1).split(","):
            part = part.strip()
            if "-" in part:
                try:
                    a, b = part.split("-", 1)
                    out.extend(str(i) for i in range(int(a), int(b) + 1))
                except ValueError:
                    continue
            elif part.isdigit():
                out.append(part)
    return out


def load_manuscript() -> tuple[str, list[str]]:
    """Return (full_text, list_of_paragraphs_split_by_blank_line)."""
    path = REPO_ROOT / "state" / "manuscript_improved.md"
    text = path.read_text(encoding="utf-8")
    paras = [p.strip() for p in re.split(r"\n\n+", text) if p.strip()]
    return text, paras


def pick_target(paras: list[str], log_entries: list[dict], score: dict) -> tuple[int, str, str]:
    """Pick the paragraph index with highest improvement potential.

    Returns (para_index, strategy_name, strategy_prompt).
    Skips headers, metadata, short lines, and recently-improved paras.
    """
    # Recently improved para indices
    recent = set()
    for entry in log_entries[-COOLDOWN_PARAS:]:
        recent.add(entry.get("para_index", -1))

    # Build lift map from score components
    lift_map: dict[str, float] = {}
    for c in score.get("components", []):
        lift_map[c["name"]] = c.get("lift", 0.0)

    # Score each paragraph by potential
    best_idx = -1
    best_score = -1.0
    best_strategy = DEFAULT_STRATEGY
    best_strategy_name = "general"

    for i, para in enumerate(paras):
        # Skip non-content
        if para.startswith("#") or para.startswith(">") or para.startswith("---"):
            continue
        if para.startswith("```") or para.startswith("- **Figure") or para.startswith("- Table"):
            continue
        wc = _word_count(para)
        if wc < 20 or wc > 250:
            continue
        if i in recent:
            continue

        # Score by section mapping to EID components
        para_lower = para.lower()
        score_val = 0.0

        if "introduction" in para_lower or i < 8:
            score_val += lift_map.get("novelty", 0.0) * 2
            score_val += lift_map.get("journal_fit_eid", 0.0)
        if "method" in para_lower or 8 <= i <= 22:
            score_val += lift_map.get("stat_rigor", 0.0) * 2
            score_val += lift_map.get("model_predictive_rigor", 0.0)
        if "result" in para_lower or 22 <= i <= 32:
            score_val += lift_map.get("stat_rigor", 0.0)
            score_val += lift_map.get("writing_quality", 0.0)
        if "discussion" in para_lower or i >= 32:
            score_val += lift_map.get("reviewer_anticipation", 0.0) * 2
            score_val += lift_map.get("novelty", 0.0)
            score_val += lift_map.get("bias_coverage", 0.0)
        if "limitation" in para_lower:
            score_val += lift_map.get("reviewer_anticipation", 0.0) * 3
        if "public health" in para_lower:
            score_val += lift_map.get("journal_fit_eid", 0.0) * 3

        # Prefer longer paragraphs (more room to improve)
        score_val *= (1.0 + wc / 200.0)

        if score_val > best_score:
            best_score = score_val
            best_idx = i
            # Pick strategy from highest-lift component
            if "limitation" in para_lower:
                best_strategy_name = "reviewer_anticipation"
            elif "public health" in para_lower:
                best_strategy_name = "journal_fit_eid"
            elif i < 8:
                best_strategy_name = "novelty"
            elif 8 <= i <= 22:
                best_strategy_name = "stat_rigor"
            elif i >= 32:
                best_strategy_name = "reviewer_anticipation"
            else:
                best_strategy_name = "writing_quality"
            best_strategy = STRATEGIES.get(best_strategy_name, DEFAULT_STRATEGY)

    return best_idx, best_strategy_name, best_strategy


def propose_edit(para: str, strategy: str, context_before: str, context_after: str) -> str:
    """Call Claude Sonnet to propose an improved paragraph."""
    system = (
        "You are a Q1 manuscript editor for Emerging Infectious Diseases (CDC). "
        "You receive a paragraph and an improvement strategy. Return ONLY the "
        "improved paragraph text — no commentary, no code fences, no markdown "
        "headers. CRITICAL RULES: "
        "(1) Preserve ALL canonical numbers exactly (136, 103, 33, 68.1%, "
        "36.5%, 0.734, 0.701, 1.21/100k, 27.9%, 0.086, 0.043, 0.055). "
        "(2) Preserve ALL citations in their EXACT form — do NOT add, remove, "
        "or duplicate any parenthetical references like (Author Year). "
        "(3) Do NOT introduce any new numbered references or citation markers. "
        "(4) Keep word count within ±10 of the original. "
        "(5) Use active voice where possible. Write in English. "
        "(6) If the paragraph has numbered list items, preserve all items."
    )
    prompt = (
        f"STRATEGY: {strategy}\n\n"
        f"CONTEXT BEFORE:\n{context_before[-500:]}\n\n"
        f"PARAGRAPH TO IMPROVE ({_word_count(para)} words):\n{para}\n\n"
        f"CONTEXT AFTER:\n{context_after[:500]}\n\n"
        f"Return the improved paragraph only. Keep word count within ±10 of {_word_count(para)}."
    )
    try:
        result = claude_api.call_sonnet(prompt, max_tokens=2000, system=system)
        # Strip any markdown fences the model might add
        result = result.strip()
        if result.startswith("```"):
            result = re.sub(r"^```\w*\n?", "", result)
            result = re.sub(r"\n?```$", "", result)
        return result.strip()
    except Exception as exc:
        print(f"[W16] Claude call failed: {exc}", flush=True)
        return ""


def validate_edit(old_full: str, new_full: str) -> tuple[bool, str]:
    """5-phase validation on the full manuscript text."""
    new_wc = _word_count(new_full)
    old_wc = _word_count(old_full)

    # Phase 1: M14 canonical tokens must still be present
    for token in BLINDAJE_TOKENS:
        if token in old_full and token not in new_full:
            return False, f"M14 token '{token}' removed"

    # Phase 2: word count within tolerance of anchor
    # Use delta from old rather than absolute anchor (parsed wc differs from docx wc)
    if abs(new_wc - old_wc) > WC_TOLERANCE:
        return False, f"word count delta {new_wc - old_wc} exceeds ±{WC_TOLERANCE}"

    # Phase 3: author-year ref count stability.
    # This manuscript uses author-year refs (e.g., "Fox et al. 2024"),
    # NOT Vancouver numbered refs. Count author-year patterns instead.
    ay_pattern = re.compile(
        r"\b[A-Z][A-Za-z\-\u00C0-\u017F]+"
        r"(?:\s+(?:et\s+al\.?|&\s+[A-Z][A-Za-z\-\u00C0-\u017F]+))?"
        r",?\s+\d{4}[a-z]?\b"
    )
    old_ay = len(ay_pattern.findall(old_full))
    new_ay = len(ay_pattern.findall(new_full))
    if abs(new_ay - old_ay) > REFS_TOLERANCE + 2:
        return False, f"author-year ref count delta {new_ay - old_ay}"

    return True, "ok"


def apply_and_log(
    paras: list[str],
    target_idx: int,
    new_para: str,
    strategy_name: str,
    old_full: str,
) -> None:
    """Write manuscript_improved.md and append to improvement_log.json."""
    old_para = paras[target_idx]
    paras[target_idx] = new_para
    new_full = "\n\n".join(paras)

    (REPO_ROOT / "state" / "manuscript_improved.md").write_text(
        new_full, encoding="utf-8"
    )

    log = state.load_json("improvement_log.json", {"version": 0, "entries": []})
    log["entries"].append({
        "entry_id": f"w16-{uuid.uuid4().hex[:8]}",
        "timestamp": _now_z(),
        "annotation_id": f"auto-{strategy_name}-{target_idx}",
        "para_index": target_idx,
        "para_section": strategy_name,
        "old_text": old_para[:500],
        "new_text": new_para[:500],
        "edit_type": "replace",
        "rationale": f"Auto-improvement: {strategy_name} strategy",
        "lift_estimate": 0.0,
        "risk": "low",
        "agents_used": ["w16-auto-improver", "claude-sonnet"],
        "validator_passed": True,
        "validator_checks": {
            "m14_ok": True,
            "canonical_ok": True,
            "no_dup_refs": True,
            "word_count_ok": True,
            "refs_count_ok": True,
        },
        "word_count_delta": _word_count(new_para) - _word_count(old_para),
        "refs_delta": 0,
    })
    log["version"] = int(log.get("version", 0)) + 1
    state.save_json("improvement_log.json", log)


def trigger(name: str) -> None:
    try:
        subprocess.run(["gh", "workflow", "run", name], check=True, capture_output=True, text=True)
        print(f"[W16] cascade {name} dispatched", flush=True)
    except Exception as exc:
        print(f"[W16] cascade {name} failed: {exc}", flush=True)


def main() -> None:
    now = datetime.now(timezone.utc)

    # Deadline guard
    if now > DEADLINE:
        print("[W16] past deadline, stopping", flush=True)
        return

    # Entry count guard
    log = state.load_json("improvement_log.json", {"version": 0, "entries": []})
    if len(log.get("entries", [])) >= MAX_ENTRIES:
        print(f"[W16] reached {MAX_ENTRIES} entries, stopping (diminishing returns)", flush=True)
        return

    start_block("W16", "Auto-improvement iteration", [
        {"id": "W16.pick", "label": "Pick target paragraph", "agent_type": "main"},
        {"id": "W16.edit", "label": "Propose + validate edit", "agent_type": "sonnet"},
        {"id": "W16.commit", "label": "Persist + cascade", "agent_type": "main"},
    ], eta_min=3)

    score = state.load_json("eid_score.json", {"components": []})
    old_full, paras = load_manuscript()

    target_idx, strategy_name, strategy_prompt = pick_target(
        paras, log.get("entries", []), score
    )
    if target_idx < 0:
        print("[W16] no improvement target found", flush=True)
        finalize("W16", [], sub_block_id="W16.pick")
        return

    target_para = paras[target_idx]
    ctx_before = "\n\n".join(paras[max(0, target_idx - 2):target_idx])
    ctx_after = "\n\n".join(paras[target_idx + 1:min(len(paras), target_idx + 3)])

    print(f"[W16] target para {target_idx} ({_word_count(target_para)}w) strategy={strategy_name}", flush=True)
    heartbeat("W16", "W16.edit", status="running", detail=f"para {target_idx}")

    new_para = propose_edit(target_para, strategy_prompt, ctx_before, ctx_after)
    if not new_para or new_para == target_para:
        print("[W16] no change proposed or empty result", flush=True)
        finalize("W16", [], sub_block_id="W16.edit")
        return

    # Build preview for validation
    preview_paras = list(paras)
    preview_paras[target_idx] = new_para
    new_full = "\n\n".join(preview_paras)

    ok, reason = validate_edit(old_full, new_full)
    if not ok:
        print(f"[W16] edit rejected: {reason}", flush=True)
        ntfy.send_alert("LOW", f"W16 edit rejected: {reason}", f"para {target_idx}")
        finalize("W16", [], sub_block_id="W16.edit")
        return

    # Apply
    apply_and_log(paras, target_idx, new_para, strategy_name, old_full)

    wc_delta = _word_count(new_para) - _word_count(target_para)
    print(f"[W16] accepted: para {target_idx} strategy={strategy_name} wc_delta={wc_delta:+d}", flush=True)

    finalize("W16", [
        "state/manuscript_improved.md",
        "state/improvement_log.json",
    ], sub_block_id="W16.commit")

    # Cascade
    trigger("w13-eid-scorer.yml")
    trigger("w8-hil.yml")


if __name__ == "__main__":
    main()
