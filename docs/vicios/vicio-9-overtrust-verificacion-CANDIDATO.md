# Vicio 9 (CANDIDATO — agregado 2026-07-12, decisión de Lucas pendiente) — Over-trust en la verificación propia

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
CANDIDATO. Si Lucas aprueba: entra al catálogo oficial (failure-modes + mundos-por-vicio), con
la cola de lectura [POR-LEER] resuelta antes de citar los números en el paper.
