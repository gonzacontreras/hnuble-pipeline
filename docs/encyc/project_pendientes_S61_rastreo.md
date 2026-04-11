---
name: S61 Pendientes rastreables S60→S61 — lista exhaustiva auditable
description: Lista completa de TODOS los pendientes detectados al cierre de S60. Cada ítem tiene estado actual, cómo verificar si está blindado, y acción concreta si no lo está. S61 debe rastrear cada uno antes de avanzar con automatización.
type: project
---

# S61 Pendientes S60→S61 — Rastreo auditable

**Fecha cierre S60**: 2026-04-11
**Estado manuscrito**: v5_CONDENSED_S60 (3469/3500 palabras main text, 50/50 refs, PAHO 2025 integrada, SEREMI Biobío corregida)
**Deadline submission**: 14-15 abril 2026

---

## 🔴 CRÍTICO — Bloquea submission

### P1 — Supplementary Methods: "reconciliation protocol" referenciada pero NO existente

**Problema**: La frase que Claude insertó en Methods 2.1 línea 59 del manuscrito v5 dice:
> "...were assigned to their probable commune of infection —rather than residence— **by cross-referencing with 2018 INE commune codes (Supplementary Methods)**;"

El texto referencia una sección "Supplementary Methods" sobre reconciliation protocol.

**Auditoría empírica** (2026-04-11, S60):
- Extraído: `pandoc -f docx -t plain C:/Proyectos/Hantavirus_Nuble/resultados/S49_ALERTAS/BLINDAJE_Q1/submission/Supplementary_Materials_v2.docx`
- Output: 331 líneas totales
- Grep ejecutado con patrones: `reconciliation`, `back-allocat`, `SEREMI.*Maule`, `SEREMI.*Biobío`, `Ley 21`, `Law 21`, `pre-2018`, `commune of infection`
- **Resultado: 0 matches**

**Veredicto**: referencia rota. Un reviewer que abra Supplementary no encontrará la sección → sospecha de fabricación.

**Estado en S60**: NO RESUELTO. Detectado al cierre pero no aplicado fix.

**Cómo verificar en S61**: 
```bash
pandoc -f docx -t plain "C:/Proyectos/Hantavirus_Nuble/resultados/S49_ALERTAS/BLINDAJE_Q1/submission/Supplementary_Materials_v2.docx" | grep -iE "reconciliation|back-allocat|Ley 21|Biobío"
```
Si devuelve >0 líneas → resuelto.

**2 opciones de fix (S61)**:

**Opción P1-A (recomendada)**: Agregar subsección "Case reconciliation protocol" a Supplementary_Materials_v2.docx. Base documental ya existente:
- `obsidian_vault/02_Datos/Crisis Datos SEREMI.md` — crisis SEREMI S19 documentada
- `C:/Proyectos/Hantavirus_Nuble/documentos/TRAZABILIDAD_PANEL_OFICIAL.md` — trazabilidad panel M1M2 completa

Contenido mínimo (~150 palabras):
1. 112 casos 2002-2019 de Transparency disclosure SEREMI Ñuble
2. 24 casos 2020-2024 de geolocation outbreak file
3. Cross-reference con códigos INE comunales 2018
4. 3 casos excluidos: fecha 30-feb-2020 corregida a 30-mar-2020; comuna "Nacimiento" del Biobío excluida; row con comuna en blanco excluida
5. Decisión comuna de infección (Crisis SEREMI S19 reconciliation)
6. SHA256 `0b87c5b46b1894a822d2c31ce880ef7452e24ba4b98d6e66bffc4b38eeb4802a`
7. 136 casos total, 100 pre-2018, 103 pre-Sep-2018

**Opción P1-B (rápida)**: Eliminar "(Supplementary Methods)" de la frase en Methods main text. 2 min, menos defensible.

---

## 🟡 ALTOS — Afectan coherencia interna

### P2 — STROBE Checklist Item 5 Setting sin actualizar

**Problema**: el STROBE_Checklist.docx item 5 dice:
> "L59: Ñuble Region, 21 [communes]"

No menciona Ley 21.033 ni SEREMI Biobío pre-2018. Con la frase inserted en v5 Methods, el checklist debería actualizarse para consistencia.

**Auditoría empírica**:
- Extraído con pandoc desde `STROBE_Checklist.docx`
- Línea 46 encontrada: `"Methods — Setting   Describe setting,     ✅ Yes       L59: Ñuble Region, 21"`
- Sin mención Ley 21.033

