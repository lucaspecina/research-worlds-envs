# Lectura completa — "LLMs are not (consistently) Bayesian" (arXiv 2605.06915)

"LLMs are not (consistently) Bayesian: Quantifying internal (in)consistencies of LLMs' probabilistic beliefs"
— Chen, Jörke, Goliński, Fedzechkina, Sapiro, Williamson, Foti. Leído completo vía
`arxiv.org/html/2605.06915`.

## Qué es

Tarea: preguntas de opción múltiple (4 opciones) con revelación secuencial de evidencia, sobre 4 espacios de
hipótesis (animales, ideología política, diagnósticos médicos, reglas lógicas tipo Eleusis). Cada pregunta se
parte en 2-11 pasos de evidencia secuencial; en cada paso se revela X_{n+1} nueva. Dos modos: **Belief
Propagation (BP)** — el modelo actualiza su creencia después de cada pieza de evidencia dados prior π y
verosimilitud ℓ elicitados; **Batch** — el modelo incorpora toda la evidencia de una vez, sin creencias
intermedias. Modelos: 10 en total — open-source (Qwen3-8B, Qwen3-14B, Ministral-8B y -14B con y sin
razonamiento, DeepSeek-R1-0528-Qwen3-8B) y cerrados (GPT-4o mini, GPT-5.1 con y sin razonamiento medio). N:
Animales 500 preguntas, Ideología Política 575, MediQ 494, Eleusis 78 trazas (de un solo modelo, GPT-5.2);
retención máxima de 80% de los datos por paso de evidencia usada para el análisis.

Puntúan con el "information processing gap" Δ(q) = I_out − I_in = D_KL(q||p) ≥ 0, donde q es la distribución
post-evidencia reportada por el modelo y p es la posterior de Bayes exacta calculada con la prior y
verosimilitud QUE EL PROPIO MODELO elicitó (p(θ|X_{1:n}) ∝ π(θ|X_{1:n}) ℓ(X_{n+1}|θ,X_{1:n})). Se descompone
como Δ(q) = D_KL(q||π) − I_LER, donde I_LER mide el alineamiento entre el cambio de creencia y la fuerza de la
evidencia. Métricas secundarias: AUROC (¿la opción correcta recibe más probabilidad que la incorrecta?) y ECE
(error de calibración esperado). En §4.5 usan, SOLO como análisis adicional, la verosimilitud de GPT-5.1 como
proxy de la verosimilitud verdadera desconocida — no es parte de la evaluación estándar.

## Citas verbatim clave

- "We introduce the novel technique of studying LLMs as information processing rules and utilize the information processing gap – the deviation from Bayes updates – to study the internal (in)consistencies." (framing metodológico central)
- "Despite this, many points lie on, or close to, the dashed line, indicating optimal or near-optimal information processing (i.e., Bayesian updating)." (modo BP: cerca del óptimo)
- "In batch mode, LLMs update their beliefs with implicit maps that are not consistent with their elicited likelihoods." (modo Batch: diverge de sus propias verosimilitudes elicitadas)
- "Surprisingly, the non-Bayesian heuristic updates often outperform exact Bayesian updates (optimal information processing) in terms of downstream task performance." (hallazgo paradójico — ser bayesiano exacto no siempre es lo mejor)
- "On MediQ, all models would perform worse if they were explicitly Bayesian." (caso concreto del hallazgo anterior)
- "Around half of the 'wrong direction' updates in batch mode are actually moving in the direction implied by the oracle likelihood," suggesting elicited likelihoods are misspecified relative to GPT-5.1's implicit model. (diagnóstico: la verosimilitud ELICITADA está mal especificada, no la actualización)
- "Δ(q) is computed relative to likelihoods elicited through a specific prompt format and might be sensitive to that format." (limitación explícita)

## Números principales

- GPT-5.1 en modo BP: casi óptimo (Δ(q)≈0) en los 4 datasets. Modelos débiles muestran actualizaciones en
  dirección equivocada en 20-60% de los pasos (Ministral sin razonamiento).
- Incluso GPT-5.1 está "frequently far from optimal in batch mode", con un número significativo de puntos
  moviéndose en dirección equivocada; la mediana de Δ(q) es consistentemente menor en BP que en Batch (Fig. 4).
- Batch mode supera a BP mode en AUROC para modelos débiles en Animales, Ideología Política y MediQ;
  comparable en modelos fuertes y en Eleusis.
- En Eleusis, los modelos con razonamiento superan al Bayes explícito pese a tener peor Δ(q) — no hay relación
  causal consistente entre Δ(q)=0 y desempeño en la tarea.
- Correlación de Spearman sustancial entre Δ(q) en modo Batch y AUROC en modo BP (Fig. 7) — permite usar el
  gap de Batch como diagnóstico de fiabilidad de las inferencias BP sin necesitar ground truth.

