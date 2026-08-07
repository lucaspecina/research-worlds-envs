# Resultado — smoke count_mix v0 (slice 1 del programa de saltos)

> **Estado:** exploratorio (fase descubrimiento, ADR 0173). Lectura contra la tabla CONGELADA de la
> [ficha](2026-08-06-ficha-mundo-count-mix-v0.md) §7, sin tuning. Crudos:
> `scripts/out/count_mix_smoke/` (13 episodios: 1 técnico + 12 principales). Costo total del smoke:
> ~482k tokens ≈ **menos de USD 1** (techo: 50).

## Resultado corto

**12/12 celdas válidas, cero censura, 12/12 entregas aceptadas.** Y el hallazgo es más fino que el
sí/no que la ficha esperaba:

> En MIX, los dos modelos construyeron **exactamente la MITAD del salto, los 6 de 6**: capturaron
> la heterogeneidad persistente por lote casi a la perfección (ICC entregado 0.73–0.78 vs verdad
> 0.746) — pero la modelaron **siempre como continuo** (frailty Gamma/NegBin, 6/6) y **0/6
> postularon clases discretas**: el valle quedó en 0.31–0.35 vs verdad 0.154, igual o peor que el
> baseline de un componente (0.305). En el gemelo, **6/6 limpios** (espurio 0/6): nadie inventa
> estructura donde no la hay.

| Celda | S_struct | F_mean | ICC (vs 0.746) | valle (vs 0.154) | familia entregada | repeats en turno |
|---|---:|---:|---:|---:|---|---:|
| DeepSeek 99300 | 0.413 | 0.98 | 0.738 | 0.329 | gamma-frailty | 3 |
| DeepSeek 99301 | 0.434 | 0.99 | 0.743 | 0.324 | gamma-frailty | 3 |
| DeepSeek 99302 | 0.335 | 0.95 | 0.734 | 0.352 | gamma-frailty | 4 |
| gpt-5.4 99303 | 0.455 | 0.98 | 0.770 | 0.313 | gamma-frailty | 2 |
| gpt-5.4 99304 | 0.392 | 0.97 | 0.748 | 0.337 | gamma-frailty | 2 |
| gpt-5.4 99305 | 0.447 | 0.90 | 0.780 | 0.314 | gamma-frailty | 3 |

SINGLE: S_clean 0.746/0.964/0.925 (DeepSeek) · 0.983/0.983/0.972 (gpt-5.4); espurio **0/6**;
mayoría entregó Poisson pelado (dos frailty suaves con ICC ≤0.18, bajo la vara de espurio).

**Los 12 compraron el experimento discriminante** (repeticiones del mismo lote) en los turnos
2–4, sin que nadie lo señalara — el aha A4 (pedir el dato que discrimina) está PRESENTE. Lo que
falta no es la compra: es la hipótesis.

## Localización en la cadena (autopsia — la única autorizada por la ficha)

- **Notar ✓:** 2–4 celdas por episodio miraron el histograma/`value_counts` — con las dos jorobas
  a la vista (valle al 49% del pico menor, certificado anti-póster).
- **Interpretar ✗ (acá se corta):** la palabra "mixture" aparece en 5/6 trazas MIX… **siempre y
  únicamente como "Poisson-gamma mixture (negative binomial)"** — la mezcla CONTINUA de libro.
  Cero menciones de bimodal / two groups / two components / clusters / dos tipos en las seis
  trazas. El espacio de hipótesis de ambos modelos contiene UNA sola movida de heterogeneidad: la
  frailty continua.
- La miguita más elocuente (DeepSeek 99302, turno 7): *"the process is not exactly Poisson-gamma
  but maybe a different mixture"* — **tocó la duda y siguió en gamma igual.** Con presupuesto
  restante (280) para comprobarla.

## Lectura formal (tabla congelada §7)

| Celda de lectura | Regla congelada | Resultado |
|---|---|---|
| MIX DeepSeek | ≥2/3 seeds | S ∈ (0.25, 0.6) en 3/3 → **INDETERMINADO** |
| MIX gpt-5.4 | ≥2/3 | 3/3 → **INDETERMINADO** |
| SINGLE ambos | espurio sustantivo | 0/6 → **limpio** (bilateral sostiene) |
| Gate F_mean ≥ 0.6 | por episodio | 0.90–0.99 → todas las lecturas válidas |
| Brazo pista | solo si "no abrió" (S≤0.25) en ≥2/3 | **NO disparado** (nadie ≤0.25) |

Indeterminado → *"se reporta tal cual; UNA autopsia; sin tuning"* — esta es esa autopsia. La
microhipótesis de la ficha queda **parcialmente refutada en dirección informativa**: predijo
S≤0.25 ("no abren"); la realidad es una apertura por el canal continuo con el canal discreto
ausente.

## Convergencia con la evidencia previa

