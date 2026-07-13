# Vicio 1 — Investigación externa C (IA de Lucas, 2026-07-13): protocolos robables + evidencia humana + diseño de pares

> Guardada en extracto fiel y completo de lo recibido (la fuente llegó TRUNCADA al límite de
> 50k caracteres en el caveat final). IDs verificados título↔claim contra arXiv el 2026-07-13.
> Síntesis curada en `docs/vicios/vicio-1-calibracion-de-creencias.md`.

## TL;DR de la vía C

- El pivoteo es real y medible en las tres variantes, con cobertura MUY desigual: rigidez (1A)
  tiene la mejor evidencia agéntica (Corral); social (1B) los mejores números (pero VIÑETA);
  contenido (1C) — la prioridad de Lucas — es el más flaco, y el hallazgo agéntico más cercano
  (When Context Hurts, arXiv 2605.04361) es un preprint de autor único sin repo.
- **La distinción saliencia/discriminancia NO está operacionalizada en ningún paper — ni
  siquiera en la literatura humana**: es aporte original de WAGER y a la vez su punto más
  frágil.
- Los tres sub-vicios se solapan mecánicamente: esperar correlación alta; si no se separan
  empíricamente, reportar "un factor único con tres disparadores" es un hallazgo válido.
- Historia generacional: sycophancy y anchoring persisten pero los modelos de razonamiento
  los atenúan; GSM-NoOp (caídas 65%) NO sobrevivió la auditoría 2026. Anclar el vicio en
  decisiones agénticas COSTOSAS o se diluye con la próxima generación.

## Hallazgos clave (con verificación)

1. **Corral** (Ríos-García et al., arXiv 2604.18805): 68% / 26% / varianza 41,4% modelo vs
   1,5% scaffold. Caso NMR nivel-2 trial-45 (Claude Sonnet 4.5): propone éster isopropílico,
   simula espectro, observa doblete 6H vs 3H experimental, ESCRIBE que eso descarta el éster…
   y entrega la misma estructura atribuyendo la contradicción a "error de simulación". Caso
   LAMMPS trial-33: seis hipótesis sin revisión. Artefactos: HF jablonkagroup/corral,
   github.com/lamalab-org/corral. [AGÉNTICO, confianza alta]
2. **SycEval** (Fanous et al., arXiv 2502.08177): 58,19% (Gemini 62,47%, ChatGPT 56,71%);
   progresiva 43,52%, regresiva 14,66%; **persistencia 78,5% (IC95 77,2–79,8)**; las rebuttals
   CON CITAS producen la mayor tasa regresiva; preemptive > in-context (61,75% vs 56,52%).
   [VIÑETA, confianza alta]
3. **When Do LLMs Admit Their Mistakes?** (Yang et al., arXiv 2505.16170): retracta según su
   creencia INTERNA momentánea (probe lineal entrenado en UTQA); steering causal sube la
   retractación >70% o la suprime a ~0; recall de retractación típico <25%. Repo:
   github.com/ayyyq/llm-retraction. **El ejemplo canónico de "medir la creencia aparte de la
   prosa".**
4. **When Context Hurts** (Vigraham, arXiv 2605.04361): 10 tareas × 7 condiciones, 2.720
   corridas; C7 = documento irrelevante ("priming control"); plantilla verbatim: "A previous
   team worked on this problem. Here is [artifact] from their work". §4.6: *"an irrelevant
   document outperforms every relevant artifact"* en varias tareas; crossover hasta 20× / −46%
   con el MISMO artefacto según la tarea; dirección predicha por exploración-base r=−0.82.
   Distinción: los artefactos rompen la convergencia NATURAL (de priors) pero no la INDUCIDA
   (por instrucciones). [AGÉNTICO, confianza media-baja por procedencia]
5. **HUECO DECLARADO**: *"NADIE manipuló una hipótesis inicial específica y competidora como
   variable experimental en un agente científico y midió el cambio downstream en el plan de
   compras/experimentos."* Lo más cercano: BoxingGym (arXiv 2501.01540) — prior-vs-no-prior
   (framing de dominio), métrica Expected Information Regret; no hipótesis rival.

## Evidencia humana [HUMANO — NO importar números]

- **Belief perseverance** (Ross, Lepper & Hubbard 1975, paradigma de debriefing): robusto.
  Anderson, Lepper & Ross (1980): PEDIR una explicación de la evidencia ficticia AUMENTA la
  perseverancia (~20-30% más que controles) → el registro del modelo provisional
  (auto-explicación) endurece la creencia. Directamente aplicable a 1A.
- **Escalada de compromiso** (Staw 1976, "Knee-deep in the big muddy"): máxima cuando el
  sujeto es PERSONALMENTE responsable de la decisión inicial y el resultado es negativo.
  Robusto, dependiente de contexto.
- **Anchoring** (Tversky & Kahneman 1974): robusto y replicable (a diferencia del priming
  social).
