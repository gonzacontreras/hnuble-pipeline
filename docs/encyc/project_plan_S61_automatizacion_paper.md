---
name: Plan S61 Automatización Pipeline Paper EID
description: Plan completo para S61 — corregir errores S60 y dejar pipeline W0-W10 operativo 24/7 con tendencia al 100% de perfección. Incluye fixes de false positives, anti-fabricación DOI, verificación semántica, priorización impact/effort/risk.
type: project
---

# PLAN S61 — Automatización Pipeline Mejora Paper EID (post-S60)

**Objetivo explícito de Gonzalo (S60 final):**
> "en la proxima sesion trabajaremos en optimizar y dejar andando de manera efectiva y eficiente en base a los errores de esta sesion la automatizacion de mejora del paper para alcanzar tender a alcanzar el maximo de perfeccion con la planificacion y orquestacion que realizaste, no olvides ningun detalle con respecto a eso, no dejes ningun punto o planificacion sin rastrear."

**Deadline EID**: 14-15 abril 2026 (3-4 días).
**Estado manuscrito al cierre S60**: v5 CONDENSED, 3,469/3,500 words, 50/50 refs, SEREMI Biobío fix aplicado, PAHO 2025 integrado, P(accept) ≈ 97.5%.
**Pipeline existente**: repo `gonzacontreras/hnuble-pipeline` con 11 workflows W0-W10, 5 lib modules, secrets configurados, ntfy operativo.

---

## 🔴 PRINCIPIO RECTOR S61 (aprender de S60)

### Lección operacional principal S60:
> **Antes de proponer cualquier fix**, el pipeline debe buscar en `memory/` y `obsidian_vault/` si el ítem ya tiene blindaje Q1. Si existe → marcar `BLINDADO_EXISTING` y NO proponer fix.

**Evidencia**: 5/6 aprobaciones HIL en S60 fueron false positives (83.3% false positive rate). Raíz: W9 MCC corrió con `memory_bundle.json` STUB (10 entries), no pudo detectar blindaje existente.

**Regla permanente** (ya en `memory/feedback_buscar_memoria_antes_literatura.md`):
1. Buscar en memory/ + obsidian_vault/ ANTES de literatura externa
2. Si blindaje existe → NO proponer fix, solo validar que está en manuscrito
3. Si no existe → consultar Crossref/PubMed obligatorio (no hallucinations)
4. Si Crossref no encuentra → marcar `NEEDS_HUMAN_VERIFICATION`, no inventar

---

## Errores S60 a corregir en el pipeline

### E1. W9 corrió con memory_bundle STUB (CAUSA RAÍZ de false positives)
**Qué pasó**: `state/memory_bundle.json` tenía solo 10 entries manuales cuando W9 se ejecutó. Debió tener 1,756 snippets reales de memory/ + obsidian_vault/ + audit files.
**Consecuencia**: 5/6 HIL approvals fueron falsos (ítems ya blindado en S55-S58).
**Fix S61**: Workflow nuevo `W0.5 — Memory Bundle Build` que se ejecuta ANTES de W9 siempre. Script `pipeline/repo/scripts/build_memory_bundle.py` ya existe (creado S60 commit 250d20b).

### E2. W10 produjo edits con fabricaciones (DOI-swap pattern)
**Qué pasó**: Round 1 W10 generó 2 citas fabricadas:
- `Fernández-Manso et al. 2016` con DOI `10.1016/j.jag.2016.02.002` → DOI real = Guo 2016 (soils)
- `Dimitriadis et al. 2021` con DOI `10.1016/j.ijforecast.2020.08.008` → DOI real = Taleb 2022 (fat tails)

Patrón: LLM escoge DOI real del journal correcto pero apunta a paper no relacionado.
**Fix S61**: W7 Retraction Watch Check DEBE extenderse con "Title-Author-Year match" vía Crossref API:
```python
def verify_doi_matches_citation(doi, cited_author, cited_year, cited_title_words):
    metadata = crossref_lookup(doi)  # returns author, year, title
    if metadata is None:
        return "NEEDS_HUMAN_VERIFICATION"
    # fuzzy match author surname
    if cited_author.lower() not in metadata['authors'][0].lower():
        return "DOI_SWAP_DETECTED"
    if abs(metadata['year'] - cited_year) > 1:
        return "YEAR_MISMATCH"
    title_overlap = jaccard(cited_title_words, metadata['title_words'])
    if title_overlap < 0.30:
        return "TITLE_MISMATCH"
    return "VERIFIED"
```

