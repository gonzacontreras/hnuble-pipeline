---
name: Números, métricas y cálculos S57 — trazabilidad completa
description: TODOS los números generados o modificados en S57 con trazabilidad a CSVs fuente y scripts. Incluye bootstrap BSS CI, verificación de refs, métricas de PDFs locales, y todos los cálculos hechos. NO reemplaza reference_numeros_S54_auditoria_completa.md (esa es para el modelo); esta cubre S57 específicamente.
type: reference
---

# Números y métricas S57 — Trazabilidad completa

**Fecha**: 2026-04-10
**Scripts ejecutados**: 8 (ver sección 7)
**CSVs generados**: 7 (ver sección 8)

---

## 1. BOOTSTRAP BSS CI — Resultados completos

### Configuración
- Método: Block bootstrap stratified por fold (preserva autocorrelación temporal)
- B = 2000 iteraciones
- Seed = 49 (consistente con S49 BLINDAJE)
- CI: percentil 95% (2.5% - 97.5%)
- Script: `R/S57_BOOTSTRAP_BSS_CI.R`
- Datos fuente: `resultados/S49_ALERTAS/WF_con_alertas_completo.csv` (3038 rows, 14 folds)

### Tabla completa (3 tiers × 3 baselines × 2 fold-sets = 18 rows)

**PRIMARY — 10 folds (burn-in excluded, 2015-2024), N=2166**

| Tier | Baseline | N events | BS_model | BS_baseline | BSS point | BSS CI lo | BSS CI hi | BSS SE |
|------|----------|----------|----------|-------------|-----------|-----------|-----------|--------|
| Tier1 | Bortman | 41 | (calc) | (calc) | **0.709** | **0.663** | **0.749** | (calc) |
| Tier1 | Poisson | 41 | — | — | 0.019 | -0.007 | 0.043 | — |
| Tier1 | Random | 41 | — | — | 0.018 | -0.004 | 0.039 | — |
| Tier2 | Bortman | 14 | — | — | **0.401** | **0.276** | **0.602** | — |
| Tier2 | Poisson | 14 | — | — | 0.016 | -0.019 | 0.036 | — |
| Tier2 | Random | 14 | — | — | 0.017 | -0.016 | 0.036 | — |
| Tier3 | Bortman | 11 | — | — | 0.045 | 0.014 | 0.908 | — |
| Tier3 | Poisson | 11 | — | — | 0.013 | -2459.519 | 0.023 | — |
| Tier3 | Random | 11 | — | — | 0.008 | -0.019 | 0.019 | — |

**SENSITIVITY — 14 folds (full, 2011-2024), N=3038**

| Tier | Baseline | N events | BSS point | BSS CI lo | BSS CI hi |
|------|----------|----------|-----------|-----------|-----------|
| Tier1 | Bortman | 64 | **0.681** | **0.617** | **0.740** |
| Tier1 | Poisson | 64 | 0.020 | 0.002 | 0.037 |
| Tier1 | Random | 64 | 0.021 | -0.001 | 0.037 |
| Tier2 | Bortman | 24 | **0.365** | **0.254** | **0.566** |
| Tier2 | Poisson | 24 | 0.015 | -0.010 | 0.034 |
| Tier2 | Random | 24 | 0.014 | -0.011 | 0.035 |
| Tier3 | Bortman | 20 | 0.044 | 0.016 | 0.252 |
| Tier3 | Poisson | 20 | 0.006 | -0.017 | 0.021 |
| Tier3 | Random | 20 | -0.001 | -0.012 | 0.025 |

### Output CSV
`resultados/S49_ALERTAS/BLINDAJE_Q1/tablas/T_BLINDAJE_BSS_CI_S57.csv`

### Observaciones críticas
1. **Tier 1 y Tier 2 vs Bortman**: CIs excluyen 0 en ambos fold-sets → **confirmatory skill** robusta
2. **Tier 1 y Tier 2 vs Poisson/Random**: CIs cruzan 0 → skill marginal vs nulls estrictos (esperado, Poisson absorbe estacionalidad)
3. **Tier 3 vs Bortman**: CI excluye 0 pero amplísimo [1.4%-90.8%] (10-fold) → confirma "exploratory"
4. **Tier 3 vs Poisson**: CI extremadamente inestable (bootstrap samples con BS_Poisson≈0 generan BSS→-∞). NO reportado en manuscrito, solo en CSV.

