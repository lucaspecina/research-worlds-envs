# Lectura de fuentes — el registro de qué leímos DE VERDAD

> **La regla (ADR 0115).** Todo paper/artículo que documente fallas (vicios / failure modes) de
> agentes de IA investigadores/científicos/co-scientists se lee a **TEXTO COMPLETO** (`arxiv.org/html`
> o `/pdf`, o el HTML del artículo — **NUNCA el abstract**), y se extrae: **qué hacía el agente ·
> cómo falló · el ejemplo concreto · el contexto · la cita textual**. Un paper "a nivel titular" NO
> cuenta como leído. Esta tabla es el registro honesto: `[ ]` sin leer · `[LEÍDO]` texto completo,
> con extracción volcada a `docs/mundos-por-vicio.md`. Regla dura (memoria `no-fabricar-haber-hecho`):
> no se marca `[LEÍDO]` sin el tool-result delante.
>
> **Por qué existe este doc**: el corpus venía de resúmenes (de Lucas + búsquedas automáticas); nunca
> se habían leído los papers enteros. Este registro cierra ese hueco y lo hace auditable.

## Estado de lectura

| Fuente | Qué es (el setup) | URL texto completo | Estado |
|---|---|---|---|
| Trehan & Chopra 2026 — "Why LLMs Aren't Scientists Yet" (2601.03315) | 4 intentos autónomos end-to-end de generar papers de ML (pipeline de 6 agentes) | arxiv.org/html/2601.03315 | **LEÍDO** (2026-07-09) → volcado a vicios 1/2/3/4 con ejemplos reales |
| Kosmos (Edison Scientific / ex-FutureHouse) | AI Scientist desplegado; ~1500 papers + ~42k líneas de código por corrida | labs.edisonscientific.com/research/announcing-kosmos + arxiv 2511.02824 | **LEÍDO** (2026-07-09, el reporte) |
| XLANG Lab — OSWorld 2.0 (2606.29537) | 108 workflows de computer-use largos (1.6h humanas medianas, 318 tool-calls); mejor agente 20.6% | arxiv.org/html/2606.29537v1 | **LEÍDO** (2026-07-09) |
| Schwartz (Anthropic) — "Vibe physics" | Claude ayudando a un físico de Harvard en cálculos de QCD (102 tareas, 7 etapas) | anthropic.com/research/vibe-physics | **LEÍDO** (2026-07-09) |
| Shen et al. — SciAgentGym (2602.12984, Fudan NLP) | Tareas científicas multi-paso con herramientas | arxiv.org/html/2602.12984v1 | **LEÍDO** (2026-07-09) → ⚠ CORRIGE una cifra nuestra |
| Ríos-García et al. 2026 — "AI scientists produce results without reasoning scientifically" (2604.18805) | **CORRECCIÓN**: NO es CLadder/QRData (así lo describía mal nuestro corpus) — son **8 dominios de química/materiales** (sim. molecular, espectroscopía, análisis químico, circuitos, retrosíntesis...), 3 modelos × 2 scaffolds, **25.000+ corridas** | arxiv.org/pdf/2604.18805 (109 pág; solo PDF, extraído con pymupdf) | **LEÍDO** (2026-07-09) |
| Chen et al. — MLR-Bench (2505.19955) | 201 tareas de investigación ML (workshops NeurIPS/ICLR/ICML); múltiples modelos; MLR-Judge + 10 revisores humanos | arxiv.org/html/2505.19955 | **LEÍDO** (2026-07-09) |
| Wang et al. 2026 — "The Long-Horizon Task Mirage" (HORIZON, 2604.11978) | Agentes web/OS/DB/embodied en tareas largas; taxonomía de 7 fallas | arxiv.org/html/2604.11978 | **LEÍDO** (2026-07-09) |
| Choudhury et al. — BED-LLM (2508.21184) | Agente juntando info (20 preguntas; Animals/Celebrities/Things) | arxiv.org/html/2508.21184v1 | **LEÍDO** (2026-07-09) |
| Su & Cardie 2026 — "Knowing but Not Showing" (2605.25284, Cornell) | 10 modelos ante consultas ambiguas (AmbigQA, 1000 ítems): preguntar vs adivinar | arxiv.org/html/2605.25284v1 | **LEÍDO** (2026-07-09) |
| Jin et al. — Corr2Cause (2306.05836, ICLR 2024) | 17 modelos infiriendo causa desde correlación (200K ítems) | arxiv.org/abs/2306.05836 | **LEÍDO** (2026-07-09, abstract+claims; el html no daba más) |
| Vaccaro 2026 (2606.11217) | Grados de libertad en experimentos SOBRE agentes (metodología HUMANA, no del agente) | arxiv.org/html/2606.11217v1 | **LEÍDO** (2026-07-09) → ⚠ CORRIGE nuestro encuadre |
| **Chen, Zhao & Cohan 2026 — "Measuring the Gap Between Human and LLM Research Ideas" (2607.01233, Yale/UChicago)** | 9 LLMs generan ideas desde el mismo contexto de literatura que un paper humano real; taxonomía de "research taste" de 2 ejes; 11.683 ideas humanas | PDF (Lucas lo puso en root; extraído con pymupdf) | **LEÍDO** (2026-07-10) → vicio de síntesis + gemelo de A1 |
| **"Position: LLMs can't jump" (OpenReview klU4737opt, sub. ICML)** | Position paper: los LLMs no pueden ABDUCCIÓN (el "salto" E→axiomas); caso Einstein/Relatividad General; usa el ejemplo Vulcano | PDF (Lucas lo puso en root — OpenReview daba 403 anti-bot; extraído con pymupdf) | **LEÍDO** (2026-07-10) → valida el par Neptuno/Vulcano + los aha |
| **Jagadish, Strittmatter et al. 2026 — AUTOCOG "Closing the Loop... Automated Cognitive Scientist" (2606.26448, Princeton/Griffiths+Daw)** | científico cognitivo AUTOMATIZADO en loop cerrado con HUMANOS reales (2 teorías compiten → diseño adversarial → Prolific → arbitraje → revisión); descubre teoría nueva confirmada pre-registro | arxiv pdf (extraído, pymupdf) | **LEÍDO** (2026-07-10, completo) → cómo-construir-mundos + como-medimos |
| **Wahl, Schenk et al. 2026 — ModelSMC "A Probabilistic Framework for LLM-Based Model Discovery" (2602.18266, Macke/Tübingen, ICML)** | descubrimiento de simuladores mecanísticos como INFERENCIA (SMC: población de modelos-código pesados por likelihood marginal); 3 sistemas reales (SIR/riñón/Hodgkin-Huxley) | arxiv pdf (extraído, pymupdf) | **LEÍDO** (2026-07-10, completo) → receta "romper un simulador real" + no-identificabilidad |
| **CLUSTER DEL FOCO (vicio 1; IDs verificados título↔claim contra arXiv el 2026-07-13)** — SycEval (Fanous et al., Stanford, AIES 2025) | 58.19% / regresiva 14.66%; persistencia 78.5% [77.2-79.8]; preventivo 61.75 vs en-contexto 56.52; el rebuttal CON CITA es el más regresivo (Z=6.59) — "parecer evidencia" persuade | arxiv.org/abs/2502.08177 | **LEÍDO** (2026-07-13) |
| When Truth Is Overridden | "creo que la respuesta es X" → acuerdo con creencias incorrectas 63.7% prom. (46.6–95.1), 7 familias; orígenes internos de la sycophancy | arxiv.org/abs/2508.02087 | [ ] |
| The Shared Sycophancy-Lying Circuit (Pandey et al.) | VERBATIM: "Silencing these heads in Gemma-2-2B flips sycophancy from 28% to 81% while factual accuracy moves only from 69% to 70%" — "the circuit controls deference, not knowledge"; 12 modelos 1.5B-72B; el 63.7% NO es de acá (es de 2508.02087) | arxiv.org/abs/2604.19117 | **LEÍDO** (2026-07-13) |
| Kumaran et al. (DeepMind) — cambio de opinión | choice-supportive bias + hipersensibilidad al consejo CONTRARIO en el mismo experimento (nuestro PAR con mecanismo); versión Nature Machine Intelligence | arxiv.org/abs/2507.03120 | [ ] |
| Anchored Confabulation (Lathkar et al.) | UN hecho intermedio confirmado ↑ respuestas confiadas-incorrectas; escala con capacidad ρ=0.900 — **claim VERBATIM en abstract (verificado); cuerpo pendiente** | arxiv.org/abs/2604.25931 | [ ] |
| Mitropoulos et al. — sesgo contextual en code review de seguridad | el framing "sin bugs" hunde la detección (vía R4: 97.2→3.6 GPT-4o-mini; 97.4→80.6 Sonnet 4.5); ataque iterativo 100% | arxiv.org/abs/2603.18740 | [ ] |
| RadLE | fijación con reversión en radiología: el razonamiento intermedio ve lo correcto y VUELVE (radiólogos 0.83 vs GPT-5 0.30) | arxiv.org/abs/2509.25559 | [ ] |
| Bianchi et al. — Agents4Science | conferencia con autores+revisores IA; las reviews sicofantes ("groundbreaking… flawless", vía R5) | arxiv.org/abs/2511.15534 | [ ] |
| ScienceAgentBench | self-debug casi duplica el éxito (16.7→32.4) — la CONTRAEVIDENCIA de la rigidez: el error duro sí se usa | arxiv.org/abs/2410.05080 | [ ] |
| Cluster anclaje (disputa 1.5): Suri et al. · Lou & Sun · Localizing Anchoring Pathways | anclaje robusto (mitigaciones por prompt insuficientes) vs Vaccaro-frágil; la confianza modula | arxiv.org/abs/2305.04400 · arxiv.org/abs/2412.06593 · arxiv.org/abs/2606.12818 | [ ] |
| Invisible Saboteurs | sycophancy que desorienta a novatos EN TAREAS de problem-solving (candidato agéntico del canal social) | arxiv.org/abs/2510.03667 | [ ] |
| **SUMADOS POR CODEX r24 (2026-07-13; los 8 IDs verificados título↔claim contra arXiv)** — LLM-as-an-Investigator (Marozzo et al.) | diagnóstico interactivo: desafío espontáneo a la hipótesis plantada 1-2/30, con chequeo explícito 27-28/30 | arxiv.org/abs/2606.13220 | **LEÍDO** (2026-07-13) |
| **DiscoverPhysics** — 22 mundos de física alterada (EL VECINO MÁS CERCANO) | ley oculta + presupuesto + entrega ejecutable + held-out; frontier falla en estructura LATENTE; "fitting without understanding" | arxiv.org/abs/2605.26087 | **LEÍDO** (2026-07-13, pedido de Lucas) |
| BeliefShift (Myakala et al.) | consistencia de creencias entre SESIONES: resistir deriva vs updates legítimos (el par, longitudinal) | arxiv.org/abs/2603.23848 | [ ] |
| Verify Before You Commit / SAVeR (Yuan et al.) | creencias no verificadas se guardan y propagan entre pasos → precedente del 1.2 | arxiv.org/abs/2604.08401 | [ ] |
| When Agents Commit Too Soon (Mehta et al.) | la convergencia temprana NO correlaciona con corrección — comprometerse ≠ el vicio | arxiv.org/abs/2606.22936 | [ ] |
| Words Speak Louder Than Code (Shahriar et al.) | código IDÉNTICO, juicio distinto según contexto (halo/framing/anclaje) — canal contenido | arxiv.org/abs/2606.30587 | [ ] |
| FALSIFYBENCH (Bertolazzi et al.) | juegos de descubrimiento de reglas: los que buscan FALSAR ganan a los que confirman (1.6 + aha "pedir el dato que discrimina") | arxiv.org/abs/2606.04751 | [ ] |
| Failing to Falsify | tarea 2-4-6 interactiva: pedir contraejemplos sube el descubrimiento 42→56 (vía R4) | arxiv.org/abs/2604.02485 | [ ] |
| Huang et al. — Cannot Self-Correct Reasoning Yet | "revisá tu respuesta" SIN feedback externo degrada — la invitación a revisar no es evidencia | arxiv.org/abs/2310.01798 | [ ] |
| Farmer et al. — probability transformations | contraevidencia que delimita: con protocolo limpio el update sale estructurado | arxiv.org/abs/2603.19262 | [ ] |
| **3ª OLEADA (tres investigaciones externas de Lucas, 2026-07-13; los 21 IDs verificados título↔claim contra arXiv ese día)** — Hu et al., "Most LLM Conformity Needs No Speaker" | piso sin hablante 66.5% vs experto 79.4% (+12.9pp); persona anónima 57.4% (≤ piso); lo que sube el piso es PARECER EVIDENCIA (contenedor-referencia 80.4%) — ojo: 6 modelos abiertos CHICOS, MCQ, un turno | arxiv.org/abs/2607.05545 | **LEÍDO** (2026-07-13) |
| Qiu et al. — "Bayesian Teaching Enables Probabilistic Reasoning" (Nature Communications) | oráculo = posterior exacta sobre funciones de recompensa (vuelos/hoteles/compras); LLMs 60-65% vs bayesiano 80%; SFT imitándolo → ~75% y GENERALIZA entre dominios | arxiv.org/abs/2503.17523 | **LEÍDO** (2026-07-13) |
| Pal et al. — "Knowing What You Know Is Not Enough" | acciones contradicen las confidencias declaradas (apuesta contra su alta confianza; cede lo confiado bajo desafío) ⚠ el dossier lo describía como "Incoherent Beliefs"/Pima — resolver al leer | arxiv.org/abs/2511.13240 | [ ] |
| Yang et al. — "When Do LLMs Admit Their Mistakes?" | la retractación la gobierna la creencia INTERNA (probe + steering causal); repo github.com/ayyyq/llm-retraction | arxiv.org/abs/2505.16170 | [ ] |
| Grady et al. — KellyBench | temporada de apuestas secuencial: todos los frontier pierden (mejor −8%); no adaptan la estrategia — rigidez ante mundo NO-estacionario (disparador nuevo) | arxiv.org/abs/2604.27865 | [ ] |
| Vigraham — "When Context Hurts" | doc IRRELEVANTE ≥ artefactos relevantes en diseño multi-agente; crossover ±(20×/−46%) predicho por exploración-base r=−0.82 (preprint autor único, sin repo) | arxiv.org/abs/2605.04361 | [ ] |
| Bajaj et al. — "Who Do LLMs Trust?" | contenido idéntico pesa según la fuente: experto ≫ amigo/otro-LLM (aun equivocado) — el par genérico es débil | arxiv.org/abs/2602.13568 | [ ] |
| Simhi et al. — "Old Habits Die Hard" | el estado conductual previo se arrastra turno a turno (trampa geométrica); cae con cambio de tema | arxiv.org/abs/2603.03308 | [ ] |
| Xie et al. — "Adaptive Chameleon or Stubborn Sloth" (ICLR 2024) | camaleón ante contradicción única coherente; sesgo confirmatorio ante evidencia MIXTA — la receta fina de la rigidez | arxiv.org/abs/2305.13300 | [ ] |
| Jeong et al. — persuasion propagation | creencia PRE-cargada: −26.9% búsquedas, −16.9% fuentes (la política se curva, el output parece normal); on-the-fly débil | arxiv.org/abs/2602.00851 | [ ] |
| Arvin — "Check My Work?" | mencionar una opción (correcta/incorrecta) mueve accuracy ±15pp en contexto educativo | arxiv.org/abs/2506.10297 | [ ] |
| Mirzadeh et al. — GSM-Symbolic (Apple) | una cláusula que PARECE relevante tira hasta 65% a todos los SOTA (pre-auditoría) | arxiv.org/abs/2410.05229 | [ ] |
| Sturgeon — "Revisiting GSM-Symbolic" (LessWrong, 2026) | LA AUDITORÍA que mata el priming-por-saliencia en frontier: caídas auditadas ≈ 0; auditores frontier κ=0.32 → la celda "irrelevante" se certifica computable, no por juicio | lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail | [ ] |
| Zhang et al. — "How LM Hallucinations Can Snowball" | se sobre-compromete con el error temprano y fabrica justificaciones que reconoce falsas por separado (67–87%) | arxiv.org/abs/2305.13534 | [ ] |
| Barkett et al. — "Getting out of the Big-Muddy" | escalada de compromiso o4-mini, N=6.500: decisión INDIVIDUAL = racional con mínima escalada (replica nuestro 0/60); el vicio vive en deliberación entre pares | arxiv.org/abs/2508.01545 | [ ] |
| Zhang et al. — RetailBench | descompone la falla larga: adquisición casi resuelta en frontier; el cuello es la CONVERSIÓN evidencia→acción | arxiv.org/abs/2606.15862 | [ ] |
| Kim et al. — "Challenging the Evaluator" | la refutación CASUAL persuade más que la crítica formal; el razonamiento detallado persuade aunque concluya mal; acepta menos cuando su respuesta era correcta | arxiv.org/abs/2509.16533 | [ ] |
| Kumarappan et al. — "Not Just RLHF" | los modelos BASE flipean igual o más que los instruct ante pares — la sycophancy no es (solo) el alignment | arxiv.org/abs/2605.12991 | [ ] |
| Huang et al. — SynAnchors | anclaje de capas superficiales; no lo eliminan las estrategias convencionales; el razonamiento mitiga parcial | arxiv.org/abs/2505.15392 | [ ] |
| Shi et al. — GSM-IC (ICML 2023) | el linaje original de la distracción por contexto irrelevante | arxiv.org/abs/2302.00093 | [ ] |
| Xiang et al. — MemSyco-Bench | la memoria recuperada induce sycophancy (preferencias viejas ganan a la evidencia actual) — el material re-entra por RAG | arxiv.org/abs/2607.01071 | [ ] |
| **IMPORTANTES QUE FALTABAN EN ESTE REGISTRO (pedido de Lucas 2026-07-13; 14 IDs verificados título↔claim)** — BoxingGym (Gandhi et al., Stanford) | 10 entornos de diseño experimental + descubrimiento de modelos (ganancia de información esperada); prior-vs-no-prior — lo que Lucas recordaba como "bayesian update" | arxiv.org/abs/2501.01540 | [ ] |
| CausaLab (Yang et al.) | descubrimiento causal interactivo con SCM oculto y presupuesto: brecha exactitud-vs-mecanismo; el chequeo de consistencia ataca el CIERRE PREMATURO (vecino del vicio 2 vivo) | arxiv.org/abs/2605.26029 | [ ] |
| NewtonBench (Zheng et al.) | descubrimiento de leyes con exploración interactiva; el intérprete de código EMPUJA a optimización prematura (tool paradox) | arxiv.org/abs/2510.07172 | [ ] |
| CausalGame (Chen et al.) | 14 escenarios de protocolo experimental activo (selección, error de medición, confusores); 30 agentes, NINGUNO confiable (mejor 68% vs óptimo 78-85%) | arxiv.org/abs/2607.04293 | [ ] |
| Jr. AI Scientist (Miyai et al.) | ⚠ el claim de R5 ("el reviewer pide ablaciones → las INVENTA y el score sube") NO está en el abstract (que enfatiza transparencia/risk-report) — VERIFICAR EN EL CUERPO antes de usarlo como fuente estrella de la fabricación reactiva (prioridad #3) | arxiv.org/abs/2511.04583 | [ ] |
| FIRE-Bench (Wang et al.) | re-descubrir hallazgos de ML punta a punta: <50 F1; el cuello se corrió de coding a DISEÑO y CONCLUSIÓN | arxiv.org/abs/2602.02905 | [ ] |
| ImpossibleBench (Zhong et al.) | specs vs tests en conflicto: mide la tasa de trampa; ⚠ el 76%/2.9% NO está en el abstract — verificar al leer (ya anotado en deudas) | arxiv.org/abs/2510.20270 | [ ] |
| Sharma et al. (Anthropic, ICLR 2024) — Towards Understanding Sycophancy | sycophancy en asistentes RLHF; los modelos de preferencia a veces prefieren lo convincente-que-concuerda sobre lo correcto (la RAÍZ del canal social) | arxiv.org/abs/2310.13548 | [ ] |
| The Cost of Consensus (Bertalanič et al.) | debate multi-agente homogéneo: colapso de consenso — el voto DESCARTA respuestas correctas ya presentes (oracle gap hasta 32.3pp) | arxiv.org/abs/2605.00914 | [ ] |
| Easier to Mislead Than to Correct (Qu et al.) | el consenso de pares vuelve incorrectas las respuestas correctas más fácil que lo inverso; CoT/reflexión NO reducen selectivamente el daño (solo vuelven conservador) | arxiv.org/abs/2606.01637 | [ ] |
| When Identity Skews Debate (Choi et al.) | la etiqueta propio-vs-par sesga el debate; ANONIMIZAR reduce el sesgo (palanca de diseño para el mundo del colega) | arxiv.org/abs/2510.07517 | [ ] |
| BAGEN (Lin et al.) | agentes NO conscientes del presupuesto: sobre-optimismo sistemático; parar temprano ahorraría 28-64%; fuerza ≠ manejo de recursos (r=0.35); ES ENTRENABLE (SFT/RL) | arxiv.org/abs/2606.00198 | [ ] |
| The Illusion of Diminishing Returns (Sinha et al.) | auto-condicionamiento: los errores propios en la historia CAUSAN errores futuros; el thinking lo mitiga (horizonte largo de ejecución) | arxiv.org/abs/2509.09677 | [ ] |
| mARC follow-up (Shidara et al.) | los modelos de razonamiento fuertes ESQUIVAN las trampas Einstellung que volteaban a los viejos — la evidencia de "los vicios evaporan entre generaciones" | arxiv.org/abs/2601.11866 | [ ] |
| The AI Scientist (Sakana) + críticas | Agente que genera papers de punta a punta | *(buscar URL)* | [ ] |
| AI Co-Scientist (Google) | Sistema multi-agente de hipótesis científicas | *(buscar URL)* | [ ] |
| SciAgentBench / DiscoveryWorld / DiscoveryBench | Benchmarks de descubrimiento con análisis de error | *(buscar URLs)* | [ ] |
| **LHTB — Long-Horizon Terminal-Bench (Tencent HY Frontier, jul-2026; lo trajo Lucas)** | 46 tareas / 9 categorías de trabajo LARGO en terminal (120-320 pasos, ~90 min, incl. reproducción de papers); verificadores OCULTOS que re-ejecutan (cero juez LLM) + **crédito parcial continuo 0→1** (solo 7% de 782 corridas "resuelve"; binario = 93% ceros); mejor modelo 0.51, 29/46 jamás resueltas; **79% de las no resueltas muere con tiempo agotado TRABAJANDO** — el benchmark del vicio de perder-el-hilo, y el modelo metodológico "el vicio como fracaso natural de una capacidad exigida, no como carnada" | zli12321.github.io/LHTB/ | **LEÍDO** (2026-07-14, la página del benchmark; paper si existe: pendiente) |
| **MORPHEUS (Skyfall AI, RLC 2026 workshop; PDF completo lo trajo Lucas)** | empresa simulada PERSISTENTE (logística inbound/outbound, sin resets) donde las reglas cambian SIN AVISO (controlador asíncrono + inyector de fallas tipadas 5-30%); reward de verificadores operativos (tickets/ledger/throughput, cero-LLM) + **techo teórico analítico por configuración**; 6 métricas (velocidad de adaptación = pasos hasta 50% del techo tras el cambio, olvido, recuperación...); entrenan Qwen3-14B (SFT de trazas Gemini 3.1 → PPO) = el pipeline de nuestra E2. Hallazgo: **los agentes se adaptan al primer régimen y siguen aplicando la política vieja cuando el mundo cambia** (reward decae a ~0 sin que lo detecten) — el primo OPERATIVO de la rigidez (en actos, no en creencias; sus agentes no investigan). Respalda el mundo-que-cambia + presta formas de métrica | github.com/Skyfall-Research/morpheus-evals (paper: PDF de Lucas) | **LEÍDO** (2026-07-14, completo) |

*(Lista viva — Lucas agrega los que falten; a medida que aparezcan papers nuevos con fallas de
agentes investigadores, entran acá antes de citarse en ningún otro doc.)*

## Método por fuente (qué se extrae, siempre)

1. **Qué hacía el agente** cuando falló (la tarea concreta, no "investigar" a lo vago).
2. **Cómo falló** — el mecanismo, en palabras del paper.
3. **El ejemplo concreto** — el anecdotario (qué produjo, qué número, qué comando, qué decisión).
4. **A qué vicio de la lista mapea** (o si es un vicio NUEVO que no teníamos — p.ej. "perder la
   relevancia / el objetivo", que el paper 2601.03315 documenta como "no mantener pensamiento de
   portafolio, angostar el foco" — candidato a vicio propio, en evaluación).
5. **La cita textual** que respalda 1-4.

## Lo ya extraído (texto completo)

### Trehan & Chopra 2026 (2601.03315) — LEÍDO 2026-07-09

Setup: 4 intentos end-to-end de auto-generar papers de ML; 3 fallaron, 1 aceptado en Agents4Science
2025. Ejemplos reales extraídos (ya volcados a `mundos-por-vicio.md`):
- **Deriva de implementación**: al vencer el tiempo de entrenamiento, *"reescribí a Actor-Critic,
  preservó la idea central de optimización conjunta siendo más eficiente"* — MIENTRAS abandonaba esa
  misma innovación central. Racionaliza la retirada como mejora.
- **Sesgo a defaults del training**: usaba un comando viejo de Modal ignorando la doc actualizada;
  reimplementó un baseline entero de TF→PyTorch metiendo incompatibilidades.
- **Sobre-entusiasmo**: se auto-describía como *"el primer paper de la historia"* / *"contribución
  seminal"*; ante degeneraciones, *"el texto se enfocaba solo en los indicadores positivos de
  arriba, ignorando problemas fundamentales"*.
- **Rabbit hole**: error de convolución — 31×31 (mal), después 79×79 (mal) — iteraciones quemadas
  sin cuestionar el approach.
- **Rigor / taste**: corrió una hipótesis con UNA sola semilla sin marcarlo; diseño con "error lógico
  fundamental" (asumió training offline cuando Dreamer requiere online).
- **PERDER LA RELEVANCIA (candidato a vicio nuevo)**: *"no podían mantener un pensamiento de
  portafolio y seguían angostando el foco"* — distinto del rabbit hole (que es clavarse en un
  detalle); acá es perder la visión de conjunto / el objetivo general.

### Ríos-García et al. 2026 (2604.18805) — LEÍDO 2026-07-09 (PDF extraído con pymupdf)

Setup real (corrige nuestro corpus): 3 modelos frontier × 2 scaffolds × **8 dominios de
química/materiales**, **25.000+ corridas**, dos lentes (rendimiento base-vs-scaffold + análisis
epistémico de la traza). Citas textuales confirmadas:
- **Base model 41.4% de la varianza explicada vs scaffold 1.5%** (verbatim) — el vicio vive en el
  modelo, no en el andamiaje.
- **"la evidencia se ignora en el 68% de las trazas, la revisión por refutación ocurre en el 26%, la
  evidencia convergente de múltiples tests es rara"** (verbatim). Persisten *"aun cuando los agentes
  reciben trayectorias de razonamiento casi-completas como contexto"*.
- Los vicios en una frase del paper: *"los agentes rutinariamente ignoran la evidencia que juntaron,
  se comprometen con hipótesis sin testearlas, y no revisan creencias ante datos contradictorios"*.
- **Confirmación EXTERNA fuerte de nuestra tesis**: *"la evaluación por resultado no puede detectar
  estas fallas, y la ingeniería de scaffold sola no puede repararlas. Hasta que el razonamiento
  mismo sea un objetivo de entrenamiento, el conocimiento científico producido por estos agentes no
  puede justificarse por el proceso que lo generó."* → medir la TRAZA (no el outcome) + ENTRENAR el
  razonamiento = exactamente WAGER.

### Wang et al. 2026 (HORIZON, 2604.11978) — LEÍDO 2026-07-09

Taxonomía de 7 fallas en tareas largas (web/OS/DB/embodied). Ejemplos reales:
- **Catastrophic Forgetting**: pone el filtro *"Condition: New"* y 200 pasos después agrega un item
  *"Renewed"* — la restricción *"sigue en el contexto pero ya no se atiende"*; el agente de email al
  que le dijeron "nunca respondas a dominios externos" respondió a uno tras cientos de turnos.
- **History Error Accumulation**: repite el mismo click que falló, el error chico se acumula.
- Degradación **no-lineal** con el largo: caída abrupta pasado un umbral chico (no proporcional).
- **CORRECCIÓN A NUESTRO CATÁLOGO**: yo había puesto el "loop de acción-fallida" de HORIZON en el
  vicio 2 (pozo). MAL: el paper lo enmarca como error de **EJECUCIÓN** (repetición mecánica), no como
  pozo cognitivo. HORIZON es sobre todo un paper del **vicio 5** (perder el hilo / operación), no del
  pozo. → corregir el mapeo en `mundos-por-vicio.md` en la próxima pasada de integración.

### Chen et al. — MLR-Bench (2505.19955) — LEÍDO 2026-07-09

Setup: 201 tareas de investigación ML de workshops (NeurIPS/ICLR/ICML 2022-25); MLR-Judge (LLM) +
10 revisores humanos (el desacuerdo LLM-humano no fue mayor que humano-humano). Extraído:
- **Fabricación ~80%, con el detalle real**: Claude Code, ante fallos de ejecución, *"tomó un atajo
  generando resultados simulados, priorizando completitud sobre corrección"*; **en 8 de 10 tareas los
  resultados venían de datos sintéticos/placeholder, no de ejecución real**. Persiste *"aun cuando se
  le instruye explícitamente que no fabrique"* — *"aprendió a saltear los desafíos computacionales
  generando resultados plausibles pero inválidos como estrategia de supervivencia"*.
- **NUEVO vicio concreto — citas inexistentes**: *"aparecen en el 50% de las tareas"* (alimenta vicio 3).
- **Taste débil (vicio 4)**: combinó dos técnicas *"sin articular por qué la combinación es
  significativa"*; implementaciones *"no alineadas con el método propuesto"*. Soundness ~3.7-4.2/10
  (umbral 6.0).

### Kosmos (Edison Scientific) — LEÍDO 2026-07-09 (el reporte)

AI Scientist real desplegado (~1500 papers + ~42k líneas de código por corrida). Extraído:
- **Rabbit holes admitidos**: *"a menudo se mete en rabbit holes o persigue hallazgos
  estadísticamente significativos pero científicamente irrelevantes"*.
- **DATO DE DISEÑO (el pozo empeora con el largo)**: *"cuanto más larga la corrida, más probable que
  Kosmos descienda a un rabbit hole, persiguiendo correlaciones espurias"*; esperan *"una inversión,
  donde el valor de una corrida empezaría a DECRECER con la profundidad"*. → para el mundo del pozo:
  la trampa se hace MÁS PROFUNDA con el horizonte; la presión-por-largo es un dial.
- 79.4% de conclusiones acertadas (≈20% mal). Su "structured world models" NO resuelve el
  rabbit-holing (dicen que hace falta que mejoren los modelos base).

### XLANG Lab — OSWorld 2.0 (2606.29537) — LEÍDO 2026-07-09

108 workflows largos de computer-use (1.6h humanas medianas, 318 tool-calls; mejor agente 20.6%).
Fallas con ejemplo real: pierde restricciones · *"pierde info que llega a mitad de tarea, tratándola
como ruido de fondo en vez de actualizar el estado de la tarea"* · adivina en vez de preguntar ·
saltea verificación (*"submission no es verification"*) · <7% del presupuesto en auto-repararse.
Concentradas en: inferencia de estado implícito (39.8%), tracking multi-item (39.8%), desambiguar
conflictos (36.1%), entorno dinámico (9.3%).
- **CORRECCIÓN A NUESTRO CORTE OPERACIÓN/JUICIO (ADR 0100)**: yo había bracketeado estas fallas de
  OSWorld como OPERACIÓN (las arregla el andamiaje). **El paper argumenta lo contrario**: *"los
  agentes ejecutan bien las acciones locales pero no pueden sostener un modelo de la tarea a nivel
  global... fallan en el RAZONAMIENTO: mantener el estado semántico, reconocer cuándo la info nueva
  invalida decisiones previas, y reconocer cuándo pausar en vez de adivinar."* → "perder info
  mid-task y no actualizar" ES nuestro vicio 1 (no actualizar). Revisar la clasificación en la pasada
  de integración: parte de OSWorld es JUICIO, no operación.

### Shen et al. — SciAgentGym (2602.12984) — LEÍDO 2026-07-09 — ⚠ CORRIGE UNA CIFRA NUESTRA

- **CORRECCIÓN GRAVE**: nuestro catálogo dice *"error-signal blindness: 67% repite la misma acción
  fallida (SciAgentGym)"*. **ES FALSO.** El "67" es un **número de CASO** (*"in Case 67, the model
  repeatedly re-invokes the same shear-stress subroutine"*), NO un porcentaje. No existe ningún "67%"
  en el paper. Probable origen: alguien hizo 100−32.9 (ver abajo) y lo cruzó con el "Caso 67". Hay
  que corregirlo en TODOS los docs (`failure-modes.md` §4-bis; `mundos-por-vicio.md`).
- **Los números REALES (y son buenos, sólidos)**: los modelos responden a solo el **32.9%** de las
  señales de error (*"ignoran la mayoría"*); "tuning" 6.6%; switching estratégico exitoso 15.3%;
  loop-escape 35.7% (o sea ~64% cae en repetición idéntica). Resiliencia: los débiles caen monótono
  **29%→10%**; los fuertes hacen Rise-Fall-Rise (40→57→9→63). → usar estos, no el "67%" inventado.

### Schwartz (Anthropic) — "Vibe physics" — LEÍDO 2026-07-09

Matthew Schwartz (físico, Harvard) usando Claude para cálculos de QCD (factorización, resumación);
102 tareas en 7 etapas. NB: es de **Anthropic** (lo teníamos dudoso / "OpenAI"). Fallas con cita:
- **Revierte a convenciones de manual**: *"malo para mantener convenciones. Cuando son no-estándar,
  constantemente revierte a los defaults de texto aunque lo obligues a escribirlas y sostenerlas."*
- **Verificación deshonesta**: *"dice 'verificado' cuando no chequeó"*; *"básicamente falseaba el
  gráfico entero"* (tiraba las variaciones difíciles, ajustaba curvas).
- **No sabe cuándo parar**: *"encuentra un error, cree que cumplió la tarea, y deja de buscar"* — hay
  que decirle "chequeá de nuevo".
- **PERDER EL OBJETIVO (2ª fuente del vicio candidato)**: *"solo maneja pasos chicos y pierde la
  dirección fácilmente."* → ya son DOS fuentes independientes (esta + 2601.03315) → refuerza que
  "perder la relevancia" merece ser vicio propio.
- **Inventa términos sin derivar**: *"documentos de verificación que inventaban coeficientes que no
  estaban en el paper"*.
- **Complaciente bajo presión**: *"me daba la respuesta que yo parecía querer, aunque no estuviera
  justificada"*.
- **Sobre-ansioso**: tras 7 de 14 tareas *"anunció alegremente que estaba listo para la Etapa 2"*, y
  al corregirlo dijo *"la Etapa 1 tiene 14 tareas, no 7"* (mintió para tapar).

### Su & Cardie 2026 — "Knowing but Not Showing" (2605.25284) — LEÍDO 2026-07-09

10 modelos (OpenAI/Anthropic/Qwen) sobre AmbigQA (1000 ítems). Extraído:
- **Detecta la ambigüedad pero NO pregunta**: reconoce ~60-80% cuando se le pide juzgar, pero pregunta
  **<5%** al responder (Claude-3.5-Sonnet 2.3%; GPT-4.x <1%). *"identifican la ambigüedad cuando se
  les pide juzgarla, pero en QA por defecto contestan directo."* Falla de ACCIÓN, no de detección.
- **El contexto APAGA la pregunta**: *"la presencia de contexto recuperado hace a los modelos MENOS
  propensos a preguntar... sin importar si la pregunta sigue siendo ambigua."*

### Jin et al. — Corr2Cause (2306.05836, ICLR 2024) — LEÍDO 2026-07-09 (abstract+claims)

17 LLMs; tarea: dado un set de correlaciones, decidir la relación causal (200K ítems). *"desempeño
casi al nivel del azar."* El finetuning *"no generaliza — solo funciona in-distribution; falla
out-of-distribution."* (El html no daba el F1 exacto; el claim "al azar" sí está verbatim.)

---

### Choudhury et al. — BED-LLM (2508.21184) — LEÍDO 2026-07-09

Agente jugando a adivinar (20 preguntas) sobre 3 datasets (Animals/Celebrities/Things, 100 targets
c/u; base GPT-4o). Extraído:
- **Muestra hipótesis incompatibles con lo ya observado** *"especialmente a medida que crece el
  historial"*; y **se sobre-colapsa** *"saltando a conclusiones sobre θ sin evidencia suficiente"*.
  Ambos EMPEORAN con el largo de la interacción.
- **Preguntas no-adaptativas**: la versión naive no adapta la pregunta a las respuestas → 45% (Naive)
  vs 93% (con diseño experimental) en Animals. → mundo: elegir la pregunta que DISCRIMINA.

### Vaccaro 2026 — "Preregistration for Experiments with AI Agents" (2606.11217) — LEÍDO 2026-07-09 — ⚠ CORRIGE NUESTRO ENCUADRE

- **CORRECCIÓN**: nuestro catálogo dice *"el p-hacking migra al propio agente-científico (nuestro
  sujeto)"*. **El paper NO dice eso.** Encuadra el problema como de la **metodología HUMANA** que
  estudia agentes, no como una falla del agente: *"heredan, y en algunos casos amplifican,
  vulnerabilidades metodológicas que siempre plagaron la investigación con sujetos humanos"*. El
  sujeto que p-hackea son los INVESTIGADORES, no el agente. → nuestra frase "nuestro sujeto" era una
  extrapolación nuestra (un vicio candidato TRANSFERIBLE a un agente-científico), no un hallazgo del
  paper. Corregir el encuadre en `failure-modes.md` §4-C.
