# Ficha congelada — count_regime_v1 (el episodio del impasse; brazos RAW/VISIBLE)

> **Congelada 2026-08-09 ANTES de construir y de correr** (GO de Lucas: "todo sí"; diseño =
> veredicto de Codex 2026-08-09, sesión supervisora ADR 0172 — crudos en
> `scratch/codex-respuesta-2026-08-09.txt`). Nada de esta ficha se edita después de correr;
> cambios de Codex/Lucas superseden por addendum fechado. Es **la única prueba decisiva** de
> esta familia: no hay v1.1/v1.2 ni escalera de frases — después de esta corrida se vuelve
> arriba (MANTENER/MODIFICAR/PIVOTEAR).

## Pregunta (el claim reencuadrado — ADR 0174)

> ¿Cuándo un agente amplía su conjunto activo de hipótesis durante una indagación, **después
> de que su modelo vigente falla**, y qué tipos de estructura logra o no logra activar?

**Estimando de esta corrida**: ¿hacer VISIBLE el fallo del modelo propio (mismos datos,
mismo contenido) aumenta la aparición de una familia estructural nueva? — el test causal de
la teoría del impasse (Ohlsson), que hoy es teoría rival prometedora, NO doctrina confirmada
en LLMs.

**Qué NO afirma**: nada sobre "creatividad general" ni invención fuera del repertorio
(novedad relativa: quiebre de régimen es estructura de manual — lo que se mide es la
ACTIVACIÓN de esa estructura tras el fallo, no su invención). La celda de count_mix (0/9,
generación espontánea) queda intocada como fenómeno aparte.

## Constructo: generación vs aceptación, separadas SERVER-SIDE por timing (cero-LLM)

Para cada episodio se computa mecánicamente el **punto de discriminación**: el primer momento
en que la evidencia acumulada disponible al agente da al modelo de régimen ventaja clara y
sostenida sobre los rivales congelados (regla congelada: ΔBIC ≥ 6 contra el mejor rival, y
que no se revierta con la compra siguiente). Entonces:

- candidata de régimen **registrada ANTES** de ese punto = **expansión generativa** (el
  fenómeno que buscamos);
- registrada **DESPUÉS** = **aceptación** (lo que midió la v0; se reporta aparte, no compite).

La clasificación semántica de trazas puede validarse offline con lectura humana; **el reward
y esta clasificación primaria siguen cero-LLM** (timing + artefactos ejecutables).

## Verdad (polo principal `brk`) — la firma NO flagrante

Cada lote i entrega `y_i ~ Poisson(λ(speed))`, una medición por lote.

- **Ley A** (s < s*): `λ_A(s) = lam0 · s^alpha`.
- **Ley B** (s ≥ s*): `λ_B(s) = lam0 · s^alpha + delta1 · (s − s*)` — **la media es CONTINUA
  en s*** (sin salto de nivel: delta0 = 0); lo que cambia es la PENDIENTE. Nada de 5.5→11.5
  en una tabla: un spline/interpolador ajusta lo visto razonablemente y falla en condiciones
  nuevas relevantes (extrapolación más allá de lo comprado).

**Gemelo `smooth`**: ley de potencia única apareada en nivel sobre la grilla de examen (sin
quiebre) — castiga el régimen fantasma, ahora también bajo VISIBLE (¿mostrar residuos induce
quiebres imaginarios? — chequeo bilateral obligatorio).

Historia física (fidelidad a casos reales, regla dura 2026-07-13): transición de régimen al
superar velocidad crítica (caso canónico Reynolds; la línea vibra y aparece un modo nuevo de
defectos — mismo anclaje que la v0). El lado del descarte ancla en Onnes (la
superconductividad descartada como "cortocircuito del equipo"): por eso el fallo llega en el
**monitoreo rutinario**, sin anuncio — como en los casos reportados.

## El episodio (las 7 compuertas de diseño — Codex 2026-08-09)

