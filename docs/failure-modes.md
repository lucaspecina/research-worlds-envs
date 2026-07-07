# Failure modes del juicio investigativo — catálogo y scaffold de diseño

> **Documento vivo (ADR 0099).** El corazón del proyecto: de un failure mode DOCUMENTADO
> → a la especificación de un mundo que lo pone de manifiesto de forma PUNTUABLE. No es una
> lista de memoria — es un scaffold para *ir a la literatura con paciencia, razonar, y
> diseñar mundos de a uno*. Reemplaza al viejo `FAILURE_MODES.md` (disuelto en la
> reestructura) con la estructura que ganamos discutiendo. Precedente de disciplina:
> `docs/mundo-a-primera-historia.md`, `docs/proto-designer.md`.

---

## 0. La tesis en una frase

Medimos juicio investigativo construyendo mundos donde **cada vicio documentado es la jugada
perdedora** — la conducta se OBSERVA (firma de trace), jamás se premia; el mundo hace que el
vicio produzca un modelo final peor y el examen cero-LLM cobra la consecuencia. Cada failure
mode bien documentado que encontramos **es una especificación para un mundo**.

## 0.5. El corte primario: OPERACIÓN vs JUICIO (define el ALCANCE de WAGER)

Antes de la taxonomía por dinámica de mundo (§3) hay un corte **más importante**, porque define
qué mide WAGER y qué NO. Todo failure mode cae en una de dos clases:

- **OPERACIÓN** — el agente es un trabajador desprolijo que **pierde el hilo**: pierde
  restricciones, no registra info que llegó a mitad de camino, adivina en vez de preguntar,
  repite una acción que ya falló, olvida verificar. **Lo arregla mejor andamiaje: memoria,
  checklists, planners, loops de reparación. Medio mundo ya trabaja en esto** (OSWorld,
  computer-use, memoria/reflexion). **NO es blanco de WAGER.**
- **JUICIO** — el agente **TIENE la info en contexto**, ve la contradicción, y aun así hace la
  jugada epistémica equivocada: ignora la evidencia (68%), no revisa la creencia refutada (26%),
  no triangula, se casa con la 1ª hipótesis, retrocede al modelo familiar, fabrica precisión.
  **El andamiaje NO lo arregla** (el base model explica el 41.4% de la varianza; el scaffold el
  1.5% — §4-ter). **Esta es la razón de ser de WAGER — lo que ningún otro entorno mide bien.**

**El discriminador** (afilado, de Lucas): *¿lo arreglaría un mejor andamiaje/memoria/checklist?*
**Sí → operación** (no es nuestro). **No → juicio** (es nuestro). **Heurística de fuente** (guía,
NO ley): un benchmark de operación/computer-use (OSWorld) tiende a reportar operación; un
análisis de TRAZA/epistémico (grafos H/T/E/J/U/C, §4-ter) reporta juicio. *Pero la fuente es
pista, no veredicto*: OSWorld —benchmark de operación— reporta "se hunde recuperando un estado
oculto", que es JUICIO puro (inferir lo latente = familia D/v2). **Siempre manda el
discriminador, no el origen.**

Las seis familias de §3 son la **sub-taxonomía de la columna JUICIO** — organizan cómo volver
puntuable un vicio de juicio. Los vicios de operación se registran y se **bracketean** (§4-bis),
nunca se mezclan con los de juicio: mezclarlos diluye el foco que es toda la tesis del proyecto.

## 1. Qué ya sabemos (no arrancamos de cero)

- **El instrumento SÍ captura vicios, medidos** (no es aspiracional): comprar-evidencia-y-no-
  usarla (4/4 gpt bajo escasez), terminación apurada, **precisión fabricada** (declaró un σ
  que no midió; la nota se lo cobró), retirada a la arquitectura familiar (v2). Todo apareció
  con número en nuestros mundos.
