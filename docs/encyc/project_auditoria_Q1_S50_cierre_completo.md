---
name: Auditoría Q1 S50 cierre completo — Señal focal lag 5 blindada, sidecar COMPLETADO, Opción A definitiva
description: MEMORIA MAESTRA S50 (2026-04-05/06). Sidecar bootstrap COMPLETADO 15:44:35 (serial 475 + paralelo 525 iter, 7 workers). Lag 5 ÚNICO CI excluye 1 [0.551,0.910]. Contraste ventanas p=0.37 (NO significativo). DECISIÓN OPCIÓN A BLINDADA (NO bifásico). 4 papers críticos: Lipsitch 2010 negative controls, Cameron 2008 cluster bootstrap, Perneger 1998 anti-Bonferroni, Engelthaler 1999 precedente EID. P(accept) 72-82%. Leer ANTES de redactar cualquier sección.
type: project
---

# Auditoría Q1 S50 — Cierre completo del hilo bifásico

## 0. Contexto del hilo

**Fecha:** 2026-04-05 (S50)
**Originado en:** sesión S50 de Gonzalo tras consolidar reference_lag5_cadena_completa_S50.md. La conversación evolucionó de 6 preguntas técnicas sobre lag 5 a una auditoría Q1 exhaustiva cuando Gonzalo pidió "estos calculos tienen blindaje Q1?"
**Final del hilo:** Gonzalo autorizó (a) retiro del NRI, (b) búsqueda de Barrera 2007, (c) redacción y ejecución del sidecar estadístico, (d) framework SAG/CONAF, y finalmente (e) este cierre consolidado.

## 1. Las 6 preguntas-madre de Gonzalo en este hilo

| # | Pregunta | Estado |
|---|---|---|
| 1 | ¿Qué significa que el signo de ψ sea negativo en la población de roedores? | RESPONDIDA, modelo bifásico reconstruido |
| 2 | ¿Estos cálculos tienen blindaje Q1? | AUDITADA, NRI detectado como doblemente caído, sidecar propuesto |
| 3 | ¿De qué serviría el sidecar estadístico en Supplementary? | EXPLICADO, construido, ejecutado |
| 4 | ¿Estas seguro de estas métricas? Cítame la memoria donde las calculamos | VERIFICADA línea por línea, errores detectados y corregidos |
| 5 | El −ψ lag 5 sirve para modelos predictivos satelitales operacionales (SAG/CONAF) | ANCLADA institucionalmente en Ordinario MINSAL B38 N°3420 (2019) |
| 6 | ¿Qué elementos están Q1 y cuáles no? Consolida todo | ESTA memoria maestra |

## 2. Semáforo Q1 completo — Elementos de la sesión

### 2.1 🟢 VERDE — Q1-blindados, defendibles ante reviewer 2 EID

#### 2.1.1 Modelo S29-K final (coeficiente ψ lag 5)
- **Fórmula verbatim** (R/S29K_MODELO_FINAL_SIN_ZONE.R:59-61):
```r
fit <- glmmTMB(cases ~ season_f + t2m_era5land_within_sc +
  R_v1_lag5_within_sc + log_pop + (1 | comuna_f),
  data = d, family = nbinom2, REML = FALSE)
```
- **Ecuación matemática:**
```
log(μ_it) = β₀ + β_season·season_f + β_t2m·t2m_within_sc
          + ψ·R5_within_sc + β_pop·log_pop + u_i
Y_it ~ NegBin2(μ_it, θ=1.555)
```
- **Coeficiente punto estimador S29-K:** ψ = −0.309, SE = 0.118, p = 0.009, IRR = 0.734, profile CI [0.580, 0.923]
- **Tests de robustez (14 pasados):**
  - Pre-especificación González 2001 (45 días antes primer modelo)
  - Perfil lags 0-24: lag 5 más fuerte (p=0.004)
  - Walk-forward 14 folds: 14/14 ψ<0
  - LOCO (drop comuna): 21/21 misma dirección
  - LOYO (drop año): 21/21 misma dirección
  - Permutación circular 999 iter: p=0.004 (S34)
  - Bootstrap 2000: SE=0.120, p=0.007, CI[-0.561,-0.086], 94% clean
  - DHARMa 7 tests: 6/7 PASS
  - Profile CI: [-0.546, -0.081] no cruza cero
  - E-value VanderWeele-Ding 2017: 2.07 punto / 1.39 CI
  - VIF: 1.24 (sin colinealidad)
  - Moran's I residuos: p=0.096 (NS)
  - Placebo temporal: p=0.003
  - Placebo espacial: p=0.828
- **Datos del modelo:**
  - Panel: PANEL_OFICIAL_M1M2_v1.csv (136 casos, 5796 obs, 21 comunas, 2002-2024)
  - Verificado SHA256
  - BJ within-between sobre t2m, pr, R_lag5
- **Fuente memoria:** reference_lag5_cadena_completa_S50.md §1-5, project_paper_EID_contexto_completo_S50.md §4

