# Resultado — smoke count_regime_v0 (mundo 2): el salto tiene GRADIENTE por operador

> **Ficha:** [count-regime-v0](2026-08-07-ficha-mundo-count-regime-v0.md) (congelada antes de
> construir; microhipótesis H-M1/2/3 pre-registradas). Certificación VERDE (4 compuertas + 8
> robots; R direccional +1.0). Corridas: técnico gpt 99490 + tanda 12 (2 modelos × 2 polos × 3
> seeds 99500–99511, sin ayuda, en paralelo). Costo ≈ USD 3. Crudos en
> `scripts/out/count_regime_smoke/`.
>
> **Alcance del titular:** 2 modelos × 1 mundo × n=3 por celda (+ técnico), sin ayuda, v0.

## Números

| Celda | S_quiebre_fuerte | R | Velocidades compradas |
|---|---|---|---|
| gpt brk 99503 | **0.633** | 0.883 | **10** (grilla fina 1.03–1.10) |
| gpt brk 99505 | **0.653** | 0.935 | **9** (grilla fina 1.02–1.10) |
| gpt brk 99504 | censura (no_cell) | — | 7 (estaba zoomeando 1.05–1.15) |
| gpt brk técnico 99490 | 0.0 | 0 | 4 (gruesa) |
| DeepSeek brk 99500 | 0.479 | 0.503 | 5 (gruesa 0.1) |
| DeepSeek brk 99501 / 99502 | 0.0 / 0.0 | 0 | 4–5 (gruesa) |
| Gemelo (6 celdas, ambos modelos) | S_clean 0.72–0.93 | 0.94–0.99 | espurio **0/6** |

## Microhipótesis vs realidad

- **H-M1 (más salto espontáneo que en count_mix): CONFIRMADA.** 2/5 válidas postulan el
  quiebre (gpt 2/2 de tanda) vs **0/9** en count_mix. La distancia-al-menú difiere por
  operador: el modelo de quiebre es alcanzable de manual; la mezcla no lo era. Y el salto que
  aparece es **PARCIAL** (~0.65): postulan las dos leyes pero ubican el corte en 1.08 (verdad
  1.071) con pendientes gruesas.
- **H-M2 (gemelo limpio): PASA.** Espurio 0/6 — nadie inventa quiebres donde no hay.
- **H-M3 (shopping): CONFIRMADA y más rica.** Los que saltan hacen **zoom adaptativo** — gpt
  99503 t3: *"there seems to be a sharp jump around 1.05–1.1... A few targeted experiments near
  the suspected threshold are worth more than broad extra sampling"* → compra grilla fina →
  *"strongly support a discontinuity... a piecewise Poisson model is the most defensible"*.
  Los que no saltan compran grilla gruesa (3–5 puntos) y la curva suave absorbe el escalón.
- **R direccional: FUNCIONA** (novedad vs mundo 1): R 0.88/0.94 para los que capturan el
  quiebre, 0 para los que no — primera familia donde la nota gruesa premia el descubrimiento
  (A2 por construcción, verificado con agentes reales).

## Los dos especímenes de racionalización (la juntura rota, otra vez, con citas)

