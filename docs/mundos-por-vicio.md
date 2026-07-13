# Mundos por vicio — dónde fallan los AGENTES DE IA investigadores, y qué mundo caza cada falla

> **Capa fina (ADR 0140)**: la descomposición de cada vicio en SUB-FORMAS con casos
> reales etiquetados (verificación × tipo × estado generacional) vive en **`docs/vicios/`**
> — este doc deriva mundos; aquél detalla el fenómeno.

> **Qué es este documento (ADR 0113, re-enfocado por ADR 0114).** El foco es **IA**: por cada vicio,
> **dónde está documentado EN AGENTES DE IA haciendo investigación** — qué paper/benchmark, qué
> estaba haciendo el agente, cómo se manifestó, con qué número. La psicología humana y la historia
> de la ciencia quedan **al margen** (una línea por vicio, como fondo — sirven para las estructuras,
> no son el foco). Después, por cada vicio: sus estructuras y **el mundo que lo caza** (exista o no
> hoy). Catálogo-primero: lo construido no manda. La evidencia completa con citas vive en
> `docs/failure-modes.md`; la cola de trabajo, en `docs/roadmap.md`.

**La vara de validación, común a todos** (cómo sabemos que un mundo caza su vicio): (1) dos
jugadores-robot — el que comete el vicio DEBE perder, el cuidadoso DEBE poder ganar; (2) IAs reales
jugando libres — ¿caen solas?; (3) la prueba de la frase — advertir sobre ESE vicio lo arregla, y no
mueve nada en mundos sin él (validada con gpt-5.4 y DeepSeek); (4) ideal con 2+ modelos — cada uno
tiene su propio perfil de mañas (hallazgo propio: PERFILES DE VICIO POR MODELO).

---

## Vicio 1 — No cambiar de idea ante la evidencia

**Qué es.** El agente se forma una explicación temprano y no la suelta: ignora lo que la contradice,
revisa poco, no triangula.

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **Análisis de trazas por grafo epistémico (arxiv 2604.18805, 2026)** — agentes resolviendo tareas
  de razonamiento científico (CLadder, QRData, DiscoveryBench), traza anotada paso a paso: la
  evidencia que contradice la hipótesis se **ignora en el 68%** de los casos; la creencia refutada se
  **revisa solo el 26%**; triangular con tests independientes es raro (**6-13%** según modelo). Y el
  dato estructural: el modelo base explica el 41.4% de la varianza del proceso; el andamiaje solo el
  1.5% — el vicio vive en el modelo, no en el prompt (y darle un ejemplo bueno en contexto NO lo
  arregla).
- **BED-LLM (arXiv 2508.21184, 2025)** — agente juntando información activamente (estilo 20
  preguntas): propone hipótesis **incompatibles con lo que ya observó** y su confianza CRECE con la
  historia — cuanto más lleva, menos revisa.
- **Benchmark de apuestas por temporada (corpus de Lucas)** — el agente no actualiza cuando el mundo
  cambia; y el hermano raro: identifica bien la ventaja y **no actúa** en consecuencia
  (análisis-decisión desconectados).
- **Vibe-physics (Anthropic, corpus de Lucas)** — haciendo física exploratoria con un humano: se
  ancla a sus primeras preferencias y cede bajo presión social (sycophancy) — da la respuesta que
  parecés querer en vez de sostener la evidencia.
- **Nuestra propia mesa (medido, 2026-07)** — `first_story`: gpt-5.4 entrega la primera historia
  bajo escasez (mediana 0.00 libre → 0.87 con la advertencia); **DeepSeek se casa con la 1ª hipótesis
  AUN con presupuesto de sobra** (0.36→0.89 con la advertencia de pivoteo). Dos modelos, el mismo
  vicio, condiciones distintas.

