"""W9 — Memory Cross-Checker (MCC, V1).

Reactive: triggered after W3 / W5 find new candidates, or manually with a
baseline input file (Fase F retroactive classification of S59 35 findings).

For each candidate:
 1. Extract semantic keywords.
 2. grep_memory + grep_vault + grep_audit_findings -> context snippets.
 3. Claude Sonnet classifies into BLINDADO / PARCIAL / NUEVO / CONTRADICCION.
 4. BLINDADO  -> log only, mark status=BLINDADO
 5. PARCIAL   -> status=PARCIAL + gap description -> triggers W10 BU
 6. NUEVO     -> status=NUEVO -> triggers W8 HIL
 7. CONTRADICCION -> URGENT ntfy + status=CONTRADICCION
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api  # noqa: E402
from scripts.lib import github as gh  # noqa: E402
from scripts.lib import memory_search  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


MCC_SYSTEM = """You are the Memory Cross-Checker for the Hantavirus Nuble EID pipeline.

Your job: classify each FINDING against PRIOR-EVIDENCE snippets found by grepping memory/ and obsidian_vault/.

Classification rules:
- BLINDADO: the prior evidence contains (a) a Q1 citation, (b) a specific calculation/value, AND (c) an explicit sentence already integrated in the manuscript. All three required.
- PARCIAL: some but not all of the three exist. Must name the missing piece.
- NUEVO: no prior evidence found, genuinely new.
- CONTRADICCION: prior evidence directly contradicts the finding claim.

Return STRICT JSON with a single top-level key 'classifications' whose value is a list of objects. Each object must have exactly these fields:
- 'finding_id': string, the finding id exactly as given in the input payload.
- 'classification': string, must be exactly one of these literal values: 'BLINDADO', 'PARCIAL', 'NUEVO', 'CONTRADICCION'.
- 'rationale': string, at most 250 characters, explaining why this classification was chosen.
- 'missing': string or JSON null. When classification is PARCIAL this must be one of 'CITATION_MISSING', 'CALC_MISSING', 'PHRASE_MISSING'. For any other classification use JSON null.
- 'prior_refs': list of strings, each in the form 'file:line' pointing to prior evidence locations. Empty list if none.

