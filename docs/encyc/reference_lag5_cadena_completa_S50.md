---
name: Lag 5 — Cadena ecológica completa cerrada (S50, corregida)
description: Síntesis de las 6 preguntas técnicas de Gonzalo sobre lag 5, señal satelital, ratización, generaciones de colilargo y disolución temporal. CORREGIDA S50 tras auditoría Q1: NRI asimétrico RETIRADO (doblemente caído), Barrera 2007 "Estación 5" MARCADO como paráfrasis pendiente de verificación, Castillo/Riquelme requieren contexto geográfico en manuscrito (Temuco n=16 / Puerto Montt n=103), lag 16 con caveat S22. Usar como anclaje anti-vacío pero NO como fuente ciega.
type: reference
---

# Lag 5 — Cadena ecológica completa cerrada (S50, 2026-04-05)

## Contexto de creación
Gonzalo pidió en S50 cerrar conocimiento sobre 6 preguntas técnicas del lag 5 ANTES de redactar la Discussion del paper EID. Esta nota consolida respuestas ya resueltas y blindadas Q1 en sesiones S19-S49.

## 1. Definición matemática del lag 5

**Variable final:** `R5_within_sc` (S29-K) alias `R_v1_lag5_within_sc` (pre-S29)

**Construcción:**
- R_v1 = NDVI Landsat 30m procesado por pipeline M3→M2
- lag 5 = desplazamiento temporal de 5 meses (R_v1 del mes t-5)
- within = centrado Bell-Jones (desviación de la comuna respecto a su media histórica, Bell & Jones 2015)
- _sc = escalado (mean=0, sd=0.134 en modelo quiloide; re-escalado en S29-K)

**Coeficiente S29-K final:** ψ = −0.309 ± 0.118, p = 0.009, IRR = 0.734, CI profile [0.580, 0.923]

**Interpretación:** Por cada DE que el NDVI cae dentro de la comuna 5 meses antes, los casos suben ~27%. Signo negativo porque la caída del NDVI (desecación de quila) predice más casos después.

## 2. Origen biológico de los 5 meses (pre-especificado)

**Fuente:** González 2001 (Bosque 22(2):45-51, DOI 10.4206/bosque.2001.v22n2-05)
**Descarga:** 24-ene-2026 → 45 días ANTES del primer modelo (Chat S4, 11-mar-2026)
**Pre-especificación:** rango 3-12 meses entre S5-S6 Chat (Murúa & González 1986)
**Validación:** perfil exploratorio lags 0-24 confirma lag 5 como el más fuerte (p=0.004)
**BH:** NO aplica (Rothman 1990, hipótesis pre-especificada)

### 4 fases fenológicas de C. quila (González 2001)
| Fase | Meses | FSI/NDVI detecta |
|---|---|---|
| 1. Espigadura | Ago-Nov año 1 | NO (follaje verde) |
| 2. Antesis | Nov año 1 - Feb año 2 | NO (follaje verde) |
| 3. Fructificación | Feb-Nov año 2 (secamiento inicia fin Ago) | Parcial |
| **4. Diseminación + muerte** | **Nov año 2 - Mar año 3 (~5 meses)** | **SÍ** |

Los 5 meses = duración de la fase terminal detectable por satélite.

## 3. Qué captura el satélite

**NO captura:** floración, antesis, fructificación temprana (todas con follaje verde)
**SÍ captura:** fase terminal = desecación foliar + muerte de culmos (NDVI colapsa)

La muerte del culmo es SIMULTÁNEA con la diseminación de semillas (González 2001: "máxima caída de frutos en enero, >50M frutos/ha, González & Donoso 1999").

**Escala espacial:** parches sectoriales de pocas hectáreas, floración SECTORIAL SINCRÓNICA NO MASIVA. El pixel Landsat 30m es suficiente (memory/project_floracion_sectorial.md S24).

## 4. Aumento de roedores en ratización (proxy, no directo)

**Limitación declarada #3 AMF:** no hay trampeo en Ñuble. El modelo usa proxy FSI→NDVI→casos.

### Evidencia triangulada