- **DeepSeek 99502 — nombra el candidato correcto y lo descarta.** Ve la anomalía (t9: *"fit
  matches well except at speed 1.1 (predicted 8.11 vs observed 12.40). That's a large
  discrepancy"*), compra MÁS datos del punto anómalo (¡shopping perfecto!), confirma que es
  real (11.0), escribe *"Perhaps a piecewise linear in log space: two segments? **But given the
  limited data, I'll go back to the exponential form**"* — y entrega la suave SABIENDO que
  falla ahí (t12: *"underestimates speed 1.1... maybe the true mean at 1.1 is an outlier"*).
  El candidato entró al menú por sus propios medios y lo mató el mismo filtro de siempre.
- **gpt técnico 99490 — la discontinuidad explicada como ruido.** Ve el salto 1.0→1.1 y escribe
  *"That makes me suspect the historical sample at 1.0 was noisy… **not that the process is
  discontinuous**"* — entrega un polinomio suave. La evidencia se re-etiqueta para no abrir
  estructura.

## Addendum — autopsia fina (pedido de Lucas: "¿qué es lo que pasa?")

**El dato de partida: acá NADIE puede no-ver el escalón.** Todos compran velocidades a ambos
lados y el promedio pasa de ~5.5 a ~11.5 entre 1.0 y 1.1 — está en sus tablas siempre. La
diferencia entera del mundo está en la RESPUESTA al escalón visto. Hay tres, y las tres están
en las trazas:

1. **Postular dos leyes** (gpt 99503/99505): conjetura el corte, zoomea, entrega piecewise.
   Descomposición del error sobre la grilla de examen: **clavan TODO** (±0.2 en zona baja, ±0.2
   en 1.18, corte a 0.009 del real) **menos el nivel de la ley alta justo después del corte**
   (+1.0/+1.3), porque lo anclaron en su medición ruidosa de 1.08 (compraron muchas velocidades
   con pocas filas cada una: localizaron el corte a costa de precisión por punto). El S≈0.65 es
   **concepto completo + calibración limitada** — no medio-concepto.
2. **Explicarlo como ruido** (gpt técnico: *"the historical sample at 1.0 was noisy… not that
   the process is discontinuous"*; DeepSeek 99502: *"outlier"*): la evidencia se re-etiqueta
   para no abrir estructura. Entregan suave. S=0.
3. **Esquivar el compromiso: unir los puntos** (DeepSeek 99500) — la sorpresa de la autopsia:
   NO postuló el quiebre (mi primera lectura del 0.479 era errada). Consideró piecewise por
   escrito (*"Or a piecewise linear with a breakpoint"*) y eligió interpolación lineal entre
   sus 5 puntos medidos (*"which will be monotonic and match the observed means exactly.
   That's easy to implement"*) — **cero ley postulada, ajuste local máximo**. Su 0.479 es el
   abrazo a los puntos comprados; la vara lo caza donde no compró (error +2.7 en 1.05, el hueco
   entre 1.0 y 1.1). Tercer refugio del menú: ni la ley vieja ni la nueva — ninguna ley.

**La censura que duele (gpt 99504):** su último razonamiento tenía el MEJOR diagnóstico de toda
la tanda — *"salto abrupto entre 1.05 y 1.08… un umbral en ~1.065"* (verdad: 1.0711) — y murió
sin emitir la celda de código (no_cell). La censura esconde el que probablemente era el mejor
salto. (Anécdota: ese razonamiento final salió en castellano.)

**Implicación para la vara** (para Codex): la interpolación pura obtiene crédito parcial sin
postular nada; la grilla de examen ya la castiga en los huecos entre compras (por eso 0.479 y
no 0.9), pero conviene reportar la sub-métrica "error en huecos" por separado en la versión
benchmark.

## Nivel arriba

- **Aprendizaje real:** la juntura rota (el candidato estructural no entra — o entra y lo
  matan sin test) **generaliza al segundo operador, pero con tasa distinta**: mezcla 0/9,
  quiebre 2/5 parcial. La matriz saltos×realismo ya tiene su segunda celda medida y la
  variable "distancia-al-menú por operador" existe y es medible. El zoom adaptativo de compra
  es un fenómeno positivo nuevo (no existía en count_mix).
- **Límite del claim:** n=3 por celda, sin ayuda, v0 sin escalera; los saltos son parciales
  (~0.65) — capturan el corte, no la forma fina; 1 censura.
- **Explicación rival viva:** para el 2/5, "gpt zoomea por estilo de shopping, no por
  hipótesis" — distinguible leyendo si el zoom PRECEDE o SIGUE a la conjetura del umbral (en
  99503 la conjetura precede al zoom fino: t3 lo dice antes de comprar).
- **¿Mejor uso del próximo dólar?** El programa ahora tiene DOS celdas de la matriz con
  vara certificada y una variable nueva entre ellas. Siguiente decisión (Codex/Lucas):
  tercer operador (invariante/conservación) vs escalera de ayudas acá vs tercera familia de
  modelos sobre ambos mundos congelados.
