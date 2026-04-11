"""W1 — Papers Q1 Watcher.

Cron: every 12 hours.
Queries OpenAlex + PubMed + bioRxiv for new papers on Hantavirus, Andes virus,
HCPS ecology, EWS forecasting, scoring rules. Scores each candidate 0-10 with
Claude Sonnet for relevance to our manuscript. Writes candidates to
state/paper_candidates.json. Score >= 9 triggers an HIL notification.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api  # noqa: E402
from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


QUERIES = [
    "Andes hantavirus ecology",
    "Hantavirus pulmonary syndrome forecasting",
    "zoonosis early warning system satellite",
    "Oligoryzomys longicaudatus rodent population",
    "Chusquea quila bamboo flowering",
    "scoring rules probabilistic forecast Brier",
]

SCORING_SYSTEM = """You are a scientific relevance scorer for the Hantavirus Nuble EID paper. Context:
- Observational eco-epidemiological study of Andes hantavirus HCPS in Nuble region, Chile (2002-2024).
- Core methods: GLMM nbinom2 (glmmTMB), time-lagged FSI satellite index, scoring rules (Brier/BSS/RPS), DAG adjustment, E-value sensitivity.
- Novel claim: 5-month lag FSI -> HCPS cases allows operational early warning tiers.
Score each candidate 0-10 based on:
- Relevance to our argument (methodological triangulation, new contradicting evidence, extension of findings)
- Recency and Q1 venue
- Direct usability as a citation in Intro / Methods / Discussion

Return STRICT JSON with a single top-level key 'papers' whose value is a list of objects. Each object must have exactly these fields:
- 'id': string, the candidate id exactly as given in the input payload.
- 'score': integer between 0 and 10 inclusive.
- 'reason': string, at most 120 characters, describing why the paper is relevant.
- 'target_section': string, must be one of these literal values: 'intro', 'methods', 'results', 'discussion', 'reject'.

Only include candidates with score >= 6. Score 10 = must-cite. Score 9 = strong addition.