*Al margen, en humanos:* es el sesgo más clásico de la psicología (Wason; Klayman-Ha: si tu regla es
un caso particular de la verdadera, confirmar no refuta NUNCA; la creencia sobrevive incluso a que te
digan que la evidencia era falsa) y de la historia de la ciencia (Apollo; ozono; deriva continental).
De ahí salen las geometrías de las trampas.

**Estructuras → el mundo que lo caza.** Ingredientes: (a) una primera explicación tentadora que la
piel del mundo planta sola; (b) está mal; (c) la refutación está disponible pero hay que ir a
buscarla. Variantes (mundos distintos): la contradicción llega a mitad de camino (maquinaria de
noticias lista) · la trampa de solo-confirmar y su ESPEJO (par diseñado: ningún reflejo fijo gana
ambos) · te retiran un dato que compraste (¿la creencia vuelve atrás?) · el ancla (un número
prominente corrido al inicio).

**Estado.** `first_story` HECHO y validado con 2 modelos — y protocolo vicio-vivo corrido
(2026-07-11): **en gpt-5.4 el vicio NO está vivo** (1/8 con la firma; 8/8 usan la escapatoria)
→ queda como CONTROL de facto para frontier actuales. Par confirmar/espejo: spec en cantera.
Retracción y ancla: sin mundo. **NUEVO (ADR 0141): el ESPEJO de este vicio — dejarse influenciar
(sub-actualizar ante DATOS ↔ sobre-actualizar ante OPINIONES) — elevado a par de primera clase:
dos mundos con la misma fachada donde en uno ceder es virtud (dato) y en el otro sostener es
virtud (testimonio sin evidencia); firma computable = cambio de conclusión sin evidencia nueva.
Candidato a contribución original; detalle en `docs/vicios/vicio-1-no-cambiar-de-idea.md`.**

---

## Vicio 2 — El pozo: no soltar, no pivotear, no saber parar

**Qué es.** El agente se mete en un detalle fascinante que no paga; o repite lo que ya falló; o
sigue invirtiendo en la línea muerta.

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **Kosmos (Edison Scientific; reporte leído entero)** — AI Scientist desplegado: admite que *"se mete
  en rabbit holes y persigue hallazgos significativos pero científicamente irrelevantes"*. **DATO DE
  DISEÑO clave**: *"cuanto más larga la corrida, más probable que descienda a un rabbit hole"*, hasta
  esperar que el VALOR de la corrida se INVIERTA con la profundidad → **el largo de la investigación
  es un dial natural de la trampa: cuanto más lo dejás cavar, más se hunde.**
- **Trehan & Chopra (2601.03315; leído)** — investigación de ML end-to-end: **loop de cada-vez-más-
  detalle sin pivotear** (ej. real: se clavó en un error de convolución, 31×31→79×79, ambos mal,
  quemando iteraciones); se ata al prototipo inicial (POC-fixation).
- **SciAgentGym (Shen et al., 2602.12984; leído)** — tareas científicas con herramientas: los modelos
  **responden a solo el 32.9% de las señales de error** (loop-escape 35.7%: ~2 de cada 3 caen en
  repetición idéntica). *CORREGIDO 2026-07-09: nuestro "67%" era el "Caso 67" (un ejemplo), NO un
  porcentaje — se leyó el paper.*
- **HORIZON (Wang et al., 2604.11978; leído)** — su "loop de acción-fallida-repetida" *lo tenía acá,
  pero CORREGIDO: el paper lo enmarca como error de EJECUCIÓN (repetición mecánica), no pozo cognitivo
  → pertenece al vicio 5, no al pozo.* Se deja la nota para no volver a mapearlo mal.
- **Vibe-physics (corpus de Lucas)** — no sabe **cuándo parar**; sigue elaborando cuando lo correcto
  era cerrar.
- **OSWorld-V2 (corpus de Lucas)** — tareas de computadora: gasta **<7% del presupuesto** en detectar
  y reparar sus propios errores (todo lo demás es avanzar ciego).

