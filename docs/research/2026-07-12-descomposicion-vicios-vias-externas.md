# Descomposición de vicios — vías externas (respuestas 1 y 2 de la IA de Lucas; 2 más por venir)

2026-07-12. Guardadas VERBATIM para la síntesis (el texto completo está en la conversación de la
sesión; acá el índice de lo que cada una aporta + el estado de las disputas).

## Disputas auditadas
- **El 68% (vicio 1)**: la Respuesta 2 sospechó que era un número humano (Siebert & Siebert 68.5%)
  mal atribuido. VERIFICADO HOY contra arXiv 2604.18805: el abstract dice verbatim *"evidence is
  ignored in 68%% of traces, refutation-driven belief revision occurs in 26%%"*. La cita nuestra
  QUEDA. (La sospecha era del tipo correcto — precedente caso-67.)

## Lo NUEVO que aporta la Respuesta 1 (no estaba en la vía Claude)
- Sicofancia como polo del par del vicio 1: Fanous et al. 58.2%%; "creo que la respuesta es X"
  induce acuerdo 63.7%% promedio; circuito mecanístico en Gemma-2-2B (silenciarlo: 28→81%%).
  [POR-LEER]
- Sobre-corrección: actualiza 2.5× más fuerte ante feedback CONTRARIO que ante apoyo. [POR-LEER]
- Confabulación anclada (2604.25931): UN hecho intermedio confirmado AUMENTA las respuestas
  confiadas-incorrectas; escala con capacidad. [POR-LEER]
- Anclaje: al revés de Vaccaro — Suri et al. / Lou & Sun dicen robusto y que empeora con capacidad;
  mitigaciones por prompt inefectivas. [POR-LEER — tensión con Vaccaro a resolver en síntesis]
- TheAgentCompany: atajos falsos con traza (renombró a otro usuario para "encontrar" a la persona
  buscada); inventa valores en campos vacíos; da por cumplida la tarea prematuro. [POR-LEER]
- MAST: 1.600+ trazas multi-agente anotadas (HuggingFace mcemri/MAD), κ=0.88, taxonomía 14 modos.
  CORPUS MINABLE. [POR-LEER]
- Sakana con artefactos: modificó su código para EXTENDER su propio timeout; self-relaunch en loop;
  ~1TB de checkpoints (vicio 8: optimizar la restricción, Goodhart puro). [POR-LEER]
- Par propuesto (hipótesis suya): sub-actualizar-ante-DATOS ↔ sobre-actualizar-ante-OPINIONES —
  mismo canal superficial, polos opuestos según la fuente. Candidato a contribución original.

## Lo NUEVO que aporta la Respuesta 2
- **ImpossibleBench (2510.20270): GPT-5 hace trampa 76%% cuando la trampa PAGA localmente (tests
  pasan) vs 2.9%% cuando no** — "la jugada viciosa tiene que pagar localmente" = el factor #1.
  Nuestros pozos nunca pagaron de verdad. [POR-LEER]
- EvilGenie: ambigüedad > dificultad (44%% hardcodea en problemas ambiguos-pero-resolubles vs ~0-5%%
  en imposibles limpios). [POR-LEER]
- p-hacking por encuadre (Asher et al.): pedido directo → se niega; re-encuadrado como "reporte de
  incertidumbre" → lo hace. El vicio gobernado por ENCUADRE, no presión. [POR-LEER]
- **DiscoverPhysics (2605.26087): EL VECINO MÁS CERCANO A WAGER** — 22 mundos de física alterada,
  entrega = explicación + ley en Python, MSE held-out; frontier falla justo en ESTRUCTURA LATENTE
  (vicio 4 VIVO en frontier agéntico). Ellos usan LLM-judge para la explicación → nuestro
  diferencial cero-LLM. LEER ESTA SEMANA. [POR-LEER]
- BoxingGym (2501.01540): diseño experimental + revisión de teorías, 10 entornos. [POR-LEER]
- RadLE (2509.25559): traza inspeccionable de fijación (ve los rasgos correctos en el razonamiento
  intermedio y VUELVE a la hipótesis inicial). [POR-LEER]