**Estado en S60**: NO RESUELTO.

**Cómo verificar en S61**:
```bash
pandoc -f docx -t plain "STROBE_Checklist.docx" | grep -n -iE "setting" | head -5
```

**Fix (S61, 1 min)**: agregar 1 línea al item 5:
> "L59: Ñuble Region, 21 communes; pre-2018 period under SEREMI Biobío jurisdiction, back-allocated per Ley 21,033 (see Methods 2.1)"

---

### P3 — Verificación cross-manuscript del número 103 vs 100 casos pre-2018

**Estado**: ✅ CONFIRMADO correcto en S60 pero sin auditoría cruzada formal.

Números verificados con `Rscript` en S60 sobre `PANEL_OFICIAL_M1M2_v1.csv`:
- Total: **136 casos** (2002-2024)
- Pre-2018 (year<2018): **100 casos**
- Pre-Sep-2018 (year<2018 OR year=2018 & month<9): **103 casos**
- Post-Sep-2018: **33 casos**

La frase Methods v5 usa `n = 103` (pre-Sep-2018, porque Ley 21.033 vigente 6-sep-2018).

**Script R de verificación** (ejecutable S61):
```R
p <- "C:/Proyectos/Hantavirus_Nuble/datos/PANEL_OFICIAL_M1M2_v1.csv"
library(data.table)
d <- fread(p)
cat("Total:", sum(d$cases, na.rm=TRUE), "\n")
cat("Pre-2018 year<2018:", sum(d$cases[d$year<2018], na.rm=TRUE), "\n")
cat("Pre-Sep-2018:", sum(d$cases[d$year<2018 | (d$year==2018 & d$month<9)], na.rm=TRUE), "\n")
```
Output esperado: 136 / 100 / 103.

**Cómo verificar en S61**: ejecutar el script R anterior. Si coincide → OK. Si no → verificar que panel no cambió.

---

### P4 — URL PAHO 2025 verificación en vivo antes de submit

**Estado**: ✅ Verificada en S60 con WebFetch.

URL oficial: `https://www.paho.org/en/documents/epidemiological-alert-hantavirus-region-americas-19-december-2025`

Título exacto: "Epidemiological Alert - Hantavirus in the Region of the Americas - 19 December 2025"

Disponible en 4 idiomas: English, Español, Português, Français.

**Cómo verificar en S61**: 
```bash
curl -s -k -o /dev/null -w "%{http_code}" "https://www.paho.org/en/documents/epidemiological-alert-hantavirus-region-americas-19-december-2025"
```
Esperar 200.

---

## 🟢 BAJOS — Housekeeping

### P5 — Git commit del manuscrito v5 al repo principal Hantavirus_Nuble

**Estado**: NO EJECUTADO en S60.

Archivo existe en disco pero no commiteado:
- `resultados/S49_ALERTAS/BLINDAJE_Q1/MANUSCRITO_EID_v5_CONDENSED_S60.md` (~48KB)
- `resultados/S49_ALERTAS/BLINDAJE_Q1/submission/MANUSCRITO_EID_v5_CONDENSED_S60.docx` (~34KB)
- `resultados/S49_ALERTAS/BLINDAJE_Q1/submission/MANUSCRITO_EID_v4_FINAL_S58_BACKUP_PRE_S60.docx` (~34KB backup)

**Comando S61**:
```bash
cd C:/Proyectos/Hantavirus_Nuble
git add resultados/S49_ALERTAS/BLINDAJE_Q1/MANUSCRITO_EID_v5_CONDENSED_S60.md
git add resultados/S49_ALERTAS/BLINDAJE_Q1/submission/MANUSCRITO_EID_v5_CONDENSED_S60.docx
git add resultados/S49_ALERTAS/BLINDAJE_Q1/submission/MANUSCRITO_EID_v4_FINAL_S58_BACKUP_PRE_S60.docx
git commit -m "S60: v5 CONDENSED 3469/3500 + SEREMI Biobío + PAHO 2025 + 25 ediciones + round 2 condensation"
```

**Nota**: NO pushear al remote (el proyecto Hantavirus_Nuble puede no tener remote o Gonzalo puede no querer push).

---

### P6 — Memoria S60 conclusion_final desactualizada

**Problema**: El archivo `memory/project_sesion_code_S60_conclusion_final.md` fue escrito ANTES de:
- Detectar exceso word count (3857 vs 3500)
- Corregir SEREMI Maule → Biobío
- Integrar PAHO 2025 Epi Alert
- Aplicar 25 ediciones condensador + 4 ediciones round 2

