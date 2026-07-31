> Notas de POSICIONAMIENTO de Lucas (2026-07-31), guardadas VERBATIM — su síntesis personal tras
> la campaña de lectura completa (16 papers a texto completo + 4 repasos; extracciones con citas
> en `docs/research/2026-07-31-lectura-*.md`, links y estado en `docs/lectura-de-fuentes.md`,
> cluster de posicionamiento). Es el mapa oficial de competidores y la tabla comparativa semilla
> del futuro paper. Las menciones "Paper" sin link son artefactos del export; los links viven en
> el registro.

WAGER no estudia simplemente si un modelo “cambia de opinión”. La pregunta es:

> **Cuando evidencia nueva justifica alejarse, reforzar o conservar un modelo previo —en una magnitud conocida—, ¿cuánto de esa respuesta legal llega al artefacto ejecutable que el agente entrega, y cómo cambia bajo trayectoria previa, dependencias y costo de reparación?**

- Para ubicar la literatura conviene separar seis dimensiones
    1. **Norma epistémica:** ¿se sabe cuánto debería actualizar?
    2. **Respuesta bilateral:** ¿incluye cambiar correctamente y también resistir cambios injustificados?
    3. **Trayectoria:** ¿el agente llega con trabajo previo realmente construido?
    4. **Fricción:** ¿corregir tiene un costo verificable?
    5. **Consecuencia aplicada:** ¿se puntúa una entrega o sólo una declaración?
    6. **Identificación causal:** ¿se compara el mismo episodio cambiando una sola condición?

---

## Competidores más directos en revisión normativa

- **BeliefTrack — *When Should Models Change Their Minds?***
  Dos mundos cerrados (descubrir reglas desde datos; diagnosticar circuitos) donde en cada turno se sabe qué debería creer el modelo. Separan tres fallas: no revisar cuando había que revisar, revisar cuando no, y moverse con ruido. **Leído por dentro: ya usan pares bifurcados** (mismo prefijo, cambia solo el ruido) con recompensa simbólica sin juez, **y entrenaron con RL** bajando las fallas de 99% a 0-30%. **Lo que no tienen:** la "creencia" es una lista de hipótesis discretas — no hay entrega ejecutable con consecuencia, ni trabajo propio acumulado, ni fricción, ni dosis de evidencia.

  Es el competidor conceptual más cercano. Construye dos mundos cerrados —descubrimiento de reglas y diagnóstico de circuitos— donde un oráculo simbólico determina qué hipótesis debería sostener el modelo en cada turno. Separa tres fallas:
    - no actualizar cuando cambió el estado correcto;
    - fallar cuando el estado debía permanecer estable;
    - dejarse desviar por información irrelevante.

  También utiliza pares clean/noise que comparten la evidencia y difieren sólo en el ruido, y entrena con reward simbólico sin juez LLM.

  Su límite es fundamental: la “creencia” es un conjunto discreto de hipótesis. No mide fuerza probabilística, sub/sobreactualización gradual ni evidencia parcial. Tampoco existe proyecto acumulado, presupuesto, reparación de dependencias ni artefacto ejecutable.

  **Importancia para WAGER:** ocupa cualquier claim amplio de ser los primeros en medir `cambiar / conservar / ignorar ruido`. WAGER debe diferenciarse por proporcionalidad, trayectoria, fricción y entrega ejecutable.

- **BayesBench**
  En tareas de varias rondas comparan cuánto actualiza el modelo contra cuánto *debería* actualizar según la matemática exacta. Hallazgos que nos convienen: los modelos se estancan después de la primera evidencia, y a veces infieren bien la estructura pero no la usan al predecir (su versión de "dice pero no entrega"). **Lo que les falta:** todo es a carga cero — sin trabajo propio, sin costo, sin nada firmado.

  Sigue trayectorias de creencia durante múltiples rondas y, donde el mundo lo permite, las compara con una referencia bayesiana. Su resultado más importante para nosotros es que un modelo puede inferir correctamente la estructura latente y aun así producir una predicción downstream mal calibrada.

  También encuentra patrones de subactualización y sobreactualización que dependen del modelo y del entorno.

  **Importancia para WAGER:** ocupa gran parte de la actualización normativa multivuelta. Su separación `inferir la estructura → usarla al predecir` es el antecedente más cercano de nuestra cadena `reconocer → registrar → actuar → entregar`.

  **Lo que queda abierto:** no hay proyecto propio, costo de reabrir, fork desde el mismo checkpoint ni artefacto construido.

