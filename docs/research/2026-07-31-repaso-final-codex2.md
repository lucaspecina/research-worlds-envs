# Repaso final de literatura y comunidad para WAGER

## Veredicto ejecutivo

**No encontré, hasta el 31 de julio de 2026, un trabajo que reúna la contribución completa de WAGER**: episodios agénticos largos con acciones y consecuencias; evaluación mediante el modelo predictivo final contra una verdad oculta y verificable; bifurcación del mismo episodio congelado modificando una sola condición; manipulación separada de claridad de señal, autoría de la trayectoria y fricción de revisión; y descomposición conjunta en rigidez, influenciabilidad, subactualización, sobreactualización y actualización en dirección errónea.

Lo que sí ocurrió durante los últimos meses es que **distintos trabajos ocuparon casi todas esas piezas por separado**:

- BayesBench mide trayectorias probabilísticas multivuelta y sub/sobreactualización.
- Strategic Play conecta observaciones, creencias y acciones en entornos interactivos con consecuencias.
- Agentic Forecasting y FutureSim evalúan agentes que buscan evidencia durante mucho tiempo y entregan predicciones puntuadas contra resultados reales.
- GeneBench-Pro evalúa trabajo científico multietapa cuyo resultado terminal depende de haber reaccionado correctamente a diagnósticos intermedios.
- Causal Agent Replay y AgenTracer introducen bifurcación y replay ejecutado de trayectorias.
- DeltaLogic aplica ediciones mínimas controladas a la evidencia.
- La literatura psicométrica de 2026 muestra que las disposiciones medidas en viñetas o autorreportes suelen tener baja validez ecológica.

Por eso, el riesgo principal **no es que exista ya “WAGER con otro nombre”**, sino que un reviewer pueda interpretar WAGER como la unión incremental de estas líneas. La defensa debe ser muy explícita: **la unidad evaluada no es una respuesta, una probabilidad verbalizada ni una acción aislada, sino cuánto cambia causalmente la calidad predictiva del producto de trabajo del agente cuando recibe la misma evidencia diagnóstica bajo condiciones distintas**.

La pieza más novedosa y defendible parece ser esta combinación:

> **Contrafactual causal sobre el mismo trabajo ya realizado + evidencia diagnóstica igualada + consecuencia medida en una predicción verificable.**

Eso sigue abierto.

## Mapa de riesgo competitivo reciente

