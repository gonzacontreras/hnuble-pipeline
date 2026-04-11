"""W3 — Bias Hunter.

Cron: daily at 03:00 UTC.
Uses Claude Sonnet as a bias-auditor over the current manuscript_improved.md
(or excerpt bundle) with the S59 baseline findings as context. Outputs new
candidate biases NOT already in baseline, and triggers W9 MCC on them.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api  # noqa: E402
from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


BIAS_SYSTEM = """You are an anti-bypass bias auditor for the Hantavirus Nuble EID manuscript.

Taxonomy: selection, information, confounding, measurement, temporal, ecological, publication, immortal-time, attrition, detection, ascertainment, winner's curse, model-mis-specification.

Rules:
1. Use the baseline findings as context: if a candidate is already covered there, DO NOT repeat it.
2. Only flag biases that have a realistic path to change conclusions or CI width materially.
3. Every flag must cite the manuscript evidence (line or sentence fragment) that triggered it.
4. Return strict JSON only.

Output schema:
{
  "new_candidates": [
    {
      "id": "W3-YYYYMMDD-NN",
      "taxonomy": "selection|information|confounding|...",
      "severity": "HIGH|MED|LOW",
      "title": "short title",
      "evidence": "verbatim fragment from manuscript (<=200 chars)",
      "mechanism": "how it could bias results",
      "fix_hint": "concrete actionable suggestion"
    }
  ]
}
"""


def load_manuscript_excerpt() -> str:
    """Load manuscript_improved.md or fall back to manuscript_control.md."""
    candidates = [
        REPO_ROOT / "state" / "manuscript_improved.md",
        REPO_ROOT / "state" / "manuscript_control.md",
    ]
    for c in candidates:
        if c.exists():
            text = c.read_text(encoding="utf-8", errors="ignore")
            # keep first 25000 chars to control tokens
            return text[:25000]
    return ""


def main() -> int:
    findings = state.load_findings()
    baseline = [f for f in findings.get("items", []) if f.get("source") != "W3"]
    baseline_compact = [
        {
            "id": f.get("id"),
            "title": f.get("title"),
            "taxonomy": f.get("taxonomy") or f.get("severity_class", ""),
            "severity": f.get("severity"),
        }
        for f in baseline[:60]
    ]

    manuscript = load_manuscript_excerpt()
    if not manuscript:
        print("[w3] no manuscript available", flush=True)
        ntfy.send_alert("LOW", "W3 skipped", "No manuscript in state/, run state_init")
        return 0

    prompt = (
        "BASELINE FINDINGS (already flagged, do not repeat):\n"
        + json.dumps(baseline_compact, ensure_ascii=False)
        + "\n\nMANUSCRIPT EXCERPT:\n"
        + manuscript
        + "\n\nAnalyze for NEW bias candidates only. Return JSON only."
    )

    try:
        resp = claude_api.call_sonnet(prompt, max_tokens=3500, system=BIAS_SYSTEM)
    except claude_api.ClaudeAPIError as exc:
        print(f"[w3] claude error: {exc}", flush=True)
        return 1

    parsed = claude_api.extract_json(resp) or {}
    new_candidates = parsed.get("new_candidates", []) if isinstance(parsed, dict) else []

    now = dt.datetime.utcnow().isoformat() + "Z"
    added = 0
    pending_mcc = []
    existing_ids = {f.get("id") for f in findings.get("items", [])}
    for c in new_candidates:
        cid = c.get("id") or f"W3-{now[:10].replace('-', '')}-{added+1:02d}"
        if cid in existing_ids:
            continue
        entry = {
            "id": cid,
            "source": "W3",
            "severity": c.get("severity", "MED"),
            "taxonomy": c.get("taxonomy"),
            "title": c.get("title"),
            "evidence": c.get("evidence"),
            "mechanism": c.get("mechanism"),
            "fix_hint": c.get("fix_hint"),
            "status": "PENDING_MCC",
            "discovered_at": now,
        }
        findings.setdefault("items", []).append(entry)
        pending_mcc.append(entry)
        added += 1

    findings["last_w3_run"] = now
    state.save_findings(findings)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w3"] = {
        "last_run": now,
        "new_candidates": added,
        "pending_mcc": len(pending_mcc),
    }
    state.save_pipeline_status(status)

    if added:
        ntfy.send_alert(
            "MED",
            f"W3: {added} new bias candidate(s)",
            f"Flowing to W9 MCC. Check docs/findings.html",
        )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/findings.json", "state/pipeline_status.json"],
            f"W3: +{added} candidates @ {now}",
        )

    # Trigger W9 via workflow_dispatch if new candidates exist
    if added and os.environ.get("GITHUB_ACTIONS") and os.environ.get("GH_DISPATCH_TOKEN"):
        try:
            import httpx  # local import

            repo = os.environ.get("GITHUB_REPOSITORY", "")
            r = httpx.post(
                f"https://api.github.com/repos/{repo}/actions/workflows/w9-mcc.yml/dispatches",
                headers={
                    "Authorization": f"token {os.environ['GH_DISPATCH_TOKEN']}",
                    "Accept": "application/vnd.github+json",
                },
                json={"ref": "main", "inputs": {"trigger": "w3"}},
                timeout=30.0,
            )
            print(f"[w3] triggered w9 via dispatch: {r.status_code}", flush=True)
        except Exception as exc:
            print(f"[w3] dispatch error: {exc}", flush=True)

    print(f"[w3] done added={added}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