- **Bayesian Teaching**

  En una tarea de recomendación multi-ronda, compara a los LLMs con un asistente bayesiano exacto. Los modelos base mejoran poco después de la primera interacción. Además, elicitar la creencia y convertirla externamente en una decisión funciona mejor que pedir directamente la decisión.

  Entrenar al modelo para imitar la actualización bayesiana generaliza mejor que entrenarlo sólo sobre respuestas finales.

  **Importancia para WAGER:** es un antecedente limpio de oráculo por construcción y muestra que aprender el proceso de actualización puede ser más útil que memorizar respuestas.

  **Límite:** carga prácticamente cero: sin obra previa, dependencias o costo de revisión.

- ***LLMs Are Not Consistently Bayesian***

  Separa la calidad del prior, las likelihoods atribuidas a la evidencia y la integración posterior. Su advertencia más importante es que seguir un Bayes explícito no siempre maximiza el rendimiento: la representación probabilística elicitada puede estar mal especificada o competir con conocimiento implícito útil del modelo.

  **Importancia para WAGER:** un valor bajo de incorporación no demuestra automáticamente “apego al trabajo propio”. También puede significar que el agente interpretó de otra manera la confiabilidad de la evidencia o posee un prior implícito competitivo.

  La defensa más fuerte de WAGER es utilizar mundos frescos con DGP conocido y evidencia cuya likelihood esté definida server-side.

- **BASIL**

  Compara cómo cambian probabilidades ante evidencia, opinión de un tercero y opinión del usuario. Distingue subactualización, sobreactualización y dirección equivocada.

  Su hallazgo más útil es que un mismo empujón puede:
    - empeorar a un modelo que ya sobreactualiza;
    - mejorar accidentalmente a otro que subactualiza.

  Promediar ambos casos puede producir un efecto aparentemente nulo.

  **Importancia para WAGER:** obliga a estratificar por régimen basal del donante. No alcanza con reportar un promedio de incorporación.

  **Límite:** su norma deriva de probabilidades declaradas por el propio modelo, no de una verdad externa, y no existe entrega ejecutable.

## Actualización en agentes con acciones y entregas

- **Agentic Forecasting**

  Un agente busca información en la web, mantiene una probabilidad junto con un resumen estructurado de evidencia y termina entregando un forecast puntuado contra resultados reales. Las ablaciones indican que mantener un estado explícito de creencia es tan importante como disponer de búsqueda.

  **Importancia para WAGER:** es probablemente el precedente más cercano a “agente largo que investiga, actualiza y entrega una distribución verificable”.

  **Diferencia:** evalúa un sistema diseñado para actualizar bien. No manipula causalmente las condiciones bajo las que el agente incorpora o rechaza una corrección. Tampoco bifurca el mismo trabajo previo.

- **Strategic Play — *Broken Links Between Observations, Beliefs, and Actions***

  Estudia juegos interactivos donde las creencias afectan apuestas, jugadas y coordinación. Compara los cambios observados con actualizaciones bayesianas y encuentra que la relación se deteriora con los turnos. Incluso una creencia correcta puede no traducirse en una acción coherente.

  **Importancia para WAGER:** ayuda a separar tres posibles fallas:
  `evidencia → creencia → modelo entregado → decisión`
  WAGER no debería llamar “falla de actualización” a toda mala entrega sin localizar primero dónde se rompió esa cadena.

  **Estado:** conceptualmente muy importante; conviene una lectura completa antes de usar resultados específicos.

- **STALE**
  Historias de hasta 150 mil tokens con información que queda obsoleta: los modelos reconocen que un dato ya no vale y actúan desde él igual (mejor modelo: 55%). **Lo que les falta:** todo el puntaje lo pone un juez-IA (confirmado con cita); no hay obra científica propia ni consecuencia.

  Presenta historias largas donde determinada información deja de ser válida. Los sistemas pueden reconocer bajo una pregunta directa que el dato quedó obsoleto y, aun así, seguir usándolo en una respuesta downstream.

  **Importancia para WAGER:** valida el fenómeno `recuperar/reconocer ≠ aplicar`.

  **Límite:** todo el scoring principal utiliza juez LLM. No existe verdad ejecutable, modelo científico propio ni reparación con consecuencias.