| Trabajo | Qué midió exactamente y formato de tarea | Relación con WAGER |
|---|---|---|
| **BayesBench**, junio de 2026 | Cuatro entornos multivuelta: inferencia del sesgo de una moneda, recomendación cold-start tras 50 ratings, predicción de veredictos sociales y triage médico. En cada turno elicita una distribución sobre un estado latente y, cuando corresponde, una predicción downstream. Compara la trayectoria con un posterior bayesiano en los entornos donde es calculable. Encuentra que modelos mayores recuperan mejor el latente pero frecuentemente llevan la predicción demasiado hacia los extremos. citeturn14view1turn16view4turn16view5turn16view6 | **Competidor más próximo en medición normativa.** Valida medir la trayectoria y la entrega, pero no hay trabajo agéntico abierto, consecuencias de decisiones, trayectoria propia ni forks apareados. |
| **Why Do LLMs Struggle in Strategic Play? Broken Links Between Observations, Beliefs, and Actions**, abril de 2026 | Juegos repetidos de forma normal, póker de Kuhn generalizado y The Chameleon. Define el Bayesian Coherence Coefficient como la relación entre los cambios de log-odds del modelo y los cambios bayesianos correctos. La pendiente cae con los turnos, indicando subactualización. También interviene causalmente representaciones de creencia y observa cambios en la política de acción. citeturn14view2 | **Compite conceptualmente.** Tiene flujo interactivo, consecuencias y proporcionalidad; WAGER se distingue por el producto predictivo terminal, la trayectoria de trabajo extensa y las bifurcaciones sobre condiciones experimentales. |
| **Agentic Forecasting using Sequential Bayesian Updating of Linguistic Beliefs**, abril de 2026, actualizado en julio | Agente de forecasting que busca en la web, abre fuentes y mantiene en cada paso una probabilidad más un resumen de evidencia. La acción de investigación y la creencia actualizada salen en la misma llamada. La predicción final se puntúa contra eventos reales mediante reglas de scoring de forecasting. Quitar el estado de creencia o acumular texto sin estructura empeora el rendimiento. citeturn16view0turn17view1turn17view2turn20search16 | **Competidor fuerte en formato de entrega.** Es el precedente más claro de agente largo cuyo output es una distribución verificable, pero evalúa un sistema diseñado para actualizar, no las condiciones causales bajo las que un modelo actualiza. |
| **FutureSim: Replaying World Events to Evaluate Adaptive Agents**, mayo de 2026 | Replay offline de 88 días de noticias, con 330 preguntas abiertas. Los agentes poseen shell, archivos y buscador sobre un corpus que se revela día a día; pueden mantener workspace y revisar distribuciones sobre hasta cinco outcomes. Se puntúa con Brier Skill Score y exactitud final. El matching entre respuestas libres y verdad usa DeepSeek, por lo que no cumple el requisito de ausencia de juez-LLM. citeturn21view1 | **Compite en horizonte y forecasting.** WAGER debe enfatizar grading determinista, intervención experimental y una entrega que sea consecuencia del trabajo acumulado, no solamente forecasts renovables. |
| **LLMs are not consistently Bayesian**, mayo de 2026 | Elicita del propio modelo prior, likelihood y posterior para animales, ideología política, diagnóstico y un juego de reglas ocultas. Define un information-processing gap que mide inconsistencia bayesiana sin necesitar un prior externo. Compara actualización secuencial, donde la evidencia anterior se omite pero se transmite el estado previo, contra procesamiento batch. citeturn14view0 | **Valida la proporcionalidad, no compite en ecología.** Es una prueba de coherencia interna basada en probes, sin trayectoria autónoma ni producto de trabajo. |
| **OAKS: Online Adaptation to Continual Knowledge Streams**, marzo de 2026 | Streams largos de cambios factuales donde una misma pregunta reaparece durante diferentes fases del mundo. Evalúa modelos con contexto completo, RAG y memorias agénticas. Separa transiciones no incorporadas —subactualización— de volatilidad cuando la verdad no cambió —sobreactualización—. citeturn14view3 | **Valida la taxonomía de fallas y el eje de dilución.** No estudia trabajo con consecuencias ni iguala contenido diagnóstico entre condiciones. |
| **DeltaLogic: Minimal Premise Edits Reveal Belief-Revision Failures**, abril de 2026 | Convierte ejemplos de FOLIO y ProofWriter en episodios de cuatro turnos. Inserta soporte, inserta un hecho derrotador, elimina soporte o agrega un hecho irrelevante. Mide exactitud inicial y revisada, inercia, over-flip y abstención. Las modificaciones tienen efectos semánticos deterministas. citeturn21view0 | **Competidor en el principio “cambiar una sola cosa”.** Pero su intervención es local, lógica y de un turno; no congela una trayectoria agéntica extensa ni observa consecuencias downstream. |
| **Do Language Models Update their Forecasts with New Information?**, septiembre de 2025, actualizado en 2026 | EvolveCast alinea 1.613 pares pregunta–noticia de 203 preguntas de Metaculus. Compara el cambio de confianza del modelo con el cambio del agregado humano mediante dirección, magnitud absoluta y magnitud relativa. Acumular varias noticias generalmente no ayuda y puede diluir la señal; los modelos son mejores acertando la dirección que produciendo una magnitud calibrada. citeturn17view3turn17view4turn16view1 | **Valida fuertemente claridad/dilución.** Sin embargo, la cantidad y el contenido diagnóstico no están igualados, y la referencia es el movimiento de forecasters humanos, no una verdad oculta normativa. |
| **TimeSeek**, abril de 2026 | Diez modelos, 150 mercados regulados de Kalshi, cinco checkpoints del ciclo de vida y condiciones con/sin búsqueda, para 15.000 forecasts. Web search mejora el Brier Skill Score agregado, pero lo empeora en una fracción de combinaciones modelo–momento. citeturn21view3 | **Valida que “más evidencia/herramientas” no implica mejor actualización.** Es descriptivo entre snapshots, no causal sobre el mismo episodio. |
| **GeneBench-Pro**, junio de 2026 | 129 análisis científicos multietapa sobre datasets deliberadamente desordenados. Cada problema tiene un estimando terminal identificable, pero llegar a él requiere elegir correctamente entre forks estadísticos dependientes. Las fallas tempranas contaminan la decisión científica downstream. citeturn23view1turn23view2 | **Competidor vecino más serio en trabajo profesional largo.** No mide actualización de creencias, no interviene evidencia ni trayectoria y no produce una curva de sub/sobreactualización. |
| **Causal Agent Replay**, junio de 2026 | Reejecuta trayectorias interviniendo un paso y resampleándolo con la misma política. Estima cuánto cambia la distribución del resultado, con intervalos de confianza y asignación Shapley cuando hay interacciones entre pasos. citeturn18view4 | **Cambia el diseño.** Proporciona vocabulario y controles causales que WAGER debería adoptar, aunque su objetivo es atribuir una falla, no medir incorporación de evidencia. |
| **Beyond Forecasting: The Belief-to-Trade Layer**, julio de 2026 | Toma forecasts archivados y mantiene esas creencias fijas mientras modifica módulos de decisión, sizing y riesgo para medir cómo se traducen en rendimiento económico. citeturn21view4 | **Valida la separación belief → action → consequence.** WAGER debería distinguir error de actualización de error de utilización de una creencia ya correcta. |