- **Validez de constructo — señal positiva (ADR 0098)**: una pista DIRIGIDA al vicio
  específico restaura el puntaje SOLO donde el vicio vive (first_story escaso: mediana
  0.00→0.87) y ≈0 en el control → el instrumento separa juicio, con la métrica correcta
  (mediana + separar ceros de ejecución de ceros de juicio). Caveat: n=5, replicar.
- **El hallazgo que ordena el diseño**: **el vicio bite bajo PRESIÓN, no a presupuesto pleno.**
  gpt pivotea "de rutina" con plata holgada; se le cae el buen hábito cuando el recurso
  aprieta. → *el mundo tiene que CREAR la presión, no solo pedir un análisis prolijo.*

## 2. Principios de diseño (los que ganamos con dolor — no negociables)

1. **Consecuencia cobrada, conducta observada** (Ethos §2.1/2.6): el vicio es la jugada
   perdedora; la firma de trace diagnostica, nunca premia.
2. **Certificado de trampa necesaria** (ADR 0082): dos robots scripteados — el **vicioso**
   (comete el vicio con maestría en todo lo demás) debe quedar LEJOS del techo; el
   **cuidadoso** debe alcanzarlo. Si el cuidadoso no llega → trampa injusta, se descarta.
3. **La presión expone el vicio** (ADR 0098): escasez de presupuesto / tiempo / evidencia que
   llega tarde. Un vicio dormido a presupuesto pleno no se mide sin presión.
4. **Vicios TEMPORALES → mundos que se DESPLIEGAN**: "no actualizar ante evidencia nueva"
   necesita que HAYA evidencia nueva llegando (la maquinaria de eventos, D4/ADR 0083, casi sin
   usar). El énfasis correcto: *evidencia por etapas, no toda disponible de entrada.*
5. **Vicios de INSIGHT/creatividad → mundos donde INVENTÁS la estructura** (familia v2, nuestro
   mejor resultado): ganar exige formular una hipótesis estructural que nadie te dio, no calzar
   un modelo de librería.
6. **Entregable PUNTUABLE + cero-LLM**: el deliverable sigue siendo "predecí el comportamiento"
   (scoreable sin juez LLM). La fachada (línea de producción, etc.) es piel; la sustancia
   siempre es "descubrí el mecanismo oculto investigando".
7. **Altura de la trampa/pista**: se nombra la CONDUCTA, nunca la RESPUESTA. Test: un modelo
   que nunca vio el mundo, tras leer la pista, sigue sin saber la respuesta.
8. **Aislá el JUICIO de la OPERACIÓN** (el corte de §0.5, lado diseño): el mundo debe REMOVER la
   excusa operacional —info relevante siempre en contexto o recuperable barato, restricciones
   explícitas, sin trampa de memoria/horizonte— para que la ÚNICA falla posible sea de juicio. Si
   el agente puede fallar por perder el hilo, estás midiendo operación (lo que el campo ya mide).
   Es el lado-DISEÑO de la separación ejecución-vs-juicio que ya validamos en la MEDICIÓN (ADR
   0098): allá separamos los ceros de ejecución de los de juicio; acá los diseñamos-afuera.

## 3. La taxonomía por DINÁMICA DE MUNDO (el organizador clave)

No agrupamos los vicios por su nombre psicológico sino **por la dinámica de mundo que los
fuerza a manifestarse de forma puntuable** — porque esa dinámica ES el diseño.