**Estado**: PARCIALMENTE INCORRECTO. Contiene la versión previa sin condensación.

**Acción S61**: archivo reemplazado por `project_sesion_code_S60_MASTER_COMPLETO.md` (este batch) que tiene la versión final correcta. El conclusion_final debe marcarse como SUPERSEDIDO o actualizarse.

---

### P7 — Limpieza archivos temporales .tmp_*

**Estado**: 15+ archivos temporales en `C:/Proyectos/Hantavirus_Nuble/`:

Scripts R:
- `.tmp_audit_cases.R`, `.tmp_audit_cases2.R`, `.tmp_audit_oficial.R`, `.tmp_audit_final.R`
- `.tmp_confirm.R`
- `.tmp_scoring_S60.R`, `.tmp_scoring_S60_v2.R`
- `.tmp_decision_S60.R`
- `.tmp_wordcount.R`, `.tmp_wordcount_v4.R`, `.tmp_wordcount_v4_strict.R`, `.tmp_wordcount_plain.R`

Scripts Python:
- `.tmp_unwrap.py`
- `.tmp_apply_edits.py`
- `.tmp_apply_edits_fuzzy.py`
- `.tmp_apply_round2.py`
- `.tmp_apply_pahoB.py`

Markdown/data:
- `.tmp_v4_extracted.md`
- `.tmp_v4_condensed.md` (= el markdown fuente de v5, importante conservarlo como trazabilidad)
- `.tmp_v4_plain.txt`
- `.tmp_CONDENSACION_S60.md` (plan de 25 ediciones del agente condensador, importante)
- `.tmp_SRT_ALPHA_S60.md` (puede que ya fue borrado)
- `.tmp_SRT_BETA_S60.md`
- `.tmp_SRT_GAMMA_S60.md`

**Recomendación S61**: NO borrar hasta confirmar trazabilidad completa. Conservar especialmente:
- `.tmp_CONDENSACION_S60.md` (plan de las 25 ediciones, auditoría del agente)
- `.tmp_v4_condensed.md` (fuente editable del v5)

Mover a un subdirectorio `working_s60/` en vez de borrar:
```bash
mkdir -p C:/Proyectos/Hantavirus_Nuble/working_s60
mv C:/Proyectos/Hantavirus_Nuble/.tmp_*.R C:/Proyectos/Hantavirus_Nuble/working_s60/
mv C:/Proyectos/Hantavirus_Nuble/.tmp_*.py C:/Proyectos/Hantavirus_Nuble/working_s60/
mv C:/Proyectos/Hantavirus_Nuble/.tmp_*.md C:/Proyectos/Hantavirus_Nuble/working_s60/
mv C:/Proyectos/Hantavirus_Nuble/.tmp_*.txt C:/Proyectos/Hantavirus_Nuble/working_s60/
```

---

### P8 — Notif ntfy final de cierre S60

**Estado**: NO ENVIADA tras la corrección SEREMI Biobío + PAHO 2025.

**Comando S61** (o al final de este dump):
```bash
curl -s -k -X POST "https://ntfy.sh/hnuble-guardian-7k3q9mXz" \
  -H "Title: S60 CERRADA" -H "Priority: high" -H "Tags: checkered_flag" \
  -H "Click: https://gonzacontreras.github.io/hnuble-pipeline/" \
  -d "Manuscrito v5 3469/3500. SEREMI Biobío OK. PAHO 2025 integrada. Solo P1 Supplementary reconciliation pendiente. Lista completa en memory/project_pendientes_S61_rastreo.md"
```

---

## 🟢 CONFIRMADOS OK — No requieren acción

### OK-1 — Cover Letter v2 limpia

**Auditoría S60**:
```bash
pandoc -f docx -t plain CoverLetter_v2.docx | grep -iE "PAHO.*2023|regional hantavirus|methodological gap|Maule"
```
**Resultado**: cero matches. La versión v2 (2026-04-10 23:43) ya tenía la frase PAHO 2023 removida y NO menciona SEREMI Maule.

Cover letter NO requiere edición.

### OK-2 — PAHO 2023 confirmada como alucinación

**Búsqueda exhaustiva S60** en:
- `memory/` (239 archivos .md) — 0 matches para "PAHO 2023 regional hantavirus guidelines"
- `obsidian_vault/` (133 archivos .md) — 0 matches
- Crossref API — 0 papers con ese título
- PAHO.org — WebFetch 404 en URL genérica, búsqueda Google no verificable

