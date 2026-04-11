"""EID manuscript scoring library (stub).

This module provides the scoring scaffolding used by ``scripts/w13_eid_scorer.py``
to estimate the probability that a Hantavirus Nuble manuscript is accepted at
the target journal (Emerging Infectious Diseases, CDC).

The score is a logistic regression over 11 quality components. The intercept
``beta_0`` encodes the baseline prior ``Beta(7, 18)`` with mean 0.28, i.e.
``beta_0 = ln(0.28 / 0.72) ~= -0.9444616``.

Formula:
    score_EID = sigmoid(beta_0 + sum_i beta_i * f_i(manuscript))  in [0, 1]

NOTE: This file is a STUB. Every ``score_*`` function returns a hard-coded
fake value so that downstream smoke tests can run end-to-end. Real
implementations (Claude agent calls, MCP lookups, regex/keyword matching,
embedding distance, etc.) will live in ``scripts/w13_eid_scorer.py`` and will
be wired in by worker B5.3.
"""

from __future__ import annotations

import math
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Logistic intercept. Prior Beta(7, 18) -> mean 0.28 -> ln(0.28 / 0.72).
BETA_0: float = -0.9444616

# Weights calibrated manually from the M14 catalog. Must sum to 1.0.
WEIGHTS: dict[str, float] = {
    "strobe": 0.12,
    "tripod_ai": 0.10,
    "epiforge": 0.08,
    "stat_rigor": 0.12,
    "reproducibility": 0.08,
    "novelty": 0.10,
    "writing_quality": 0.08,
    "ref_quality": 0.08,
    "bias_coverage": 0.08,
    "reviewer_anticipation": 0.08,
    "journal_fit_eid": 0.08,
}

# Fail fast at import time if the weights are ever edited inconsistently.
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, (
    f"WEIGHTS must sum to 1.0, got {sum(WEIGHTS.values())!r}"
)


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------


def sigmoid(x: float) -> float:
    """Compute the logistic sigmoid.

    Args:
        x: Real-valued logit.

    Returns:
        ``1 / (1 + exp(-x))`` in ``(0, 1)``.
    """
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x: float) -> float:
    """Compute the derivative of the logistic sigmoid.

    Args:
        x: Real-valued logit.

    Returns:
        ``sigma(x) * (1 - sigma(x))``, used for local lift estimates.
    """
    s = sigmoid(x)
    return s * (1.0 - s)


# ---------------------------------------------------------------------------
# Component scorers (STUBS)
#
# Each function accepts the shape it will receive in production and returns
# a constant fake score. Real logic will be filled in by B5.3.
# ---------------------------------------------------------------------------


def score_strobe(manuscript_json: dict) -> float:
    """Compute fraction of STROBE 22 items satisfied.

    Args:
        manuscript_json: Parsed manuscript with ``sections``, ``tables``, etc.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.91``.
    """
    return 0.91


def score_tripod_ai(manuscript_json: dict) -> float:
    """Compute fraction of TRIPOD+AI 27 items satisfied.

    Args:
        manuscript_json: Parsed manuscript with model-reporting fields.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.89``.
    """
    return 0.89


def score_epiforge(manuscript_json: dict) -> float:
    """Compute fraction of EPIFORGE 18 items satisfied.

    Args:
        manuscript_json: Parsed manuscript with forecasting sections.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``1.00``.
    """
    return 1.00


def score_stat_rigor(manuscript_json: dict) -> float:
    """Score statistical rigor (CI reporting, assumptions, validation).

    Args:
        manuscript_json: Parsed manuscript with statistics subsections.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.85``.
    """
    return 0.85


def score_reproducibility(manuscript_json: dict) -> float:
    """Score reproducibility as ``(code + data + env_pinned) / 3``.

    Args:
        manuscript_json: Parsed manuscript with data/code availability block.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``1.00``.
    """
    return 1.00


def score_novelty(
    manuscript_json: dict,
    top_biorxiv: list[dict] | None = None,
) -> float:
    """Score novelty as semantic distance to top-5 bioRxiv hantavirus preprints.

    Args:
        manuscript_json: Parsed manuscript (abstract + contributions).
        top_biorxiv: Optional list of recent bioRxiv preprint metadata dicts
            (2024-2025 hantavirus). When ``None`` the real implementation
            pulls them via MCP; the stub ignores this argument.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.62``.
    """
    return 0.62


def score_writing_quality(manuscript_json: dict) -> float:
    """Aggregate writing quality from red-team and paper-review agents.

    Args:
        manuscript_json: Parsed manuscript.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.80``.
    """
    return 0.80


def score_ref_quality(refs: list[dict]) -> float:
    """Score reference quality as ``pct_<=5y * pct_Q1 * pct_not_retracted``.

    Args:
        refs: List of reference dicts with ``year``, ``journal_quartile``,
            and ``retracted`` fields.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.88``.
    """
    return 0.88


def score_bias_coverage(
    m14_catalog: dict,
    bias_findings: list[dict],
) -> float:
    """Fraction of the 14 M14 blindings actually covered in the manuscript.

    Args:
        m14_catalog: Parsed ``project_S55_sesgos_56_completos.md`` catalog
            (or equivalent) keyed by bias id.
        bias_findings: Auditor agent findings listing which bias ids were
            referenced in the current manuscript.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.93``.
    """
    return 0.93


def score_reviewer_anticipation(reviewer_objections: list[dict]) -> float:
    """Score reviewer anticipation as ``anticipated / total`` attacks.

    Args:
        reviewer_objections: List of objection dicts produced by the
            reviewer-simulator agent, each with an ``anticipated`` bool.

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.75``.
    """
    return 0.75


