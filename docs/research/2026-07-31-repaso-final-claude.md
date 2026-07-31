# Repaso final de literatura y comunidad (Claude, 2026-07-31)

> Barrido con 4 agentes en paralelo tras el refoco (nota de dirección + ADRs 0153-0155).
> Regla de verificación: TODO link listado fue ABIERTO por el agente y el contenido confirmado
> contra lo que se afirma; las excepciones están marcadas. Veredictos: NOS-COMPITE /
> NOS-VALIDA / NOS-CAMBIA-EL-DISEÑO / IRRELEVANTE. Archivo hermano de la otra sesión:
> `2026-07-31-repaso-final-otra-sesion.md`.

## VEREDICTO GLOBAL (lo que cambia y lo que no)

1. **Riesgo de scoop: BAJO, verificado.** Nadie combina las cinco piezas nuestras (fork apareado
   mid-episodio × revisión del modelo propio con trayectoria × evidencia con dosis cuantificada ×
   consecuencia cobrada sobre la entrega × cero juez-LLM). Los dos hemisferios existen por
   separado y calientes: fork-replay causal para debugging/atribución, y medición de updating
   contra norma bayesiana en formato declarativo. El mejor posicionado para cruzarlos: el grupo
   de Causal Agent Replay (jun 2026). Razón para preprint temprano.
2. **Nuestra premisa (los tests cortos no predicen la conducta en acto) ya tiene soporte externo
   múltiple e independiente** — incluida una INVERSIÓN de rankings de sycophancy entre benchmark
   sintético y replay realista (LURE), la misma inversión en otro dominio (ANIMA/TAC), la brecha
   creciendo con capacidad (ActTraitBench), y el postmortem de OpenAI admitiendo que sus evals no
   predijeron el despliegue. Pero **el estudio exacto (mismo modelo, test corto vs trabajo largo
   con consecuencia cobrada) NO existe** — sigue vacante para nosotros.
3. **La frontera cero-LLM quedó vindicada por OpenAI**: GeneBench-Pro gradea con scripts Python
   contra targets pre-especificados, cero juez. Su hallazgo cualitativo central ("notice-act
   gap": notan la señal y no propagan la implicancia) ES nuestro fenómeno, descripto a mano;
   nosotros lo dosificamos. La industria entera (Epoch AI) admite que sabe gradear "¿pasó el
   test?" y no "¿fue buen juicio?".
4. **Dos vacíos confirmados con búsquedas declaradas**: (a) manipulación CAUSAL del costo real de
   revisar en agentes (nadie lo hizo — la pasada 2/fricción ataca terreno virgen); (b) el score
   corto de disposición correlacionado con conducta agéntica larga del mismo modelo.
5. **Solapamiento más serio a citar y diferenciarse**: "When Should Models Change Their Minds?"
   (Xu et al., may 2026) — mundo cerrado + oráculo + sub/sobre-revisión separadas; sin economía
   de consecuencias, sin ejes de carga, sin dosis.

## FRENTE A — medición agéntica de creencias + fork/replay como evaluación causal

- **Causal Agent Replay** (jun 2026) https://arxiv.org/abs/2606.08275 — do-operación sobre un
  paso de una corrida de agente + re-ejecución forward, sin juez-LLM; para ATRIBUCIÓN de fallas,
  no revisión de creencias. NOS-VALIDA; vecino metodológico más cercano; cita obligada.
- **BayesBench** (jun 2026) https://arxiv.org/abs/2606.30850 — trayectorias de creencia
  multi-turno vs razonador bayesiano exacto; formato conversacional sin entrega ni trayectoria
  propia. Hallazgo: infieren la estructura y no la usan en la predicción (converge con nuestro
  decir≠entregar). NOS-VALIDA / compite en la métrica.
- **ClawArena** (abr 2026) https://arxiv.org/abs/2604.04202 — updating ante evidencia
  contradictoria con chequeos ejecutables; sin forks apareados ni dosis ni autoría. NOS-VALIDA
  con roce parcial.
- **When Agents Commit Too Soon** (jun 2026) https://arxiv.org/abs/2606.22936 — compromiso
  prematuro medido por convergencia de hidden states (necesita pesos abiertos), QA corto. Su
  frase "es estado de la tarea, no rasgo del modelo" = munición contra los tests de rasgo.
  NOS-VALIDA / compite parcial.
- **Harness-Induced Belief Divergence** (jul 2026) https://arxiv.org/abs/2607.04528 — las
  creencias DECLARADAS mid-run dependen del arnés → refuerza cobrar por la entrega. NOS-VALIDA.
- **Escalation of Commitment (Big-Muddy)** (2025) https://arxiv.org/abs/2508.01545 — escalada
  ~0 individual, 99.2% con pares (viñeta). NOS-VALIDA (converge con H1/H2 planas).
- Fork/replay como infraestructura ya estándar (para otros fines): **DoVer**
  https://arxiv.org/abs/2512.06749 · **CausalFlow** https://arxiv.org/abs/2605.25338 ·
  **Counterfactual Trace Auditing** https://arxiv.org/abs/2605.11946 · **Shepherd**
  https://arxiv.org/abs/2605.10913 · **LUMINA** https://arxiv.org/abs/2601.16649.
- Menores: FalsifyBench https://arxiv.org/abs/2606.04751 (revisión ante disconfirmación en
  juegos cortos; ganan los que falsean) · ABBEL (BAIR) https://bair.berkeley.edu/blog/2026/07/26/abbel/
  (belief states para eficiencia — agenda caliente, no compite) · InquiTree
  https://arxiv.org/abs/2606.09550 ("cognitive tunneling" en interacción larga).