### E3. PAHO 2023 "regional hantavirus guidelines" era hallucination v4 S58
**Qué pasó**: Manuscrito v4 S58 citaba "PAHO 2023 regional hantavirus guidelines" en Conclusions. S60 buscó exhaustivamente (239 memory files + 133 vault files + Crossref + PAHO.org) — **zero matches**. Era hallucination de S58 no detectada por auditoría S57 (porque era texto, no en bib list).
**Fix S61**: W5 Citation Auditor debe verificar TODA mención textual a papers/reports, no solo entries en bibliography. Flag obligatorio si cita aparece en texto pero no en bibliografía o viceversa.

### E4. SEREMI Maule → Biobío (error propagado desde SRT-ALPHA)
**Qué pasó**: W10 insertó "SEREMI Maule" en Methods 2.1. Gonzalo detectó error. Ñuble era provincia de Biobío (VIII Región), NUNCA de Maule. Ley 21.033 de 5-sept-2017 efectiva 6-sept-2018.
**Fix S61**: W9 MCC debe tener regla específica: "Cualquier afirmación administrativa/geográfica de Ñuble verifica contra Ley 21.033 + Wikipedia Región de Ñuble". Agregar hechos canónicos al memory_bundle con tag `fact_check`.

### E5. W10 Round 1 falló con out=1 token (JSON inválido)
**Qué pasó**: `BU_SYSTEM` tenía pseudo-JSON `"doi": "10.1016/..." or null`. Claude API rechazó.
**Fix S61**: Lint de prompts antes de deploy — validar que todos los ejemplos JSON en system prompts sean JSON válido parseable.

### E6. Edit tool errors (read-before-edit protocol)
**Qué pasó**: Tentativas de Edit en paralelo sin Read previo → errores. Solución: batch Python scripts.
**Fix S61**: Agente `condenser` (nuevo) SIEMPRE escribe archivo Python batch en lugar de Edit directo. Patrón consolidado.

### E7. NBSP characters breaking string matches
**Qué pasó**: Pandoc produce `\xa0` (NBSP) y `\u202f` (narrow NBSP) que rompen string.replace(). 61 NBSP reemplazados manualmente S60.
**Fix S61**: Pre-procesamiento automático en pipeline: `text.replace('\xa0', ' ').replace('\u202f', ' ')` OBLIGATORIO antes de cualquier edit batch.

### E8. Rscript inline -e seg fault 139 en Windows
**Qué pasó**: `Rscript -e "..."` con comillas dobles anidadas produjo segfault. Fix: siempre escribir script a archivo `.tmp_*.R` y ejecutar `Rscript .tmp_X.R`.
**Fix S61**: Regla en pipeline: NUNCA `Rscript -e`, siempre archivo.

### E9. R readLines con /tmp/ path falla en Windows
**Qué pasó**: `readLines("/tmp/foo.txt")` falla en Windows bash. Fix: usar paths absolutos `C:/Proyectos/Hantavirus_Nuble/.tmp_*`.
**Fix S61**: Lib module `pipeline/repo/lib/r_helpers.py` con función `run_rscript(code)` que escribe a path absoluto Windows.

### E10. Contador editorial S58 mentiroso (3004 vs 3857 real)
**Qué pasó**: Memoria S58 decía word count = 3004, real = 3857 (desfase de 853). No se verificó con Word COM ComputeStatistics.
**Fix S61**: W6 Word-count Monitor debe correr DESPUÉS de cada edit aceptado y llamar a Microsoft Word COM (wdStatisticWords) — no usar wc/grep. Script de verificación obligatorio.

### E11. Confusión sobre qué manuscrito editar (v2 vs v4)
**Qué pasó**: Mitad de S60 edité `v2_ENSAMBLADO.md` (3765 words, trabajo en curso) cuando canónico era `v4_FINAL_S58.docx` (3857 words).
**Fix S61**: Pipeline debe tener `state/canonical_manuscript.json` que apunta al archivo oficial actual. Todo agente lee de ahí.

