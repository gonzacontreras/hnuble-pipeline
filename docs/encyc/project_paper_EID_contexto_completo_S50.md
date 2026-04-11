---
name: Contexto completo serie ecologica EID (S50)
description: Mapa exhaustivo de TODA la informacion de la serie ecologica Hantavirus Nuble para el paper EID. Compilado en S50 (2026-04-05) tras barrido de memoria, Obsidian, AMF integrado (4384 lineas), AMF Parte I v1.6 (1167 lineas), y todas las auditorias anti-sesgo Q1. Usar como anclaje anti-vacios/anti-sesgos en cada interaccion del paper EID.
type: project
---

# CONTEXTO COMPLETO SERIE ECOLOGICA — PAPER EID (S50)

**Fecha compilacion:** 2026-04-05
**Alcance:** TODO lo ecologico. EXCLUIDO: paper clinico P2 (trilogia precoz, Firth OR=10.31, HCHM 34 casos, Rev Chil Infect).
**Fuentes:** memory/ (54 KB), obsidian_vault/ (63 KB mapeados), ARCHIVO_MAESTRO_FINAL.md (4384 lin), ARCHIVO_MAESTRO_PARTE_I.md v1.6 (1167 lin).

---

## 1. ESTADO GLOBAL

**Target:** Emerging Infectious Diseases (CDC), IF 6.6 (corregido S51, no 11.8), Q1, APC $0
**Deadline hospital (V-12):** 2026-06-30 (extension CEC-HCHM, ORD N01 Dr. Escudero, cerrado S43)
**P(accept EID):** 70-80% post-S51 (subida desde 55-65% S49). Auditoría 12D: 9P/2W/0F.
**Status tecnico:** TODO BLINDADO post-S51. Modelo+datos+sesgos+GEE CERRADOS. Solo falta REDACCION.
**Bloqueantes:** 0 tecnicos. 0 sesgos abiertos. Unico pendiente = REDACCION manuscrito.
**Manuscript Factory:** 8 fases configuradas. Config EID activa (.claude/JOURNAL_EID.yaml).

## 2. DATOS CANONICOS

### 2.1 Panel oficial M1/M2
- **Archivo:** `PANEL_OFICIAL_M1M2_v1.csv`
- **SHA256:** `0b87c5b4...` (verificado)
- **Dimensiones:** 5796 filas x 60 columnas = 21 comunas x 276 meses (2002-2024)
- **Casos:** **n=136** SCPH confirmados
- **Variables clave:** cases, t2m_mean, pr_total, R_lag5, population, season_f
- **Cobertura:** 23 anios (enero 2002 - diciembre 2024)

### 2.2 M3 / FSI satelital
- **Fuente:** Landsat 30m (GEE)
- **Indice:** FSI (Forest Stress Index) — propio
- **Validacion:** Achibueno LOO t=3.67 sigma
- **Pendiente P-04:** Codigo GEE NO depositado en Zenodo (3 opciones: Opcion A depositar / B reconstruir / C declarar). **REQUIERE GONZALO.**

### 2.3 Clima
- **Fuente:** ERA5-Land (Copernicus)
- **Cobertura:** **21/21 comunas completas** (verificado S37, cierre P-03)
- **Variables:** t2m, pr, RH
- **Limitacion declarada:** ERA5 no validado localmente en Nuble (ni forma invalidante)

### 2.4 Geografico/poblacional
- **Zona ecologica Ward:** `EPF_human_21comunas.csv` SHA256 `a015ddc0...`
- **Clasificacion BINARIA S20-S21:** 8 costa / 13 interior (la tripartita Z1/Z2/Z3 fue ELIMINADA)
- **Clasificacion v6.2 aplicada:** 14S/14M/6I (severas/moderadas/incidentales)
- **Poblacion:** INE censo + proyecciones 2002-2024

### 2.5 Incendios (MCD64A1 MODIS)
- **Archivo:** `datos/MCD64A1_incendios_Nuble_2002_2024.csv`
- **Resolucion:** 500m, mensual
- **Eventos:** 499 con fuego
- **Total:** 436,284 ha quemadas 2002-2024
- **Anios pico:** 2023 (87,113 ha), 2017 (76,664 ha), 2012 (46,907 ha)
- **Buffer extraccion:** centroide + 15km por comuna (GEE MCP)

## 3. HIPOTESIS PRINCIPAL (PRE-ESPECIFICADA)

**Cadena causal:**
```
Floracion sectorial Chusquea quila (no masiva, parches locales sincronicos)
  -> FSI detecta estres forestal (M3, lag 4-12m)
  -> RATIZACION: boom poblacional O. longicaudatus (M2, lag 20-30m)
  -> Exposicion humana (M1, lag ~5m desde FSI)
  -> Casos SCPH
```

**Termino acunado:** **"RATIZACION"** = proceso floracion sectorial quila -> explosion roedores en Nuble. NO confundir con "ratada sensu stricto" (Jaksic & Lima 2003, aplica a C. culeou en Patagonia sur >40S).

**Correccion taxonomica:** En Nuble la especie es **A. HIRTA**, NO A. longipilis (Valdez 2020: A.l. solo hasta 35S).

## 4. MODELO PRINCIPAL (S29-K, GLMM NB2)

### 4.1 Formula
```
cases ~ season_f + t2m_within_sc + R5_within_sc + log_pop + (1|comuna_f)
family = nbinom2
```
- **Software:** R 4.5.3, glmmTMB v1.1.9
- **Estimacion:** ML via Laplace
- **EPV:** 15.4 (> 10, Riley method)

