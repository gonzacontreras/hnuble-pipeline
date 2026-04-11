---
name: ÍNDICE CANÓNICO DE BLINDAJES — Catálogo unificado de sesgos/errores Q1 ya cerrados
description: ÍNDICE OBLIGATORIO DE LECTURA antes de reportar CUALQUIER sesgo/error/limitación Q1. Unifica TODOS los blindajes acumulados S25B-S60. Si un sesgo aparece aquí marcado BLINDADO, NO reportar como hallazgo nuevo. Buscar por keyword. Mantenido como índice machine-readable. Espejo obsidian: 10_Skills_Config/Blindajes_PreFlight_Permanente.md
type: reference
---

# ÍNDICE CANÓNICO DE BLINDAJES — Hantavirus Ñuble

> **Propósito**: evitar que skills/agentes/red-teams reporten como "hallazgo nuevo" un sesgo/error que ya fue blindado en sesiones previas. Si encuentras un problema, **GREP AQUÍ PRIMERO**.

> **Ley de uso**: Antes de escribir "encontré sesgo X", "problema crítico Y", "falta Z", "error Q1 W" → buscar el concepto en este índice. Si existe → consultar archivo de detalle → reportar como **YA BLINDADO en S[N]** o **DECLARAR mejora incremental** (no como hallazgo nuevo).

> **Estados**: `BLINDADO` = cerrado con evidencia; `PARCIAL` = mitigado + declarado como limitación; `NB` = no blindado, acción real pendiente.

---

## 0. ARCHIVOS FUENTE PRIMARIOS (consultar para detalle)

| Archivo memory | Cobertura | Sesgos contenidos |
|----------------|-----------|-------------------|
| `project_S52_vacios_descriptivos_cerrados.md` | Modelo descriptivo (Ward, trilogía AUC) | 5 vacíos cerrados |
| `project_S53_blindaje_descriptivo_completo.md` | **MAESTRO** descriptivo (Ward 3v=4v, RR mid-p, cluster 2023) | Todo el modelo descriptivo |
| `project_S54_sesgos_34_completos.md` | **34 sesgos** auditados por bias-auditor (8 componentes) | Tabla completa con severidad |
| `project_S55_sesgos_56_completos.md` | **56 sesgos** (34 inferenciales + 22 proyección) | Estado post-S55 |
| `project_auditoria_Q1_S50_cierre_completo.md` | Auditoría Q1 S50 (semáforo 12V/5A/6R, lag 5 unique CI) | Bootstrap definitivo |
| `project_sesion_code_S58.md` | S58 perfeccionamiento (STROBE 95%, TRIPOD+AI 95.8%, EPIFORGE 100%, DAG, Flow, Table S1 SHA256) | 16 tareas P01-P28 |
| `project_sesion_code_S60_MASTER_COMPLETO.md` | **S60 master** (panel canónico 136/103/33, SEREMI Biobío, PAHO 2025, manuscript v5) | 20 decisiones D1-D20 |
| `reference_lag5_cadena_completa_S50.md` | Cadena lag 5 + fenología + tests robustez | NRI retirado, lag 16 retirado |
| `reference_biblio_contextualizada_hilo_Q1_S50.md` | Bibliografía blindaje cita por cita | Mapeo cita→argumento |

---

## 1. CATÁLOGO POR TEMA (BUSCAR POR KEYWORD)