*Al margen, en humanos:* costo hundido (Arkes-Blumer; efecto real, mediano) y escalada del
compromiso (inversión previa + mala noticia + decidir seguir/soltar; la mala noticia empuja a
"hacer algo", sea lo que sea). Advertencia del flogisto: persistir es vicio SOLO si soltar es
claramente mejor — si empatan, es prudencia y el mundo no debe castigarla.

**Estructuras → el mundo que lo caza.** El **señuelo fascinante**: una fuente con un patrón
intrincado que parece la clave y no aporta nada al examen — el costo es de oportunidad (lo que
quemaste ahí te falta para lo que importa). O la **apuesta perdida**: una línea de investigación
pagada deja de rendir, con señal clara y punto de decisión explícito — seguir es perder. El robot
que excava el señuelo hasta el fondo DEBE perder; el que lo prueba un poco y sale DEBE ganar.
**Dial de dificultad (dato real de Kosmos): el LARGO permitido de la investigación — cuanto más
largo, más se hunde el que no sabe cortar.**

**Estado (2026-07-12/13, ADRs 0138/0139/0141 — reformulado BIPOLAR: el polo vivo es el CIERRE
PREMATURO; el costo hundido queda pausado → experimento propio-vs-heredado; detalle en
`docs/vicios/vicio-2-el-pozo.md`).**
TRES mundos verificados: `rabbit_hole_v0` (certificado 19/19, claim estrecho: solo el pozo
PROFUNDO), `rabbit_hole_v2` (portafolio de 5 líneas — separación 0.57: el robot-pozo paga de
verdad) y `lab_largo_v0` (14 rondas, obra propia registrada + expansión de alcance en ronda 4 —
separación 0.58; estrena el verbo `register`). Y el HALLAZGO fuerte de la casa: **en gpt-5.4 el
vicio NO es elicitable en episodios compactos con presupuesto explícito — 6 diseños × 60
episodios = 0 caídas** (escalera de emergencia completa: costo itemizado, difuso, residual
nombrado, arranque en caliente, micro-compromisos, escalada con obra propia — todas con firma
pre-registrada; la predicción 45% de Codex r21 quedó refutada). Con costo difuso y UN solo tema
(v1, no certificado) SÍ cava — la conducta existe, el juicio de asignación la domina cuando hay
alternativas visibles. En la clase entrenable (DeepSeek): 1/10 pozo moderado real (R=0.47) +
4/10 fallas de entrega → los mundos SÍ tienen señal para E2. El hueco AHORA: corridas
genuinamente largas sin presupuesto explícito (la condición Kosmos real, sin testear) y la
clase 4-8B.

---

## Vicio 3 — No verificar / inflar el hallazgo / fabricar

**Qué es.** El agente reporta lo vistoso sin verificarlo — o directamente inventa el resultado que
le falta.

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **MLR-Bench (Chen et al., 2505.19955; leído)** — agentes en investigación de ML abierta: **~80% de
  resultados fabricados/inválidos** (8 de 10 tareas con datos placeholder/sintéticos). *Ejemplo real:
  Claude Code, ante un fallo de ejecución, "tomó un atajo generando resultados simulados, priorizando
  completitud sobre corrección"; y persiste aun instruido "no fabriques" — "aprendió a saltear los
  problemas de cómputo generando resultados plausibles pero inválidos como estrategia de
  supervivencia".* Además **cita papers que NO existen en el 50% de las tareas.**
- **Vibe-physics (Schwartz/Anthropic; leído)** — dice "verificado" sin chequear. *Ejemplos reales:
  "básicamente falseaba el gráfico entero" (tiraba las variaciones difíciles y ajustaba las curvas); y
  en las verificaciones "inventaba coeficientes que no estaban en el paper", con "justificaciones
  plausibles para respuestas que no había derivado".*
- **Trehan & Chopra (2601.03315; leído)** — *ejemplo real*: *"reescribí a Actor-Critic, preserva la
  idea central de optimización conjunta"* — MIENTRAS abandonaba esa misma idea central: racionaliza la
  retirada como si fuera una mejora.