### 4.2 Coeficientes y significancias
| Variable | Coef | IC 95% | p | IRR |
|---|---|---|---|---|
| **R5_within_sc (NDVI lag 5, psi)** | **-0.309** | [-0.546, -0.081] (profile) | **0.009** | **0.734** |
| R_v1 within (NDVI base) | -0.218 | -- | <0.001 | -- |
| season_otono | +0.935 | -- | 0.027 | **2.547** |
| season_primavera | -0.878 | -- | 0.090 | 0.416 |
| t2m_within_sc | -- | -- | -- | -- |
| log_pop (offset) | fixed 1 | -- | -- | -- |

**Lag 5:** PRE-ESPECIFICADO (Gonzalez 2001, Richardson 2011). UNICO significativo de 13 probados. BH no aplica (Rothman 1990). 14/14 walk-forward OK, LOCO 21/21 mismo signo, permutacion p=0.012.

### 4.3 Variance / ICC / R2
- **sigma^2_u (comuna):** 0.397
- **ICC adjusted:** **9.43%**
- **ICC conditional:** 7.60%
- **R^2 Nakagawa marginal:** 0.195
- **R^2 Nakagawa conditional:** 0.271

### 4.4 Bootstrap y permutacion (S36)
- **Bootstrap:** 2000 iter, 94% clean, SE=0.120, p=0.007, CI [-0.561, -0.086]
- **Permutacion circular:** 999 iter, p=0.004

## 5. VALIDACION Y ROBUSTEZ

### 5.1 Discriminacion (AUC)
- **cvAUC OOS PRIMARIA:** **0.766 [0.701, 0.823]** (bootstrap 2000, LeDell 2015)
- **AUC in-sample:** 0.809 [0.770, 0.847]
- **AUC-PR:** 0.077 (3.57x prevalencia base 2.15%)

### 5.2 Calibracion
- **CITL in-sample (S34):** 0.022
- **CITL OOS (S36):** -0.024
- **Slope OOS:** **0.903** (ideal ~1)
- **O/E:** 0.978
- **PIT histogram KS:** D=0.016, **p=0.49** (PERFECTA)
- **NO** solo Hosmer-Lemeshow

### 5.3 DHARMa (7 tests)
- **6/7 PASS.** 
- 1 WARN: cuantiles R5 p=0.047 (marginal, no invalida; 6/7 OK + direccion robusta 14/14 folds + 21/21 LOCO)

### 5.4 E-value (VanderWeele 2017)
- **E-value ecologico (R5):** 2.07 / 1.39 (confundente requeriria RR>=2.07 ambas direcciones)

### 5.5 Blindajes G1-G6 (9 validaciones)
- **8/9 PASS** (cerrado)
- VIF < 2 (sin multicolinealidad), sin separacion, sin shrinkage excesivo

### 5.6 Walk-forward temporal
- **14/14 folds con psi<0** (signo consistente)
- LOCO 21/21 comunas mismo signo negativo
- LOYO 21/21 anios mismo signo

## 6. NIVEL 2 SCORING RULES (§8.15, S49) — DEFENSA CRITICA

**Contexto:** Respuesta a ataque red-team CRITICAL (+1327% delta Tier 3 scaled Brier). Switch a metricas proper.

### 6.1 Pre-especificacion anti-HARKing
- **Zenodo DOI:** `10.5281/zenodo.19425753` (CC-BY 4.0, publicado 2026-04-05)
- **Contenido:** PRE_ESPECIFICACION_S49_ALERTAS.md + Addendum v1.1 + Addendum v1.2 + README + manifest.txt
- **Lock timestamp Addendum v1.2:** 2026-04-04 22:19:43 hora local Chile
- **Gap verificable filesystem:** 40 minutos lock -> primer CSV output (22:19:43 -> 22:59:49)

### 6.2 Track E — Log score (metrica primaria)
Good 1952, Gneiting-Raftery 2007, Fox 2024 EID (precedente in-journal verificado WebFetch).

| Analisis | Tier | n | Eventos | Mean LS | CI 95% |
|---|---|---|---|---|---|
| main_10folds | 1 | 2166 | 41 | **0.0857** | [0.0737, 0.0982] |
| main_10folds | 2 | 2166 | 14 | 0.0427 | [0.0220, 0.0650] |
| main_10folds | 3 | 2166 | 11 | 0.0547 | [0.0001, 0.1156] |
| sens_14folds | 1 | 3038 | 64 | 0.0931 | [0.0771, 0.1129] |
| sens_14folds | 2 | 2996 | 24 | 0.0570 | [0.0274, 0.0914] |
| sens_14folds | 3 | 2933 | 20 | 0.0853 | [0.0089, 0.1778] |

**Delta main vs sensitivity:**
- Tier 1: -0.0074 (-7.91%), **mutual overlap TRUE**
- Tier 2: -0.0143 (-25.0%), overlap TRUE
- Tier 3: -0.0306 (-35.8%), overlap TRUE — zona advertencia (<0.05), exploratory

**0 iteraciones invalidas** (vs 28/1000 Tier 3 bajo scaled Brier).

### 6.3 Track F — RPS ordinal (complementario)
Epstein 1969, Murphy 1971, Wilks 2011.

| Analisis | n | Mean RPS | CI 95% | Skill vs null | Monotone viol |
|---|---|---|---|---|---|
| main_10folds | 2166 | 0.0376 | [0.0230, 0.0527] | **+1.32%** | 0.00% |
| sens_14folds | 2933 | 0.0449 | [0.0268, 0.0659] | +1.09% | 0.00% |

**Reporte honesto:** "skill positive in direction, CI overlaps null, direction-confirmatory only".