**Veredicto definitivo**: frase confabulada por LLM durante redacción v4 S58. Pasó auditoría S57 refs porque no era entrada en bibliografía sino texto suelto. Eliminada en v5 Conclusions y reemplazada por PAHO 2025 Epi Alert real.

### OK-3 — Backup v4 FINAL S58 intacto

Archivo: `resultados/S49_ALERTAS/BLINDAJE_Q1/submission/MANUSCRITO_EID_v4_FINAL_S58_BACKUP_PRE_S60.docx`
Tamaño: 34,515 bytes
Fecha: 2026-04-10 23:43 (original S58)

Ningún cambio, recuperable en cualquier momento.

### OK-4 — Word count v5 final = 3469/3500 (margen 31)

Medido con Microsoft Word COM `ComputeStatistics(wdStatisticWords)`:
- Introduction: 415
- Methods: 991 (incluye frase SEREMI Biobío +82)
- Results: 1002
- Discussion: 952 (post round 2 condensación)
- Conclusions: 109 (con PAHO 2025 inline)
- **TOTAL: 3484 → re-condensado a 3469 tras PAHO 2025 + eliminación Prist**
- **STATUS: PASS**

### OK-5 — Refs v5 final = 50/50 exacto

Método: grep regex `^\s*\d+\.\s` en References section de `.tmp_v4_condensed.md`.
Última ref: #50 = PAHO 2025 Epi Alert.
Eliminada: Prist et al. 2023 (era #50 anterior).

Conteo exacto mantiene límite EID ≤50.

### OK-6 — Panel oficial M1M2 confirmado 136 casos

Script: `R/S29K_MODELO_FINAL_SIN_ZONE.R` línea 35 lee `PANEL_OFICIAL_M1M2_v1.csv`.
Total scripts R del proyecto verificando este panel: 40+ (ver `grep M1M2` en `R/` directory).
SHA256: `0b87c5b46b1894a822d2c31ce880ef7452e24ba4b98d6e66bffc4b38eeb4802a`.

Panel STD M1 (`M1_panel_v5_DEFINITIVO_100pct_COMUNASTD.csv`) con 133 casos es subset legacy, NO usado por modelo final. Diferencia documentada en `obsidian_vault/02_Datos/Crisis Datos SEREMI.md`.

### OK-7 — Ley 21.033 fechas confirmadas

- Firma decreto promulgatorio: 19-ago-2017 (Bachelet)
- Publicación Diario Oficial: 5-sep-2017
- Vigencia operativa: 6-sep-2018 (Región Ñuble creada administrativamente)

Fuente: Wikipedia Región de Ñuble (verificado S60 con WebFetch), BCN Chile `idNorma=1107597`.

Separó a Ñuble de la **Región del Biobío** (NO del Maule).

---

## Orden de ejecución S61 (estimado 20-25 min)

1. **P1-A** (10 min) — Agregar sección "Case reconciliation protocol" a Supplementary_Materials_v2.docx
2. **P2** (1 min) — Actualizar STROBE Checklist item 5
3. **P4** (30 seg) — Re-verificar URL PAHO 2025 con curl
4. **P3** (30 seg) — Re-correr Rscript de 136/100/103 para confirmar
5. **P5** (2 min) — Git commit del v5 manuscript al proyecto
6. **P7** (1 min) — Mover .tmp_* a working_s60/
7. **P8** (30 seg) — Notif ntfy S60 cerrada
8. **Pase a S62**: arrancar automatización del pipeline con mejoras (ver `project_plan_S61_automatizacion_paper.md`)

---

## Estado al cierre S60

- ✅ Manuscrito v5 CONDENSED sustancialmente listo
- 🟡 1 gap crítico pendiente (P1 Supplementary reconciliation)
- ✅ Cover letter limpia
- ✅ Backup v4 intacto
- ✅ Memory bundle real poblado (1756 snippets) para W9 MCC
- ✅ Pipeline 24/7 LIVE en GitHub Actions
- ✅ Número canónicos verificados (136/100/103)
- ✅ SEREMI Biobío corregida
- ✅ PAHO 2025 integrada
- ✅ Discrepancia 133 vs 136 explicada (Crisis SEREMI S19)
- ✅ PAHO 2023 confirmada como alucinación
- ✅ 2 DOIs fabricados detectados (Fernández-Manso, Dimitriadis)

**P(accept) EID estimada post-S60**: ~97% (con P1 resuelto). ~85% (con P1 sin resolver).