Mi ranking de riesgo es:

**Riesgo alto de solapamiento parcial:** BayesBench, Strategic Play, Agentic Forecasting y GeneBench-Pro.

**Riesgo medio:** FutureSim, DeltaLogic, EvolveCast, OAKS y Causal Agent Replay.

**Riesgo bajo pero útil para framing:** TimeSeek, BeliefShift, BASIL, LoopTrap y los sistemas de memoria bayesiana.

Ninguno cubre el tratamiento **trayectoria heredada versus etiquetada como propia versus realmente construida**. Tampoco encontré un benchmark que mantenga constante el contenido diagnóstico y modifique únicamente su saliencia o dilución dentro de una trayectoria congelada.

## Actualización normativa y proporcionalidad

**Belief-R no es un benchmark bayesiano ni mide grados de creencia.** Es un dataset lógico inspirado en la suppression task. En el primer paso presenta dos premisas compatibles con modus ponens o modus tollens y obtiene una conclusión inicial; luego agrega una tercera premisa que hace necesario revisar esa conclusión o mantenerla. Sus métricas son Belief Update Accuracy, Belief Maintain Accuracy y BREU, el promedio balanceado de ambas. El hallazgo central es el trade-off entre modelos que cambian demasiado y modelos que se aferran a su primera conclusión. citeturn18view0turn19search3turn19search6

**Impacto WAGER: valida separar rigidez de influenciabilidad, pero no mide sub/sobreactualización.** Para Belief-R una respuesta cambia o no cambia; no existe una magnitud normativa de cuánto debería cambiar.

**ReviseQA** extiende este paradigma a secuencias multivuelta de razonamiento lógico generadas a partir de ProverGen. El contexto previo es modificado progresivamente mediante adición o eliminación de hechos y reglas; un theorem prover verifica la respuesta correcta en cada estado. Pude verificar el paper de workshop en OpenReview y el repositorio público, pero no una publicación main-track. citeturn19search0turn19search2turn19search4turn19search13

**Impacto WAGER: valida usar un oráculo simbólico y cadenas de revisión, pero no es una evaluación agéntica ni proporcional.**

**DeltaLogic** es el sucesor metodológicamente más limpio: hace ediciones mínimas y posee controles donde el label debe permanecer estable. Esto permite separar stale commitment, unnecessary revision y abstención. Su propia limitación declarada es que estudia un único cambio, etiquetas cerradas y pequeños modelos, no cadenas largas o productos abiertos. citeturn21view0

**Impacto WAGER: cambia el diseño.** Conviene adoptar explícitamente sus dos familias de contrafactuales: tratamientos donde la predicción normativa debe cambiar y placebos donde debe permanecer igual.

**Bayesian Teaching** tampoco es principalmente un benchmark: es una intervención de fine-tuning. Un usuario simulado elige vuelos durante varias interacciones y el asistente debe inferir una función de preferencias para recomendar la siguiente opción. Los modelos base mejoran poco después de la primera ronda; después de entrenarlos con las elecciones del asistente bayesiano, sus recomendaciones coinciden aproximadamente 80% con él y generalizan a hoteles y web shopping. Además, los modelos entrenados se vuelven más sensibles a la informatividad de cada comparación. citeturn18view1