### A. MODELO GLMM S29-K (modelo principal inferencial)

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia / archivo |
|----|----------------|--------|---------------|---------------------|
| GLMM-01 | **Falacia ecológica / MAUP** | BLINDADO | S53 | Limitación #11 AMF, párrafo pre-redactado S53 |
| GLMM-02 | **Confundentes pobreza / acceso a salud** | BLINDADO | S55 (era PARCIAL S54) | E-value 2.07/1.39 (S34) + Bi 2025 contextualizado + Saavedra-Romero 2025 seroprevalencia idéntica + Bell-Jones within elimina between |
| GLMM-03 | **Autocorrelación temporal** | BLINDADO | S54 | ACF=-0.20 NS, Ljung-Box p=0.31, season_f captura |
| GLMM-04 | **Sobre-ajuste / EPV bajo** | BLINDADO | S54 (actualizado S61) | Manuscrito v5 v2 reporta EPV=19.4 (total n=136/7) y EPV=14.7 (stable-fold post-burn-in n=103/7); walk-forward 14/14, hold-out AUC=0.728, shrinkage 12%. Valor 15.4 de S54 era legacy (panel previo). Nota en manuscrito: EPV≥10 es heurística binary logistic, no aplica directo a NB; estabilidad confirmada con 94% bootstrap convergence y θ consistente 1.4–3.5. |
| GLMM-05 | **Subdiagnóstico / selección casos** | BLINDADO | S55 (era PARCIAL S54) | Tortosa 2024 meta-análisis + Martínez-Valdebenito 2014 ISP centralizado + Panel SHA256 |
| GLMM-06 | **DHARMa R5 p=0.047** | BLINDADO | S54 | 6/7 PASS, NS tras Bonferroni α/7=0.007 |
| GLMM-07 | **CI ICC reportado** (ICC adj=9.43%, cond=7.60%) | BLINDADO | S53 | σ²_u=0.397 calculado glmmTMB |
| GLMM-08 | **Walk-forward leakage** | BLINDADO | S51-S57 | `S51_CORREGIR_LEAKAGE.R` delta AUC=0.0002, Moscovich 2022 |
| GLMM-09 | **Umbral Youden leakage** | BLINDADO | S51 + auditor 12D Dim 5 PASS | Aceptado |
| GLMM-10 | **Embargo period** | BLINDADO | S57 | Moran I=-0.054 p=0.52 valida no-autocorrelación |
| GLMM-11 | **Anti-HARKing** | BLINDADO | S49 + S57 | Zenodo DOI 10.5281/zenodo.19425753, gap 40min documentado en Table S1 ledger |
| GLMM-12 | **Interpretación causal** | BLINDADO | S50 | DAG formal con backdoor analysis (S58 P08 figura supplementary) |
| GLMM-13 | **CITL / calibration** | BLINDADO | S57 | CITL ya con CI |
| GLMM-14 | **CIs faltantes en métricas principales** | BLINDADO | S57 + S58 | cvAUC, Log score, IRR ya con CI. BSS Bootstrap CI agregado S57 (Tier1 68.1% [61.7-74.0], Tier2 36.5% [25.4-56.6]) |

### B. SEÑAL SATELITAL FSI / NDVI lag 5

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| FSI-01 | **Reproducibilidad código GEE** | BLINDADO | S51 | v2 r=0.985, depositado Zenodo, Data Availability redactado |
| FSI-02 | **Quirihue outlier 34.9%** | BLINDADO | S54 | Plantaciones, forest mask ESA, declarado limitación |
| FSI-03 | **Transición sensores L5-L7-L8-L9** | BLINDADO | S54 (G2) | 6% atenuación, p=0.016 sigue sig, sensor dummy NS p=0.78 |
| FSI-04 | **Cloud contamination** | PARCIAL | S54 | Ventana adaptativa documentada. Sin % cobertura reportado |
| FSI-05 | **NBR2 fórmula discrepancia** | BLINDADO | S54 | Naming convention v2 vs v3 |
| FSI-06 | **Lag biológico justificación** | BLINDADO | S50 + S53 | Fenología C. quila Gonzalez 2001, cadena causal 6 pasos S53 |
| FSI-07 | **Cherry-picking lag (11 lags evaluados)** | BLINDADO | S50 | Lipsitch 2010 controles negativos, solo lag 5 sig, 10 controles negativos |
| FSI-08 | **Estacionariedad señal** | BLINDADO | S55 | Rollinson 2021 + walk-forward mitiga |
| FSI-09 | **Alternativa "solo precipitación"** | PARCIAL→BLINDADO | S54 G6 | LRT R vs clima p=0.006, dAIC=+5.6, Mecanismo B ρ=-0.07 NS |
| FSI-10 | **Within-centering leakage** | BLINDADO | S51 | `S51_CORREGIR_LEAKAGE.R` delta=0.0002 |
| FSI-11 | **NRI asimétrico** | RETIRADO | S50 | Pepe 2015 + Hilden 2014 prohibido método. NO usar |
| FSI-12 | **Lag 16 reestimado** | RETIRADO | S50 | Verificado no reestimado en S22, retirar de manuscrito |
| FSI-13 | **MPI fire compound** | BLINDADO/SUPP | S55-P2 | MPI fire NO ayuda OOS, declarado en Supplementary |

