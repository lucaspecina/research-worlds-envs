# Lectura completa — BayesBench (arXiv 2606.30850)

"BayesBench: Evaluating LLM Belief Trajectories Under Multi-Turn Evidence Accumulation" — Samanta, Magesh,
Lancewicki, Jain, Yu, Sajda, Hassani, Modi, Jiang, Efroni. Leído completo vía ar5iv (html); el intento previo
por `arxiv.org/html/...` dio 404 y el PDF crudo trajo texto parcial — la versión ar5iv es la fuente de este
documento.

## Qué es

Cuatro entornos, cada uno con su propia noción de "turno" y N:

1. **Estimación bayesiana (moneda)**: el modelo observa T=100 tiradas secuenciales de una moneda con sesgo
   θ ∈ {0.25, 0.5, 0.75} y estima θ turno a turno.
2. **Predicción bayesiana (recomendador)**: el modelo observa T=50 ratings de películas de un usuario de uno
   de K=4 tipos (derivados de MovieLens) y predice el rating de una película no vista.
3. **Predicción con marco latente (juicio social)**: 100 posts de r/AmItheAsshole; el modelo predice el
   veredicto de la comunidad.
4. **Predicción con marco latente (triage médico)**: 100 casos del dataset medical-symptom-triage; el modelo
   predice la urgencia clínica.

Modelos: 7 modelos open-weight instruction-tuned — LLaMA 3 (3B, 8B, 70B) y Qwen 2.5 (3B, 7B, 14B, 32B). Puntúan
con dos métricas contra una referencia bayesiana cerrada (donde existe): Total Variation Distance sobre la
distribución completa y Mean Absolute Error sobre la media posterior. La creencia se elicita con preguntas de
opción múltiple con rotación cíclica de posiciones (cuadrado latino) para cancelar sesgo de posición. La norma
bayesiana: en el entorno moneda, prior Beta(1,1) y posterior cerrada Beta(1+n_h, 1+t-n_h); en el recomendador,
posterior categórica cerrada sobre los K=4 tipos ajustados a MovieLens; en juicio social y triage médico NO hay
forma cerrada — la "verdad" es el veredicto de la comunidad / la etiqueta clínica, no una posterior bayesiana
formal (los autores lo declaran explícitamente, ver abajo).

## Citas verbatim clave

- "Models infer latent structure from accumulating evidence, and scaling strengthens this inference." (resultado central, latent inference)
- "Better latent inference does not yet translate into calibrated downstream prediction." (el gap central del paper)
- "Larger models can over-update in the coin task, pushing predictions toward the extremes when the Bayesian reference remains more moderate." (sobre-actualización en modelos grandes)
- "Active engagement reveals a persistent pro-user bias relative to passive observation of the same evidence." (sesgo pro-usuario cuando el modelo participa activamente vs. observa)
- "The recurring pattern is an alignment gap between latent inference and downstream prediction: models can identify relevant hidden structure, but cannot yet reliably translate that inference into calibrated later predictions."
- "Active engagement significantly lowers final-turn p(true tier) for five of seven models, with paired passive-minus-active gaps from +0.054 to +0.173" (Tabla 7, triage médico)

## Números principales

- Recomendador (TVD tipo-posterior, escala 0–100): LLaMA-3B 61.4±0.8 vs. LLaMA-70B 45.4±3.7 (mejora con
  escala) — pero la TVD sobre la predicción de RATING (lo downstream) NO mejora consistentemente con escala:
  rango 28.1–65.7 en la Tabla 1, y modelos grandes a veces degradan.
- Triage médico: modelos grandes llegan a ~0.80 de probabilidad en el perfil de comunicación verdadero a mitad
  de conversación; casos de emergencia identificados con fiabilidad (~1.00); etiquetas de urgencia media
  empujadas a los extremos.
- Juicio social: el engagement activo aumenta consistentemente el error en casos "YTA"; solo Qwen-14B y
  Qwen-32B muestran cambios de ≈2–3 errores estándar; contra-concesión 6–20% en estilos conciliadores vs. ≤5%
  en otros estilos.
- Moneda: modelos grandes se mueven en la dirección alineada con la evidencia pero sobrepasan con frecuencia
  la referencia bayesiana, empujando hacia 0/1 cuando la referencia permanece moderada.

## Qué les falta respecto de WAGER

- **Sin consecuencia cobrada contra verdad oculta de un mundo ejecutable**: en 2 de 4 entornos (moneda,
  recomendador) hay posterior cerrada, pero se puntúa la CREENCIA ELICITADA (una respuesta de opción múltiple
  o media posterior), no un artefacto ejecutable que se corre contra casos ocultos. En los otros 2 entornos
  (juicio social, triage) NO hay oráculo bayesiano formal en absoluto — es accuracy contra etiqueta humana/
  clínica, mezclando "¿acertó el veredicto?" con "¿actualizó proporcionalmente a la evidencia?".