La regla central: **el impasse debe FALSIFICAR el modelo vigente; no debe NOMBRAR su
reemplazo.** Achicar el escalón de la v0 no alcanza (sería "candidato un poco menos
dictado").

1. **Prefijo y M0 rutinario.** Tras el archivo y las primeras compras, el agente **registra
   un modelo provisional ejecutable (M0)**. Si ya propone régimen ahí, cuenta como salto
   espontáneo (celda aparte, comparable con count_mix).
2. **Firma no flagrante** (compuerta de instancia): sobre las compras típicas del prefijo, el
   mejor suave/spline deja residuos no flagrantes (máximo |z| < 2 en lo visto) y la media es
   continua en s*. Si el quiebre grita en la tabla, la instancia se descarta.
3. **Calificación rutinaria.** El mundo ejecuta el M0 sobre un **lote de control
   preprogramado, idéntico en calendario entre polos y brazos**, y devuelve predicción y
   resultado crudo. Nada de "detectamos un quiebre" — cero lenguaje de anomalía.
4. **Persistencia.** Tras reajustar la misma familia, un **segundo lote independiente**
   vuelve a fallar con la misma firma. Un residuo puede ser ruido; dos fallos frescos y
   estructurados crean el impasse.
5. **Verificación comprable.** Replicar el control o probar una referencia instrumental
   cuesta **< 10% del presupuesto**. Separa "creyó que era error" de "confirmó y aun así
   descartó" (el gate de Onnes).
6. **No-dictación certificada.** En el momento del primer fallo siguen vivas **≥ 3
   explicaciones estructuralmente distintas** — deriva instrumental, mezcla cambiante,
   heteroscedasticidad, régimen — separables por un experimento posterior. Regla congelada:
   en ese punto, ningún candidato le saca al segundo ΔBIC ≥ 6 con la evidencia disponible.
   Si changepoint ya gana aplastante, volvimos a medir aceptación → instancia descartada.
7. **Necesidad teleológica** (certificado, ANTES de gastar en agentes): el régimen gana en un
   contexto no visitado donde un spline o parche suave comprable **pierde**, contra el rival
   fuerte congelado. Si no se puede certificar, **se abandona el host** y se sube de nivel —
   no se corre.

## Los dos brazos (misma información; manipulan VISIBILIDAD, no evidencia)

- **`RAW`**: recibe las filas crudas del lote de control.
- **`VISIBLE`**: recibe las MISMAS filas **más un resumen mecánico** de residuos/calibración
  de su propio M0 (generado por código, formato fijo, sin interpretación).

Seeds apareadas entre brazos; el contraste RAW-vs-VISIBLE es el estimando primario.

## La cadena mínima registrada (verbos del harness)

`M0 → reconoce/rechaza M0 → registra candidata → compra test discriminante → M1 → entrega`

- **No se penalizan candidatas provisionales** (Nersessian: no cobrar los andamios).
- **"Sin hipótesis" es estado válido y registrable** — Klahr–Dunbar predice que puede ser la
  vía de escape del marco viejo; prohibirlo mataría el fenómeno.

## Métricas

- **Primaria conductual**: expansión generativa (candidata de familia nueva registrada ANTES
  del punto de discriminación) — por brazo.
- **Entrega**: S_quiebre_fuerte (0 = rival suave fuerte, 1 = verdad; misma construcción que
  v0 adaptada a quiebre de pendiente) + sub-métrica **error-en-huecos** aparte (caza la
  interpolación-sin-ley de la v0).
- **R direccional** (premia el descubrimiento por construcción, como v0) · **espurio**
  bilateral en gemelo (por brazo — VISIBLE no debe fabricar fantasmas).
- Cadena de eventos con timestamps (M0, fallos servidos, réplicas compradas, registro de
  candidatas, M1) — el "instrumento de cadena" que reemplaza la lectura retrospectiva de
  prosa.

## Microhipótesis pre-registradas (firmadas antes de mirar, MODO AUTONOMÍA)

- **H-V1 (test causal del impasse)**: VISIBLE > RAW en expansión generativa. Regla de
  decisión: señal si VISIBLE−RAW ≥ 2 episodios con expansión en n=6 por brazo (polo brk);
  diferencia 0 con capacidad OK = **Ohlsson muere para este sustrato** (condición de salida).
- **H-V2**: en RAW (sin resumen del fallo), la tasa de familia nueva ≈ 0 — la continuación
  del 0/9.
- **H-V3**: las expansiones que aparezcan serán mayoritariamente DESPUÉS del segundo fallo
  (persistencia), no del primero.
- **Control de capacidad** (obligatorio para interpretar cualquier nulo): con el concepto
  dado explícitamente, el modelo implementa el régimen y S sube — separa "no lo activa" de
  "no puede escribirlo".

## Condición de salida (falsabilidad del programa — Codex H)

Si v1 pasa el control de capacidad pero el impasse visible NO aumenta la expansión: la
explicación Ohlsson muere para este sustrato. Si después proceso-del-observador (el tercer
operador ordenado — NO invariante) tampoco reproduce la firma: **se abandona el claim general
de "falla de salto"** y se conserva count_mix como fenómeno específico de mezcla discreta.

## Presupuesto, seeds y modelos

- Familia de seeds del caso: 99400–99599. Ya quemadas (v0): 99400–99449 · 99460–99467 ·
  99490 · 99499 · 99500–99511. **Asignación v1**: scan de instancia 99450–99459 y 99468–99489
  (la primera que pasa TODAS las compuertas se congela en `instance.json`); testigo 99512;
  batería 99513–99519; episodio técnico 99520; tanda 99521–99544.
- Tanda mínima informativa: 2 modelos (gpt, DeepSeek) × 2 brazos × 3 seeds en `brk` (12) +
  2 brazos × 2 seeds en `smooth` (4, un modelo) = **16 episodios ≈ USD 5–8**. Primera pasada,
  la mínima informativa (regla de infraestructura).
- Certificados previos a agentes: los 4 de siempre (necesidad vs rival fuerte ·
  alcanzabilidad con witness · gemelo bilateral · anti-memorización) + compuertas 2/6/7 de
  esta ficha (no-flagrancia · no-dictación · necesidad teleológica).

## Qué se decide con el resultado

Una sola corrida decisiva → dossier a Codex/Lucas → MANTENER (escalar con instancias
frescas) / MODIFICAR / PIVOTEAR (si la señal está en otra juntura) / ABANDONAR el host. La
firma de la taxonomía (codebook, unidad = edición-dentro-de-cadena) corre EN PARALELO sin
bloquear esta prueba.