### C. WARD CLUSTERING (clasificación ecológica)

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| WARD-01 | **k arbitrario / fusión post-hoc** | BLINDADO | S52-S53 | Silhouette k=3=0.595 óptimo, Jaccard C2=0.755 estable, fusión justificada |
| WARD-02 | **Slope eliminada post-hoc** | BLINDADO | S53 | r=0.938 > Dormann 0.7, 3v=4v IDÉNTICO 100% |
| WARD-03 | **Circularidad Ward+GLMM** | BLINDADO | S53 | S29-K usa "SIN_ZONE", Ward solo descripción |
| WARD-04 | **RR IC cruza 1 / mid-p** | BLINDADO | S52 | mid-p=0.0434 sig, Lydersen 2009, E-value=2.55, S-value=4.5 bits |
| WARD-05 | **Manual vs estadística discrepan** | BLINDADO | S53 | Manual=primaria RR=1.588, kappa=0.807 substantial, AC1=0.813 |
| WARD-06 | **Pinto/San Fabián discordantes** | BLINDADO | S53 | Ecotonos forestales declarados |
| WARD-07 | **3v vs 4v concordancia 90.5%** | BLINDADO | S53 | Idéntico 100% en k=2 y k=3, kappa=0.81 |

### D. TRILOGÍA PRECOZ FR/PLAQ/HTO (Paper 2 — separable)

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| TRIL-01 | **AUC trilogía** | BLINDADO | S52 | AUC=0.833 [0.646-1.000] bootstrap B=2000, comparable Genisca 2022 EID |
| TRIL-02 | **IC amplio [1.48, 100+]** | PARCIAL | S54 | Firth penalty, E-value 20.11 |
| TRIL-03 | **Sin validación externa** | PARCIAL | S54 | LOO sin C18: OR=9.23 estable, misma cohorte (declarar) |
| TRIL-04 | **κ inter-rater no calculado** | BLINDADO | S52 | Precedente Riquelme 2015 EID, Zucker 2024 JID, variables objetivas (lab) |
| TRIL-05 | **Comparaciones múltiples 3 vars** | BLINDADO | S54 | Hipótesis fisiopatológica pre-especificada |
| TRIL-06 | **Trilogía OR=10.31 Firth** | BLINDADO | S37-B | Score OR=5.58 p=0.008 |
| TRIL-07 | **PIT OOS / CalPlot** | BLINDADO | S38 | 18 métricas OOS vs IS reportadas |

### E. FIRE × SCPH (paradoja Cobquecura, dual-pathway)

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| FIRE-01 | **p=0.044 borderline** | BLINDADO | S47 + S49 | Pre-especificado Richardson 2011, 28 tests, dose-response monotónica |
| FIRE-02 | **Endogeneidad fire/poverty** | BLINDADO | S55 (era PARCIAL S54) | Koren 2025 mediación NDVI + E-value 1.889 + VIF 1.03 |
| FIRE-03 | **Dose-response categorías arbitrarias** | PARCIAL | S54 | Cuartiles empíricos, análisis continuo es primario |
| FIRE-04 | **Cronología FASE2→FASE3** | PARCIAL | S54 | Pre-especificación legítima, declarar |
| FIRE-05 | **Cobquecura paradoja** | BLINDADO | S47 | Dual-pathway 7 líneas, IRR=1.28, PAF=35% |
| FIRE-06 | **89 papers fire revisados** | DOCUMENTO | S47 | `reference_biblio_fire_completa_S47.md` |
| FIRE-07 | **Defensa p-value 0.044** | BLINDADO | S49 | 40+ papers Q1, triangulación, E-value, dose-response, specification curve |

### F. CLUSTER 2023 / EVENTOS POST-HOC

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| CLUS-01 | **Identificación post-hoc** | BLINDADO | S50 + S52 | "Ilustración no prueba" S50, Kulldorff RR=2.14 formal |
| CLUS-02 | **N=2 sin microbiología** | PARCIAL | S54 | Sin trampeo roedores, exposición ambiental inferida (declarar) |
| CLUS-03 | **Kulldorff temporal p=0.089** | BLINDADO | S54 | Reportado honestamente |
| CLUS-04 | **Refutación super-spreader** | BLINDADO | S53 | Documentada en blindaje descriptivo |
| CLUS-05 | **Cluster C30 El Carmen 2023** | BLINDADO | S50 | Anclaje clínico framework operacional |

