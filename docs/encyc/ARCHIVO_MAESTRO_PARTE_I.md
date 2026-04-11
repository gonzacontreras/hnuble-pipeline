# ARCHIVO MAESTRO -- PARTE I: COMPONENTE ECO-EPIDEMIOLOGICO
# SCPH (Virus Andes) en Region de Nuble, Chile

**Version:** 1.6
**Fecha de creacion:** 2026-03-26
**Fecha de revision:** 2026-03-29
**Estado:** v1.6 -- S38 anti-sesgo Q1 COMPLETO. 5 acciones menores resueltas: (1) Nota A2 residual eliminada (P-07 CERRADO); (2) Baseline AUC-PR explicitado (prevalencia OOS 61/2840=2.15%); (3) Letalidad 27.9% vs 14.7% reconciliada cross-parte; (4) Tabla escenarios CMIP6 con IC P5-P95 de 10k MC; (5) Nota DAG adjustment set teorico vs implementado + confundentes evaluados. Previo: v1.5 -- S37 COMPLETO. 11 acciones ejecutadas: (1) cvAUC=0.766 primario (LeDell 2015); (2) Limitaciones regionales expandidas; (3) P-02 S34→S36; (4) Permutacion canonica p=0.004; (5) SE=0.118 Wald; (6) Nota DAG dagitty (proxy vs causa, mediador vs confundente); (7) P-03 CERRADO (21/21 comunas ERA5-Land completo); (8) P-07 CERRADO (ratio 3-5x verificado); (9) P-04 checklist deposito preparado; (10) P-08 mapeo STROBE/TRIPOD preliminar (6 gaps alta prioridad); (11) P-05 DOIs parcial (fase manuscrito). 7 papers nuevos. 5/9 pendientes CERRADOS.
**Compilador:** Claude Code (master-builder), Sesion S33. Correcciones: S34, S36
**Fuentes primarias:** CONTEXTO_PROYECTO.md, CONTEXTO_M3_CONSTRUCCION_COMPLETA.md, memory_mcp.json, 35+ CSVs verificados, 253 papers compilados (S32)

---

## INDICE NAVEGABLE

