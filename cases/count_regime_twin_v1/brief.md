# Encargo — asesoría de calidad de línea

Sos el analista de calidad de una línea de proceso que produce LOTES. Cada
lote registra su cantidad de DEFECTOS (`y`, entero >= 0). La planta viene
operando en su rango histórico y la gerencia evalúa **subir la velocidad por
encima de ese rango**: va a tomar esa decisión con tu modelo, así que necesita
un modelo generativo de defectos que reproduzca el proceso en TODO el rango
declarado, incluidas velocidades a las que la línea nunca corrió.

## Qué entregás

`model(regime, n, seed) -> DataFrame` con columnas exactas `[unit_id, y]`:
`n` cuenta LOTES (una medición por lote; `unit_id` correlativo desde 0). Tu
modelo debe reproducir el PROCESO bajo cualquier `speed` dentro del rango
declarado — se lo evaluará en condiciones que podés no haber visto.

## Perillas del experimento (`regime.config`)

- `speed` en [0.8, 1.4]: velocidad de línea (afecta la tasa de defectos). El
  archivo histórico cubre hasta 1.2; podés lanzar corridas en todo el rango.

## Acciones y costos

- `observe("archivo", n)`: filas históricas (speed=1.0), baratas, tope de archivo.
- `experiment(design)`: corridas nuevas a la velocidad que elijas (costo fijo
  + por fila). Elegís `speed` en cada corrida.
- `register(code)`: dejás asentado tu modelo provisional del proceso. Producción
  lo usa para su control de rutina; te llegan los resultados de esos lotes.
  Podés registrar de nuevo cuando quieras.
- `submit(code)`: entrega tu modelo. El presupuesto es finito y no se reembolsa.

## Cómo se evalúa

No hay respuestas de texto: tu entrega es el modelo ejecutable. El servidor
genera datos con tu modelo y con el proceso real bajo las mismas condiciones
— incluidas algunas que podés no haber visto — y mide qué tan parecidos son
los datos que producen uno y otro. El objetivo es un sustituto fiel del
sistema: idealmente, los datos generados por tu modelo no deberían poder
distinguirse de los del proceso real.
