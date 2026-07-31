# Lectura completa — "Skill Use or Skill Theater? Evaluating the Reasoning Backroom in Skill-Augmented Language Agents" (BACKTRACE / BackroomBench, arXiv 2607.27484)

Autores: Jinwei Hu, Yi Qi, Xinmiao Huang, Youcheng Sun, Yi Dong, Xiaowei Huang.

Fuente leída: `arxiv.org/html/2607.27484` (HTML completo), no solo abstract — extracción con secciones, ecuaciones y tablas citadas abajo.

## Qué es

- **Tarea**: agentes con "skills" (herramientas/prompts de habilidad inyectados) resuelven problemas de lógica y matemática. Para cada instancia se generan tanto la decisión SIN skill (d_∅) como la decisión CONDICIONADA por skill (d_v) bajo siete condiciones de intervención (none, correct, paraphrase, misleading, name swap, content swap, irrelevant), y se compara contra la afirmación explícita del agente sobre si usó el skill. Dos dominios: **Lógica** (problemas estilo PrOntoQA, taxonomías de primer orden) y **Matemática** (problemas naturales estilo MATH-500).
- **Turnos/duración**: NO es una interacción multi-turno — son episodios de decisión únicos con una consulta de atribución posterior a la decisión ("post-decision attribution queries"). El paper no reporta T ni duración porque no aplica.
- **n**: **BackroomBench** = 300 problemas de Lógica (60 instancias por cada una de 5 profundidades de prueba: 2, 4, 6, 8, 10 pasos) + 283 problemas de Matemática (MATH-500, estratificados por dificultad 1-5). Total single-agent: 600 instancias lógica+matemática. Además hay una condición multi-agente con "matched single- and multi-agent organizations" (n de equipos no desglosado en el extracto).
- **Modelos evaluados**: doce modelos en Lógica, subconjunto de seis en Matemática — Qwen2.5-Instruct (7B, 14B, 32B), DeepSeek-R1-Distill-Qwen (7B, 14B, 32B), GPT-4.1 (nano, mini), GPT-5 (nano, mini), GPT-5.4 (nano, mini).
- **Cómo puntúan** (con números):
  - **Reliance (confianza causal)**: `r_v(s,x) = 𝟙[d_v ≠ d_∅]` — si la decisión cambia al dar el skill.
  - **Signed utility**: `u_v(s,x) = 𝟙[d_v = d*] − 𝟙[d_∅ = d*]` — si el cambio ayuda (+1), perjudica (−1) o no cambia la corrección (0).
  - **Reasoning Backroom / mismatch**: `m_v(s,x) = 𝟙[a_v(s,x) ≠ r_v(s,x)]` — el agente afirma uso (a_v) pero la dependencia real (r_v) no coincide.
  - **AFS (Attribution Fidelity Score)**: `AFS = 2n₁₁/(2n₁₁ + n₁₀ + n₀₁) = HMean(1−SUR, 1−PUR)`, con n₁₁ = uso explícito fiel, n₁₀ = adopción silenciosa (usó pero no lo dijo), n₀₁ = uso performativo (dijo que usó pero no dependió de él).
  - **Backroom Gap (Γ)**: `Γ_v = (n₁₀ + n₀₁)/N_v` — tasa de desacuerdo entre reliance-por-intervención y uso afirmado.
  - Métricas multi-agente: CAP (Cross-Agent Propagation), LR (Laundering Rate), FPR (False Provenance Rate).
  - Detectores observacionales de línea de base (Tabla 5): precisión de atribución explícita 0.32 / recall 0.90 (a tasa base de reliance de 0.34, equivalente a adivinar al azar); mención de skill: precisión 0.37 / recall 0.08; similaridad de traza: precisión 0.31 / recall 0.45.

## Citas verbatim clave

1. (Formulación del problema) "The intervention defines causal reliance and signed utility as r_v(s,x)=𝟙[d_v≠d_∅], u_v(s,x)=𝟙[d_v=d*]−𝟙[d_∅=d*]."
2. (Introducción, hallazgo principal) "We find a pervasive Reasoning Backroom: attribution diverges from decision dependence, effects follow procedural content rather than displayed identity, and propagated influence loses provenance."
3. (Formulación del problema, definición de Backroom) "A Reasoning Backroom failure occurs when the front-room claim disagrees with intervention-defined dependence, m_v(s,x)=𝟙[a_v(s,x)≠r_v(s,x)]."
4. (Experimentos, RQ1) "Skill-augmented agents exhibit a clear Reasoning Backroom. Figure 1 shows nearly saturated correct-skill attribution even as accuracy and removal-defined reliance vary across models and proof depths."
5. (Experimentos, RQ3) "Skill influence can propagate while its causal provenance is lost. In Table 4, LR is often nearly as large as CAP across both domains."
6. (Metodología, conclusión de método) "Confirming dependence requires intervention. The Reasoning Backroom is a general AI provenance problem whose causal claims require intervention."
7. (Diseño apareado) "Every comparison fixes the task instance, model, prompt frame, decoding policy, and organization while varying only the skill or its assignment."
8. (Sobre el observador ciego) "At this base rate, a flagged run is no more likely than an average run to show actual reliance." (Tabla 5, sobre detectores observacionales)

## Números principales