- [1. Metadatos del proyecto](#1-metadatos-del-proyecto)
- [2. Fuentes de datos y muestreo](#2-fuentes-de-datos-y-muestreo)
- [3. Epidemiologia descriptiva](#3-epidemiologia-descriptiva)
- [4. Ecologia y marco teorico](#4-ecologia-y-marco-teorico)
- [5. Pipeline M3 -- Forest Stress Index](#5-pipeline-m3--forest-stress-index)
- [6. Pipeline M2 -- Ratizacion](#6-pipeline-m2--ratizacion)
- [7. Pipeline M1 -- GLMM Epidemiologico](#7-pipeline-m1--glmm-epidemiologico)
- [8. Validaciones y robustez](#8-validaciones-y-robustez)
- [9. Framework predictivo y escenarios](#9-framework-predictivo-y-escenarios)
- [10. Variables evaluadas y descartadas](#10-variables-evaluadas-y-descartadas)
- [11. Bibliografia organizada por tema](#11-bibliografia-organizada-por-tema)
- [12. Vacios, pendientes y contradicciones](#12-vacios-pendientes-y-contradicciones)
- [RESUMEN FINAL](#resumen-final)

---

## 1. Metadatos del proyecto

### 1.1 Investigador principal

- **Gonzalo**: Medico cirujano, Hospital Clinico Herminda Martin (HCHM), Chillan, Nuble, Chile
- **Aprobacion etica:** Comite Etico Cientifico (CEC) HCHM, N° CEC-HCHM 202501-25, ORD N°05. Aprobado 04-mar-2025, vigencia 1 ano. Presidente: Dr. Carlos Escudero Orozco. Excepcion de Consentimiento Informado otorgada. Protocolo 2a version. [ALERTA: vigencia vencio 04-mar-2026 — renovar antes de submission]

### 1.2 Alcance

- **Tipo de estudio:** Estudio ecologico de series de tiempo con datos agregados a nivel comuna-mes, modelado como GLMM. Analisis exploratorio estructurado (Hernan 2018).
- **Region:** Nuble, Chile (16 comunas Region de Nuble + 5 comunas que integraban la antigua Provincia de Nuble). 21 comunas totales.
- **Periodo:** 2002-2024 (23 anos, 276 meses por comuna)
- **Enfermedad:** Sindrome Cardiopulmonar por Hantavirus (SCPH), virus Andes (ANDV), linaje Sur
- **Vector:** *Oligoryzomys longicaudatus* (raton de cola larga)
- **Framework:** One Health (ecologia + epidemiologia + clinica + gestion sanitaria)
- **Journals objetivo:** PLoS Neglected Tropical Diseases, Int J Health Geographics, EcoHealth
- **Deadline:** Publicacion Q1, 2026

### 1.3 Hipotesis central

La **floracion SECTORIAL** (no sinconica masiva) de *Chusquea quila* se asociaria con un aumento subliminal de *O. longicaudatus* denominado **"ratizacion"**, que contribuiria a la endemia persistente en Nuble.

### 1.4 Terminologia clave

| Termino | Definicion | Fuente |
|---------|-----------|--------|
| **Ratada** | Floracion masiva sincronica (>10,000 ha, >10x roedores, brotes epidemicos). Tipica >40S con *C. culeou*. | Jaksic & Lima 2003 |
| **Ratizacion** (NUEVO, hipotesis de trabajo) | Aumento subliminal de natalidad *O. longicaudatus* (2-5x basal) por floracion sectorial parcheada (10-1,000 ha). Indetectable sin proxies satelitales. Recurrente. Zona transicion 36-40S con *C. quila*. Sin datos directos de trampeo de roedores -- inferido indirectamente via proxy satelital (FSI) y correlacion con casos SCPH. | Propuesto en este paper |
| **FSI** | Forest Stress Index = indice de estres forestal (algoritmo M3). | Desarrollado para este proyecto |
| **R_main** / **R** | Variable predictora en M1, derivada de M2 que deriva de M3 | Pipeline anti-circular |
| **Q_area_conf** | Fraccion de pixeles con estres forestal confirmado por comuna-mes | Variable principal de M3 |

### 1.5 Panel oficial

- **Archivo:** `PANEL_OFICIAL_M1M2_v1.csv` (ubicaciones: `datos/` y `planilla proyecto/M1 cerrado/`)
- **Dimensiones:** 5796 filas (21 comunas x 276 meses), ~60 columnas
- **SHA256:** 0b87c5b46b1894a822d2c31ce880ef7452e24ba4b98d6e66bffc4b38eeb4802a
- **Casos totales:** 136 (112 Transparencia SEREMI 2002-2019 + 24 Geolocalizacion 2020-2024)
- **Trazabilidad:** documentos/TRAZABILIDAD_PANEL_OFICIAL.md

### 1.6 Alerta de contaminacion

**`M1_panel_v5_DEFINITIVO_100pct.csv` esta CONTAMINADO** -- asignaciones comuna/mes generadas por Gemini AI, NO de registros fuente. NUNCA USAR. Todos los resultados previos basados en ese panel estan INVALIDADOS.

---

## 2. Fuentes de datos y muestreo

### 2.1 Datos epidemiologicos

| Atributo | Valor |
|----------|-------|
| **Fuente** | SEREMI Salud Nuble (base oficial de vigilancia) |
| **Periodo** | 2002-2024 (23 anos) |
| **Cobertura** | 21 comunas, mensual |
| **Criterio diagnostico** | SCPH confirmado por IgM Hantavirus y/o PCR (ISP) |
| **Clasificacion** | Comuna de residencia (no de infeccion) |
| **Sub-fuentes** | 2002-2019: Ley de Transparencia SEREMI; 2020-2024: Geolocalizacion SEREMI |
| **Limitaciones** | Vigilancia pasiva (survivorship bias ISP -- sesgo NUEVO-07, S32). Fichas clinicas perdidas pre-2012 (Dospital discrepancia). Hospital San Carlos → HLH (fugas diagnosticas documentadas). |
| **Referencia** | Boletin Epidemiologico SE52 MINSAL 2024; PPT SEREMI 2002-2023, 2020-2024 |

**Nota sobre discrepancia con Dospital et al. 2024:** La tasa reportada de 3.0/100k es un ERROR -- corresponde al grupo etario 20-24, NO la tasa regional (Resuelto A1, S20). La tasa real es 1.22/100k hab-ano.

### 2.2 Datos satelitales (M3/FSI)

| Atributo | Valor |
|----------|-------|
| **Plataforma** | Google Earth Engine (GEE) |
| **Sensores** | Landsat 5/7/8 (2002-2016), Sentinel-2 (2017-2024) |
| **Resolucion espacial** | 30m (Landsat), 20m efectiva (Sentinel-2, limitada por SWIR) |
| **Resolucion temporal** | Mensual (composites) |
| **Indices** | dNDMI (detector primario), NDVI (guardian dosel), NBR2 (guardian fuego) |
| **Mascara forestal** | ESA WorldCover 2021, clase 10 |
| **Cobertura** | 21 comunas de Nuble |
| **Referencia algorítmo** | Documentado en CONTEXTO_M3_CONSTRUCCION_COMPLETA.md (631 lineas) |
| **Limitacion critica** | El codigo GEE del algoritmo FSI (que genera M3) NO esta en el repositorio del proyecto. Solo estan los scripts de ERA5-Land (R/GEE_ERA5Land_*.js). Esto limita la reproducibilidad directa, aunque la especificacion textual del algoritmo es completa. (Correccion obligatoria #6) |

### 2.3 Datos climaticos

| Atributo | Valor |
|----------|-------|
| **Fuente** | ERA5-Land Monthly Aggregated (ECMWF) |
| **Variables** | Temperatura 2m (t2m, Kelvin→Celsius), Precipitacion total (pr, m→mm) |
| **Resolucion nativa** | ~11 km (0.1 grados) |
| **Periodo** | 1999-2024 |
| **Extraccion** | GEE reduceRegions con scale=11132, media por poligono comunal |
| **Derivadas** | t2m_era5land_ma3 (media movil 3 meses), pr_era5land_ma3 |
| **Scripts GEE** | R/GEE_ERA5Land_con_GADM.js (GADM level 3), R/GEE_ERA5Land_precipitacion_invernal.js (centroides) |
| **Cobertura scripts** | Scripts versionados cubren Z2+Z3 (13 comunas interior). Las 8 comunas costeras tienen datos ERA5-Land completos en el panel (276/276 meses, 0 NAs; 7 con ERA5L_centroid, 1 Cobquecura con ERA5L_inland_point). Extraccion costera por script no versionado. **P-03 CERRADO S37.** |
| **Limitacion** | ERA5-Land no validado con estaciones meteorologicas locales (sesgo NUEVO-05, S32) -- estandar Q1 para estudios ecologicos globales, pero declarar como limitacion. |

### 2.4 Datos geograficos (covariables estaticas)

| Variable | Fuente | Resolucion | Valor |
|----------|--------|-----------|-------|
| `forest_pct` | GEE (ESA WorldCover 2021) | 10m | % cobertura forestal por comuna |
| `agri_pct` | GEE (ESA WorldCover 2021) | 10m | % cobertura agricola por comuna |
| `mean_elev_m` | GEE (SRTM 30m DEM) | 30m | Elevacion media comunal (m.s.n.m.) |
| `mean_slope_deg` | Derivado de SRTM | 30m | Pendiente media (grados) |

**Multicolinealidad:** forest_pct vs mean_slope_deg rho=0.952 → slope ELIMINADA. forest_pct rho=0.193 con tasa (NS) → ELIMINADA del modelo primario. mean_elev_m retenida (rho=0.418, R2=0.606 con tasa entre comunas).

### 2.5 Datos poblacionales

| Atributo | Valor |
|----------|-------|
| **Fuente** | INE (Instituto Nacional de Estadisticas Chile) |
| **Censos** | 2002, 2017 |
| **Metodo** | Interpolacion intercensal log-lineal por comuna-ano |
| **Variable** | `pop_year` (poblacion anual), `log_pop` = log(pop_year) |
| **Poblacion regional** | ~487,866 hab (promedio periodo) |
| **Uso en modelo** | log_pop como COVARIABLE (NO offset). Coef=0.614, p=0.002. Riesgo NO escala linealmente con poblacion (test coef=1 rechazado, z=-2.511, p=0.012). |

### 2.6 Datos de zona ecologica

| Atributo | Valor |
|----------|-------|
| **Fuente** | EPF_human_21comunas.csv (ecotone-prone fraction) |
| **Clasificacion** | BINARIA Ward: costa (8 comunas) / interior (13 comunas "quiloide") |
| **Estado** | zone_f REMOVIDA del modelo final S29-K (p=0.186, redundante con RE, Hodges & Reich 2010). Clasificacion Z1/Z2/Z3 ELIMINADA. |
| **SHA256 EPF:** | a015ddc0ed4d... |

### 2.7 Transicion de sensor

| Periodo | Sensor | Observaciones |
|---------|--------|-------------|
| 2002-2016 | Landsat 5/7/8 | MIN_CLEAR=2, resolucion 30m |
| 2017-2024 | Sentinel-2 | MIN_CLEAR=3, resolucion 20m |

**Control:** Variable `sensor_era_f` en modelo (Landsat vs S2). Split-sample S25B: psi_Landsat=-0.20 (p=0.22), psi_S2=-0.58 (p=0.01). Sensor dummy NS (p=0.78). Sensor NO confunde. (Correccion obligatoria #4)

**NO hubo calibracion cruzada espectral** entre sensores. NDMI baja sin calibrar, pero el algoritmo trabaja con cambios relativos (delta-NDMI), mas robustos al cambio de sensor que valores absolutos.

---

## 3. Epidemiologia descriptiva

### 3.1 Incidencia

- **Incidencia media:** 1.22/100k hab-ano (136 casos / 23 anos / 487,866 hab) (Panel oficial)
- **Ratio vs nacional:** ~3-5x (nacional ~0.26-0.42/100k; Boletin MINSAL SE52 2024, Reyes et al. 2019, Riquelme 2015). Multiples fuentes convergen en el rango. (P-07 CERRADO S37)
- **Nuble 2021-2024:** 3 (0.58), 5 (0.97), 8 (1.54 = maxima nacional), 5 (0.96) casos por ano (Boletin MINSAL 2024)
- **Nuble consistentemente top 2-3 nacional** (2019, 2023, 2024, 2025)
- **Letalidad regional:** 38/136 = 27.9% (PPT SEREMI + Reporte 2024). [NOTA: La serie clinica HCHM (n=34, 2012-2025) presenta letalidad 5/34=14.7% (IC 95% Clopper-Pearson: 5.0-31.1%), inferior a la regional historica. Esto es consistente con: (a) mejoras en el manejo del SCPH post-2012 (ECMO, ventilacion protectora), (b) sesgo de seleccion por fichas clinicas perdidas pre-2012 que incluyen muertes tempranas no registradas en HCHM, y (c) derivaciones a Hospital Las Higueras sin retorno de informacion. La letalidad regional (27.9%) es la correcta para el componente eco-epidemiologico; la clinica (14.7%) refleja el subconjunto con fichas disponibles.]

### 3.2 Distribucion mensual verificada (Correccion obligatoria #9)

Fuente: PANEL_OFICIAL_M1M2_v1.csv, verificado contra CSV real.

| Mes | Casos | % |
|-----|-------|---|
| Ene | 21 | 15.4% |
| Feb | 13 | 9.6% |
| Mar | 26 | 19.1% |
| Abr | 17 | 12.5% |
| May | 15 | 11.0% |
| Jun | 5 | 3.7% |
| Jul | 3 | 2.2% |
| Ago | 4 | 2.9% |
| **Sep** | **0** | **0.0%** |
| Oct | 4 | 2.9% |
| Nov | 8 | 5.9% |
| Dic | 20 | 14.7% |
| **Total** | **136** | **100%** |

**Estacionalidad (Correccion obligatoria #1):**
- Oct-Mar = 92/136 = **67.6%**
- Oct-May = 124/136 = **91.2%**
- Septiembre = 0 casos en 23 anos consecutivos (2002-2024)
- [NOTA: El "89%" del CONTEXTO_M3 es INCORRECTO -- correspondia a una version anterior del panel. Los valores correctos son 67.6% (Oct-Mar) o 91.2% (Oct-May)]

### 3.3 Distribucion geografica

**Top comunas por tasa /100k (Panel oficial, Ranking_Comunas_Verificado):**
1. El Carmen: 7.49/100k
2. Pinto: 3.93/100k
3. Coihueco: 2.54/100k
4. San Ignacio: 2.36/100k
5. Yungay: 2.08/100k

**Ninhue:** 0 casos (control natural, structural zero)
**11 de 21 comunas** tienen 3 o menos casos totales en 23 anos.

### 3.4 Distribucion de conteos

- cases=0: 97.7% de observaciones
- cases=1: 2.17%
- cases=2: 0.03%
- cases=3: 0.02%
- Max mensual = 3. El 97.7% de los no-ceros son exactamente 1.
- **Esporadicidad:** 97.2% de casos en anos epidemicos son esporadicos (1 caso/comuna-mes)
- **Ano epidemico operacional:** >=7 casos regionales/ano (P75)

### 3.5 Demografia

- 73% masculino (Panel oficial)
- Mediana edad: **32 anos** (serie clinica HCHM 2012-2025, n=34, verificado contra datos/parsed_clinical_all.csv; media=34.9, rango 11-69). [CORRECCION: el valor "17 anos" del CONTEXTO_M3 es un ERROR -- no se pudo reproducir contra ningun CSV del proyecto. Dospital 2024 reporta mediana 34 en su serie de 101 casos, consistente con los 32 de HCHM. NOTA: esta mediana es de la serie clinica (n=34), NO del panel ecologico completo (n=136) que no tiene variable edad individual]
- Rurales: 59%, agricultores/forestales: 49%

---

## 4. Ecologia y marco teorico

### 4.1 Fenologia de *Chusquea quila* (Gonzalez 2001)

| Fase | Timing | Descripcion |
|------|--------|-------------|
| Espigadura | Mes 0 (tipicamente Ago) | Gatillo climatico (sequia/precipitacion extrema) |
| Pico floracion | Mes +5 (tipicamente Ene) | Floracion sectorial visible |
| Pico dispersion semillas | Mes +17 | >50 millones frutos/ha |
| Muerte completa | Mes +20-23 | Abr-Jul del ano 2 |
| **Ciclo total** | ~20 meses | |
| Ciclos de recurrencia | 5-15 anos (algunos hasta 70) | |

**Referencia:** Gonzalez, M. & Donoso, C. (1999). Bosque 20(1):47-56; Gonzalez (2001). Bosque 22(2):45-51, DOI:10.4206/bosque.2001.v22n2-05.

**Floracion SECTORIAL (correccion de Gonzalo):** La floracion de *C. quila* en Nuble es sectorial sincronica, NO masiva como las ratadas clasicas de *C. culeou* >40S. Esto fue confirmado por el patron espacial de eventos: regionales simultaneos, sin migracion ni propagacion (r sinconia entre comunas=0.546, S27).

### 4.2 Biologia de *Oligoryzomys longicaudatus*

| Parametro | Valor | Fuente |
|-----------|-------|--------|
| Madurez sexual | 2-3 meses | Allen 2006 |
| Gestacion | ~25 dias | Allen 2006 |
| Camadas/ano | 3 | Allen 2006 |
| Crias normal/outbreak | 5 / 7 | Allen 2006 |
| Potencial anual | 15-21 crias/hembra | Allen 2006 |
| Seroprevalencia M vs F | 19% vs 5.8% | Allen 2006 |
| Contacto machos | 5x mas frecuente | Allen 2006 |
| R0 estimado | 1.38-2.12 | Allen 2006, Gutierrez-Jara 2022 |

### 4.3 Modelo Abramson (2007)

- K_c = capacidad de carga critica
- K < K_c → infeccion se extingue
- K > K_c → infeccion persiste
- Mast seeding: K → K x alpha → explosion infeccion (traveling wave)

### 4.4 Linea temporal integrada quila-roedor-humano

```
Mes 0:     Gatillo climatico (sequia/precipitacion extrema)
Mes 4-12:  Floracion sectorial C. quila → NDMI baja (FSI detecta)
Mes 17:    PICO DISPERSION SEMILLAS (>50M frutos/ha)
Mes 20-24: Muerte quila + boom reproductivo O.l.
Mes 22-30: Ratizacion: densidad 2-5x basal
Mes 26-33: Onda infecciosa viral
Mes 28-36: CASOS HUMANOS SCPH (pico primavera-verano)
Mes 30-42: Agotamiento recurso, retorno a basal
```

**Lags esperados:** Floracion→Casos: 18-24 meses. Semillacion→Casos: 8-16 meses.
**Lag modelado:** 5 meses (FSI→casos), pre-especificado antes de modelar (Gonzalez 2001 descargado 24-ene-2026, 45 dias antes de Chat S4).

### 4.5 Notas ecologicas para interpretacion

1. R NO marca DONDE ocurren los casos -- marca CUANDO hubo evento quiloide en la comuna. Casos ocurren en ecotonos bosque-agricultura, no dentro del bosque.
2. R detecta "evento quiloide" = perturbacion forestal compatible con floracion/muerte de bambuseas. NO confirma especie.
3. Signo negativo de psi: R alto (cicatriz post-floracion visible) → ciclo ya paso → menos casos. Lo peligroso: R bajo + condiciones calidas (fase activa de floracion).
4. **Trampa ecologica** (concepto rescatado S32): El ecotono bosque-agricultura atrae roedores pero expone humanos. Asociacion incondicional respecto a configuracion del paisaje (ecotono NS, p=0.601).
5. **Asociacion inversa R-casos TRIPLE-INCONDICIONAL:** La asociacion inversa entre R y casos se observa de forma consistente e independiente de: (a) zona ecologica, (b) temperatura, (c) configuracion del paisaje. [NOTA: lenguaje observacional -- estudio ecologico, no causal]

### 4.6 Diferenciacion con Epuyen (Martinez et al. 2020, NEJM)

- Epuyen (Chubut, Argentina, 2018-2019): 34 casos, 11 muertes (32%), R0=2.12 pre-medidas
- Los autores no incluyeron factores ecologicos/ambientales en su analisis, lo que representa una oportunidad de complementacion
- Zona con 500 anos de documentacion quila-roedor-enfermedad (O'Higgins 1780, Gonzalez 2006)
- Floracion *C. culeou* 2011-2012 llego a PN Lago Puelo (7 km de Epuyen), consistente con un componente ecologico no evaluado
- 82 HCW expuestos directamente → 0 infectados: hallazgo consistente con una predominancia de transmision ambiental sobre la transmision persona-persona por aerosoles
- **Argumento para Discusion:** El marco de ratizacion podria complementar la hipotesis de super-spreaders, ofreciendo un mecanismo ecologico para la amplificacion viral previa al brote. Nuble y Epuyen podrian representar manifestaciones del mismo fenomeno ecologico a diferente escala (hipotesis a evaluar).

---

## 5. Pipeline M3 -- Forest Stress Index

### 5.1 Arquitectura anti-circularidad (INVIOLABLE)

```
M3 (senal satelital pura: dNDMI/NBR2/NDVI, Landsat + Sentinel-2)
  ↓ CERO datos epidemiologicos
M2 (indice de ratizacion: transformacion monotonica de M3)
  ↓ SHA256 verificado, 0 columnas epidemiologicas
M1 (GLMM: ¿R predice casos SCPH?)
```

**Prohibiciones absolutas:**
- M1 NUNCA ajusta M3 (sin tuning retrospectivo)
- M2 NO se calibra con M1 (sin usar casos para elegir rezagos/umbrales)
- No mezclar etapas antes del cierre individual

### 5.2 Algoritmo FSI -- 3 pasos

Para cada pixel clasificado como bosque (ESA WorldCover 2021, clase 10), en cada timestep mensual t:

**PASO 1 -- Deteccion de candidatos (dNDMI):**
```
DELTA_NDMI_pre  = NDMI(t) - NDMI(t-1)
DELTA_NDMI_post = NDMI(t+1) - NDMI(t)

CANDIDATO = (DELTA_NDMI_pre < p25_comuna) AND (DELTA_NDMI_post < p25_comuna)
```
Donde p25_comuna = percentil 25 de TODA la serie historica de DELTA_NDMI para esa comuna (2002-2024).

**PASO 2 -- Veto por disturbio antropogenico:**
```
VETO = (DELTA_NDVI_pre < -0.20) OR (DELTA_NDVI_post < -0.20)
    OR (DELTA_NBR2_pre < -0.15) OR (DELTA_NBR2_post < -0.15)
```

**PASO 3 -- Metrica FSI:**
```
Q_area_conf = (pixeles CONFIRMADOS) / (pixeles EVALUABLES en la comuna)
donde: CONFIRMADO = CANDIDATO AND NOT(VETO)
```

### 5.3 Logica ecologica

| Evento | NDMI | NDVI | NBR2 | Vetado? |
|--------|------|------|------|---------|
| Floracion quila | baja bajo p25 | ESTABLE | ESTABLE | NO → confirmado |
| Tala/cosecha | baja bajo p25 | baja < -0.20 | baja < -0.15 | SI → vetado |
| Incendio | baja bajo p25 | baja < -0.20 | baja < -0.15 | SI → vetado |

Los tres indices tienen significados ecologicos DIFERENTES. No se promedian ni combinan linealmente. Logica AND-NOT, no aritmetica.

### 5.4 Parametros congelados (Correccion obligatoria: fijados en Achibueno)

| Parametro | Valor | Significado |
|-----------|-------|-------------|
| PCTL_DNDMI | 25 | Percentil 25 comunal para candidato |
| thrNDVI | -0.20 | Umbral de veto por perdida de dosel |
| thrNBR2 | -0.15 | Umbral de veto por fuego/quemadura |
| MIN_CLEAR | 2 (Landsat) / 3 (S2) | Minimo observaciones claras para mes evaluable |
| Mascara | ESA WorldCover 2021, clase 10 | Pixeles forestales elegibles |

**Estos parametros fueron definidos y congelados en Achibueno ANTES de aplicar a Nuble. No se re-optimizaron.**

### 5.5 Validacion en Achibueno

- Achibueno (Region del Maule) = sitio de referencia con evento documentado 2022 y 2003
- LOO t-score para evento historico 2003: t = +3.67 sigma. [Metodo: se excluye el mes del evento conocido, se calcula la media y DE de la serie residual, y se evalua cuantas DE el mes excluido se desvía de la media. Un t>2 indica que el FSI detecta anomalia significativa sin haber "visto" el evento.]
- Multi-scale spatial convergence: p < 0.001

### 5.6 Migracion a Nuble

1. **Parametros congelados** aplicados identicos a 21 comunas
2. **Correcciones nombres:** Ranquil → Ranquil (tilde), Treguaco → Trehuaco
3. **Periodo:** 2002-2024 (Landsat 5/7/8 + Sentinel-2)
4. **Mascara unica:** ESA WorldCover 2021 clase 10

### 5.7 Reproducibilidad M3 -- Tabla de correlaciones

Correlacion parcial entre Achibueno y cada comuna de Nuble (controlando T y P regionales), con block permutation (B=2000, bloques 12 meses) y BH-FDR:

| Comuna | r_partial | p_block | p_FDR | Sig |
|--------|-----------|---------|-------|-----|
| Treguaco | +0.55 | <0.001 | <0.01 | *** |
| Coelemu | +0.54 | <0.001 | <0.01 | *** |
| Niquen | +0.48 | <0.001 | <0.01 | *** |
| Cobquecura | +0.46 | 0.002 | <0.01 | ** |
| San Nicolas | +0.46 | 0.001 | <0.01 | *** |
| San Ignacio | +0.43 | 0.001 | <0.01 | ** |
| Pemuco | +0.44 | 0.002 | <0.01 | ** |
| Quirihue | +0.44 | <0.001 | <0.01 | *** |
| Portezuelo | +0.44 | <0.001 | <0.01 | *** |
| San Carlos | +0.44 | <0.001 | <0.01 | *** |
| El Carmen | +0.42 | 0.001 | <0.01 | ** |
| Coihueco | +0.42 | <0.001 | <0.01 | *** |
| Ranquil | +0.41 | <0.001 | <0.01 | *** |
| Chillan | +0.40 | 0.001 | <0.01 | ** |
| Yungay | +0.40 | 0.002 | <0.01 | ** |
| Chillan Viejo | +0.37 | 0.002 | <0.01 | ** |
| Ninhue | +0.37 | 0.002 | <0.01 | ** |
| Pinto | +0.34 | 0.008 | <0.01 | ** |
| Bulnes | +0.34 | 0.019 | 0.02 | * |
| San Fabian | +0.31 | 0.012 | 0.01 | * |
| Quillon | +0.23 | 0.090 | 0.09 | ns |

**Resultado:** 20/21 comunas significativas (BH-FDR). Bonferroni: 13/21. T y P regional explican <3% (retencion 97.1%).

### 5.8 Vulnerabilidades M3

1. **Mascara incluye potencialmente plantaciones:** ESA WorldCover clase 10 puede clasificar pino/eucalipto. Mitigado por veto NDVI/NBR2 (r=0.94 entre M3 primario y M3_EHF800).
2. **Sin calibracion cruzada Landsat→S2:** Diferente sensibilidad. Mitigado por uso de cambios relativos (delta-NDMI) y sensor_era_f en M1.
3. **R no validado en terreno:** Proxy indirecto. Detecta "evento quiloide compatible", no confirma especie.
4. **Codigo GEE no depositado:** La especificacion textual es completa pero el script JS no esta en el repositorio. Depositar en Zenodo/GitHub antes de submission. (Correccion obligatoria #6)

---

## 6. Pipeline M2 -- Ratizacion

### 6.1 Transformacion M3 → M2

Script: `R/M2_PIPELINE_REPRODUCIBLE.R` (reproducido con error=0.000000 en CADA columna vs panel oficial).

```
Paso 1: X = Q_area_conf filtrado por okEval (meses no evaluables = NA, NO 0)
Paso 2: z = (X - mediana_comuna) / MAD_comuna
         MAD = median absolute deviation SIN factor 1.4826 (Correccion obligatoria #12)
Paso 3: m_v1 = 1 + 0.5 * sigmoid(z)     [rango m ∈ [1.0, 1.5]]
Paso 4: R_v1_lag0 = m_v1 - 1             [rango ∈ [0, 0.5]]
Paso 5: R_v1_lagk = shift(R_v1_lag0, k)  [k = 0..12 meses, por comuna]
Paso 6: R_v1_main = mean(lag1..lag6, minimo 3 disponibles)
```

**MAD sin factor 1.4826 (Correccion obligatoria #12):** El z-score usa MAD raw (`median(abs(X - median_X))`), NO la version escalada (`MAD * 1.4826` para normalidad). Confirmado en linea 44 de M2_PIPELINE_REPRODUCIBLE.R:
```r
panel[, mad_X := median(abs(X_recalc - median_X), na.rm = TRUE), by = comuna]
```

### 6.2 Sigmoide y rango

- sigma(z) = 1 / (1 + exp(-z))
- m_v1 = 1 + 0.5 * sigma(z) → rango [1.0, 1.5]
- Define operacionalmente "ratizacion" = aumento 0-50% sobre densidad basal
- Ratada sensu stricto = >1000% (>10x). Factor separacion conceptual: ~20x.

### 6.3 Lags pre-calculados

- R_v1_lag0 a R_v1_lag12 disponibles en el panel
- **R_v1_lag5** = lag usado en modelo final S29-K (pre-especificado por hipotesis biologica, Gonzalez 2001)
- R_v1_main = media de lags 1-6 (variable usada en modelo S22, NO en modelo final S29-K). [NOTA: en el panel, R_v1_main y R_v1_lag5 son columnas distintas. El modelo S29-K usa exclusivamente R_v1_lag5]

### 6.4 Verificacion anti-circularidad

- SHA256 verificado: 0 columnas epidemiologicas en M3 ni M2
- Pipeline Q→z→sigma→R→lags reproducido con error 0.0 (S26 auditoria integral)
- M3 no tiene NINGUN dato de casos. M2 es transformacion monotonica de M3.

### 6.5 Justificacion biologica del lag 5

**Pre-especificacion (Lag5_Preespecificado, S23):**
- Gonzalez 2001 descargado 24-ene-2026 (45 dias antes de Chat S4, 11-mar-2026)
- UNICO paper con fenologia de *C. quila* en zona centro-sur Chile
- Fase terminal (diseminacion + muerte): Nov-Mar = 5 meses = lo que FSI detecta
- Cadena bibliografica: Gonzalez 2001 + Jaksic & Lima 2003 + Barrera 2007 + Ortiz 2004
- BH correction p=0.089 NO APLICA a hipotesis pre-especificada (Rothman 1990)

**Validacion confirmatoria (S34 -- perfil lags recalculado con especificacion S29-K):**
- Perfil lags 0-12 recalculado con especificacion S29-K (S34): lag 5 UNICO significativo (psi=-0.309, p=0.009). Los 12 restantes NS (todos p>0.32). Pre-especificacion CONFIRMADA.
- Walk-forward 14/14 folds con psi<0
- Permutacion circular p=0.004 (S36, 999 iter, Phipson-Smyth; S34 previo: p=0.002, 499 iter)
- LOCO 21/21 negativo

---

## 7. Pipeline M1 -- GLMM Epidemiologico

### 7.1 Modelo cerrado S29-K (DEFINITIVO)

**Especificacion:**
```
cases ~ season_f + t2m_era5land_within_sc + R_v1_lag5_within_sc +
        log_pop + (1 | comuna_f)

family = nbinom2
```

**Ecuacion matematica:**
```
cases_it ~ NegBin(mu_it, theta)

log(mu_it) = beta_0
           + beta_1 * I(season=primavera)
           + beta_2 * I(season=verano)
           + beta_3 * I(season=otono)
           + beta_4 * t2m_within_sc_it
           + psi * R5_within_sc_it
           + beta_5 * log(pop_it)
           + u_i

u_i ~ N(0, sigma^2_u)
```

**Variables y justificacion:**

| Variable | Tipo | Justificacion | Referencia |
|----------|------|---------------|------------|
| season_f | FE categorico (4 niveles: primavera, verano, otono; **invierno = categoria base/referencia**) | Estacionalidad 91.2% Oct-May. LRT p<0.0001 vs sin season. | Toro 1998, chi2=29.7 |
| t2m_within_sc | FE continuo | Temperatura within-comuna, scaled. Captura variacion temporal. | Bell & Jones 2015 |
| R5_within_sc | FE continuo | Ratizacion within-comuna, lag 5, scaled. Variable de interes. | Gonzalez 2001 |
| log_pop | FE continuo | Poblacion como covariable (no offset). Coef!=1. | Feng 2021, Patterson-Lomba 2022 |
| (1\|comuna_f) | RE intercept | Heterogeneidad comunal. 21 clusters. | Bolker 2009 |

### 7.2 Within-between decomposition (Bell-Jones)

```
Para cada variable v ∈ {t2m_era5land, R_v1_lag5}:
  v_between_i = mean(v_it) por comuna (toda la serie)
  v_within_it = v_it - v_between_i

Scaling: post-filtro por lag (CRITICO -- scale() DESPUES de filtrar NA de lag 5)
```

**Justificacion:** Separa variacion temporal intra-comuna (mecanismo de interes) de heterogeneidad geografica inter-comuna (confundente). Bell & Jones 2015, Mundlak 1978, Schunck & Perales 2017. **Primera aplicacion a hantavirus** (contribucion metodologica novel).

**Between-component:** psi_between=-0.018 (p=0.935) → confundimiento espacial DESCARTADO. Hausman NS (p=0.291).

### 7.3 Cambios respecto a modelos anteriores

| Atributo | S22 (operativo) | S29-K (definitivo) | Cambio |
|----------|----------------|-------------------|--------|
| zone_f | SI (p=0.186) | **NO** (redundante con RE) | Removida: Hodges & Reich 2010 |
| year_centered | SI | **NO** (3 enfoques identicos) | Removida: sin efecto |
| log_pop | offset | **covariable** (coef=0.614) | Test coef=1 rechazado p=0.012 |
| psi | -0.287 | **-0.309** | -7.7% (mas fuerte) |
| AUC OOS | 0.7402 | **0.766** (cvAUC, LeDell 2015) | +3.5% |
| AIC | -- | **950.7** | -- |
| BIC | -- | **1009.1** | -6.8 vs con zone |
| EPV | 13.5 | **15.4** | +14% (menos parametros) |
| Hessian warns | 5/14 | **1/14** | Mejor convergencia |
| Shrinkage | 14% | **12%** | Menos optimismo |

### 7.4 Resultados -- Coeficientes

Fuente: resultados/S34_Q1_CALCULOS/01_coeficientes_IC_profile.csv (verificado contra CSV)

| Parametro | Estimado | IC 95% profile | SE | p | IRR | IC 95% IRR |
|-----------|----------|----------------|-----|---|-----|-----------|
| Intercept | -10.415 | [-14.726, -6.603] | 1.951 | <0.001 | -- | -- |
| season_primavera | -0.877 | [-1.925, 0.120] | 0.516 | 0.090 | 0.416 | [0.146, 1.128] |
| season_verano | +0.177 | [-0.976, 1.337] | 0.588 | 0.764 | 1.193 | [0.377, 3.808] |
| season_otono | +0.935 | [0.114, 1.779] | 0.422 | 0.027 | 2.547 | [1.120, 5.924] |
| beta_t2m_within | +0.384 | [0.017, 0.756] | 0.188 | 0.041 | 1.468 | [1.017, 2.130] |
| **psi_R5_within** | **-0.309** | **[-0.546, -0.081]** | **0.118** | **0.009** | **0.734** | **[0.580, 0.923]** |
| beta_log_pop | +0.614 | [0.223, 1.047] | 0.196 | 0.002 | 1.847 | [1.250, 2.850] |
| theta (NB2) | 1.555 | -- | -- | -- | -- | -- |

**AIC:** 950.7 | **BIC:** 1009.1

**Interpretacion psi:** Un incremento de 1 DE en R5_within_sc se asocia con una reduccion del 26.6% en la tasa de SCPH (IRR=0.734, IC 95% profile [0.580, 0.923]). R alto = cicatriz post-floracion visible = ciclo ya paso = menos riesgo.

**IC 95% profile (S34):** Calculados via `confint(modelo, method="profile")`. IC profile [-0.546, -0.081] para psi. SE Wald=0.118 (CSV: 01_coeficientes_IC_profile.csv). SE bootstrap S36=0.120 (consistente). IRR IC = exp(IC profile) = [0.580, 0.923]. Referencia: Cole 2014 Stat Med (profile likelihood).

### 7.5 BLUPs (efectos aleatorios comunales)

**Top 5 riesgo (S29-K):**
1. El Carmen: u=+1.221, IRR=3.39
2. Coihueco: u=+0.764, IRR=2.15
3. Pinto: u=+0.573, IRR=1.77
4. San Ignacio: u=+0.503, IRR=1.65
5. Quillon: u=+0.434, IRR=1.54

**Bottom 3:**
- Chillan Viejo: u=-0.933, IRR=0.39
- Ninhue: u=-0.517, IRR=0.60
- Quirihue: u=-0.481, IRR=0.62

### 7.6 EPV (Correccion obligatoria #8)

- **EPV con parametros efectivos:** 136 eventos / 8.8 parametros = **15.4** (RE cuenta como fraccion del total)
- **EPV con parametros nominales:** 136 eventos / 7 parametros fijos = **19.4**
- Ambos superan la regla de 10 (Peduzzi 1996). Reportar ambos con explicacion.
- Referencia adicional: Riley 2019 (Stat Med), van Smeden 2016/2019, Vittinghoff 2007.

### 7.7 Panel oficial -- Estructura

| Atributo | Valor |
|----------|-------|
| Filas | 5796 (21 comunas x 276 meses) |
| Columnas clave | comuna, year, month, cases, deaths, pop_year, log_pop, t2m_era5land, pr_era5land, sensor, okEval, Q_area_conf, R_v1_lag0..R_v1_lag12, R_v1_main |
| Casos totales | 136 |
| Missingness R_v1_lag5 | ~5-10% (meses iniciales por lag + meses no evaluables) |
| Muestra analitica | Filas con !is.na(R_v1_lag5) |

### 7.8 Decisiones metodologicas

| Decision | Justificacion | Referencia |
|----------|---------------|------------|
| glmmTMB (no INLA/BYM) | 21 areas insuficiente para spatial smoothing; ICC=9.43% (S34) | Vranckx et al. 2015, Riebler 2016, Leckie 2020 |
| NB2 (no Poisson/ZINB) | Ratio ceros obs/esp=1.000 → NO zero-inflation. Poisson AIC empata | Preisser 2012, Cameron & Trivedi 2013 |
| Season FE (no Fourier/AR) | LRT p<0.0001. Fourier empata AUC pero BIC peor | Zuur et al. 2009 |
| Bell-Jones within-between | Separa variacion temporal de heterogeneidad geografica | Bell & Jones 2015, Mundlak 1978 |
| Permutacion circular | Respeta estructura temporal (no simple) | Adaptado de block permutation |
| Walk-forward blocked | Evita leakage temporal (no LOYO simple) | Bergmeir & Benitez 2012 |
| log_pop covariable (no offset) | Test coef=1 rechazado (p=0.012). Riesgo no escala linealmente | Feng 2021, Smith 2009 |
| Sin zone_f | p=0.186, redundante con RE, BIC -6.8 | Hodges & Reich 2010 |
| Sin year_centered | Year centering no afecta AUC ni psi (3 enfoques identicos, S25B) | Wooldridge 2021 |
| Sin pr_within | NS (p=0.64), ya eliminada en S29 | -- |
| Sin interaccion R x t2m | Post-hoc. Modelo sin interaccion es mas parsimonioso | Hernan 2018 |

---

## 8. Validaciones y robustez

### 8.1 Blindaje G1-G6 (S24-S25B)

| ID | Test | Resultado | Detalle | Modelo |
|----|------|-----------|---------|--------|
| G1 | Walk-forward temporal | **PASS** | 14/14 folds psi<0. cvAUC=0.766 [0.701-0.823] (LeDell 2015); simple pooled=0.761 (S29-K) | S29-K |
| G2 | Sensor era split | **PASS** | psi_Landsat=-0.20 (p=0.22), psi_S2=-0.58 (p=0.01) (Correccion #4) | S25B, 21 comunas |
| G3 | Sensor dummy | **PASS** | sensor_f NS (p=0.78), VIF=2.91 | S25B |
| G4 | Random slope LRT | **PASS** | Singular convergence, LRT p=0.63 | S25B |
| G5 | Quiloide 13 comunas | **PASS** | psi=-0.332, IRR=0.718 (+9.6% mas fuerte) | S24 |
| G6 | LRT M1→M2 | **PASS** | p=0.006 (S29-K) / p=0.020 (S24) | S29-K |

### 8.2 Diagnosticos DHARMa (S29-K, S34)

| Test | Resultado | p-value | Estado |
|------|-----------|---------|--------|
| KS uniformidad | OK | 0.670 | PASS |
| Dispersion | OK | 0.840 | PASS |
| Zero-inflation | OK | 0.980 | PASS |
| Outliers | OK | 0.732 | PASS |
| Autocorrelacion temporal | -- | N/A | No aplicable (season FE) |
| Cuantiles t2m | OK | 0.809 | PASS |
| Cuantiles R5 | Marginal | 0.047 | WARN |

**Fuente:** S34, DHARMa sobre modelo S29-K (21 comunas, sin zone, log_pop covariable). 6/7 tests PASS, 1 WARN marginal (cuantiles R5, p=0.047 -- borderline, no invalida modelo). Autocorrelacion temporal no aplica porque season_f captura estacionalidad.

### 8.3 Moran's I -- Autocorrelacion espacial

- **KNN k=4:** I=0.004, p=0.328 → SIN autocorrelacion espacial (S24)
- **Delaunay:** I=-0.044, p=0.478 → confirma
- **Moran's I sobre BLUPs:** I=0.10, p=0.065 (borderline NS, S25B)

### 8.4 LOCO (Leave-One-Commune-Out)

- 21/21 comunas con psi negativo al removerlas
- Delta_max=16.7% (al remover Coihueco)
- Rango psi: [-0.335, -0.251] (S24)

### 8.5 Permutacion circular y bootstrap (S29-K, S34)

**Bootstrap S29-K (S36, corregido):**
- N = 2000 iteraciones (Davison & Hinkley 1997: >=1000 para CI percentile)
- SE bootstrap = 0.120 (vs Wald SE=0.118)
- p bootstrap = 0.007
- CI percentile = [-0.561, -0.086]
- Convergencia: 1880/2000 limpias (94%), 120/2000 con warnings (6%), 0 fallidas
- Sesgo = -0.004 (<1.2% del estimado, despreciable)
- **NOTA:** Bootstrap original S34 (1000 iter) reportaba 100% convergencia, pero el warning handler tragaba warnings silenciosamente. El bootstrap corregido S36 identifica 6% con warnings, confirmando que el resultado es robusto (SE y CI practicamente identicos).
- **Referencia:** R/S36_BOOTSTRAP_CORREGIDO.R, resultados/S36_BOOTSTRAP_CORREGIDO/

**Permutacion circular S29-K — valor CANONICO (S36):**
- **p permutacion = 0.004** (999 iteraciones, formula anti-conservadora Phipson-Smyth 2010: (b+1)/(m+1), donde b=3 permutaciones mas extremas que observado)
- Interpretacion: en 999 permutaciones circulares de la serie temporal, solo 3 produjeron un psi tan extremo como el observado (-0.309).
- **Valor previo S34:** p=0.002 (499 iter, formula clasica). Superseded por S36 (mas iteraciones, formula correcta).

**Referencia historica:** S22 reportaba SE bootstrap=0.0877, p=0.001 (modelo diferente con zone+year+offset). S29-J (blindaje): p_permutacion=0.012.

### 8.6 Discriminacion y meta-analisis de psi por fold

**AUC in-sample S29-K (S34):** 0.809 (IC 95% DeLong: 0.770-0.847). Nota: AUC in-sample > cvAUC OOS (0.766), diferencia esperada (optimismo por resubstitucion, van Leeuwen et al. 2025).

- psi pooled meta-analisis: -0.249 (p<0.0001, S24)
- I2=0%, tau2=0 → HOMOGENEIDAD PERFECTA entre folds
- Shrinkage S29-K: 12.0% (ratio psi_pooled/psi_full = -0.272/-0.309 = 0.880, shrinkage = 1-0.880 = 12.0%)

### 8.7 ICC (S34 -- DEFINITIVO)

Los distintos valores de ICC reportados en diferentes sesiones provienen de MODELOS DISTINTOS:

| Valor | Modelo | Sesion | Significado |
|-------|--------|--------|-------------|
| 3.2% | S22 VPC, 21 comunas, zone+year+offset | S24 | Variance Partition Coefficient del modelo operativo |
| 12.1% | glmer M21 (modelo quiloide diferente) | S25B | ICC calculado con formula estandar |
| 15.0% | glmer M13 quiloide (13 comunas) | S25B | ICC modelo quiloide 13 comunas |
| **9.43%** | **S29-K, 21 comunas, sin zone, log_pop covar (adjusted)** | **S34** | **DEFINITIVO. sigma2_u=0.397** |
| 7.60% | S29-K, idem (conditional) | S34 | ICC conditional (Leckie 2020) |

**Argumento anti-BYM (actualizado S34):** ICC=9.43% < 10% (Vranckx et al. 2015: spatial smoothing innecesario con ICC<10%) + Moran's I NS (p=0.328) + solo 21 areas (insuficiente para BYM2/CAR). Conclusion: glmmTMB con RE intercept es la especificacion correcta.

### 8.8 Mecanismo A (R x Temperatura) -- CERRADO

- 0/38 interacciones probadas significativas (S24)
- Asociacion inversa R-casos es consistente independientemente de la temperatura
- Modelo sin interaccion es mas parsimonioso

### 8.9 Mecanismo B (Clima → Flora) -- CERRADO

- Alternancia climatica NO predice FSI
- ENSO descartado: r~0, p>0.4 en 8 variantes de lag (S29-E)
- Driver es ciclo endogeno del bambu (C. quila), independiente de ENSO
- t2m x NDVI: r=+0.030, p=0.893 (INDEPENDIENTES)

### 8.10 Sensibilidades adicionales

| Test | Resultado | Sesion |
|------|-----------|--------|
| Linealidad splines | 4/4 predictores lineales (todos p>0.18) | S25B |
| LOYO 23 anos | 23/23 negativos, mediana AUC=0.787 | S24 |
| Lag 4/5/6 AUC | 0.742 / 0.740 / 0.725 | S24 |
| Offset vs covariable | psi difiere 0.4% | S24 |
| Fold 3 excluido | AUC sin fold3=0.738, delta=-0.002 | S25B |
| Sparsity >=4 casos | psi=-0.256 (8 comunas, p=0.078), sigue negativo | S25B |
| Poisson vs NB2 | AIC Poisson=954 vs NB2=955 (~empate) | S24 |
| ZINB | Innecesario (theta→infinito, ratio ceros=1.000) | S24 |
| Fourier K=1,2 | AUC empata, BIC peor que categorical | S29-F |
| Modelo con zone_f | psi delta=0.2%, AIC -0.3, BIC +6.8 | S29-K |

### 8.11 Metricas Q1 -- modelo quiloide comparativo (S25B, 13 comunas)

**NOTA: Las metricas de esta seccion corresponden al modelo quiloide comparativo (13 comunas, S25B), NO al modelo final S29-K. Ver seccion 8.11b para metricas S29-K.**

| Categoria | Metrica | Valor | Referencia |
|-----------|---------|-------|------------|
| Efecto | IRR | 0.718 (0.546-0.943), p=0.017 | Bolker 2009 |
| Varianza | R2m / R2c | 0.070 / 0.108 | Nakagawa 2013 |
| Heterogeneidad | MRR / ICC | 2.07 / 0.150 | Austin 2018 |
| Discriminacion | AUC global / quiloide | 0.74 / 0.73 | Van Klaveren 2014 |
| Calibracion PIT | KS p | 0.42 → CALIBRADO | Wei & Held 2014 |
| Calibracion OOS | CITL / slope / O/E | -0.70 / 0.75 / 1.20 | Van Calster 2016 |
| Scoring rules | LogS mejora vs nulo | 7.3% | Czado 2009 |
| Brier | BS / BSS | 0.020 / 0.018 | Steyerberg 2010 |
| AUC-PR | ratio vs baseline | 3.1x / 2.7x | Saito 2015 |

**Debilidades documentadas:**
- CITL=-0.70 y slope=0.75 → calibracion suboptima (sobre-prediccion leve)
- R2 bajo (0.07) → normal en GLMM ecologico con evento raro (Nakagawa 2013)
- BSS=0.018 → mejora marginal sobre prevalencia (esperado con 2% prevalencia)

### 8.11b Metricas Q1 -- modelo final S29-K (S34 + S36)

| Categoria | Metrica | Valor | Fuente |
|-----------|---------|-------|--------|
| Efecto | psi | -0.309 | S29-K |
| Efecto | IC 95% profile | [-0.546, -0.081] | S34 |
| Efecto | IRR [IC 95%] | 0.734 [0.580, 0.923] | S34 |
| Varianza explicada | R2m Nakagawa (marginal) | **0.195** | S36 |
| Varianza explicada | R2c Nakagawa (condicional) | **0.271** | S36 |
| Discriminacion | AUC in-sample (DeLong) | 0.809 [0.770, 0.847] | S34 |
| Discriminacion | cvAUC OOS (walk-forward, LeDell 2015) | **0.766 [0.701, 0.823]** | S36 (IC influence-curve; simple pooled=0.761) |
| Discriminacion | AUC-PR OOS | **0.077 (3.57x prevalencia OOS = 61/2840 = 2.15%)** | S36 |
| Calibracion in-sample | CITL / slope / O:E | 0.022 / 1.105 / 1.021 | S34 |
| Calibracion OOS walk-forward | CITL / slope / O:E | **-0.024 / 0.903 / 0.978** | S36 |
| Scoring rules OOS | Brier Score / BSS | **0.0205 / 0.024** | S36 |
| Heterogeneidad | ICC adjusted / conditional | 9.43% / 7.60% | S34 |
| Heterogeneidad | sigma2_u | 0.397 | S34 |
| Robustez | Bootstrap SE (2000 iter) | 0.120 (p=0.007, 94% clean) | S36 |
| Robustez | Permutacion circular (999 iter) | **p=0.004** (Phipson-Smyth) | S36 |
| Sensibilidad residuos | E-value point / IC | 2.07 / 1.39 | S34 |
| Diagnostico | DHARMa | 6/7 PASS, 1 WARN (R5 p=0.047, NS tras Bonferroni alpha/7=0.007) | S34 |
| Diagnostico | Rootogram | NB2 fit perfecto (count0: 4743 vs 4745) | S34 |
| Colinealidad | VIF R5_within / t2m / season_f | **1.24 / 3.29 / 3.64** (todos <5) | S36 |
| Separacion | Hessian positivo-definido | **SI**. Max SE/|est|=3.33 (season_verano, NS p=0.764) | S36 |

**Calibracion in-sample S29-K (S34):** CITL=0.022, slope=1.105, O/E=1.021. BUENA.
**Calibracion OOS walk-forward S29-K (S36):** CITL=-0.024, slope=0.903, O/E=0.978. BUENA. Leve shrinkage esperado (slope<1). Contrasta con modelo quiloide S25B (CITL=-0.70, slope=0.75, suboptima).
**R2 Nakagawa (S36):** R2m=0.195 (varianza fija), R2c=0.271 (fija+aleatoria). Valores adecuados para evento raro en GLMM ecologico (Nakagawa et al. 2017). Contrasta con modelo quiloide S25B (R2m=0.070, R2c=0.108) — S29-K explica ~3x mas varianza.
**VIF (S36):** Todos <5 (Dormann et al. 2013). Bell-Jones decomposition reduce colinealidad al separar within/between.

**DAG dagitty (S36, 9 nodos, 11 aristas) -- Nota interpretativa:**
El DAG formal (R1_DAG_dagitty.txt) especifica FSI_R5 como exposure y SCPH_cases como outcome. El adjustment set automatico de dagitty (Textor et al. 2016) incluye {Commune_RE, Rodent_density, Temperature}. Sin embargo, esta salida requiere interpretacion:
- **FSI_R5 es un PROXY** de Quila_flowering, no una causa directa de SCPH_cases. No existe flecha FSI_R5→SCPH_cases en el DAG porque FSI mide el estres forestal post-floracion, no genera riesgo directamente.
- **La asociacion estadistica** entre FSI y casos existe porque comparten la causa comun Quila_flowering (→ FSI_R5 como indicador; → Rodent_density → SCPH_cases como mecanismo biologico).
- **Rodent_density** es un mediador en la via Quila→Roedores→Casos, NO un confundente. Ajustar por Rodent_density (si estuviera medido) BLOQUEARIA la senal de interes (Jackson et al. 2023). Ademas, es no medido (no existen datos de trampeo de roedores en Nuble).
- **El modelo S29-K** ajusta por los confundentes identificables: Commune_RE (via RE intercept), Temperature (within-comuna), Season (categorico), Population (log_pop). Estos bloquean los backdoor paths FSI←Commune_RE→Cases y FSI←Quila←Temperature→Cases.
- **E-value=2.07** (VanderWeele & Ding 2017) cuantifica la robustez: un confundente no medido (incluyendo Rodent_density a traves de vias alternativas) necesitaria RR>=2.07 con AMBOS FSI y Cases para explicar la asociacion. Ningun confundente plausible identificado alcanza este umbral.
- **Referencia metodologica:** Jackson C et al. (2023) recomiendan esta distincion mediador/confundente explicita en DAGs de zoonosis donde la cadena ecologica tiene eslabones no medidos.
- **ADVERTENCIA sobre R1_DAG_resumen.csv:** El archivo CSV reporta adjustment_set={Commune_RE, Rodent_density, Temperature}. Este es el set TEORICO que dagitty calcula por d-separacion, NO el set a implementar en el modelo. Rodent_density es un mediador no medido — incluirlo bloquearia la senal de interes. El modelo S29-K implementa el set CORRECTO: {Commune_RE (via RE), Temperature (within), Season, Population}. Confundentes plausibles no incluidos en el DAG (actividad agricola estacional, cambios en vigilancia) fueron evaluados: agri_pct (r=-0.15, p=0.50, NS → descartada, seccion 10), season_f controla estacionalidad (LRT p<0.0001), y Commune_RE absorbe heterogeneidad espacial incluyendo perfil agro-productivo comunal. E-value=2.07 indica que un confundente residual necesitaria RR>=2.07 con AMBAS variables para explicar la asociacion, umbral no alcanzado por ninguno identificado.

### 8.12 Walk-forward por fold (S29-K)

| Fold | Casos | AUC | psi OOS | Hessian |
|------|-------|-----|---------|---------|
| 2011 | 3 | 0.662 | -0.363 | WARN |
| 2012 | 10 | 0.738 | -0.388 | OK |
| 2013 | 2 | 0.882 | -0.306 | OK |
| 2014 | 9 | 0.805 | -0.320 | OK |
| 2015 | 5 | 0.892 | -0.324 | OK |
| 2016 | 6 | 0.689 | -0.264 | OK |
| 2017 | 7 | 0.813 | -0.181 | OK |
| 2018 | 3 | 0.781 | -0.204 | OK |
| 2019 | 2 | 0.567 | -0.179 | OK |
| 2020 | 3 | 0.869 | -0.213 | OK |
| 2021 | 3 | 0.810 | -0.240 | OK |
| 2022 | 5 | 0.664 | -0.276 | OK |
| 2023 | 6 | 0.791 | -0.252 | OK |
| 2024 | 4 | 0.652 | -0.324 | OK |

**cvAUC (primario):** 0.766 [0.701-0.823] (promedio fold-aware con IC influence-curve, LeDell et al. 2015). **Simple pooled:** 0.761 (todos los casos OOS concatenados en una sola curva ROC). **Mean per-fold:** 0.758 (promedio simple, no ponderado). 14/14 folds psi<0. Hessian warns=1 (fold 2011, solo 3 casos en test). [NOTA: Reportamos cvAUC como metrica primaria porque el simple pooling asume intercambiabilidad de clasificadores entre folds, supuesto problematico con heterogeneidad espacial (van Leeuwen et al. 2025). Collins et al. 2024 (TRIPOD+AI Item 10d) recomienda transparencia total del metodo de validacion interna.]

### 8.13 E-value (VanderWeele & Ding 2017) -- S34

- **E-value punto:** 2.07 (para IRR=0.734)
- **E-value IC inferior:** 1.39 (para IC upper=0.923)
- **Interpretacion:** Un confundente no medido necesitaria asociarse con AMBOS la exposicion (R5) y el outcome (casos SCPH) con un RR >= 2.07 para explicar completamente la asociacion observada. Para mover el IC a incluir el nulo, bastaria RR >= 1.39.
- **Contexto:** En estudios ecologicos con datos agregados, E-value > 2.0 se considera moderadamente robusto. Ningun confundente plausible identificado tiene RR >= 2.07 con ambas variables.
- **Referencia:** VanderWeele TJ, Ding P (2017). Sensitivity analysis in observational research: introducing the E-value. Ann Intern Med 167(4):268-274.

### 8.14 Rootogram (Kleiber & Zeileis 2016) -- S34

| Conteo | Observado | Esperado NB2 |
|--------|-----------|-------------|
| 0 | 4743 | 4745 |
| 1 | 98 | 97 |
| 2 | 5 | 4 |

**Interpretacion:** El modelo NB2 predice casi exactamente la distribucion de conteos observada. No hay evidencia de zero-inflation (obs 4743 vs esp 4745, delta=-2). Consistente con test ZINB NS y ratio ceros obs/esp=1.000.

**Referencia:** Kleiber C, Zeileis A (2016). Visualizing count data regressions using rootograms. Am Stat 70(3):296-303.

---

## 9. Framework predictivo y escenarios

### 9.1 Modelo 2 etapas (S27)

**Etapa 1:** n_eventos_quiloides = 70.4 - 193.3 x NDVI_mean (R2=0.523, R2adj=0.500, p=0.0001, SE=11.0, n=23 anos)
**Etapa 2:** eventos → distribucion por comuna (proporcion historica) → GLMM → MC 10k simulaciones

### 9.2 Escenarios NDVI x CMIP6 (S29-D/S29-K)

Deltas CMIP6 (IPCC AR6 Atlas, SWS, 10 GCMs):
- SSP2-4.5 ~2030: +0.7C → IRR=1.061 (+6.1%)
- SSP2-4.5 ~2050: +1.2C → IRR=1.108 (+10.8%)
- SSP5-8.5 ~2030: +0.8C → IRR=1.071 (+7.0%)
- SSP5-8.5 ~2050: +1.8C → IRR=1.166 (+16.6%)

**Tabla escenarios S29-K (Correccion obligatoria #10):**

| Escenario NDVI | Actual: E [IC 95%] | SSP2-4.5 2050: E [IC 95%] | SSP5-8.5 2050: E [IC 95%] |
|----------------|---------------------|---------------------------|---------------------------|
| BAJO | 3.4 [0, 8] | 3.8 [0, 8] | 4.1 [1, 9] |
| NEUTRO | 3.3 [0, 7] | 3.6 [0, 8] | 3.8 [1, 8] |
| ALTO | 3.1 [0, 7] | 3.4 [0, 8] | 3.6 [0, 8] |

Fuente: tabla_escenarios_FINAL.csv (10,000 simulaciones MC, script S29K_MODELO_FINAL_SIN_ZONE.R). E=E[total] casos/ano regional. IC 95% = percentiles 2.5-97.5 de las 10k realizaciones.

**Tabla extendida — probabilidades de excedencia (peor escenario: BAJO + SSP5-8.5 2050):**

| Metrica | Valor |
|---------|-------|
| P(>=2 casos en alguna comuna) | 41.4% |
| P(>=3 casos en alguna comuna) | 8.2% |
| P(>=5 casos totales regionales) | 38.2% |
| P(>=8 casos totales regionales) | 6.3% |

[NOTA: Valores de S29-K sin zone ni offset. El CONTEXTO_M3 y S29-D reportaban 3.6 para BAJO+Actual, que correspondia al modelo con zone+offset. Los IC amplios reflejan la incertidumbre compuesta de: (a) R2=0.52 etapa 1 NDVI→eventos, (b) R2m=0.195 etapa 2 GLMM, (c) variabilidad estocastica NB2 con theta=1.555. CMIP6 deltas provienen de 10 GCMs IPCC AR6 Atlas SWS (Iturbide et al. 2020). Los IC deben interpretarse como rangos plausibles, no predicciones puntuales.]

Efecto marginal NDVI (BAJO/ALTO): +13%
Efecto marginal clima (SSP585_2050/Actual): +16.4%
Combinado peor vs mejor: **+32%**

### 9.3 Ciclos NDVI (S27)

- Bloques ALTO: media 1.7 anos (max 3)
- Bloques BAJO: media 2.2 anos
- Estado 2024: Fase ALTO, 2 anos consecutivos
- P(transicion ALTO→BAJO): 2yr=50%, 3yr=83%, 4yr=100%
- Fase BAJO: 2.8 casos/ano; Fase ALTO: 1.6 casos/ano

### 9.4 Semaforo SEREMI (producto operativo)

| Color | Criterio | Comunas |
|-------|----------|---------|
| ROJO | P>=25% | Chillan 34%, Coihueco 30%, El Carmen 29%, San Carlos 26% |
| AMARILLO | P 10-25% | Pinto, San Ignacio, Yungay, Quillon, Bulnes |
| NARANJO | P 5-10% | San Fabian, Pemuco, Coelemu, Chillan Viejo, Niquen, Cobquecura |
| VERDE | P<5% | San Nicolas, Quirihue, Ranquil, Trehuaco, Portezuelo, Ninhue |

### 9.5 Modelos descartados

| Modelo | Razon descarte | Sesion |
|--------|----------------|--------|
| Patron temporal (ACF/lag anual) | ACF=-0.20, lag NS, AIC empeora | S26 |
| Modelo 2 niveles macro→micro | AUC=0.607, NDVI macro p=0.91 | S26 |
| Modelo hibrido GLMM+desc | MAE 2.04 vs desc 2.01, bug validacion | S27/S28 |
| 3 opciones quiloide como covariable | gamma NS, delta-AIC positivo | S27 |
| Markov NDVI | Converge en ~2 pasos, predicciones indistinguibles | S29-B |

---

## 10. Variables evaluadas y descartadas

| Variable | Resultado | Razon | Sesion |
|----------|-----------|-------|--------|
| ENSO (ONI) | r~0, p>0.4 | Quila no responde a ENSO | S29-E |
| % Cobertura agricola | r=-0.15, p=0.50 | Colineal con NDVI, sin variacion comunal | S29-G |
| % Cobertura forestal | r=-0.13, p=0.58 | Idem | S29-G |
| Precipitacion within | NS (p=0.64) | Ya eliminada | S29 |
| Precipitacion between | NS | -- | -- |
| Temperatura between | NS con bootstrap | 21 clusters insuficientes | S24 |
| DLNM lag flexible | No testeado | 136 casos insuficientes | S29 |
| ZINB | No necesario | NB predice 97.7% ceros = observado 97.8% | S24 |
| BYM2/CAR espacial | No implementado | ICC=9.43% (<10%, Vranckx 2015), Moran NS, solo 21 areas | S34 |
| Fourier season | AUC empata, BIC peor | Categorical se mantiene | S29-F |
| Random slopes | No testeado | 6.5 eventos/comuna, insuficiente | S25B |
| Gasto municipal SINIM | Descartado pre-test | Sin evidencia Q1, causalidad reversa | S29 |
| VIIRS luminosidad | Descartado pre-test | Redundante con BLUPs | S29 |
| Interaccion R x t2m | 0/38 interacciones significativas | Post-hoc, no parsimonioso | S24 |
| Interaccion zone x NDVI | p=0.647 NS | Sin mejora | S29-A |
| Cobertura suelo MODIS | AIC empeora (+1.7 a +2.0) | Sin variacion entre comunas | S29-G |
| year_centered | 3 enfoques identicos | No afecta nada | S25B |

---

## 11. Bibliografia organizada por tema

### 11.1 Ecologia y biologia

- Gonzalez M (2001). Floracion C. quila. Bosque 22(2):45-51. DOI:10.4206/bosque.2001.v22n2-05
- Gonzalez M, Donoso C (1999). Produccion semillas C. quila. Bosque 20(1):47-56
- Munoz AA, Gonzalez ME (2009). Regeneracion quila zona centro-sur
- Guerreiro C, Lizarazu MJ (2010). Causas floracion quila
- Jaksic FM, Lima M (2003). Myths and facts on ratadas. Austral Ecology 28:237-251 [NOTA: aplica a Chile semiarido ~30S, NO a Nuble ~36S]
- Veblen TT (1979). Structure/dynamics Nothofagus forests. Ecology 60(5):937-945
- Pacheco et al. (2017). C. montana floracion PN Puyehue
- Gonzalez (2006). Documentacion quila-roedor historica Patagonia

### 11.2 Hantavirus -- Epidemiologia y modelamiento

- Dospital et al. (2024). Perfil epidemiologico Nuble. Brazilian Journal of Biology [NOTA: tasa 3.0/100k es ERROR -- grupo etario]
- Martinez VP et al. (2020). Person-to-person hantavirus, Epuyen. NEJM 383:2230-41. DOI:10.1056/NEJMoa2009040
- Allen LJS (2006). SEIR hantavirus + parametros O. longicaudatus
- Abramson G (2007). Modelo K_c traveling wave
- Gutierrez-Jara JP (2022). Modelamiento SEIR hanta Chile
- Ortiz et al. (2004). Contexto regional hantavirus
- Barrera et al. (2007). Mecanismo biologico roedores-bambu
- Tagle et al. (2013). [Lag 5 cadena bibliografica]
- Nsoesie et al. (2014). ARIMA Chile 667 casos. PLoS NTD
- Gao et al. (2025). NDVI+hantavirus. PLoS NTD
- Tian et al. (2017). PNAS hantavirus NDVI
- Ferro et al. (2020). Hantavirus satelital
- Murua R (2003). ENSO+roedores. Oikos
- Reyes et al. (2019). Incidencia nacional hantavirus Chile
- Prist et al. (2017). Land cover+hantavirus Brasil. PLoS NTD
- Muylaert et al. (2019). Hantavirus Brasil municipal INLA

### 11.3 Estadistica y metodologia

- Brooks ME et al. (2017). glmmTMB. R Journal 9(2):378-400
- Hartig F (2022). DHARMa R package
- Bell A, Jones K (2015). Fixed effects. Polit Sci Res Methods 3(1):133-153
- Mundlak Y (1978). On pooling time series and cross-section data. Econometrica
- Schunck R, Perales F (2017). Within-between decomposition. British J Math Stat Psych
- Peduzzi P et al. (1996). EPP rule. J Clin Epidemiol 49:1373-1379
- Riley RD et al. (2019). EPV minimum sample size. Stat Med
- van Smeden M et al. (2016/2019). EPV revision
- Vittinghoff E et al. (2007). EPV relaxation
- Hernan MA (2018). Exploratory vs confirmatory. Am J Epidemiol
- Wagenmakers EJ et al. (2012). Pre-registro y transparencia
- Bolker BM et al. (2009). GLMMs practical guide. TREE 24(3):127-135
- Harrison XA et al. (2018). Brief intro GLMMs. PeerJ
- Burnham KP, Anderson DR (2002/2004). Model selection. Springer / Sociol Meth Res
- Hodges JS, Reich BJ (2010). Adding random effects. Am Stat
- Nakagawa S, Schielzeth H (2013/2017). R2 for GLMM. Methods Ecol Evol
- Preisser JS et al. (2012). Zero-inflated models. Caries Res 46:413-423
- Cameron AC, Trivedi PK (2013). Regression analysis of count data
- Zuur AF et al. (2009). Mixed effects models ecology. Springer
- Vranckx et al. (2015). MCMC vs INLA disease mapping. Arch Public Health 73
- Bergmeir C, Benitez JM (2012). Walk-forward cross-validation time series
- Steyerberg EW (2010/2019). Clinical prediction models. Springer
- Van Calster B et al. (2016/2019). Calibration
- Pencina MJ et al. (2008/2011). NRI/IDI
- Pustejovsky JE, Tipton E (2018). Robust SE
- Cameron AC, Miller DL (2015). Robust SE clusters
- Dormann CF et al. (2013). VIF collinearity
- von Elm E et al. (2007). STROBE
- Moons KGM et al. (2015). TRIPOD
- Collins GS et al. (2024). TRIPOD+AI. BMJ 385:e078378
- Cole SR et al. (2014). Maximum likelihood, profile likelihood, and penalized likelihood. Am J Epidemiol / Stat Med
- Leckie G et al. (2020). Partitioning variation in multilevel models for count data. Psychol Methods 25(6):787-801
- Kleiber C, Zeileis A (2016). Visualizing count data regressions using rootograms. Am Stat 70(3):296-303
- Van Calster B et al. (2019). Calibration: the Achilles heel of predictive analytics. BMC Med 17:230
- VanderWeele TJ, Ding P (2017). Sensitivity analysis in observational research: introducing the E-value. Ann Intern Med 167(4):268-274
- Roberts DR et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8):913-929
- Sofaer HR et al. (2019). Area under the precision-recall curve: point estimates, confidence intervals and the role of class imbalance. Methods Ecol Evol 10(7):962-972
- Benchimol EI et al. (2015). RECORD
- Shmueli G (2010/2025). Explain vs predict. Stat Sci
- Greenland S et al. (1999). DAGs. Epidemiology
- Textor J et al. (2016). DAGitty
- Jackson C et al. (2023). DAG zoonotico
- LeDell E, Petersen M, van der Laan M (2015). Computationally efficient confidence intervals for cross-validated area under the ROC curve estimates. Electron J Stat 9(1):1583-1607. DOI:10.1214/15-EJS1035
- Van Leeuwen FD et al. (2025). Instability of the AUROC of clinical prediction models. Stat Med 44(5):e70011. DOI:10.1002/sim.70011
- Greenland S, Morgenstern H (1989). Ecological bias, confounding, and effect modification. Int J Epidemiol 18(1):269-274. DOI:10.1093/ije/18.1.269
- Phipson B, Smyth GK (2010). Permutation P-values should never be zero. Stat Appl Genet Mol Biol 9:article 39. DOI:10.2202/1544-6115.1585
- Zheng X et al. (2020). Bamboo flowering cycle sheds light on flowering diversity. Front Plant Sci 11:381. DOI:10.3389/fpls.2020.00381
- Bogdziewicz M et al. (2024). Evolutionary ecology of masting. TREE 39(9):851-862. DOI:10.1016/j.tree.2024.05.002
- Wang Y et al. (2017). Accommodating the ecological fallacy in disease mapping. Stat Med 36(30):4930-4942. DOI:10.1002/sim.7494

### 11.4 Anti-sesgo y validacion

- Rothman KJ (1990). No corrections for multiple comparisons on pre-specified hypotheses
- Imai K, Kim IS (2019). Exogeneity within-between. AJPS
- Wooldridge JM (2021). TWFE Mundlak
- Zhang L et al. (2018). RSE sensor remote sensing
- Matuschek H et al. (2017). Random slopes parsimonia
- Maas CJM, Hox JJ (2005). Random effects clusters
- Khan ME, Calder CA (2022). Spatial confounding. JASA
- Feng C et al. (2021). Offset vs covariate. J Appl Stat
- Smith CE et al. (2009). Population scaling. PNAS
- Patterson-Lomba O et al. (2022). Population offset. J Urban Health

### 11.5 Clima y escenarios

- Salazar A et al. (2024). CMIP6 Chile. Clim Dyn
- Garreaud RD et al. (2020). Megadrought Chile. Int J Climatol
- Iturbide M et al. (2020). IPCC AR6 Atlas. ESSD
- Runge M et al. (2024). Escenarios enfermedad. Epidemics
- Colon-Gonzalez FJ et al. (2021). Escenarios clima-enfermedad. PLoS Med

### 11.6 Deteccion remota

- Pena Araya MA (2007). Deteccion satelital quila
- Garrido et al. (2021). Deteccion remota floracion bambu

### 11.7 Scoring y prediccion

- Czado C et al. (2009). Predictive assessment count data. Biometrics
- Bracher J et al. (2021). Proper scoring rules. PLoS Comput Biol
- Bosse NI et al. (2023). Scoring epidemic forecasts. PLoS Comput Biol
- Wei W, Held L (2014). Calibration tests. TEST
- Kim S et al. (2024). CPS metric exceedance. Stat Med
- Saito T, Rehmsmeier M (2015). AUC-PR

### 11.8 Vigilancia y reportes Chile

- Boletin Epidemiologico SE52 MINSAL 2024
- Informe Epidemiologico Hantavirus 2022 MINSAL
- Informe Epidemiologico Hantavirus 2024 MINSAL
- PPT SEREMI Nuble 2002-2023, 2020-2024
- Toro J et al. (1998). Estacionalidad hantavirus Chile

### 11.9 Papers pendientes de DOI o verificacion

[NOTA: S32 auditoria identifico 42 papers sin DOI y 11 citados sin entrada formal. Estos deben completarse durante la fase de manuscrito. Lista detallada en resultados/AUDITORIA_TOTAL/03_bibliografia_completa.md]

---

## 12. Vacios, pendientes y contradicciones

### 12.1 Pendientes criticos

| ID | Pendiente | Prioridad | Nota |
|----|-----------|-----------|------|
| P-01 | ~~Recalcular ICC para modelo S29-K~~ | **CERRADO** | ICC=9.43% adjusted, 7.60% conditional, sigma2_u=0.397. Seccion 8.7. Fuente: S34. |
| P-02 | ~~Recalcular bootstrap SE y permutacion circular para S29-K~~ | **CERRADO** | Bootstrap S36 (2000 iter, 94% clean): SE=0.120, p=0.007, CI [-0.561, -0.086]. Perm S36 (999 iter, Phipson-Smyth): p=0.004. Seccion 8.5. Fuentes: S36_BOOTSTRAP_CORREGIDO/, S36_METRICAS_Q1/. [Valores previos S34 (1000 iter): SE=0.119, p=0.016 — superseded] |
| P-03 | ~~Verificar fuente climatica comunas costa (8 comunas)~~ | **CERRADO** | Panel oficial confirma: 21/21 comunas con t2m ERA5-Land completo (276/276 meses, 0 NAs). 20 comunas=ERA5L_centroid, Cobquecura=ERA5L_inland_point (centroide en mar). Script GEE versionado solo cubre 13 comunas Z2+Z3; extraccion costera por script no versionado o GEE manual. Fuente: PANEL_OFICIAL_M1M2_v1.csv columna climate_source. Verificado S37. |
| P-04 | Depositar codigo GEE FSI en Zenodo/GitHub | ALTA | Especificacion textual COMPLETA en CONTEXTO_M3 (631 lineas, Parte 4). Parametros congelados documentados. Checklist de deposito preparado: resultados/AUDIT_S37/P04_GEE_DEPOSIT_CHECKLIST.md. **REQUIERE ACCION GONZALO:** localizar script GEE original y depositar (Opcion A), o reconstruir (Opcion B), o declarar en Supplementary (Opcion C). S37. |
| P-05 | 42 papers sin DOI verificado | MEDIA | Lista completa en resultados/AUDITORIA_TOTAL/03_bibliografia_completa.md (188 papers unicos, 561 lineas). Busqueda parcial S37 (agente alcanzo limite web). Muchos son revistas chilenas sin DOI (Bosque, Rev Med Chile, Rev Chil Infectol) o tesis/documentos gubernamentales sin DOI asignable. **Completar durante fase manuscrito** via CrossRef/Google Scholar. No bloquea AM-I. |
| P-06 | ~~IC 95% exactos para IRR de modelo S29-K~~ | **CERRADO** | IC profile [-0.546, -0.081], IRR [0.580, 0.923]. Seccion 7.4. Fuente: S34 confint profile. |
| P-07 | ~~Dato MINSAL exacto ratio nacional (A2)~~ | **CERRADO** | Nuble: 136 casos / 23 anos / 487,866 hab media = 1.21/100k hab-ano. Nacional: ~50-80 casos/ano / ~19M hab = 0.26-0.42/100k (Boletin MINSAL SE52 2024; Reyes et al. 2019; Riquelme 2015). Ratio = 2.9-4.7x (conservador). Reportar como "~3-5x la tasa nacional" con rango. No se requiere dato unico oficial porque multiples fuentes convergen. Verificado S37 contra PANEL_OFICIAL_M1M2_v1.csv. |
| P-08 | TRIPOD + STROBE checklists formales | MEDIA | Mapeo preliminar completado S37: STROBE 4 PRESENT/16 PARTIAL/6 MISSING, TRIPOD 4/14/6. 6 gaps ALTA prioridad identificados (missing data handling, flow diagram, univariables, funding, TRIPOD type, generalizabilidad). Todos son gaps de REPORTE, no de metodologia. Detalle: resultados/AUDIT_S37/STROBE_TRIPOD_MAPPING_AMI.md. **Ejecutar checklists formales sobre MANUSCRITO** (decision S32 confirmada). |
| P-09 | ~~DHARMa diagnosticos completos para S29-K~~ | **CERRADO** | 7 tests: 6 PASS, 1 WARN (R5 cuantiles p=0.047). Seccion 8.2. Fuente: S34. |

### 12.2 Contradicciones resueltas

| Contradiccion | Resolucion | Sesion |
|---------------|-----------|--------|
| Incidencia 3.0 vs 1.22/100k | 3.0=error Dospital (tasa etaria 20-24). Real=1.22 | S20 |
| Panel 135 vs 136 casos | 135=PANEL_OFICIAL_COMPLETO_v1 (version anterior). 136=PANEL_OFICIAL_M1M2_v1 (actual) | Trazabilidad |
| "89%" estacionalidad | Incorrecto. Oct-Mar=67.6%, Oct-May=91.2% | Correccion #1 |
| ICC 3.2% vs 15% | Modelos distintos (VPC S22 vs ICC glmer M13 quiloide) | S32 |
| Sensor psi -0.42/-0.28 | Valores del modelo quiloide S25, DESCARTADOS. Correctos: -0.20/-0.58 (S25B, 21 comunas) | S32 |
| AUC 0.7402 vs 0.7611 | 0.7402=S22 (zone+year+offset). 0.7611 pooled=S29-K (sin zone, log_pop covar). Modelos distintos | S29 |
| Escenarios 3.6 vs 3.4 (BAJO+Actual) | 3.6=S29-D (con zone+offset). 3.4=S29-K (sin zone, log_pop covar) | Correccion #10 |
| AUC pooled vs cvAUC vs mean | cvAUC=0.766 (LeDell 2015, primario). Simple pooled=0.761 (concatenado). Mean per-fold=0.758. Reportar cvAUC con IC [0.701-0.823] | S36/S37 |
| Nombre panel OFICIAL vs COMPLETO | PANEL_OFICIAL_M1M2_v1.csv=nombre actual. PANEL_OFICIAL_COMPLETO_v1.csv=nombre anterior | Correccion #11 |
| AUC 0.53 quiloide | Pipeline diferente (13 comunas sin zone_f). AUC quiloide subset del modelo 21com=0.73 | S25B |
| Mediana edad 17 vs 32 anos | 17=ERROR CONTEXTO_M3 (no reproducible contra ningun CSV). Real: mediana 32 (HCHM n=34, parsed_clinical_all.csv), media 34.9. Dospital: mediana 34 (n=101). | S34 |

### 12.3 Sesgos abiertos (declarar como limitacion)

| Sesgo | Estado | Mitigacion |
|-------|--------|-----------|
| ERA5-Land no validado localmente | Limitacion | Estandar Q1 global pero declarar |
| Survivorship bias ISP | Limitacion | Intrinseco a vigilancia pasiva |
| R no validado en terreno | Limitacion | Proxy indirecto, validacion Achibueno parcial |
| Single region (generalizabilidad regional) | Limitacion | Este estudio demuestra dinamicas ecotono-especificas de Nuble (interfaz bosque nativo *C. quila* / agricultura). Las regiones del sur de Chile (>40S), donde predomina *C. culeou* con floraciones gregarias masivas (ratadas sensu stricto, Jaksic & Lima 2003), podrian presentar dinamicas distintas — mayor amplitud poblacional de roedores, mayor extension espacial, y brotes epidemicos reconocidos. El concepto de "ratizacion" (florecimiento sectorial sincronico no masivo de *C. quila*) propuesto aqui requiere validacion en otras regiones con ecotonos y bambu similares. Los datos agregados a nivel comunal no permiten inferencias individuales (Greenland & Morgenstern 1989), pero el diseno ecologico es apropiado para identificar patrones poblacionales a escala regional. |
| Calibracion OOS modelo quiloide (CITL=-0.70) | Contexto | Corresponde al modelo quiloide 13 comunas (S25B), NO al modelo final S29-K. Calibracion S29-K: in-sample CITL=0.022 (S34), OOS CITL=-0.024, slope=0.903, O/E=0.978 (S36). AMBAS BUENAS. |
| Codigo GEE no depositado | Mitigable | Depositar antes de submission |
| Mascara forestal incluye plantaciones | Limitacion | Veto NDVI/NBR2 mitiga (r=0.94 con EHF800) |
| Drift psi temporal | Limitacion | slope +0.008, Mann-Kendall NS (S25B) |
| DHARMa cuantiles R5 p=0.047 | Limitacion | Marginal (borderline). No invalida modelo: 6/7 tests PASS, direccion del efecto robusta en 14/14 folds y 21/21 LOCO. Puede reflejar no-linealidad residual menor en R5. |
| Estacionariedad CMIP6 | Limitacion | Texto S25B redactado |

### 12.4 Contribuciones metodologicas unicas

Segun comparacion con 14 papers hantavirus Latinoamerica (S24):
1. **Primer GLMM** para hantavirus en Sudamerica
2. **Primer Bell-Jones within-between** aplicado a hantavirus
3. **Primer walk-forward temporal** para hantavirus
4. **Primer FSI satelital** para hantavirus (indice propio)
5. **Primer modelo NDVI x CMIP6** para hantavirus

---

## RESUMEN FINAL

### Secciones completas: 12/12 (+ 4 subsecciones nuevas en v1.2: 8.11b, 8.13, 8.14, perfil lags actualizado)

### Correcciones obligatorias aplicadas: 12/12

| # | Correccion | Aplicada en |
|---|-----------|-------------|
| 1 | Estacionalidad 67.6%/91.2% | Seccion 3.2 |
| 2 | AUC especificar "pooled" | Secciones 7.4, 8.12 |
| 3 | ICC modelos distintos → RESUELTO S34 (9.43%) | Seccion 8.7 |
| 4 | Sensor psi correctos S25B | Secciones 2.7, 8.1 |
| 5 | ERA5-Land solo Z2+Z3 + PENDIENTE | Seccion 2.3 |
| 6 | Codigo GEE FSI no en repositorio | Secciones 2.2, 5.8 |
| 7 | Bootstrap/permutacion → RESUELTO S34 | Seccion 8.5 |
| 8 | EPV doble reporte | Seccion 7.6 |
| 9 | Distribucion mensual verificada CSV | Seccion 3.2 |
| 10 | Escenarios S29-K (3.4 no 3.6) | Seccion 9.2 |
| 11 | Nombre panel correcto | Seccion 1.5 |
| 12 | MAD sin factor 1.4826 | Seccion 6.1 |

### Integraciones S34 (v1.2):
- ICC adjusted=9.43%, conditional=7.60% (Seccion 8.7)
- IC profile psi [-0.546, -0.081], IRR [0.580, 0.923] (Seccion 7.4)
- DHARMa S29-K 7 tests, 6 PASS + 1 WARN (Seccion 8.2)
- E-value=2.07 / 1.39 (Seccion 8.13)
- Rootogram NB2 fit perfecto (Seccion 8.14)
- Perfil lags 0-12 confirmado: lag 5 UNICO sig (Seccion 6.5)
- AUC in-sample=0.809 DeLong (Seccion 8.6)
- Calibracion in-sample CITL=0.022, slope=1.105, O/E=1.021 (Seccion 8.11b)

### Integraciones S36 (v1.3):
- Bootstrap 2000 iter corregido: SE=0.120, p=0.007, 94% clean (Seccion 8.5)
- Permutacion 999 iter Phipson-Smyth: p=0.004 (Seccion 8.5, 8.11b)
- R2m Nakagawa=0.195, R2c=0.271 (Seccion 8.11b) — 3x mejor que quiloide
- AUC OOS con IC: 0.766 [0.701, 0.823] (Seccion 8.11b)
- Calibracion OOS: CITL=-0.024, slope=0.903, O/E=0.978 (Seccion 8.11b) — BUENA
- AUC-PR OOS=0.077 (3.57x baseline) (Seccion 8.11b)
- Brier Score=0.0205, BSS=0.024 (Seccion 8.11b)
- VIF: todos <5. R5_within=1.24 (Seccion 8.11b)
- Hessian positivo-definido. Sin separacion (Seccion 8.11b)
- DAG dagitty formal con 9 nodos (Seccion 8.11b, archivo R1_DAG_dagitty.txt)
- Aprobacion etica V-12 integrada (Seccion 1.1)

### Pendientes criticos: 5 items (Seccion 12.1) -- 4 CERRADOS en v1.2 (P-01, P-02, P-06, P-09)

### Contradicciones resueltas: 11 (Seccion 12.2)

### Sesgos abiertos como limitacion: 9 (Seccion 12.3) -- Calibracion OOS reclasificada (modelo quiloide, no S29-K)

### Papers compilados: ~261 (S32 base ~253 + 8 nuevos S34), organizados en 9 categorias tematicas

---

*Fin del Archivo Maestro Parte I -- Componente Eco-Epidemiologico*
*Compilado: 2026-03-26 por Claude Code (master-builder)*
*Actualizado: 2026-03-28 v1.2 -- Integracion completa calculos S34/S34B*
*Proximos pasos: Manuscrito, integracion con Parte II (clinica)*
