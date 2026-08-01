# Resultado exploratorio — hito de modelo y grilla apareada SOTA

## Variante B: primer artefacto válido

DeepSeek 94500 y 94501 pasaron replay, reporte y entregas en ambos gemelos, pero sus `Mpre` de t2
eran placeholders compartidos: `ratio=0.035`, pero `R_line1=0` en ambos. El trigger resolvió
“no hay código”, no “hay una creencia formada”. Después del reporte, ambos resolvieron el polo
limitado (`R=0.861/0.870`); en transferencia uno terminó bien (`0.881`) y otro mal (`0.107`). Esto
es heterogeneidad interesante de formación, pero no revisión atribuible desde un prior competente.

La auditoría de siete prefijos confirmó que DeepSeek madura un modelo compartido sustantivo en
momentos heterogéneos (t5 o t7 en los casos que lo hicieron), mientras gpt-5.4 construye antes un
modelo competente pero a veces fragmentado. Por eso “primer string” y “turno fijo” son proxies
distintos e imperfectos; ninguno define por sí solo creencia formada.

## Variante A2: prueba directa en gpt-5.4

Se corrigió de forma visible el gate entre modelos: DeepSeek validó mecánica, pero no podía decidir
una hipótesis sobre el sobreajuste específico visto en gpt. La única réplica SOTA 94420 con grilla
apareada pasó toda la integridad.

| Estado | Limitado | Transferencia |
|---|---:|---:|
| `Mpre` ratio | `0.035` | mismo prefijo |
| `Mpre R_line1` | `0.886` | mismo prefijo |
| `Mpre R` global | `0.234` | `0.901` contra esa verdad |
| ratio final | `1.668` | `0.536` |
| `R` final | `0.767` | `0.780` |

En limitado, el agente reconoció que líneas 2–3 exigían desviaciones y capturó `F=0.779` de la
mejora diagnóstica de referencia. En transferencia conservó la familia compartida, pero su refit
flexible bajó el score desde `0.901` a `0.780`: dirección estructural correcta con sobreajuste
innecesario. Esta separación es justamente lo que una métrica única habría ocultado.

## Cambio de creencia del equipo

- La grilla apareada es **prometedora**, no demostrada causalmente por una semilla.
- `overgen` ya tiene una línea base SOTA natural, bilateral y ejecutable; no hace falta fabricar
  una falla para justificarlo.
- El siguiente probe debe intentar reproducir el vicio sin cambiar el blanco: mismo historial y
  mismas filas diagnósticas, presentadas limpias o mezcladas con relleno rutinario. Si ambas se
  incorporan igual, la hipótesis de visibilidad pierde fuerza en esta estructura.

Crudos: `technical_DeepSeek-V3.2_seed94500_formed.json`,
`technical_DeepSeek-V3.2_seed94501_formed.json`,
`technical_gpt-5.4_seed94420_paired_low.json`,
`probe_structure_DeepSeek94500_94501_formed.json`,
`probe_structure_gpt94420_paired_low.json` y `prefix_belief_maturity_audit_v1.json`.