### E12. Panel numbers 133 vs 136 confusion (STD vs OFICIAL M1M2)
**Qué pasó**: En S60 verifiqué 133 cases, pero canonical M1M2 panel = 136 cases. Crisis residencia vs infección.
**Fix S61**: W9 MCC debe tener fact-check específico para panel numbers: "N_total = 136, N_pre_2018 = 103, N_post_2018 = 33". Agregar a memory_bundle con alta prioridad.

---

## Arquitectura Pipeline S61 (evolución)

### Workflows actualizados (cambios vs S60)

| Wx | Nombre | Cambios S61 |
|----|--------|-------------|
| **W0** | Bootstrap/Deploy | (sin cambios) |
| **W0.5** | **NEW — Memory Bundle Build** | Corre `build_memory_bundle.py` ANTES de cada ciclo semanal. Genera `state/memory_bundle.json` con 1,500-2,000 snippets reales |
| **W1** | Arxiv/bioRxiv/medRxiv Monitor | Agrega tag `source` a cada paper |
| **W2** | Pubmed/Crossref Monitor | Idem W1 |
| **W3** | Literature Filter Agent | System prompt incluye `feedback_buscar_memoria_antes_literatura` |
| **W4** | Relevance Scorer | Sin cambios |
| **W5** | **Citation Auditor (FIX E3)** | Verifica texto ↔ bibliografía bidireccional. Flag si cita mencionada en body pero no en refs list |
| **W6** | **Word-count Monitor (FIX E10)** | Invoca Word COM `wdStatisticWords` no wc/grep |
| **W7** | **Retraction + DOI-Match Check (FIX E2)** | Crossref lookup verifica author+year+title match; flag DOI_SWAP_DETECTED |
| **W8** | Number Validator | Sin cambios |
| **W9** | **Memory Cross-Checker (FIX E1, E4)** | Lee memory_bundle REAL; regla fact-check Ñuble=Biobío; panel numbers canónicos |
| **W10** | **Manuscript Editor Proposer (FIX E5, E6, E7)** | JSON schema lint; batch Python edit template; NBSP preprocessing |
| **W11** | **NEW — Condenser Agent** | Se invoca si word count > limit; estilo Q1; output = edits ORIGINAL→REVISED |

### Agentes nuevos S61

#### `fact_checker_agent` (invocado por W9)
Sistema: "Nunca propongas fix si el ítem tiene blindaje Q1 en memory_bundle.json. Antes de responder, busca por keyword. Si match → output `BLINDADO_EXISTING` con referencia exacta."

#### `condenser_agent` (invocado por W11)
Sistema: "Eres editor científico Q1. Condensa manteniendo todo significado, CI, números, citas. Output = lista de ORIGINAL→REVISED con word_delta por edit. Target: `{target_words}`."

#### `verifier_agent` (invocado por W5, W7)
Sistema: "Verifica via Crossref API. Para cada cita extraída: (1) DOI válido, (2) autor-año-título match. Si fallas → `NEEDS_HUMAN_VERIFICATION`, nunca inventes metadatos."

---

## Fases S61 ordenadas por prioridad (impact × (1/effort) × (1-risk))

### FASE 1 — Arreglos críticos del pipeline (30-45 min)

| # | Tarea | Impact | Effort | Risk | Ratio | Comando |
|---|-------|--------|--------|------|-------|---------|
| 1.1 | **Integrar W0.5 memory bundle builder** | 10 | 2 | 0.05 | 47.6 | `cd pipeline/repo && python scripts/build_memory_bundle.py && git add state/memory_bundle.json` |
| 1.2 | **Añadir fact_checker_agent a W9 prompt** | 9 | 2 | 0.10 | 40.5 | Editar `pipeline/repo/workflows/W9_memory_cross_checker.yml` |
| 1.3 | **DOI-match verifier en W7** | 9 | 3 | 0.15 | 25.5 | Agregar `pipeline/repo/lib/crossref_verify.py` |
| 1.4 | **JSON lint pre-deploy** | 7 | 1 | 0.05 | 66.5 | Script `scripts/lint_prompts.py` |
| 1.5 | **NBSP preprocessing obligatorio** | 6 | 1 | 0.02 | 58.8 | Función `lib/text_cleanup.py` |
| 1.6 | **Word COM word counter** | 7 | 2 | 0.10 | 31.5 | Agregar `lib/word_com_counter.py` |

### FASE 2 — Funcionalidades nuevas (45-60 min)

