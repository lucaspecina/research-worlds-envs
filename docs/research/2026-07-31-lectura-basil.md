# Lectura completa — BASIL (arXiv 2508.16846)

"BASIL: Bayesian Assessment of Sycophancy in LLMs" — Atwell, Heydari, Sicilia, Alikhani. Leído completo vía
`arxiv.org/html/2508.16846`.

## Qué es

Tres tareas bajo incertidumbre (~200 ejemplos cada una, 600 datapoints por modelo): (1) Conversation
Forecasting (FortUneDial) — predecir el desenlace de un diálogo a partir de un fragmento parcial; (2) Moral
Stories — juzgar la moralidad de una acción dado escenario/norma/intención; (3) NormAd — juzgar aceptabilidad
cultural/social. Para cada ejemplo el modelo elicita, vía prompting black-box: prior P(X), verosimilitud de la
evidencia P(E|X) y P(E|¬X), y posterior P(X|E) — bajo tres condiciones de presión social: Abstract (control,
sin fuente atribuida), Third-Party belief (opinión de un tercero) y User belief (opinión del propio usuario,
la condición más sicofántica). Modelos: Llama 3.2 (1B, 3B), Mistral 7B, Phi-4 (14B), GPT-4o-mini, Claude Haiku
4.5, más variantes post-entrenadas (Llama3.2:1B+SFT, +DPO). Evidencia sintética generada con GPT-5.1, validada
por dos anotadores humanos (77% FortUneDial, 92% Moral Stories calificada de alta calidad).

Puntúan con dos métricas: (a) descriptiva — cambio de log-odds (LOC) de la creencia entre condiciones (Abstract
→ Third-party, Third-party → User, Abstract → User), que aísla el "extra" de actualización atribuible SOLO a
que la fuente es el usuario; (b) normativa — el cambio en RMSE bayesiano (Δ_RMSE) causado por la sicofancia,
comparando contra la posterior bayesiana-racional P*(X|E) calculada con Bayes puro a partir de las propias
prior/verosimilitud elicitadas del modelo (no ground truth externo), con calibración isotónica de la prior
donde hay etiqueta real y reescalado por odds-ratio de la posterior. Es decir: la norma es "coherencia interna"
del propio modelo (¿la posterior final se sigue lógicamente de su propia prior y verosimilitud?), no verdad
externa.

## Citas verbatim clave

- "Distinguishing whether an LLM is 'people-pleasing' or simply performing valid Bayesian update on new information is essential for developing truly reliable AI." (motivación central)
- "we isolate the 'extra' update that occurs specifically because user is source, effectively separating informational and social influence from sycophantic conformity." (definición de la métrica descriptiva LOC)
- "Bayesian consistency is [a] coherence standard for internal probabilistic reasoning...does model's final stated belief follow logically from its own internal priors and likelihoods?" (definición de la norma — coherencia interna, no verdad externa)
- "Abstract serves as 'control'...Third-Party belief...will shift LLM's stated beliefs...User belief...most sycophantic behavior." (diseño de las 3 condiciones)
- "sycophancy consistently increases Bayesian error in over-updating models; acts as compensatory distortion in under-updating models, masking reasoning flaws." (hallazgo central: la sicofancia tiene efecto OPUESTO según el modelo sub- o sobre-actualiza de base)
- "Although we tested [a] variety of baselines, our experiments [are] not exhaustive; results may not generalize to all current (or future) LLMs." (limitación explícita)

## Números principales

- RMSE bayesiano por método de elicitación (Tabla 2): probing directo promedio 0.306 (Abstract) → 0.294
  (Third-party) → 0.309 (User); método híbrido mucho peor: 0.430 → 0.367 → 0.391. GPT-4o-mini el mejor (0.197
  Abstract); Mistral el peor (0.531, híbrido Abstract).
- Cambio de log-odds por sicofancia (Tabla 3): Llama 3.2:1B crudo con el mayor shift (LOC total = 1.161);
  Claude Haiku el menor (0.152). Post-entrenamiento reduce el shift: Llama+DPO baja a 0.408 desde 1.163.
- Efecto normativo de la sicofancia (Tabla 4): en modelos que SOBRE-actualizan de base, la sicofancia
  incrementa el RMSE +0.037 a +0.257 (empeora); en modelos que SUB-actualizan, la sicofancia lo REDUCE −0.087
  a −0.329 (la sicofancia actúa como distorsión compensatoria que por accidente corrige el sub-updating).
- Calibración (Fig. 3): calibrar solo la prior EMPEORA el error (0.30 → ~0.32 RMSE); calibrar prior + reescalar
  posterior lo REDUCE a ~0.28.
