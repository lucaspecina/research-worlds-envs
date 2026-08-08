# Lecturas del programa de saltos — 4 papers a texto completo (2026-08-07)

> Cuatro lectores en paralelo, texto completo verificado, extracción con citas verbatim.
> Registro oficial: [lectura-de-fuentes](../lectura-de-fuentes.md). Este doc guarda el detalle.

---

## 1. KellyBench — arXiv 2604.27865 (Grady et al., General Reasoning Inc., 2026-04)

**Qué es.** Benchmark de decisión secuencial de horizonte largo: una temporada COMPLETA de la
Premier League 2023/24 (~120 matchdays), apuestas obligatorias por matchday, odds reales de
cierre (vig ~5.3%), sandbox con numpy/pandas/sklearn y red bloqueada, 500–1000 tool-calls por
episodio. **Reward denso cero-LLM** (log-wealth por matchday = criterio de Kelly) — llegaron a
nuestra misma decisión de diseño. 5 modelos × 5 seeds (GPT-5.4, Opus 4.6, GLM-5, Gemini 3.1
Pro, Kimi K2.5); 3 modelos más excluidos por no poder completar la temporada.

**Números.** Todos pierden EN PROMEDIO de 5 seeds: GPT-5.4 −7.9% (mejor) · Opus −11.2% ·
GLM-5 −51.6% · Gemini −66.0% · Kimi −89.6%. 3/25 seeds sueltos positivos (+34.1/+33.7/+21.5);
ruina 6/25. Humano cuant (2 años exp., 1 semana) +5.1%; el baseline Dixon-Coles de los 2000s
(−15.4%) le gana a 3/5 frontier. Driver principal declarado: el modelo predictivo pierde contra
el mercado (Δ log-loss positivo para todos) — la rigidez es uno de cinco clusters de falla.

**Lo que nos importa (adaptación / no-estacionariedad):**
- ⚠️ **NO hay switch inyectado a mitad de temporada** — la no-estacionariedad es la NATURAL del
  dominio (equipos recién ascendidos sin historia = shift declarado desde el día 1; el mercado
  ganando ventaja informacional sobre modelos congelados). Corrección a nuestro registro previo.
- 7/25 seeds **nunca reentrenaron** pese a datos frescos tras cada matchday; 22/25 sin manejo
  general de ascendidos ("No model implemented a general solution").
- **Adaptativos −11.1% vs estáticos −70.0%** (parciales −49.6%). El único seed de Gemini que
  reentrenaba a diario: +33.7%; sus cuatro hermanos estáticos: −91% promedio.
- **La firma fina es "knowledge-action gap"** (§4.4): diagnostican por escrito y no corrigen.
  GLM-5 escribió TRES documentos de autocrítica identificando la causa raíz de sus pérdidas y
  "translated none of these diagnoses into model corrections". Opus diagnosticaba el error de
  ascendidos e igual difería a su modelo. (= nuestro espécimen "outlier" de count_regime.)

**Citas.** "No model makes a return on average across 5 seeds. Models also fail to adapt
strategies in response to failure." (Fig. 1) · "models have poor adaptivity and low competence
in accounting for potential estimation error and non-stationarity" (§1) · "the market
progressively grew its information edge over the model" (§4.1.3) · "Models can write
sophisticated code, diagnose their own failures, and articulate correct strategies, yet
persistently fail to execute those strategies reliably, monitor their own performance, or adapt
when their approach is not working" (§5.2).

**Límites declarados.** Una sola temporada (n=1; "restricts us from making overly strong
conclusions"); mercado ultra-eficiente; solo single-agent; contaminación potencial (2023/24
pre-cutoff de todos) mitigada por instrucción+auditoría — y aun con esa ventaja pierden.

**Claim corregido para citar:** "temporada EPL simulada (500–1000 tool-calls, 5×5 seeds); todos
pierden en promedio (mejor: −7.9%; 3/25 seeds sueltos positivos, 6/25 ruina); 7/25 nunca
reentrena, 22/25 sin manejo del shift natural (ascendidos — no hay switch inyectado);
adaptativos −11.1% vs estáticos −70.0%; firma fina: knowledge-action gap (diagnostican por
escrito, no corrigen)".

**Estado: LEÍDO texto completo** (ar5iv, ~80K chars, con apéndices A–E; figuras solo por caption).

---

## 2. The Einstein Test — arXiv 2501.06948 (Benrimoh, Mikus & Rosenfeld, 2025-01)

**Qué es.** Position paper puro (cero experimentos, cero números): proponen el test de
re-descubrir breakthroughs (CDIs — "Creative and Disruptive Insights") desde el corpus
PRE-descubrimiento. Excluyen descubrimientos por azar (penicilina) y por búsqueda exhaustiva
(tabla periódica); restringen a física/matemática porque ahí la equivalencia formal es
demostrable. Protocolo de 6 pasos con comité: dataset curado sin NADA posterior al CDI →
entrenamiento verificado → preguntas motivadoras reconstruidas por historiadores SIN presuponer
la forma de la solución (ni que exista) → oráculo que solo entrega experimentos posibles con la
tecnología de la época y deniega los cost-prohibitivos → terminación: lo logró / afirma-y-está-mal /
declara imposible.

**Convergencias con WAGER** (es nuestro gemelo con historia real): corpus pre-verdad = mundo;
brief ciego escrito sin hints ("not even given an impression that there is a specific answer");
oráculo con presupuesto por época; el derecho a declarar "no hay respuesta" como anti-vicio del
solución-plantada; desconfianza del crédito parcial por parecido-al-camino (el progreso a un CDI
no es lineal) → anclar crédito en consecuencias observables.