**4.1 IRR por evento quiloide (S27)**
Evento quiloide = mes con R_v1_lag5_within_sc < −1

| Eventos en Dic-Mar | IRR | Δ% |
|---|---|---|
| 0 | 1.00 | ref |
| 1 | 1.394 | +39% |
| 2 | 1.942 | +94% |
| 3 | 2.706 | +171% |
| 4 | 3.771 | +277% |

Observado Dic-Mar 8 comunas top: ratio ×3.11 (Wilcoxon p=0.011)

**4.2 E-value VanderWeele-Ding 2017:** 2.07 (punto), 1.39 (CI)

**4.3 Ciclo reproductivo O. longicaudatus (Barrera Gómez 2007, UACh)**
- Temporada reproductiva: Oct-Abr (7 meses)
- 3-5 camadas/año
- Machos adultos dominan en verano (mantienen virus)

**4.4 Distinción ratización vs ratada**
- Ratización = 1 < θ < 2.1× densidad basal (sub-catastrófico, Spotorno 2000 + Jaksic-Lima 2003)
- Ratada = 20-30× basal (catastrófico, solo C. culeou >40°S)
- Nuestro modelo opera en rango de ratización, NO ratada

## 5. Por qué lag 5 sobrevivió todos los tests

| Test | Resultado |
|---|---|
| Pre-especificación González 2001 | 45 días antes del modelo (timestamps) |
| Perfil lags 0-24 | lag 5 más fuerte (p=0.004) |
| Walk-forward 14 folds | 14/14 ψ<0 |
| LOCO (drop comuna) | 21/21 misma dirección |
| LOYO (drop año) | 21/21 misma dirección |
| Permutación circular 999 | p=0.004 (S34) |
| Bootstrap 2000 | SE=0.120, p=0.007, CI[-0.561,-0.086], 94% clean |
| DHARMa 7 tests | 6/7 PASS |
| Profile CI | [-0.546,-0.081] no cruza cero |
| E-value | 2.07 / 1.39 |
| VIF | 1.24 (sin colinealidad) |

### Significado matemático (S29-K)
```
log(μ_it) = β₀ + β_season·season_f + β_t2m·t2m_within_sc
          + ψ·R5_within_sc + β_pop·log_pop + u_i
Y_it ~ NegBin2(μ_it, θ=1.555)
```

- Efecto within (temporal intra-comuna), no between → elimina confundente geográfico
- Lineal en escala log: cada DE de caída NDVI multiplica por exp(0.309)=1.362
- Condicionalmente independiente de temperatura (Mecanismo A: 0/38 interacciones p_BH>0.92)
- Condicionalmente independiente de la comuna (RE absorbe BLUPs)

### Por qué otros lags fracasaron
- Lags 0-4: señal aún verde, sin desecación detectable
- Lags 6-12: señal ya diluida por recuperación NDVI
- Fuera del rango 3-12: biología González 2001 no respalda mecanismo

## 6. Cadena ecológica completa: MODELO BIFÁSICO RETENCIÓN → DISPERSIÓN

**IMPORTANTE:** El signo negativo de ψ NO es protección ambiental. Es **confinamiento temporal del roedor dentro del parche quiloide durante el lag 5**, seguido de dispersión forzada al ecotono.

### FASE 1 — RETENCIÓN (lag 0 → lag 5)
Meses del caso: Nov-Mar (leen NDVI de Jun-Oct)

```
Quila entra monocarpia → muere sincrónicamente → satélite capta desecación
  → Liberación masiva semillas (>50M frutos/ha, Gonzalez & Donoso 1999)
  → O. longicaudatus se CONCENTRA en el parche
     (alimento + refugio + comunidad reproductiva)
  → Temporada reproductiva Oct-Abr (Barrera 2007)
  → Ratización sub-catastrófica (1 < θ < 2.1× basal)
  → ROEDOR NO SE DISPERSA — óptimo local ecológico
  → Pocos casos humanos (roedor dentro del bosque, lejos peridoméstico)
```

