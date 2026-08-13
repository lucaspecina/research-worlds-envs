# 0183 — Réplica externa de Perfiles persistentes con DeepSeek

**Fecha**: 2026-08-13 · **Estado**: vigente · **Aplica**: ADR 0182.

## Decisión

El siguiente nivel es cambiar de familia de modelo sin tocar el anfitrión. Se congela una réplica
con `DeepSeek-V3.2` en dos etapas:

1. capacidad con la misma idea nombrada, `n=3`, seeds `99840–99842`;
2. solo si al menos 2/3 cruza `S_profile>=0.5`, tanda sin ayuda `n=10`, seeds `99843–99852`.

Si la compuerta de capacidad falla, las diez partidas no corren. No se prueban otras frases ni se
retoca el mundo. La medida funcional sigue siendo primaria y el modelo compacto de dos tipos se
informa por separado.

## Motivo

La tanda `gpt-5.4 × n=10` confirmó una falla dentro de un único cruce modelo×mundo. Repetir con una
familia distinta es el cambio mínimo que distingue una regularidad del anfitrión de una regularidad
más amplia, manteniendo el contrato de Lucas: antes de interpretar negativos, el mismo modelo debe
demostrar con una pista que el salto es posible para él.

Protocolo completo: [ficha de Perfiles persistentes](../research/2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md).
