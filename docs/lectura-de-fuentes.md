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
| Kosmos (corpus de Lucas) | Agente de descubrimiento autónomo | *(buscar URL)* | [ ] |
| OSWorld-V2 (corpus de Lucas) | Agentes de computer-use en tareas de escritorio | *(buscar URL)* | [ ] |
| Vibe-physics (corpus de Lucas; ¿Anthropic?) | Modelo haciendo física exploratoria con un humano | *(buscar URL + confirmar autoría)* | [ ] |
| SciAgentGym (corpus de Lucas) | Gimnasio de tareas científicas con herramientas | *(buscar URL)* | [ ] |
| Ríos-García et al. 2026 — "AI scientists produce results without reasoning scientifically" (2604.18805) | **CORRECCIÓN**: NO es CLadder/QRData (así lo describía mal nuestro corpus) — son **8 dominios de química/materiales** (sim. molecular, espectroscopía, análisis químico, circuitos, retrosíntesis...), 3 modelos × 2 scaffolds, **25.000+ corridas** | arxiv.org/pdf/2604.18805 (109 pág; solo PDF, extraído con pymupdf) | **LEÍDO** (2026-07-09) |
| MLR-Bench (2505.19955) | Agentes en investigación de ML abierta (NeurIPS 2025) | arxiv.org/html/2505.19955 | [ ] |
| Wang et al. 2026 — "The Long-Horizon Task Mirage" (HORIZON, 2604.11978) | Agentes web/OS/DB/embodied en tareas largas; taxonomía de 7 fallas | arxiv.org/html/2604.11978 | **LEÍDO** (2026-07-09) |
| BED-LLM (2508.21184) | Agente juntando info (20 preguntas / diseño experimental) | arxiv.org/html/2508.21184 | [ ] |
| Su & Cardie 2026 (2605.25284) | Modelos ante consultas ambiguas (preguntar vs adivinar) | arxiv.org/html/2605.25284 | [ ] |
| Corr2Cause (2306.05836) | Inferencia causal desde correlación, 17 modelos | arxiv.org/html/2306.05836 | [ ] |
| Vaccaro 2026 (2606.11217) | Grados de libertad en experimentos hechos POR agentes | arxiv.org/html/2606.11217 | [ ] |
| The AI Scientist (Sakana) + críticas | Agente que genera papers de punta a punta | *(buscar URL)* | [ ] |
| AI Co-Scientist (Google) | Sistema multi-agente de hipótesis científicas | *(buscar URL)* | [ ] |
| SciAgentBench / DiscoveryWorld / DiscoveryBench | Benchmarks de descubrimiento con análisis de error | *(buscar URLs)* | [ ] |

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