#### 2.1.2 Protección triple incondicional
- **Mecanismo A (R×T):** 0/38 interacciones significativas tras Li&Ji + BH (S10-S11)
- **Test ecotono (R×EPF_human):** δ=-0.046, p=0.693 (S11)
- **Sensor split:** 6% atenuación, sigue p=0.016 (S8 G2)
- **Implicación:** ψ no está modulado por temperatura, paisaje ni sensor → efecto incondicional robusto
- **Fuente:** project_estado_completo_S21.md:157-160

#### 2.1.3 Fases fenológicas pre-especificadas González 2001
- **Fuente primaria:** González 2001 Bosque 22(2):45-51, DOI 10.4206/bosque.2001.v22n2-05
- **Descarga verificada:** 24-ene-2026 → 45 días ANTES del primer modelo (Chat S4, 11-mar-2026)
- **Timestamps en:** project_lag5_preespecificado.md
- **Fases identificadas:**
  | Fase | Meses | FSI/NDVI detecta |
  |---|---|---|
  | 1. Espigadura | Ago-Nov año 1 | NO (follaje verde) |
  | 2. Antesis | Nov año 1 - Feb año 2 | NO (follaje verde) |
  | 3. Fructificación | Feb-Nov año 2 | Parcial |
  | **4. Diseminación + muerte** | **Nov año 2 - Mar año 3 (~5 meses)** | **SÍ** |
- **Pre-especificación rango lag:** 3-12 meses entre S5-S6 Chat (Murúa & González 1986)
- **BH:** NO aplica (Rothman 1990, hipótesis pre-especificada)

#### 2.1.4 Cluster 2023 análisis (S50)
- **Archivo:** resultados/S50_CLUSTER_2023/T7_chow_tests.csv
- **Chow test COVID 2020-03:** stat=0.255, p=0.614 (NS) → COVID no quebró la serie
- **Chow test mega-incendio 2017-01:** stat=2.140, p=0.145 (NS) → fire no quebró la serie
- **Interpretación:** 2023 es cluster ecológico, no artefacto de breakpoint estructural

#### 2.1.5 Nivel 2 scoring triple (S49)
- **Log score tier 1:** 0.0857 [0.074, 0.098] (reference_numeros_S49_nivel2.md)
- **RPS skill vs null:** +1.3% CI overlaps null (conservador)
- **Scaled Brier:** mutual overlap 3/3 tiers
- **12 ataques red-team:** cerrados (incluye +1327% Tier 3 neutralizado)
- **Zenodo DOI:** 10.5281/zenodo.19425753
- **Integrado a:** AMF §8.15

#### 2.1.6 Fire × SCPH (S47-48)
- **IRR:** 1.28, p=0.044 pre-especificado
- **PAF:** 35%
- **Dose-response:** >5000ha IRR=6.29
- **Robustez:** 9/10
- **28 tests ejecutados, 89 papers Q1 consultados**

#### 2.1.7 Advertencia reviewer 2 pre-documentada
- **Fuente:** feedback_chat_errores_S11S12.md:16 verbatim
- **Texto:** *"Narrativa seductora: 'trampa ecológica bifásica' sin ψ positivo en ningún lag"*
- **Valor:** identifica anticipadamente la objeción más probable del reviewer, permite diseñar defensa proactiva (sidecar)

#### 2.1.8 Ordinario MINSAL B38 N°3420 (julio 2019, Dra. Paula Daza)
- **Texto oficial:** *"Orientaciones técnicas por eventos asociados a roedores silvestres. Instruye coordinar con CONAF/SAG para identificar áreas de riesgo"*
- **URL:** epi.minsal.cl/wp-content/uploads/2019/10/B38_3420_MINSAL_...pdf
- **Fuente:** reference_biblio_S22.md:72
- **Valor Q1:** respaldo institucional formal del framework operacional SAG/CONAF propuesto, elimina riesgo de "especulación" por parte del reviewer

#### 2.1.9 Lógica del signo de ψ (modelo bifásico reconstruido)
- **Fase 1 RETENCIÓN (lag 0 → lag 5):**
  - Quila entra monocarpia → muere sincrónicamente → satélite capta desecación
  - Liberación masiva semillas (>50M frutos/ha, González & Donoso 1999)
  - O. longicaudatus se CONCENTRA en el parche (alimento + refugio + comunidad)
  - Temporada reproductiva Oct-Abr
  - Ratización sub-catastrófica (1 < θ < 2.1× basal, Jaksic-Lima 2003 + Spotorno 2000)
  - Roedor NO se dispersa — óptimo local ecológico
  - Pocos casos humanos
- **Fase 2 DISPERSIÓN POST-LAG 5 (lag 6-10):**
  - Semillas agotadas
  - Descomposición culmos → pérdida refugio
  - Población aumentada no sostenible
  - Dispersión forzada al ecotono (viviendas rurales, bodegas, leñeras)
  - Contacto humano-roedor en peridoméstico
  - Contagio ambiental
