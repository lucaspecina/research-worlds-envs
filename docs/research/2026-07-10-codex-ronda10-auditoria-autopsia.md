# Codex ronda 10 — auditoría de la autopsia Fase 1 — 2026-07-10

> Auditó la clasificación ciega de ADR 0129. Sostiene lo central (sin sobre-incorporación sistemática inducida por la pista; fallas heterogéneas en ambos brazos; n=8 por corrida inútil) pero CORRIGE el grano: "T4 gana" es demasiado específico (no hay UN atractor — es mezcla de diseño experimental no-discriminante, inferencia causal, descomposición de ruido y traducción a código); "15/16 descubrieron" y "el fallo vive en la entrega" inflados ("muchos experimentos no equivalen a experimentos discriminantes"). Cambios a v2: firmas ESTRECHAS predefinidas (no "buena entrega"); el FORK de evidencia fija pasa a ser el experimento central; réplicas por batches temporales (≥5); controlar complejidad de entrega entre mundos; decidir el nombre honesto del principio (integración vs terminación). first_story_scarce DEGRADADO como confirmatorio de ese vicio en DeepSeek (el headroom viene de otros fallos → rompe score↔vicio); queda como fixture del fork / stress-test de traducción / control activo / perfil de otros modelos. Crudo:

codex
### (a) Auditoría: conclusión general sí, etiquetas no del todo

Sostengo esto:

> No hay evidencia de sobre-incorporación inducida sistemáticamente por la pista. Hay fallas heterogéneas de traducción desde investigación a modelo, presentes en ambos brazos.

Pero **“T4 gana sobre T2” es demasiado específico**. No veo un único atractor T4:

- **Libre/s58:** T2+T6, quizá T4 secundario. Descubrió buenos coeficientes, pero inventó `grade=10−10t`, fabricó ambient→humidity por rango y duplicó efectos. Es una maqueta nueva y arbitraria, no un default típico.
- **Libre/s56:** T1+T2+T6. `ambient=(h+t+speed)/3`, coeficiente de grade declarado “arbitrary” y mediador feedstock→outcome sin identificar. Además, investigó insuficientemente los knobs.
- **Hint/s59:** principalmente **T5+T6**, no T2. Estimó temp/speed explícitamente; los términos chicos pueden ser ruido muestral legítimo. El problema serio es sumar process noise inflado y measurement noise: confusión proceso–medición.
- **Hint/s61:** T1 limpio: transporta asociación feedstock–outcome a una flecha causal.
- **Hint/s56:** no es solo entrega. Varió humidity/temp/speed siempre juntos; el diseño no podía separarlos y luego repartió el efecto por tercios. Es **fallo de diseño experimental/identificabilidad upstream** —T8+T6, con arbitrariedad T2—.

Por eso tampoco acepto literalmente “15/16 descubrieron la estructura” ni “el fallo vive en la entrega”. La mayoría reconoció que el hall/humidity explica la historia, pero algunos nunca identificaron cuál knob era causal. **Muchos experimentos no equivalen a experimentos discriminantes.**

Además, las trazas tienen bastantes errores operacionales —librerías ausentes, columnas, serialización, presupuesto—. No impidieron entregar, pero pudieron degradar la síntesis final. El cuello observado es una mezcla de:

1. diseño experimental;
2. inferencia causal;
3. descomposición de ruido;
4. traducción a código.

La autopsia actual tampoco explica retroactivamente los cinco ceros de 0121: esas trazas no existen. Solo vuelve menos plausible que todos hayan sido T2 inducido por la pista.

Las tres corridas sí demuestran que **n=8 en una única corrida es inútil**. No demuestran aún qué componente varía: sampling del modelo, deriva del proveedor/backend o efecto temporal de bloque.

### (b) Cambios a v2

El factorial 2 mundos × 3 principios sigue correcto. Cambiaría cuatro cosas antes de Fase 3:

1. **No ampliar el endpoint a “buena entrega”.** Es demasiado cercano al score y mezcla cuatro vicios. Predefinir firmas estrechas: flecha causal no identificada, varianza no medida/doble-contada, experimento no discriminante y discrepancia análisis→código.

2. **Hacer primero el fork de evidencia fija.** Mismo transcript y paquete de datos, variando solo pista al construir el modelo. Es ahora el experimento discriminante central: aísla entrega de adquisición.

3. **Replicar por batches.** Dividir cada celda entre al menos 5 bloques intercalados temporalmente; batch/día entra como factor y unidad de clustering. Meter 40 episodios en una sola corrida no arregla esta inestabilidad.

4. **Controlar complejidad de entrega entre mundos.** Si el otro mundo requiere código mucho más simple, una pista genérica de finalización puede parecer “específica” solo porque first_story tiene más oportunidades de equivocarse implementando.

El principio de 0125 ya está más cerca de **integración análisis→submission** que de terminación. Deben elegir:

- o lo renombran honestamente y aceptan que puede ser operación/checklist;
- o mantienen “terminación prematura” como constructo y buscan otro mundo/modelo donde esa conducta exista basalmente.

No cambien variantes por el +0.64 actual. El banco está congelado y esta corrida no selecciona texto.

### (c) Rol de `first_story_scarce`

Sí: **queda degradado como mundo confirmatorio de terminación/descubrimiento para DeepSeek**. Hay score headroom, pero el headroom proviene mayormente de otros fallos. Eso rompe la correspondencia score↔vicio objetivo.

No diría “discovery resuelto” ni “la varianza es calibración”: algunos episodios fallaron en identificación causal y otros en modelización observacional. La lectura correcta es:

> El cuello dominante se desplazó downstream y se volvió heterogéneo.

Mantendría el mundo como:

- fixture de desarrollo del fork;
- stress test de traducción evidencia→modelo;
- control activo en el factorial;
- perfil para otros modelos que sí muestren terminación o evidencia-comprada-no-usada.

Pero no como diagonal confirmatoria de ese vicio en DeepSeek salvo que un baseline nuevo demuestre, en varios batches, que la conducta objetivo está realmente viva.