- Vacíos declarados: búsqueda "paired fork agent evaluation counterfactual" = 0 resultados;
  nadie manipula autoría del modelo previo en forks; nadie cobra la actualización con proper
  scores contra verdad oculta en formato agéntico.

## FRENTE B — validez externa de los tests cortos de disposición

- **LURE** (may 2026) https://arxiv.org/abs/2605.26438 — replay de trayectorias reales +
  consulta final indistinguible del deployment; **rankings de sycophancy INVERTIDOS** vs
  benchmark sintético (SYCON). Juzga con LLM, sin consecuencia. NOS-COMPITE (el más cercano) y
  NOS-VALIDA. Leer entero antes de la pasada 2.
- **Cuestionarios psicométricos malcaracterizan a los LLMs** https://arxiv.org/abs/2509.10078 —
  el ítem transparente delata qué se mide; el perfil no sobrevive a la generación realista.
- **ActTraitBench** https://arxiv.org/pdf/2605.29791 — la brecha conocimiento-decisión CRECE con
  la capacidad del modelo.
- **PropensityBench** https://arxiv.org/html/2511.20703v1 — bajo presión dosificada abandonan lo
  que declaran; capacidad y propensión casi no correlacionan (r≈0.10).
- **Constructo "sycophancy" fragmentado** https://arxiv.org/html/2605.21778v1 — 106
  investigadores no acuerdan qué conductas cuentan; medir por consecuencia esquiva la disputa.
- **Construct validity en 445 benchmarks** (NeurIPS 2025) https://arxiv.org/abs/2511.04703.
- **Postmortem de sycophancy de OpenAI** (verificado vía
  https://www.lesswrong.com/posts/KyndnEA7NMFrDKtJG/gpt-4o-sycophancy-post-mortem): "nuestras
  evals offline no eran lo bastante amplias ni profundas" — el caso real de manual.
- **ANIMA "Stated Values, Revealed Habits"**
  https://animainternational.substack.com/p/stated-values-revealed-habits — inversión
  benchmark↔tarea realista en dilemas de valores; diseño "buried needle" primo del fork.
- **Sycophancy financiera agéntica** https://arxiv.org/abs/2604.24668 — en agentes resisten el
  rebuttal explícito y ceden a la contradicción SUTIL (rima con "la evidencia sucia domina").
- **MemSyco-Bench** https://arxiv.org/abs/2607.01071 — sycophancy inducida por memoria propia
  acumulada; vecino de la pasada 2, estático y con juez. Vigilar.
- **Vending-Bench / Project Vend** https://arxiv.org/abs/2502.15840 — meltdown loops sin
  recuperación en trabajo largo. · **Petri (Anthropic)**
  https://www.anthropic.com/research/petri-open-source-auditing — auditoría realista, juez LLM.
- **Multi-turn: LLMs Get Lost** https://arxiv.org/abs/2505.06120 — −39% al pasar a multi-turno;
  no incorporan aclaraciones posteriores. · **Constituciones violadas en agencia**
  https://arxiv.org/pdf/2605.24229.
- Vacío declarado: ningún trabajo corre el mismo modelo en test corto Y trabajo agéntico largo
  con consecuencia y reporta la correlación.
- Nota de honestidad del agente: la cifra "r<0.3 entre sub-tests de sycophancy" atribuida a un
  "syco-bench" NO pudo rastrearse a fuente real — no citar.

## FRENTE C — actualización normativa y fricción de revisión

- **Belief-R** (EMNLP 2024) https://aclanthology.org/2024.emnlp-main.586/ +
  https://arxiv.org/abs/2406.19764 — VERIFICADO QUÉ ES: viñeta de 3 oraciones (modus
  ponens/tollens + premisa derrotante), multiple choice de 3 opciones, ground truth por VOTACIÓN
  de 5 anotadores, métrica binaria cambiar/mantener (BREU). Sin magnitud, sin dosis, sin
  consecuencia. Carga cero en versión lógica. NOS-VALIDA; la cita de la nota de dirección era
  generosa — corregir el encuadre al citarlo.