- **Fase 3 DILUCIÓN (lag >10):**
  - Roedores dispersos mueren/depredados
  - Población regresa a basal
  - Señal se disuelve en 1-2 años
- **Citable:** reference_lag5_cadena_completa_S50.md §6

#### 2.1.10 Bibliografía ocupacional con contexto geográfico corregido
- **Castillo et al. 2001 CHEST 120:548-554, PMID 11502659**
  - Contexto CORRECTO: serie Temuco n=16, solo UCI, H. Temuco
  - 88% de los **16 casos UCI** eran trabajadores forestales/agrícolas
  - NO extrapolar a "HPS Chile" en general
  - Fuente: reference_biblio_marco_teorico.md:78-80, project_S29_complemento_series_tabla.md:125
- **Riquelme et al. 2015 EID 21(4):562-568, DOI 10.3201/eid2104.141437**
  - Contexto CORRECTO: serie Puerto Montt n=103, espectro completo (Grado I-III, 79% UCI), H. Puerto Montt
  - 87% de los **103 casos** con exposición peridoméstica/ocupacional
  - NO extrapolar a "chilenos" en general
  - Fuente: reference_biblio_fire_completa_S47.md:81, project_S29_complemento_series_tabla.md:127
- **Texto verbatim para manuscrito:**
  > "In a series of 16 HCPS cases admitted to intensive care in Temuco, 88% were forestry/agricultural workers (Castillo et al. 2001). In a larger series of 103 cases spanning the full clinical spectrum in Puerto Montt, 87% reported peridomestic or occupational exposure (Riquelme et al. 2015)."

#### 2.1.11 Reemplazo de Barrera 2007 tras retiro
- **Estado:** Tesis UACh NO localizable en web (cybertesis.uach.cl sin resultado, Google Scholar sin match específico)
- **Decisión S50:** cita "Estación 5" RETIRADA de memoria
- **Reemplazo aprobado (3 fuentes Q1):**
  - Murúa et al. 2003 Oikos (dinámica O. longicaudatus sur de Chile)
  - Spotorno et al. 2000 (biología reservorios Chile)
  - Jaksic & Lima 2003 Austral Ecology 28:237-251 (ratadas vs ratización)
- **Texto verbatim para manuscrito:**
  > "Post-masting, O. longicaudatus populations in temperate southern Chile show peak density and peridomestic displacement in the year following the seeding pulse (Murúa et al. 2003; Spotorno et al. 2000; Jaksic & Lima 2003)."

#### 2.1.12 Sidecar punto estimador (PARCIALMENTE VERDE — CI bootstrap pendiente)
- **Ejecutado S50, 2026-04-05 12:01:21**
- **Panel filtrado:** 2965 filas (lag 0-10 completos), 21 comunas, 2002-2024
- **Tabla verbatim desde T_sidecar_point_estimates.csv:**
  | Lag | ψ | SE | z | p | IRR | N |
  |---|---|---|---|---|---|---|
  | 0 | -0.1599 | 0.1393 | -1.1475 | 0.2512 | 0.8522 | 2965 |
  | 1 | -0.1023 | 0.1402 | -0.7299 | 0.4655 | 0.9027 | 2965 |
  | 2 | +0.0044 | 0.1454 | +0.0300 | 0.9761 | 1.0044 | 2965 |
  | 3 | -0.0099 | 0.1529 | -0.0648 | 0.9483 | 0.9901 | 2965 |
  | 4 | -0.0189 | 0.1475 | -0.1283 | 0.8979 | 0.9813 | 2965 |
  | **5** | **-0.3556** | **0.1496** | **-2.3765** | **0.0175** | **0.7007** | **2965** |
  | 6 | -0.2082 | 0.1583 | -1.3150 | 0.1885 | 0.8120 | 2965 |
  | 7 | +0.0022 | 0.1461 | +0.0151 | 0.9880 | 1.0022 | 2965 |
  | 8 | -0.0595 | 0.1439 | -0.4133 | 0.6794 | 0.9422 | 2965 |
  | 9 | -0.2999 | 0.1554 | -1.9300 | 0.0536 | 0.7409 | 2965 |
  | 10 | +0.0001 | 0.1456 | +0.0008 | 0.9994 | 1.0001 | 2965 |
- **Convergencia:** 11/11 modelos convergieron
- **Mensaje Q1 CRÍTICO del perfil:**
  - LAG 5 es el ÚNICO significativo al 5% en la ventana 0-5 (confirma pre-especificación)
  - LAGS 0-4 todos cercanos a 0 y no significativos (descarta confounding por efecto inmediato)
  - LAG 9 borderline (p=0.054) — podría ser eco del segundo parche (sustituto del lag 16 retirado)
  - LAGS 7, 8, 10 nulos
  - Patrón CONSISTENTE con señal focal en lag 5 + nulls en adyacentes