Example of a well-formed response (values are illustrative only, use the real findings from the input):
```json
{
  "classifications": [
    {
      "finding_id": "F-A1-001",
      "classification": "BLINDADO",
      "rationale": "Prior evidence includes Gorris 2025 citation, IRR 0.701 CI [0.551,0.910] computed in S50, and explicit Methods sentence already in manuscript v5.",
      "missing": null,
      "prior_refs": ["memory/project_auditoria_Q1_S50_cierre_completo.md:42", "obsidian_vault/04_Parte_I_EcoEpi/Paper_EID_Final.md:128"]
    },
    {
      "finding_id": "F-B2-014",
      "classification": "PARCIAL",
      "rationale": "Q1 citation present (PAHO 2025) but no numeric calculation derived yet and no sentence integrated in the manuscript body.",
      "missing": "CALC_MISSING",
      "prior_refs": ["memory/project_sesion_code_S59_capa1_2_hallazgos.md:77"]
    },
    {
      "finding_id": "F-C3-022",
      "classification": "NUEVO",
      "rationale": "No prior grep hits across memory/ or obsidian_vault/; genuinely new finding from current audit pass.",
      "missing": null,
      "prior_refs": []
    }
  ]
}
```
"""

KEYWORD_STOPWORDS = set(
    "the a an of in to and or for with on at by from is are was were be been being "
    "this that these those it its our we they their some any all no not as such "
    "which who whom whose while when where why how".split()
)


def extract_keywords(text: str, k: int = 6) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text)
    seen: list[str] = []
    for w in words:
        lw = w.lower()
        if lw in KEYWORD_STOPWORDS:
            continue
        if lw not in (s.lower() for s in seen):
            seen.append(w)
        if len(seen) >= k:
            break
    return seen


def gather_evidence(finding: dict) -> dict:
    text = " ".join(
        str(finding.get(k, "") or "")
        for k in ("title", "evidence", "mechanism", "fix_hint", "description")
    )
    keywords = extract_keywords(text)
    return {
        "keywords": keywords,
        "memory": memory_search.grep_memory(keywords)[:8],
        "vault": memory_search.grep_vault(keywords)[:8],
        "audit": memory_search.grep_audit_findings(keywords)[:8],
    }


def classify_batch(findings: list[dict]) -> list[dict]:
    if not findings:
        return []
    payload = []
    for f in findings:
        evidence = gather_evidence(f)
        payload.append(
            {
                "finding_id": f.get("id"),
                "finding_title": f.get("title"),
                "finding_severity": f.get("severity"),
                "finding_text": (f.get("evidence") or "")[:400],
                "prior_memory": [
                    {"loc": e.get("file", ""), "snippet": e.get("snippet", "")[:300]}
                    for e in evidence["memory"]
                ],
                "prior_vault": [
                    {"loc": e.get("file", ""), "snippet": e.get("snippet", "")[:300]}
                    for e in evidence["vault"]
                ],
                "prior_audit": [
                    {"loc": e.get("file", ""), "snippet": e.get("snippet", "")[:300]}
                    for e in evidence["audit"]
                ],
            }
        )

    prompt = (
        "Classify these findings. Return JSON only.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    try:
        resp = claude_api.call_sonnet(prompt, max_tokens=4000, system=MCC_SYSTEM)
    except claude_api.ClaudeAPIError as exc:
        print(f"[w9] claude error: {exc}", flush=True)
        return []
    parsed = claude_api.extract_json(resp) or {}
    return parsed.get("classifications", []) if isinstance(parsed, dict) else []


def main() -> int:
    findings = state.load_findings()
    items = findings.get("items", [])
    pending = [f for f in items if f.get("status") in ("PENDING_MCC", None, "NEW")]
    # if Fase F baseline mode: also process findings loaded from baseline file
    baseline_file = os.environ.get("W9_INPUT_FILE")
    if baseline_file and Path(baseline_file).exists():
        with open(baseline_file, "r", encoding="utf-8") as f:
            baseline_data = json.load(f)
        pending = baseline_data.get("items", [])

    if not pending:
        print("[w9] nothing to classify", flush=True)
        return 0

    # batch in chunks of 10 for token control
    classifications: list[dict] = []
    for i in range(0, len(pending), 10):
        chunk = pending[i : i + 10]
        classifications.extend(classify_batch(chunk))

    now = dt.datetime.utcnow().isoformat() + "Z"
    by_id = {c.get("finding_id"): c for c in classifications}

    counts = {"BLINDADO": 0, "PARCIAL": 0, "NUEVO": 0, "CONTRADICCION": 0}
    upgrades_needed: list[dict] = []
    for f in pending:
        c = by_id.get(f.get("id"))
        if not c:
            continue
        cls = c.get("classification", "NUEVO")
        counts[cls] = counts.get(cls, 0) + 1
        f["mcc_classification"] = cls
        f["mcc_rationale"] = c.get("rationale")
        f["mcc_missing"] = c.get("missing")
        f["mcc_prior_refs"] = c.get("prior_refs", [])
        f["mcc_at"] = now
        if cls == "BLINDADO":
            f["status"] = "BLINDADO"
        elif cls == "PARCIAL":
            f["status"] = "PARCIAL"
            upgrades_needed.append(f)
        elif cls == "NUEVO":
            f["status"] = "NUEVO_PENDING_HIL"
        elif cls == "CONTRADICCION":
            f["status"] = "CONTRADICCION"

    # ensure classified findings exist in state (baseline mode)
    if baseline_file:
        existing_ids = {x.get("id") for x in items}
        for f in pending:
            if f.get("id") not in existing_ids:
                items.append(f)
        findings["items"] = items
    state.save_findings(findings)

    # Save upgrades queue for W10
    if upgrades_needed:
        queue = state.load_json("w10_queue.json", {"items": []})
        queue.setdefault("items", [])
        existing = {q.get("id") for q in queue["items"]}
        for f in upgrades_needed:
            if f.get("id") in existing:
                continue
            queue["items"].append(f)
        state.save_json("w10_queue.json", queue)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w9"] = {
        "last_run": now,
        "classified": len(classifications),
        "counts": counts,
    }
    state.save_pipeline_status(status)

    # notifications
    contradictions = [f for f in pending if f.get("status") == "CONTRADICCION"]
    if contradictions:
        lines = "\n".join(f"- {f.get('id')}: {f.get('title','')[:80]}" for f in contradictions)
        ntfy.send_alert("URGENT", f"W9: {len(contradictions)} CONTRADICCION", lines)
    else:
        ntfy.send_alert(
            "MED",
            "W9 MCC pass complete",
            f"BLINDADO={counts['BLINDADO']} PARCIAL={counts['PARCIAL']} "
            f"NUEVO={counts['NUEVO']} CONTRA={counts['CONTRADICCION']}",
        )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/findings.json", "state/w10_queue.json", "state/pipeline_status.json"],
            f"W9: {sum(counts.values())} classified @ {now}",
        )

    print(f"[w9] done counts={counts}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