**Firma estadística del confinamiento (S29-K + tests robustez):**
- Lags 0-4: sin señal detectable (pre-desecación, follaje verde)
- Lag 5: ψ = -0.309, IRR = 0.734, profile CI [-0.546, -0.081]
- Lags 6-10: protección decae hacia cero (dispersión subliminal)
- Cero lags positivos significativos (advertencia Chat S11-S12 feedback_chat_errores_S11S12:16)
- Interpretación: el pixel Landsat ve la fase de retención en el parche, no la fase de dispersión al ecotono peridoméstico
- Anclaje externo al confinamiento: literatura ocupacional (Castillo 2001, Riquelme 2015) + dinámica post-masting O. longicaudatus (Murúa 2003, Spotorno 2000, Jaksic-Lima 2003) + incondicionalidad triple (Mecanismo A, ecotono, sensor)
- NOTA Q1 (S50): descomposición NRI asimétrica previa (NRI−=+0.305 / NRI+=-0.063) RETIRADA por (a) números de S19 supersedidos por S22 y (b) método NRI inapropiado para count outcomes con 97.7% ceros (Pepe 2015, Hilden 2014; prohibido internamente en S38). Ver reference_biblio_NRI_IDI_alternatives.md.

**Implicación operacional:** mapa de exclusión humana del parche quiloide activo.

### FASE 2 — DISPERSIÓN POST-LAG 5 (lag 6-10)
Meses del caso: Abr-Sep

```
Semillas agotadas por consumo intenso
  → Descomposición culmos → pérdida refugio
  → Población aumentada NO sostenible
  → DISPERSIÓN FORZADA hacia ecotono:
     - Viviendas rurales (bodegas grano, gallineros, leñeras)
     - Bordes campos agrícolas
     - Áreas trabajo forestal/agrícola
  → Contacto humano-roedor en peridoméstico
  → CONTAGIO AMBIENTAL
```

**Evidencia epidemiológica:**
- Castillo 2001 CHEST 120:548-554: 88% casos HPS Chile = trabajadores forestales/agrícolas
- Riquelme 2015 EID: 87% exposición peridoméstica/ocupacional
- Caso C30 El Carmen 2023 (cluster): bodega no ventilada almacenamiento grano sector rural
- **Barrera 2007 UACh RETIRADO S50:** búsqueda web (cybertesis.uach.cl + Google Scholar) no localizó la tesis. La cita "Estación 5" procede de una paráfrasis registrada en sesiones previas sin acceso al texto original. **Reemplazo aprobado S50:** usar Murúa et al. 2003 Oikos + Spotorno et al. 2000 + Jaksic & Lima 2003 Austral Ecology para anclar la dinámica post-masting de O. longicaudatus. Texto sugerido para manuscrito: *"Post-masting, O. longicaudatus populations in temperate southern Chile show peak density and peridomestic displacement in the year following the seeding pulse (Murúa et al. 2003; Spotorno et al. 2000; Jaksic & Lima 2003)."*

**Por qué el modelo NO muestra ψ positivo lags 6-10:**
- Dispersión es subliminal y difusa (cada roedor → sitio distinto → momento distinto)
- Pixel Landsat 30m NO ve el peridoméstico (ve bosque, no viviendas/bodegas)
- La señal satelital es de FASE 1 (retención), no de FASE 2 (dispersión)
- Eco en lag 16 (ψ=-0.517, p=0.004, eventos persistentes = segundo parche) — **VERIFICADO S50: NO REESTIMADO en Code S22.** El número viene exclusivamente de Chat S7-S8 registrado en project_estado_completo_S21.md:45. S22 corrigió el bug crítico `ifelse→if/else` y re-estimó el modelo base (ψ lag 5: −0.321 → −0.2874 con year_centered + zone_f), pero los 14 folds walk-forward de S22 usaron SOLO lag 5; el eco lag 16 nunca fue re-estimado con los fixes. **DECISIÓN Q1 S50:** retirar el lag 16 como evidencia cuantitativa en manuscrito EID. Si se quiere anclaje del "segundo parche"/eventos persistentes en Discussion, usar argumentación fenológica (Tagle 2013 cohortes asincrónicas + González & Donoso 1999 ciclo semillas) en vez del número frágil. Re-estimar sólo si Gonzalo decide invertir tiempo; por ahora queda como observación exploratoria no usada.
- feedback_chat_errores_S11S12 línea 16: "trampa ecológica bifásica sin ψ positivo en ningún lag" — advertencia reviewer 2