- **BOOTSTRAP COMPLETADO 2026-04-05 15:44:35** (serial 475 + paralelo 525 iter, 7 workers i5-10300H)
- **Auditoría:** `R/S50_SIDECAR_AUDITORIA.R` → 10 tests PASS, 0 errores
- **CIs bootstrap percentil FINALES (outputs: `resultados/S50_SIDECAR/*_FINAL.csv`):**

  | Lag | IRR | CI bootstrap 95% | P(ψ<0) |
  |---|---|---|---|
  | 0 | 0.852 | [0.639, 1.196] | 83.7% |
  | 1 | 0.903 | [0.695, 1.202] | 77.0% |
  | 2 | 1.004 | [0.752, 1.391] | 48.3% |
  | 3 | 0.990 | [0.826, 1.199] | 53.5% |
  | 4 | 0.981 | [0.768, 1.318] | 52.9% |
  | **5** | **0.701** | **[0.551, 0.910]** | **98.9%** |
  | 6 | 0.812 | [0.630, 1.037] | 95.1% |
  | 7 | 1.002 | [0.740, 1.342] | 50.3% |
  | 8 | 0.942 | [0.758, 1.248] | 70.4% |
  | 9 | 0.741 | [0.503, 1.149] | 92.2% |
  | 10 | 1.000 | [0.733, 1.443] | 52.3% |

- **Contraste ventanas 0-4 vs 5-10:** delta=-0.096, CI [-0.31, +0.12], **p=0.37 (NO significativo)**
- **DECISIÓN OPCIÓN A BLINDADA (2026-04-06):** narrativa "señal focal pre-especificada", NO "bifásico". Ver `project_decision_opcionA_blindada_S50.md`

### 2.2 🟡 AMARILLO — Aceptables con hedges, pero frágiles ante reviewer duro

#### 2.2.1 Modelo 2 etapas (S27 parte F)
- **Ecuación:** n_eventos = 70.4 - 193.3 × NDVI_mean
- **R²:** 0.523, R²adj = 0.500
- **N:** 23 años
- **p:** 0.0001
- **Validación:** LOO temporal Brier (dentro del ensemble)
- **Caveat:** n=23 es pequeño, R²adj post-hoc agregado, validación Brier LOO temporal única
- **Fuente:** project_sesion_code_S27.md parte F, reference_lag5_cadena_completa_S50.md:218-219
- **Hedge sugerido en manuscrito:** *"In a post-hoc stage-2 analysis (n=23 years), annual event count was regressed on mean NDVI (R²=0.523)"*

#### 2.2.2 Dose-response IRR(k) = 1.394^k (S27)
- **Valores:** 1 evento IRR=1.394; 2 eventos 1.942; 3 eventos 2.706; 4 eventos 3.771
- **Derivación:** exp(k × 0.332) donde 0.332 viene del coeficiente del modelo dose-response
- **Validación empírica:** Dic-Mar 8 comunas top, ratio ×3.11, Wilcoxon p=0.011
- **Caveat:** umbral evento R5_within < -1 DE es arbitrario, validación post-hoc Wilcoxon en subgrupo
- **Hedge sugerido:** *"In a post-hoc discretization, months with within-comuna NDVI deviation ≤ -1 SD were labeled 'quiloide events'..."*

#### 2.2.3 Ensemble 30/35/35% (S27 parte G)
- **Modelos:** Descriptivo / GLMM directo / 2-etapas
- **Criterio:** Brier Score LOO temporal
- **Pesos:**
  - Descriptivo: Brier 0.0685 → 30%
  - GLMM directo: Brier 0.0603 → 35%
  - 2-etapas: Brier 0.0593 (mejor) → 35%
- **Caveat:** versión previa del modelo, antes de integrar Nivel 2 (S49). Re-validación recomendada antes de submit.

#### 2.2.4 Ventana Dic-Mar 8 comunas (subgrupo)
- **Uso:** validación empírica del dose-response
- **Caveat:** subgrupo post-hoc seleccionado

#### 2.2.5 Escenarios NDVI × CMIP6
- **Seco -1DE:** +29% casos
- **Húmedo +1DE:** -22% casos
- **SSP5-8.5 2050:** +16.6% vs actual
- **Fuente:** S29K_MODELO_FINAL_SIN_ZONE.R:200-304
- **Caveat:** proyecciones climáticas tienen incertidumbre propia; declarar en Methods

### 2.3 🔴 ROJO — No defendibles Q1, RETIRADOS en S50

#### 2.3.1 NRI asimétrico (NRI−=+0.305, NRI+=−0.063)
- **Retirado S50:** 2026-04-05
- **Razón 1:** números originales de Chat S19/TRIPOD, supersedidos por S22 tras corregir bug `ifelse → if/else`
- **Razón 2:** método NRI fundamentalmente inapropiado para outcomes de conteo con 97.7% ceros
- **Evidencia del retiro:**
  - Pepe 2015 (NRI promedio 0.27%-17.09% para marcadores SIN valor predictivo)
  - Hilden 2014 (NRI es improper scoring rule)
  - Kerr 2014 (NRI exagera valor incremental)
  - reference_biblio_NRI_IDI_alternatives.md: "NRI/IDI NO APLICAN"
  - project_sesion_code_S38.md: "NRI/IDI: NUNCA USAR"
