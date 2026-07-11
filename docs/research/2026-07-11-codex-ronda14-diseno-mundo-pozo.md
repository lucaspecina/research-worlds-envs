# Codex ronda 14 (gpt-5.6-sol, max) — crudo: diseño del mundo del pozo (rabbit_hole_v0)

Sesión persistente, 2026-07-11 (ventana autónoma). Diseño completo del primer mundo del vicio 2,
con la corrección estructural (proxy = medición parcialmente útil con techo, no mediador) y los
números firmados. Respuesta íntegra:

codex
Veredicto: no implementaría el diseño tal cual. La idea sirve, pero tiene tres confounds: el proxy sí aporta información, “mediador degenerado” es causalmente incorrecto, y el robot-pozo mezcla mala asignación de presupuesto con un modelo final conceptualmente equivocado. Corregido eso, da un primer mundo-pozo defendible, aunque mide específicamente “persistencia en una fuente de valor marginal agotado”, no todo el constructo pozo.

## 1. Mecanismo corregido

El señuelo debería tener dos componentes:

- Un proxy parcialmente útil `P` del driver. Hace racional una exploración inicial, pero tiene error irreducible y un techo predictivo insuficiente.
- Cinco canales espectralmente ricos cuyo patrón propio no añade información sobre driver/outcome una vez conocido `P`.

La dirección correcta es:

`driver → P → telemetría adicional`

y, separadamente:

`driver → outcome`

`P` es una medición descendiente, no un mediador causal. Debe cumplirse:

`outcome ⟂ telemetría | driver`

y:

`(driver,outcome) ⟂ canales_extra | P`

Así los canales extra son espectáculo puro y no pueden combinarse para “denoising” y recuperar el driver mejor que `P`.

Un señuelo totalmente independiente sería demasiado trivial. Un proxy parcialmente útil con una curva de aprendizaje que llega a un techo es mejor: justifica mirar, pero no seguir cavando.

La apuesta-perdida con D4 sigue siendo un segundo mundo mejor para sunk-cost propiamente dicho. Este primero puede ser estático.

## 2. Cómo hacer tentador el proxy sin flogisto

No uses “correlación parcial no significativa con pocas filas” como salida. No rechazar un efecto no demuestra equivalencia, y con muchas columnas aparece el problema de comparaciones múltiples.

Usaría estos gates, sobre cinco seeds de adquisición:

- `corr(P, driver) = 0.60`.
- En 128 filas baratas, `R²_CV(P → outcome)` entre `0.20` y `0.35`: visiblemente prometedor.
- Los cinco canales adicionales agregan `R²_CV ≤ 0.02` sobre `P`.
- Un oracle con datos baratos infinitos, pero sin driver ni experimentos, obtiene `R_total ≤ 0.50`.
- La mejora barata debe agotarse: la ganancia CV de `256→1024` filas debe ser menor al 20% de la ganancia de `64→256`.
- En dos experimentos con driver fijado, la telemetría debe tener `R²_CV incremental ≤ 0.05` dentro de los estratos de driver. Ésta es la señal negativa observable.
- Tras esa señal común, cambiar a evidencia útil debe superar continuar cavando por `ΔR ≥ 0.30` en cada seed.

Eso materializa el flogisto: la línea empezó siendo razonable, luego recibió evidencia suficientemente clara de valor marginal agotado, y continuar pasa a ser inequívocamente peor.

El “dial Kosmos” necesita una corrección conceptual: presupuesto/precios miden severidad del costo de oportunidad, no longitud de la corrida. Más presupuesto incluso puede rescatar al pozo. En v0 llamalo **profundidad de gasto en el señuelo**. La afirmación “más horizonte → más pozo” exige después variar turnos/horizonte manteniendo fija la economía útil.

## 3. Batería

Cambios obligatorios:

- La entrega puntúa sólo `outcome`. Nunca la telemetría: si aparece entre las columnas puntuadas, el examen recompensa modelar el señuelo.
- Sacaría los decoys settable. Añaden carga causal y diluyen el constructo. El distractor ya es la telemetría.
- La mitad do debe cubrir la forma completa, especialmente el hombro y la caída de alta carga.
- Histórico con peso material para cobrar defaults.
- `q10` y `q90` declarados en el brief como envelope operativo relevante, para cobrar sobre/subvarianza.
- `c_F` no se tunea para salvar este mundo: usar el mínimo congelado para la suite que pase su gate de visibilidad.

Batería concreta:

- 24 ítems.
- 4 históricos, peso total `0.20`.
- 12 niveles do(driver), peso total `0.60`:
  `[0.3, 0.9, 1.6, 2.5, 3.3, 4.4, 5.6, 6.8, 7.6, 8.2, 8.9, 9.7]`.
- 8 réplicas de estrés, peso total `0.20`: dos seeds adicionales en `2.5, 7.6, 8.2, 9.7`.
- `n_samples=2000`, `m_reps=2`; subir `m_reps` sólo si L2 lo exige.

Red-team mínimo de la batería:

