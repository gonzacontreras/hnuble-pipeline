# HANDOFF S61 — Guia de uso para los 4 dias finales

**Deadline EID: 2026-04-14 06:00 UTC** (~3 dias desde 2026-04-11)
**Version pipeline:** S61 (W1-W15 activos, 4 frontends + workflow map)
**Para:** Gonzalo (medico, sin programacion — todo copy-paste)

---

## 1. Contexto en un parrafo

Este sistema es un pipeline autonomo que corre en GitHub Actions 24/7 sobre el manuscrito EID (Hantavirus Nuble). Recibe **tus anotaciones** desde 4 interfaces web, las procesa con 20+ agentes Claude en paralelo, valida cada edit contra blindajes M14 + canonical facts, calcula un **score bayesiano de probabilidad de aceptacion EID** y expone todo en un dashboard web. Existe porque el deadline es en 3 dias y necesitas un copiloto que trabaje mientras duermes. Todo reversible, todo trazable, cero edits ciegos al manuscrito.

---

## 2. Las 5 URLs que debes abrir

Cuando el deploy este vivo (revisa `gh run list --workflow=pages.yml` para confirmar):

| URL | Que es | Cuando usarla |
|-----|--------|---------------|
| `https://gonzacontreras.github.io/hnuble-pipeline/` | Landing con 9 cards | Punto de entrada — elige desde aqui |
| `https://gonzacontreras.github.io/hnuble-pipeline/live.html` | Que hace Claude Code en tiempo real | Ver heartbeat, agentes activos, fase actual |
| `https://gonzacontreras.github.io/hnuble-pipeline/encyclopedia.html` | 402 archivos en 13 categorias | Buscar un dato, CSV, memoria o decision |
| `https://gonzacontreras.github.io/hnuble-pipeline/paper-current.html` | **Anotar el manuscrito v5** | Tu herramienta principal |
| `https://gonzacontreras.github.io/hnuble-pipeline/paper-improved.html` | Diff + score EID + modelos | Revisar si W14 mejoro algo |

Complementarias (menos usadas a diario): `workflow.html` (mapa 69 nodos de W1-W15), `dashboard.html` (runs activos), `findings.html` (hallazgos agentes), `approvals.html` (HIL pendientes).

---

## 3. Guia de uso en 5 pasos

### Paso 1 — Anotar una parte del manuscrito

Abre `paper-current.html`. Veras el texto completo del manuscrito v5 condensado (3469 palabras, las que enviaste a EID). Seleccionas un trozo de texto con el mouse, eliges un **color** (ver seccion 4), escribes una nota corta en el popup, pulsas **Enviar**.

Que pasa por detras: el frontend hace `POST` a ntfy topic `hnuble-annotations` con JSON `{ann_id, selection, color, note, xpath}`. Tu navegador no necesita estar abierto despues.

### Paso 2 — El sistema procesa tu anotacion

Cada 5 minutos corre **W12 (annotation-consumer)** via cron. Lee el topic ntfy, dedupe por `ann_id`, escribe en `state/annotations.json` con `processed=false`, y dispara **W14 (master-orchestrator)** pasando el `ann_id`.

W14 es el cerebro. Segun el color decide que capas lanzar, corre agentes en paralelo, consolida resultados, pasa edit candidato por validator 5-fase, y si pasa lo escribe en `state/manuscript_improved.md` + marca `processed=true`.

### Paso 3 — W14 orquesta agentes en paralelo

Tiempo total: 5-10 minutos. Internamente:

- **Capa A (fact-check)**: number-validator, bias-auditor, stats-reviewer, causal-dag-validator, crossref-retraction-checker
- **Capa B (contenido)**: biologist-analyst, environmentalist-analyst, epidemiologist-analyst, methods-paper-writer, citation-manager, literature-review
- **Capa C (revision)**: strobe-checker, paper-review, scientific-critical-thinking, red-team
- **Capa D (sintesis)**: scientific-writing, journal-formatter, number-consistency-validator
- **Validator 5-fase**: INTENT / PLAN / RED-TEAM / EXECUTE / AUDIT (protocolo anti-bypass)
- **Cascade**: W13 recalcula score EID, W15 re-evalua modelos (si el edit toca algo estadistico)

Todos paralelizados con `asyncio.gather`. Si un agente falla, W14 lo ignora y sigue con el resto (no-blocking).

### Paso 4 — Revisar el resultado

Abre `paper-improved.html`. Ves 4 paneles:

1. **Diff side-by-side** — version actual vs mejorada, cambios resaltados
2. **Score EID** — 13 barras bayesianas + delta vs baseline + top 3 recomendaciones
3. **Changelog** — lista de ediciones con justificacion por agente que la propuso
4. **Panel modelos y herramientas** — los 8 modelos S29-K/Ward/Trilogia/Fire/etc con metricas ultima eval