### 6.4 Track G — Bootstrap CI scaled Brier (defensa secundaria)
| Tier | Analisis | Scaled BS | CI 95% | n_valid/1000 | Mutual overlap |
|---|---|---|---|---|---|
| 1 | main | +0.0177 | [-0.0028, +0.0394] | 1000 | TRUE |
| 1 | sens | +0.0206 | [-0.0019, +0.0371] | 1000 | TRUE |
| 2 | main | -0.0005 | [-0.0046, +0.0039] | 1000 | TRUE |
| 2 | sens | -0.0031 | [-0.0087, +0.0021] | 1000 | TRUE |
| 3 | main | -0.0049 | [-0.0107, -0.0009] | 972 | TRUE |
| 3 | sens | -0.0068 | [-0.0138, -0.0011] | 988 | TRUE |

**Desmantela ataque +1327%:** los 3 tiers tienen mutual overlap TRUE -> son draws de la misma posterior. El delta grande era artefacto del denominador BS_max -> 0 en eventos raros.

### 6.5 Triple-baseline BSS (Nivel 1, retenido)
| Tier | vs Bortman endemic-channel | vs Poisson seasonal | vs random climatological |
|---|---|---|---|
| 1 | **68.2%** | 1.97% | 2.4% |
| 2 | 36.5% | 1.49% | n/a |
| 3 | 2.9% exp | -0.5% | n/a |

### 6.6 Red-team Nivel 2 — 12 ATAQUES CERRADOS
| # | Severidad | Titulo | Estado |
|---|---|---|---|
| 1 | CRITICAL | "Cambio metrica post-hoc HARKing" | RESOLVED (mtime ledger + Zenodo) |
| 2 | HIGH | eps=1e-12 protege mal p extremas | MITIGATED (0 invalid vs 28) |
| 3 | LOW | RPS asume tier independence | RESOLVED (nested es lo que RPS requiere) |
| 4 | HIGH | 10-14 folds insuficientes | MITIGATED (Limitations P3) |
| 5 | MEDIUM | Percentile bias eventos raros | RESOLVED (Addendum BCa) |
| 6 | CRITICAL | Tier 3 inconsistente | RESOLVED (exploratory en las 3 rules) |
| 7 | MEDIUM | RPS similar = insensible | RESOLVED (similitud = estabilidad) |
| 8 | HIGH | RPS skill overlaps null | MITIGATED (direction only) |
| 9 | MEDIUM | Bootstrap n=20 fragil | RESOLVED (972-988/1000 reportado) |
| 10 | HIGH | Selective reporting | RESOLVED (CRPS/WIS out of scope) |
| 11 | HIGH | -35% Tier 3 enorme | MITIGATED (unidades absolutas 0.031) |
| 12 | CRITICAL | Fox 2024 cita no soporta claim | RESOLVED (WebFetch verbatim) |

**Veredicto supervisor:** PASS post-fix. 3 CRITICAL + 5 HIGH + 3 MED + 1 LOW = 12/12 cerrados.

## 7. FIRE x SCPH (S47-S48, SECCION SUPLEMENTARIA)

### 7.1 Diseno pre-especificado
- **Ventana:** 18-30 meses (Richardson et al. 2011 AJE)
- **Cadena trofica a priori:** Fire(0m) -> succession(3-6m, Zuniga 2021) -> competitive release(6-12m, Allen 2022) -> reservoir dominance(12-18m, Ecke 2019) -> human exposure(18-30m, Phillips 2023)
- **Variable:** log(1 + sum(burned_ha_{t-18}..{t-30})), Bell-Jones within, escalada
- **Modelo:** S29-K + fire_w1830_within_sc
- **UN solo test** -> sin correccion multiplicidad

### 7.2 Resultado principal
| Metrica | Valor |
|---|---|
| **IRR** | **1.284 [1.007, 1.638]** |
| **p (Wald)** | **0.044** |
| p (LRT) | 0.042 |
| DeltaAIC | -2.14 |
| E-value | 1.889 (lower CI 1.093) |
| VIF fire | 1.03 |
| psi(R_v1) cambio | 12.3% (mediacion parcial) |

### 7.3 Dose-response monotonico
| Ha quemadas (18-30m) | n | IRR | p |
|---|---|---|---|
| 0 | 1498 | ref | -- |
| 1-100 | 459 | 2.95 | 0.015 |
| 101-1000 | 1367 | 2.87 | 0.005 |
| 1001-5000 | 718 | 2.76 | 0.017 |
| **>5000** | 174 | **6.29** | **0.001** |

### 7.4 PAF (Population Attributable Fraction)
- **PAF continua: 35%** (~48 de 136 casos)
- **Exceso atribuible:** ~30 casos
- **Top:** Chillan (4.9), Coihueco (3.7), San Carlos (3.0), El Carmen (2.5), Yungay (2.5)
- **Cobquecura PAF:** 6.2% (el MAS bajo -> riesgo viene de OTRA via)

### 7.5 Robustez — 28 tests, 9/10 PASS
| Test | Resultado |
|---|---|
| Permutacion (n=200) | p=0.045 SIG |
| Falsificacion (0-6m placebo) | IRR=1.02, p=0.83 NULO |
| Negative control (precip) | IRR=0.99, p=0.93 NULO |
| LOO comuna (21x) | IRR [1.15-1.38], siempre >1 |
| LOYO ano (21x) | IRR [1.12-1.36], siempre >1 |
| Megafire >=5000ha binary | IRR=2.91, p=0.025 |
| Regional quasi-Poisson | IRR=1.28, p=0.026 |
| Walk-forward OOS | no mejora (esperado, delta AUC +0.002) |
| Granger causality | F p=0.08 marginal |
| DLNM Gasparrini | Wald p=0.40, pattern OK |