- **Kosmos (Edison; reporte leído)** — sobre-afirma (overclaiming): reclama más de lo que sus corridas
  sostienen; su propio reporte lo admite.
- **Robin (Ghareeb et al., 2505.13400; leído)** — overclaiming que se AUTO-CONTRADICE: se anuncia como
  *"el primer sistema en automatizar TOTALMENTE los pasos intelectuales de la ciencia"* y *"el primer
  sistema en descubrir y validar autónomamente un candidato terapéutico"* — mientras el mismo abstract
  lo llama *"semi-autónomo"* y "lab-in-the-loop" (con humano). El reclamo contradice lo que admite ser.
- **Vaccaro 2026 (2606.11217; leído)** — grados de libertad "**fáciles de explotar y difíciles de
  detectar**". *OJO (CORREGIDO): el paper habla de los INVESTIGADORES humanos que estudian agentes, NO
  del agente p-hackeándose; el agente-que-lo-hace es extrapolación NUESTRA (estructura transferible).*
- **Sakana AI Scientist (Beel & Kan, 2502.14297; leído)** — 4 de 7 papers (**57%**) con números
  fabricados. *Ej. real: un estudio de "eficiencia energética" reclamó mejora de RMSE mientras el
  tiempo bajaba 116→115s pero la memoria SUBÍA, sin justificar — y "su propio mecanismo de review no
  lo detectó".* De fondo: *"no puede evaluar críticamente sus propios resultados; no detecta fallos
  metodológicos".*
- **Crítica CMU (Luo, Kasirzadeh & Shah, 2509.08713; leído)** — 4 fallas de tipo p-hacking en agentes
  investigadores, con ejemplo real: **cherry-picking de benchmarks** (Agent Laboratory elige los
  primeros 4 de la lista el **82.4%** de las veces, sin importar la dificultad — sesgo de POSICIÓN);
  data-leakage no documentado; mal uso de métricas según el ORDEN en que se presentan; sesgo de
  selección post-hoc (el reward premia buen test aunque el train sea flojo). *Y todas son INVISIBLES
  en el paper final — hay que mirar la traza (74% de detección con traza) = nuestra tesis exacta.*
- **Nuestra propia mesa (medido)** — la **precisión fabricada**: un modelo declaró un σ que jamás
  midió; la nota se lo cobró.

*Al margen, en humanos:* la crisis de replicación entera — con los 4 atajos típicos a la vez, la
chance de un falso hallazgo sube del 5% al 60.7% (Simmons 2011); y pasa sin mala intención (el
jardín de senderos de Gelman: cada decisión "parece la única razonable" mirando estos datos).

**Estructuras → el mundo que lo caza.** 2-3 métricas alternativas legítimas donde UNA da un efecto
llamativo que es ruido y la aburrida es la real — el examen fuera de muestra cobra al que entrega lo
vistoso. O el **corte oportunista**: el agente decide cuándo dejar de muestrear; cortar "cuando se ve
bien" infla el efecto (chico, barato, angosto). La fabricación ya se cobra por construcción (el
examen corre el modelo entregado: la retórica vale cero).

**Estado.** Cero mundos dedicados; los dos diseños son de los más baratos de construir.

---

## Vicio 4 — No inventar la explicación escondida / retirarse a lo familiar

**Qué es.** Los datos solo cierran si postulás algo que nadie te dio (una variable oculta, dos
mecanismos, otro marco) — y el agente se queda con el modelo de manual.

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **Nuestra propia mesa (el trofeo, medido)** — el mundo de la composición oculta por lote: **10
  partidas, 2 familias de modelos, NADIE intentó inferir la composición** desde la muestrita
  disponible; el mejor jugó "técnicamente perfecto, cero errores" y sacó **0.096 sobre 1** —
  retirada al modelo familiar medida en vivo. Ejecutar la idea ganadora cuesta 10 líneas;
  **concebirla** es lo que faltó.
