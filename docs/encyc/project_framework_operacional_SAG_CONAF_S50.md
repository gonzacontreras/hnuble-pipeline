---
name: Framework operacional multi-agencia SAG/CONAF/SEREMI basado en ψ lag 5 (S50)
description: Propuesta operacional S50 para transformar el signo negativo de ψ lag 5 (retención→dispersión) en un pipeline de alerta temprana con tres actores institucionales (SEREMI Salud, CONAF, SAG) y ventana operacional de 5 meses. Respaldo legal Ordinario MINSAL B38 N°3420 (2019). Contenido central de Public Health Implications en manuscrito EID.
type: project
---

# Framework operacional multi-agencia basado en ψ lag 5

## Origen
Gonzalo propuso en S50 (2026-04-05) extender la lectura ecológica del −ψ lag 5 a un framework de alerta temprana con tres actores institucionales distintos. No estaba registrado antes en memoria del proyecto, aunque la **implicación operacional SEREMI** ya estaba en reference_lag5_cadena_completa_S50.md:144 y :258.

## Principio central
El signo negativo de ψ lag 5 tiene **dos lecturas simultáneas** resueltas por el desfase temporal:
- **En el momento t:** el roedor está CONFINADO al parche quiloide (alimento + refugio + comunidad reproductiva). Riesgo peridoméstico momentáneo BAJO.
- **En t+5:** el roedor se DISPERSA al ecotono buscando sustento para la población aumentada. Riesgo peridoméstico ALTO.

Esta ventana de 5 meses es **tiempo operacional real** — suficiente para coordinar intervenciones multi-agencia antes de que ocurra el contagio humano.

## Anclaje legal-institucional
**Ordinario MINSAL B38 N°3420 (26 julio 2019)**, firmado Dra. Paula Daza, Subsecretaria Salud Pública:
> "Orientaciones técnicas por eventos asociados a roedores silvestres. Instruye coordinar con CONAF/SAG para identificar áreas de riesgo."

URL: `epi.minsal.cl/wp-content/uploads/2019/10/B38_3420_MINSAL_...pdf`
Fuente: `memory/reference_biblio_S22.md:72`

**Implicación:** la coordinación SEREMI/CONAF/SAG **ya está mandatada** por MINSAL desde 2019. Lo que falta es el **disparador temporal objetivo** — el satélite no opera como alarma, aunque el mandato existe. Este paper propone ese disparador.

## Pipeline operacional por ventana temporal

### Ventana 1 — t = 0 (NDVI cae AHORA, señal satelital activa)
**Lectura ecológica:** Retención. Quila muere sincrónicamente, culmos se desecan, el pixel Landsat 30m capta la desecación. Roedores concentrados en parche por alimento (50M frutos/ha) + refugio + comunidad reproductiva.

**Actor: CONAF**
- Control preventivo en parches boscosos con floración-muerte detectada por NDVI
- Cercado, señalética informativa, restricción de ingreso a recolectores de leña/frutos
- Coordinación con propietarios privados de predios forestales
- Monitoreo de densidad roedora mediante trampeo tipo Sherman (opcional, si existen recursos)

**Base legal:** Ley de Bosques + Ordinario MINSAL 2019.

### Ventana 2 — t = 0 a t+5 (5 meses de confinamiento)
**Lectura ecológica:** Sabemos dónde están los roedores. No están en el peridoméstico. El roedor no quiere salir del parche porque el óptimo local es máximo.

**Actor: SEREMI Salud**
- Mapa público de exclusión humana del parche quiloide activo (equivalente a "mapa de peligro volcánico" pero para hantavirus)
- Alertas a comunidades rurales en radio de 1-3 km del parche
- Educación en medidas de vivienda rural (sellado, limpieza segura, precauciones en bodegas)
- Coordinación con municipios y postas rurales
- Mensajería ocupacional a trabajadores forestales/agrícolas

**Base:** Código Sanitario Art. 67 (protección sanitaria de la población) + Ordinario MINSAL 2019.

### Ventana 3 — Justo antes de t+5 (dispersión inminente)
**Lectura ecológica:** Semillas agotadas, población aumentada no sostenible, dispersión forzada al ecotono en curso.

**Actor: SAG (Servicio Agrícola y Ganadero)**
- Inspección sanitaria preventiva en viviendas rurales del ecotono
- Control de plaga en bodegas de grano, gallineros, leñeras, silos
- Rodenticidas donde corresponda, bajo protocolo sanitario
- Inspección de predios agrícolas colindantes al parche
- Verificación de sellado de estructuras de almacenamiento

**Base:** Ley 18.755 (Ley Orgánica SAG) + Ordinario MINSAL 2019 + coordinación intersectorial.

### Ventana 4 — t+5 a t+10 (dispersión en curso, riesgo peridoméstico activo)
**Lectura ecológica:** Contagio ambiental en el ecotono. Trabajadores agrícolas/forestales expuestos. Riesgo máximo.

**Actor: SEREMI + SAG conjunto**
- Alerta epidemiológica reforzada
- Vigilancia activa de síntomas prodrómicos en poblaciones expuestas (ARF, síndrome gripal-like)
- Protocolos de limpieza segura en bodegas y estructuras rurales
- Coordinación con hospitales rurales y APS para alta sospecha clínica temprana
- Red de laboratorio para diagnóstico rápido (PCR ANDV)

## Comparación con literatura internacional

