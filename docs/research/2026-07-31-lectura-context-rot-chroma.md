# Lectura completa — "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (Chroma Technical Report, Kelly Hong / Anton Troynikov / Jeff Huber, 14 jul 2025)

Fuente leída: reporte técnico completo (`trychroma.com/research/context-rot`, HTML crudo descargado y
limpiado de tags, ~51k caracteres, TODAS las secciones: Introduction, Related Work, Needle in a Haystack
Extension, Needle-Question Similarity, Impact of Distractors, Needle-Haystack Similarity, Haystack Structure,
LongMemEval, Repeated Words, Limitations & Future Work, Conclusion, Footnotes, References, Appendix) — no solo
resumen ni abstract.

## Qué es (formato exacto, números)

- **Qué miden**: si 18 LLMs (GPT-4.1/4o/4-Turbo/3.5-Turbo, Claude Opus 4/Sonnet 4/3.7/3.5/Haiku 3.5, Gemini
  2.5 Pro/2.5 Flash/2.0 Flash, Qwen3-235B-A22B/32B/8B) procesan el contexto de forma UNIFORME a medida que
  crece el input, en tareas deliberadamente simples (para aislar longitud de dificultad de tarea).
- **4 experimentos de Needle-in-a-Haystack (NIAH) extendido** + **LongMemEval** (QA conversacional) +
  **Repeated Words** (tarea de replicación textual).
- **Escala del estudio**: 194.480 llamadas a LLM totales, 0.035% de rechazos (69 casos). 8 longitudes de input
  × 11 posiciones de aguja por combinación de tipo-de-aguja/tema-de-haystack/estructura-de-haystack.
  Temperature=0 salvo excepciones (o3, modo "thinking" de Qwen). Juez GPT-4.1 con >99% de alineación a juicio
  humano (calibrado sobre ~500 outputs para NIAH, ~600 para LongMemEval).

## Citas verbatim clave

1. (Introducción) "Large Language Models (LLMs) are typically presumed to process context uniformly—that is,
   the model should handle the 10,000th token just as reliably as the 100th. However, in practice, this
   assumption does not hold."
2. (Needle in a Haystack Extension, distinción metodológica clave) "Distractors are topically related to the
   needle, but do not quite answer the question. Irrelevant content is unrelated to the needle and question."
3. (Haystack Structure, hallazgo contraintuitivo) "Surprisingly, we find that structural coherence consistently
   hurts model performance. Although it seems counterintuitive, models perform worse when the haystack
   preserves a logical flow of ideas. Shuffling the haystack and removing local coherence consistently improves
   performance."
4. (LongMemEval, construcción exacta del dataset) "We use LongMemEval_s and filter for tasks that fall under
   the knowledge update, temporal reasoning, and multi-session categories. We then manually clean this dataset
   as some questions are too ambiguous and/or can not be answered, filtering out 38 prompts to end up with 306
   total prompts. These prompts average out to ~113k tokens... Focused prompts average to ~300 tokens."
5. (Repeated Words, construcción del filler/needle) "We design a controlled task in which the model must
   replicate a sequence of repeated words, with a single unique word inserted at a specific position... Number
   of words: 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000."
6. (Conclusión) "Even on tasks as simple as non-lexical retrieval or text replication, we see increasing
   non-uniformity in performance as input length grows... Whether relevant information is present in a model's
   context is not all that matters; what matters more is how that information is presented."

## Números principales

- Needle-question similarity (cos. sim., 5 modelos de embedding promediados): PG essay needles 0.445–0.775;
  arXiv needles 0.521–0.829 — a menor similitud, degradación más rápida con longitud.
- Needle-haystack similarity: en haystack PG, needles PG=0.529 (±0.101) vs needles arXiv=0.368 (±0.111); en
  haystack arXiv, needles arXiv=0.654 (±0.0858) vs needles PG=0.394 (±0.105). Efecto NO uniforme: en haystack
  PG, needles arXiv (menor similitud) rinden MEJOR que needles PG (mayor similitud) — contraintuitivo.
  En haystack arXiv, la diferencia entre ambos tipos de needle es mínima.
- Distractores: incluso 1 distractor reduce performance vs. baseline sin distractores; con 4 distractores la
  degradación se compone. El distractor 3 (de 4, en la combinación arXiv-haystack/PG-needle) causa caída mayor
  que los otros — impacto no uniforme entre distractores. Claude = menor tasa de alucinación (conservador,
  se abstiene ante ambigüedad); GPT = mayor tasa de alucinación (respuestas confiadas pero incorrectas).
- LongMemEval: gap de performance entre prompts focalizados (~300 tokens) y prompts completos (~113k tokens);
  Claude Opus 4/Sonnet 4 muestran el gap más pronunciado por abstención bajo ambigüedad.