- **Seeing Isn’t Believing**
  Agentes que reciben observaciones contradiciendo su estado previo y siguen actuando desde la creencia vieja, medido por éxito de tarea con recompensa binaria del entorno (sin juez). Su remedio, el agente estima, verifica, y recién ahí actualiza, mejora +18 puntos: **es nuestro brazo comparador para separar "no quiso" de "no pudo"**.

  En entornos embodied, agentes reciben observaciones que contradicen su estado previo pero continúan actuando desde la creencia vieja. El fracaso se mide mediante reward del entorno, no por una explicación textual.

  Su scaffold `Estimate → Verify → Update` mejora considerablemente el éxito.

  **Importancia para WAGER:** es el mejor baseline de proceso para comprobar si estructurar explícitamente la revisión reduce la inercia. También confirma que ésta puede observarse en acciones y consecuencias, no sólo en probabilidades declaradas.

  **Precaución:** no separa por sí mismo “no quiso revisar” de “entendió pero no pudo reparar”. Para eso WAGER necesita controles de dificultad operativa y presupuesto.

- **FCPAgent — *Falsifiable Commitment Planning***

  Convierte cada paso de un plan en un compromiso con evidencia confirmatoria, posibles falsadores y confianza. Ante una contradicción decide continuar, avanzar o reparar, y clasifica el alcance de la reparación:
    - acción local;
    - componente o skill;
    - sufijo completo del plan.

  **Importancia para WAGER:** ofrece una taxonomía concreta de fricción. Una falla puede no estar en revisar la creencia, sino en propagar esa revisión por todas las dependencias del artefacto.

  **Diferencia:** es un sistema diseñado para autocorregirse, no una medición causal de la tendencia natural a revisar.

## Modelos ejecutables y grading contra verdad oculta

- **Autonomous Model Discovery — Virginia Tech/Baylor**
  Agentes de código (Codex, Claude Code) exploran datos de un juego real y entregan modelos ejecutables puntuados comparando distribuciones, sin juez. Hallazgo de ellos: más esfuerzo de razonamiento no mejoró la calidad, solo el costo. **Lo que no tienen:** una sola corrida (sin bifurcaciones apareadas), sin medición de actualización de creencias, sin trabajo previo ni fricción; su comparación de distribuciones es métrica de salida, no dosis de evidencia.

  Agentes de código construyen modelos predictivos y simuladores ejecutables sobre datos de un juego. Los productos se puntúan contra el DGP mediante métricas como KL y distancias distribucionales, sin juez LLM.

  El estudio analiza 140 corridas válidas y tiene comparaciones matched entre disponibilidad completa y parcial de datos. No es, sin embargo, un fork desde el mismo prefijo congelado.

  Un hallazgo llamativo es que aumentar el esfuerzo de razonamiento elevó costo y complejidad sin producir una mejora proporcional de calidad.

  **Importancia para WAGER:** ocupa claramente el claim “agente entrega modelo ejecutable comparado distribucionalmente contra verdad oculta, sin juez”.

  **Lo que deja abierto:** no existe modelo previo que revisar, evidencia correctiva post-checkpoint, trayectoria comprometida ni fricción de reparación.