**Impacto WAGER: valida que la informatividad marginal debe ser parte de la verdad normativa.** También sugiere evaluar si una intervención mejora la conducta final, no solamente la probabilidad verbalizada.

**BASIL** es el trabajo de sycophancy más cercano a la taxonomía de cinco fallas. En conversación, moralidad y aceptabilidad cultural, el modelo entrega prior, probabilidades de evidencia, likelihood y posterior. Los autores calculan el posterior que sería bayesianamente coherente con las propias cantidades del modelo y clasifican el resultado como dirección correcta o incorrecta y, dentro de la dirección correcta, subactualización o sobreactualización. Una opinión o racionalización atribuida a otra persona puede desplazar el posterior y frecuentemente aumentar el error. citeturn17view8turn17view9turn16view3

**Impacto WAGER: valida casi exactamente la taxonomía, pero no la validez externa.** Hay una caveat importante: BASIL mide coherencia entre números elicited del propio modelo, no cuánto mejora una predicción real debido a evidencia objetivamente diagnóstica.

**BayesBench** representa un avance mayor porque combina trayectoria completa, posterior por turno y predicción downstream. En moneda y recomendación dispone de una referencia bayesiana cerrada; en social judgment y medicina, la evidencia es lenguaje natural y no existe un posterior exacto comparable. El paper reconoce además que las distribuciones obtenidas dependen del formato del probe y que inferir correctamente un latente no garantiza utilizarlo bien en la predicción final. citeturn16view4turn16view5turn16view6

**Impacto WAGER: obliga a no definir “actualización correcta” sólo por una creencia intermedia.** La métrica primaria debe ser el delta de proper score del producto predictivo; los probes de creencia deberían quedar como mecanismo secundario.

**EvolveCast** mide explícitamente dirección y magnitud de actualización, pero toma como referencia el cambio del crowd de Metaculus. Eso responde “¿se movió como los forecasters humanos?”, no necesariamente “¿se movió en la cantidad epistémicamente correcta?”. Los propios autores señalan que la resolución final tampoco es una referencia suficiente para juzgar una actualización puntual: un evento puede terminar ocurriendo aunque, dados los datos disponibles en ese momento, sólo justificara 60%. citeturn17view3turn17view4

**Impacto WAGER: cambia el diseño estadístico.** Para hablar rigurosamente de sub/sobreactualización hacen falta episodios generativos donde conozcan tanto la verdad oculta como la likelihood de la evidencia, no solamente el outcome realizado.

Una formulación recomendable sería medir, para cada bifurcación:

\[
\Delta_{\text{modelo}}
=
\operatorname{logit}\hat p_{\text{post}}
-
\operatorname{logit}\hat p_{\text{pre}}
\]

y compararla con:

\[
\Delta_{\text{normativo}}
=
\log
\frac{P(e\mid y=1)}{P(e\mid y=0)}.
\]

El cociente o pendiente entre ambos permite distinguir de manera continua:

- alrededor de cero: rigidez o no incorporación;
- entre cero y uno: subactualización;
- alrededor de uno: actualización proporcional;
- mayor que uno: sobreactualización;
- signo contrario: actualización errónea.

La puntuación contra la verdad oculta sigue siendo la métrica principal de utilidad predictiva; el delta normativo sirve para explicar **por qué** mejoró o empeoró. Esta separación evita premiar a un modelo que llega casualmente al outcome correcto mediante una actualización epistemológicamente injustificada.

## Trayectorias agénticas y evaluación causal

**Agentic Forecasting es la respuesta más cercana a “actualización en un flujo agéntico largo con consecuencias sobre la entrega”.** En cada paso el modelo decide qué herramienta usar, recibe una observación y entrega simultáneamente un estado semiestructurado con probabilidad y resumen de la evidencia. Esa creencia entra en la historia y condiciona las siguientes búsquedas. El episodio termina cuando el agente hace `submit`, y la predicción se puntúa contra el resultado real. La ablación sin estado de creencia estructurado y la variante batch empeoran claramente el forecasting. citeturn16view0turn17view0

Pero no es una evaluación causal de actualización. El agente elige evidencia diferente entre runs, los historiales divergen y no se puede atribuir una diferencia final a una condición concreta. Además, el sistema está diseñado deliberadamente para promover actualización explícita, mientras que WAGER pretende medir el comportamiento espontáneo del modelo.