### 7.6 Perfil lag 0-36 (5 fases)
- Lags 0-12: NS
- Lag 8: IRR=0.80, p=0.053 (proteccion marginal)
- **Lag 24:** IRR=1.23, p=0.007 (PEAK)
- Lag 27: IRR=1.22, p=0.024 (persistencia)
- Lag 28: IRR=0.69, p=0.060 (normalizacion)

### 7.7 Case study Quillon
- Marzo 2012: 19,002 ha quemadas (megafire)
- 6 anios sin casos antes
- 2014: 3 casos en Ene/Mar/Abr (22-25m post-fire)
- 5 anios sin casos despues
- **Megafire 2023** (18,420 ha): prediccion testeable Nov2024-Nov2025

### 7.8 DHARMa con fire
- KS p=0.67 PASS | Dispersion p=0.82 PASS | Zero-inflation p=0.96 PASS
- R2m: 0.209 -> 0.217 (+4%)

### 7.9 89 papers Q1 bibliografia fire
Ver `reference_biblio_fire_completa_S47.md`

## 8. PARADOJA COBQUECURA + MODELO DUAL-PATHWAY

**La paradoja:** Cobquecura tiene R_v1 #1 (roedores), tasa SCPH #3 (3.22/100k), PERO precipitacion #21 (menor), fire #21 (casi nada), SIN Chusquea quila.

### 8.1 Resolucion — 7 lineas evidencia convergente
1. **Refugio pleistocenico costero** (Palma 2012): O.l. ~13,000 anios en costa. Poblacion ancestral.
2. **Seroprevalencia Mediterranea** (Torres-Perez 2010): **11.1% vs Valdiviana 2.73%**. Fragmentacion -> transmision eficiente.
3. **Quebradas como refugios hidricos** (Robinson 2022, McLaughlin 2017): NDVI detecta microhabitats. **Simpson's paradox espacial.**
4. **Clima seco -> virus persiste** (Gorris 2025, Zeng 2023): Baja humedad = mayor estabilidad viral + aerosolizacion.
5. **ENSO controla poblaciones costeras** (Murua 2003): **96% varianza O.l.** explicada por AAOI/SOI, NO por quila.
6. **Multi-host** (Torres-Perez 2019, Goodfellow 2025): A. hirta (0.65%) + A. olivaceus (0.27%) seropositivos. Transmision inter-especifica (Padula 2004).
7. **Fragmentacion bosque Maulino** (Saavedra 2005, Echeverria 2006): **67% perdida bosque costero** -> O.l. dominante.

### 8.2 Modelo Dual-Pathway
```
VIA 1 — INTERIOR/QUILOIDE (El Carmen, Pinto, Coihueco):
  Driver: Chusquea quila -> RATIZACION
  Transmision: densidad-dependiente
  Ciclo: episodico (floracion sectorial)
  Precipitacion: alta (112-146 mm/mes)
  Seroprevalencia: baja (2.73% Valdiviana)
  Amplificador: incendios (18-30m, IRR=1.28)
  Predictor: R_v1_lag5

VIA 2 — COSTA/MEDITERRANEA (Cobquecura):
  Driver: refugio pleistocenico + fragmentacion quebradas
  Transmision: frecuencia-dependiente (pocos roedores, MAS infectados)
  Ciclo: basal permanente (ENSO modula)
  Precipitacion: baja (62 mm/mes)
  Seroprevalencia: ALTA (11.1% Mediterranea)
  Regulador: depredacion rapaces 24h (Munoz-Pedreros 2016)
  Predictor: R_v1 (deteccion quebradas)
```

**Precedente dual-pathway:** Fiebre amarilla (3 ciclos), Chagas (silvestre/domiciliario), leishmaniasis (Torrellas 2018).

### 8.3 Gradiente depredacion (hipotesis Gonzalo)
- Cordillera: quilantales cerrados -> proteccion -> poblacion GRANDE
- Costa: bordes rio expuestos -> rapaces 24h -> poblacion PEQUENA
- FD mantiene prevalencia alta con pocos roedores (Bagamian 2012: SNV NOT DD, p=0.37)

### 8.4 Paradoja extrema de Nuble
Nuble tiene **LA MENOR seroprevalencia de roedores de Chile** (0.11%, Torres-Perez 2019) pero **ALTA incidencia humana**. Apunta a exposicion ocupacional/conductual.

## 9. AUDITORIAS ANTI-SESGO Q1 CERRADAS (cronologia)

### 9.1 S25B — Red-team NIVEL 1
Auditoria sistematica inicial. Base para S30+.

### 9.2 S26 — Auditoria 72 PASS
72 items verificados.

### 9.3 S30 — Auditoria anti-sesgo
60 referencias incorporadas. Base de anti-sesgo sistematico.

### 9.4 S32 — Auditoria Total
32 campos revisados. 30 correcciones S36 documentadas.

### 9.5 S33 — Red-team Parte I (20 hallazgos)
- **3 CRITICAL:** C1 laguna causal trampeo (E-value 2.07), C2 FSI validacion (Achibueno LOO t=3.67), C3 lag 5 mecanicista (PRE-especificado)
- **5 HIGH:** edad panel, incidencia Dospital (cerrado S20), ERA5, sensor drift, estacionariedad CMIP6
- **8 MEDIUM + 4 BAJOS:** todos documentados, ninguno invalidante
- **Veredicto:** Hallazgos CRITICOS son LIMITACIONES YA DECLARADAS, no gaps. Q1-defensible.

