# docs/ — el índice maestro

> Un archivo, todo el mapa. Cuatro rutas rápidas según lo que busques:
> **entender algo** → los wikis del root · **un nombre/término** → [glosario](glosario.md) ·
> **un hallazgo/resultado** → [índice de hallazgos](research/README.md) ·
> **el estado y el próximo paso** → [roadmap](roadmap.md) (única fuente de verdad).

## Entrada (en el root del repo)

| Doc | Qué es |
|---|---|
| [WIKI.md](../WIKI.md) | La máquina WAGER desde cero: mundos, gemelos, puntaje |
| [WIKI-INDAGACION.md](../WIKI-INDAGACION.md) | El marco teórico: qué estudiamos, el ciclo, las perillas |
| [WIKI-SALTOS.md](../WIKI-SALTOS.md) | Los 11 saltos explicados, con tabla de un vistazo |
| [WIKI-FALLAS.md](../WIKI-FALLAS.md) | Dónde se rompe el ciclo de indagar (failure modes) |
| [CLAUDE.md](../CLAUDE.md) | Operativa del repo (reglas duras, workflow) |
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Índice de la referencia técnica → `docs/reference/` |

## Estado y plan

| Doc | Qué es |
|---|---|
| [roadmap.md](roadmap.md) | **Única fuente de verdad del estado** + próximo paso + programa E1→E4 |
| [open-questions.md](open-questions.md) | Lo sin decidir (inbox; al resolverse migra a un ADR) |
| [red-team.md](red-team.md) | Amenazas al proyecto |

## Marco y canon científico

| Doc | Qué es |
|---|---|
| [glosario.md](glosario.md) | Chuleta de una página: todos los nombres de la casa |
| [saltos.md](saltos.md) | EL LIBRO de los saltos: historias, fuentes, formalidad, biblioteca |
| [failure-modes.md](failure-modes.md) | La definición operativa del juicio + el catálogo vicios/ahas de a pares |
| [vicios/](vicios/README.md) | **Evidencia canónica por vicio** (un doc c/u; el README es el tablero; guardia en pre-commit) |
| [mundos-por-vicio.md](mundos-por-vicio.md) | La derivación vicio→mundo + estado de los mundos |
| [como-medimos.md](como-medimos.md) | CÓMO se mide (métodos de cada paper + doctrina medir-vs-premiar) |
| [lectura-de-fuentes.md](lectura-de-fuentes.md) | Registro AUDITABLE de lecturas a texto completo |
| [nota-direccion-revision-de-creencias.md](nota-direccion-revision-de-creencias.md) | Guía de la línea SECUNDARIA (revisión de creencias) |
| [posicionamiento-revision-de-creencias.md](posicionamiento-revision-de-creencias.md) | Mapa de competidores (16 papers) de esa línea |

## Registros (no se editan, se agregan)

| Dónde | Qué es |
|---|---|
| [research/](research/README.md) | Docs fechados de resultados/lecturas/autopsias — su README es el **índice de hallazgos** |
| [adr/](adr/) | Decisiones, una por archivo, append-only |

## Operativa y técnica

| Doc | Qué es |
|---|---|
| [operativa-codex-claude.md](operativa-codex-claude.md) | Reparto de roles Codex (supervisor) / Claude (worker) |
| [reference/](reference/) | Contratos, operadores, scoring, harness (abrir vía ARCHITECTURE) |

## Archivo (histórico — nada se borra)

| Dónde | Qué es |
|---|---|
| [archived/](archived/) | Docs de eras anteriores (specs cerradas, estados viejos, el NORTH_STAR original) |
| `cases/archive/` | Mundos de eras anteriores (con README de qué es cada familia) |
| `scripts/archive/` | Scripts de eras anteriores (+ `era_tests/`: sus tests) |
| `scripts/out/archive/` | Corridas viejas de agentes (crudos preservados) |

> **Convención de mantenimiento**: doc nuevo de primer nivel → una línea acá. Doc que muere →
> `archived/` con nota de motivo, jamás borrado.