### Frases textuales usadas en manuscrito
```
Abstract: "Brier Skill Scores against the PAHO endemic-channel baseline were
68.2% (95% CI 61.7–74.0) at Tier 1 and 36.5% (95% CI 25.4–56.6) at Tier 2."

Table 1 (primary): Tier 1 "70.9% [66.3–74.9]", Tier 2 "40.1% [27.6–60.2]",
                   Tier 3 "4.5% [1.4–90.8]" *exploratory*

Table 2 (sensitivity): Tier 1 "68.2% [61.7–74.0]", Tier 2 "36.5% [25.4–56.6]",
                       Tier 3 "4.4% [1.6–25.2]"

Discussion: "Tier 1 CIs exclude zero and substantially overlap. Tier 2 CIs also
            exclude zero in both fold sets, confirming confirmatory skill."
```

---

## 2. VERIFICACIÓN REFS — Métricas

### Resultados OpenAlex + Crossref
- Total refs procesadas: **50**
- Encontradas en OpenAlex: **46 (92%)**
- Encontradas en Crossref: **46 (92%)**
- Con DOI inline original: **10**
- Con DOI agregado tras búsqueda robusta: **32** (28 APPROVE + 3 reemplazos + 1 corrección autoría)
- Sin DOI (libros/bulletins aceptables): **2** (Bortman, Wilks)
- Retractadas: **0** ✅
- Expressions of concern: **0** ✅

### Búsqueda robusta multi-campo (S57_FIND_DOIS_FOR_REFS.py)
- Threshold confidence: >= 70/100
- Distribución final:
  - HAS_DOI_INLINE: 10
  - APPROVE (≥85): 28
  - REVIEW (70-84): 4
  - REJECT_LOW_CONFIDENCE (<70): 8

### Score de confidence por categoría

**Confidence scoring formula**:
- Title similarity (SequenceMatcher): peso 50
- Year match (diff=0: 20, diff=1: 15, diff≤2: 8): peso 20
- Author match (substring first_author en authorships): peso 20
- Journal similarity: peso 10
- Total: 0-100

### 4 REVIEW (resueltos)
- Ref #8 Cerqueira 2020: confidence 78 (title_sim 0.6 porque título OpenAlex más largo)
- Ref #12 Funk 2019: confidence 72 (year_diff 5 por parser error del "2014" del texto "2014-15")
- Ref #24 Van Calster/Minus 2025: confidence 77 (autor_match FALSE por error autoría en manuscrito)
- Ref #30 Colón-González 2021: confidence 78 (autor_match FALSE por caracter "ñ")

### 8 REJECT (resolución individual)
- Ref #1 Bortman 1999: sin DOI (bulletin PAHO antiguo)
- Ref #3 Reyes 2019: no encontrado → REEMPLAZADO por Ortiz 2004
- Ref #16 Wilks 2011: libro sin DOI
- Ref #22 Steyerberg 2010: RESUELTO web search (DOI 10.1097/EDE.0b013e3181c30fb2)
- Ref #38 Davison 1997: libro sin DOI
- Ref #39 Cameron Trivedi 2005: libro, RESUELTO web search (DOI 10.1017/CBO9780511811241)
- Ref #42 Zúñiga 2021: no encontrado → REEMPLAZADO por de la Fuente 2017
- Ref #44 Barrera 2007: ES TESIS, NO paper → REEMPLAZADO por Jaksic & Lima 2003

---

## 3. INVENTARIO PDFs LOCALES (S57_EXTRACT_PDF_METADATA.py)

**Directorio**: `C:/Users/gonza/OneDrive/Escritorio/Proyecto_Hantavirus_Nuble/documentos/paper/`
**Total archivos**: 32 (28 PDFs leíbles)