**Impacto WAGER: compite en framing, pero valida la necesidad de congelar la trayectoria.**

**Strategic Play** sí introduce consecuencias inmediatas: las creencias afectan apuestas, jugadas y coordinación. Su resultado más relevante es que el vínculo observación → creencia se degrada con la longitud, y que incluso creencias correctas pueden no traducirse en acciones coherentes. citeturn14view2

**Impacto WAGER: cambia el modelo causal.** Conviene separar al menos tres errores:

\[
\text{evidencia}\rightarrow\text{creencia},
\quad
\text{creencia}\rightarrow\text{modelo predictivo},
\quad
\text{modelo predictivo}\rightarrow\text{decisión}.
\]

Si WAGER sólo observa la predicción final, una falla puede ser de incorporación o de utilización. Los probes intermedios, aunque no sean la métrica principal, ayudan a identificar ese punto de ruptura.

**FutureSim** recrea bastante bien la temporalidad real. La evidencia aparece día por día, el agente puede investigar, escribir archivos y revisar forecasts durante casi tres meses simulados. Sin embargo, todos los agentes pueden construir trayectorias distintas y la evaluación no presenta el mismo episodio bajo condiciones apareadas. Además, el matcher de outcomes es otro LLM. citeturn21view1

**Impacto WAGER: valida horizonte y workspace persistente, pero también la ventaja de un entorno sintético con grader determinista.**

Sobre **bifurcación o replay apareado**, sí existe ya una comunidad emergente:

**Causal Agent Replay** representa una trayectoria como un modelo causal, resamplea un paso bajo la misma política y ejecuta nuevamente el resto. No pregunta a un juez qué paso “parece culpable”: calcula cuánto cambia la distribución del outcome. También usa Shapley para repartir responsabilidad cuando dos pasos interactúan. citeturn18view4

**AgenTracer** modifica y reejecuta trayectorias multiagente para localizar quién y en qué paso introdujo una falla. Trabajos posteriores describen su replay como sistemático, pero advierten que alterar una acción modifica los prompts, herramientas y coordinación posteriores, generando forks muy distintos y atribuciones inestables. citeturn18view4turn23view4

**Impacto WAGER: cambia el diseño de forma importante.** WAGER debería decir que no inventa el counterfactual replay en agentes; su novedad está en **qué se interviene y qué efecto se estima**:

- CAR interviene una acción endógena para localizar una falla.
- WAGER interviene una condición exógena de presentación, autoría o costo, manteniendo constante la información diagnóstica.
- CAR deja correr una nueva trayectoria downstream.
- WAGER puede medir tanto el efecto total —permitiendo divergencia— como un efecto controlado —con herramientas y observaciones posteriores fijadas—.
- CAR pregunta qué paso causó el fracaso.
- WAGER pregunta qué condición impidió que la evidencia mejorara el modelo predictivo.

Para que la inferencia sea defendible, cada fork debería compartir el mismo prefijo serializado, archivos, memoria, estado del entorno, resultados de herramientas, presupuesto restante, temperatura y semillas cuando sean controlables. Después de la intervención conviene reportar dos estimandos:

\[
\text{ATE total}
=
E[S(Y_{\text{fork A}})-S(Y_{\text{fork B}})]
\]

donde se permite que la política siga caminos diferentes, y

\[
\text{efecto directo controlado}
\]

donde las observaciones posteriores se mantienen iguales. El primero captura consecuencias reales; el segundo identifica con más limpieza el efecto cognitivo de la condición.

## Fricción, costo hundido y dependencia de trayectoria

No localicé una evaluación empírica de 2025–2026 que manipule causalmente **trabajo realmente invertido por un agente** y luego mida si ese mismo agente revisa adecuadamente una entrega predictiva cuando aparece evidencia contraria.

Los trabajos existentes cubren sustitutos débiles.

**LoopTrap** incluye un “Sunk Cost Trap” dentro de ataques de termination poisoning. La inyección le recuerda al agente que ya invirtió mucho esfuerzo y que detenerse desperdiciaría el progreso. Esto puede prolongar innecesariamente una ejecución, pero manipula una frase persuasiva: no compara una trayectoria realmente construida con la misma trayectoria heredada. citeturn18view6

**Impacto WAGER: valida que el framing de inversión puede modificar conducta, pero deja completamente abierta la autoría real de la trayectoria.**

