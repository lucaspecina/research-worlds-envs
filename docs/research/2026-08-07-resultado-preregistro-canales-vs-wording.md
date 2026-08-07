# Resultado — pre-registro canales vs wording: mi teoría murió y dejó algo mejor

> **Pre-registro:** [2026-08-07-preregistro-canales-vs-wording.md](2026-08-07-preregistro-canales-vs-wording.md)
> (commiteado ANTES de correr). 14 episodios, seeds congeladas, ~USD 2–3. Crudos completos en
> `scripts/out/count_mix_smoke/` (seeds 99340–99345, 99392–99399). **Este doc aplica las reglas
> de decisión tal como quedaron firmadas.**
>
> **Alcance del titular:** 2 modelos × 1 mundo (count_mix v0.2) × n=4 por celda de ayuda
> (2 viejas + 2 nuevas) × 3 frases congeladas.

## Los números (nuevas corridas + acumulado)

| Celda (mix) | Corridas nuevas | **Acumulado n=4** |
|---|---|---|
| gpt + concepto (nivel3) | 0.513 · 0.902 | **4/4 salta** (0.87 · 0.97 · 0.51 · 0.90) |
| gpt + receta (nivel4) | **0.997** · 0.0 | **1/4** (0.17 · 0.0 · 0.997 · 0.0) |
| DeepSeek + concepto (nivel3) | 0.0 · **0.909** | **1/4** (0.0 · 0.0 · 0.0 · 0.909) |
| DeepSeek + receta (nivel4) | 0.993 · 0.917 | **3/3 válidas** (1.0 · 0.993 · 0.917; 1 censura) |
| **gpt + comparación mandada (nivel4b)** | 0.0 · censura (no_cell) | **0/1 válida** |
| **DeepSeek + comparación mandada (nivel4b)** | 0.0 · 0.0 | **0/2** |
| Gemelo nivel4b | gpt 0.973 espurio=no · DS censura (max_tokens) | limpio 1/1 válida |

## Predicciones firmadas vs realidad

- **P1 (gpt salta con la comparación mandada): FALLA.** 0/1 válida (+1 censura). La frase del
  "acto" no produjo ni un salto en nadie: **0/3 válidas** entre ambos modelos.
- **P2 (DeepSeek corre la comparación): MITAD.** Corrió la comparación 2/2 — formal y con
  datos de validación frescos — pero salto 0/2.
- **P3 (bilateral): PASA** en la única celda válida del gemelo (0.973, sin grupos fantasma).
- **P4 (se repite el patrón cruzado): FALLA en las celdas "cero".** gpt+receta ya no es 0
  (99398 = 0.997) y DeepSeek+concepto tampoco (99393 = 0.909).

**Reglas que disparan** (escritas antes de mirar): la 2 (autopsiar QUÉ comparación corrieron
con nivel4b) y la 3 (el patrón cruzado determinista se degrada; corregir alcance donde fue
citado — vicios 1.C/9, índice de hallazgos, roadmap — hecho en este mismo commit).

## La autopsia de nivel4b — la orden se obedeció, y no sirvió de nada

Los tres episodios válidos EJECUTARON la comparación mandada. El detalle es lo que importa:

- **DeepSeek 99340 (18 turnos, el más aplicado):** Candidato 1 = Poisson-gamma jerárquico;
  Candidato 2 = **NB inflado en ceros**. Ajustó ambos, corrió un experimento de validación a
  velocidad nueva (1.05), comparó por KS y momentos, eligió el 1 con criterio. Una comparación
  de libro… **entre dos familias continuas de su menú de siempre**. S = 0.0.
- **gpt 99342:** interpretó "dos familias de modelos" como **dos formas de la curva
  media-vs-velocidad** (potencia vs lineal) — comparó en un eje ortogonal a la estructura.
  S = 0.0 en 4 turnos.
- **gpt 99343:** comparó **Poisson vs NegBin** y luego "NB plano vs NB jerárquico" —
  comparaciones reales, menú familiar. Murió sin entregar (censura no_cell).