Si ves un nuevo item verde en el diff, W14 lo aplico y paso validator.

### Paso 5 — Aceptar o revertir

**Te gusta el edit** → no hagas nada. W14 sigue. El edit ya esta en el manuscrito mejorado.

**NO te gusta** → vuelve a `paper-current.html`, anota el mismo parrafo en ROJO con nota `"no aplicar"` o `"revertir edit ann-xxx"`. W14 detecta el flag, revierte el cambio en `manuscript_improved.md`, y agrega entry al changelog como "reverted by user feedback".

Si quieres congelar TODO (caso raro, crisis) → `gh workflow disable w12-annotation.yml` en la terminal.

---

## 4. Los 3 colores explicados

| Color | Significado | Capas que dispara en W14 | Tiempo tipico |
|-------|-------------|--------------------------|---------------|
| **Amarillo** (duda/pregunta) | "No estoy seguro de este numero" | Capa A ligera: number-validator + bias-auditor + stats-reviewer | 3-5 min |
| **Verde** (sugerencia mejora) | "Aqui se puede decir mejor" | Capa B completa: biologist + environmentalist + methods-writer + citation-manager + literature-review + causal-dag | 7-10 min |
| **Rojo** (error) | "Esto esta mal, revisar" | Capa A completa + Capa C severa: strobe-checker + red-team + paper-review + scientific-critical-thinking | 8-12 min |

**Regla practica**: si dudas, usa amarillo. Es el mas barato en costo API y el menos disruptivo. El rojo solo cuando estas seguro de que hay un error.

---

## 5. El score EID bayesiano (como leerlo)

**Prior**: Beta(7, 18) = **28%** (base rate EID accept segun registros 2020-2025, 25 papers Nuble-related en cola)

**Modelo**: logit lineal con 11 componentes + intercepto β₀ = -0.9444

**Output**: score en [0, 1] + delta vs baseline v5 condensed + ranking de componentes por "lift" (cual mejoraria mas el score si subes 10 puntos) + top 3 recomendaciones accionables

**Los 11 componentes** (con peso):
1. `strobe_compliance` (0.10)
2. `tripod_ai_compliance` (0.08)
3. `epiforge_compliance` (0.06)
4. `stat_rigor` (0.12) — **se decompone en frontend en `model_descriptive_rigor` + `model_predictive_rigor`** → barras 12 y 13
5. `reproducibility` (0.10)
6. `novelty` (0.11)
7. `writing_quality` (0.09)
8. `ref_quality` (0.09)
9. `bias_coverage` (0.10)
10. `reviewer_anticipation` (0.08)
11. `journal_fit_eid` (0.07)

**Ejemplo interpretacion**: si `strobe_compliance` = 0.95 y `novelty` = 0.60, el ranking te dira que **subir novelty +10 pp es mas alto lift que pulir STROBE**, porque novelty tiene peso 0.11 y esta mas lejos del techo.

El score actual esta en `state/eid_score.json`. Se actualiza cada vez que W13 corre (automatico despues de cada W14 exitoso, o manual con `gh workflow run w13-eid-scorer.yml`).

---

## 6. Los 8 modelos activos que W15 evalua diariamente

W15 (model-evaluator) corre cron diario 06:00 UTC + on-demand. Ejecuta los scripts R originales contra los CSVs canonicos y reporta metricas en `state/model_evaluations.json`. Si alguno se degrada → alerta ntfy.

| # | Modelo | Metrica principal | Valor esperado |
|---|--------|-------------------|----------------|
| 1 | S29-K GLMM NegBin (descriptivo) | BSS Tier1 | 68.1% [61.7-74.0] |
| 2 | S29-K GLMM (predictivo, LOCO-CV) | IRR lag 5 | 0.734 [0.551-0.910] |
| 3 | Ward clustering k=3 | Silhouette | 0.595 |
| 4 | Ward RR Cluster1 vs 2+3 | RR (mid-p) | 1.59 (p=0.043) |
| 5 | Trilogia precoz Firth | AUC | 0.833 |
| 6 | Trilogia Firth (FR>22+Plaq<150k+Htro>ULN) | OR | 10.31 [2.1-50.4] |
| 7 | Fire x SCPH dual-pathway | IRR fire effect | 1.28 (p=0.044) |
| 8 | Fire x SCPH | PAF | 35% |
| + | Cluster 2023 El Carmen (Kulldorff) | RR | 2.14 |
| + | Framework operacional SEREMI/CONAF/SAG | — | documental |
| + | Decision curve analysis | Net benefit | positivo 0.1-0.6 |
| + | Walk-forward 14 folds | AUC mean | 0.728 |