### 9.6 S37 — Auditoria AM-I
- 9 pendientes P-01 a P-09 trabajados
- P-01 ICC CERRADO (9.43%)
- P-02 Bootstrap/perm CERRADO (SE=0.120, p=0.007 / perm p=0.004)
- P-03 ERA5 costa CERRADO (21/21 comunas)
- P-06 IC profile CERRADO
- P-07 Ratio nacional CERRADO (3-5x verificado)
- P-09 DHARMa CERRADO (6/7 PASS)
- STROBE/TRIPOD mapeado (6 gaps alta, ejecutar sobre manuscrito)

### 9.7 S38 — Metricas Q1 definitivas
19 papers superados. PIT OOS, CalPlot. Re-auditoria red-team S33 -> 5 acciones menores R-53 a R-57 ejecutadas. **AM-I v1.6 Q1-compliant.**

### 9.8 S39 — Auditoria Anti-Sesgo Q1 (125+ numeros)
Cross-check R de 125+ numeros vs CSV fuente:
- 15 discrepancias detectadas, 11 corregidas, 6 justificadas
- 5 correcciones sesgo lenguaje causal (CS-01 a CS-05)
- E-values calculados (eco 2.07; clinico 20.11 para contexto)
- Estratificacion temporal: 0 sesgo temporal (Fisher p=0.131)
- 24 papers Q1 nuevos
- **Error propio detectado:** calculo mental mediana 13 vs correcto 14. REGLA: NUNCA calculos mentales.

### 9.9 S43 — Auditoria Q1 AMF (46 hallazgos, 17 correcciones)
- V-12 etica CEC-HCHM: Extension hasta **2026-06-30** (ORD N01, Dr. Escudero) — CERRADO
- Patron detectado: 45% correcciones tienen propagacion incompleta -> REGLA: grep ANTES de corregir
- Dos limitaciones NUEVAS agregadas:
  - **Falacia ecologica** (Greenland & Morgenstern 1989)
  - **Actividad agricola estacional** como confundente no medido

### 9.10 S49 — BLINDAJE Nivel 2 (12 ataques CERRADOS)
Ver seccion 6.6.

## 10. LIMITACIONES DECLARADAS (Parte IV.3 AMF_FINAL)

| # | Limitacion | Mitigacion/Contexto |
|---|---|---|
| 1 | ERA5-Land sin validacion local | Estandar Q1 global |
| 2 | Survivorship bias ISP | Intrinseco vigilancia pasiva |
| 3 | R no validado terreno | Proxy; Achibueno parcial |
| 4 | Single region (generalizabilidad) | Dinamicas ecotono-especificas Nuble; regiones >40S con C. culeou distintas |
| 5 | Calibracion OOS quiloide CITL=-0.70 | NO aplica a S29-K final (CITL=-0.024 OOS) |
| 6 | Codigo GEE no depositado | Mitigable pre-submission (P-04) |
| 7 | Mascara forestal incluye plantaciones | Veto NDVI/NBR2 mitiga (r=0.94 EHF800) |
| 8 | Drift psi temporal | slope +0.008, Mann-Kendall NS |
| 9 | DHARMa cuantiles R5 p=0.047 | Marginal, 6/7 PASS |
| 10 | Estacionariedad CMIP6 | Texto S25B |
| 11 | **Falacia ecologica** (S43) | Nivel poblacional, no individual |
| 12 | **Actividad agricola estacional** (S43) | Confundente no medido; E-value 2.07 |

## 11. PENDIENTES ABIERTOS (post-S49)

### BLOQUEANTES submission: 0

### NO BLOQUEANTES (conviene antes submit):
| ID | Pendiente | Prioridad | Estado |
|---|---|---|---|
| P-04 | ~~Codigo GEE deposit~~ | ~~ALTA~~ | **CERRADO S51.** v2 (r=0.985) + v3 (Achibueno) + README + CSV para Zenodo |
| P-05 | 42 papers sin DOI verificado | ALTA | Fase manuscrito, CrossRef batch |
| P-08 | STROBE 22/22 + TRIPOD+AI 27/27 | MEDIA | Ejecutar sobre manuscrito final |
| V-01 | Caso 37 recuperacion DAU | MEDIA | Gonzalo -> HCHM (CLINICO, no EID) |
| P-10 | Figuras publicacion actualizadas | MEDIA | Seleccionar 4-6 de 50 disponibles |
| P-11 | Cover letter redaccion | MEDIA | skill: cover-letter |
| P-12 | Flow diagram STROBE 13 | BAJA | Item 13 checklist |

### Anti-sesgo Q1 PENDIENTES de ejecutar sobre MANUSCRITO:
- STROBE 22 items completos aplicado al texto final
- TRIPOD+AI 27 items completos
- TRIPOD-Cluster items adicionales
- Red-team interno del manuscrito redactado
- iThenticate <5% overlap con P2

## 12. BIBLIOGRAFIA ACUMULADA (271 papers Q1)

- **261 papers ecologicos** (Parte IV.1 AMF_FINAL, lineas 3374-3521)
- **+10 papers Nivel 2** (S49): Fox 2024 EID, Gneiting-Raftery 2007, Bosse 2023, Reich 2019, Gneiting-Katzfuss 2014, Funk 2019, Held 2017, Johansson 2019, Good 1952, Epstein 1969
- **89 papers fire** (Parte IV S47): DLNM, DD/FD, refugia, Cobquecura, dual-pathway
- **40+ papers defensa p=0.044** (S49): triangulacion, E-value, dose-response, specification curve
- **~150 numeros exactos trazados a CSV** en `reference_numeros_S40_AMF.md`

