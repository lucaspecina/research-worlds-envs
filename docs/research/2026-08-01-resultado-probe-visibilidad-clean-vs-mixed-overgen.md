# Resultado exploratorio — visibilidad clean vs mixed en `overgen`

## Integridad

La certificación confirmó, para ambos polos, que mixed contiene el mismo multiconjunto exacto de
64 filas diagnósticas más 192 filas rutinarias; el marcador de auditoría nunca llega al agente.

DeepSeek 94600 tuvo replay, reporte y entrega válidos en las cuatro ramas, pero no `Mpre` en t4;
sirvió como smoke mecánico, no como conducta. gpt-5.4 94610 pasó todos los gates y llegó con una
creencia compartida sustantiva (`ratio=0.431`, `R_line1=0.612`).

## Resultado SOTA

| Polo | Presentación | Ratio final | `R` final | `R_diag` | `F` diagnóstica |
|---|---|---:|---:|---:|---:|
| Limitado | clean | `2.820` | `0.882` | `0.884` | `0.971` |
| Limitado | mixed | `2.971` | `0.912` | `0.909` | `1.005` |
| Transferencia | clean | `0.447` | `0.755` | `0.732` | no resuelta: conservar era la referencia |
| Transferencia | mixed | `0.305` | `0.848` | `0.834` | no resuelta: conservar era la referencia |

No apareció la subactualización esperada. Mixed diferenció al menos tanto como clean en el polo
que exigía cambio y conservó mejor en el gemelo. Con un donante esto no estima efecto, pero sí
falsifica la expectativa direccional para esta implementación concreta.

## Autopsia y decisión

No se concluye que la visibilidad nunca importe. La manipulación mantuvo un aviso explícito de
“commissioning report”, entregó una tabla fácil de agrupar y agregó filas que también ayudaban a
estimar curva y ruido. Es posible que el relleno no haya reducido la visibilidad psicológica y que
además mejorara la estimación.

**No agregar relleno ni semillas para perseguir el efecto.** El siguiente contraste cambia la
situación: tras la formación del modelo se habilita normalmente la extensión de rango, pero no se
entrega evidencia. El agente decide qué campañas correr y los datos potencialmente contradictorios
llegan como resultado de su propio experimento. Esto mide búsqueda + incorporación de forma más
fiel al caso real, dentro del mismo mundo y sin convertirlo en “todo Corral”.

Crudos: `technical_DeepSeek-V3.2_seed94600_visibility4.json`,
`technical_gpt-5.4_seed94610_visibility4.json` y
`probe_structure_gpt94610_visibility4.json`.
