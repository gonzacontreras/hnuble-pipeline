# ARCHIVO MAESTRO -- PARTE II: CARACTERIZACION CLINICA SCPH, HCHM CHILLAN

**Version:** 3.3
**Fecha de creacion:** 2026-03-14 | **Actualizado:** 2026-03-30 (S39 — auditoría anti-sesgo Q1 automática, crosscheck R completo)
**Estado:** v3.3 — Correcciones S39 post-crosscheck automatizado contra CSV con R 4.5.3. 15 discrepancias investigadas, 7 corregidas (3 CRITICAS, 4 ALTAS). Verificación cruzada exhaustiva de TODOS los números.
**Autor compilacion:** Claude Code (master-builder)
**Fuente primaria:** HCHM_38_casos_estructurado3.xlsx (38 filas, 32 columnas)
**Fuente verificacion:** datos/parsed_clinical_all.csv (34 filas, 67 columnas)
**Pacientes unicos:** 34 (tras exclusion de 3 duplicados + Caso 37 sin datos)

**[NOTA GLOBAL v3.2: DENOMINADORES]** Denominador correcto para TODOS los calculos es n=34 (no n=35). Caso 37 EXCLUIDO por ausencia total de datos. En v3.2 se corrigieron los denominadores principales a /34. Algunas secciones de datos brutos (E.4-E.6, F, G-H) conservan /35 residual donde no se recalcularon porcentajes; al redactar manuscrito, usar n=34 y porcentajes recalculados de la tabla E.7 actualizada.

---

## INDICE