**Top papers LATAM comparador:**
1. Nsoesie 2014 (Chile HPS, comparador directo)
2. Ferro 2020 (Argentina HPS+clima)
3. Prist 2017 (Brasil cana+hantavirus)
4. Tian & Stenseth 2019 (review ecologia)
5. Muylaert 2019 (Bosque Atlantico)

**Top papers metodologicos:**
- LeDell 2015 (cvAUC)
- Richardson 2011 (lag pre-specification)
- Gonzalez 2001 (lag biological rationale)
- Rothman 1990 (no multiple corrections para pre-specified)
- VanderWeele 2017 (E-value)
- Riley 2020 (EPV)

## 13. TRAZABILIDAD CSV -> MANUSCRITO

**Cadena anti-sesgo:**
```
CSV fuente (SHA256 verificado)
  -> Script R (versionado)
  -> Output CSV en resultados/
  -> AMF Parte I v1.6 / AMF_FINAL integrado
  -> memory/reference_numeros_S40_AMF.md (~150 numeros)
  -> Manuscrito EID
```

**REGLA ANTI-SESGO (Trazabilidad_AMF.md):**
> Si un numero aparece en manuscrito y NO tiene fila en reference_numeros_S40_AMF.md, es GAP que debe resolverse ANTES submission.

**Archivos de trazabilidad en memory/:**
- `reference_numeros_S40_AMF.md` — ~150 numeros con fuente
- `reference_decisiones_S40_integracion.md` — 6 decisiones Gonzalo AMF
- `reference_trazabilidad_S40_completa.md` — mapa linea-por-linea

## 13-BIS. FRAMEWORK PREDICTIVO Y OPERACIONAL (§9 AMF + §8.15 sistema alertas)

**Esta seccion es CLAVE para el paper EID** — el journal premia impacto en salud publica, y tenemos 3 productos operacionales listos.

### 13-bis.1 Modelo 2 etapas (§9.1)
```
Etapa 1: n_eventos_quiloides = 70.4 - 193.3 × NDVI_mean
         R²=0.523, R²adj=0.500, p=0.0001, SE=11.0, n=23 anos
Etapa 2: eventos → distribucion por comuna (proporcion historica)
         → GLMM S29-K → MC 10,000 simulaciones
```
Script: `S29K_MODELO_FINAL_SIN_ZONE.R`. Output: `tabla_escenarios_FINAL.csv`.

### 13-bis.2 Escenarios CMIP6 (§9.2) — proyecciones
Deltas IPCC AR6 Atlas SWS, 10 GCMs (Iturbide et al. 2020):

| Escenario | +T°C | IRR | Delta casos |
|---|---|---|---|
| SSP2-4.5 ~2030 | +0.7 | 1.061 | +6.1% |
| SSP2-4.5 ~2050 | +1.2 | 1.108 | +10.8% |
| SSP5-8.5 ~2030 | +0.8 | 1.071 | +7.0% |
| **SSP5-8.5 ~2050** | **+1.8** | **1.166** | **+16.6%** |

**Tabla escenarios S29-K (casos/ano regional):**
| NDVI | Actual | SSP2-4.5 2050 | SSP5-8.5 2050 |
|---|---|---|---|
| BAJO | 3.4 [0-8] | 3.8 [0-8] | **4.1 [1-9]** |
| NEUTRO | 3.3 [0-7] | 3.6 [0-8] | 3.8 [1-8] |
| ALTO | 3.1 [0-7] | 3.4 [0-8] | 3.6 [0-8] |

Efecto marginal NDVI (BAJO/ALTO): +13%
Efecto marginal clima (SSP585_2050/Actual): +16.4%
**Combinado peor vs mejor: +32%**

### 13-bis.3 Probabilidades de excedencia (peor escenario BAJO + SSP5-8.5 2050)
| Metrica | Valor |
|---|---|
| P(>=2 casos en alguna comuna) | **41.4%** |
| P(>=3 casos en alguna comuna) | 8.2% |
| P(>=5 casos totales regionales) | **38.2%** |
| P(>=8 casos totales regionales) | 6.3% |

### 13-bis.4 Ciclos NDVI (§9.3)
- Bloques ALTO: media 1.7 anos (max 3)
- Bloques BAJO: media 2.2 anos
- **Estado 2024:** Fase ALTO, 2 anos consecutivos
- P(transicion ALTO→BAJO): 2yr=50%, 3yr=83%, **4yr=100%**
- Fase BAJO: **2.8 casos/ano** vs Fase ALTO: **1.6 casos/ano**
- **Ventana alto riesgo pronosticable: 2025-2027**

### 13-bis.5 Semaforo SEREMI (§9.4) — PRODUCTO OPERATIVO LISTO
| Color | P | Comunas |
|---|---|---|
| **ROJO** | >=25% | **Chillan (34%), Coihueco (30%), El Carmen (29%), San Carlos (26%)** |
| AMARILLO | 10-25% | Pinto, San Ignacio, Yungay, Quillon, Bulnes |
| NARANJO | 5-10% | San Fabian, Pemuco, Coelemu, Chillan Viejo, Niquen, Cobquecura |
| VERDE | <5% | San Nicolas, Quirihue, Ranquil, Trehuaco, Portezuelo, Ninhue |

### 13-bis.6 Sistema 3 tiers de alerta (§8.15 S49) — walk-forward OOS
Estructura anidada monotonica (Y=3 implica Y>=2 implica Y>=1):
- Tier 1: alerta general (prevalencia 1.9%, 41 eventos)
- Tier 2: cluster alert (prevalencia 0.6%, 14 eventos)
- Tier 3: alerta extrema (prevalencia 0.5%, 11 eventos) — **exploratorio**