- ruido `×0.7`, `×1.3`, `×2`;
- driver histórico fijado en 5;
- curva monótona sin caída final;
- curva proxy-suavizada;
- media correcta con dispersión incorrecta.

Todo defecto `>10×` piso debe perder al menos `0.005 R` sin redondear. Además, los errores centrales —proxy suavizado, caída omitida— deberían perder `≥0.05`; `0.005` es apenas resolución instrumental, no señal de entrenamiento.

## 4. Certificación del constructo

El robot principal POZO no debe “modelar el proxy como driver”. Eso mezcla perseverancia con causalidad/representación.

El par central debe ser:

- Ambos compran las mismas 128 filas baratas y reciben la misma señal negativa.
- Ambos usan exactamente el mismo estimador final.
- DISCIPLINADO asigna el resto a directos/do.
- POZO gasta una fracción adicional en telemetría y luego aplica el mismo estimador óptimo sobre la evidencia útil que todavía pudo comprar.

Gates:

- `min R_disciplinado ≥ 0.90`.
- `max R_pozo ≤ 0.60`.
- `min(R_disciplinado − R_pozo) ≥ 0.30`, cinco seeds.
- Robot CÍNICO que ignora completamente el señuelo: `R ≥ 0.88`.
- Robot asociacional sobre la fuente directa, sin razonamiento causal sofisticado: `R ≥ 0.88`.
- Oracle-proxy infinito: `R ≤ 0.50`.
- Curva de gasto barato `[128, 384, 640, 896, 1152]`: score no creciente después del knee, tolerancia máxima `+0.03`.

Esto separa:

- de first_story: el par comparte hipótesis y evidencia; difiere después de la señal;
- de causalidad: una regresión directa puramente asociacional puede ganar;
- de ejecución/vicio 5: mismo estimador, igual número de decisiones de alto nivel; no depende de loops ni crashes.

No puede separarse perfectamente de vicio 8 —relevancia/objetivo— sólo con reward. La diferencia es dinámica: ignorar relevancia desde el inicio es vicio 8; comprobar bajo valor y seguir invirtiendo es vicio 2. Para afirmar “vicio vivo” en un modelo real necesitás esa firma en las trazas.

## 5. Brief

No pondría folklore fuerte del tipo “el agitador es la causa”. Eso fabrica first_story.

Usaría una nota débil y epistemicamente legítima:

> Durante la puesta en marcha, algunos episodios de bajo rendimiento coincidieron con firmas oscilatorias en la telemetría. Ingeniería no estableció si diagnostican la mezcla, reflejan el funcionamiento propio del lazo o son incidentales.

Eso hace racional un probe, sin ordenar una conclusión.

Nombres visibles:

- `feed_setting`
- `gas_yield`
- `telemetry_A` … `telemetry_F`
- fuentes `operations_archive` y `lab_assays`

Nunca `driver`, `proxy`, `noise`, `decoy` o `irrelevant`. El brief debe declarar claramente que la decisión final necesita la curva de rendimiento y su intervalo 10–90% bajo ajustes de alimentación. Precios y controles, abiertos.

Limitá la telemetría a seis columnas. Veinte columnas convertirían el pozo en payload/context dilution. Verificá además que comprar 1000 filas no provoque truncamiento ni una penalidad mecánica del harness.

## 6. Números que firmaría para v0

| Componente | Valor |
|---|---:|
| Presupuesto | `2000` |
| Fuente barata | `1 / fila` |
| Fuente directa | `15 / fila` |
| Experimento | `220 fijo + 5 / fila` |
| Driver histórico | `Uniforme(0,10)` |
| `corr(P,driver)` | `0.60` |
| Canales visibles | `P + 5` canales auxiliares |
| Bursts auxiliares | probabilidad `0.04` |
| Ruido de proceso | `Normal(0,1.5²)` |
| Batería | `24 × 2000`, `m_reps=2` |

Proxy estandarizado:

\[
P=0.60D_z+0.80\eta,\qquad \eta\sim N(0,1)
\]

Curva:

\[
g(d)=12+\frac{16d^3}{27+d^3}
-\frac{4}{1+\exp(-(d-8)/0.45)}
\]

Es saturante pero tiene una caída suave por alta carga. Eso evita que una saturación genérica sin datos llegue al techo y obliga a cubrir la zona alta sin introducir una estructura creativa difícil.

Plan disciplinado legal:

- 128 filas baratas: `128`.
- Experimentos iniciales en `d=2.2, 7.5`, 40 filas cada uno: `2×420=840`.
- Experimentos en `d=0.6, 3.8, 9.3`, 20 filas cada uno: `3×320=960`.
- Total: `1928 ≤ 2000`.

Ruta directa alternativa:

- 128 filas baratas + 120 directas:
  `128 + 120×15 = 1928`.

El pozo profundo que compra 1000 filas baratas queda con 1000: ni siquiera cubre los cinco costos fijos experimentales (`5×220=1100`). Esa es una consecuencia limpia. Si aun así su robot supera `R=0.60`, el mundo no certifica: no retunearía la batería para hundirlo; revisaría primero si cuatro niveles o 66 filas directas realmente bastan para recuperar `g`.
tokens used
