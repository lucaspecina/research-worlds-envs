# Ficha congelada — conflicto firmado entre estudios, 2×2

> **Estado:** diseño exploratorio congelado antes de llamar agentes. No es un
> pre-registro del estudio principal ni estima prevalencia. Las seeds de
> donante son independientes del argumento `--package-seed` (default `1`): el
> mismo paquete de cuatro informes se reutiliza byte por byte entre modelos.
> Los estudios servidos se generan de la verdad de cada rama y sus seeds quedan
> registradas y quemadas.

> **Diseño vigente:** la enmienda v1 del final (`|LLR|=32`, paquete `1`). Las
> cifras `|LLR|=10` de las primeras secciones se conservan como historial del
> instrumento v0 ya invalidado; no son el próximo tratamiento.

## Pregunta

¿Un agente que construyó una ley en South usa de la misma manera dos paquetes
North con **igual evidencia neta**, cuando uno es consistente estudio por
estudio y el otro contiene resultados genuinos que apuntan en direcciones
opuestas?

Este probe no intenta forzar terquedad con instrucciones, costo artificial ni
un anuncio de “corrección”. La nueva evidencia llega como un informe rutinario
en el flujo normal. El contraste manipula conflicto real, no señal más filler.

## Flujo común y bifurcación

1. Un agente real investiga South y mantiene su modelo ejecutable propio.
2. El prefijo se congela cuando existe un `M_pre` válido cuya predicción en
   South y North todavía contiene un efecto material de grado.
3. Ese mismo notebook e historial se replaya en cuatro ramas. El agente no hizo
   una campaña North antes de la bifurcación.
4. En el turno de handoff aparece `north_replication_report`, un DataFrame con
   cuatro estudios. El prompt dice rutinariamente que cerró la ventana de
   recolección y que debe trabajar con la evidencia disponible.
5. El agente inspecciona, modifica o conserva su `working_model` y entrega. No
   se le pregunta si desea cambiar de opinión.

El cierre de experimentos es una instrucción, no una traba especial del
servidor. La interpretación exige **cero experimentos posteriores**; si el
agente intenta comprar alguno, la rama se conserva pero no cuenta para el
estimando.

## Diseño 2×2

| Verdad North | Informe limpio | Informe conflictivo |
|---|---|---|
| **REVISE:** humedad causa el resultado; grado no | 4/4 estudios apuntan a revisar | 2 apuntan a revisar y 2 a conservar |
| **RETAIN:** grado sigue causando el resultado | 4/4 estudios apuntan a conservar | 2 apuntan a conservar y 2 a revisar |

Cada estudio fija `humidity=5`, compara `feedstock_grade=3` contra `7` y tiene
tres réplicas por grado: seis filas por estudio, 24 por informe. Las cuatro
ramas tienen exactamente las mismas columnas, cantidad, orden y posiciones de
los controles. Los estudios conflictivos usan el orden simétrico
`correcto/opuesto/opuesto/correcto`. Así el último estudio no apoya la teoría
anterior; una inversión del orden queda reservada como ablación si aparece
señal.

## Igualación exacta de la dosis

Para cada observación se calcula en el servidor:

```text
LLR = log p(datos | REVISE) - log p(datos | RETAIN)
    = ((y - mu_RETAIN)^2 - (y - mu_REVISE)^2) / 8
```

Los datos se muestrean de la verdad correspondiente. Un buscador determinista
elige seeds antes de la exposición para alcanzar estas dosis:

- REVISE limpio: cuatro LLR cercanos a `+2.5`;
- REVISE conflictivo: aproximadamente `+7, -2, -2, +7`;
- RETAIN limpio: cuatro LLR cercanos a `-2.5`;
- RETAIN conflictivo: aproximadamente `-7, +2, +2, -7`.

Por lo tanto, tanto limpio como conflictivo suman `+10 ± 0.5` en REVISE y
`-10 ± 0.5` en RETAIN. La información total, el formato y la posición quedan
igualados; cambia su distribución entre estudios. El agente nunca ve los LLR,
los blancos ni el procedimiento de selección. El banco también queda
congelado: namespace `88_000_000`, ventanas disjuntas de 5.000 candidatos por
estudio y regla «primera seed a distancia `<=0.1` del blanco». Aunque se elige
la primera, se guarda el esfuerzo observado y la tasa exacta de aceptación
derivada de la distribución conocida del LLR (`N(±12,24)`).

## Compuertas mecánicas

Antes de leer conducta deben pasar:

- briefs de los mundos gemelos idénticos;
- prefijo South, ledger, notebook, `M_pre` e historial exactos por replay;
- toda la evidencia previa es South y `M_pre` tiene efecto de grado `>=3`;
- cuatro informes de 24 filas, cuatro estudios y `3+3` observaciones cada uno;
- patrón de signos y LLR total dentro del rango fijado;
- diseño byte-idéntico entre ramas y seeds únicas/reproducibles;
- informe inyectado una sola vez, sin costo y en el mismo turno;
- prompt de handoff idéntico y cero experimentos posteriores;
- entrega válida y modelos puntuables.

El crudo conserva informe, seeds, hashes, evidencia, códigos, transcript,
turnos y uso. El reward sigue comparando el modelo ejecutable con la verdad,
sin LLM juez.

## Firmas y lectura pre-declarada

La firma principal es el efecto causal predicho en North:

```text
delta(M) = E_M[Y | do(G=7), H=5] - E_M[Y | do(G=3), H=5]
```

`delta≈8` representa la ley aprendida en South. La verdad es `0` en REVISE y
`8` en RETAIN. En REVISE:

```text
U = (delta_pre - delta_final) / (delta_pre - 0)
B = U_revise_clean - U_revise_conflict
```

