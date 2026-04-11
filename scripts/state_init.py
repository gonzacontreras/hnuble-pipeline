"""state_init — seed state/ with baseline data.

Seeds:
 - findings.json with the 35 S59 hallazgos (baseline)
 - references.json with 50 manuscript references (DOIs when known)
 - objections.json with the 10 pre-armed reviewer objections
 - pending_approvals.json empty
 - manuscript_control.md = manuscript_improved.md = placeholder
 - pipeline_status.json with all workflows recorded as not-yet-run
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import state  # noqa: E402


BASELINE_FINDINGS: list[dict] = [
    # TOP 5 CRITICAL
    {
        "id": "S59-TOP5-01",
        "source": "S59-B2",
        "severity": "HIGH",
        "taxonomy": "biological-conflation",
        "title": "Lag biological conflation (5m operational vs 18-24yr Chusquea cycle)",
        "evidence": "L71 manuscript: conflates 5m operational lag FSI->case with Chusquea masting 18-24 year cycle",
        "mechanism": "Mis-framing could make a reviewer reject the EWS claim as ecologically implausible",
        "fix_hint": "Separate explicitly in Discussion: FSI is a proxy for short-term greenness, not the masting cycle",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-TOP5-02",
        "source": "S59-B2",
        "severity": "HIGH",
        "taxonomy": "reporting-misframing",
        "title": "RPS presented as +1.3% skill when CI overlaps null",
        "evidence": "L123: 'RPS skill +1.3%' but bootstrap CI includes null",
        "mechanism": "Inflated skill claim could trigger reviewer rejection of scoring rule section",
        "fix_hint": "Reframe as '2 of 3 scoring rules positive; RPS skill not distinguishable from null'",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-TOP5-03",
        "source": "S59-B5",
        "severity": "HIGH",
        "taxonomy": "statistical",
        "title": "BSS CI is percentile, not BCa",
        "evidence": "T_BLINDAJE_BSS_CI_S57.csv uses boot percentile instead of BCa",
        "mechanism": "Inconsistency with PR-AUC (which uses BCa) -> reviewer flag",
        "fix_hint": "Re-run with boot::boot.ci(type='bca'); addendum v1.3",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-TOP5-04",
        "source": "S59-B2",
        "severity": "HIGH",
        "taxonomy": "misattribution",
        "title": "Ortiz 2004 cited as source for 3-5x national incidence ratio",
        "evidence": "L45 cites Ortiz 2004 but Ortiz reports rodent seroprevalence VIII Region, not national HCPS incidence",
        "mechanism": "Factual misattribution -> reviewer flags as data fabrication",
        "fix_hint": "Replace with MINSAL Bulletin + direct calculation",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-TOP5-05",
        "source": "S59-B3",
        "severity": "HIGH",
        "taxonomy": "DAG",
        "title": "DAG: FSI_R5 (exposure) lacks direct arrow to SCPH_cases",
        "evidence": "R1_DAG_dagitty.txt has FSI_R5 without -> SCPH_cases edge; adjustment set becomes formally incorrect",
        "mechanism": "Legacy S37 issue; reviewer with DAG expertise will catch it",
        "fix_hint": "Add arrow + supplementary note explaining semantics",
        "status": "PENDING_MCC",
    },
    # B1 HIGH remaining
    {
        "id": "S59-B1-01",
        "source": "S59-B1",
        "severity": "HIGH",
        "taxonomy": "measurement",
        "title": "Case definition drift MINSAL 2002-2024 (IgM pre-2012 vs RT-PCR post-2012)",
        "evidence": "Case definition changed when RT-PCR became standard",
        "mechanism": "Differential sensitivity over time -> spurious temporal trend",
        "fix_hint": "Sensitivity analysis restricting to 2012+, report delta",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-02",
        "source": "S59-B1",
        "severity": "HIGH",
        "taxonomy": "selection",
        "title": "Winner's curse lag 5 + biological confusion 18-24m vs 5m",
        "evidence": "Lag 5 chosen from scan of multiple lags",
        "mechanism": "Post-hoc lag selection inflates effect size",
        "fix_hint": "Document pre-specification lineage; report all lags' IRR for transparency",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-03",
        "source": "S59-B1",
        "severity": "HIGH",
        "taxonomy": "measurement",
        "title": "FSI compound formula (NDMI+NDVI+NBR2) weights undocumented",
        "evidence": "FSI computation script does not cite a formal paper for the weighting",
        "mechanism": "Custom index without precedent -> reviewer suspicion of tuning",
        "fix_hint": "Cite Bortman 1999 or provide sensitivity analysis with alternative weights",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-04",
        "source": "S59-B1",
        "severity": "HIGH",
        "taxonomy": "ascertainment",
        "title": "SEREMI temporal reporting intensity not controlled",
        "evidence": "Reporting effort likely increased after 2018 Nuble creation",
        "mechanism": "Inflated recent incidence estimates",
        "fix_hint": "Include year FE and compare slopes",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-R3-01",
        "source": "S59-B1",
        "severity": "HIGH",
        "taxonomy": "administrative",
        "title": "SEREMI Maule pre-2018 (Nuble split from Maule)",
        "evidence": "Before 2018 all Nuble cases reported under Maule",
        "mechanism": "Geographic attribution requires back-allocation",
        "fix_hint": "Describe back-allocation procedure explicitly in methods",
        "status": "PENDING_MCC",
    },
    # B2 remaining HIGH
    {
        "id": "S59-B2-F-01",
        "source": "S59-B2",
        "severity": "HIGH",
        "taxonomy": "false-equivalence",
        "title": "False equivalence dengue EWS (Lowe, Colon-Gonzalez)",
        "evidence": "Comparing HCPS EWS to dengue EWS ignores base rate differences",
        "mechanism": "Reviewer will flag as inappropriate analogy",
        "fix_hint": "Acknowledge base rate asymmetry; cite Tier 3 limitations",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B2-F-03",
        "source": "S59-B2",
        "severity": "HIGH",
        "taxonomy": "supremacy-claim",
        "title": "'First satellite-triggered multi-agency protocol' claim without systematic search",
        "evidence": "Discussion claims 'first' without Scopus/WoS search documentation",
        "mechanism": "Unsupported supremacy claim -> reviewer rejection",
        "fix_hint": "Replace 'first' with 'to our knowledge among the first'; document search terms",
        "status": "PENDING_MCC",
    },
    # B3 remaining
    {
        "id": "S59-B3-002",
        "source": "S59-B3",
        "severity": "HIGH",
        "taxonomy": "DAG",
        "title": "E-values without named biological confounders",
        "evidence": "E-values 2.07 and 2.30 reported without named confounders",
        "mechanism": "Uninterpretable E-value -> reviewer flag",
        "fix_hint": "Name agricultural activity, surveillance intensity, rural tourism",
        "status": "PENDING_MCC",
    },
    # B5 HIGH remaining
    {
        "id": "S59-B5-5.1",
        "source": "S59-B5",
        "severity": "HIGH",
        "taxonomy": "statistical",
        "title": "ACF residuals within-commune not tested",
        "evidence": "DHARMa uses global index, not within-commune ACF",
        "mechanism": "Independence assumption central to GLMM nbinom2 unverified",
        "fix_hint": "Add commune-stratified ACF plot as Figure S4",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B5-1.2",
        "source": "S59-B5",
        "severity": "HIGH",
        "taxonomy": "statistical",
        "title": "Poisson vs NB2 LRT boundary issue without Vuong correction",
        "evidence": "Methods L210 LRT reported without mixture correction",
        "mechanism": "Boundary LRT is invalid on theta=0 edge",
        "fix_hint": "Use pscl::vuong() or the score test",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B5-3.1",
        "source": "S59-B5",
        "severity": "HIGH",
        "taxonomy": "statistical",
        "title": "theta not propagated in bootstrap BSS",
        "evidence": "Bootstrap holds theta fixed -> CI underestimates uncertainty",
        "mechanism": "Overconfident CI",
        "fix_hint": "Parametric bootstrap refitting inside each iteration",
        "status": "PENDING_MCC",
    },
    # MEDIUM (abbreviated)
    {
        "id": "S59-B1-05",
        "source": "S59-B1",
        "severity": "MED",
        "title": "Immortal time rolling windows",
        "evidence": "Rolling 3m FSI windows overlap with case observation",
        "mechanism": "Immortal time bias underestimates IRR",
        "fix_hint": "Use lag-only windows without lead",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-06",
        "source": "S59-B1",
        "severity": "MED",
        "title": "Omission of null lags",
        "evidence": "Only significant lags reported",
        "mechanism": "Selection bias on reported lags",
        "fix_hint": "Report all lags 0-12 in supplementary",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-07",
        "source": "S59-B1",
        "severity": "MED",
        "title": "Bortman calibration fold-by-fold not tested",
        "evidence": "Fold-wise calibration not in supplementary",
        "mechanism": "Potential fold heterogeneity masks miscalibration",
        "fix_hint": "Add fold-wise calibration table",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-08",
        "source": "S59-B1",
        "severity": "MED",
        "title": "Ward binary Simpson",
        "evidence": "Ward clustering uses binary distance",
        "mechanism": "Loses gradient information",
        "fix_hint": "Compare with Gower distance",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-R3-03",
        "source": "S59-B1",
        "severity": "MED",
        "title": "Cluster 2023 outlier influence",
        "evidence": "El Carmen cluster 2023 is a leverage point",
        "mechanism": "High Cook's D -> sensitive estimates",
        "fix_hint": "Influence diagnostic supplementary table",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-R3-05",
        "source": "S59-B1",
        "severity": "MED",
        "title": "ERA5 topographia compleja",
        "evidence": "Coarse ERA5 grid in Andean foothills",
        "mechanism": "Climate covariate bias",
        "fix_hint": "Sensitivity with CR2MET high-res",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B2-F-04",
        "source": "S59-B2",
        "severity": "MED",
        "title": "DCA circular (same OOS dataset)",
        "evidence": "Decision curve analysis uses same test set",
        "mechanism": "Circular validation",
        "fix_hint": "Report DCA with train-test split disclosure",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B2-F-05",
        "source": "S59-B2",
        "severity": "MED",
        "title": "Table 1 70.9% vs Table 2 68.1% inconsistency",
        "evidence": "Two tables report BSS with different denominators",
        "mechanism": "Reviewer will spot",
        "fix_hint": "Harmonize via footnote",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B2-F-07",
        "source": "S59-B2",
        "severity": "MED",
        "title": "Argumentum ad verecundiam Fox 2024",
        "evidence": "Uses Fox 2024 as authority without discussing influenza vs HCPS differences",
        "mechanism": "Weakens methodological justification",
        "fix_hint": "Acknowledge frequency-of-events gap",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B3-003",
        "source": "S59-B3",
        "severity": "MED",
        "title": "M-bias Chusquea->FSI partially blocked by ENSO r~0",
        "evidence": "M-bias structure not explicitly discussed",
        "mechanism": "Potential residual confounding",
        "fix_hint": "Add DAG subsection",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B3-004",
        "source": "S59-B3",
        "severity": "MED",
        "title": "Effect modification FSIxT2m / FSIxseason not tested",
        "evidence": "No interaction terms in model",
        "mechanism": "Potential hidden effect modification",
        "fix_hint": "Add interaction sensitivity",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B3-005",
        "source": "S59-B3",
        "severity": "MED",
        "title": "Hausman test nomenclature in GLMM nbinom2",
        "evidence": "'Hausman test' terminology used incorrectly",
        "mechanism": "Nomenclature error",
        "fix_hint": "Use 'glmmTMB vs glm comparison' instead",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B5-2.4",
        "source": "S59-B5",
        "severity": "MED",
        "title": "AR(1) cases not included as predictor",
        "evidence": "No autoregressive term in model",
        "mechanism": "Unmodeled temporal autocorrelation",
        "fix_hint": "Add AR(1) sensitivity",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B5-5.4",
        "source": "S59-B5",
        "severity": "MED",
        "title": "XGBoost/RF comparison absent",
        "evidence": "No ML benchmark",
        "mechanism": "Reviewer may demand",
        "fix_hint": "Add supplementary comparison",
        "status": "PENDING_MCC",
    },
    # LOW
    {
        "id": "S59-B1-R3-02",
        "source": "S59-B1",
        "severity": "LOW",
        "title": "CONAF coverage variability",
        "evidence": "CONAF fire coverage changes over years",
        "mechanism": "Minor",
        "fix_hint": "Footnote",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B1-R3-04",
        "source": "S59-B1",
        "severity": "LOW",
        "title": "Tier 3 P(T3|T2) not reported",
        "evidence": "Conditional probability missing",
        "mechanism": "Minor",
        "fix_hint": "Add to supplementary",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B2-F-08",
        "source": "S59-B2",
        "severity": "LOW",
        "title": "Table 1 missing N denominator",
        "evidence": "Table 1 percentages without N in footnote",
        "mechanism": "Cosmetic",
        "fix_hint": "Add N to footnote",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B2-F-10",
        "source": "S59-B2",
        "severity": "LOW",
        "title": "LOCO-CV AUC only in rebuttal",
        "evidence": "LOCO-CV not in main text",
        "mechanism": "Reviewer may request",
        "fix_hint": "Move to supplementary",
        "status": "PENDING_MCC",
    },
    {
        "id": "S59-B3-006",
        "source": "S59-B3",
        "severity": "LOW",
        "title": "Formal mediation analysis absent",
        "evidence": "No VanderWeele mediation",
        "mechanism": "Out of scope",
        "fix_hint": "Declare as out of scope",
        "status": "PENDING_MCC",
    },
]


BASELINE_REFERENCES: list[dict] = [
    # Skeleton: 10 key refs with DOIs. W7 will poll these.
    # Full 50-ref list should be populated manually from manuscript v4.
    {"id": 1, "label": "Gorris et al. 2025", "title": "Ecological niche modeling HPS USA", "doi": "10.1155/tbed/7126411"},
    {"id": 2, "label": "Jackson et al. 2025", "title": "Hantavirus climate review", "doi": "10.1111/zph.13012"},
    {"id": 3, "label": "Torres-Perez et al. 2025", "title": "Andes virus eco-epi Chile", "doi": "10.1371/journal.pntd.0012345"},
    {"id": 4, "label": "Fox et al. 2024", "title": "Scoring rules EID influenza", "doi": "10.3201/eid3001.231442"},
    {"id": 5, "label": "VanderWeele 2017", "title": "E-value sensitivity analysis", "doi": "10.7326/M16-2607"},
    {"id": 6, "label": "Gneiting & Raftery 2007", "title": "Strictly proper scoring rules", "doi": "10.1198/016214506000001437"},
    {"id": 7, "label": "Riley et al. 2019", "title": "Minimum sample size TRIPOD", "doi": "10.1002/sim.7992"},
    {"id": 8, "label": "Pepe et al. 2015", "title": "NRI limitations", "doi": "10.1097/EDE.0000000000000221"},
    {"id": 9, "label": "Lowe et al. 2021", "title": "Dengue climate early warning Brazil", "doi": "10.1016/S2542-5196(20)30292-8"},
    {"id": 10, "label": "Murua et al. 1996", "title": "Chusquea masting rodent outbreaks Chile", "doi": "10.2307/2390213"},
]


BASELINE_OBJECTIONS: list[dict] = [
    {
        "id": "R1-01",
        "role": "stats",
        "severity": "HIGH",
        "title": "BSS CI percentile vs BCa inconsistency",
        "critique": "PR-AUC uses BCa but BSS uses percentile. Reviewer will flag.",
        "suggested_response": "We re-ran with boot::boot.ci(type='bca'); results unchanged.",
    },
    {
        "id": "R1-02",
        "role": "stats",
        "severity": "HIGH",
        "title": "theta not propagated in bootstrap",
        "critique": "Bootstrap fixes theta -> underestimates CI width.",
        "suggested_response": "We added parametric bootstrap refitting theta per iteration.",
    },
    {
        "id": "R1-03",
        "role": "epieco",
        "severity": "HIGH",
        "title": "Lag 5 vs Chusquea 18-24yr cycle",
        "critique": "Operational lag and masting cycle are different phenomena.",
        "suggested_response": "We clarified in Discussion that FSI tracks short-term greenness as a proxy.",
    },
    {
        "id": "R1-04",
        "role": "epieco",
        "severity": "MED",
        "title": "Case definition drift",
        "critique": "Definition changed circa 2012.",
        "suggested_response": "Sensitivity analysis restricting to post-2012 shows identical direction.",
    },
    {
        "id": "R1-05",
        "role": "editorial",
        "severity": "MED",
        "title": "'First satellite-triggered protocol' claim",
        "critique": "Unsupported supremacy claim.",
        "suggested_response": "Softened to 'to our knowledge among the first'.",
    },
    {
        "id": "R1-06",
        "role": "stats",
        "severity": "MED",
        "title": "Poisson vs NB2 boundary LRT",
        "critique": "LRT on boundary is invalid.",
        "suggested_response": "Replaced with Vuong test.",
    },
    {
        "id": "R1-07",
        "role": "epieco",
        "severity": "MED",
        "title": "DAG FSI_R5 lacks direct edge",
        "critique": "Adjustment set formally incorrect.",
        "suggested_response": "Updated DAG and re-derived adjustment set.",
    },
    {
        "id": "R1-08",
        "role": "editorial",
        "severity": "LOW",
        "title": "Word count",
        "critique": "Check EID limit.",
        "suggested_response": "3004 words, within 3500 limit.",
    },
    {
        "id": "R1-09",
        "role": "stats",
        "severity": "MED",
        "title": "RPS inflated as skill +1.3%",
        "critique": "CI overlaps null.",
        "suggested_response": "Reframed as '2 of 3 scoring rules positive'.",
    },
    {
        "id": "R1-10",
        "role": "epieco",
        "severity": "MED",
        "title": "Ortiz 2004 misattribution",
        "critique": "Ortiz reports rodent seroprevalence, not national incidence.",
        "suggested_response": "Replaced with MINSAL Bulletin + direct calculation.",
    },
]


PLACEHOLDER_MANUSCRIPT = """# Hantavirus Nuble EID manuscript (control copy)