**Importante**: si W15 reporta que alguna metrica cambio > ±5% del valor esperado → detente, investiga, no dejes que W14 escriba edits basados en eso.

---

## 7. Que hacer si algo falla

### No veo updates en `live.html`
Abre el dashboard en otra pestana. Verifica que `state/claude_live.json` tenga `heartbeat_sequence` reciente (<10 min). Si no, probablemente W12 no esta corriendo el cron. Fix rapido:
```bash
gh workflow run w12-annotation.yml
```

### Envie anotacion pero no aparece en `paper-improved.html`
Espera 5 min (cron W12) + 10 min (run W14) = **maximo 15 min**. Luego verifica:
```bash
gh run list --workflow=w12-annotation.yml --limit 3
gh run list --workflow=w14-master.yml --limit 3
```
Si ves `failed` → `gh run view --log` para ver el error.

### Score EID no actualiza
```bash
gh workflow run w13-eid-scorer.yml
```
Espera 2-3 min y refresca `paper-improved.html`.

### W14 timeout (>15 min)
Probablemente un agente de Capa B quedo colgado. Cancelar y re-lanzar:
```bash
gh run list --workflow=w14-master.yml --limit 1
gh run cancel <run-id>
gh workflow run w14-master.yml --field annotation_ids=<ann-id>
```

### Landing page no carga / 404
`gh workflow run pages.yml` para re-deploy manual de GitHub Pages.

### Encyclopedia.html muestra "file not found"
El encyclopedia.json puede tener paths stale. Regenerar:
```bash
gh workflow run w11-encyclopedia.yml
```

---

## 8. Comandos de emergencia (copy-paste ready)

```bash
# Disparar W14 manual sobre una anotacion especifica
gh workflow run w14-master.yml --field annotation_ids=ann-xxx

# Re-ejecutar calculo de score EID
gh workflow run w13-eid-scorer.yml

# Re-evaluar los 8 modelos
gh workflow run w15-model-eval.yml

# Reconstruir enciclopedia (402 archivos)
gh workflow run w11-encyclopedia.yml

# Ver ultimos 10 runs
gh run list --limit 10

# Ver logs del ultimo run (cualquier workflow)
gh run view --log

# Ver logs del ultimo run de un workflow especifico
gh run list --workflow=w14-master.yml --limit 1 --json databaseId --jq '.[0].databaseId' | xargs gh run view --log

# Cancelar un run colgado
gh run cancel <run-id>

# Pausar W12 (no mas procesamiento de anotaciones)
gh workflow disable w12-annotation.yml

# Reanudar W12
gh workflow enable w12-annotation.yml

# Ver status de state files criticos
gh api repos/gonzacontreras/hnuble-pipeline/contents/state/eid_score.json --jq '.sha'
gh api repos/gonzacontreras/hnuble-pipeline/contents/state/annotations.json --jq '.sha'

# Forzar re-deploy de GitHub Pages
gh workflow run pages.yml
```

---

## 9. Principio M14 (recordatorio)

**Ningun edit llega al manuscrito sin pasar validator 5-fase.** Cada edit candidato es evaluado por:

1. **No bypass blindajes M14** — no puede violar anti-bypass protocol, no edita secciones marcadas `LOCKED`, no remueve CI obligatorios, no introduce post-hoc filtering sin flag
2. **Canonical facts preservados** — no cambia los 136/103/33 casos, no altera el SHA256 del dataset, no re-numera tablas maestras, no modifica DOIs verificados
3. **No duplicacion de refs** — detecta si el edit introduce una ref ya presente en otra parte del manuscrito
4. **Word count ±50** — el edit no puede cambiar total de palabras en mas de ±50 (target: 3469, techo: 3500)
5. **Refs count ±2** — el edit no puede agregar/quitar mas de 2 refs en una sola pasada

**Si falla cualquier fase** → ntfy dispara alerta roja con detalle, edit NO se aplica, changelog queda con entry `validator_rejected` + razon. No perdiste nada, solo esa propuesta fue bloqueada.

**El validator es mas estricto que tu** — confia en el. Si bloquea un edit que "parece bueno", es porque toca un blindaje. Abre `state/validator_log.json` para ver detalles o pregunta a Claude Code.

---

## Resumen de una linea

Abre `paper-current.html`, anota con 3 colores, revisa en `paper-improved.html`, copia-paste los comandos bash si algo falla, confia en el validator 5-fase. Deadline 14-abr 06:00 UTC.

**Listo. A trabajar.**
