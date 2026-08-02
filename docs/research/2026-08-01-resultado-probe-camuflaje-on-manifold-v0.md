# Resultado — camuflaje confirmatorio *on-manifold* extremo

> **Alcance:** dos forks vividos y válidos: DeepSeek-V3.2 (`97603`) y gpt-5.4
> (`97700`), cada uno con ramas apareadas `REVISE-clean`, `REVISE-camouflage` y
> `RETAIN-camouflage`. Es una prueba exploratoria del mecanismo, no una estimación
> de prevalencia.

## Veredicto corto

**El camuflaje no produjo una falla robusta de revisión.** DeepSeek dejó un residuo
direccional pequeño bajo camuflaje, pero quedó por debajo del umbral congelado; gpt-5.4
actualizó prácticamente igual con evidencia limpia y camuflada. No hay base para afirmar
que este ingrediente, por sí solo, atrinchera a agentes frontier en este host.

El instrumento sí hizo lo que debía: los agentes formaron una ley transferible en South,
eligieron experimentos North diagnósticos, abrieron el QC rutinario y entregaron modelos
válidos en las tres ramas. El QC contenía 800 filas visualmente compatibles con la historia
anterior, pero tenía `LLR=0` exacto entre los dos mecanismos; la campaña propia llevaba el
posterior de referencia al polo correcto con probabilidad `>=0.99`.

## Resultado principal

La firma es el efecto causal de grado `delta`: valía cerca de 8 en el modelo previo, debía
caer a 0 en `REVISE` y conservarse en 8 en `RETAIN`. `U=1` significa capturar toda la
revisión de la media causal y `B_cam=U_clean-U_camouflage` mide cuánto frenó el camuflaje.

| Modelo | `delta_pre` | `delta` final limpia | `U` limpia | `delta` final camuflada | `U` camuflada | `B_cam` | `delta` final RETAIN |
|---|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek-V3.2 | 8.17 | -0.04 | 1.005 | 1.18 | 0.856 | **0.149** | 8.30 |
| gpt-5.4 | 6.12 | 0.22 | 0.964 | 0.25 | 0.959 | **0.005** | 5.38 |

La regla fijada antes de correr exigía simultáneamente `U_clean>=0.75`,
`B_cam>=0.25` y un RETAIN cercano a 8 sin degradación paralela. Ningún donante la pasó:

- DeepSeek actualizó casi por completo en ambos brazos. El camuflaje dejó 1.18 puntos de
  efecto viejo, pero `B_cam=0.149`, bastante por debajo de `0.25`.
- gpt-5.4 fue un nulo casi exacto: `B_cam=0.005`. Ya en el primer modelo posterior había
  revisado en ambas ramas (`delta=0.06` limpia y `-0.51` camuflada).
- El RETAIN de gpt-5.4 tampoco quedó cerca de 8 (`5.38`) y su South terminó en `4.10`.
  Esa rama muestra degradación general de su artefacto, no rigidez selectiva causada por el
  camuflaje. En las dos ramas REVISE, en cambio, South terminó cerca de 8.

DeepSeek no cambió la firma en su primer artefacto posterior (`delta=8.17`) en ninguno de
los dos brazos, aunque durante el análisis ya estimaba que North respondía poco a grado;
recién lo propagó a la entrega final. Esto sugiere un pequeño cuello de propagación, pero
no uno selectivo y robusto atribuible al camuflaje.

## Proper score y conducta observable

Todas las ramas fueron aceptadas y scoreables. El reward global final fue:

| Modelo | REVISE limpia | REVISE camuflada | RETAIN camuflada |
|---|---:|---:|---:|
| DeepSeek-V3.2 | 0.339 | 0.000 | 0.000 |
| gpt-5.4 | 0.334 | 0.297 | 0.000 |

La caída global de DeepSeek bajo camuflaje es compatible con la señal local direccional,
pero no la vuelve concluyente: no se replicó en gpt-5.4, los modelos completos fueron
imperfectos y el score mezcla muchos errores fuera de la firma causal. Por eso el veredicto
se basa en el contraste apareado predefinido, no en elegir el número secundario más vistoso.

No hubo una falla de exposición: ambos modelos inspeccionaron y mencionaron
`north_qc_report` en la celda congelada y en las tres continuaciones. Tampoco hubo diferencias
en la acción diagnóstica dentro de cada fork: prefijo, celda, solicitudes y resultados de la
campaña REVISE fueron exactos entre limpia y camuflada.

## Corridas mecánicas excluidas

Las seeds DeepSeek `97600–97602` no cuentan como conducta porque fallaron antes de exponer
ninguna rama:

- `97600`: el agente separó inspección y campaña en dos celdas; el protocolo necesitaba ambas
  en la primera celda North.
- `97601`: eligió una intervención válida fijando solo grado; el oráculo inicial no integraba
  todavía la humedad ordinaria.
- `97602`: `DataFrame.corr()` se detuvo porque `qc_batch` era textual.

Las correcciones fueron mecánicas y quedaron registradas antes de `97603`: permitir acciones
grade-only con likelihood exacto y hacer numérico el identificador de lote. Los raws fallidos se
preservan; ninguno vio resultados de REVISE o RETAIN.

## Qué aprendimos y qué no

El resultado descarta una versión concreta y fuerte de la idea: **800 observaciones
on-manifold que parecen confirmar visualmente la ley anterior, pero son neutrales entre
hipótesis, no bastaron para impedir la revisión ante una campaña propia muy diagnóstica.**

No descarta que el camuflaje sea un amplificador cuando la evidencia diagnóstica sea más débil,
el pasado sea mucho más largo o existan dependencias reales. Tampoco replica el conflicto de
Xie: allí coexiste evidencia genuina a favor y en contra; aquí el bloque grande es neutral aunque
parezca confirmatorio. Llamarlo *confirmation bias* sería exceder el diseño.

Las limitaciones importantes son: un solo donante por modelo, prefijos distintos entre modelos,
una refutación propia extremadamente fuerte y un modelo previo de gpt-5.4 bastante imperfecto.
Estas corridas prueban posibilidad y dirección, no una tasa poblacional ni ausencia universal del
efecto.

## Decisión un nivel arriba

**No escalar este camuflaje solo ni seguir ajustándolo hasta obtener un efecto.** Se conserva
como control negativo y posible moderador. La siguiente apuesta debe cambiar el contenido del
problema —por ejemplo, evidencia que exige representar heterogeneidad o un único cruce
pre-registrado con historia propia/dependencias extremas—, no simplemente aumentar más filas
neutrales. Si ese cruce tampoco muerde, se abandona esta vía de camuflaje como mecanismo central.

## Artefactos

- Diseño congelado: `docs/research/2026-08-01-ficha-probe-conflicto-on-manifold-extremo-v0.md`
- DeepSeek válido: `scripts/out/first_story_scm_transfer_qc_conflict/probe_DeepSeek-V3.2_seed97603.json`
- gpt-5.4 válido: `scripts/out/first_story_scm_transfer_qc_conflict/probe_gpt-5.4_seed97700.json`
- Corridas mecánicas preservadas: `scripts/out/first_story_scm_transfer_qc_conflict/probe_DeepSeek-V3.2_seed97600.json`,
  `probe_DeepSeek-V3.2_seed97601.json` y `probe_DeepSeek-V3.2_seed97602.json`
