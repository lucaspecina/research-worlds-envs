# Auditoría ecológica de escenarios e hipótesis del “cuaderno propio”

**Fecha:** 2026-08-01
**Estado:** reassessment exploratorio; hipótesis candidata, no nueva tesis oficial.

## Dos mapas que deben consultarse por separado

1. **Mapa de aparición:** dónde se documenta el vicio, qué estaba haciendo el agente, cómo llegó
   la información y en qué parte del flujo se perdió.
2. **Mapa de reproducción:** cómo benchmarks y proyectos relacionados fabrican el contraste,
   mantienen una norma correcta y observan cambio, conservación o acción posterior.

El primer mapa da fidelidad ecológica. El segundo aporta instrumentos. Copiar el instrumento sin
la ecología produce un test limpio pero posiblemente irrelevante; copiar una anécdota sin controles
produce una historia realista pero no un estimando.

## 1. Qué dicen los casos sobre memoria y longitud

La propuesta “los vicios aparecen cuando el agente ya no puede releer y depende de sus apuntes” es
**plausible como subfamilia y falsa como explicación universal**.

| Caso | Escala/estado | ¿La compresión es necesaria para explicar la falla? |
|---|---|---|
| Corral | flujo agéntico, datos y candidatos propios | No demostrado: reconoce la contradicción en el mensaje 18 y entrega lo anterior en el 20 |
| KellyBench | 500–1000 tools, estado persistente y temporadas | Compatible y probablemente importante, pero bajo el mismo régimen también hay adaptación |
| OSWorld / STALE | información intermedia o memoria recuperada | Sí apoyan una familia de estado/memoria; STALE muestra que visible no implica que gobierne |
| RadLE | una imagen y una generación | No: ve el rasgo correcto y vuelve al diagnóstico inicial dentro del mismo razonamiento |
| Xie | una viñeta | No: la evidencia mixta basta para inducir selección confirmatoria |
| Kumaran | dos turnos | No: ver la respuesta propia reduce la revisión sin carga larga |
| Snowball / Yang | primer token o respuesta inmediata | No: el autoarrastre aparece antes de cualquier cuaderno |
| MemSyco | ~10 turnos; memoria histórica | La memoria vieja perjudica, pero también falla `Full Dialog`, donde la historia completa está disponible |

La lectura defendible es: **la forma de representar el pasado puede amplificar o reducir la
inercia**, especialmente en agentes largos. No es condición necesaria ni sabemos a priori el signo.
PABU incluso muestra que un estado compacto selectivo puede superar ampliamente al historial
completo; Context Rot demuestra que “más historia visible” también puede dañar.

La misma cautela vale para la receta opuesta “obra propia + evidencia mixta + post-compromiso”. Es
una conjunción candidata de alto rendimiento, no una explicación sin excepciones: Jeong parte de una
creencia precargada, STALE estudia invalidaciones indirectas y Seeing Isn't Believing encuentra
inercia ante observaciones del entorno. El objetivo del mapa es conservar estas familias rivales,
no sustituir una teoría universal prematura por otra.

## 2. Qué enseñan los proyectos que intentan medir fenómenos vecinos

| Proyecto | Cómo crea el fenómeno/contraste | Qué conviene copiar |
|---|---|---|
| BeliefTrack | estados finitos; turnos `stay/update/isolation`; pares misma evidencia con/sin ruido; verificador simbólico | controles bilaterales y separación de fallas, no su espacio de creencias de juguete |
| Bayesian Teaching / BayesBench | evidencia secuencial y posterior normativo exacto; evaluación en cada ronda | trayectoria completa y norma por turno; distinguir inferencia de acción downstream |
| STALE | memoria vieja/nueva, invalidación directa o propagada; resolución, resistencia a premisa y adaptación | separar recuperar, adjudicar y aplicar; incluir cambios indirectos |
| MemSyco | `No Memory` vs `Full Dialog` vs sistemas de memoria | comparar representaciones del pasado, sin asumir que compresión empeora |
| Context Rot | longitud, posición, distractores y coherencia controlados | tratar longitud/posición como confounds y resultados propios |
| LURE | replay de una trayectoria de uso real y gancho mínimo al final | reducir conciencia de evaluación y reutilizar prefijos ecológicos |
| Seeing Isn't Believing | observación ordinaria después de una acción; 7–10 pasos; reward del entorno | evidencia como consecuencia natural y comparador de proceso, prueba de que una historia enorme no es necesaria |
| Causal Agent Replay | una acción/paso se fija y se reejecuta contrafactualmente | bifurcar después de igualar la acción, como en el probe de dato propio |

## 3. Auditoría honesta de nuestro `overgen` actual

