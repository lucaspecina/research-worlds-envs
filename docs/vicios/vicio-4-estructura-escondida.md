# Vicio 4 — No postular la estructura escondida / retirarse a lo familiar

> Etiquetas y marco: ver [README](README.md). Estado WAGER: latent_mix v2 = el trofeo de la casa
> (0/10 promovieron la anomalía a composición oculta; techo 0.096). **VIVO en frontier agéntico
> — validación externa nueva y fuerte (DiscoverPhysics).**

**Qué es (paraguas).** La explicación correcta requiere postular algo NO observado (una entidad,
una mezcla, una geometría) y el agente se queda en el menú familiar: ajusta curvas, parcha
parámetros, promedia.

## Sub-formas

### 4.1 Fallo en descubrir estructura latente — VIVO en frontier agéntico
- **Casos**: DiscoverPhysics ([arXiv 2605.26087](https://arxiv.org/abs/2605.26087))
  `[VERIFICADO][AGÉNTICO]` (LEÍDO 2026-07-13; extracción en lectura-de-fuentes) — 22 mundos de
  física alterada con ley OCULTA (simulador N-body; el agente compra trayectorias con
  presupuesto de rondas y entrega explicación + la ley como función Python; MSE en held-out +
  juez-LLM para la explicación): los mejores frontier pasan la mitad (Opus 4.7 pass@5 50.0 ·
  GPT-5.5 36.4 · **gpt-5.4 4.5**) y *"fail to solve the more difficult worlds, which are
  characterized by important latent structure (three particle species, dark matter, extra
  dimensions)"*; predicción y comprensión se DESACOPLAN — *"fitting the data well without
  necessarily understanding it"* (gpt-5.5 logra el mejor MSE sin la mejor explicación, por
  *"lock in a candidate law early and refine its parameters rather than revise its conceptual
  picture"* — el vicio 1 dentro del benchmark del vicio 4). Nuestro trofeo `[VERIFICADO propio]`: 0/10
  postulan la mezcla; el genérico sin-mezcla no cierra la brecha. OSWorld estado-oculto
  `[VERIFICADO]` (inferir lo latente es juicio — el propio benchmark de operación lo dice).
- **count_mix_v0 + gemelo (nuestra mesa, 2026-08-07)** `[VERIFICADO propio][AGÉNTICO]` — primer
  mundo del programa de saltos (mezcla discreta de dos tasas por lote; gemelo continuo apareado
  por media): **0/9 episodios espontáneos postulan los grupos** (gpt-5.4 y DeepSeek-V3.2, encargo
  v0.2 corregido tras la auditoría de incentivos); todos entregan frailty gamma continua —
  capturan la persistencia por lote (ICC≈verdad) sin la discretitud (valle≈0 contra el rival
  fuerte). Gemelo limpio (0/10 espurio) y compra del experimento discriminante casi universal
  (11/12): la pieza ausente es la HIPÓTESIS y su test, no el shopping. Con ayudas, la variable
  activa es el CANAL de la pista × modelo, no su fuerza (evidencia en vicio-1 §1.C y vicio-9).
  [Resultado](../research/2026-08-07-resultado-smoke-count-mix-v0.md) ·
  [auditoría](../research/2026-08-07-auditoria-critica-slice-count-mix.md) ·
  [autopsia de canales](../research/2026-08-07-autopsia-canales-de-ayuda.md).
- **count_regime_v0 + gemelo (mundo 2, 2026-08-07)** `[VERIFICADO propio][AGÉNTICO]` — segundo
  operador medido (régimen/quiebre oculto): **el vicio generaliza pero con TASA distinta** —
  salto espontáneo 2/5 válidas (parcial, ~0.65) vs 0/9 en count_mix; la distancia-al-menú
  depende del operador. Espécimen nuevo de la juntura: DeepSeek 99502 ve la anomalía, compra
  MÁS datos del punto anómalo, confirma, escribe *"Perhaps a piecewise linear… two segments?
  But given the limited data, I'll go back to the exponential form"* y entrega la suave
  llamando "outlier" al punto que sabe real — el candidato entró al menú por sus propios medios
  y lo mató el filtro sin test (cruza con vicio-1 rigidez y vicio-9). gpt técnico: *"I suspect
  the historical sample was noisy… not that the process is discontinuous"* — la discontinuidad
  re-etiquetada como ruido. Gemelo 0/6 espurio; los que saltan hacen zoom adaptativo de compra
  (conjetura ANTES del zoom en traza).
  [Resultado](../research/2026-08-07-resultado-smoke-count-regime-v0.md) ·
  [ficha](../research/2026-08-07-ficha-mundo-count-regime-v0.md).
- **Es la celda del catálogo donde la evidencia externa ya nos esperaba** — y donde el par
  Neptuno/Vulcano (postular-entidad ↔ parchar) tiene además el respaldo del position paper
  "LLMs can't jump" `[VERIFICADO]` (usa literalmente el ejemplo Vulcano).

### 4.2 Topología de razonamiento que no se adapta a la demanda epistémica
- Corral `[POR-LEER el detalle]`: la estructura del razonamiento es IDÉNTICA trabaje en
  workflow o en inferencia de hipótesis — no cambia de modo cuando la tarea exige postular.

### 4.3 Retirada a curve-fitting / a lo familiar
- BoxingGym `[POR-LEER][AGÉNTICO]` (falla en model discovery; el modelo estadístico explícito
  no ayuda confiable); vibe-physics `[VERIFICADO]` (*"revierte a convenciones de manual"*);
  Trehan `[VERIFICADO]` (reescribe a Actor-Critic — el default del training — racionalizándolo).
- Einstellung clínico `[POR-LEER][VIÑETA]`: **MURIÓ entre generaciones** (mARC 2025 → follow-up
  [2601.11866](https://arxiv.org/abs/2601.11866): los de razonamiento alcanzan nivel humano). Lección generacional: las sub-formas
  de viñeta evaporan; las agénticas-latentes persisten.

### 4.4 El gemelo del aha de síntesis: integrar-como-reflejo
- Chen/Zhao/Cohan `[VERIFICADO]`: los LLMs sobre-producen "conectá dos cosas" (bridge 47-64% vs
  12% humano; integrate 34.2% vs 2.35%) y evitan replace/decouple/formalize; el thinking lo
  EMPEORA. El reflejo "siempre uní" gana el polo-aha y debe perder el gemelo (apofenia de
  ideación). Par ya doctrinado.

## Estado en WAGER y diseño
- El trofeo valida; DiscoverPhysics obliga a diferenciarnos: **ellos LLM-judge, nosotros
  cero-LLM** — el claim de novedad del paper.
- **count_mix_v0/twin (2026-08-07)**: segunda familia MEDIDA del vicio — certificada 19/19,
  28 episodios v0.2, fenómeno replicado con el encargo justo (0/9); la escalera de ayudas
  además LOCALIZA dónde muere la hipótesis regalada por modelo (canales, no dosis).
- **count_regime_v0/twin (2026-08-07)**: tercera familia MEDIDA (operador régimen) —
  certificación verde con R direccional (+1.0: primera familia donde R premia el salto, A2 por
  construcción); 13 episodios v0; el vicio generaliza con tasa menor (2/5 parcial vs 0/9) →
  la matriz saltos×realismo tiene su segunda celda y la variable distancia-al-menú.
- Pendientes de familia: partir-en-dos, solución-cebada, par Vulcano (specs en cantera).
