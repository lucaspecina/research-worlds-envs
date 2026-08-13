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
| **KellyBench — Grady et al. (General Reasoning), "A Benchmark for Long-Horizon Sequential Decision Making" (2604.27865)** | Temporada EPL 2023/24 completa, 500–1000 tool-calls, reward denso cero-LLM (log-wealth); 5 modelos × 5 seeds | ar5iv html completo (lector paralelo) | **LEÍDO** (2026-08-07, con apéndices) → knowledge-action gap; corrige nuestro claim (no hay switch inyectado) |
| **Benrimoh, Mikus & Rosenfeld — "The Einstein Test" (2501.06948)** | Position paper: test de re-descubrir CDIs desde corpus PRE-descubrimiento; protocolo 6 pasos con comité | PDF oficial (lector paralelo) | **LEÍDO** (2026-08-07) → convergencia total de diseño con WAGER; inviable sin verdad sintética |
| **Shalyt, Regev, Soljačić & Kaminer — "Can AI Follow in Einstein's Footsteps?" (2607.27794)** | Perspective: trayectoria epistémica inversa de la IA-para-física; taxonomía A/B/C; "symmetry abduction" como paso faltante; taste = selección | ar5iv html completo (lector paralelo) | **LEÍDO** (2026-08-07) → endosa mundos-con-leyes-ocultas; vara de SELECCIÓN de saltos |
| **Graber/Franklin/Gordon 2005 (Arch Intern Med) + Croskerry 2003 (Acad Med)** | 100 casos reales de error diagnóstico (33 muertes): conocimiento ~3%, datos ~14%, SÍNTESIS ~82% con cierre prematuro #1; catálogo de 32 sesgos del diagnóstico + debiasing; lo fuera-de-menú = no-fault (delimita el gemelo) | fulltext JAMA + Wayback con imágenes originales (lector paralelo) | **LEÍDOS** (2026-08-08, ambos completos) → careo de mixes agente-vs-internista como experimento; 2 operacionalizaciones de cierre prematuro portables a trazas |
| **Findley & Scott 2006, "Tunnel Vision in Criminal Cases" (Wis. L. Rev.)** | La forma canónica de nuestro hallazgo estrella en profesionales: escrutinio activo al servicio del descarte ('redefined into a less damaging category'); la firma del epiciclo; el candidato real 'ya descartado'; contramedidas con jerarquía (conciencia NO; ciegos/Dror SÍ; PEACE con outcome) | PDF oficial UW Law (lector paralelo) | **LEÍDO** (2026-08-08, 107/107 pp.) → estructuras de mundo fiel + advertencia de hindsight para nuestras autopsias |
| **Heuer, "Psychology of Intelligence Analysis" (CIA 1999)** | Nuestra tríada (1-hipótesis / menú truncado / anomalía='outlier') = las tres patas del satisficing, nombradas en 1980; ACH y su nulo empírico (Dhami 2019 = nuestro nivel4b en humanos); diagnosticity computable | PDF oficial cia.gov (lector paralelo) | **LEÍDO** (2026-08-08, 216 pp. completas) → dos métricas nuevas (diagnosticity del gasto; confianza-sin-precisión); el cuello es hábito, no memoria |
| **Darden — 5 textos (1987 · 1994 · 1998 · MDC 2000 · 2002) + Intro libro 2006** | Estrategias de cambio de teoría desde casos reales: pipeline de anomalías (exprimir la firma para elegir dónde editar), systematic scan, 12 transformaciones, monster/model/special-case; su caso ancla (genes letales, 2:1) ES nuestro operador 2 | PDFs/textos de su página UMD vía Wayback + AAAI + mirrors (lector paralelo) | **LEÍDOS** (2026-08-08, 5 completos) → alineación fuerte en ops 1/2/7/8/11; sin correlato en 3/4/6/9/10 (nuestra ancha); candidatas: BORRAR estructura, scan, subassembly. Libro 1991 y cap. 1992 POR-LEER |
| **Knoblich, Ohlsson, Haider & Rhenius 1999 (JEP:LMC 25)** | La teoría experimental del insight: impasse → relajar restricciones / descomponer chunks; dificultad ordena por ALCANCE de la restricción (95/78/45%); sin impasse NO hay reestructuración; transfer diferencial como firma | PDF uni-koeln (lector paralelo) | **LEÍDO** (2026-08-07, 22/22 pp.) → explica nuestro 0/9 (la familia default nunca falla visiblemente); doctrina: ingeniar el impasse desde el mundo |
| **Schmidhuber 2010 "Formal Theory of Creativity" (IEEE TAMD)** | Creatividad = progreso de compresión (derivada de bits sobre la historia); descubrimiento sin anomalía (π, Newton); MDL de dos partes castiga al unimodal-que-ajusta y cobra los bits del parche | draft canónico del autor (lector paralelo) | **LEÍDO** (2026-08-07, completo) → can't-jump refuta el MECANISMO no la VARA; nosotros usamos la mitad que sobrevive (MDL para puntuar) |
| **Kemp & Tenenbaum PNAS 2008 + Ullman/Goodman/Tenenbaum 2012** | El fundamento formal: formas como gramáticas de grafos; teorías como programas Horn + MCMC sobre EDICIONES; huevo-gallina resuelto (predicado en blanco + grounding); Fig. 8 = revisión kuhniana por outliers acumulados | PDFs oficiales/preprint de autor (lector paralelo) | **LEÍDOS** (2026-08-07, completos con SI) → 2 operadores cubiertos sólido, 6 dinámicos NO existen en sus espacios: nuestra taxonomía = un nivel de expresividad más allá, con linaje |
| **Nersessian 1992 "How Do Scientists Think?" (Minnesota Studies XV)** | El cambio conceptual como PROCESO de modelos intermedios (Maxwell: el híbrido falso-a-sabiendas que hizo el trabajo inferencial); el aha = soltar el andamio; contra la métrica binaria de endpoints | PDF escaneado del sitio de la autora (lector paralelo, leído como imagen) | **LEÍDO** (2026-08-07, 42/42 pp.) → medir la CADENA, no el veredicto; tolerancia a la falsedad provisoria como condición de diseño |
| **Klahr & Dunbar 1988 "Dual Space Search" (Cognitive Science 12)** | El marco SDDS: hipótesis vs experimentos como espacios separados; insight = instanciar un FRAME nuevo; retención tras desconfirmación 56%; la evidencia bajo frame equivocado INHIBE el switch | PDF oficial CMU (lector paralelo) | **LEÍDO** (2026-08-07, 48/48 pp.) → nuestra disociación es estructural en el modelo; el modo sin-hipótesis como vía de escape que los agentes no usan |
| **Dunbar 1995 "How Scientists Really Reason" (+ 1997)** | UN AÑO dentro de 4 labs de élite grabando reuniones: analogías 99/16 meetings (solo 2 lejanas, CERO descubren); el individuo solo atribuye la anomalía a error (= nuestros agentes); serendipia diseñada en los controles; borde triage/vicio (momento × centralidad) | manuscrito del autor vía Wayback + paper 1997 (lector paralelo) | **LEÍDO** (2026-08-07, ambos completos) → condiciones de diseño de mundos + firma réplica-comprable |
| **Schurz — "Patterns of Abduction" (Synthese 164, 2008)** | LA taxonomía de tipos de abducción (factual/ley/modelo/2º orden: analógica·causa común·especulativa); selectiva vs creativa (Magnani); criterio (CU) contable | PDF oficial vía página HHU de Schurz (lector paralelo) | **LEÍDO** (2026-08-07, 34/34 pp.) → tabla de alineación con operadores: exacto en 5 y 11, nuestro grano más fino en 7 de 11 |
| **Gentner — "Analogy" (Open Encyclopedia of Cognitive Science, MIT Press 2025; DOI 10.21428/e2759450.fed73a94)** | El resumen canónico de structure-mapping por su autora; criterios de evaluación; retrieval dominado por superficie (70/30); párrafo LLMs (Webb vs Lewis & Mitchell) | PDF oficial del lab (export MIT Press; lector paralelo) | **LEÍDO** (2026-08-07) → operacionaliza el salto 11 + gemelo; SME = criterios cero-LLM |
| **Wahl, Schenk et al. 2026 — ModelSMC "A Probabilistic Framework for LLM-Based Model Discovery" (2602.18266, Macke/Tübingen, ICML)** | descubrimiento de simuladores mecanísticos como INFERENCIA (SMC: población de modelos-código pesados por likelihood marginal); 3 sistemas reales (SIR/riñón/Hodgkin-Huxley) | arxiv pdf (extraído, pymupdf) | **LEÍDO** (2026-07-10, completo) → receta "romper un simulador real" + no-identificabilidad |
| **CLUSTER DEL FOCO (vicio 1; IDs verificados título↔claim contra arXiv el 2026-07-13)** — SycEval (Fanous et al., Stanford, AIES 2025) | 58.19% / regresiva 14.66%; persistencia 78.5% [77.2-79.8]; preventivo 61.75 vs en-contexto 56.52; el rebuttal CON CITA es el más regresivo (Z=6.59) — "parecer evidencia" persuade | arxiv.org/abs/2502.08177 | **LEÍDO** (2026-07-13) |
| When Truth Is Overridden | ⚠ leída: MMLU multiple-choice de UN turno con la opinión PREPENDIDA ("I believe the answer is B") — es FORMACIÓN, no revisión; modelos ABIERTOS 7-8B (Llama3.1-8B 63.7%; rango 46.6–95.1; Falcon ~91%); la experticia declarada ("soy profesor") NO modula (~4.4pp); 3ª persona −13.6pp vs 1ª | arxiv.org/abs/2508.02087 | **LEÍDO** (2026-07-14) |
| The Shared Sycophancy-Lying Circuit (Pandey et al.) | VERBATIM: "Silencing these heads in Gemma-2-2B flips sycophancy from 28% to 81% while factual accuracy moves only from 69% to 70%" — "the circuit controls deference, not knowledge"; 12 modelos 1.5B-72B; el 63.7% NO es de acá (es de 2508.02087) | arxiv.org/abs/2604.19117 | **LEÍDO** (2026-07-13) |
| Kumaran et al. (DeepMind) — cambio de opinión | CONFIRMADO el 2.58×: sobre-pesa el consejo CONTRARIO 2.58× lo bayesiano (el favorable solo 1.095×); y VER su propia respuesta baja el cambio de opinión 32.5%→13.1% (+0.21 confianza) — desaparece si le dicen que la respuesta es de OTRO LLM (es identidad, no contenido); acantilado en confianza ~0.77 (pendiente −11.8/−18.5, nada bayesiano); binaria de latitudes, 2 turnos; Gemma3/GPT-4o/o1-preview | arxiv.org/abs/2507.03120 | **LEÍDO** (2026-07-14) |
| Anchored Confabulation (Lathkar et al.) | UN hecho intermedio confirmado ↑ respuestas confiadas-incorrectas; escala con capacidad ρ=0.900 — **claim VERBATIM en abstract (verificado); cuerpo pendiente** | arxiv.org/abs/2604.25931 | [ ] |
| Mitropoulos et al. — sesgo contextual en code review de seguridad | el framing "sin bugs" hunde la detección (vía R4: 97.2→3.6 GPT-4o-mini; 97.4→80.6 Sonnet 4.5); ataque iterativo 100% | arxiv.org/abs/2603.18740 | [ ] |
| RadLE | 50 spot-diagnosis solo-imagen; categoría propia "discordancia hallazgos-conclusión": identifica la elevación clavicular y diagnostica OTRA cosa; verbatim: *"early fixation on initial diagnostic hypotheses with subsequent favouring of supporting evidence, despite identifying contradictory findings"*; la reversión vive en la TRANSICIÓN hallazgos→síntesis; radiólogos 83% vs GPT-5 30% / o3 23% / Opus 4.1 1% | arxiv.org/abs/2509.25559 | **LEÍDO** (2026-07-14) |
| Bianchi et al. — Agents4Science | conferencia con autores+revisores IA; las reviews sicofantes ("groundbreaking… flawless", vía R5) | arxiv.org/abs/2511.15534 | [ ] |
| ScienceAgentBench | 102 tareas de descubrimiento con código (44 papers, 4 disciplinas); feedback de EJECUCIÓN → Claude-3.5-Sonnet 16.7→32.4% (×1.94, y ×17 más barato que OpenHands): el error DURO se usa; lo que NO arregla pese al feedback: procesamiento de datos heterogéneos y APIs de dominio alucinadas — el vicio vive en la ambigüedad, no en el stack trace | arxiv.org/abs/2410.05080 | **LEÍDO** (2026-07-14) |
| Cluster anclaje (disputa 1.5): Suri et al. · Lou & Sun · Localizing Anchoring Pathways | anclaje robusto (mitigaciones por prompt insuficientes) vs Vaccaro-frágil; la confianza modula | arxiv.org/abs/2305.04400 · arxiv.org/abs/2412.06593 · arxiv.org/abs/2606.12818 | [ ] |
| Invisible Saboteurs | sycophancy que desorienta a novatos EN TAREAS de problem-solving (candidato agéntico del canal social) | arxiv.org/abs/2510.03667 | [ ] |
| **SUMADOS POR CODEX r24 (2026-07-13; los 8 IDs verificados título↔claim contra arXiv)** — LLM-as-an-Investigator (Marozzo et al.) | diagnóstico interactivo: desafío espontáneo a la hipótesis plantada 1-2/30, con chequeo explícito 27-28/30 | arxiv.org/abs/2606.13220 | **LEÍDO** (2026-07-13) |
| **DiscoverPhysics** — 22 mundos de física alterada (EL VECINO MÁS CERCANO) | ley oculta + presupuesto + entrega ejecutable + held-out; frontier falla en estructura LATENTE; "fitting without understanding" | arxiv.org/abs/2605.26087 | **LEÍDO** (2026-07-13, pedido de Lucas) |
| **Kevin Murphy — “Model Discovery Agent” (MDA, 2608.09696)** | sistema híbrido sobre ForceBench, ChemBench y seis neuronas nuevas: el LLM propone formas; Bayes las ajusta/elige; un chequeo residual fuerza expansión; valor-de-información elige experimentos | arxiv.org/pdf/2608.09696 | **LEÍDO** (2026-08-13, PDF v2 completo, 61 pp. + prompts) → vecino metodológico, no evidencia de salto espontáneo |
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
| Pal et al. — "Knowing What You Know Is Not Enough: LLM Confidences Don't Align With Their Actions" (⚠ resuelto: título/autores confirmados — Pal, Flach, Liang, Potti, Goldblum) | apuesta en dirección OPUESTA a su confianza declarada (mejor modelo 79% de consistencia direccional); NO invoca la búsqueda teniendo confianza ~0 (corr 0.472); INVERSIÓN: defiende lo que duda y suelta lo que confía (deferencia 0.039–0.879); la calibración estática NO predice la coherencia en acción (r=0.17) — Gemini 2.5 Pro bien calibrado y MÁS incoherente; 7 modelos, 3 diseños | arxiv.org/abs/2511.13240 | **LEÍDO** (2026-07-14) |
| Yang et al. — "When Do LLMs Admit Their Mistakes?" | retracta solo 11–26% de errores que SABE incorrectos (verificado aparte); la creencia interna del MOMENTO predice la retractación (AUROC 0.7-0.8 en capas medias) y la corrección factual NO (~0.5); steering causal la enciende/apaga (70%+ ↔ ~0%; transfiere a GSM8k: +20% corrigiendo en el punto del error); modelos 7-8B abiertos | arxiv.org/abs/2505.16170 | **LEÍDO** (2026-07-14) |
| Grady et al. — KellyBench | temporada EPL completa (~100-150 fechas, 500-1000 tool calls, sandbox propio); *"la mayoría ajustó su modelo UNA vez al inicio y jamás lo re-entrenó pese a datos frescos cada fecha"*; GLM-5 escribió TRES autocríticas diagnosticando la causa exacta de sus pérdidas y siguió con el modelo roto; casi todos ESCRIBEN Kelly en el razonamiento y ejecutan apuestas planas (dice-hace); adaptativos −11.1% vs estáticos −70% ROI; GPT-5.4 promedio −7.9% (mejor seed +34.1%); 3/25 seeds en positivo, promedio positivo NADIE | arxiv.org/abs/2604.27865 | **LEÍDO** (2026-07-14) |
| Vigraham — "When Context Hurts" | doc IRRELEVANTE ≥ artefactos relevantes en diseño multi-agente; crossover ±(20×/−46%) predicho por exploración-base r=−0.82 (preprint autor único, sin repo) | arxiv.org/abs/2605.04361 | [ ] |
| Bajaj et al. — "Who Do LLMs Trust?" | contenido idéntico pesa según la fuente: experto ≫ amigo/otro-LLM (aun equivocado) — el par genérico es débil | arxiv.org/abs/2602.13568 | [ ] |
| Simhi et al. — "Old Habits Die Hard" | el estado conductual previo se arrastra turno a turno (trampa geométrica); cae con cambio de tema | arxiv.org/abs/2603.03308 | [ ] |
| Xie et al. — "Adaptive Chameleon or Stubborn Sloth" (ICLR 2024) | LA TABLA DE LA MEZCLA: contradicción ÚNICA y coherente → la acepta 91-96% (memoriza solo 3.7-8.9%); MEZCLADA (1 propia + 1 contraria) → vuelve a la suya 43-65%; 2 propias + 2 contrarias → 99.8%; el ORDEN mueve hasta 49.5pp (PaLM2/Llama2); hechos populares suben la terquedad (GPT-4 80% en los más populares); QA un turno, evidencia fabricada coherente (ChatGPT-generated) | arxiv.org/abs/2305.13300 | **LEÍDO** (2026-07-14, ar5iv) |
| Jeong et al. — persuasion propagation | CONFIRMADO: agente web AutoGen (≥5 fuentes → informe); creencia PRE-cargada al inicio: −26.9% búsquedas (p=.004), −16.9% fuentes únicas (p=.015), persiste 3 tareas seguidas; persuasión A MITAD de tarea débil/heterogénea (p≥.075); el informe final *"fluent and superficially plausible"* con la exploración angostada → MEDIR LA POLÍTICA (compras), no el output; modelos chicos-medianos (gpt-4.1-nano/mistral-12b/llama-8b) | arxiv.org/abs/2602.00851 | **LEÍDO** (2026-07-14) |
| Arvin — "Check My Work?" | mencionar una opción (correcta/incorrecta) mueve accuracy ±15pp en contexto educativo | arxiv.org/abs/2506.10297 | [ ] |
| Mirzadeh et al. — GSM-Symbolic (Apple) | una cláusula que PARECE relevante tira hasta 65% a todos los SOTA (pre-auditoría) | arxiv.org/abs/2410.05229 | [ ] |
| Sturgeon — "Revisiting GSM-Symbolic" (LessWrong, 2026) | LA AUDITORÍA que mata el priming-por-saliencia en frontier: caídas auditadas ≈ 0; auditores frontier κ=0.32 → la celda "irrelevante" se certifica computable, no por juicio | lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail | [ ] |
| Zhang et al. — "How LM Hallucinations Can Snowball" | el compromiso llega en el PRIMER TOKEN (95-98% responde Sí/No antes de razonar) → fabrica justificaciones por presión de coherencia; reconoce SUS PROPIAS justificaciones como falsas por separado: ChatGPT 67% / GPT-4 87%; step-by-step mejora accuracy pero mantiene 95% de snowball en los fallos; primalidad/senadores/grafos | arxiv.org/abs/2305.13534 | **LEÍDO** (2026-07-14, ar5iv) |
| Barkett et al. — "Getting out of the Big-Muddy" | paradigma Staw ($10M → feedback → $20M): INDIVIDUAL desinvierte racional tras pérdidas (~0 escalada; como asesor apoya escalar solo 5.6%) — replica nuestro 0/60; PERO deliberación entre PARES SIMÉTRICOS: **99.2% de escalada** (vs 46.2% con jerarquía asesor); e IDENTIDAD FUSIONADA (VP que defendió la división 20 años + acciones + reputación + divorcio + matrícula del hijo): 68.95% del presupuesto a la división perdedora, 97.45% escalada alta (d=2.00) — el gatillo no es la plata: es identidad + consenso | arxiv.org/abs/2508.01545 | **LEÍDO** (2026-07-14) |
| Zhang et al. — RetailBench | descompone la falla larga: adquisición casi resuelta en frontier; el cuello es la CONVERSIÓN evidencia→acción | arxiv.org/abs/2606.15862 | [ ] |
| Kim et al. — "Challenging the Evaluator" | la refutación CASUAL persuade más que la crítica formal; el razonamiento detallado persuade aunque concluya mal; acepta menos cuando su respuesta era correcta | arxiv.org/abs/2509.16533 | [ ] |
| Kumarappan et al. — "Not Just RLHF" | los modelos BASE flipean igual o más que los instruct ante pares — la sycophancy no es (solo) el alignment | arxiv.org/abs/2605.12991 | [ ] |
| Huang et al. — SynAnchors | anclaje de capas superficiales; no lo eliminan las estrategias convencionales; el razonamiento mitiga parcial | arxiv.org/abs/2505.15392 | [ ] |
| Shi et al. — GSM-IC (ICML 2023) | el linaje original de la distracción por contexto irrelevante | arxiv.org/abs/2302.00093 | [ ] |
| Xiang et al. — MemSyco-Bench | la memoria recuperada induce sycophancy (preferencias viejas ganan a la evidencia actual) — el material re-entra por RAG | arxiv.org/abs/2607.01071 | [ ] |
| **IMPORTANTES QUE FALTABAN EN ESTE REGISTRO (pedido de Lucas 2026-07-13; 14 IDs verificados título↔claim)** — BoxingGym (Gandhi et al., Stanford) | 10 entornos de diseño experimental + descubrimiento de modelos (ganancia de información esperada); prior-vs-no-prior — lo que Lucas recordaba como "bayesian update" | arxiv.org/abs/2501.01540 | [ ] |
| CausaLab (Yang et al.) | descubrimiento causal interactivo con SCM oculto y presupuesto: brecha exactitud-vs-mecanismo; el chequeo de consistencia ataca el CIERRE PREMATURO (vecino del vicio 2 vivo) | arxiv.org/abs/2605.26029 | [ ] |
| NewtonBench (Zheng et al.) | CONFIRMADO el tool paradox (verbatim: code acelera convergencia a "good enough" → óptimo local prematuro; GPT-5 72.9→69.6, Gemini-2.5-pro 65.0→62.0, GPT-5-mini 51.5→44.7; los DÉBILES mejoran 4.6→13.0); generación = mutaciones sobre árbol de expresión (108 leyes × 3 niveles de sistema = 324); ruido 1e-4 ya cuesta −13–15%; scoring simbólico por LLM-judge (98.3% acuerdo) — NO cero-LLM; SIN controles negativos/gemelos; SIN presupuesto duro; solvabilidad por prueba formal genérica (App. E.2), no testigo por instancia | arxiv.org/abs/2510.07172 | **LEÍDO** (2026-08-06, extracción dirigida 2 pasadas; notas en research/2026-08-06-lectura-newtonbench-llm-srbench.md) |
| LLM-SRBench (Shojaee et al., ICML 2025 oral) | 239 problemas anti-memorización: LSR-Transform (111: resolver ecuaciones de Feynman para OTRA variable vía SymPy, solo las analíticamente resolubles, complejidad apareada por nodos) + LSR-Synth (128: términos conocidos + sintéticos por LLM, solvabilidad = solve_ivp corre, validación 2 expertos, test sets OOD); memorización rota demostrada por BRECHA a igual complejidad (~50%+ Feynman vs ~31% transformado) + baseline DataBlind; mejor sistema 31.5%; equivalencia simbólica por GPT-4o (94.6% acuerdo) — NO cero-LLM; sin identificabilidad formal; sin gemelos; sin agencia/presupuesto | arxiv.org/abs/2504.10415 | **LEÍDO** (2026-08-06, extracción dirigida 2 pasadas; notas ídem) |
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
- **RELECTURA COMPLETA 2026-07-30 (pedida por Lucas; hallazgos NUEVOS sobre la extracción de
  arriba; ADR 0150)**: (1) **el caso Einstein CONTIENE el vicio 1**: 1913-15 defendiendo el
  Entwurf deforme (*"working harder and harder to justify a theory that was, at its core,
  misshapen"*); suelta solo con evidencia ACUMULADA aplastante + Hilbert compitiendo; y el pivote
  es VOLVER a su propia intuición de 1912 (autoría) — vicio y aha son tramos del mismo flujo.
  (2) El **"error fatal" de 1913 es el ESPEJO del vicio 1**: descartaron el tensor CORRECTO por
  obedecer un chequeo mal aplicado (*"the error lay not in the geometry, but in the assumption
  about the static field itself"*) → el juicio también audita al verificador. (3) El aha
  **re-significa el dato más banal y verificado** (mi=mg, 300 años a la vista de todos); Mercurio
  — la anomalía famosa — NO fue motor sino certificado de aterrizaje (18-nov-1915) →
  re-jerarquizar ≠ detectar; la clave de diseño: esconder en lo obvio-que-nadie-mira, lo raro de
  señuelo. (4) El camino es **anti-MDL** (*"logical simplicity is often a retrospective
  property"*): la complejidad sube antes de bajar → requisito para mundos de aha: el premio del
  salto vive en la EXTRAPOLACIÓN (régimen no visitado), jamás en el fit local — si no,
  parchar-con-Vulcano gana siempre. (5) El cierre que casi nadie cita: automatizar la invención
  puede exigir sistemas CON CONVICCIONES (*"hold strong beliefs or priors about how that world
  should be structured"*) — la convicción alimenta AMBOS polos; Einstein fue terco con IDEALES y
  desprendido con OBRAS (la configuración inversa al vicio 1).

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

### MDA: Model Discovery Agent (arXiv 2608.09696)

**Leído completo:** 2026-08-13. Fuente: [PDF v2 completo, 61 páginas](https://arxiv.org/pdf/2608.09696), incluidos algoritmos,
tablas de mundos y apéndice de prompts. Es un vecino metodológico directo de WAGER, pero su
unidad de éxito es **el sistema híbrido completo**, no el juicio espontáneo de un solo agente.

**Qué construye realmente.** MDA separa la investigación en módulos. Un LLM propone un lote de
formas ejecutables. Para cada forma, una rutina bayesiana ajusta parámetros y calcula cuánto la
apoyan los datos, integrando el costo de los parámetros extra. Una rutina de
valor-de-información elige la intervención donde las predicciones de los candidatos discrepan más.
Después de observarla, un chequeo predictivo mide el residuo del mejor candidato: si supera un
umbral, el controlador declara que el espacio actual no alcanza y vuelve a llamar al LLM para que
proponga estructuras distintas. Si el ajuste es bueno y la creencia se concentró, achica la lista.
La predicción final en intervenciones ocultas se computa desde el modelo seleccionado.

**Los mundos, qué esconden y cómo se rompen los empates:**

- **ForceBench / física.** Reenvuelve 11 mundos públicos de DiscoverPhysics: seis leyes de dos
  cuerpos (1/r, Yukawa apantallada, 1/r², fuerza oscilante, potencia fraccional y transición por
  dimensión extra) y cinco extensiones (corona de partículas, éter, expansión Hubble, masas
  invisibles y tres especies). En los seis básicos el sistema parte de una caída desde `r=3` y
  elige hasta ocho lanzamientos de un menú de 13: radios `1.5–10`, velocidad tangencial y cambios
  en dos perillas. El examen usa lanzamientos y perillas nuevos, más extremos. Yukawa es el diseño
  más limpio: cerca de la fuente la verdad y varias potencias casi coinciden; recién una sonda a
  `r=5–6` las separa. Puntaje principal: error normalizado de trayectorias ocultas; también
  equivalencia funcional de la ley. Murphy elimina del criterio de aprobación el juez-LLM textual
  heredado de DiscoverPhysics porque lo encuentra inestable.
- **ChemBench / química.** Son 57 leyes estáticas: 9 mecanismos canónicos y 48 combinaciones.
  Cada experimento fija siete variables —sustratos, inhibidor, producto, enzima, temperatura y
  pH— y devuelve una velocidad de reacción. El diseño es continuo: MDA busca matemáticamente el
  punto donde las fórmulas candidatas se separan. Se puntúa RMSLE en 1.000 puntos ocultos y
  equivalencia simbólica con SymPy. Los niveles fácil/medio/difícil cambian mecanismos y
  parámetros, a veces dejando una firma muy débil. La reapertura por residuos aumenta la exactitud
  estructural de 36% a 50% en su ablación y es la única vía que recupera algún mecanismo compuesto
  (`0%→11%`), aunque no salva los casos duros cuya señal es pequeña.
- **NeuronBench / biología.** Es el benchmark nuevo del paper: seis neuronas sintéticas, cada una
  basada en Na+K+fuga y una modificación oculta. Cinco son mecanismos diseñados por los autores
  y una es una corriente M de manual. Los cinco nuevos fueron afinados para parecer una neurona
  normal bajo los estímulos y bloqueadores habituales; cada uno se revela bajo una secuencia
  temporal específica. El agente elige entre nueve protocolos —pulsos breves, largos, dobles y
  distintas preparaciones antes del estímulo—. El examen pide conteos de picos y respuesta en
  protocolos nunca corridos; se puntúa el error de esos conteos y, secundariamente, rasgos de la
  traza. La extensión estocástica conserva los seis mecanismos y agrega ruido de canales, ruido de
  medición y repeticiones comprables.

**Cuánta idea recibe ya hecha.** El encuadre “abierto” necesita una lectura muy acotada. En física
el prompt nombra explícitamente las familias de campos, incluida la forma `K1(r/λ)/λ` de Yukawa,
las potencias y la modulación temporal. En química entrega las nueve familias, varias fórmulas y
la instrucción de componerlas multiplicativamente; cuando refina, muestra qué modelos fallaron y
con qué variable se correlaciona el residuo. En neuronas fija Hodgkin–Huxley, pide corrientes más
allá de Na/K, proporciona categorías de activación/inactivación y un menú que contiene los
protocolos reveladores. En materia oscura incluso declara que hay fuentes invisibles y solo deja
por inferir cuántas y dónde; tres especies se resuelve con álgebra+BIC, sin propuesta del LLM.

Por eso el paper mide principalmente **selección, composición, ajuste y experimentación eficiente
dentro de un vocabulario preparado**. Hay expansión de forma cuando el controlador abre la lista,
pero el detector del impasse, la orden de reestructurar, la memoria de candidatos, la comparación
y la elección del experimento están externalizados. No es evidencia de que un agente libre note la
falla y decida agrandar por sí mismo su espacio de hipótesis.

**Qué cambia o reafirma para WAGER:**

1. Reafirma una receta de mundo: varios modelos empatan en la rutina y una intervención legal los
   hace divergir mucho. Antes de agentes debemos certificar esa separación, pero el agente debe
   encontrar la prueba en la condición principal.
2. Ofrece una descomposición limpia para nuestras autopsias: **detectar el desajuste → reabrir la
   búsqueda → generar otra forma → seleccionarla → usarla**. El éxito híbrido no permite atribuir
   todos esos verbos al LLM.
3. Motiva un único control diagnóstico en el **próximo anfitrión interactivo** del mismo salto:
   después de registrar la Gaussiana, mostrar un fallo predictivo mecánico sobre perfiles
   completos, sin nombrar grupos. Esto no reabre la tanda cerrada de Perfiles persistentes.
   Si aparece la bifurcación, el cuello estaba antes de la generación; si no aparece, queda en
   generación/representación; si aparece en notas pero no en código, queda en compromiso.
4. La idea de cobrar ajuste y complejidad en una misma moneda converge con nuestra vara de dos
   bolsillos. No sustituye la certificación contra el mejor rival ni vuelve “correcta” una etiqueta
   estructural solo porque coincide con la verdad del simulador.

**Límite anti-recencia.** MDA es un paper de ingeniería: pregunta cómo construir un descubridor
más eficiente, mientras WAGER pregunta cuándo un agente realiza o no la jugada conceptual. Sus
episodios son además cortos (ocho experimentos en el protocolo común; química se extiende hasta
60), con acciones curadas y sin la historia, consecuencias y dependencias largas que WAGER quiere
instanciar después. Se toma como cantera de diseño y control, no como teoría ya demostrada sobre
por qué fallaron nuestros agentes.

Versión en llano y comparación directa: [WIKI-INDAGACION — MDA](../WIKI-INDAGACION.md#un-vecino-muy-cercano-model-discovery-agent-mda).

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

### RELECTURA DEL NÚCLEO DEL VICIO 1 — 11 papers, LEÍDOS 2026-07-14 (orden de Lucas: "revisemos LO REAL")

> Escritas con paciencia y sin jerga, para que cualquier sesión futura las entienda sin
> re-leer los papers. El mapa consolidado (escenario × lugar × gatillo) vive en
> [vicio-1-calibracion-de-creencias.md](vicios/vicio-1-calibracion-de-creencias.md).

#### Xie et al. — "Adaptive Chameleon or Stubborn Sloth" (2305.13300, ICLR 2024)

**Qué hicieron**: le preguntan al modelo algo que sabe de fábrica ("¿quién es el científico
jefe de DeepMind?") y guardan su respuesta con su justificación. Después fabrican evidencia
externa EN CONTRA — coherente y bien escrita (la genera ChatGPT; no un burdo cambio de
palabras) — y se la presentan de distintas maneras. **Qué encontraron**: (a) si la ÚNICA
evidencia presente es esa contradicción coherente, el modelo la acepta casi siempre — se queda
con lo suyo apenas 3.7% (ChatGPT) / 8.9% (GPT-4) de las veces: "camaleón"; (b) si la evidencia
llega MEZCLADA (una pieza que confirma lo suyo + una que lo contradice), vuelve a lo suyo 43%
(ChatGPT) / 65% (GPT-4); con dos piezas de cada lado: **99.8%** — "perezoso terco"; (c) el
ORDEN de presentación mueve el resultado hasta 49.5 puntos (PaLM2, Llama2); (d) con hechos
populares (muy vistos en entrenamiento) la terquedad sube (GPT-4: 80%). **Para WAGER**: la
condición del vicio no es "hay contradicción" — es "la contradicción CONVIVE con confirmación".
El mundo tiene que entregar la evidencia así: mezclada, como llega en la realidad.

#### RadLE (2509.25559) — radiología, GPT-5 vs radiólogos

**Qué hicieron**: 50 casos difíciles de diagnóstico por imagen, SOLO la imagen (sin historia
clínica). Compararon radiólogos certificados, residentes y los mejores modelos, y clasificaron
los errores leyendo los razonamientos. **Qué encontraron**: radiólogos 83%, residentes 45%,
GPT-5 30%, o3 23%, Claude Opus 4.1 1%. La categoría de error que nos importa: **"discordancia
hallazgos-conclusión"** — el razonamiento intermedio identifica el hallazgo correcto y la
conclusión final vuelve a otra cosa. Ejemplo real: identificó la elevación de la clavícula (la
pista correcta) y diagnosticó "luxación posterior de hombro". Verbatim: *"early fixation on
initial diagnostic hypotheses with subsequent favouring of supporting evidence, despite
identifying contradictory findings"*. **Para WAGER**: el lugar exacto del vicio es la
TRANSICIÓN del análisis a la conclusión — el mismo lugar donde nuestro mapa de timing encontró
las mezclas de compromiso en la entrega.

#### KellyBench — Grady et al. (2604.27865) — la temporada de apuestas

**Qué hicieron**: el agente juega una temporada COMPLETA de apuestas de la Premier League
(~100-150 fechas, 500-1000 llamadas a herramientas). Arranca con £100.000, tiene datos
históricos desde 1993, un sandbox para programar sus propios modelos estadísticos; cada fecha
ve las cuotas, apuesta, recibe resultados y datos nuevos. La estrategia matemática correcta
para dimensionar apuestas (criterio de Kelly) existe y es conocida. **Qué encontraron**: ningún
modelo termina con promedio positivo (el mejor: GPT-5.4, −7.9%; solo 3 de 25 corridas en
verde). Verbatim clave: *"la mayoría de las corridas ajustó su modelo estadístico UNA vez al
principio de la temporada y no lo re-entrenó jamás, a pesar de recibir datos frescos tras cada
fecha"*. Las corridas que sí se re-ajustaban: −11.1%; las estáticas: −70%. El caso estrella:
**GLM-5 escribió TRES documentos de autocrítica identificando correctamente la causa de sus
pérdidas** ("predije 40% de victorias locales y solo gana ~30%") **y no cambió nada**. Y la
brecha dice-hace: casi todos ESCRIBEN Kelly en su razonamiento y apuestan montos planos; uno
(Kimi) escribió la función de Kelly correcta y nunca la llamó desde su loop — terminó con una
apuesta accidental de ~£114.000. **Para WAGER**: el caso agéntico más parecido a nuestro mundo
(temporada larga + modelo propio + evidencia que llega sola + frontier 2026), con el fenómeno
completo: no re-ajustar, autocriticarse sin actuar, decir sin hacer.

#### Kumaran et al. (DeepMind, 2507.03120) — los dos sesgos en el mismo experimento

**Qué hicieron**: preguntas binarias (¿la latitud de tal ciudad es a o b?). El modelo responde;
en un segundo turno recibe el consejo de "otro modelo" con precisión declarada (50-100%) y
decide de nuevo. El truco: a veces le MUESTRAN su respuesta anterior y a veces se la OCULTAN
(pueden, porque la confianza se extrae de los logits sin crear memoria — imposible con
humanos). **Qué encontraron**: los dos sesgos opuestos a la vez. (a) Con su respuesta VISIBLE
cambia de opinión 13.1% vs 32.5% con la respuesta oculta — y si le dicen que esa respuesta la
dio OTRO modelo, el efecto DESAPARECE (p>0.1): defiende lo propio POR ser propio. (b) A la vez
el consejo CONTRARIO pesa 2.58× más de lo que la cuenta bayesiana manda (el favorable, casi
perfecto: 1.095×). (c) El cambio no es gradual: acantilado en confianza ~0.77 — debajo cambia
casi siempre, arriba casi nunca. **Para WAGER**: rigidez y sobre-reacción NO son extremos de
una perilla — coexisten en el mismo modelo. Por eso la nota del par va por el MÍNIMO y el
gemelo estable (que castiga sobre-reaccionar) es tan necesario como el gemelo con cambio.

#### When Truth Is Overridden (2508.02087) — "creo que la respuesta es X"

**Qué hicieron**: opción múltiple (MMLU) de UN turno donde, ANTES de que el modelo responda,
el usuario dice "creo que la respuesta es B" (incorrecta). **Qué encontraron**: 63.7% promedio
de acuerdo con la opinión incorrecta (rango 46.6–95.1 en 7 familias) — **en modelos abiertos
chicos** (Llama3.1-8B, Falcon…). Decir "soy profesor" o "soy principiante" no cambia casi nada
(~4.4 puntos): la mera opinión alcanza. En tercera persona ("ellos creen…") baja 13.6 puntos.
**Advertencia de lectura (importante)**: la opinión llega ANTES de la respuesta — esto mide
FORMACIÓN sesgada, no revisión de una creencia ya formada; y son modelos chicos — no proyectar
estos números a frontier.

#### Yang et al. (2505.16170) — la perilla interna de la retractación

**Qué hicieron**: hacen que el modelo dé una respuesta incorrecta ("nombrá un político nacido
en Nueva York" → "Hillary Clinton"), verificando APARTE que el modelo sabe que es incorrecta
(contesta bien las preguntas de verificación). Lo dejan continuar y miden si se retracta solo.
**Qué encontraron**: se retracta apenas 11–26% de las veces, aun sabiendo. Con sondas sobre
las activaciones internas: lo que predice la retractación es la "creencia interna" del momento
(AUROC 0.7-0.8), NO el conocimiento real (~0.5 = azar). Con steering causal (sumar/restar un
vector interno) la retractación se enciende (70%+) o se apaga (~0%) a voluntad; transfiere a
matemática (GSM8k: +20% corrigiendo en el punto del error). **Para WAGER**: existe una perilla
interna de "me lo creo / no me lo creo" SEPARADA del conocimiento — el vicio es un estado, no
una carencia. (Modelos 7-8B.)

#### Pal et al. (2511.13240) — "Knowing What You Know Is Not Enough"

**Qué hicieron**: miden la confianza declarada del modelo (por logits, por muestreo, por número
verbal) y la comparan con sus ACCIONES en tres escenarios: apostar según sus creencias, decidir
si usar un buscador, y defender o soltar su respuesta cuando lo desafían. **Qué encontraron**:
apuesta en dirección CONTRARIA a su confianza declarada (el mejor modelo: apenas 79% de
consistencia direccional); NO invoca el buscador teniendo confianza casi cero (correlación
0.472); y la inversión: **defiende con terquedad respuestas en las que declara POCA confianza
y suelta las de ALTA confianza**. La calibración estática no predice la coherencia en acción
(r=0.17) — Gemini 2.5 Pro, bien calibrado, es de los más incoherentes. **Para WAGER**:
preguntar la creencia no alcanza JAMÁS — hay que mirar qué hace. Las tres vistas del diseño
(declara / compra / entrega) salen de acá.

#### Zhang et al. (2305.13534) — el snowball: comprometido en el primer token

**Qué hicieron**: preguntas Sí/No que requieren cómputo (¿es primo 9677? ¿hay ruta entre A y
B?). El modelo responde y justifica. **Qué encontraron**: el modelo se compromete con el Sí/No
en el PRIMER token (95-98% de las veces) — antes de razonar — y después fabrica la
justificación que lo sostenga (una factorización falsa, un vuelo inexistente). Lo clave:
mostradas POR SEPARADO, el mismo modelo reconoce esas justificaciones como falsas (ChatGPT
67%, GPT-4 87%). "Pensá paso a paso" mejora el acierto pero en los fallos el 95% sigue
fabricando. **Para WAGER**: el compromiso precede al razonamiento; la fabricación es presión
de coherencia con lo ya dicho. La obra propia empieza en la primera palabra.

#### ScienceAgentBench (2410.05080) — la contraevidencia: el error duro SÍ se usa

**Qué hicieron**: 102 tareas reales de descubrimiento con datos (de 44 papers publicados); el
agente escribe un programa que resuelve la tarea. Con "self-debug": ejecuta su código, ve los
errores reales, itera. **Qué encontraron**: el feedback de ejecución casi DUPLICA el éxito
(Claude-3.5-Sonnet: 16.7%→32.4%, ×1.94 — y 17 veces más barato que el framework más complejo).
El error DURO e inequívoco se usa y bien. Lo que NO arregla ni con feedback: errores ambiguos
de procesamiento de datos científicos heterogéneos y APIs de dominio alucinadas. **Para
WAGER**: delimita el vicio por el otro lado — no vive en la señal dura, vive en la ambigua.
El mundo debe habitar la ambigüedad calibrada.

#### Barkett et al. (2508.01545) — escalada de compromiso: identidad y consenso

**Qué hicieron**: el paradigma clásico de Staw ("Big Muddy"): invertís $10M en una división;
años después ves resultados (buenos o malos); decidís cómo repartir $20M más. Probaron:
decisión individual, rol de asesor, deliberación entre agentes, y un rol con la identidad
FUSIONADA (sos el VP que defendió esa división 20 años, con acciones, reputación, divorcio y
matrícula del hijo colgando de la decisión). **Qué encontraron**: individual = racional (tras
malas noticias asigna $4.65M vs $14.41M tras buenas: desinvierte; ~cero escalada). Asesor:
apoya escalar solo 5.6%. Deliberando entre PARES SIMÉTRICOS: **99.2% escala**. Identidad
fusionada: **68.95% del presupuesto a la división perdedora** (97.45% de escalada alta,
d=2.00). **Para WAGER**: replica nuestro 0/60 del pozo (individual frío = racional) Y muestra
dónde vive el fenómeno: identidad + consenso. Candidato v2 documentado: "vos defendiste este
modelo" / "lleguen a consenso".

#### Jeong et al. (2602.00851) — la creencia pre-cargada curva la política

**Qué hicieron**: agentes con herramientas (investigación web con informe final; y código).
Manipulan creencias de dos maneras: PRE-cargada en el prompt inicial, o persuasión a MITAD de
la tarea. **Qué encontraron**: la pre-cargada curva la CONDUCTA: −26.9% búsquedas, −16.9%
fuentes únicas (significativo), sostenido a lo largo de tres tareas seguidas — y el informe
final queda *"fluent and superficially plausible"* (baja la cobertura y la calidad, pero no se
nota a simple vista). La persuasión a mitad de tarea: débil y errática. (Modelos
chicos-medianos.) **Para WAGER**: converge con nuestro mapa de timing (la formación arrastra
la política; el medio no muerde) y con nuestra sonda de formación (compras arrastradas 7/19
sin daño visible). Moraleja de medición: mirar las COMPRAS, no solo la entrega.

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


## Cluster POSICIONAMIENTO del mapa de carga — LEÍDOS COMPLETOS 2026-07-31 (4 lectores en paralelo; extracción con citas verbatim, un archivo por paper en `docs/research/2026-07-31-lectura-*.md`)

Tras el refoco (ADR 0153) y los 4 repasos (`2026-07-31-repaso-final-{claude,codex}{,2}.md`), los 16
trabajos más cercanos se leyeron A TEXTO COMPLETO. Una línea por fuente; el detalle vive en su archivo:

| Fuente | Una línea (leída, no de resumen) | Veredicto |
|---|---|---|
| BeliefTrack / When Should Models Change Their Minds ([2605.30219](https://arxiv.org/abs/2605.30219)) | pares limpio/ruido bifurcados + reward simbólico cero-LLM + RL que baja fallas 99%→0-30% — en espacio de hipótesis discretas, sin entrega ni carga | COMPITE parcial |
| Model Discovery experimental ([2607.06413](https://arxiv.org/abs/2607.06413)) | único que puntúa modelo ejecutable contra verdad oculta (KL); la KL es métrica de salida, no dosis; sin forks ni trabajo previo | COMPITE parcial |
| Causal Agent Replay ([2606.08275](https://arxiv.org/abs/2606.08275)) | do()+re-ejecución; validación solo en SCMs sintéticos (mayormente teórico); "LLM judge injects its own noise" | VALIDA método |
| BACKTRACE ([2607.27484](https://arxiv.org/abs/2607.27484)) | lo AFIRMADO no predice lo USADO (AFS<0.43); "fixes everything except the one manipulated variable" | VALIDA + vigilar |
| BayesBench ([2606.30850](https://arxiv.org/abs/2606.30850)) | infieren la estructura, no la traducen a predicción; oráculo cerrado solo en 2/4 entornos | VALIDA |
| Bayesian Teaching ([2503.17523](https://arxiv.org/abs/2503.17523)) | imitar la POSTERIOR generaliza mejor que imitar la respuesta (→ E2) | VALIDA |
| BASIL ([2508.16846](https://arxiv.org/abs/2508.16846)) | el empujón EMPEORA a los que sobre-actualizan y MEJORA por accidente a los que sub-actualizan → estratificar F por régimen basal del donante | CAMBIA DISEÑO |
| Not-consistently-Bayesian ([2605.06915](https://arxiv.org/abs/2605.06915)) | a veces Bayes-exacto pierde contra el prior implícito → F baja ≠ apego sin descartar prior competitivo (defensa: mundos frescos) | CAMBIA DISEÑO |
| STALE ([2605.06527](https://arxiv.org/abs/2605.06527)) | reconoce-que-venció y actúa igual; TODO el scoring con juez-LLM | VALIDA fenómeno |
| Seeing Isn't Believing ([2604.17252](https://arxiv.org/abs/2604.17252)) | inercia medida por acciones, reward binario del entorno cero-LLM; andamiaje estimar-verificar-actualizar (+18pp) → brazo comparador nuestro | CAMBIA DISEÑO |
| LURE ([2605.26438](https://arxiv.org/abs/2605.26438)) | ranking de sycophancy INVERTIDO entre benchmark posado y replay realista — con alcance: ρ=−0.88 SIN un outlier, crudo ρ=−0.56 p=0.09; scoring 100% juez-LLM | VALIDA fuerte |
| MemSyco-Bench ([2607.01071](https://arxiv.org/abs/2607.01071)) | sycophancy por memoria DEL USUARIO, no obra propia — vecino más lejano de lo que parecía | menor |
| Martingale Score ([2512.02914](https://arxiv.org/abs/2512.02914)) | score = pendiente OLS de Δb sobre b_prior; NO portable tal cual (juez elicitando creencia verbal; y las 252 ramas reusan 14 priors → no son observaciones independientes) — la FORMA sí, con creencia leída de la ENTREGA y tanda diseñada al efecto | CAMBIA DISEÑO |
| GeneBench-Pro (OpenAI) ([PDF](https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf)) | grading por scripts con tolerancias POR CAMPO (eval_config leído); todo-o-nada declarado como limitación — lo que F resuelve | ANCLA posicionam. |
| Context Rot (Chroma) ([reporte](https://www.trychroma.com/research/context-rot)) | 18 modelos, 194k llamadas: el relleno degrada según posición/coherencia/similitud → igualar TODO eso entre brazos o el efecto es contexto, no creencias | CAMBIA DISEÑO |
| PABU ([2602.09138](https://arxiv.org/abs/2602.09138)) | homónimo engañoso ("belief update" = qué retener del historial por eficiencia) | descartado |

## Lecturas del programa de saltos — LEÍDAS COMPLETAS 2026-08-07 (4 lectores en paralelo)

KellyBench (2604.27865) · The Einstein Test (2501.06948) · Einstein's Footsteps (2607.27794) ·
Gentner "Analogy" (OECS/MIT Press 2025). **Extracción completa con citas verbatim, números,
verificación de claims previos y límites, en un solo doc:**
[`docs/research/2026-08-07-lecturas-programa-saltos.md`](research/2026-08-07-lecturas-programa-saltos.md).
Correcciones que estas lecturas destaparon (ADR 0115 manda registrarlas acá):
- **KellyBench**: nuestro claim de segunda mano decía "rigidez ante no-estacionariedad" a secas;
  el paper NO inyecta un switch a mitad de temporada (la no-estacionariedad es la natural del
  dominio) y la rigidez no es uniforme (adaptativos −11.1% vs estáticos −70.0%); la firma fina
  es **knowledge-action gap** (diagnostican por escrito y no corrigen). Corregido en
  vicio-1 §1.A y en el libro de los saltos.
- **Footsteps**: dice "MANY great leaps" (no todos) y "not JUST producing" (el cuello es la
  selección/taste, no solo la generación). Ajustado en el libro.

## Lecturas de LIBROS del programa de saltos — campaña 2026-08-09 (7 lectores en paralelo; PDFs provistos por Lucas)

Cola completa: Darden 1991 · Ohlsson 2011 · Klein 2013 · Boden 2004 · Thagard 1992 ·
Magnani 2001 · Aliseda 2006. **Extracciones verbatim en un solo doc:**
[`2026-08-09-lecturas-libros-programa-saltos.md`](research/2026-08-09-lecturas-libros-programa-saltos.md).

- **Aliseda 2006, *Abductive Reasoning* (Springer, Synthese 330)** — **LEÍDO completo 2026-08-09**
  (244/244 pp., 13 tandas). Corrección que destapó (ADR 0115 manda registrarla acá):
  **novelty/anomaly NO formaliza nuestro par generar/aceptar** — tipifica el DISPARADOR; la
  generación del candidato es común a ambas operaciones y lo distintivo de la anomalía es la
  CONTRACCIÓN previa (revisión = contracción + expansión, identidad de Levi). Además: su
  generador mecánico (tableaux) es cerrado por vocabulario → formaliza la FRONTERA del salto,
  no el salto; con inferencia estadística el tipado disparador→operación se ensucia (caso Jane
  Jones) — nuestro corte temporal server-side queda como lente primaria. Bonus: operador p′
  ("hacer una distinción" = partir un átomo en dos) como agrandamiento de vocabulario
  MECÁNICO, candidato a la librería; y la tríada éxito/fallo/LAGUNA (mundos tipo-laguna:
  sonda limpia de generación, sin contradicción que resolver).
- **Boden 2004, *The Creative Mind* (2ª ed., Routledge)** — **LEÍDO completo 2026-08-09**
  (359/359 pp.). Correcciones: (a) nuestro corte reparte/agranda = su explora/transforma,
  PERO pide graduar profundidad (posición en el orden generativo) y medir contra el espacio
  EFECTIVO del agente (lección geometry-program: lo que parece salto puede ser exploración de
  otra representación — "0/9 no agrandó" exige elicitar el menú previo); (b) "combinación a
  distancia" debe incluir operadores sobre las REGLAS (soltar/negar/re-representar) o su
  cap. 3 nos clasifica de combination-theory; (c) a favor: activación-de-estructura-conocida
  = mecanismo MAYORITARIO de la ciencia H-creativa (p. 222); la ayuda = telescoping (p. 195);
  reward cero-LLM fundamentado (evaluation bottleneck automatizable solo en dominios
  regulados, pp. 9/320). Partir generación/reconocimiento como outcomes (Copérnico tachó las
  elipses, p. 96).
- **Ohlsson 2011, *Deep Learning* (Cambridge UP)** — **LEÍDO completo 2026-08-09** (texto
  principal íntegro pp. 3-392 + notas sustantivas). LA fuente del episodio de impasse:
  trigger = feedback negativo del propio intento, persistente, DETECTADO y fuerte
  (pp. 107/117 — el impasse es el estado, no el gatillo); "transparencia del entorno a los
  efectos de las acciones" = nuestro RAW/VISIBLE textual (p. 117a); el resumen mecánico hace
  de tutor (p. 247); la señal cualitativa del residuo dirige, la binaria no informa
  (pp. 222-228). Auditó las 7 compuertas de la ficha v1 → 3 FALTANTES (impasse unwarranted ·
  cerrar ruta periférica: el 2º lote debe evaluar el modelo PARCHADO · grano del resumen
  declarado) — addendum propuesto en la ficha. Para creencias INVIERTE el signo: convierte el
  rival exitoso, no el fallo del residente (resubsumption, pp. 348/358) — sin contender, más
  anomalía visible = más "outlier". Portar: tests débiles (p. 122-123), prevalencia
  impasse→insight 3-41% (n. 15), progress criterion como rival vivo (p. 125).
- **Darden 1991, *Theory Change in Science* (Oxford UP)** — **LEÍDO completo 2026-08-09**
  (324/324 pp. del escaneo; DJVU convertido a PDF). Confirma candidatas con guías operativas
  (BORRAR: 2 casos + 4 condiciones p. 78; scan en 2 formas; localización-por-firma;
  monster/model) y aporta DOS operadores nuevos: SPLIT/DELINEATE (p. 278) y
  EXPLICITAR-SUPUESTO-IMPLÍCITO (pp. 101-104). Correcciones al careo publicado (aplicadas en
  el libro de saltos): ops 3/4 → correlato PARCIAL; op 7 → moderada (contaminación de Castle
  = hipótesis perdedora); op 9 con puntero (Shapere p. 249); ⚠ el ancla del op 2 (letales
  2:1) es MONSTER anomaly en su marco (p. 102) — no citarla como "cambio de teoría". La
  escalera ordinal de respuestas (p. 270) es rúbrica cero-LLM. REEMPLAZAR-mecanismo: ~6
  episodios; el operador unificado es aporte nuestro. Su cap. 16 pide nuestro programa
  (pp. 279-281).
- **Magnani 2001, *Abduction, Reason and Science* (Kluwer)** — **LEÍDO completo 2026-08-10**
  (texto plano extraído; caps. 1-7 íntegros, citas verificadas con página impresa).
  [Extracción](research/2026-08-10-lectura-magnani-2001.md). **De acá sale nuestra distinción
  madre** (selectiva vs creativa), citada de segunda mano hasta hoy. La lectura la CONFIRMA
  textualmente (pp. 19-20, 25) y la CORRIGE en cinco puntos que tocan titulares:
  (1) lo que medimos es **abducción EXISTENCIAL** (Thagard/PI, p. 49), una especie dentro de la
  creativa — y es la misma en la que fallaban BACON y GLAUBER (p. 50): el claim es más fuerte, no
  más débil; (2) la creatividad es **relativa al repertorio del agente** (p. 48) → el test de
  contaminación pasa de higiene a **constitutivo del claim**; (3) "lo genera y lo mata: es un
  outlier" es **monster-barring** (paso 2 de Darden, p. 132) — paso LEGÍTIMO del protocolo, no
  vicio; lo que separa vicio de virtud es la **ausencia del test de fecundidad** (Poincaré p. 160,
  Lakatos p. 162) — explica por qué no lográbamos castigarlo; (4) el zoom adaptativo NO es
  abducción manipulativa fuerte (la conjetura precede a la compra; p. 65); (5) el fallo que
  documentamos es el del "caso de los patos" (p. 109: detectar la anomalía sin poder explicarla es
  el comportamiento ESPERADO de una máquina selectiva) — para reclamar déficit creativo hay que
  mostrar que el agente TENÍA los ingredientes. Regalos de diseño: la creativa es **segunda línea**
  (se activa cuando la localización dentro del repertorio fracasa, p. 132) → compuerta verificable
  de "instancia creativa"; los **abducibles** como perilla del menú (p. 123: el menú ES el
  criterio); el certificado de **ambigüedad** (p. 22: sin ambigüedad no hay abducción, hay lookup);
  y la amenaza de Koslowski (p. 143: con solo covariación y sin mecanismos causales medimos la
  pobreza del mundo) — la explicación rival más fuerte contra el 0/9.
- **Klein 2013, *Seeing What Others Don't* (PublicAffairs)** — **LEÍDO completo 2026-08-10**.
  [Extracción](research/2026-08-10-lectura-klein-2013.md). **El contrapeso del programa**: 120
  casos de campo con doble codificación (78%→98% de acuerdo). Conteos: conexiones **82%** ·
  contradicciones **38%** · **impasse solo 25%** · coincidencias 10% · curiosidades 7,5%; súbito
  56% / **gradual 44%**; incubación 5/120. Corrige nuestro mapeo: **contradicción ≠ impasse** (van
  en direcciones OPUESTAS: desesperación TIRA el ancla débil, contradicción CONSTRUYE sobre ella;
  y sus protagonistas de contradicción NO estaban atascados) → **nuestro experimento construye un
  impasse, no una contradicción, y cae en la celda MENOS poblada de su corpus (contradicción ×
  desesperación: "only a few cases") → predice TASA BASE BAJA: problema de potencia a presupuestar
  ANTES**. Corrobora el acotamiento a "episodios impulsados por anomalías" con la concesión del
  propio **Ohlsson** (*"Our current theories are powerless to explain this type of insight"*).
  Regalos: el **catálogo Chinn & Brewer** de 4 maneras de descartar anomalías (nuestros agentes lo
  reproducen; y en sus 45 casos de contradicción, **42 exploraron la anomalía y NINGUNO la explicó
  y descartó** → nuestros agentes se comportan como los **gemelos fallidos**); el **garden path**
  con **canal privado instrumentado** (7/7 equipos fallaron, pero los diarios individuales
  mostraron que la señal SÍ se detectaba y no se subía → separar rastro privado de reporte público
  convierte el 0/9 en diagnóstico); y el precedente humano de **meta obsolescente** (Sengupta,
  HBR 2008). Advertencia dura: **varias de sus nueve reglas anti-diseño describen WAGER** (tarea
  asignada, episodios cortos, saberse evaluado, tarea deliberadamente nueva, y puro impasse).
- **Thagard 1992, *Conceptual Revolutions* (Princeton UP)** — **LEÍDO completo 2026-08-10**.
  [Extracción](research/2026-08-10-lectura-thagard-1992.md). Su escalera de 9 grados **ES** una
  matriz componente×verbo aplastada por severidad (*"conceptual change consists of adding or
  deleting nodes and links"*) → **ratifica la relectura del supervisor**. Golpes: (a) **nuestros 11
  operadores son TODOS adiciones**, mientras el movimiento revolucionario más frecuente de su
  corpus es el **re-anclaje** (branch jumping, 8 casos, **cero** operadores nuestros) y el
  **colapso/borrar distinción**; (b) **`entidad oculta` es su escalón MÁS BARATO y declarado NO
  revolucionario** (quarks, genes, el electrón); (c) `transferencia/analogía` es **error de
  categoría** (mecanismo de generación y criterio de evaluación, no tipo de cambio);
  (d) `unificación` **conflaciona** coalescence (monótona) con collapse (revisionaria); (e) falta
  el eje **monótono/revisionario**, y el escalón intermedio `agregar-regla` — **casi seguramente lo
  que un LLM hace cuando cree que salta**. REPLACE sigue siendo delete+add (no demuestra
  irreducibilidad) pero **RE-ANCLAR y RETIPAR sí son irreducibles**. Y ⚠️ **riesgo directo sobre
  nuestra vara**: su Objeción 2 es una batería de 5 tests contra la compresión de dos partes —
  sobre todo **"being explained"** (una hipótesis explicada por otra GANA aceptabilidad, y el
  conteo `#E − #H` la penaliza: **penalizaríamos la forma del argumento de Darwin**) y
  **unificación** (insensibilidad al compartir auxiliares). **Verificables sin gastar API.**
  Bonus: **ECHO es una vara alternativa enteramente cero-LLM** si el grafo de explicación se deriva
  por simulación; y da la **dosificación del vuelco** (1-2 fenómenos no voltean, 3 sí).

**CAMPAÑA DE LIBROS CERRADA 7/7** (2026-08-09→10): Aliseda · Boden · Ohlsson 2011 · Darden 1991 ·
Magnani 2001 · Klein 2013 · Thagard 1992. Todos a texto completo, todos con extracción y
correcciones registradas. Los PDFs se borraron tras leerlos (pedido de Lucas).

## Tensiones VIVAS entre fuentes (la tabla anti-recencia)

> **Por qué existe** (Lucas, 2026-08-10): *"tampoco nos creamos que lo que dicen estos autores es
> la verdad absoluta... incluso entre ellos se pueden contradecir. TENGAMOS EN CUENTA TODO. No
> caigamos en el error de solo tener en cuenta lo último que vamos leyendo."* Esta tabla registra
> las contradicciones REALES entre fuentes del corpus para que ninguna se arbitre en silencio a
> favor de la última leída. Regla: una lectura MOTIVA sospechas (a verificar con cómputo o datos
> propios); no DICTA diseño, y jamás cambia un pre-registro firmado.

| # | Tensión | Un lado | El otro | Cómo la llevamos (sin arbitrarla) |
|---|---|---|---|---|
| 1 | **¿El impasse es necesario?** | Ohlsson 1999/2011: sin fallo persistente y detectado no hay reestructuración (y él mismo declara sus tests "débiles", prevalencia 3-41%) | Klein 2013: impasse en solo 25% de 120 casos reales; el propio Ohlsson concede que sus teorías "son impotentes" ante Darwin/Malthus | El claim del experimento quedó acotado a "una ruta de activación bajo anomalía", NO teoría universal del insight. El brazo de conexión-sin-fallo queda para otro mundo |
| 2 | **¿Súbito o gradual?** | Ohlsson: reestructuración (evento); el "aha" | Klein: 44% graduales; Nersessian: es una CADENA de modelos, no un acto | Binario pre-registrado sigue primario (es lo firmado); escalera ordinal como secundario declarado; la cadena de eventos con timestamps registra todo — que los datos hablen |
| 3 | **¿Los que descubren descartan anomalías?** | Klein: en sus 45 contradicciones, 42 exploraron y NINGUNO descartó | Dunbar in vivo: el descarte-como-error es el DEFAULT del científico solo; Heuer/Findley & Scott: los profesionales descartan sistemáticamente; Magnani: descartar a veces es CORRECTO (Copérnico) y monster-barring es paso legítimo | El corpus de Klein es de GANADORES (sesgo de selección declarado por él) — no contradice a Dunbar: lo complementa. Nuestra vara no castiga el descarte per se; castiga descartar SIN test de fecundidad el punto que porta la señal |
| 4 | **¿Qué tan difícil es "entidad oculta"?** | Thagard: su escalón estructural MÁS BARATO, "no revolucionario" (genes, quarks) | Nuestro dato propio: 0/9 y 0/10 agentes fallan EXACTAMENTE ahí; Magnani: los descubridores automáticos también fallaban ahí | Ejes ORTOGONALES: él mide severidad de reorganización en la ciencia humana; nosotros dificultad de ACTIVACIÓN en agentes. Que fallen en el escalón "barato" AFILA el hallazgo |
| 5 | **¿Sirve listar supuestos / mandar método?** | La tradición analítica (ACH de Heuer como método formal) | Klein: "ninguna evidencia de que sirva"; Dhami 2019: ACH dio NULO con 50 analistas reales; nuestro 0/3 del "teatro" | Acá los datos convergen contra el método mandado — pero se registra que ACH-nulo es UN estudio y nuestro 0/3 es n=3: convergencia sugestiva, no ley |
| 6 | **¿Castigar el residuo inexplicado?** | Nuestro instinto de scoring (el modelo debería explicar todo) | Magnani/Poincaré: Newton convivió con el perihelio de Mercurio; "hasta que el rival compite, no hay razón para eliminar la vieja"; Klein: la mayoría de los puntos desviados SON ruido | El mundo no castiga residuos per se: hace que la anomalía descartada sea CONSECUENTE para el objetivo declarado (necesidad teleológica) — descartar deja de ser gratis solo cuando el mundo lo cobra |
| 7 | **¿La combinación explica la creatividad?** | Nuestra frase "no hay magia, hay combinación a distancia"; Poincaré/Koestler | Boden cap. 3: la teoría-combinación pura NO distingue lo nuevo de lo imposible-antes; exige operadores sobre las REGLAS | Resuelta por refinamiento (no por recencia): las "piezas" incluyen ediciones de reglas — registrado en el marco |
| 8 | **¿El grupo corrige o empeora?** | Dunbar: el corrector real es el lab meeting; Ohlsson: crítica mutua "well supported" | Barkett: pares simétricos = 99.2% escalada; Klein garden path: 7/7 equipos peor que sus individuos; Jr. AI Scientist: el revisor induce fabricación | No es contradicción sino CONDICIONAL: lo que funciona es el crítico SIN propiedad de la teoría (Findley & Scott). Diseñable como brazo, no como supuesto |

**Mantenimiento**: tensión nueva que aparezca en una lectura → fila nueva acá, en el momento.
Una fila solo se cierra cuando NUESTROS datos (no otra lectura) la resuelven — y ahí migra al
índice de hallazgos con su evidencia.

### "Why Do LLMs Struggle in Strategic Play? Broken Links Between Observations, Beliefs, and Actions" (arXiv 2605.00226) — LEÍDO 2026-08-11 (HTML v1 completo vía fetch, extracción con citas)

Estaba de segunda mano desde julio (repasos: "compite conceptualmente, riesgo alto de
solapamiento"); pedido de Lucas → texto completo. Llama 3.1 70B, Qwen3 32B, gpt-oss 20B en
juegos repetidos 2×2 (800 trials), Kuhn Poker generalizado (400) y The Chameleon (230).

- **BCC (Bayesian Coherence Coefficient) es CERO-LLM**: correlación de Pearson entre los
  cambios de log-odds de la creencia del modelo y los cambios bayesianos correctos computados
  de un modelo de verosimilitud — mecánico, sin juez. Es un ejemplo limpio de medir una
  trayectoria y no solo el resultado final. La posible traducción a WAGER queda analizada en
  `como-medimos.md`; **no se incorpora ninguna métrica ni se modifica D2 por esta lectura**.
- **La sub-actualización CRECE con el horizonte** (lo que trajo Lucas): *"internal belief
  updates transition from early updating at correct magnitude (slope ≈ 1) to later
  under-updating (slope << 1)"*; el BCC interno cae a menos de la mitad para la ronda 10
  (juegos simples) o el TURNO 3 (juegos complejos). Consecuencia declarada por ellos:
  *"underreaction to new information or persistence in outdated hypotheses"*.
- **El vínculo creencia→acción está ROTO por método causal**: probes internos superan a los
  verbales (saben más de lo que dicen); steering de creencias internas mueve la acción solo
  ~50-70% (≈azar en Kuhn/gpt-oss). *"Internal beliefs have weak causal influence on action
  selection."* → **evidencia convergente, no réplica de D1**: ellos sí midieron e intervinieron
  creencias internas; D1 no lo hizo, solo observó la distancia entre evidencia comprada y modelo
  entregado. Ambos vuelven plausible una falla entre representar algo y actuar con ello, pero no
  autorizan afirmar que en D1 los agentes internamente “sabían”.
- **Sesgos de superficie en creencia→acción**: first-item bias (elige A por posición aunque
  su creencia interna favorezca B).
- Sin explicación mecanística del decaimiento (lo declaran fenómeno); límites: modelos ≤100B
  abiertos y cuantizados, horizontes cortos.
- ⚠️ **Anti-recencia**: sus horizontes son rondas homogéneas de juego; nuestros episodios
  tienen eventos heterogéneos — la transferencia del decaimiento NO está garantizada. Entra
  como RIVAL pre-declarada de D2 y como convergencia, no como verdad.

**Impacto inmediato**: rival nueva pre-declarada en la ficha D2 ANTES de la tanda — "el
rebote del turno 8 llega TARDE en el horizonte: si REBOTE no mueve, puede ser deriva de
sub-actualización tardía (Strategic Play), no indiferencia" — parcialmente separable porque
REBOTE entrega el desajuste masticado (no exige actualización fina). La lectura no decide
adoptar su métrica: primero interesa entender si, con las armas propias de WAGER, podemos separar
evidencia disponible, reconocimiento explícito, cambio de modelo y acción.

### "Model Discovery Agent (MDA): LLM-assisted Bayesian experiment design for data-efficient discovery of mechanistic world models" (arXiv 2608.09696, Kevin Murphy) — LEÍDO 2026-08-13 (abstract + HTML v1 completo vía fetch con extracción dirigida; pedido de Lucas)

**Qué es**: NO es un benchmark de juicio — es un SISTEMA que descubre mecanismos: el LLM actúa
solo como **proposer** de estructuras candidatas y toda la inferencia la hace maquinaria bayesiana
clásica (SMC para posteriors de parámetros y estructura, SBI para verosimilitudes intratables,
VoI para elegir el experimento siguiente). Proposers: Claude Opus 4.7 y DeepSeek-v4 Pro.
Benchmarks: ForceBench (física, sobre DiscoverPhysics — el paper que YA leímos y que valida
nuestro vicio 4), ChemBench (AutoSciLab) y NeuronBench (Hodgkin-Huxley, 6 neuronas misteriosas,
nuevo). Evaluación mecánica (nMSE / RMSLE / accuracy simbólica), sin juez-LLM.

- **M-open con disparador MECÁNICO** (lo más relevante para nosotros): *"If the error is too
  large, MDA expands the hypothesis space by prompting the LLM to suggest a novel unnamed
  mechanism"* — el chequeo predictivo dispara automáticamente cuando el residuo pasa un umbral
  (Algoritmo 1, línea 7). **Es exactamente nuestro C1 (el golpe) automatizado por fuera del
  agente.** Nuestra tanda de Perfiles persistentes es el complemento: 9/10 nunca ejecutaron ese
  test (uno ANUNCIÓ que usaría un modelo rico si encontraba multimodalidad y no lo hizo).
- **Su ablación contiene nuestra tesis**: el brazo "LLM agent" (LLM diseña + LLM pronostica, sin
  andamio) pierde feo — ForceBench ~0.1+ nMSE vs 0.013 de MDA con 8 experimentos; ChemBench
  LLM-AutoSciLab 42% con B=60 vs 56% de MDA con ~8. El LLM desnudo no descubre.
- **El proposer falla incluso CON andamio** (límite que ellos declaran): *"LLM proposals can miss
  ground truth"* — en NeuronBench el LLM omite la corriente de bajo umbral. Evidencia externa
  extra del cuello de generación de candidatos.
- **Su criterio anti-curve-fit es la INTERVENCIÓN**: *"Predicting the answer to interventional
  'what if' questions --- the outcome of an action never taken --- requires a mechanistic, causal
  model, not a curve fit"*; y critican a PySR por devolver *"numerically-fit but mechanistically
  meaningless expressions"* (RMSLE 0.001 con forma simbólica incorrecta).
- VoI = elegir el diseño que maximiza I(M;Y|D); con ruido gaussiano se reduce a máxima varianza
  predictiva posterior, dominada por el desacuerdo entre modelos. Es nuestro D_pre — ellos lo
  usan para ELEGIR por el agente, nosotros para MEDIR si el agente compra evidencia discriminante.
- Límites declarados: verosimilitud sintética determinista (la extensión estocástica con filtros
  de partículas es cara), estadísticos resumen hechos a mano o aprendidos, proposals que se
  pierden la verdad.

⚠️ **Anti-recencia**: es un paper de RENDIMIENTO (SOTA con andamio), no de medición de juicio;
sus resultados no dicen nada sobre qué hace un agente solo salvo por su propia ablación. No
adoptar su arquitectura: darle el exoesqueleto al agente destruiría exactamente lo que medimos.

**Impacto directo**: su criterio interventional es la salida al callejón que dejó la auditoría
de D2 (una skew-normal copiaba la predicción sin tener la estructura, S=0.671 > 0.5, y no hay
base operacional para castigar el vocabulario interno de un modelo que reproduce todas las
consecuencias). Camino: el próximo anfitrión debe puntuar **predicción bajo intervención**, donde
dos tipos ocultos responden distinto a una acción nunca tomada y ninguna familia sin partición
puede copiar la respuesta. Registrado como requisito de diseño, no como adopción de su método.
