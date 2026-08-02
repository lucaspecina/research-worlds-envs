# Resultado exploratorio — historial de investigación y revisión posterior

**Fecha:** 2026-08-01
**Estado:** resultado de localización; no es estimación de prevalencia ni estudio principal.
**Diseño previo:**
[`2026-08-01-ficha-stress-historial-real-y-evidencia-enterrada-v0.md`](2026-08-01-ficha-stress-historial-real-y-evidencia-enterrada-v0.md).

## Veredicto corto

Sí logramos reproducir repetidamente una forma concreta del vicio, pero todavía en un único
donante DeepSeek seleccionado:

> Con el historial analítico completo presente, el agente ve la anomalía, pero la explica
> reajustando la estructura que ya venía usando; con exactamente el mismo workspace, modelo
> previo y reporte en una conversación compactada sin ese historial, separa correctamente las
> formas de las líneas.

En el donante 94101, `REVISE + clean64` falló en las dos continuaciones nativas (`F=0.04, 0.00`)
y funcionó en las dos continuaciones frescas sin sugerencia (`F=1.06, 0.91`, contando en la
primera el último modelo válido aunque no alcanzó a entregar). El gemelo `RETAIN` conservó la
estructura correcta en todos esos brazos.

Esto es un **control positivo local repetido**, no todavía una regularidad robusta: gpt-5.4
revisó correctamente incluso con evidencia enterrada y un historial sintético mucho más largo.

## Qué se mantuvo fijo

- mismo mundo gemelo, semilla, evidencia y `M_pre`;
- mismo workspace real rehidratado por replay;
- reporte rutinario ya anunciado por el brief, sin decir “esto refuta tu modelo”;
- score mecánico contra verdad oculta, sin juez LLM;
- polo bilateral: en `REVISE` hay que separar; en `RETAIN` hay que conservar.

El `M_pre` de 94101 era sustantivo: `R=0.226` en la región `REVISE` y `0.826` en `RETAIN`, con
forma compartida explícita. El actualizador de referencia se construyó solo desde `M_pre` y el
ledger visible. `F` es fracción de su mejora capturada; es una **referencia predefinida**, no un
posterior matemático único.

### Corrección de auditoría

Los `85.040` tokens guardados en el donante son uso API acumulado entre 12 llamadas, no longitud
única del historial. El transcript reconstruido tiene 45.886 caracteres, aproximadamente
11–13k tokens. Por lo tanto, estos datos no prueban “saturación de una ventana gigante”. Sí
permiten estudiar la influencia de un historial científicamente relevante de longitud moderada.

## Resultados principales

### 1. Trayectoria nativa realmente vivida

| Verdad y reporte | Repetición | `R_pre → R_final` | `F` | Estructura final |
|---|---:|---:|---:|---|
| REVISE limpio | 0 | 0.226 → 0.164 | 0.038 | compartida, incorrecta |
| REVISE limpio | 1 | 0.226 → 0.226 | 0.000 | compartida, incorrecta |
| RETAIN limpio | 0 | 0.826 → 0.876 | — | compartida, correcta |
| RETAIN limpio | 1 | 0.826 → 0.876 | — | compartida, correcta |
| REVISE conflicto 256 | 0 | 0.226 → 0.226 | 0.000 | compartida |
| REVISE enterrada 256 | 0 | 0.226 → 0.138 | -0.193 | compartida |

La suciedad no fue necesaria para elicitar la falla en este donante: ya aparece 2/2 con el
reporte limpio. Los brazos sucios muestran que puede persistir, pero tienen una sola continuación
y no deben leerse como una curva de dosis.

### 2. Mismo estado, conversación fresca sin sugerencia

| Verdad | Repetición | Fuente puntuada | `R_pre → R` | `F` | Estructura |
|---|---:|---|---:|---:|---|
| REVISE | 0 | último modelo válido; no submit | 0.226 → 0.886 | 1.061 | separada |
| REVISE | 1 | entrega | 0.226 → 0.803 | 0.913 | separada |
| RETAIN | 0 | entrega | 0.826 → 0.858 | — | compartida |
| RETAIN | 1 | entrega | 0.826 → 0.856 | — | compartida |

La primera versión fresca incluía una frase balanceada que podía funcionar como SOP de revisión;
se descartó para inferencia. La tabla usa únicamente el rerun corregido, sin esa frase.

### 3. ¿Autoría, longitud o contenido?

