# Lectura completa — "An Experimental Design Approach to Evaluating Agentic AI's Autonomous Model Discovery" (arXiv 2607.06413)

Autores: Hao He, Xueying Liu, Chris J. Kuhlman, Xinwei Deng.

Fuente leída: `arxiv.org/html/2607.06413` (HTML completo), no solo abstract — extracción con secciones, ecuaciones y tablas citadas abajo.

## Qué es

- **Tarea**: agentes de código (Codex, Claude Code) hacen "model discovery" autónomo sobre datos de un juego en red de formación de palabras (anagram game). Dos tareas: **Task 1 (Timestep)** — predicción de próxima acción de 4 clases por jugador y tiempo, con probabilidad `p̂(a_{v,t+1}=j | h_{v,t})`; **Task 2 (ABM)** — construcción de un simulador generativo basado en agentes (agent-based model).
- **Turnos/duración**: no es un episodio conversacional multi-turno tipo chat; cada "run" es una sesión completa de descubrimiento de modelo por el agente de código. Las sesiones de juego que generan los datos base duran `t_max = 300 segundos` (§3.1).
- **n**: dataset base de 2.828 sesiones y 209 jugadores = 62.700 registros jugador-tiempo, partido en 3 folds de cross-validation (§3.1). Total de **144 corridas programadas del agente**, de las cuales **140 son válidas** (analizadas en §5.1).
- **Modelos evaluados**: dos agentes de código comerciales con versión fijada — **Codex: OpenAI Codex CLI v0.125, modelo GPT-5.5**; **Claude Code: Claude Opus 4.7** (§3.1). Tres niveles de esfuerzo de razonamiento por agente, codificados con contrastes polinomiales ortogonales (contraste lineal x^L_i, §4.1).
- **Cómo puntúan** (con números): cuatro métricas primarias (§3.3):
  - **wAUC** (Task 1, ponderado por clase): `wAUC^(k) = Σ_{j=1}^4 (n_j^(k)/n^(k))·AUC_j^(k)`.
  - **MRI-RO** (Task 1, mejora relativa media en casos raros): `MRI^(k) = (1/|D_rare^(k)|)·Σ_{r∈D_rare^(k)} Δ_r`.
  - **KL₆** (Task 2, divergencia KL promedio sobre 6 magnitudes): `KL₆^(k) = (1/6)·Σ_{m=1}^6 KL_m^(k)`.
  - **DLD** (Task 2, distancia tipo Levenshtein sobre distribuciones): `DLD^(k) = ∫_0^∞ |F^(k)(z) − F̂^(k)(z)| dz`.
  - Ocho coordenadas de respuesta en total (Tabla 2): performance (2), costo (2), proceso (4). Se corren regresiones e inferencia por cada combinación agente-tarea-métrica, más una "descomposición canónica alineada a utilidad" para caracterizar la dirección dominante del efecto de esfuerzo de razonamiento.

## Citas verbatim clave

1. (Sección 1) "Agentic AI and large language coding agents now carry out the technical work of data modeling and analysis without human intervention. These agents are stochastic, adaptive, sequential decision-making systems, and their autonomous discovery behavior cannot be adequately evaluated by single-run benchmarks."
2. (Sección 1) "We propose an experimental design and analysis framework that systematically probes the AI model-discovery operator through data from networked anagram games, measuring the variability of its discovery process and identifying the factors that affect it."
3. (Sección 5.2, hallazgo de efecto de esfuerzo) "More effort lowers utility in every stratum" — pendiente lineal negativa en las 8 franjas, "significant without correction in seven of eight."
4. (Sección 6.1, implicación práctica) "The main practical implication is that requested reasoning effort acts more like a resource-control parameter than a reliable path to better models."
5. (Sección 6.1) "Higher effort produces longer, costlier, and more complex runs. It does not produce a matching gain in model quality."
6. (Sección 3.2, diseño apareado) comparación de régimen de descubrimiento completo vs. parcial ("halving training data") — corridas "matched" que difieren solo en disponibilidad de datos.

## Números principales