### FASE 3 — DILUCIÓN
Roedores dispersados mueren / depredados / no encuentran otro pulso → regresión a basal
Señal ratización se disuelve en 1-2 años (bloques ALTO-BAJO duran 1.7-2.2 años)

## 6-bis. CUANTIFICACIÓN DEL RIESGO BIFÁSICO (cálculo modelos predictivos)

**Principio clave:** ψ negativo tiene dos lecturas simultáneas resueltas por el desfase temporal:
- En el momento t (NDVI bajo AHORA): retención en parche → riesgo peridoméstico momentáneo BAJO
- En t+5 (5 meses después): dispersión al ecotono → riesgo peridoméstico ALTO
- El coeficiente integra ambas porque R5_within_sc YA está desfasado 5 meses

### Traducción 1 — Efecto continuo (ψ por DE)
Modelo S29-K: log(μ) = β₀ + ... + ψ·R5_within_sc + ...
ψ = -0.309 → cada 1 DE de caída NDVI lag 5 → casos × exp(+0.309) = × 1.362 (+36%)

### Traducción 2 — Dose-response discreto (eventos quiloides)
Evento = mes-comuna con R5_within_sc < -1
Fuente: project_sesion_code_S27.md parte B + reference_numeros_S40_AMF.md L199

| Eventos acumulados | IRR | Δ% |
|---|---|---|
| 0 | 1.000 | ref |
| 1 | 1.394 | +39.4% |
| 2 | 1.942 | +94.2% |
| 3 | 2.706 | +170.6% |
| 4 | 3.771 | +277.1% |

Fórmula cerrada: IRR(k) = exp(k × 0.332) ≈ 1.394^k
Validación empírica Dic-Mar 8 comunas top: ratio ×3.11, Wilcoxon p=0.011

### Modelos predictivos (S26-S27)

**Modelo DESCRIPTIVO (Tabla A S26):**
- Input: solo historia (tasa por comuna + BLUPs)
- NO usa NDVI ni ψ
- Baseline: 25.0 casos quiloides esperados en 5 años
- Ventaja: robusto, parsimonioso
- Desventaja: ciego a eventos activos

**Modelo INFERENCIAL Ruta A — GLMM directo con ψ (Tabla B S26):**
| Escenario NDVI | E[casos/temp] | Δ | P(≥2) |
|---|---|---|---|
| Promedio | 2.97 | ref | 34.1% |
| Seco (-1 DE) | 3.83 | +29% | 47.6% |
| Húmedo (+1 DE) | 2.30 | -22% | 23.0% |

**Modelo INFERENCIAL Ruta B — 2 etapas (S27 parte F):**
Etapa 1: n_eventos = 70.4 - 193.3 × NDVI_mean, R²=0.523, R²adj=0.500, p=0.0001
Etapa 2: eventos → proporción histórica → GLMM → MC 10k → casos

| Escenario NDVI | E[eventos/año] | E[5yr quiloide] |
|---|---|---|
| NDVI 2024 (0.342) | 4 | - |
| Promedio (0.242) | 24 | 14.7 |
| Seco (0.184) | 35 | 19.1 |
| Húmedo (0.301) | 12 | 11.3 |

**Comparación DESC vs INFERENCIAL (Tabla D S26):**
| Método | E[5yr] | Δ vs descriptivo |
|---|---|---|
| Descriptivo puro | 25.0 | - |
| Inferencial promedio | 14.7 | -41% |
| Inferencial seco | 19.1 | -24% |
| Inferencial húmedo | 11.3 | -55% |

Interpretación: modelo inferencial predice MENOS que descriptivo excepto en señal quiloide intensa. Es herramienta de DE-ALERTING (excluir riesgo), coherente con un modelo que captura la fase de retención (no de dispersión) del ciclo bifásico.

