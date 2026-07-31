# Lectura completa — "Martingale Score: An Unsupervised Metric for Bayesian Rationality in LLM Reasoning" (arXiv 2512.02914)

Fuente leída: HTML completo (`arxiv.org/html/2512.02914v1`, ~77k caracteres tras strip de tags, sección por
sección incluyendo el desarrollo matemático completo de la Proposición del Martingale Score) — no solo abstract.

## Qué es (formato exacto, números)

- **Fenómeno que miden**: "belief entrenchment" — cuando la creencia futura de un modelo es predecible a partir
  de su creencia previa (viola la propiedad de Martingala de la actualización bayesiana racional).
- **3 dominios**: forecasting (Metaculus/Polymarket, con resolución de verdad tras el corte de conocimiento),
  preguntas valorativas (r/ChangeMyView), revisión de papers académicos (ICLR vía OpenReview).
- **Modelos**: GPT-4o, DeepSeek R1/V3, Gemini 2.0 Flash, Llama 4 Scout/Maverick.
- **Técnicas de razonamiento**: Chain-of-Thought (CoT) y Debate; 3 variantes de system prompt (prior-conforming,
  no-prompt, critical-thinking).
- **Elicitación de creencia**: un modelo "juez" separado (GPT-4o por default) puntúa la confianza expresada en
  cada paso del razonamiento del modelo evaluado, en [0,1].
- **Validado con jueces múltiples**: humanos y DeepSeek-v3 como jueces alternativos, para descartar sesgo del juez.

## Citas verbatim clave

1. (Abstract) "This property implies that, under rational belief updating, the expected value of future beliefs
   should remain equal to the current belief, i.e., belief updates cannot be predicted from solely the current
   belief."
2. (§4.1, Defining the Martingale Score) "We define the sample estimate β̂₁ of the linear coefficient as the
   Martingale Score M, with the Ordinary Least Squares (OLS) method."
3. (§4.2, Theoretical Justification) "The Martingale property states that the expectation over one's posterior,
   conditional on their prior, should always be equal to the prior... E[Δb|b_prior=p]=0, ∀p∈[0,1]."
4. (Figure 2, caption) "'Prior Belief' refers to the expressed beliefs in most immediate LLM output; whereas
   'Posterior Belief' usually refers to the terminal beliefs after extended reasoning or engagements with
   external evidence."
5. (§5, resultados) "In most of the experiments, including almost all of those with CoT (51 out of 54), we see
   positive Martingale Scores, suggesting consistent belief entrenchment."
6. (§6, discusión de dominios) "We see a statistically significant difference between the three problem domains
   of Forecasting, r/ChangeMyView, and OpenReview acceptance prediction, in increasing order of propensity for
   belief entrenchment... the gap in their propensity for belief entrenchment hints, more generally, at a gap
   between fact-based and judgment-based domains."

## Números principales

- **Definición formal (Ec. 1)**: M = β̂₁ = Σᵢ(Δbᵢ − Δb̄)(b_prior,i − b̄_prior) / Σᵢ(b_prior,i − b̄_prior)²,
  donde Δb = b_posterior − b_prior. Regresión OLS simple; significancia vía t-test (p<0.05).
- Rangos de M por dominio (CoT): Forecasting ~+0.012 a +0.076 (bajo); r/ChangeMyView ~+0.052 a +0.142
  (moderado); OpenReview ~+0.068 a +0.103 (moderado). M̄_OpenReview-CoT = 0.086 ± 0.012 (95% CI).
- Validación contra verdad: correlación positiva entre |M| y Brier Score en Forecasting (más entrenchment →
  peor predicción); en OpenReview esta correlación NO se sostiene (los autores lo atribuyen a que el ground
  truth ahí es voto comunitario ruidoso, no verdad objetiva).
- Consistencia entre jueces: correlación r = 0.88–0.72 con evaluadores humanos, r = 0.78 con DeepSeek-v3, todas
  p<0.001 — comparado como referencia contra el experimento de consistencia de revisión NeurIPS 2021.

## Qué les falta / qué nos toca respecto de WAGER

- **No hay agente que entregue un modelo ejecutable puntuado contra verdad oculta**: la salida elicitada es una
  probabilidad verbalizada en cada paso de razonamiento (via juez-LLM), no un artefacto/modelo ejecutable ni una
  entrega cero-LLM puntuable contra ground truth continuo.
