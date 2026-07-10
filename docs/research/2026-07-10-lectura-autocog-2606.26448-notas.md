# NOTAS — AUTOCOG (2606.26448, Princeton/Griffiths+Daw) — LEÍDO COMPLETO 2026-07-10 (pymupdf)

## Qué es
"AUTOmated COGnitive Scientist": loop cerrado 100% autónomo — diseño experimental adversarial →
recolección de datos (HUMANOS reales vía Prolific, N=25/experimento, US$0.80) → análisis/arbitraje →
revisión de teoría. 2 slots de teorías COMPITIENDO (agentes-abogados). Gemini-3.1-pro, temp 0.7.

## Citas clave (verbatim)
- Teorías ejecutables: "each expressed as an executable cognitive model... a generate function
  mapping parameters/stimulus/history to choice probabilities, a policy, and parameter ranges".
- Scoring GENERATIVO sin fitting: "It relies on generative behavior to compare theories, rather than
  fitting models to observed behavior, as it is faster and less likely to overfit".
- Auto-verificación: "It is self-verifying: every proposal, whether an experiment or a theory, is
  verified against its own predictions before it observes any actual data". Experimentos aceptados
  solo si simulación forward los muestra DISCRIMINANTES al N planeado (Welch, α=.01).
- Avance por unificación: "a candidate theory progresses between cycles only by capturing ALL the
  behavior collected so far rather than being tuned to one dataset".
- Resultado estrella: teoría NUEVA (Diminishing Returns WADD — sensibilidad decreciente al valor de
  los cues, utilidad cóncava) CONFIRMADA en estudio PRE-REGISTRADO con participantes nuevos
  (H1 p=5.6e-4; H2 p=3e-5; H3 p=.036). "the regularity is a new and confirmed fact about how people
  decide... echoes prospect theory".
- Control anti-apofenia: "when given pure noise it converged on theories equivalent to random
  guessing rather than imposing structure on it" (→ fixture negativo para nuestra fábrica).
- Recupera estrategias NO-canónicas (anti-majority, take-the-worst...) → "its discoveries are
  ultimately driven by the data rather than strictly bound by the priors of the underlying LLMs"
  (las raras necesitan 20 ciclos en vez de 5).
- Límite admitido: "The loop verifies that each synthesized model compiles and predicts the data,
  but not that its code faithfully realizes the verbal theory it is paired with, a verbal-to-formal
  translation problem the field is yet to solve".

## Los CONTROLES (lo más valioso para "cómo construir mundos")
1. **Métrica adaptativa vs distancia FIJA (JSD)** — la distancia fija FALLÓ en recuperar
   perseveración (0/3) y take-the-worst (0/3); la métrica propuesta-por-LLM: 3/3 y 2/3. CITA ORO:
   *"fixing an explicit distance fixes in advance which behavioral differences count as evidence:
   theories that differ only in ways the chosen distribution cannot express are indistinguishable to
   the pipeline, and therefore earn no selection pressure."* → nuestro red-team #5 (puntos ciegos de
   D) dicho desde el otro lado. Aceptan métricas solo si el contraste es grande EN MEDIA y ESTABLE
   POR-SUJETO (la varianza entre-sujetos como criterio de admisión).
2. **Diseño LLM vs RANDOM**: random solo recupera TTB; las no-canónicas necesitan diseño OPTIMIZADO
   para separar → la batería no puede ser random puro.
3. **Framing adversarial vs neutral**: empatan en separación promedio, pero solo el adversarial
   recuperó perseveración (3/3 vs 0/3) → la ADVOCACÍA (agentes con stake) encuentra estructuras que
   la neutralidad no.

## Relevancia WAGER
1. VALIDACIÓN EXTERNA de nuestro formato exacto (entrega=modelo generativo, evaluación comportamental
   sin fitting, generalización held-out como criterio) — top-lab, loop cerrado en HUMANOS, hallazgo
   nuevo confirmado pre-registro.
2. INVERSO COMPLEMENTARIO: ellos descubren teorías DEL agente (humano); nosotros hacemos que agentes
   descubran MUNDOS. Misma maquinaria, dirección opuesta.
3. Recetas de construcción: "experimento aceptado solo si la simulación lo muestra discriminante" =
   frontera descubrible mecanizada (OQ 18) + diseño de batería; control de ruido puro (no inventa
   estructura) = fixture negativo/mundo-nulo a adoptar; dos-slots adversariales = patrón del
   proto-designer difícil.
4. Presupuestos: ≤3 experimentos/agente, ≤4 métricas/experimento, ≤10 iteraciones de crítica.
   Accept-gate programático (el gate decide qué queda, no el LLM).