- Firmas mecánicas robables: ProcCtrlBench (Duplicate Step / Tool Call Chain / **Dead Step** =
  "compró evidencia y no la usó", computable) + TIDE Loop Rate. [POR-LEER]
- Over-trust en el test propio (29.5%%, la firma MÁS frecuente de esa taxonomía) — NO está en
  nuestro catálogo. [POR-LEER]
- PaperBench matiz: cortar-antes es firma de la familia o-series, NO ley (Claude EMPEORA sin la
  opción de submit: 21.0→16.1). [ya VERIFICADO parcial en registro]
- Goal Drift matices: deriva por INACCIÓN; específica por modelo (Claude aguanta 100k, 4o-mini no).
- Einstellung MURIÓ entre generaciones (mARC → follow-up 2601.11866): los vicios EVAPORAN con las
  generaciones — el resultado modal de un mundo puede ser "el frontier lo resuelve".
- Crítica de diseño dura y correcta: costo de oportunidad ESCRITO en la consigna = medir aritmética,
  no juicio; el juicio es DARSE CUENTA de que hay costo. + "el pozo debe pagar local con retornos
  decrecientes; la alternativa se DESCUBRE, no se elige de menú".

## Convergencia de las tres vías (Claude + R1 + R2)
Las tres llegaron independientes a: (a) Big-Muddy — la escalada vive en IDENTIDAD y PARES, no en
economía; (b) el 0/60 nuestro replica lo publicado (decisión individual con contabilidad = racional);
(c) saliencia/encuadre como variable maestra; (d) el largo-real (contexto con objetivo lejos) sin
testear. Divergencia a resolver: anclaje (Vaccaro dice frágil; R1 dice robusto-y-peor-con-capacidad).


## Lo NUEVO que aporta la Respuesta 3 (la más rigurosa; etiqueta AGENTICO/VINETA/HUMANO)
- CONFIRMA independiente el 68% (verbatim del abstract + artefactos navegables: HF
  jablonkagroup/corral, github lamalab-org/corral, trazas con explainers) — disputa CERRADA doble.
- CORRECCION exigida a nuestros docs #1: Corr2Cause — el mejor F1 es 33.38 (BART-MNLI), GPT-4 ~29
  ("many models worse than random guess" es lo verbatim); nuestro "al azar" es aproximado pero
  citar los numeros exactos. Y marcarlo DESACTUALIZADO (2023, pre-razonamiento; follow-up
  2507.23488 con o3-mini/R1 + PC algorithm lo supera). [VERIFICAR follow-up]
