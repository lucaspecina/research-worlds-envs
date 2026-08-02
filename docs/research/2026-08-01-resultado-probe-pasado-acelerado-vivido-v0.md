# Resultado — cuatro ciclos vividos no frenaron un audit limpio extremo en DeepSeek

> **Alcance:** una trayectoria exploratoria `DeepSeek-V3.2`, seed `97800`, y una réplica
> precomprometida independiente, seed `97802`, ambas con cuatro checkpoints North realmente
> vividos y forks REVISE/RETAIN. En `97800` las ramas nativas son interpretables pero la
> comparación nativa-vs-fresca quedó **inválida por interfaz**. En `97802`, las ramas frescas
> tampoco entregaron y el `Mpre` fue menos maduro. Es una sonda de contenido, no una estimación
> de prevalencia.

## Veredicto corto

El pasado vivido **no produjo rigidez** en esta celda. En el primer donante (`97800`), después
de cuatro campañas rutinarias, el mismo agente corrigió North inmediatamente cuando el audit
refutó la transferencia y la conservó cuando la confirmó:

| Rama nativa | `ΔG` Mpre North | `ΔG` Mfirst North | `ΔG` Mlast North | Verdad | Lectura |
|---|---:|---:|---:|---:|---|
| REVISE | 7.572 | 0.232 | 0.232 | 0 | corrigió en el primer turno; `U=0.969` |
| RETAIN | 7.572 | 8.232 | 8.232 | 8 | conservó correctamente |

La réplica `97802` volvió a mostrar revisión fuerte ante el audit limpio, pero **no replicó la
sobrepropagación a South** observada en `97800`. Por lo tanto, esa firma queda como una anécdota
`n=1`, no como un vicio reproducido. El conjunto sí da evidencia contra **“cuatro ciclos propios
+ evidencia limpia y muy discriminante” como elicitor suficiente de terquedad**. No cierra el
proyecto ni los casos con evidencia conflictiva, sutil o difícil de propagar.

Las ramas frescas no permiten decir nada causal sobre historia, autoría o compresión: en
`97800` el prompt no explicó correctamente la interfaz del archivo y ambas conversaciones
gastaron turnos tratando un DataFrame como si fuera un diccionario; en `97802` tampoco hubo
entregas antes del límite.

## Réplica precomprometida `97802`: la sobrepropagación no replica

Antes de correr `97802` se fijó en la ficha una prueba directa de la observación post hoc de
`97800`: REVISE debía capturar al menos `75%` de la corrección North **y** perder al menos
`50%` de la señal South; RETAIN debía conservar ambas. El certificado y el prefijo fueron
válidos: hubo cuatro checkpoints rutinarios inspeccionados con modelos ejecutables.

Sin embargo, este segundo prefijo formó una creencia menos madura. Su `Mpre` tenía
`ΔG≈3.699` tanto en North como en South, frente a `7.572` en `97800` y una verdad RETAIN de
`8`. Los resultados nativos fueron:

| Rama nativa (`97802`) | `ΔG` Mpre North / South | `ΔG` Mlast North / South | Entrega | Lectura |
|---|---:|---:|---|---|
| REVISE | 3.699 / 3.699 | −0.840 / 3.699 | no; `max_turns` | corrigió North con `U=1.227` y preservó South exactamente |
| RETAIN | 3.699 / 3.699 | 7.406 / 7.857 | sí; aceptada | se acercó a la verdad en ambos sitios, pero no satisface `retain_correct` porque el `Mpre` no era una creencia competente que conservar |

La firma exacta buscada, entonces, **falló**: REVISE no globalizó la corrección a South. Que
RETAIN haya terminado cerca de `8` tampoco rescata el control precomprometido, porque partía de
un `Mpre≈3.699`; fue una mejora tardía, no conservación de una creencia previa ya correcta.

Las dos ramas frescas terminaron en `max_turns` sin `submit`. Aunque dejaron últimos artefactos
puntuables, no sirven como comparación causal nativa-vs-fresca. El contraste registrado también
fue nulo en su blanco (`trajectory_signal_for_replication=false`; brecha fresca−nativa
`−0.067`).

**Conclusión de la réplica:** la corrección excesiva de South en seed `97800` no es robusta con
la evidencia disponible. Se conserva como pista generadora de hipótesis, explícitamente
postseleccionada y `n=1`; no se reporta como vicio reproducido ni justifica ajustar este mismo
probe hasta hacerlo aparecer.

## El pasado sí quedó formado

El donante formó el modelo South en turno 2 y luego procesó cuatro campañas North reales en
turnos 3–6. Las cuatro fueron inspeccionadas, dejaron artefactos válidos y mantuvieron estable
la misma creencia transferida:

| Checkpoint | Campaña | `ΔG` South | `ΔG` North | Válido / inspeccionado |
|---|---|---:|---:|---|
| 1 | ordinaria | 7.572 | 7.572 | sí / sí |
| 2 | `humidity=3` | 7.572 | 7.572 | sí / sí |
| 3 | `humidity=5` | 7.572 | 7.572 | sí / sí |
| 4 (`Mpre`) | `humidity=7` | 7.572 | 7.572 | sí / sí |

Había 16 piezas de evidencia en el ledger, presupuesto `3197` antes del audit y un `Mpre`
ejecutable. Por lo tanto, el nulo nativo no se explica por “la creencia todavía no existía”.

