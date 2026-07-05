# WAGER — ARCHITECTURE.md
## Diseño técnico (referencia; el "por qué" está en WIKI.md)

> **Qué es este documento.** El "cómo" a nivel de contratos, librerías y algoritmos — es un
> **índice** (ADR 0072); el detalle vive en `docs/reference/` (un archivo por tema, cada uno con
> sus marcadores `[ESTABLE]`/`[EN DEBATE]`, se abre solo el que la tarea pide). El "por qué" llano
> en `WIKI.md`; el ethos/reglas en `CLAUDE.md`; las decisiones en `docs/adr/`. Changelog histórico
> del header (v0.1→v0.14, del ARCHITECTURE monolítico) en [`docs/archived/ARCHITECTURE_changelog.md`](docs/archived/ARCHITECTURE_changelog.md).

## Índice de referencia

| Tema | Archivo | Secciones |
|---|---|---|
| El mundo + anatomía de un caso + tipos de caso + **contrato de ventana §10.1** | [`docs/reference/world-model.md`](docs/reference/world-model.md) | §1-2, §10-11 |
| Librería de operadores + generación de un caso | [`docs/reference/operators.md`](docs/reference/operators.md) | §3-4 |
| Rivales + algoritmo de batería | [`docs/reference/rivals-battery.md`](docs/reference/rivals-battery.md) | §5-6 |
| Scoring (R, D_MAX, score combinado, pivot de trayectorias) | [`docs/reference/scoring.md`](docs/reference/scoring.md) | §9 |
| Certificados + validación de la maquinaria (la pirámide) | [`docs/reference/certificates.md`](docs/reference/certificates.md) | §7, §13 |
| Episodio/harness + lo mínimo para E1 + open items | [`docs/reference/harness.md`](docs/reference/harness.md) | §8, §12, §14 |