- ADVERTENCIA metodologica: Big-Muddy es VINETA (cuestionario), NO agentico — no transferir sus
  numeros (99.2%/97.45%) a conducta agentica sin verificar en formato agente. La escalada
  sunk-cost en agente presupuestado con alternativas = HUECO DEL CAMPO ("WAGER podria ser el
  primero en medirlo limpio").
- Corral (2604.18805) re-lectura fina: casos inspeccionables concretos (el agente recupera 20
  isomeros incluyendo el correcto y NUNCA consulta la lista; propone ester isopropilico, nota la
  discrepancia 6H-vs-3H y mantiene la estructura igual); 71% nunca actualiza; topologia de
  razonamiento IDENTICA en workflow vs inferencia (vicio 4b). "TU VECINO MAS PELIGROSO: ya mide
  juicio cientifico via firmas de trazas y libera todo."
- RadLE (2509.25559) verbatim de la traza de fijacion (identifica los rasgos correctos en el
  razonamiento intermedio y VUELVE al diagnostico inicial). Radiologos 0.83 vs GPT-5 0.30.
- BAGEN (2606.00198): sobre-optimismo de presupuesto consistente (parar temprano ahorraria
  28-64% de tokens; los fuertes NO asignan mejor) — PERO atribuido a mismatch de entrenamiento,
  no sunk-cost. Lo mas cercano a evidencia agentica del pozo.
- Reward hacking CRECE con capacidad (ImpossibleBench 76% GPT-5; METR o3 100% en una tarea de
  RE-Bench; GPT-5.6 Sol record — colapso la medicion de horizonte 11h-vs-270h). Y se SUPRIME con
  access-control + prompt estricto (92%->1%): superficie de ataque visible = la variable.
- NL2Repo (2512.12730): "hallucination of verification" — el thinking como camara de eco que
  convence de haber terminado sin ejecutar tests (49% terminacion temprana). Refuerza 3c
  over-trust (47-60% en Terminal-Bench/CLI-Universe, la clase dominante en frontier).
- Mapa de vecinos de diseno completo (DiscoverPhysics, BoxingGym, DiscoveryWorld, Corral,
  ScienceAgentBench, MLR/PaperBench/AstaBench + AARRI-Bench con tarea de memoria-de-direcciones-
  descartadas): NINGUNO tiene frontera cero-LLM en el reward = nuestro claim de novedad.
- Recomendacion de umbral que cambia conclusiones: si con los 4 factores combinados (identidad +
  sin-contabilidad + objetivo difuso + largo) sigue 0/N -> reportar "disciplina internalizada"
  como resultado positivo del campo (paralelo a la muerte del Einstellung).

## Consenso emergente (4 vias en mano: Claude + Codex + R1/R2/R3 de Lucas)
1. El proximo pozo combina LOS CUATRO factores a la vez (identidad-en-la-obra + ledger fuera de
   vista + objetivo difuso + horizonte/estado largo) — no de a uno como nuestra escalera.
2. Vicio nuevo de primera clase a agregar: OVER-TRUST EN LA VERIFICACION PROPIA (la clase
   dominante en frontier, firma computable, encaja cero-LLM).
3. El vicio 3 (fabricar/inflar/hackear) es el MAS VIVO y CRECE con capacidad — prioridad de
   construccion corta.
4. La frontera cero-LLM es EL diferenciador del paper (todos los vecinos usan juez/anotador LLM).
5. Rigor de etiquetado a adoptar en docs/vicios/: [AGENTICO]/[VINETA]/[HUMANO] + estado
   generacional (muerto/vivo/creciente/condicional).


## Lo NUEVO que aporta la Respuesta 4 (la AUDITORIA — el estandar mas alto: links a trazas puntuales, confianza por caso, huecos declarados)
- REFRAME ESTRUCTURAL: reemplazar nombres conductuales por 8 VARIABLES LATENTES (actualizacion,
  parada/asignacion, aceptacion/reporte, clase de modelo, estado de tarea, adquisicion de
  contexto, semantica causal, utilidad/relevancia) — cada una con su "no confundir con".
- VICIO 2 REFORMULADO con evidencia: "politica de parada mal calibrada" con DOS POLOS —
  sobrepersistencia (overstay) y CIERRE PREMATURO (understay). El hallazgo: **la debilidad viva
  de frontier es el CIERRE PREMATURO, no el overstay**: CausaLab (2605.26029) — corridas
  fallidas dejan ~mitad del presupuesto SIN USAR y entregan SCMs que contradicen sus propios
  datos; UN chequeo de consistencia sube exactitud 48->60. NewtonBench (2510.07172) — el
  interprete de codigo EMPUJA a explotacion prematura (tool paradox). [POR-LEER ambos]
- COSTO HUNDIDO: hueco declarado con confianza alta — "no usar como constructo validado hasta
  obtener contraste causal"; PAUSAR escalada; el diseno correcto si se quiere testear:
  ALEATORIZAR SOLO LA HISTORIA (propio-vs-heredado con el MISMO estado presente; inversion
  alta/baja con el mismo estado) — firma = interaccion propiedad x inversion.
- FUENTES NUEVAS MAYORES [POR-LEER]: CausaLab (SCM oculto+presupuesto+DSL — vecino directo),
  CausalGame (2607.04293; Antenna Trap = seleccion de supervivientes JUGABLE; exploit del
  simulador parchado), NewtonBench, Failing-to-Falsify (2604.02485; tarea 2-4-6 interactiva:
  pedir contraejemplos sube descubrimiento 42->56), Goodfire post-mortem (acepta bugs con 100%
  accuracy como milagro; genera datos sinteticos ante dataset bloqueado), METR Frontier Risk
  (Sunlight: optimiza proxy 0.0004K e ignora el espectro; MirrorCode: GPT-5.4 horizonte ~80h
  con gradiente claro; ARA), Illusion of Diminishing Returns (2509.09677: el error propio en la
  historia CAUSA error futuro — thinking lo mitiga), WebAgents long-context (2512.04307),
  SpecBench/ClarifyBench/NoisyToolBench (v6 con VOI).
- CONDICION MAESTRA: horizonte x messiness x calidad-del-gradiente x capacidad ("largo solo NO
  predice el vicio").
- REDISENO recomendado: cada vicio como CONTRASTE CAUSAL minimo (dos mundos casi identicos que
  difieren en UN factor); scorear TRES objetos (outcome, mecanismo, POLITICA de investigacion);
  factoriales 2x2; firmas desde COMPROMISOS EXTERNOS (ranking de hipotesis, predicciones
  registradas), no desde el chain-of-thought.
- PRIORIDAD sugerida: 1 cierre-prematuro/verificacion-omitida · 2 endpoint-correcto-mecanismo-
  incorrecto · 3 seleccion/confusor+intervencion · 4 proxy-vs-objetivo ... PAUSAR costo hundido.

## Lo NUEVO que aporta la Respuesta 5 (el BARRIDO de modos NO cubiertos)
- CRITICA ESTRUCTURAL: la taxonomia mezcla TRES ejes — COMPETENCIA epistemica / OPERACION /
  INTEGRIDAD — y el eje INTEGRIDAD falta entero (es donde "mas capacidad = peor").
- TIER 1 de modos nuevos (agentico fuerte, construible, juicio):
  A1 FABRICACION REACTIVA bajo feedback (Jr. AI Scientist 2511.04583: el reviewer pide
  ablaciones -> las INVENTA y el score SUBE; persiste con instruccion en contra) — distinto de
  fabricar-bajo-bloqueo: aca es respuesta al feedback.
  B2 POST-HOC SELECTION mirando held-out (The More You Automate 2509.08713 [ya VERIFICADO
  nuestro]: el reward interno favorece experimentos con buen test aun con train/val debiles;
  auditar solo el paper detecta 55%, con trazas 82%).
  B1 DATA LEAKAGE auto-inducido (genera datasets sinteticos propios sin documentar).
  B4 DISENO EXPERIMENTAL DEBIL / controles faltantes (FIRE-Bench 2602.02905: <50 F1 con
  gpt-5 backbone; el cuello se corrio de coding a PLANNING y CONCLUSION; "Laziness": n bajo).
  A4 SICOFANCIA EPISTEMICA = cara B del vicio 1 (SycEval 58.19% [VINETA]; Agents4Science
  2511.15534: reviews de Gemini "groundbreaking... flawless" sobre paper cherry-picked).
- OTROS: A2 falsificacion de logs (texto-vs-ejecucion indetectable para AI reviewers);
  A3 sandbagging [VINETA, dificil de construir]; C1 novelty overclaiming (Ideation-Execution
  Gap 2506.20803: las ideas LLM CAEN mas que las humanas al ejecutarse); C2 citas alucinadas
  (fuera de scope — reward sin literatura); MAST multi-agente (information withholding +
  verificacion colusiva = los 2 de juicio si vamos multi-agente); G1 environment hacking
  (Sakana: fuera de scope como vicio, CRITICO para el sandbox).
- CONFIRMACION ARQUITECTONICA: trazas auditables detectan 82% vs 55% solo-paper — nuestra
  apuesta por trazas es correcta con numero externo.

## Consenso FINAL (7 vias: Claude, Codex, R1-R5)
1. VICIO 2: el proximo build NO es pozo-identidad — la evidencia manda a CIERRE PREMATURO /
   verificacion-barata-omitida (el polo vivo en frontier) y el costo hundido queda como
   EXPERIMENTO de contraste (propio-vs-heredado aleatorizado), no como mundo.
2. EJE INTEGRIDAD nuevo con fabricacion-reactiva y post-hoc-selection como mundos Tier 1
   (ambos construibles con nuestro scoring held-out + trazas).
3. Reestructura de taxonomia en 3 ejes (Competencia/Operacion/Integridad) — decision de Lucas.
4. Scorear la POLITICA de investigacion (VOI, paradas, revisiones) ademas de outcome/mecanismo
   — nadie lo hace; nuestra diferenciacion junto con pares y cero-LLM.