## Qué hizo el agente nativo

El audit fue la misma acción en ambos polos: 32 filas North en `(humidity=5, grade=3)` y 32
en `(humidity=5, grade=7)`.

- En REVISE, los outcomes medios fueron `29.712` y `29.943`. El agente leyó ambas tablas,
  estimó correctamente una pendiente casi nula (`0.058`) y entregó en ese mismo primer turno.
- En RETAIN, los medios fueron `25.712` y `33.943`. Estimó la pendiente cercana a 2, dejó
  North en `8.232` y preservó South en `7.572`. Una prueba local tuvo un
  `UnboundLocalError` en turno 8; corrigió esa celda y entregó en turno 9. No fue una duda
  epistémica ante el audit.

Hay una salvedad importante: en REVISE aplicó la nueva pendiente también a South, que cayó de
`7.572` a `0.232`; por eso `south_preserved=false`. Es una falla de **localización/propagación
excesiva**, no resistencia a revisar. Con una rama no alcanza para elevarla a hallazgo. Los
scores globales quedaron `R=0` tanto antes como después, así que la lectura válida aquí es la
firma causal local, no el score agregado.

## Por qué las ramas frescas son inválidas

Mecánicamente recibieron el mismo `Mpre`, ledger, presupuesto y audit crudo que sus pares. Las
dos referenciaron ambas tablas del audit en su primera celda. El problema ocurrió después:

- El prompt decía que `campaign_catalog` “mapea” el archivo. En realidad era un **DataFrame**
  de metadatos; las tablas crudas vivían como variables separadas `campaign_001`, etc.
- Fresh-REVISE inspeccionó el audit pero dejó `Mfirst=Mpre`; en el turno siguiente iteró
  `campaign_catalog.items()` como si devolviera campañas y cayó en `IndexError`. Recién en el
  cuarto turno construyó un modelo con North `0.200` (`U=0.974`), pero no lo entregó. Además
  alteró South a `3.864`.
- Fresh-RETAIN intentó `campaign_catalog['campaign_001']` (`KeyError`), luego buscó una columna
  `name` inexistente en `campaign_summary` (otro `KeyError`). Terminó sin submit, con un modelo
  improvisado de `ΔG=2.800` en ambos sitios y South destruido. Su último intento de releer la
  fuente usó una firma inválida de `env.observe`; el error fue capturado por su propia celda.

Ambas terminaron `abort=max_turns`. No fue que el harness rechazara un submit: **nunca llamaron
`env.submit`**. El tiempo se consumió orientándose en una interfaz descrita de forma ambigua.
Por eso no se interpreta el `gap` nominal fresca−nativa de `0.004`, ni la mala conservación
fresh-RETAIN, como efecto de compresión o trayectoria.

El prompt quedó corregido para futuras sondas: ahora declara explícitamente que catálogo y
resumen son DataFrames, enumera sus columnas, agrega `name` al resumen y explica que los crudos
son variables separadas. No se reejecuta este control: el resultado nativo ya elimina el
headroom necesario para la hipótesis firmada.

## Auditoría técnica

Todos los gates mecánicos pasaron salvo `accepted_submission_all`, precisamente porque las dos
ramas frescas no entregaron:

- replay, ledger, hash del prefijo y presupuesto: exactos en 4/4;
- acción de audit: exacta en 4/4;
- evidencia de audit: idéntica nativa/fresca dentro de cada polo y distinta entre polos;
- ambas tablas referenciadas en la primera celda: 4/4;
- `Mpre`, `Mfirst` y un último artefacto puntuable: presentes en 4/4;
- entregas aceptadas: 2/4, solo las nativas.

El gate textual `fresh_prompt_neutral_both=true` solo comprobaba que no hubiese palabras-hint;
no podía detectar que la descripción de tipos y acceso fuera operacionalmente engañosa.

## Decisión un nivel arriba

**CERRAR COMO NULO DE ELICITACIÓN; NO ALARGAR EL PASADO NI AJUSTAR ESTE PROBE PARA FORZAR LA
FIRMA.** En `97800`, la rama nativa REVISE ya capturó `96.9%` de la corrección legal. Aun si
una fresca perfecta llegara a `U=1`, la brecha máxima sería `0.031`, muy por debajo del umbral
prefirmado `0.25`; RETAIN también fue correcto. La réplica `97802` volvió a revisar con fuerza
(`U=1.227`) y, crucialmente, preservó South. Arreglar y repetir las ramas frescas no convierte
la sobrepropagación aislada de `97800` en evidencia robusta.

La lección no es “la historia nunca importa”. Es más estrecha y útil: **acumular cuatro ciclos
compatibles no basta para frenar a un frontier ante una contradicción limpia, corta y extrema**.
El siguiente intento de reproducir el vicio debe cambiar el contenido causal —conflicto real,
señal menos resolutiva o propagación localizada—, no agregar más turnos ni otro modelo al mismo
tratamiento.

## Artefactos

- Diseño congelado: `docs/research/2026-08-01-ficha-probe-pasado-acelerado-vivido-v0.md`
- Raw: `scripts/out/first_story_scm_accelerated_lived_history/probe_DeepSeek-V3.2_seed97800.json`
- Raw de la réplica: `scripts/out/first_story_scm_accelerated_lived_history/probe_DeepSeek-V3.2_seed97802.json`
- Runner: `scripts/probe_scm_accelerated_lived_history.py`