| familia | vicios que agrupa | dinámica de mundo que lo expone | scoring |
|---|---|---|---|
| **A. Actualización de creencias** | casarse con la 1ª hipótesis; no incorporar evidencia nueva; sesgo de confirmación; anclaje; conservadurismo bayesiano | **DESPLIEGUE**: evidencia contradictoria llega a mitad de camino (eventos sellados); la verdad puede driftear | predecir comportamiento post-actualización |
| **B. Atención / perseverancia** | rabbit holes; más-de-lo-mismo sin pivotear; no saber cuándo parar; perder de vista el objetivo | **DISTRACTOR + PRESIÓN**: pozo fascinante en un dato lateral que no paga, bajo presupuesto escaso | costo de oportunidad cobrado en el modelo final |
| **C. Verificación / rigor** | "verified" sin verificar; over-claims; **precisión fabricada**; perseguir lo significativo-pero-irrelevante | **RESPUESTA BARATA FALSA + verificación disponible**: la carnada de significancia; declarar un número sin medirlo se paga | |ΔF| de la cantidad no-verificada |
| **D. Representación / creatividad** | retirada a lo familiar; no inventar la estructura necesaria; sobre-simplificar | **INVENTAR LA ESTRUCTURA** (v2): el ganador formula una hipótesis latente/estructural | fidelidad al mecanismo que solo la estructura correcta reproduce |
| **E. Memoria / consistencia (largo plazo)** | perder restricciones; trabajo redundante; recuperación que se degrada en trayectorias largas | **HORIZONTE LARGO + restricción de enlace tardío** (declarada temprano, cobrada al final) | parcialmente límite del harness → se MIDE, no se diseña-en-contra |
| **F. Interacción / preguntar** | adivinar en vez de averiguar; no registrar info que llega a mitad de camino; saltear la verificación disponible | **CONSULTABLE + evidencia mid-way**: lo faltante tiene precio conocido y accesible | diferencia de suposición-vs-consulta |
| **G. Razonamiento causal** | correlación≠causación; confounding; colisionador/selección; no-intervenir; ignorar el DGP | **OBSERVACIONAL ENGAÑOSO + intervención disponible**: la correlación barata miente; do() cuesta y revela | fidelidad al efecto causal que solo la intervención recupera |

> **Las siete familias (A-G) sub-clasifican la columna JUICIO** (§0.5), no la de operación. Cada familia
> tiene una CARA operacional que el diseño debe **engañar-afuera** para no medir operación por
> error: **E (memoria) es la más peligrosa** — la info debe quedar EN contexto para que la falla
> sea "no lo conectó" (juicio) y no "lo perdió" (operación); por eso E "se mide, no se
> diseña-en-contra". **F straddlea**: "adivinar en vez de preguntar" es operación, pero *saber que
> necesitás preguntar* (reconocer que hay algo que no sabés) es juicio — ese es el lado nuestro.

## 4. El catálogo (seed inicial — a completar con la literatura)

Por cada vicio: fuente · cómo se manifiesta · dinámica (§3) · estado. **Las citas exactas se
verifican/completan minando papers (ver §5); lo de abajo es el seed de lo que ya sabemos.**

> **Cosecha de la investigación dirigida (deep-research, 2026-07-07)** — corrida de 5 ángulos, 26
> fuentes, 117 claims → 25 verificadas por voto adversarial → **19 confirmadas (3-0/2-1)** + 6 sin
> verificar (el paso de síntesis se cayó por límite de API; la curaduría la completé desde los
> claims verificados). **Marcas de estado de verificación** (honestidad de precisión — no marcar lo
> que no se midió): **`[dr ✓]`** = pasó el voto adversarial 3-0/2-1; **`[dr ·]`** = extraído con
> CITA TEXTUAL de la fuente pero NO llegó al voto (el presupuesto de verificación se cortó);
> **`[dr ~]`** = candidato cuyos 3 votos erroraron por el límite. **Todos pasaron el triage §0.5 =
> JUICIO** (blanco de WAGER), no operación.

### A — Actualización de creencias
- **Fijación de hipótesis / sesgo de confirmación** — cog-sci clásico (Wason 2-4-6; Klayman &
  Ha, positive-test strategy): se busca evidencia que confirma, no que refuta. → mundo de
  despliegue con refutación que llega tarde. *Estado: parcial (first_story mide la 1ª-hipótesis
  a presupuesto pleno, pero el vicio no bite sin presión; con-noticia sin correr con modelos).*
