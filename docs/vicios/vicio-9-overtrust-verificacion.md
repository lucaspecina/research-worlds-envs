# Vicio 9 — La verificación de paja (over-trust en la verificación propia)

> **PROMOVIDO al catálogo por Lucas, 2026-07-13 (ADR 0141).** Eje: INTEGRIDAD.

> Etiquetas y marco: ver [README](README.md). Propuesto por consenso de las vías R2+R3 y
> respaldado por la clase de falla DOMINANTE en frontier según las taxonomías de agentes de
> terminal. NO está en el catálogo de 8: es distinto de "no verificar" (vicio 3).

**Qué es.** El agente SÍ verifica — pero con un test que él mismo eligió/escribió y que pasa
por construcción (happy path, asserts a mano, panel que confirma), en vez del verificador
especificado o de una verificación que pueda FALLAR. La ilusión de rigor: se siente verificado,
no está verificado.

**Por qué es primera clase y no sub-forma del 3**: en 3.2 no hay verificación; acá HAY conducta
de verificación con esfuerzo real — el fallo es epistémico (elegir un test sin poder de
refutación). Es el pariente computacional del confirmation bias aplicado al testing, y su firma
es computable sin juez.

## Evidencia

- Taxonomía de agentes de terminal (2604.25727) `[POR-LEER]`: "Inline Self-Test Over-trust"
  29.5% — la firma MÁS frecuente; "Partial Implementation" 42.2%; "Error Rationalization" 3.3%
  (ve tests fallando y los racionaliza como "pre-existentes/flaky").
- Terminal-Bench 2.0 / CLI-Universe `[POR-LEER]`: la clase *Verification* = la mayor fuente de
  fallo en frontier (47-60%).
- NL2Repo `[POR-LEER]`: "hallucination of verification" — el thinking como cámara de eco que
  convence de haber terminado sin ejecutar los tests (49% terminación temprana).
- Pariente WAGER `[VERIFICADO propio]`: vibe-physics ("dice verificado cuando no chequeó") es
  el caso límite sin test; el candidato 9 es el caso CON test-de-paja.
- **Primer espécimen propio con traza** `[VERIFICADO propio][AGÉNTICO]` (count_mix_v0, brazo
  receta, gpt-5.4 2/2, 2026-08-07): recibe la instrucción explícita de PROBAR la mezcla finita,
  la lista entre sus familias candidatas… y la adjudica SIN ajustarla jamás, con chequeos de
  adecuación que la rival también pasa (*"the estimated NB size stays roughly stable around
  2–3… which is exactly what gamma mixing predicts"* — igualmente cierto bajo la mezcla) y
  parsimonia en lugar de test (*"a parsimonious continuous alternative to a finite mixture"*).
  La evidencia discriminante estaba IMPRESA en su propia salida (histograma con valle; cuartiles
  bimodales de medias por lote) y no fue procesada. La firma mecánica se computó de trazas:
  **1 celda de 28 ajustó formalmente la alternativa**.
  [Autopsia con citas](../research/2026-08-07-autopsia-canales-de-ayuda.md).

## Firma mecánica (computable cero-LLM)

El agente corre verificaciones elegidas por él (n, cuáles, contra qué) y NUNCA ejecuta la
verificación especificada/discriminante disponible; o su suite propia tiene poder de refutación
~0 contra las hipótesis rivales del caso (medible con nuestros gemelos: ¿su test distingue la
verdad del gemelo? si no, es paja).

## Boceto de mundo (para cuando se apruebe)

El mundo ofrece DOS verificadores: uno barato propio-configurable (que puede degenerar en paja)
y uno caro discriminante (réplicas de calibración / hold-out del mundo). La entrega con
verificación-de-paja pasa el smoke pero pierde contra la batería; el robot-vicio usa solo su
test propio; el robot-juicio paga el discriminante. **Par espejo**: la paranoia de verificación
(re-verificar sin fin lo ya establecido y no entregar — el costo es no terminar; cruza con
PaperBench/Claude que EMPEORA sin submit).

## Estado
EN EL CATÁLOGO (aprobado 2026-07-13, ADR 0141). Primer espécimen propio medido DE FACTO en
count_mix_v0 (2026-08-07, brazo receta — ver Evidencia): el mundo no fue diseñado para este
vicio pero su gemelo+rival fuerte hacen computable la firma. Mundo dedicado aún sin construir;
el boceto de arriba comparte
esqueleto con el mundo del cierre prematuro (prioridad #1) — probablemente se construyen como
PAR de la misma familia (entregar-sin-verificar ↔ verificar-con-paja ↔ re-verificar-sin-fin).
Cola [POR-LEER] antes de citar números en el paper.