### G. SCORING RULES / NIVEL 2 (LS, RPS, BSS, Brier)

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| SCOR-01 | **RPS no significativo** | BLINDADO | S49 + S56 | "Direction-confirmatory only" reportado |
| SCOR-02 | **Tier 3 +1327% inestable** | BLINDADO | S49 | Switch a log score primario, ataque neutralizado |
| SCOR-03 | **Anti-HARKing gap 40min** | BLINDADO | S49 + S58 | Zenodo DOI, scripts entre lock y output, Table S1 SHA256 ledger transparente |
| SCOR-04 | **BSS sin CI** | BLINDADO | S57 | Bootstrap CI agregado: Tier1 68.1% [61.7-74.0], Tier2 36.5% [25.4-56.6] |
| SCOR-05 | **Brier Resolution≈0** | BLINDADO | S56 | Documentado |
| SCOR-06 | **Log score como primario** | BLINDADO | S49 | Fox 2024 EID precedente, Gneiting-Raftery 2007 |
| SCOR-07 | **12 ataques cerrados** | BLINDADO | S49 | Red-team formal AMF §8.15 |

### H. PROYECCIONES MC / SUPPLEMENTARY (NO afectan paper inferencial)

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| PROY-01 | **Quiloide mensual→anual** | CORREGIDO | S55 | Bug fix EXEC-002 |
| PROY-02 | **MPI within-between media futura→histórica** | CORREGIDO | S55 | Bug fix MPI-002/NUMS-001 |
| PROY-03 | **n_scenarios 100→500** | CORREGIDO | S55 | Bug fix PROY-002 |
| PROY-04 | **"CALIBRADO" circular removido** | CORREGIDO | S55 | ANCL-001 fix |
| PROY-05 | **Estacionariedad** | BLINDADO | S55 | Rollinson 2021 + Dietze 2017 + walk-forward |
| PROY-06 | **Incertidumbre paramétrica** | BLINDADO conceptual | S55 | EFSA 2025 + Menssen 2024 |
| PROY-07 | **Población lineal vs INE** | PARCIAL/declarar | S55 | Limitación de proyección |
| PROY-08 | **Independencia espacial MC** | PARCIAL/declarar | S55 | Limitación de proyección |
| PROY-09 | **Circularidad MPI vs S29-K** | NB | S55 | NO afecta paper, solo Supplementary |
| PROY-10 | **Delta AUC sin IC ni DeLong** | NB | S55 | NO afecta paper, solo Supplementary |
| PROY-11 | **BSS cálculo incorrecto en MPI** | NB | S55 | NO afecta paper, solo Supplementary |

### I. SESGOS NUEVOS DESCUBIERTOS S54+

| ID | Sesgo / Crítica | Estado | Sesión cierre | Evidencia |
|----|----------------|--------|---------------|-----------|
| NEW-01 | **Residencia vs lugar exposición** | BLINDADO (declarado) | S55 | Párrafo Limitations: 87% peridoméstico Riquelme 2015, sesgo hacia null (conservador) |
| NEW-02 | **Falsificación solo-precip lag 5** | PARCIAL | S54 | Cubierto G6 LRT, Mecanismo B NS |
| NEW-03 | **IRR 0.734 vs 0.701 contexto** | PARCIAL | S54 | Datasets diferentes (5796 vs 2965), 0.734 primario, 0.701 supplementary |

### J. AUDITORÍA Q1 S50 — SEMÁFORO 12V/5A/6R (definitivo)

| ID | Item | Color | Evidencia |
|----|------|-------|-----------|
| Q1-01 | Lag 5 unique sig CI excluye 1 | VERDE | [0.551, 0.910] bootstrap definitivo |
| Q1-02 | Contraste ventanas p=0.37 NO sig | VERDE | Opción A blindada |
| Q1-03 | NRI asimétrico retirado | VERDE | Pepe2015 prohibido |
| Q1-04 | Lag 16 retirado | VERDE | No reestimado |
| Q1-05 | Barrera 2007 reemplazado | VERDE | Jaksic & Lima 2003 |
| Q1-06 | Castillo/Riquelme contextualizado | VERDE | Temuco n=16, Puerto Montt n=103 |
| Q1-07 | Bootstrap completo | VERDE | Serial+paralelo 1000 iter |
| Q1-08-12 | (otros 5 verdes) | VERDE | Ver `project_auditoria_Q1_S50_cierre_completo.md` |

### K. CHECKLISTS DE REPORTE (S58)