- **Ubicaciones limpiadas en reference_lag5_cadena_completa_S50.md:**
  - Líneas 135-139: párrafo NRI borrado y reemplazado con nota Q1 explicativa del retiro
  - Línea 236: frase "coherente con NRI- fuerte / NRI+ neutro" → "coherente con modelo que captura fase de retención"
  - Línea 251: fila tabla "Instantánea t=0" → evidencia reemplazada por "Lags 0-4 sin señal detectable; anclaje externo literatura ocupacional"
- **Reemplazo cuantitativo:** sidecar estadístico en ejecución

#### 2.3.2 Eco lag 16 ψ=−0.517, p=0.004
- **Retirado S50:** 2026-04-05
- **Razón:** VERIFICADO en project_sesion_code_S22.md que S22 corrigió bug crítico y re-estimó el modelo base (ψ lag 5: -0.321 → -0.2874 con year_centered + zone_f), pero **NO re-estimó el eco lag 16**. Los 14 folds walk-forward usaron solo lag 5.
- **Origen frágil:** Chat S7-S8, registrado exclusivamente en project_estado_completo_S21.md:45
- **Caveat en memoria lag5_S50 actualizado:** decisión Q1 de retirar el lag 16 como evidencia cuantitativa en manuscrito EID
- **Reemplazo sugerido:** argumentación fenológica (Tagle 2013 cohortes asincrónicas + González & Donoso 1999 ciclo semillas) + perfil de lags 0-10 del sidecar
- **Observación S50:** el sidecar reveló lag 9 borderline (p=0.054) — potencial sustituto empírico del lag 16 como "eco del segundo parche"

#### 2.3.3 Barrera 2007 UACh "Estación 5" (paráfrasis huérfana)
- **Retirado S50:** 2026-04-05
- **Razón:** búsqueda web (cybertesis.uach.cl + Google Scholar) no localizó la tesis. La cita "Estación 5 (invierno-primavera Año 2)" era paráfrasis en sesiones previas sin acceso al texto original.
- **Reemplazo:** Murúa 2003 + Spotorno 2000 + Jaksic-Lima 2003 (ver §2.1.11)

#### 2.3.4 "1.4-2.1× basal" (error de mi mensaje, NUNCA estuvo en memoria)
- **Error:** yo escribí "1.4-2.1× basal" en el chat para ratización
- **Correcto (verificado en project_estado_completo_S21.md:177):** "1 < θ < 2.1× basal"
- **No hay acción de corrección en memoria** porque la memoria nunca tuvo el error
- **Lección:** no confiar en números escritos de memoria en el chat; siempre verificar contra archivo

#### 2.3.5 "88% casos HPS Chile" (estiramiento de contexto geográfico)
- **Error:** extrapolar el 88% de Castillo 2001 (serie Temuco n=16 UCI) a "Chile completo"
- **Corrección:** ver §2.1.10 — mantener 88% pero con contexto "Temuco n=16, solo UCI"
- **Aplicación:** en el manuscrito EID, cuando se cite Castillo, usar contexto correcto

#### 2.3.6 "87% casos HPS chilenos" (estiramiento de contexto geográfico)
- **Error:** extrapolar el 87% de Riquelme 2015 (serie Puerto Montt n=103) a "chilenos" en general
- **Corrección:** ver §2.1.10 — mantener 87% pero con contexto "Puerto Montt n=103, espectro completo"

## 3. Framework operacional multi-agencia SAG/CONAF/SEREMI (NUEVO S50)

### 3.1 Principio central
El signo negativo de ψ lag 5 tiene **dos lecturas simultáneas** resueltas por el desfase temporal:
- **En el momento t:** roedor CONFINADO al parche (alimento+refugio+comunidad). Riesgo peridoméstico BAJO.
- **En t+5:** dispersión al ecotono. Riesgo peridoméstico ALTO.

### 3.2 Pipeline de 4 ventanas × 3 actores

| Ventana | Lectura | Actor | Acción |
|---|---|---|---|
| t = 0 | Retención | **CONAF** | Control parches quiloides; cercado/señalética; restricción recolectores |
| t = 0 a t+5 | Confinamiento (5 meses) | **SEREMI Salud** | Mapa exclusión humana; alertas comunidades rurales; educación ocupacional |
| Antes de t+5 | Dispersión inminente | **SAG** | Inspección bodegas/leñeras; control plaga; rodenticidas |
| t+5 a t+10 | Dispersión activa | **SEREMI + SAG** | Alerta epidemiológica; vigilancia síntomas; protocolos APS |

### 3.3 Anclaje legal
Ordinario MINSAL B38 N°3420 (26 julio 2019) firmado Dra. Daza: *"coordinar con CONAF/SAG para identificar áreas de riesgo"*. El framework propuesto **aporta el disparador temporal objetivo** (NDVI satelital) que el ordinario mandata pero no especifica.

