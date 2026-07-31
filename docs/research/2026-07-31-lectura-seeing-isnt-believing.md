# Lectura completa — Seeing Isn't Believing: Mitigating Belief Inertia via Active Intervention in Embodied Agents (arXiv 2604.17252)

> Leído vía `arxiv.org/html/2604.17252` (fetch + extracción dirigida, NO solo abstract).

## Qué es

- **Tarea**: agentes embodied que ejecutan acciones en simuladores y reciben observaciones del entorno;
  el paper mide y corrige "belief inertia" (adherencia terca a la expectativa previa pese a evidencia
  contradictoria) con el mecanismo **Estimate-Verify-Update (EVU)**.
- **Benchmarks**: ALFWorld (Shridhar et al. 2020), VirtualHome (Puig et al. 2018), ScienceWorld (Wang et
  al. 2022).
- **Turnos/longitud** (Apéndice B, Tabla 3): promedio de turnos por episodio — ALFWorld 7.97, VirtualHome
  8.79, ScienceWorld 9.64.
- **n** (train/test seen/unseen): ALFWorld 2.851 train, 140 seen / 134 unseen test; VirtualHome 2.460
  train, 125/125; ScienceWorld 1.253 train, 151/161.
- **Modelos**: DeepSeek V3.2 (evaluación por prompting, con ReAct); Qwen2.5-3B-Instruct y
  Qwen3-1.7B-Instruct (evaluación por entrenamiento, con GRPO).
- **Cómo puntúan y quién juzga**: **Success Rate = recompensa binaria del ENTORNO** (1 tarea completada, 0
  no) — **no hay juez-LLM** para la corrección; el reward es del simulador.

## Citas verbatim clave

- Mecanismo EVU, fase de estimación (Sección 4.1): *"the agent attempts to predict the immediate
  consequence of its previous action before processing the actual new observation... establishes a
  baseline expectation by estimating action outcomes Et as: Et∼πθ(⋅∣Bt−1,at−1,ot)"*
- Fase de verificación: *"The agent then processes the actual observation ot from the environment. Instead
  of updating the belief directly, the agent first generates a verification evidence Vt to compare its
  estimation against the actual observation: Vt∼πθ(⋅∣Bt−1,at−1,ot,Et)"*
- Fase de actualización de creencia: *"the agent synthesizes the reasoning chain to transition from the
  previous belief state Bt−1 to the current belief state Bt... takes the prior belief, the initial
  estimation Et, and the verification evidence Vt (i.e., the surprise signal) as inputs:
  Bt∼πθ(⋅∣Bt−1,at−1,ot,Et,Vt)"*
- Definición de belief inertia: *"agents tend to stubbornly adhere to their prior expectations of action
  outcomes, even when faced with contradictory evidence."*
- Métrica (Sección de evaluación): *"Across all three domains, the environments provide binary final
  rewards, where a reward of 1 indicates successful task completion and 0 indicates failure."*
- Hallazgo estadístico (Figura 2): *"our statistical analysis on the ALFWorld benchmark reveals that such
  neglect is not a marginal error but a predominant failure mode in unsuccessful trajectories."*

## Números principales

- DeepSeek V3.2 + ReAct + EVU vs baseline (Success Rate): ALFWorld seen 55.7→56.4 (+0.7), unseen
  47.6→49.8 (+2.2); VirtualHome seen 13.6→16.0 (+2.4), unseen 12.8→13.6 (+0.8); ScienceWorld seen
  60.3→62.3 (+2.0), unseen 57.8→60.9 (+3.1).
- Qwen2.5-3B-Instruct + GRPO + EVU (mayores ganancias): ALFWorld unseen 70.8→79.1 (+8.3); VirtualHome
  unseen 24.8→36.0 (+11.2); ScienceWorld unseen 52.8→70.8 (**+18.0**, el salto mayor del paper).

## Qué les falta respecto de WAGER

- No hay evidencia DOSIFICADA por diseño (KL/logLR controlado): la evidencia es la observación natural que
  da el simulador tras cada acción, sin manipulación de dosis limpia/mezclada/placebo.
- No hay bifurcaciones apareadas (mismo punto de partida, atribución self/peer, compromiso draft/bound) —
  es una comparación con-EVU vs sin-EVU, no un factorial de autoría × compromiso × evidencia.
- El reward SÍ es cero-LLM (binario del entorno) — en esto coincide con la regla dura de WAGER — pero la
  tarea es de acción física de corto alcance (7-10 turnos), no de trabajo propio acumulado largo con costo
  de reabrir ni de corrección de un MODELO EJECUTABLE.
- No miden fracción de mejora legal capturada (F) ni brecha dice/compra/entrega explícita — miden éxito de
  tarea, no qué fracción de la corrección disponible quedó incorporada.
- Limitaciones declaradas por los propios autores: *"Dependency on Observation Quality: Our method relies
  on the quality and granularity of environmental observations... the agent's belief updates may become
  unstable."* y *"Limited Exploration of Model Variants: Due to computational resource constraints, our
  experiments on prompting methods were primarily conducted using DeepSeek V3.2."*

## Lecciones de diseño para WAGER

- El andamiaje **Estimate→Verify→Update** es un comparador de proceso que hoy no tenemos: pedirle al agente
  que declare su expectativa ANTES de ver la evidencia inyectada, que la compare explícitamente contra lo
  observado (evidencia de verificación = "señal de sorpresa"), y recién ahí actualice. Es una intervención
  candidata para testear en el mapa de carga (ADR 0154) — NO como parte del reward (sigue siendo cero-LLM,
  puntuado contra verdad oculta), sino como manipulación de PROCESO adicional a AUTHOR_ROLE/MODEL_STATUS,
  para ver si estructurar la actualización mueve F.
- El hallazgo de que la inercia de creencia "no es un error marginal sino el modo de falla predominante en
  trayectorias fallidas" valida la estrategia de WAGER de medir por CONSECUENCIA real (falla de tarea /
  score contra verdad oculta) en vez de por verbalización — coincide con nuestra regla de "cobrado contra la
  verdad, cero-LLM".

## Veredicto

**NOS-CAMBIA-EL-DISEÑO** (parcial): el mecanismo EVU es una intervención de proceso concreta y barata de
adoptar como tratamiento experimental (no como reward) dentro del mapa de carga — vale proponerlo como una
celda o manipulación adicional para ver si estructurar estimar/verificar/actualizar mueve la fracción de
mejora legal capturada, manteniendo el scoring cero-LLM que ya usamos.