- Repeated Words: refusal rate GPT-4.1 = 2.55% (empieza ~2500 palabras); Claude Opus 4 = 2.89% (única familia
  Claude que rechaza la tarea, por riesgo percibido de "generar material con copyright"); Qwen3-8B genera
  outputs aleatorios desde ~5000 palabras (4.21% de no-intentos); GPT-3.5-turbo EXCLUIDO del todo por 60.29%
  de rechazos (`finish_reason='content_filter'`). Precisión de posición del needle es mayor cuando la palabra
  única está cerca del INICIO de la secuencia, más marcado a mayor longitud. Score = distancia de Levenshtein
  normalizada.

## Qué les falta / qué nos toca respecto de WAGER — EL RIESGO METODOLÓGICO #1

- **Este es exactamente el riesgo que WAGER declara como riesgo metodológico #1**: que "evidencia diluida" se
  confunda con degradación por contexto largo. Context Rot demuestra que el mero HECHO de agregar tokens
  irrelevantes (sin cambiar la evidencia en sí) degrada performance de forma no uniforme — y que la posición,
  la coherencia estructural del relleno, y la similitud semántica relleno-pregunta AFECTAN el resultado
  independientemente de si el relleno "contamina" la evidencia real.
- **Implicación directa para el diseño de dosis limpia/mezclada de WAGER**: si el relleno usado para diluir
  evidencia en los forks (mixed/placebo) tiene distinta longitud, posición, o coherencia estructural que el
  relleno del brazo limpio, cualquier diferencia de F observada podría deberse a Context Rot, NO a que la
  evidencia esté "sucia". El pre-registro 0154 ya declaró una desviación en la construcción del relleno
  (relleno = 2 puntos de menor brecha de la grilla + mixed anidado) — este paper es el argumento externo de
  POR QUÉ esa desviación importa y necesita controles de longitud/posición idénticos entre brazos.
- **No miden revisión de creencias**: es un estudio puramente de recuperación/retención de información, sin
  ninguna noción de creencia, actualización, ni entrega puntuable contra verdad oculta. Es 100% un paper de
  CONTROL METODOLÓGICO para WAGER, no un competidor ni un molde de mundo.

## Lecciones de diseño — controles de longitud/posición/relleno que WAGER debería exigir

1. **Igualar longitud total del contexto entre brazos apareados** (clean vs mixed vs placebo): la cantidad de
   tokens de relleno debe ser IDÉNTICA entre brazos, no solo la cantidad de "evidencia real" — de lo contrario
   Context Rot por sí solo genera una diferencia de F espuria.
2. **Igualar POSICIÓN de la evidencia real dentro del contexto entre brazos**: el paper muestra que la posición
   del needle (early vs late) afecta precisión de forma sistemática; si en el brazo clean la evidencia cae
   temprano y en el mixed cae en medio del relleno, hay un confound de posición, no de dosis.
3. **Controlar la SIMILITUD SEMÁNTICA relleno-vs-contenido real, no solo el volumen**: el hallazgo de que
   needles semánticamente similares al haystack rinden distinto que needles disímiles (Needle-Haystack
   Similarity) implica que el relleno usado para "mixed" en WAGER debería documentar su similitud semántica al
   contenido de evidencia real, para poder descartar que ESA es la variable que mueve F, no la dosis de
   evidencia.
4. **Controlar la COHERENCIA ESTRUCTURAL del relleno**: contraintuitivamente, relleno con flujo lógico
   coherente DEGRADA más que relleno desordenado. Si el relleno de WAGER (turnos de conversación neutral,
   según el pre-registro 0154) tiene una narrativa coherente distinta entre brazos, eso es una variable de
   confusión adicional a controlar o al menos declarar.
5. **Reportar tasas de no-respuesta/abstención por separado, nunca mezclarlas con "no actualizó"**: el patrón
   de Claude (abstención conservadora bajo ambigüedad) que Context Rot documenta en NIAH y LongMemEval es
   directamente análogo al riesgo de que un "no entregó" o "entregó vacío" en un fork de WAGER se cuente como
   "no actualizó su creencia" cuando en realidad es una abstención distinta. WAGER ya tiene la disciplina de
   nunca excluir en silencio las no-entregas (ADR reciente, 28 no-entregas contadas en la pasada 1 del mapa) —
   este paper es la validación externa de por qué esa disciplina es necesaria específicamente en el eje de
   longitud/dilución de evidencia.

## Veredicto

**NOS ALERTA, riesgo confirmado empíricamente** — Context Rot no compite con WAGER (no mide creencias ni
entrega artefactos puntuables) pero es la evidencia externa más directa y más citable de que el riesgo
metodológico #1 de WAGER (diluir evidencia con relleno = confundir con degradación por contexto largo) es real,
medido en 18 modelos con 194k llamadas, y no uniforme (depende de posición, coherencia, similitud semántica).
Cualquier pre-registro de WAGER que use relleno para dosificar evidencia debe declarar explícitamente cómo
controla longitud, posición y coherencia del relleno entre brazos apareados, o el hallazgo de "evidencia sucia
domina" queda confundido con un artefacto de contexto largo puro.
