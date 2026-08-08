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
