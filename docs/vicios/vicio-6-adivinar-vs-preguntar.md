# Vicio 6 — Adivinar en vez de preguntar (bloqueado: exige el verbo PREGUNTAR)

> Etiquetas y marco: ver [README](README.md). Sigue BLOQUEADO para construcción (agregar un
> oráculo consultable cambia el contrato de todos los mundos — decisión grande de Lucas).
> Lo construible hoy (elegir la pregunta que discrimina) ya tiene mundo diseñado (Mundo B).

## Sub-formas

- **6.1 Brecha reconocimiento-acción**: detecta la ambigüedad (60-80% si se le pide juzgarla) y
  pregunta <5% al responder. Su & Cardie `[VERIFICADO][VIÑETA]`. **El dato de diseño letal**:
  el contexto recuperado hace preguntar MENOS — *"darle datos para comprar hace que pregunte
  menos"* (R2): nuestro juego de comprar-evidencia SUPRIME el preguntar por estructura. Si un
  día se construye, el ASK debe ser más barato que comprar y la evidencia comprable
  insuficiente por diseño.
- **6.2 En agentes desplegados**: OSWorld-V2 `[VERIFICADO]` (adivina en vez de preguntar);
  DiscoBench `[POR-LEER][AGÉNTICO]` (F1 de detección de ambigüedad 16%; 0.07 preguntas de
  seguimiento por tarea; buscar repetido rinde peor que adivinar directo); inventa valores en
  campos vacíos `[POR-LEER]` (el vacío es intolerable — cruza con 3.1).
- **6.3 Con scaffold que pregunta**: "Ask or Assume?" `[POR-LEER]` — scaffold uncertainty-aware
  sube resolve-rate 61.2→69.4 en SWE-bench underspecified → parte es operación (lo arregla
  andamiaje); la parte juicio es ELEGIR qué preguntar (Mundo B).
- **6.4 Preguntas no-adaptativas**: BED-LLM `[VERIFICADO]` (45% naive vs 93% adaptando la
  pregunta a lo ya respondido).

## Estado
VIVO y el mejor medido en modelos; bloqueado por contrato. Sin cambios de decisión.
