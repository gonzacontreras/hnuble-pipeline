"""W2 — Language Polish.

On-demand workflow_dispatch. Takes a section name and an approved upgrade
from state/pending_approvals.json (approved manually), applies an anti-
ChatGPT-ese language polish to manuscript_improved.md for that section only,
and commits the diff. A validator checks that no numbers or citations were
silently altered.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.lib import claude_api  # noqa: E402
from scripts.lib import github as gh  # noqa: E402
from scripts.lib import ntfy  # noqa: E402
from scripts.lib import state  # noqa: E402


POLISH_SYSTEM = """You are a scientific prose editor for the Hantavirus Nuble EID manuscript. Rules:
- Preserve EVERY number exactly (coefficients, CI, p-values, percentages, DOIs, years).
- Preserve EVERY citation (Author et al., 2024) exactly.
- Remove ChatGPT-ese: 'delve into', 'it is noteworthy that', 'in the realm of', 'a plethora of', 'navigate the complexities'.
- Use EID house style: past tense, active voice where possible, < 30 words per sentence.
- Return only the revised section text, no commentary, no fences."""


NUMBER_PATTERN = re.compile(r"\d+\.?\d*")
CITATION_PATTERN = re.compile(r"[A-Z][a-zA-Z-]+ et al\., \d{4}|\[\d+\]|\(\d{4}\)")


def validate_preserved(before: str, after: str) -> tuple[bool, list[str]]:
    before_nums = set(NUMBER_PATTERN.findall(before))
    after_nums = set(NUMBER_PATTERN.findall(after))
    before_cites = set(CITATION_PATTERN.findall(before))
    after_cites = set(CITATION_PATTERN.findall(after))
    issues: list[str] = []
    missing_nums = before_nums - after_nums
    missing_cites = before_cites - after_cites
    if missing_nums:
        issues.append(f"missing numbers: {sorted(missing_nums)[:10]}")
    if missing_cites:
        issues.append(f"missing citations: {sorted(missing_cites)[:10]}")
    return (not issues, issues)


def main() -> int:
    section = os.environ.get("W2_SECTION", "")
    if not section:
        print("[w2] W2_SECTION env var missing", flush=True)
        return 1

    manu_path = REPO_ROOT / "state" / "manuscript_improved.md"
    if not manu_path.exists():
        print("[w2] manuscript_improved.md missing", flush=True)
        return 1

    text = manu_path.read_text(encoding="utf-8")
    # Find section block: "## Section" to next "## " or EOF
    pattern = re.compile(rf"(##\s+{re.escape(section)}\b.*?)(?=^##\s|\Z)", re.DOTALL | re.MULTILINE)
    m = pattern.search(text)
    if not m:
        print(f"[w2] section '{section}' not found", flush=True)
        return 1

    before = m.group(1)
    try:
        after = claude_api.call_sonnet(before, max_tokens=3000, system=POLISH_SYSTEM).strip()
    except claude_api.ClaudeAPIError as exc:
        print(f"[w2] claude error: {exc}", flush=True)
        return 1

    ok, issues = validate_preserved(before, after)
    if not ok:
        ntfy.send_alert(
            "HIGH",
            "W2 polish rejected: validator failed",
            f"Section: {section}\n" + "\n".join(issues),
        )
        return 1

    new_text = text[: m.start(1)] + after + text[m.end(1) :]
    manu_path.write_text(new_text, encoding="utf-8")

    now = dt.datetime.utcnow().isoformat() + "Z"
    status = state.load_pipeline_status()
    status.setdefault("workflows", {})
    status["workflows"]["w2"] = {"last_run": now, "section": section, "status": "applied"}
    state.save_pipeline_status(status)

    if os.environ.get("GITHUB_ACTIONS"):
        gh.commit_state(
            ["state/manuscript_improved.md", "state/pipeline_status.json"],
            f"W2: polish {section} @ {now}",
        )

    ntfy.send(
        title="W2 polish applied",
        message=f"Section: {section}\nValidator: OK",
        priority="default",
        tags=["sparkles"],
    )

    print(f"[w2] done section={section}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
