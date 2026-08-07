# Ficha congelada — count_regime_v0 (mundo 2: operador "régimen oculto")

> **Congelada 2026-08-07 ANTES de construir y de correr** (GO de Lucas: "dale avancemos.
> empecemos"). Plan y justificación del operador:
> [plan-mundo-2](2026-08-07-plan-mundo-2-regimen-borrador.md). Lecciones del mundo 1 horneadas:
> A1 (stakes teleológicos en el encargo), A2 (el salto paga en extrapolación POR CONSTRUCCIÓN),
> A3 (ancla = rival suave FUERTE, congelado acá). Codex revisa el dossier completo mañana; si
> ordena cambios, superseden por addendum — nada de esta ficha se edita después de correr.

## Verdad (polo principal `brk`)

Cada lote i entrega `y_i ~ Poisson(λ(speed))`, UNA medición por lote (sin perilla de
repeticiones — este mundo tiene una sola variable a mirar: la curva defectos-vs-velocidad).

- **Ley A** (s < s*): `λ_A(s) = lam0 · s^alpha` (suave, de manual).
- **Ley B** (s ≥ s*): `λ_B(s) = lam0 · s^alpha + delta0 + delta1 · (s − s*)` — salto de NIVEL
  (delta0) + pendiente extra (delta1). Historia física: pasada la velocidad crítica la línea
  vibra y se activa un modo nuevo de defectos (caso canónico: Reynolds).

**Gemelo `smooth`**: `λ_T(s) = c · s^beta` — ley de potencia única ajustada por LS al log de la
curva del polo brk sobre la grilla de examen (apareado en nivel; SIN quiebre). Castiga el
quiebre fantasma.

## Instancia por regla (no a mano)

`params_from_seed(seed)`: lam0 ∈ [5,7] · alpha ∈ [0.8,1.2] · s* ∈ [1.06,1.14] ·
delta0 ∈ [3,5] · delta1 ∈ [15,30]. Familia de seeds de mundo: **99400–99449** (primera que pasa
TODAS las compuertas se congela en `instance.json`). Seeds ya quemadas de la familia del caso
(99400–99599): mundo 99400–99449 · testigo 99499 · batería 99460–99467 · episodios técnicos
99490 · tanda 99500–99511.

## Compuertas de aceptación de instancia (todas deben pasar)

1. **Invisible en archivo**: `s* > 1.0` (el archivo vive en speed=1.0, lado A: el quiebre SOLO
   se ve comprando experimentos — el shopping es parte del fenómeno).
2. **Necesidad (contra rival FUERTE)**: rival suave = log-cuadrática
   `log λ = a + b·log s + c·(log s)²` ajustada por LS **con información generosa** (grilla densa
   de la verdad, 0.8–1.2 paso 0.025). `D_rival = media |λ_rival − λ_verdad|` sobre la grilla de
   examen **≥ 1.2** defectos. Si una curva suave de 3 parámetros con datos infinitos no puede
   fingir el quiebre, ninguna comprable puede.
3. **Alcanzabilidad (testigo mecánico)**: con un diseño COMPRABLE (archivo 200 filas a 1.0 +
   experimentos en {0.8, 0.95, 1.05, 1.12, 1.2} × 70 lotes ≈ presupuesto 750/1000), el testigo
   piecewise-2-tramos (s* por grilla, MLE Poisson por tramo) le gana a la log-cuadrática por
   **ΔBIC ≥ 10** en brk.
4. **Gemelo**: mismo testigo en smooth elige la suave por ΔBIC ≥ 6; apareo de nivel
   `|media_examen(λ_T) − media_examen(λ_brk)| ≤ 0.35`.

## Vara del salto (cero-LLM)

- **Grilla de examen**: speeds {0.85, 0.95, 1.05, 1.10, s*+0.01, 1.18} (ambos lados del
  quiebre). `λ̂_prog(s)` = media de n=1500 muestras del programa en s (seed fija 424242).
- **S_quiebre_fuerte** (polo brk): `D(prog) = media |λ̂_prog − λ_verdad|` sobre la grilla;
  anclada `0 = rival suave fuerte, 1 = verdad`: `S = clip(1 − D_model/D_rival, 0, 1)`.
- **F_mean**: nivel en s=1.0 (como en count_mix).
- **espurio_quiebre** (gemelo): ajuste piecewise sobre λ̂ del programa entregado en grilla densa;
  bandera si el mejor split mejora SSE ≥ 40% respecto de la suave Y el salto implícito ≥ 1.5
  defectos.
- **S_clean** (gemelo): anclada `1 = verdad suave, 0 = programa quiebre-forzado` (quiebre
  delta0=4 inyectado en s=1.10 sobre la curva del gemelo).
- **Conductuales de traza** (post-hoc, criterio fijo): #speeds distintos comprados; ¿compró
  algún speed en (1.0, 1.2) estricto (interior alto, donde vive el quiebre)? ¿comparó
  quebrada-vs-suave formalmente?

## Episodio (mismo contrato que count_mix v0.2)

Presupuesto 1000 · archivo speed=1.0, 0.5/fila, tope 400 · experimento 40 fijo + 1/fila ·
perilla única `speed ∈ [0.8, 1.2]` · entrega `model(regime, n, seed) -> [unit_id, y]` con n =
LOTES. Brief byte-idéntico entre polos, ciego a batería/vara, con el stake teleológico
declarado: **la gerencia está evaluando subir la velocidad de línea y decide con este modelo**
(A1: el objetivo REQUIERE acertar la zona alta). Sección "Cómo se evalúa" = texto v0.2 de
count_mix, sin cambios. Guardia anti-leak del brief: prohibidas las palabras umbral / quiebre /
fase / vibra / tramo / crítica / "dos leyes" / cambio de comportamiento.

## Certificados de robots (por el server real, antes de agentes)

oracle-piecewise (verdad exacta) → S_quiebre ≈ 1 · rival-suave → S_quiebre ≈ 0 en brk y
S_clean alto + espurio=NO en smooth · null-plano → malo en ambos · quiebre-forzado en smooth →
espurio=SÍ y S_clean ≈ 0. **Chequeo direccional de R** (novedad vs mundo 1): batería con speeds
de ambos lados ⇒ `R(oracle) − R(rival suave) ≥ +0.03` en brk — en este mundo el salto debe
pagar TAMBIÉN en la nota gruesa (A2 por construcción; si no pasa, la instancia se descarta).

## Tanda smoke (tras certificación verde)

Técnico 1 episodio (gpt, seed 99490) → tanda **2 modelos × 2 polos × 3 seeds (99500–99511), sin
ayuda**, en paralelo. Costo estimado ≈ USD 3.

## Microhipótesis pre-registradas (antes de correr)

- **H-M1**: el salto espontáneo acá es MÁS frecuente que en count_mix (0/9) — esperado 1–4 de
  6 en brk (los modelos de quiebre están más cerca del menú de manual). Cualquier valor
  informa la **distancia-al-menú por operador** — incluido 6/6 (operador fácil) o 0/6
  (fenómeno general fuerte).
- **H-M2**: espurio en gemelo ≤ 1/6.
- **H-M3**: conductual — la mayoría muestrea solo bordes {0.8, 1.2} + archivo 1.0 al inicio;
  muestrear ≥4 speeds distintos correlaciona con salto.
- **Regla de lectura**: brk y smooth se leen JUNTOS (bilateral); censuras se reportan aparte;
  ninguna frase de ayuda en esta tanda (primero la línea de base espontánea).