| Paper | Región | Proxy | Ventana operacional | Actores | Bifásico |
|---|---|---|---|---|---|
| Engelthaler 1999 EID | Four Corners USA | Precipitación + ENSO | ~12 meses | CDC + servicios salud | NO |
| Lowe 2014/2016 eLife | Brasil dengue | Clima + socioecon | 2-3 meses | Municipios | NO |
| Colón-González 2021 | Vietnam dengue | Temperatura + Niño | 3 meses | Gobierno nacional | NO |
| Andreo 2024 Pathogens | Argentina hantavirus | NDVI + fire | Variable | MSAL Argentina | NO |
| **Este trabajo** | **Ñuble Chile SCPH** | **NDVI floración quila** | **5 meses fijos** | **SEREMI + CONAF + SAG** | **SÍ** |

**Novedad del framework:** ninguno de los papers previos de early warning (a) propone un pipeline bifásico retención→dispersión, (b) coordina 3 actores institucionales distintos bajo un mismo proxy, (c) tiene una ventana operacional pre-especificada por fenología de la planta (5 meses = fase terminal de C. quila por González 2001).

## Anclaje clínico del framework: cluster C30 El Carmen 2023
Este cluster (bodega no ventilada, madre 49F fallecida + hijo 11M sobreviviente, sector rural) ocurrió **exactamente en la ventana de dispersión post-lag 5** en una zona sin alerta activa.

**Contrafactual:** si el framework hubiera estado operativo, SEREMI Ñuble habría notificado riesgo peridoméstico 5 meses antes (al detectar NDVI bajo en el parche quiloide asociado a El Carmen) y SAG habría inspeccionado bodegas rurales en El Carmen durante la ventana de dispersión.

El cluster C30 no es evidencia del modelo (eso sería razonamiento circular post-hoc); es **ilustración del caso tipo** que el framework está diseñado para prevenir.

## Papers Q1 para anclar la Discussion / Public Health Implications

1. **Engelthaler et al. 1999 EID** — primer early warning hantavirus Four Corners USA
2. **Lowe et al. 2016 eLife** — early warning dengue Brasil operacional
3. **Andreo et al. 2024 Pathogens** — precedente Argentina hantavirus con lags operacionales
4. **Ordinario MINSAL B38 N°3420 (2019)** — respaldo legal nacional
5. **Castillo et al. 2001 CHEST** (serie Temuco n=16, solo UCI) — 88% trabajadores forestales/agrícolas [**corregir contexto geográfico en manuscrito**]
6. **Riquelme et al. 2015 EID 21(4):562-568** (serie Puerto Montt n=103, espectro completo) — 87% peridoméstico/ocupacional [**corregir contexto geográfico en manuscrito**]
7. **González 2001 Bosque 22(2):45-51** — fenología C. quila, base pre-especificación lag 5
8. **Jaksic & Lima 2003 Austral Ecology** — ratización vs ratada
9. **Murúa et al. 2003 Oikos** — dinámica O. longicaudatus sur de Chile

## Integración en manuscrito EID

### Sección "Public Health Implications" (Discussion, ~250-350 palabras)
Estructura sugerida:
1. Problema actual: alertas reactivas, post-contagio, ineficaces para SCPH con letalidad 30-40%
2. Framework bifásico propuesto: retención → dispersión → contagio
3. Ventana operacional 5 meses: tiempo real para intervención
4. Tres actores coordinados: CONAF (parche), SEREMI (comunicación), SAG (ecotono)
5. Respaldo institucional: Ordinario MINSAL 2019
6. Comparación con Engelthaler 1999 / Lowe 2016 / Andreo 2024 (más corto, menos coordinado, no bifásico)
7. Limitaciones operacionales: requiere re-entrenamiento del modelo cada ~5 años con nuevo NDVI, coordinación intersectorial no trivial, costo del monitoreo satelital

### Figura operacional (opcional, para Supplementary o figura principal)
Esquema tipo timeline de 12 meses con:
- Señal NDVI (línea azul, cae en Mes 0)
- Fase retención (Meses 0-5, fondo verde)
- Fase dispersión (Meses 5-10, fondo naranja)
- Fase dilución (Meses 10+, fondo gris)
- Bandas operacionales de cada actor (CONAF, SEREMI, SAG) superpuestas

## Pendientes antes de integrar a manuscrito
1. **Conseguir Ordinario MINSAL B38 N°3420 en PDF** — verificar texto exacto de "coordinar con CONAF/SAG"
2. **Verificar Ley 18.755 SAG** — capítulo relevante para control sanitario en predios rurales
3. **Consultar con Gonzalo** si prefiere framework detallado en Discussion (~350 palabras) o condensado (~150 palabras) dado límite 3500 EID
4. **Decidir** si la figura operacional va en cuerpo principal (máximo 4-6 figuras EID) o en Supplementary

**Why:** Gonzalo identificó en S50 que el signo del ψ lag 5 no solo es interpretación ecológica sino valor operacional directo para 3 actores institucionales. El Ordinario MINSAL 2019 ya mandata la coordinación pero falta el disparador temporal objetivo. Este paper puede aportarlo.
**How to apply:** Leer esta nota al redactar Discussion / Public Health Implications en manuscrito EID. Usar como base para la sección más vendible del paper (EID premia impacto en salud pública). Contenido suficiente para ~250-350 palabras de Discussion.