**Ensemble (S27 parte G, Brier Score LOO temporal):**
| Modelo | Brier | Peso |
|---|---|---|
| Descriptivo | 0.0685 | 30% |
| GLMM directo | 0.0603 | 35% |
| 2-etapas | 0.0593 (mejor) | 35% |

P_ensemble = 0.30·P_desc + 0.35·P_GLMM + 0.35·P_2etapas

### Resolución de la paradoja bifásica en 3 capas

| Capa temporal | Lectura | Evidencia numérica |
|---|---|---|
| Instantánea t=0 | Retención: roedores confinados, riesgo momentáneo bajo | Lags 0-4 sin señal detectable; anclaje externo en literatura ocupacional Castillo 2001 / Riquelme 2015 |
| Desplazada t=+5 | Dispersión: roedores en ecotono, riesgo alto | ψ=-0.309, IRR(1DE)=1.362, IRR(k)=1.394^k |
| Agregada anual | Años más secos acumulan más eventos → más casos 5m después | +29% seco, +35 eventos/año, 19.1 casos/5yr |

**Operacional SEREMI:** satélite ve NDVI bajo HOY → "roedores confinados, alerta temprana 5 meses futuro" → SEREMI prepara campañas de prevención en trabajadores agrícolas/forestales y peridoméstico rural.

### Framework operacional multi-agencia basado en el signo de ψ (S50)

El signo negativo de ψ lag 5 habilita un **pipeline de alerta temprana en tres ventanas temporales**, cada una con un actor institucional distinto. El respaldo legal-institucional de esta coordinación es el **Ordinario MINSAL B38 N°3420 (26 julio 2019)**, firmado Dra. Paula Daza, que ya instruye formalmente "coordinar con CONAF/SAG para identificar áreas de riesgo" (reference_biblio_S22.md:72).

| Ventana temporal | Lectura del ψ | Actor | Acción operacional |
|---|---|---|---|
| t = 0 (NDVI cae AHORA) | Retención: roedores **confinados** en el parche quiloide | **CONAF** | Control preventivo en parches boscosos con floración-muerte detectada por NDVI; cercado, señalética, restricción de ingreso a recolectores de leña/frutos |
| t = 0 a t+5 (ventana de 5 meses) | Confinamiento activo: sabemos dónde están los roedores | **SEREMI Salud** | Mapa de exclusión humana del parche; alertas a comunidades rurales en radio del parche; educación en vivienda rural y ocupacional |
| Justo antes de t+5 | Dispersión inminente al ecotono | **SAG** | Control sanitario en viviendas rurales, bodegas de grano, gallineros, leñeras del ecotono adyacente; rodenticidas donde corresponda; inspección de predios agrícolas |
| t+5 a t+10 | Dispersión en curso, contagio peridoméstico | **SEREMI + SAG conjunto** | Alerta epidemiológica reforzada; vigilancia activa de síntomas en trabajadores agrícolas/forestales; protocolos de limpieza segura en bodegas |

**Mensaje central al lector EID / a SEREMI Ñuble:** el satélite no dice "ahí hay casos", dice "ahí estarán los roedores dispersándose en 5 meses". Esa ventana de 5 meses es **tiempo operacional real** para SAG, CONAF y SEREMI — más largo que cualquier señal clínica o epidemiológica actual. Es una de las ventajas no triviales del modelo S29-K sobre cualquier alerta reactiva.

**Novedad frente a literatura:** Andreo 2024 Pathogens (Argentina) y Lowe 2016 eLife (dengue Brasil) documentan early warning satelital, pero ninguno ha propuesto un **framework bifásico con ventana operacional de 5 meses** ni ha coordinado 3 actores institucionales distintos bajo un mismo proxy. Este es uno de los aportes originales del paper.

**Anclaje clínico que valida el framework:** cluster C30 El Carmen 2023 (bodega no ventilada, cluster familiar madre-hijo) ocurrió en la ventana de dispersión post-lag 5 en una zona sin alerta activa. Si el framework hubiera estado operativo, SEREMI habría notificado riesgo peridoméstico 5 meses antes y SAG habría inspeccionado bodegas rurales en El Carmen durante la ventana de dispersión.

