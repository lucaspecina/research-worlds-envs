# Encargo — asesoría de calidad de línea

Sos el analista de calidad de una línea de proceso que produce LOTES. Cada
medición de un lote registra su cantidad de DEFECTOS (`y`, entero >= 0). La
gerencia necesita un modelo generativo de defectos para planificar inspección
y descartes bajo distintas velocidades de línea.

## Qué entregás

`model(regime, n, seed) -> DataFrame` con columnas exactas `[unit_id, y]`:
`n` cuenta MEDICIONES (filas). Con `regime.config["repeats_per_unit"] = R`, las
filas se agrupan de a R por lote (comparten `unit_id`; el último lote puede
quedar con menos mediciones). Tu modelo debe reproducir el PROCESO
bajo cualquier `speed` dentro del rango declarado — se lo evaluará en
condiciones que podés no haber visto.

## Perillas del régimen (`regime.config`)

- `speed` en [0.8, 1.2]: velocidad de línea (afecta la tasa de defectos).
- `repeats_per_unit` en [1, 4]: mediciones por lote.

## Acciones y costos

- `observe("archivo", n)`: filas históricas (speed=1.0), baratas, tope de archivo.
- `experiment(design)`: corridas nuevas con las perillas que elijas (costo fijo
  + por fila/medición). Podés fijar `repeats_per_unit` para repartir esas
  mediciones en menos lotes, midiendo varias veces cada uno.
- `submit(code)`: entrega tu modelo. El presupuesto es finito y no se reembolsa.

La nota compara el comportamiento de tu modelo contra el proceso real en
condiciones elegidas por el servidor. No hay respuestas de texto: solo el
modelo ejecutable.