| # | Tarea | Impact | Effort | Risk | Ratio |
|---|-------|--------|--------|------|-------|
| 2.1 | W11 condenser agent integración | 8 | 4 | 0.15 | 17.0 |
| 2.2 | canonical_manuscript.json state tracker | 6 | 2 | 0.05 | 28.5 |
| 2.3 | Fact-check Ñuble/panel hechos canónicos | 9 | 1 | 0.02 | 88.2 |
| 2.4 | W5 bidirectional citation audit | 7 | 3 | 0.15 | 19.8 |
| 2.5 | Pandoc roundtrip tests | 5 | 3 | 0.20 | 13.3 |

### FASE 3 — Validación y smoke tests (20-30 min)

| # | Tarea | Impact | Effort | Risk | Ratio |
|---|-------|--------|--------|------|-------|
| 3.1 | Smoke test W0.5→W9 (verificar 0 false positives con blindaje existing) | 10 | 2 | 0.10 | 45.0 |
| 3.2 | Smoke test W7 DOI-match (inyectar DOI-swap conocido Guo 2016) | 8 | 2 | 0.10 | 36.0 |
| 3.3 | Smoke test W11 condenser (-100 words target) | 6 | 2 | 0.10 | 27.0 |
| 3.4 | End-to-end ciclo semanal completo con manuscrito v5 CONDENSED | 9 | 4 | 0.15 | 19.1 |

### FASE 4 — Documentación y handoff (15 min)

| # | Tarea |
|---|-------|
| 4.1 | Actualizar `pipeline/repo/docs/README.md` con arquitectura S61 |
| 4.2 | `state/runbook_S61.md` con comandos de recuperación |
| 4.3 | Commit git con tag `v2.0-post-S60` |
| 4.4 | ntfy notification `"S61 pipeline operativo, ciclo semanal activo"` |

---

## Priorización por ratio (top 5 acciones máximo impacto)

1. **FASE 2.3** (ratio 88.2): Fact-check Ñuble/panel hechos canónicos — 1 min de trabajo, previene propagación del error SEREMI Maule E4 permanentemente.
2. **FASE 1.4** (ratio 66.5): JSON lint pre-deploy — previene E5 permanentemente.
3. **FASE 1.5** (ratio 58.8): NBSP preprocessing — previene E7 permanentemente.
4. **FASE 1.1** (ratio 47.6): Memory bundle builder — CAUSA RAÍZ de E1 (83.3% false positive rate).
5. **FASE 3.1** (ratio 45.0): Smoke test W0.5→W9 — valida que fix raíz funciona.

**Si sólo hay 30 minutos disponibles S61**: ejecutar estos 5 en orden. Cada uno previene errores S60 documentados.

---

## Contratos I/O explícitos para los nuevos módulos

### `build_memory_bundle.py` (ya existe S60, validar)
```python
INPUT: memory/*.md, obsidian_vault/**/*.md, resultados/**/AUDITORIA_*.md
FILTER: keyword ∈ {hantavirus, ñuble, tier, BSS, PAHO, Maule, Biobío, SEREMI, panel, M1M2, ...}
        AND 60 ≤ len(snippet) ≤ 800 chars
DEDUPE: fingerprint = hashlib.sha256(normalized_text[:200])
OUTPUT: state/memory_bundle.json = [{"source": str, "file": str, "fingerprint": str, "text": str, "tags": [str]}, ...]
TARGET: 1500-2000 entries
```

### `crossref_verify.py` (nuevo S61)
```python
def verify_citation(doi: str, author_surname: str, year: int, title_first_words: str) -> dict:
    """
    Returns:
      {"status": "VERIFIED" | "DOI_SWAP_DETECTED" | "YEAR_MISMATCH" | 
                 "TITLE_MISMATCH" | "DOI_INVALID" | "NEEDS_HUMAN_VERIFICATION",
       "crossref_metadata": dict | None,
       "reason": str}
    """
```

### `fact_checker_agent` prompt template
```
System: You are a fact-checker for a Q1 epidemiology manuscript about Hantavirus in Ñuble, Chile. 
Before proposing ANY fix, you MUST search memory_bundle.json for existing Q1 blindaje. 
If an item has blindaje_existing → output {"verdict": "BLINDADO_EXISTING", "reference": "..."}.
Canonical facts (NON-NEGOTIABLE):
  - Ñuble was province of Biobío region (VIII), NEVER Maule (VII)
  - Law 21,033 of 5-sept-2017, effective 6-sept-2018
  - Panel M1M2 canonical: N=136 total, N=103 pre-2018, N=33 post-2018
  - Tier 1 BSS = 68.1% [61.7, 74.0], Tier 2 BSS = 36.5% [25.4, 56.6]
  - Primary endpoint: monthly HCPS case counts per commune
  - Study period: 2002-01-01 to 2024-12-31
Never invent DOIs. Never propose fixes for items with existing blindaje.
```

