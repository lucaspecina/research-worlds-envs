# Desviación declarada del pre-registro (ADR 0133) — registrada ANTES de correr los bloques 2-4 y ANTES de mirar ningún resultado

- **Fecha/hora**: 2026-07-11 ~03:05 UTC (bloques 0-1 completos, 24/60 celdas; ningún R mirado
  más allá del primero impreso en el log del bloque 0).
- **Qué se desvía**: el pre-registro fija "inicio de bloque separado ≥60 min". Los bloques 2, 3 y 4
  correrán consecutivos (separación ~5 min, lo que tarda cada bloque).
- **Quién y por qué**: decisión de Lucas (2026-07-11): el costo de reloj (~2.5 h) no paga la
  hipótesis que el espaciado sondea (deriva LENTA del proveedor, la más débil de las dos
  explicaciones de la varianza corrida-a-corrida). La protección principal de la comparación entre
  brazos —los tres brazos intercalados y aleatorizados DENTRO de cada bloque— no se toca.
- **Efecto honesto sobre la lectura**: los bloques siguen siendo réplicas completas (factor bloque
  se mantiene en el análisis), pero para los bloques 2-4 el factor pierde poder como sonda de
  deriva temporal lenta; los bloques 0-1 sí quedaron espaciados 60 min. Las lecturas prefirmadas
  (umbral scaffold ≥30 puntos, ≥4/5 bloques, etc.) NO cambian.