**El punto estructural:** su test es INVIABLE con modelos off-the-shelf — exige pre-training
bespoke por CDI con auditoría de fugas de un corpus histórico completo (el modelo ya vio la
relatividad). Ese costo es el argumento más fuerte a favor de nuestro camino: **verdad sintética
nueva = misma estructura epistémica, contaminación imposible por construcción.**

**Citas.** "given the data available prior to the emergence of a known CDI, can an AI
independently reproduce that insight (or one that is formally equivalent)?" (abstract) · "it is
critical to allow an AI to be able to decide not to continue" · "no knowledge from the period of
time after the CDI is included in any of the training data" (paso 3).

**Límites.** Viewpoint de 3 autores sin implementación ni adopción; fallar el test no descarta
nada (asimetría de datos); "closeness" reconocido como problema abierto. Citar como convergencia
de diseño, no como evidencia.

**Estado: LEÍDO texto completo** (PDF oficial, 9 pp.; ar5iv no existe para este paper).

---

## 3. Can AI Follow in Einstein's Footsteps? — arXiv 2607.27794 (Shalyt, Regev, Soljačić, Kaminer, 2026-07)

**Qué es.** Perspective histórico-epistemológico (no empírico). Tesis: la IA-para-física se
vuelve extraordinariamente predictiva recorriendo la historia de la física EN ORDEN INVERSO
(hacia oráculos pre-científicos tipo AlphaFold), alejándose del modo que produjo los saltos.
Taxonomía de outputs A (solución/capacidad) / B (ecuación/ley) / C (marco matemático/principio
de simetría). "Strikingly, no AI has made a discovery of Category C."

**Verificación de nuestra anotación:** FIEL con tres matices — dice "MANY great leaps… were
neither inductive nor deductive" (muchos, no todos); "the primary bottleneck is not JUST
producing a novel creative idea"; el término primario es "gut feeling" ("scientific taste" es
componente).

**Los tres regalos:**
1. **"Symmetry abduction" con nombre** (§6): los métodos existentes usan la simetría como
   CONSTRAINT para ajustar; falta proponerla como PRINCIPIO GENERADOR — exactamente nuestro
   operador 6 ("promover el invariante a axioma"), declarado "the crucial step". El box §4
   abstrae la estructura de 4 casos reales (Laughlin, Bethe, Ginzburg-Landau, Parisi): "impose
   an additional structured hypothesis (ansatz, symmetry, gauge) — enforcing simplicity before
   deducing falsifiable consequences".
2. **El taste como SELECCIÓN, no generación**: "Novelty is cheap in a sufficiently large search
   space. The harder task is estimating the scientific payoff of each novel idea… a
   payoff-per-effort ratio". Y es tácito: "only rarely written down as a procedure, current AI
   systems have little direct training data for it". → Implicación para WAGER: los mundos deben
   cobrar también la mala SELECCIÓN de saltos, no solo la incapacidad de producirlos.
3. **Endoso textual de nuestra metodología** (box §6): "We can give AI systems artificial
   worlds with hidden laws and test whether they can invent simple theories inside those
   worlds" — con "Machina Mirabilis" y el "1911 cutoff" de Hassabis como comparables a fichar.

**Bonus para revisión de creencias:** "Revolutionary work, by definition, looks wrong from
inside the consensus until it changes that consensus. LLMs are optimized to do the exact
opposite: notice when the field disagrees and update toward the center." (§6, sobre RLHF).
Propuesta §7: "Reverse ITP" — axiomas provisionales + contradicción como señal de loss.

**Límites.** Perspective sin evidencia empírica propia; taxonomía A/B/C declaradamente borrosa;
caveat de Wigner (donde las escalas no separan, quizá no HAY teoría elegante); quizá el cuello
sea la física, no la IA.

**Estado: LEÍDO texto completo** (ar5iv completo: §1–7, 3 boxes, 126 refs; un footnote no
renderizado, irrelevante).

---

## 4. Gentner, "Analogy" — Open Encyclopedia of Cognitive Science, MIT Press, 2025

**Qué es.** La entrada enciclopédica autoritativa (8 pp., DOI 10.21428/e2759450.fed73a94)
escrita por la creadora de structure-mapping — el resumen canónico de ~45 años del programa,
con consenso del campo declarado.

**El núcleo.** Analogía = "a kind of similarity in which the same system of relations holds
across different sets of elements, regardless of whether the elements are similar"; los objetos
se corresponden POR SU ROL en la estructura relacional común, no por parecido. **Systematicity**:
se prefieren sistemas conectados por relaciones de orden superior (causales/matemáticas) sobre
relaciones sueltas. La transferencia va en 3 etapas: retrieval → mapping → evaluation, y las
inferencias se proyectan por COMPLETACIÓN estructural (el "transplante de la hipótesis" de
Darwin ES la candidate inference de la teoría).

**El dato que fundamenta nuestro gemelo (analogía falsa):** el retrieval espontáneo está
dominado por la SUPERFICIE — "People mostly failed to retrieve relationally similar cases…
instead, people tended to retrieve cases that were surface-similar" (la línea Gick & Holyoak/
Ross/Novick); Trench & Minervino 2015 con memoria natural (películas): **70% recupera con alta
similitud superficial vs 30% sin ella**. Matiz obligatorio de diseño: en la vida real superficie
y estructura CORRELACIONAN — el mundo del gemelo debe **descorrelacionarlas deliberadamente**
(objetos parecidos que NO se corresponden por rol). Moderador medible: la expertise mejora el
retrieval puramente relacional.

**Criterios computables de transferencia válida** (sección Evaluation): (1) consistencia
estructural (correspondencias 1-a-1 + conectividad paralela), (2) sistematicidad, (3)
no-contradicción con lo conocido del target — el check que la analogía falsa saltea —, (4)
relevancia al goal. Y crucial: la analogía es INDUCTIVA — evalúa buena formación del mapeo, no
verdad; **el aha legítimo termina en verificación en el target, no en el mapeo**. Existe
implementación cero-LLM de estos criterios: el **Structure-Mapping Engine** (Falkenhainer 1989;
Forbus 2017) — compatible con nuestro reward path.

