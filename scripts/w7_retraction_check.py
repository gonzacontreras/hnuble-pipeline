"""W7 — Retraction Check.

Cron: every 6 hours.
No Claude API required. Queries Crossref + OpenAlex for retraction signals on
the 50 references of the manuscript. If any retraction is detected, updates
state/findings.json and sends an URGENT ntfy notification.

References are loaded from state/references.json.
"""

from __future__ import annotations

import datetime as dt
import os
import sys
import time
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


CROSSREF_URL = "https://api.crossref.org/works/{doi}"
OPENALEX_URL = "https://api.openalex.org/works/doi:{doi}"


def check_crossref(doi: str, client: httpx.Client) -> dict:
    try:
        r = client.get(CROSSREF_URL.format(doi=doi), timeout=30.0)
        if r.status_code != 200:
            return {"ok": False, "error": f"HTTP {r.status_code}"}
        data = r.json().get("message", {})
        update_to = data.get("update-to", [])
        updated_by = data.get("updated-by", [])
        # retraction signal: any updated-by entry with type "retraction"
        retracted = any(u.get("type") == "retraction" for u in updated_by)
        return {
            "ok": True,
            "retracted": retracted,
            "update_to": update_to,
            "updated_by": updated_by,
        }
    except httpx.HTTPError as exc:
        return {"ok": False, "error": str(exc)}


def check_openalex(doi: str, client: httpx.Client) -> dict:
    try:
        r = client.get(OPENALEX_URL.format(doi=doi), timeout=30.0)
        if r.status_code != 200:
            return {"ok": False, "error": f"HTTP {r.status_code}"}
        data = r.json()
        retracted = bool(data.get("is_retracted"))
        return {"ok": True, "retracted": retracted}
    except httpx.HTTPError as exc:
        return {"ok": False, "error": str(exc)}


def main() -> int:
    refs = state.load_references().get("items", [])
    if not refs:
        print("[w7] no references loaded, nothing to check", flush=True)
        return 0

    findings = state.load_findings()
    findings.setdefault("items", [])

    now = dt.datetime.utcnow().isoformat() + "Z"
    retractions: list[dict] = []
    checked = 0
    errors = 0

    with httpx.Client(headers={"User-Agent": "hnuble-pipeline/1.0 (+ntfy)"}, verify=False) as client:
        for ref in refs:
            doi = (ref.get("doi") or "").strip()
            if not doi:
                continue
            checked += 1
            cr = check_crossref(doi, client)
            oa = check_openalex(doi, client)
            is_retracted = (cr.get("retracted") is True) or (oa.get("retracted") is True)
            if not cr.get("ok") and not oa.get("ok"):
                errors += 1
            if is_retracted:
                entry = {
                    "id": f"W7-RETRACT-{doi}",
                    "severity": "URGENT",
                    "source": "W7",
                    "timestamp": now,
                    "doi": doi,
                    "reference": ref.get("label") or ref.get("title") or doi,
                    "crossref": cr,
                    "openalex": oa,
                    "status": "RETRACTED",
                }
                retractions.append(entry)
                # dedupe by id
                existing_ids = {f.get("id") for f in findings["items"]}
                if entry["id"] not in existing_ids:
                    findings["items"].append(entry)
            time.sleep(0.3)  # be polite to public APIs

    findings["last_w7_run"] = now
    findings["last_w7_checked"] = checked
    findings["last_w7_errors"] = errors
    state.save_findings(findings)

    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w7"] = {
        "last_run": now,
        "checked": checked,
        "errors": errors,
        "retractions": len(retractions),
    }
    state.save_pipeline_status(status)

    if retractions:
        titles = "\n".join(f"- {r['reference']} ({r['doi']})" for r in retractions)
        ntfy.send_alert(
            "URGENT",
            f"W7 detected {len(retractions)} retraction(s)",
            f"References flagged as retracted:\n{titles}\n\nCheck docs/findings.html",
        )
    else:
        # low priority heartbeat only when run manually or weekly
        if os.environ.get("W7_HEARTBEAT", "0") == "1":
            ntfy.send(
                title="W7 heartbeat",
                message=f"Checked {checked} refs, 0 retractions, {errors} API errors.",
                priority="min",
            )

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/findings.json", "state/pipeline_status.json"],
            f"W7: {checked} refs checked, {len(retractions)} retractions @ {now}",
        )

    print(f"[w7] done checked={checked} retractions={len(retractions)} errors={errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