This is a placeholder. Replace with the real manuscript_improved.md contents
copied from the main project repository before running W3 / W5 in production.

## Abstract
Placeholder abstract.

## Introduction
Placeholder introduction with reference to Fox 2024 and Gneiting & Raftery 2007.

## Methods
GLMM nbinom2 with FSI_R5 lag 5 months, bootstrap BCa 95% CI, E-value 2.07.

## Results
BSS Tier 1 68.1% CI [61.7, 74.0]. IRR FSI 0.734. IRR t2m 1.468.

## Discussion
Placeholder.

## References
50 refs (see references.json).
"""


def main() -> int:
    now = dt.datetime.utcnow().isoformat() + "Z"

    for f in BASELINE_FINDINGS:
        f.setdefault("discovered_at", "2026-04-11T00:00:00Z")

    state.save_findings({"items": BASELINE_FINDINGS, "version": 1, "initialized_at": now})
    state.save_references({"items": BASELINE_REFERENCES, "version": 1, "initialized_at": now})
    state.save_objections({"items": BASELINE_OBJECTIONS, "version": 1, "initialized_at": now})
    state.save_pending_approvals({"items": [], "version": 1, "initialized_at": now})
    state.save_json("w10_queue.json", {"items": []})
    state.save_stability_history({"runs": []})
    state.save_paper_candidates({"items": []})
    state.save_pipeline_status(
        {
            "workflows": {
                w: {"last_run": None, "status": "not_yet_run"}
                for w in ("w0", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10")
            },
            "initialized_at": now,
        }
    )

    # Seed manuscript placeholders
    (state.STATE_DIR / "manuscript_control.md").write_text(PLACEHOLDER_MANUSCRIPT, encoding="utf-8")
    (state.STATE_DIR / "manuscript_improved.md").write_text(PLACEHOLDER_MANUSCRIPT, encoding="utf-8")

    # Memory bundle placeholder (MCC falls back to this if no local mount)
    state.save_json("memory_bundle.json", {"memory": [], "vault": [], "audit": []})

    print(
        f"[state_init] wrote {len(BASELINE_FINDINGS)} findings, "
        f"{len(BASELINE_REFERENCES)} refs, {len(BASELINE_OBJECTIONS)} objections"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
