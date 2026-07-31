# Lectura completa — GeneBench-Pro (OpenAI, Jeremy Li & Andrew Ho, 30 jun 2026)

Fuente leída: PDF completo (22 págs, extraído verbatim con `pdftotext -layout` desde
`https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf`, no solo abstract) +
paquete público de Hugging Face `ajh-oai/genebench-pro-public-package` (listado completo de archivos vía API +
descarga y lectura directa de un `eval_config.json` real, problema `carrier_cnv_pseudogene_residual_risk`).

## Qué es (formato exacto, números)

- **Qué mide**: si un agente puede ejecutar un análisis científico multi-etapa (genómica, biología cuantitativa,
  biomedicina traslacional) desde datos crudos "sucios" hasta una conclusión cuantitativa, navegando bifurcaciones
  inferenciales encadenadas donde una elección plausible-pero-incorrecta cambia el resultado final.
- **Tamaño**: 129 evaluaciones, 10 dominios primarios, 21 subdominios terminales. Relativo a GeneBench (103
  problemas): +29 nuevos, −3 retirados, 54 rediseñados. Mediana de 6 "decision points" por problema (rango 3–13).
- **Release por capas**: 10 problemas públicos en HuggingFace (con grader y ground truth incluidos), 50 en
  holdout para benchmarking de terceros vía Artificial Analysis, 69 en holdout interno.
- **Revisión externa**: 84 problemas revisados por 11 expertos de dominio (grad students, postdocs, científicos
  de industria, profesores); 82 quedaron en la suite, 2 se retiraron por fallas fatales.
- **Datos**: 100% simulados (DGP completamente conocido/controlado), NO datasets reales históricos — esto es
  deliberado para que el grading sea identificable (ver cita §Construction abajo).
- **Grading**: binario, todo-o-nada por problema — pasa solo si TODOS los campos puntuados cumplen tolerancia.
  10 intentos independientes por par modelo-problema (5 para GPT Pro Extended y Claude Opus).

## Citas verbatim clave

1. (Abstract) "GPT-5.6 Sol reaches an eval-level pass rate of 28.7% at the max reasoning level... GPT-5.5
   reaches 12.0%, GPT-5.4 reaches 8.9%, and the strongest non-GPT baseline, Claude Opus 4.8, reaches 16.0%."
2. (Abstract, hallazgo cualitativo central) "models often complete substantial portions of the workflow but
   exhibit a consistent gap between noticing and acting by identifying local diagnostic signals but failing to
   propagate the implications to the corresponding analysis decision."
3. (Construction, Validation, and Grading) "GeneBench-Pro problems are based on constructively simulated
   problems where the full causal structure is known and where we simulate the full data-generating process
   (DGP)... [ensuring] (1) QC-sensitive decisions are robust to small researcher-choice variation, (2) plausible
   wrong analyses fail for substantive reasons, and (3) the graded endpoint is actually recoverable from the
   agent-visible data."
4. (Methods, Evaluation and grading) "Binary grading was performed based on pre-specified problem-specific
   target fields, exact-match rules, and absolute numeric tolerances. A run is counted as passing only if all
   graded fields satisfied their respective constraints."
5. (Discussion, sobre la limitación del grading binario) "a run that resolves most decision points but fails
   late is scored the same as one that fails immediately. Future versions of GeneBench-Pro may therefore add
   auxiliary stage-level or rubric-based scoring to measure partial progress, while retaining end-to-end pass
   rate as the primary metric."
6. (Table 1, principio de diseño) "Recoverable target: Agents are graded on recovering the quantity that is
   actually recoverable from agent-visible data, and not the hidden data-generating parameters."

## Números principales

- Progresión de pass rate por nivel de razonamiento GPT (mainline, mejor nivel reportado): GPT-5.2 4.9% →
  GPT-5.4 8.9% → GPT-5.5 12.0% → GPT-5.6 Luna 16.5% → GPT-5.6 Terra 23.3% → GPT-5.6 Sol 28.7% (max reasoning).
  GPT Pro (Extended): 8.5% → 16.3% → 20.5% → 23.6% → 28.5% → 31.5%.
  Dentro de GPT-5.6 Sol, subiendo el nivel de razonamiento: none 3.7% → low 14.4% → medium 22.5% → high 24.4%
  → xhigh 26.8% → max 28.7%.
- Cola sin resolver: fracción de problemas con 0% pass rate baja de 77.5% (GPT-5.2) a 45.7% (GPT-5.6 Sol);
  fracción con ≥50% pass rate sube de 1.6% a 30.2%.
- Costo humano de referencia: "a typical GeneBench-Pro problem would take on the order of 10–40 hours all-in.
  At a conservative $100–$200 per hour, the human labor cost of a single problem is already on the order of a
  few thousand dollars."

## Estructura del `eval_config.json` (leído directo, problema público real)

Archivo completo descargado y leído (`problems/carrier_cnv_pseudogene_residual_risk/eval_config.json`, 3054
bytes). Campos:

- `id`, `eval_uuid`: identificadores.
- `task`: el prompt completo mostrado al agente (texto libre en inglés, con la especificación exacta del JSON
  de salida esperado — schema in-line en el propio prompt).
- `data_files`: lista de rutas a los 5 archivos `.tsv.gz` que el agente puede leer.
- `grader`: `{"type": "multi_numeric_tolerance", "config": {"keys": {<campo>: {"absolute_tolerance": X,
  "min_value": 0.0, "max_value": 1.0}, ...}}}` — CADA campo de la respuesta tiene su PROPIA tolerancia absoluta
  independiente (en este ejemplo: 0.002, 0.002, 0.0005, 0.003, 0.0001 — varían en orden de magnitud según la
  sensibilidad esperada de cada estimando), más un rango `min_value`/`max_value` de validez.
- `ground_truth`: valores numéricos exactos de referencia para cada campo (ej.
  `couple_reproductive_risk: 0.0027676606874265544`) — publicados en el paquete público para reproducibilidad.

Layout del paquete completo (confirmado vía API de HF, `manifest.json`/`checksums.sha256` para integridad):
`problems.csv`, `manifest.json`, `checksums.sha256`, `reference_grader.py` (grader de referencia en Python
3.10+), `reference_definitions.md`, y `problems/<eval_id>/{eval_config.json, data_files/, report_public.pdf}`.

## Qué les falta / qué nos toca respecto de WAGER

- **No hay bifurcación apareada de creencia bajo evidencia dosificada**: GeneBench-Pro mide competencia
  estática de análisis multi-etapa, no revisión de creencias ante evidencia nueva inyectada en curso — no hay
  noción de "el agente ya entregó algo, llega evidencia, ¿corrige proporcionalmente?".
  Es un pariente de la MECÁNICA (mundo simulado con DGP conocido, grading cero-LLM con tolerancias) pero no
  del FENÓMENO (revisión de creencias).
- **Grading todo-o-nada vs F continua de WAGER**: GeneBench-Pro explícitamente NO mide fracción de mejora
  capturada — es pass/fail estricto por problema. Ellos mismos señalan esto como limitación futura (cita 5).
  WAGER con su métrica F (fracción de mejora legal capturada) ya resuelve lo que GeneBench-Pro declara como
  trabajo pendiente.
- **Sin verdad "hackeable" para test de identificabilidad rigurosa**: el principio "Recoverable target" (Table
  1) — gradúa solo lo recuperable de los datos visibles al agente, no el parámetro oculto del DGP — es
  exactamente la misma disciplina que la regla de certificación de mundos de WAGER (verdad oculta puntuable,
  no arbitraria); vale la pena citarlo como precedente externo de esa misma disciplina.

## Lecciones de diseño — estructura de `eval_config` y reglas de tolerancia

- **Tolerancia absoluta por campo, no relativa uniforme**: cada campo de salida tiene su propio
  `absolute_tolerance` calibrado a la escala/sensibilidad de ese estimando específico (0.0001 a 0.003 en el
  ejemplo) — no un umbral global. Para el scoring cero-LLM de WAGER (S_local, F) esto es un patrón directamente
  aplicable: si algún mundo de WAGER pide múltiples campos numéricos, la tolerancia debería fijarse por campo
  según sensibilidad, documentada en el propio contrato del problema, no como constante global del harness.
- **Ground truth publicado junto al grader**: para los 10 problemas públicos, el `ground_truth` completo vive
  en el mismo `eval_config.json` que el grader — reproducibilidad total sin caja negra. WAGER ya hace esto
  (verdad oculta server-side) pero el patrón de "todo el contrato de grading en un JSON versionado con
  checksums" (`manifest.json` + `checksums.sha256`) es una práctica de higiene que vale la pena adoptar para los
  bundles de casos si no está ya cubierta.
- **Ablation-supported workflow adjudication** (Table 1 del paper): antes de fijar una tolerancia o un ground
  truth, corren una "comprehensive ablation suite" que verifica que análisis plausibles-pero-incorrectos caen
  CLARAMENTE fuera de tolerancia — no basta con calcular el valor correcto, hay que demostrar separación
  numérica de los caminos incorrectos más plausibles. Esto es directamente relevante para la calibración de
  dosis de evidencia limpia/mezclada de WAGER: la separación entre brazos debe estar demostrada, no asumida.

## Veredicto

**NOS INFORMA, no compite** — comparte la disciplina de fondo (simulación con DGP conocido para que el grading
sea cero-LLM y defendible, verdad oculta recuperable-no-arbitraria, tolerancias calibradas por campo) pero mide
un fenómeno distinto (competencia de análisis multi-etapa estático, no revisión de creencias ante evidencia).
Su propia autocrítica (grading todo-o-nada pierde progreso parcial) es exactamente el problema que la métrica F
de WAGER ya resuelve — un buen punto de comparación para el paper/informe de WAGER cuando llegue el momento.
La estructura de `eval_config.json` (tolerancias por campo + ground_truth versionado) es el hallazgo más
directamente portable de esta lectura.