- **OSWorld-V2 (corpus de Lucas)** — los agentes **se hunden justo en las tareas que dependen de
  recuperar un estado oculto** (lo latente es su punto ciego).
- **arxiv 2601.03315 (corpus de Lucas)** — investigación de ML end-to-end: **deriva de
  implementación hacia lo simple-familiar** (reimplementa con las librerías que conoce, se aleja de
  la idea original); sesgo del dato de entrenamiento.
- **Vibe-physics (corpus de Lucas)** — no logra **sostener una convención no-estándar** que él mismo
  escribió: vuelve a los defaults de manual una y otra vez.
- **HLER (2026)** — generación de hipótesis autónoma: sin anclar a la estructura del dataset, solo el
  **41%** de las hipótesis son factibles (vs 87% ancladas) — el lado generativo, medido.
- **Sakana AI Scientist (Beel & Kan, 2502.14297; leído)** — *taste débil, medido*: juzgó *"las 10
  ideas generadas y las 2 semilla como NOVEDOSAS"* usando *"keyword matching en vez de síntesis
  profunda"* — ej. real: llamó novedoso al micro-batching para SGD, técnica ya documentada (Jain et
  al. 2018). No distingue lo conocido de lo nuevo.
- **Si, Yang & Hashimoto (2409.04109; leído)** — estudio con 100+ investigadores: las ideas del LLM se
  juzgan MÁS novedosas que las humanas (5.64 vs 4.84, p<0.05), PERO **mode-collapse**: de 4000 ideas
  generadas solo **200 únicas (~5%)**, y las no-duplicadas caen con cada tanda — *genera la misma idea
  una y otra vez* (mata la estrategia de generar-y-rankear). Bonus: como JUEZ de ideas el LLM llega a
  53.3% (peor que humanos) → **confirma nuestra regla de cero-LLM-en-la-nota.**
- **Lewis & Mitchell (2024)** — razonamiento por analogía: el desempeño **colapsa en variantes
  contrafácticas** donde los humanos aguantan — mapea por parecido superficial, no por estructura
  profunda (campo en disputa, pero el colapso en variantes es robusto).
- **★ Chen, Zhao & Cohan 2026 ("Measuring the Gap...", 2607.01233; leído; TIER A, la evidencia más
  fuerte de este vicio)** — 9 modelos generan ideas desde el mismo contexto de literatura que un paper
  humano real. El vicio con número: el **REFLEJO DE SÍNTESIS** — sobre-producen "conectá/combiná estas
  dos cosas" (ideas de puente **12% humano vs 47-64% LLM**; operación "integrar" **34.2% modelo vs
  2.35% humano**). Evitan las movidas humanas locales: **reemplazar** (9.1% vs 0.9%), **desacoplar dos
  mecanismos confundidos** (2.3% vs 0.2% — ¡nuestra familia causal!), **formalizar**. Poner el modelo a
  razonar más EMPEORA el reflejo; los modelos se parecen entre sí más que a los humanos. Es el
  polo-vicio de la analogía a nivel ideación, medido a escala. **Y es la mejor justificación externa
  del proyecto entero** (que el juicio/taste falta y se puede medir).

*Al margen, en humanos:* el laboratorio clásico — reconcebir un parámetro de "contador" a "selector"
(17 de 20 no cruzaron nunca; cruzar exige cambiar ≥3 cosas A LA VEZ, por eso revisar de a pasitos no
llega); el descubrimiento real corre en analogías cercanas, no en el salto lejano romántico (Dunbar).

**Estructuras → el mundo que lo caza.** El modelo de manual toca un techo medible; el techo solo se
cruza postulando la estructura no dada. Variantes: partir-una-causa-en-dos · la solución cebada que
casi funciona (bloquea la mejor) · re-representar (el dial: cuántas cosas hay que cambiar a la vez).
El robot revisor-de-a-pasitos DEBE fallar (certifica que hay salto, no rampa).

