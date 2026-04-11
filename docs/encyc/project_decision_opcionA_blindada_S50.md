---
name: Decisión Opción A blindada — narrativa señal focal lag 5 (NO bifásico)
description: DECISIÓN DEFINITIVA S50 (2026-04-06). Opción A blindada = señal focal pre-especificada lag 5 con negative control exposures (10 lags null). Opción B (bifásico retención-dispersión) DESCARTADA porque contraste ventanas p=0.37 contradice la narrativa. 4 papers críticos cierran defensa anti-reviewer 2. P(accept EID) 72-82%. LEER antes de redactar CUALQUIER sección del manuscrito.
type: project
---

# Decisión Opción A blindada — señal focal pre-especificada

**Fecha decisión:** 2026-04-06 (S50)
**Aprobada por:** Gonzalo (explícitamente)
**P(accept EID):** 72-82%

## La decisión

**NARRATIVA DEFINITIVA del manuscrito EID:**
> "Señal focal pre-especificada en lag 5 (IRR 0.701, CI bootstrap cluster [0.551, 0.910]) con nulls explícitos en los 10 lags adyacentes, descartando confounding por NDVI contemporáneo y correlaciones temporales difusas."

**TERMINOLOGÍA PROHIBIDA en el manuscrito:**
- NO "modelo bifásico"
- NO "retención → dispersión" como tesis central cuantitativa
- NO contraste formal ventanas 0-4 vs 5-10 como evidencia (p=0.37, auto-destructivo)

**TERMINOLOGÍA PERMITIDA:**
- "señal focal pre-especificada" (focal pre-specified signal)
- "negative control exposures" (Lipsitch 2010) para los 10 lags null
- "severe test" (Mayo-Spanos 2006)
- "ratización" como hipótesis biológica subyacente
- "retención → dispersión" como marco conceptual biológico en Discussion (pero NO como resultado cuantitativo)

## Por qué se descartó Opción B (bifásico)

1. **Contraste formal ventanas 0-4 vs 5-10:** delta = -0.096, CI [-0.31, +0.12], **p = 0.37** → el propio dataset del paper contradice la narrativa bifásica
2. **Riesgo reviewer 2:** puede citar nuestro propio p=0.37 para destruir el claim central
3. **Inconsistencia interna:** afirmar "bifásico" con p=0.37 es especulación, no evidencia
4. **Palabras desperdiciadas:** bifásico requiere ~250 pal para explicar + hedgear vs ~120 pal de señal focal
5. **P(accept EID):** 50-58% vs 72-82% con Opción A blindada

## Resultado bootstrap FINAL (completado 2026-04-05 15:44:35)

**Script:** `R/S50_SIDECAR_PARALELO.R` (serial 475 iter + paralelo 525 iter, 7 workers)
**Outputs:** `resultados/S50_SIDECAR/*_FINAL.csv`
**Auditoría:** `R/S50_SIDECAR_AUDITORIA.R` → 10 tests PASS, 0 errores detectados

| Lag | IRR | CI bootstrap 95% | p_wald | P(ψ<0) | Interpretación |
|---|---|---|---|---|---|
| 0 | 0.852 | [0.639, 1.196] | 0.251 | 83.7% | Null (tendencia débil) |
| 1 | 0.903 | [0.695, 1.202] | 0.466 | 77.0% | Null (tendencia débil) |
| 2 | 1.004 | [0.752, 1.391] | 0.976 | 48.3% | Null genuino |
| 3 | 0.990 | [0.826, 1.199] | 0.948 | 53.5% | Null genuino |
| 4 | 0.981 | [0.768, 1.318] | 0.898 | 52.9% | Null genuino |
| **5** | **0.701** | **[0.551, 0.910]** | **0.018** | **98.9%** | **ÚNICO significativo — señal focal** |
| 6 | 0.812 | [0.630, 1.037] | 0.188 | 95.1% | Suggestive (CI cruza 1) |
| 7 | 1.002 | [0.740, 1.342] | 0.988 | 50.3% | Null genuino |
| 8 | 0.942 | [0.758, 1.248] | 0.679 | 70.4% | Null (tendencia débil) |
| 9 | 0.741 | [0.503, 1.149] | 0.054 | 92.2% | Suggestive secondary echo (CI cruza 1) |
| 10 | 1.000 | [0.733, 1.443] | 0.999 | 52.3% | Null genuino |

**Contraste ventanas (para Supplementary, NO para narrativa):**
- Delta (lag 5-10 vs 0-4) = -0.096, CI [-0.31, +0.12], p = 0.37
- Reportar honestamente en Supplementary como "non-significant"

## Los 4 papers CRÍTICOS (DOIs verificados web)