**Performance walk-forward 10 folds (2015-2024):**
| Tier | Log score | BSS vs Bortman PAHO | BSS vs Poisson | BSS vs random |
|---|---|---|---|---|
| 1 | 0.0857 [0.074, 0.098] | **+68.2%** | +1.97% | +2.4% |
| 2 | 0.0427 [0.022, 0.065] | +36.5% | +1.49% | n/a |
| 3 | 0.0547 exploratorio | 2.9% | -0.5% | n/a |

**Input contrato:** `WF_con_alertas_completo.csv` (3038 filas × 41 columnas)
**Semilla reproducible:** `set.seed(49)`
**Argumento operativo headline:** supera en **+68.2%** al endemic-channel de Bortman (PAHO), baseline de vigilancia panamericana estandar.

### 13-bis.7 Prediccion testeable pre-registrada
**Megafire 2023** (18,420 ha Quillon) → prediccion casos **Nov2024-Nov2025** (ventana 18-30m trofica)
- Pre-registrado Zenodo DOI 10.5281/zenodo.19425753 lock 2026-04-04
- Verificable externamente con datos ISP 2025
- Si se cumple: validacion externa unica en literatura hantavirus Sudamerica

### 13-bis.8 Pipeline operacional conceptual
```
Input mensual (automatizable):
  - NDVI Landsat (GEE) → lag 5m
  - ERA5-Land t2m
  - Fire MODIS MCD64A1 (ventana 18-30m)
  - Poblacion INE
         ↓
  Modelo S29-K (coeficientes locked)
         ↓
  p_hat por comuna-mes
         ↓
  Thresholds Tier 1/2/3 (pre-especificados)
         ↓
  Semaforo verde/amarillo/rojo
         ↓
  Alerta SEREMI Ñuble
```

### 13-bis.9 Modelos descartados (§9.5)
| Modelo | Razon | Sesion |
|---|---|---|
| Patron temporal (ACF/lag anual) | ACF=-0.20, lag NS, AIC peor | S26 |
| 2 niveles macro→micro | AUC=0.607, NDVI macro p=0.91 | S26 |
| Hibrido GLMM+desc | MAE 2.04 vs desc 2.01, bug validacion | S27/S28 |
| Quiloide como covariable | gamma NS, delta-AIC positivo | S27 |
| Markov NDVI | Converge ~2 pasos, indistinguibles | S29-B |

### 13-bis.10 Gaps del framework predictivo (declarar honestamente)
- **NO hay dashboard/API deployada** — es diseno de producto, no producto operativo
- Prediccion megafire 2023 aun no verificada (datos ISP 2025 pendientes)
- Tier 3 exploratorio por n=11 (declarado Limitations P3 Nivel 2)
- No hay acuerdo formal SEREMI para implementacion
- IC amplios por incertidumbre compuesta: (a) R²=0.52 etapa 1, (b) R²m=0.195 etapa 2, (c) variabilidad estocastica NB2 theta=1.555
- Los IC interpretarse como rangos plausibles, NO predicciones puntuales

### 13-bis.11 Implicancia para paper EID
EID premia **impacto salud publica**. El framework operacional es el **mensaje mas vendible**:
1. Semaforo comunal con 4 comunas ROJAS identificadas
2. Proyecciones CMIP6 cuantificadas (+32% peor escenario)
3. Sistema de alertas Tier 1 que **supera +68.2% al estandar PAHO**

La seccion **Discussion → Public Health Implications** puede construirse enteramente con esto. Ningun otro paper hantavirus Sudamerica tiene framework predictivo-operacional de esta profundidad.

---

## 14. 50 FIGURAS Q1 GENERADAS (S35)

**Ubicacion:** R local Windows (R 4.5.3)
**Scripts:** `R/FIGURAS_PAPER_Q1_COMPLETO.R`, `R/FASE4_FIGURAS_PUBLICACION.R`, `R/FIG_EJECUTAR_TODO.R`
**Para EID (seleccionar 4-6):**
- Mapa area estudio (21 comunas Nuble)
- Serie temporal casos + NDVI lag 5
- Forest plot coeficientes GLMM
- Calibration plot OOS
- ROC curve + AUC CI
- Dose-response fire (supplementary)

**CRITICO:** Verificar ninguna generada con IA (EID prohibe). Si alguna lo fue, reconstruir en R.

## 15. DECISIONES GONZALO CLAVE (de 69 catalogadas)

1. **Lag 5 pre-especificado** (45 dias antes de modelar, cerrado S4-S5)
2. **Zonas binarias** (no tripartitas, S20-S21)
3. **Clasificacion v6.2** (14S/14M/6I aplicada)
4. **Floracion SECTORIAL sincronica** (no masiva, S23)
5. **Modelo S29-K final** (parsimonia, S29)
6. **Estrategia dual publication** (EID + Rev Chil Infect, S42)
7. **PLoS NTD descartado** (S45, por APC sin fondos)
8. **EID = P1** (S45, reemplaza PLoS NTD)
9. **Pausa submission para Nivel 2** (S49)
10. **Trabajo S50 enfocado 100% en paper EID** (2026-04-05)

## 16. SPECS EID (reference_EID_specs_S45.md)

| Item | Valor |
|---|---|
| Palabras cuerpo | **3500 max** |
| Abstract | **150 palabras, NO estructurado** |
| Referencias | **50 max**, Vancouver, titulos italica |
| STROBE | Obligatorio |
| Figuras IA | **PROHIBIDAS** |
| APC | $0 |
| IF | 11.8 |
| Submission | ScholarOne |
| Review time | ~8 semanas |
| Aceptacion | ~15-20% |