**Revisable by Design** formula teóricamente el costo de adaptación de un agente streaming como la suma del costo de compensación y el trabajo abandonado. Evalúa cambios aditivos, restrictivos, sustitutivos, cancelaciones y cambios de prioridad. Esto trata el sunk cost como costo objetivo del sistema, no como sesgo psicológico del modelo. citeturn18view5

**Impacto WAGER: cambia la manipulación de fricción.** Hay que separar costo racional de revisión y apego irracional a lo producido. Si revisar exige rehacer veinte archivos, no revisar puede ser óptimo.

**GeneBench-Pro** observa una forma relacionada del problema: los modelos suelen notar una anomalía estadística pero no modificar el workflow apropiadamente y continúan por un fork incorrecto. Los autores lo denominan notice–act gap. citeturn23view3

**Impacto WAGER: valida que detectar una corrección y actuar sobre ella son capacidades distintas, pero no atribuye la falla a costo hundido.**

El eje de trayectoria de WAGER es, por tanto, probablemente original, pero debe diseñarse con cuidado. Las tres condiciones propuestas no aíslan un único mecanismo si se implementan superficialmente:

| Condición | Qué puede cambiar además de la “autoría” |
|---|---|
| Trayectoria heredada | Menor comprensión del estado, menor memoria episódica y menor conocimiento tácito de decisiones previas |
| Heredada pero etiquetada como propia | Identidad narrativa o compromiso declarado, sin experiencia real de construcción |
| Construida realmente | Comprensión, exposición repetida, esfuerzo invertido, selección endógena y posible racionalización de decisiones propias |

La comparación **heredada versus “te dijeron que es tuya”** aproxima el efecto de ownership narrativo. La comparación **“te dijeron que es tuya” versus realmente construida** mezcla sunk cost, memoria, comprensión y selección endógena.

Para aislar mecanismos sería recomendable añadir una cuarta condición: **trayectoria observada paso a paso pero sin capacidad de decidir**. El modelo recibe exactamente las mismas acciones y resultados durante la construcción, pero se le informa que fueron seleccionados por otro agente. Así se controla exposición y comprensión sin ownership decisional.

La fricción también debería descomponerse:

- **Fricción mecánica:** cantidad de acciones o archivos que deben rehacerse.
- **Costo de descarte:** cuánto trabajo previo se invalida.
- **Costo reputacional:** reconocer explícitamente que la estrategia anterior fue incorrecta.
- **Reversibilidad:** posibilidad de crear una rama nueva sin destruir la anterior.

La condición de baja fricción ideal no debería ser simplemente “¿querés cambiar tu respuesta?”. Debería ofrecer una operación real y barata, como clonar el workspace, recalcular el modelo y reemplazar automáticamente los outputs dependientes. Así se distingue incapacidad de actualización de costo operativo razonable.

## Validez externa y críticas a las evaluaciones de disposición

**No encontré una investigación que tome los mismos modelos, mida primero sycophancy, terquedad o sunk cost mediante viñetas cortas y luego pruebe si esos scores predicen el comportamiento de esos modelos en tareas agénticas largas comparables.** Esta ausencia es uno de los gaps más claros y publicables de WAGER.

Hay evidencia indirecta considerable de que la correlación podría ser baja.

**Incoherent Beliefs & Inconsistent Actions** muestra que alta exactitud o buena calibración estática no garantiza actualización bayesiana ni acciones coherentes con las creencias. En perfiles de diabetes divide las features en dos conjuntos, elicita una probabilidad con el primero y agrega el segundo como evidencia; la posterior directa puede diferir sustancialmente de la calculada a partir del prior y likelihoods del propio modelo. En mercados de apuestas, algunos modelos incluso apuestan en dirección contraria a la probabilidad que acaban de expresar. También mide si la disposición a ceder ante “tu respuesta es incorrecta” varía razonablemente con la confianza inicial. citeturn16view2turn17view5turn17view6

**Impacto WAGER: valida que un proxy estático no basta, pero no prueba directamente la transferencia micro → macro.**

**Do Psychometric Tests Work for LLMs?**, EACL 2026, estudia 17 modelos con tests humanos de sexismo, racismo y moralidad. Los instrumentos presentan una fiabilidad moderada frente a variaciones de ítems y prompts, pero sus scores no se alinean —y a veces correlacionan negativamente— con el comportamiento en tareas downstream. citeturn22view2