- **Bayesian Teaching** https://arxiv.org/abs/2503.17523 — VERIFICADO: recomendación de vuelos,
  5 rondas, posterior bayesiano exacto como vara; los LLMs se estancan tras UNA interacción
  (sub-actualización en acto); fine-tuning imitando al bayesiano generaliza. Lo más cercano a
  nuestra vara, en la esquina sin carga. NOS-COMPITE parcial / NOS-VALIDA.
- **BASIL** https://arxiv.org/abs/2508.16846 — separa desplazamiento por presión social de
  actualización racional por evidencia, con norma bayesiana; **mide sobre- y sub-actualización
  como fallas distintas**. Declarativo, sin entrega. NOS-CAMBIA-EL-DISEÑO (su forma de reportar
  sobre/sub es lo que queremos para F). Leer entero antes de la pasada 2.
- **Martingale Score** https://arxiv.org/abs/2512.02914 — norma SIN ground truth: la creencia
  actual no debe predecir el update futuro; detecta atrincheramiento. **Computable GRATIS sobre
  nuestras trayectorias ya corridas** → puente directo de nuestro mapa a su literatura.
  NOS-CAMBIA-EL-DISEÑO (barato).
- **When Should Models Change Their Minds?** (may 2026) https://arxiv.org/html/2605.30219 — EL
  SOLAPAMIENTO MÁS SERIO: dos entornos cerrados con verificador simbólico y creencia oráculo;
  Failed Update / Failed Stay / Failed Isolation como fallas separadas (95-99% de falla en
  modelos vanilla). Sin consecuencias cobradas, sin ejes de carga, sin dosis. Citar y
  diferenciarse explícitamente.
- Otros: BCC/coherencia bayesiana (base models, 1 turno) https://arxiv.org/abs/2507.17951 ·
  BeliefShift (proporcionalidad con vara sintética-anotada, declarativo)
  https://arxiv.org/html/2603.23848 · "LLMs are not (consistently) Bayesian"
  https://arxiv.org/abs/2605.06915 · creencia→acción rota en juegos
  https://arxiv.org/abs/2605.00226 (probing: las creencias internas son mejores que lo que
  reportan) · number game https://arxiv.org/abs/2605.05851 · cue combination
  https://arxiv.org/abs/2512.02719 (percepción, irrelevante).
- **Fricción/costo causal de revisar: VACÍO CONFIRMADO** (búsquedas declaradas en el crudo).
  Bordes: **Act or Escalate** https://arxiv.org/abs/2604.08588 (SÍ manipula ratios de costo
  causalmente — el molde metodológico correcto, aplicado a derivar-a-humano, no a revisar lo
  propio) · **Calibrate-Then-Act** https://arxiv.org/html/2602.16699v1 (costo real de explorar
  antes de decidir) · **Failure as a Process** https://arxiv.org/abs/2607.09510 (1.794
  trayectorias: persisten en rumbo fallido hasta que es tarde — observacional, el porqué-causal
  vacante) · CogBias https://arxiv.org/abs/2604.01366 (costo hundido en viñeta) · ABxLab
  https://arxiv.org/abs/2509.25609 (plantilla de manipulación de-a-una-variable en agentes).

## FRENTE D — GeneBench-Pro y la ola comercial