**Estado.** v2 HECHO (el trofeo; la familia con margen demostrado). Partir-en-dos y solución-cebada:
sin mundo. Gemelo Vulcano: par bandera decidido → **ESTACIONADO en cantera (ADR 0117: es par de AHA,
y los gemelos son agregado, no eje)**; su test de viabilidad (gratis) queda listo para rato ocioso.
**Validado por afuera**: el position paper "LLMs can't jump" (2026) usa el ejemplo Vulcano exacto
—parchar-con-Vulcano vs reestructurar-la-teoría— y propone mundos con intervención contrafáctica como
la vía al salto: es nuestra tesis desde la filosofía de la ciencia. (Deja una tensión honesta: el
salto más duro pasa SIN señal de error, y nuestro reward ES señal de error — ver `failure-modes.md`.)

---

## Vicio 5 — Perder el hilo en tareas largas → NO se construye en contra (a propósito)

Documentadísimo en agentes (METR 2025: la tasa de éxito cae monótona con el largo de la tarea;
HORIZON 2026: la restricción sigue EN el contexto y la viola igual — "desatención, no olvido";
tau-bench: no sostiene la política declarada; deriva que se auto-refuerza +22.7pp por paso;
SciAgentGym: la resiliencia cae sin recuperarse en trayectorias largas). **Pero es mayormente el
vicio del "trabajador desprolijo"**: lo arreglan memoria y andamiaje, no juicio — y medio campo
trabaja en eso. Decisión vigente: **se MIDE si aparece, no se diseña en contra.**

---

## Vicio 6 — Adivinar en vez de preguntar → BLOQUEADO por una regla del juego

**El mejor documentado EN MODELOS de toda la lista** — y sin embargo bloqueado para nosotros:
- **Su & Cardie (2026)** — 10 modelos respondiendo consultas ambiguas: **detectan la ambigüedad
  (60-80%) pero preguntan <5%** — el fallo es de acción, no de detección. Y peor: **darles contexto
  los hace preguntar MENOS** (falsa sensación de suficiencia).
- **BED-LLM (2025)** — juntando información: no adapta la próxima pregunta a lo ya respondido
  (45% de acierto vs 93% con estrategia).
- **OSWorld-V2 (corpus de Lucas)** — **adivina en vez de preguntar** cuando le falta un dato de la
  tarea.

**Por qué está bloqueado:** sus estructuras exigen el verbo **PREGUNTAR** (un oráculo consultable
con costo), y nuestro juego solo tiene "comprar datos" y "experimentar". Agregarlo cambia el
contrato de todos los mundos → decisión grande, de Lucas, sin apuro. Lo único construible hoy —
elegir la pregunta/experimento que de verdad discrimina — **ya tiene mundo diseñado (Mundo B)**.

---

## Vicio 7 — Confundir "pasan juntas" con "una causa la otra"

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **Corr2Cause (Jin et al., 2023)** — 17 modelos decidiendo si una relación causal se sigue de
  correlaciones puras (200 mil ítems): verbatim *"the best performance is 33.38% F1 by BART MNLI...
  even higher than GPT-4... many models are worse than random guess"*. **OJO (corrección 2026-07-12,
  ADR 0140): es VIÑETA, 2023, pre-razonamiento — probablemente MUERTO en frontier de razonamiento**
  (follow-up 2507.23488 con o3-mini/R1 + algoritmo PC lo supera; por leer). El ancla del vicio pasa
  a ser NUESTRA evidencia agéntica (la pendiente espuria heredada, abajo).
- **Ríos-García et al. (2604.18805; leído)** — la evaluación por RESULTADO esconde el proceso: un
  agente ejecuta bien y razona basura (ignora evidencia 68%). *CORREGIDO: su setup son 8 dominios de
  química, NO "CLadder/QRData".* Por eso importa la TRAZA (nuestra doctrina, confirmada afuera).