## Qué les falta respecto de WAGER

- **Norma auto-referencial, no verdad externa del mundo**: igual que BASIL, la "posterior correcta" p se
  calcula a partir de la PROPIA prior y verosimilitud que el modelo elicitó — un test de consistencia interna
  (Bayes puro aplicado a insumos propios), no de acierto contra verdad oculta construida server-side. El paper
  incluso muestra que esto puede llevar a conclusiones contraintuitivas (ser bayesiano-consistente empeora el
  desempeño real en MediQ) — que es justo el peligro que WAGER evita al anclar la métrica a una verdad externa
  cero-LLM y a un oráculo LEGAL (basado en evidencia realmente inyectada), no a la coherencia del propio LLM.
- **Sin entrega ejecutable, sin trabajo propio, sin fricción de revisión**: el output puntuado es una
  distribución de probabilidad sobre 4 opciones, elicitada de una vez por paso — no hay artefacto acumulado
  que el modelo deba defender o revisar, ni costo de reabrir.
- **Sin bifurcación apareada ni control de dosis cuantificada**: no hay diseño factorial de manipulaciones
  (autoría, compromiso) sobre el mismo episodio congelado; la única variable manipulada es el modo de
  presentación de la evidencia (secuencial vs. batch).
- **El propio paper señala que su métrica depende del formato del prompt de elicitación** — una fragilidad de
  medición que WAGER evita al puntuar el artefacto entregado, no una probabilidad autoreportada.

## Lecciones de diseño para WAGER

- **Definición de norma/oráculo**: la eligen deliberadamente auto-referencial ("using the model's own
  elicited prior/likelihood") para poder aislar el proceso de INTEGRACIÓN de evidencia de la calidad de la
  creencia previa — es una separación limpia de dos fuentes de error (prior mal calibrada vs. mala
  actualización) que WAGER no separa hoy: F mide la brecha total capturada de la mejora legal, pero no dice si
  el F bajo viene de que el modelo parte de un prior/creencia previa mal calibrada o de que integra mal la
  evidencia nueva dado su propio punto de partida. Podría valer la pena, en análisis futuros, elicitar
  explícitamente la "verosimilitud implícita" que el donante asigna a la fila inyectada ANTES de puntuar la
  entrega, para descomponer el freno igual que ellos hacen.
- **Cómo separan sub/sobre-actualización**: vía el SIGNO y la descomposición de Δ(q) = D_KL(q||π) − I_LER —
  permite ver si el modelo se mueve MENOS de lo que la evidencia amerita (sub) o hacia el lado equivocado /
  demasiado (sobre), y en qué modo (BP vs Batch) ocurre cada patrón. Es más fino que un solo número de F.
- **El hallazgo "ser bayesiano no siempre maximiza performance"** es la objeción más filosa que le harían a
  cualquier métrica que trate F=1 (capturar toda la mejora legal) como el óptimo deseable sin matices: en
  dominios donde el modelo tiene un prior implícito de alta calidad aprendido del pre-entrenamiento (su ejemplo:
  diagnóstico médico), aplicar Bayes EXPLÍCITO sobre una verosimilitud mal elicitada puede ser PEOR que la
  heurística implícita del modelo. Objeción directa a F/regret: un F bajo en una celda del mapa de carga podría
  reflejar que el modelo tiene un prior implícito fuerte y razonablemente calibrado sobre el dominio del mundo
  (aprendido en pre-entrenamiento) que compite con la "mejora legal" definida por la fila inyectada — habría
  que descartar esta alternativa antes de atribuir un F bajo únicamente a apego motivado a lo propio /
  fricción de revisión. Sugerencia concreta: correr un control de "verosimilitud implícita fuerte" (¿el modelo
  ya acierta MUCHO sin la evidencia inyectada, porque el dominio es de los que "ha visto mucho"?) como
  covariable al leer F bajo.
- El uso del modo Batch como "diagnóstico barato" de la fiabilidad de BP (correlación con AUROC sin necesitar
  ground truth) es un patrón reusable: un "modo resumen" de bajo costo que predice la fiabilidad del "modo
  secuencial" costoso — análogo a usar un control barato (placebo/calibración) antes de invertir en la
  lectura completa de hipótesis, que es exactamente lo que WAGER ya hace con el freno de calibración
  CLEAN>MIXED>PLACEBO.

## Veredicto

NOS-CAMBIA-EL-DISEÑO (parcial) — su hallazgo de que Bayes-exacto no siempre es el óptimo de desempeño, y su
separación explícita prior-vs-integración, son una objeción seria y constructiva a leer F bajo como "apego a
lo propio" sin descartar primero que el modelo tenga un prior implícito fuerte compitiendo con la evidencia
inyectada — vale la pena incorporar ese control en la próxima pasada del mapa de carga.