- **GeneBench-Pro ES DE OPENAI** (jun 2026; Jeremy Li + Andrew Ho, que se fue un mes después).
  Paper completo leído: https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf
  — 129 problemas de bioinformática, contenedor sin internet, datos sucios + estimando target
  atado a decisión; 3-13 puntos de decisión por problema. **Grading: scripts de Python,
  exact-match + tolerancias, binario, CERO juez-LLM** (el campo de razonamiento se recolecta y
  NO se gradea — señuelo deliberado). Verdad = estimador recuperable desde los archivos (no el
  parámetro generador); ablaciones verifican que los análisis plausibles-equivocados caen lejos.
  GPT-5.6 Sol 28.7%, Opus 4.8 16.0%. Su hallazgo central: **"notice-act gap"** — notan la señal
  diagnóstica y no propagan la implicancia. NOS-VALIDA (convergencia independiente con nuestra
  frontera cero-LLM y nuestro fenómeno); su binario terminal declarado como limitación = nuestra
  diferencia defendible (nosotros medimos MAGNITUD de actualización por unidad de evidencia).
- **10 problemas públicos MIT con grader ejecutable**:
  https://huggingface.co/datasets/ajh-oai/genebench-pro-public-package — leer los
  `eval_config.json` antes del próximo pre-registro. NOS-CAMBIA-EL-DISEÑO (referencia de
  contratos de grading).
- **La empresa de Ho: sin nombre ni sitio aún** (Fortune 2026-07-30:
  https://fortune.com/2026/07/30/former-openai-researcher-overvalued-lockup/ · The Decoder:
  https://the-decoder.com/ex-openai-researcher-bets-100-billion-will-flow-into-training-data-because-scaling-alone-wont-cut-it/).
  NOS-COMPITE a mediano plazo; la ventana para publicar primero sigue abierta.
- **LatchBio** (SpatialBench/scBench + versiones Long):
  https://github.com/latchbio/spatialbench · https://arxiv.org/abs/2605.28065 ·
  https://arxiv.org/abs/2606.26563 · https://benchmarks.bio/ — la TERCERA VÍA: datos REALES +
  claims publicados reproducidos y encerrados en vocabularios de respuesta controlados; 5
  familias de graders determinísticos open-source (tolerancia numérica, multiple choice,
  precision/recall de listas, Jaccard de conjuntos, comparación de distribuciones).
  NOS-VALIDA + NOS-CAMBIA-EL-DISEÑO (catálogo de graders portable; le habla a la regla de
  fidelidad a casos reales).
- **Panorama de mercado** (Epoch AI): https://epoch.ai/gradient-updates/state-of-rl-envs —
  Anthropic >US$1B/año en ambientes; tareas a US$200-2.000; criterio #1 = robustez anti
  reward-hacking; **"fuera de 'pasa los tests' no tienen criterio limpio" para caminos
  múltiples**. · Periodic Labs (reward = experimentos físicos, ~US$550M):
  https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science · Prime Intellect
  Environments Hub (sin categoría ciencia): https://www.primeintellect.ai/blog/environments ·
  Directorio de vendors (ninguno en ciencia): https://www.rl-list.com/ — el casillero "ciencia
  con juicio" está vacío en toda la ola comercial.

## COLA DE LECTURA PRIORITARIA (texto completo antes de la pasada 2)

1. LURE (2605.26438) — el vecino más cercano en espíritu.
2. When Should Models Change Their Minds? (2605.30219) — el solapamiento más serio.
3. BASIL (2508.16846) — reporte de sobre/sub-actualización para F.
4. Causal Agent Replay (2606.08275) — el fork-replay causal formalizado.
5. GeneBench-Pro público (eval_configs) — contratos de grading.
6. Martingale Score (2512.02914) — métrica gratis sobre nuestras trayectorias.
7. Act or Escalate (2604.08588) — el molde causal de costo para el eje fricción.

## IMPLICANCIAS DE DISEÑO INMEDIATAS

- Computar el score martingala sobre los 252 forks YA corridos (gratis, CPU).
- Reportar F desagregado en sobre/sub-actualización (estilo BASIL) desde la pasada 2.
- Los `eval_config.json` de GeneBench-Pro y las 5 familias de graders de LatchBio como
  referencia al endurecer contratos de entrega.
- Related work obligado del futuro paper: Causal Agent Replay, BayesBench, ClawArena, LURE,
  When-Should-Models-Change, BASIL, Bayesian Teaching, GeneBench-Pro, Belief-R (con el encuadre
  corregido: viñeta de 3 oraciones con norma por votación).
- Corregir en la nota de dirección la descripción de Belief-R.
