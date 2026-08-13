# 0185 — DeepSeek falla capacidad y cierra la réplica

**Fecha**: 2026-08-13 · **Estado**: vigente · **Aplica**: ADRs 0183–0184.

## Resultado

Dos partidas de la compuerta con idea nombrada terminaron válidas y ambas dieron `S_profile=0`.
La tercera no comenzó: su llamada fue rechazada por permisos antes de la API y la seed quedó sin
quemar. Como la regla exigía al menos 2/3, dos fallos hacen imposible pasar aun con un tercer éxito.

En las filas exactas vistas por cada agente, el ajuste legal de dos perfiles alcanzaba
`S_profile=.982/.964` y ganaba por `Delta BIC=361.6/368.0`. DeepSeek consideró la pista, pero
entregó factores continuos dentro de una sola Gaussiana en ambas partidas.

## Decisión

**ABANDONAR** la réplica DeepSeek en este anfitrión y no ejecutar su tanda sin ayuda. Tampoco se
prueba otra frase: eso convertiría la réplica en búsqueda de una formulación favorable.

Se **MANTIENE** el resultado acotado `gpt-5.4 × Perfiles persistentes × n=10`, sin promoverlo a
claim multi-modelo. El siguiente nivel será otro anfitrión del mismo salto, con evidencia
secuencial e investigación real en lugar de otra prueba local sobre esta tabla.

Detalle y crudos: [ficha de Perfiles persistentes](../research/2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md).