- Tabla 2 (Lógica, single-agent): Qwen-7B AFS = .53 (correcto), colapsa a .53 (misleading), .45 (paraphrase), .47 (name swap). GPT-5-mini: accuracy base 1.00 pero AFS cae a .01 (correcto), .02 (paraphrase), .31 (misleading). GPT-5.4-nano: ΔAcc +.49 (correcto), +.47 (paraphrase), con AFS igual alto (.72, .69) — es decir, la afirmación de uso rastrea mal la dependencia real incluso cuando el skill sí ayuda.
- Tabla 3 (Matemática, single-agent): ningún par modelo-condición supera AFS .43. Qwen-32B: .27 (correcto), .25 (paraphrase), .29 (name swap).
- Tabla 4 (Multi-agente): Laundering Rate sigue de cerca a CAP — Qwen-14B: CAP .33, LR .33, PR .01 en Lógica. False Provenance Rate cercana a 1.00 de forma consistente en equipos SIN skill (nombran skills que no existieron).
- Tabla 5 (Detectores observacionales): precisión de atribución explícita apenas .32 con recall .90, no mejor que azar a la tasa base de reliance (.34).

## Qué les falta respecto de WAGER

- **Modelo ejecutable puntuado contra verdad oculta**: NO — la salida es una decisión discreta (respuesta a un problema de lógica/matemática), correcta o incorrecta contra d*, no un modelo/artefacto ejecutable evaluado con una métrica rica.
- **Bifurcación apareada del mismo episodio congelado cambiando UNA condición**: SÍ, de forma muy limpia — "every comparison fixes the task instance, model, prompt frame, decoding policy, and organization while varying only the skill or its assignment" es exactamente la disciplina de un solo grado de libertad por brazo que WAGER exige. Es el paper más disciplinado de los cuatro en este punto específico, aunque el "fork" acá es sobre presencia/atribución de un skill, no sobre evidencia post-hoc que corrige una creencia previa.
- **Evidencia con valor probatorio cuantificado (KL/likelihood)**: NO — confirmado explícitamente ("No Quantified Likelihood/KL Metrics... The paper uses deterministic paired comparisons rather than probabilistic divergence measures"). La incertidumbre se maneja con bootstrap pareado sobre 10.000 remuestreos de instancias, no con dosis de evidencia cuantificada.
- **Trabajo propio acumulado**: NO — cada instancia es una decisión aislada de un problema, sin historial de trabajo previo del agente que compita con la nueva información.
- **Fricción de revisión**: parcialmente — hay una noción acotada de costo ("at most one format-only repair, which cannot re-solve the task"), pero es un límite de reparación de formato, no una fricción estructural de reabrir/rehacer un artefacto ya entregado.
- **Casos cambiar/conservar/parcial**: NO en el sentido de WAGER (revisar una creencia frente a evidencia gradual) — su taxonomía es sobre FIDELIDAD DE ATRIBUCIÓN (¿lo que el agente dice que usó coincide con lo que realmente usó?), un eje ortogonal al de "cuánta evidencia justificada se incorpora".
- **Cero-LLM en el reward**: SÍ — todas las métricas (AFS, Γ, CAP, LR, FPR) se computan de forma determinística contra d* (respuesta correcta conocida) y contra las decisiones mismas, sin juez-LLM en el cómputo.

## Lecciones de diseño para WAGER

- **Copiar (disciplina de un grado de libertad)**: la frase "fixes everything except the one manipulated variable" es la formulación más limpia y citable de la disciplina de bifurcación de WAGER — vale la pena citarla textualmente en cualquier ADR o pre-registro que defienda el diseño de "cambiar UNA condición por brazo".
- **Copiar (el gap dicho-vs-hecho)**: el patrón central de BACKTRACE — comparar lo que el agente AFIRMA (atribución explícita) contra lo que la intervención MIDE (reliance real) — es directamente transportable a WAGER como un chequeo lateral: comparar lo que el agente dice que incorporó de la evidencia nueva (si se le pregunta) contra lo que el modelo entregado realmente refleja (F). Es una fuente potencial de un "vicio" adicional: afirmar haber actualizado sin haberlo hecho (o al revés, actualizar sin admitirlo).
- **Copiar**: el hallazgo de que detectores observacionales pasivos (mención de skill, similaridad de traza) rinden igual que azar para detectar dependencia real (Tabla 5) es una advertencia útil para WAGER — si en algún punto WAGER quisiera inferir actualización de creencia SOLO de lo que el agente dice en el texto (sin forzar el brazo contrafactual), este paper es evidencia directa de que eso no funciona y hay que forzar la intervención.
- **Evitar**: el dominio (lógica/matemática con respuesta correcta única) es demasiado pobre para servir de molde de mundo — no hay gradación de "cuánto" se actualizó, solo si la decisión discreta cambió.
- **Citar**: el término acuñado "Reasoning Backroom" y el framework BACKTRACE son referencias directas para posicionar WAGER dentro de la literatura de "lo que el agente dice vs. lo que el agente realmente hace/incorpora" — mismo espíritu que la regla dura de WAGER de puntuar la ENTREGA, no el discurso.

## Veredicto

**NOS-VALIDA** — con la disciplina experimental más cercana a la de WAGER de los cuatro papers ("fix everything except one manipulated variable") y con un hallazgo hermano directamente relevante (lo que el agente DICE que hizo con la información no predice lo que realmente hizo con ella, y los detectores pasivos no lo distinguen de azar). No compite porque mide fidelidad de atribución de skills en decisiones discretas de un solo paso, sin modelo ejecutable, sin evidencia cuantificada, sin trabajo propio acumulado ni fricción de revisión — pero es la lectura más útil de las cuatro para reforzar por qué WAGER exige forzar el contrafactual en vez de confiar en lo que el agente narra sobre su propio proceso.