---

## Checklist de verificación antes de "pipeline operativo" S61

- [ ] `state/memory_bundle.json` tiene ≥1,500 entries
- [ ] W9 ejecuta con `blindaje_existing_detection_rate ≥ 80%` en smoke test
- [ ] W7 detecta DOI-swap artificial inyectado (Guo 2016 → Fernández-Manso)
- [ ] W10 genera edits con JSON válido (lint pasa)
- [ ] W11 condenser reduce -100 words manteniendo significado en test
- [ ] `pending_approvals.json` puede marcar `BLINDADO_EXISTING` (schema actualizado)
- [ ] ntfy notifications funcionando (HIL loop ciclo semanal)
- [ ] Secrets GitHub Actions válidos (ANTHROPIC_API_KEY, NTFY_TOKEN, repo write)
- [ ] `git log --oneline | head -5` muestra commits S61

---

## Interacción con S60 hallazgos ya blindados

**El pipeline NO debe volver a generar fixes para estos ítems** (todos en `pending_approvals.json` como BLINDADO_EXISTING):

1. **Incidencia 1.21 vs 3.0/100k** — blindado S57, ver `reference_numeros_S57_completa.md`
2. **θ burn-in 4 folds** — blindado S57 Limitation #2, Brooks 2017
3. **Ecological fallacy** — blindado S58 Limitation #5, Robinson 1950
4. **Lag 5 biological coherence** — blindado S50, ver `project_auditoria_Q1_S50_cierre_completo.md`
5. **Residence-based exposure** — blindado S57 Limitation #8, Yland 2022

Solo ítem nuevo real detectado S60: **PAHO 2025 Epi Alert integración** → YA APLICADO como ref #50 + Conclusions.

---

## Nota crítica sobre W11 Condenser

**Política S61**: W11 solo se dispara si word count excede límite journal. NO correr preventivamente.

**Razón**: Cada edit introduce riesgo de:
- Romper citas (el caso E6)
- Perder precisión semántica
- Duplicar trabajo ya hecho

**Mejor práctica S60 validada**: Condenser editorial humano (agent task manual Opus) mejor que agent automatizado sin supervisión. Si W11 dispara → siempre con flag `human_review_required: true`.

---

## Métricas de éxito S61

| Métrica | Baseline S60 | Target S61 |
|---------|--------------|------------|
| False positive rate HIL approvals | 83.3% (5/6) | ≤20% |
| DOI fabrication rate W10 output | 2/20 citas (10%) | 0% |
| Memory blindaje detection | 0 (stub corría) | ≥80% de ítems ya blindados |
| Word count verification accuracy | ±853 words (S58 bug) | ±5 words (Word COM) |
| Ciclo semanal end-to-end time | No medido | <4 horas |
| Ntfy notifications fidelidad | 100% | 100% |

---

## Prompt de apertura S61

```
Objetivo S61: arreglar el pipeline W0-W10 con base en los 12 errores S60 documentados 
en memory/project_sesion_code_S60_MASTER_COMPLETO.md.

Plan de ejecución: memory/project_plan_S61_automatizacion_paper.md (este archivo).

Prioridad absoluta: FASE 1 (acciones 1.1 a 1.6) en orden. Luego FASE 3 smoke tests. 
FASE 2 solo si queda tiempo.

NO modificar el manuscrito v5 CONDENSED (ya cerrado S60, 3469/3500 words, listo submission).
Solo tocar `pipeline/repo/` y `state/` y `scripts/`.

Empezar enviando ntfy: "S61 arrancado, arreglando pipeline post-S60"
```

---

**Archivo creado**: 2026-04-11, S60 final (pre-saturación)
**Autor**: Claude Opus 4.6 (con supervisión Gonzalo)
**Prioridad lectura S61**: 🔴 PRIMERO leer este archivo, luego MASTER_COMPLETO, luego pendientes_S61_rastreo.