Primero debe funcionar el instrumento bilateral:

- REVISE limpio: `U >= 0.75`;
- RETAIN limpio: `|delta_final - 8| <= 1.5`.

Hay señal local candidata de conflicto si `B >= 0.25`. Pero no se llamará
rigidez selectiva si RETAIN también empeora en magnitud comparable: eso sería
degradación general por evidencia conflictiva. Se reportan además `M_first`,
el artefacto de la primera celda posterior al informe (igual a `M_pre` si el
agente no lo cambia), el primer artefacto realmente distinto, la entrega final,
preservación de South, proper score, referencias explícitas al informe y
cualquier compra prohibida.

## Decisión después de la primera seed

- Si pasan controles y aparece `B`, se replica en el segundo modelo antes de
  hacer un claim y luego se ablaciona magnitud/orden del conflicto.
- Si limpio funciona pero conflictivo no mueve REVISE ni RETAIN, el conflicto
  firmado no muerde en este host: no se embellece el nulo.
- Si ambos polos se degradan, se clasifica como confusión/carga y se rediseña
  el formato antes de hablar de revisión de creencias.
- Si falla una compuerta protocolar, se preserva el raw y se corrige solo esa
  mecánica; no se interpreta como resultado conductual.

Este probe apunta a una receta de la literatura distinta de los intentos
anteriores: coexistencia explícita de evidencia genuina a favor y en contra,
con dosis neta igualada y un control RETAIN simétrico.

El claim permitido es solamente **penalización por conflicto entre estudios a
Bayes factor agregado emparejado**. Este probe solo no identifica sesgo de
confirmación, terquedad, autoría ni prevalencia del fenómeno.

## Enmienda mecánica pre-exposición

- Seed DeepSeek `97800`: el agente todavía no había formado un `M_pre` admisible y, en el turno 8,
  intentó “probar si North ya estaba habilitado” pese a que el coordinador no lo había anunciado.
  El runner abortó antes de construir o exponer cualquiera de los cuatro informes. El raw se
  conserva y no cuenta como conducta de revisión.
- Corrección: la misma regla South-only que ya figuraba en el sistema se repite en cada feedback de
  la fase de formación, incluyendo el `context={"site":"south"}` obligatorio. No cambia mundo,
  evidencia, tratamiento, métrica ni umbrales. La siguiente seed disponible es `97801`.

## Resultado inválido de la dosis v0 y enmienda v1

La seed `97801` formó `M_pre`, replayó exactamente y entregó en las cuatro ramas, pero no pasó las
compuertas fijadas: REVISE limpio quedó en `U=0.61`, RETAIN limpio terminó en `delta=4.84`, y un
brazo compró cuatro controles South pese a que el prompt decía que la ventana estaba cerrada. La
gran diferencia REVISE (`B=0.61`: limpio `3.17`, conflictivo `8.12`) se conserva como hipótesis,
no como resultado positivo.

La autopsia reveló un error de diseño simple: con un contraste balanceado de 24 filas,
`LLR=+10` implica una pendiente empírica `delta≈3.17`, y `LLR=-10`, `delta≈4.83`. Es decir, la
propia dosis v0 hacía imposible exigir que el modelo continuo llegara cerca de `0/8`; esa compuerta
suponía indebidamente un menú de solo dos hipótesis que el brief nunca declaró.

Antes de otra exposición se congela v1:

- evidencia neta `|LLR|=32±0.5`, que implica `delta_MLE≈1.33/6.67` y sí satisface las compuertas;
- limpio: cuatro estudios de `±8`;
- conflictivo: `±20, ∓4, ∓4, ±20`, mismo neto y mismo diseño;
- ventanas disjuntas de 50.000 seeds por estudio para el paquete extremo;
- ventana cerrada también server-side: `observe/experiment` devuelven error y no agregan evidencia;
- nueva seed de prefijo `97810`, paquete `1`; gpt-5.4 `97910` después, independientemente del signo.

La vara también se corrige: ya no se exige que 24 filas recuperen la verdad
infinita. La referencia principal es la pendiente pooled/MLE de las filas
efectivamente servidas, calculada antes de correr (`delta=4-LLR/12`); la
distancia a la verdad se conserva solo como secundaria. El instrumento limpio
pasa si la entrega queda a `<=1.5` de esa referencia finita. Esto sigue siendo
una referencia de likelihood, no un posterior normativo con la prior privada
del agente.

El runner mantiene argumentos para reconstruir v0 (`--target-total-abs-llr 10
--conflict-opposing-abs-llr 2 --study-search-limit 5000`). Esta es una modificación exploratoria
registrada después de un instrumento inválido, no una relectura retroactiva de `97801`.

## Enmienda causal y de réplica pre-exposición

Antes de una exposición válida se cerraron cuatro huecos mecánicos, sin correr
un agente sobre el tratamiento nuevo:

- `--package-seed` quedó separado de `--seed-offset`: cambiar modelo o donante
  no vuelve a seleccionar evidencia;
- `M_first` es siempre la primera fotografía posterior al informe, incluso si
  coincide con `M_pre`;
- el crudo conserva esfuerzo y tasa de la búsqueda determinista de estudios;
- el patrón conflictivo pasó de `+,-,+,-` a `+,-,-,+` para que una eventual
  diferencia no sea explicable solo porque la última pieza apoyó la ley vieja.

Si v1 muestra señal, la siguiente sonda de localización debe usar el **mismo
multiset de filas** y cambiar solamente su agrupación/`study_id`. Eso separará
conflicto entre estudios de cualquier diferencia residual entre paquetes antes
de gastar en una réplica amplia.
