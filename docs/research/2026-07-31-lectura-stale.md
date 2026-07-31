# Lectura completa — STALE: Can LLM Agents Know When Their Memories Are No Longer Valid? (arXiv 2605.06527)

> Leído vía `arxiv.org/html/2605.06527` (fetch + extracción dirigida, NO solo abstract). El apéndice de
> Limitaciones (A) aparece con headings pero el CUERPO de esas subsecciones no vino en la extracción —
> declarado explícito en la sección correspondiente abajo, no se rellena de memoria.

## Qué es

- **Tarea**: agente conversacional con memoria de largo plazo enfrenta escenarios donde una observación
  posterior invalida IMPLÍCITAMENTE una creencia anterior (sin negación explícita) — dos tipos: **Type I
  (co-referencial)**: dos observaciones actualizan el mismo atributo ("vive en Seattle" → luego firma
  contrato de alquiler en Portland, sin decir "ya no vivo en Seattle"). **Type II (propagado)**: una
  observación actualiza OTRO atributo cuyas consecuencias en cascada invalidan una creencia distinta (una
  lesión en la pierna invalida indirectamente la vigencia de "commutea en bici").
- **Turnos/longitud**: contextos de hasta 150K tokens; no es multi-turno agéntico con acción — son
  escenarios de conflicto de memoria conversacional con preguntas puntuales al final.
- **n**: 400 escenarios de conflicto validados por expertos, 1.200 queries de evaluación (3 dimensiones ×
  400), sobre 100+ temas cotidianos.
- **Modelos**: GPT-4o-mini, GPT-5.4-nano, GPT-5.4, Gemini-3.1-flash-lite, Gemini-3.1-pro,
  Llama-3.3-70B-Instruct, Qwen3.5-9B, Qwen3.5-27B, MiniMax-M2.5; + frameworks de memoria (LightMem, Zep,
  LiCoMemory, A-mem, mem-0); + su propio método CUPMem.
- **Cómo puntúan y quién juzga**: **juez LLM** (Gemini-3.1-flash-lite) evalúa la respuesta contra la
  "lógica de estado fundacional" (no contra strings de referencia sintéticos), con 95.8% de acuerdo con
  humanos reportado en el Apéndice E.3.

## Citas verbatim clave

- Definición del benchmark (Abstract/Intro): *"STALE, a benchmark of 400 expert-validated conflict
  scenarios (1,200 evaluation queries across three probing dimensions) spanning over 100 everyday topics
  with contexts up to 150K tokens."*
- Tipos de conflicto (Sección de diseño): *"Type I (co-referential) conflict arises when two observations
  update the same underlying attribute while remaining surface-compatible"* / *"Type II (propagated)
  conflict arises when the new observation updates a different attribute whose consequences cascade to an
  older belief."*
- Dimensión State Resolution: *"A successful response must identify the belief invalidation introduced by
  m_n."*
- Dimensión Premise Resistance: *"We present a misleading query that presupposes m_o remains true, without
  mentioning new entities from m_n... A successful model must reject the false premise and ground its
  response in the updated belief."*
- Dimensión Implicit Policy Adaptation: *"A successful response must proactively retrieve the current
  belief and translate it into appropriate downstream behavior."*
- Juez LLM (Experimental Setup): *"We use Gemini-3.1-flash-lite as the LLM judge to assess whether each
  response demonstrates awareness of the conflict and the updated user state."*
- Diagnóstico central (Sección 4.4): *"Our analysis reveals a central finding: updated evidence can be
  stored and retrieved, but it does not reliably become the basis that governs subsequent answers. We term
  this the current-state adjudication gap."*

## Números principales

- Mejor modelo evaluado (sin su propio método): **Gemini-3.1-pro, 55.2% overall accuracy**.
- Su método **CUPMem** (backbone GPT-4o-mini) sube overall de **8.7% → 68.0%**; el salto más grande es en
  Premise Resistance: 78.0%/75.0% (Type I/II) vs cerca de 0% en casi todos los baselines (GPT-4o-mini PR
  Type I = 0.0%; Gemini-3.1-pro PR Type I = 30.0%, el mejor baseline).
- Brecha reconocer-vs-actuar (gap SR→IPA): Qwen3.5-27B pasa de 76.0% (Type I-SR) a 39.0% (Type I-IPA); y de
  42.0% (Type II-SR) a 23.0% (Type II-IPA).
- Evidencia visible pero no gobierna la respuesta (Tabla 3): *"New evidence appears in retrieval results
  for 77.5% of SR/PR cases and 67.8% of IPA cases. However, visibility does not imply authority."*

## Qué les falta respecto de WAGER

- **Usan juez-LLM para TODO el scoring** (citado arriba: Gemini-3.1-flash-lite juzga si la respuesta
  "demuestra awareness" del conflicto) — no hay oráculo cero-LLM ni verdad ejecutable puntuada
  server-side; es lo opuesto de la regla dura de WAGER.
- No hay entrega de un artefacto EJECUTABLE puntuado contra verdad oculta — son preguntas puntuales sobre
  el estado de una memoria conversacional, no un modelo/código que el agente construye y entrega.
- No hay bifurcaciones apareadas (mismo punto de partida, evidencia dosificada distinta) ni fricción de
  reabrir trabajo propio acumulado — cada escenario es un par de memorias (vieja/nueva) inyectado una vez,
  no una trayectoria de trabajo largo con costo de revisar.
- Mide si la respuesta VERBAL refleja el estado actualizado (dice), no si una decisión con consecuencia
  real quedó actualizada (compra/entrega) — la brecha dice-vs-entrega central de WAGER no está instrumentada
  acá aunque el fenómeno que reportan (SR alto, IPA bajo) es un primo cercano.
- Apéndice de Limitaciones: los headings ("Benchmark scope", "Data construction", "Evaluation", "Method")
  aparecen pero el TEXTO no vino en la extracción — no se puede citar, declarado explícito, no inventado.

## Lecciones de diseño para WAGER

- La distinción **Type I (co-referencial) vs Type II (propagado)** es un eje de dosis de evidencia útil:
  hoy nuestras inyecciones CLEAN/MIXED/PLACEBO (ADR 0154) dosifican por KL/logLR pero no distinguen si la
  invalidación es DIRECTA (mismo atributo) o PROPAGADA (cascada a otro atributo) — podría ser un eje nuevo
  de dificultad dentro de la carga.
- El fenómeno **"visibility ≠ authority"** (evidencia aparece en el contexto recuperado pero no gobierna
  la respuesta) es literalmente el vocabulario que buscamos para la brecha dice/compra/entrega: ellos lo
  miden vía retrieval logs; nosotros ya lo medimos vía consecuencia cobrada (F), lo cual es un paso más
  fuerte — vale citarlos como validación externa de que el fenómeno existe y es medible.
- Su gap SR→IPA (reconocer bajo pregunta directa vs aplicar en tarea downstream natural) es análogo a nustro
  contraste "declarar la corrección" vs "que la corrección aparezca en el modelo entregado" — confirma que
  medir solo lo primero sobreestima la actualización real.

## Veredicto

**NOS-VALIDA** (con matiz): confirma con un benchmark independiente y de escala considerable
(1.200 queries, 14+ modelos/sistemas) que "recuperar evidencia actualizada ≠ que gobierne el comportamiento
subsiguiente" — la tesis nuclear de WAGER — pero lo hace con juez-LLM y preguntas puntuales, no con reward
cero-LLM sobre un artefacto entregado y trabajo propio acumulado. Sirve como evidencia externa de que el
fenómeno es real y generalizable, no como método a portar.
