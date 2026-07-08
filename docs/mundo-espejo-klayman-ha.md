# Mundo espejo Klayman-Ha (estructuras 1a/1b del vicio "no actualizar")

> **Spec de diseño** (spec-first, precede al código). Primer build estructural elegido del ★ Mapa
> de estructuras por vicio (`docs/failure-modes.md` §4, ADR 0104). Es el PAR: dos mundos que
> comparten mecanismo y solo invierten la geometría — la demostración viva del principio 9
> (diversidad de estructuras ⇒ no se puede overfitear con un atajo).

## 0. El punto (por qué este par primero)

Estructura **1a** (hipótesis demasiado ESTRECHA) y su **espejo 1b** (demasiado AMPLIA) son el
vicio "no actualizar / confirmation bias" en su forma geométrica pura (Klayman & Ha 1987, sobre el
2-4-6 de Wason). Lo valioso: **un modelo que memorice una regla fija de exploración gana uno y
PIERDE el otro.**

| Política fija del agente | 1a (H estrecha) | 1b (H amplia) |
|---|---|---|
| "siempre testear donde ESPERO el efecto" (positive test) | **PIERDE** | GANA |
| "siempre testear donde NO espero (buscar refutar)" | GANA | **PIERDE** |
| adaptativa: ¿mi H es angosta o ancha? pruebo el borde correcto | GANA | GANA |

Solo el juicio (sospechar de qué lado falla tu hipótesis y probar ese borde) gana los dos. Por eso
el par, junto, mide juicio y no un truco memorizado.

## 1. El mecanismo (un SCM de intervalo — del catálogo, no inventado)

Control 1-D `x ∈ [0,10]` (una perilla settable, como `dose` en `dummy_dose_v0`). El efecto vive en
un intervalo verdadero `T = [t_lo, t_hi]`:

```
y := effect_amp * 1[t_lo <= x <= t_hi] + noise      # el "efecto" solo ocurre dentro de T
```

`PARAMS = {t_lo, t_hi, effect_amp, noise_sd}`. `sample(regime,n,seed)` corre esto (la verdad, el
ancla S_truth). Idéntico patrón a `dummy_dose_v0`: `mechanism(PARAMS, regime, n, seed)` → tabla
`[x, y]`; `model = sample`.

**Las dos instancias (mismo motor, geometría invertida):**
- **1a — H demasiado estrecha**: verdad `T=[2,10]`; la piel hace que el naive espere `H=[6,10]`
  (el efecto "solo se activa alto"). El efecto TAMBIÉN está en `[2,6)`, invisible si solo testeás
  alto. Escape: testear BAJO.
- **1b — H demasiado amplia**: verdad `T=[6,10]`; la piel hace que el naive espere `H=[2,10]`
  (el efecto "arranca temprano"). En `[2,6)` NO hay efecto. Escape: testear donde esperás efecto
  (positive) y chocarte con que `[2,6)` no responde.

## 2. Superficie de control + entregable + scoring (cero-LLM)

- **Superficie**: `x` settable en `[0,10]` (comprás una query = corrés el mundo en el `x` elegido y
  ves `y`). Presupuesto ESCASO (§4).
- **Entregable**: un `model(regime,n,seed)` que prediga `y` sobre una grilla held-out de `x`. Igual
  que todos: se puntúa corriendo submission vs `world.py` (S_truth) vs ancla naive, sobre la
  batería. **Cero LLM en el reward.**
- **Batería**: pesa la región de desacuerdo `T △ H` (en 1a: `[2,6)`; en 1b: `[2,6)` de nuevo, pero
  ahí la verdad es "sin efecto"). Ahí es donde el vicio se cobra.
- **Anclas**: **naive = predecir H** (la corazonada de la piel — la jugada del vicioso). **Techo =
  `world.py` = predecir T.** `R = (S_agente − S_naive)/(S_truth − S_naive)`.

## 3. La presión que hace morder el vicio (principio 3)

Con presupuesto holgado el agente barre toda la grilla y encuentra `T` — el vicio se duerme. **La
trampa necesita queries ESCASAS**: pocas para permitirse confirmar Y explorar el borde. Bajo
escasez, el que gasta todo confirmando su H (positive testing en 1a) se queda sin con qué probar el
borde. La escasez es la perilla de dificultad (como en `first_story_scarce_v0`).

## 4. Certificado de trampa necesaria (ADR 0082 — dos robots × dos mundos)

- **Vicioso "positive-tester"**: samplea solo dentro de su H actual (donde la piel apunta) →
  confirma → entrega H. Pre-registro: en **1a** queda LEJOS del techo (se pierde `[2,6)`); en **1b**
  GANA (choca el hueco). Es el espejo.
- **Vicioso "disconfirmation-fijo"**: samplea solo fuera de su H → en **1a** GANA; en **1b** queda
  lejos (testea `(10,·)` vacío, no aprende). El espejo del anterior.
- **Cuidadoso adaptativo**: prueba ambos bordes / el borde relevante → recupera `T` → alcanza el
  techo en LOS DOS. Debe llegar; si no llega, la trampa es injusta y se descarta.
- Distribucional sobre seeds (no un punto).

## 5. La pieza delicada — la piel/prior (necesita ojo de Lucas)

Para que `H` sea la corazonada NATURAL del agente (no una que le dictamos), la **piel semántica**
tiene que hacerla obvia, y se **verifica con un panel de LLMs frescos** (`prior_reliability`): dado
solo el brief, ¿el panel espera `H`? Ej. 1a: "el aditivo recién se activa a alta concentración"
→ el naive espera efecto solo alto. Ej. 1b: "el aditivo actúa desde dosis bajas". **Riesgo**: si la
piel no ancla bien `H`, no hay trampa (el agente no tiene por qué empezar por H). Esto es lo único
que depende de LLM (panel de prior), fuera del reward path.

## 6. Pre-registro (firmar antes de correr)

- 1a: `gap(vicioso positive) ` grande (lejos del techo) ∧ `gap(cuidadoso) ≈ 0` (llega).
- 1b: espejo exacto — `gap(vicioso disconfirmation-fijo)` grande ∧ cuidadoso llega.
- **La prueba del principio 9**: un mismo robot de política FIJA cambia de ganador↔perdedor entre
  1a y 1b. Si un solo atajo ganara los dos, el par no mide juicio → se rediseña.
- Ambas monedas (R y R_uncl). Distribucional sobre seeds.

## 7. Preguntas abiertas de diseño (para decidir con Lucas)

1. **¿1a solo primero, o el par 1a+1b junto?** El par junto es lo que prueba el anti-overfitting;
   pero 1a solo es el slice más chico para validar el motor.
2. **La piel** (§5): ¿qué dominio? (proceso industrial como el resto, o algo más neutro). ¿Cuánto
   invertir en el panel de prior antes del primer humo?
3. **¿1-D basta o el efecto vive en 2-D?** 1-D es el slice mínimo fiel a Wason; 2-D daría más
   estructuras de borde (pero más complejidad).