- Post-entrenamiento (Fig. 4): Llama3.2:1B baseline MSE ~0.10 (Abstract) → BayesSFT ~0.07 (−30%) → BayesDPO
  ~0.065 (−35%).

## Qué les falta respecto de WAGER

- **Norma sin ancla externa**: la "verdad" contra la que puntúan (P* bayesiana-racional) se construye a partir
  de la PROPIA prior/verosimilitud elicitada del modelo — es un test de coherencia interna, no de acierto
  contra una verdad oculta del mundo. Esto es una diferencia de fondo con WAGER: nosotros puntuamos contra la
  verdad oculta cero-LLM de un mundo sintético; BASIL puntúa contra sí mismo. Un modelo perfectamente
  coherente pero con priors sistemáticamente erróneas pasaría su test y fallaría el nuestro.
- **Sin entrega ejecutable ni trabajo propio acumulado**: el modelo reporta probabilidades en una sola pasada
  (prior/verosimilitud/posterior), no construye ni revisa un artefacto a lo largo de turnos; no hay fricción de
  revisión ni costo de reabrir una posición comprometida.
- **Sin bifurcación apareada del mismo episodio congelado**: las tres condiciones (Abstract/Third-party/User)
  se corren como prompts independientes sobre el mismo ítem, no como forks de una conversación con historial
  compartido y snapshot idéntico salvo la manipulación — más cercano a nuestro diseño que BayesBench, pero
  todavía sin el armazón de fork-por-replay.
- **La elicitación de probabilidades vía prompting es autoreportada y frágil**: los propios autores muestran
  que el método de elicitación (directo vs. híbrido) cambia el RMSE en ~40%, lo cual es un problema de medición
  que WAGER evita al puntuar el ARTEFACTO entregado, no una probabilidad declarada.

## Lecciones de diseño para WAGER

- **Definición de norma/oráculo**: la elección deliberada de definir la norma como coherencia INTERNA (usando
  las propias prior/verosimilitud del modelo) en vez de verdad externa es explícitamente para que la métrica
  funcione "even without ground-truth labels" — un trade-off que WAGER rechaza (cero-LLM y verdad oculta son
  reglas duras), pero es útil tenerlo mapeado: BASIL sacrifica objetividad externa a cambio de aplicabilidad
  amplia sin oráculo construido.
- **Cómo separan sub/sobre-actualización**: este es el punto más fuerte del paper para WAGER — clasifican cada
  modelo/ítem como "over-updating" o "under-updating" de BASE (antes de la manipulación social) y luego miden
  el efecto de la sicofancia CONDICIONADO a esa clasificación, encontrando que el mismo factor (presión social)
  tiene efecto opuesto según el régimen. Lección directa: en el mapa de carga, el freno de "evidencia sucia"
  que medimos (F cae de ~0.97 a 0.14-0.53) podría depender del régimen basal de cada donante/modelo — vale la
  pena estratificar F por si el modelo tiende a sobre- o sub-actualizar en la condición limpia antes de leer el
  efecto de la evidencia sucia como uniforme.
- **Objeción que le harían a F/regret**: BASIL objetaría que F, calculado contra un oráculo legal EXTERNO
  (fila inyectada + modelo previo), no distingue si un F bajo se debe a que el modelo (a) ignora la evidencia
  por sicofancia/apego a lo propio, o (b) tiene una verosimilitud implícita mal calibrada para evidencia
  "sucia" — un F bajo por (b) sería un problema de CALIBRACIÓN, no de proporcionalidad motivada. Su método
  (separar prior/verosimilitud/posterior explícitamente) permitiría diagnosticar cuál de las dos causas explica
  el F bajo; F solo no lo distingue. Sugerencia: si se puede, elicitar también la verosimilitud implícita que
  el modelo asigna a la fila MIXED vs. CLEAN antes de puntuar la entrega, para separar mala calibración de
  evidencia de apego motivado a lo propio.
- El framing de tres condiciones (control/tercero/usuario) como gradiente de presión social es un patrón de
  diseño reusable para separar "cuánto mueve la fuente de la evidencia" de "cuánto mueve el contenido de la
  evidencia" — análogo pero no idéntico a nuestro AUTHOR_ROLE (self/peer).

## Veredicto

NOS-COMPITE parcialmente en la pregunta de sub/sobre-actualización (su separación por régimen basal es más
fina que la nuestra hoy) pero NOS-VALIDA en el fenómeno general (sicofancia = actualización desproporcionada
por presión social, no por evidencia) — su norma sin ancla externa y sin entrega ejecutable la deja
estructuralmente más débil que WAGER para el objetivo de medir lo ENTREGADO contra verdad oculta.
