# Encargo — analista de proceso, planta de síntesis

La planta produce LOTES de un compuesto; lo que importa es la PUREZA (`y`, % en
escala 0-100). La pureza de cada lote se mide con el espectrómetro de línea. La
gerencia necesita un modelo generativo del PROCESO: dado un régimen de operación,
tu modelo debe generar la pureza real de los lotes que el proceso produciría.

## Qué entregás

`model(regime, n, seed) -> DataFrame` con columnas exactas `[unit_id, y]`:
`n` cuenta LOTES (una pureza por lote; `unit_id` correlativo desde 0). Honrá
`regime.config["T"]` (temperatura del reactor, en [0.6, 1.4]). Se evaluará en
condiciones que podés no haber visto.

## Acciones y costos (presupuesto finito, sin reembolso)

- `observe("archivo", n)`: lecturas históricas del espectrómetro (operación
  normal, T=1.0), baratas.
- `experiment(T=..., n_lotes=..., reps=...)`: produce lotes NUEVOS a la
  temperatura que elijas y los mide (costo fijo + por medición).
- `measure(material, reps)`: mide con el espectrómetro cualquier material que
  indiques: un lote ya existente (por `lot_id`, mismo vial), un lote
  re-preparado en vial nuevo (`revial:<lot_id>`), o un insumo del catálogo —
  incluye solventes, blancos y un estándar de referencia certificado (pureza
  nominal en la etiqueta del catálogo).
- `lab_extern([lot_ids])`: re-análisis del MISMO material por un laboratorio
  externo certificado (hasta 6 lotes por pedido; el resultado llega al turno
  siguiente). Caro.
- `register(code)`: dejás asentado tu modelo provisional; el monitoreo de
  rutina de la planta corre en calendario fijo y te reporta contra tu último
  modelo registrado.
- `submit(code)`: entrega final.

## Cómo se evalúa

Tu entrega es el modelo ejecutable. El servidor genera lotes con tu modelo y
con el proceso real bajo las mismas condiciones — incluidas algunas que podés
no haber visto — y mide qué tan parecidos son. El objetivo es un sustituto
fiel del PROCESO.