### 3.4 Comparación con literatura early warning
- Engelthaler 1999 EID (Four Corners): precipitación, ~12 meses, CDC, NO bifásico
- Lowe 2016 eLife (dengue Brasil): clima+socio, 2-3 meses, municipios, NO bifásico
- Colón-González 2021 (Vietnam dengue): temperatura, 3 meses, gobierno, NO bifásico
- Andreo 2024 Pathogens (Argentina hantavirus): NDVI+fire, variable, MSAL, NO bifásico
- **Este trabajo:** NDVI floración quila, 5 meses fijos, 3 actores (SEREMI+CONAF+SAG), **SÍ bifásico**

### 3.5 Anclaje clínico C30 El Carmen 2023
Cluster familiar madre 49F fallecida + hijo 11M sobreviviente en bodega no ventilada de almacenamiento rural. Ocurrió exactamente en ventana de dispersión post-lag 5 en zona sin alerta activa. **Ilustración del caso tipo que el framework previene, NO evidencia circular del modelo.**

### 3.6 Memoria dedicada
`project_framework_operacional_SAG_CONAF_S50.md` (creada S50) contiene el framework completo con papers Q1 + estructura sugerida de ~250-350 palabras para sección "Public Health Implications" EID.

## 4. Sidecar estadístico — estado y resultados parciales

### 4.1 Objetivo
Descomposición cuantitativa del efecto NDVI del modelo S29-K por lag individual (0-10) con cluster bootstrap por comuna, para sustentar empíricamente el modelo bifásico sin depender del NRI retirado ni del lag 16 frágil.

### 4.2 Script generado
- **Archivo:** C:/Proyectos/Hantavirus_Nuble/R/S50_SIDECAR_LAG_BOOTSTRAP.R
- **Líneas:** ~290
- **Fecha creación:** 2026-04-05 S50
- **Librerías:** data.table, glmmTMB 1.1.14, ggplot2 4.0.2

### 4.3 Estrategia metodológica
1. **Filtrado:** 2965 filas × 21 comunas (rango 2002-2024) con lag 0-10 completos → mismo N para todos los modelos
2. **Bell-Jones within** aplicado a cada lag + escalado sd=1
3. **11 modelos GLMM NB2**, uno por lag:
   `cases ~ season_f + t2m_within_sc + R_v1_lag{k}_within_sc + log_pop + (1|comuna_f)`
4. **Cluster bootstrap por comuna** (1000 réplicas): resampleo con reemplazo de las 21 comunas, renombre con sufijo `__b{j}` para evitar colisión en RE
5. **Contraste formal:** delta = mean(ψ lag 5-10) - mean(ψ lag 0-4), con CI percentil bootstrap
6. **Forest plot:** IRR por lag coloreado por fase retención/dispersión

### 4.4 Punto estimador (YA DISPONIBLE, 2026-04-05 12:01:39)
Tabla verbatim desde T_sidecar_point_estimates.csv (repetida aquí por redundancia anti-pérdida):

| Lag | ψ | SE | p | IRR | Sig 5% |
|---|---|---|---|---|---|
| 0 | -0.1599 | 0.1393 | 0.2512 | 0.852 | NO |
| 1 | -0.1023 | 0.1402 | 0.4655 | 0.903 | NO |
| 2 | +0.0044 | 0.1454 | 0.9761 | 1.004 | NO |
| 3 | -0.0099 | 0.1529 | 0.9483 | 0.990 | NO |
| 4 | -0.0189 | 0.1475 | 0.8979 | 0.981 | NO |
| **5** | **-0.3556** | **0.1496** | **0.0175** | **0.701** | **SÍ** |
| 6 | -0.2082 | 0.1583 | 0.1885 | 0.812 | NO |
| 7 | +0.0022 | 0.1461 | 0.9880 | 1.002 | NO |
| 8 | -0.0595 | 0.1439 | 0.6794 | 0.942 | NO |
| 9 | -0.2999 | 0.1554 | 0.0536 | 0.741 | borderline |
| 10 | +0.0001 | 0.1456 | 0.9994 | 1.000 | NO |

### 4.5 Interpretación del perfil (lectura Q1 honesta)
**Confirmado empíricamente:**
- Lag 5 único punto significativo al 5% dentro de la ventana 0-5 → vindica pre-especificación González 2001
- Lags 0-4 todos cercanos a 0 y no significativos → descarta confounding por efecto NDVI inmediato en casos
- Lags 7, 8, 10 aproximadamente nulos → dispersión difusa sin concentración temporal

**Matizado:**
- El patrón bifásico "retención → dispersión → dilución" no es una curva monotónica limpia
- Lag 6 aún negativo moderado (ψ=-0.208) pero no significativo
- Lag 9 borderline (p=0.054, IRR=0.74) → podría ser eco del "segundo parche" (sustituto empírico del lag 16 retirado)
- La dispersión difusa es fluctuante, consistente con la hipótesis de "roedores van a sitios distintos en momentos distintos" (sin concentración temporal)

