# RUNBOOK S61 — Debugging y recovery del pipeline

**Sesion:** S61 (2026-04-11 a 2026-04-14)
**Repo:** gonzacontreras/hnuble-pipeline
**Deadline:** 2026-04-14 06:00 UTC

---

## 1. Topology

```
                      +------------------+
                      | paper-current.   |
                      | html (frontend)  |
                      +--------+---------+
                               |
                               | POST ntfy topic: hnuble-annotations
                               v
                      +------------------+
                      | ntfy.sh (relay)  |
                      +--------+---------+
                               |
                               | cron */5 min
                               v
              +----------------------------------+
              | W12 annotation-consumer          |
              | - dedupe by ann_id               |
              | - write state/annotations.json   |
              | - trigger W14 w/ annotation_ids  |
              +-----------------+----------------+
                                |
                                | workflow_dispatch
                                v
              +----------------------------------+
              | W14 master-orchestrator          |
              |                                  |
              |  Capa A (fact-check, parallel)   |
              |   +-- W1  number-validator       |
              |   +-- W3  bias-auditor           |
              |   +-- W5  stats-reviewer         |
              |   +-- W9  causal-dag-validator   |
              |   +-- W10 crossref-retraction    |
              |                                  |
              |  Capa B (content, parallel)      |
              |   +-- biologist-analyst          |
              |   +-- environmentalist-analyst   |
              |   +-- epidemiologist-analyst     |
              |   +-- methods-paper-writer       |
              |   +-- citation-manager           |
              |   +-- literature-review          |
              |                                  |
              |  Capa C (review, parallel)       |
              |   +-- strobe-checker             |
              |   +-- paper-review               |
              |   +-- scientific-critical        |
              |   +-- red-team                   |
              |                                  |
              |  Capa D (synthesis, serial)      |
              |   +-- scientific-writing         |
              |   +-- journal-formatter          |
              |   +-- number-consistency-val     |
              |                                  |
              |  Validator 5-fase (INTENT/PLAN/  |
              |   RED-TEAM/EXECUTE/AUDIT)        |
              +----+----------+---------+--------+
                   |          |         |
                   v          v         v
             +----------+ +-------+ +---------+
             | W13 EID  | | W7    | | W15     |
             | scorer   | | paper-| | model-  |
             |          | | build | | eval    |
             +----+-----+ +---+---+ +----+----+
                  |           |          |
                  v           v          v
             eid_score   manuscript  model_evals
             .json       _improved   .json
                         .md
                              |
                              v
                    paper-improved.html
                    (frontend render)
```

---

## 2. State files (16 archivos criticos)

| Archivo | Escribe | Lee | Proposito |
|---------|---------|-----|-----------|
| `state/annotations.json` | W12, W14 | W14, frontend | Cola de anotaciones pendientes |
| `state/manuscript_v5_condensed.json` | W7 (una vez) | W14, frontend | Version canonical del v5 (3469 pal) |
| `state/manuscript_control.md` | W7 | W14 | Baseline texto actual |
| `state/manuscript_improved.md` | W14 | W13, frontend | Version mejorada post-edits |
| `state/memory_bundle.json` | builder | agentes | 402 archivos de memoria consolidada |
| `state/canonical_facts.json` | manual | validator | 136/103/33 + refs + SHA256 |
| `state/encyclopedia.json` | W11 | frontend | 402 archivos indexados 13 cat |
| `state/eid_score.json` | W13 | frontend | Score bayesiano + 11 componentes |
| `state/model_evaluations.json` | W15 | frontend | 8 modelos + metricas |
| `state/claude_live.json` | hook live | frontend | Heartbeat + fase actual |
| `state/findings.json` | W1-W10 | frontend | Hallazgos agentes |
| `state/objections.json` | W4 red-team | W14 | Objeciones acumuladas |
| `state/paper_candidates.json` | W9 literature | citation-manager | Papers nuevos candidatos |
| `state/references.json` | citation-manager | W13 ref_quality | Lista refs activas |
| `state/pending_approvals.json` | W14 | HIL frontend | Edits HIL-gated |
| `state/pipeline_status.json` | todos | dashboard | Status global |
| `state/w10_queue.json` | W10 | W10 | Cola crossref check |
| `state/stability_history.json` | W13 | W13 | Historial scores |
| `state/validator_log.json` | W14 validator | frontend | Audit 5-fase |
| `state/schemas/*.json` | manual | todos los agentes | JSON Schema contracts |

---

## 3. Workflows activos

