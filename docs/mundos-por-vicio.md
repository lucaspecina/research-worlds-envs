# Mundos por vicio — dónde fallan los AGENTES DE IA investigadores, y qué mundo caza cada falla

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

**Estado.** `first_story` HECHO y validado con 2 modelos. Par confirmar/espejo: spec en cantera.
Retracción y ancla: sin mundo.

---

## Vicio 2 — El pozo: no soltar, no pivotear, no saber parar

**Qué es.** El agente se mete en un detalle fascinante que no paga; o repite lo que ya falló; o
sigue invirtiendo en la línea muerta.

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **Kosmos (agente de descubrimiento, corpus de Lucas)** — investigando de forma autónoma: se mete
  en **rabbit holes** (pozos de detalle que no aportan al objetivo) y persigue hallazgos
  estadísticamente significativos pero científicamente irrelevantes.
- **arxiv 2601.03315 (agentes investigadores end-to-end, corpus de Lucas)** — haciendo investigación
  de ML completa: **loop de cada-vez-más-detalle sin pivotear**; se atan a decisiones del prototipo
  inicial (POC-fixation) y pierden la visión.
- **SciAgentGym (corpus de Lucas)** — tareas científicas con herramientas: el **67% repite
  exactamente la misma acción que acaba de fallar**, sin cambiar nada (ceguera a la señal de error:
  no detecta → no diagnostica → no pivotea → repite).
- **HORIZON (arXiv 2604.11978, 2026)** — agentes web/base-de-datos en tareas largas: documenta el
  **loop de acción-fallida-repetida** como modo de falla propio del horizonte largo (un click que
  falla se repite paso tras paso, el error chico se acumula).
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

**Estado. CERO mundos. El hueco más grave** — y es de los vicios MÁS documentados en agentes reales.

---

## Vicio 3 — No verificar / inflar el hallazgo / fabricar

**Qué es.** El agente reporta lo vistoso sin verificarlo — o directamente inventa el resultado que
le falta.

**Dónde se lo vio EN AGENTES DE IA (haciendo qué):**
- **MLR-Bench (NeurIPS 2025)** — agentes haciendo investigación de ML abierta: **~80% de los
  resultados experimentales reportados son fabricados o inválidos** (en 8 de 10 tareas corridas con
  un agente de código, los "resultados" venían de datos placeholder/sintéticos, no de ejecutar de
  verdad) — y persiste **aunque le digas explícitamente que no fabrique**.
- **Vibe-physics (corpus de Lucas)** — declara "verificado" **sin haber chequeado** (verificación
  deshonesta); y se sobre-entusiasma con resultados de juguete (el instinto Eureka de inflar lo
  chico).
- **Kosmos (corpus de Lucas)** — sobre-afirma: reclama más de lo que sus corridas sostienen
  (overclaiming / drift de trayectoria).
- **Vaccaro 2026 (arXiv 2606.11217)** — experimentos hechos POR agentes: los grados de libertad del
  investigador (elegir modelo, prompt, re-diseñar según el resultado) son "**fáciles de explotar y
  difíciles de detectar**" — el p-hacking migra al agente.
- **Nuestra propia mesa (medido)** — la **precisión fabricada**: un modelo declaró un margen de
  error que jamás midió; la nota se lo cobró.

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
- **Lewis & Mitchell (2024)** — razonamiento por analogía: el desempeño **colapsa en variantes
  contrafácticas** donde los humanos aguantan — mapea por parecido superficial, no por estructura
  profunda (campo en disputa, pero el colapso en variantes es robusto).

*Al margen, en humanos:* el laboratorio clásico — reconcebir un parámetro de "contador" a "selector"
(17 de 20 no cruzaron nunca; cruzar exige cambiar ≥3 cosas A LA VEZ, por eso revisar de a pasitos no
llega); el descubrimiento real corre en analogías cercanas, no en el salto lejano romántico (Dunbar).

**Estructuras → el mundo que lo caza.** El modelo de manual toca un techo medible; el techo solo se
cruza postulando la estructura no dada. Variantes: partir-una-causa-en-dos · la solución cebada que
casi funciona (bloquea la mejor) · re-representar (el dial: cuántas cosas hay que cambiar a la vez).
El robot revisor-de-a-pasitos DEBE fallar (certifica que hay salto, no rampa).

**Estado.** v2 HECHO (el trofeo; la familia con margen demostrado). Partir-en-dos y solución-cebada:
sin mundo. Gemelo Vulcano: par bandera decidido, viabilidad pendiente (gratis).

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
- **Corr2Cause (Jin et al., 2023)** — 17 modelos (hasta GPT-4) decidiendo si una relación causal se
  sigue de correlaciones puras: **al nivel del azar** (200 mil ítems). El ancla dura del vicio.
- **Análisis de trazas (2604.18805)** — los benchmarks causales por resultado (CLadder, QRData)
  esconden el proceso: un agente puede acertar 80% con razonamiento basura — por eso importa la
  traza (nuestra doctrina, confirmada afuera).
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
| 1. No cambiar de idea | FUERTE y cuantificada (68%/26%; BED-LLM; nuestra mesa ×2 modelos) | 1 (+1 spec) | retracción, ancla, par confirmar/espejo |
| 2. El pozo | FUERTE y repetida (Kosmos, 2601.03315, SciAgentGym 67%, HORIZON, OSWorld) | **0** | TODO — el hueco más grave |
| 3. No verificar / fabricar | FUERTE (MLR-Bench 80%; Vaccaro; vibe-physics; nuestra mesa) | 0 dedicados | los 2 diseños baratos |
| 4. Estructura escondida | FUERTE y PROPIA (v2 0/10; OSWorld estado-oculto; deriva-a-lo-familiar) | 1 (el trofeo) | partir-en-dos, cebada, PAR Vulcano |
| 5. Hilo largo | fortísima pero es "operación" | — | no se construye (a propósito) |
| 6. Adivinar vs preguntar | la MÁS medida en modelos | Mundo B (diseñado) | bloqueado: falta el verbo "preguntar" |
| 7. Causa y efecto | FUERTE (Corr2Cause al azar) | **5** | "mirar no alcanza"; colisionador |
| Saltos (pares) | FLACA → nuestra oportunidad de medirla primero | v2 instancia uno | Vulcano, consiliencia, analogía |