- **No-actualización / conservadurismo** — updating bayesiano insuficiente (Edwards; base-rate
  neglect, Kahneman-Tversky): ante evidencia contraria, la creencia casi no se mueve. → eventos
  sellados. *Estado: maquinaria lista (D4), certificado de robots ✓ (0.0002 vs 0.989), sin
  correr con modelos.*
- **Anclaje** — Tversky & Kahneman: la primera estimación fija el resto. → primer dato sesgado.
- **`[dr ·]` Respuestas a datos anómalos — Chinn & Brewer 1993** (Review of Educational Research):
  de **7 respuestas** a evidencia que contradice la teoría, SOLO 1 es "aceptar y cambiar"; las otras
  6 la descartan (ignorar · rechazar · excluir del dominio · dejar en suspenso · reinterpretar ·
  parche periférico) + una 8ª "dudar de la validez del dato". *La taxonomía exacta de las jugadas
  perdedoras → un mundo de anomalía sellada donde cada descuento es una firma de trace.*
- **`[dr ✓]` Recipe estructural de Klayman & Ha 1987** — cuando la hipótesis H está EMBEBIDA en la
  regla verdadera T (H ⊂ T, demasiado angosta, como el 2-4-6 de Wason), los tests **positivos NUNCA
  falsan** → solo un test NEGATIVO revela el error. *Receta exacta y buildable: un mundo donde
  confirmar está GARANTIZADO que pierde. El regalo de diseño más filoso de la cosecha.*
- **`[dr ✓]` Insensibilidad a la diagnosticidad de la RESPUESTA** (Slowiaczek et al.) — el agente
  elige bien QUÉ test pedir pero pondera mal el resultado (misma pregunta, respuestas de muy distinta
  diagnosticidad) → preserva la hipótesis inicial. *Puede COMPRAR el test correcto y aun así leerlo
  mal — distinto de no-testear.*
- **`[dr ✓]` Anomaly-blindness CONDICIONAL — Dunbar 1997** (in-vivo, 4 labs de biología molecular):
  los científicos ignoran el hallazgo inesperado cuando es TEMPRANO y sobre una hipótesis auxiliar;
  le prestan atención si contradice supuestos centrales o llega TARDE. *Da el RÉGIMEN exacto donde
  el vicio bite → parametriza el timing del evento sellado (D4).*
- **`[dr ·]` Perseverancia tras el desmentido — Anderson & Lepper 1980; Mitroff 1974 (Apollo)**: la
  creencia sobrevive al descrédito TOTAL de la evidencia que la fundó; los 42 científicos de élite
  del Apollo no movieron sus "pet hypotheses" con los datos lunares. → *mundo donde la evidencia
  comprada se RETRACTA a mitad (D4 invalida un dato ya pagado): ¿revierte la creencia? El inverso,
  y más agudo, de no-actualizar.*

