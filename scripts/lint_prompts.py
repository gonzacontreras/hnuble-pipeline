"""lint_prompts — static JSON validator for system prompts embedded in Python.

Referenced by E5 S60 post-mortem: the BU_SYSTEM prompt in w9 (the memory
cross-checker's auto-patch synthesizer) contained a JSON skeleton with a
pseudo-schema annotation like::

    {
      "citation": "Smith 2020",
      "doi": "10.1234/abc" or null,
      "confidence": 0.9
    }

The ``"doi": "..." or null`` token is NOT valid JSON; Claude API rejected the
response schema enforcement and the workflow hung for ~3 minutes before the
parent orchestrator killed it. This lint pass catches the same class of bugs
before deploy: it scans every .py file under scripts/ for string constants
whose name ends in ``_SYSTEM``, ``_PROMPT``, or ``_TEMPLATE``, extracts every
```json ... ``` fenced block and every ``{ ... }`` span that plausibly looks
like JSON, and runs ``json.loads()`` on each.

Additionally a small regex pass catches explicitly-forbidden pseudo-JSON
patterns (``" or null``, ``"|``, ``"/optional``, etc.) that are valid JSON
strings but are clearly meant as schema annotations and will confuse
downstream LLM parsers.

Usage::

    python scripts/lint_prompts.py
    python scripts/lint_prompts.py --path scripts/w9_memory_crosschecker.py

Exit codes:
    0 = all JSON blocks parse cleanly
    1 = one or more violations found (printed to stdout)

The script is pure-stdlib: only ``ast``, ``json``, ``re``, ``glob``.
"""
from __future__ import annotations

import argparse
import ast
import glob
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROMPT_VAR_SUFFIXES = ("_SYSTEM", "_PROMPT", "_TEMPLATE", "_INSTRUCTIONS", "_SCHEMA")

# Pseudo-JSON red flags — syntactically valid JSON strings but semantic poison
# because they look like schema annotations that downstream LLMs will interpret
# as instructions rather than data.
# Patterns target content INSIDE or AFTER a JSON string/value.
PSEUDO_JSON_PATTERNS: list[tuple[re.Pattern, str]] = [
    (
        re.compile(r'"[^"]*"\s+or\s+null', re.IGNORECASE),
        '"..." or null   (schema annotation leaking into JSON body)',
    ),
    (
        re.compile(r'"[^"]*"\s*\|\s*null', re.IGNORECASE),
        '"..." | null   (type-union annotation leaking into JSON body)',
    ),
    (
        re.compile(r'"[^"]*"\s+or\s+"[^"]*"', re.IGNORECASE),
        '"A" or "B"   (enum annotation leaking into JSON body)',
    ),
    (
        re.compile(r'"[^"]*"\s*/\s*optional', re.IGNORECASE),
        '"..."/optional   (optional-field annotation leaking into JSON body)',
    ),
    (
        re.compile(r'<[A-Za-z_][A-Za-z0-9_]*>'),
        '<placeholder>   (angle-bracket placeholder leaking into JSON body)',
    ),
]