- **Kapoor & Narayanan (2023)** — ciencia hecha con ML: 8 tipos de fuga/desajuste que inflan
  resultados aun con partición limpia (la práctica real de ML-para-ciencia comete el error en masa).
- **Nuestra propia mesa (medido)** — el mundo del confusor: el jugador ingenuo hereda una pendiente
  espuria de +87%; nuestros 5 mundos causales lo cobran sistemáticamente.

*Al margen:* la "ciencia patológica" humana cayó 4 veces seguidas en el MISMO mecanismo (un factor
escondido que acompaña la manipulación — polywater, Mpemba, etc.).

**Estructuras → el mundo que lo caza.** La familia MÁS cubierta (5 mundos hechos). **Falta el
derivado directo de la lista:** el mundo donde **mirar no alcanza ni en principio** — gana el que
interviene o se abstiene con honestidad; pierde el que entrega confianza mirando. (Y queda por minar
en agentes: el sesgo del colisionador/selección.)

---

## Vicio 8 (NUEVO — agregado 2026-07-09 leyendo los papers) — Perder el objetivo / la relevancia

**Qué es.** El agente pierde de vista para qué estaba investigando: angosta el foco a un sub-problema,
deja de mantener el panorama, o persigue algo que dejó de ser relevante al objetivo. **Relacionado con
el pozo (vicio 2) pero DISTINTO**: el pozo es clavarse en un detalle que no paga; esto es perder el
NORTE — se puede perder el objetivo sin meterse en ningún pozo (persiguiendo lo significativo-pero-
irrelevante, o resolviendo prolijo un sub-problema que no es la pregunta).

**Dónde se lo vio EN AGENTES DE IA (TRES fuentes independientes — por eso entra a la lista):**
- **Trehan & Chopra (2601.03315; leído)** — investigación de ML end-to-end: *"no podían mantener un
  pensamiento de portafolio y seguían angostando el foco"*.
- **Schwartz / Anthropic "vibe-physics" (leído)** — Claude en física de QCD (102 tareas, 7 etapas):
  *"solo maneja pasos chicos y pierde la dirección fácilmente."*
- **PaperBench (Starace et al., OpenAI, 2504.01848; leído)** — replicando papers de ML: *"todos los
  modelos salvo Claude 3.5 Sonnet cortaban ANTES, afirmando que habían terminado o que habían chocado
  un problema"*; *"todos fallaron en estrategizar cómo replicar el paper dado el tiempo limitado"*.
  **Evidencia CAUSAL**: o1 con "BasicAgent" saca 13.2%; con "IterativeAgent" (que le SACA la opción de
  cortar antes) sube a **24.4%** — casi el doble solo por no dejarlo abandonar. → directamente
  medible: ¿corta antes afirmando que terminó?
- *(Relacionado, ya contado en otros vicios: Kosmos persiguiendo lo significativo-pero-irrelevante;
  la POC-fixation de 2601.03315.)*

**Estructuras → el mundo que lo caza (por diseñar).** Un objetivo global claro con varios sub-
problemas, donde el reward SOLO paga el objetivo global; el que se pierde en un sub-problema
parcial (aun resolviéndolo bien) entrega peor el global. Firma: reporta un sub-resultado prolijo que
no responde la pregunta que le hicieron. **Más tramposo que el pozo**: allá el señuelo no paga NADA;
acá el sub-problema paga PARCIAL. Ojo de diseño: distinguirlo de la buena descomposición (resolver
sub-problemas ES investigar) — el vicio es perder el ENSAMBLE, no descomponer.

**Estado.** CERO mundos. Candidato nuevo con 2 fuentes.

---

## Vicio 9 — La verificación de paja (PROMOVIDO 2026-07-13, ADR 0141; eje INTEGRIDAD)

**Qué es.** El agente SÍ verifica — pero con un test que él mismo eligió y que pasa por
construcción (el happy path, el panel que confirma), en vez del verificador que podría refutarlo.
La ilusión de rigor. Distinto del vicio 3 (ahí no hay verificación; acá hay esfuerzo real con
poder de refutación ~cero).