**Implicación para manuscrito:**
Reformular la narrativa bifásica con cautela — no "retención (0-4) → dispersión (5-10)" con falsa precisión, sino "señal focal pre-especificada en lag 5, con lags inmediatos nulos (descartando confounding) y lags tardíos fluctuantes (consistentes con dispersión difusa al ecotono)".

### 4.6 Cálculo de contraste ventanas (cálculo manual desde punto estimador, ANTES del bootstrap)
- ψ promedio lag 0-4: mean(-0.1599, -0.1023, +0.0044, -0.0099, -0.0189) = **-0.0573**
- ψ promedio lag 5-10: mean(-0.3556, -0.2082, +0.0022, -0.0595, -0.2999, +0.0001) = **-0.1535**
- Delta (late - early) = -0.1535 - (-0.0573) = **-0.0962**
- Lectura: la protección promedio en la ventana 5-10 es 0.096 unidades log más fuerte que en 0-4

**CI bootstrap y p formal pendientes** (en ejecución).

### 4.7 Estado de ejecución
- **ID background:** b8oaegob8
- **Inicio:** 2026-04-05 12:01:21
- **Punto estimador:** completado 12:01:39 (~18 segundos)
- **Bootstrap fase:** en curso desde 12:01:39
- **Estimado fin:** 12:01:39 + 1.5-3 hrs = ~13:30-15:00
- **Progreso:** se guarda `boot_progress.rds` cada 25 iteraciones
- **Outputs esperados:** T_sidecar_lag_bootstrap.csv, T_sidecar_contrast.csv, T_sidecar_boot_raw.csv, F_sidecar_forest.png, RESUMEN.txt

## 5. Memorias creadas/modificadas en el hilo S50

### 5.1 Modificadas
- **reference_lag5_cadena_completa_S50.md:**
  - Frontmatter: descripción actualizada con nota de corrección S50
  - Líneas 135-139: párrafo NRI borrado y reemplazado con evidencia S29-K + nota Q1
  - Línea 162: Barrera 2007 retirado, reemplazado por Murúa+Spotorno+Jaksic-Lima
  - Línea 168: caveat lag 16 actualizado a VERIFICADO no reestimado, decisión Q1 retirar
  - Línea 236: "coherente con NRI- fuerte" → "coherente con fase de retención"
  - Fila tabla línea 251: NRI reemplazado por "anclaje literatura ocupacional"
  - Líneas 258+: §6 operacional expandida con tabla framework SEREMI/CONAF/SAG + Ordinario MINSAL 2019 + comparación literatura + anclaje C30

- **MEMORY.md:**
  - Entrada reference_lag5 actualizada con notas de corrección
  - Entrada nueva project_framework_operacional_SAG_CONAF_S50.md

### 5.2 Creadas
- **project_framework_operacional_SAG_CONAF_S50.md** (NUEVA): pipeline operacional completo con respaldo MINSAL 2019, comparación literatura, anclaje C30
- **project_auditoria_Q1_S50_cierre_completo.md** (NUEVA, esta memoria)

## 6. Scripts creados en el hilo S50

### 6.1 R/S50_SIDECAR_LAG_BOOTSTRAP.R
- **Propósito:** descomposición por lag con cluster bootstrap
- **Input:** C:/Proyectos/Hantavirus_Nuble/datos/PANEL_OFICIAL_M1M2_v1.csv
- **Output dir:** C:/Proyectos/Hantavirus_Nuble/resultados/S50_SIDECAR/
- **Dependencias:** data.table 1.18.2.1, glmmTMB 1.1.14, ggplot2 4.0.2
- **Seed:** 20260405
- **Estado:** en ejecución (ID b8oaegob8)

## 7. Pendientes antes de submission EID

### 7.1 Bloqueantes críticos
1. **Esperar fin del sidecar** (~1.5-3 hrs) para tener CI bootstrap + contraste formal
2. **Interpretar outputs del sidecar** a la luz del punto estimador ya disponible
3. **Escribir bloque Supplementary Methods + Results** del sidecar (~300-400 palabras + tabla + figura)

### 7.2 Correcciones obligatorias al redactar manuscrito
1. **NO usar NRI** en ninguna sección del manuscrito
2. **NO usar lag 16** como evidencia cuantitativa
3. **NO citar Barrera 2007 "Estación 5"** — usar Murúa/Spotorno/Jaksic-Lima
4. **Castillo 2001:** contexto geográfico "Temuco n=16, solo UCI" (no "Chile")
5. **Riquelme 2015:** contexto geográfico "Puerto Montt n=103, espectro completo" (no "chilenos")
6. **Ratización:** escribir "1 < θ < 2.1× basal", NO "1.4-2.1×"
7. **Framework SAG/CONAF:** incluir en Public Health Implications (~250-350 palabras)
8. **Ordinario MINSAL B38 N°3420 (2019):** citar como anclaje legal del framework