Con el transcript completo convertido en archivo de **otro analista**, `REVISE` siguió fallando
2/2 (`F=0.152, 0.127`) mientras `RETAIN` mantuvo la forma. Por lo tanto, este resultado no se
explica principalmente por “ego” o por la etiqueta de autoría.

Un archivo administrativo de igual longitud fue inestable: una continuación revisó
(`F=1.066`) y otra empeoró (`F=-0.937`). La longitud/carga puede degradar la ejecución, pero no
explica por sí sola el patrón estable del historial relevante.

Se hizo después un igualado más estricto: 24 posiciones y 45.554 caracteres en todos los
perfiles; cada mensaje removido fue reemplazado en el mismo lugar.

| Perfil histórico atribuido a otro | `F` en REVISE, dos continuaciones | Resultado bilateral |
|---|---|---|
| neutral | 0.000; 0.461 | forma compartida 2/2; RETAIN correcto 2/2 |
| exploración temprana, turnos 1–6 | -0.619; -0.078 | una separación mal ejecutada y una persistencia; RETAIN correcto |
| compromiso final, turnos 9–12 | 0.887; 0.830 | revisión correcta 2/2; RETAIN correcto 2/2 |
| historial completo, turnos 1–12 | 0.147; -0.299 | forma compartida incorrecta 2/2; RETAIN correcto 2/2 |

El patrón refuta una historia demasiado simple de “más compromiso explícito = menos revisión”:
los últimos turnos solos ayudaron. La candidata más precisa es que **el camino analítico completo
funciona como andamiaje para interpretar el dato nuevo dentro de la clase de modelo anterior**.
También hay context rot operativo: el perfil temprano intentó una estructura distinta pero la
implementó mal. Los perfiles tuvieron igual longitud en caracteres, no en tokens del proveedor
(primer prompt: aproximadamente 11.4k–14.9k), así que esta descomposición sigue siendo
exploratoria.

Además, “nativo” y “fresco” no difieren en una sola variable psicológica: el fresco reempaqueta
el estado en un mensaje nuevo y puede perder los nombres/roles de objetos del workspace aunque
los objetos sigan allí. Por eso una no-entrega fresca se trata como censura operativa salvo que
el último modelo válido demuestre una decisión científica clara. Un futuro contraste limpio
necesita un manifiesto neutral de variables idéntico entre brazos o un horizonte suficiente para
recuperar orientación.

## Autopsia de la falla

No fue ceguera total. En la continuación nativa limpia, el agente calculó errores mucho mayores
en líneas 2–3 que en 1 y 4. Sin embargo, los trató como offsets, ruido o heterocedasticidad y volvió
a ajustar una cuadrática común. En las ramas frescas, ante los mismos datos, comparó
interacciones/curvaturas por línea y abandonó la forma compartida.

La localización provisional es:

`notar` **sí** → `interpretar la implicancia estructural` **falla** → `modelo ejecutable` queda
subactualizado.

No alcanza con contar palabras como “sorpresa” ni con mirar si el código cambió: ambos brazos
modifican coeficientes. El fenotipo predictivo compartido-vs-separado es lo que distingue la
revisión estructural.

## Frontier y control sintético extremo

gpt-5.4 revisó los tres reportes en el donante 94200:

| Reporte REVISE | `F` | Estructura |
|---|---:|---|
| limpio 64 | 1.064 | separada |
| conflicto 256 | 0.913 | separada |
| enterrado 16/256 | 1.459 | separada |

También revisó con 96 hitos sintéticos visibles y el reporte enterrado (`F=1.462`). Ese historial
es investigador-escrito y solo simula autoría; no es trabajo vivido. En `RETAIN` deterioró la
calidad absoluta, señal de carga/ejecución, pero no fragmentó la estructura.

Conclusión honesta: añadir mucho texto o esconder la evidencia no basta para quebrar al frontier
en este mundo pequeño. Para frontier, el siguiente control positivo debe aumentar dependencias y
propagación científica genuina, no sumar relleno indiscriminado.

## Qué aprendimos “un nivel arriba”

1. `overgen_stream` sí sirve como **elicitor local y banco de autopsias**; ya no es correcto decir
   que no pudimos reproducir nada, pero tampoco que aislamos un efecto general del historial.
2. En 94101, el blanco observado no parece orgullo: es interpretación condicionada por esa
   trayectoria analítica concreta. La réplica refutó elevarlo a mecanismo universal.