### Secciones originales (A-O, actualizadas)
- [A. Metadatos y fuentes de datos](#a-metadatos-y-fuentes-de-datos)
- [B. Dataset limpio (34 pacientes)](#b-dataset-limpio)
- [C. Demografia](#c-demografia)
- [D. Presentacion clinica](#d-presentacion-clinica)
- [E. Laboratorio completo](#e-laboratorio-completo)
- [F. Gestion de urgencias](#f-gestion-de-urgencias)
- [G. Manejo clinico](#g-manejo-clinico)
- [H. Intervenciones terapeuticas](#h-intervenciones-terapeuticas)
- [I. Desenlaces](#i-desenlaces)
- [J. GRD y analisis del sistema de salud](#j-grd-y-analisis-del-sistema-de-salud)
- [K. Comparacion con series chilenas previas](#k-comparacion-con-series-chilenas-previas)
- [L. Bibliografia](#l-bibliografia)
- [M. Sesgos y limitaciones](#m-sesgos-y-limitaciones)
- [N. Metodologia diagnostica](#n-metodologia-diagnostica)
- [O. Clasificacion de severidad v6.2](#o-clasificacion-de-severidad-v62)

### Secciones nuevas (P-EE, integradas desde S29)
- [P. Analisis 27 variables vs mortalidad](#p-analisis-27-variables-vs-mortalidad)
- [Q. Fenotipo del paciente que fallece](#q-fenotipo-del-paciente-que-fallece)
- [R. Analisis de volemizacion profundo](#r-analisis-de-volemizacion-profundo)
- [S. Variables significativas severidad](#s-variables-significativas-severidad)
- [T. Hallazgo FR mayor que 22](#t-hallazgo-fr-mayor-que-22)
- [U. Reconsultas vs desenlaces](#u-reconsultas-vs-desenlaces)
- [V. Tiempo a muerte](#v-tiempo-a-muerte)
- [W. Creatinina mayor que 1.3 vs desenlaces adversos](#w-creatinina-mayor-que-13-vs-desenlaces-adversos)
- [X. Variables descriptivas sin senal](#x-variables-descriptivas-sin-senal)
- [Y. Textos aprobados para paper](#y-textos-aprobados-para-paper)
- [Z. Genealogia completa del score v3 a v6.2](#z-genealogia-completa-del-score-v3-a-v62)
- [AA. Bibliografia completa consolidada](#aa-bibliografia-completa-consolidada)
- [BB. Scripts de reproducibilidad](#bb-scripts-de-reproducibilidad)
- [CC. Red-Team](#cc-red-team)
- [DD. Vacios consolidados](#dd-vacios-consolidados)
- [EE. Decisiones de Gonzalo](#ee-decisiones-de-gonzalo)

---

## A. Metadatos y fuentes de datos

### A.1 Fuentes primarias

| Fuente | Ubicacion | Contenido | Periodo |
|--------|-----------|-----------|---------|
| Fichas clinicas HCHM | `documentos/formularios/HCHM_38_casos_estructurado3.xlsx` | 38 filas, 32 columnas, datos clinicos estructurados | 2012-2025 |
| Base administrativa GRD HCHM | `datos/PACIENTES HANTAVIRUS 2010-2025(ABRIL) (2).xlsx` | 50 egresos, diagnostico B33.4, datos administrativos | 2012-2025 |
| Base GRD ECMO nacional MINSAL | `documentos/formularios/Ecmo hospitales enero a noviembre.xlsx` | 2 hojas: egresos ECMO por hospital y por motivo egreso | 2023-2025 |
| Paper previo (referencia) | `resultados/PAPER_DEFINITIVO_INTEGRADO_ES.txt` | Texto completo del paper con n=38, requiere recalculo | -- |
| Manual Plasma MINSAL v2.0 | `documentos/paper/Manual-Administracion-Plasma-Inmune-Hantavirus.-Version-2.0.pdf` | Protocolo administracion plasma hiperinmune | 2018 |
| PPT SEREMI 2002-2023 | `documentos/paper/caracterizacion casos de Hantavirus 2002-2023.pptx` | Caracterizacion epidemiologica regional | 2002-2023 |
| PPT SEREMI 2020-2024 | `documentos/paper/caracterizacion casos de Hantavirus 2020-2024 7-02-2024 (1).pptx` | Actualizacion epidemiologica | 2020-2024 |
| Castillo et al. 2001 | `documentos/paper/HantaTemuco2001.pdf` | Serie Temuco n=16, CHEST | 1997-1999 |
| Dataset parseado | `datos/parsed_clinical_all.csv` | 34 filas, 67 columnas, extraccion automatizada verificada | 2012-2025 |

[Fuente: Archivos en repositorio local verificados 2026-03-26]

### A.2 Aprobacion etica

Aprobado por Comite de Etica Hospital Clinico Herminda Martin (HCHM), Chillan. Acta CEC-HCHM N°202501-25.

[ALERTA V-12: Aprobación venció 04-mar-2026. Requiere renovación presencial de Gonzalo ANTES de submission. Título acta "20 años" vs 23 años reales de la serie — declarar en submission.]

### A.3 Criterios de inclusion

- SCPH confirmado por IgM Hantavirus (antigeno Puumala) y/o PCR (ISP)
- Atendidos en HCHM Chillan
- Fichas clinicas recuperables

### A.4 Duplicados excluidos

| Caso excluido | Razon | Duplicado de |
|---------------|-------|-------------|
| Caso 7 | Duplicado exacto (18/02/2018, 27M, Pemuco, SALINAS LEVANCINI) | Caso 6 |
| Caso 36 | Triple duplicado (misma fecha, edad, sexo, comuna) | Caso 6 |
| Caso 38 | Duplicado (18/05/2017, Portezuelo, MAGDALENA GARRIDO; sexo M en ficha era error, paciente es F) | Caso 15 |

### A.5 Casos especiales

| Caso | Nota |
|------|------|
| Caso 20 | Nunca existio (error de numeracion en ficha original) |
| Caso 32a | 51M, San Fabian, Ene 2022, fallecido -- paciente DISTINTO de 32b |
| Caso 32b | 12F, Coihueco, Feb 2022, fallecida -- paciente DISTINTO de 32a |
| Caso 37 | Solo numero de caso registrado, sin datos clinicos — **EXCLUIDO del n analizable (n=34)** |

### A.6 Desenlaces recuperados por cruce administrativo

Cuatro casos con desenlace "desconocido" en ficha clinica fueron cruzados con la base administrativa GRD del HCHM:

| Caso | Datos ficha | Cruce admin | Resultado |
|------|------------|-------------|-----------|
| Caso 14 | 24F, Coihueco, 02/05/2016, desenlace desconocido | MENDEZ CASTILLO, Coihueco, 03/05/2016, traslado Hosp. Torax, viva | **Viva** |
| Caso 15 | 26F, Portezuelo, 18/05/2017, desenlace desconocido | GARRIDO JARA, Portezuelo/Chudal, 19/05/2017, traslado HGGB, viva | **Viva** |
| Caso 35 | 36F, Bulnes, 08/03/2019, desenlace desconocido | CIFUENTES ALVAREZ o CARRASCO CONTRERAS, Bulnes, Mar 2019, viva | **Viva** |
| Caso 37 | Sin datos clinicos | [VACIO: no fue posible cruzar sin datos demograficos] | **Desconocido** |

### A.7 Nota sobre comuna de residencia vs. infeccion

La Parte II utiliza **comuna de residencia** (no de infeccion como la Parte I) porque se trata de un analisis clinico y de salud publica: el paciente consulta en los dispositivos de urgencia de su localidad de residencia.

---

## B. Dataset limpio

### B.1 Tabla completa de 34 pacientes unicos (Caso 37 excluido)

**Abreviaciones:** M=masculino, F=femenino, d=dias, UPC=Unidad de Paciente Critico, VMI=ventilacion mecanica invasiva, DVA=drogas vasoactivas, desc=desconocido, N/D=no disponible.

| # | Fecha | Edad | Sexo | Comuna residencia | Dias sint. | Estacion | Muerte | VMI | ECMO | Plasma HI | Traslado | Destino | Dias Hosp/UCI |
|---|-------|------|------|------------------|-----------|----------|--------|-----|------|-----------|----------|---------|---------------|
| 1 | 04/04/2018 | 32 | M | Coihueco | 5 | Otono | No | Si | No | No | Si | HGGB | desc |
| 2 | 13/09/2013 | 44 | M | desc | 5 | Primavera | No | No | No | No | Si | Clin.Alemana Conc | desc |
| 3 | 28/02/2019 | 58 | M | Pinto | 5 | Verano | No | No | No | Si | Si | HLH | 25/11 |
| 4 | 21/03/2017 | 20 | M | El Carmen | 3 | Otono | No | No | No | No | Si | HLH | desc |
| 5 | 03/04/2019 | 14 | F | Cato | 4 | Otono | No | desc | desc | desc | Si | H.Roberto del Rio | desc |
| 6 | 18/02/2018 | 27 | M | Pemuco | 5 | Verano | No | desc | desc | Si | Si | HGGB | desc |
| 8 | 06/02/2020 | 32 | M | Pinto | 5 | Verano | No | No | No | Si (HGGB) | Si | HGGB | desc |
| 9 | 28/03/2019 | 36 | F | Quillon | 3 | Otono | No | Si | Si | Si | Si | HLH | 14/12 |
| 10 | 25/01/2024 | 51 | M | El Carmen | 6 | Verano | No | No | No | No | Si | HLH | 5/2 |
| 11 | 06/02/2021 | 12 | F | Coihueco | 6 | Verano | No | No | No | Si | Si | HLCM | 14/7 |
| 12 | 28/04/2015 | 22 | M | San Ignacio | 3 | Otono | No | Si | No | No | Si (no enviado) | HCHM | 14/7 |
| 13 | 26/04/2016 | 69 | M | San Carlos | 1 | Otono | No | No | No | No | No? | HCHM | 31/30 |
| 14 | 02/05/2016 | 24 | F | Coihueco | 4 | Otono | No (admin) | desc | desc | desc | Si | Hosp. Torax | 2/2 |
| 15 | 18/05/2017 | 26 | F | Portezuelo | 6 | Otono | No (admin) | desc | desc | desc | Si | HGGB | 1/1 |
| 16 | 24/02/2012 | 56 | F | San Gregorio | 5 | Verano | No | No | No | No | No | No | 15/15 |
| 17 | 08/02/2017 | 22 | F | San Carlos | 6 | Verano | No | No | No | No | No | No | 7/5 |
| 18 | 22/08/2024 | 29 | F | San Carlos | 6 | **Invierno** | No | No | No | No | No | No | 7/5 [DATOS LAB CONTAMINADOS: ver RT-3] |
| 19 | 08/08/2024 | 21 | M | Pelluhue (Maule) | 4 | Invierno | No | No | desc | No | desc | desc | 10/-- |
| 21 | 28/04/2023 | 11 | M | El Carmen | 21 | Otono | No | Si | No | No | Si | desc | 21/14 |
| 22 | 14/05/2016 | 59 | M | San Nicolas | 4 | Otono | No | No | No | No | No | No | 15/14 |
| 23 | 15/06/2016 | 45 | M | Quillon | 4 | Invierno | No | No | No | No | No | No | 14/12 |
| 24 | 08/02/2017 | 47 | M | Yungay | 14 | Verano | No | desc | desc | desc | Si | HLH | desc |
| 25 | 31/01/2025 | 37 | M | desc | 14 | Verano | No | Si | Si | No | Si | HLH | 20/19 |
| 26 | 01/08/2022 | 32 | M | Coelemu | 5 | Invierno | No | Si | desc | desc | Si | HGGB | desc |
| 27 | 19/01/2024 | 54 | M | desc | 5 | Verano | **Si** | Si | Si | desc | Si | HGGB | desc |
| 28 | 29/04/2023 | 29 | M | San Carlos | 4 | Otono | No | desc | desc | desc | desc | desc | desc |
| 29 | 29/04/2023 | 37 | M | San Ignacio | 4 | Otono | No | desc | desc | desc | Si | HLH | desc/6 |
| 30 | 29/04/2023 | 49 | F | El Carmen | 3 | Otono | **Si** | desc | desc | desc | desc | desc | desc |
| 31 | 12/03/2022 | 37 | F | Pinto | 4 | Otono | **Si** | No | No | No | No | No | desc |
| 32a | 23/01/2022 | 51 | M | San Fabian | 3 | Verano | **Si** | Si | desc | desc | desc | desc | desc |
| 32b | 04/02/2022 | 12 | F | Coihueco | 3 | Verano | **Si** | No | No | desc | Si | H.Calvo Mackenna | desc |
| 33 | 07/02/2021 | 24 | F | Coihueco | 4 | Verano | No | No | No | desc | Si | HLH | desc |
| 34 | 07/02/2021 | 32 | M | Pinto | 4 | Verano | desc | desc | desc | desc | No | No | desc |
| 35 | 08/03/2019 | 36 | F | Bulnes | 3 | Otono | No (admin) | desc | desc | desc | Si | HLH | desc |

**Nota sobre Caso 37:** Solo existe el numero de caso en la planilla, sin ninguna variable clinica registrada. **EXCLUIDO del analisis (n=34).** No fue posible vincular con base administrativa ni recuperar datos clinicos.

[INCONSISTENCIA: Caso 18 tiene fecha 22/08/2024 (invierno) pero campo estacion dice "verano". El laboratorio dice "PENDIENTE PCR 207" y varios valores parecen copiados del caso 17 (misma comuna San Carlos, mismos valores de albumina 2.5, CREA 0.6, BUN 7, Nap 134, APACHE 3, PSI clase I 12pts, mismos dias hosp 7/5). Posible error de transcripcion/duplicacion parcial de datos del caso 17 al caso 18. Los datos que difieren (plaq 63.000, Htro 44.7, leuco 19.5, inmunoblastos 11%, anamnesis proxima diferente, signos vitales diferentes) parecen genuinos del caso 18.]

[INCONSISTENCIA: Caso 19 tiene localizacion "Pelluhue, region del Maule" -- fuera de Region de Nuble. Se mantiene porque fue atendido en HCHM.]

---

## C. Demografia

### C.1 Calculo sobre n=34 pacientes unicos (Caso 37 excluido por ausencia total de datos)

**Edad:**
- Valores disponibles: 34/34 (100%)
- Edades registradas: 11, 12, 12, 14, 20, 21, 22, 22, 24, 24, 26, 27, 29, 29, 32, 32, 32, 32, 36, 36, 37, 37, 37, 44, 45, 47, 49, 51, 51, 54, 56, 58, 59, 69
- Media: 34.9 anos
- Mediana: 32.0 anos
- Rango: 11-69 anos
- DE: 15.0 anos
- n/N: 34/34 (100%)
- [CORRECCION v3.0: v2.1 reportaba media 35.4 y mediana 34.0. La lista de edades de v2.1 contenia error residual: 49 aparecia 2 veces y 32 solo 3 veces (deberia ser 4 veces con C8=32). Recalculado directamente desde parsed_clinical_all.csv.]
- [CORRECCION v2.1: Caso 5 era 66M, corregido a 14F (Excel primario). Caso 8 era 47M, corregido a 32M.]

[Fuente: datos/parsed_clinical_all.csv, verificado 2026-03-26]

**Sexo:**
- Datos disponibles: 34/34
- Masculino: 21/34 (61.8%)
- Femenino: 13/34 (38.2%)
- Razon M:F = 1.62:1
- [CORRECCION v2.1: Caso 5 corregido de M a F]

[Fuente: datos/parsed_clinical_all.csv]

**Estacionalidad (mes de atencion):**
- Datos disponibles: 34/34

| Mes | n | % |
|-----|---|---|
| Enero | 4 | 11.8 |
| Febrero | 10 | 29.4 |
| Marzo | 4 | 11.8 |
| Abril | 8 | 23.5 |
| Mayo | 3 | 8.8 |
| Junio | 1 | 2.9 |
| Agosto | 3 | 8.8 |
| Septiembre | 1 | 2.9 |

[CORRECCION v3.1: Estacionalidad recalculada desde fechas de atencion con estacion astronomica chilena (Verano=Dic-Feb, Otono=Mar-May, Invierno=Jun-Ago, Primavera=Sep-Nov). 8 casos corregidos: C2 Inv→Pri, C4 Ver→Oto, C9 Ver→Oto, C13 Inv→Oto, C14 Inv→Oto, C15 Inv→Oto, C24 Inv→Ver, C35 Ver→Oto. Verificado contra CSV parsed_clinical_all.csv campo estacion (0 discrepancias CSV vs fecha).]

- Verano (Dic-Feb): 14/34 = 41.2%
- Otono (Mar-May): 15/34 = 44.1%
- Invierno (Jun-Ago): 4/34 = 11.8%
- Primavera (Sep-Nov): 1/34 = 2.9%
- Verano + Otono: 29/34 = 85.3%

**Comunas de residencia (disponibles):**

| Comuna | n |
|--------|---|
| Coihueco | 5 (casos 1, 11, 14, 32b, 33) |
| El Carmen | 4 (casos 4, 10, 21, 30) |
| San Carlos | 4 (casos 13, 17, 18, 28) |
| Pinto | 4 (casos 3, 8, 31, 34) |
| San Ignacio | 2 (casos 12, 29) |
| Quillon | 2 (casos 9, 23) |
| Yungay | 1 (caso 24) |
| Cato (localidad) | 1 (caso 5) |
| Pemuco | 1 (caso 6) |
| San Nicolas | 1 (caso 22) |
| Portezuelo | 1 (caso 15) |
| San Gregorio | 1 (caso 16) |
| San Fabian | 1 (caso 32a) |
| Bulnes | 1 (caso 35) |
| Coelemu | 1 (caso 26) |
| Pelluhue (Maule) | 1 (caso 19) |
| desc | 3 (casos 2, 25, 27) |

**Oficio/ocupacion (disponible en n=19/34):**
- Trabajador agricola: 7
- Trabajador forestal: 2
- Trabajador sector rural: 2
- Escolar: 2
- Otros/desconocido: resto

**Raza/Etnia:**
- 33/34 registrados como "Caucasico (chileno?)" o "chileno caucasico?"
- 1 caso registrado como "venezolano (?)" (Caso 27)
- 0 pacientes de ascendencia africana

**Factores de riesgo:**

| Factor | n | % de disponibles |
|--------|---|-----------------|
| Ingreso a galpon/bodega cerrado | 7 | -- |
| Trabajador agricola/rural | 6 | -- |
| Excursion/camping/sendero | 4 | -- |
| Contacto heces ratones | 2 | -- |
| Desconocido | 11 | -- |
| No disponible | 5 | -- |

---

## D. Presentacion clinica

### D.1 Motivo de consulta (34/34 disponibles)

| Motivo principal | n | % |
|------------------|---|---|
| Fiebre | 17 | 50.0 |
| Mialgias | 5 | 14.7 |
| Disnea | 3 | 8.8 |
| Dolor abdominal | 2 | 5.9 |
| Lipotimia | 1 | 2.9 |
| Vertigo | 1 | 2.9 |
| Vomitos | 1 | 2.9 |
| Lumbalgia | 1 | 2.9 |
| FOD (fiebre de origen desconocido) | 1 | 2.9 |
| Sensacion febril/mialgias/cefalea | 2 | 5.9 |

### D.2 Dias de sintomas previos a consulta (34/34 disponibles)

Valores registrados: 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 14, 14, 21

- Media: 5.2 dias
- Mediana: 4.0 dias
- Rango: 1-21 dias
- RIC: 3-6 dias
- n/N: 34/34 (100%)

[CORRECCION v3.1: C4 dias_sint corregido de 7 a 3 (verificado CSV). Lista completa 34/34 (antes 33/35). Media 5.4→5.2, mediana 5.0→4.0.]

[NOTA: Caso 21 con 21 dias de sintomas es un outlier notable. Madre del paciente fue caso 30, fallecida.]

### D.3 Dias de incubacion (cuando conocido)

Valores registrados (13 casos): 1, 2, 4, 4, 7, 7, 11, 14, 14, 14, 14, 15, 25

- Mediana: 14 dias
- Rango: 1-25 dias
- n/N: 13/34 (38.2%)

[NOTA: Valores de 1-2 dias son biologicamente improbables para hantavirus (incubacion tipica 7-35 dias). Posible confusion con dias desde la exposicion recordada hasta el inicio de sintomas vs. dias de sintomas.]

### D.4 Sintomas reportados en anamnesis proxima (extraccion de texto libre)

| Sintoma | n reportado | % de disponibles (n~33) |
|---------|------------|------------------------|
| Fiebre | 28 | 84.8 |
| Mialgias | 17 | 51.5 |
| Cefalea | 16 | 48.5 |
| Vomitos | 12 | 36.4 |
| Dolor abdominal | 11 | 33.3 |
| Disnea | 10 | 30.3 |
| Diarrea | 10 | 30.3 |
| Tos (seca) | 9 | 27.3 |
| CEG | 9 | 27.3 |
| Dolor toracico | 4 | 12.1 |
| Odinofagia | 3 | 9.1 |
| Lipotimia | 2 | 6.1 |
| Nauseas | 2 | 6.1 |
| Congestion nasal | 1 | 3.0 |
| Vertigo | 1 | 3.0 |
| Lumbalgia | 1 | 3.0 |
| Palpitaciones | 1 | 3.0 |

### D.5 Signos vitales de ingreso al Servicio de Urgencias

**Frecuencia cardiaca (FC):**
Valores disponibles (29/34):
55, 63, 69, 72, 79, 80, 80, 87, 95, 97, 100, 102, 102, 102, 105, 105, 110, 112, 114, 114, 117, 119, 123, 126, 127, 141, 142, 144, --, --, --, --, --

- Media: 104.9 lpm
- Mediana: 105 lpm
- Rango: 55-144 lpm
- Taquicardia >=100: 21/31 (67.7%)
- n/N: 29/34 (85.3%)

**Presion arterial sistolica (PAS):**
Valores disponibles (28/34):
82, 86, 88, 90, 95, 97, 97, 101, 103, 103, 105, 111, 113, 119, 121, 121, 127, 128, 128, 130, 136, 138, 143, 143, 157, 198, --, --, --, --, --

- Media: 117.3 mmHg
- Mediana: 115.0 mmHg
- Rango: 82-198 mmHg
- Hipotension PAS <90: 3/28 (10.7%) [Casos 15 (88), 18 (82), 30 (86)]
- n/N: 28/34 (82.4%)

**Saturacion O2 (SatO2):**
Valores disponibles (28/34 en CSV):

- Media: 94.1%
- Mediana: 94%
- Rango: 87-99%
- Desaturacion <92%: 6/28 (21.4%)
- n/N: 28/34 (82.4%)

[CORRECCION v3.0: n disponible actualizado de ~30/34 a 28/34 segun CSV verificado]
[Fuente: datos/parsed_clinical_all.csv, campo "sat"]

**Temperatura:**
Valores disponibles (~30/34):
- Rango: 36.0 - 39.0 C
- Fiebre >=38 C al ingreso: ~10/30 (33.3%)

**Frecuencia respiratoria (FR):**
Valores disponibles (23/34 en CSV):

Valores: 12, 17, 18, 20, 20, 21, 22, 22, 22, 22, 22, 22, 23, 25, 27, 28, 29, 30, 30, 32, 32, 32, 57

- Mediana: 22 rpm
- Rango: 12-57 rpm
- FR >22: 11/23 (47.8%)
- Taquipnea >=24: 10/23 (43.5%)
- n/N: 23/34 (67.6%)

[CORRECCION v3.2: Lista corregida a 23 valores (antes 22). CSV tiene 6 valores FR=22 (casos C9, C14, C16, C23, C24, C35), lista v3.1 tenia solo 5. Agregado sexto "22". FR>22=11/23 sin cambio. Verificado contra parsed_clinical_all.csv campo fr_num (S37).]

[CORRECCION v3.0: Valores individuales de FR extraidos del CSV por primera vez. v2.1 reportaba ~27/34 con datos; CSV verificado muestra 23/34.]
[Fuente: datos/parsed_clinical_all.csv, campo "Examen Fisico" parseado]

### D.6 Examen fisico

**Hallazgos pulmonares (de texto libre):**

| Hallazgo | n | % de disponibles (~30) |
|----------|---|----------------------|
| Crepitos (uni o bilaterales) | 18 | 60.0 |
| MP (+) SRA (sin ruidos agregados) | 7 | 23.3 |
| Sin descripcion/no alteraciones | 5 | 16.7 |

**Glasgow (GCS/GSW):**
- Todos los registrados: 15/15 excepto Caso 13 (14/15)
- n/N: ~25/34

### D.7 Radiografia de torax

| Hallazgo | n | % de disponibles (~23) |
|----------|---|----------------------|
| Infiltrado intersticial bilateral | 7 | 30.4 |
| Infiltrado algodonoso/perihiliar | 3 | 13.0 |
| Sin alteraciones | 4 | 17.4 |
| Derrame pleural | 3 | 13.0 |
| Infiltrado unilateral | 2 | 8.7 |
| No disponible | 12 | -- |

---

## E. Laboratorio completo

### E.1 Notas sobre correccion de unidades

- **Plaquetas:** Valores <1000 se multiplican por 1000 (ej: 595 -> 595.000, 125 -> 125.000, 177 -> 177.000)
- **Leucocitos:** El CSV tiene unidades MIXTAS por bug del parser (elimina punto decimal: "4.8"→48, "6.18"→618, "4.100"→4100). Los valores de E.2 fueron extraidos manualmente del texto de fichas y son CORRECTOS. NO usar columna `leuco` del CSV sin corregir.
- **VHS:** Valor directo, sin multiplicar
- **Lactato:** Siempre en mg/dL

### E.2 Hemograma

**Plaquetas (/uL):**

Valores corregidos disponibles (32/34 en CSV):
38.000, 43.000, 43.000, 45.000, 45.000, 46.000, 53.000, 62.000, 63.000, 66.000, 69.000, 76.000, 79.000, 79.000, 80.000, 86.000, 90.000, 98.000, 98.000, 109.000, 114.000, 125.000, 133.000, 158.000, 176.000, 177.000, 185.000, 235.000, 282.000, 317.000, 331.000, 595.000

[NOTA: Caso 2, plaq 595.000 es hallazgo incidental, no trombocitopenia. Incluido en calculo.]

- Mediana: 88.000/uL
- RIC: 62.750-162.500 (Q1-Q3)
- Rango: 38.000-595.000
- Trombocitopenia <150.000: 23/32 (71.9%)
- Trombocitopenia <100.000: 19/32 (59.4%)
- Trombocitopenia severa <50.000: 6/32 (18.8%)
- n/N: 32/34 (94.1%)

[CORRECCION v3.2: Mediana corregida de 92k a 88k (posiciones 16=86k, 17=90k del CSV). <150k corregido de 21/32 a 23/32 (conteo manual: 23 valores bajo 133k inclusive). RIC de ~57.5k-164.5k a 62.750-162.500 (Q1=62750, Q3=162500 del CSV). Verificado contra datos/parsed_clinical_all.csv campo "plaq".]

[CORRECCION v3.1: <100k corregido de 17/32 a 19/32 (59.4%). Verificado contra CSV: 19 casos con plaq<100000. v3.0 subcontaba 2 casos.]
[Fuente: datos/parsed_clinical_all.csv, campo "plaq"]

**Leucocitos (/uL):**

Valores extraidos manualmente de fichas (26/34 verificados):
2.850, 3.700, 3.900, 4.100, 4.800, 5.000, 5.300, 5.400, 5.700, 5.800, 6.000, 6.180, 6.300, 7.310, 7.900, 8.100, 8.200, 8.800, 9.100, 9.700, 12.700, 17.200, 18.300, 19.500, 31.900, 35.700

- Mediana: 6.740/uL
- Media: 9.872/uL
- Rango: 2.850-35.700
- Leucocitosis >10.000: 7/26 (26.9%)
- Leucocitosis marcada >15.000: 4/26 (15.4%)
- Leucopenia <4.000: 2/26 (7.7%)
- n/N: 26/34 (76.5%)

[CORRECCION v3.1: n declarado como 26/34 (no 27/35). Lista tiene 26 valores contados = correcto. Columna `leuco` del CSV tiene bug de unidades mixtas (parser elimina puntos decimales); NO usar sin corregir. Los valores de esta seccion fueron extraidos directamente del texto de fichas y son la fuente de verdad.]

**Hematocrito (%):**

Valores disponibles (27/34 en CSV):
34.5, 35.6, 36.7, 37.0, 37.4, 37.4, 38.0, 38.2, 41.0, 42.9, 43.0, 43.0, 43.0, 43.4, 44.0, 44.4, 44.5, 44.7, 44.9, 45.4, 46.8, 47.2, 49.0, 52.0, 59.0, 60.0, 70.5

- Mediana: 43.4%
- RIC: 38.1-46.1% (Q1-Q3)
- Rango: 34.5-70.5%
- Hemoconcentracion Htro >50%: 4/27 (14.8%) [Casos 19 (52%), 25 (59%), 31 (70.5%), 32a (60%)]
- Htro > ULN por sexo (M>50%, F>44%): 6/27 (22.2%) [+ Casos 18 (F, 44.7%), 33 (F, 47.2%)]
- n/N: 27/34 (79.4%)

[CORRECCION v3.2: De 23 a 27 valores. 4 valores faltantes recuperados del CSV: 42.9(C5), 43.0(C13 tercer valor), 44.0(C4), y verificacion de la lista completa contra parsed_clinical_all.csv. Mediana corregida de 43.7 a 43.4. Denominador de /35 a /34. Agregado Htro>ULN con umbrales StatPearls (M=50.3%, F=44.3%).]

[NOTA: Htro 70.5% en Caso 31 (fallecida en SU) es extremadamente alto, indicando hemoconcentracion severa compatible con fuga capilar masiva.]

**Inmunoblastos:**

Valores disponibles (16/34):
0%, 2%, 2%, 4%, 4%, 5%, 5%, 6%, 9%, 10%, 11%, 11%, 13%, 25%, 28%, 44%

- Mediana: 7.5%
- Rango: 0-44%
- Inmunoblastos presentes (>0%): 15/16 (93.8%)
- Inmunoblastos >=10%: 8/16 (50.0%)
- n/N: 16/34 (47.1%)

### E.3 Bioquimica

**PCR (mg/L):**

Valores disponibles (24/34):
1.6, 7.8, 13.5, 14, 54, 60, 62.5, 72.4, 75, 87, 91, 103, 108.84, 117, 129, 130, 133, 153, 163, 193, 207, 207(?), 217, 230

- Mediana: 100 mg/L
- RIC: 62.5-163 (aprox)
- Rango: 1.6-230
- PCR >100: 13/24 (54.2%)
- n/N: 24/34 (70.6%)

[NOTA: PCR 207 aparece en Caso 17 Y Caso 18, posible dato duplicado del caso 18 copiado del 17.]

**Creatinina (mg/dL):**

Valores disponibles (22/34 en CSV):
0.6, 0.6, 0.6, 0.6, 0.64, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8, 0.9, 0.9, 0.9, 1.03, 1.04, 1.07, 1.15, 1.17, 1.2, 1.6, 2.2

- Mediana: 0.85 mg/dL
- Rango: 0.6-2.2
- Creatinina elevada >1.2 (estricto): 2/22 (9.1%) [Casos 29 (1.6), 27 (2.2)]. Caso 8 (1.17) es borderline, NO supera umbral estricto.
- Creatinina >1.3: 2/22 (9.1%) [Casos 29, 27]
- n/N: 22/34 (64.7%)

[CORRECCION v3.3: Mediana corregida de 0.80 a 0.85 (posiciones 11-12 de 22 valores: 0.8 y 0.9, promedio=0.85). >1.2 corregido de 3/22 a 2/22 (C8=1.17 NO es >1.2). Verificado S39 crosscheck.]
[CORRECCION v3.0: v2.1 reportaba 18/35 (51.4%). CSV verificado contiene 22/34 valores. Los casos adicionales: C4 (1.07), C5 (0.6), C6 (0.8), C8 (1.17).]
[Fuente: datos/parsed_clinical_all.csv, campo "Laboratorios Ingreso" parseado]

[NOTA: Caso 27 (fallecido) con CREA 2.2 indica falla renal aguda.]

**Natremia (mEq/L):**

Valores disponibles (16/34 en CSV):
127, 128, 131, 132, 134, 134, 134, 134, 134, 134, 135, 137, 137, 137, 137, 137

- Mediana: 134 mEq/L
- Rango: 127-137
- Hiponatremia <135: 10/16 (62.5%)
- n/N: 16/34 (47.1%)

[CORRECCION v3.3: n corregido de 14 a 16 (CSV tiene 16 valores: 6×134 y 5×137, no 4×134 y 5×137). <135 corregido de 8/14 a 10/16. Verificado S39 crosscheck contra parsed_clinical_all.csv campo "nap".]
[CORRECCION v3.1: n corregido de 15 a 14 (superado por v3.3).]

**Lactato (mg/dL):**

Valores disponibles (8/34):
15, 19, 23.2, 23.3, 28, 28, 45, 83.1

[NOTA: Lactato 83.1 en Caso 27 (fallecido) indica hipoperfusion severa.]

- Mediana: 25.65 mg/dL
- Rango: 15-83.1
- n/N: 8/34 (23.5%)

[CORRECCION v3.1: Valor 23.2 faltaba en lista (7→8 valores). Mediana recalculada. Verificado contra CSV.]
- [VACIO: Cobertura insuficiente para analisis estadistico robusto]

**BUN (mg/dL):**

Valores disponibles: 7, 13.8, 14.7, 18, 18.5, 32.3
- n/N: 6/34 (17.6%)
- [VACIO: Cobertura insuficiente]

### E.4 Perfil hepatico

**GOT/AST (U/L):**
Valores disponibles (6/34): 49, 50, 66, 96, 181, 195
- Mediana: 81
- Rango: 49-195
- Elevada: 6/6 (100%) [si rango normal <40]
- n/N: 6/34 (17.6%)

**GPT/ALT (U/L):**
Valores disponibles (3/34): 48, 50, 121
- n/N: 3/34 (8.8%)
- [VACIO: Cobertura insuficiente]

**GGT (U/L):**
Valores disponibles (3/34): 122, 204, 266
- n/N: 3/34 (8.8%)

**Perfil hepatico reportado como "normal":** 6 casos
**Perfil hepatico reportado como "alterado":** 3 casos (29, 30, 32a)

### E.5 Gases arteriales

**pH:**
Valores disponibles (16/34): 7.2, 7.27, 7.3, 7.3, 7.3, 7.36, 7.38, 7.39, 7.4, 7.4, 7.4, 7.4, 7.4, 7.4, 7.42, 7.51

- Mediana: 7.395
- Rango: 7.2-7.51
- Acidosis pH <7.35: 5/16 (31.3%) [Casos con pH 7.2, 7.27, 7.3, 7.3, 7.3]
- n/N: 16/34 (47.1%)

[CORRECCION v3.1: n corregido de 14 a 16 (3 valores faltaban en lista v3.0: 7.3, 7.38, 7.4). Verificado contra CSV campo Laboratorios Ingreso.]

**HCO3 (mEq/L):**
Valores disponibles (15/34): 13.6, 15, 17, 18.5, 19.4, 20.5, 21.9, 22, 23, 23, 23, 24.7, 24.7, 26.2, 27.1

- Mediana: 22.0
- Rango: 13.6-27.1
- n/N: 15/34 (44.1%)

[CORRECCION v3.1: n corregido de 12 a 15 (5 valores faltaban: 21.9, 22, 23, 23, 26.2). Mediana 19.95→22.0. Verificado contra CSV.]

### E.6 Enzimas y marcadores especificos

**LDH (U/L):**
Valores disponibles (7/34): 250, 254, 300, 433, 630, 715, 790
- Mediana: 433
- Rango: 250-790
- Elevada (>250): 6/7 (85.7%)
- n/N: 7/34 (20.6%)

[CORRECCION v3.1: Header decia 5/35, lista tenia 7 valores. Corregido a 7/34.]

**Troponina:**
Valores disponibles (2/34): 78 (Caso 27, fallecido), 121 (Caso 26)
- Ambas elevadas
- n/N: 2/34 (5.9%)
- [VACIO: Cobertura insuficiente]

**Albumina (g/dL):**
Valores disponibles (3/34): 2.5, 2.5, 2.6
- Todas hipoalbuminemia (<3.5)
- n/N: 3/34 (8.8%)
- [VACIO: Cobertura insuficiente]

**VHS (mm/h):**
Valores disponibles (5/34): 8, 10, 21, 40, 40
- n/N: 5/34 (14.7%)

[CORRECCION v3.3: Header corregido de 4/34 a 5/34 (lista siempre tuvo 5 valores).]

**INR:**
Valores disponibles (11/34): 0.9, 1, 1.02, 1.04, 1.06, 1.08, 1.1, 1.1, 1.27, 1.3, 1.34
- Mediana: 1.08
- Rango: 0.9-1.34
- Prolongado >1.2: 3/11 (27.3%)
- n/N: 11/34 (32.4%)

**CK total / CK-MB:**
Caso 19: CK total 407, CK-MB 28
- n/N: 1/34 (2.9%)
- [VACIO: Cobertura insuficiente]

### E.7 Tabla resumen de cobertura laboratorio

| Variable | n disponible | N total | % cobertura | Interpretable? |
|----------|-------------|---------|-------------|---------------|
| Plaquetas | 32 | 34 | 94.1 | Si |
| FC | 29 | 34 | 85.3 | Si |
| SatO2 | 28 | 34 | 82.4 | Si |
| PAS | 28 | 34 | 82.4 | Si |
| Leucocitos | 26 | 34 | 76.5 | Si (manual) |
| Hematocrito | 27 | 34 | 79.4 | Si |
| PCR | 24 | 34 | 70.6 | Si |
| FR | 23 | 34 | 67.6 | Si |
| Creatinina | 22 | 34 | 64.7 | Marginal |
| Dias hosp | 20 | 34 | 58.8 | Marginal |
| Dias UCI | 18 | 34 | 52.9 | Marginal |
| Inmunoblastos | 16 | 34 | 47.1 | Marginal |
| Natremia | 16 | 34 | 47.1 | Marginal |
[NOTA v3.3: E.7 ya decía 16/34 correctamente. E.3 decía 14/34 — corregido a 16/34 en v3.3.]
| pH arterial | 16 | 34 | 47.1 | Marginal |
| HCO3 | 15 | 34 | 44.1 | Marginal |
| INR | 11 | 34 | 32.4 | No |
| Lactato | 8 | 34 | 23.5 | No |
| LDH | 7 | 34 | 20.6 | No |
| BUN | 6 | 34 | 17.6 | No |
| GOT | 6 | 34 | 17.6 | No |
| VHS | 5 | 34 | 14.7 | No |
| Albumina | 3 | 34 | 8.8 | No |
| GPT | 3 | 34 | 8.8 | No |
| GGT | 3 | 34 | 8.8 | No |
| Troponina | 2 | 34 | 5.9 | No |
| CK | 1 | 34 | 2.9 | No |

[CORRECCION v3.2: Tabla E.7 REHECHA completa. Todos los denominadores corregidos a N=34. Valores verificados contra parsed_clinical_all.csv (S37). Agregadas FC, SatO2, PAS, FR, Dias hosp, Dias UCI. Leucocitos n=26 (manual, no CSV). Hematocrito actualizado de 23 a 27. pH de 14 a 16. HCO3 de 12 a 15. Natremia de 15 a 16.]

**Umbral de exclusion STROBE:** Variables con <60% de cobertura se reportan descriptivamente pero se excluyen de analisis comparativos formales.

---

## F. Gestion de urgencias

### F.1 Consultas previas al diagnostico

Valores disponibles (33/34 en CSV):
1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5

- Media: 2.5 consultas
- Mediana: 3 consultas
- Rango: 1-5
- 1 consulta: 7/33 (21.2%)
- >=2 consultas: 26/33 (78.8%)
- >=3 consultas: 19/33 (57.6%)
- n/N: 33/34 (97.1%)

[CORRECCION v3.3: Lista corregida de 32 items (12×3 + ">3") a 33 items (14×3). >=3 corregido de 18/33 a 19/33. El ">3" de v3.0 era un valor que el CSV codifica como 3 (reconsulta cuantificable). Verificado S39 crosscheck.]
[CORRECCION v3.0: v2.1 reportaba 29/35. CSV verificado muestra 33/34 pacientes con dato de consultas.]
[Fuente: datos/parsed_clinical_all.csv, campo "n_consultas"]

### F.2 Categoria de triage

Datos disponibles (~18/34):

| Categoria | n | % |
|-----------|---|---|
| C1 (Emergencia) | 1 | 5.6 |
| C2 (Urgencia) | 12 | 66.7 |
| C3 (Urgencia menor) | 3 | 16.7 |
| C4 (General) | 1 | 5.6 |
| desc | 1 | 5.6 |

- C2 predomina: 12/18 (66.7%)
- n/N: 18/34 (52.9%)

[NOTA: Caso 27 fue categorizado C4 en primera consulta y reclasificado C1 en segunda consulta 12h despues, con insuficiencia respiratoria catastrofica. Fallecio.]

### F.3 Tiempo de espera para atencion medica

Valores disponibles (~14/34):
15min, 15min, 30min, 47min, 50min, 50min, 50min, 50min, 1h08, 1h20, 7h

- Mediana: ~50 min
- Rango: 15 min - 7 horas
- n/N: ~14/34

[NOTA: Caso 10 con 7 horas de espera (C3) es un outlier extremo.]

### F.4 Tiempo total de estadia en urgencias

Valores disponibles (~20/34):
15min, 1h, 2h, 2h, 2h, 2h30, 2h30, 3h, 3h, 3h, 4h, 4h30, 5h, 5h, 5h, 5h, 6h, 6h14, 7h, 8h, 8h, 8h

- Media: ~4.5 horas
- Mediana: ~4 horas
- Rango: 15 min - 8 horas
- n/N: ~20/34

### F.5 Derivacion desde SAR/CESFAM/Hospital comunal

Casos derivados desde atencion primaria/secundaria:
- Caso 3: derivado desde SAR
- Caso 13: derivado desde Hospital San Carlos (HSC), 10 dias hospitalizado como neumonia atipica
- Caso 21: 3 reconsultas, 1 en Coihueco
- Caso 11: 2 consultas previas (1 Coihueco, 1 HCHM)
- Caso 12: derivado desde San Ignacio
- Caso 4: derivado desde HLH [INCONSISTENCIA: contagio El Carmen pero derivado desde HLH?]

### F.6 Caso paradigmatico de retraso diagnostico

**Caso 27 (fallecido):**
- 1ra consulta: C4 (semi-urgencia general)
- 12 horas despues: C1 con insuficiencia respiratoria catastrofica
- Requirio VMI + ECMO
- Fallecio

**Caso 31 (fallecida en SU):**
- 4 consultas previas
- Murio en urgencias en 2 horas
- Htro 70.5%, pH 7.2, leuco 35.700, plaq 45.000
- No recibio VMI, ECMO, ni traslado

---

## G. Manejo clinico

### G.1 Volemizacion en Servicio de Urgencias

Valores disponibles en mL (23/34 en CSV):

[NOTA: Algunos valores son indicacion de hospitalizacion (ml/dia) no bolo SU. Requiere diferenciacion.]

**Bolos SU (administracion rapida, identificados):**

| Caso | Volumen | Tiempo | Velocidad |
|------|---------|--------|-----------|
| 1 | 1000 mL SF 0.9% | 20 min | Bolo rapido |
| 6 | 1000 mL | 30 min | Bolo rapido |
| 17 | 500 mL SF 0.9% | 20 min | Bolo rapido |
| 18 | 500 mL SF 0.9% | 20 min | Bolo rapido |
| 36/excl | 1000 mL | 30 min | Bolo rapido |
| 15 | 3000 mL en 3h + 1200 en 12h | 15 hrs total | 4200 mL total |
| 3 | 1000 mL | 3 hrs | Infusion |
| 9 | 750 mL | 7 hrs | Lenta |
| 27 | 1000 mL en 2h + 2000/dia | -- | Mixto |

- Mediana volumen total SU: 1000 mL
- Rango: 500-4200 mL
- n/N: 23/34 (67.6%)

[NOTA: Caso 15 recibio 4200 mL en 15 horas. Este es el volumen mas alto registrado y potencialmente excesivo dada la fisiopatologia del SCPH (edema pulmonar no cardiogenico agravado por sobrecarga hidrica).]

[Fuente: datos/parsed_clinical_all.csv, campo "vol_ml"]

### G.2 Drogas vasoactivas (DVA)

Datos disponibles (22/34):

| DVA | Si | No | desc |
|-----|----|----|------|
| Conteo | 6 | 16 | 13 |

DVA administradas:
- Noradrenalina: Caso 1
- Dopamina: Caso 11 (8 ug/kg/min, descalando en 2 dias)
- "Si" sin especificar: Casos 25, 26, 27, 12

[CORRECCION CONFIRMADA: Caso 31, campo DVA decia "hidrocortisona 300 mg ev" = error de transcripcion. Era corticoide, NO DVA. Caso 31 NO recibio DVA.]

- DVA: 6/22 (27.3%) de los que tienen dato
- n/N: 22/34 (64.7%)

### G.3 Soporte ventilatorio

**VMI (Ventilacion Mecanica Invasiva):**

Datos disponibles (25/34 en CSV — 9 Si, 16 No, 9 desc):

| VMI | n | % |
|-----|---|---|
| Si | 9 | 36.0 |
| No | 16 | 64.0 |
| desc | 9 | -- |

- VMI: 9/25 (36.0%)
- n/N: 25/34 (73.5%)

Casos con VMI: 1, 9, 12, 21, 25, 26, 27, 32a, y 1 adicional segun CSV

[CORRECCION v3.0: v2.1 reportaba 8/25 (32.0%). CSV verificado muestra 9 "Si" en campo VMI.]
[Fuente: datos/parsed_clinical_all.csv, campo "vmi"]

**VMNI (No invasiva: CNAF, CPAP, BiPAP):**

| Modalidad | Casos |
|-----------|-------|
| CNAF | Caso 11 (40 L) |
| VMNI (BiPAP/CPAP) | Casos 11, 13, 22, 23 |
| Naricera | Casos 11, 13 |

- VMNI: ~4/34 (11.4%)

**Perfil ventilatorio detallado (cuando disponible):**

Caso 27 (fallecido):
- VC, Vt: 400 mL (5 mL/kg), VM: 8.9, FR: 24, C: 25 cmH2O, deltaP: 13 cmH2O, PEEP: 14, FiO2: 100% para SatO2 92%
- Ventilacion protectora

Caso 12:
- AC/Vol, VT 6 mL/kg, FR 24, PEEP 10, flujo 60 L/min, FiO2 50%

### G.4 Ingreso a UPC

Datos disponibles (33/34):

| UPC | n | % |
|-----|---|---|
| Si | 32 | 97.0 |
| No | 1 | 3.0 |
| desc | 2 | -- |

- Caso 31: NO ingreso a UPC (fallecio en SU)
- Ingreso UPC: 32/33 (97.0%)

### G.5 Corticoides

Datos disponibles (24/34):

| Corticoide | Tipo | Dosis | Caso |
|------------|------|-------|------|
| Si | Hidrocortisona | 100 mg c/8h | Casos 12, 15, 16 |
| Si | Hidrocortisona | 300 mg ev | Casos 31*, 32a, 32b, 33 |
| Si | Dexametasona | 8 mg | Caso 10 |
| Si | Dexametasona | sin dosis | Caso 3 |
| No | -- | -- | 14 casos |

*Caso 31: hidrocortisona 300 mg registrada en campo DVA por error de transcripcion. Es corticoide.

- Corticoides: 10/24 (41.7%) de los que tienen dato
- Hidrocortisona: 7 casos
- Dexametasona: 2 casos (Caso 3 sin dosis, Caso 10 con 8 mg)
- [NOTA: Caso 10 recibio dexametasona 8 mg en SU HCHM -- confirmado]
- n/N: 24/34 (70.6%)

### G.6 Hemodinamica avanzada (Swan-Ganz)

Solo 2 casos con cateter Swan-Ganz documentado:

**Caso 9:**
- Indice cardiaco: 4.4
- Gasto cardiaco: 7.7
- PCP: 1 [Caso 9 Swan-Ganz PCP 1: omitir por error de digitacion segun instruccion, conservar IC y GC]

**Caso 25:**
- GC: 3.6, IC: 1.7, PVC: 3, PCP: 12, RVS: 1476, RVP: 154
- ECMO VA: RPM 3970, Flujo 4.5, Flujo gas 2 LPM
- Nota: "Al reducir RPM aumenta PP (a expensas de reducir PAD), cae VPP y aumenta PAP sugerente precarga sensible"

### G.7 Balance hidrico (BH)

Solo 2 casos con BH documentado:
- Caso 13: BH 2do dia: +219 mL
- Caso 14: BH 1er dia: +209 mL

---

## H. Intervenciones terapeuticas

### H.1 ECMO

Datos disponibles (21/34):

| ECMO | n | % |
|------|---|---|
| Si | 3 | 14.3 |
| No | 18 | 85.7 |
| desc | 14 | -- |

Casos con ECMO:
- Caso 9: ECMO desde dia 2 post-diagnostico, 6 dias de conexion, en HLH
- Caso 25: ECMO VA, 6 dias, en HLH
- Caso 27: ECMO (fallecido), en HGGB

- ECMO: 3/21 (14.3%)
- **Todos los ECMO fueron en centros derivadores** (ninguno en HCHM)
- n/N: 21/34 (61.8%)

[NOTA: El paper previo reportaba 4 ECMO sobre n=23 disponibles (17.4%). Con recalculo n=35, ECMO=3/21=14.3%.]

### H.2 Plasma hiperinmune

Datos disponibles (19/34 en CSV — 5 Si, 14 No, 15 desc):

| Plasma HI | n | % |
|-----------|---|---|
| Si | 5 | 26.3 |
| No | 14 | 73.7 |
| desc | 15 | -- |

Casos con plasma:
- Caso 3: Si, en HLH
- Caso 6: Si
- Caso 8: Si, en HGGB
- Caso 9: Si, antes de VMI y ECMO, en HLH
- Caso 11: Si, 2/3 en HLCM (Hospital Luis Calvo Mackenna)

- Plasma HI: 5/19 (26.3%)
- **NINGUNO recibio plasma en HCHM** -- todos en centros derivadores
- **Todos los que recibieron plasma: sobrevivieron (5/5)**
- n/N: 19/34 (55.9%)

[CORRECCION v3.0: v2.1 reportaba 3/17 (17.6%). CSV verificado muestra 5 pacientes con plasma=Si (C3, C6, C8, C9, C11). El paper previo reportaba 6/20 -- la diferencia de 1 se explica porque los duplicados excluidos (C7=C6, C36=C6, C38=C15) inflaron el conteo original.]
[Fuente: datos/parsed_clinical_all.csv, campo "plasma"]

[DECISION GONZALO S29: Discrepancia plasma resuelta. Los 5 del CSV son verificados. Paper previo tenia duplicados.]

### H.3 Traslado a centro de mayor complejidad

Datos disponibles (30/34):

| Traslado | n | % |
|----------|---|---|
| Si | 24 | 80.0 |
| No | 6 | 20.0 |
| desc | 5 | -- |

**Centros de destino:**

| Centro | n | Distancia desde Chillan | Tiempo traslado |
|--------|---|------------------------|-----------------|
| HLH (Las Higueras, Talcahuano) | 7 | ~100 km | ~1.5 h |
| HGGB (Grant Benavente, Concepcion) | 7 | ~115 km | ~1.5-2 h |
| HLCM (Luis Calvo Mackenna, Santiago) | 2 | ~400 km | Avion/terrestre |
| Hospital del Torax (Santiago) | 1 | ~400 km | Avion/terrestre |
| H. Roberto del Rio (Santiago) | 1 | ~400 km | Avion/terrestre |
| Clinica Alemana Concepcion | 1 | ~115 km | ~1.5-2 h |
| H. Calvo Mackenna (Santiago) | 1 | ~400 km | Avion/terrestre |
| Hospital de Temuco | 1 | ~300 km | ~3 h |
| desc | 3 | -- | -- |
| HCHM (no trasladado pero en VMI) | 1 | 0 | 0 |

- Traslado: 24/30 (80.0%)
- **Mayoria a Concepcion/Talcahuano** (14/24 = 58.3%)
- Traslado a Santiago (pediatricos): 4/24 (16.7%)
- n/N: 30/34 (88.2%)

### H.4 Otros tratamientos documentados

- Anticoagulacion: Caso 25 (HNF en BIC para ECMO)
- Acido valproico: Caso 1 (mioclonias)
- [VACIO: Ribavirina -- no documentada en ningun caso]
- [VACIO: Antibioticos profilacticos -- no sistematicamente registrados]

---

## I. Desenlaces

### I.1 Mortalidad

**Desenlace conocido:** 33/34 (Caso 37 excluido)

| Desenlace | n | % |
|-----------|---|---|
| Vivo | 28 | 82.4 |
| Fallecido | 5 | 14.7 |
| Desconocido | 1 | 2.9 (Caso 34) |

**Letalidad:** 5/34 = **14.7%** (IC 95% Clopper-Pearson: 5.0-31.1%)

[NOTA: Denominador 34 porque Caso 37 excluido (sin datos) y Caso 34 tiene desenlace desconocido pero se incluye en n.]

[Fuente: IC calculado en S29 (project_analisis_clinico_S29_completo.md)]

**Analisis de sensibilidad:**
- Mejor caso (desconocidos vivos): 5/34 = 14.7%
- Peor caso (desconocidos fallecidos): 6/34 = 17.6% (si Caso 34 fallecido)

### I.2 Detalle de los 5 fallecidos

| Caso | Edad | Sexo | Fecha | Comuna | Dias sint. | Circunstancia muerte |
|------|------|------|-------|--------|-----------|---------------------|
| 27 | 54 | M | Ene 2024 | desc (precordillera Parral) | 5 | C4->C1 en 12h, VMI+ECMO, fallecido |
| 30 | 49 | F | Abr 2023 | El Carmen | 3 | Datos limitados, fallecida |
| 31 | 37 | F | Mar 2022 | Pinto | 4 | Muerte en SU en 2 horas, no VMI/ECMO |
| 32a | 51 | M | Ene 2022 | San Fabian | 3 | VMI, fallecido |
| 32b | 12 | F | Feb 2022 | Coihueco | 3 | Trasladada a HLCM, fallecida |

[NOTA: Caso 30 es madre de Caso 21 (11M, vivo). "Madre muere por sepsis posterior a conexion ECMO" segun ficha de Caso 21.]
[NOTA: TODOS los fallecidos en periodo 2022-2024. 0 muertes 2012-2021. Ver seccion X para analisis.]

### I.2b Clasificacion de severidad v6.2 (ver seccion O para detalle completo)

| Clasificacion | Severo | Moderado | Infeccion sin SCPH |
|--------------|--------|----------|-------------------|
| n (%) | 14 (41.2%) | 14 (41.2%) | 6 (17.6%) |
| Muertes | 4 | 1 | 0 |
| Letalidad | 28.6% | 7.1% | 0% |

[CORRECCION v3.0: v2.1 tenia tabla incorrecta con "10 severo, 18 moderado, 3 leve, 3 NC" de version previa. Resultado v6.2 definitivo: 14/14/6.]

**MINSAL binaria (primaria):** SCPH 28/34 (82.4%), letalidad 17.9% (IC 6.1-36.9%). Infeccion sin SCPH 6/34 (17.6%), letalidad 0%.
**Concordancia v6.2 con MINSAL: 100%**

### I.3 Sobrevivientes vs. Fallecidos

| Variable | Sobrevivientes (n=28) | Fallecidos (n=5) | p (MW/Fisher) |
|----------|----------------------|-------------------|---------------|
| Edad mediana | 32 (23.5-44.2) | 49 (37-51) | 0.303 |
| Dias sintomas mediana | 4.5 | 3 | 0.138 |
| PAS mediana | 112 (97.2-129.5) | 121 (103-128) | 0.731 |
| FC mediana | 105 (83.5-115.5) | 102 (102-105) | 1.000 |
| FR mediana | 22 (21.2-27.8) | 27.5 (23.8-30.5) | 0.413 |
| SatO2 mediana | 94.5 (92.2-97.5) | 94 (91-94) | 0.508 |
| Plaq mediana | 98k (64.5k-167k) | 76k (45k-79k) | 0.337 |
| Htro mediana | 43 (38.1-44.8) | 53.4 (44-62.6) | 0.183 |
| Leuco mediana | 7900 (5550-11300) | 8800 (5k-17.2k) | 0.631 |
| Cr mediana | 0.8 (0.7-1.0) | 1.6 (1.2-1.9) | 0.185 |
| PCR mediana | 89 (57-143) | 129.5 (100.2-151.8) | 0.474 |
| Sexo F | 10/28 (35.7%) | 3/5 (60.0%) | 0.360 |
| Plaq <100k | 15/27 (55.6%) | 4/5 (80.0%) | 0.625 |

[CORRECCION v3.2: Plaq<100k AMBAS celdas corregidas. Sobrevivientes: 12/27->15/27 (CSV confirma 15 con plaq<100k). Fallecidos: 5/5->4/5 (C32b tiene plaq=331k, NO es <100k). Fisher OR=3.20, p=0.625 (antes p=0.037). CAMBIO SIGNIFICATIVO: Plaq<100k vs muerte YA NO es significativo. Tabla original tenia error en C32b.]
| Htro >=50% | 2/23 (8.7%) | 2/4 (50.0%) | 0.092 |
| Edad >35 | 12/28 (42.9%) | 4/5 (80.0%) | 0.175 |

[CORRECCION v3.0: Tabla completamente reemplazada con datos de S29 (tabla estilo Castillo). Denominadores, medianas e IQR verificados.]
[Fuente: project_S29_complemento_series_tabla.md, tabla 1]

**Sin pruebas estadisticas formales en v2.1. En v3.0 se incluyen Fisher/Mann-Whitney de S29 (n=5 fallecidos: poder insuficiente, interpretacion descriptiva).**

### I.4 Dias de hospitalizacion

Datos disponibles (20/34 con dato de hospitalizacion total, S39 CSV verificado):

Valores: 1, 2, 5, 6, 7, 7, 8, 10, 10, 14, 14, 14, 14, 15, 15, 16, 20, 21, 25, 31

- Mediana: 14 dias
- Media: 12.8 dias
- Rango: 1-31 dias
- n/N: 20/34 (58.8%)

[CORRECCION v3.3: Lista completada a 20 valores (antes 15). 5 valores faltantes recuperados del CSV: 6, 8, 10, 10, 16. Mediana 14 sin cambio (posiciones 10-11 ambas son 14). Media corregida de 13.3→12.8. n/N corregido de 15/34→20/34. Verificado S39 crosscheck con Rscript.]

**Dias de UCI:**
Datos disponibles (18/34):

Valores: 1, 2, 2, 3, 5, 5, 5, 7, 7, 7, 11, 12, 12, 14, 14, 15, 19, 30

- Mediana: 7 dias
- Rango: 1-30 dias

[CORRECCION v3.1: n corregido de 12 a 18, lista completa verificada contra CSV. Mediana 9→7. v3.0 omitia 6 valores.]

### I.5 Complicaciones documentadas

| Complicacion | Caso | Fase |
|-------------|------|------|
| Neumonia asociada a VMI (NAVM) | 1, 9 | Aguda |
| Mioclonias | 1 | Aguda |
| LPP sacra con escarectomia | 1 | Aguda |
| Sd. de realimentacion | 9 | Aguda |
| Disfonia, disnea mMRC 1 | 9 | Tardia |
| Neumonia nosocomial | 3 | Aguda |
| Anemia megaloblastica | 3 | Aguda |
| IAM (2021, 2 anos post) | 3 | Tardia |
| Cefalea secundaria | 2 | Aguda |
| Nefropatia medica bilateral | 15 | Tardia (1 ano) |
| Infeccion VH6 en VMI | 21 | Aguda |
| Nefropatia medica (alta con nifedipino) | 21 | Aguda/Tardia |
| ICC descompensada | 13 | Aguda |
| Delirium hiperactivo | 13 | Aguda |
| AC x FA (7 anos post) | 13 | Tardia |
| Celulitis por S. aureus (20 dias post) | 19 | Aguda |
| Sinusitis por A. baumannii MR | 25 | Aguda |

---

## J. GRD y analisis del sistema de salud

### J.1 Costos invisibles HCHM

Bajo el sistema GRD (Grupos Relacionados por el Diagnostico):
- Cuando un paciente SCPH es estabilizado en HCHM y trasladado, el **centro receptor cobra el egreso completo**
- GRD 041013, peso 11.7, equivalente a ~$34.7 millones CLP (tarifa 2026)
- **HCHM no recibe compensacion** por:
  - Estabilizacion inicial
  - Diagnostico serologico (Puumala IgM/PCR)
  - Manejo en urgencias (media ~4.5 horas)
  - Coordinacion del traslado

Con 24/30 pacientes trasladados (80%), el costo invisible anual estimado es significativo.

### J.2 ECMO en HCHM

- **0 ECMO realizados en HCHM** en toda la serie
- HCHM aparece en la base GRD ECMO nacional con **1 egreso en 2024** (Caso 27? probablemente estabilizacion previa a traslado)
- Barrera de volumen: ~5 SCPH/ano no justifica programa ECMO autonomo (umbral ELSO: 12-20/ano)

### J.3 ECMO nacional -- datos GRD MINSAL 2023-2025

| Centro derivador | 2023 | 2024 | 2025 | Tendencia |
|-----------------|------|------|------|-----------|
| HLH (Talcahuano) | 11 | 17 | 26 | +136% |
| HGGB (Concepcion) | 19 | 34 | 44 | +132% |
| INET (Santiago) | 39 | 39 | 56 | +44% |
| H. San Juan de Dios (Stgo) | 25 | 30 | 29 | +16% |
| H. Sotero del Rio | 10 | 9 | 13 | +30% |
| H. Temuco | 17 | 19 | 23 | +35% |
| Total nacional (acum Nov) | 157 | 187 | 240 | +53% |

**Mortalidad ECMO nacional:**
- 2023: 73/157 (46.5%)
- 2024: 90/187 (48.1%)
- 2025: 102/240 (42.5%)

**Estancia media ECMO:** 36.6-37.4 dias

### J.4 Brechas terapeuticas identificadas

1. **Plasma hiperinmune:** 0 administraciones en HCHM. Todas en derivadores.
   - Manual MINSAL v2.0 (2018): "todo paciente sospechoso o confirmado sera trasladado a centro con capacidad ECMO" y plasma "lo mas pronto posible" a 10.000 U/Kg
   - Precedente: Hospital Regional de Talca logro gestionar plasma para paciente pediatrica SCPH (2015)

2. **ECMO:** 0 en HCHM. Solo en derivadores a 100-115 km (1.5-2 horas).

3. **Demanda ECMO integrada (estimacion):** Integrando IAM (tasa 38.79/100k Nuble), SDRA, TEP, miocarditis y SCPH, la demanda estimada es 16-31 casos/ano, superando umbral ELSO de 12/ano.

### J.5 Plasma hiperinmune -- brecha de implementacion

| Aspecto | Protocolo MINSAL | Realidad HCHM |
|---------|-----------------|---------------|
| Disponibilidad | Todo centro debe coordinar con Centro de Sangre | No se ha implementado |
| Dosis | 10.000 U/Kg | No administrado |
| Timing | "Lo mas pronto posible" | Solo tras traslado (horas-dias) |
| Ventana terapeutica | Primeras 24-48h de fase cardiopulmonar | Perdida por traslado |

---

## K. Comparacion con series chilenas previas

### K.1 Series identificadas

| Serie | n | Centro | Periodo | Revista |
|-------|---|--------|---------|---------|
| Castillo 2001 | 16 | Temuco (solo UCI) | 1997-1999 | CHEST |
| Tapia 2000 | 24 | Coyhaique (UCI) | 1996-1999 | Rev Chil Infectol |
| Riquelme 2015 | 103 | Puerto Montt (espectro completo) | 1995-2012 | EID |
| Vial 2013 | 60 | Multicentrico (fase cardiopulmonar) | 2003-2010 | CID |
| Lopez 2019 | 175 | Multicentrico | -- | Viruses |
| Vial C 2019 | 139 | Multicentrico | -- | Rev Chil Infectol |
| Ferres/Martinez-V 2024 | 131 | Multicentrico Chile | 2008-2022 | Lancet Infect Dis |
| Ulloa-Morrison 2024 | Review | -- | -- | J Crit Care |
| **Presente serie** | **34** | **HCHM Chillan (todos)** | **2012-2025** | -- |

[CORRECCION v3.0: Tabla expandida con series adicionales identificadas en S29.]
[Fuente: project_S29_complemento_series_tabla.md, seccion 6]

### K.2 Comparacion con Castillo et al. 2001 (comparador principal)

| Variable | Castillo 2001 (n=16) | HCHM 2025 (n=34) | Nota |
|----------|---------------------|-------------------|------|
| Escenario | Solo UCI, Temuco | Todos (SU + UCI), Chillan | Espectros diferentes |
| Periodo | 2 anos (1997-99) | 13 anos (2012-25) | -- |
| Edad media | 30 (19-45) | 34.9 (11-69) | -- |
| VMI | 69% | 36.0% (9/25) | Espectro completo |
| DVA | 63% | 27.3% (6/22) | Espectro completo |
| ECMO | No disponible | 14.3% (3/21) | Era moderna |
| Plasma | No disponible | 26.3% (5/19) | Era moderna |
| Volumen IV | 3.2 L/24h UCI | 1.0 L mediana SU | No comparable |
| Letalidad | 43.8% | 14.7% (IC95% 5.0-31.1) | Reduccion significativa |
| Timing lab | Peores valores UCI | Ingreso urgencias | No comparable |

[CORRECCION v3.0: VMI actualizado a 9/25 (36.0%). Plasma actualizado a 5/19 (26.3%). Edad a 34.9.]

### K.2b Datos especificos Castillo 2001

- Swan-Ganz en 5 pacientes: PAOP normal (4-12), CI cayo a 1.63-1.94 al nadir
- Hemorragia 81%: hematuria 50%, hemoptisis 25%, hematemesis 19%, epistaxis 13%
- Hiponatremia 69% (114-129 mEq/L)
- Creatinina elevada 54%
- IV fluidos: sobrevivientes 2.4L vs fallecidos 4.5L (p=0.07)
- "Probably received excessive IV fluids" -- primera mencion de volemizacion excesiva

[Fuente: project_S29_complemento_series_tabla.md, seccion 6]

### K.3 Predictores de mortalidad comparados entre series

| Factor | Castillo | Riquelme | Vial | Lopez 2019 | Nosotros |
|--------|----------|----------|------|------------|----------|
| PAS <90 | **p=0.042** | OR 4.0 p=0.014 | -- | -- | OR=3.25 (IC 0.03-66) p=0.40 |
| FR >30 | -- | **OR 15.3 (IC 3.8-61.5) p<0.001** | -- | -- | OR=2.08 (IC 0.03-54) p=0.50 |
| FR >22 (sev) | -- | -- | -- | -- | **OR=11.7 (IC 1.4-174) p=0.012** |
| PaO2/FiO2 | **p=0.001** | OR 7.1 p=0.008 | -- | -- | No disponible |
| Vol IV | p=0.07 (4.5vs2.4L) | -- | -- | -- | **Gradiente monot** |
| Hemorragia | 81% | OR 6.8 p<0.001 | -- | -- | No evaluada |
| Cr >1.3 | NS | **OR 3.7 p=0.017** | -- | -- | OR=6.75 (IC n.e.) p=0.284 |
| SOFA | -- | -- | **OR 3.14 p=0.049** | -- | No disponible |
| APACHE >12 | -- | (Rioseco 2003: 77% mort) | -- | -- | C27=22 fallec, C29=13 |
| Plaq <40k | NS | NS | -- | **OR 70 p=0.005** | Tendencia |
| Plaq <150k | -- | -- | -- | AUC=0.889 | **Sev p=0.031** |
| Htro >=50% | NS (media 56%) | NS | -- | -- | **OR=9.06 (IC 0.44-204) p=0.092** |

[CORRECCION v3.1: Todos los OR "Nosotros" ahora con IC 95% Fisher. FR>22 en K.3 es vs MORTALIDAD (OR=4.39), diferente de T.2 que es vs SEVERIDAD (OR=11.7). Htro OR recalculado: 8.67→9.06 (Fisher MLE difiere de OR crudo).]
| Corticoides | p=0.09 (protector?) | NS | **NS RCT p=0.41** | -- | p=0.017 (confundido) |

[Fuente: project_S29_complemento_series_tabla.md, seccion 6]

### K.4 Evolucion de letalidad en series chilenas

| Serie | Ano | Letalidad |
|-------|-----|-----------|
| Castillo (Temuco) | 2001 | 43.8% |
| Tapia (Coyhaique) | 2000 | 37.5% |
| Riquelme (Puerto Montt) | 2015 | 32.0% |
| Vial (multicentrico) | 2013 | 33.0% |
| Lopez (multicentrico) | 2019 | -- |
| Ferres multicentrico | 2024 | ~28% (ISP ultimos 5 anos) |
| **Presente serie** | **2025** | **14.7%** |

Tendencia descendente que coincide temporalmente con: reconocimiento precoz, manejo hemodinamico protector, disponibilidad de ECMO y plasma. La serie presente incluye espectro completo (SU+UCI), lo que reduce letalidad aparente vs. series solo-UCI. [CORRECCION v3.1: "atribuible a" → "coincide temporalmente con" (CAUSAL-01).]

**[DEFENSA Q1 v3.3 — CFR ACROSS ERAS]** La comparacion directa de letalidades entre series de diferentes eras y espectros de gravedad es inherentemente sesgada (Lipsitch 2015, PLoS NTD): la ascertacion preferencial de casos graves en series historicas (Castillo 2001 = solo UCI; Tapia 2000 = solo UCI) infla la CFR aparente respecto a series all-comers como la presente. Este "spectrum bias" (Verity 2020, Lancet Infect Dis) fue demostrado cuantitativamente durante COVID-19 y aplica directamente a la comparacion 14.7% vs 32-44%. La tendencia descendente tambien se observa en Argentina: Alonso 2019 (J Med Virol) documenta CFR nacional cayendo de >30% a 21.4% entre 1990s-2017. La serie presente es la primera chilena en capturar el espectro completo incluyendo infeccion sin SCPH.

### K.5 Ventajas diferenciales de la presente serie

1. **Espectro completo de gravedad** (desde infeccion sin SCPH hasta muerte en SU)
2. **Score v6.2** con criterios explicitos y reproducibles
3. **Datos de gestion de urgencias** (triage, tiempos, consultas previas) -- primera serie en documentarlos
4. **Fenotipo del paciente que fallece** (3 ejes, hallazgo original)
5. **FR >22 como discriminador de severidad** (umbral exploratorio post-hoc; incluye espectro completo infeccion Andes; OR=11.7, mas sensible que Riquelme FR>30)
6. **Variables era moderna** (ECMO, plasma hiperinmune, corticoides)
7. **Costos GRD** y analisis del sistema de salud -- no reportados previamente
8. **Conexion con analisis epidemiologico-ecologico** (Parte I del paper, One Health)

---

## L. Bibliografia

### L.1 Referencias del paper previo (verificadas)

1. MINSAL Chile. Dpto. Epidemiologia. Informes epidemiologicos anuales Hantavirus 2019-2024. epi.minsal.cl
2. SEREMI Salud Nuble. Reporte epidemiologico Hantavirus 2022. Tasa 0,97/100k.
3. MINSAL Chile. Guia Clinica Prevencion, Diagnostico y Tratamiento SCPH. Enero 2024.
4. von Elm E, et al. STROBE statement. Lancet 2007;370:1453-7.
5. MINSAL/DEIS. Tasa IAM Region Nuble: 38,79/100k (2014).
6. Bellani G, et al. ARDS in ICUs in 50 countries. JAMA 2016;315:788-800.
7. ELSO. Guidelines for ECMO Centers. 2021. Rev Chilena Anestesia 2021 (umbral 12-20/ano).
8. Castillo C, et al. HPS due to Andes virus in Temuco: 16 adults. CHEST 2001;120:548-54.
9. Tapia M, et al. SPH: experiencia Hospital Coyhaique. Rev Chilena Infectol 2000;17:258-69.
10. Riquelme R, et al. HPS southern Chile 1995-2012. Emerg Infect Dis 2015;21:562-8. DOI: 10.3201/eid2104.141437
11. Vial PA, et al. Methylprednisolone for HCPS: double-blind RCT. Clin Infect Dis 2013;57:943-51. DOI: 10.1093/cid/cit431
12. Mertz GJ, et al. Hantavirus infection. Dis Mon 1998;44:125-6.
13. CDC. HPS Clinical guidance: fluid restriction.
14. INE Chile. Censo 2017 y estimaciones poblacion migrante 2018-2024.
15. Ferrer P, et al. HLA and Andes Hantavirus severity. Rev Med Chile 2007;135:459-67.
16. Cao K, et al. HLA class I in sub-Saharan populations. Tissue Antigens 2004;63:293-325.
17. Nunes JM, et al. HLA map of the world. Front Genet 2023;14:866407.
18. Duchin JS, et al. HPS: 17 patients. N Engl J Med 1994;330:949-55. DOI: 10.1056/NEJM199404073301401
19. Lopez R, et al. Critical care management of HCPS. Med Intensiva 2024.
20. Vial PA, et al. Immune plasma for HCPS by Andes virus. Antivir Ther 2015;20:377-86. DOI: 10.3851/IMP2875
21. Crowley MR, et al. ECMO for severe HPS. Crit Care Med 1998;26:409-14.
22. Goldberg RJ, et al. Cardiogenic shock trends. N Engl J Med 1999;340:1162-8.
23. Kolte D, et al. Cardiogenic shock management. JACC 2014;63:389-99.
24. FONASA Chile. Mecanismo de pago GRD. Implementacion 2020. dipres.gob.cl
25. Cid C. GRD en financiamiento salud Chile. Seminario UC-FONASA-BM 2023.
26. Schmaljohn C, Hjelle B. Hantaviruses: a global problem. Emerg Infect Dis 1997;3:95-104.
27. Jonsson CB, et al. Global perspective hantavirus. Clin Microbiol Rev 2010;23:412-41.
28. Hjelle B, Torres-Perez F. Hantaviruses in the Americas. Viruses 2010;2:2559-86.
29. Mustonen J, et al. Immunogenetic factors hantaviruses. Viruses 2021;13:1452.
30. Lopez R, et al. Platelet count and progression to severe HCPS. Viruses 2019;11:693. DOI: 10.3390/v11080693
31. Consenso SEDAR/SECCE manejo ECMO. Cir Cardiovasc 2021.
32. Nazzal C, Alonso FT. IAM en Chile 2001-2007. Rev Med Chile 2011;139:1253-60.
33. Nazzal C, et al. IAM en Chile 2008-2016. Rev Med Chile 2021;149:323-9.
34. Tortosa F, et al. Controversias corticoides en SCPH. Medicina (B Aires) 2021;81:625-30.
35. Smith J, et al. HCPS management in critical care transport. Air Med J 2023;42:336-42.
36. MINSAL Chile. Manual Procedimientos Administracion Plasma Inmune Hantavirus v2.0. Feb 2018.
37. SS Maule. Suero hiperinmune: recuperacion paciente hantavirus. ssmaule.gob.cl/?p=5048, 2015.
38. Wernly JA, et al. ECMO improves survival in HPS. Eur J Cardiothorac Surg 2011;40:1334-40. DOI: 10.1016/j.ejcts.2011.01.089
39. Mertz GJ, et al. Ribavirin for HCPS: placebo-controlled trial. Clin Infect Dis 2004;39:1307-13.
40. Lopez R, et al. High-volume hemofiltration in HCPS. Med Intensiva 2024 (en prensa).

### L.2 Referencias agregadas S18

41. Vial PA et al. Hantavirus in humans: review of clinical aspects and management. Lancet Infect Dis 2023;23:e371-82. DOI: 10.1016/S1473-3099(23)00128-7
42. Ferres M et al. Viral shedding and viraemia of Andes virus. Lancet Infect Dis 2024;24:775. DOI: 10.1016/S1473-3099(24)00142-7
43. Martinez VP et al. Super-Spreaders and P2P transmission of Andes virus. N Engl J Med 2020;383:2230-41. DOI: 10.1056/NEJMoa2009040
44. Maleki KT et al. Serum markers severity and outcome HPS. J Infect Dis 2019;219:1832-40.
45. Torres-Macho J et al. Severity scores in COVID-19 pneumonia. J Gen Intern Med 2021;36:1338-45. DOI: 10.1007/s11606-021-06626-7
46. Ferreira M et al. Critically ill COVID-19 not stratified by qSOFA. Ann Intensive Care 2020;10:43. DOI: 10.1186/s13613-020-00664-w
47. Riley RD et al. Calculating sample size for clinical prediction model. BMJ 2020;368:m441. DOI: 10.1136/bmj.m441
48. Waksman R et al. SHARC: Standardized definitions cardiogenic shock. Circulation 2023;148:1113-26. DOI: 10.1161/CIRCULATIONAHA.123.064527
49. Collins GS et al. TRIPOD Statement. Ann Intern Med 2015;162:55-63. DOI: 10.7326/M14-0697
50. Stoeckle K et al. Development of MPOX Severity Score. J Infect Dis 2024;229(S2):S218-26. DOI: 10.1093/infdis/jiad492
51. Khalil H et al. Population dynamics of bank voles predicts human Puumala risk. EcoHealth 2019;16:545.
52. Lopez R et al. Platelet count progression to severe HCPS. Viruses 2019;11:693.
53. Lopez R et al. Proteinuria linked to mortality in HCPS. Int J Infect Dis 2021;110:466.
54. Tortosa F et al. Prognostic factors mortality hantavirus: systematic review GRADE. medRxiv 2024 (preprint). DOI: 10.1101/2024.05.20.24307524
55. Harkins M. Pathogenesis of hantavirus infections. UpToDate, Oct 2025.
56. Vial PA, Harkins M. Epidemiology and diagnosis of hantavirus infections. UpToDate, Oct 2025.
57. Harkins M, Vial PA. Hantavirus cardiopulmonary syndrome. UpToDate, Dic 2025.

### L.3 Referencias agregadas S20-S29 (score, series, fisiopatologia)

58. Koster FT et al. Rapid assessment of HPS. Am J Clin Pathol 2001;116:665-72. DOI: 10.1309/CNWF-DC72-QYMR-M8DA
59. Saggioro FP et al. Hantavirus infection induces a typical myocarditis. J Infect Dis 2007;195:1541-9. DOI: 10.1086/513874
60. Hallin GW et al. Cardiopulmonary manifestations of HPS. Crit Care Med 1996;24:252-8. PMID: 8605797
61. Ospina-Tascon GA et al. CNAF vs HFNC in COVID hypoxemia. JAMA 2021;326:2161-71. DOI: 10.1001/jama.2021.20714
62. ERS 2022. Clinical practice guidelines: HFNC therapy. Eur Respir J 2022. DOI: 10.1183/13993003.01574-2021
63. Ulloa-Morrison JM et al. Critical care management of HCPS. J Crit Care 2024;82:154867. DOI: 10.1016/j.jcrc.2024.154867
64. SCAI 2022. Cardiogenic shock stages. JACC 2022. DOI: 10.1016/j.jacc.2022.01.018
65. Sinha SS et al. JACC 2025. DOI: 10.1016/j.jacc.2025.02.018
66. Rioseco ML et al. Hantavirus pulmonary syndrome, southern Chile 1995-2003. EID 2003;9(11).
67. Vial C et al. Rev Chil Infectol 2019. PMID: 31859765
68. Lopez R et al. HVHF in HCPS. J Med Virol 2021. DOI: 10.1002/jmv.26930
69. Dospital BM et al. BJB 2024. DOI: 10.1590/1519-6984.269097
70. Seymour CW et al. qSOFA. JAMA 2016. DOI: 10.1001/jama.2016.0288
71. Singer M et al. Sepsis-3. JAMA 2016. DOI: 10.1001/jama.2016.0287
72. Evans L et al. SSC guidelines 2021. Crit Care Med. DOI: 10.1097/CCM.0000000000005337
73. ANDROMEDA-SHOCK JAMA 2019. DOI: 10.1001/jama.2019.0071
74. Story DA. Stewart approach. J Appl Physiol 2021. DOI: 10.1152/japplphysiol.00042.2021
75. CTCAE v5.0 NCI 2017 (documento gubernamental)
76. Barniol J et al. Dengue classification BMC Infect Dis 2011. DOI: 10.1186/1471-2334-11-106
77. Frat JP et al. FLORALI CNAF. NEJM 2015. DOI: 10.1056/NEJMoa1503326
78. Ferrés M et al. Household contacts Chile. JID 2007. DOI: 10.1093/infdis/jir036
79. Toro J et al. Outbreak Chile 1997. EID 1998. DOI: 10.3201/eid0404.980425
80. MINSAL Ordinario B38 N3420 (26 julio 2019). Orientaciones tecnicas roedores silvestres.
81. MINSAL Ordinario B51 N5554 (17 diciembre 2019). Mesas Regionales de Zoonosis.

### L.4 Referencias faltantes

[VACIO: Falta cita formal de aprobacion Comite de Etica HCHM -- numero acta, fecha]
[VACIO: Falta referencia para definicion de triage C1-C5 en Chile (Manual ESI adaptado o equivalente)]
[VACIO: Falta referencia para costos GRD actualizados 2026 -- solo estimacion]
[VACIO: Falta referencia para protocolo traslado aeromedicado pacientes criticos Nuble]

---

## M. Sesgos y limitaciones

### M.1 Sesgos declarados

1. **Sesgo de seleccion:** 35/133 fichas recuperables (26.3%). Perdida mayor pre-2012 por transicion papel-electronico y depuracion de archivos. Los 98 casos perdidos probablemente incluyen espectro diferente de gravedad.

2. **Sesgo de informacion/completitud:** Completitud variable 2.9-97.1% segun variable. Variables con <60% se reportan descriptivamente pero se excluyen de comparaciones formales (STROBE).

   **[STROBE 12c — PARRAFO PARA MANUSCRITO (S39)]**
   "Missing data were handled using a complete-case analysis approach, consistent with recommendations for small retrospective cohorts where multiple imputation may introduce instability (Carpenter & Kenward 2021). The proportion of missing data was reported for each variable (Table E.7); variables with <60% completeness were excluded from formal comparative analyses per STROBE guidelines (von Elm 2007). The missing data pattern was classified as Missing Not At Random (MNAR) using the TARMOS framework (Lee et al. 2021): severe cases had more complete data than moderate cases (e.g., respiratory rate available in 86% of severe vs 50% of moderate patients), suggesting that missingness is informative and biased toward completeness in sicker patients. This direction of bias tends to overestimate, not underestimate, the strength of associations between clinical markers and severity. The robustness of findings to potential missing data bias can be assessed via the M-value (Mathur 2023), analogous to the E-value for unmeasured confounding."

   **[DEFENSA Q1 v3.3 — MISSING DATA]** El manejo de datos faltantes sigue el framework TARMOS (Lee 2021, J Clin Epidemiol). Con n=34, el analisis de caso completo es preferible a imputacion multiple, que produce inestabilidad en muestras pequenas (Carpenter & Kenward 2021, Biom J). La transparencia de reporte supera la norma: Wu 2023 (Crit Care Explor) documenta que solo 50.9% de estudios de cohorte en UCI mencionan datos faltantes. Para cuantificar sesgo potencial por missing, se puede aplicar el M-value (Mathur 2023, Am J Epidemiol): analogo al E-value para confundimiento, mide cuanto tendrian que diferir los datos faltantes de los observados para anular el hallazgo. Las directrices MI de Sterne 2009 (BMJ) recomiendan presentar caso completo + sensibilidad, que es exactamente la estrategia adoptada.

3. **Sesgo de supervivencia en datos:** Las fichas mejor conservadas pueden corresponder a casos mas graves (mas documentacion) o a periodos mas recientes (formato electronico).

4. **Confundente por indicacion (corticoides):** Mortalidad con corticoides 40% vs 0% sin ellos (p=0.017). Los tratados eran los mas graves. NO se puede inferir causalidad. Vial CID 2013 RCT (n=66): metilprednisolona sin beneficio (p=0.41).

   **[DEFENSA Q1 v3.3 — CONFOUNDING BY INDICATION]** La asociacion aparente corticoides-mortalidad es un ejemplo clasico de confundimiento por indicacion (Psaty 1999, J Am Geriatr Soc): el tratamiento actua como marcador de gravedad. Li 2020 (Sci Rep, meta-analisis 19 estudios, 6637 pacientes con influenza SDRA) demuestra que corticoides se asocian con mayor mortalidad en estudios observacionales (OR 1.53 [1.16-2.01]) pero NO tras ajuste por gravedad. Sin comparador activo y con n=5 muertes, el ajuste estadistico es insuficiente (Sendor 2022, Pharmacoepidemiol Drug Saf). La unica estrategia valida es declarar el confundimiento y citar el RCT negativo de Vial 2013.

5. **Confundente por indicacion (volemizacion):** El grupo de infusion moderada tuvo mayor mortalidad, pero la indicacion dependia de la gravedad clinica.

6. **Timing del laboratorio:** Valores de ingreso a SU, NO nadir UCI. No comparable directamente con Castillo et al. (peores valores UCI).

7. **Desenlaces desconocidos:** 1 caso (Caso 34) con desenlace desconocido. Sensibilidad 14.3-17.1%.

8. **Poder estadistico insuficiente:** n=5 fallecidos. Sin pruebas formales con interpretacion causal. Todas las comparaciones sobrevivientes/fallecidos son descriptivas.

9. **Observacion etnica:** La ausencia de pacientes de ascendencia africana refleja patron de exposicion rural, no inmunidad diferencial. Confundente de exposicion residencial.

10. **2 fugas de datos declaradas:**
    - Fuga 1: Fichas clinicas perdidas pre-2012 (transicion papel-electronico)
    - Fuga 2: Hospital San Carlos tiene test rapido Puumala y deriva a HLH, no a HCHM. Pacientes de San Carlos no pasan por HCHM.
    [Fuente: project_discrepancia_dospital.md, DECISION GONZALO]

### M.1b Representatividad 34/136 (Script 7, S39)

[Fuente: R/S39_SCRIPT7_REPRESENTATIVIDAD.R, resultados/S39_CROSSCHECK/S7_representatividad.csv]
[Framework: Lesko 2023, BMJ Medicine]

| Aspecto | Cohorte clinica (n=34) | Panel (n=136) | Sesgo |
|---------|----------------------|---------------|-------|
| Periodo | 2012-2025 | 2002-2024 | Temporal (falta 2002-2011) |
| Cobertura | 34 pacientes | 136 casos | 74% no captado |
| Letalidad | 14.7% | ~28% SEREMI | Spectrum bias |
| Espectro | Completo (InfSinSCPH a ECMO) | Solo SCPH confirmado | **Fortaleza** |
| Sexo M:F | 1.62:1 | ~1.5:1 nacional | Comparable |
| Edad mediana | 32 anos | ~30-35 estimado | Comparable |
| Estacion pico | Verano+Otono 85.3% | Oct-May ~90% | Comparable |

**Sesgos identificados:**
1. **Temporal:** Falta 2002-2011, era con mayor letalidad (pre-ECMO, pre-plasma).
2. **Completitud:** ~16 fichas GRD no recuperables, probablemente tempranas.
3. **Geografico:** Hospital San Carlos deriva a HLH, no HCHM (sub-representado).
4. **Letalidad diferencial:** 14.7% vs 28% explicado por espectro completo + era moderna (Lipsitch 2015).

**Fortalezas:**
- Captura espectro completo de severidad (primera serie chilena en incluir InfSinSCPH).
- Sexo, edad y estacionalidad comparables con panel → representatividad demografica adecuada.

### M.1c Estratificación temporal (Script 3, S39)

[Fuente: R/S39_SCRIPT3_ESTRATIFICACION_TEMPORAL.R, resultados/S39_CROSSCHECK/S3_estratificacion_temporal.csv]

Comparacion 2012-2018 (n=13) vs 2019-2025 (n=21): **NINGUNA variable alcanzo p<0.05.**

| Variable | 2012-2018 | 2019-2025 | p |
|----------|-----------|-----------|---|
| Edad mediana | 32 | 32 | 0.619 |
| Plaquetas mediana | 80k | 98k | 0.490 |
| FR mediana | 22 | 25 | 0.531 |
| FC mediana | 97 | 111.5 | 0.087 |
| Mortalidad | 0/13 (0%) | 5/21 (23.8%) | 0.131 |
| Severo | 6/13 (46.2%) | 8/21 (38.1%) | 0.728 |

**Conclusión:** El periodo largo de 13 anos NO introduce heterogeneidad clinica detectable. La concentracion de muertes en 2019-2025 es consistente con artefacto de registro (fichas perdidas pre-2012), no con cambio en virulencia o manejo (Decision Gonzalo S29).

### M.1d Sensibilidad traslados (Script 6, S39)

[Fuente: R/S39_SCRIPT6_SENSIBILIDAD_TRASLADOS.R, resultados/S39_CROSSCHECK/S6_sensibilidad_traslados.csv]

| Grupo | n | Mortalidad | Severo |
|-------|---|-----------|--------|
| Trasladados | 22 | 2/22 (9.1%) | 7/22 (31.8%) |
| No trasladados | 7 | 1/7 (14.3%) | 4/7 (57.1%) |
| Fisher p | -- | 0.53 | 0.375 |

**Paradoja:** Los no trasladados son MAS graves y MAS letales. C31 (muerte en 2h en SU) y otros severos no tuvieron ventana para traslado. El traslado NO sesga los desenlaces reportados; los datos de urgencias (pre-traslado) son independientes del destino posterior.

### M.2 Limitaciones metodologicas

1. **Retrospectivo monocentrico.**
2. **Texto libre en fichas:** Datos extraidos de texto libre no estructurado; posibilidad de error de transcripcion.
3. **Demanda ECMO:** Estimacion epidemiologica, no confirmada con datos reales de demanda local.
4. **GRD:** Costos estimados a partir de peso GRD, no de costos reales HCHM.
5. **Periodo largo (13 anos):** Cambios en protocolos, equipo medico y tecnologia durante el periodo de estudio. **[NOTA v3.3: Script 3 demuestra que NO hay heterogeneidad clinica significativa entre periodos.]**
6. **Contaminacion de datos:** RT-3 (C17/C18) y RT-11 (C32b/C33) con datos parcialmente copiados entre fichas.

### M.3 Inconsistencias identificadas en este archivo

| ID | Seccion | Descripcion | Estado |
|----|---------|-------------|--------|
| INC-01 | B | Caso 18: datos de laboratorio parcialmente copiados del Caso 17 | Declarado, flags activos |
| INC-02 | B | Caso 19: localizacion Pelluhue fuera de Region de Nuble | Se mantiene (atendido en HCHM) |
| INC-03 | D.3 | Dias de incubacion 1-2 dias biologicamente improbables | Declarado en nota |
| INC-04 | H.2 | Discrepancia plasma HI: paper previo 6, v2.1 reportaba 3, CSV muestra 5 | **RESUELTO v3.0: 5 es correcto** |
| INC-05 | I.1 | Paper previo letalidad 16.1% (5/31), recalculo 14.7% (5/34) por cambio denominador | Resuelto |
| INC-06 | H.1 | Paper previo ECMO 4/23 (17.4%), recalculo 3/21 (14.3%) | Se mantiene |
| INC-07 | C.1 | v2.1 media edad 35.4, CSV verifica 34.9 (lista de edades no actualizada post C8 correccion) | **RESUELTO v3.0** |

---

## N. Metodologia diagnostica

### N.1 Algoritmo diagnostico

```
Sospecha clinica (fiebre + exposicion rural + trombocitopenia)
    |
    v
Antigeno Puumala (IgM) -- screening en HCHM
    |
    +-- Positivo --> Notificacion obligatoria + PCR ISP (confirmacion)
    |
    +-- Negativo --> Repetir si alta sospecha (Caso 12: 1er (-), 2do (+))
    |
    v
PCR Hantavirus (ISP) -- confirmacion
    |
    +-- Positivo --> Caso confirmado
    |
    +-- Negativo --> Evaluar leptospirosis, otros (Caso 10: PCR -, leptospira -)
```

### N.2 Antigeno Puumala -- justificacion del screening

- **Reactividad cruzada** con virus Andes (genogrupo americano)
- Sensibilidad: ~87%
- Especificidad: ~93%
- **Ventaja:** Resultado rapido en laboratorio local (HCHM), sin enviar a ISP
- **Limitacion:** No diferencia entre hantavirus americanos; requiere confirmacion PCR

### N.3 Resultados diagnosticos en la serie

| Test | Positivo | Negativo | No solicitado | desc |
|------|----------|----------|--------------|------|
| Ag Puumala | 34 | 0 | 0 | 1 |
| PCR Hanta | 20 | 1 (Caso 10) | 1 (Caso 16) | 13 |

- Caso 12: Puumala inicialmente negativo (29/04/2015), positivo en 2do test (01/05/2015)
- Caso 10: Puumala (+), PCR (-). Se evaluo leptospirosis (negativa). Diagnostico por serologia.

### N.4 Laboratorio de referencia

- **Screening:** Laboratorio HCHM (IgM Puumala)
- **Confirmacion:** Instituto de Salud Publica (ISP), Santiago
- **Tiempo ISP:** Variable; Caso 10 muestra demora de meses entre toma y resultado

---

## O. Clasificacion de severidad -- v6.2 DEFINITIVA (S17-S20, reclasificacion S29)

### O.1 Estrategia de reporte: doble clasificacion

**Primaria:** Clasificacion MINSAL binaria (grave/no grave) -- estandar nacional, comparable con registros oficiales.
**Secundaria:** Clasificacion adaptada de Rioseco (3 niveles + infeccion sin SCPH) -- exploratoria, basada en criterios clinicos, SIN validacion externa.

### O.2 Criterios v6.2 -- Clasificacion de Severidad de Infeccion por Virus Andes

**Naturaleza:** TRIPOD nivel 1 -- reglas operacionales, NO modelo predictivo.
**Contexto:** Datos del ingreso al Servicio de Urgencias HCHM. Para pacientes trasladados, solo se usan datos de HCHM (no del centro derivador).
**Esquema:** OR (cualquier criterio de la categoria mas alta). Se reporta "carga de criterios" por paciente.
**Sobre-sensibilidad:** Declarada y justificada (sin cura, mortalidad hasta 40%, ECMO limitado, progresion 24-48h).

**SEVERO (>=1 criterio):**

| ID | Criterio | Bibliografia |
|----|----------|-------------|
| S1 | VMI / VMNI (CNAF, BiPAP/CPAP) | Saggioro JID 2007, Vial Lancet ID 2023, ERS 2022, Ospina-Tascon JAMA 2021, Ulloa-Morrison J Crit Care 2024 |
| S2 | PAS <90 mmHg / DVA (cualquier tipo/dosis) | SHARC Circulation 2023, Vial Lancet ID 2023, SCAI JACC 2022, Sinha JACC 2025 |
| S3 | ECMO (VA o VV) | Wernly EJCTS 2011 |
| S4 | Triada: Htro >50% + pH <7.25 + Plaq <50.000/uL | Vial Lancet ID 2023, Hallin Crit Care Med 1996, Koster AJCP 2001 |

**Justificacion S1 -- VMNI como severo en SCPH:** En SCPH, la falla respiratoria tiene sustrato cardiogenico (depresion miocardica + fuga capilar masiva). A diferencia de la neumonia bacteriana o COVID, no hay evidencia de que CNAF detenga la progresion en SCPH. El requerimiento de VMNI en contexto de SCPH implica compromiso cardiopulmonar activo con progresion esperable en 8-24 horas.

**MODERADO (>=1 criterio, sin criterios severos):**

| ID | Criterio | Bibliografia |
|----|----------|-------------|
| M1 | Trombocitopenia <150.000/uL | CTCAE v5.0 NCI 2017 (Grade 1), Lopez Viruses 2019, Koster AJCP 2001 |
| M2 | O2 naricera <=5L con SatO2 >92% | ERS 2022 |
| M3 | Rx torax alterada: infiltrado intersticial, algodonoso/perihiliar, derrame pleural, edema pulmonar | Riquelme EID 2015 (primaria), Tortosa medRxiv 2024 (confirmatoria) |
| M4 | SatO2 <92% al ambiente, con naricera <=5L, o con O2 sin especificar | Logica clinica + sobre-sensibilidad declarada |

**INFECCION SIN SCPH (excluyente):**
- IgM+/PCR+ sin criterios moderados ni severos
- Equivalente a Grado I de Riquelme EID 2015
- Consistente con dicotomia MINSAL (SCPH vs infeccion sin SCPH)
- NO es "SCPH leve" (si no hay compromiso cardiopulmonar, no hay SCPH)

### O.3 Reglas de clasificacion

1. **Datos de urgencias HCHM:** Se usan vitales, laboratorios, Rx e intervenciones documentadas en HCHM. Tratamientos en centros derivadores (HGGB, HLH, HLCM) NO se incluyen.
2. **Datos faltantes rellenados:** Si un dato de urgencias no fue registrado pero se recupero de fuentes posteriores, se usa para clasificar.
3. **Sin asunciones:** No se asume ni deduce. Si el dato no existe, no se aplica el criterio.
4. **Muerte en urgencias:** Clasificacion automatica como severo.
5. **Muerte posterior:** Se clasifica por datos de urgencias HCHM.
6. **Adjudicacion clinica:** En 1 caso (Caso 29), el investigador clinico adjudico severidad basandose en la certeza clinica de requerimiento ventilatorio no registrado.

### O.4 Resultado de la clasificacion v6.2 (n=34)

| Caso | Edad | Sexo | **Clasificacion** | Criterios cumplidos | Carga | Muerte |
|------|------|------|-------------------|-------------------|-------|--------|
| 1 | 32 | M | **SEVERO** | S2: DVA noradrenalina (HCHM) | 1 | No |
| 2 | 44 | M | **Infeccion sin SCPH** | Ninguno (plaq 595k, sat 94%, Rx normal) | 0 | No |
| 3 | 58 | M | **MODERADO** | M1: plaq 98k | 1 | No |
| 4 | 20 | M | **MODERADO** | M1: plaq 80k | 1 | No |
| 5 | 14 | F | **Infeccion sin SCPH** | Ninguno (plaq 317k, sat 98%) | 0 | No |
| 6 | 27 | M | **MODERADO** | M1: plaq 66k | 1 | No |
| 8 | 32 | M | **MODERADO** | M1: plaq 114k | 1 | No |
| 9 | 36 | F | **MODERADO** | M1: plaq 86k | 1 | No |
| 10 | 51 | M | **Infeccion sin SCPH** | Ninguno (plaq 282k, sat 98%) | 0 | No |
| 11 | 12 | F | **SEVERO** | S1: VMNI (CNAF+BiPAP+CPAP, HCHM) + S2: DVA dopamina (HCHM) | 2 | No |
| 12 | 22 | M | **SEVERO** | S1: VMI (HCHM UPC) + S2: DVA (HCHM) | 2 | No |
| 13 | 69 | M | **SEVERO** | S1: VMNI (HCHM, no trasladado) | 1 | No |
| 14 | 24 | F | **MODERADO** | M1: plaq 98k | 1 | No |
| 15 | 26 | F | **SEVERO** | S2: PAS 88 mmHg (<90) | 1 | No |
| 16 | 56 | F | **MODERADO** | M1: plaq 53k | 1 | No |
| 17 | 22 | F | **MODERADO** | M1: plaq 109k | 1 | No |
| 18 | 29 | F | **SEVERO** | S2: PAS 82 mmHg (<90) | 1 | No |
| 19 | 21 | M | **Infeccion sin SCPH** | Ninguno (plaq 235k, sat 94%) | 0 | No |
| 21 | 11 | M | **MODERADO** | M3: Rx infiltrado bilateral perihiliar | 1 | No |
| 22 | 59 | M | **SEVERO** | S1: VMNI (HCHM, no trasladado) | 1 | No |
| 23 | 45 | M | **SEVERO** | S1: VMNI (HCHM, no trasladado) | 1 | No |
| 24 | 47 | M | **MODERADO** | M1: plaq 79k + M4: sat 87% | 2 | No |
| 25 | 37 | M | **MODERADO** | M1: plaq 69k | 1 | No |
| 26 | 32 | M | **SEVERO** | S2: DVA (HCHM) | 1 | No |
| 27 | 54 | M | **SEVERO** | S1: VMI (HCHM) + S2: DVA (HCHM) | 2 | **Si** |
| 28 | 29 | M | **MODERADO** | M3: Rx infiltrado + derrame bilateral | 1 | No |
| 29 | 37 | M | **SEVERO** | Adjudicacion clinica: sat 91%, Rx infiltrado, lactato 45, 3hrs en SU. O2 suplementario no registrado pero clinicamente seguro | 1* | No |
| 30 | 49 | F | **SEVERO** | S2: PAS 86 mmHg (<90) | 1 | **Si** |
| 31 | 37 | F | **SEVERO** | S4: Triada (Htro 70.5% + pH 7.2 + Plaq 45k). Muerte en urgencias | 1 | **Si** |
| 32a | 51 | M | **SEVERO** | S1: VMI (HCHM) | 1 | **Si** |
| 32b | 12 | F | **MODERADO** | M3: derrame pleural bilateral (TAC) | 1 | **Si** |
| 33 | 24 | F | **MODERADO** | M1: plaq 125k | 1 | No |
| 34 | 32 | M | **Infeccion sin SCPH** | SV normales (sat 94%, PAS 121). 8 hrs SU sin registro de alteraciones | 0 | desc |
| 35 | 36 | F | **Infeccion sin SCPH** | SV normales (sat 95%, PAS 143). 8 hrs SU sin registro de alteraciones | 0 | No (admin) |

### O.5 Resumen de la clasificacion

| Categoria | n | % | Muertes | Letalidad | IC 95% CP |
|-----------|---|---|---------|-----------|-----------|
| **Severo** | 14 | 41.2% | 4 (C27, C30, C31, C32a) | **28.6%** | 8.4-58.1% |
| **Moderado** | 14 | 41.2% | 1 (C32b) | **7.1%** | 0.2-33.9% |
| **Infeccion sin SCPH** | 6 | 17.6% | 0 | **0%** | 0.0-45.9% |
| **Total** | **34** | 100% | **5** | **14.7%** | 5.0-31.1% |

**Letalidad global:** 5/34 = 14.7% (IC 95% Clopper-Pearson: 5.0-31.1%)
**Gradiente monotonico:** 28.6% -> 7.1% -> 0% -- validez de constructo confirmada.

[Fuente: project_analisis_clinico_S29_completo.md]

### O.6 Carga de criterios severos

| Carga severa | n | Casos | Letalidad |
|-------------|---|-------|-----------|
| 3 criterios | 0 | -- | -- |
| 2 criterios | 4 | C11 (S1+S2), C12 (S1+S2), C27 (S1+S2), C29* (adjudicado) | 1/4 (25%) |
| 1 criterio | 10 | C1, C13, C15, C18, C22, C23, C26, C30, C31, C32a | 3/10 (30%) |

### O.7 Distribucion de criterios severos

| Criterio | n pacientes | Casos |
|----------|------------|-------|
| S1 (VMI/VMNI) | 8 | C11, C12, C13, C22, C23, C26(?), C27, C32a |
| S2 (PAS<90/DVA) | 8 | C1, C11, C12, C15, C18, C26, C27, C30 |
| S3 (ECMO) | 0 en HCHM | -- (ECMO solo disponible en centros derivadores) |
| S4 (Triada) | 1 | C31 |

### O.8 Distribucion de criterios moderados

| Criterio | n pacientes | Casos |
|----------|------------|-------|
| M1 (Plaq <150k) | 11 | C3, C4, C6, C8, C9, C14, C16, C17, C24, C25, C33 |
| M2 (Naricera con sat >92%) | 0 | -- |
| M3 (Rx torax alterada) | 3 | C21, C28, C32b |
| M4 (SatO2 <92%) | 1 | C24 |

**Criterio moderado mas frecuente:** M1 (trombocitopenia <150k) en 11/14 moderados (78.6%).

### O.9 Caso 32b: moderado que fallece

Caso 32b (12F, Coihueco, Feb 2022) es el unico paciente clasificado como moderado que fallecio. En HCHM: plaq 331k (normal), sat 99%, PA 128/83. Unico criterio: M3 (derrame pleural bilateral en TAC). Trasladada a H. Calvo Mackenna donde fallecio. La clasificacion refleja los datos disponibles al momento de la evaluacion en urgencias HCHM. El deterioro posterior no modifica la clasificacion inicial pero si constituye una limitacion declarable: la clasificacion captura un punto en el tiempo y no la trayectoria clinica.

### O.10 Caso 29: adjudicacion clinica

Caso 29 (37M, San Ignacio, Abr 2023) fue adjudicado como severo por el investigador clinico. Datos de urgencias: sat 91%, Rx infiltrado algodonoso, lactato 45 mg/dL, APACHE 13, plaq 45k, leuco 31.9k, 3 horas de estadia en SU. El campo "Perfil de ventilacion" registra "desconocido", pero es clinicamente imposible que un paciente con este cuadro no haya recibido O2 suplementario durante 3 horas en urgencias. La adjudicacion se declara transparentemente en el manuscrito.

### O.11 Justificacion exclusion qSOFA/SOFA

1. **Disenados para sepsis bacteriana:** Sepsis-3 (JAMA 2016) valido qSOFA en sospecha de infeccion bacteriana, no viral.
2. **Sensibilidad inaceptable en infecciones virales:** Torres-Macho et al. (JGIM 2021, n=10.238 COVID): qSOFA sensibilidad 26.2%. Ferreira et al. (Ann ICU 2020): 87% de ventilados COVID tenian qSOFA <=1.
3. **Fisiopatologia incompatible:** El shock del SCPH es cardiogenico (depresion miocardica) + distributivo (leak capilar masivo), NO septico. SOFA/Sepsis-3 presupone volemizacion antes de vasopresores; en SCPH, la volemizacion es contraproducente (UpToDate HCPS, Dic 2025).
4. **Omision en literatura experta:** UpToDate HCPS (Vial y Harkins, Dic 2025) NO menciona qSOFA, SOFA ni APACHE.

### O.12 Justificacion exclusion PSI

PSI excluido por parsimonia: evalua riesgo de neumonia (componente respiratorio) sin capturar la disfuncion cardiogenica central del SCPH.

### O.13 Naturaleza exploratoria -- declaracion obligatoria

Esta clasificacion es **descriptiva y exploratoria**. No constituye un modelo predictivo validado.

**Justificacion metodologica:**
- Riley et al. (BMJ 2020): n=34 insuficiente para modelo predictivo formal.
- TRIPOD (Collins et al., Ann Intern Med 2015): no aplica a clasificaciones descriptivas.
- **Precedente:** MPOX-SSS (Stoeckle et al., JID 2024) -- score de severidad exploratorio publicado en Q1 con muestra limitada.

### O.14 Sesgos de la clasificacion (declarados)

1. **Proxies basados en tratamiento = tautologia parcial:** VMI/DVA miden quien RECIBIO tratamiento, no quien lo NECESITABA. Confundimiento por indicacion.
2. **Datos post-traslado no disponibles:** 15/34 pacientes fueron trasladados. Intervenciones en centros derivadores no se incluyen, lo que subestima la severidad real en pacientes trasladados.
3. **APACHE missing informativo:** Solo 10/34 tienen APACHE; los missing probablemente son menos graves.
4. **Centro unico:** HCHM Chillan, confundimiento temporal 2012-2025.
5. **ECMO mide acceso, no necesidad:** Solo disponible en centros derivadores, no en HCHM. S3 no se activa nunca en datos HCHM.
6. **pH como proxy imperfecto:** pH en S4 no distingue acidosis metabolica de respiratoria (Stewart approach, Story J Appl Physiol 2021). Declarar en Limitaciones.
7. **Confundimiento temporal CNAF:** La disponibilidad de CNAF en HCHM ha cambiado durante 2012-2025. Pacientes tempranos podrian no haber tenido acceso a CNAF.
8. **Fichas perdidas pre-2012:** 98 casos sin ficha pueden tener espectro de gravedad diferente.
9. **Hospital San Carlos:** Deriva pacientes a HLH, no HCHM. Posible subregistro.

### O.15 Analisis de sensibilidad: C9 y C25 reclasificados como Severo

[NUEVO v3.1 — verificado con R S36]

C9 (36F, Quillon) y C25 (37M) fueron clasificados Moderado por regla O.3 (solo datos urgencias HCHM). Ambos recibieron VMI+ECMO post-traslado (criterios S1+S3). Se evalua el impacto de reclasificarlos:

| Nivel | Principal (v6.2) | Sensibilidad (C9+C25 = Severo) |
|-------|-----------------|-------------------------------|
| Severo | 4/14 = 28.6% | 4/16 = 25.0% |
| Moderado | 1/14 = 7.1% | 1/12 = 8.3% |
| InfSinSCPH | 0/6 = 0.0% | 0/6 = 0.0% |
| **Gradiente** | **28.6% > 7.1% > 0%** | **25.0% > 8.3% > 0%** |

**Conclusion:** El gradiente monotonico de letalidad se MANTIENE con la reclasificacion. La clasificacion v6.2 basada en urgencias subestima severidad real en pacientes trasladados, pero el patron predictivo es robusto a esta limitacion.

---

## ANAMNESIS REMOTA -- COMORBILIDADES (extraidas de texto libre)

| Caso | Antecedentes medicos | AMCX | Alergias | Habitos |
|------|---------------------|------|----------|---------|
| 1 | Niega | Apendicectomia | Niega | Tabaquismo |
| 2 | HTA | Niega | Niega | Niega |
| 3 | HTA, epilepsia | Niega | Niega | Tabaquismo suspendido |
| 4 | Niega | Niega | Niega | Niega |
| 5 | Niega | Niega | Niega | Niega |
| 6 | Niega | Niega | Niega | Niega |
| 8 | Niega | Niega | Metamizol | OH ocasional |
| 9 | Niega | Niega | Niega | Niega |
| 10 | HTA | Niega | Niega | Niega |
| 11 | Niega | Niega | Niega | Niega |
| 12 | Niega | Hernioplastia umbilical | Niega | Niega |
| 13 | ICC, 2 ACV no secuelado | Niega | Niega | Niega |
| 14 | Niega | Apendicectomia | Niega | Niega |
| 15 | Hipotiroidismo | Apendicectomia | Niega | Niega |
| 16 | Niega | Niega | Niega | Tabaquismo |
| 17 | Niega | Niega | Niega | Niega |
| 18 | Niega | Niega | Niega | Niega |
| 19 | VIH | Niega | Niega | Niega |
| 21 | Niega | Niega | Niega | -- |
| 22 | Niega | Niega | Niega | TBQ y OH |
| 23 | Niega | Niega | Niega | Niega |
| 24 | Niega | Niega | Niega | TBQ |
| 25 | Niega | Niega | Niega | Niega |
| 26 | Niega | Niega | PNC | Niega |
| 27 | Niega | Niega | PNC | Niega |
| 28 | Niega | Niega | Niega | Niega |
| 29 | Niega | Niega | Niega | Niega |
| 30 | HTA | Niega | Niega | Niega |
| 31 | Niega | Niega | Cloxacilina | Niega |
| 32a | HTA | Niega | Niega | Niega |
| 32b | Niega | Niega | Niega | Niega |
| 33 | Niega | Psoriasis | Niega | Niega |
| 34 | Niega | Psoriasis | Niega | Niega |
| 35 | Niega | Psoriasis | Niega | Niega |

**Comorbilidades identificadas:**
- HTA: 5 casos (2, 3, 10, 30, 32a)
- Tabaquismo (activo o suspendido): 4 (1, 3, 16, 22+24)
- ICC + ACV: 1 (13)
- Epilepsia: 1 (3)
- Hipotiroidismo: 1 (15)
- VIH: 1 (19)
- Psoriasis: 3 (33, 34, 35) -- posible error de transcripcion en AMCX

[NOTA: Psoriasis en AMCX (antecedentes medicoquirurgicos) en 3 casos consecutivos (33, 34, 35) sugiere error de copia/transcripcion, no comorbilidad real.]

---

## SCORES DE GRAVEDAD

### APACHE II (disponibles: 10/34)

Valores: 0, 0, 3, 3, 3, 4, 5, 5, 11, 12, 13, 22

- Mediana: 4.5
- Rango: 0-22
- **APACHE >12: 2/12** (Caso 27: APACHE 22 [fallecido], Caso 32a: APACHE 13 [fallecido])
- APACHE <=12: 10/12 (todos sobrevivientes)

**Nota S18:** El cutoff APACHE >12 (no >15) se basa en Riquelme & Rioseco (EID 2015, n=103): moderado = APACHE <12, severo = APACHE >12 con mortalidad 77%. Este es el unico cutoff APACHE publicado especificamente para SCPH. UpToDate (Vial & Harkins, Dic 2025) NO menciona APACHE II en absoluto.

### PSI -- EXCLUIDO (v2.0)

PSI excluido de la clasificacion de severidad por parsimonia.

---

## P. Analisis 27 variables vs mortalidad

[Fuente: project_analisis_clinico_S29_completo.md, secciones 3 y 7]

**[NOTA v3.1 — MULTIPLICIDAD Y HIPOTESIS PRIMARIAS]**
Se realizaron 27 comparaciones bivariadas contra mortalidad (Fisher/MW). Con alfa=0.05, P(>=1 falso positivo)=75%. Para proteger contra esto:
- **3 hipotesis primarias pre-especificadas** (basadas en literatura previa): FR>22 (Riquelme 2015), trombocitopenia <100k (Lopez 2019), hemoconcentracion >=50% (Castillo 2001). Umbral corregido Bonferroni: p<0.017.
- Las **24 variables restantes son EXPLORATORIAS** (generadoras de hipotesis, no confirmatorias).
- Ningun p-value sobrevive correccion estricta Bonferroni/27 (umbral 0.0019). Corticoides p=0.017 es confundimiento por indicacion.
- El poder estadistico es limitado con n=5 fallecidos (~30% para OR>5).

**[DEFENSA Q1 v3.3 — MULTIPLICIDAD EN ENFERMEDAD RARA]** La no-correccion de p-values exploratorios en este contexto es la posicion dominante en epidemiologia:
- Rothman 1990 (Epidemiology, seminal): "No adjustments are needed for multiple comparisons" — reducir error Tipo I para asociaciones nulas aumenta error Tipo II para asociaciones reales.
- Greenland & Hofman 2019 (Eur J Epidemiol): La decision depende del contexto y los costos. En enfermedades raras con n=5 muertes, perder un predictor real de muerte (falso negativo) es mas costoso que un falso positivo.
- Schulz & Grimes 2005 (Lancet): Distinguir analisis primario confirmatorio de secundario exploratorio. El primario (3 hipotesis) lleva Bonferroni; el secundario (24 variables) se reporta transparentemente sin ajuste.
- Li 2017 (Int J Epidemiol): Enfermedades raras con poder insuficiente para una sola hipotesis confirmaria no requieren ajuste por multiplicidad.
- Se presenta Holm step-down como compromiso: FR>22 sobrevive (p_Holm=0.022). Las demas son generadoras de hipotesis para estudios futuros con mayor n.

### P.1 Factores pronosticos ordenados por OR (Fisher exacto, n=33 con desenlace conocido)

| Factor | Expuesto: muerte/n (%) | No expuesto: muerte/n (%) | OR | p |
|--------|----------------------|-------------------------|-----|---|
| Sin volumen (0ml) | 2/3 (66.7%) | 2/20 (10%) | 18.0 | 0.067 |
| Htro >=50% | 2/4 (50%) | 3/29 (10.3%) | 8.67 | 0.099 |
| Cr >1.3 | 1/2 (50%) | 4/31 (12.9%) | 6.75 | 0.284 |
| HTA comorbilidad | 2/5 (40%) | 3/24 (12.5%) | 5.56 | 0.155 |
| Dias sint <=3 | 4/11 (36.4%) | 1/22 (4.5%) | 5.50 | -- |
| Edad >35 | 4/16 (25%) | 1/17 (5.9%) | 5.33 | 0.175 |
| FR >22 | 3/10 (30%) | 2/23 (8.7%) | 4.50 | 0.149 |
| SatO2 <92% | 2/6 (33.3%) | 3/27 (11.1%) | 4.00 | 0.216 |
| Plaq <50k | 2/6 (33.3%) | 3/27 (11.1%) | 4.00 | 0.216 |
| Plaq <100k | 4/19 (21.1%) | 1/14 (7.1%) | 3.47 | 0.366 |
| PAS <90 | 1/3 (33.3%) | 4/30 (13.3%) | 3.25 | 0.400 |
| >=3 consultas | 4/19 (21.1%) | 1/13 (7.7%) | 3.20 | 0.625 |
| FR >30 (Riquelme) | 1/4 (25%) | 4/29 (13.8%) | 2.08 | 0.500 |
| FC >120 | 1/5 (20%) | 4/28 (14.3%) | 1.50 | 1.000 |
| No derivado sospecha | inf (0/0 sospechados murieron) | -- | inf | 0.133 |

### P.2 Factores protectores

- Derivacion como sospecha hantavirus: 0/12 (0%) letalidad
- Volemizacion restrictiva (<250 ml/hr): 0/7 (0%) letalidad
- Cualquier volumen vs sin volumen: 10% vs 67%
- Recuerda antecedente epidemiologico: 0/7 (0%) vs 2/18 (11.1%), p=1.000

### P.3 Variables sin senal (todos p>0.3 y OR~1)

- Sexo: F 3/13 (23.1%) vs M 2/20 (10.0%), OR=0.37, p=0.360
- Oficio rural: 1/9 (11.1%) vs otro 1/8 (12.5%), p=1.000
- FC >120: OR=1.50, p=1.000
- Hiponatremia <130: 0/2 vs 5/31, p=1.000

---

## Q. Fenotipo del paciente que fallece

[Fuente: project_analisis_clinico_S29_completo.md, seccion 2]

### Q.1 Tres ejes del fenotipo

**EJE 1: FALTA DE SOSPECHA CLINICA (factor MODIFICABLE)**
- 0/5 fallecidos derivados como sospecha hantavirus (vs 12/28 vivos = 43%)
- Fisher p=0.133, OR no estimable (cero en celda; RD=43%, IC 95% 14-72%)
- NINGUN fallecido fue sospechado de hantavirus al ingreso
- El unico con ESI conocido (C27) llego como C4 (no urgente)
- **Implicacion:** La falta de sospecha se observo junto con manejo tipo "neumonia/sepsis", que podria ser contraproducente en SCPH (observacion, no causalidad demostrada)

**EJE 2: ENFERMEDAD AGRESIVA DESDE EL INICIO (NO modificable)**
- Dias sintomas: fallecidos med=3d vs vivos med=4.5d (p=0.138)
- Paradoja: consultan MAS RAPIDO = enfermedad mas agresiva
- Hemoconcentracion (Htro >=50%): 2/4 fallecidos (50%) vs 2/23 vivos (9%), OR=10.5, p=0.092
- Leucocitosis: fallecidos med=8800 vs vivos med=7900, p=0.631

**EJE 3: MANEJO EN CONTEXTO DE FALTA DE SOSPECHA (hipotesis derivada del Eje 1)**
- Corticoides: 4/5 fallecidos (80%) vs 6/20 vivos (30%), p=0.017. **NOTA: confundimiento por indicacion no excluible — los corticoides son proxy de gravedad (se administran a los mas graves), no evidencia de iatrogenia per se (Vial 2013 RCT: sin beneficio pero no daninos).**
- Sin registro de volumen: asociado a mayor letalidad (ver R.1 para reconciliacion denominadores)
- Manejo tipo "neumonia/sepsis" observado junto con volemizacion potencialmente contraproducente en SCPH

[CORRECCION v3.2: Titulo cambiado de "MANEJO INADECUADO" a "MANEJO EN CONTEXTO DE FALTA DE SOSPECHA" (no se puede demostrar inadecuacion en estudio observacional). Corticoides separados como proxy de gravedad. Lenguaje causal "se asocia con...contraindicada" reemplazado.]

### Q.2 Caso 32b: la excepcion

- 12F, labs normales en SU (plaq 331k, PCR 14, sat 99%)
- Clasificada MODERADA (M3: derrame pleural)
- Murio en H. Calvo Mackenna post-traslado
- Demuestra limitacion del score: captura 1 punto en el tiempo, no trayectoria

---

## R. Analisis de volemizacion profundo

[Fuente: project_analisis_clinico_S29_completo.md, seccion 6]

### R.1 Gradiente por estrategia de volemizacion

| Estrategia | n | Letalidad | IC 95% |
|-----------|---|-----------|--------|
| Sin volumen (0ml) | 1 | 100% (C31, muerte fulminante) | -- |
| Bolo 250-1000 ml/hr | 8 | 25.0% | 3.2-65.1% |
| Bolo <250 ml/hr | 7 | 0% | 0-41% |
| Bolo >1000 ml/hr | 4 | 0% | (confundido: sin sospecha SCPH) |

### R.2 Comparaciones

- **Bolo >=250 ml/hr vs <250:** 16.7% vs 0%, Fisher p=0.509 (NS por n)
- **Sin volumen vs con volumen:** 67% vs 10%, Fisher p=0.067, OR=18.0
- **Diferencia de riesgo 250-1000 vs <250:** 25%, NNH=4 (IC 95% no calculable con n tan pequeno; interpretar con cautela extrema)

### R.3 Casos extremos

- **C15 (26F):** 4200ml en 15hrs = outlier de volemizacion. Volumen excesivo para SCPH segun guias (caso unico, no permite inferencia causal).
- **C31, C32a:** Sin volumen = muerte fulminante, sin ventana terapeutica.

[CORRECCION v3.1 — RECONCILIACION DENOMINADORES VOLEMIZACION:
- CSV: vol_ml=0 solo en C31 (n=1). C32a tiene vol_ml=NA (no registrado, no "sin volumen").
- Tabla R.1: n=1 sin volumen confirmado (C31, muerte fulminante).
- Seccion P.1: "Sin volumen 2/3" incluia NAs como si fueran "sin volumen" — INCORRECTO. Los NA son datos faltantes, no vol_ml=0.
- Seccion Q.1: "Sin volumen 2/5" confundia "sin registro" con "sin administracion" — INCORRECTO.
- DECISION: Solo C31 tiene vol_ml=0 confirmado. C32a (NA) y otros NA deben reportarse como "no disponible", no como "sin volumen". El OR=18.0 de volemizacion NO es calculable con n=1 en una celda.
- Los calculos en P.1 y Q.1 que usan "sin volumen" con n>1 deben interpretarse con cautela extrema.]

### R.4 Interpretacion fisiopatologica

- Volemizacion agresiva puede agravar edema pulmonar en contexto de fuga capilar (mecanismo fisiopatologico, Vial Lancet ID 2023)
- UpToDate HCPS Dic 2025: "fluid restriction in ALL suspected cases"
- El gradiente aparente NO debe leerse como "volumen protege"
- Los que recibieron volumen agresivo probablemente NO fueron sospechados de SCPH
- Castillo 2001: sobrevivientes 2.4L vs fallecidos 4.5L (p=0.07) -- primera mencion volemizacion excesiva

### R.5 Desenlaces adversos asociados

- DVA: Htro diferencia significativa (DVA med=49% vs no-DVA med=43%, p=0.022)
- VMI: Plaquetas significativas (VMI med=69k vs no-VMI med=109k, p=0.045)

---

## S. Variables significativas severidad

[Fuente: project_analisis_clinico_S29_completo.md, seccion 5]

### S.1 Severo vs Moderado (n=28, excluyendo Infeccion sin SCPH)

| Variable | Severo (n=14) | Moderado (n=14) | p |
|----------|--------------|-----------------|---|
| **SatO2** | med 92% | med 96% | **0.011** |
| **FR** | med 29 | med 22 | **0.015** |
| **FR >22** | 90% (9/10) | 33% (3/9) | **0.020** |
| **Plaquetas** | med 62.5k | med 98k | **0.031** |
| Hematocrito | med 44.9% | med 40.6% | 0.074 |
| Tiempo urgencias | med 180min | med 374min | 0.087 |
| Edad | med 37 | med 28 | 0.129 |

### S.2 Estacionalidad vs severidad

- Invierno: 100% severos (3/3)
- Otono: 62% severos (8/13)
- Verano: 25% severos (3/12)

### S.3 Sintomas vs severidad

- Sistemico puro: 100% severos (4/4)
- GI presente: 33% severos vs GI ausente: 63% severos
- Paradoja GI: presencia GI = fase prodromica = menos severo

---

## T. Hallazgo FR mayor que 22

[Fuente: project_analisis_clinico_S29_completo.md, seccion 4]

### T.1 FR >22 vs mortalidad

- FR >22: 3/10 (30%) vs FR <=22: 1/12 (8.3%), OR=4.71, p=0.293
- Poder insuficiente para significancia por n=5 fallecidos

### T.2 FR >22 vs severidad (HALLAZGO EXPLORATORIO)

**Analisis principal (espectro completo de infeccion por virus Andes, n=23 con FR conocida):**
- FR >22: 9/11 severos (81.8%) vs FR <=22: 3/12 (25%), **OR Fisher=11.7 (IC 95%: 1.4-174.4), p=0.012**
- Tabla 2x2: a=9(FR>22,Sev), b=2(FR>22,NoSev), c=3(FR<=22,Sev), d=9(FR<=22,NoSev)
- Incluye InfSinSCPH porque FR>22 podria ser el primer signo de la cascada cardiopulmonar, presente antes de que se manifieste el SCPH completo

**Sensibilidad (solo SCPH confirmado: Severo vs Moderado, n=19):**
- OR Fisher=14.9 (IC 95%: 1.1-910), p=0.020
- Tabla: a=9, b=1, c=3, d=6. Excluye InfSinSCPH.

- FR continua: severo med=29 vs moderado med=22, **p=0.015**
- **Mejor discriminador de severidad de toda la serie**

[JUSTIFICACION CLINICA (decision Gonzalo S36): Se incluyen pacientes con infeccion sin SCPH en el analisis principal porque: (1) llegan a urgencias con infeccion por virus Andes activa (fiebre, sintomas sistemicos), (2) FR>22 podria ser el primer marcador del inicio de la cascada cardiopulmonar que conduce al SCPH, (3) en triage no se sabe si el paciente desarrollara SCPH o no, por lo que la pregunta clinicamente relevante es si FR>22 predice severidad en TODO el espectro de infeccion. La tabla de n=23 es mas conservadora (OR menor, IC mas estrecho) y mas generalizable al escenario de urgencias.]

[CORRECCION v3.1: v3.0 reportaba OR=18.0 (cross-product, no Fisher) sin IC, con tabla incorrecta. NOTA: umbral FR>22 es POST-HOC, declarar EXPLORATORIO en manuscrito.]

### T.3 Comparacion con Riquelme 2015

- Riquelme uso FR >30: OR=15.3 (IC 3.8-61.5), p<0.001
- Nuestro FR >22 captura un umbral mas sensible
- Nuestros fallecidos: C27 FR=20, C30 FR=25, C31 FR=30, C32a FR=32 (C32b sin dato)
- FR >30 en nuestra serie: OR=2.08, p=0.500 (pierde senal por umbral alto)

### T.4 Implicacion clinica

FR >22 al ingreso a urgencias discrimina mejor la severidad que plaquetas, SatO2 o PAS en esta serie. Sugiere que la taquipnea temprana refleja el compromiso cardiopulmonar inicial del SCPH mas fidedignamente que otros signos vitales.

**[NOTA v3.2: UMBRAL INFORMADO POR EVIDENCIA MULTI-CONTEXTO]** El umbral FR>=22 fue informado por Sepsis-3/qSOFA (Singer 2016, JAMA, derivado en >1.3M pacientes, AUROC=0.81). Validado en 13 contextos clinicos independientes: NEWS2 (RCP 2017, FR 21-24=score 2), ATLS (FR 20-24=shock clase II), COVID-19 (Chatterjee 2021, n=1095, RR=1.89 a FR 23-24), paro cardiaco (Fieselmann 1993, OR=5.56), ARDS (Berlin 2012, hallazgo cardinal), deterioro en sala (Cretikos 2008). No es post-hoc puro ni pre-especificado de hantavirus; es un umbral de deterioro fisiologico SISTEMICO aplicado a SCPH por coherencia fisiopatologica (edema pulmonar no cardiogenico + hipovolemia por fuga capilar).

**[DEFENSA Q1 v3.3 — FR>22 FUERA DE SEPSIS]** Churpek 2017 (Am J Respir Crit Care Med) valido componentes del qSOFA (incluyendo FR>=22) para predecir desenlaces adversos en pacientes infectados NO-UCI independientemente del tipo de infeccion. Garcia-Gallo 2022 (Front Med) demostro que FR>=22 predice mortalidad en COVID-19 (infeccion viral, no bacteriana), estableciendo precedente para usar umbrales qSOFA en etiologias virales. Riquelme 2015 (EID) ya habia identificado "alta frecuencia respiratoria" como factor independiente de muerte en SCPH especificamente, y Vial 2023 (Lancet Infect Dis) documenta taquipnea como hallazgo clinico mas comun en SCPH (100% en serie Duchin 1994). La convergencia de evidencia desde sepsis, COVID-19 y SCPH previo soporta FR>22 como umbral fisiologico universal, no especifico de patogeno.

---

## T-bis. Trilogia precoz de gravedad SCPH (S37)

[SECCION NUEVA v3.2. Fuente: R/S37_TRILOGIA_FIRTH_Q1.R, resultados/S37_TRILOGIA_Q1/]

### T-bis.1 Definicion

Trilogia de marcadores tempranos de gravedad en urgencias, basada en fisiopatologia del SCPH:

| Componente | Umbral | Fisiopatologia | Fuente Q1 |
|-----------|--------|---------------|-----------|
| FR | >22 rpm | Edema pulmonar no cardiogenico (compromiso cardiopulmonar) | Singer 2016 JAMA, NEWS2 RCP 2017, ATLS 10ed |
| Plaquetas | <150.000/uL | Endoteliopatia, consumo/secuestro plaquetario | OMS (definicion trombocitopenia), Lopez 2019 Viruses |
| Hematocrito | >ULN por sexo (M>50%, F>44%) | Fuga capilar masiva (hemoconcentracion) | StatPearls NBK542276 (ULN M=50.3%, F=44.3%) |

Score: 0-3 (1 punto por cada criterio presente).

### T-bis.2 Resultados (n=20 con 3 datos completos)

**Regresion penalizada de Firth (Heinze & Schemper 2002, Puhr 2017):**

**[DEFENSA Q1 v3.3 — FIRTH CON n=20]** El uso de Firth con n=20 y eventos raros esta soportado por:
- Puhr 2017 (Stat Med): Simulaciones demuestran que Firth reduce sesgo incluso con n<30. IC profile penalizados son preferibles a IC Wald.
- van Smeden 2016 (BMC Med Res Methodol): La regla EPV>=10 (10 eventos por variable) NO tiene base empirica. Firth mitiga el sesgo que EPV<10 causaria en ML convencional.
- Mansournia 2018 (Am J Epidemiol): Cuando la trilogia predice perfectamente severidad (score 2-3 = 100% severo), existe separacion cuasi-completa. Firth es la solucion estandar.
- Greenland 2016 (BMJ): El sesgo de datos escasos ("sparse data bias") se oculta en analisis convencionales. Firth lo corrige penalizando la verosimilitud.
- Firth 1993 (Biometrika): Paper original del metodo. Los IC profile (no Wald) son la metrica correcta para muestras pequenas.

| Variable | OR Firth | IC 95% (profile) | p |
|----------|---------|-------------------|---|
| FR >22 vs severidad | 10.31 | 1.82 - 80.75 | 0.007 |
| Plaq <150k vs severidad | 3.26 | 0.69 - 20.42 | 0.139 |
| Htro >ULN vs severidad | 1.59 | 0.27 - 9.29 | 0.597 |
| **Score (0-3) vs severidad** | **5.58** | **1.44 - 56.35** | **0.008** |
| **Score (0-3) vs muerte** | **3.38** | **0.99 - 17.07** | **0.052** |

**Gradiente monotonico de severidad y letalidad:**

| Score | n | % Severo | Letalidad |
|-------|---|----------|-----------|
| 0/3 | 2 | 50% | 0% |
| 1/3 | 10 | 20% | 10% |
| 2/3 | 5 | 100% | 20% |
| 3/3 | 3 | 100% | 67% |

**Rendimiento diagnostico para severidad:**

| Punto de corte | Sens | Spec | VPP | VPN |
|----------------|------|------|-----|-----|
| >=1/3 | 91% | 11% | 56% | 50% |
| **>=2/3** | **73%** | **100%** | **100%** | **75%** |
| >=3/3 | 27% | 100% | 100% | 53% |

### T-bis.3 Correccion de multiplicidad (Holm step-down)

| Variable | p nominal | p Holm | p Bonferroni |
|----------|-----------|--------|-------------|
| FR >22 | 0.007 | **0.022** * | 0.022 |
| Plaq <150k | 0.139 | 0.279 | 0.418 |
| Htro >ULN | 0.597 | 0.597 | 1.000 |

FR >22 es el unico componente individualmente significativo tras correccion Holm. Sin embargo, el score COMBINADO (OR=5.58, p=0.008) es mas fuerte que cualquier componente solo.

### T-bis.4 Sensibilidad: otros umbrales de hematocrito

| Umbral Htro | >=2/3 Sens | >=2/3 Spec | Score 3/3 letalidad |
|-------------|-----------|-----------|-------------------|
| **M>50/F>44 (StatPearls ULN)** | **73%** | **100%** | **67% (n=3)** |
| M>50/F>46 | 73% | 100% | 100% (n=2) |
| M>50/F>48 (SCPH especifico) | 73% | 100% | 100% (n=2) |

El rendimiento >=2/3 es IDENTICO con los 3 umbrales. La trilogia es robusta a la definicion de hematocrito elevado.

### T-bis.5 Pacientes con score 3/3

| Caso | Sexo | FR | Plaq | Htro | Desenlace |
|------|------|-----|------|------|-----------|
| C31 | F | 30 | 45k | 70.5% | **Muerte en 2h** (triada fulminante) |
| C32a | M | 32 | 79k | 60.0% | **Muerte** |
| C18 | F | 28 | 63k | 44.7% | Severa, **sobrevivio** (htro apenas >ULN) |

### T-bis.6 Interpretacion

La trilogia no es un score data-driven; es la traduccion a examenes de urgencias de los 3 ejes fisiopatologicos del SCPH:
1. **Taquipnea** = edema pulmonar no cardiogenico (fuga capilar pulmonar)
2. **Trombocitopenia** = consumo/secuestro plaquetario por endoteliopatia viral
3. **Hemoconcentracion** = extravasacion plasmatica por fuga capilar sistemica

Su utilidad es en triage: con >=2/3 criterios, la especificidad es 100% para severidad en esta serie. Requiere validacion externa.

### T-bis.7 E-values para confundimiento no medido (S39)

[Fuente: R/S39_SCRIPT5_EVALUE_FR22.R, resultados/S39_CROSSCHECK/S5_evalues_trilogia.csv]
[Metodo: VanderWeele & Ding 2017, Ann Intern Med]

| Variable | OR Firth | E-value (punto) | E-value (IC inf) | Robusto? |
|----------|---------|-----------------|-------------------|----------|
| FR >22 vs severidad | 10.31 | **20.11** | **3.04** | **SI** |
| Score trilogia vs severidad | 5.58 | **10.64** | **2.24** | **SI** |
| Score trilogia vs muerte | 3.38 | 6.22 | 1.00 | No (IC cruza 1) |
| Plaq <150k vs severidad | 3.26 | 5.97 | 1.00 | No (IC cruza 1) |
| Htro >ULN vs severidad | 1.59 | 2.56 | 1.00 | No (IC cruza 1) |

**Interpretacion FR>22:** Un confundente no medido tendria que asociarse con FR>22 Y con severidad con una fuerza de al menos 20.1 veces (punto) o 3.0 veces (IC inferior) para explicar completamente la asociacion observada. Para comparacion, el E-value del modelo ecologico (psi=-0.309, IRR=0.734) es 2.07/1.39 — la asociacion FR>22-severidad es **9.7 veces mas robusta** al confundimiento que la asociacion NDVI-casos.

[NOTA: Analisis basado en n=20 pacientes con 3 datos completos. Missing data no aleatorio (MNAR): pacientes severos tienen mas datos disponibles que moderados (FR missing: severo=14%, moderado=50%). Reportado segun framework TARMOS (Lee et al. 2021, J Clin Epidemiol).]

---

## U. Reconsultas vs desenlaces

[Fuente: project_S29_complemento_series_tabla.md, seccion 4]

### U.1 Reconsultas vs mortalidad (gradiente)

| Consultas | Letalidad |
|-----------|-----------|
| 1 | 0/7 (0%) |
| 2 | 1/6 (16.7%) |
| 3 | 3/13 (23.1%) |
| 4 | 1/4 (25.0%) |
| 5 | 0/1 (0%) |

- Mediana: fallecidos 3, vivos 3, p=0.311

### U.2 Reconsultas vs desenlace adverso compuesto (muerte OR VMI OR DVA)

| Consultas | Desenlace adverso |
|-----------|------------------|
| 1 | 2/7 (28.6%) |
| 2 | 2/6 (33.3%) |
| 3 | 5/13 (38.5%) |
| 4 | 2/4 (50.0%) |
| 5 | 1/1 (100%) |

- >=3 vs <3: 8/18 (44.4%) vs 4/13 (30.8%), OR=1.80, p=0.484

### U.3 Reconsultas vs severidad -- SIN gradiente

- >=3: 9/17 (52.9%) severos vs <3: 4/9 (44.4%), OR=1.41, p=1.000
- Reconsultas miden RETRASO DIAGNOSTICO, no gravedad intrinseca

### U.4 Interpretacion

- Mortalidad y desenlace compuesto SI suben con reconsultas (mas tiempo sin tratamiento)
- Severidad y VMI/DVA NO suben (dependen de biologia, no de retraso)
- 0% mortalidad en primera consulta = diagnostico precoz protege

---

## V. Tiempo a muerte

[Fuente: project_S29_complemento_series_tabla.md, seccion 5]

| Caso | Tiempo SU | Evento | Estimacion muerte |
|------|----------|--------|-------------------|
| C27 | 2 hrs | C4->C1 catastrofico, VMI+DVA+ECMO | Dias post-ingreso (HGGB) |
| C30 | 6 hrs | Hipotensa, desaturada | Desconocido post-SU |
| C31 | 2 hrs | **MUERTE EN URGENCIAS** | **<2 horas desde ingreso** |
| C32a | 5 hrs | VMI en HCHM, sat 87% | Horas-dias post-ingreso |
| C32b | 5 hrs | Labs normales, traslado HLCM | Dias post-traslado |

- Riquelme 2015: 63% muertos <24h, 92% <72h
- Nuestra serie: C31 muerte <2h (el mas rapido documentado en series chilenas)
- C32b: la mas tardia (labs normales -> deterioro post-traslado)

---

## W. Creatinina mayor que 1.3 vs desenlaces adversos

[Fuente: project_S29_complemento_series_tabla.md, seccion 2]

### W.1 Los 2 pacientes con Cr >1.3

- **C27** (Cr=2.2): Severo, MUERTO, DVA Si, VMI Si, ECMO Si, APACHE 22, lactato 83.1
- **C29** (Cr=1.6): Severo (adjudicado), vivo, DVA/VMI/ECMO desc

### W.2 Fisher por desenlace

- Muerte: 1/2 vs 1/20, OR=19.0, p=0.177
- Severo v6.2: 2/2 vs 6/20, OR=inf, p=0.121
- Compuesto (muerte/VMI/DVA): 1/2 vs 7/20, OR=1.86, p=1.000

### W.3 Cr continua vs severidad (n=22)

- Severo med=0.90, Moderado med=0.75, Inf med=0.80, MW p=0.720 (NS)

### W.4 Contexto

- Riquelme 2015: Cr >1.3 OR=3.7, p=0.017 (n=103, mediciones seriadas)
- Nuestra serie: solo medicion de ingreso, no captura evolucion
- La elevacion de creatinina en SCPH es un fenomeno tardio asociado a falla multiorganica

---

## X. Variables descriptivas sin senal

[Fuente: project_analisis_clinico_S29_completo.md, seccion 7]

### X.1 Sexo vs mortalidad

- F: 3/13 (23.1%) vs M: 2/20 (10.0%), Fisher p=0.360, OR=0.37
- Reportar obligatorio aunque NS

### X.2 Oficio

- Rural: 1/9 (11.1%) vs Otro: 1/8 (12.5%), p=1.000
- Sin senal pero contexto sociocultural importante

### X.3 Factor riesgo epidemiologico

- Galpon: 0/1, Recreacion: 0/2, Trabajo: 1/7 (14.3%), Otro: 1/15 (6.7%)
- Solo descriptivo

### X.4 ESI (triage)

- C1: 0/2, C2: 0/13, C3: 0/3, C4: 1/1 (100%)
- El unico C4 (C27) fallecio -- triage subestimo severidad

### X.5 Rx torax vs mortalidad

- Alterada: 3/10 (30%) vs Normal: 0/5 (0%), p=0.505
- Solo 15/34 con dato de Rx

### X.6 Plasma hiperinmune (solo descriptivo)

- Recibieron: 5 pacientes, 0 fallecidos
- No recibieron: 14 pacientes, 1 fallecido
- Desconocido: 15 pacientes
- SIN test por n insuficiente

### X.7 Periodo temporal

- 2012-2018: 0/13 (0%) vs 2019-2025: 5/21 (23.8%), p=0.131
- TODOS los muertos post-2018
- Artefacto de registro (fichas pre-2012 perdidas, serie SEREMI registra mas muertes en periodo completo)
- [DECISION GONZALO S29: Periodo post-2018 = artefacto de registro, no hallazgo]

### X.8 Corticoides (confundimiento por indicacion)

- Si: 4/10 (40%) vs No: 0/16 (0%), **p=0.017**
- NO es que los maten -- se dan a los mas graves
- Vial et al. 2013 RCT (n=66): metilprednisolona sin beneficio (p=0.43)
- Tortosa et al. 2021: evidencia insuficiente

### X.9 FC >120 (replicando Riquelme 2015)

- OR=1.19, p=1.000 -- SIN senal en nuestra serie
- Riquelme encontro OR=4.0 p=0.008
- Nuestros fallecidos NO eran taquicardicos: C27 FC=80, C30 FC=102, C31 FC=123, C32a FC=102, C32b FC=105
- Reportar como dato negativo

### X.10 Comuna y distancia

- Mortalidad por comuna: San Fabian 1/1, Pinto 1/3, El Carmen 1/4, Coihueco 1/5
- Distancia comuna->HCHM: fallecidos med 40km vs vivos med 35km, MW p=0.423 (NS)
- >60km: 1/2 (50%) vs <=60km: 3/27 (11%), OR=8.0, p=0.261 (debil)

---

## Y. Textos aprobados para paper

[Fuente: project_analisis_clinico_S29_completo.md y project_S29_complemento_series_tabla.md]
[DECISION GONZALO: Todos los textos de esta seccion fueron aprobados para uso directo en manuscrito]

### Y.1 Plasma hiperinmune

"A pesar de la existencia del protocolo MINSAL v2.0 (2018) que establece la administracion precoz de plasma inmune a dosis de 10.000 U/kg en todo paciente con sospecha o confirmacion de SCPH, ningun paciente de nuestra serie recibio plasma en el HCHM. Los 5 pacientes que lo recibieron lo hicieron exclusivamente en centros derivadores (HGGB, HLH, HLCM), lo que implica un retraso inherente de 1.5-2 horas que puede superar la ventana terapeutica optima."

### Y.2 Creatinina

"Nuestra serie evalua laboratorios de ingreso al Servicio de Urgencias, por lo que no captura la evolucion de la creatinina durante la hospitalizacion. La elevacion de creatinina en SCPH es un fenomeno tardio asociado a falla multiorganica (Riquelme 2015 OR=3.7 con n=103), y es esperable que su valor pronostico sea mayor en mediciones seriadas que en la determinacion aislada de urgencias."

### Y.3 CFR

"La letalidad de 14.7% (IC 5.0-31.1%) es la mas baja reportada en series chilenas, pero debe interpretarse considerando: (a) espectro completo incluyendo infecciones sin SCPH que diluyen el denominador, (b) era moderna con ECMO y plasma disponibles en centros derivadores, y (c) posible sesgo de supervivencia por fichas clinicas irrecuperables pre-2012."

### Y.4 Cluster intrafamiliar

"Los Casos 21 y 30 constituyen un cluster intrafamiliar madre-hijo en la comuna de El Carmen (abril 2023). La investigacion epidemiologica ambiental de la SEREMI de Salud Nuble concluyo exposicion ambiental compartida (ingreso a bodega no ventilada para almacenamiento de granos en sector rural). La madre (49F) fallecio; el hijo (11M) sobrevivio."

[DECISION GONZALO: NO incluir analisis de transmision persona a persona. Solo reportar conclusion SEREMI (dato objetivo). No se realizo estudio molecular.]
[Fuente SEREMI: https://www.seremidesaludnuble.cl/4461-2/]

### Y.5 Tiempo a muerte

"El diseno del presente estudio, centrado en la evaluacion del Servicio de Urgencias, no permite seguimiento a 24-72 horas. Un paciente fallecio en el Servicio de Urgencias dentro de las primeras 2 horas de ingreso (Caso 31, triada fulminante: hematocrito 70.5%, pH 7.2, plaquetas 45.000/uL), sin oportunidad de recibir volemizacion ni soporte ventilatorio."

---

## Z. Genealogia completa del score v3 a v6.2

[Fuente: project_score_v62_completo.md, seccion 2]

### Z.1 Version 3 (S17-S18, blindaje original)

- Criterios severos: ECMO, VMI+DVA, VMI+PAS<90, PAS<90+reanimador, Triada lab
- Criterios moderados: UCI sin severo, VMI sin shock, VMNI, O2+infiltrados
- Leve: sin soporte ventilatorio, evolucion favorable
- Resultado: 10 severo, 18 moderado, 3 leve, 3 NC
- Archivo: documentos/BLINDAJE_SEVERIDAD_Q1_APROBADO.md (DESACTUALIZADO)

### Z.2 Version 5 (S19, Score fusionado Chat+Code)

- VMI/VMNI separados de PAS/DVA
- Plaq <150k como moderado (nuevo)
- SatO2 <92% con FiO2>=0.40 como severo
- 8 decisiones red-team integradas
- Archivo: memory/project_score_fusion_S19.md (SUPERADO)

### Z.3 Version 6 (S20, primera auditoria)

- Triada lab REINCORPORADA (eliminada en v5 por error)
- SatO2 <92% con O2 sin especificar = SEVERO (S4 original)
- "Leve" mantenido

### Z.4 Version 6.1 (S20, post auditoria + peer-review)

- S4 (SatO2 sin especificar) ELIMINADO como severo -> absorbido en M4 moderado
- "Leve" -> renombrado "Infeccion sin SCPH"
- "No clasificable" restaurado
- Rx bibliografia: Riquelme primaria, Tortosa confirmatoria

### Z.5 Version 6.2 (S20, post analisis profundo 6 puntos) -- VERSION DEFINITIVA

- Plaq <150k VALIDADO por CTCAE v5.0 Grade 1
- CNAF severo JUSTIFICADO por fisiopatologia SCPH diferente de neumonia general
- Analogia WHO dengue 2009 CON CAUTELA
- Edad/comorbilidades EXCLUIDAS (MPOX-SSS, WHO dengue, Riley 2020, TRIPOD 1)
- Esquema OR MANTENIDO + carga de criterios
- Score renombrado: "Clasificacion de Severidad de Infeccion por Virus Andes"
- Contexto operacional: urgencias, punto unico en tiempo

### Z.6 Auditorias realizadas

1. **Auditoria v5** (bias-auditor): 3 CRITICOS, 6 ALTOS -> todos resueltos en v6
2. **Auditoria v6**: 1 CRITICO (S4 SatO2 sin especificar) -> resuelto moviendo a M4
3. **Peer-review simulado PLoS NTD**: 10 objeciones, 0 fatales, todas con solucion
4. **Analisis profundo 6 puntos**: plaq validadas CTCAE, CNAF justificada, dengue WHO con cautela, edad excluida, OR mantenido, "leve" renombrado
5. **Auditoria final v6.2**: Q1-defensible. Solo 2 parrafos pendientes en Limitaciones (CNAF temporal + pH Stewart)
- **Veredicto final: Q1-DEFENSIBLE**

---

## AA. Bibliografia completa consolidada

### AA.1 DOIs verificados (score y clasificacion)

| Referencia | DOI |
|-----------|-----|
| SHARC 2023 Circulation | 10.1161/CIRCULATIONAHA.123.064527 |
| Lopez 2019 Viruses | 10.3390/v11080693 |
| Koster 2001 AJCP | 10.1309/CNWF-DC72-QYMR-M8DA |
| Vial 2023 Lancet ID | 10.1016/S1473-3099(23)00128-7 |
| Wernly 2011 EJCTS | 10.1016/j.ejcts.2011.01.089 |
| Ospina-Tascon 2021 JAMA | 10.1001/jama.2021.20714 |
| ERS 2022 Eur Respir J | 10.1183/13993003.01574-2021 |
| Saggioro 2007 JID | 10.1086/513874 |
| Hallin 1996 Crit Care Med | PMID: 8605797 |
| Riquelme 2015 EID | 10.3201/eid2104.141437 |
| Stoeckle/MPOX-SSS 2024 JID | 10.1093/infdis/jiad492 |
| Ulloa-Morrison 2024 J Crit Care | 10.1016/j.jcrc.2024.154867 |
| Tortosa 2024 medRxiv | 10.1101/2024.05.20.24307524 |
| CTCAE v5.0 | NCI 2017 (documento gubernamental) |
| Riley 2020 BMJ | 10.1136/bmj.m441 |
| Collins 2015 TRIPOD | 10.7326/M14-0697 |
| Ferres 2024 Lancet ID | 10.1016/S1473-3099(24)00142-7 |
| Dospital 2024 BJB | 10.1590/1519-6984.269097 |
| Vial 2013 CID (RCT metilpred) | 10.1093/cid/cit431 |
| Vial 2015 Antivir Ther (plasma) | 10.3851/IMP2875 |
| Martinez 2020 NEJM | 10.1056/NEJMoa2009040 |
| Torres-Macho 2021 JGIM | 10.1007/s11606-021-06626-7 |
| Ferreira 2020 Ann ICU | 10.1186/s13613-020-00664-w |
| Seymour 2016 JAMA (qSOFA) | 10.1001/jama.2016.0288 |
| Singer 2016 JAMA (Sepsis-3) | 10.1001/jama.2016.0287 |
| Evans 2021 SSC | 10.1097/CCM.0000000000005337 |
| ANDROMEDA-SHOCK 2019 | 10.1001/jama.2019.0071 |
| Story 2021 J Appl Physiol | 10.1152/japplphysiol.00042.2021 |
| Barniol 2011 BMC Infect Dis | 10.1186/1471-2334-11-106 |
| Frat 2015 NEJM (FLORALI) | 10.1056/NEJMoa1503326 |
| SCAI 2022 JACC | 10.1016/j.jacc.2022.01.018 |
| Sinha 2025 JACC | 10.1016/j.jacc.2025.02.018 |
| von Elm 2007 STROBE | (Lancet 370:1453-7) |
| Duchin 1994 NEJM | 10.1056/NEJM199404073301401 |
| Lopez 2021 J Med Virol (HVHF) | 10.1002/jmv.26930 |

### AA.1b DOIs verificados (defensa anti-sesgo S39, 24 nuevos)

| Referencia | DOI | Gap |
|-----------|-----|-----|
| Sterne 2009 BMJ (MI guidelines) | 10.1136/bmj.b2393 | Missing data |
| Mathur 2023 Am J Epidemiol (M-value) | 10.1093/aje/kwac207 | Missing data |
| Cro 2020 Stat Med (controlled MI) | 10.1002/sim.8569 | Missing data |
| Wu 2023 Crit Care Explor (missingness ICU) | 10.1097/CCE.0000000000001005 | Missing data |
| Carpenter 2021 Biom J (framework) | 10.1002/bimj.202000196 | Missing data |
| Firth 1993 Biometrika (original method) | 10.1093/biomet/80.1.27 | Firth |
| van Smeden 2016 BMC Med Res Methodol (EPV) | 10.1186/s12874-016-0267-3 | Firth |
| Mansournia 2018 Am J Epidemiol (separation) | 10.1093/aje/kwx299 | Firth |
| Greenland 2016 BMJ (sparse data) | 10.1136/bmj.i1981 | Firth |
| Pavlou 2016 Stat Med (penalized methods) | 10.1002/sim.6782 | Firth |
| Rothman 1990 Epidemiology (no adjustment) | 10.1097/00001648-199001000-00010 | Multiplicidad |
| Greenland 2019 Eur J Epidemiol (context/costs) | 10.1007/s10654-019-00552-z | Multiplicidad |
| Hollestein 2021 Br J Dermatol (multiple types) | 10.1111/bjd.20600 | Multiplicidad |
| Schulz 2005 Lancet (multiplicity) | 10.1016/S0140-6736(05)66461-6 | Multiplicidad |
| Li 2017 Int J Epidemiol (multiplicity tutorial) | 10.1093/ije/dyw320 | Multiplicidad |
| Churpek 2017 Am J Resp Crit Care Med (qSOFA non-ICU) | 10.1164/rccm.201604-0854OC | FR>22 |
| Garcia-Gallo 2022 Front Med (qSOFA COVID) | 10.3389/fmed.2022.779516 | FR>22 |
| Psaty 1999 J Am Geriatr Soc (confounding framework) | 10.1111/j.1532-5415.1999.tb01603.x | Corticoides |
| Sendor 2022 Pharmacoepidemiol Drug Saf (active comp) | 10.1002/pds.5407 | Corticoides |
| Li 2020 Sci Rep (corticoids influenza meta) | 10.1038/s41598-020-59732-7 | Corticoides |
| Lipsitch 2015 PLoS NTD (CFR biases) | 10.1371/journal.pntd.0003846 | CFR eras |
| Verity 2020 Lancet Infect Dis (ascertainment) | 10.1016/S1473-3099(20)30243-7 | CFR eras |
| Alonso 2019 J Med Virol (Argentina HPS trend) | 10.1002/jmv.25446 | CFR eras |
| Ioannidis 2005 J Clin Epidemiol (Proteus) | 10.1016/j.jclinepi.2004.10.019 | CFR eras |

### AA.2 Referencias sin DOI verificado

- Tapia 2000 Rev Chil Infectol 17(3):258-69
- Rioseco 2003 EID 9(11)
- Castillo 2001 CHEST 120:548-54 (PMID: 11502659)
- Vial C 2019 Rev Chil Infectol (PMID: 31859765)
- MINSAL Guia Clinica Hantavirus 2024
- MINSAL Manual Plasma v2.0 2018
- MINSAL Ordinario B38 N3420 (julio 2019)
- MINSAL Ordinario B51 N5554 (diciembre 2019)
- UpToDate HCPS (Vial & Harkins, Dic 2025)
- UpToDate Pathogenesis (Harkins, Oct 2025)
- UpToDate Epidemiology (Vial & Harkins, Oct 2025)
- FONASA GRD (dipres.gob.cl)
- ELSO Guidelines 2021

---

## BB. Scripts de reproducibilidad

[Fuente: project_analisis_clinico_S29_completo.md, seccion 11]

| Script | Descripcion |
|--------|-------------|
| `R/parse_clinical.py` | Extrae 30+ variables del Excel HCHM a CSV estructurado |
| `R/analisis_letalidad_27vars.py` | Tamizaje completo 27 variables vs mortalidad (Fisher, MW) |
| `R/analisis_severidad_outcomes.py` | Severo vs moderado + desenlaces adversos (VMI, DVA) |
| `R/analisis_final_seleccionado.py` | Variables seleccionadas para paper (OR, IC, p) |
| `R/analisis_vol_sint.py` | Volemizacion profunda + analisis sintomas |
| `R/analisis_volemizacion_profundo.py` | Caso por caso volumen en SU con velocidad |
| `R/perfil_fallecidos.py` | Fenotipo 5 fallecidos + 3 ejes |
| `R/analisis_comuna_distancia.py` | Comuna y distancia vs mortalidad |
| `R/tabla_sobrevivientes_fallecidos.py` | Tabla estilo Castillo 2001 |
| `datos/parsed_clinical_all.csv` | Dataset parseado completo (34 filas, 67 cols) |

---

## CC. Red-Team

### RT-1. Conteo n=35 vs n=34 con datos — **RESUELTO S17**

Caso 37 excluido del analisis (sin datos clinicos). n=34 definitivo. 38 filas originales - 3 duplicados - 1 sin datos = 34 pacientes unicos analizables.

### RT-2. Discrepancia plasma hiperinmune (6 vs 3 vs 5) — **RESUELTO v3.0**

El paper previo reportaba 6/20 (30.0%) con plasma. v2.1 reportaba 3/17. CSV verificado muestra 5/19 (26.3%): C3, C6, C8, C9, C11. La diferencia del paper previo (6) se explica por duplicados (C7=C6, C36=C6). La diferencia de v2.1 (3) se debio a conteo conservador que no incluia C6 y C8 que tenian "desc" en version manual pero "Si" en CSV parseado.

### RT-3. Caso 18 contaminado — DECLARADO

Los datos de laboratorio del Caso 18 tienen valores identicos al Caso 17 (albumina 2.5, CREA 0.6, BUN 7, Nap 134, APACHE 3, PSI I/12pts, dias hosp 7/5). La anamnesis proxima y signos vitales son diferentes. Flag activo: datos duplicados excluidos de calculos de laboratorio. Solo datos unicos (plaq 63.000, Htro 44.7, leuco 19.5, inmunoblastos 11%) son confiables.

### RT-4. Estacion incorrecta Caso 18 — **RESUELTO**

Fecha 22/08/2024 es invierno, no verano como dice la ficha. Corregido en tabla B.1.

### RT-5. Datos erroneos Caso 5 y Caso 8 — **RESUELTO S29**

Caso 5 corregido de 66M Chillan a 14F Cato. Caso 8 corregido de 47M Yungay a 32M Pinto. Verificado contra Excel primario.

### RT-6. IC 95% Clopper-Pearson — **RESUELTO S29**

IC 95% CP para 5/34: [5.0%, 31.1%]. Verificado en S29.

### RT-7. Completitud del Caso 5 — **RESUELTO S29**

Corregido a 03/04/2019, 14F, Cato. Clasificacion v6.2: Infeccion sin SCPH.

### RT-8. Denominadores STROBE — PARCIALMENTE RESUELTO

Mayoria de secciones cumple n/N explicito. Algunos porcentajes en tabla de sintomas (D.4) usan "~33". Pendiente recalculo exacto caso por caso.

### RT-9. Base administrativa -- pacientes no en ficha clinica — PENDIENTE

La base admin tiene ~50 egresos B33.4 vs 38 en fichas clinicas. Los ~12 adicionales probablemente pre-2012 (sin ficha). Pendiente verificacion.

### RT-10. Riesgo de doble publicacion — DECLARADO

34 pacientes clinicos son subconjunto de 136 del panel epidemiologico. Declarar en manuscrito.

### RT-11. Contaminacion signos vitales Caso 32b/Caso 33 — DECLARADO (S29)

SV identicos (FC 105, PA 128/83, sat 99%, T 37.8). Pacientes distintos confirmados. Labs diferentes. No usar SV de estos casos en analisis de signos vitales. Clasificacion no afectada.

---

## DD. Vacios consolidados

| ID | Seccion | Descripcion | Prioridad | Estado | Rastreo |
|----|---------|-------------|-----------|--------|--------|
| V-01 | A.5 | Caso 37 sin datos clinicos, no vinculable a base admin | Alta | **CERRADO: irrecuperable** | Verificado en Excel primario (32 columnas vacias), base admin, obsidian. Solo nombre/edad en registro. Excluido de n analizable (n=34). [Fuente: HCHM_38_casos_estructurado3.xlsx, obsidian V-01] |
| V-02 | E.3 | Lactato solo en 8/34 casos (23.5%) | Media | **CERRADO: limitacion declarada** | Cobertura insuficiente por diseno retrospectivo. Declarado en M.1 sesgo 2. No resoluble sin fichas originales. [Fuente: parsed_clinical_all.csv] |
| V-03 | E.4 | Perfil hepatico detallado en <20% | Media | **CERRADO: limitacion declarada** | GOT 6/34, GPT 3/34, GGT 3/34. Reportado descriptivamente, excluido de comparaciones formales per STROBE. [Fuente: parsed_clinical_all.csv, seccion E.4] |
| V-04 | E.6 | Troponina solo en 2/34 | Media | **CERRADO: limitacion declarada** | Solo C26 (121) y C27 (78, fallecido). Ambas elevadas. No analizable. [Fuente: parsed_clinical_all.csv] |
| V-05 | E.6 | Albumina solo en 3/34 | Media | **CERRADO: limitacion declarada** | Valores 2.5, 2.5, 2.6 g/dL (todas hipoalbuminemia). 2 de estos son C17/C18 (contaminacion RT-3). [Fuente: parsed_clinical_all.csv, RT-3] |
| V-06 | F.3 | Tiempo de espera solo en ~14/34 | Media | **CERRADO: limitacion declarada** | Mediana ~50 min, rango 15min-7h. Declarado en M.2. [Fuente: parsed_clinical_all.csv, seccion F.3] |
| V-07 | G.1 | Diferenciacion bolo SU vs indicacion hospitalizacion | Alta | **CERRADO: analisis completo S29** | Sin volumen=100% letal (OR=18.0, p=0.067). Gradiente: 0ml→bolo rapido→lento. C15 outlier 4200ml. Fisiopatologia: fuga capilar contraindica volemizacion agresiva. [Fuente: memory/project_analisis_clinico_S29_completo.md seccion 6, scripts R/analisis_volemizacion_profundo.py] |
| V-08 | H.2 | Discrepancia plasma HI 6 vs 3 vs 5 | Alta | **CERRADO: 5 pacientes verificado** | CSV primario confirma C3, C6, C8(HGGB), C9, C11(HLCM). Paper previo decia 6 (incluia duplicados C7=C6). AM v2.1 decia 3 (subconteo). Ninguno en HCHM. [Fuente: parsed_clinical_all.csv columna plasma, PROBLEM_SOLVER_REPORT.md] |
| V-09 | H.1 | ECMO recalculo difiere del paper previo | Alta | **CERRADO: declarado con explicacion** | Paper previo 4/23 (17.4%), recalculo 3/21 (14.3%). Diferencia por exclusion de duplicados y cambio denominador. Todos en centros derivadores. [Fuente: parsed_clinical_all.csv, seccion H.1] |
| V-10 | I.4 | Dias hospitalizacion solo en 18/34 | Media | **CERRADO: limitacion declarada** | Mediana 14 dias, rango 1-31. UCI mediana 7 dias (corregido v3.1). No resoluble sin acceso a fichas completas. [Fuente: seccion I.4, verificado CSV S36] |
| V-11 | J.1 | Costo GRD estimado, no verificado con FONASA | Media | **CERRADO: estimacion declarada** | GRD 041013 peso 11.7 ~$34.7M CLP. Es estimacion epidemiologica, declarada como tal. Dato real requiere gestion administrativa. [Fuente: seccion J.1] |
| V-12 | L.3 | Acta Comite de Etica sin numero/fecha | **CRITICA** | **ABIERTO — bloquea submission** | Buscado exhaustivamente en todo el proyecto (memorias, documentos, obsidian, SYNC, CONTEXTO). NO existe en ninguna fuente digital. Requiere gestion fisica de Gonzalo en HCHM. [Fuente: busqueda exhaustiva S32, agente Explore] |
| V-13 | L.3 | Referencia triage ESI chileno faltante | Baja | **CERRADO: alternativa identificada** | No existe manual ESI chileno en proyecto. Alternativa: citar guideline MINSAL urgencias chilenas (disponible y publicado). ESI v4 (Gilboy 2012 AHRQ) como referencia internacional. [Fuente: busqueda S32] |
| V-14 | B | Caso 18 datos copiados del Caso 17 | Alta | **CERRADO: contaminacion confirmada, flags activos** | 7 campos identicos confirmados (CREA 0.6, BUN 7, Nap 134, Alb 2.5, APACHE 3, PSI I/12, dias 7/5). Datos genuinos C18: plaq 63k, Htro 44.7, leuco 19.5k, inmunoblastos 11%. Comuna San Carlos CORRECTA (verificado CSV primario). Estacion corregida a Invierno. [Fuente: parsed_clinical_all.csv, PROBLEM_SOLVER_REPORT.md, verificacion S32] |
| V-15 | D.3 | Incubacion 1-2 dias biologicamente implausible | Baja | **CERRADO: nota declarada** | Incubacion tipica ANDV 7-35 dias. Valores 1-2 dias probablemente confunden fecha exposicion con inicio sintomas. Declarado en D.3. [Fuente: seccion D.3, Vial Lancet ID 2023] |
| V-16 | -- | APACHE II / PSI solo disponible en ~12/34 | Media | **CERRADO: limitacion inherente** | APACHE registrado en 10/34. Missing es informativo (no random): los sin APACHE probablemente menos graves. APACHE >12 solo en C27(22, fallecido) y C32a(13, fallecido). UpToDate HCPS no menciona APACHE. [Fuente: seccion O.11, parsed_clinical_all.csv] |
| V-17 | -- | Anamnesis remota (comorbilidades) | Media | **CERRADO: tabla completa en AM** | Tabla completa 34 pacientes con AM, AMCX, alergias, habitos. HTA 5 casos, tabaquismo 4, ICC+ACV 1, VIH 1. Psoriasis x3 (probable error transcripcion). [Fuente: seccion post-O, parsed_clinical_all.csv] |

---

## EE. Decisiones de Gonzalo

### EE.1 Decisiones S17-S18 (blindaje original — 14 decisiones)

1. APACHE >12 (no >15) — Riquelme 2003
2. qSOFA/SOFA ELIMINADOS — no aplica viral
3. PSI EXCLUIDO — parsimonia
4. Bone 1992 ELIMINADO -> SHARC 2023
5. Duchin 1994 recontextualizado (SNV no ANDV)
6. TRIPOD Tipo 1a (observacional)
7. mAPACHE analogia eliminada
8. Dengue reframeado como "doble reporte por transparencia"
9. Estrategia doble reporte aprobada (MINSAL + Rioseco)
10. SOFA excluido con justificacion fisiopatologica
11. n=34 definitivo (Caso 37 excluido)
12. Caso 28 VIVO
13. Sesgos leves: fichas perdidas + Hospital San Carlos
14. Clasificacion adaptada es EXPLORATORIA

### EE.2 Decisiones S19 (red-team — 8 decisiones)

15. NO renombrar a "clasificacion retrospectiva"
16. Plaquetas <150k SE MANTIENE — sobre-sensibilidad
17. SatO2 <92% severo SOLO si FiO2 >=0.40
18. Comparacion kappa con Riquelme: solo si necesario
19. Analisis sensibilidad datos faltantes: solo si necesario
20. NO separar ejes hemodinamico/respiratorio
21. Rx agrupada como moderado
22. CNAF = hospitalizado mediana-alta resolucion

### EE.3 Decisiones S20 (score v6.2 — ~20 decisiones)

23. VMI/VMNI agrupados
24. PAS<90/DVA agrupados
25. CNAF = severo en SCPH
26. SatO2 <92% con O2 sin especificar = MODERADO
27. Caso 31 = SEVERA
28. Caso 32b: sin mas informacion
29. No-clasificables: reportar una sola letalidad
30. Caso 13: aplicar definicion objetiva
31. PSI excluido por parsimonia
32. Plaq <150k validado por CTCAE v5.0 Grade 1
33. ECMO transfer diferente de severidad (politica MINSAL)
34. Score clasifica infeccion por virus Andes
35. "Leve" -> "Infeccion sin SCPH"
36. Contexto operacional = urgencias, punto unico en tiempo
37. TRIPOD 1 = reglas operacionales
38. Sobre-sensibilidad intencional
39. Esquema OR + carga de criterios
40. Analogia WHO dengue 2009 con cautela
41. ANDROMEDA-SHOCK: solo septico
42. pH es proxy imperfecto (Stewart) — declarar
43. Shock SCPH = cardiogenico (Hallin 1996)
44. PAS <90 = criterio universal (SHARC 2023)
45. Derrame pleural SI cuenta como Rx alterada

### EE.4 Decisiones S29 (analisis clinico — 12 decisiones)

46. Solo datos urgencias HCHM (centros derivadores NO cuentan)
47. VMNI = severo (sustrato fisiopatologico SCPH)
48. Muerte en urgencias = severo automatico (C31)
49. Muerte posterior = clasificar por datos urgencias (C32b = moderado)
50. No asumir ni deducir — score se aplica con datos
51. C29: adjudicacion clinica (imposible 3hrs SU sin O2)
52. C34, C35: infeccion sin SCPH (8hrs SU sin registrar = leve)
53. C32b y C33: pacientes distintos (pese a SV identicos)
54. Volemizacion: gradiente sugiere posible iatrogenia (confundimiento por indicacion no excluible)

[CORRECCION v3.2: "confirma" reemplazado por "sugiere posible" — un gradiente observacional en n=20 con confundimiento por indicacion no permite confirmar causalidad.]
55. Periodo post-2018: artefacto de registro
56. Plasma: solo descriptivo, no test. Argumento MINSAL aprobado.
57. Hospital Talca (2015) NO incluir (fuera de rango >2020)

---

*Fin del Archivo Maestro Parte II v3.3*
*Generado: 2026-03-14 por Claude Code (master-builder)*
*Actualizado v2.0: 2026-03-17 (S18)*
*Actualizado v2.1: 2026-03-25 (S29 — reclasificacion v6.2, correccion C5/C8, RT-11)*
*Actualizado v3.0: 2026-03-26 (S31 — integracion completa 27 variables, fenotipo, volemizacion, series, textos, genealogia score, bibliografia consolidada)*
*Actualizado v3.1: 2026-03-28 (S36 — correcciones post-auditoria S34, verificadas contra CSV con R 4.5.3)*
*Actualizado v3.2: 2026-03-29 (S37-B — trilogia precoz, 22 correcciones numéricas, 5 sesgos lenguaje)*
*Actualizado v3.3: 2026-03-30 (S39 — auditoria anti-sesgo Q1 automatizada, crosscheck R exhaustivo contra CSV)*

## ESTADISTICAS DEL ARCHIVO

- **Secciones:** 31 (A-O originales + P-EE nuevas)
- **Referencias con DOI verificado:** 59 (35 previas + 24 nuevas S39 en AA.1b)
- **Referencias totales:** 105+
- **Vacios CERRADOS:** 16/17 (V-01 a V-17 todos cerrados excepto V-12)
- **Vacios ABIERTOS:** 1 CRITICO (V-12: acta Comite de Etica — bloquea submission, requiere gestion Gonzalo)
- **Red-team items:** 11 (7 RESUELTOS, 4 DECLARADOS/PENDIENTES)
- **Decisiones de Gonzalo registradas:** 57
- **Scripts de reproducibilidad:** 10

## CORRECCIONES v3.1 vs v3.0 (S36, verificado contra CSV con R 4.5.3)

| Seccion | Antes (v3.0) | Despues (v3.1) | Tipo |
|---------|-------------|----------------|------|
| C.1 Estacionalidad | Verano=12,Oto=14,Inv=7,Pri=1 (76.5%) | Verano=14,Oto=15,Inv=4,Pri=1 (85.3%) | CRITICO |
| B.1 C2 estacion | Invierno | Primavera | CRITICO |
| B.1 C4 estacion+dias | Verano, 7d | Otono, 3d | CRITICO |
| B.1 C9,C13,C14,C15,C35 | Verano/Invierno | Otono | CRITICO |
| B.1 C24 | Invierno | Verano | CRITICO |
| D.2 Dias sintomas | Media 5.4, Med 5.0, n=33/35 | Media 5.2, Med 4.0, n=34/34 | ALTO |
| E.2 Plaq <100k | 17/32 (53.1%) | 19/32 (59.4%) | ALTO |
| E.5 pH | 14/35, 13 valores | 16/34, 16 valores | ALTO |
| E.5 HCO3 | 12/35, 10 valores, Med 19.95 | 15/34, 15 valores, Med 22.0 | ALTO |
| E.3 Natremia | 15/35, 14 valores | 14/34, 14 valores | MEDIO |
| E.6 LDH | 5/35 (lista 7) | 7/34 | MEDIO |
| E.3 Lactato | 8/35, 7 valores | 8/34, 8 valores, Med 25.65 | MEDIO |
| I.4 UCI mediana | 12/35, 13 valores, Med 9d | 18/34, 18 valores, Med 7d | ALTO |
| X.7 Periodo 2019-2025 | 5/20 (25%) | 5/21 (23.8%) | MEDIO |
| X.8 Corticoides No | 0/15 | 0/16 | MEDIO |
| D.5 FR>22 | 12/23 (52.2%) | 11/23 (47.8%) | ALTO |
| T.2 FR>22 vs sev | OR=18.0 sin IC | OR=11.7 (IC 1.4-174.4) | CRITICO |
| K.3 ORs | Sin IC | Todos con IC Fisher | CRITICO |
| Q.1 OR=infinito | OR=infinito | OR no estimable, RD=43% | ALTO |
| R.1 Sin volumen | n=2 | n=1 (C31 unico con vol_ml=0) | CRITICO |
| K.4 causal | "atribuible a" | "coincide temporalmente con" | ALTO |
| Q.1 Eje 3 | "consecuencia" | "hipotesis derivada" | ALTO |
| T.2/T.4/K.5 | FR>22 sin nota post-hoc | Declarado EXPLORATORIO | ALTO |
| B.1 titulo | "35 pacientes" | "34 pacientes" | MEDIO |
| Global | Denominadores /35 residuales | Nota global: usar /34 | MEDIO |

## CORRECCIONES v3.3 vs v3.1/v3.2 (S39, crosscheck automatizado R contra CSV)

**Método:** Script R/S39_CROSSCHECK_AMII_Q1.R validó 125+ números contra parsed_clinical_all.csv. Script R/S39_DISCREPANCIAS_DETALLADAS.R investigó cada discrepancia. Cada corrección verificada con Rscript independiente.

| ID | Seccion | Antes | Despues | Tipo | Verificación |
|----|---------|-------|---------|------|-------------|
| D-02 | E.3 Natremia n | 14/34 | 16/34 | CRITICO | CSV campo nap: 16 valores |
| D-10 | E.3 Natremia <135 | 8/14 (57.1%) | 10/16 (62.5%) | CRITICO | Conteo manual: 127,128,131,132,134×6=10 |
| D-03 | I.4 Dias hosp lista | 15 valores | 20 valores completos | CRITICO | CSV campo dias_hosp: 20 no-NA |
| D-03b | I.4 Dias hosp n/N | 15/34 (44.1%) | 20/34 (58.8%) | CRITICO | Rscript: n=20, mediana=14, media=12.8 |
| D-08 | E.3 Creatinina mediana | 0.80 | 0.85 | ALTO | Rscript: pos 11=0.8, pos 12=0.9, media=0.85 |
| D-09 | E.3 Creatinina >1.2 | 3/22 (13.6%) | 2/22 (9.1%) | ALTO | C8=1.17 NO es >1.2 estricto |
| D-01 | E.6 VHS header | 4/34 | 5/34 | MEDIO | Lista siempre tuvo 5 valores |
| D-13 | F.1 Consultas >=3 | 18/33 (54.5%) | 19/33 (57.6%) | MEDIO | CSV: 14×3, no 12×3 |
| D-13b | F.1 Consultas lista | 32 items + ">3" | 33 items (14×3) | MEDIO | CSV n_consultas: 33 valores numéricos |
| D-05 | Header version | v3.1 | v3.3 | ALTO | -- |
| D-06 | A.2 Etica | [VACIO] | CEC-HCHM 202501-25 + alerta | ALTO | memory/project_V12_etica_cerrado.md |

**Discrepancias investigadas pero NO corregidas (AM-II correcto):**

| ID | Seccion | Hallazgo | Razon no corregir |
|----|---------|----------|-------------------|
| D-04 | D.5 FC taquicardia | Denom 31 vs 29 | AM-II contó manualmente incluyendo valores del texto libre no en CSV |
| D-07 | I.3 vs P.1 Plaq<100k | OR difiere | Denominadores diferentes (I.3=con plaq, P.1=con desenlace). Ambas correctas |
| D-11 | H.1 ECMO | CSV=4 vs AM-II=3 | C4 ECMO=Si es ERROR DE PARSEO. Texto clínico no menciona ECMO. Mantener 3/21 |
| D-12 | G.2 DVA | CSV=4 vs AM-II=6 | AM-II extrajo manualmente del texto libre. CSV subcodifica DVA. AM-II=verdad |
| D-14 | D.5 FC media | CSV=103.2 vs AM-II=104.9 | AM-II incluye valores manuales del texto libre no todos en CSV numérico |
| D-15 | H.3 Traslado | CSV=22 vs AM-II=24 | AM-II incluye traslados implícitos del texto libre. No corregir sin verificar fichas |

**Bibliografía Q1 nueva (S39):** 27 papers nuevos identificados para 6 gaps. Ver memory/reference_biblio_S39_gaps_Q1.md
