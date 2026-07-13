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
- Pendientes de familia: partir-en-dos, solución-cebada, par Vulcano (specs en cantera).