- **Juez-LLM en el corazón de la medición**: la creencia misma (b_prior, b_posterior) se extrae con un juicio de
  GPT-4o sobre texto de razonamiento — exactamente lo que la regla dura de WAGER prohíbe en el cómputo del
  reward (acá no es reward, es la métrica de análisis, pero el diseño entero depende de LLM-como-elicitador).
- **Evidencia no dosificada por KL/verosimilitud**: la evidencia entra como "nueva información" genérica
  (resultados de búsqueda, comentarios, reviews), sin cuantificación de cuánta información aporta cada pieza.
- **Sin bifurcación apareada de un mismo episodio congelado**: no manipulan una condición (autoría, compromiso,
  fricción) manteniendo el resto idéntico — miden entrenchment observacionalmente sobre trayectorias de
  razonamiento naturales, sin diseño experimental de brazo pareado.
- **Trabajo propio acumulado / fricción de revisión**: ausente; la propiedad de Martingala mide solo si la
  creencia previa predice el update, no si hay costo de reabrir un artefacto ya entregado.

## Lecciones de diseño — el score EXACTO y si es computable sobre WAGER

- **Qué datos necesita el Martingale Score**: pares (b_prior, b_posterior) ∈ [0,1]² por trayectoria/paso, MUCHOS
  puntos (n grande, para que la regresión OLS tenga poder) donde b_prior varíe en un rango razonable — el
  método requiere que el prior no esté degenerado (todo en 0 o 1) porque la pendiente se estima sobre la
  varianza de b_prior.
- **¿Es computable sobre nuestras trayectorias de forks con creencias implícitas en entregas?** Parcialmente,
  con una traducción no trivial:
  - WAGER no elicita una probabilidad verbal; entrega un MODELO EJECUTABLE. Para aplicar el score haría falta
    definir una "creencia implícita" b = una función escalar en [0,1] del modelo entregado en cada turno/fork
    respecto de la hipótesis en juego — por ejemplo, la probabilidad que el modelo asigna a la hipótesis
    correcta si el modelo es probabilístico, o una distancia normalizada a la verdad oculta convertida a
    score de creencia (ej. 1 − distancia_normalizada). Esto es viable SI los mundos WAGER tienen una noción de
    "modelo como distribución/estimador" de la que se pueda leer una probabilidad — hay que auditar caso por
    caso si el modelo ejecutable expone eso o si haría falta forzarlo con LLM-juez (que WAGER prohíbe).
  - Si se pudiera extraer b_prior (creencia antes de ver la evidencia inyectada) y b_posterior (creencia en la
    entrega tras la evidencia) SIN juez-LLM — puramente del modelo ejecutable evaluado en el punto de verdad —
    el Martingale Score sería una métrica secundaria calculable cero-LLM sobre S_local/F que WAGER ya tiene.
    Sería una regresión adicional (Δb vs b_prior) sobre el panel de celdas del mapa de carga, más fina que "F"
    porque detecta entrenchment direccional incluso cuando F es bajo por razones distintas (evidencia sucia).
  - **Riesgo**: con pocas celdas/forks por brazo (WAGER corre ~10-20 forks por celda), el n para una regresión
    OLS confiable por brazo es chico — el paper usa cientos/miles de trayectorias por setup. Habría que pool-ear
    across celdas o tratarlo como análisis exploratorio, no como métrica primaria por celda.
- **Conclusión de diseño**: no portar el score tal cual (depende de juez-LLM y de una creencia verbalizada), pero
  sí la FORMA del score — regresión de Δb contra b_prior, con el mismo argumento teórico (Cov(Δb,b_prior)=0 bajo
  actualización racional) — es reusable como chequeo secundario cero-LLM SI WAGER logra definir una creencia
  escalar leída directamente del modelo entregado (no del texto de razonamiento).

## Veredicto

**NOS INFORMA, no compite** — valida con otra metodología que "medir revisión de creencias por predictibilidad
de la actualización" es un eje legítimo y da señal fuerte (51/54 setups con entrenchment positivo, validado
contra Brier Score). Pero el diseño entero depende de un juez-LLM elicitando una creencia verbal — viola la
frontera cero-LLM de WAGER en su forma actual y no tiene bifurcación apareada ni evidencia dosificada por KL.
La forma matemática del score (regresión Δb ~ b_prior) es portable como chequeo secundario SI se logra una
lectura cero-LLM de creencia implícita en el modelo entregado — a evaluar caso por caso, no adoptar sin diseño.