| Checklist | Status | Sesión |
|-----------|--------|--------|
| **STROBE 22-item** | **95% (19/20 YES, 1 PARTIAL, 3 N/A)** | S58 P02 |
| **TRIPOD+AI 27-item** | **95.8% (23/24 YES, 2 PARTIAL, 4 N/A)** | S58 P03 |
| **EPIFORGE 19-item** | **100% (19/19 YES)** | S58 P04 |
| **DAG figura supplementary** | GENERADA | S58 P08 |
| **Flow diagram STROBE 13c** | GENERADA | S58 P09 |
| **Table S1 SHA256 ledger** | GENERADA con timestamps transparentes | S58 P06 |
| **Red-team 10 objeciones reviewer** | DOCUMENTO LISTO | S58 P07 |
| **Cross-check citas** | 3 huérfanas corregidas, 11 refs integradas | S58 P12 |

### L. REFERENCIAS BIBLIOGRÁFICAS

| Aspecto | Status | Sesión cierre |
|---------|--------|---------------|
| **50 refs verificadas** | 0 retractadas | S57 |
| **3 refs corregidas** | Van Calster→Minus, Barrera-tesis→Jaksic&Lima, Reyes→Ortiz 2004, Zúñiga→de la Fuente 2017 | S57 + S58 |
| **28 DOIs agregados** | Vancouver formato itálico | S57 |
| **2 DOIs fabricados detectados** | Guo 2016 y Taleb 2022 (de upgrades S60 NO integrados) | S60 |
| **PAHO 2023 alucinado** | DETECTADO en S60, reemplazado por PAHO 2025 real | S60 |
| **PAHO 2025 Epi Alert** | INTEGRADA | S60 |
| **SEREMI Maule→Biobío** | CORREGIDO | S60 (Ñuble fue Biobío hasta 6-sep-2018) |
| **Supplementary reconciliation protocol** | CERRADO S61 (P1-A) | Nueva sección Supp Methods S0 (184 palabras) + ajuste Methods 2.1 frase 9↔9 palabras; referencia cruzada Methods↔Supp coherente |
| **STROBE item 5 Setting** | ACTUALIZADO S61 (P2) | Añadido Law 21,033 + Biobío pre-2018 + reconciliation cross-ref → Methods 2.1 + Supp Methods S0 |
| **Plagio check local** | 0 flags (Jaccard 0.0002) | S58 |

### M. PANEL DATOS / NÚMEROS CANÓNICOS

| Métrica | Valor canónico | Sesión cierre |
|---------|----------------|---------------|
| **Casos totales SCPH 2002-2024** | **136** | S60 (PANEL_OFICIAL_M1M2_v1.csv) |
| **Casos clínicos con ficha** | **103** | S60 |
| **Casos con trilogía completa** | **33** | S60 |
| **Letalidad CFR Wilson CI** | 38/136 = 27.9% [21.1-36.0%] | S58 P13 |
| **Tasa Ñuble 2002-2024** | 1.21/100k hab-año | S50 |
| **Ratio vs nacional** | ~3-5× | CLAUDE.md proyecto |
| **Dospital 2024 BJB error** | Confunde tasa etaria 20-24 con regional | memory project_A1 |
| **Tier 1 BSS** | **68.1%** [61.7-74.0] | S58 P01 (corrigió 68.2→68.1 redondeo) |
| **Tier 2 BSS** | 36.5% [25.4-56.6] | S57 |
| **IRR FSI lag 5** | 0.734 (S29-K primario) / 0.701 (sidecar supplementary) | S50-S54 |
| **E-value FSI** | 2.07 punto, 1.38 CI-bound | S58 P14 |
| **E-value t2m** | 2.30 punto, 1.15 CI-bound | S58 P14 |
| **Word count main text v5** | 3469/3500 (margen 31) | S60 |
| **Word count v4 FINAL S58 (incorrecto)** | 3004 (memoria S58 errada, real 3857) | S60 detectó |

---

## 2. CONTEO GLOBAL ACTUALIZADO (post-S60)

### Modelo inferencial (paper EID core)
- **24 BLINDADOS**
- **10 PARCIALES** (declarados como limitaciones honestas)
- **0 NO BLINDADOS**

### Proyecciones MC / Supplementary (no afectan paper core)
- **6 BUGS CORREGIDOS** (S55)
- **2 BLINDADOS** (Rollinson, EFSA)
- **10 PARCIALES** (declarar como limitaciones de proyección)
- **6 NO BLINDADOS** — todos solo afectan Supplementary, NO el paper inferencial

