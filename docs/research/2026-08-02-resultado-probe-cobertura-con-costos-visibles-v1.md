# Resultado — cobertura de investigación con costos visibles v1

**Estado:** descubrimiento cerrado; no se reproduce falta de cobertura en este host.

## Corrección previa

La v0 no era interpretable: `env.describe()` prometía costos exactos pero omitía
`cost_per_horizon=50`, que el servidor sí cobraba. DeepSeek señaló la omisión y
gpt-5.4 lanzó una cartera que el presupuesto cortó. Se preservaron los crudos, se
añadió el costo a la hoja pública y se verificó con un test. No era verdad oculta:
era una regla pública de la decisión.

## Corridas frescas

| Modelo / seed | Cobertura comprada | Entrega | Lectura |
|---|---|---:|---|
| DeepSeek-V3.2 `99102` | feeds `0–10`; `t_max=24`; gate conjunto pasa | no, agotó 10 turnos | censurado por cierre/capacidad; no hay señal de mala adquisición |
| gpt-5.4 `99103` | feeds `0–10`; dos campañas a `t=24` y una a `t=6`; gate conjunto pasa | sí, `R=0`, `R_unclipped=-.370` | compró cobertura; falló después en planificación/modelización |

DeepSeek gastó `3555/4000` en tres pilotos tempranos, una campaña larga en feed 5
y una hasta t=12 en feed 10. Encontró saturación, pero siguió comparando familias
sin entregar.

gpt-5.4 calculó una cartera de tres campañas largas de costo `1440` cada una cuando
solo quedaban `3730`. Las dos primeras (feeds 0 y 5) se ejecutaron; la tercera
falló por presupuesto. Luego compró feed 10 solo hasta t=6 y entregó una logística
con capacidad asintótica dependiente del feed. El error de probabilidad en t=16
fue bajo en los tres feeds intervenidos (`.008/.102/.009`) pero alto en el régimen
observacional (`.639`); el score distribucional global quedó en cero. Esto no es
“no salió a mirar”: es una mezcla de planificación no transaccional, inferencia de
invariantes y mala propagación al modelo final.

## Decisión un nivel arriba

**ABANDONAR falta-de-cobertura en `logistic_yield_v0`.** Con costos visibles, los
dos agentes cubrieron tanto el horizonte relevante como la superficie de feeds.
No se baja el presupuesto ni se oculta la consecuencia para fabricar un fallo.

El episodio sí deja una candidata distinta: un frontier puede diseñar una cartera
que excede un presupuesto explícito, perder la observación decisiva y cerrar con
una extrapolación estructural pobre. Queda en el banco como **planificación
experimental adaptativa / descubrimiento de invariantes**, no se promociona con
`n=1` ni se llama revisión de creencias.

La siguiente prueba cambia de pregunta: antes de construir un host grande de
fricción real, se buscará headroom barato para la diferencia entre una corrección
local y reabrir una estructura propia compartida. En paralelo permanece la firma
ya replicada de aplanamiento de estructura latente; ninguna de las dos queda
protegida como explicación final.