**La lección, en una frase: mandar el ACTO no sirve si el MENÚ sobre el que se ejecuta lo
elige el mismo prior.** La comparación sin el candidato correcto es teatro metodológico — es el
vicio 9 un nivel más arriba: ni siquiera "no corre el test discriminante"; corre tests con
esfuerzo real sobre un espacio de hipótesis capturado. Y refuta mi mecanismo firmado ("lo que
falta es el acto"): lo que falta es **el candidato dentro del menú**.

## Las dos celdas que rompieron el patrón (autopsia)

- **gpt 99398 (receta, 0.997):** esta vez el hint aterrizó — *"The brief's hint about a finite
  mixture now looks apt: a small mixture over lot rates could capture the bimodality"* — y
  entregó la mezcla de 2 puntos. Mismo modelo, misma frase que en 99370/99371 (donde la
  descartó como "parsimonious continuous alternative"): **el canal receta en gpt es
  estocástico (1/4), no imposible** — depende de si su propia lectura de los datos hace
  saliente la heterogeneidad justo cuando la nota está en mano.
- **DeepSeek 99393 (concepto, 0.909):** esta vez su deambular llegó a las medias por lote
  ANTES de que el plan decayera (t6: entre-lotes 14.6 vs dentro-de-lote 1.7 → "distinct lot
  types" → EM → entrega). El canal concepto en DeepSeek también es estocástico (1/4).

## Síntesis (etiquetada POST-HOC — no estaba pre-registrada)

Con n=4, lo que queda en pie no es el cruce determinista sino esto:

1. **Robusto:** gpt+concepto **4/4** · DeepSeek+receta **3/3 válidas** — cada modelo tiene UNA
   puerta por la que la ayuda entra casi siempre (la mirada / la spec).
2. **Estocástico, no cero:** las puertas cruzadas (gpt+receta, DS+concepto) rescatan ~1/4.
3. **Nulo:** el procedimiento puro (compará familias, sin contenido) **0/3** — y no por
   desobediencia: obedecen y comparan dentro del menú propio.
4. Corolario conductual: la métrica "¿corrió comparación formal?" pasó de 1/28 a 3/3 bajo la
   orden — pero **sin poder discriminante**. La métrica que importa es "¿la comparación incluye
   un candidato estructuralmente distinto del entregado?" — computable de trazas, cero-LLM.

**El objeto medible que emerge:** el salto exige que el candidato correcto ENTRE AL MENÚ; el
acto de comparar es barato y lo ejecutan bajo orden — sobre el menú que ya tenían. La ayuda
efectiva es la que mete el candidato al menú por la puerta que ese modelo usa. Ordenar el
método científico no desbloquea un espacio de hipótesis capturado.

## Qué sigue (propuesta, NO corrido — regla 5: sin frases nuevas en esta tanda)

1. Dossier a Codex (mañana, con créditos) — ahora incluye un pre-registro corrido con teoría
   propia refutada: el instrumento funciona.
2. Decisión de diseño para la siguiente frase/mundo (con Codex/Lucas): ¿cómo se testea
   "candidato-en-menú" sin regalar el candidato? (p.ej. exigir que una familia candidata sea
   "de una clase distinta a la entregada" roza el leak — discusión abierta).
3. Los 2 censurados (99343 no_cell de gpt; 99344 max_tokens de DS) se reportan como censuras;
   no se re-corren sin decisión explícita.

## Nivel arriba

- **Aprendizaje real:** el acto discriminante mandado se ejecuta como teatro sobre el menú del
  prior (0/3); las puertas por-modelo son reales pero estocásticas (4/4 y 3/3 vs 1/4 y 1/4).
- **Límite del claim:** 2 modelos, 1 mundo, n=4 por celda, censuras 3/17; síntesis post-hoc.
- **Rival viva:** para las celdas 1/4, ruido puro sigue siendo indistinguible de "canal débil".
- **¿Mejor uso del próximo dólar?** Sí siguió siéndolo: este mundo acaba de refutar una teoría
  nuestra pre-registrada por USD 3 — exactamente para eso está la fase de descubrimiento.