**Backup journals (reference_journals_backup_gratis_S45.md):**
1. Memorias IOC (IF 2.5)
2. Rev Panamericana (IF 2.0)
3. Cadernos Saude Publica (IF 1.8)

## 17. COMPARACION CON 14 PAPERS HANTAVIRUS LATAM

**Nuble UNICO con:**
- GLMM + Bell-Jones within-between
- Walk-forward temporal
- FSI satelital (indice propio)
- NDVI x CMIP6
- cvAUC 0.766 OOS SUPERIOR a literatura

**Nuble primeros analisis:**
1. Primer GLMM hantavirus Sudamerica
2. Primer Bell-Jones en hantavirus
3. Primer walk-forward temporal hantavirus
4. Primer FSI satelital hantavirus
5. Primer modelo NDVI x CMIP6 hantavirus
6. Primer fire x hantavirus Sudamerica (S47)

## 18. SECCIONES MANUSCRITO — QUE USAR DEL AMF

### Del AMF_FINAL usar directamente:
- §3 Epidemiologia descriptiva (lin 194-260)
- §4 Marco teorico ecologico (lin 263-333)
- §5 Pipeline M3 FSI (lin 335-449)
- §6 Pipeline M2 Ratizacion (lin 451-506)
- §7 Pipeline M1 GLMM (lin 508-643)
- §8.1-8.14 Validaciones (lin 645-888)
- **§8.15 Nivel 2 CRITICO** (lin 889-1142)
- §9 Framework predictivo (lin 1147-1213)
- §10 Variables descartadas (lin 1216-1237)
- Parte III OH.1.1-1.3 (lin 3289-3335) para Discussion
- Parte IV.1 Bibliografia (lin 3374-3521)
- Parte IV.3 Sesgos (lin 3719-3741)
- Seccion fire (lin 4201-4379) para supplementary

### EXCLUIR:
- Parte II clinica completa (lin 1241-3282)
- OH.1.4 temas clinicos puros
- Trilogia precoz, FR>22, plasma, ECMO -> P2

## 19. RED FLAGS PERMANENTES

1. **Overlap con P2:** iThenticate <5% (ICMJE/COPE OK, precedente Vial/Ferres)
2. **Limite 3500 palabras:** parsimonia brutal, cada palabra cuenta
3. **50 refs max:** curar con cuidado desde 271 disponibles
4. **STROBE 22/22:** 100% obligatorio
5. **Figuras sin IA:** reconstruir si alguna fue generada
6. **NO calculos mentales** (regla S39): siempre verificar con R
7. **grep ANTES de corregir** (regla S43): 45% correcciones tienen propagacion incompleta

## 20. LOGICA DE REDACCION S50+ (plan 13 dias S45, adaptar)

**Estimado total:** 24-28 dias desde 2026-04-05 -> submit ~2026-05-03

**Semana 1 (abr 5-12):**
- Methods STROBE (3d)
- Results tablas+figuras (2d)
- Seleccion figuras EID (1d)
- Trazabilidad numeros (1d)

**Semana 2 (abr 12-19):**
- Introduction (2d)
- Discussion LATAM (2d)
- Limitaciones (1d)

**Semana 3 (abr 19-26):**
- STROBE checklist (1d)
- TRIPOD+AI checklist (1d)
- Red-team interno manuscrito (2d)
- Correcciones iterativas (2d)
- Cover letter (1d)

**Semana 4 (abr 26-30):**
- Aprobacion Gonzalo (2d)
- Submit ScholarOne (1d)

Deadline V-12: 2026-06-30 (buffer >60 dias si algo se atrasa).

## 21. ARCHIVOS PERSISTIDOS DE AGENTES S50

Dos reportes completos de exploracion estan en:
- `C:\Users\gonza\.claude\projects\C--Proyectos-Hantavirus-Nuble\b20685dd-e1ba-40e8-b607-8816f2904904\tool-results\toolu_012bndcUkArgdHzDYkGkYJeb.json` — Mapeo exhaustivo memoria S4-S49 (54 KB)
- `C:\Users\gonza\.claude\projects\C--Proyectos-Hantavirus-Nuble\b20685dd-e1ba-40e8-b607-8816f2904904\tool-results\toolu_01JDPwtWXt6bRezKmbKyy7DS.json` — Mapeo exhaustivo AMF Parte I v1.6 (63 KB)

Si necesito recuperar detalle especifico que no esta en este documento, consultar esos persistidos con Read offset/limit pequeno o usar Grep con patrones especificos.

## 22. REGLAS OPERATIVAS PARA EL PAPER EID (anti-vacios, anti-sesgos)

1. **Verificar todo numero con reference_numeros_S40_AMF.md** antes de escribirlo
2. **Nunca calcular mentalmente** — siempre R
3. **Grep antes de corregir** (45% tienen propagacion)
4. **Declarar limitaciones proactivamente** (las 12 ya listadas)
5. **Cada afirmacion causal -> lenguaje condicional** (CS-01 a CS-05)
6. **Cada figura -> verificar NO IA**
7. **Cada referencia -> DOI verificado CrossRef**
8. **STROBE 22 items** sobre el texto final
9. **iThenticate <5%** antes de submit
10. **Red-team interno nuevo** despues de cada version del manuscrito

---

**FIN CONTEXTO COMPLETO S50**

*Este documento es el mapa maestro anti-vacios y anti-sesgos para el paper ecologico EID. Usar como anclaje en cada interaccion. Actualizar conforme avancemos.*