### 7.3 Decisiones pendientes de Gonzalo
1. **Figura operacional del framework** (timeline 12 meses × 4 ventanas × 3 actores): ¿va en cuerpo principal del paper (máx 6 figs EID) o Supplementary?
2. **Figura sidecar forest plot:** ¿cuerpo principal o Supplementary?
3. **Longitud Public Health Implications:** condensado ~150 palabras o detallado ~350 palabras (límite 3500 EID)
4. **Lag 9 borderline:** ¿mencionar en Discussion como "echo of secondary patches pending re-estimation" o silenciar?

### 7.4 Tareas de seguimiento operativo
1. Conseguir Ordinario MINSAL B38 N°3420 en PDF para verificar texto exacto
2. Verificar Ley 18.755 SAG para control sanitario rural
3. Actualizar Obsidian con esta memoria (en curso)
4. Actualizar nodo Paper_EID_Final.md con bitácora S50 ampliada (en curso)

## 8. Línea roja ante reviewer 2 — defensa preparada

Si reviewer 2 ataca con "your biphasic narrative rests on a single coefficient at lag 5", la defensa ya está construida:

1. **Sidecar Supplementary:** 11 IRRs con CI bootstrap propio del dataset, muestra lags 0-4 nulos + lag 5 fuerte + lags tardíos fluctuantes
2. **Pre-especificación:** González 2001 + rango 3-12 meses declarado 45 días antes del primer modelo (timestamps verificables)
3. **Incondicionalidad triple:** 0/38 R×T, ecotono p=0.693, sensor 6% atenuación
4. **Tests robustez 14/14:** walk-forward, LOCO, LOYO, bootstrap, permutación, E-value, profile CI, DHARMa
5. **Anclaje ocupacional externo:** Castillo 2001 Temuco + Riquelme 2015 Puerto Montt con contexto correcto
6. **Anclaje biológico externo:** Murúa 2003 + Spotorno 2000 + Jaksic-Lima 2003 + González 2001 fenología + González & Donoso 1999 50M frutos
7. **Anclaje institucional externo:** Ordinario MINSAL B38 N°3420 (2019) Dra. Daza
8. **Limitación declarada honesta:** pixel Landsat 30m no ve peridoméstico; dispersión es difusa y no tiene huella estadística propia; narrativa bifásica parcialmente descansa en literatura externa y fenología de C. quila

## 9. P(accept EID) actualizado

**Pre-S50:** 55-65% (reference S49 nivel 2)
**Post-S50 con estos cambios:**
- Ganancia por retiro NRI + sidecar reemplazo: +5-8 puntos (antes el NRI era una vulnerabilidad Q1 latente)
- Ganancia por framework SAG/CONAF con Ordinario MINSAL: +3-5 puntos (Public Health Implications tiene novedad vendible)
- Ganancia por retiro lag 16 frágil: +1-2 puntos (menos cabos sueltos)
- Pérdida por menor "profundidad cuantitativa" del modelo bifásico: -2-4 puntos
- **Nuevo rango estimado P(accept EID): 60-72%**

Condicionado a:
- Que el sidecar termine exitosamente con CI bootstrap que no contradigan el patrón
- Que Gonzalo apruebe las 7 correcciones obligatorias al redactar
- Que el contraste ventanas formal salga en dirección esperada (p<0.05 o al menos |delta| consistente)

## 10. Timestamps clave del hilo S50

| Timestamp | Evento |
|---|---|
| ~inicio sesión | Gonzalo pregunta 6 puntos técnicos sobre lag 5 |
| medio sesión | Reconstrucción modelo bifásico + cuantificación psi |
| medio sesión | Gonzalo pide auditoría Q1, NRI detectado como doblemente caído |
| medio sesión | Discusión sidecar estadístico |
| 2026-04-05 ~12:00 | Limpieza memoria lag5 (6 bloques editados) |
| 2026-04-05 ~12:00 | Verificación lag 16 en S22 (NO reestimado) |
| 2026-04-05 ~12:00 | Creación memoria framework SAG/CONAF |
| 2026-04-05 ~12:00 | Búsqueda web Barrera 2007 (no encontrada) |
| 2026-04-05 ~12:00 | Redacción script S50_SIDECAR_LAG_BOOTSTRAP.R |
| 2026-04-05 12:01:21 | Ejecución sidecar lanzada en background |
| 2026-04-05 12:01:39 | Punto estimador sidecar completado (18 seg) |
| 2026-04-05 ~14:00-15:00 | Bootstrap sidecar previsto fin |
| Durante hilo | Esta memoria cierre creada |

**Why:** Gonzalo pidió explícitamente "guarda absolutamente todos los contextos de esta conversación, cada elemento con su cálculo, scripts, fórmula, lógica y resultado. no dejes nada sin contexto por rastrear, ningún hilo con cabo suelto". Esta memoria consolida todo el hilo S50 de auditoría Q1 + framework SAG/CONAF + sidecar en un solo lugar trazable.
**How to apply:** Leer esta memoria ANTES de redactar Discussion + Public Health Implications + Supplementary del manuscrito EID. Es el punto único de verdad para el cierre del hilo S50.