**Impacto WAGER: valida directamente la preocupación por validez ecológica.** El hecho de que una escala sea repetible no significa que mida conducta fuera de su formato.

**Rethinking Psychometric Evaluation of LLMs** encuentra que la coherencia entre autorreporte y conducta puede aparecer cuando ambos comparten contexto, pero colapsa para la mayoría de los modelos cuando los contextos se separan. Los autores concluyen que estas “disposiciones” se entienden mejor como acoplamientos contextuales que como rasgos estables entre situaciones. citeturn22view0

**Impacto WAGER: cambia el análisis.** No conviene asumir un único parámetro de “terquedad del modelo”; hay que estimar interacciones entre modelo, dominio, scaffold, longitud y condición.

**An LLM-Native Psychometric Instrument Reveals a Self-Report–Behavior Gap Across 25 Models**, actualizado en julio de 2026, llega a una conclusión similar incluso usando un instrumento diseñado específicamente para modelos, en lugar de importar sin cambios una escala humana. citeturn23view0

**Impacto WAGER: valida estudiar comportamiento revelado, no auto-descripciones o preferencias declaradas.**

El review de NeurIPS 2025 sobre **construct validity in LLM benchmarks** revisó 445 benchmarks y encontró que los constructos frecuentemente se definían de forma insuficiente y se operacionalizaban mediante tareas preexistentes cuya representatividad no estaba demostrada. citeturn22view3

**Impacto WAGER: cambia el framing del paper.** “Belief updating” debe definirse operacionalmente antes del benchmark, no inferirse después a partir de cualquier cambio de respuesta.

**Bloom**, de Anthropic, mejora la generación reproducible de evaluaciones conductuales y muestra acuerdo con anotaciones humanas y separación entre modelos baseline e intencionalmente desalineados. Pero esa validación demuestra que el instrumento reconoce escenarios sintéticos correctamente etiquetados; no demuestra que la frecuencia de una conducta en esos escenarios prediga su frecuencia en un deployment largo. citeturn22view4

**Impacto WAGER: valida la utilidad de escenarios controlados, pero deja abierto el criterion validity externo.**

La oportunidad fuerte sería incluir dentro de WAGER un estudio explícito de transferencia:

1. Construir una **micro-eval hermanada** con cada tratamiento largo: misma estructura causal, misma clase de evidencia y misma decisión normativa, pero condensada a una viñeta de uno o dos turnos.
2. Evaluar los mismos model–scaffold–prompt configurations en micro y macro.
3. Estimar correlación de ranking, calibración predictiva y varianza explicada.
4. Comparar predicción a nivel de modelo contra predicción a nivel de episodio.
5. Hacer cross-domain validation: ajustar sobre un dominio y predecir otro.

El resultado podría ser científicamente valioso incluso si la correlación es nula. En ese caso WAGER no sólo introduciría un benchmark: demostraría que las evals de disposición actuales carecen de la validez externa necesaria para justificar afirmaciones sobre agentes desplegados.

## GeneBench-Pro, reportes de labs y decisiones para WAGER

**GeneBench-Pro sí existe públicamente.** El documento oficial está fechado el 30 de junio de 2026, firmado por Jeremy Li y Andrew Ho con afiliación OpenAI en el paper. Contiene 129 evaluaciones en diez dominios principales; diez problemas completos son públicos, cincuenta se entregaron a Artificial Analysis y sesenta y nueve permanecen como holdout interno. citeturn23view1turn23view3

La frase “análisis sucios que requieren juicio” puede inducir a error sobre el grading. **No hacen que un juez-LLM evalúe si el razonamiento científico suena convincente.** Construyen o simulan los datos de modo que exista un target estimand identificable. El agente trabaja con archivos desordenados, hace QC, EDA, modelado y diagnósticos, y al final entrega campos estructurados. Un script específico por problema aplica exact match o tolerancias numéricas predefinidas; el score principal es binario, all-or-nothing. El razonamiento libre se conserva para análisis cualitativo, pero no determina la nota. citeturn10view0turn10view1turn23view2turn23view3

El “juicio” aparece en tres lugares:

- Los autores eligen un estimando que realmente debería informar una decisión downstream.
- Expertos externos revisan si el problema es realista y si el estimando está suficientemente identificado.
- El agente debe ejercer juicio para escoger el workflow correcto.

