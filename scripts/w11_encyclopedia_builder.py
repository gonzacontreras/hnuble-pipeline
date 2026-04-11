#!/usr/bin/env python3
"""
W11 — Encyclopedia Builder
Consolida ~397 archivos .md del proyecto Hantavirus Nuble en 13 categorias.

Fuentes:
  1. C:/Users/gonza/.claude/projects/C--Proyectos-Hantavirus-Nuble/memory/*.md  (~246)
  2. C:/Proyectos/Hantavirus_Nuble/obsidian_vault/**/*.md                        (~148)
  3. C:/Proyectos/Hantavirus_Nuble/ARCHIVO_MAESTRO_*.md                          (4)
  4. C:/Proyectos/Hantavirus_Nuble/CONTEXTO_*.md                                 (varios)

Modo:
  - Local (default): lee los 4 sources directamente, usa multiprocessing.Pool(8).
  - Bundle (GitHub Actions: GITHUB_ACTIONS=true): lee solo obsidian_vault/ + root + state/memory_bundle.json si existe.

Output:
  state/encyclopedia.json       (schema v1 con 13 categorias + modelos_activos)
  docs/encyc/<sanitized>.md     (top 20 priority_1 HIGH-VALUE, copiados para GH Pages)

CPU-bound: categorizacion + parse de 200 lineas * 397 archivos -> multiprocessing.Pool(8).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from multiprocessing import Pool
from pathlib import Path

# ---------- Paths ----------
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
STATE_DIR = REPO / "state"
DOCS_DIR = REPO / "docs"
ENCYC_DIR = DOCS_DIR / "encyc"

MEMORY_DIR = Path(r"C:/Users/gonza/.claude/projects/C--Proyectos-Hantavirus-Nuble/memory")
VAULT_DIR = Path(r"C:/Proyectos/Hantavirus_Nuble/obsidian_vault")
ROOT_PROJECT = Path(r"C:/Proyectos/Hantavirus_Nuble")

BUNDLE_MODE = os.environ.get("GITHUB_ACTIONS") == "true"

OUTPUT_JSON = STATE_DIR / "encyclopedia.json"

# ---------- HIGH-VALUE top 20 (hardcoded priority 1) ----------
HIGH_VALUE_NAMES = {
    "CANONICAL_BLINDAJES_INDEX.md",
    "project_sesion_code_S60_MASTER_COMPLETO.md",
    "project_sesion_code_S59_MASTER_COMPLETO.md",
    "project_sesion_code_S58.md",
    "project_sesion_code_S57.md",
    "project_sesion_code_S56.md",
    "project_plan_S61_automatizacion_paper.md",
    "project_pendientes_S61_rastreo.md",
    "project_paper_EID_contexto_completo_S50.md",
    "project_auditoria_Q1_S50_cierre_completo.md",
    "project_framework_operacional_SAG_CONAF_S50.md",
    "project_decision_opcionA_blindada_S50.md",
    "reference_biblio_S57_completa_contextualizada.md",
    "reference_numeros_metricas_S57.md",
    "reference_biblio_SRT_S56_v6.md",
    "reference_lag5_cadena_completa_S50.md",
    "ARCHIVO_MAESTRO_FINAL.md",
    "ARCHIVO_MAESTRO_PARTE_I.md",
    "ARCHIVO_MAESTRO_PARTE_II.md",
    "ARCHIVO_MAESTRO_PARTE_II_v3.md",
}

# ---------- 13 categorias ----------
CATEGORIES = [
    ("numeros_canonicos", {
        "label": "Numeros Canonicos Bloqueados",
        "description": "Metricas verificadas contra CSV, no modificables sin re-auditoria (136, 103, 33, BSS 68.1%, IRR 0.734).",
        "icon": "#",
    }),
    ("sesgos_m14", {
        "label": "Sesgos M14 / Blindajes",
        "description": "CANONICAL_BLINDAJES_INDEX + archivos de sesgos cerrados (34-56 sesgos auditados).",
        "icon": "!",
    }),
    ("decisiones", {
        "label": "Decisiones y Sesiones Master",
        "description": "Sesiones S50-S61 master completas + decisiones D1-D20 trazables.",
        "icon": "@",
    }),
    ("framework_tier", {
        "label": "Framework Tier / Decision Logic",
        "description": "Tier thresholds, decision curve, framework operacional SEREMI/CONAF/SAG.",
        "icon": "T",
    }),
    ("bibliografia", {
        "label": "Bibliografia & Referencias",
        "description": "Referencias Vancouver, DOIs, SRT (Systematic Review Team) reportes v1-v6.",
        "icon": "B",
    }),
    ("fenologia_dag", {
        "label": "Fenologia, DAG & Ratizacion",
        "description": "Chusquea quila, ratizacion, DAG causal, lag 5 cadena biologica, ecoepi.",
        "icon": "F",
    }),
    ("modelo_s29k", {
        "label": "Modelo S29-K & Variantes",
        "description": "Scripts, sesiones y walk-forward fix del modelo GLMM NegBin S29-K.",
        "icon": "M",
    }),
    ("walk_forward", {
        "label": "Walk-Forward / Scoring Rules",
        "description": "14 folds, burn-in, Log Score, RPS, Brier, Bootstrap BSS CI.",
        "icon": "W",
    }),
    ("checklists", {
        "label": "Checklists (STROBE/TRIPOD/EPIFORGE)",
        "description": "Validacion de completitud: STROBE 95%, TRIPOD+AI 95.8%, EPIFORGE 100%, red-team.",
        "icon": "C",
    }),
    ("auditoria_q1", {
        "label": "Auditoria Q1 / Cierre Completo",
        "description": "Auditorias Q1 S50-S61, cierre completo, semaforos, anti-bypass protocol.",
        "icon": "Q",
    }),
    ("clinica", {
        "label": "Clinica & Paper Companion",
        "description": "Estudio clinico companion, trilogia precoz Firth, CARE reporting.",
        "icon": "K",
    }),
    ("validacion_externa", {
        "label": "Validacion Externa / Limitaciones",
        "description": "Limitations declaradas, transferencia Argentina, validacion out-of-area.",
        "icon": "V",
    }),
    ("modelos_activos", {
        "label": "Modelos Activos & Herramientas Operativas",
        "description": "S29-K GLMM, Ward k=3, Trilogia Firth, Fire x SCPH, Framework SEREMI/CONAF/SAG, Decision Curve, Walk-Forward.",
        "icon": "*",
    }),
]

CATEGORY_IDS = [c[0] for c in CATEGORIES]

# ---------- Heuristic patterns ----------
# (regex_pattern, category_id) order matters: earlier patterns win
PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"canonical.*blindaj|sesgo|blindaj|cerrad", re.I), "sesgos_m14"),
    (re.compile(r"sesion_code_s\d+.*master|_master_completo|S6[01]_MASTER", re.I), "decisiones"),
    (re.compile(r"biblio|refs|reference_biblio|srt_v", re.I), "bibliografia"),
    (re.compile(r"numero|metrica|canonical_facts|reference_numeros", re.I), "numeros_canonicos"),
    (re.compile(r"walk|fold|scoring|brier|rps|log_score|bootstrap_ci", re.I), "walk_forward"),
    (re.compile(r"strobe|tripod|epiforge|checklist|redteam|red_team", re.I), "checklists"),
    (re.compile(r"auditoria|audit_q1|s50_cierre|auditoria_q1|anti_bypass|antibypass", re.I), "auditoria_q1"),
    (re.compile(r"clinic|trilogia|care|caso[_ ]clin|ficha", re.I), "clinica"),
    (re.compile(r"limitacion|external|validacion_ext|transferenc", re.I), "validacion_externa"),
    (re.compile(r"dag|fenologia|ratizacion|quila|chusquea|ecoepi|lag5|lag_5", re.I), "fenologia_dag"),
    (re.compile(r"framework|seremi|conaf|sag|tier|operacional", re.I), "framework_tier"),
    (re.compile(r"s29k|s29_k|s29-k|modelo_.*final|modelo_glmm|ward.*k3|s52_ward|s47_fire|s37b_firth", re.I), "modelo_s29k"),
    (re.compile(r"sesion_code_s\d+|decision|decisiones|pendientes", re.I), "decisiones"),
]

# ---------- Modelos activos (entradas explicitas, categoria 13) ----------
MODELOS_ACTIVOS_ENTRIES = [
    {
        "id": "model_s29k",
        "title": "S29-K GLMM NegBin",
        "description": "Modelo final descriptivo. GLMM NB2 con random intercept por comuna. Lag biologico 5 meses.",
        "script_path": "R/S29K_MODELO_FINAL_SIN_ZONE.R",
        "metrics": {
            "BSS_tier1": "68.1% [61.7-74.0]",
            "BSS_tier2": "36.5% [25.4-56.6]",
            "IRR_R5_quila": "0.734",
            "beta_t2m": "+0.384",
            "ICC": "9.43%",
            "cvAUC": "0.766"
        },
        "source_memory": "project_sesion_code_S58.md",
        "source_session": "S29-K -> S50 (walk-forward fix) -> S57 (bootstrap BSS CI)",
        "status": "BLINDADO",
        "priority": 1,
        "tags": ["modelo", "descriptivo", "glmm", "negbin", "blindado"]
    },
    {
        "id": "model_ward",
        "title": "Ward Clustering k=3",
        "description": "Cluster jerarquico Ward k=3 sobre 21 comunas Nuble. Silhouette 0.595. 4v = 3v (identico).",
        "script_path": "R/S52_WARD_INTEGRADO_Q1.R",
        "metrics": {
            "silhouette": "0.595",
            "kappa_3v_4v": "0.81",
            "AC1": "0.81",
            "RR_midp": "1.59 (p=0.043)",
            "E_value": "2.55"
        },
        "source_memory": "project_sesion_code_S52.md",
        "source_session": "S52 -> S53 (Ward 3v=4v confirmado)",
        "status": "BLINDADO",
        "priority": 1,
        "tags": ["modelo", "cluster", "ward", "ecoepi", "blindado"]
    },
    {
        "id": "model_trilogia",
        "title": "Trilogia Precoz Firth",
        "description": "Score clinico FR>22 + Plaq<150k + Hto>ULN. Regresion Firth para rare events.",
        "script_path": "R/S37B_FIRTH_TRILOGIA.R",
        "metrics": {
            "AUC": "0.833",
            "OR_firth": "10.31",
            "OR_score": "5.58",
            "p_value": "0.008"
        },
        "source_memory": "project_trilogia_precoz_S37.md",
        "source_session": "S37B -> S38 (OOS PIT) -> S46 (cruce GRD)",
        "status": "PARCIAL",
        "priority": 1,
        "tags": ["modelo", "clinico", "trilogia", "firth", "parcial"]
    },
    {
        "id": "model_fire",
        "title": "Fire x SCPH Dual-pathway",
        "description": "IRR fire-SCPH pre-especificado. Paradoja Cobquecura dual-pathway.",
        "script_path": "R/S47_FIRE_SCPH_ANALYSIS.R",
        "metrics": {
            "IRR": "1.28",
            "p_value": "0.044",
            "PAF": "35%",
            "n_tests": "28"
        },
        "source_memory": "project_sesion_code_S47_fire.md",
        "source_session": "S47-S48 (89 papers + 28 tests)",
        "status": "BLINDADO",
        "priority": 1,
        "tags": ["modelo", "fire", "dual-pathway", "cobquecura", "blindado"]
    },
    {
        "id": "model_cluster_2023",
        "title": "Cluster 2023 El Carmen",
        "description": "Kulldorff SaTScan cluster espaciotemporal 2023 El Carmen. N=2 casos.",
        "script_path": "R/CLUSTER_AUDIT.R",
        "metrics": {
            "RR_kulldorff": "2.14",
            "N_casos": "2"
        },
        "source_memory": "project_S53_blindaje_descriptivo_completo.md",
        "source_session": "S53 refutacion super-spreader",
        "status": "PARCIAL",
        "priority": 2,
        "tags": ["modelo", "cluster", "kulldorff", "parcial"]
    },
    {
        "id": "tool_framework",
        "title": "Framework Operacional SEREMI/CONAF/SAG",
        "description": "Pipeline 4 ventanas temporales multi-agencia. Basado en lag 5 psi.",
        "script_path": None,
        "metrics": {
            "ventanas": "4",
            "agencias": "3 (SEREMI, CONAF, SAG)",
            "respaldo_legal": "Ordinario MINSAL B38 N3420/2019"
        },
        "source_memory": "project_framework_operacional_SAG_CONAF_S50.md",
        "source_session": "S50 cierre",
        "status": "BLINDADO",
        "priority": 1,
        "tags": ["herramienta", "operacional", "seremi", "conaf", "sag", "blindado"]
    },
    {
        "id": "tool_decision_curve",
        "title": "Decision Curve Analysis",
        "description": "Net benefit analysis para decision threshold Youden=0.021.",
        "script_path": None,
        "metrics": {
            "threshold_youden": "0.021",
            "holdout_AUC": "0.728",
            "leakage_delta": "0.0002"
        },
        "source_memory": "project_sesion_code_S57.md",
        "source_session": "S57 decision curve",
        "status": "BLINDADO",
        "priority": 2,
        "tags": ["herramienta", "decision_curve", "blindado"]
    },
    {
        "id": "tool_walk_forward",
        "title": "Walk-Forward 14 folds",
        "description": "Walk-forward CV 14 folds con burn-in 4. Bootstrap BCa BSS CI.",
        "script_path": None,
        "metrics": {
            "folds": "14",
            "burn_in": "4",
            "BSS_tier1_CI": "[61.7-74.0]",
            "BSS_tier2_CI": "[25.4-56.6]"
        },
        "source_memory": "project_auditoria_Q1_S50_cierre_completo.md",
        "source_session": "S50 auditoria Q1 cierre",
        "status": "BLINDADO",
        "priority": 1,
        "tags": ["herramienta", "walk_forward", "scoring", "blindado"]
    },
]

# ---------- Helpers ----------

def strip_markdown(s: str) -> str:
    """Quita sintaxis markdown basica para preview plano."""
    s = re.sub(r"`{1,3}[^`]*`{1,3}", "", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_#>~\-]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def sanitize_name(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return s[:120]


def list_all_sources() -> list[Path]:
    paths: list[Path] = []
    if not BUNDLE_MODE and MEMORY_DIR.exists():
        paths.extend(sorted(p for p in MEMORY_DIR.glob("*.md") if p.is_file()))
    if VAULT_DIR.exists():
        paths.extend(sorted(p for p in VAULT_DIR.rglob("*.md") if p.is_file()))
    # root files
    for pattern in ("ARCHIVO_MAESTRO_*.md", "CONTEXTO_*.md"):
        paths.extend(sorted(ROOT_PROJECT.glob(pattern)))
    # dedupe preserving order
    seen = set()
    uniq: list[Path] = []
    for p in paths:
        rp = str(p.resolve())
        if rp in seen:
            continue
        seen.add(rp)
        uniq.append(p)
    return uniq


def classify(name: str, content: str) -> str:
    """Clasifica un archivo a una categoria segun heuristica por nombre + contenido."""
    lname = name.lower()
    for pat, cat in PATTERNS:
        if pat.search(lname):
            return cat
    # fallback: buscar en las primeras lineas del content
    lcontent = content.lower()[:2000]
    for pat, cat in PATTERNS:
        if pat.search(lcontent):
            return cat
    # default bucket
    return "decisiones"


def compute_source_label(path: Path) -> str:
    sp = str(path)
    if "obsidian_vault" in sp:
        return "vault"
    if "memory" in sp and ".claude" in sp:
        return "memory"
    return "root"


def parse_md_file(path_str: str) -> dict | None:
    """
    Lee primeras 200 lineas, extrae title, preview, size, lines, clasifica.
    Pure function for multiprocessing.Pool.
    """
    try:
        path = Path(path_str)
        if not path.exists() or not path.is_file():
            return None
        stat = path.stat()
        size = stat.st_size
        mtime = stat.st_mtime

        lines: list[str] = []
        title = path.stem
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= 200:
                    break
                lines.append(line.rstrip("\n"))
                if i < 25 and title == path.stem:
                    m = re.match(r"^#\s+(.+?)\s*$", line)
                    if m:
                        title = m.group(1).strip()

        content_200 = "\n".join(lines)
        # count total lines (stop at 5000)
        total_lines = 0
        try:
            with path.open("r", encoding="utf-8", errors="replace") as f:
                for total_lines, _ in enumerate(f, 1):
                    if total_lines >= 5000:
                        break
        except Exception:
            total_lines = len(lines)

        plain = strip_markdown(content_200)
        preview = plain[:300]

        # tags from filename
        name = path.name
        tags = []
        for tag in ["S5", "S6", "Q1", "STROBE", "TRIPOD", "BSS", "GLMM", "walk", "bias", "cerrad", "biblio", "numero"]:
            if tag.lower() in name.lower():
                tags.append(tag.lower())
        tags = list(dict.fromkeys(tags))[:5]

        category = classify(name, content_200)

        # priority
        priority = 5
        if name in HIGH_VALUE_NAMES:
            priority = 1
        elif size > 20000:
            priority = 2
        elif size > 8000:
            priority = 3
        elif size > 3000:
            priority = 4

        return {
            "id": str(path).replace("\\", "/"),
            "path": str(path).replace("\\", "/"),
            "name": name,
            "title": title[:200],
            "preview": preview,
            "size_bytes": size,
            "lines": total_lines,
            "mtime": mtime,
            "source": compute_source_label(path),
            "category": category,
            "tags": tags,
            "priority": priority,
        }
    except Exception as e:
        return {
            "id": path_str.replace("\\", "/"),
            "path": path_str.replace("\\", "/"),
            "name": Path(path_str).name,
            "title": Path(path_str).stem,
            "preview": f"[error parsing: {e}]",
            "size_bytes": 0,
            "lines": 0,
            "mtime": 0,
            "source": "unknown",
            "category": "decisiones",
            "tags": ["error"],
            "priority": 5,
        }


def organize_by_category(items: list[dict]) -> dict:
    cats = {cid: {"label": meta["label"], "description": meta["description"], "icon": meta["icon"], "items": []}
            for cid, meta in CATEGORIES}
    for it in items:
        if it is None:
            continue
        cid = it.get("category", "decisiones")
        if cid not in cats:
            cid = "decisiones"
        cats[cid]["items"].append(it)
    # Inject modelos_activos hardcoded (priority 1 manual entries)
    cats["modelos_activos"]["items"] = list(MODELOS_ACTIVOS_ENTRIES)
    # sort items in each category by (priority asc, size desc, mtime desc)
    for cid in cats:
        if cid == "modelos_activos":
            cats[cid]["items"].sort(key=lambda x: (x.get("priority", 5), -x.get("size_bytes", 0) if x.get("size_bytes") else 0))
            continue
        cats[cid]["items"].sort(key=lambda x: (x.get("priority", 5), -x.get("size_bytes", 0), -x.get("mtime", 0)))
    return cats


# ---------- Secret sanitizer (CRITICAL, runs on every copy) ----------
# Added 2026-04-11 post B6 push block: an API key leaked from memory/S59 into
# docs/encyc/ and GitHub secret-scanning blocked the push. Sanitize ALL
# content copied to docs/encyc/ against a list of known secret patterns.

SECRET_PATTERNS: list[tuple[str, str]] = [
    # Anthropic Claude API keys
    (r"sk-ant-api03-[A-Za-z0-9_\-]{80,}", "sk-ant-api03-[REDACTED_BY_W11_SANITIZER]"),
    (r"sk-ant-[A-Za-z0-9_\-]{20,}", "sk-ant-[REDACTED_BY_W11_SANITIZER]"),
    # GitHub tokens
    (r"ghp_[A-Za-z0-9]{36,}", "ghp_[REDACTED_BY_W11_SANITIZER]"),
    (r"gho_[A-Za-z0-9]{36,}", "gho_[REDACTED_BY_W11_SANITIZER]"),
    (r"github_pat_[A-Za-z0-9_]{82,}", "github_pat_[REDACTED_BY_W11_SANITIZER]"),
    # OpenAI
    (r"sk-[A-Za-z0-9]{48,}", "sk-[REDACTED_BY_W11_SANITIZER]"),
    # AWS
    (r"AKIA[0-9A-Z]{16}", "AKIA[REDACTED_BY_W11_SANITIZER]"),
    # Generic Bearer tokens in curl examples
    (r"Bearer\s+[A-Za-z0-9_\-\.]{40,}", "Bearer [REDACTED_BY_W11_SANITIZER]"),
]

_SECRET_REGEXES = [(re.compile(p), r) for p, r in SECRET_PATTERNS]


def sanitize_secrets(content: str) -> tuple[str, int]:
    """Replace known secret patterns with redacted placeholders.

    Returns:
        (sanitized_content, n_redactions)
    """
    n = 0
    for rx, replacement in _SECRET_REGEXES:
        new_content, count = rx.subn(replacement, content)
        if count > 0:
            n += count
            content = new_content
    return content, n


def copy_top_priority_files(all_items: list[dict]) -> int:
    """Copia los top 20 priority 1 a docs/encyc/ para servir sin CORS.

    CRITICAL: every file is sanitized against SECRET_PATTERNS before write.
    Redaction count is stored in item['_secrets_redacted'] for audit.
    """
    ENCYC_DIR.mkdir(parents=True, exist_ok=True)
    p1 = [it for it in all_items if it and it.get("priority") == 1]
    # dedupe by name, prefer HIGH_VALUE_NAMES
    seen = set()
    selected = []
    for it in p1:
        name = it.get("name", "")
        if name in HIGH_VALUE_NAMES and name not in seen:
            seen.add(name)
            selected.append(it)
        if len(selected) >= 20:
            break
    # fill with other priority 1 if needed
    for it in p1:
        if len(selected) >= 20:
            break
        name = it.get("name", "")
        if name not in seen:
            seen.add(name)
            selected.append(it)

    copied = 0
    total_redactions = 0
    for it in selected:
        src = Path(it["path"])
        if not src.exists():
            continue
        dst = ENCYC_DIR / sanitize_name(it["name"])
        try:
            raw = src.read_text(encoding="utf-8", errors="replace")
            clean, n_redacted = sanitize_secrets(raw)
            if n_redacted > 0:
                print(f"[W11 sanitizer] redacted {n_redacted} secret(s) from {it['name']}")
                total_redactions += n_redacted
            dst.write_text(clean, encoding="utf-8")
            it["copied_to"] = f"encyc/{dst.name}"
            it["_secrets_redacted"] = n_redacted
            copied += 1
        except Exception as e:
            it["copy_error"] = str(e)
    if total_redactions > 0:
        print(f"[W11 sanitizer] TOTAL: {total_redactions} secrets redacted across {copied} files")
    return copied


def main() -> int:
    t0 = time.time()
    print(f"[w11] bundle_mode={BUNDLE_MODE}")
    paths = list_all_sources()
    print(f"[w11] found {len(paths)} .md files")
    if not paths:
        print("[w11] no files found, writing empty encyclopedia")

    path_strs = [str(p) for p in paths]

    items: list[dict] = []
    if path_strs:
        with Pool(processes=min(8, max(1, os.cpu_count() or 4))) as pool:
            items = pool.map(parse_md_file, path_strs)
    items = [x for x in items if x is not None]
    print(f"[w11] parsed {len(items)} items in {time.time()-t0:.1f}s")

    # copy top 20 HIGH-VALUE
    copied = copy_top_priority_files(items)
    print(f"[w11] copied {copied} HIGH-VALUE files to docs/encyc/")

    # organize
    categories = organize_by_category(items)

    # stats
    by_source = {"memory": 0, "vault": 0, "root": 0, "unknown": 0}
    total_bytes = 0
    for it in items:
        src = it.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
        total_bytes += it.get("size_bytes", 0)

    # priority_1_top
    p1 = sorted([it for it in items if it.get("priority") == 1],
                key=lambda x: (0 if x.get("name") in HIGH_VALUE_NAMES else 1, -x.get("size_bytes", 0)))[:20]

    encyclopedia = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bundle_mode": BUNDLE_MODE,
        "source_stats": {
            "memory_files": by_source.get("memory", 0),
            "vault_files": by_source.get("vault", 0),
            "root_files": by_source.get("root", 0),
            "total_items": len(items),
            "total_mb": round(total_bytes / (1024 * 1024), 2),
        },
        "categories": categories,
        "priority_1_top": p1,
    }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(encyclopedia, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[w11] wrote {OUTPUT_JSON} in {time.time()-t0:.1f}s")

    # category counts
    for cid, meta in CATEGORIES:
        n = len(categories[cid]["items"])
        print(f"  - {cid:22s} {n:4d} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