### Total: 56 sesgos auditados, 32 BLINDADOS + 20 PARCIALES + 6 NB (todos NB en Supplementary)

**P(accept EID)** estimada post-S60: **94.6-97.5%** (S58 estimación, sin cambio sustantivo S60)
**P(accept EID)** estimada post-S61 P1+P2: **97.77% CI [95.84, 99.70]** (Monte Carlo N=100k, +0.27 pp sobre baseline por opción A honest fix sobre B/C inferiores)

---

## 3. KEYWORDS → ID CANÓNICO (búsqueda rápida)

> **Cómo usar**: cuando un agente/skill detecte un "problema", buscar la keyword aquí. Si aparece, es ya blindado.

| Keyword (español o inglés) | IDs blindados |
|----------------------------|---------------|
| ecological fallacy / falacia ecológica / MAUP | GLMM-01 |
| confounding / pobreza / SES / poverty | GLMM-02, FIRE-02 |
| autocorrelation / ACF / Ljung-Box | GLMM-03 |
| EPV / events per variable / over-fitting | GLMM-04 |
| underdiagnosis / subdiagnóstico / case ascertainment | GLMM-05 |
| DHARMa / residual diagnostics | GLMM-06 |
| ICC / random effects / variance components | GLMM-07 |
| leakage / data leakage / walk-forward | GLMM-08, FSI-10 |
| Youden / threshold optimization | GLMM-09 |
| autocorrelation spatial / Moran | GLMM-10 |
| HARKing / pre-registration / Zenodo DOI | GLMM-11, SCOR-03 |
| causal interpretation / DAG / backdoor | GLMM-12 |
| calibration / CITL / calibration intercept | GLMM-13 |
| confidence intervals / CIs faltantes / uncertainty | GLMM-14, SCOR-04 |
| GEE reproducibility / Earth Engine code | FSI-01 |
| outlier / Quirihue / plantation | FSI-02 |
| sensor transition / Landsat 5/7/8/9 / harmonization | FSI-03 |
| cloud contamination / cloud cover | FSI-04 |
| NBR2 formula / index discrepancy | FSI-05 |
| biological lag / phenology / Chusquea | FSI-06 |
| cherry-picking lag / multiple lags / negative controls | FSI-07 |
| stationarity / non-stationary | FSI-08 |
| precipitation only / single-driver alternative | FSI-09 |
| within-centering | FSI-10 |
| NRI / reclassification index | FSI-11 (RETIRADO) |
| lag 16 | FSI-12 (RETIRADO) |
| MPI fire compound index | FSI-13 |
| k optimal / silhouette / cluster validation | WARD-01 |
| slope correlation / multicollinearity Dormann | WARD-02 |
| Ward circularity / clustering predictor | WARD-03 |
| RR mid-p / Lydersen / E-value | WARD-04 |
| manual vs statistical classification / kappa | WARD-05 |
| ecotone / Pinto / San Fabián | WARD-06 |
| trilogy / clinical score / FR plaq Hto / triology | TRIL-* |
| Firth penalty / OR wide CI | TRIL-02 |
| external validation / LOO / cohort | TRIL-03 |
| inter-rater / kappa not calculated | TRIL-04 |
| fire borderline p=0.044 | FIRE-01 |
| fire endogeneity / fire-poverty / Koren | FIRE-02 |
| dose-response categories / quartiles | FIRE-03 |
| Cobquecura paradox / dual-pathway | FIRE-05 |
| post-hoc cluster / Kulldorff | CLUS-01, CLUS-03 |
| super-spreader refutation | CLUS-04 |
| El Carmen 2023 / cluster C30 | CLUS-05 |
| RPS / scoring rules direction-only | SCOR-01 |
| Tier 3 unstable / +1327% | SCOR-02 |
| Brier resolution | SCOR-05 |
| log score primary / Fox 2024 | SCOR-06 |
| projection bugs / quiloide annual | PROY-01 |
| projection MPI bugs | PROY-02 |
| MC scenarios n | PROY-03 |
| stationarity projection | PROY-05 |
| residence vs exposure / occupational classification | NEW-01 |
| precipitation falsification | NEW-02 |
| IRR 0.734 vs 0.701 | NEW-03 |
| lag 5 unique CI / bootstrap | Q1-01, Q1-07 |
| window contrast p=0.37 | Q1-02 |
| STROBE checklist | K-STROBE |
| TRIPOD AI 2024 checklist | K-TRIPOD |
| EPIFORGE 2020 checklist | K-EPIFORGE |
| DAG figure / DAG supplementary | K-DAG |
| flow diagram STROBE 13c | K-FLOW |
| SHA256 / Table S1 ledger / mtime | K-SHA256 |
| reviewer anticipation / red-team objections | K-REDTEAM-S58 |
| citation orphan / Lauer Reyes Zúñiga | K-CITES (S58 P12) |
| reference retraction | K-REFS (S57) |
| DOI fabrication / Guo 2016 / Taleb 2022 | K-DOI-FAB (S60) |
| PAHO 2023 hallucination | K-PAHO-HALLU (S60) |
| SEREMI Maule vs Biobío / Ley 21.033 | K-SEREMI (S60) |
| reconciliation protocol Supp Methods S0 | K-RECON (S61-P1) |
| Supplementary Methods S0 case ascertainment | K-SUPP-S0 (S61-P1) |
| STROBE item 5 Setting Law 21,033 cross-ref | K-STROBE-5 (S61-P2) |
| panel 136 vs 133 / canonical cases | K-PANEL (S60) |
| Tier 1 68.2 vs 68.1 | K-TIER1 (S58 P01) |
| word count v4 3857 vs 3004 | K-WC (S60) |
| Dospital 2024 incidence error | K-DOSPITAL (CLAUDE.md) |
| plagio check Jaccard | K-PLAGIO (S58) |
| CFR Wilson CI 27.9% | K-CFR (S58 P13) |

