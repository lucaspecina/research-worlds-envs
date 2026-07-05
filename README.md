# WAGER — Worlds As Generators of Epistemic Reward

**Mundos sintéticos ejecutables para medir y entrenar el juicio investigativo de las IAs.**

Fabricamos pequeños universos-programa con una verdad oculta y trampas realistas. Una IA los
investiga con un presupuesto y entrega un modelo ejecutable; un juez **puramente matemático**
(jamás otra IA opinando) le pone una nota. Esa nota puede usarse como recompensa de entrenamiento
sin que se pueda hacer trampa. El objetivo: mundos donde la única ruta al éxito sea investigar
bien — actualizar ante la evidencia, salir de pozos, no exagerar, no refugiarse en lo familiar.

👉 **Para entender el proyecto desde cero, sin jerga: leé [`WIKI.md`](WIKI.md).**

## Setup

```bash
uv venv .venv --python 3.13
uv pip install -e .[dev,agent,report]
git config core.hooksPath hooks      # lints de docs + guardia de ADRs en pre-commit
.venv/Scripts/python -m pytest -q    # ~125 verdes
```

Credenciales de LLM (lado solver/fábrica) en `.env` (nunca se commitea). Ver `pyproject.toml`.

## Correr una partida

```bash
# un episodio real (modelo frontier vía API) sobre un caso, con dossier
.venv/Scripts/python cases/latent_mix_v2/e0_episode.py gpt-5.4 0
.venv/Scripts/python -m wager.report.episode_report cases/latent_mix_v2   # dossier E2E → reports/
```

## Mapa de documentos

| Documento | Para qué |
|---|---|
| [`WIKI.md`](WIKI.md) | Entender de cero, sin jerga, en profundidad |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Referencia técnica: contratos, scoring, rivales, batería, harness |
| [`CLAUDE.md`](CLAUDE.md) | Operativa del repo (reglas duras, workflow, convenciones) |
| [`docs/roadmap.md`](docs/roadmap.md) | Estado vivo + cartera E1 + programa E1→E4 |
| [`docs/adr/`](docs/adr/) | Decisiones (una por archivo, append-only) |
| [`docs/open-questions.md`](docs/open-questions.md) · [`docs/red-team.md`](docs/red-team.md) | Lo sin decidir · amenazas del proyecto |

## Estructura del código

```
wager/
  reward/     zona CERO-LLM (protegida por CI): distance, scorer, sandbox, trajectory, mdl
  factory/    lado fábrica (LLM permitido): derive_rivals, battery_builder, case_loader
  harness/    world_server, source_view, episode (loop LLM), kernel
  report/     dossier E2E humano
cases/        los mundos (world.py oculto, meta.json, brief.md, ladder/, certificados)
docs/         adr/, roadmap, open-questions, red-team, archived
```