def score_journal_fit_eid(manuscript_json: dict) -> float:
    """Score fit with EID aims/scope via regex + keyword overlap.

    Args:
        manuscript_json: Parsed manuscript (title, abstract, keywords).

    Returns:
        Score in ``[0, 1]``. STUB: returns ``0.85``.
    """
    return 0.85


# ---------------------------------------------------------------------------
# Aggregation + lift ranking
# ---------------------------------------------------------------------------


def aggregate(features: dict[str, float]) -> float:
    """Compute the final EID score via the logistic formula.

    Args:
        features: Dict with the 11 keys of ``WEIGHTS`` mapped to values in
            ``[0, 1]``. Missing keys are treated as ``0.0``.

    Returns:
        ``sigmoid(beta_0 + sum_i w_i * f_i)`` in ``[0, 1]``.
    """
    linear = BETA_0
    for name, weight in WEIGHTS.items():
        linear += weight * features.get(name, 0.0)
    return sigmoid(linear)


def compute_lift_ranking(
    features: dict[str, float],
    max_feasible: dict[str, float] | None = None,
) -> list[dict]:
    """Rank components by local lift on the final score.

    For each component ``i`` we compute the local marginal effect of pushing
    the feature to its feasible ceiling:

        lift_i = beta_i * sigma'(x) * (max_feasible_i - current_i)

    where ``x`` is the current linear combination and
    ``sigma'(x) = sigma(x) * (1 - sigma(x))``.

    Args:
        features: Current feature values (must contain the ``WEIGHTS`` keys).
        max_feasible: Optional feasibility ceiling per feature. Defaults to
            ``1.0`` for every component when ``None``.

    Returns:
        List of dicts ``{"component", "value", "weight", "lift"}`` sorted
        descending by ``lift``.
    """
    if max_feasible is None:
        max_feasible = {k: 1.0 for k in WEIGHTS}

    linear = BETA_0 + sum(
        WEIGHTS[k] * features.get(k, 0.0) for k in WEIGHTS
    )
    sigma_prime = sigmoid_derivative(linear)

    ranking: list[dict] = []
    for name, weight in WEIGHTS.items():
        current = features.get(name, 0.0)
        headroom = max(0.0, max_feasible.get(name, 1.0) - current)
        lift = weight * sigma_prime * headroom
        ranking.append(
            {
                "component": name,
                "value": current,
                "weight": weight,
                "lift": lift,
            }
        )

    ranking.sort(key=lambda r: r["lift"], reverse=True)
    return ranking


# ---------------------------------------------------------------------------
# Top-level API
# ---------------------------------------------------------------------------


def score_manuscript(
    manuscript_json: dict,
    refs: list[dict] | None = None,
    m14_catalog: dict | None = None,
    bias_findings: list[dict] | None = None,
    reviewer_objections: list[dict] | None = None,
    top_biorxiv: list[dict] | None = None,
) -> dict:
    """Compute the full EID score, per-component lifts, and a payload dict.

    STUB: uses the constant component scores defined above. The real
    implementation in ``scripts/w13_eid_scorer.py`` orchestrates asyncio
    Claude agents and MCP lookups before delegating the numeric aggregation
    to :func:`aggregate` and :func:`compute_lift_ranking`.

    Args:
        manuscript_json: Parsed manuscript payload.
        refs: Optional list of reference dicts. Defaults to empty list.
        m14_catalog: Optional M14 bias catalog. Defaults to empty dict.
        bias_findings: Optional list of bias findings. Defaults to empty list.
        reviewer_objections: Optional list of reviewer objections. Defaults
            to empty list.
        top_biorxiv: Optional list of top bioRxiv hantavirus preprints.

    Returns:
        A dict following ``state/schemas/eid_score.schema.json`` with the
        final score, baseline delta, per-component breakdown, lift ranking,
        top-3 recommendations (empty in the stub), and logit params.
    """
    features: dict[str, float] = {
        "strobe": score_strobe(manuscript_json),
        "tripod_ai": score_tripod_ai(manuscript_json),
        "epiforge": score_epiforge(manuscript_json),
        "stat_rigor": score_stat_rigor(manuscript_json),
        "reproducibility": score_reproducibility(manuscript_json),
        "novelty": score_novelty(manuscript_json, top_biorxiv),
        "writing_quality": score_writing_quality(manuscript_json),
        "ref_quality": score_ref_quality(refs or []),
        "bias_coverage": score_bias_coverage(
            m14_catalog or {}, bias_findings or []
        ),
        "reviewer_anticipation": score_reviewer_anticipation(
            reviewer_objections or []
        ),
        "journal_fit_eid": score_journal_fit_eid(manuscript_json),
    }

    score = aggregate(features)
    ranking = compute_lift_ranking(features)
    lift_by_component = {r["component"]: r["lift"] for r in ranking}

    components_payload: list[dict[str, Any]] = [
        {
            "i": i + 1,
            "name": name,
            "value": features[name],
            "weight": WEIGHTS[name],
            "lift": lift_by_component[name],
        }
        for i, name in enumerate(WEIGHTS)
    ]

    return {
        "version": 1,
        "score": score,
        "baseline_prior": 0.28,
        "delta_vs_baseline": score - 0.28,
        "components": components_payload,
        "ranking_lift": [r["component"] for r in ranking],
        "top3_recommendations": [],  # stub: populated by B5.3
        "logit_params": {
            "beta0": BETA_0,
            "betas": list(WEIGHTS.values()),
        },
    }


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import json

    result = score_manuscript({}, [], {}, [], [], [])
    print(json.dumps(result, indent=2))