**Dónde se lo vio EN AGENTES DE IA**: la clase de falla dominante en las taxonomías de agentes
de terminal/código de 2026 (detalle y fuentes en `docs/vicios/vicio-9-overtrust-verificacion.md`;
cola de lectura antes de citar números).

**Estructuras → el mundo que lo caza.** Dos verificadores disponibles: el propio-configurable
barato (degenerable en paja) y el discriminante caro (réplicas/hold-out). La firma es computable
con nuestros gemelos: ¿su test distingue la verdad del gemelo? Si no, es paja. **Par espejo**:
la paranoia de verificación (re-chequear sin fin y no entregar). Probablemente se construye como
familia con el mundo del cierre prematuro.

**Estado.** CERO mundos; prioridad alta (comparte esqueleto con la prioridad #1).

---

## Los saltos creativos (el espejo — SIEMPRE de a pares)

La evidencia EN MODELOS del lado creativo es la más flaca de todas (casi todo lo tipificado es
humano) — **y eso es exactamente la oportunidad**: nuestros mundos pueden ser la primera medición
sistemática (la pregunta abierta "estructuras nativas de modelos"). Lo que hay: analogía superficial
en vez de estructural (Lewis-Mitchell 2024, tier A); exploración angosta correlaciona con peor
research (2510.10472, sin verificar); hipótesis no ancladas 41% factibles (HLER); follow-ups sin
imaginación (corpus de Lucas). Los pares decididos: **Neptuno/Vulcano** (postular lo invisible ↔
parchar) — bandera; **consiliencia** (dos anomalías, una causa ↔ apofenia) — barato; **analogía
estructural** (transferir el mecanismo ↔ dejarse llevar por el parecido) — con evidencia tier A del
lado malo.

---

## Estado global (la foto)

| Vicio | Evidencia EN AGENTES | Mundos hechos | El hueco |
|---|---|---|---|
| 1. No cambiar de idea | FUERTE y cuantificada (68%/26%; BED-LLM; nuestra mesa ×2 modelos) | 1 (+1 spec); **vicio NO vivo en frontier → control** | retracción, ancla, par confirmar/espejo |
| 2. El pozo | FUERTE y repetida (Kosmos —empeora con el largo—, 2601.03315, SciAgentGym) + **NUESTRA: 0/60 en frontier compacto (6 diseños pre-registrados, ADR 0139); señal en DeepSeek** | **3** (v0 certificado; v2 portafolio 0.57; lab_largo 0.58) | corridas largas SIN presupuesto explícito (Kosmos real); clase 4-8B |
| 3. No verificar / fabricar | FUERTE (MLR-Bench 80%; Vaccaro; vibe-physics; nuestra mesa) | 0 dedicados | los 2 diseños baratos |
| 4. Estructura escondida | FUERTE y PROPIA (v2 0/10; OSWorld estado-oculto; deriva-a-lo-familiar) | 1 (el trofeo) | partir-en-dos, cebada, PAR Vulcano |
| 5. Hilo largo | fortísima pero es "operación" | — | no se construye (a propósito) |
| 6. Adivinar vs preguntar | la MÁS medida en modelos | Mundo B (diseñado) | bloqueado: falta el verbo "preguntar" |
| 7. Causa y efecto | FUERTE (Corr2Cause al azar) | **5** | "mirar no alcanza"; colisionador |
| **8. Perder el objetivo/relevancia (NUEVO)** | 2 fuentes (2601.03315; vibe-physics) | **0** | por diseñar — distinguirlo de la buena descomposición |
| **9. La verificación de paja (PROMOVIDO 2026-07-13)** | dominante en taxonomías de agentes 2026 (cola de lectura) | **0** | par con el mundo del cierre prematuro (prioridad #1) |
| Saltos (pares) | FLACA → nuestra oportunidad de medirla primero | v2 instancia uno | Vulcano, consiliencia, analogía |
