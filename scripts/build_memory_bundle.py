"""build_memory_bundle — indexa memory/ + obsidian_vault/ para W9 MCC.

Corre localmente. Genera state/memory_bundle.json con ~500-1500 snippets
relevantes para que W9 clasifique contra blindaje real (no stub vacío como S60).

Uso: python scripts/build_memory_bundle.py
Env override: HNUBLE_MEMORY_ROOT, HNUBLE_VAULT_ROOT, HNUBLE_AUDIT_ROOT
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path

MEMORY = Path(os.environ.get("HNUBLE_MEMORY_ROOT",
    "C:/Users/gonza/.claude/projects/C--Proyectos-Hantavirus-Nuble/memory"))
VAULT = Path(os.environ.get("HNUBLE_VAULT_ROOT",
    "C:/Proyectos/Hantavirus_Nuble/obsidian_vault"))
AUDIT_ROOT = Path(os.environ.get("HNUBLE_AUDIT_ROOT", "C:/Proyectos/Hantavirus_Nuble"))
REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "state" / "memory_bundle.json"

KEYWORDS = {
    "glmm","nbinom2","poisson","bootstrap","bca","brier","bss","auc","loco",
    "walk-forward","dharma","vuong","icc","vif","e-value","vanderweele","dag",
    "confounder","confundente","hantavirus","scph","hcps","andes","ñuble","nuble",
    "seremi","case","caso","incidence","lag","rolling","within","between",
    "ascertainment","immortal","leakage","look-ahead","forecast","ews","early warning",
    "fsi","ndvi","ndmi","nbr2","sentinel","landsat","r_v1","m_v1","q_area","era5",
    "oligoryzomys","chusquea","quila","rodent","fire","incendio","pm2.5","blindaje",
    "blindado","parcial","declarado","strobe","tripod","epiforge","retraction","doi",
    "ley 21.033","back-allocat","maule","pre-2018","s29","s37","s49","s50","s51",
    "s54","s55","s57","s58","s59","cobquecura","yungay","bortman","pham","engelthaler",
    "andreo","lowe","koren","vadell","tortosa","martinez-valdebenito","fox 2024",
    "riley 2019","dimitriadis","efron","dicicco","carpenter","gneiting","suissa",
    "bergmeir","hewamalage","saavedra","tier1","tier2","tier3",
}

_FM_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
_WIKI_RE = re.compile(r"\[\[([^\]|]+\|)?([^\]]+)\]\]")
_FM_TAG_LINE = re.compile(r"^(tags|name|type)\s*:\s*(.+)$", re.IGNORECASE)


def extract_frontmatter_tags(text: str) -> list[str]:
    m = _FM_RE.match(text)
    if not m:
        return []
    tags: list[str] = []
    for line in m.group(0).splitlines():
        mm = _FM_TAG_LINE.match(line.strip())
        if not mm:
            continue
        val = mm.group(2).strip().strip("[]")
        for t in val.split(","):
            t = t.strip().strip('"').strip("'")
            if t:
                tags.append(t)
    return tags


def split_blocks(text: str) -> list[str]:
    text = _FM_RE.sub("", text, count=1)
    text = _CODE_RE.sub("", text)
    blocks: list[str] = []
    cur: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            if cur:
                blocks.append("\n".join(cur))
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    out: list[str] = []
    for b in blocks:
        lines = b.splitlines()
        if all(re.match(r"^\s*[-*+]\s", ln) for ln in lines):
            out.extend(ln.strip() for ln in lines)
        else:
            out.append(b)
    return out


def clean(text: str) -> str:
    text = _WIKI_RE.sub(r"\2", text)
    return re.sub(r"\s+", " ", text).strip()


def has_kw(text: str) -> list[str]:
    tl = text.lower()
    return [k for k in KEYWORDS if k in tl]


def fingerprint(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())[:120]


def index_dir(root: Path, cap: int, label: str) -> list[dict]:
    if not root.exists():
        print(f"[{label}] missing: {root}", file=sys.stderr)
        return []
    seen: set[str] = set()
    out: list[dict] = []
    files = sorted(root.rglob("*.md"))
    print(f"[{label}] scanning {len(files)} md files", file=sys.stderr)
    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        fm_tags = extract_frontmatter_tags(raw)
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.name
        for blk in split_blocks(raw):
            c = clean(blk)
            if len(c) < 60 or len(c) > 800:
                continue
            kws = has_kw(c)
            if not kws:
                continue
            fp = fingerprint(c)
            if fp in seen:
                continue
            seen.add(fp)
            out.append({"file": rel, "text": c,
                        "tags": list(dict.fromkeys(fm_tags + kws[:8])),
                        "loc": rel})
            if len(out) >= cap:
                break
        if len(out) >= cap:
            break
    print(f"[{label}] indexed {len(out)} entries", file=sys.stderr)
    return out


def index_audit(root: Path, cap: int) -> list[dict]:
    candidates = [
        root / "audit_findings.md",
        root / "04_sesgos_vacios.md",
        root / "submission" / "audit_findings.md",
    ]
    if root.exists():
        candidates += list(root.rglob("*audit_findings*.md"))[:5]
    out: list[dict] = []
    seen: set[str] = set()
    for p in candidates:
        if not p.exists() or not p.is_file():
            continue
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for blk in split_blocks(raw):
            c = clean(blk)
            if len(c) < 60 or len(c) > 800:
                continue
            kws = has_kw(c)
            if not kws:
                continue
            fp = fingerprint(c)
            if fp in seen:
                continue
            seen.add(fp)
            out.append({"file": p.name, "text": c, "tags": kws[:8], "loc": p.name})
            if len(out) >= cap:
                return out
    return out


def main() -> int:
    mem = index_dir(MEMORY, 800, "memory")
    vault = index_dir(VAULT, 800, "vault")
    audit = index_audit(AUDIT_ROOT, 300)
    bundle = {
        "description": "Indexed memory/ + obsidian_vault/ for W9 MCC. "
                       "Generated by scripts/build_memory_bundle.py. "
                       "Filtered by keyword match, 60-800 char length, deduped.",
        "schema_version": 1,
        "counts": {"memory": len(mem), "vault": len(vault), "audit": len(audit)},
        "memory": mem, "vault": vault, "audit": audit,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[bundle] {OUT} memory={len(mem)} vault={len(vault)} audit={len(audit)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