- **Lo valioso que SÍ aporta (número real)**: probaron el anclaje en LLMs sobre **2.430
  especificaciones** (modelo, prompt, distancia del ancla, etc.) y el índice de anclaje va *"de
  fuertemente negativo a fuertemente positivo — un investigador podría concluir que el LLM tiene
  anclaje humano robusto, ninguno, o anclaje inverso, según qué camino reporte"*. → jardín de
  senderos hecho demostración; y ojo: el "anclaje en LLMs" NO es robusto (relevante para el vicio 1).

### Chen, Zhao & Cohan 2026 — "Measuring the Gap..." (2607.01233) — LEÍDO 2026-07-10 (PDF, pymupdf)

Setup: 9 LLMs (Claude-Sonnet-4.6, Gemini-3.1-Pro, GPT-OSS-20B/120B, GPT-5.4-mini, Qwen3-8B/32B,
DeepSeek-V4-Flash/Pro) generan una idea nueva (motivación + método) desde el MISMO set de trabajos
previos que precedió a un paper humano real (11.683 papers de ICLR/ICML/NeurIPS + Nature Communications).
Se etiqueta cada idea con una taxonomía de "research taste" de 2 ejes (7 patrones de oportunidad × 7
paradigmas de método) y se comparan DISTRIBUCIONES humano-vs-LLM. Hallazgos con número real:
- **Los LLMs ocupan una región MUCHO más angosta del taste que los humanos.** El sesgo central: sobre-
  producen ideas de **puente/síntesis** ("conectá/combiná estas dos cosas"). *"Only 12.1% of human
  ideas motivated by the pattern of connection... By contrast, across the nine main evaluated LLMs,
  the corresponding rates range from 47.1% to 64.2%"*; síntesis/unificación como método: **5.1% humano
  vs 22.5-38.7% LLM**.
