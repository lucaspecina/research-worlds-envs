# Plan mundo 2 — operador "régimen oculto" (BORRADOR para revisión Codex+Lucas)

> **Estado: BORRADOR.** Nada congelado, nada construido. Se firma la ficha después de la
> revisión de Codex (dossier 2026-08-08) y el GO de Lucas. Diseño contrastado con la anatomía
> del vicio 4 ([doc](../vicios/vicio-4-estructura-escondida.md), regla ADR 0152) y con las
> lecciones de la auditoría del mundo 1 ([A1/A2/A3](2026-08-07-auditoria-critica-slice-count-mix.md)).

## Por qué el operador 3 (régimen/fase oculto) y no otro

**Qué es:** el sistema obedece UNA ley hasta un umbral y OTRA después (dos leyes, no una). El
salto = postular el quiebre; el vicio = ajustar una curva suave única que lo promedia.

1. **Fundación externa fuerte** (regla ≥2 columnas): historia de la ciencia — transiciones de
   fase, punto de Curie, y el caso canónico industrial: **Reynolds** (resistencia laminar hasta
   una velocidad crítica → turbulenta después); ciencia cognitiva — descomponer lo monolítico
   (Ohlsson; Darden "dividir"); era-LLM — la anatomía KellyBench ("el mundo que cambia debajo",
   palanca #10 sin probar) y DiscoverPhysics (fallan justo en estructura latente).
2. **Arregla la falla A2 del mundo 1 POR CONSTRUCCIÓN** (ADR 0150): en count_mix la estructura
   era invariante entre regímenes y el salto no pagaba en extrapolación. Acá el premio del salto
   ES extrapolación: la curva suave ajustada de un lado del umbral extrapola MAL del otro, y el
   examen sondea todo el rango declarado. No hace falta parche.
3. **Arregla A1 (stakes vacíos) con historia natural:** el encargo declara que la gerencia
   evalúa **subir la velocidad de línea** — la pregunta declarada del cliente REQUIERE saber qué
   pasa a velocidades altas. El objetivo necesita el salto; nada de funcionales postizos.
4. **Es la palanca más fuerte que tenemos** (§5.1 de fundamentos: dónde vive la señal —
   media→forma→régimen) y continúa la misma fachada realista (línea de calidad) reusando TODA la
   maquinaria de count_mix (server, costos, contratos, explorer).

**Riesgo honesto declarado:** los modelos de quiebre (changepoint) son más "de manual" que las
mezclas — puede que el fenómeno NO se reproduzca (más salto espontáneo). Eso no invalida el
mundo: **mide la distancia-al-menú por operador**, que es exactamente lo que el programa
necesita saber (¿qué saltos les cuestan más?). Microhipótesis pre-registrable: salto espontáneo
mayor que en count_mix pero < 100%; el gemelo separa apofenia (quiebres fantasma).

## Diseño candidato (C1 — umbral en la perilla)

- **Verdad**: defectos y ~ Poisson(λ(speed)) por lote; λ sigue la ley A (suave, p.ej.
  λ_A·speed^α) hasta `s* ≈ 1.12` y salta a la ley B (nivel + pendiente distintos: "la línea
  empieza a vibrar") de ahí en adelante. Umbral ADENTRO del rango declarado [0.8, 1.2] pero
  cerca del borde: el archivo (solo speed=1.0) no lo muestra; hay que COMPRARLO experimentando.
- **Gemelo**: λ(speed) suave única en todo el rango, apareada en media sobre la grilla muestreable.
  Castiga el quiebre fantasma (espurio bilateral, como en count_mix).
- **Rival fuerte del ancla** (lección A3): la MEJOR familia suave (potencia + corrección, grilla
  de nudos limitada) ajustada a los datos comprables — congelada en la ficha antes de correr.
- **Vara del salto** (cero-LLM, análoga a S_valley_fuerte): captura del quiebre en el examen —
  error en velocidades a ambos lados de s* del modelo entregado vs verdad, anclado 0=rival
  suave fuerte, 1=verdad. + F_mean, espurio (gemelo), y conductuales de traza: ¿muestreó más
  allá de s*? ¿comparó quebrada-vs-suave?
- **Certificados**: los del kit (necesidad contra el rival suave fuerte — brecha ≥ umbral en el
  examen; alcanzabilidad — testigo mecánico changepoint por BIC/CV con datos comprables; gemelo;
  anti-memorización) + **necesidad DOBLE** (la teleológica de arriba, primera vez de serie).

## Matriz saltos × realismo (el mapa del programa)

| Operador \ Realismo | R0 juguete controlado | R1 +distractores | R2 encuadre ecológico | R3 horizonte largo | R4 semilla real documentada |
|---|---|---|---|---|---|
| 2 grupos escondidos | ✅ count_mix (hecho, 42 ep.) | | | | |
| 3 régimen oculto | ← **mundo 2 (este plan)** | | | | |
| 6/9 invariante–conservación | candidato mundo 3 | | | | |
| 11 transferencia (Darwin) | (overgen ya existe como par) | | | | |

Estrategia: llenar la columna R0 con 3–4 operadores (¿generaliza la juntura rota entre TIPOS de
salto?) → recién después subir por la fila del fenómeno más robusto (R1: columnas señuelo; R2:
carpeta heredada/notas de colegas; R3: artefactos propios; R4: casos reales con links — regla de
fidelidad). En cada escalón se mantiene el núcleo certificado (verdad ejecutable, gemelo,
cero-LLM): realismo en la superficie, cirugía en la medición.

## Preguntas abiertas para Codex (dossier 2026-08-08)

1. ¿Operador 3 como mundo 2, o preferís 6/9 (invariante)? ¿Y el orden de la columna R0?
2. Calibración de la necesidad: ¿cuánta brecha contra el rival suave fuerte exige el
   certificado para que "postular el quiebre" no sea aproximable por splines?
3. ¿Firmar la taxonomía (cola de lectura de clásicos + expedientes por operador) antes de
   escalar la máquina, o en paralelo a la columna R0?
4. ¿Tercera familia de modelos ahora (sobre count_mix congelado) o después del mundo 2?
