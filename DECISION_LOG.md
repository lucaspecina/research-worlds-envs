# Decision Log → movido a `docs/adr/`

El registro de decisiones ahora vive en **[`docs/adr/`](docs/adr/)**, con **una decisión
por archivo** (patrón ADR estándar, [adr.github.io](https://adr.github.io/)) y un
[índice](docs/adr/README.md). Se movió desde este archivo único en la migración de docs
(ADR 0070) para que sea navegable en vez de un blob de 700 líneas.

- **Append-only**: los archivos ADR existentes son inmutables; superseder = archivo nuevo.
- La guardia `scripts/check_decision_log.py` (pre-commit) lo verifica.
- Citas viejas del estilo "Decision Log v0.64" resuelven vía el índice (columna Versión).