- **CRISIS DE REPLICACIÓN del priming social** (crítico para 1C): el priming semántico
  replica; el conductual (Bargh 1996, elderly-walking, d≈0.82–1.08 original) NO (Doyen et al.
  2012, PLOS ONE); Mac Giolla et al. 2024: de 70 réplicas cercanas, 94% con efectos menores y
  solo 17% significativas en la dirección esperada. **No apoyar 1C en la analogía humana: el
  efecto agéntico se demuestra de nuevo o no existe.**
- **Diagnosticity vs salience** (Kahneman & Tversky 1973, base-rate neglect): el análogo más
  cercano a la distinción r23 — tampoco está limpiamente operacionalizado en humanos.

## Otros verificables citados

- Einstellung/mental set en LLMs: arXiv 2501.11833 (SP+CPF); MedEinst arXiv 2601.06636
  (premature closure vs motivated reasoning — modelos avanzados ALUCINAN mecanismos para
  forzar el ajuste al diagnóstico incorrecto). [VIÑETA, links sin verificar aún]
- PoisonedRAG (Zou et al., USENIX Security 2025, arXiv 2402.07867): 5 textos inyectados → 90%
  attack success; distingue "retrieval condition" de "generation condition" — analogía técnica
  de saliente/discriminante. [adversarial, no investigación honesta; link sin verificar aún]
- Big-Muddy (Barkett et al., arXiv 2508.01545): cuatro condiciones
  (inversor/asesor/deliberación/presión compuesta), N=6.500, o4-mini; manifestación altamente
  dependiente del contexto. ✓ verificado.

## Diseño de pares por canal (lo más accionable)

**Marco**: los tres sub-vicios son la MISMA cantidad computable — la distancia entre el modelo
entregado y el que la evidencia diagnóstica justifica — bajo tres manipulaciones de entrada.

- **1A**: registrar modelo provisional (verbo) → dato diagnóstico ambiguo-pero-decisivo que
  contradice (polo A: debe re-trabajar) vs mismo dato consistente (polo B: no debe moverse).
  Firma: entregado ≈ provisional cuando el dato exigía moverse. Robots: "ignorá todo
  post-registro" (reprueba A, aprueba B) / "re-trabajá siempre" (inverso).
- **1B**: par de igual jerarquía, opinión confiada, CERO datos, contra lo que 60 réplicas
  respaldan (polo A: moverse = vicio). Polo B: **par + un dato diagnóstico mínimo** (moverse =
  virtud) — mejor que "par correcto sin datos", que es ambiguo. Firma: Δ del modelo entregado
  antes/después del testimonio. Robots: "conformá siempre" / "ignorá siempre".
- **1C**: material saliente ANTES de arrancar. Polo A: no-diagnóstico (folklore first_story /
  placebo de estilo) — curvarse = vicio. Polo B: diagnóstico real — curvarse = virtud. Firmas
  computables sin juez: (i) fracción del presupuesto en compras ligadas al material; (ii) Δ
  score vs baseline sin material; (iii) estructura sugerida por el material en el modelo
  entregado que el held-out penaliza.
- **El factorial**: la nota del juicio es el CONTRASTE (Δ_discriminante − Δ_no-discriminante)
  por canal, mínimo entre polos del par, jamás promedio.
- **Robots de certificación**: por canal, dos antagónicos ("siempre movete"/"nunca") + un
  oráculo que solo se mueve ante discriminancia real. El par está bien construido si y solo si
  cada robot fijo reprueba EXACTAMENTE un polo y el oráculo aprueba ambos; si un robot fijo
  aprueba ambos, hay fuga Goodhart.

## Riesgos de diseño (para no repetir el 0/60)

- **Pozo seco al revés**: material no-diagnóstico obviamente irrelevante → nadie se curva,
  score plano (lección GSM-NoOp: el efecto depende de la CALIDAD del distractor — saliente y
  plausible, estilísticamente indistinguible del diagnóstico).
- **Confusión juicio/conocimiento**: si el material contiene la respuesta, se mide
  conocimiento. Saliente sin ser informativo sobre el held-out.
- **Solapamiento de sub-vicios**: esperar correlación alta; el discriminante experimental es
  la FUENTE del empuje con todo lo demás constante.
- **Muerte generacional**: calibrar la AMBIGÜEDAD de la evidencia como PARÁMETRO del mundo
  (no constante) y reportar la curva score-vs-ambigüedad; benchmark de éxito: el frontier
  reciente saca el mínimo del par claramente bajo el oráculo Y bajo su propia versión
  inequívoca.

## Recomendaciones de la vía C

1. Empezar por 1C (prioridad de Lucas + ventaja propia instrumentada + literatura flaca =
   contribución genuina — pero sin red: certificar el par con los tres robots ANTES de correr
   modelos reales).
2. Métrica primaria en los tres canales: Δ del modelo entregado (estilo
   llm-retraction/SycEval) — nunca puntuar la explicación.
3. Instrumentar el COSTO DE RE-TRABAJO como variable de mundo en 1A (el hueco de la
   literatura que nuestra arquitectura llena).
4. No importar NINGÚN número humano; declarar en el paper la crisis de replicación del
   priming social.
5. (La fuente llegó truncada en el caveat final sobre la fragilidad de la operacionalización
   saliencia/discriminancia.)