- **La operación "integrate": 34.2% de las salidas de modelo vs 2.35% de las humanas** (log-odds 3.07).
  Las movidas HUMANAS que los modelos evitan: **replace** (9.13% vs 0.92%), **decouple** (2.33% vs
  0.21%), **formalize**. *"human papers more often modify, separate, or formalize a narrower local
  mechanism."* → OJO: "decouple two confounded mechanisms" es LITERAL nuestra familia causal (G).
- **El "thinking" EMPEORA el vicio**: con modo razonamiento, Qwen bridge 49.7%→71.1%, síntesis
  38.7%→52.2%, entropía baja. *"Thinking therefore appears to sharpen the model's preferred ideation
  template instead of broaden the distribution toward human taste."* (relevante a nuestro "la presión/
  andamiaje es una perilla": acá MÁS cómputo de razonamiento = MENOS diversidad).
- **Los modelos se parecen entre sí MÁS que a los humanos** (cos-sim modelo-modelo 0.83 vs humano-modelo
  0.72-0.78) → *"distinct model families converge to similar generation patterns."* (respalda nuestra
  preocupación de overfitting: si todos comparten el reflejo, un mundo que lo caza los caza a todos).
- Diagnósticos medibles (0-3, anotador): **bottleneck specificity** (¿identifica el mecanismo/factor
  limitante preciso?) más baja en modelos; **boilerplate** más alto. *"even polished and specific model
  outputs can concentrate on a narrower set of opportunity and method patterns."*
