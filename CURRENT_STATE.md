# CURRENT_STATE — WAGER

> Estado vivo del repo: qué corre hoy, qué falta, próximo paso. Lo mantiene Claude Code
> al día en cada sesión (regla NORTH_STAR §0.10). El histórico detallado sesión-a-sesión
> está en `docs/archived/CURRENT_STATE_hist.md`; el registro de decisiones en `DECISION_LOG.md`.
> Última actualización: **2026-07-05**.

## Qué corre hoy (todo verde)

Reward path (Slice 1), harness interactivo (C1+C2+C3) y factory de derivación
(rivales + batería + certificados) **completos**. `pytest` → ~125 verdes, 2 skip
(tests LLM opt-in con `RUN_LLM_TESTS=1`). Python 3.13, venv `uv`, hook de pre-commit
activo (`git config core.hooksPath hooks`).

- `wager/reward/` — **zona cero-LLM** (allowlist de imports en CI): `seeds`, `distance`,
  `mdl`, `sandbox`, `scorer` (R, D_MAX, combinado energía+funcionales), `trajectory`
  (pivot largo→ancho, v0.68), `ladder`, `episode_score`.
- `wager/factory/` — `case_loader`, `derive_rivals`, `battery_builder`, `calibration`,
  `world_lint` (lado fábrica; LLM permitido).
- `wager/harness/` — `world_server` (verbos + ledger + humo + scoring), `source_view`,
  `episode` (loop LLM + trace), `case_episode`, kernel en proceso separado.
- `wager/report/` — `episode_report` (dossier E2E humano → `reports/`, regenerable).
- `cases/` — 6 mundos (ver abajo).

## Mundos (6 hechos)

| # | Caso | Suite | Bucket | Resultado |
|---|------|-------|--------|-----------|
| 1 | dummy_dose_v0 | causal-cliente | control | brecha de teoría 0.062 |
| 2-3 | latent_mix_v0/v1 | Latent | control | tríptico: v0 proxy limpio, v1 dial declarado |
| 4 | selection_bias_v0 | sampling | control (saturado) | collider+medición; R 0.97/0.99 a presupuesto pleno |
| 5 | **latent_mix_v2** | Latent | **[T] trofeo** | estado oculto por lote; **tríptico confirmado con solver real** |
| 6 | selection_bias_scarce_v0 | sampling | [T] | presupuesto ÷4 → **el presupuesto DISCRIMINA estilos** |

**Hallazgos centrales** (detalle en `DECISION_LOG.md` v0.64-v0.68):
- **v2 (trofeo)**: techo Bayes-adaptivo por ventana de calibración; en 10 episodios /
  2 familias (gpt-5.4 + DeepSeek) **nadie infiere composición por-lote** — máx R=0.666,
  muro conceptual ≈0.67 (≈0.33 R sin reclamar). La arquitectura que cerró v0 anota 0.096.
  Headroom genuino: falta juicio, no ejecución. Ledger completo en `cases/latent_mix_v2/E0_LEDGER.md`.
- **#6 (escasez)**: la escasez no bloquea el premio, **separa estilos** — gasto-apurado-sin-pensar
  vs profundidad-frugal (DeepSeek: 0.742 con 33% del presupuesto). Firmas conductuales al
  catálogo: `bought_unused_evidence`, `fabricated_precision`.
- Recurrente: **R y |ΔP| divergen** (4 apariciones) → presión sobre la pregunta κ (en espera).

## Infra de mundos-trayectoria (v0.68, lista para #11)

R1/R2/R3 cableados y testeados: pivot largo→ancho (`wager/reward/trajectory.py`, función
pura del reward path con tests de propiedad), guardia de persistencia enmendada (se
persiste lo DECLARADO `t_grid`, se bloquea lo DERIVADO `cal_window`), contrato de
cronograma + `cost_per_horizon`. `CaseMeta.trajectory_protocol` cablea el pivot end-to-end.

## En curso AHORA

1. **Reestructura de docs (v0.69)**: Decision Log movido a `DECISION_LOG.md` (append-only,
   guardia repunteada); headers `Estado` gigantes archivados en `docs/archived/`; CURRENT_STATE
   podado (este archivo). NORTH_STAR 912→363 líneas.
2. **Re-skin a "línea de proceso"** (neutral, anti-flag): en progreso — prosa + nombres de
   carpeta a vocabulario industrial; matemática intacta, certificados verificados idénticos.

## Próximo

**#11 — primer mundo ODE** (logístico saturante, suite Horizon): valida el 2º formalismo.
Spec de trabajo en `MUNDOS_DINAMICOS_CONTEXT.md`. Orden: contrato de fuentes → world+meta →
brief ciego → derivación → certificados → E0-probe. Vara: 1-2 sesiones.

Después: eventos mid-trayectoria (§10-15) → 1er mundo anti-vicio con certificado de trampa
necesaria (§10-16) → proto-designer con yield (§10-14) → llenar cartera → E1 multi-modelo → E2 RL.

**Decisiones pendientes de Lucas**: GO para re-orientar la matriz E1 a cobertura de failure
modes; prioridad del proto-designer.

**Deudas registradas sin gatillar**: barrido c_F suite sampling; κ (4 divergencias acumuladas);
re-elicitación rival (c); derivación automática para mundos-ventana.
