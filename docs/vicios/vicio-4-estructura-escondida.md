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
- **Perfiles persistentes (2026-08-13)** `[VERIFICADO propio][AGÉNTICO]` — primer anfitrión
  diseñado después del freno de la paga: una sola banda queda en `S_profile=0.464`, mientras
  dos perfiles aprendidos llegan a `.924–.997`. Con la idea nombrada `gpt-5.4` construyó el
  salto 2/3. En la tanda sin ayuda (`gpt-5.4 × mundo × n=10`), **1/10** cruzó funcionalmente
  remuestreando perfiles completos, **0/10** entregó el modelo compacto de dos tipos y 9/10
  entregaron una sola Gaussiana. La auditoría sobre las 400 filas exactas de cada partida da
  `Delta BIC=705–795` y `S=.943–.999` para dos perfiles: no es la falla de incentivos de D1 ni
  falta de señal. [Ficha y resultado](../research/2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md).
- **count_regime_v0 + gemelo (mundo 2, 2026-08-07; constructo CORREGIDO por Lucas la misma
  noche)** `[VERIFICADO propio][AGÉNTICO]` — segundo operador construido (régimen/quiebre
  oculto), certificado verde y con R que premia el descubrimiento. **OJO: la v0 NO mide este
  vicio (generación)** — el escalón grita en las tablas de todos, la evidencia DICTA el
  candidato, y la falla observada es de ACEPTACIÓN: lo generan y lo matan ("outlier", "ruido",
  interpolar-sin-ley). Esa evidencia vive en su casa canónica:
  [vicio-1 §1.A rigidez](vicio-1-calibracion-de-creencias.md). El 2/5 de aceptación NO es
  comparable con el 0/9 de generación de count_mix. **La creatividad del operador régimen queda
  SIN medir hasta la versión con quiebre no-flagrante** (señal chica vs ruido / firma en forma
  / umbral fuera del muestreo racional) — diseño pendiente para Codex. Positivo nuevo: zoom
  adaptativo de compra en los que aceptan (conjetura antes del zoom).
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
- **Perfiles persistentes (2026-08-13)**: anfitrión validado y tanda `gpt-5.4 × n=10` cerrada;
  confirma la retirada a una sola campana aun con premio grande y evidencia exacta suficiente.
  Estado: replicar fuera del modelo/anfitrión, sin tuning local.
- **count_regime_v0/twin (2026-08-07)**: tercera familia CONSTRUIDA (operador régimen) —
  certificación verde con R direccional (+1.0: primera familia donde R premia el salto, A2 por
  construcción); 13 episodios v0. Constructo corregido: la v0 dicta el candidato → midió
  ACEPTACIÓN (evidencia en vicio-1 §1.A), no generación; la celda de CREATIVIDAD del operador
  régimen en la matriz sigue vacía hasta la versión con quiebre no-flagrante.
- **count_regime_v1 rung 0 (2026-08-10)** `[VERIFICADO propio][AGÉNTICO]`: la CONDICIÓN que
  enciende la postulación — el mismo gpt-5.4 que da 0/9 sin fallo entrega la familia de dos
  leyes **30/30 con el fallo del propio modelo a la vista** (impasse operativo: M0 → piloto →
  parche); más detalle de reporte NO ayuda (H-V1 invertida: RAW 5/10 > estructurado 3/10).
  Consistente con Ohlsson (sin impasse no hay reestructuración); confound declarado: el
  encargo planta la sospecha (menciones en turnos 1-5). Estado: VIVO/CONDICIONAL (condicional
  al gatillo de fallo). [Resultado](../research/2026-08-10-resultado-tanda-count-regime-impasse-v1.md).
- **Par D1 calibración (2026-08-10)** `[VERIFICADO propio][AGÉNTICO]` — **la versión más
  incriminante de 4.3 hasta ahora, y aísla el eslabón**: con la horquilla desplegada (K=2),
  30/30 compran evidencia discriminante (el "no pagan el test" de Dunbar NO se reproduce) y
  la auditoría cero-LLM muestra que en 14/15 la mezcla ganaba claro (ΔBIC≥10+CV) **sobre los
  datos que el propio agente compró** — y aun así 13/15 entregan gaussiana unimodal con la
  subpoblación horneada en la varianza (skew −0.04 vs −0.97 de la verdad). Y=1/15 donde la
  verdad exige AGREGAR estructura vs 9/15 donde el default es la verdad (McNemar 8:0). No es
  "no lo ven" (sus datos lo gritan): es la retirada a lo familiar EN LA ENTREGA — convergencia
  con 8.6. Titular defendible (Codex): "tras comprar evidencia que favorece causa material,
  gpt-5.4 comprime sistemáticamente la subpoblación en una entrega unimodal". Estado: VIVO como HECHO conductual; ⚠️ ATRIBUCIÓN BAJADA (2026-08-10, freno de Lucas
  confirmado con números): la vara continua pagaba el salto 0.014 (mejor campana sin
  estructura S=0.986) y el episodio no cobraba nada → "vicio" confundido con indiferencia
  racional; titular vigente: "eligió sustituto unimodal cuando la estructura apenas pagaba y
  sin consecuencias visibles". Programa nuevo: la paga del salto como dial certificado
  (CRPS + headroom vs mejor-rival-sin-estructura + visibilidad). Ronda 2 (wording neutral de Lucas, mismas seeds,
  reglas congeladas): escriben 1/15, espurio 1/15, apareo sin rescate — el rival "no les
  avisaron" REFUTADO; y la frase DUPLICÓ la compra de evidencia sin mover la escritura
  (disociación esfuerzo-de-compra vs compromiso-de-entrega). Confirmación fuera de D1
  pendiente (instancia fresca, gpt-5.4 + DeepSeek-V3.2, espera GO). [Dossier](../research/2026-08-10-resultado-tanda-d1-calibracion.md).
- Pendientes de familia: partir-en-dos, solución-cebada, par Vulcano (specs en cantera).