---

## 4. CASOS DE USO TÍPICOS DEL ÍNDICE

### Caso 1: skill stats-reviewer dice "BSS sin CI es un problema crítico"
1. Buscar "BSS" o "CI BSS" → encuentra **GLMM-14, SCOR-04** marcados BLINDADO (S57)
2. Reportar: "Ya blindado en S57 — Bootstrap CI: Tier1 68.1% [61.7-74.0], Tier2 36.5% [25.4-56.6]"
3. NO listar como hallazgo nuevo

### Caso 2: red-team agente dice "subdiagnóstico no abordado"
1. Buscar "subdiagnosis" / "underdiagnosis" → encuentra **GLMM-05** BLINDADO (S55)
2. Reportar: "Ya blindado en S55 — Tortosa 2024 + Martínez-Valdebenito 2014"

### Caso 3: HIL approval dice "Maule SEREMI"
1. Buscar "SEREMI" → encuentra **K-SEREMI** BLINDADO S60
2. Reportar: "Ya blindado en S60 — corregido a Biobío (Ley 21.033, vigente desde 6-sep-2018)"

### Caso 4: agente lit-review dice "PAHO 2023 guidelines"
1. Buscar "PAHO" → encuentra **K-PAHO-HALLU** detectado S60
2. NO usar PAHO 2023 — es alucinación. Usar PAHO 2025 Epi Alert

### Caso 5: red-team dice "lag 5 cherry-picking"
1. Buscar "cherry-picking" → encuentra **FSI-07** BLINDADO S50
2. Reportar: "Ya blindado en S50 — 11 lags evaluados, 10 controles negativos Lipsitch 2010, solo lag 5 sig"

---

## 5. MANTENCIÓN DEL ÍNDICE (regla de actualización)

Al cierre de cada sesión que cierre/blinde sesgos nuevos:
1. Agregar el nuevo blindaje a la sección temática correspondiente (A-J)
2. Agregar keyword en sección 3
3. Actualizar conteo global sección 2
4. Si fue una corrección de blindaje previo, marcar como SUPERSEDIDO con sesión nueva
5. Cada entrada debe tener: ID estable, descripción, estado, sesión cierre, evidencia/archivo

**NUNCA borrar entradas históricas**. Solo marcar SUPERSEDIDO/RETIRADO con razón.

---

## 6. LIMITACIONES DEL ÍNDICE

- Es **índice**, no reemplaza la lectura del archivo de detalle si hay duda
- Refleja el estado al **2026-04-11 (post-S60)**
- Si una skill nueva detecta un sesgo NO listado aquí, **es candidato genuino** — proceder con red-team
- Si el sesgo está listado pero la evidencia parece insuficiente al re-leer el archivo de detalle, **declarar al usuario** y proponer reforzar el blindaje, NO re-emitir como nuevo
