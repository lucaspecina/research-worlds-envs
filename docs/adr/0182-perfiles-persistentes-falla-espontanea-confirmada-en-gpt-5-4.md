# 0182 — Perfiles persistentes: falla espontánea confirmada en gpt-5.4

**Fecha**: 2026-08-13 · **Estado**: vigente · **Aplica**: ADR 0181.

## Decisión

Se mantiene el experimento **Grupos escondidos — Perfiles persistentes** como anfitrión válido y
se cierra su ajuste local para `gpt-5.4`. La tanda congelada queda sellada en **1/10 cruces
funcionales** y **0/10 modelos compactos de dos tipos**. No se prueban más pistas, frases ni
retoques del mundo antes de volver un nivel arriba.

El próximo paso permitido es una réplica externa: otra familia de modelo sobre el anfitrión
congelado o un segundo anfitrión del mismo salto. Cualquier claim conserva el alcance
`gpt-5.4 × Perfiles persistentes × n=10` hasta esa réplica.

## Evidencia

- Las diez partidas terminaron con entregas ejecutables y sin reintentos.
- La medida primaria congelada `S_profile>=0.5` dio un solo cruce: `0/0/0/.942/0/0/0/0/0/0`.
- Ese cruce fue un remuestreador empírico de perfiles completos: preserva funcionalmente las dos
  familias, aunque no las comprime en una explicación de dos tipos.
- Las otras nueve entregas fueron una sola Gaussiana conjunta.
- En las 400 filas exactas vistas en cada partida, un ajuste legal de dos perfiles ganó por
  `Delta BIC=705–795` y alcanzó `S_profile=.943–.999`. Falta de señal queda descartada.
- Con la idea nombrada, el mismo modelo había realizado correctamente el salto en 2/3 partidas.

## Interpretación acotada

La evidencia separa capacidad de activación espontánea: el modelo puede investigar e implementar
la idea cuando entra en su menú, pero rara vez produce por sí solo una entrega con la bifurcación.
La autopsia localiza el cuello dominante entre notar la dependencia y representar/probar tipos
discretos. No demuestra una propiedad de todos los LLM ni distingue todavía modelo de anfitrión.

Detalle, reglas y crudos: [ficha de Perfiles persistentes](../research/2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md).
