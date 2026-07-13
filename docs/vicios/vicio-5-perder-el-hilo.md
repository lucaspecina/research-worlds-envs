# Vicio 5 — Perder el hilo en tareas largas (operación — NO se construye en contra)

> Etiquetas y marco: ver [README](README.md). Decisión vigente: se MIDE si aparece, no se
> diseña en contra (lo arreglan memoria/andamiaje; medio campo trabaja en eso).

## Sub-formas (para atribución en trazas, no para mundos)

- **5.1 Restricción visible ignorada**: HORIZON `[VERIFICADO]` (*"la restricción sigue EN el
  contexto y la viola igual — desatención, no olvido"*; el filtro "Condition: New" violado 200
  pasos después). Degradación NO lineal con el largo.
- **5.2 Acumulación de errores / loops**: HORIZON `[VERIFICADO]`; SciAgentGym `[VERIFICADO]`
  (loop-escape 35.7%); TIDE Loop Rate / ProcCtrlBench Duplicate-Step `[POR-LEER]` — **firmas
  mecánicas robables para nuestro clasificador de trazas**.
- **5.3 Deriva por inacción** (matiz nuevo, R2/R3): goal-drift `[POR-LEER][AGÉNTICO]` — la
  deriva se manifiesta MÁS por lo que el agente DEJA de hacer que por acción desalineada; y es
  específica por modelo (Claude >100k tokens, 4o-mini siempre). **Nota de borde**: "deriva por
  inacción bajo objetivo instrumental prolongado" tiene componente de juicio — queda anotada,
  no cerrada (matiz de R2 aceptado).
- **5.4 Terminación prematura por scaffold**: Terminal-Bench 12.9% `[POR-LEER]`; PaperBench
  `[VERIFICADO parcial]` — firma de la familia o-series, NO ley (Claude empeora sin submit).

## Corpus minable
MAST `[POR-LEER]`: 1.600+ trazas multi-agente anotadas (HF mcemri/MAD, κ=0.88, 14 modos) —
~41.8% especificación, ~36.9% desalineación inter-agente, ~21.3% verificación. Confirma que la
mayoría es sistema/operación. Útil para calibrar nuestros clasificadores de firma.