Pero **el grader no juzga ese juicio directamente**. Juzga si condujo al endpoint correcto. Ésta es exactamente la filosofía adecuada para WAGER: convertir capacidades abiertas y difíciles de observar en consecuencias terminales verificables.

**Impacto WAGER: competidor vecino y modelo de grading.** Adoptaría su principio de “juicio durante la tarea, determinismo en el grader”, pero evitaría su binarización extrema usando proper scores continuos.

Sobre reportes de laboratorios, la evidencia disponible es más cualitativa que experimental.

En la evaluación de **GPT-4o de METR**, el equipo identificó diez runs donde el agente, cerca de entregar, saltaba a una conclusión no apoyada por su razonamiento previo. Un modelo más débil podía reconocer retrospectivamente la inconsistencia. METR rebobinó esos puntos, resampleó acciones y continuó el episodio: sólo cuatro de diez runs pasaron después del patch, y varios de los restantes cayeron en loops repetitivos. También documentaron mala interpretación de observaciones de herramientas como una categoría de error consecuencial. citeturn22view5

**Impacto WAGER: valida tres decisiones.** La capacidad de detectar retrospectivamente un error no implica incorporarlo online; reparar un paso puede revelar otra falla downstream; y el replay ejecutado es más informativo que pedir una crítica verbal.

El **International AI Safety Report 2026** sintetiza que los agentes pierden el estado del progreso, fallan frente a inputs inesperados y presentan una caída pronunciada al crecer la duración de las tareas. citeturn22view6

**Impacto WAGER: valida el horizonte largo, pero no demuestra específicamente una falla de actualización.** WAGER debe evitar atribuir todo fracaso en tareas largas a creencias: también existen memoria insuficiente, mala planificación, tool errors y límites de contexto.

GeneBench-Pro aporta un indicio más específico: los modelos suelen mencionar correctamente anomalías o diagnósticos, pero no alteran el análisis para resolverlos. citeturn23view3

**Impacto WAGER: valida usar la entrega y no el texto de razonamiento como evidencia de incorporación.**

No encontré un reporte de lab que haga exactamente lo siguiente: introducir una corrección controlada durante un deployment largo, ejecutar un fork idéntico sin corrección o con diferente fricción, y comparar deterministicamente el producto final. Por tanto, esa afirmación de novedad sigue siendo sostenible.

La especificación final que defendería para WAGER es:

| Componente | Decisión recomendada |
|---|---|
| Unidad experimental | Un prefijo completo y congelado de trayectoria, no dos runs independientes |
| Tratamiento | Una sola condición manipulada; evidencia diagnóstica y likelihood igualadas |
| Outcome primario | Proper score del modelo predictivo terminal contra una variable oculta |
| Outcome causal | Diferencia apareada de score entre forks del mismo episodio |
| Norma de actualización | Cambio esperado en log-odds dado el generative process |
| Modos de falla | No cambio, cambio por señal no diagnóstica, cambio insuficiente, excesivo o en dirección incorrecta |
| Consecuencias | Las decisiones posteriores consumen recursos, seleccionan datos o afectan qué predicción puede entregarse |
| Probes internos | Secundarios, para localizar evidence→belief frente a belief→delivery |
| Replay | Prefijo, archivos, tools, budgets y estado del mundo compartidos |
| Fricción | Separar costo real de revisión, pérdida de trabajo y framing de ownership |
| Validez externa | Microviñeta hermanada y tarea macro sobre los mismos modelos |
| Grading | Determinista y continuo; ningún juez-LLM en la métrica principal |

La claim central no debería ser genéricamente “los agentes no actualizan sus creencias”. Esa afirmación ya está densamente ocupada. La formulación más precisa y diferencial sería:

> **Evaluamos causalmente cuándo la evidencia nueva mejora —o empeora— el modelo predictivo que un agente produce después de haber construido una trayectoria de trabajo extensa, separando fuerza diagnóstica, saliencia, ownership y costo de revisión mediante forks apareados del mismo episodio.**

Con ese framing, BayesBench y BASIL aportan la norma de proporcionalidad; Agentic Forecasting y FutureSim aportan el paradigma de predicción agéntica; GeneBench-Pro aporta la filosofía de entrega verificable; CAR aporta la metodología contrafactual; y las críticas psicométricas aportan la motivación de validez externa. **La combinación, el estimando causal y la manipulación de dependencia de trayectoria continúan siendo propios de WAGER.**