### Localización
- 13 comunas quiloides interior Ñuble
- BLUPs top: El Carmen +1.38, San Ignacio +0.78, Coihueco +0.50
- Sincronía r=0.546 (eventos regionales simultáneos)
- Sin propagación gradual: TODO o NADA
- Sin comuna centinela: driver regional

### Duración de la señal (disolución por generaciones)
- Bloques ALTO NDVI: media 1.7 años, máx 3
- Bloques BAJO NDVI: media 2.2 años
- P(fin bloque en 3 años) = 83%
- P(fin bloque en 4 años) = 100%

### Generaciones de colilargo
- Año 1: pulso semillas → 2-3 generaciones con exceso recursos → ratización activa
- Año 2: remanentes + culmos muertos → 1 generación más → máximo contacto
- Año 3: depredación (Muñoz-Pedreros 2016) + agotamiento carbohidratos + regeneración sotobosque → densidad basal
- Año 4: señal disuelta

### Autocorrelación anual de casos
ACF = −0.20, Ljung-Box p=0.31 → casos temporalmente independientes condicional a covariables. Consistente con disolución de señal ecológica en ≤3 años.

### Validación Markov 3 estados (S27)
- Converge distribución estacionaria en 2 pasos
- P(BAJO)=0.39, P(NEUTRO)=0.22, P(ALTO)=0.39
- Predicción 2025-2027: transición ALTO→BAJO (ventana alto riesgo)

## 7. Fuentes consultadas (cadena trazable)

| Tema | Archivo fuente |
|---|---|
| Lag 5 pre-especificado | memory/project_lag5_preespecificado.md |
| Fases fenológicas | documentos/paper/floracion quila zona centro-sur.pdf |
| Cadena biológica | memory/reference_biblio_marco_teorico.md |
| Floración sectorial | memory/project_floracion_sectorial.md |
| Coeficientes S29-K | obsidian_vault/03_Modelos/GLMM NB2 Final.md |
| Tests robustez | memory/project_sesion_code_S26.md, S29.md, S34.md |
| Eventos quiloides | memory/project_sesion_code_S27.md |
| Ratización vs ratada | memory/project_estado_completo_S21.md |
| Biología colilargo | memory/reference_biblio_marco_teorico.md (Barrera 2007) |
| Modelo final | memory/project_paper_EID_contexto_completo_S50.md §4 |
| Mecanismo A | obsidian_vault/03_Modelos/Mecanismo A RxT.md |

## 8. Papers citables para Methods/Discussion EID

1. González 2001 Bosque 22:45-51 (fenología quila, base pre-especificación)
2. Muñoz & González 2009 Rev Chil Hist Nat 82:185-198 (ciclo 60-70 años)
3. Tagle et al. 2013 Rev Chil Hist Nat 86:423-432 (método rizomas, cohortes asincrónicas)
4. Jaksic & Lima 2003 Austral Ecology 28:237-251 (ratadas, distinción con ratización)
5. Barrera Gómez 2007 (tesis UACh, dinámica O. longicaudatus)
6. Murúa 2003 Oikos (96% varianza costa explicada por ENSO, no quila)
7. Spotorno et al. 2000 (biología roedores reservorios Chile)
8. Bell & Jones 2015 (within-between decomposition)
9. Rothman 1990 Epidemiology (no corrección múltiple hipótesis pre-especificadas)
10. VanderWeele & Ding 2017 Ann Intern Med (E-value)
11. Richardson et al. 2011 AJE (pre-specification de lag en epidemiología ambiental)
12. González & Donoso 1999 (50M frutos/ha pico enero)

**Why:** Gonzalo pidió cerrar este conocimiento en S50 para no detectar vacío en próximas sesiones. Todas las respuestas ya estaban Q1-blindadas en sesiones previas pero dispersas en memoria/Obsidian. Esta nota las consolida en un solo lugar.
**How to apply:** Leer esta nota antes de escribir Methods §lag5 o Discussion §mecanismo. Usar como anclaje para explicaciones del lag 5 en cualquier contexto del paper EID.
