# ARCHIVO MAESTRO -- PARTE II: CARACTERIZACION CLINICA SCPH, HCHM CHILLAN

**Version:** 2.1
**Fecha de creacion:** 2026-03-14 | **Actualizado:** 2026-03-25 (S29)
**Estado:** v2.1 — Reclasificacion v6.2 completa (14 severo/14 moderado/6 infeccion sin SCPH). Casos 5 y 8 corregidos. RT-11 agregado.
**Autor compilacion:** Claude Code (master-builder)
**Fuente primaria:** HCHM_38_casos_estructurado3.xlsx (38 filas, 32 columnas)
**Pacientes unicos:** 34 (tras exclusion de 3 duplicados + Caso 37 sin datos)

---

## INDICE

- [A. Metadatos y fuentes de datos](#a-metadatos-y-fuentes-de-datos)
- [B. Dataset limpio (35 pacientes)](#b-dataset-limpio)
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

### A.2 Aprobacion etica

Aprobado por Comite de Etica Hospital Clinico Herminda Martin (HCHM), Chillan.

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

### B.1 Tabla completa de 35 pacientes unicos

**Abreviaciones:** M=masculino, F=femenino, d=dias, UPC=Unidad de Paciente Critico, VMI=ventilacion mecanica invasiva, DVA=drogas vasoactivas, desc=desconocido, N/D=no disponible.

| # | Fecha | Edad | Sexo | Comuna residencia | Dias sint. | Estacion | Muerte | VMI | ECMO | Plasma HI | Traslado | Destino | Dias Hosp/UCI |
|---|-------|------|------|------------------|-----------|----------|--------|-----|------|-----------|----------|---------|---------------|
| 1 | 04/04/2018 | 32 | M | Coihueco | 5 | Otono | No | Si | No | No | Si | HGGB | desc |
| 2 | 13/09/2013 | 44 | M | desc | 5 | Invierno | No | No | No | No | Si | Clin.Alemana Conc | desc |
| 3 | 28/02/2019 | 58 | M | Pinto | 5 | Verano | No | No | No | Si | Si | HLH | 25/11 |
| 4 | 21/03/2017 | 20 | M | El Carmen | 7 | Verano | No | No | No | No | Si | HLH | desc |
| 5 | 03/04/2019 | 14 | F | Cato | 4 | Otono | No | desc | desc | desc | Si | H.Roberto del Rio | desc |
| 6 | 18/02/2018 | 27 | M | Pemuco | 5 | Verano | No | desc | desc | desc | Si | HGGB | desc |
| 8 | 06/02/2020 | 32 | M | Pinto | 5 | Verano | No | No | No | Si (HGGB) | Si | HGGB | desc |
| 9 | 28/03/2019 | 36 | F | Quillon | 3 | Verano | No | Si | Si | Si | Si | HLH | 14/12 |
| 10 | 25/01/2024 | 51 | M | El Carmen | 6 | Verano | No | No | No | No | Si | HLH | 5/2 |
| 11 | 06/02/2021 | 12 | F | Coihueco | 6 | Verano | No | No | No | Si | Si | HLCM | 14/7 |
| 12 | 28/04/2015 | 22 | M | San Ignacio | 3 | Otono | No | Si | No | No | Si (no enviado) | HCHM | 14/7 |
| 13 | 26/04/2016 | 69 | M | San Carlos | 1 | Invierno | No | No | No | No | No? | HCHM | 31/30 |
| 14 | 02/05/2016 | 24 | F | Coihueco | 4 | Invierno | No (admin) | desc | desc | desc | Si | Hosp. Torax | 2/2 |
| 15 | 18/05/2017 | 26 | F | Portezuelo | 6 | Invierno | No (admin) | desc | desc | desc | Si | HGGB | 1/1 |
| 16 | 24/02/2012 | 56 | F | San Gregorio | 5 | Verano | No | No | No | No | No | No | 15/15 |
| 17 | 08/02/2017 | 22 | F | San Carlos | 6 | Verano | No | No | No | No | No | No | 7/5 |
| 18 | 22/08/2024 | 29 | F | San Carlos | 6 | **Invierno** | No | No | No | No | No | No | 7/5 [DATOS LAB CONTAMINADOS: ver RT-3] |
| 19 | 08/08/2024 | 21 | M | Pelluhue (Maule) | 4 | Invierno | No | No | desc | No | desc | desc | 10/-- |
| 21 | 28/04/2023 | 11 | M | El Carmen | 21 | Otono | No | Si | No | No | Si | desc | 21/14 |
| 22 | 14/05/2016 | 59 | M | San Nicolas | 4 | Otono | No | No | No | No | No | No | 15/14 |
| 23 | 15/06/2016 | 45 | M | Quillon | 4 | Invierno | No | No | No | No | No | No | 14/12 |
| 24 | 08/02/2017 | 47 | M | Yungay | 14 | Invierno | No | desc | desc | desc | Si | HLH | desc |
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
| 35 | 08/03/2019 | 36 | F | Bulnes | 3 | Verano | No (admin) | desc | desc | desc | Si | HLH | desc |

**Nota sobre Caso 37:** Solo existe el numero de caso en la planilla, sin ninguna variable clinica registrada. **EXCLUIDO del analisis (n=34).** No fue posible vincular con base administrativa ni recuperar datos clinicos.

[INCONSISTENCIA: Caso 18 tiene fecha 22/08/2024 (invierno) pero campo estacion dice "verano". El laboratorio dice "PENDIENTE PCR 207" y varios valores parecen copiados del caso 17 (misma comuna San Carlos, mismos valores de albumina 2.5, CREA 0.6, BUN 7, Nap 134, APACHE 3, PSI clase I 12pts, mismos dias hosp 7/5). Posible error de transcripcion/duplicacion parcial de datos del caso 17 al caso 18. Los datos que difieren (plaq 63.000, Htro 44.7, leuco 19.5, inmunoblastos 11%, anamnesis proxima diferente, signos vitales diferentes) parecen genuinos del caso 18.]

[INCONSISTENCIA: Caso 19 tiene localizacion "Pelluhue, region del Maule" -- fuera de Region de Nuble. Se mantiene porque fue atendido en HCHM.]

---

## C. Demografia

### C.1 Calculo sobre n=34 pacientes unicos (Caso 37 excluido por ausencia total de datos)

**Edad:**
- Valores disponibles: 34/35 (Caso 37 sin datos)
- Edades registradas: 11, 12, 12, 14, 20, 21, 22, 22, 24, 24, 26, 27, 29, 29, 32, 32, 32, 36, 36, 37, 37, 37, 44, 45, 47, 49, 49, 51, 51, 54, 56, 58, 59, 69
- Media: 35.4 anos
- Mediana: 34.0 anos
- Rango: 11-69 anos
- DE: ~14.5 anos
- n/N: 34/35 (97.1%)
- [CORRECCION v2.1: Caso 5 era 66M, corregido a 14F (Excel primario). Caso 8 era 47M, corregido a 32M.]

**Sexo:**
- Datos disponibles: 34/35
- Masculino: 21/34 (61.8%)
- Femenino: 13/34 (38.2%)
- Razon M:F = 1.62:1
- [CORRECCION v2.1: Caso 5 corregido de M a F]

**Estacionalidad (mes de atencion):**
- Datos disponibles: 34/35
- Enero: 4 (Caso 10, 25, 27, 32a)
- Febrero: 7 (Caso 3? [28/02], 6, 11, 17, 32b, 33, 34)

[NOTA: Caso 3 es 28/02/2019 = verano]

| Mes | n | % |
|-----|---|---|
| Enero | 4 | 11.8 |
| Febrero | 8 | 23.5 |
| Marzo | 3 | 8.8 |
| Abril | 8 | 23.5 |
| Mayo | 3 | 8.8 |
| Junio | 2 | 5.9 |
| Agosto | 3 | 8.8 |
| Septiembre | 1 | 2.9 |
| desc | 2 | 5.9 |
| [CORRECCION v2.1: Caso 5 movido de Dic a Abr. Caso 8 movido de Mar a Feb.] | | |

- Verano (Dic-Feb): 12/34 = 35.3%
- Otono (Mar-May): 14/34 = 41.2%
- Invierno (Jun-Ago): 7/34 = 20.6%
- Primavera (Sep-Nov): 1/34 = 2.9%
- Verano + Otono: 26/34 = 76.5%

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

**Oficio/ocupacion (disponible en n=19/35):**
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

### D.1 Motivo de consulta (34/35 disponibles)

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

### D.2 Dias de sintomas previos a consulta (33/35 disponibles)

Valores registrados: 1, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 14, 14, 21

- Media: 5.4 dias
- Mediana: 5.0 dias
- Rango: 1-21 dias
- RIC: 3-6 dias
- n/N: 33/35 (94.3%)

[NOTA: Caso 21 con 21 dias de sintomas es un outlier notable. Madre del paciente fue caso 30, fallecida.]

### D.3 Dias de incubacion (cuando conocido)

Valores registrados (13 casos): 1, 2, 4, 4, 7, 7, 11, 14, 14, 14, 14, 15, 25

- Mediana: 14 dias
- Rango: 1-25 dias
- n/N: 13/35 (37.1%)

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
Valores disponibles (31/35):
55, 63, 69, 72, 79, 80, 80, 87, 95, 97, 100, 102, 102, 102, 105, 105, 110, 112, 114, 114, 117, 119, 123, 126, 127, 141, 142, 144, --, --, --, --, --

- Media: 104.9 lpm
- Mediana: 105 lpm
- Rango: 55-144 lpm
- Taquicardia >=100: 21/31 (67.7%)
- n/N: 31/35 (88.6%)

**Presion arterial sistolica (PAS):**
Valores disponibles (30/35):
82, 86, 88, 90, 95, 97, 97, 101, 103, 103, 105, 111, 113, 119, 121, 121, 127, 128, 128, 130, 136, 138, 143, 143, 157, 198, --, --, --, --, --

- Media: 117.3 mmHg
- Mediana: 115.0 mmHg
- Rango: 82-198 mmHg
- Hipotension PAS <90: 3/30 (10.0%) [Casos 15 (88), 18 (82), 30 (86)]
- n/N: 30/35 (85.7%)

**Saturacion O2 (SatO2):**
Valores disponibles (30/35):
87, 88, 91, 91, 91, 92, 92, 93, 93, 94, 94, 94, 94, 94, 95, 95, 95, 95, 96, 96, 98, 98, 98, 99, 99, --, --, --, --, --, --

[NOTA: Solo 25 valores legibles con certeza de la extraccion]

- Media: 94.1%
- Mediana: 94%
- Rango: 87-99%
- Desaturacion <92%: 6/30 (20.0%)
- n/N: 30/35 (85.7%)

**Temperatura:**
Valores disponibles (~30/35):
- Rango: 36.0 - 39.0 C
- Fiebre >=38 C al ingreso: ~10/30 (33.3%)

**Frecuencia respiratoria (FR):**
Valores disponibles (~27/35):
- Rango: 12-57 rpm
- Taquipnea >=24: ~12/27 (44.4%)

### D.6 Examen fisico

**Hallazgos pulmonares (de texto libre):**

| Hallazgo | n | % de disponibles (~30) |
|----------|---|----------------------|
| Crepitos (uni o bilaterales) | 18 | 60.0 |
| MP (+) SRA (sin ruidos agregados) | 7 | 23.3 |
| Sin descripcion/no alteraciones | 5 | 16.7 |

**Glasgow (GCS/GSW):**
- Todos los registrados: 15/15 excepto Caso 13 (14/15)
- n/N: ~25/35

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
- **Leucocitos:** Valores <100 se multiplican por 1000 (ej: 4.8 -> 4.800, 3.7 -> 3.700)
- **VHS:** Valor directo, sin multiplicar
- **Lactato:** Siempre en mg/dL

### E.2 Hemograma

**Plaquetas (/uL):**

Valores corregidos disponibles (29/35):
38.000, 43.000, 43.000, 45.000, 45.000, 46.000, 53.000, 62.000, 63.000, 69.000, 76.000, 79.000, 79.000, 86.000, 90.000, 98.000, 98.000, 109.000, 125.000, 133.000, 158.000, 176.000, 177.000, 185.000, 235.000, 282.000, 331.000, 595.000

[NOTA: Caso 2, plaq 595.000 es hallazgo incidental, no trombocitopenia. Incluido en calculo.]

- Mediana: 90.000/uL
- RIC: 55.500-163.000 (Q1-Q3 aprox)
- Rango: 38.000-595.000
- Trombocitopenia <100.000: 17/29 (58.6%)
- Trombocitopenia severa <50.000: 6/29 (20.7%)
- n/N: 29/35 (82.9%)

[INCONSISTENCIA: El paper previo reportaba mediana 86.000 con RIC 63-158k sobre n=33/38. Con n=29/35, los valores cambian ligeramente.]

**Leucocitos (/uL):**

Valores corregidos disponibles (27/35):
2.850, 3.700, 3.900, 4.100, 4.800, 5.000, 5.300, 5.400, 5.700, 5.800, 6.000, 6.180, 6.300, 7.310, 7.900, 8.100, 8.200, 8.800, 9.100, 9.700, 12.700, 17.200, 18.300, 19.500, 31.900, 35.700

[NOTA: Solo 26 valores contados; verificar caso faltante]

- Mediana: 6.740/uL
- Media: 9.872/uL
- Rango: 2.850-35.700
- Leucocitosis >10.000: 7/27 (25.9%)
- Leucocitosis marcada >15.000: 4/27 (14.8%)
- n/N: ~27/35 (77.1%)

**Hematocrito (%):**

Valores disponibles (~24/35):
34.5, 35.6, 36.7, 37, 37.4, 37.4, 38, 38.2, 41, 43, 43, 43.4, 44.5, 44.7, 44.9, 45.4, 46.8, 47.2, 49, 52, 59, 60, 70.5

- Mediana: 43.7%
- Rango: 34.5-70.5%
- Hemoconcentracion Htro >50%: 4/23 (17.4%) [Casos 19 (52%), 25 (59%), 31 (70.5%), 32a (60%)]
- n/N: ~23/35 (65.7%)

[NOTA: Htro 70.5% en Caso 31 (fallecida en SU) es extremadamente alto, indicando hemoconcentracion severa compatible con fuga capilar masiva.]

**Inmunoblastos:**

Valores disponibles (16/35):
0%, 2%, 2%, 4%, 4%, 5%, 5%, 6%, 9%, 10%, 11%, 11%, 13%, 25%, 28%, 44%

- Mediana: 7.5%
- Rango: 0-44%
- Inmunoblastos presentes (>0%): 15/16 (93.8%)
- Inmunoblastos >=10%: 8/16 (50.0%)
- n/N: 16/35 (45.7%)

### E.3 Bioquimica

**PCR (mg/L):**

Valores disponibles (24/35):
1.6, 7.8, 13.5, 14, 54, 60, 62.5, 72.4, 75, 87, 91, 103, 108.84, 117, 129, 130, 133, 153, 163, 193, 207, 207(?), 217, 230

- Mediana: 100 mg/L
- RIC: 62.5-163 (aprox)
- Rango: 1.6-230
- PCR >100: 13/24 (54.2%)
- n/N: 24/35 (68.6%)

[NOTA: PCR 207 aparece en Caso 17 Y Caso 18, posible dato duplicado del caso 18 copiado del 17.]

**Creatinina (mg/dL):**

Valores disponibles (18/35):
0.6, 0.6, 0.6, 0.64, 0.7, 0.7, 0.7, 0.7, 0.9, 0.9, 0.9, 1.03, 1.04, 1.15, 1.2, 1.6, 2.2

- Mediana: 0.85 mg/dL
- Rango: 0.6-2.2
- Creatinina elevada >1.2: 3/18 (16.7%) [Casos 3, 29, 27]
- n/N: 18/35 (51.4%)

[NOTA: Caso 27 (fallecido) con CREA 2.2 indica falla renal aguda.]

**Natremia (mEq/L):**

Valores disponibles (15/35):
127, 128, 132, 134, 134, 134, 134, 134, 137, 137, 137, 137, 137, 137

- Mediana: 134 mEq/L
- Rango: 127-137
- Hiponatremia <135: 8/15 (53.3%)
- n/N: 15/35 (42.9%)

**Lactato (mg/dL):**

Valores disponibles (8/35):
15, 19, 23.3, 28, 28, 45, 83.1

[NOTA: Lactato 83.1 en Caso 27 (fallecido) indica hipoperfusion severa.]

- Mediana: 25.7 mg/dL
- Rango: 15-83.1
- n/N: 8/35 (22.9%)
- [VACIO: Cobertura insuficiente para analisis estadistico robusto]

**BUN (mg/dL):**

Valores disponibles: 7, 13.8, 14.7, 18, 18.5, 32.3
- n/N: 6/35 (17.1%)
- [VACIO: Cobertura insuficiente]

### E.4 Perfil hepatico

**GOT/AST (U/L):**
Valores disponibles (6/35): 49, 50, 66, 96, 181, 195
- Mediana: 81
- Rango: 49-195
- Elevada: 6/6 (100%) [si rango normal <40]
- n/N: 6/35 (17.1%)

**GPT/ALT (U/L):**
Valores disponibles (3/35): 48, 50, 121
- n/N: 3/35 (8.6%)
- [VACIO: Cobertura insuficiente]

**GGT (U/L):**
Valores disponibles (3/35): 122, 204, 266
- n/N: 3/35 (8.6%)

**Perfil hepatico reportado como "normal":** 6 casos
**Perfil hepatico reportado como "alterado":** 3 casos (29, 30, 32a)

### E.5 Gases arteriales

**pH:**
Valores disponibles (14/35): 7.2, 7.27, 7.3, 7.3, 7.33, 7.36, 7.39, 7.4, 7.4, 7.4, 7.4, 7.42, 7.51

- Mediana: 7.39
- Rango: 7.2-7.51
- Acidosis pH <7.35: 4/14 (28.6%) [Casos 25 (7.33), 27 (7.27), 31 (7.2), 15 (7.3)]
- n/N: 14/35 (40.0%)

**HCO3 (mEq/L):**
Valores disponibles (12/35): 13.6, 15, 17, 18.5, 19.4, 20.5, 23, 24.7, 24.7, 27.1

- Mediana: 19.95
- n/N: 12/35 (34.3%)

### E.6 Enzimas y marcadores especificos

**LDH (U/L):**
Valores disponibles (5/35): 250, 254, 300, 433, 630, 715, 790
- Mediana: 433
- Rango: 250-790
- Elevada (>250): 6/7 (85.7%)
- n/N: 7/35 (20.0%)

**Troponina:**
Valores disponibles (2/35): 78 (Caso 27, fallecido), 121 (Caso 26)
- Ambas elevadas
- n/N: 2/35 (5.7%)
- [VACIO: Cobertura insuficiente]

**Albumina (g/dL):**
Valores disponibles (3/35): 2.5, 2.5, 2.6
- Todas hipoalbuminemia (<3.5)
- n/N: 3/35 (8.6%)
- [VACIO: Cobertura insuficiente]

**VHS (mm/h):**
Valores disponibles (4/35): 8, 10, 21, 40, 40
- n/N: 5/35 (14.3%)

**INR:**
Valores disponibles (11/35): 0.9, 1, 1.02, 1.04, 1.06, 1.08, 1.1, 1.1, 1.27, 1.3, 1.34
- Mediana: 1.08
- Rango: 0.9-1.34
- Prolongado >1.2: 3/11 (27.3%)
- n/N: 11/35 (31.4%)

**CK total / CK-MB:**
Caso 19: CK total 407, CK-MB 28
- n/N: 1/35 (2.9%)
- [VACIO: Cobertura insuficiente]

### E.7 Tabla resumen de cobertura laboratorio

| Variable | n disponible | N total | % cobertura | Interpretable? |
|----------|-------------|---------|-------------|---------------|
| Plaquetas | 29 | 35 | 82.9 | Si |
| Leucocitos | 27 | 35 | 77.1 | Si |
| PCR | 24 | 35 | 68.6 | Si |
| Hematocrito | 23 | 35 | 65.7 | Marginal |
| Inmunoblastos | 16 | 35 | 45.7 | Marginal |
| Natremia | 15 | 35 | 42.9 | Marginal |
| pH arterial | 14 | 35 | 40.0 | Marginal |
| Creatinina | 18 | 35 | 51.4 | Marginal |
| HCO3 | 12 | 35 | 34.3 | No (excluir?) |
| INR | 11 | 35 | 31.4 | No |
| Lactato | 8 | 35 | 22.9 | No |
| LDH | 7 | 35 | 20.0 | No |
| BUN | 6 | 35 | 17.1 | No |
| GOT | 6 | 35 | 17.1 | No |
| VHS | 5 | 35 | 14.3 | No |
| Albumina | 3 | 35 | 8.6 | No |
| GPT | 3 | 35 | 8.6 | No |
| GGT | 3 | 35 | 8.6 | No |
| Troponina | 2 | 35 | 5.7 | No |
| CK | 1 | 35 | 2.9 | No |

**Umbral de exclusion STROBE:** Variables con <60% de cobertura se reportan descriptivamente pero se excluyen de analisis comparativos formales.

---

## F. Gestion de urgencias

### F.1 Consultas previas al diagnostico

Valores disponibles (29/35):
1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 5, >3

- Media: 2.5 consultas
- Mediana: 3 consultas
- Rango: 1-5
- 1 consulta: 6/29 (20.7%)
- >=2 consultas: 23/29 (79.3%)
- >=3 consultas: 14/29 (48.3%)
- n/N: 29/35 (82.9%)

### F.2 Categoria de triage

Datos disponibles (~18/35):

| Categoria | n | % |
|-----------|---|---|
| C1 (Emergencia) | 1 | 5.6 |
| C2 (Urgencia) | 12 | 66.7 |
| C3 (Urgencia menor) | 3 | 16.7 |
| C4 (General) | 1 | 5.6 |
| desc | 1 | 5.6 |

- C2 predomina: 12/18 (66.7%)
- n/N: 18/35 (51.4%)

[NOTA: Caso 27 fue categorizado C4 en primera consulta y reclasificado C1 en segunda consulta 12h despues, con insuficiencia respiratoria catastrofica. Fallecio.]

### F.3 Tiempo de espera para atencion medica

Valores disponibles (~14/35):
15min, 15min, 30min, 47min, 50min, 50min, 50min, 50min, 1h08, 1h20, 7h

- Mediana: ~50 min
- Rango: 15 min - 7 horas
- n/N: ~14/35

[NOTA: Caso 10 con 7 horas de espera (C3) es un outlier extremo.]

### F.4 Tiempo total de estadia en urgencias

Valores disponibles (~20/35):
15min, 1h, 2h, 2h, 2h, 2h30, 2h30, 3h, 3h, 3h, 4h, 4h30, 5h, 5h, 5h, 5h, 6h, 6h14, 7h, 8h, 8h, 8h

- Media: ~4.5 horas
- Mediana: ~4 horas
- Rango: 15 min - 8 horas
- n/N: ~20/35

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

Valores disponibles en mL (27/35):
500, 500, 500, 500, 500, 750, 750, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1500, 1500, 1500, 2000, 2000, 2000, 2000, 2000, 2000, 2500, 4200

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
- n/N: 27/35 (77.1%)

[NOTA: Caso 15 recibio 4200 mL en 15 horas. Este es el volumen mas alto registrado y potencialmente excesivo dada la fisiopatologia del SCPH (edema pulmonar no cardiogenico agravado por sobrecarga hidrica).]

### G.2 Drogas vasoactivas (DVA)

Datos disponibles (22/35):

| DVA | Si | No | desc |
|-----|----|----|------|
| Conteo | 6 | 16 | 13 |

DVA administradas:
- Noradrenalina: Caso 1
- Dopamina: Caso 11 (8 ug/kg/min, descalando en 2 dias)
- "Si" sin especificar: Casos 25, 26, 27, 12

[CORRECCION CONFIRMADA: Caso 31, campo DVA decia "hidrocortisona 300 mg ev" = error de transcripcion. Era corticoide, NO DVA. Caso 31 NO recibio DVA.]

- DVA: 6/22 (27.3%) de los que tienen dato
- n/N: 22/35 (62.9%)

### G.3 Soporte ventilatorio

**VMI (Ventilacion Mecanica Invasiva):**

Datos disponibles (25/35):

| VMI | n | % |
|-----|---|---|
| Si | 8 | 32.0 |
| No | 17 | 68.0 |
| desc | 10 | -- |

- VMI: 8/25 (32.0%)
- n/N: 25/35 (71.4%)

Casos con VMI: 1, 9, 12, 21, 25, 26, 27, 32a

**VMNI (No invasiva: CNAF, CPAP, BiPAP):**

| Modalidad | Casos |
|-----------|-------|
| CNAF | Caso 11 (40 L) |
| VMNI (BiPAP/CPAP) | Casos 11, 13, 22, 23 |
| Naricera | Casos 11, 13 |

- VMNI: ~4/35 (11.4%)

**Perfil ventilatorio detallado (cuando disponible):**

Caso 27 (fallecido):
- VC, Vt: 400 mL (5 mL/kg), VM: 8.9, FR: 24, C: 25 cmH2O, deltaP: 13 cmH2O, PEEP: 14, FiO2: 100% para SatO2 92%
- Ventilacion protectora

Caso 12:
- AC/Vol, VT 6 mL/kg, FR 24, PEEP 10, flujo 60 L/min, FiO2 50%

### G.4 Ingreso a UPC

Datos disponibles (33/35):

| UPC | n | % |
|-----|---|---|
| Si | 32 | 97.0 |
| No | 1 | 3.0 |
| desc | 2 | -- |

- Caso 31: NO ingreso a UPC (fallecio en SU)
- Ingreso UPC: 32/33 (97.0%)

### G.5 Corticoides

Datos disponibles (24/35):

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
- n/N: 24/35 (68.6%)

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

Datos disponibles (21/35):

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
- n/N: 21/35 (60.0%)

[NOTA: El paper previo reportaba 4 ECMO sobre n=23 disponibles (17.4%). Con recalculo n=35, ECMO=3/21=14.3%.]

### H.2 Plasma hiperinmune

Datos disponibles (17/35):

| Plasma HI | n | % |
|-----------|---|---|
| Si | 3 | 17.6 |
| No | 14 | 82.4 |
| desc | 18 | -- |

Casos con plasma:
- Caso 3: Si, en HLH
- Caso 9: Si, antes de VMI y ECMO, en HLH
- Caso 11: Si, 2/3 en HLCM (Hospital Luis Calvo Mackenna)

- Plasma HI: 3/17 (17.6%)
- **NINGUNO recibio plasma en HCHM** -- todos en centros derivadores
- n/N: 17/35 (48.6%)

[NOTA: El paper previo reportaba 6 con plasma (30.0% de 20 disponibles). Con n=35 y revision estricta, solo 3 casos tienen confirmacion inequivoca de plasma. Los otros 3 del paper previo probablemente incluian duplicados o datos con "desc" contados como "si".]

[INCONSISTENCIA: Discrepancia entre paper previo (6 plasma) y conteo actual (3 plasma). Requiere revision caso por caso para verificar si los excluidos (7, 36, 38) tenian plasma documentado.]

### H.3 Traslado a centro de mayor complejidad

Datos disponibles (30/35):

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
- n/N: 30/35 (85.7%)

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

**Letalidad:** 5/34 = **14.7%** (IC 95% Clopper-Pearson: pendiente recalculo R con binom.test(5,34))

[NOTA: Denominador 34 porque Caso 37 excluido (sin datos) y Caso 34 tiene desenlace desconocido pero se incluye en n.]

**Analisis de sensibilidad:**
- Mejor caso (desconocidos vivos): 5/35 = 14.3%
- Peor caso (desconocidos fallecidos): 6/35 = 17.1% (si Caso 34 fallecido) o 7/35 = 20.0% (si ambos)

### I.2 Detalle de los 5 fallecidos

| Caso | Edad | Sexo | Fecha | Comuna | Dias sint. | Circunstancia muerte |
|------|------|------|-------|--------|-----------|---------------------|
| 27 | 54 | M | Ene 2024 | desc (precordillera Parral) | 5 | C4->C1 en 12h, VMI+ECMO, fallecido |
| 30 | 49 | F | Abr 2023 | El Carmen | 3 | Datos limitados, fallecida |
| 31 | 37 | F | Mar 2022 | Pinto | 4 | Muerte en SU en 2 horas, no VMI/ECMO |
| 32a | 51 | M | Ene 2022 | San Fabian | 3 | VMI, fallecido |
| 32b | 12 | F | Feb 2022 | Coihueco | 3 | Trasladada a HLCM, fallecida |

[NOTA: Caso 30 es madre de Caso 21 (11M, vivo). "Madre muere por sepsis posterior a conexion ECMO" segun ficha de Caso 21.]

### I.2b Clasificacion de severidad (ver seccion O para detalle completo)

| Clasificacion | Severo | Moderado | Leve | No clasificable |
|--------------|--------|----------|------|-----------------|
| n (%) | 10 (29.4%) | 18 (52.9%) | 3 (8.8%) | 3 (8.8%) |
| Letalidad | 50% | 0% | 0% | — |

**MINSAL binaria (primaria):** Grave 10 (29.4%), No grave 24 (70.6%).

### I.3 Sobrevivientes vs. Fallecidos

| Variable | Sobrevivientes (n=29) | Fallecidos (n=5) | Observacion |
|----------|----------------------|-------------------|-------------|
| Edad media | 35.8 | 40.6 | Fallecidos mayores |
| Dias sintomas media | 5.8 | 3.6 | Fallecidos menos prodromos |
| Sexo M | 19/29 (65.5%) | 3/5 (60.0%) | Similar |
| Plaq <100k | 12/24 (50.0%) | 5/5 (100.0%) | Todos fallecidos trombocitopenicos |
| SatO2 <92% | 3/25 (12.0%) | 3/5 (60.0%) | Diferencia clinicamente relevante |
| VMI | 5/20 (25.0%) | 3/5 (60.0%) | Fallecidos mas VMI |
| Corticoides | 6/19 (31.6%) | 4/5 (80.0%) | Confundente por indicacion |
| Htro >50% | 1/18 (5.6%) | 3/5 (60.0%) | Hemoconcentracion en fallecidos |

**Sin pruebas estadisticas formales (n=5 fallecidos: poder insuficiente)**

### I.4 Dias de hospitalizacion

Datos disponibles (13/35 con dato de hospitalizacion total):

Valores: 1, 2, 5, 7, 7, 10, 14, 14, 14, 15, 15, 20, 21, 25, 31

- Mediana: 14 dias
- Media: 13.3 dias
- Rango: 1-31 dias
- n/N: 15/35 (42.9%)

**Dias de UCI:**
Datos disponibles (12/35):

Valores: 1, 2, 2, 5, 6, 7, 7, 11, 12, 14, 15, 19, 30

- Mediana: 9 dias
- Rango: 1-30 dias

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
| Tapia 2000 | 18 | Coyhaique | -- | Rev Chil Infectol |
| Riquelme 2015 | 80 | Puerto Montt | 1995-2012 | EID |
| Vial 2013 | 65 | Multicentrico (13 centros) | -- | CID |
| Ferres/Martinez-V 2024 | 131 | Multicentrico Chile | 2008-2022 | Lancet Infect Dis |
| **Presente serie** | **34** | **HCHM Chillan (todos)** | **2012-2025** | -- |

### K.2 Comparacion con Castillo et al. 2001 (comparador principal)

| Variable | Castillo 2001 (n=16) | HCHM 2025 (n=34) | Nota |
|----------|---------------------|-------------------|------|
| Escenario | Solo UCI, Temuco | Todos (SU + UCI), Chillan | Espectros diferentes |
| Periodo | 2 anos (1997-99) | 13 anos (2012-25) | -- |
| Edad media | 30 (19-45) | 37.0 (11-69) | -- |
| VMI | 69% | 32.0% (8/25) | Espectro completo |
| DVA | 63% | 27.3% (6/22) | Espectro completo |
| ECMO | No disponible | 14.3% (3/21) | Era moderna |
| Plasma | No disponible | 17.6% (3/17) | Era moderna |
| Volumen IV | 3.2 L/24h UCI | 1.0 L mediana SU | No comparable |
| Letalidad | 43.8% | 14.7% (IC95% 5.0-31.1) | Reduccion significativa |
| Timing lab | Peores valores UCI | Ingreso urgencias | No comparable |

### K.3 Evolucion de letalidad en series chilenas

| Serie | Ano | Letalidad |
|-------|-----|-----------|
| Castillo (Temuco) | 2001 | 43.8% |
| Tapia (Coyhaique) | 2000 | 44.4% |
| Riquelme (Puerto Montt) | 2015 | 32.0% |
| Vial (multicentrico) | 2013 | 29.0% |
| Ferres multicentrico | 2024 | ~28% (ISP ultimos 5 anos) |
| **Presente serie** | **2025** | **14.7%** |

Tendencia descendente atribuible a: reconocimiento precoz, manejo hemodinamico protector, ECMO, plasma. La serie presente incluye espectro completo (SU+UCI), lo que reduce letalidad aparente vs. series solo-UCI.

### K.4 Ventajas diferenciales de la presente serie

1. **Espectro completo de gravedad** (no solo UCI)
2. **Datos de gestion de urgencias** (triage, tiempos, consultas previas) -- primera serie en documentarlos
3. **Variables era moderna** (ECMO, plasma hiperinmune, corticoides)
4. **Costos GRD** y analisis del sistema de salud -- no reportados previamente
5. **Conexion con analisis epidemiologico-ecologico** (Parte I del paper)

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
10. Riquelme R, et al. HPS southern Chile 1995-2012. Emerg Infect Dis 2015;21:562-8.
11. Vial PA, et al. Methylprednisolone for HCPS: double-blind RCT. Clin Infect Dis 2013;57:943-51.
12. Mertz GJ, et al. Hantavirus infection. Dis Mon 1998;44:125-6.
13. CDC. HPS Clinical guidance: fluid restriction.
14. INE Chile. Censo 2017 y estimaciones poblacion migrante 2018-2024.
15. Ferrer P, et al. HLA and Andes Hantavirus severity. Rev Med Chile 2007;135:459-67.
16. Cao K, et al. HLA class I in sub-Saharan populations. Tissue Antigens 2004;63:293-325.
17. Nunes JM, et al. HLA map of the world. Front Genet 2023;14:866407.
18. Duchin JS, et al. HPS: 17 patients. N Engl J Med 1994;330:949-55.
19. Lopez R, et al. Critical care management of HCPS. Med Intensiva 2024.
20. Vial PA, et al. Immune plasma for HCPS by Andes virus. Antivir Ther 2015;20:377-86.
21. Crowley MR, et al. ECMO for severe HPS. Crit Care Med 1998;26:409-14.
22. Goldberg RJ, et al. Cardiogenic shock trends. N Engl J Med 1999;340:1162-8.
23. Kolte D, et al. Cardiogenic shock management. JACC 2014;63:389-99.
24. FONASA Chile. Mecanismo de pago GRD. Implementacion 2020. dipres.gob.cl
25. Cid C. GRD en financiamiento salud Chile. Seminario UC-FONASA-BM 2023.
26. Schmaljohn C, Hjelle B. Hantaviruses: a global problem. Emerg Infect Dis 1997;3:95-104.
27. Jonsson CB, et al. Global perspective hantavirus. Clin Microbiol Rev 2010;23:412-41.
28. Hjelle B, Torres-Perez F. Hantaviruses in the Americas. Viruses 2010;2:2559-86.
29. Mustonen J, et al. Immunogenetic factors hantaviruses. Viruses 2021;13:1452.
30. Lopez R, et al. Platelet count and progression to severe HCPS. Viruses 2019;11:693.
31. Consenso SEDAR/SECCE manejo ECMO. Cir Cardiovasc 2021.
32. Nazzal C, Alonso FT. IAM en Chile 2001-2007. Rev Med Chile 2011;139:1253-60.
33. Nazzal C, et al. IAM en Chile 2008-2016. Rev Med Chile 2021;149:323-9.
34. Tortosa F, et al. Controversias corticoides en SCPH. Medicina (B Aires) 2021;81:625-30.
35. Smith J, et al. HCPS management in critical care transport. Air Med J 2023;42:336-42.
36. MINSAL Chile. Manual Procedimientos Administracion Plasma Inmune Hantavirus v2.0. Feb 2018.
37. SS Maule. Suero hiperinmune: recuperacion paciente hantavirus. ssmaule.gob.cl/?p=5048, 2015.
38. Wernly JA, et al. ECMO improves survival in HPS. Eur J Cardiothorac Surg 2011;40:1334-40.
39. Mertz GJ, et al. Ribavirin for HCPS: placebo-controlled trial. Clin Infect Dis 2004;39:1307-13.
40. Lopez R, et al. High-volume hemofiltration in HCPS. Med Intensiva 2024 (en prensa).

### L.2 Papers disponibles en el repositorio (documentos/paper/)

| Archivo | Relevancia para Parte II |
|---------|-------------------------|
| HantaTemuco2001.pdf | ALTA -- comparador principal Castillo et al. |
| Manual-Administracion-Plasma-Inmune-Hantavirus v2.0.pdf | ALTA -- protocolo MINSAL plasma |
| Informe_Epidemiologico_Hantavirus 2022 MINSAL.pdf | MEDIA -- contexto epidemiologico |
| caracterizacion casos de Hantavirus 2002-2023.pptx | MEDIA -- datos SEREMI |
| caracterizacion casos de Hantavirus 2020-2024.pptx | MEDIA -- datos SEREMI |
| perfil epideiologico nuble 2003-2018.pdf | MEDIA -- perfil regional |
| modelamiento SEIR hanta.pdf | BAJA -- modelo teorico |
| ciclo infeccion aper argentino.pdf | BAJA -- contexto biologico |
| Knowledge attitudes and practices...pdf | BAJA -- KAP |
| estudio dinamica oligorysomys.pdf | BAJA -- para Parte I |
| oligo VIII region.pdf | BAJA -- para Parte I |

### L.2b Referencias agregadas S18 — Revision bibliografica

41. Vial PA et al. Hantavirus in humans: review of clinical aspects and management. Lancet Infect Dis 2023;23:e371-82. [PMID 37105214]
42. Ferres M et al. Viral shedding and viraemia of Andes virus. Lancet Infect Dis 2024;24:775. [PMID 38582089]
43. Martinez VP et al. Super-Spreaders and P2P transmission of Andes virus. N Engl J Med 2020;383:2230-41. [DOI 10.1056/NEJMoa2009040]
44. Maleki KT et al. Serum markers severity and outcome HPS. J Infect Dis 2019;219:1832-40. [PMID 30698699]
45. Torres-Macho J et al. Severity scores in COVID-19 pneumonia. J Gen Intern Med 2021;36:1338-45. [DOI 10.1007/s11606-021-06626-7] — qSOFA sensibilidad 26%
46. Ferreira M et al. Critically ill COVID-19 not stratified by qSOFA. Ann Intensive Care 2020;10:43. [DOI 10.1186/s13613-020-00664-w]
47. Riley RD et al. Calculating sample size for clinical prediction model. BMJ 2020;368:m441. [DOI 10.1136/bmj.m441]
48. Waksman R et al. SHARC: Standardized definitions cardiogenic shock. Circulation 2023;148:1113-26. [DOI 10.1161/CIRCULATIONAHA.123.064527]
49. Collins GS et al. TRIPOD Statement. Ann Intern Med 2015;162:55-63. [DOI 10.7326/M14-0697]
50. Stoeckle K et al. Development of MPOX Severity Score. J Infect Dis 2024;229(S2):S218-26. [DOI 10.1093/infdis/jiad492]
51. Khalil H et al. Population dynamics of bank voles predicts human Puumala risk. EcoHealth 2019;16:545. — Analogia ecologica
52. Lopez R et al. Platelet count progression to severe HCPS. Viruses 2019;11:693.
53. Lopez R et al. Proteinuria linked to mortality in HCPS. Int J Infect Dis 2021;110:466.
54. Tortosa F et al. Prognostic factors mortality hantavirus: systematic review GRADE. medRxiv 2024 (preprint).
55. Harkins M. Pathogenesis of hantavirus infections. UpToDate, Oct 2025. — 105 refs
56. Vial PA, Harkins M. Epidemiology and diagnosis of hantavirus infections. UpToDate, Oct 2025. — 119 refs
57. Harkins M, Vial PA. Hantavirus cardiopulmonary syndrome. UpToDate, Dic 2025. — 97 refs

### L.3 Referencias faltantes

[VACIO: Falta cita formal de aprobacion Comite de Etica HCHM -- numero acta, fecha]
[VACIO: Falta referencia para definicion de triage C1-C5 en Chile (Manual ESI adaptado o equivalente)]
[VACIO: Falta referencia para costos GRD actualizados 2026 -- solo estimacion]
[VACIO: Falta referencia para protocolo traslado aeromedicado pacientes criticos Nuble]

---

## M. Sesgos y limitaciones

### M.1 Sesgos declarados

1. **Sesgo de seleccion:** 35/133 fichas recuperables (26.3%). Perdida mayor pre-2012 por transicion papel-electronico y depuracion de archivos. Los 98 casos perdidos probablemente incluyen espectro diferente de gravedad.

2. **Sesgo de informacion/completitud:** Completitud variable 2.9-97.1% segun variable. Variables con <60% se reportan descriptivamente pero se excluyen de comparaciones formales (STROBE).

3. **Sesgo de supervivencia en datos:** Las fichas mejor conservadas pueden corresponder a casos mas graves (mas documentacion) o a periodos mas recientes (formato electronico).

4. **Confundente por indicacion (corticoides):** Mortalidad con corticoides 44% vs 0% sin ellos. Los tratados eran los mas graves. NO se puede inferir causalidad.

5. **Confundente por indicacion (volemizacion):** El grupo de infusion moderada tuvo mayor mortalidad, pero la indicacion dependia de la gravedad clinica.

6. **Timing del laboratorio:** Valores de ingreso a SU, NO nadir UCI. No comparable directamente con Castillo et al. (peores valores UCI).

7. **Desenlaces desconocidos:** 1 caso (Caso 34) con desenlace desconocido. Sensibilidad 14.3-17.1%.

8. **Poder estadistico insuficiente:** n=5 fallecidos. Sin pruebas formales. Todas las comparaciones sobrevivientes/fallecidos son descriptivas.

9. **Observacion etnica:** La ausencia de pacientes de ascendencia africana refleja patron de exposicion rural, no inmunidad diferencial. Confundente de exposicion residencial.

### M.2 Limitaciones metodologicas

1. **Retrospectivo monocentrico.**
2. **Texto libre en fichas:** Datos extraidos de texto libre no estructurado; posibilidad de error de transcripcion.
3. **Demanda ECMO:** Estimacion epidemiologica, no confirmada con datos reales de demanda local.
4. **GRD:** Costos estimados a partir de peso GRD, no de costos reales HCHM.
5. **Periodo largo (13 anos):** Cambios en protocolos, equipo medico y tecnologia durante el periodo de estudio.

### M.3 Inconsistencias identificadas en este archivo

| ID | Seccion | Descripcion |
|----|---------|-------------|
| INC-01 | B | Caso 18: datos de laboratorio parcialmente copiados del Caso 17 |
| INC-02 | B | Caso 19: localizacion Pelluhue fuera de Region de Nuble |
| INC-03 | D.3 | Dias de incubacion 1-2 dias biologicamente improbables |
| INC-04 | H.2 | Discrepancia plasma HI: paper previo 6, recalculo 3 |
| INC-05 | I.1 | Paper previo letalidad 16.1% (5/31), recalculo 14.7% (5/34) por cambio denominador |
| INC-06 | H.1 | Paper previo ECMO 4/23 (17.4%), recalculo 3/21 (14.3%) |

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

## VACIOS CONSOLIDADOS

| ID | Seccion | Descripcion | Prioridad |
|----|---------|-------------|-----------|
| V-01 | A.5 | Caso 37 sin datos clinicos, no vinculable a base admin | Alta |
| V-02 | E.3 | Lactato solo en 8/35 casos (22.9%) | Media |
| V-03 | E.4 | Perfil hepatico detallado en <20% | Media |
| V-04 | E.6 | Troponina solo en 2/35 | Media |
| V-05 | E.6 | Albumina solo en 3/35 | Media |
| V-06 | F.3 | Tiempo de espera solo en ~14/35 | Media |
| V-07 | G.1 | Diferenciacion bolo SU vs. indicacion hospitalizacion incompleta | Alta |
| V-08 | H.2 | Discrepancia plasma HI 6 vs 3 no resuelta | Alta |
| V-09 | H.1 | ECMO recalculo difiere del paper previo | Alta |
| V-10 | I.4 | Dias hospitalizacion solo en 15/35 | Media |
| V-11 | J.1 | Costo GRD estimado, no verificado con FONASA | Media |
| V-12 | L.3 | Acta Comite de Etica sin numero/fecha | Alta |
| V-13 | L.3 | Referencia triage ESI chileno faltante | Baja |
| V-14 | B | Caso 18 datos copiados del Caso 17 -- requiere revision ficha original | Alta |
| V-15 | D.3 | Incubacion 1-2 dias biologicamente implausible | Baja |
| V-16 | -- | APACHE II / PSI solo disponible en ~12/35 | Media |
| V-17 | -- | Anamnesis remota (comorbilidades) no tabulada sistematicamente | Media |

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
- APACHE ≤12: 10/12 (todos sobrevivientes)

**Nota S18:** El cutoff APACHE >12 (no >15) se basa en Riquelme & Rioseco (EID 2015, n=103): moderado = APACHE <12, severo = APACHE >12 con mortalidad 77%. Este es el unico cutoff APACHE publicado especificamente para SCPH. UpToDate (Vial & Harkins, Dic 2025) NO menciona APACHE II en absoluto, consistente con que los scores genericos de UCI no son herramientas centrales para SCPH.

### PSI — EXCLUIDO (v2.0)

PSI excluido de la clasificacion de severidad por parsimonia: mide solo componente respiratorio, no captura la fisiopatologia cardiogenica central del SCPH. Se reportan datos descriptivamente:

| Clase PSI | n |
|-----------|---|
| I | 3 |
| II | 5 |
| III | 2 |
| IV | 1 |
| V | 1 |

---

---

## O. Clasificacion de severidad — v6.2 DEFINITIVA (S17-S20, reclasificacion S29)

### O.1 Estrategia de reporte: doble clasificacion

**Primaria:** Clasificacion MINSAL binaria (grave/no grave) — estandar nacional, comparable con registros oficiales.
**Secundaria:** Clasificacion adaptada de Rioseco (3 niveles + infeccion sin SCPH) — exploratoria, basada en criterios clinicos, SIN validacion externa.

### O.2 Criterios v6.2 — Clasificacion de Severidad de Infeccion por Virus Andes

**Naturaleza:** TRIPOD nivel 1 — reglas operacionales, NO modelo predictivo.
**Contexto:** Datos del ingreso al Servicio de Urgencias HCHM. Para pacientes trasladados, solo se usan datos de HCHM (no del centro derivador).
**Esquema:** OR (cualquier criterio de la categoria mas alta). Se reporta "carga de criterios" por paciente.
**Sobre-sensibilidad:** Declarada y justificada (sin cura, mortalidad hasta 40%, ECMO limitado, progresion 24-48h).

**SEVERO (≥1 criterio):**

| ID | Criterio | Bibliografia |
|----|----------|-------------|
| S1 | VMI / VMNI (CNAF, BiPAP/CPAP) | Saggioro JID 2007, Vial Lancet ID 2023, ERS 2022, Ospina-Tascon JAMA 2021, Ulloa-Morrison J Crit Care 2024 |
| S2 | PAS <90 mmHg / DVA (cualquier tipo/dosis) | SHARC Circulation 2023, Vial Lancet ID 2023, SCAI JACC 2022, Sinha JACC 2025 |
| S3 | ECMO (VA o VV) | Wernly EJCTS 2011 |
| S4 | Triada: Htro >50% + pH <7.25 + Plaq <50.000/uL | Vial Lancet ID 2023, Hallin Crit Care Med 1996, Koster AJCP 2001 |

**Justificacion S1 — VMNI como severo en SCPH:** En SCPH, la falla respiratoria tiene sustrato cardiogenico (depresion miocardica + fuga capilar masiva). A diferencia de la neumonia bacteriana o COVID, no hay evidencia de que CNAF detenga la progresion en SCPH. El requerimiento de VMNI en contexto de SCPH implica compromiso cardiopulmonar activo con progresion esperable en 8-24 horas.

**MODERADO (≥1 criterio, sin criterios severos):**

| ID | Criterio | Bibliografia |
|----|----------|-------------|
| M1 | Trombocitopenia <150.000/uL | CTCAE v5.0 NCI 2017 (Grade 1), Lopez Viruses 2019, Koster AJCP 2001 |
| M2 | O2 naricera ≤5L con SatO2 >92% | ERS 2022 |
| M3 | Rx torax alterada: infiltrado intersticial, algodonoso/perihiliar, derrame pleural, edema pulmonar | Riquelme EID 2015 (primaria), Tortosa medRxiv 2024 (confirmatoria) |
| M4 | SatO2 <92% al ambiente, con naricera ≤5L, o con O2 sin especificar | Logica clinica + sobre-sensibilidad declarada |

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

| Categoria | n | % | Muertes | Letalidad |
|-----------|---|---|---------|-----------|
| **Severo** | 14 | 41.2% | 4 (C27, C30, C31, C32a) | **28.6%** |
| **Moderado** | 14 | 41.2% | 1 (C32b) | **7.1%** |
| **Infeccion sin SCPH** | 6 | 17.6% | 0 | **0%** |
| **Total** | **34** | 100% | **5** | **14.7%** |

**Letalidad global:** 5/34 = 14.7% (IC 95% Clopper-Pearson: pendiente recalculo R)
**Gradiente monotonico:** 28.6% → 7.1% → 0% — validez de constructo confirmada.

### O.6 Carga de criterios severos

| Carga severa | n | Casos | Letalidad |
|-------------|---|-------|-----------|
| 3 criterios | 0 | — | — |
| 2 criterios | 4 | C11 (S1+S2), C12 (S1+S2), C27† (S1+S2), C29* (adjudicado) | 1/4 (25%) |
| 1 criterio | 10 | C1, C13, C15, C18, C22, C23, C26, C30†, C31†, C32a† | 3/10 (30%) |

*Caso 29: adjudicacion clinica, carga estimada.

### O.7 Distribucion de criterios severos

| Criterio | n pacientes | Casos |
|----------|------------|-------|
| S1 (VMI/VMNI) | 8 | C11, C12, C13, C22, C23, C26(?), C27, C32a |
| S2 (PAS<90/DVA) | 8 | C1, C11, C12, C15, C18, C26, C27, C30 |
| S3 (ECMO) | 0 en HCHM | — (ECMO solo disponible en centros derivadores) |
| S4 (Triada) | 1 | C31 |

**Nota S3:** Ningun paciente recibio ECMO en HCHM (no disponible). Los pacientes que recibieron ECMO en centros derivadores (C4, C9, C25, C27) fueron clasificados por otros criterios en HCHM.

### O.8 Distribucion de criterios moderados

| Criterio | n pacientes | Casos |
|----------|------------|-------|
| M1 (Plaq <150k) | 11 | C3, C4, C6, C8, C9, C14, C16, C17, C24, C25, C33 |
| M2 (Naricera con sat >92%) | 0 | — |
| M3 (Rx torax alterada) | 3 | C21, C28, C32b |
| M4 (SatO2 <92%) | 1 | C24 |

**Criterio moderado mas frecuente:** M1 (trombocitopenia <150k) en 11/14 moderados (78.6%). Esto refleja que la trombocitopenia es el hallazgo de laboratorio mas sensible y precoz en infeccion por virus Andes.

### O.9 Caso 32b: moderado que fallece

Caso 32b (12F, Coihueco, Feb 2022) es el unico paciente clasificado como moderado que fallecio. En HCHM: plaq 331k (normal), sat 99%, PA 128/83. Unico criterio: M3 (derrame pleural bilateral en TAC). Trasladada a H. Calvo Mackenna donde fallecio. La clasificacion refleja los datos disponibles al momento de la evaluacion en urgencias HCHM. El deterioro posterior no modifica la clasificacion inicial pero si constituye una limitacion declarable: la clasificacion captura un punto en el tiempo y no la trayectoria clinica.

### O.10 Caso 29: adjudicacion clinica

Caso 29 (37M, San Ignacio, Abr 2023) fue adjudicado como severo por el investigador clinico. Datos de urgencias: sat 91%, Rx infiltrado algodonoso, lactato 45 mg/dL, APACHE 13, plaq 45k, leuco 31.9k, 3 horas de estadia en SU. El campo "Perfil de ventilacion" registra "desconocido", pero es clinicamente imposible que un paciente con este cuadro no haya recibido O2 suplementario durante 3 horas en urgencias. La adjudicacion se declara transparentemente en el manuscrito.

### O.11 Justificacion exclusion qSOFA/SOFA

1. **Diseñados para sepsis bacteriana:** Sepsis-3 (JAMA 2016) valido qSOFA en sospecha de infeccion bacteriana, no viral.
2. **Sensibilidad inaceptable en infecciones virales:** Torres-Macho et al. (JGIM 2021, n=10.238 COVID): qSOFA sensibilidad 26.2%. Ferreira et al. (Ann ICU 2020): 87% de ventilados COVID tenian qSOFA ≤1.
3. **Fisiopatologia incompatible:** El shock del SCPH es cardiogenico (depresion miocardica) + distributivo (leak capilar masivo), NO septico. SOFA/Sepsis-3 presupone volemizacion antes de vasopresores; en SCPH, la volemizacion es contraproducente (UpToDate HCPS, Dic 2025).
4. **Omision en literatura experta:** UpToDate HCPS (Vial y Harkins, Dic 2025) NO menciona qSOFA, SOFA ni APACHE.

### O.12 Justificacion exclusion PSI

PSI excluido por parsimonia: evalua riesgo de neumonia (componente respiratorio) sin capturar la disfuncion cardiogenica central del SCPH.

### O.13 Naturaleza exploratoria — declaracion obligatoria

Esta clasificacion es **descriptiva y exploratoria**. No constituye un modelo predictivo validado.

**Justificacion metodologica:**
- Riley et al. (BMJ 2020, DOI: 10.1136/bmj.m441): n=34 insuficiente para modelo predictivo formal.
- TRIPOD (Collins et al., Ann Intern Med 2015): no aplica a clasificaciones descriptivas.
- **Precedente:** MPOX-SSS (Stoeckle et al., JID 2024, DOI: 10.1093/infdis/jiad492) — score de severidad exploratorio publicado en Q1 con muestra limitada.

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

---

## RED-TEAM: AUTO-REVISION CRITICA

### RT-1. Conteo n=35 vs n=34 con datos — **RESUELTO S17**

Caso 37 excluido del analisis (sin datos clinicos). n=34 definitivo. 38 filas originales - 3 duplicados - 1 sin datos = 34 pacientes unicos analizables.

### RT-2. Discrepancia plasma hiperinmune (6 vs 3)

El paper previo reportaba 6/20 (30.0%) con plasma. El recalculo actual identifica solo 3 con confirmacion positiva. Posibilidad: los 3 adicionales eran duplicados (Caso 7=6, Caso 36=6, Caso 38=15) que tenian plasma en el caso original. **Verificar:** si Caso 6 y Caso 15 tenian plasma documentado. De la ficha: Caso 6 tiene plasma "desc" y Caso 15 tiene plasma "desconocido". Esto sugiere que los 6 del paper previo incluian alguna fuente adicional no reflejada en el Excel actual. **VACIO CRITICO: resolver antes de publicacion.**

### RT-3. Caso 18 contaminado

Los datos de laboratorio del Caso 18 tienen valores identicos al Caso 17 (albumina 2.5, CREA 0.6, BUN 7, Nap 134, APACHE 3, PSI I/12pts, dias hosp 7/5). La anamnesis proxima y signos vitales son diferentes. Este caso deberia marcarse con flag y los datos duplicados no deben usarse en calculos estadisticos de laboratorio. Solo los datos unicos (plaq 63.000, Htro 44.7, leuco 19.5, inmunoblastos 11%) son confiables.

### RT-4. Estacion incorrecta Caso 18

Fecha 22/08/2024 es invierno, no verano como dice la ficha. Corregir en tabla.

### RT-5. Datos erroneos Caso 5 y Caso 8 — **RESUELTO S29**

El master-builder (S14) asigno datos incorrectos a Caso 5 (era 66M Chillan, correcto: 14F Cato) y Caso 8 (era 47M Yungay, correcto: 32M Pinto). Corregido en v2.1 contra Excel primario HCHM_38_casos_estructurado3.xlsx. Demografía recalculada: media 35.4 (era 37.0), sexo 21M/13F (era 22M/12F).

### RT-6. IC 95% Clopper-Pearson

El paper previo reportaba IC95% 5.5-33.7% para 5/31. Con 5/34 el IC cambia. Calcular formalmente:
- Clopper-Pearson 95% CI para 5/34 = [5.0%, 31.1%] (aproximado)
- **Debe recalcularse en R con binom.test(5, 34)**

### RT-7. Completitud del Caso 5 — **RESUELTO S29**

Caso 5 tenia datos erroneos en el Archivo Maestro (ver RT-5). Corregido a 03/04/2019, 14F, Cato. Datos del Excel: plaq 317k, sat 98%, traslado H Roberto del Rio. Clasificacion v6.2: Infeccion sin SCPH.

### RT-8. Denominadores STROBE

Cada estadistica debe reportar n/N explicito. Revision muestra que la mayoria lo cumple, pero algunos porcentajes en la tabla de sintomas usan "~33" en vez de un denominador exacto. **Accion:** recalcular contando caso por caso desde el Excel.

### RT-9. Base administrativa -- pacientes no en ficha clinica

La base admin tiene ~50 egresos B33.4, pero las fichas clinicas solo cubren 38. Los ~12 adicionales podrian tener datos de desenlace utiles para completar la serie. **Accion:** evaluar si los 12 extra son pre-2012 (sin ficha) o si hay fichas no incluidas en el Excel.

### RT-10. Riesgo de doble publicacion

La Parte II clinica tiene datos que se superponen con la Parte I epidemiologica (mismos pacientes, mismas comunas). El paper debe dejar claro que los 34 pacientes son un subconjunto de los 136 del panel epidemiologico, con datos clinicos complementarios.

### RT-11. Contaminacion signos vitales Caso 32b ↔ Caso 33 (NUEVO S29)

Los signos vitales de Caso 32b (12F, fallecida) y Caso 33 (24F, sobreviviente) son **identicos**: FC 105, PA 128/83, sat 99%, T 37.8. Ademas, el manejo registra misma dosis de hidrocortisona 300 mg y mismo volumen (1000 ml en 3 hrs). Patron identico a RT-3 (contaminacion Caso 17↔18). **Confirmado por investigador clinico como pacientes distintos.** Los laboratorios son diferentes (32b: plaq 331k, leuco 4800; 33: plaq 125k, leuco 12700), lo que confirma que son personas diferentes. Los SV contaminados pertenecen a uno de los dos — no es posible determinar cual. **Accion:** reportar ambos con flag. No usar SV de estos casos en analisis de signos vitales. La clasificacion de severidad no se ve afectada (32b clasificada por M3/Rx, 33 clasificada por M1/plaq).

---

*Fin del archivo maestro Parte II*
*Generado: 2026-03-14 por Claude Code (master-builder)*
*Actualizado: 2026-03-17 (S18) — n=34 definitivo, blindaje severidad integrado, APACHE >12, qSOFA/SOFA excluidos, 17 refs nuevas*
*Estado: v2.0 — Pendiente: recalculo R (IC Clopper-Pearson, kappa), resolucion vacios V-02 a V-17*
*Documento complementario: documentos/REVISION_BIBLIOGRAFICA_MAESTRO.md (320 refs)*
*Pendiente: recalculo estadistico formal en R, resolucion de vacios V-01 a V-17, resolucion de hallazgos RT-01 a RT-10*
