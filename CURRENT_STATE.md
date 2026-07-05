# CURRENT_STATE — WAGER

> Estado vivo del repo: qué corre hoy, qué falta, próximo paso. Lo mantiene Claude Code
> al día en cada sesión. Complementos: `WIKI.md` (entender de cero), `ARCHITECTURE.md`
> (referencia técnica), `docs/adr/` (decisiones), `docs/roadmap.md` (programa E1→E4),
> `docs/open-questions.md` (lo sin decidir), `docs/red-team.md` (amenazas del proyecto).
> Histórico detallado en `docs/archived/`. Última actualización: **2026-07-05**.

## Qué corre hoy (todo verde)

Reward path (Slice 1), harness interactivo (C1+C2+C3) y factory de derivación
(rivales + batería + certificados) **completos**. `pytest` → ~125 verdes, 2 skip
(tests LLM opt-in con `RUN_LLM_TESTS=1`). Python 3.13, venv `uv`, hook de pre-commit
activo (`git config core.hooksPath hooks`).

- `wager/reward/` — **zona cero-LLM** (allowlist de imports en CI): `seeds`, `distance`,
  `mdl`, `sandbox`, `scorer` (R, D_MAX, combinado energía+funcionales), `trajectory`
  (pivot largo→ancho, ADR 0068), `ladder`, `episode_score`.
- `wager/factory/` — `case_loader`, `derive_rivals`, `battery_builder`, `calibration`,
  `world_lint` (lado fábrica; LLM permitido).
- `wager/harness/` — `world_server` (verbos + ledger + humo + scoring), `source_view`,
  `episode` (loop LLM + trace), `case_episode`, kernel en proceso separado.
- `wager/report/` — `episode_report` (dossier E2E humano → `reports/`, regenerable).

## Mundos (6 hechos)

| # | Caso | Suite | Bucket | Resultado |
|---|------|-------|--------|-----------|
| 1 | dummy_dose_v0 | causal-cliente | control | brecha de teoría 0.062 |
| 2-3 | latent_mix_v0/v1 | Latent | control | tríptico: v0 proxy limpio, v1 dial declarado |
| 4 | selection_bias_v0 | sampling | control (saturado) | collider+medición; R 0.97/0.99 pleno |
| 5 | **latent_mix_v2** | Latent | **[T] trofeo** | estado oculto por lote; **tríptico confirmado con solver real** |
| 6 | selection_bias_scarce_v0 | sampling | [T] | presupuesto ÷4 → **el presupuesto DISCRIMINA estilos** |

**Hallazgos centrales** (detalle en `docs/adr/` 0064-0068):
- **v2 (trofeo)**: techo Bayes por ventana; en 10 episodios / 2 familias **nadie infiere
  composición por-lote** — máx R=0.666, muro ≈0.67. La arquitectura que cerró v0 anota 0.096.
  Falta juicio, no ejecución. Ledger en `cases/latent_mix_v2/E0_LEDGER.md`.
- **#6 (escasez)**: no bloquea el premio, **separa estilos**. Firmas al catálogo:
  `bought_unused_evidence`, `fabricated_precision`.
- Recurrente: **R y |ΔP| divergen** (4 apariciones) → presión sobre κ (en espera, `docs/open-questions.md`).

## Cartera E1 (20 slots; 6 hechos)

> El mundo = **composición de operadores** con dificultad declarada, no trampas sueltas.
> Buckets: **[C]ontrol** (frontier debe aprobar) / **[T]rampa** (headroom buscado).
> Presupuesto holgado en [C], ajustado en [T] (el dial central). El programa que valida
> la cartera está en `docs/roadmap.md`.

| # | Slot | Suite | Formalismo | Bucket | Estado |
|---|------|-------|-----------|--------|--------|
| 1 | dummy_dose_v0 | causal-cliente | SCM | C | HECHO |
| 2 | latent_mix_v0 | Latent | SCM | C | HECHO (control negativo) |
| 3 | latent_mix_v1 | Latent | SCM | C | HECHO |
| 4 | selection_bias_v0 | sampling | SCM | C | HECHO (saturado) |
| 5 | latent_mix_v2 | Latent | SCM | T | HECHO (tríptico confirmado) |
| 6 | selection_bias_scarce_v0 | sampling | SCM | T | HECHO (presupuesto discrimina) |
| 7 | survivorship+censura | sampling | SCM | T | por autorar |
| 8 | immortal-time | sampling | SCM longitudinal | T | por autorar |
| 9 | batch-effect confundido | canal | SCM | T | por autorar |
| 10 | missingness informativo | canal | SCM | T | por autorar |
| 11 | **logístico saturante** | Horizon | **ODE** | C→T | **PRÓXIMO** (1er ODE, valida formalismo 2) |
| 12 | compartimental 2-tanques | Horizon | ODE | T | por autorar |
| 13 | colas M/M/k | diagnóstico | eventos discretos | T | por autorar (3er formalismo) |
| 14 | anomalía plantada | Anomaly | SCM | T | por autorar |
| 15 | anomalía temporal | Anomaly | ODE | T | por autorar |
| 16 | prior confiable | Prior | SCM | C | por autorar |
| 17 | prior traicionero (move-37) | Prior | SCM | T | por autorar |
| 18 | identificabilidad | identificabilidad | SCM | T | por autorar |
| 19 | triangulación | Horizon | SCM/ODE | T | por autorar |
| 20 | revelación secuencial | causal-cliente | SCM | T | por autorar |

Reglas: ningún [T] se certifica sin visibilidad de TODOS sus operadores + E0-probe con
headroom pre-registrado; cada [T] carga ≥2 coordenadas; los [C] son ~25% y ya están.
**Decisión pendiente de Lucas**: re-orientar los slots 7-20 a cobertura de failure modes
(`docs/open-questions.md` #16).

## Infra de mundos-trayectoria (ADR 0068, lista para #11)

R1/R2/R3 cableados y testeados: pivot largo→ancho (`wager/reward/trajectory.py`, función
pura con tests de propiedad), guardia de persistencia (persiste lo DECLARADO `t_grid`,
bloquea lo DERIVADO `cal_window`), contrato de cronograma + `cost_per_horizon`.

## En curso

**Reestructura de docs** (ADR 0070): Decision Log → `docs/adr/` (una por archivo); NORTH_STAR
disuelto (por qué→WIKI, diseño→ARCHITECTURE, ethos→CLAUDE, red-team→docs/, programa+open-Q→docs/);
WIKI.md nueva (entender de cero); CLAUDE.md a punteros. **Re-skin** a "línea de proceso"
(anti-flag): rename `mendel_subtypes→latent_mix` hecho; falta la prosa (grade→modo, scrap→rechazo).

## Próximo

**#11 — primer mundo ODE** (logístico saturante, Horizon): valida el 2º formalismo. Spec de
trabajo archivado en `docs/archived/MUNDOS_DINAMICOS_CONTEXT.md`. Orden: contrato de fuentes →
world+meta → brief ciego → derivación → certificados → E0-probe. Vara: 1-2 sesiones.

**Deudas registradas sin gatillar**: barrido c_F suite sampling; κ (4 divergencias); re-elicitación
rival (c); derivación automática para mundos-ventana; terminar la prosa del re-skin.
