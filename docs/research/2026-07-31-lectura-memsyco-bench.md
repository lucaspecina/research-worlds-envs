# Lectura completa — MemSyco-Bench: Benchmarking Sycophancy in Agent Memory (arXiv 2607.01071)

> Leído vía `arxiv.org/html/2607.01071` (fetch + extracción dirigida, NO solo abstract). El Apéndice D
> (rúbricas/métricas completas) aparece referenciado pero su texto NO vino completo en la extracción — no
> se pudo confirmar con cita textual si el grading final usa juez-LLM o es rule-based; declarado explícito
> abajo, no inventado. Tampoco apareció una sección "Limitations" explícita en el texto extraído (el paper
> pasa de resultados a "Conclusion" en lo que se pudo leer).

## Qué es

- **Tarea**: agentes con sistema de memoria de largo plazo responden consultas donde memorias
  almacenadas del usuario (hechos/preferencias declarados antes) pueden entrar en conflicto con evidencia
  objetiva actual o con el alcance correcto de aplicación — mide "sycophancy inducida por memoria".
- **Cinco categorías de tarea** (Sección 3.2): *"Objective Fact Judgment tests objective questions where
  historical user memory is present but should not serve as evidence"*; *"Contextual Scope Control tests
  whether the agent respects memory scope"*; *"Memory-Evidence Conflict tests whether the agent follows
  verified evidence when it conflicts with user memory"*; *"Valid Memory Selection tests whether the agent
  can identify the currently valid preference when a user's preference has been updated"*; *"Personalized
  Memory Use tests whether the agent can use it to improve responses in recommendation, advice, or
  subjective-choice tasks."*
- **Turnos/longitud** (Sección 3.3): *"we simulate preceding dialogues between a user and an agent to place
  these fragments into a natural interaction history"*, con *"each dialogue around 10 turns"*.
- **n**: tamaño exacto del dataset no confirmado en el texto extraído (Tabla 1 muestra comparación entre
  sistemas pero el conteo de instancias no vino en la porción leída) — declarado explícito, no inventado.
- **Modelos**: Qwen3-8B y DeepSeek-V4-Flash como backbones principales; otros backbones reportados en
  apéndice (no confirmados con números en esta lectura). Sistemas de memoria evaluados: NaiveRAG, Mem0,
  A-Mem, LightMem, MemGPT, MemoryBank, SuperMemory.
- **Cómo puntúan y quién juzga**: métricas de "Generation Accuracy", "Sycophancy Rate" y "Memory-Use
  Metrics" (Sección 3.4 / Apéndice D); la Sycophancy Rate se calcula *"when the response follows memory
  when it should not"* en las categorías Objective Fact Judgment, Contextual Scope Control y
  Memory-Evidence Conflict. **No se pudo confirmar con cita textual si hay juez-LLM** en el grading final —
  el Apéndice D con la rúbrica completa no vino en la extracción.

## Citas verbatim clave

- Definición de sycophancy inducida por memoria (Sección 3.1): *"memory-induced sycophancy"* es *"a failure
  mode in which a long-term memory system stores user beliefs, preferences, or past statements from
  historical dialogues as external memory, and later reintroduces them into main context for new requests.
  This memory is intended to support personalization, but it can become misleading when the current task
  requires objective evidence."*
- Distinción vs sycophancy tradicional (Introducción): *"prior work mainly examines sycophancy within the
  current interaction, where the model aligns with a position explicitly stated by the user in the prompt
  or dialogue... In memory-enabled agents, user influence is no longer confined to the current
  interaction."*
- Tres características propias (Introducción): *"Source: the source of influence shifts from the current
  user input to retrieved historical memories"*; *"Decision role: the failure extends beyond simply
  agreeing with the user"*; *"Duration: the same memory can persist across sessions and repeatedly shape
  later responses."*
- Caso extremo citado (Sección 3.4, Memory-Evidence Conflict, Qwen3-8B Full Dialog): *"0.67 Acc with a
  99.33 Syco. Rate."*