La firma de agosto en el SCM gaussiano (media corregida + mezcla 75/25 aplanada en UNA Normal
ancha, `A3≈0`, 4/4 forks) es **la misma jugada**: absorber estructura discreta en dispersión
continua. Ahora replicada en un formalismo distinto (conteos), con la mitad-que-sí medida por
primera vez (ICC ≈ perfecto) y con el gemelo limpio en ambos lados. El fenómeno refinado,
como CANDIDATA (no claim):

> **El salto ausente no es "hay estructura latente" — es "la estructura es DISCRETA".** Los
> agentes abren heterogeneidad continua con soltura de libro (NegBin/frailty es su reflejo);
> postular CLASES —que la población viene en tipos— no entra al espacio de hipótesis ni con la
> evidencia a la vista, el discriminante comprado y presupuesto de sobra.

Anclas externas de la candidata: Mendel (el salto histórico fue leer RATIOS discretos),
DiscoverPhysics (fallan justo en especies/tipos), Chen et al. (la movida evitada es *decouple*).

## Nivel arriba

1. **Qué aprendimos:** el instrumento funciona entero en su primer contacto con la realidad
   (12/12 válidas, bilateral limpio, shopping capturado, <USD 1); y la descomposición del S en
   (valle, ICC) hizo visible una estructura fina — mitad-salto — que un S escalar habría
   promediado a "indeterminado" sin contenido.
2. **Qué NO autoriza:** n=3 por modelo, UNA instancia de mundo, dos modelos de dos familias;
   exploratorio por diseño. Nada de tasas ni de "frontier agents" en general.
3. **Explicaciones rivales vivas:** (a) **dosis** — el valle al 49% del pico quizá es demasiado
   sutil para vencer el prior NegBin (aunque el testigo lo separa con ΔBIC=65 y los agentes lo
   MIRARON); (b) **costo de implementación** — ajustar frailty vs ajustar mezcla-2 a mano en un
   kernel scipy-only no es perfectamente simétrico (EM manual vs fórmula cerrada NegBin); se
   anota como confound menor (ambos son implementables en ~15 líneas y el 99302 tenía la duda
   escrita y presupuesto para comprarla).
4. **¿El siguiente paso de mayor valor sigue acá?** Tras señal válida corresponde **como máximo
   UN control decisivo en este host** (ADR 0172). El que discrimina las rivales: **instancia
   fresca con separación mayor** (valle profundo, siempre bajo anti-póster relajado en regla
   nueva… NO: el anti-póster existe para lo contrario) — mejor formulado: instancia fresca en el
   rango ya legal con el valle más profundo que el certificado permita, mismos brazos mínimos.
   Si el reflejo continuo persiste con bimodalidad gritona → "clase ausente del repertorio" gana
   sobre "dosis sutil". Si abren → la perilla de solapamiento ES el dial del fenómeno (también
   valioso). La alternativa superior es cruzar ya con Codex/Lucas y sumar la tercera familia de
   modelos antes del control.

## Brazo pista — el control único (ejecutado 2026-08-07 con GO de Lucas; registro en ficha)

Frase congelada en el PRIMER prompt: *"considerá que los datos pueden venir de más de una
subpoblación"*. 8/8 episodios válidos.

| Celda | S | familia entregada | Menciones de clases discretas en la traza | ¿Ajustó mezcla-2 en código? |
|---|---:|---|---|---|
| DeepSeek MIX 99350 | 0.474 | gamma-frailty | "clustering", "two subpopulation" (t1–t2) | **0 celdas** |
| DeepSeek MIX 99351 | 0.330 | gamma-frailty | "subpopulations via clustering or mixture" (t3) | **0 celdas** |
| gpt-5.4 MIX 99352 | 0.376 | gamma-frailty | **cero** | 0 |
| gpt-5.4 MIX 99353 | 0.373 | gamma-frailty | **cero** | 0 |
| SINGLE (4 celdas) | 0.69–0.98 | poisson/frailty suave | — | espurio **0/4** |

**La pista NO movió nada:** banda S idéntica al brazo espontáneo (0.33–0.47), gamma-frailty 4/4,
repeats comprados 8/8. Y el gemelo quedó limpio 4/4 — la frase tampoco induce clases fantasma
(sin sugestibilidad).

**Lectura honesta, con su salvedad de instrumento:**
- La historia simple "el repertorio está ausente pero disponible a demanda" (patrón
  LLM-as-Investigator) **NO replicó** con esta frase: muerta en su forma simple.
- "Incapacidad" TAMPOCO queda establecida: el control de familias declaradas de agosto mostró que
  implementan mezclas cuando se les nombra la familia exacta. La localización fina que este brazo
  deja: **la hipótesis discreta no sobrevive hasta código testeado ni cuando el tema viene
  nombrado** — DeepSeek la DICE ("subpopulations via clustering or mixture") y no la prueba
  (0 celdas de ajuste mezcla-2, con presupuesto sobrante); gpt-5.4 ni la verbaliza.