Example of a well-formed response (the values are illustrative only, use the real candidates from the input):
```json
{
  "papers": [
    {
      "id": "10.1234/example.2025.001",
      "score": 9,
      "reason": "Provides independent validation of 5-month lag FSI signal in a comparable rodent-borne zoonosis",
      "target_section": "discussion"
    },
    {
      "id": "abc123def4",
      "score": 7,
      "reason": "Methodological extension of GLMM nbinom2 with DHARMa residuals for count data",
      "target_section": "methods"
    }
  ]
}
```
"""


def query_openalex(query: str, since: str, client: httpx.Client) -> list[dict]:
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "filter": f"from_publication_date:{since},type:article",
        "per-page": "25",
        "sort": "publication_date:desc",
    }
    try:
        r = client.get(url, params=params, timeout=40.0)
        if r.status_code != 200:
            return []
        results = r.json().get("results", [])
        out = []
        for w in results:
            doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
            out.append(
                {
                    "source": "openalex",
                    "id": w.get("id"),
                    "doi": doi,
                    "title": w.get("title", "")[:300],
                    "pub_date": w.get("publication_date"),
                    "venue": (w.get("host_venue") or {}).get("display_name"),
                    "citations": w.get("cited_by_count", 0),
                    "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
                }
            )
        return out
    except httpx.HTTPError:
        return []


def _reconstruct_abstract(idx: dict | None) -> str:
    if not idx:
        return ""
    pos: dict[int, str] = {}
    for word, positions in idx.items():
        for p in positions:
            pos[p] = word
    return " ".join(pos[i] for i in sorted(pos.keys()))[:1500]


def query_pubmed(query: str, since: str, client: httpx.Client) -> list[dict]:
    esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    try:
        r = client.get(
            esearch,
            params={
                "db": "pubmed",
                "term": f'{query} AND ("{since}"[Date - Publication] : "3000"[Date - Publication])',
                "retmode": "json",
                "retmax": "15",
                "sort": "pub date",
            },
            timeout=40.0,
        )
        if r.status_code != 200:
            return []
        ids = (r.json().get("esearchresult") or {}).get("idlist", [])
        if not ids:
            return []
        # fetch summaries
        esum = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        s = client.get(
            esum,
            params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
            timeout=40.0,
        )
        if s.status_code != 200:
            return []
        result = s.json().get("result", {})
        out = []
        for pmid in ids:
            rec = result.get(pmid)
            if not rec:
                continue
            doi = None
            for aid in rec.get("articleids", []):
                if aid.get("idtype") == "doi":
                    doi = aid.get("value")
                    break
            out.append(
                {
                    "source": "pubmed",
                    "id": pmid,
                    "doi": doi,
                    "title": rec.get("title", "")[:300],
                    "pub_date": rec.get("pubdate"),
                    "venue": rec.get("fulljournalname"),
                    "citations": 0,
                    "abstract": "",
                }
            )
        return out
    except httpx.HTTPError:
        return []


def query_biorxiv(query: str, since: str, client: httpx.Client) -> list[dict]:
    # bioRxiv search API is limited; we pull recent preprints and let Claude filter.
    try:
        r = client.get(
            f"https://api.biorxiv.org/details/biorxiv/{since}/",
            timeout=40.0,
        )
        if r.status_code != 200:
            return []
        data = r.json().get("collection", [])
        out = []
        ql = query.lower()
        for w in data[:200]:
            title = (w.get("title") or "").lower()
            if not any(tok in title for tok in ql.split()):
                continue
            out.append(
                {
                    "source": "biorxiv",
                    "id": w.get("doi"),
                    "doi": w.get("doi"),
                    "title": w.get("title", "")[:300],
                    "pub_date": w.get("date"),
                    "venue": "bioRxiv",
                    "citations": 0,
                    "abstract": (w.get("abstract") or "")[:1500],
                }
            )
        return out
    except httpx.HTTPError:
        return []


def dedupe(papers: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for p in papers:
        key = (p.get("doi") or p.get("title", "")).lower().strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def score_with_claude(candidates: list[dict]) -> list[dict]:
    if not candidates:
        return []
    # Limit to top 40 by recency to control token usage
    candidates = candidates[:40]
    # Compact the payload
    compact = [
        {
            "id": p.get("doi") or hashlib.md5(p.get("title", "").encode()).hexdigest()[:10],
            "title": p.get("title"),
            "venue": p.get("venue"),
            "pub_date": p.get("pub_date"),
            "abstract": (p.get("abstract") or "")[:800],
        }
        for p in candidates
    ]
    prompt = (
        "Score these candidate papers for relevance to the Hantavirus Nuble EID manuscript.\n\n"
        "CANDIDATES:\n"
        + json.dumps(compact, ensure_ascii=False)
        + "\n\nReturn only the JSON object, no prose."
    )
    try:
        resp = claude_api.call_sonnet(prompt, max_tokens=3500, system=SCORING_SYSTEM)
    except claude_api.ClaudeAPIError as exc:
        print(f"[w1] claude error: {exc}", flush=True)
        return []
    parsed = claude_api.extract_json(resp) or {}
    scored = parsed.get("papers", []) if isinstance(parsed, dict) else []
    # Merge scores back into originals
    lookup = {c["id"]: c for c in compact}
    out = []
    for s in scored:
        base = lookup.get(s.get("id"))
        if not base:
            continue
        merged = dict(base)
        merged.update(
            {
                "score": int(s.get("score", 0)),
                "reason": s.get("reason", ""),
                "target_section": s.get("target_section", "reject"),
            }
        )
        out.append(merged)
    return out


def main() -> int:
    since = (dt.datetime.utcnow() - dt.timedelta(days=14)).strftime("%Y-%m-%d")
    all_papers: list[dict] = []
    with httpx.Client(headers={"User-Agent": "hnuble-pipeline/1.0"}, verify=False) as client:
        for q in QUERIES:
            all_papers.extend(query_openalex(q, since, client))
            all_papers.extend(query_pubmed(q, since, client))
            all_papers.extend(query_biorxiv(q, since, client))

    unique = dedupe(all_papers)
    print(f"[w1] raw={len(all_papers)} unique={len(unique)}", flush=True)

    scored = score_with_claude(unique)
    scored = [p for p in scored if p.get("score", 0) >= 7]
    scored.sort(key=lambda p: p.get("score", 0), reverse=True)

    now = dt.datetime.utcnow().isoformat() + "Z"
    candidates = state.load_paper_candidates()
    candidates.setdefault("items", [])
    existing_ids = {c.get("id") for c in candidates["items"]}
    new_items = [p for p in scored if p.get("id") not in existing_ids]
    for p in new_items:
        p["discovered_at"] = now
        p["status"] = "NEW"
        candidates["items"].append(p)
    # keep most recent 200
    candidates["items"] = candidates["items"][-200:]
    candidates["last_run"] = now
    state.save_paper_candidates(candidates)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w1"] = {
        "last_run": now,
        "scanned": len(unique),
        "new_candidates": len(new_items),
    }
    state.save_pipeline_status(status)

    high = [p for p in new_items if p.get("score", 0) >= 9]
    if high:
        lines = "\n".join(f"- [{p['score']}] {p['title'][:120]}" for p in high[:8])
        ntfy.send_alert(
            "HIGH",
            f"W1: {len(high)} high-score paper(s)",
            f"{lines}\n\nReview in docs/findings.html",
        )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/paper_candidates.json", "state/pipeline_status.json"],
            f"W1: +{len(new_items)} candidates @ {now}",
        )

    print(f"[w1] done new={len(new_items)} high={len(high)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