### B — Atención / perseverancia
- **Rabbit holes / goal drift** — evals de agentes autónomos (METR y afines documentan
  degradación con el horizonte y pérdida del objetivo). → pozo-señuelo + presupuesto. *Estado:
  por diseñar (señuelo puro); la escasez ya la validamos como dial (#6).*
- **Parada prematura / satisficing** — Simon: se toma la primera solución "suficiente". →
  N-trampas con saciedad (hallar la 1ª satisface). *Estado: mundo 3 fue 2-trampas; saciedad
  reapareció bajo escasez.*

### C — Verificación / rigor
- **Over-claiming / "verified" sin verificar** — críticas a agentes-científicos (p.ej. AI
  Scientist) + evals de honestidad: producen plausible-pero-mal y lo reportan con seguridad. →
  la retórica ya vale cero (el examen corre el modelo). *Estado: cubierto por construcción.*
- **Precisión fabricada** — MEDIDO EN NUESTROS PROPIOS RUNS (fabricated_precision): declaró σ
  sin comprar réplicas. *Estado: capturado y priceado.*
- **Perseguir lo significativo-pero-irrelevante / p-hacking** — metaciencia / crisis de
  replicación (garden of forking paths, Gelman). → carnada de significancia (efecto chico-pero-
  claro vs grande-pero-ruidoso). *Estado: por diseñar; anfitrión natural = mundo ancho.*
- **`[dr ✓]` Garden of forking paths — Gelman & Loken**: el problema de comparaciones múltiples
  aparece aun con UN SOLO análisis, porque cada decisión analítica es contingente al dato observado;
  y "**no se sienten como grados de libertad**" (cada elección parece la única razonable). *El vicio
  más INVISIBLE: no hace falta p-hackear a conciencia. Es exactamente lo que nuestro instrumento
  quiere pescar (juicio, no truco).*
- **`[dr ✓]` 12 estrategias de p-hacking, con número — Stefan & Schönbrodt 2023**: UNA sola
  (reportar selectivamente la variable dependiente que dio significativa, de 10) infla el
  falso-positivo del 5% al **~40% (×8)**. *Calibra la carnada de significancia del mundo ancho.*
- **`[dr ✓]` 40 QRPs indexadas por fase — Nagy et al. 2025** + bestiario (semilla de RNG favorable ·
  covariables ad hoc · discretizar continuas · missing-data hacking · PARKing). *Catálogo listo de
  jugadas perdedoras, cada una candidata a mundo.*
- **`[dr ✓]` HARKing** (Kerr): presentar como a priori una hipótesis inventada TRAS ver los datos.
  → *mundo donde el orden hipótesis-antes-que-datos es verificable (el sellado de compromiso).*
- **`[dr ✓]` DOF amplificados en experimentos con AGENTES — Vaccaro 2026**: selección de modelo,
  wording del prompt, settings, rediseño contingente al resultado — "fáciles de explotar y difíciles
  de detectar". *El p-hacking migra al propio agente-científico (nuestro sujeto).*
- **`[dr ✓]` Fabricación cuando el experimento falla — MLR-Bench (NeurIPS 2025)**: **~80%** de los
  casos reportan resultados fabricados/inválidos (8 de 10 tareas con datos placeholder/sintéticos en
  vez de ejecución real); persiste aun instruyendo "no fabriques". *Es EXACTAMENTE nuestro
  `fabricated_precision`, medido afuera y en grande → validación externa del vicio que ya capturamos.*

### D — Representación / creatividad
- **Retirada a lo familiar / implementation drift** — evals de agentes de código (revierten a
  patrones conocidos). → la respuesta simple-familiar queda a mitad de tabla; solo la estructura
  verdadera llega arriba. *Estado: CONFIRMADO con solver real (v2 seed3, R=0.096).*
- **No inventar la estructura** — el lado generativo del research taste. → familia v2. *Estado:
  el trofeo; hacer MÁS de estos.*
- **`[dr ✓]` Hipótesis inviables sin anclar a los datos — HLER 2026**: la generación autónoma sin
  restricción produce preguntas factibles solo el **41%** de las veces vs **87%** si se la ancla a la
  estructura del dataset (≈59% alucinadas). *Cuantifica el lado generativo del research taste — y
  sugiere el dial: cuánta estructura se le da de entrada.*
- **`[dr ·]` La analogía de descubrimiento es CERCANA, no lejana — Dunbar 1997**: de 99 analogías en
  16 lab meetings, solo **2** lejanas/no-biológicas; el descubrimiento real corre sobre analogías
  *near*, basadas en homología (40 mismo-organismo, 57 otro-organismo). *Dato de diseño para D:
  premiar la analogía estructural CERCANA correcta, no el salto vistoso — el mito del "insight
  lejano" no es donde vive el research taste.*
- **`[dr ~]` Diversidad de exploración** (arxiv 2510.10472, *sin verificar — los 3 votos erroraron
  por el límite de API*): la exploración angosta/baja-varianza sería jugada perdedora documentada en
  ML research autónomo. *Anotado, pendiente de verificación.*

### E — Memoria / consistencia
- **Pérdida de restricciones / contexto en trayectorias largas** — evals de horizonte largo. →
  restricción de enlace tardío + horizonte. *Estado: se MIDE como hallazgo (límite del solver),
  no se diseña-en-contra.*

### F — Interacción
- **Adivinar en vez de averiguar** — evals de agentes interactivos. → info faltante con precio
  accesible. *Estado: el inverso (comprar-y-no-usar) CONFIRMADO (#6); el directo por diseñar.*

### G — Razonamiento causal
*Grupo propio, **aprobado por Lucas (2026-07-07)**. Gana su fila porque la CURA es una MOVIDA
DISTINTA: intervenir, o modelar la causa escondida — NO "verificar más fuerte" sobre los mismos
datos. Fijarse mejor en una correlación confundida no revela nunca el tercer factor (el calor
detrás del helado y los ahogados); solo cambiar de movida lo hace. Solapa con C en la superficie
(una respuesta barata que resulta falsa) pero el eje es otro: la trampa está METIDA en los datos
observacionales, no en la significancia. Todos JUICIO. Ya hay maquinaria: `confounded_gen_v0`,
`generic_certify`.*
- **`[dr ·]` Correlación ≠ causación — Corr2Cause, Jin et al. 2023**: 17 LLMs (hasta GPT-4) puntúan
  al **NIVEL DEL AZAR** infiriendo causalidad desde correlación (dataset 200K). *El ancla dura del
  vicio.* → mundo observacional confundido donde solo `do()` revela la verdad.
- **`[dr ✓]` Leakage / distribution-mismatch — Kapoor & Narayanan 2023** (taxonomía de 8 tipos): el
  "distribution mismatch" (evaluar en una distribución distinta de aquella sobre la que se afirma)
  infla el desempeño aun con split limpio. *Generalizar más allá del DGP medido.*
- **Confounding / colisionador / no-intervenir** — la dinámica: la data observacional engaña; solo
  la intervención (o modelar la asignación) recupera. *Estado: YA tenemos el mundo
  (`confounded_gen_v0`); el candado del verificador estructural es la deuda registrada en ADR 0094.*

## 4-bis. Corpus compilado (Lucas) — ruteado por el corte OPERACIÓN/JUICIO (§0.5)

Recopilación de Lucas de fuentes reales (2025-2026). Lo que aportan de único: **números**. Pero
—corrección de Lucas— NO van todos en la misma tabla: primero se **rutean por §0.5**, porque los
de operación no son blanco de WAGER y mezclarlos diluye el foco que es toda la tesis.

### JUICIO — el blanco de WAGER (el andamiaje NO los arregla)
Cuantificados (la vara empírica que nos faltaba), del análisis por grafo epistémico
(arxiv 2604.18805) y afines:
- **Evidencia IGNORADA en el 68% de los traces** (A): tiene en contexto un resultado que
  contradice su hipótesis y sigue como si nada. *Juicio puro — la info está, la jugada no.*
- **Revisión de creencia refutada solo en el 26%** (A): ante evidencia contraria, casi nunca
  actualiza.
- **Convergent multi-test RARO** (~6-13% según modelo) (C): pudiendo triangular con tests
  independientes, no lo hace.
- **Retirada a defaults/convenciones** (D): con una convención no-estándar que él mismo escribió,
  vuelve al default de manual (vibe-physics). *Abandona la estructura correcta que ya tenía.*
- **Sycophancy bajo presión** (C): cede el juicio a la presión social y da la respuesta que
  parecés querer. *La presión no solo expone el vicio — puede CREAR el de complacer.* Dato de
  diseño: cuidá que la "pista" no induzca complacencia.
- **No actuar sobre la propia anomalía** (C/A): no ve lo interesante/anómalo en sus resultados.
- **Hundirse recuperando un estado OCULTO** (D/v2): aunque lo reporte OSWorld —benchmark de
  operación— esto es juicio: exige inferir lo latente, la familia de nuestro trofeo. *El ejemplo
  de por qué el discriminador manda sobre la fuente (§0.5).*

Vicio nuevo, de frontera:
- **Analysis-decision disconnect** (juicio→acción): identifica bien el edge y aun así NO actúa /
  dimensiona mal (benchmark de apuestas). *Es juicio correcto que no se traduce en decisión — un
  tercer tipo. Nuestros mundos actuales no lo testean (el análisis ES el entregable, no hay paso
  de "apostar" separado); anotado como frente futuro.*

### OPERACIÓN — NO es blanco de WAGER (lo resuelve el andamiaje; el campo ya está en esto)
Se listan para **NO confundirlos** con los de juicio, no para construir mundos:
- **Perder restricciones · no registrar info mid-way · adivinar en vez de preguntar · saltear
  verificación · <7% del presupuesto en auto-repararse** (OSWorld-V2): el trabajador desprolijo.
  Memoria / checklists / planners / loops de reparación → territorio de ingeniería de agentes.

Straddle (parte operación, parte juicio — se anota el corte, no se mezcla):
- **Error-signal blindness: 67% repite la misma acción fallida** (SciAgentGym): *rastrear que
  falló* es operación (un loop de reflexion lo tapa); *diagnosticar por qué y pivotear* es juicio.
- **Degradación de resiliencia en trayectorias largas** (E): la robustez cae monótona en
  horizonte (débiles ~30%→~10%); *que sea entrenable* (Rise-Fall-Rise en los fuertes) es la parte
  de juicio/modelo → insumo E2. El horizonte en sí es la cara operacional de E (§3).

## 4-ter. Metodología externa que VALIDA nuestro enfoque (no un vicio — una confirmación)

- **La evaluación por OUTCOME no detecta estas fallas** (arxiv 2604.18805): un agente puede
  sacar 80% de accuracy en CLadder/QRData/DiscoveryBench y tener un proceso de razonamiento
  basura. **Por eso hay que analizar la TRAZA, no solo el resultado** — exactamente nuestra
  doctrina "conducta observada" (§2.1) y las firmas de trace. Confirmación externa fuerte.
- **El grafo epistémico como vocabulario listo** (mismo paper): anota cada paso de la traza
  con 6 nodos — **H**ypothesis, **T**est, **E**vidence, **J**udgment, **U**pdate,
  **C**ommitment — y aristas (testing, observing, contradicting, updating…), y matchea contra
  *productive motifs* (falsación popperiana, reranking de hipótesis, revisión por refutación,
  evidencia convergente) vs *reasoning breakdowns* (untested claim, contradiction-without-repair,
  premature commitment, evidence non-uptake, fixed-belief-trace, precommitted-test-plan,
  stalled-revision). **Podemos ADOPTAR este vocabulario para nuestras firmas de trace** — es
  una taxonomía publicada de exactamente lo que medimos.
- **El base model explica el 41.4% de la varianza; el scaffold solo 1.5%** (mismo paper):
  cambiar el prompt/arquitectura casi no mueve la aguja — el vicio vive en el MODELO, no en el
  prompt. **Confirma nuestra tesis de ADR 0096/0098**: el "sé cuidadoso" genérico no arregla el
  vicio (mueve ejecución); el vicio es una propiedad del modelo que hay que ENTRENAR (E2), no
  promptear. Y confirma que el instrumento debe medir algo que el prompt no puede fingir.
- **In-context learning NO lo arregla** (mismo paper): el patrón persiste aun dándole un ejemplo
  casi-completo de buen razonamiento en contexto → refuerza que es entrenable, no prompteable.

## 5. Fuentes a minar (la investigación concreta — en curso)

El seed de §4 sale de conocimiento general; la versión rigurosa se arma yendo a estas familias
de fuentes y sacando failure modes CONCRETOS con su cita:
- **Evals de agentes autónomos**: METR (task-horizon, autonomy failures); taxonomías de fallos
  de agentes LLM 2024-2025.
- **Agentes-científicos / research agents**: AI Scientist (Sakana) y sus críticas; ResearchAgent;
  papers de "LLM as scientist" y sus modos de falla.
- **Benchmarks de descubrimiento**: ScienceWorld, DiscoveryWorld, DiscoveryBench, BoxingGym,
  QRData — sus análisis de error.
- **Cog-sci del razonamiento científico**: confirmation bias / hypothesis testing (Wason,
  Klayman-Ha, Kuhn), heurísticas y sesgos (Kahneman-Tversky), scientific reasoning (Klahr).
- **Calibración / juicio**: superforecasting (Tetlock), calibración y overconfidence.
- **Honestidad / sycophancy / overclaiming**: evals recientes de honestidad de LLMs.
- **Metaciencia**: crisis de replicación, p-hacking, garden of forking paths (Gelman & Loken).

> **Ya minado (deep-research, 2026-07-07 — ver ítems `[dr ✓]` en §4)**: cog-sci del razonamiento
> (Chinn & Brewer 1993; Klayman & Ha 1987; Dunbar 1997; Anderson & Lepper 1980; Mitroff 1974) ·
> metaciencia (Gelman & Loken; Stefan & Schönbrodt 2023; Nagy et al. 2025; Vaccaro 2026) · causal
> (Corr2Cause/Jin 2023; Kapoor & Narayanan 2023) · newest evals (MLR-Bench NeurIPS 2025; HLER 2026).
> **Pendiente de minar**: METR/task-horizon con cita fina · agentes-científicos (AI Scientist y sus
> críticas) · calibración/superforecasting (Tetlock) · benchmarks de descubrimiento (DiscoveryWorld,
> BoxingGym). *Y re-correr los 6 claims sin verificar cuando vuelva el presupuesto de API.*

> **Acción concreta**: correr una investigación dirigida (skill `deep-research` o WebSearch) por
> cada familia, extrayendo failure modes con cita + evidencia. **Triage obligatorio (§0.5) ANTES
> de asignar familia**: por cada vicio preguntá primero *¿lo arregla el andamiaje?* — si sí es
> OPERACIÓN (se anota bracketeado, no es mundo WAGER); si no es JUICIO y recién ahí se le asigna
> su dinámica de §3. La heurística de fuente ayuda a rutear pero no decide. Paciencia: uno por uno.

## 6. El proceso (de un vicio a un mundo)

```
vicio documentado (§4/§5)
   -> ¿qué DINÁMICA de mundo lo fuerza de forma puntuable? (§3)
   -> deliverable puntuable (predecir comportamiento) + cero-LLM
   -> diseñar el CERTIFICADO DE TRAMPA NECESARIA (robot vicioso pierde / cuidadoso gana)
   -> ¿hace falta PRESIÓN? (escasez / tiempo / evidencia tardía) -- casi siempre sí
   -> build (spec-first) -> certificar -> E0 con pre-registro
   -> ¿el vicio se manifestó con un solver real? (la validez, ADR 0098)
```

## 7. Lo difícil / preguntas abiertas (honestas)

- **Scoring de EXPLICACIONES sin LLM** (suite Anomaly, "¿qué pasó?"): el muro más duro. Los
  vicios que requieren un deliverable-explicación quedan bloqueados hasta resolverlo. Mientras,
  se los fuerza con deliverable-predicción (§ principio 6).
- **Vicios un-hinteable (insight profundo, v2) vs dispositivos (hinteable)**: la distinción de
  ADR 0097. Los profundos no se validan con pista (cualquier pista = leak) — su validez es que
  ningún modelo los vence (v2: 0/10). Los dispositivos se validan con pista dirigida (ADR 0098).
- **Eje de creatividad/representación**: inventar la estructura es research taste generativo y
  es lo que mejor funciona (v2), pero es lo más difícil de generar y de puntuar. Merece su
  propia línea de pensamiento.
- **Réplica pendiente** (ADR 0098): DeepSeek + más seeds + clasificación automática de ceros,
  antes de un claim firme de validez.