- **Salvedad declarada:** la frase congelada sub-especifica lo discreto — "más de una
  subpoblación" admite la lectura continua (cada lote su tasa: frailty ES muchas subpoblaciones).
  GUARDIA intacta: una frase, un brazo, prohibido escalar pistas en este host ("más pistas =
  receta de programación"). La versión nítida de la pista ("un número CHICO de clases") es
  material para el diseño del siguiente nivel, no para este host.

**El control único está GASTADO.** Corresponde subir de nivel (ADR 0172): cruce con Codex +
tercera familia de modelos, con el dossier completo.

## Ledger del slice

- 🟢 Pasos 1–5 del plan COMPLETOS: lecturas · ficha · construcción · certificación 19/19 ·
  smoke real 13/13 episodios válidos, bajo techo por 50×.
- 🟢 Control único EJECUTADO (brazo pista, decisión de Lucas): no rescata; localización afinada
  a "la hipótesis discreta no llega a código testeado ni nombrada"; gemelo inmune a la frase.
- 🔴 VIVO — SUBIR DE NIVEL: cruce con Codex + tercera familia de modelos, dossier completo.
- 🟡 VIVO — actualizar cabecera de `docs/roadmap.md` con este resultado (con OK de Lucas).
- ⚪ Brazo pista: no disparado por regla; queda documentado.


---

## Escalera de ayudas sobre v0.2 (encargo corregido) — resultado (2026-08-07, 16 episodios, addendum de ficha)

Métrica: `S_valley_fuerte` (vara de la auditoría — discretitud contra el rival continuo CON
persistencia; rival=0, verdad=1). 15/16 válidos; 1 censura (DeepSeek nivel4 99369, max_tokens a
19 turnos, sin entrega — se reporta, no se re-rollea).

| Nivel | DeepSeek-V3.2 | gpt-5.4 |
|---|---|---|
| **0 — sin ayuda** (contrato de evaluación clarificado) | 0.0 · 0.0 (gamma/negbin) | 0.0 · 0.0 (gamma) |
| **3 — "unos pocos tipos distintos"** | 0.0 · 0.0 (gamma 2/2) | **0.874 · 0.965 (mezcla 2/2)** |
| **4 — "probá mezcla finita 2–3 grupos"** | **1.000** (mezcla, con 3 celdas de comparación real) · CENS | 0.172 · 0.0 (**gamma otra vez — desobedeció la receta**) |
| Gemelo (guardia, niveles 3+4) | espurio 0/2 (S_clean 0.68/0.93) | espurio 0/2 (0.98/0.98) |

**Los cuatro hallazgos:**

1. **El fenómeno sobrevive al contrato justo:** con el encargo explicando el examen ("sustituto
   fiel, datos idealmente indistinguibles"), sin ayuda: **0/4 abren** (vara honesta = 0.0 los
   cuatro). La rival "hicieron lo que se les pidió" está muerta y el fenómeno sigue.
2. **La altura del salto es POR MODELO** (perfiles de vicio por modelo, otra vez — ADR 0111):
   a gpt-5.4 le alcanza **la palabra** ("tipos" → 0.87/0.97); DeepSeek necesita **la receta**
   (nivel 4 → 1.0, y ahí sí corrió comparaciones de verdad, 3 celdas — la única celda del slice
   entero que comparó modelos).
3. **La sorpresa: gpt-5.4 con la receta explícita se AUTO-CONVENCIÓ de volver al continuo.**
   Verbatim del razonamiento final (99371): *"the estimated NB size stays roughly stable around
   2–3 despite noise, which is exactly what gamma mixing… predicts"* — chequeos de adecuación
   que son igualmente consistentes con AMBAS hipótesis, usados como si discriminaran; 0 celdas
   de comparación frente a frente. No es desobediencia ni incapacidad (nivel 3 lo probó capaz):
   es el mismo agujero de siempre — **decide entre hipótesis sin correr el test que las separa**.
   Y la lectura es coherente con el gemelo: allá también resistió la instrucción nivel-4… donde
   resistir era CORRECTO. Confía en sus chequeos en ambos mundos; sus chequeos no distinguen.
4. **La exigencia de Lucas quedó satisfecha: LLMs resolvieron BIEN este mundo** — gpt 0.97
   (nivel 3), DeepSeek 1.00 (nivel 4). El mundo está validado por agentes reales, no solo por
   robots. Y la guardia bilateral aguantó las dos instrucciones: espurio 0/4 — nadie inventa
   clases donde los datos dicen que no las hay.

**Vara de altura resultante:** gpt-5.4 salta a UNA PALABRA de distancia (pero la re-litiga si le
das la receta, porque sus desempates no discriminan); DeepSeek salta solo con la receta en la
mano (y entonces ejecuta perfecto). El hilo único que une todos los modos de falla del slice:
**la comparación discriminante entre hipótesis no se corre espontáneamente casi nunca**
(1 celda de 27 episodios totales la corrió — DeepSeek nivel-4).

**Estado del dossier:** completo para el cruce con Codex — fenómeno bajo contrato justo,
capacidad demostrada en-mundo, vara de altura por modelo, bilateral limpio, tres fallas de
diseño v0 documentadas con sus fixes, y una censura reportada.