## Números principales

- Qwen3-8B, Objective Fact Judgment: baseline sin memoria 49.12% accuracy / 27.43% sycophancy rate; con
  diálogo completo en contexto ("Full Dialog") 30.62% accuracy (**-18.50pp**) / 44.67% sycophancy
  (**+17.24pp**); con NaiveRAG 34.00% accuracy / 46.00% sycophancy rate.
- DeepSeek-V4-Flash, Objective Fact Judgment: baseline sin memoria 74.33% / 18.67%; Full Dialog 61.67%
  (**-12.66pp**) / 32.67% (**+14.00pp**).
- Memory-Evidence Conflict, Qwen3-8B Full Dialog: 0.67% accuracy con 99.33% sycophancy rate — el modelo
  casi siempre sigue la memoria vieja aun con evidencia verificada en contra.

## Qué les falta respecto de WAGER

- **No confirmado si el scoring final usa juez-LLM** — es una brecha de lectura, no un hallazgo firme; hay
  que volver al Apéndice D antes de citar esto como "cero-LLM" o como "usa juez". No se cita como uno u
  otro sin la evidencia textual.
- No hay verdad ejecutable/oráculo de dominio con presupuesto de acción — es Q&A sobre memorias
  simuladas, no un artefacto que el agente construye y entrega puntuado contra verdad oculta.
- La "memoria" acá es la del USUARIO (preferencias/hechos que el usuario declaró antes), no el trabajo
  PROPIO del agente — es un eje distinto al de "carga por trabajo propio acumulado" que persigue WAGER
  (mapa de carga, ADR 0153/0154): en MemSyco el agente sigue una preferencia AJENA vieja, en WAGER
  buscamos si el agente protege SU PROPIA conclusión previa.
- No hay bifurcaciones apareadas ni dosis de evidencia cuantificada por KL/logLR — el contraste es
  estructural (No Memory vs Full Dialog vs sistema de memoria X), no dosis fina.

## Lecciones de diseño para WAGER

- El patrón de contraste **"No Memory (baseline) vs Full Dialog vs sistema de memoria específico"** es un
  diseño de control limpio y reusable: aísla cuánto degrada la sola PRESENCIA de memoria acumulada,
  independientemente del mecanismo de recuperación. Podríamos adoptar una versión de ese contraste como
  chequeo de calibración adicional en el mapa de carga (celda "sin carga previa" vs "con carga previa
  acumulada") — cerca de lo que ya hace el freno CLEAN>MIXED>PLACEBO pero para el eje de carga propia en
  vez de dosis de evidencia.
- Confirma cuantitativamente que retener memoria vieja compite con evidencia nueva incluso cuando la
  evidencia está "verificada" (Memory-Evidence Conflict: 99.33% sycophancy rate) — deltas grandes y
  medibles contra un baseline sin memoria son la forma de hacer visible el efecto, que es la misma lógica
  de nuestro dS vs media de bases apareadas.
- Distinción útil para el vocabulario del proyecto: la memoria del USUARIO vs la memoria/trabajo PROPIO del
  AGENTE son dos fuentes de carga distintas — vale nombrar explícitamente cuál mide cada mundo para no
  confundir "sycophancy hacia el usuario" con "apego al propio trabajo previo" (el segundo es el foco de la
  Pasada 2 del mapa de carga, "carga vivida").

## Veredicto

**NOS-COMPITE parcialmente**: el fenómeno que miden (memoria vieja que gana a evidencia nueva verificada)
es un primo cercano del vicio central de WAGER, con números duros y un diseño de contraste reusable, pero
mide sycophancy HACIA EL USUARIO (memoria ajena), no carga de TRABAJO PROPIO del agente — es un eje
relacionado pero distinto, no reemplaza el mapa de carga. Útil como comparador de diseño y como fuente
externa a citar en `docs/vicios/`, pendiente de confirmar su mecanismo exacto de scoring antes de citarlo
como cero-LLM o no.
