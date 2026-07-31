# Lectura completa — Bayesian Teaching (arXiv 2503.17523)

"Bayesian Teaching Enables Probabilistic Reasoning in Large Language Models" — Qiu, Sha, Allen, Kim, Linzen,
van Steenkiste. Leído completo vía `arxiv.org/html/2503.17523`.

## Qué es

Tarea: recomendación de vuelos en un entorno interactivo multi-ronda. El modelo (rol "asistente") recomienda 1
de 3 opciones de vuelo a un usuario simulado (con función de recompensa/preferencia oculta θ), recibe el
feedback de qué eligió el usuario realmente, y así por 5 rondas. Después de cada ronda se evalúa la accuracy
del asistente sobre 100 sets NUEVOS de 3 vuelos (sin feedback). Turno = 1 recomendación + 1 señal de feedback +
100 trials de evaluación held-out. N: 624 usuarios simulados distintos (vectores de preferencia); fine-tuning
con 624 usuarios × 10 interacciones = 6.240 ejemplos; evaluación humana con 500 participantes (10 por lista ×
50 listas); generalización a shopping web con 100 categorías de producto × 10 usuarios. Modelos: cerrados
(Gemini 1.5 Pro, GPT-4.1 Mini) y abiertos fine-tuneados (Gemma 2 9B/27B, Llama 3 8B/70B, Qwen 2.5 7B/32B), más
comparación con humanos (n=10 en rol asistente).

Puntúan con accuracy: ¿la recomendación del modelo coincide con la elección real del usuario en el set
held-out? La norma bayesiana ("Bayesian Assistant") tiene prior uniforme sobre los 624 tipos de usuario
posibles y actualiza con Bayes puro: la verosimilitud es un indicador binario de si el tipo θ es consistente
con la elección observada (p(o*|θ,O) = 𝟙[argmax_o r(o;θ) = o*]); la posterior tras cada ronda usa solo la
elección observada del usuario (no la preferencia verdadera); la predicción usa la media de esa posterior.
Métrica secundaria: fracción de acuerdo entre las predicciones del LLM y las del Bayesian Assistant.

## Citas verbatim clave

- "do LLMs act as if they have probabilistic beliefs that are updated as expected from normative Bayesian inference? To the extent that the LLMs' behavior deviates from the normative Bayesian strategy, how can we minimize these deviations?" (Introducción)
- "most of the models show little improvement after the first round of interaction...pointing to a limited ability to adapt to new information." (§2.2, LLMs sin fine-tuning)
- "Bayesian teaching leads to higher accuracy and less variability across repetitions...Bayesian-tuned LLMs' predictions agree with those of the Bayesian Assistant around 80% of the time." (§3.1)
- "we provide the LLM with examples of interactions between the user and the Bayesian Assistant, and have the LLM mimic those interactions...the Bayesian model's educated guesses make for a stronger learning signal than the correct answers." (§3, mecanismo de enseñanza bayesiana)
- "LLMs fine-tuned on the flight recommendation task generalize to both hotel recommendations and web shopping: they perform much better than the original LLMs on those tasks." (§3.2)
- "these simulated users are highly simplified and are not meant to capture the full complexity of humans: humans do not always choose the option that maximizes their utility, and their preferences may evolve over time." (limitaciones)

## Números principales

- Modelos originales (sin fine-tuning): ~55-60% de accuracy en ronda 5, con mejora <5% desde ronda 1 (Fig. 2).
  El Bayesian Assistant llega a ~80%. Humanos: ~65-70% con mejora significativa (p=0.002).
- Tras fine-tuning bayesiano: ~75-80% en ronda 5 (vs. ~70-75% enseñando con la respuesta "oráculo" correcta en
  vez de la predicción bayesiana) — el fine-tuning bayesiano gana consistentemente sobre el oracle-teaching en
  las tres familias de modelos (Fig. 3).
- Acuerdo con el Bayesian Assistant: modelos originales ~55-60%, bayesiano-enseñados ~80%, oráculo-enseñados
  ~70-75% (Fig. 4).
- Generalización: a hoteles, ~70-75% (bayesiano) vs. ~55-60% (original); a shopping web ~55-60% (bayesiano) vs.
  ~45-50% (original), con upper bound de fine-tuning directo en shopping ~70%.
- Con usuarios humanos reales: modelos bayesiano-enseñados mejoran de ~50% a ~60% ronda1→ronda5; los
  originales quedan planos en ~55%.

## Qué les falta respecto de WAGER

