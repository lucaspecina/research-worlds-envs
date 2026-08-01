# Ficha exploratoria — variante A2: prueba directa SOTA de la grilla apareada

> **Congelada antes de correr.** Enmienda metodológica explícita, no rescate retroactivo.

## Por qué se abre A2

La regla de A exigía que DeepSeek mostrara la condición antes de gastar en SOTA. Las corridas
revelaron que DeepSeek suele tardar 5–7 turnos en construir un modelo sustantivo, mientras que los
gpt previos lo construyeron en 1–3 pero sobreajustaron interacciones. Por tanto, el gate barato
validó mecánica pero no responde la hipótesis específica que originó la grilla. Transportar esa
conducta entre modelos sería otro error de inferencia.

## Prueba única

- gpt-5.4, semilla nueva 94420.
- Mismo `paired_low`, reporte automático t5 y criterios mecánicos anteriores.
- La pregunta primaria es el `Mpre`: `ratio <= 1` y `R_line1 >= 0.60`.
- Si es compartido sustantivo, la grilla queda prometedora; si es fragmentado, la explicación de
  comparabilidad inicial queda debilitada; si falta modelo, el resultado es timing, no estructura.
- Las ramas solo se interpretan si replay, reporte y entregas son íntegros.

No se agregan semillas según el resultado.
