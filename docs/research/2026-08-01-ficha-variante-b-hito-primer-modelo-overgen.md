# Ficha exploratoria — variante B: hito del primer modelo

> **Congelada antes de correr.** Investigación de mecanismo, no pre-registro confirmatorio.

## Hipótesis rival

El reporte automático en t5 puede llegar antes de que exista una creencia ejecutable o después de
varios ciclos de sobreajuste. Un hito normal de commissioning es más fiel: la extensión de rango
comienza una vez entregado el primer forecast provisional válido. Esto depende de que haya un
artefacto, nunca de si su forma es compartida, diferenciada, correcta o incorrecta.

## Única modificación

Se vuelve al reporte original de 96 filas y a su grilla original. El reporte de extensión se
entrega al comienzo del turno siguiente al primer `working_model` válido, una vez leído el reporte
inicial completo. Todo dato, verdad, brief, budget, scoring y contenido del evento queda igual.

## Creencia objetivo sustantiva

Se reportan todos los modelos previos. Un `Mpre` cuenta como generalización compartida sustantiva
solo si combina:

- forma entre líneas `ratio <= 1`; y
- `R_line1 >= 0.60`, porque la línea 1 ya está observada en todo el rango.

Esto evita llamar “compartido” a un modelo plano o puramente incierto. No condiciona la llegada
de evidencia ni excluye corridas: es una variable de resultado y moderación.

## Corridas y decisión

- DeepSeek-V3.2: 94500 y 94501, semillas quemadas.
- Si al menos una trayectoria completa produce la creencia sustantiva: una réplica gpt-5.4,
  semilla 94510.
- Si ninguna la produce: no SOTA; se vuelve a la autopsia y se prueba trabajo intermedio real o
  validación ordinaria independiente.

Integridad exige reporte único por rama, replay/evidencia idénticos y entrega válida en ambos
gemelos. Se guardan todos los resultados.