- **No hay entrega ejecutable contra verdad oculta de un mundo**: la "entrega" es una recomendación puntual
  (argmax sobre 3 opciones), no un modelo/artefacto acumulativo que se corre contra casos held-out de forma
  ejecutable — se parece más a nuestra frontera de "creencia dicha" que a lo entregado. Aunque el mecanismo de
  evaluación (100 sets held-out por ronda) SÍ es cero-LLM y comportamental, que es un punto a favor comparado
  con juicio-LLM.
- **Sin trabajo propio acumulado que revisar**: el "asistente" no tiene una posición previa propia comprometida
  (no hay draft propio que defender); cada ronda es una recomendación fresca — no hay eje de compromiso/
  fricción de revisión como en nuestro AUTHOR_ROLE/MODEL_STATUS.
- **Sin evidencia dosificada por valor probatorio cuantificado**: la evidencia es simplemente "la elección real
  del usuario" — no hay control de cuán informativa es esa evidencia (no hay CLEAN/MIXED/PLACEBO), aunque el
  diseño factorial de features (2/4/8) en la generalización se acerca a variar la dificultad de la inferencia.
- **La norma bayesiana asume acceso al verdadero espacio de hipótesis** (624 tipos de usuario enumerados, prior
  uniforme conocido) — esto es exacto/computable porque el mundo lo diseñaron así; en WAGER el oráculo legal
  también se limita a lo que la fila inyectada + modelo previo permiten, pero la escala de "espacio de
  hipótesis" en WAGER es mundos abiertos, no un conjunto discreto enumerable de 624 tipos.
- **Fine-tuning como intervención, no solo diagnóstico**: el paper usa el gap bayesiano para ENTRENAR (mejorar
  el modelo), mientras que WAGER mide para diagnosticar el fenómeno (mapa de carga) sin (por ahora) intervenir
  vía fine-tuning.

## Lecciones de diseño para WAGER

- **Definición de norma/oráculo**: exacta por construcción — el mundo fue diseñado (funciones de utilidad
  lineales θᵀφ(o), tipos de usuario discretos) precisamente para que el Bayesian Assistant sea computable en
  forma cerrada. Es el mismo movimiento que nuestro "oráculo legal": restringir el mundo lo suficiente para que
  la mejor actualización posible sea calculable, no imaginada.
- **Cómo separan sub/sobre-actualización**: no lo hacen de forma explícita — solo miden accuracy y acuerdo con
  el oráculo; no hay una métrica de dirección de sesgo (sub vs. sobre) como en BASIL o en "not consistently
  Bayesian". Es una laguna del paper que WAGER con F (que captura fracción de mejora capturada, con signo si
  hay overshooting) cubre mejor.
- **Insight de diseño reutilizable**: "the Bayesian model's educated guesses make for a stronger learning
  signal than the correct answers" — enseñar a imitar la POSTERIOR bayesiana (no la respuesta correcta cruda)
  generaliza mejor. Relevante si WAGER algún día usa hallazgos para proponer intervenciones/fine-tuning: la
  señal de entrenamiento útil es el proceso de actualización, no el resultado final.
- **Objeción que le harían a F/regret**: el paper mostraría que el gap grande entre "mejora con evidencia
  limpia" (F~0.97 en nuestro hallazgo con gpt-5.4) y "evidencia sucia" (F 0.14-0.53) podría deberse, según su
  marco, a que el modelo no tiene una BUENA estimación implícita de la verosimilitud de la evidencia sucia (no
  sabe cuán informativa es la fila mezclada), no necesariamente a que "vuelve a lo suyo" por apego a lo propio.
  Ellos aislarían esto separando el espacio de hipótesis de la política de decisión — sugieren que antes de
  atribuir el freno a AUTHOR_ROLE/MODEL_STATUS, vale confirmar que el modelo interpreta la dosis de evidencia
  sucia de forma correcta y consistente (podría ser un problema de verosimilitud mal especificada, análogo al
  "Batch mode Δ(q)" del paper de Chen et al.).

## Veredicto

NOS-VALIDA (parcial) — confirma con un diseño limpio y cerrado que los LLMs sub-actualizan sin ayuda pero que
el gap es corregible, y aporta el patrón "oráculo bayesiano por construcción del mundo" que WAGER ya usa; no
compite porque se queda en creencia/recomendación puntual sin trabajo propio acumulado, sin fricción de
revisión, y sin dosis cuantificada de evidencia — el terreno que WAGER cubre es estrictamente más amplio.