| # | Workflow | Trigger | Last-known | Proposito |
|---|----------|---------|------------|-----------|
| W1 | w1-number-validator | dispatch + W14 | OK | Verifica numeros en manuscrito |
| W2 | w2-canonical-facts | push schemas | OK | Hash canonical_facts.json |
| W3 | w3-bias-auditor | dispatch + W14 | OK | 27 modos de falla + anti-bypass |
| W4 | w4-red-team | cron 12h | OK | Genera objeciones estructurales |
| W5 | w5-stats-reviewer | dispatch + W14 | OK | Revision estadistica |
| W6 | w6-figures-validator | dispatch | OK | Verifica figuras vs CSVs |
| W7 | w7-paper-builder | dispatch | OK | Rebuild manuscript_improved |
| W8 | w8-cascade | W14 post | OK | Cascade downstream effects |
| W9 | w9-causal-dag | dispatch + W14 | OK | DAG structural validator |
| W10 | w10-crossref-retraction | cron 6h | OK | Check refs retracted |
| **W11** | **w11-encyclopedia** | cron 2h + push | NEW S61 | Build 402-file index |
| **W12** | **w12-annotation-consumer** | cron 5min | NEW S61 | Consume ntfy annotations |
| **W13** | **w13-eid-scorer** | post W14 | NEW S61 | Bayesian EID score |
| **W14** | **w14-master-orchestrator** | dispatch (W12) | NEW S61 | Run 20+ agents parallel |
| **W15** | **w15-model-eval** | cron daily 06:00 UTC | NEW S61 | 8 models metrics |
| pages | github-pages deploy | push docs/ | OK | GitHub Pages |

---

## 4. Secrets esperados en GitHub Actions

```
Settings > Secrets and variables > Actions > Repository secrets
```

| Secret | Usado por | Mandatory | Proposito |
|--------|-----------|-----------|-----------|
| `CLAUDE_API_KEY` | W1, W3, W5, W9, W10, W13, W14, W15 | YES | API Anthropic (agentes) |
| `NTFY_TOPIC` | W4, W14, W15, validator alerts | YES | Topic HIL global |
| `NTFY_TOPIC_ANNOTATIONS` | W12, frontend | YES | Topic anotaciones (separado del HIL global) |
| `GITHUB_TOKEN` | todos | auto | gh api, commit state |

**Verificacion**:
```bash
gh secret list --repo gonzacontreras/hnuble-pipeline
```

Debe listar los 3 secrets arriba (GITHUB_TOKEN es automatico).

**Si falta alguno** (sintoma: W1/W3/etc con `exit 1` y `KeyError: CLAUDE_API_KEY`):
```bash
gh secret set CLAUDE_API_KEY --body "sk-ant-..."
gh secret set NTFY_TOPIC --body "hnuble-hil"
gh secret set NTFY_TOPIC_ANNOTATIONS --body "hnuble-annotations"
```

---

## 5. Comandos de recovery

### memory_bundle.json corrupto o stale
Sintoma: W14 agentes fallan con `JSONDecodeError` o `key 'project_...' not found`.
Fix:
```bash
python scripts/build_memory_bundle.py --out state/memory_bundle.json
git add state/memory_bundle.json
git commit -m "fix: rebuild memory bundle"
git push
```

### encyclopedia.json con items que no existen
Sintoma: encyclopedia.html muestra "file not found" al click.
Fix:
```bash
gh workflow run w11-encyclopedia.yml
# espera 2-3 min
gh run list --workflow=w11-encyclopedia.yml --limit 1
```

### Workflow bloqueado (queued > 10 min o in_progress > 20 min)
```bash
# Listar runs pendientes
gh run list --status queued
gh run list --status in_progress

# Cancelar run especifico
gh run cancel <run-id>

# Re-disparar
gh workflow run <workflow-name>.yml
```

### W14 dejo anotaciones en `processed=false` despues de error
Sintoma: `state/annotations.json` con items sin procesar pero W14 exit 0.
Fix manual via Python:
```python
import json
from pathlib import Path
p = Path('state/annotations.json')
data = json.loads(p.read_text(encoding='utf-8'))
stuck = [a for a in data['annotations'] if not a.get('processed')]
print(f"Stuck: {len(stuck)}")
for a in stuck:
    a['processed'] = False  # forzar reprocessing
    a.pop('processing_started_at', None)
p.write_text(json.dumps(data, indent=2), encoding='utf-8')
```
Luego:
```bash
git add state/annotations.json && git commit -m "fix: reset stuck annotations" && git push
gh workflow run w14-master.yml --field annotation_ids=<ids-comma-sep>
```