- Pendientes de utilidad (Tabla 5): rango −0.46 a −1.08 con IC 95% que excluye cero en 7 de 8 franjas.
- Descomposición canónica: los 8 valores η^(1) son negativos; sign test p=0.008 (§5.2).
- Costo en tokens: "Median fresh-token use climbs from 29.4k to 91.6k for claude-code and from 69.6k to 170.5k for codex" (§5.1).
- Costo en dólares: "Codex stays at low dollar cost... median cost of $0.60 against claude-code's $4.19, roughly seven times higher" (§5.1).
- Performance: efecto del esfuerzo "weak" sobre métricas primarias solas (Tabla 4) — solo a-DLD llega a p=0.029.
- Auto-evaluación (§5.1, Figura 8): los agentes se autoevalúan bien en la tarea predictiva (Task 1) y mal en la generativa (Task 2); en Task 2, "83% of claude-code's a-KL runs" quedan marcados como sobreconfiados; cuatro corridas fallan la validez de simulación por completo.
- Ventaja de más datos (régimen completo vs. parcial): solo se ve claramente en la condición a-KL (Figura 6).

## Qué les falta respecto de WAGER

- **Modelo ejecutable puntuado contra verdad oculta**: SÍ tienen algo cercano — Task 2 construye explícitamente un simulador (ABM) ejecutable puntuado contra estadísticas de la simulación real vía KL y distancia tipo-Levenshtein. Es el paper de los cuatro más cercano en esta pieza específica.
- **Bifurcaciones apareadas del mismo episodio cambiando UNA condición**: parcial — tienen el contraste full-vs-half-data (§3.2) que es apareado y cambia una sola condición, pero no bifurcan desde un punto congelado idéntico de conversación con un fork; son corridas independientes con distinta composición de datos de entrenamiento, no el mismo prefijo congelado.
- **Evidencia con valor probatorio cuantificado (KL/likelihood)**: usan KL, pero como MÉTRICA DE SALIDA (qué tan cerca está el modelo descubierto de la verdad), no como propiedad de la EVIDENCIA que se inyecta para forzar una revisión de creencia. No hay manipulación server-side de dosis de evidencia.
- **Trabajo propio acumulado**: no existe la noción de que el agente tenga un modelo previo propio en el que invirtió y deba decidir si lo abandona; cada corrida es de cero.
- **Fricción de revisión**: no existe — no hay noción de "reabrir" nada, cada run es una sesión de descubrimiento nueva.
- **Casos cambiar/conservar/parcial**: no aplica — no hay una decisión explícita de revisar una creencia previa frente a evidencia nueva; es descubrimiento de modelo desde cero, no actualización.
- **Cero-LLM en el reward**: SÍ — wAUC, MRI, KL₆, DLD son todas métricas cero-LLM computadas contra ground truth del juego.

## Lecciones de diseño para WAGER

- **Copiar**: el patrón de "ocho coordenadas de respuesta" (performance/costo/proceso) y la descomposición canónica alineada a utilidad es un buen modelo para reportar más que un solo número de fracción capturada F — WAGER podría adoptar el hábito de reportar costo (tokens/dólares) junto al delta-S como coordenadas separadas, no solo como nota al margen.
- **Copiar**: el hallazgo "más esfuerzo de razonamiento no mejora la calidad del modelo, solo el costo" es una hipótesis directamente transportable como eje candidato de WAGER (¿el esfuerzo de razonamiento correlaciona con F o con resistencia a actualizar?) — vale la pena citarlo si WAGER decide meter "esfuerzo/effort" como eje.
- **Evitar**: el diseño full-vs-half-data no es un fork conversacional congelado — no sirve de molde de mecánica de bifurcación, solo de idea de contraste apareado a nivel de "qué datos ve el agente".
- **Citar**: útil como precedente de que evaluar "descubrimiento de modelo" agentic con diseño experimental formal (ANOVA/regresión, contrastes ortogonales) es un género reconocido — refuerza la legitimidad metodológica del enfoque de WAGER de tratar brazos como factores experimentales.

## Veredicto

**NOS-COMPITE** (parcial, en una pieza) — es el único de los cuatro papers que puntúa un modelo ejecutable generado por un agente contra verdad oculta con KL, lo cual toca directamente el corazón del scoring de WAGER. Pero no tiene evidencia probatoria cuantificada inyectada para forzar revisión, no tiene trabajo propio previo que deba abandonarse, no tiene fricción de revisión, y su bifurcación apareada es a nivel de dataset de entrenamiento, no de conversación congelada — así que compite en el "cómo puntuar la salida" pero no en la pregunta central de WAGER sobre revisión de creencias bajo evidencia.
