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

## Ledger del slice

- 🟢 Pasos 1–5 del plan COMPLETOS: lecturas · ficha · construcción · certificación 19/19 ·
  smoke real 13/13 episodios válidos, bajo techo por 50×.
- 🔴 VIVO — decisión de Lucas (+Codex): ¿control único de dosis en este host, o subir de nivel
  (cruce + tercera familia + lectura del programa)?
- 🟡 VIVO — actualizar cabecera de `docs/roadmap.md` con este resultado (con OK de Lucas).
- ⚪ Brazo pista: no disparado por regla; queda documentado.