| Dimensión | Estado actual | Conducta que probablemente induce |
|---|---|---|
| Historia | commissioning simple y explícita | el agente sabe desde el inicio qué región importará |
| Formación | 4 turnos a menudo; a veces 12 | muchas veces no hay teoría propia estable; hay placeholder o ajuste prematuro |
| Memoria | transcript completo + variables Python persistentes | puede reagrupar y reajustar todos los datos cuando quiera |
| Volumen efectivo | cientos de filas, pero tres columnas y suficiente estadística simple | cognitivamente chico aunque tenga muchas filas |
| Evidencia | reporte anunciado, grande y agrupable | máxima atención; actualización mecánica |
| Problema | regresión por línea | cambiar estructura suele equivaler a cambiar coeficientes/cinco fits |
| Acción | inspeccionar, ajustar, entregar | casi no hay decisión intermedia gobernada por el modelo |
| Dependencias | ninguna o muy pocas | revisar no invalida trabajo real |
| Tiempo post-dato | normalmente 1–2 pasos | casi no puede aparecer reversión ni persistencia |
| Dinamismo | un hito y una entrega | no hay uso repetido del modelo ni consecuencias acumulativas |

Por eso `overgen` es un buen **control bilateral de actualización fácil** y un elicitor débil de
inercia ecológica. El probe de campaña propia mejora origen, búsqueda y acción igualada, pero no
resuelve por sí solo memoria, dependencias ni semántica estructural.

**Volumen de filas no equivale a carga cognitiva.** Un millón de observaciones reducibles a cinco
medias puede ser más fácil que veinte resultados que deben cruzarse con hipótesis, herramientas y
dependencias distintas. El generador futuro debe parametrizar complejidad de estado, no solo `n`.

## 4. Contraste correcto para la hipótesis de memoria

Dos brazos (`historia completa` vs `cuaderno`) mezclarían longitud, pérdida de información,
posición, autoría, conciencia de replay y calidad del resumen. El mínimo interpretable es:

| Brazo | Estado al continuar | Qué identifica |
|---|---|---|
| `H+N` | historia completa + el mismo cuaderno | referencia con acceso total |
| `N-self` | estado actual + cuaderno exacto, etiquetado como propio | efecto conjunto de depender del estado comprimido |
| `N-other` | mismos bytes que `N-self`, atribuidos a otro/registro neutral | componente de autoría atribuida, no contenido |

Los tres parten del mismo donante y de conversaciones nuevas. Se cruzan al menos con:

- **REVISE:** evidencia que exige cambio;
- **RETAIN:** evidencia compatible que debe conservar el modelo.

Antes del tratamiento debe pasar una **compuerta de fidelidad sin conflicto**: los tres estados
permiten continuar con modelo y acción equivalentes dentro de un efecto mínimo fijado. Si el
cuaderno omitió información necesaria, una peor actualización puede ser racional: el hallazgo es
falla de compresión/encoding, no terquedad.

El estimando no es score bruto. Es la interacción bilateral: revisión capturada en `REVISE`
menos deriva indebida en `RETAIN`, comparada entre representaciones. Si `N-self` empeora en ambos
polos, es degradación general; si cambia más siempre, es labilidad; si revisa menos sin derivar más,
aparece una señal de atrincheramiento.

## 5. Ficha de auditoría para todo escenario nuevo

Antes de construir o escalar, responder:

1. ¿Qué caso documentado reproduce y qué detalle causal conserva?
2. ¿Qué objetivo práctico cree estar resolviendo el agente?
3. ¿Qué creencia propia se formó y cómo sabemos que gobernó una acción?
4. ¿Qué parte del pasado puede releer, recuperar o solo recordar mediante un resumen?
5. ¿La carga es realmente cognitiva/causal o solo cantidad de filas/tokens?
6. ¿La evidencia llega como parte natural del trabajo o como cartel de evaluación?
7. ¿Qué tan ambiguo es el dato y qué explicaciones rivales siguen siendo defendibles?
8. ¿Cambiar exige un parámetro, una estructura o rehacer dependencias reales?
9. ¿Hay tiempo y acciones después para observar propagación, persistencia o reversión?
10. ¿Qué gemelo hace perder al reflejo contrario?
11. ¿Qué información permite distinguir búsqueda, atención, interpretación y asimilación?
12. ¿Qué resultado haría abandonar este escenario en vez de seguir maquillándolo?

## 6. Resultado del primer contraste real de representación

El probe sobre el donante DeepSeek `94101` no confirmó “los apuntes congelan la creencia”. En
`REVISE`, la rama con historia completa conservó la forma compartida pese a ver anomalías, mientras
la rama de apuntes separó las curvas pero implementó mal la incertidumbre. En `RETAIN`, ambas
construyeron modelos razonables, pero la rama sin workspace gastó turnos reconstruyendo estado y no
llamó a `submit`. Ver
[`resultado-probe-historia-vs-apuntes-94101.md`](2026-08-01-resultado-probe-historia-vs-apuntes-94101.md).

El signo mixto es coherente con la literatura: comprimir puede quitar ruido y también destruir
continuidad. Como el donante fue seleccionado con la anomalía conocida y el contraste cambia datos,
workspace e historia a la vez, no identifica un efecto de “apuntes propios”.

## Decisión

No pivotear WAGER entero a “memoria” ni escalar este probe. Memoria queda como eje posterior y
tratamiento del harness. La segunda estructura debe ser causal/semántica, contener una creencia que
gobierne trabajo y hacer que la evidencia nazca de una acción ordinaria del agente, no otra regresión
más larga ni otro reporte anunciado.