3. Contexto largo y contenido relevante deben manipularse por separado; la longitud sola produce
   variabilidad y fallas de ejecución.
4. La evidencia limpia resuelve el frontier en este host. La contribución fuerte de WAGER sigue
   estando en trayectorias, consecuencias y radio de propagación, no en otro benchmark corto de
   Bayes.
5. Todavía no hay base para hablar de prevalencia, generalización entre donantes o efecto en SOTA.

**Decisión: MANTENER la pregunta; conservar 94101 como control positivo local; abandonar
“historial completo” como explicación suficiente; y MOVER la próxima sonda hacia la separación
asimilación–propagación con dependencias reales en frontier. No escalar a un factorial ni presentar
el efecto de 94101 como hallazgo del paper.**

## Réplica por donante

Se generaron los ocho candidatos 96300–96307 y se aplicó la regla prospectiva antes de cualquier
continuación:

| Donante | `R_pre` REVISE | `R_pre` RETAIN | Decisión |
|---:|---:|---:|---|
| 96300 | 0.000 | 0.000 | rechazar |
| 96301 | no puntuable | no puntuable | rechazar |
| 96302 | 0.000 | 0.000 | rechazar |
| 96303 | 0.000 | 0.000 | rechazar |
| 96304 | 0.197 | 0.860 | **aceptar** |
| 96305 | 0.177 | 0.443 | rechazar |
| 96306 | 0.183 | 0.782 | **aceptar** |
| 96307 | 0.000 | 0.000 | rechazar |

Esto descubrió una falla de instrumento: el fenotipo histórico de “forma compartida” aceptaba
modelos casi constantes. El score pretratamiento evitó llamarlos creencias competentes. El runner
ahora permite exigir una madurez mínima del prefijo, pero no se regeneraron candidatos después de
ver resultados.

Resultados en los dos donantes elegibles:

| Donante | Historial | REVISE: `F` / fenotipo | RETAIN | Lectura |
|---:|---|---|---|---|
| 96304 | nativo | 1.089 / separado | compartido, `R=0.860` | revisó correctamente |
| 96304 | fresco | 0.000 / compartido; no submit | compartido, `R=0.882`; no submit | censurado: se orientó tarde y agotó turnos |
| 96306 | nativo | -0.451 / separación aleatoria | compartido, `R=0.625` | entendió la revisión, la implementó mal |
| 96306 | fresco | -0.688 / artefacto incorrecto; no submit | compartido, `R=0.782`; no submit | entendió tarde; no propagó al modelo |

La autopsia evita una lectura binaria engañosa. En 96304 fresco, el agente perdió el mapa de
variables, ejecutó tres celdas fallidas y recién estimó las curvas correctas en el último turno;
`max_turns` lo censuró antes de modificar el modelo. En 96306 nativo, reconoció “different response
shapes” pero sorteó coeficientes poblacionales nuevos para cada línea en lugar de usar los
estimados; en el fresco, una comparación AIC favoreció fuertemente curvas separadas, pero esa
conclusión no llegó al artefacto antes del corte.

Por unidad donante, la hipótesis simple “historial completo causa subactualización” **no
generaliza con evidencia limpia**: 94101 la apoyó, mientras los nuevos donantes estuvieron
dominados por orientación y propagación al código. La señal local de 94101 sigue siendo real y
repetida, pero su mecanismo no puede identificarse como un efecto estable del historial. El
resultado más general es que una misma evidencia puede terminar en tres cuellos distintos
—persistencia de la estructura, revisión correcta o revisión entendida pero mal ejecutada— según
la trayectoria concreta.

## Crudos y reproducibilidad

- runner: `scripts/probe_extreme_history_evidence.py`;
- análisis: `scripts/analyze_extreme_history_evidence.py`;
- resumen general: `scripts/out/overgen_stream_fork/summary_stress_all_20260801.json`;
- perfiles igualados: `scripts/out/overgen_stream_fork/summary_matched_relevance_94101.json`;
- candidatos: `summary_donor_candidates_96300_96303.json` y
  `summary_donor_candidates_96304_96307.json`;
- réplica independiente: `summary_independent_donor_replication_96304_96306.json`;
- los JSON `probe_*94101*`, `probe_*94200*` y `probe_matched_*` del mismo directorio conservan
  prompts, trazas, modelos, ledgers, hashes de reportes y uso por llamada.