### validator_log.json crece sin freno (>10 MB)
Sintoma: commits lentos, push rechazado.
Fix: rotar log.
```bash
mv state/validator_log.json state/archive/validator_log_$(date +%Y%m%d).json
echo '{"entries":[]}' > state/validator_log.json
git add state/validator_log.json state/archive/
git commit -m "chore: rotate validator log"
git push
```

### GitHub Pages deploy falla
```bash
gh workflow run pages.yml
gh run list --workflow=pages.yml --limit 3
# si persiste:
gh api repos/gonzacontreras/hnuble-pipeline/pages --jq '.status'
```

---

## 6. Metricas clave a monitorear

Revisar cada 4-6 horas durante los 3 dias finales:

| Metrica | Comando | Valor OK | Alerta si |
|---------|---------|----------|-----------|
| Runs failing | `gh run list --status failure --limit 10` | <3 en ultimas 24h | >5 en 1h |
| Score EID estable | `jq '.score' state/eid_score.json` | >=0.55 y monotono | caida >0.05 |
| Annotations processed ratio | `jq '[.annotations[] \| select(.processed)] \| length' state/annotations.json` | >90% del total | <80% |
| Heartbeat | `jq '.heartbeat_sequence' state/claude_live.json` | incrementa cada run | sin cambio >30 min |
| Word count manuscript_improved | `wc -w state/manuscript_improved.md` | 3419-3519 (±50 de 3469) | fuera rango |
| Refs count | `jq '.references \| length' state/references.json` | 48-52 (±2 de 50) | fuera rango |
| Models eval freshness | `jq '.last_run' state/model_evaluations.json` | <24h | >48h |

**Dashboard de un solo comando** (guardar como alias):
```bash
gh run list --limit 5 && \
  jq -r '"score: \(.score) (\(.delta_vs_baseline))"' state/eid_score.json && \
  jq -r '"annotations: \([.annotations[] | select(.processed)] | length) / \(.annotations | length)"' state/annotations.json && \
  jq -r '"heartbeat: \(.heartbeat_sequence) phase: \(.current_phase)"' state/claude_live.json
```

---

## 7. Post-submission cleanup (post 2026-04-14 06:00 UTC)

Una vez enviado el manuscrito a EID:

### Paso 1: Archivar anotaciones
```bash
mkdir -p state/archive
cp state/annotations.json state/archive/annotations_S61_$(date +%Y%m%d).json
echo '{"annotations":[],"version":"post_S61","archived":true}' > state/annotations.json
git add state/ && git commit -m "archive: S61 annotations post-submission"
```

### Paso 2: Congelar W14 temporal disabling cron W12
```bash
gh workflow disable w12-annotation.yml
gh workflow disable w14-master.yml
gh workflow disable w15-model-eval.yml
# mantener activos: W11 encyclopedia, W13 scorer, W4 red-team (para reviewer response)
```

### Paso 3: Generar reporte final de versiones
```bash
# Guardar snapshot final manuscrito
cp state/manuscript_improved.md state/archive/manuscript_FINAL_submitted_$(date +%Y%m%d).md
cp state/eid_score.json state/archive/eid_score_FINAL_$(date +%Y%m%d).json
cp state/model_evaluations.json state/archive/model_evaluations_FINAL_$(date +%Y%m%d).json

# Generar reporte
python scripts/generate_submission_report.py \
  --manuscript state/archive/manuscript_FINAL_submitted_*.md \
  --score state/archive/eid_score_FINAL_*.json \
  --models state/archive/model_evaluations_FINAL_*.json \
  --out docs/S61_SUBMISSION_REPORT.md

git add docs/S61_SUBMISSION_REPORT.md state/archive/
git commit -m "archive: S61 final submission snapshot"
git push
```

### Paso 4: Preparar para ciclo reviewer-response (proxima sesion)
Reactivar solo W4 red-team y W10 crossref para mantener refs verificadas durante revision editorial.

---

## 8. Contactos / escalacion

- **Error critico que bloquea submission** → ntfy topic `hnuble-hil` (alerta en tu telefono)
- **Agente Claude API 429/503** → esperar 5 min, re-lanzar. Si persiste >30 min → revisar status.anthropic.com
- **GitHub Actions down** → status.github.com. Fallback: correr W1/W3/W5 localmente con `python scripts/run_local.py`
- **ntfy.sh down** → frontend guarda anotaciones en localStorage hasta que reconecte (verificar en DevTools > Application > Local Storage)

---

**Fin runbook S61. Actualizar si algo cambia.**