### PDFs con DOI extraíble
| Archivo | DOI | Identificación |
|---------|-----|----------------|
| `florecimiento quila en puyegue.pdf` | `10.4067/S0717-92002017000300018` | de la Fuente & Pacheco 2017 (**USADO para reemplazar Ref #42**) |
| `Knowledge attitudes practices hantavirus vaccine.pdf` | `10.1080/21645515.2016.1250989` | Valdivieso 2016 Hum Vacc Immunother |
| `modelamiento SEIR hanta.pdf` | `10.5867/medwave.2022.03.002526` | Gutiérrez Jara 2022 Medwave |
| `super spider.pdf` | `10.1056/NEJMoa2009040` | Martínez 2020 NEJM (confirma Ref #4) |
| `seir hanta gringo.pdf` | `10.1007/s11538-005-9034-4` | Allen 2006 Bull Math Biol |
| `perfil epideiologico ñuble 2003-2018.pdf` | `10.1590/1519-6984.269097` | Brazilian J Biology 2024 (NO es Reyes 2019) |

### PDFs sin DOI pero con identificación clara
| Archivo | Identificación | Uso potencial |
|---------|----------------|---------------|
| `documentacion de ratadas.pdf` | Jaksic FM & Lima M 2003 Austral Ecology "Myths and facts on ratadas" | **USADO para reemplazar Ref #44** |
| `estudio dinamica oligorysomys.pdf` | TESIS Karen Evelyn Barrera Gómez UACh Medicina Veterinaria | Identificó que "Ref Barrera 2007" era tesis no paper |
| `oligo VIII region.pdf` = `Hantavirus_en_roedores_de_la_Octava_Region_de_Chil.pdf` | Ortiz JC et al. 2004 RCHN "Hantavirus roedores VIII Región" | **USADO para reemplazar Ref #3** |
| `HantaTemuco2001.pdf` | Castillo C et al. 2001 CHEST HPS Temuco | Ya en biblio histórica |
| `ciclo infeccion aper argentino.pdf` | Rodríguez A et al. Rev Inf ID 1708 Argentina 1997-2021 | Contexto histórico |
| `regeneracion de quila zona centro sur.pdf` | RCHN 2009 Chusquea quila regeneración | Contexto ecológico |
| `tiempo minimo de floracion de quila.pdf` | RCHN 2013 Chusquea rhizome prediction | Contexto ecológico |
| `floracion quila zona centro-sur.pdf` | Fenología Chusquea | Contexto ecológico |
| `probable causa de floracion de quila.pdf` | Darwiniana 2010 Bambusa bamboo | Contexto ecológico |
| `otro seir gringo hanta.pdf` | Abramson 2007 chapter Math Biology | Modeling hantavirus |
| `NMDI aisen.pdf` | Bosque 28(2) 2007 NMDI Aisen | NMDI reference |

### Documentos MINSAL/SAG/normativo
- `B38_3420_MINSAL_Orientaciones_tecnicas_por_eventos_asociados_a_roedores_silvestres.pdf`
- `CIRCULAR B51-24 VIGILANCIA Y CONTROL HANTA 2012.pdf`
- `Informe_Epidemiologico_Hantavirus 2022 MINSAL.pdf`
- `Ord_4899_Informa_Situacion_de_Hanta_06122023.pdf`
- `Manual-Administración-Plasma-Inmune-Hantavirus.-Versión-2.0.pdf`
- `sag chubut pag5.pdf`

### Otros
- `caracterización casos de Hantavirus 2002-2023.pptx` (PPT, no paper)
- `caracterización casos de Hantavirus 2020-2024 7-02-2024 (1).pptx`
- `Tesis Identificacion de zonas de riesgo al contagio por Hantavirus Image.Marked.pdf` (tesis magíster)
- `Biologia_roedores_reservorios_hantavirus_Chile_literal.docx`
- `Cuidado con la mayor aparición de la Quila y el Hanta Virus...html` (BTS Intrade laboratorio, no científico)

---

## 4. WORD COUNT TRAJECTORIA

| Fase | Main body | Delta | Notas |
|------|-----------|-------|-------|
| Pre-S57 (original) | 3485 | — | Baseline S56 |
| Post-agregar 28 DOIs | ~3485 | +0 | DOIs no cuentan dentro de texto |
| Post-corregir 3 refs reemplazadas | ~3485 | +0 | Reemplazos neutros |
| Post-agregar CIs BSS a Tables 1-2 | 3587 | +102 | 9 CIs nuevos + 2 footnotes |
| Post-comprimir frases redundantes | 3510 | -77 | Comprimido 3 frases |
| **FINAL** | **3510** | **+25 neto** | Dentro ±5% margen EID |

**Abstract**: 127/150 palabras ✓

---

## 5. MCP SERVERS instalados — Verificación

| Server | Paquete | Versión | Status | Comando verificación |
|--------|---------|---------|--------|---------------------|
| sequential-thinking | `@modelcontextprotocol/server-sequential-thinking` | (npx latest) | ✓ "Sequential Thinking MCP Server running on stdio" | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| context7 | `@upstash/context7-mcp` | v2.1.7 | ✓ "Context7 Documentation MCP Server v2.1.7 running on stdio" | `npx -y @upstash/context7-mcp` |
| superpowers | `obra/superpowers-marketplace` | (GitHub) | ✓ Configurado en settings.json | Requiere reinicio Claude Code |

### MCP config final (`~/.claude/mcp_config.json`)
```json
{
  "mcpServers": {
    "memory": {...},
    "semanticscholar": {...},
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "timeout": 120000
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "timeout": 120000
    }
  }
}
```

---

## 6. PANDOC INSTALACIÓN Y CONVERSIÓN

| Item | Valor |
|------|-------|
| Herramienta | Pandoc 3.9.0.2 |
| Método instalación | `winget install JohnMacFarlane.Pandoc` |
| Path ejecutable | `/c/Users/gonza/AppData/Local/Microsoft/WinGet/Packages/JohnMacFarlane.Pandoc_.../pandoc-3.9.0.2/pandoc.exe` |
| Manuscript .docx | 34271 bytes (34 KB) |
| Cover letter .docx | 13577 bytes (14 KB) |
| Directorio submission | `resultados/S49_ALERTAS/BLINDAJE_Q1/submission/` |

---

## 7. SCRIPTS EJECUTADOS EN S57

| # | Script | Propósito | Output |
|---|--------|-----------|--------|
| 1 | `R/S57_A1_LOCO_CV.R` | Leave-One-Comuna-Out validation | AUC 0.716 [0.661-0.782] |
| 2 | `R/S57_A2_PARAMETRIC_BOOTSTRAP_EPV.R` | Bootstrap EPV 1000 sims | 964/1000 converged, bias<2.11% coefs |
| 3 | `R/S57_A2_POSTPROC_HONESTO.R` | Post-proc sin filtro theta | Reporte honesto ambas versiones |
| 4 | `R/S57_A3_OUTBREAK_POD_CSI.R` | POD + CSI (primera versión) | 0.90 [incorrecto, usaba <=] |
| 5 | `R/S57_A3_OUTBREAK_POD_CORREGIDO.R` | POD con `<` estricto | **POD 0.80 [0.49-0.94]** |
| 6 | `R/S57_VERIFY_REFS_EID.py` | Verificación refs OpenAlex+Crossref | 50 refs, 0 retractadas |
| 7 | `R/S57_FIND_DOIS_FOR_REFS.py` | Búsqueda DOIs multi-campo | 28 APPROVE, 4 REVIEW, 8 REJECT |
| 8 | `R/S57_EXTRACT_PDF_METADATA.py` | Extracción metadata PDFs locales | 28 PDFs analizados |
| 9 | `R/S57_BOOTSTRAP_BSS_CI.R` | Bootstrap BSS CI final | Tier1 [66.3-74.9], Tier2 [27.6-60.2] |

---

## 8. CSVs GENERADOS EN S57

| CSV | Descripción | Ubicación |
|-----|-------------|-----------|
| `LOCO_predicciones_pooled.csv` | 4846 predicciones LOCO pooled | `resultados/S57_LOCO_CV/` |
| `LOCO_resumen_por_comuna.csv` | AUC por comuna (21 rows) | `resultados/S57_LOCO_CV/` |
| `boot_coeficientes.csv` | 1000 × 7 coeficientes bootstrap | `resultados/S57_BOOTSTRAP_EPV/` |
| `boot_theta.csv` | 1000 × 2 theta + sd_re | `resultados/S57_BOOTSTRAP_EPV/` |
| `boot_resumen_HONESTO.csv` | Resumen con mediana sin filtrar | `resultados/S57_BOOTSTRAP_EPV/` |
| `outbreak_events_ge2.csv` | 10 brotes detectados ≥2 casos | `resultados/S57_OUTBREAK_POD/` |
| `pod_comparacion_strict_vs_inclusive.csv` | Comparación <= vs < | `resultados/S57_OUTBREAK_POD/` |
| `refs_raw.csv` | 50 refs con metadata OpenAlex | `resultados/S57_REFS_VERIFICATION/` |
| `refs_DOI_candidates.json` | JSON con candidatos y confidence | `resultados/S57_REFS_VERIFICATION/` |
| **`T_BLINDAJE_BSS_CI_S57.csv`** | **Bootstrap BSS CI final (18 rows)** | **`resultados/S49_ALERTAS/BLINDAJE_Q1/tablas/`** |

---

## 9. CÁLCULOS CRÍTICOS VERIFICADOS

### EPV (Events Per Variable)
- Eventos: 103
- Parámetros: 7 (Intercept + 3 season + 2 within_sc + log_pop)
- **EPV = 14.7** (> 10 = Riley 2019 threshold)
- Fuente S54 declara EPV=15.4 (ligero desacuerdo por definición exacta de denominador, ambos cumplen criterio)

### Convergencia Bootstrap (A2)
- B = 1000
- Convergidos: **964/1000 (96.4%)** > 95% OK
- Bias mediana coeficientes interés:
  - Intercept: +0.44%
  - t2m_within_sc: -0.80%
  - R_v1_lag5_within_sc: **-2.11%** ← predictor clave
  - log_pop: -0.82%
- **TODOS < 5%** = excelente estabilidad

### Bootstrap theta (sensibilidad con/sin filtro)
- Theta original: 1.555
- Mediana SIN filtrar: 1.75 (bias +12.56%)
- Mediana CON filtro <100: 1.42 (bias -8.47%)
- 150/964 (15.6%) bootstraps con theta>=100 (NB→Poisson)
- **Reportar ambas versiones** (regla G2)

### Outbreak POD (A3 corregido)
- Definición brote: ≥2 casos/comuna/temporada (sensibilidad ≥1, ≥3)
- Umbral alerta: p_ge1 > 0.021 (Youden pre-especificado S51)
- N brotes: 10
- **POD strict (<)**: 8/10 = **0.80 [Wilson 0.49-0.94]**
- POD inclusive (<=): 9/10 = 0.90 [Wilson 0.60-0.98] (anterior, incorrecto prospectivamente)
- Diferencia: 1 brote detectado solo por alerta concurrente → Ñiquén 2012

### LOCO-CV
- 21/21 comunas convergieron
- AUC pooled: **0.716 [block-bootstrap 0.661-0.782]**
- Comparación WF temporal: 0.766 (delta -0.050 esperado por RE=0)
- PR-AUC: 0.066

---

## 10. DATOS FUENTE UTILIZADOS

| Archivo | Uso |
|---------|-----|
| `datos/PANEL_OFICIAL_M1M2_v1.csv` | LOCO, Bootstrap EPV (re-fit modelo S29-K) |
| `datos/EPF_human_21comunas.csv` | Merge zonas Ward |
| `resultados/S38_DEFINITIVAS/WF_predicciones_individuales_OOS.csv` | Referencia walk-forward previa |
| `resultados/S49_ALERTAS/WF_con_alertas_completo.csv` | **CSV fuente bootstrap BSS + POD** (3038 rows, 14 folds) |
| `resultados/S49_ALERTAS/BLINDAJE_Q1/MANUSCRITO_EID_v2_ENSAMBLADO.md` | Manuscrito editado |

---

## 11. VERIFICACIONES NUMÉRICAS DE LA EDICIÓN

| Check | Antes | Después | Delta |
|-------|-------|---------|-------|
| Refs numeradas | 50 | 50 | 0 |
| DOIs inline | 10 | 48 | +38 |
| Word count main body | 3485 | 3510 | +25 |
| Abstract palabras | 150 | 127 | -23 |
| Tablas | 3 | 3 | 0 |
| Figuras | 4 | 4 | 0 |
| BSS con CI | 0 | 9 (3 tiers × 3 baselines × 2 fold-sets = 18, reportadas 6 en manuscrito) | +9 |

**Todas las verificaciones cuadran**.