**Sobre LLMs:** Webb et al. 2023 (GPT-3 rinde bien → "emergent analogy") vs **Lewis & Mitchell
2024**: en problemas FUERA del training data los GPT quedan "substantially worse than humans…
undermining the claim that GPT can do true analogical reasoning". El único estándar que el campo
aceptó como discriminante = held-out/contaminación — nuestro estándar.

**Estado: LEÍDO texto completo** (PDF oficial export MIT Press; solo la lista alfabética de
referencias del PDF está truncada, no el cuerpo).

---

## Nivel arriba (las 4 juntas)

- **Aprendizaje real:** el programa quedó apuntalado por afuera en sus tres patas — metodología
  (Footsteps endosa mundos-con-leyes-ocultas; Einstein Test converge en corpus-pre-verdad +
  brief ciego y es inviable sin verdad sintética), operadores (symmetry abduction nombrado como
  EL paso faltante; los criterios de Gentner operacionalizan el salto 11 y su gemelo con
  maquinaria cero-LLM existente), y fenómeno (KellyBench: knowledge-action gap = nuestra familia
  "outlier", medida afuera a escala).
- **Correcciones aplicadas:** KellyBench no tiene switch inyectado (no-estacionariedad natural)
  y su rigidez no es uniforme (adaptativos −11% vs estáticos −70%); Footsteps dice "many" no
  "all", y el cuello es "not JUST" generar.
- **Nueva idea de vara (de Footsteps):** cobrar la SELECCIÓN de saltos (payoff-per-effort), no
  solo la generación — "novelty is cheap".
- **Deuda que sigue viva:** los clásicos-libro (Boden, Ohlsson, Nersessian, Darden, Klahr &
  Dunbar) no son accesibles online — siguen como biblioteca curada sin fichar.

---

## 5. Schurz, "Patterns of Abduction" — Synthese 164 (2008), 201–234

**Qué es.** LA taxonomía sistemática de la abducción: no una regla general (IBE) sino
**patrones específicos** cuya estructura determina la conjetura prometedora; su función
esencial es ESTRATÉGICA (búsqueda en un espacio exponencial). Clasifica por tres dimensiones:
qué se abduce (hecho / ley / modelo teórico / concepto nuevo), qué evidencia lo pide, y qué
mecanismo lo impulsa (leyes conocidas / extrapolación / analogía / unificación pura).

**La taxonomía**: factual (con sub-formas: hecho observable · **existencial de primer orden**
[postular individuos nuevos: la huella en la playa] · hecho histórico inobservable) ·
**law-abduction** (el "middle term" de Aristóteles) · **theoretical-model** (ciencia normal:
derivar el fenómeno desde una teoría dada) · **existencial de segundo orden** (concepto NUEVO:
micro-partes · **analógica** [mapping à la Gentner + abstracción conceptual] · **causa común
hipotética**). La divisoria normativa: postular UNA entidad para UN fenómeno = **abducción
especulativa** (ad hoc, virtus dormitiva — su ANTI-PATRÓN); solo la causa común que unifica
MUCHOS fenómenos intercorrelacionados independientes es legítima — criterio **(CU)**, con
reducción contable **n·m leyes empíricas → n+m teóricas**.

**Selectiva vs creativa (Magnani, la distinción organizadora):** *"abductions which introduce
new concepts or models [are] creative, in contrast to selective abductions whose task is to
choose the best candidate among a given multitude"*. Y la asimetría de dificultad (Result 3):
*"In selective abductions, the difficulty usually lies in the fact that the search space… is
astronomically large. In creative abductions, however, the difficulty often consists in finding
just ONE conjecture which meets the required constraints."* — nuestro hallazgo (menú que no
crece) en idioma filosófico.

**LA TABLA DE ALINEACIÓN (operador nuestro ↔ tipo de Schurz):**

| Operador | Schurz | Ajuste |
|---|---|---|
| 1 entidad oculta | existencial de 1er orden (+ theoretical-model al cuantificar) | alto |
| 2 grupos escondidos | causa común estricta / factor analysis discreto | medio |
| 3 régimen · 4 geometría · 6 invariante · 7 observador · 8 feedback · 9 conservación · 10 memoria | **SIN correlato** (los agrupa indistintos bajo theoretical-model / 2º orden) | — |
| 5 unificación | **causa común — correlato EXACTO** (Newton es SU ejemplo) | exacto |
| 11 transferencia | **abducción analógica — correlato EXACTO** | exacto |

**Lectura de la tabla:** las taxonomías son mayormente ORTOGONALES — Schurz clasifica el tipo
EPISTÉMICO de lo abducido; nosotros la EDICIÓN ESTRUCTURAL al programa. Donde se cruzan,
coincidimos exacto (5, 11); en 7 de 11 operadores nuestro grano es más fino que el suyo. La
lista nuestra queda: anclada donde hay ancla, más fina donde no la hay — no huérfana.

**Regalos operativos:** (a) tipos de Schurz sin operador nuestro = candidatos a la matriz
(evento pasado oculto · mediador conocido interpuesto · descomposición en micro-nivel · latente
continuo); (b) la **abducción especulativa** como anti-patrón con demarcación (CU) contable
**cero-LLM** (¿cuántos fenómenos independientes unifica la entidad postulada?) — candidata a
certificado/vara del gemelo; (c) su paper posterior "Abductive Belief Revision in Science"
(2011, PDF accesible) conecta NUESTRAS DOS LÍNEAS — próxima lectura natural.

**Límites.** Sin patrón general para theoretical-model (donde viven la mayoría de nuestros
operadores); (R) falla en cuántica (él lo admite); esquemas cualitativos sin dinámica temporal
ni feedback ni observador; teoriza la operación exitosa, no las fallas (salvo la especulativa).