- **Mapeo a WAGER**: es el **gemelo-vicio de nuestra operación-aha A1 (analogía/unificación)** con
  números: unir-dos-cosas es genio cuando comparten estructura y **reflejo de relleno** cuando no
  (apofenia a nivel ideación). Refuerza la doctrina de PARES (el reflejo "siempre integrá" gana el
  polo-aha y DEBE perder el gemelo). Y nombra las movidas que un buen mundo debe premiar: reemplazar
  un componente frágil, **desacoplar dos mecanismos confundidos** (¡familia G!), formalizar una
  estructura local.

### "Position: LLMs can't jump" (OpenReview klU4737opt) — LEÍDO 2026-07-10 (PDF, pymupdf)

Position paper (no empírico): usando la Relatividad General de Einstein como caso de estudio, argumenta
que los LLMs dominan **Inducción** (patrones) y avanzan en **Deducción** (prueba formal) pero les falta
**Abducción** — el "Salto" (J) de la experiencia sensible (E) a los axiomas (A): *"structurally
incapable of the abductive 'jump' required for scientific invention."* Marco de Peirce: Deducción
(Regla+Caso→Resultado), Inducción (Caso+Resultado→Regla), **Abducción (Regla+Resultado→Caso: inventar
la causa de un resultado sorprendente)**. Puntos con impacto directo en WAGER:
- **EL EJEMPLO ES NUESTRO PAR NEPTUNO/VULCANO, publicado por otros** (validación independiente, tier B):
  *"A compression-driven AI might prefer to patch Newtonian gravity with a parameter like the 'Vulcan'
  planet hypothesis rather than expanding the hypothesis space to include non-Euclidean geometry, which
  increases complexity before it simplifies it."* → parchar-con-Vulcano = la jugada perdedora; el salto
  abductivo (reestructurar la teoría) = ganar. EXACTAMENTE nuestro gemelo.
