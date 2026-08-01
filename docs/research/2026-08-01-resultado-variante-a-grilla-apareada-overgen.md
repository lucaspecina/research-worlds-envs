# Resultado exploratorio — variante A: grilla inicial apareada

## Veredicto corto

**La variante no pasa a SOTA.** Hizo comparables las líneas, pero no produjo dos trayectorias
interpretables de revisión y reveló un falso positivo de la métrica de forma compartida.

## Corridas

- 94400: fallo técnico antes de llamar al agente; semilla quemada y arreglo auditado en la ficha.
- 94401: DeepSeek no materializó `working_model` antes del reporte de t5. Las ramas terminaron,
  pero sin `Mpre` no miden revisión.
- 94402: sí creó `Mpre`, con `ratio=0.035`, pero era esencialmente un pronóstico plano y ancho
  (`predictive_sd=2.40`) que obtuvo `R_line1=0`. Las ramas no entregaron antes del límite porque
  el agente siguió corrigiendo análisis y código.

## Qué aprendimos

1. Ofrecer comparaciones directas no garantiza que el agente las use: 94401 siguió comparando la
   pendiente global de la línea 1 con pendientes de rango bajo de las demás.
2. `ratio <= 1` solo no alcanza: también clasifica como “compartido” a un modelo no resuelto.
   Una creencia objetivo sustantiva debe compartir forma **y** explicar la curva de la línea 1,
   que está observada en todo el rango.
3. Un turno fijo mezcla revisión con velocidad de construcción del primer modelo. El siguiente
   contraste debe programar el hito por existencia de un artefacto válido, nunca por su contenido.

No se interpreta este resultado como ausencia del vicio. Se rechaza esta modificación aislada y
se formula una explicación rival.

Crudos: `technical_DeepSeek-V3.2_seed94401_paired_low.json`,
`technical_DeepSeek-V3.2_seed94402_paired_low.json` y
`probe_structure_DeepSeek94402_paired_low.json`.