**Estado: LEÍDO completo** (34/34 pp., PDF oficial enlazado por el propio Schurz desde su
página de HHU Düsseldorf).

---

## 6. Dunbar (1995), "How Scientists Really Reason" (+ Dunbar 1997) — el estudio in vivo

**Qué es.** El primer estudio cognitivo de científicos reales trabajando: Dunbar pasó UN AÑO
dentro de 4 laboratorios de élite de biología molecular (estudió biología 5 años para poder
hacerlo), grabando las reuniones de lab y entrevistando antes/después, siguiendo proyectos
desde su inicio — capturó descubrimientos EN VIVO ("I have the moment of discovery on tape").
Leídos completos el capítulo 1995 (manuscrito del autor, 19 pp.) y el paper hermano 1997 (que
consolida los números preliminares).

**Hallazgos que nos reordenan:**

1. **El mito de la analogía lejana MUERE con datos**: 99 analogías en 16 reuniones — solo 2
   fueron de dominio lejano, y **CERO produjeron descubrimientos** ("we did not find one
   instance of a case where a long-distance analogy led to any conceptual changes"). Las que
   descubren son LOCALES y REGIONALES (dominios hermanos), hechas por expertos, y las
   regionales solo aparecen DESPUÉS de que el científico construyó su modelo del dominio.
2. **El cambio conceptual real del corpus fue… nuestra operación 2**: partir un mecanismo
   unitario en dos (entrada al órgano ≠ inicio de la enfermedad), empujado por una anomalía
   creída-real + desafío grupal. "Conceptual change, like evolutionary change, is the result
   of tinkering" — cirugía estructural local, no salto romántico.
3. **El individuo solo = nuestros agentes**: "individual scientists out of a group context
   usually attributed inconsistent evidence to error of some sort, and hoped that the finding
   would go away". El comportamiento de nuestros agentes ("es un outlier", "es ruido") ES el
   default humano individual documentado; el mecanismo corrector real es SOCIAL (el meeting
   que diseca la anomalía, las preguntas que cambian de nivel).
4. **El gate absoluto es la creencia sobre error**: si el investigador cree que la anomalía es
   error, NINGÚN desafío produce cambio ("no amount of challenging… will result in conceptual
   change"). → Diseño: la RÉPLICA debe ser comprable; la firma fina cero-LLM es
   descartar-sin-replicar vs replicar-persiste-y-descartar-igual (peor) vs replicar-y-perseguir.
5. **El borde triage/vicio que necesitábamos**: anomalía TEMPRANA sobre supuesto AUXILIAR se
   ignora — y es triage sano (los de élite lo hacen); tardía o nuclear se atiende siempre. El
   vicio es descartar la tardía/replicada/nuclear. (Cruce momento × centralidad = knob de mundo.)
6. **La serendipia está diseñada**: los descubrimientos del corpus nacieron de CONTROLES que
   dieron raro — los controles se diseñan también "to expose novel mechanisms, should they be
   there". → Mundos fieles: la firma oculta asoma en el canal de chequeo, no donde el agente
   mira; y "¿compró controles? ¿qué hizo cuando dieron raro?" es puntuable de traza.
7. **El polo espejo existe en expertos**: "falsification bias" — los muy experimentados
   descartan datos BUENOS que confirman su hipótesis. Bipolar, como nuestra doctrina de pares.
8. **Jamás medir del autorrelato**: el postdoc del descubrimiento, re-entrevistado a la semana
   y a los meses, NUNCA recordó las analogías ni el razonamiento distribuido de su propio
   descubrimiento — solo la cinta lo preservó. (= nuestra doctrina de leer trazas, no resúmenes.)
9. Dato de tasa base: en 70 condiciones experimentales de un lab, 18 inesperadas + 30
   exploratorias vs 22 esperadas — lo inesperado es lo NORMAL; y los buenos labs le dedican
   176 interacciones vs 23 a lo esperado.

**Citas clave.** "when (i) surprising findings occur, (ii) the researcher believes that these
findings are not due to error, and (iii) other members of the group challenge the researcher's
interpretation…, significant conceptual change will occur" · "The so-called serendipitous
findings are the result of careful experimentation and planning that are designed to expose
novel mechanisms."

**Límites.** n=4 laboratorios de élite, un campo, un año, un observador; números 1995
preliminares (el 1997 consolida); heurísticas extraídas, no causalidad probada.

**Estado: LEÍDO completo** (manuscrito 1995 del autor vía Wayback del Dunbar Lab + 1997 completo;
citas del manuscrito, pueden diferir en detalle menor de la versión impresa MIT Press).

---

## 7. Klahr & Dunbar (1988), "Dual Space Search During Scientific Reasoning" — Cognitive Science 12(1)

**Qué es.** El clásico fundacional: descubrir = buscar COORDINADAMENTE en dos espacios — el de
hipótesis y el de experimentos (marco SDDS). Paradigma BigTrak: 20+10 sujetos descubren qué
hace la tecla RPT de un robot programable (la regla verdadera es contraintuitiva: N no cuenta
repeticiones, SELECCIONA un segmento — nadie arrancó con ella). Leído completo (48/48 pp., PDF
oficial de CMU).

**El modelo, en lo que nos toca:** el espacio de hipótesis está organizado en FRAMES (marcos);
cambiar de hipótesis dentro del frame es barato (tocar un slot); **cambiar DE frame es el
insight** ("Insight… is the instantiation of a new frame — this is what is meant by a
restructuring of the representation"). GENERATE FRAME tiene exactamente dos vías: **EVOKE**
(recuperarlo de la memoria/prior) o **INDUCE** (leerlo del patrón de resultados). Y la
generación de experimentos vive en OTRO módulo (E-SPACE MOVE) — **la disociación que medimos
(compran bien el experimento discriminante, no les nace el candidato) es estructural en el
modelo de 1988.**

**Los números humanos:** 19/20 descubren la regla (el mundo era generoso: existe una región del
espacio de experimentos cuyo resultado EXHIBE la regla a la vista). Tras desconfirmación,
retienen la hipótesis desconfirmada el **56%** de las veces. Dos perfiles: **Theorists** (7/20:
cambian de frame consultando la memoria bajo una restricción abstraída de la evidencia — "la
unidad de repetición es variable ⇒ ningún counter sirve") y **Experimenters** (13/20: agotado
el frame, entran en modo SIN hipótesis ~6 experimentos, caen en la región discriminante, y el
patrón les dicta el frame). La diferencia es CONOCIMIENTO PREVIO, no un rasgo.

**Los tres regalos para WAGER:**
1. **"La evidencia comprada bajo el frame equivocado puede INHIBIR el cambio de frame"**
   (verbatim: "the information gathered from the exploration of the experiment space may have
   inhibited subjects from switching") — el frame activo fija QUÉ atributos se miran; los datos
   se codifican en el vocabulario del frame vigente. Nuestra descripción exacta, publicada en
   1988.
2. **La vía de escape que nuestros agentes NUNCA usan**: el modo ateórico ("it was permissible
   to replace something with nothing" — quedarse SIN hipótesis y explorar). Nuestros agentes
   siempre tienen un candidato → jamás entran al modo que en SDDS es la salida cuando la
   memoria no da el frame. Hipótesis mecanística nueva para el fenómeno.
3. **La conexión causal de nuestras dos líneas**: la retención de hipótesis desconfirmadas se
   explica por la INCAPACIDAD DE GENERAR LA ALTERNATIVA (modo reemplazo de Einhorn & Hogarth:
   no se suelta una explicación sin tener otra). El no-nace-el-candidato (saltos) es causa
   documentada del no-revisa (creencias). No son dos fenómenos.

**Intervenciones que funcionaron (baratas, pre-registrables para nuestros mundos):** enumerar
hipótesis EN FRÍO antes de experimentar (Study 2: tiempo −68%, revisión tras desconfirmación
44%→85%, y aparece el diseño discriminante entre pares — 5/10 humanos produjeron la regla
correcta con CERO datos); el prompt de redescripción ("¿qué tienen en común todas las
desconfirmaciones?").

**Matiz anti-sobre-lectura:** en su mundo, el resultado discriminante llevaba la regla escrita
encima (ves los últimos N pasos repetirse) — la disociación dura (discriminante comprado +
inducción fallida) casi no ocurre en sus datos porque el puente era gratis. Nuestros mundos
miden EXACTAMENTE el hueco que ellos predicen y no cuantificaron.

**Estado: LEÍDO completo** (48/48 pp., tablas y figuras incluidas).

---

## 8. Nersessian (1992), "How Do Scientists Think?" — el cambio conceptual como PROCESO

**Qué es.** El paper canónico del análisis cognitivo-histórico: el cambio conceptual radical NO
es un reemplazo súbito ("gestalt switch" kuhniano) sino un **proceso extendido de construcción
de modelos intermedios** — analógicos, imagísticos, experimentos mentales, casos límite. El
error de Kuhn: comparar solo los EXTREMOS (Newton vs relatividad) hace parecer abrupto lo que
fue una cadena. "We need to give up the notion that 'creativity' is an *act* and try to fathom
it as a *process*."

**El caso Maxwell (el corazón):** para las ecuaciones del electromagnetismo construyó un modelo
mecánico de vórtices que FALLABA (vórtices vecinos se frenan) → lo parchó con "idle wheels"
(ruedas locas contrarrotantes) = **un híbrido que él mismo declaraba inexistente en la
naturaleza** — y desde ese andamio falso-a-sabiendas extrajo una estructura matemática MÁS
general que la newtoniana. Meses después ("Aha! now I know how to do it without the model")
**rederivó las ecuaciones SIN el modelo** — el aha no es el momento de creación: es el momento
de **soltar el andamio**. Firma fina: sus errores (el signo del displacement current) eran
CORRECTOS en términos del modelo intermedio — prueba de que razonaba A TRAVÉS del modelo.

**Implicación dura para nuestra vara: el binario salta/no-salta es el error de los endpoints.**
- Medir solo el veredicto final = el error que ella le imputa a Kuhn. La unidad observable
  debería ser la **cadena**: fuente cruda → fuente enriquecida → esquema → descarte del andamio.
- Un agente que arma un HÍBRIDO (maquinaria vieja + entidad ad hoc para satisfacer una
  restricción nueva) está A MITAD del camino correcto, no "fallando" — y el salto completo
  tiene firma final específica: **sostener la conclusión sin el andamio**.
- Firma cero-LLM candidata: errores sistemáticos COHERENTES con el modelo intermedio =
  razonamiento-a-través-del-modelo (vs decoración post hoc).
- Advertencia para como-medimos: comparar estado inicial vs final "VE" saltos de gestalt
  espurios — es un modo de fallo del INSTRUMENTO, no del agente.

**Condiciones de diseño que su análisis exige** (checklist para mundos de salto): (1) un
dominio FUENTE con estructura propia disponible al agente (sin fuente análoga, el salto es
imposible por diseño); (2) restricciones EXPLÍCITAS y suficientes del destino (pocas → la
analogía se vuelve "too generative": sobre-importa — firma medible del gemelo); (3)
**tolerancia a la falsedad provisoria**: un scoring que cobra caro cada postulación intermedia
MATA el mecanismo — solo la adecuación final debe cobrar; (4) iteración/persistencia (episodios
de un turno no pueden materializar el fenómeno; a Maxwell le llevó meses); (5) nivel intermedio
de abstracción disponible (diagramas/representaciones externas); (6) casos límite: extrapolación
controlada con camino de vuelta.

**Estado: LEÍDO completo** (42/42 pp., PDF escaneado del sitio de la autora en Georgia Tech,
leído como imagen — citas transcriptas a mano). El capítulo de 1999 (candidato original) está
paywalled; el de 1992 es más rico para nuestro uso.

---

## 9. Kemp & Tenenbaum (PNAS 2008) + Ullman, Goodman & Tenenbaum (2012) — el fundamento formal

**Qué son.** El par formal de la ciencia cognitiva computacional. **Kemp 2008**: descubrir la
FORMA de un dominio (¿árbol? ¿anillo? ¿cadena? ¿grilla?) como inferencia bayesiana sobre
gramáticas de grafos — recupera el árbol de Linneo, el círculo cromático de Newton, la cadena
liberal-conservador de la Corte, y reproduce el shift infantil partition→tree como efecto puro
de cantidad de datos. **Ullman 2012**: las teorías SON programas (cláusulas de Horn) y aprender
es **búsqueda estocástica (MCMC) sobre EDICIONES del programa** — agregar/borrar/cambiar
predicado, instanciar template, agregar/borrar ley — con el problema huevo-gallina de los
conceptos nuevos RESUELTO: la ley nueva introduce un predicado EN BLANCO y el loop interno le
busca significado ("the novel concepts that began as blank symbols f and g… have now
effectively become what we call 'magnets'").

**El veredicto de formalidad para nuestra taxonomía (la tabla completa está arriba en el
informe del lector; resumen):**
- Nuestra premisa ("descubrir = editar la estructura del programa generativo") tiene acá su
  fundamento formal EXACTO, publicado — incluida la legitimidad de "agregar variable latente"
  (el predicado en blanco + grounding).
- De nuestros 11 operadores, sus espacios cubren sólido **2** (latente, partir-en-tipos) y
  parcial **3** (invariante, unificar, transferir). **Los 6 dinámicos/mecanísticos nuestros
  (régimen, feedback, memoria, observador, reparametrizar, cuantizar) NO EXISTEN en ninguno de
  los dos espacios** — y Ullman nombra la extensión necesaria: "a functional language, in which
  the laws are more similar to mathematical equations… much more expressive". **Nuestra
  taxonomía es la lista de clases de edición que ese lenguaje funcional necesita** — no está
  "ya publicada": está un nivel de expresividad más allá, con linaje nombrado.
- Rival de diseño a discutir: que nuestros operadores sean COMPOSICIONES de sus primitivas en
  un lenguaje más rico ("agregar régimen" = latente + ley condicional) — derivados, no
  primitivos. Discusión de diseño, no de lectura.

**Dos regalos extra:** (1) la Fig. 8 de Ullman es un **modelo formal de la revisión kuhniana
por anomalías acumuladas**: la teoría simple absorbe las excepciones **como outliers** hasta
que el costo las vuelve insostenibles y fuerza el salto — la mecánica exacta de nuestros
agentes ("es un outlier"), modelada; (2) firma de traza medible: la búsqueda estructural real
tiene MESETAS + SALTOS DISCRETOS individuales (que se ven suaves en promedio — advertencia
contra promediar corridas).

**Estado: LEÍDOS completos** (Kemp: paper + SI de 10 pp; Ullman: preprint de autor 47 pp).

---

## Nivel arriba de TODA la campaña (9 fuentes a texto completo en un día)

1. **La formalidad de la taxonomía quedó resuelta con el mejor veredicto posible**: marco con
   linaje formal exacto (Tenenbaum ×2), alineación fina con la taxonomía filosófica de
   abducciones (Schurz: exacta donde se cruzan, más fina en 7/11), y "un nivel de expresividad
   más allá de lo publicado" en los 6 operadores dinámicos. Ni huérfana ni ya-hecha. Falta:
   Darden/Thagard/Boden/Ohlsson (LIBROS — pedir PDFs).
2. **Doctrina de diseño nueva que sale de Dunbar + Nersessian + Klahr&Dunbar** (para las
   próximas fichas): medir la CADENA de modelos, no el veredicto final (híbridos = estado
   intermedio productivo; el aha = soltar el andamio); scoring que NO cobre la postulación
   provisoria (solo la adecuación final); réplica comprable (el gate es la creencia-sobre-error);
   la firma oculta asomando en CONTROLES; cruce momento×centralidad de la anomalía (triage vs
   vicio); sonda barata de enumeración-en-frío; y el modo sin-hipótesis como vía de escape
   (que los agentes nunca usan).
3. **Nuestras dos líneas son UNA en la literatura**: no-generar-la-alternativa causa
   no-revisar (Einhorn&Hogarth vía K&D), la acumulación de "outliers" fuerza el salto kuhniano
   (Ullman Fig. 8), y Aliseda (POR-LEER) las une desde la lógica.
4. **El mito muere**: la analogía lejana romántica NO produce descubrimientos (Dunbar 2/99,
   cero causales); el cambio real es tinkering local — partir mecanismos, híbridos, controles
   que dan raro. Nuestros mundos de "cirugía estructural local" miden el fenómeno real, no el
   mito.

---

## 10. Schmidhuber (2010), "Formal Theory of Creativity, Fun, and Intrinsic Motivation" — IEEE TAMD

**Qué es.** LA teoría matemática de la creatividad: la recompensa intrínseca (el "fun", la
curiosidad, el interés) = **el PROGRESO DE COMPRESIÓN** — la derivada de cuántos bits necesita
tu modelo para codificar la historia completa, cuando el modelo mejora. Ni lo ya-comprimido
(aburre) ni el ruido incompresible (aburre): lo interesante es la franja aprendible. Un
**descubrimiento** = "an unusually large compression breakthrough" (Newton: un programa corto
que comprime milenios de manzanas cayendo — SIN anomalía; las manzanas caían predeciblemente).

**Los tres veredictos para nosotros:**

1. **La crítica de can't-jump queda partida en dos, con precisión**: NO refuta la VARA (bajo
   MDL de dos partes, el salto es rentable sin señal de error — el ejemplo de π: cero anomalía
   estadística, ningún residuo explotable, y sin embargo existe el programa corto); SÍ aplica
   al MECANISMO — Schmidhuber mismo concede casi textual que un aprendedor limitado "will get
   discouraged from spending too much effort" en patrones fuera de su clase (sin gradiente
   hacia el salto). **Nuestra arquitectura usa exactamente la mitad que sobrevive: MDL para
   PUNTUAR, no para entrenar.**
2. **Nuestro escenario canónico cae del lado correcto de su distinción**: bajo error cuadrático
   (la medida ingenua que él descarta), el unimodal-que-ajusta-bien NO es castigado; bajo su
   medida oficial (C_l, código sin pérdida de la historia completa) SÍ — la densidad unimodal
   sobre datos bimodales gasta bits de más, la mezcla los ahorra tras pagar su descripción.
   Descubrir la mezcla ES un evento de progreso de compresión, en bits, computable, cero-LLM.
3. **Tres disciplinas para importar a la vara**: (a) ambos modelos evaluados sobre la MISMA
   historia completa; (b) código de DOS partes — los bits del modelo se cobran siempre
   (anti-parche estructural: el Vulcano paga sus polígonos); (c) el umbral "unusually large"
   para separar descubrimiento de micro-mejora — sin fórmula en el paper, lo fijamos nosotros
   contra la distribución de progresos. Bonus: EURISKO se estancó por "interesante" hardcodeado
   → refuerza nuestra regla de cero jueces de interés en el reward.

**Límites.** Teoría + implementaciones de juguete pre-2010; define QUÉ recompensar, no CÓMO
encontrar el salto (las instancias óptimas son incomputables); neutralidad de contenido (un bit
de empapelado = un bit de física — la relevancia entra solo por reward externo); amplitud
post-hoc (explica ciencia, arte, humor y consciencia — falsabilidad discutible).

**Estado: LEÍDO completo** (draft del autor de 18 pp. que él mismo enlaza como el paper
canónico; §I–VIII con ecuaciones y las 120 referencias).

---

## 11. Knoblich, Ohlsson, Haider & Rhenius (1999) — la teoría experimental del insight

**Qué es.** LA operacionalización experimental del insight (teoría del cambio representacional
de Ohlsson): el insight NO es magia — es la resolución de un IMPASSE mediante un cambio de
representación. Dos mecanismos: **relajar restricciones auto-impuestas** (heredadas de la
experiencia previa, no de la tarea) y **descomponer chunks** (patrones perceptuales
automáticos). Paradigma: aritmética de fósforos con numerales romanos donde respetar la
aritmética escolar hace el problema INSOLUBLE. Predicciones cuantitativas confirmadas en 4
experimentos (N=170): la dificultad ordena por el ALCANCE de la restricción a relajar (ajustar
un valor < cambiar el operador < admitir una forma "prohibida" de ecuación — 95% vs 78% vs 45%
de solución) y por la APRETADEZ del chunk; el orden predicho no se violó NUNCA; lo difícil
transfiere más; la similitud superficial no importa (p=.79).

**EL HALLAZGO CENTRAL PARA NOSOTROS — sin impasse no hay reestructuración, y es inequívoco:**
el gatillo de ambos mecanismos es el **fracaso persistente** ("one of the mind's responses to
persistent failure" — no es deliberado ni voluntario). Su paradigma garantiza el fracaso: (i)
el estado es VISIBLEMENTE falso (la ecuación no cierra — detector de verdad barato e
inequívoco); (ii) el espacio inicial NO contiene solución (éxito espurio imposible). **Nuestros
mundos violan las dos**: un modelo mal especificado puede ajustar bien — la "ecuación falsa"
del agente nunca se ve falsa. La teoría predice entonces EXACTAMENTE nuestro fenómeno:
**fluidez sin reestructuración** — el agente no salta no porque no pueda, sino porque nada
dispara el salto.

**Implicaciones de diseño (las más accionables de toda la campaña):**
1. **El impasse se ingenia desde el mundo**: hacer que la familia default falle de forma
   persistente, VISIBLE y barata de verificar (colapso en held-out comprable, intervenciones
   que contradicen el modelo ajustado, estructura residual que reaparece) — el análogo de "la
   ecuación sigue siendo falsa". Palanca #1 para la versión escondida del mundo 2 y para todo
   mundo de creatividad futuro.
2. **La reestructuración NO obedece instrucciones** — "promptear creatividad" no es el
   mecanismo (¡coincide con nuestro nivel4b-teatro!); crear condiciones de fracaso sí. Y el
   curriculum del Exp 3 explica nuestro nivel3: mostrar UNA VEZ que la forma "prohibida" es
   admisible relaja la restricción de una vez y para siempre — selectivamente (cura la
   restricción, no el chunk).
3. **Dos perillas ortogonales de mundo**: alcance del supuesto a abandonar (parámetro <
   likelihood < qué-cuenta-como-modelo — ordenamiento pre-registrable de dificultad entre
   operadores) × granularidad de los observables (agregados = chunks apretados; series crudas
   = sueltos).
4. **Predicción falsable para el programa**: si un agente reestructura SIN señal de fracaso, o
   no reestructura CON fracaso persistente y visible, el gatillo de la teoría está mal para
   este sustrato — ambas salidas informan.

**Estándar metodológico**: su vara para que "insight" no sea etiqueta post hoc — ordenamiento
de dificultad pre-registrado por tipo + firma de transfer diferencial — es medible sin LLM
(tasas y tiempos por tipo y bloque). El estándar que nuestra matriz saltos×realismo necesita.

**Límites.** Micro-dominio único (un movimiento, solución única, señal binaria de verdad);
claims solo ordinales; sin modelo computacional; el impasse se infiere de tiempos (la evidencia
ocular es del companion 2001, POR-LEER); erratas direccionales en p. 1546 del impreso
(resueltas contra tablas).

**Estado: LEÍDO completo** (22/22 pp., PDF de uni-koeln.de, con las 13 tablas y 9 figuras).

## Addendum al Nivel arriba de la campaña (cerrada con 11 fuentes)

**La tensión productiva que ordena todo el programa:** Ohlsson dice "sin impasse no hay
reestructuración" (explica nuestro 0/9: la familia default nunca falla VISIBLEMENTE) y
prescribe ingeniar el impasse; can't-jump/Schmidhuber muestran que los saltos supremos ocurren
SIN señal de error (el techo impuntuable). No se contradicen: **definen los dos extremos de
nuestra escalera** — "cuánta señal de fracaso hace falta para que el agente compre el salto"
es LA variable del programa, con Ohlsson explicando por qué el peldaño de señal-cero es casi
imposible (para humanos también) y Dunbar agregando el gate intermedio (la señal tiene que ser
CREÍDA — réplica comprable). La doctrina de diseño consolidada: ingeniar el impasse + medir la
cadena (Nersessian) + réplica comprable (Dunbar) + vara de compresión de dos partes
(Schmidhuber) + transfer diferencial como estándar (Knoblich/Ohlsson).

---

## 12. Darden — 5 textos a texto completo (1987 · 1994 · 1998 · MDC 2000 · 2002)

**Qué es.** La fuente más cercana a nuestra lista buscada: estrategias de cambio de teoría
extraídas de casos históricos REALES (genética 1900-1930 + 5 meses de observación en el
laboratorio de Lederberg + biología molecular). Su marco de tres categorías: estrategias para
**producir ideas** (analogía, abstracción→instanciación, tipos de teoría, relaciones entre
campos) · para **evaluar** (test de predicciones; la escalera how-possibly→plausibly→actually)
· para **resolver anomalías** (el corazón). Y un principio arquitectónico que nos habla directo:
*"Given a good revision procedure, one's discovery methods can be weaker."*

**Su pipeline de resolución de anomalías (6 pasos)** con las estrategias finas: confirmar la
anomalía ANTES de rediseñar (¿es problema de datos?) → **exprimir la firma de la anomalía para
elegir DÓNDE editar** (predicho 1:2:1, observado 2:1 → los AA faltantes DEBEN aparecer en el
rediseño; una anomalía 1:0:1 pediría OTRA edición) → localización modular exhaustiva (cada paso
puede fallar antes/en/después) → rediseño (tweak paramétrico vs fix estructural con biblioteca
de procesos genéricos) → test → repertorio explicativo indexado por tipo de anomalía para
reuso. Más: el **systematic scan** de Lederberg (generar el espacio de alternativas con ejes
ortogonales ANTES de comprometerse — el antídoto explícito contra fijarse temprano) y el
protocolo de **12 transformaciones** (negá cada supuesto / sustituí variable / insertá cláusula
— 4 oraciones × 3 = 12 candidatas casi mecánicas, visto EN VIVO en el lab).

**La tipología de anomalías (libro 2006, Intro leída):** **monster** (se excluye del dominio
sin cambiar la teoría) · **model** (exige exemplar nuevo de alcance amplio) · **special-case**
(exemplar para una subclase — reverse transcriptase). Con el veredicto histórico: linkage y
reverse transcriptase NO podían ser monsters. → El "monster-barring ilegítimo" es la firma
precisa de nuestro vicio de no-revisión, con casos reales etiquetables.

**LA ALINEACIÓN (el careo "¿inventamos o curamos?"):**
- Coincidencias fuertes: postular etapa/entidad no representada = **op 1**; ¡su caso ancla
  (genes letales para la anomalía 2:1) ES nuestro **op 2** — postular una subclase oculta con
  dinámica distinta!; cláusulas insertadas sobre la detección ("la reparación borra las
  mutaciones ANTES de medirlas") = **op 7**; reverse transcriptase abriendo mecanismos con lazo
  = **op 8**; schema instantiation / tipos de teoría = **op 11** (su operador central, con
  mecánica más fina que la nuestra: niveles de abstracción, criterios de elección de tipo).
- Sin correlato en ella: nuestros **3, 4, 6, 9, 10** (los saltos de estructura matemática) —
  su catálogo está sesgado a mecanismos biológicos por etapas; nuestra cobertura es más ancha.
- **Candidatas de ella que NO tenemos**: (a) **BORRAR estructura** (nuestros 11 operadores
  AGREGAN; "el modelo tiene una etapa de más" no está — candidata real a la matriz);
  (b) systematic scan (estrategia de cobertura — métrica conductual anti-fijación, pega directo
  con nuestro hallazgo de no-generación de alternativas); (c) modular subassembly (componer de
  una biblioteca de módulos conocidos — composición, no analogía); (d) forward/backward
  chaining; (e) la localización guiada por la firma de la anomalía (habilidad puntuable por
  consecuencias); (f) el repertorio explicativo (memoria entre episodios).

**Rival honesta (del propio lector):** el buen encaje puede deberse en parte a que ambos marcos
beben de la misma tradición (la IA de los 80: abstracción, diagnóstico, rediseño), no a
convergencia de fenómenos.

**Estado: LEÍDOS 5 completos** (1987 AI Magazine · Darden & Cook 1994 · 1998 Digital Phoenix ·
Machamer/Darden/Craver 2000 · 2002 PSA) + Intro del libro 2006. El capítulo 1992 y el libro
1991 (tablas canónicas 9.1/9.3) siguen POR-LEER — esperan PDF.
