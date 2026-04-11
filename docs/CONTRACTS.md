# Contratos del Pipeline S61

Documentación de los mensajes y estructuras que fluyen entre frontend, workflows y state files.

## 1. `annotation_message_v1` — Frontend → ntfy → W12

Contrato del payload que `docs/paper-current.html` envía vía POST a `https://ntfy.sh/hnuble-annot-<secret>`.

### Topic

- **Producción**: `hnuble-annot-<hash-secreto-32-chars>` (guardado en `state/secrets_local.json`, git-ignored)
- **Test**: `hnuble-annot-test-<random>` (usado por B6.5 smoke test)

### Payload (JSON en body)

```json
{
  "schema_version": "v1",
  "annotation_id": "ann-2026-04-11-a1b2c3d4",
  "para_id": 12,
  "selection_start": 0,
  "selection_end": 50,
  "selected_text": "HCPS incidence in Ñuble 1.21/100k hab-year",
  "color": "yellow",
  "comment": "verificar que este número es correcto contra PAHO 2025",
  "ts": "2026-04-11T13:45:00Z",
  "user_agent": "Mozilla/5.0 ...",
  "para_section": "Results (epidemiology)",
  "prior_annotations_count": 3
}
```

### Headers ntfy

- `Title: Annotation <annotation_id>`
- `Priority: default` (3)
- `Tags: annotation,<color>`

### Validaciones

- `schema_version` debe ser exactamente `"v1"`
- `color` ∈ {`yellow`, `green`, `red`} (yellow=duda, green=mejora sugerida, red=error reportado)
- `para_id` ∈ [1, 40] (el manuscrito v5 tiene 40 párrafos)
- `selection_end > selection_start`
- `selected_text` y `comment` ≤ 2000 chars cada uno
- `ts` en formato ISO8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`)

### Consumer

`scripts/w12_annotation_listener.py` (cron cada 5 min):
1. Poll `https://ntfy.sh/<topic>/json?poll=1&since=10m`
2. Parse cada mensaje con `scripts/lib/annotations.parse_ntfy_message`
3. Validate con `annotations.validate`
4. Dedupe por `annotation_id`
5. Merge a `state/annotations.json`
6. Si hay nuevos → `gh workflow run w14-master.yml --field annotation_ids=<csv>`

---

## 2. Cascadas de workflows

Flujo de disparo después de una anotación:

```
Frontend POST ntfy
  ↓
W12 Annotation Listener (cron */5min)
  ↓ gh workflow run w14-master --field annotation_ids=<csv>
  ↓
W14 Master Orchestrator (workflow_dispatch, timeout 20min)
  ├─ Capa A (paralelo): number-validator, bias-auditor, epidemiologist-analyst,
  │                      stats-reviewer, clinical-reports, number-consistency-validator
  ├─ Capa B (paralelo): causal-dag-validator, biologist-analyst, environmentalist-analyst,
  │                      scientific-critical-thinking, methods-paper-writer, scientific-figures,
  │                      citation-manager, literature-review (+MCP PubMed)
  ├─ Capa C (paralelo): red-team, strobe-checker, journal-formatter,
  │                      figure-reviewer, paper-review, overlap-firewall
  └─ Capa D (secuencial): supervisor → manuscript-writer → validator 5-fase
  ↓
commit state/ + push
  ↓ gh workflow run w13-eid-scorer.yml (siempre)
  ↓ gh workflow run w8-hil.yml (siempre)
  ↓ gh workflow run w3-bias.yml (si números cambiaron)
  ↓ gh workflow run w7-retraction.yml (si refs cambiaron)
  ↓
deploy-pages (cron */30min + push a state/**)
  ↓
Frontend paper-improved.html polling 10s → detecta nueva versión → refresh diff+score+changelog
```

---

## 3. Validator 5-fase en Capa D W14

Antes de aceptar cualquier edit propuesto por `manuscript-writer`:

1. **M14 bypass check**: el edit no viola ninguno de los 14 blindajes canónicos (consulta `memory/CANONICAL_BLINDAJES_INDEX.md`)
2. **Canonical consistency**: todos los números del edit matchean `state/canonical_facts.json` (panel 136/103/33, BSS 68.1%, etc.)
3. **No duplicate refs**: el edit no añade referencia ya existente en la lista 50 refs
4. **Word count ±50**: `|new_total_wc - 3469| ≤ 50`
5. **Refs count ±2**: `|new_refs_count - 50| ≤ 2`

Si cualquier fase falla → edit revertido, entry en `state/improvement_log.json` con `validator_passed=false` y razón.

---

## 4. state/claude_live.json — Heartbeat de Claude Code

Escrito manualmente por el Claude Code principal durante construcción del pipeline. Leído por `docs/live.html` y `docs/index.html` cada 3-5s.

Schema: `state/schemas/claude_live.schema.json`
Helper: `scripts/lib/claude_live.py` (funciones `heartbeat`, `start_block`, `finalize`, `error`)

Campos esperados por el frontend:
- `overall_status` ∈ {`running`, `active`, `idle`, `error`, `failed`}
- `current_block` (string corto, ej: `"B1.4"`)
- `current_block_label` (string legible, ej: `"frontend landing + contracts"`)
- `current_agent` (fallback si falta `current_block_label`)

---

## 5. Deploy automático de state/ → docs/state/

`.github/workflows/deploy-pages.yml` copia `state/*.json → docs/state/` en cada run (cron */30min + push a `docs/**` o `state/**`). El frontend hace `fetch('state/<file>.json')` (ruta relativa) sin necesidad de CORS, PAT ni proxy.