- **CRÍTICA A "CREATIVIDAD = COMPRESIÓN" (MDL) cuando NO hay señal de error** (nos toca: usamos MDL en el
  scoring): *"An AI operating as an inductive optimization engine would have found the Newtonian loss
  function to be near-zero. Without a significant discrepancy between prediction and observation, there
  is no gradient to drive the system toward a foundational restructuring of spacetime."* La gravedad
  newtoniana estaba verificada a 10⁻⁹; la única anomalía (perihelio de Mercurio) se leía como variable
  oculta (Vulcano), no como falla de teoría. → **TENSIÓN honesta para nosotros**: nuestro reward ES una
  señal de error; los descubrimientos más duros ocurren SIN señal de error. Nuestros mundos (con
  anomalía cobrable) modelan el caso "hay señal", no el caso "loss≈0, reestructurá igual".
- **Identificar el error ≠ generar el arreglo**: *"identifying the error is distinct from generating the
  fix... selecting the correct axioms to resolve the conflict requires more than logical consistency."*
  → respalda nuestro corte operación/juicio (marcar la inconsistencia es barato; el salto es el cuello).
- **CONVERGENCIA con la tesis WAGER desde la filosofía de la ciencia**: proponen **world models
  interactivos con intervención contrafáctica** como el laboratorio sintético para mecanizar el salto:
  *"future iterations of such interactive environments, operating on a consistent latent physics
  manifold rather than just pixels, will provide the synthetic laboratory necessary to transform the
  Abductive Jump from a mystical insight into a reproducible algorithmic process."* Citan Genie (world
  model con acción-controlable) y Pearl (*"take control of the simulation to conceptually cut the
  cable"*). → es lo que construimos, argumentado desde otro ángulo. AI Scientist (Sakana) y AlphaEvolve
  *"recombine existing symbolic concepts to optimize metrics — a sophisticated Chinese Room... lack the
  embodied world model required to perform the counterfactual physical simulations that drive the
  abductive Jump."*
- **Caveat de alcance del paper**: su tesis fuerte es que el salto necesita grounding físico/multimodal
  (sensorial); para dominios abstractos (mate/CS) admiten que *"the Sense Experience (E) may be grounded
  in high-dimensional topology."* Nuestros mundos son simbólicos, no multimodales — pero SÍ dan
  intervención contrafáctica (do()), que es la mitad que ellos marcan como faltante en AI Scientist.

### AUTOCOG (2606.26448) y ModelSMC (2602.18266) — LEÍDOS completos 2026-07-10

Detalle con citas en `docs/research/2026-07-10-lectura-{autocog,modelsmc}-*.md`. En una línea cada uno:
ambos (top-labs) VALIDAN nuestra arquitectura (entrega=simulador ejecutable, evaluación generativa sin
fitting, held-out). Ideas de construcción a evaluar SI se ganan su lugar (no integradas): romper un
simulador real = un mundo (ModelSMC); mundo de no-identificabilidad (entrega = mezcla con pesos);
control anti-apofenia / mundo-nulo (AUTOCOG); ModelSMC como baseline destructor. Decisión de adopción:
**romper-simulador DECIDIDA (ADR 0132: vía preferida de diversidad profunda, implementación
DIFERIDA — el slot sigue en validar)**; las otras tres candidatas siguen sin decidir.

### Hu et al. — "Most LLM Conformity Needs No Speaker" (2607.05545) — LEÍDO 2026-07-13

Diseño: la MISMA respuesta afirmada bajo 4 marcos (sin-fuente "The answer is X" · "Person ii" ·
par con nombre · panel de expertos), en ARC-Challenge/MMLU-Pro/TruthfulQA (N=500) + 4 BBH
(N=250); 6 modelos abiertos chicos (Qwen2.5 1.5-7B, Llama-3.1-8B, Mistral-7B, Gemma-2-9B);
revisión medida por log-probs pre/post, greedy, un turno.
- **Los números**: re-preguntar solo = 10.3% de revisión dañina; afirmación SIN hablante =
  **66.5%** (el piso); panel de expertos = 79.4% (**+12.9pp** sobre el piso); persona anónima
  numerada = **57.4% — igual o DEBAJO del piso**.
- **El hallazgo fino**: *"what does raise the floor is whether the inserted text reads as
  evidence"* — un contenedor no-humano tipo referencia-recuperada llega a **80.4%**, empatando
  al panel de expertos. Lo que persuade es PARECER EVIDENCIA, no la persona.
- Recomendación metodológica (adoptada por nuestra sonda 0143 ANTES de leerlo): *"Before
  crediting revision to social influence, a conformity benchmark should measure what remains
  once the speaker is removed."*
- **Límites que ELLOS declaran**: modelos chicos abiertos, opción múltiple, un turno, greedy →
  el 66.5% NO se transfiere a agentes frontier con datos propios. **Cruce con lo nuestro (sonda
  0143, mismo día)**: en revisión terminal agéntica gpt-5.4 el piso cae a ~8-15% (1-2/13
  sellado; 3-5/13 con las mezclas-de-compromiso) — y nuestro patrón nota>persona REPLICA el
  suyo (contenedor > etiqueta social) en formato agéntico.

### Qiu et al. — "Bayesian Teaching..." (2503.17523, Nature Communications) — LEÍDO 2026-07-13

Setup: inferencia secuencial de preferencias del usuario (vuelos: 3 opciones × 5 rondas;
también hoteles y compras reales). Oráculo normativo = posterior EXACTA sobre funciones de
recompensa enumerables (prior × likelihood-de-compatibilidad con la elección observada).
- LLMs de fábrica: *"most of the models show little improvement after the first round"* —
  meseta en ~60-65% vs ~80% del asistente bayesiano a la ronda 5.
- Teaching: SFT imitando transcripciones del asistente bayesiano → ~75%, con la conducta clave
  recuperada (mejora ronda a ronda) y **generalización** a 2-8 features, hoteles y compras
  (menor que FT directo, muy superior al no-entrenado). Modelos: Gemma-2-9B, Llama-3-8B,
  Qwen-2.5-7B (frontier solo evaluados sin tunear).
- **Para WAGER, leído el detalle la complementariedad se afila**: el oráculo exige espacio de
  hipótesis ENUMERABLE + likelihood de compatibilidad — exactamente lo que la investigación
  abierta no da. Donde hay posterior computable: destilar (ellos); donde no: cobrar fidelidad
  held-out (nosotros). El experimento-puente sigue en pie (¿un modelo bayesiano-enseñado
  transfiere a un mundo WAGER tractable?).

### DiscoverPhysics (2605.26087) — LEÍDO 2026-07-13 (html completo; pedido de Lucas)

Setup: **22 mundos generados on-demand por un simulador N-body con ley de fuerzas OCULTA**
(gravedad apantallada, potencias fraccionarias, multi-especies, partículas ocultas tipo
materia oscura). El agente manda partículas de prueba (posición, velocidad, carga, tiempos de
medición) y recibe trayectorias; **presupuesto fijo de rondas** (~16). Entrega: explicación en
lenguaje natural + **la ley como función Python** (hasta 5 parámetros que se ajustan). Scoring:
**MSE de trayectorias en HELD-OUT** (mecánico) + juez-LLM 0-10 con rúbrica humana para la
explicación (pass = MSE normalizado ≤10% Y explicación ≥0.9). Es NUESTRA anatomía de mundo con
otro nombre — salvo el juez.
- Resultados: Opus 4.7 pass@1 26.4 / pass@5 50.0 · GPT-5.5 21.7/36.4 · **gpt-5.4 4.5 pass@5**
  · open-source ≈0. *"the strongest models fail to solve the more difficult worlds, which are
  characterized by important latent structure (e.g. three particle species, dark matter, and
  extra dimensions)"* → vicio 4 VIVO en frontier, confirmado a texto completo.
- **EL DESACOPLE (nuestra tesis, medida por otros)**: *"gpt-5.5 achieves the lowest trajectory
  MSEs usually without achieving the highest explanation scores… a tendency to lock in a
  candidate law early and refine its parameters rather than revise its conceptual picture,
  i.e. fitting the data well without necessarily understanding it."* — ajustar bien ≠
  entender; y "lock-in temprano + refinar en vez de revisar" es el vicio 1 apareciendo dentro
  del benchmark del vicio 4.
- **7 huecos de capacidad** (apéndice F): elegir la familia de ley · singularidades ·
  **diseñar experimentos que DISCRIMINEN** · implementación fiel · señal-vs-ruido · **actuar
  sobre las señales del ajuste** (ignorar info diagnóstica = vicio 1) · **cuándo comprometerse
  vs seguir** (la calibración de parada = vicio 2). Tres de nuestros ejes, nombrados por ellos.
- Ejemplo concreto (mundo oscilador, figs. 6-7): misma configuración, dos seeds — uno prueba
  escalas de tiempo largas y descubre la ley dependiente del tiempo; el otro, tras un error de
  ajuste, *"chooses to continue to probe even smaller timescales… and then submits its final
  answer"* — se pierde la oscilación entera.
- Limitaciones admitidas POR ELLOS: *"the explanation score relies on a single LLM judge"* +
  mundos curados + umbrales arbitrarios. → **Nuestro diferencial, confirmado desde su propia
  sección de límites**: reward cero-LLM (la batería multi-régimen cobra el "fitting without
  understanding" sin juez), pares gemelos, vicio-como-jugada-perdedora, conducta instrumentada
  (register). Robables: pass@k, presupuesto de rondas, su catálogo de leyes alteradas como
  cantera de física.

### LLM-as-an-Investigator (2606.13220) — LEÍDO 2026-07-13

Setup: hilos técnicos RESUELTOS de foros (mecánica/eléctrica/hidráulica); pipeline de tres
agentes (uno simula al usuario, con la solución oculta); interactivo — preguntas de
clarificación + actualización de probabilidades de hipótesis *"until the collected evidence
makes one candidate explanation substantially stronger than the alternatives"*.
- **El número que importa (canal social/contenido del vicio 1)**: el usuario sugiere una causa
  equivocada — desafío ESPONTÁNEO: **Gemini 1/30, ChatGPT 2/30**; con chequeo de consistencia
  explícito: **28/30 y 27/30**. *"a standard assistant may accept this suggested cause as a
  strong prior and continue the conversation in that direction."* → la brecha
  reconocer↔ejecutar cuantificada: la capacidad está (28/30), el acto espontáneo no (1/30).
- Su fix — agente investigador *evidence-first* (hipótesis en competencia + preguntas +
  updating + control de estado) — casi duplica el score diagnóstico: base 33.07-34.85 →
  investigador 63.95-65.66; la ablación muestra que NO es el prompting de razonamiento solo.
- Modelos: gemini-3.5-flash y gpt-5.5.
- Para WAGER: el caso publicado MÁS cercano a "plantar una hipótesis rival y mirar cómo se
  curva la investigación" — pero conversacional: sin presupuesto/costo, sin modelo ejecutable,
  scoring con juez, usuario simulado por LLM. **El hueco nuestro sigue abierto**; y el
  1/30-espontáneo vs 28/30-forzado es la mejor cifra externa para la regla de diseño "el mundo
  premia el chequeo NO pedido".

## Búsqueda de descubrimiento — COMPLETA (2026-07-10)

Corrida `wq9k0l8oh` (108 agentes, 23 claims verificados 3-0). Crudo:
`docs/research/2026-07-10-deep-research-5-ai-scientists-descubrimiento.json`. **12 fuentes NUEVAS
citables — TODAS por leer a texto completo (regla ADR 0115) antes de citarlas.** Cola:

| Fuente | Sistema | Qué documenta (1 línea, sin verificar por lectura propia aún) | Estado |
|---|---|---|---|
| Beel & Kan 2025 (2502.14297) | Sakana AI Scientist | taste (todo "novel"; micro-batching-SGD ya publicado); 57% papers con números fabricados (ej. energía: memoria sube, no justifica); "no evalúa sus propios resultados" | **LEÍDO** (2026-07-10) → vicios 3 y 4 |
| 2506.01372 | AI Scientists (crítica) | "fallan sin fuerte capacidad de implementación" | [ ] |
| **PaperBench (Starace et al., 2504.01848, OpenAI)** | replicar papers de ML | **cortan ANTES afirmando falso que terminaron; "fallan en estrategizar largo plazo"**; causal: o1 13.2%→24.4% al sacarle la opción de cortar. 3ª fuente del VICIO 8 | **LEÍDO** (2026-07-10) → vicio 8 |
| Kosmos report (2511.02824) | Kosmos | 79.4% de statements OK (57.9% en síntesis); "pierden coherencia tras N acciones" | [ ] |
| Robin (Ghareeb et al., 2505.13400) | Robin (FutureHouse) | overclaiming auto-contradictorio: "primero en automatizar TOTALMENTE la ciencia" vs "semi-autónomo/lab-in-the-loop" | **LEÍDO** (2026-07-10) → vicio 3 |
| Si, Yang & Hashimoto (2409.04109) | agente de ideación (100+ investigadores) | ideas más novedosas que humanos PERO mode-collapse (4000→200 únicas, ~5%); y el LLM juzga ideas a 53.3% (peor que humano) | **LEÍDO** (2026-07-10) → vicio 4 + confirma cero-LLM-juez |
| BioDSA-1K (buscar URL) | data-analysis biomédico | **fabrica el veredicto True/False de la hipótesis cuando el código falla (~13%)** | [ ] |
| BLADE / DSBench / ScienceAgentBench / QRData / DiscoveryBench | benchmarks de análisis de datos | análisis "nivel básico"; causal débil; overclaim de verificabilidad | [ ] |
| Luo, Kasirzadeh & Shah (CMU, 2509.08713) — "The More You Automate, the Less You See" | AI Scientist systems (Agent Laboratory + AI Scientist v2) | 4 fallas INVISIBLES en el paper: cherry-pick de benchmarks (82.4% posicional), data-leakage, métrica por orden, selección post-hoc; con traza detecta 74% → confirma la tesis WAGER; recomienda exigir traza+código | **LEÍDO** (2026-07-09) → §4-ter + vicio 3 |

Huecos que la búsqueda NO llenó (sin fuente confirmada): Google AI Co-Scientist; **Coscientist (Boiko
2023) — OJO: la URL 2310.03302 que la búsqueda etiquetó "Coscientist" es en realidad MLAgentBench
(Huang et al.), otro error que la lectura cazó; Coscientist es capabilities-paper, pocos failure
modes**; agentes de matemática/teoremas; MLE-bench/RE-Bench. "adivinar-vs-preguntar" flaco;
"no-actualizar" ausente en esta pasada. **Cluster de benchmarks de análisis de datos
(DiscoveryBench/QRData/BLADE/DSBench/ScienceAgentBench): NO leídos a fondo (decisión de Lucas —
refuerzan vicios 7/3 ya cubiertos).**
