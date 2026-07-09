# Investigaciones crudas (deep-research)

Outputs completos y sin editar de las corridas de investigación bibliográfica (harness
multi-agente con verificación adversarial por voto). Cada archivo es el JSON que devolvió la
corrida: pregunta, hallazgos con cita y voto (3-0 / 2-1), refutados, huecos y fuentes.
**Esto es la evidencia primaria; el catálogo (`docs/failure-modes.md`) es la curaduría.**
Rescatados de la carpeta temporal de la sesión (se borraba en cualquier limpieza de Windows).

| # | Archivo | Qué buscó | Resultado |
|---|---------|-----------|-----------|
| 1 | `2026-07-06-...-failure-modes-literatura` | Vicios ADICIONALES al corpus de Lucas (cog-sci, metaciencia, evals 2025-26, causal) | 19 claims verificados; el synthesize se cayó (curado a mano en ADR 0101) |
| 2 | `2026-07-07-...-estructuras-por-vicio` | CASOS por vicio agrupados por TIPO de estructura (principio 9) | 23 claims; mapa 1≈8/6=4/3=4/7=2; ciegos 4/5/2 (ADR 0104) |
| 3 | `2026-07-07-...-puntos-ciegos` | Solo los ciegos: vicios 4, 5, 2 + colisionador | 22 claims; 4=6, 5=7, 2=5; queda colisionador/selección (ADR 0105) |
| 4 | `2026-07-09-...-estructuras-de-aha-pares` | El catálogo ESPEJO: estructuras de aha DE A PARES (aha + mal uso), tier A/B, ¿se paga en predicción? | 23 claims; 5 estructuras; falta el par entidad-oculta (Neptuno↔N-rays) — **pendiente de discutir con Lucas e integrar al catálogo** |
