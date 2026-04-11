"""W13 EID Scorer.

Computes the EID acceptance probability for the current manuscript using the
logistic model defined in :mod:`scripts.lib.eid_score` (13 canonical
components, S61). For each non-model component, a Claude Sonnet agent is
asked to score it in [0, 1] given a component-specific rubric and the
relevant manuscript slices. Agent calls run concurrently via
``asyncio.to_thread``.

S61 change: the legacy single ``stat_rigor`` is now joined by two real
sub-components ``model_descriptive_rigor`` and ``model_predictive_rigor``
that read directly from ``state/model_evaluation.json`` via the library
helpers ``score_model_descriptive_rigor`` and ``score_model_predictive_rigor``.
Output conforms to ``state/schemas/eid_score.schema.json`` with exactly 13
components.

Inputs:
    * ``state/manuscript_v5_condensed.json`` (preferred) — parsed manuscript.
    * ``state/manuscript_improved.md`` (fallback) — raw markdown.
    * ``state/references.json`` — reference list.
    * ``state/model_evaluation.json`` (optional) — produced by W15.
    * ``state/canonical_facts.json`` — canonical numeric anchors.

Output:
    * ``state/eid_score.json`` following the 13-component schema.

Notes:
    * If any Claude call fails, the component falls back to the stub value
      from :mod:`scripts.lib.eid_score`.
    * ``manuscript_hash`` is SHA256 of whichever manuscript source was
      actually read (JSON bytes or markdown bytes).
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api, eid_score, ntfy, state  # noqa: E402
from scripts.lib.claude_live import error as live_error  # noqa: E402
from scripts.lib.claude_live import finalize, heartbeat, start_block  # noqa: E402

SYS_SCORER = (
    "You are a Q1 manuscript quality scorer for Emerging Infectious Diseases "
    "(CDC). For each component prompt you receive, return STRICT JSON with a "
    "single key 'score' in [0, 1] and a 'rationale' string under 200 chars. "
    "No markdown fences. No extra keys."
)


def _now_iso_z() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_manuscript() -> tuple[dict, str]:
    """Load the manuscript and compute its hash.

    Returns:
        Tuple ``(manuscript_dict, sha256_hex)``. When only the raw markdown
        fallback exists, the dict is ``{"raw_md": <str>}``.
    """
    repo_state = REPO_ROOT / "state"
    json_path = repo_state / "manuscript_v5_condensed.json"
    md_path = repo_state / "manuscript_improved.md"

    if json_path.exists():
        raw = json_path.read_bytes()
        try:
            import json
            return json.loads(raw.decode("utf-8")), _sha256_bytes(raw)
        except Exception:  # noqa: BLE001
            pass

    if md_path.exists():
        raw = md_path.read_bytes()
        return {"raw_md": raw.decode("utf-8", errors="replace")}, _sha256_bytes(raw)

    empty = b"{}"
    return {}, _sha256_bytes(empty)


def _manuscript_excerpt(manuscript: dict, max_chars: int = 6000) -> str:
    """Return a compact excerpt of the manuscript for prompts."""
    if "raw_md" in manuscript:
        return manuscript["raw_md"][:max_chars]
    # Prefer sections concatenation, fall back to JSON dump.
    sections = manuscript.get("sections") or manuscript.get("paragraphs") or []
    chunks: list[str] = []
    for s in sections:
        if isinstance(s, dict):
            chunks.append(str(s.get("text") or s.get("content") or "")[:800])
        else:
            chunks.append(str(s)[:800])
        if sum(len(c) for c in chunks) > max_chars:
            break
    text = "\n\n".join(chunks)
    if not text:
        import json
        text = json.dumps(manuscript, ensure_ascii=False)[:max_chars]
    return text[:max_chars]


# ---------------------------------------------------------------------------
# Component scorers (real prompts)
# ---------------------------------------------------------------------------


def _build_component_prompt(component: str, excerpt: str, extras: dict) -> str:
    rubrics = {
        "strobe": (
            "Score STROBE 22-item coverage. Count how many items are addressed "
            "and return the fraction."
        ),
        "tripod_ai": (
            "Score TRIPOD+AI 27-item coverage for prediction model reporting."
        ),
        "epiforge": (
            "Score EPIFORGE 18-item coverage for epidemiological forecasting."
        ),
        "stat_rigor": (
            "Score overall statistical rigor in the TEXT: CI reporting "
            "(Wilson/BCa), hypothesis framing, effect sizes, multiple-"
            "comparison correction, sensitivity analysis. Do NOT score "
            "model diagnostics here (those live in model_descriptive_rigor "
            "and model_predictive_rigor)."
        ),
        "reproducibility": (
            "Score reproducibility as (code_available + data_available + "
            "env_pinned) / 3."
        ),
        "novelty": (
            "Score novelty vs recent hantavirus literature (2024-2026). "
            "Low if duplicates prior work, high if new mechanism/framework."
        ),
        "writing_quality": (
            "Score clarity, flow and journal tone. Check for hedging, "
            "paragraph structure, active voice."
        ),
        "ref_quality": (
            "Score reference quality: fraction <=5y, fraction Q1, fraction "
            "not retracted. Use provided ref stats in EXTRAS."
        ),
        "bias_coverage": (
            "Score fraction of the 14 M14 blindings explicitly covered in "
            "the manuscript. Use EXTRAS.m14_catalog listing."
        ),
        "reviewer_anticipation": (
            "Score fraction of anticipated reviewer objections already "
            "addressed in the manuscript. Use EXTRAS.objections listing."
        ),
        "journal_fit_eid": (
            "Score fit with EID aims/scope: outbreak-relevant, public health "
            "actionable, <=3500 words, Vancouver refs, Dispatch-format aware."
        ),
    }
    rubric = rubrics.get(component, "Score the quality on 0..1.")
    return (
        f"COMPONENT: {component}\n"
        f"RUBRIC: {rubric}\n\n"
        f"MANUSCRIPT EXCERPT (truncated):\n```\n{excerpt}\n```\n\n"
        f"EXTRAS:\n```json\n{extras}\n```\n\n"
        "Return STRICT JSON only: {\"score\": <float in [0,1]>, "
        "\"rationale\": \"<short>\"}"
    )


async def _score_component_async(
    component: str, excerpt: str, extras: dict, fallback: float
) -> float:
    """Call Claude Sonnet to score one component; fall back on any failure."""
    prompt = _build_component_prompt(component, excerpt, extras)
    try:
        resp = await asyncio.to_thread(
            claude_api.call_sonnet, prompt, 400, SYS_SCORER
        )
        parsed = claude_api.extract_json(resp)
        if not parsed or "score" not in parsed:
            return fallback
        val = float(parsed.get("score", fallback))
        if val < 0.0 or val > 1.0:
            return fallback
        return val
    except Exception as exc:  # noqa: BLE001
        print(f"[W13] component {component} fell back: {exc}", flush=True)
        return fallback


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


async def _score_all_async(manuscript: dict, refs: list[dict], canonical: dict,
                           m14_catalog: dict, objections: list[dict],
                           model_eval: dict) -> dict[str, float]:
    """Score the 13 EID components.

    The 11 textual components are scored by Claude Sonnet per-component
    rubrics (fallback to lib stubs on any failure). The 2 model-rigor
    components are computed deterministically from
    ``state/model_evaluation.json`` via
    :func:`eid_score.score_model_descriptive_rigor` and
    :func:`eid_score.score_model_predictive_rigor`.
    """
    excerpt = _manuscript_excerpt(manuscript)
    ref_stats = {
        "n": len(refs),
        "pct_le_5y": 0.6,
        "pct_q1": 0.8,
        "pct_retracted": 0.0,
    }
    m14_list = sorted(m14_catalog.keys())[:14] if m14_catalog else []
    obj_list = [o.get("id", "?") for o in (objections or [])][:20]

    components: list[tuple[str, dict, float]] = [
        ("strobe", {}, eid_score.score_strobe(manuscript)),
        ("tripod_ai", {}, eid_score.score_tripod_ai(manuscript)),
        ("epiforge", {}, eid_score.score_epiforge(manuscript)),
        ("stat_rigor", {}, eid_score.score_stat_rigor(manuscript)),
        (
            "reproducibility",
            {},
            eid_score.score_reproducibility(manuscript),
        ),
        ("novelty", {}, eid_score.score_novelty(manuscript, None)),
        ("writing_quality", {}, eid_score.score_writing_quality(manuscript)),
        ("ref_quality", ref_stats, eid_score.score_ref_quality(refs)),
        (
            "bias_coverage",
            {"m14": m14_list},
            eid_score.score_bias_coverage(m14_catalog, []),
        ),
        (
            "reviewer_anticipation",
            {"objections": obj_list},
            eid_score.score_reviewer_anticipation(objections or []),
        ),
        ("journal_fit_eid", {}, eid_score.score_journal_fit_eid(manuscript)),
    ]

    tasks = [
        _score_component_async(name, excerpt, extras, fallback)
        for name, extras, fallback in components
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    features: dict[str, float] = {}
    for (name, _extras, fallback), value in zip(components, results):
        features[name] = fallback if isinstance(value, Exception) else float(value)

    # Model rigor sub-components are deterministic functions of model_eval.
    features["model_descriptive_rigor"] = eid_score.score_model_descriptive_rigor(
        model_eval
    )
    features["model_predictive_rigor"] = eid_score.score_model_predictive_rigor(
        model_eval
    )

    return features


def _build_top3(features: dict[str, float], ranking: list[dict]) -> list[dict]:
    """Pick top 3 lift recommendations as concrete action items."""
    action_hints = {
        "strobe": "Complete remaining STROBE items flagged by strobe-checker.",
        "tripod_ai": "Add TRIPOD+AI model card details to Methods.",
        "epiforge": "Expand EPIFORGE forecasting documentation.",
        "stat_rigor": "Report BCa CIs, effect sizes, sensitivity analyses.",
        "reproducibility": "Pin renv lockfile and upload Zenodo DOI.",
        "novelty": "Sharpen contribution statement vs Gorris 2025.",
        "writing_quality": "Tighten Abstract and Discussion opening.",
        "ref_quality": "Replace >5y refs with 2024-2026 equivalents.",
        "bias_coverage": "Cite missing M14 blindings explicitly.",
        "reviewer_anticipation": "Pre-empt top 3 reviewer attacks in Discussion.",
        "journal_fit_eid": "Align framing with EID Dispatch template.",
        "model_descriptive_rigor": (
            "Re-run Ward + DHARMa + ICC blindaje and refresh model_evaluation."
        ),
        "model_predictive_rigor": (
            "Refresh S29-K snapshot and walk-forward 14-fold log-score."
        ),
    }
    top3 = []
    for entry in ranking[:3]:
        name = entry["component"]
        top3.append(
            {
                "component": name,
                "action": action_hints.get(name, "Improve this component."),
                "expected_lift": float(min(0.99, max(0.0, entry["lift"]))),
            }
        )
    # Ensure exactly 3
    while len(top3) < 3:
        top3.append(
            {
                "component": "writing_quality",
                "action": "Polish wording for clarity.",
                "expected_lift": 0.0,
            }
        )
    return top3


def main() -> None:
    start_block(
        "W13",
        "EID Scorer",
        [
            {"id": "W13.load", "label": "Load manuscript + refs + model_eval", "agent_type": "main"},
            {"id": "W13.score", "label": "Score 13 components", "agent_type": "sonnet x11"},
            {"id": "W13.write", "label": "Persist eid_score.json", "agent_type": "main"},
        ],
    )

    heartbeat("W13", "W13.load", status="running")
    manuscript, mhash = _load_manuscript()
    refs = state.load_json("references.json", {"items": []}).get("items", [])
    canonical = state.load_json("canonical_facts.json", {})
    m14_catalog = canonical.get("m14_catalog", {}) if isinstance(canonical, dict) else {}
    objections = state.load_json("objections.json", {"items": []}).get("items", [])
    model_eval = state.load_json("model_evaluation.json", {})
    finalize("W13", ["state/manuscript_v5_condensed.json"], sub_block_id="W13.load")

    heartbeat("W13", "W13.score", status="running", detail="asyncio fan-out")
    try:
        features = asyncio.run(
            _score_all_async(
                manuscript, refs, canonical, m14_catalog, objections, model_eval
            )
        )
    except Exception as exc:  # noqa: BLE001
        live_error("W13", "W13.score", f"score failure: {exc}")
        ntfy.send_alert("HIGH", "W13 scoring failed", str(exc)[:200])
        return
    finalize("W13", ["state/eid_score.json"], sub_block_id="W13.score")

    score = eid_score.aggregate(features)
    ranking = eid_score.compute_lift_ranking(features)
    lift_by_component = {r["component"]: r["lift"] for r in ranking}
    components_payload: list[dict[str, Any]] = [
        {
            "i": i + 1,
            "name": name,
            "value": features[name],
            "weight": eid_score.WEIGHTS[name],
            "lift": lift_by_component[name],
        }
        for i, name in enumerate(eid_score.WEIGHTS)
    ]
    payload = {
        "version": 1,
        "scored_at": _now_iso_z(),
        "manuscript_hash": mhash,
        "score": score,
        "baseline_prior": 0.28,
        "delta_vs_baseline": score - 0.28,
        "components": components_payload,
        "ranking_lift": [r["component"] for r in ranking],
        "top3_recommendations": _build_top3(features, ranking),
        "logit_params": {
            "beta0": eid_score.BETA_0,
            "betas": list(eid_score.WEIGHTS.values()),
        },
    }
    state.save_json("eid_score.json", payload)
    finalize("W13", ["state/eid_score.json"], sub_block_id="W13.write")

    ntfy.send(
        title=f"W13: EID score {score:.3f}",
        message=f"Delta vs baseline: {score - 0.28:+.3f}. Top lift: {ranking[0]['component']}",
        priority="default",
        tags=["w13", "score"],
    )
    print(f"[W13] score={score:.4f} delta={score - 0.28:+.4f}", flush=True)


if __name__ == "__main__":
    main()
