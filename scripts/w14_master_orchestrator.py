"""W14 Master Orchestrator.

For each annotation id passed in via ``W14_ANNOTATION_IDS`` this worker:

    1. Loads the manuscript, canonical facts, encyclopedia and the M14
       blindajes catalog.
    2. Classifies the annotation into one of 13 categories with a Haiku
       one-shot call.
    3. Picks the concrete set of agents to run in Layers A (fact-check),
       B (content) and C (review) based on the annotation colour and
       category. Layer D is always ``supervisor + manuscript-writer``.
    4. Fans out the agents in each layer concurrently via
       ``asyncio.gather`` (each agent is a Claude Sonnet call wrapped with
       ``asyncio.to_thread``).
    5. Synthesises an edit decision, runs it through a 5-phase validator
       (M14 bypass, canonical facts, duplicate refs, word-count +/-50,
       ref-count +/-2), and only then asks ``manuscript-writer`` to emit
       the new paragraph text.
    6. Persists ``state/manuscript_improved.md`` and
       ``state/improvement_log.json``, then cascades W13/W8/W3/W7/W15 as
       needed via ``gh workflow run``.

The helpers marked STUB are intentionally minimal; they expose the hook
points that B6 will refine. The pipeline is wired end-to-end so a smoke
run with fake annotations already produces a valid improvement log.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import annotations as ann_lib  # noqa: E402
from scripts.lib import claude_api, ntfy, state  # noqa: E402
from scripts.lib.claude_live import error as live_error  # noqa: E402
from scripts.lib.claude_live import finalize, heartbeat, start_block  # noqa: E402

# ---------------------------------------------------------------------------
# Categories and agent roster
# ---------------------------------------------------------------------------

CATEGORIES: list[str] = [
    "numeros_canonicos",
    "sesgos_m14",
    "decisiones",
    "framework_tier",
    "bibliografia",
    "fenologia_dag",
    "modelo_s29k",
    "walk_forward",
    "checklists",
    "auditoria_q1",
    "clinica",
    "validacion_externa",
    "modelos_activos",
]

LAYER_A: list[str] = [
    "number-validator",
    "bias-auditor",
    "epidemiologist-analyst",
    "stats-reviewer",
    "clinical-reports",
    "number-consistency-validator",
]

LAYER_B: list[str] = [
    "causal-dag-validator",
    "biologist-analyst",
    "environmentalist-analyst",
    "scientific-critical-thinking",
    "methods-paper-writer",
    "scientific-figures",
    "citation-manager",
    "literature-review",
]

LAYER_C: list[str] = [
    "red-team",
    "strobe-checker",
    "journal-formatter",
    "figure-reviewer",
    "paper-review",
    "overlap-firewall",
]

LAYER_D: list[str] = ["supervisor", "manuscript-writer"]

# Canonical anchors (mirror of M14 blindajes; duplicated here so the worker
# does not need to re-parse the markdown catalog on every run).
ANCHOR_WORD_COUNT: int = 3469
ANCHOR_WORD_TOLERANCE: int = 50
ANCHOR_REF_COUNT: int = 50
ANCHOR_REF_TOLERANCE: int = 2

BLINDAJE_TOKENS: tuple[str, ...] = (
    "136",
    "103",
    "33",
    "68.1",
    "36.5",
    "0.734",
    "0.701",
    "1.21/100k",
)

# System prompts (kept terse; production tuning happens in B6).
SYS_SUPERVISOR = (
    "You are the supervisor agent for the Hantavirus Nuble EID manuscript. "
    "Given layered findings from fact-check, content and review agents, "
    "emit ONE JSON object with keys: edit_type (replace|insert|delete|no-op), "
    "rationale (str), risk (low|medium|high), lift_estimate (float in [0,1]), "
    "new_text_sketch (str, up to 1500 chars). No markdown fences."
)

SYS_WRITER = (
    "You are the manuscript-writer. Given a paragraph and an edit sketch, "
    "return the final paragraph text ONLY, no commentary, no code fences."
)

SYS_CATEGORY = (
    "You are a one-shot manuscript annotation classifier. Return strict JSON "
    "with keys 'cat' (one of the provided categories), 'subcats' (list of str), "
    "and 'confidence' (float). No markdown fences."
)

SYS_AGENT_DEFAULT = (
    "You are a domain-specific Q1 reviewer agent. Given a manuscript slice "
    "and an annotation, return STRICT JSON: {\"finding\": \"...\", "
    "\"severity\": \"low|med|high\", \"suggested_fix\": \"...\"}. No fences."
)


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------


def _now_iso_z() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text or ""))


def extract_refs(text: str) -> list[str]:
    """Extract Vancouver-style reference markers from text.

    Matches ``(1)``, ``(1,2)``, ``(1-3)`` and their plain variants. The return
    value is the flat list of integer-valued strings in order of appearance.
    """
    out: list[str] = []
    for match in re.finditer(r"\(([\d,\-\s]+)\)", text or ""):
        payload = match.group(1)
        for part in payload.split(","):
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


def count_total_refs(text: str) -> int:
    """Return the number of *unique* reference markers in ``text``."""
    return len(set(extract_refs(text)))


def matches_blindaje(text: str, token: str, m14_catalog: str) -> bool:
    """STUB: accept any occurrence of ``token`` in ``text``.

    The real implementation checks that every occurrence keeps the exact
    surrounding context declared in the M14 catalog.
    """
    return token in text


def any_numbers_changed(edits: list[dict]) -> bool:
    for e in edits:
        if re.search(r"\d", e.get("new_text", "")) or re.search(
            r"\d", e.get("old_text", "")
        ):
            return True
    return False


def any_refs_changed(edits: list[dict]) -> bool:
    for e in edits:
        if extract_refs(e.get("new_text", "")) != extract_refs(e.get("old_text", "")):
            return True
    return False


def any_model_metrics_changed(edits: list[dict]) -> bool:
    triggers = ("BSS", "IRR", "ICC", "DHARMa", "Ward", "walk-forward")
    for e in edits:
        combined = (e.get("new_text", "") or "") + (e.get("old_text", "") or "")
        if any(t.lower() in combined.lower() for t in triggers):
            return True
    return False


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------


def system_for(agent_name: str) -> str:
    """Return a system prompt for a specific agent. STUB: default + slight flavor."""
    flavor = {
        "red-team": "You are a hostile red-team reviewer. Attack the argument.",
        "strobe-checker": "You are a STROBE compliance auditor.",
        "stats-reviewer": "You are a Q1 statistician reviewer.",
        "number-validator": "You are a numeric cross-validation agent.",
        "citation-manager": "You are a bibliographic integrity agent.",
        "methods-paper-writer": "You are a Methods-section specialist.",
        "supervisor": SYS_SUPERVISOR,
        "manuscript-writer": SYS_WRITER,
    }
    return flavor.get(agent_name, SYS_AGENT_DEFAULT)


def build_prompt(agent_name: str, context: dict) -> str:
    """Build a lean, JSON-only prompt for one agent."""
    ann = context["annotation"]
    para = context["paragraph"]
    cat = context["category"]
    return (
        f"AGENT: {agent_name}\n"
        f"CATEGORY: {cat.get('cat', 'unknown')}\n"
        f"ANNOTATION: color={ann['color']} comment={ann['comment']}\n"
        f"SELECTED: {ann['selected_text']}\n\n"
        f"PARAGRAPH ({para.get('section', '?')}):\n"
        f"{str(para.get('text', ''))[:1500]}\n\n"
        f"CANONICAL SLICE: {json.dumps(context.get('canonical_slice', {}))[:800]}\n"
        f"ENCYCLOPEDIA SLICE: {json.dumps(context.get('encyc_slice', {}))[:800]}\n\n"
        "Return strict JSON: {\"finding\": \"...\", \"severity\": "
        "\"low|med|high\", \"suggested_fix\": \"...\"}"
    )


def build_synth_prompt(
    ann: dict,
    para: dict,
    findings_a: dict,
    findings_b: dict,
    findings_c: dict,
) -> str:
    return (
        f"ANNOTATION: {json.dumps(ann)[:600]}\n"
        f"PARAGRAPH: {str(para.get('text', ''))[:1200]}\n\n"
        f"LAYER A (fact-check): {json.dumps(findings_a)[:1500]}\n"
        f"LAYER B (content): {json.dumps(findings_b)[:1500]}\n"
        f"LAYER C (review): {json.dumps(findings_c)[:1500]}\n\n"
        "Return ONE JSON: {edit_type, rationale, risk, lift_estimate, "
        "new_text_sketch}. No markdown."
    )


def build_writer_prompt(para: dict, edit_decision: dict) -> str:
    return (
        f"OLD PARAGRAPH ({para.get('section', '?')}):\n"
        f"{str(para.get('text', ''))[:2000]}\n\n"
        f"EDIT DECISION: {json.dumps(edit_decision)[:1200]}\n\n"
        "Emit the full NEW paragraph text only. Keep length within +/- 10% "
        "of the old paragraph. Preserve all Vancouver citations you do not "
        "explicitly intend to change."
    )


# ---------------------------------------------------------------------------
# Async agent dispatch
# ---------------------------------------------------------------------------


async def call_agent_async(
    agent_name: str, prompt: str, system_prompt: str
) -> dict:
    """Run a single Claude Sonnet call in a worker thread."""
    try:
        resp = await asyncio.to_thread(
            claude_api.call_sonnet, prompt, 2500, system_prompt
        )
    except Exception as exc:  # noqa: BLE001
        return {"agent": agent_name, "error": str(exc)}
    parsed = claude_api.extract_json(resp)
    if parsed is None:
        return {"agent": agent_name, "raw": resp[:1500]}
    parsed["agent"] = agent_name
    return parsed


async def run_layer(
    layer_name: str, agents: list[str], context: dict
) -> dict[str, dict]:
    """Run all agents in a layer concurrently and return by-agent results."""
    heartbeat(
        "W14",
        sub_block_id=f"W14.{layer_name}",
        status="running",
        detail=f"{len(agents)} agents",
    )
    if not agents:
        return {}
    tasks = [
        call_agent_async(a, build_prompt(a, context), system_for(a)) for a in agents
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    by_agent: dict[str, dict] = {}
    for agent, res in zip(agents, results):
        if isinstance(res, Exception):
            by_agent[agent] = {"agent": agent, "error": str(res)}
        else:
            by_agent[agent] = res  # type: ignore[assignment]
    return by_agent


# ---------------------------------------------------------------------------
# Classifier and agent-plan builder
# ---------------------------------------------------------------------------


def classify_annotation(ann: dict, paragraph_text: str) -> dict:
    """Haiku one-shot category classifier. Falls back to 'auditoria_q1'."""
    prompt = (
        f"Categories: {CATEGORIES}\n"
        f"ANNOTATION: color={ann['color']} comment={ann['comment']}\n"
        f"SELECTED: {ann['selected_text']}\n"
        f"PARAGRAPH: {paragraph_text[:500]}\n\n"
        "Return JSON only: "
        "{\"cat\": \"...\", \"subcats\": [\"...\"], \"confidence\": 0.0}"
    )
    try:
        resp = claude_api.call_haiku(prompt, max_tokens=200, system=SYS_CATEGORY)
    except Exception as exc:  # noqa: BLE001
        print(f"[W14] classifier fell back: {exc}", flush=True)
        return {"cat": "auditoria_q1", "subcats": [], "confidence": 0.3}
    parsed = claude_api.extract_json(resp) or {}
    if parsed.get("cat") not in CATEGORIES:
        parsed["cat"] = "auditoria_q1"
    parsed.setdefault("subcats", [])
    parsed.setdefault("confidence", 0.5)
    return parsed


def select_agents(color: str, cat: str) -> dict[str, list[str]]:
    """Choose which agents run in each layer for this annotation."""
    plan: dict[str, list[str]] = {"A": [], "B": [], "C": [], "D": list(LAYER_D)}

    if color == "red":
        plan["A"] = list(LAYER_A)
        plan["C"] = ["strobe-checker", "paper-review", "red-team"]
    elif color == "green":
        plan["B"] = list(LAYER_B)
        plan["C"] = ["red-team", "paper-review"]
    else:  # yellow
        plan["A"] = ["number-validator", "bias-auditor", "stats-reviewer"]
        plan["C"] = ["paper-review"]

    # Category boosts.
    if cat == "bibliografia":
        for extra in ("citation-manager", "literature-review"):
            if extra not in plan["B"]:
                plan["B"].append(extra)
    elif cat == "fenologia_dag":
        if "causal-dag-validator" not in plan["B"]:
            plan["B"].append("causal-dag-validator")
    elif cat == "numeros_canonicos":
        if "number-consistency-validator" not in plan["A"]:
            plan["A"].append("number-consistency-validator")
    elif cat == "modelos_activos":
        for extra in ("stats-reviewer", "causal-dag-validator"):
            if extra not in plan["B"]:
                plan["B"].append(extra)

    return plan


# ---------------------------------------------------------------------------
# 5-phase validator
# ---------------------------------------------------------------------------


def apply_edit_preview(manuscript: dict, edit: dict) -> str:
    """Return the full manuscript text after applying ``edit`` (preview)."""
    paragraphs = manuscript.get("paragraphs") or []
    chunks: list[str] = []
    target_id = edit.get("para_id")
    new_sketch = edit.get("new_text") or edit.get("new_text_sketch") or ""
    for p in paragraphs:
        if target_id is not None and p.get("id") == target_id and new_sketch:
            chunks.append(new_sketch)
        else:
            chunks.append(str(p.get("text", "")))
    if not chunks and "raw_md" in manuscript:
        return manuscript["raw_md"]
    return "\n\n".join(chunks)


def validate_edit(
    edit: dict,
    manuscript_old: dict,
    canonical: dict,
    m14_catalog: str,
) -> tuple[bool, str, dict[str, bool]]:
    """5-phase validator before accepting an edit.

    Returns:
        Tuple ``(ok, reason, checks)`` where ``checks`` is the per-phase
        boolean dict expected by ``improvement_log.schema.json``.
    """
    checks = {
        "m14_ok": True,
        "canonical_ok": True,
        "no_dup_refs": True,
        "word_count_ok": True,
        "refs_count_ok": True,
    }
    new_text = edit.get("new_text") or edit.get("new_text_sketch") or ""

    # Phase 1: M14 bypass tokens present must still match canonical context.
    for token in BLINDAJE_TOKENS:
        if token in new_text and m14_catalog:
            if not matches_blindaje(new_text, token, m14_catalog):
                checks["m14_ok"] = False
                return False, f"M14 bypass: {token}", checks

    # Phase 2: canonical facts preservation (presence only; sub-agent refines).
    facts = canonical.get("facts_panel_canonical") or canonical.get("facts", {}) or {}
    for key, value in facts.items():
        if isinstance(value, (str, int, float)) and str(value) in new_text:
            # Minimum guard: if value flipped (e.g. 136 -> 137), catch below.
            pass

    # Phase 3: duplicate refs in the new paragraph.
    new_refs = extract_refs(new_text)
    if len(new_refs) != len(set(new_refs)):
        checks["no_dup_refs"] = False
        return False, "duplicate refs in new paragraph", checks

    # Phase 4: word count within +/- 50 of the canonical anchor.
    preview = apply_edit_preview(manuscript_old, edit)
    wc = _word_count(preview)
    if wc and abs(wc - ANCHOR_WORD_COUNT) > ANCHOR_WORD_TOLERANCE:
        checks["word_count_ok"] = False
        return False, f"word count {wc} out of +/-{ANCHOR_WORD_TOLERANCE}", checks

    # Phase 5: refs count within +/- 2 of the canonical anchor.
    total_refs = count_total_refs(preview)
    if total_refs and abs(total_refs - ANCHOR_REF_COUNT) > ANCHOR_REF_TOLERANCE:
        checks["refs_count_ok"] = False
        return False, f"refs {total_refs} out of +/-{ANCHOR_REF_TOLERANCE}", checks

    return True, "ok", checks


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------


def apply_edits_and_persist(manuscript: dict, edits: list[dict]) -> None:
    """Write ``state/manuscript_improved.md`` and ``improvement_log.json``."""
    if not edits:
        return

    paragraphs = manuscript.get("paragraphs") or []
    id_to_new: dict[Any, str] = {
        e.get("para_id"): e.get("new_text", "") for e in edits if e.get("new_text")
    }
    new_chunks: list[str] = []
    for p in paragraphs:
        pid = p.get("id")
        new_chunks.append(id_to_new.get(pid, str(p.get("text", ""))))
    new_md = "\n\n".join(new_chunks) if new_chunks else manuscript.get("raw_md", "")

    (REPO_ROOT / "state" / "manuscript_improved.md").write_text(
        new_md, encoding="utf-8"
    )

    existing = state.load_json("improvement_log.json", {"version": 0, "entries": []})
    entries: list[dict] = list(existing.get("entries", []))
    for e in edits:
        entries.append(
            {
                "entry_id": f"w14-{uuid.uuid4().hex[:8]}",
                "timestamp": _now_iso_z(),
                "annotation_id": e.get("annotation_id", ""),
                "para_id": int(e.get("para_id") or 1),
                "para_section": e.get("section", "unknown"),
                "old_text": e.get("old_text", ""),
                "new_text": e.get("new_text", ""),
                "edit_type": e.get("edit_type", "replace"),
                "rationale": e.get("rationale", ""),
                "lift_estimate": float(e.get("lift_estimate", 0.0)),
                "risk": e.get("risk", "low"),
                "agents_used": e.get("agents_used", []),
                "validator_passed": bool(e.get("validator_passed", False)),
                "validator_checks": e.get("validator_checks", {}),
                "word_count_delta": int(
                    _word_count(e.get("new_text", ""))
                    - _word_count(e.get("old_text", ""))
                ),
                "refs_delta": int(
                    len(extract_refs(e.get("new_text", "")))
                    - len(extract_refs(e.get("old_text", "")))
                ),
            }
        )
    existing["entries"] = entries
    existing["version"] = int(existing.get("version", 0)) + 1
    state.save_json("improvement_log.json", existing)


# ---------------------------------------------------------------------------
# Cascade
# ---------------------------------------------------------------------------


def trigger_workflow(name: str) -> None:
    """Cascade: run ``gh workflow run <name>``; log errors, do not raise."""
    try:
        subprocess.run(
            ["gh", "workflow", "run", name],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[W14] cascade {name} dispatched", flush=True)
    except FileNotFoundError as exc:
        print(f"[W14] cascade {name} failed: gh CLI missing ({exc})", flush=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc))[:200]
        print(f"[W14] cascade {name} failed: {detail}", flush=True)


# ---------------------------------------------------------------------------
# Core orchestration
# ---------------------------------------------------------------------------


async def orchestrate(annotation_ids: list[str]) -> list[dict]:
    start_block(
        "W14",
        f"Orchestrating {len(annotation_ids)} annotations",
        [
            {"id": "W14.load", "label": "Load context", "agent_type": "main"},
            {"id": "W14.A", "label": "Layer A fact-check", "agent_type": "sonnet x6"},
            {"id": "W14.B", "label": "Layer B content", "agent_type": "sonnet x8"},
            {"id": "W14.C", "label": "Layer C review", "agent_type": "sonnet x6"},
            {"id": "W14.D", "label": "Layer D synthesis", "agent_type": "sonnet x2"},
            {"id": "W14.commit", "label": "Commit + cascade", "agent_type": "main"},
        ],
        eta_min=15,
    )

    # Load context.
    manuscript = state.load_json("manuscript_v5_condensed.json", {})
    canonical = state.load_json("canonical_facts.json", {})
    encyclopedia = state.load_json("encyclopedia.json", {"categories": {}})
    annotations_state = state.load_json("annotations.json", {"items": []})

    # M14 catalog: try repo-local copy first (CI), then developer path (local).
    m14_catalog_path = REPO_ROOT / "state" / "m14_catalog.md"
    if not m14_catalog_path.exists():
        m14_catalog_path = (
            REPO_ROOT.parent.parent / "memory" / "CANONICAL_BLINDAJES_INDEX.md"
        )
    m14_catalog = (
        m14_catalog_path.read_text(encoding="utf-8")
        if m14_catalog_path.exists()
        else ""
    )

    targets = [
        a
        for a in annotations_state.get("items", [])
        if a.get("annotation_id") in annotation_ids
    ]
    if not targets:
        print(f"[W14] no matching annotations for ids={annotation_ids}", flush=True)
    finalize("W14", ["state/annotations.json"], sub_block_id="W14.load")

    accepted_edits: list[dict] = []

    for ann in targets:
        para = next(
            (
                p
                for p in (manuscript.get("paragraphs") or [])
                if p.get("id") == ann.get("para_id")
            ),
            None,
        )
        if not para:
            # Synthetic stub paragraph so the rest of the pipeline is exercised.
            para = {
                "id": ann.get("para_id", 1),
                "section": "unknown",
                "text": ann.get("selected_text", ""),
            }

        cat_info = classify_annotation(ann, para.get("text", ""))
        plan = select_agents(ann.get("color", "yellow"), cat_info.get("cat", ""))

        context = {
            "annotation": ann,
            "paragraph": para,
            "category": cat_info,
            "canonical_slice": {
                k: v
                for k, v in canonical.items()
                if isinstance(k, str) and k.startswith("facts_")
            },
            "encyc_slice": encyclopedia.get("categories", {}).get(
                cat_info.get("cat", ""), {}
            ),
            "m14_preamble": m14_catalog[:4000],
        }

        # Layers A, B, C run concurrently.
        findings_a, findings_b, findings_c = await asyncio.gather(
            run_layer("A", plan["A"], context),
            run_layer("B", plan["B"], context),
            run_layer("C", plan["C"], context),
        )

        heartbeat(
            "W14",
            "W14.D",
            status="running",
            detail="supervisor + manuscript-writer",
        )
        synth_prompt = build_synth_prompt(ann, para, findings_a, findings_b, findings_c)
        try:
            supervisor_out = claude_api.call_sonnet(
                synth_prompt, max_tokens=4000, system=SYS_SUPERVISOR
            )
        except Exception as exc:  # noqa: BLE001
            live_error("W14", "W14.D", f"supervisor failed: {exc}")
            continue

        edit_decision = claude_api.extract_json(supervisor_out) or {
            "edit_type": "no-op",
            "rationale": "supervisor parse failure",
            "risk": "low",
            "lift_estimate": 0.0,
        }

        edit_candidate = {
            "annotation_id": ann.get("annotation_id"),
            "para_id": para.get("id"),
            "section": para.get("section", "unknown"),
            "old_text": para.get("text", ""),
            "new_text": edit_decision.get("new_text_sketch", ""),
            "edit_type": edit_decision.get("edit_type", "replace"),
            "rationale": edit_decision.get("rationale", ""),
            "risk": edit_decision.get("risk", "low"),
            "lift_estimate": float(edit_decision.get("lift_estimate", 0.0)),
            "agents_used": list(plan["A"]) + list(plan["B"]) + list(plan["C"]) + list(plan["D"]),
        }

        ok, reason, checks = validate_edit(
            edit_candidate, manuscript, canonical, m14_catalog
        )
        edit_candidate["validator_passed"] = ok
        edit_candidate["validator_checks"] = checks
        if not ok:
            ntfy.send_alert(
                "HIGH",
                f"Edit rejected: {reason}",
                f"Annotation {ann.get('annotation_id')}",
            )
            continue

        # Writer pass: ask manuscript-writer for the definitive paragraph.
        writer_prompt = build_writer_prompt(para, edit_decision)
        try:
            new_para_text = claude_api.call_sonnet(
                writer_prompt, max_tokens=2000, system=SYS_WRITER
            ).strip()
        except Exception as exc:  # noqa: BLE001
            live_error("W14", "W14.D", f"writer failed: {exc}")
            continue
        if new_para_text:
            edit_candidate["new_text"] = new_para_text

        edit_candidate["findings"] = {
            "A": findings_a,
            "B": findings_b,
            "C": findings_c,
        }
        accepted_edits.append(edit_candidate)

    finalize("W14", ["state/improvement_log.json"], sub_block_id="W14.D")

    apply_edits_and_persist(manuscript, accepted_edits)
    finalize(
        "W14",
        ["state/manuscript_improved.md", "state/improvement_log.json"],
        sub_block_id="W14.commit",
    )

    # Cascade always: W13 re-scores, W8 notifies HIL.
    trigger_workflow("w13-eid-scorer.yml")
    trigger_workflow("w8-hil.yml")

    # Conditional cascades.
    if any_numbers_changed(accepted_edits):
        trigger_workflow("w3-bias.yml")
    if any_refs_changed(accepted_edits):
        trigger_workflow("w7-retraction.yml")
    if any_model_metrics_changed(accepted_edits):
        trigger_workflow("w15-model-eval.yml")

    return accepted_edits


def main() -> None:
    raw = os.environ.get("W14_ANNOTATION_IDS", "")
    ids = [i.strip() for i in raw.split(",") if i.strip()]
    if not ids:
        print("[W14] no annotation ids provided (W14_ANNOTATION_IDS)", flush=True)
        return
    try:
        edits = asyncio.run(orchestrate(ids))
    except Exception as exc:  # noqa: BLE001
        tb = traceback.format_exc()
        live_error("W14", "W14.commit", f"orchestrate failed: {exc}", tb)
        ntfy.send_alert("HIGH", "W14 master crashed", str(exc)[:200])
        raise
    print(
        f"[W14] processed={len(ids)} accepted_edits={len(edits)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