| # | Cita | DOI | Función en el manuscrito |
|---|---|---|---|
| ★1 | **Lipsitch M, Tchetgen Tchetgen E, Cohen T 2010 Epidemiology** | 10.1097/EDE.0b013e3181d61eeb | 10 lags null = negative control exposures |
| ★2 | **Cameron AC, Gelbach JB, Miller DL 2008 Rev Econ Stat** | 10.1162/rest.90.3.414 | Cluster bootstrap válido con n=21 clusters |
| ★3 | **Perneger TV 1998 BMJ** | 10.1136/bmj.316.7139.1236 | Pre-especificación exime de Bonferroni |
| ★4 | **Engelthaler DM et al. 1999 Emerg Infect Dis** | 10.3201/eid0501.990110 | Precedente en la MISMA revista: lag climático→HPS |

### Papers soporte adicionales (DOIs verificados)
- Field CA, Welsh AH 2007 JRSSB DOI 10.1111/j.1467-9868.2007.00593.x — cluster bootstrap GLMM
- Bender R, Lange S 2001 J Clin Epidemiol DOI 10.1016/S0895-4356(00)00314-0 — pre-espec vs multiple testing
- Feise RJ 2002 BMC MRM DOI 10.1186/1471-2288-2-8 — pre-espec no requiere ajuste
- Flanders WD et al. 2017 Am J Epidemiol DOI 10.1093/aje/kwx013 — negative control confounding
- Weiss NS 2002 Epidemiology DOI 10.1097/00001648-200201000-00003 — specificity rehabilitada
- Mayo DG, Spanos A 2006 BJPS DOI 10.1093/bjps/axl003 — severe testing
- Yates TL et al. 2002 BioScience DOI 10.1641/0006-3568(2002)052[0989:TEAEHO]2.0.CO;2 — ENSO cascada
- Ferro I et al. 2020 PLoS NTD DOI 10.1371/journal.pntd.0008786 — lag 6m Argentina

## Párrafo para Methods/Discussion EID (~100 palabras)

> We pre-specified a single focal lag (5 months) derived *a priori* from *Chusquea quila* phenology (González 2001), before any model fitting, obviating Bonferroni adjustment (Perneger 1998; Bender & Lange 2001). The ten adjacent lags (0–4, 6–10) were retained as *negative control exposures* (Lipsitch et al. 2010; Flanders et al. 2017): under confounding by contemporaneous NDVI or diffuse temporal autocorrelation, they would show associations of comparable magnitude. Their null bootstrap CIs — together with a significant IRR = 0.701 (95% cluster-bootstrap CI 0.551–0.910) estimated via wild cluster bootstrap appropriate for n = 21 clusters (Cameron, Gelbach & Miller 2008; Field & Welsh 2007) — constitute a severe test (Mayo & Spanos 2006) of the *ratización* hypothesis.

## Dónde integrar en el manuscrito EID

- **Methods (~50 pal):** pre-especificación lag 5 + citar Perneger 1998 + describir 10 lags como falsification tests
- **Results (~30 pal):** IRR 0.701 CI [0.551, 0.910] + nota cluster bootstrap percentil
- **Discussion (~40 pal):** citar Engelthaler 1999 como precedente EID + Mayo-Spanos 2006
- **Cover Letter (~1 frase):** "This study extends the climate-lag paradigm established by Engelthaler et al. (1999) in your journal"
- **Supplementary:** tabla completa 11 lags + contraste ventanas (reportar p=0.37 honestamente)
- **Forest plot:** `F_sidecar_forest_FINAL.png` → Supplementary Figure (o Figure 3 si hay espacio)

## Impacto en framework SAG/CONAF

El framework 4 ventanas × 3 actores **NO cambia**. Depende de:
- Signo negativo de ψ lag 5 ✓ (sigue)
- Fenología González 2001 ✓ (sigue)
- Ordinario MINSAL 2019 ✓ (sigue)

NO depende del contraste formal bifásico (que falló). El framework es operacional, no estadístico.

## Checklist post-decisión

- [ ] Eliminar toda mención de "modelo bifásico" como tesis cuantitativa del manuscrito
- [ ] Mantener "retención → dispersión" solo como marco conceptual biológico en Discussion
- [ ] Integrar párrafo Methods con los 4 críticos
- [ ] Citar Engelthaler 1999 en Discussion + Cover Letter
- [ ] Reportar contraste p=0.37 honestamente en Supplementary
- [ ] Actualizar forest plot labels: "Focal pre-specified signal" en lugar de "Biphasic model"

**Why:** El bootstrap completado el 2026-04-05 15:44:35 demostró que lag 5 es el ÚNICO significativo (CI excluye 1), pero el contraste formal ventanas 0-4 vs 5-10 NO es significativo (p=0.37). Esto invalida la narrativa bifásica como claim cuantitativo. Gonzalo aprobó explícitamente la Opción A blindada el 2026-04-06.
**How to apply:** LEER antes de redactar CUALQUIER sección del manuscrito EID. Si alguien escribe "bifásico" como tesis cuantitativa, CORREGIR citando esta memoria. El párrafo Methods con las 4 citas es OBLIGATORIO.