# Fenced JSON extraction (triple-backtick with optional json tag)
FENCED_JSON_RE = re.compile(r"```(?:json)?\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)

# Candidate balanced-brace span. Used only when no fence is present.
# We find every '{' and scan forward balancing braces.
def _find_balanced_braces(text: str) -> list[tuple[int, int, str]]:
    """Return list of (start, end, substring) for every balanced { } span.

    Greedy: returns outermost spans only. Ignores spans <20 chars (too small
    to be a real JSON payload; often just f-string interpolation).
    """
    out: list[tuple[int, int, str]] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "{":
            depth = 0
            start = i
            while i < n:
                ch = text[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        span = text[start : i + 1]
                        if len(span) >= 20:
                            out.append((start, i + 1, span))
                        i += 1
                        break
                i += 1
            else:
                break
        else:
            i += 1
    return out


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Violation:
    file: str
    lineno: int
    var_name: str
    kind: str  # "JSON_PARSE_ERROR" | "PSEUDO_JSON"
    detail: str
    snippet: str = ""

    def format(self) -> str:
        return (
            f"  {self.file}:{self.lineno}  [{self.kind}]  {self.var_name}\n"
            f"    -> {self.detail}\n"
            f"    snippet: {self.snippet[:120]}..."
        )


@dataclass
class LintReport:
    files_scanned: int = 0
    prompts_checked: int = 0
    violations: list[Violation] = field(default_factory=list)

    def ok(self) -> bool:
        return not self.violations


# ---------------------------------------------------------------------------
# AST walker
# ---------------------------------------------------------------------------


def _is_prompt_name(name: str) -> bool:
    u = name.upper()
    return any(u.endswith(suf) for suf in PROMPT_VAR_SUFFIXES)


def _string_value(node: ast.AST) -> tuple[str, int] | None:
    """Return (string_value, lineno) if node is a string constant, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value, node.lineno
    # Python 3.8 compatibility: ast.Str deprecated but still handled
    if hasattr(ast, "Str") and isinstance(node, ast.Str):  # pragma: no cover
        return node.s, node.lineno
    # Joined strings (f-strings): concat all literal parts
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                parts.append(v.value)
            elif isinstance(v, ast.FormattedValue):
                parts.append("{}")  # placeholder
        return "".join(parts), node.lineno
    return None


def _collect_prompt_strings(tree: ast.AST) -> list[tuple[str, str, int]]:
    """Walk AST and return [(var_name, string_value, lineno), ...] for every
    assignment whose target name matches PROMPT_VAR_SUFFIXES."""
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        # Regular assignment:  FOO_SYSTEM = "..."
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and _is_prompt_name(target.id):
                    sv = _string_value(node.value)
                    if sv:
                        out.append((target.id, sv[0], sv[1]))
        # Annotated assignment:  FOO_PROMPT: str = "..."
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and _is_prompt_name(node.target.id):
                if node.value is not None:
                    sv = _string_value(node.value)
                    if sv:
                        out.append((node.target.id, sv[0], sv[1]))
    return out


# ---------------------------------------------------------------------------
# JSON block extraction + validation
# ---------------------------------------------------------------------------


def _extract_json_candidates(prompt_text: str) -> list[str]:
    """Return candidate JSON strings from a prompt.

    Priority 1: fenced ```json ... ``` blocks (explicit).
    Priority 2: balanced-brace spans >= 20 chars (heuristic).
    """
    fenced = FENCED_JSON_RE.findall(prompt_text)
    if fenced:
        return [f.strip() for f in fenced]
    return [span for _, _, span in _find_balanced_braces(prompt_text)]


def _check_pseudo_json(snippet: str) -> list[str]:
    """Return human-readable descriptions for each pseudo-JSON pattern hit."""
    hits: list[str] = []
    for pat, desc in PSEUDO_JSON_PATTERNS:
        if pat.search(snippet):
            hits.append(desc)
    return hits


def _validate_json_block(
    snippet: str, file: str, lineno: int, var_name: str
) -> list[Violation]:
    """Run both pseudo-JSON regex and json.loads on a candidate block."""
    violations: list[Violation] = []

    # 1. Pseudo-JSON check (catches E5 S60 BU_SYSTEM pattern)
    for desc in _check_pseudo_json(snippet):
        violations.append(
            Violation(
                file=file,
                lineno=lineno,
                var_name=var_name,
                kind="PSEUDO_JSON",
                detail=desc,
                snippet=snippet.replace("\n", " "),
            )
        )

    # 2. Strict json.loads
    # If the snippet contained an f-string {} placeholder we inserted, skip
    # strict parse (we can't know the runtime value).
    contains_placeholder = "{}" in snippet and snippet.count("{}") > snippet.count('"{}"')
    if not contains_placeholder:
        try:
            json.loads(snippet)
        except json.JSONDecodeError as e:
            # Only report as JSON_PARSE_ERROR if not already flagged as pseudo.
            # (Pseudo-JSON usually IS valid json -- the issue is semantic.)
            already_pseudo = any(v.kind == "PSEUDO_JSON" for v in violations)
            if not already_pseudo:
                violations.append(
                    Violation(
                        file=file,
                        lineno=lineno,
                        var_name=var_name,
                        kind="JSON_PARSE_ERROR",
                        detail=f"json.loads failed: {e.msg} at line {e.lineno} col {e.colno}",
                        snippet=snippet.replace("\n", " "),
                    )
                )
    return violations


# ---------------------------------------------------------------------------
# File-level driver
# ---------------------------------------------------------------------------


def lint_file(path: Path, report: LintReport) -> None:
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  WARN cannot read {path}: {e}", file=sys.stderr)
        return

    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError as e:
        print(f"  WARN syntax error in {path}: {e}", file=sys.stderr)
        return

    report.files_scanned += 1

    for var_name, text, lineno in _collect_prompt_strings(tree):
        report.prompts_checked += 1
        candidates = _extract_json_candidates(text)
        for cand in candidates:
            vs = _validate_json_block(cand, str(path), lineno, var_name)
            report.violations.extend(vs)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Lint JSON blocks inside Python prompt strings."
    )
    p.add_argument(
        "--path",
        default=None,
        help="Single file or glob to scan. Default: scripts/*.py in pipeline repo.",
    )
    args = p.parse_args(argv)

    repo_scripts = Path(__file__).resolve().parent
    if args.path:
        targets = [Path(p) for p in glob.glob(args.path)] or [Path(args.path)]
    else:
        targets = [Path(p) for p in sorted(glob.glob(str(repo_scripts / "*.py")))]

    report = LintReport()

    print(f"lint_prompts: scanning {len(targets)} file(s)")
    print("=" * 60)

    for t in targets:
        if t.name == "lint_prompts.py":
            continue  # don't lint ourselves
        lint_file(t, report)

    print(
        f"files_scanned={report.files_scanned} "
        f"prompts_checked={report.prompts_checked} "
        f"violations={len(report.violations)}"
    )
    print("=" * 60)

    if report.ok():
        print("OK: no JSON violations found.")
        return 0

    # Print violations as a table
    print(f"FAIL: {len(report.violations)} violation(s) found:\n")
    by_file: dict[str, list[Violation]] = {}
    for v in report.violations:
        by_file.setdefault(v.file, []).append(v)
    for f, vs in sorted(by_file.items()):
        rel = os.path.relpath(f, str(repo_scripts.parent))
        print(f"[{rel}]")
        for v in vs:
            print(v.format())
        print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