- **GeneBench-Pro**
  Análisis científicos sucios multi-etapa corregidos por **scripts con tolerancias por campo, cero juez** (leímos hasta sus contratos de corrección públicos: https://huggingface.co/datasets/ajh-oai/genebench-pro-public-package). No mide revisión de creencias; su corrección todo-o-nada la declaran ellos como limitación — **que es justo lo que nuestra métrica graduada resuelve**. La frase del paper: ellos miden aprobado/reprobado al final; nosotros cuánto y por qué se actualiza.

  Evalúa 129 análisis científicos multi-etapa sobre DGPs simulados. El agente trabaja con datos desordenados, atraviesa decisiones estadísticas dependientes y entrega campos estructurados. Scripts deterministas aplican exact match o tolerancias numéricas por campo; el razonamiento textual no entra en el score.

  Su hallazgo cualitativo central es el *notice–act gap*: los modelos identifican señales diagnósticas locales, pero no propagan su implicancia al workflow.

  **Importancia para WAGER:**
    - legitima “juicio durante la tarea, determinismo en el grader”;
    - demuestra que el trabajo científico abierto puede puntuarse sin juez LLM;
    - aporta contratos de grading versionados y tolerancias específicas por campo.

  **Diferencia:** GeneBench-Pro mide éxito final todo-o-nada. No inyecta evidencia en un modelo previo ni mide dirección y magnitud de la revisión. WAGER puede convertir su observación cualitativa noticing→acting en un fenómeno graduado y causal, pero no debería afirmar que GeneBench ya midió subactualización formalmente.

## Fork, replay y dependencia causal

- **Causal Agent Replay**
  Intervenir un paso de una corrida de agente y re-ejecutar para comparar, sin juez. **Leído por dentro: es mayormente teórico** — su validación es sobre modelos sintéticos, no agentes reales. Para atribuir fallas, no para medir revisión. Bonus: advierten textual que un evaluador con juez-IA "inyecta su propio ruido". Siguen siendo los mejor posicionados para cruzarse a lo nuestro.

  Conserva el prefijo factual de una trayectoria, interviene un paso y reejecuta el downstream múltiples veces. Esto permite estimar distribuciones contrafactuales y localizar puntos de compromiso.

  **Importancia para WAGER:** es el prior art metodológico obligatorio del fork ejecutado. WAGER no inventa replay; debe diferenciarse por la intervención y el estimando.
    - CAR interviene acciones para atribuir una falla.
    - WAGER interviene evidencia, trayectoria o fricción para medir revisión aplicada.

  **Correcciones importantes:** CAR no exige outcomes sin juez; los admite, aunque recomienda outcomes programáticos. Su validación cuantitativa publicada es principalmente sobre estructuras causales sintéticas, no sobre una gran suite de agentes reales.

- **BACKTRACE / BackroomBench**

  Mantiene fijos tarea, modelo, prompt y decoding, y cambia únicamente un skill o su asignación. Después compara:
    - lo que el agente afirma haber utilizado;
    - aquello de lo que su decisión dependió causalmente.

  La correspondencia entre ambas puede ser muy baja, y detectores observacionales basados en menciones o similitud de trazas predicen mal la dependencia real.

  **Importancia para WAGER:** ofrece la formulación experimental más limpia de “fijar todo salvo una variable” y respalda medir lo incorporado desde la entrega, no desde la narración del agente.

  **Diferencia:** evalúa dependencia de skills en decisiones discretas, no revisión gradual de modelos.

- **LURE**

  Utiliza trayectorias como prefill y agrega una evaluación de forma natural al final, buscando reducir la conciencia de estar siendo evaluado.

  En sycophancy, el ranking cambia fuertemente frente a un benchmark sintético. Pero la formulación “los tests cortos mienten” es demasiado fuerte:
    - el `ρ=-0,88` aparece después de excluir un outlier;
    - el resultado bruto es `ρ=-0,56`, `p=0,09`;
    - la inversión de sycophancy usa conversaciones largas sintéticas generadas por Opus;
    - los replays de programación real pertenecen a otros experimentos del paper.

  **Importancia para WAGER:** convierte la fidelidad del snapshot en una amenaza experimental concreta. Hay que comparar continuación nativa, historial replayado y snapshot canónico.

  **Límite:** emplea jueces LLM y no puntúa una entrega contra verdad oculta.

## Trayectoria, compromiso y costo de revisión

- **Getting Out of the Big-Muddy**

  Manipula responsabilidad y escalada de compromiso en viñetas de inversión. El resultado central es más incómodo e interesante que “los modelos tienen sunk cost”:
    - bajo responsabilidad individual muestran poca escalada e incluso desinversión racional;
    - la escalada extrema aparece bajo deliberación entre pares;
    - también aparece bajo un bundle muy fuerte de identidad, reputación y presión personal.

  **Importancia para WAGER:** destruye la suposición de que autoría o esfuerzo previo necesariamente producen apego. Si WAGER encuentra un efecto de trayectoria sin presión social o identidad extrema, sería un resultado genuinamente nuevo. Si no aparece, no hay que rescatarlo agregando prompts antropomórficos.

- **MemSyco-Bench**

  Estudia cuándo un agente debe usar, limitar, actualizar o ignorar memorias previas. Muestra que una memoria obsoleta puede dominar evidencia nueva incluso cuando la corrección es recuperada.

  **Importancia para WAGER:** valida el conflicto memoria previa versus evidencia y la necesidad de incluir condiciones `REVISE` y `RETAIN`.

  **Diferencia esencial:** la memoria contiene creencias o preferencias del usuario. No es una teoría científica que el propio agente construyó. Debe quedar como vecino, no como competidor directo del eje de trabajo propio.

## Amenaza metodológica principal

- **Context Rot**

  Evalúa 18 modelos y aproximadamente 194.000 llamadas. Muestra que el rendimiento puede degradarse sólo por:
    - longitud total;
    - posición de la señal;
    - similitud semántica entre evidencia y relleno;
    - coherencia narrativa del contexto.

  **Importancia para WAGER:** puede explicar por completo un resultado CLEAN > MIXED sin necesidad de ninguna falla epistémica.

  Por eso WAGER necesita dos contrastes separados:
    1. **Misma evidencia diagnóstica con/sin filler:** mide costo de presentación y contexto.
    2. **Misma longitud y formato, distinta LLR esperada:** mide sensibilidad a dosis.

  Si se cambia simultáneamente cantidad de información, longitud y presentación, no puede afirmarse que “la misma evidencia fue ignorada por estar diluida”.

## Métrica complementaria, no núcleo

- **Martingale Score**

  Pregunta si la creencia previa predice su propio cambio posterior. Una relación positiva sugiere auto-refuerzo o atrincheramiento.

  **Importancia para WAGER:** la forma matemática `Δb ~ b_prior` puede convertirse en un chequeo secundario si `b` se obtiene directamente del modelo ejecutable.

  **Por qué no es una métrica inmediata:**
    - el paper obtiene `b` mediante un juez LLM;
    - las 252 ramas de WAGER reutilizan sólo 14 priors;
    - la evidencia fue seleccionada usando el modelo previo;
    - tratar los forks como observaciones independientes rompería la interpretación martingala.

  No es “gratis” sobre la pasada existente: requeriría una adaptación y una tanda diseñada específicamente.

## Antecedentes secundarios

- Belief-R: antecedente binario de actualizar versus mantener.
- DeltaLogic: ediciones mínimas que exigen cambiar, conservar o ignorar; corto y todavía pequeño.
- OAKS: adaptación a streams de hechos cambiantes; útil para subactualización y volatilidad.
- BeliefShift: intenta separar revisión causada por evidencia de deriva no justificada.
- Agentic Automata Learning: hipótesis formal ejecutable, queries y contraejemplos; eleva el estándar de baselines algorítmicos.
- BoxingGym: mundos generativos y model discovery, pero sin aislamiento causal de una revisión.
- HEP: registro explícito de hipótesis, evidencia y linaje; advierte que `REGISTER` también es una intervención.
- FutureSim: horizonte largo y forecasts revisables, pero sin forks apareados y con matcher LLM.

---

## Lectura final del panorama

Las piezas individuales ya están ocupadas:

- `cambiar / conservar / aislar ruido`: BeliefTrack;
- actualización proporcional multi-ronda: BayesBench, BASIL y Bayesian Teaching;
- agente largo con forecast verificable: Agentic Forecasting;
- modelo ejecutable contra verdad oculta: Autonomous Model Discovery;
- trabajo científico con grader determinista: GeneBench-Pro;
- replay contrafactual: Causal Agent Replay;
- dependencia dice–hace mediante intervención: BACKTRACE;
- reconocimiento sin aplicación: STALE y GeneBench-Pro;
- reparación explícita de dependencias: FCPAgent;
- context rot como confundidor: Chroma.

La pregunta que permanece abierta es más estrecha, pero también más interesante:

> **¿Cómo interactúan el valor probatorio de la evidencia, la exposición real a una trayectoria previa y el costo material de reparación para determinar la desviación entre la actualización legal y el modelo ejecutable finalmente entregado?**

Esa interacción —incluyendo cuándo alejarse, reforzar o conservar, y cuánto hacerlo— sigue sin estar cubierta. Ése es el centro publicable de WAGER.