- **Sin trabajo propio acumulado ni fricción de revisión**: el modelo observa evidencia y reporta una
  creencia; no hay ningún artefacto previo propio que deba reabrir, ni costo de revisar. Es la esquina de
  carga cero que en WAGER es un extremo del mapa, no el mapa completo.
- **Sin bifurcación apareada del mismo episodio congelado**: cada trial es independiente; no hay control
  contrafáctico "mismo episodio, misma evidencia, con/sin manipulación X" que aísle causalmente el efecto de
  un factor (autoría, compromiso, etc.).
- **Cero-LLM roto en la construcción**: el dataset de triage médico y juicio social usa etiquetas humanas
  reales (community verdicts, clinical labels) sin cuantificar el valor probatorio de la evidencia dosificado
  — no hay control de "dosis" de evidencia como en nuestro CLEAN/MIXED/PLACEBO.
- El paper mismo admite: "MCQ probes likewise provide an elicited distribution rather than a direct readout
  of internal belief" — igual que nuestra preocupación de que lo DICHO no es lo ENTREGADO; a diferencia de
  WAGER, ellos se quedan en lo dicho (excepto quizás en el recomendador, donde el rating predicho SÍ es un
  producto verificable, pero no ejecutable/acumulativo).

## Lecciones de diseño para WAGER

- **Definición de norma/oráculo**: usan forma cerrada exacta (posterior conjugada Beta, o mezcla categórica
  ajustada a datos reales de MovieLens) SOLO donde el mundo lo permite, y declaran explícitamente que en los
  otros dos entornos no hay tal oráculo — no fuerzan una pseudo-norma. Lección: declarar sin pudor cuándo el
  oráculo legal es exacto vs. aproximado, en vez de maquillar.
- **Cómo separan sub/sobre-actualización**: comparan el TVD/MAE del modelo contra la referencia bayesiana en
  cada turno, y ven la DIRECCIÓN del error (empuja hacia extremos = sobre-actualización; se queda plano =
  sub-actualización) — es una lectura cualitativa de la curva, no una métrica única con signo. WAGER con F
  (fracción de mejora legal capturada) sí tiene signo/magnitud en una sola métrica, lo cual es más fuerte para
  comparar celdas del mapa de carga.
- **El hallazgo del "alignment gap"** (infiere bien la estructura latente pero no la traduce a predicción
  calibrada) es un separador fino que WAGER no tiene explícito: F mide la traducción de evidencia a resultado
  ejecutable, pero no distingue si el fallo fue en la INFERENCIA de la estructura latente vs. en el USO de esa
  inferencia para el artefacto final. Podría ser un eje de diagnóstico adicional (¿el modelo "sabe" pero no
  "aplica"?) útil para diagnosticar por qué F es bajo en una celda dada.
- **Objeción que le harían a F/regret**: BayesBench separaría TVD/MAE en cada turno intermedio, no solo al
  final — permite ver SI la sub-captura de evidencia (F bajo) es un fenómeno del primer turno (anclaje inicial)
  o se acumula/empeora turno a turno. F como estadístico agregado del episodio completo podría esconder una
  trayectoria de deterioro (sube y luego cae) que una serie temporal de TVD por turno revelaría. Sugerencia:
  reportar F también por punto de inyección dentro del episodio, no solo al cierre.
- El control "active engagement vs. passive observation" (el modelo PARTICIPA en la conversación vs. solo
  observa el mismo log) es directamente análogo a nuestro eje AUTHOR_ROLE self/peer — confirma
  independientemente que la autoría/participación activa introduce sesgo pro-uno-mismo medible incluso sin
  compromiso previo (draft), lo cual es congruente con nuestro hallazgo de que H1/H2 solos (autoría atribuida)
  dan señal plana — BayesBench lo ve con OTRA operacionalización (activo vs. pasivo) y SÍ encuentra sesgo, lo
  que sugiere revisar si nuestra manipulación de autoría fue demasiado débil/atribuida en vez de vivida.

## Veredicto

NOS-VALIDA (parcial) + insumo de diseño — confirma independientemente, con otra metodología (multi-modelo,
multi-dominio, forma cerrada donde es posible), que hay un gap sistemático entre inferir estructura latente y
usarla para predicción calibrada, y que la participación activa sesga la actualización; pero no compite con
WAGER en rigor causal (sin bifurcación apareada, sin trabajo propio, sin dosis cuantificada de evidencia) ni
en fidelidad a "lo entregado" (se queda en creencia elicitada, no artefacto ejecutable puntuado contra verdad
oculta).
