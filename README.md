# hnuble-pipeline

Hantavirus Ñuble 24/7 perfection pipeline. 11 workflows (W0-W10) orquestando 20 agentes en 6 capas para mantener el manuscrito EID en estado óptimo hasta submission y durante el ciclo de revisión.

## Arquitectura

| Workflow | Descripción | Cron | Modelo |
|----------|-------------|------|--------|
| W0 | Reconnaissance semanal | `0 6 * * 1` | Sonnet |
| W1 | Papers Q1 Watcher | `0 */12 * * *` | Sonnet |
| W2 | Language Polish | On-demand | Sonnet |
| W3 | Bias Hunter | `0 3 * * *` | Sonnet |
| W4 | Figure Iterator | On-demand | Sonnet |
| W5 | Reviewer Virtuals | `0 4 * * *` | Sonnet |
| W6 | Model Stability | `0 2 * * *` | — (R) |
| W7 | Retraction Check ⭐ | `0 */6 * * *` | Haiku |
| W8 | HIL ntfy | Continuo | — |
| W9 | Memory Cross-Checker (MCC) | Reactivo | Sonnet |
| W10 | Blindaje Upgrader (BU) | Reactivo | Sonnet |

## Estado

Baseline: 35 hallazgos S59, 50 referencias, dashboard público vía GitHub Pages.

## Dashboards

- `docs/dashboard.html` — estado live del pipeline
- `docs/encyclopedia.html` — enciclopedia del proyecto
- `docs/findings.html` — findings activos
- `docs/approvals.html` — HIL approvals pendientes

## Credenciales

- Secrets GitHub: `CLAUDE_API_KEY`, `NTFY_TOPIC`
- Canal HIL: ntfy.sh/hnuble-guardian-7k3q9mXz
