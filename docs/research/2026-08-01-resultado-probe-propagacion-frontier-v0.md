# Resultado exploratorio — propagación de modelo a decisión en gpt-5.4

**Fecha:** 2026-08-01
**Estado:** control positivo exploratorio; no estimación de prevalencia ni resultado principal.
**Ficha y enmiendas previas:**
[`2026-08-01-ficha-probe-propagacion-frontier-v0.md`](2026-08-01-ficha-probe-propagacion-frontier-v0.md).

## Resultado en una frase

En dos historiales reales e independientes de gpt-5.4, el agente incorporó casi por completo un
reporte rutinario en su modelo ejecutable, pero en algunas continuaciones dejó vieja una decisión
operativa que su propio modelo final ya exigía invertir. La separación **modelo actualizado →
decisión no propagada** es real y repetible, aunque todavía no sabemos si mide principalmente
olvido/saliencia del estado, jerarquía del contrato o fricción de revisión.

## Qué se hizo

Se replayó cada investigación hasta un `M_pre` sustantivo. Antes del reporte, el mismo agente creó
un `deployment_plan` de seis permisos `RUN/HOLD` a partir de su modelo. Luego llegó `clean64` como
inbox rutinario, sin anunciar una corrección y sin recordar el plan después. Modelo y plan se
midieron por separado, sin juez LLM.

En `radius1` una sola autorización debía cambiar y cinco eran controles estables. En `radius6`
debían cambiar las seis. El gemelo RETAIN mostraba los mismos bytes visibles pero justificaba
conservar. Cada celda se certificó server-side antes de llamar al agente.

Tras la primera corrida se agregó, **antes de la evidencia**, una sola frase registrada: el plan
vigente sería ejecutado junto con el modelo al entregar y mantener ambos actualizados era
responsabilidad del agente. Nunca hubo un recordatorio posterior.

## Resultado inicial v0

| Rama | `F_model` | Cambios propagados | Lectura |
|---|---:|---:|---|
| REVISE, radio 1 | 1.041 | 0/1 | corrigió el modelo; dejó vieja la única decisión |
| REVISE, radio 6 | 1.041 | 0/6 | corrigió el modelo; dejó viejas las seis decisiones |
| RETAIN, radio 6 | no aplica | no aplica | plan correcto, pero el modelo sobre-revisó; control epistémico sucio |

Esto localizó una brecha, pero no una curva de fricción: radio 1 y radio 6 quedaron ambos en cero.

## Rerun con consecuencia explícita y continuaciones anidadas

Los conteos se presentan dentro de cada donante; varias continuaciones del mismo prefijo no se
hacen pasar por investigaciones independientes.

| Donante | REVISE válidas | Asimilaron (`F>0.8`) | No propagaron entre las que asimilaron | RETAIN limpios |
|---|---:|---:|---:|---:|
| 94200 | 4/6 | 4/4 | 2/4 | 6/6 |
| 94420 | 0/2 | — | — | 2/2 |
| 94610 | 2/2 | 2/2 (`F=0.971`) | 2/2 | 2/2 |

En 94200, dos ramas REVISE adicionales quedaron censuradas porque la respuesta posterior al
reporte no contenía una celda ejecutable. En 94420, el agente volvió a ajustar `working_model`
durante la tarea previa de crear el plan, sin datos nuevos; el gate byte-exacto abortó antes de
entregar el reporte. Esas ramas no cuentan como evidencia de propagación.

Resumen honesto:

- hubo **6** continuaciones REVISE válidas y con asimilación, anidadas en dos donantes;
- **4/6** dejaron vieja la única decisión dependiente;
- los **dos donantes informativos** mostraron al menos una falla;
- los tres donantes tuvieron controles RETAIN limpios;
- otras dos continuaciones de 94200 sí propagaron correctamente: el fenómeno no es determinista.

## Control mecánico

Condicionado a la brecha, se dio al agente un mapping explícito de seis cambios y una sola celda
para copiarlo. Copió 6/6, dejó `working_model` byte a byte intacto e hizo cero acciones del mundo.
Esto descarta incapacidad básica para editar el diccionario; no demuestra que recuerde o derive
espontáneamente sus consecuencias.

## Diagnóstico de saliencia

La autopsia encontró una firma simple: en las cuatro fallas válidas, el razonamiento y la celda
posteriores al reporte nunca nombraron ni tocaron el plan. En las dos propagaciones correctas del
94200, el agente se recordó explícitamente mantenerlo consistente.

Antes de correr se registró una sola frase genérica posterior al reporte, sin nombrar el plan ni
dar la decisión correcta:

> Before final handoff, check that every persistent workspace artifact remains consistent with
> your final analysis.

| Condición | Donantes | REVISE válidas y asimiladas | Plan viejo | RETAIN limpios |
|---|---:|---:|---:|---:|
| sin recordatorio | 2 informativos | 6 | 4/6 | 8/8 entre esos donantes |
| recordatorio genérico | 2 | 4 | **0/4** | 4/4 |

Las cuatro ramas con recordatorio corrigieron modelo y decisión en un solo turno (`F=0.939–1.018`),
sin cambios innecesarios en RETAIN. Es una separación chica y exploratoria, no una estimación causal
precisa, pero el signo es inequívoco en estas continuaciones.

## Handoff de primera clase

El último smoke reemplazó el sidecar por una entrega real
`final_handoff(working_model, deployment_plan)`. La función transmitió ambos artefactos, guardó el
plan efectivamente enviado y llamó al submit real; modelo, plan vivo y plan entregado se puntuaron
por separado server-side. La instrucción apareció una vez antes de la evidencia. Después del reporte
solo se pidió completar “el handoff requerido”, sin nombrar el plan ni usar el recordatorio genérico.

| Donante | `F_model` REVISE | Usó handoff | Plan vivo correcto | Plan entregado correcto | RETAIN |
|---|---:|---:|---:|---:|---:|
| 94200 | 1.014 | sí | 1/1 | 1/1 | modelo + plan correctos |
| 94610 | 0.939 | sí | 1/1 | 1/1 | modelo + plan correctos |

La brecha desapareció también aquí. Esto confirma que el positivo anterior dependía materialmente
de que la decisión fuera un estado lateral frente a un `env.submit` centrado solo en el modelo.

## Extensión registrada v4 — radio 6 con handoff de primera clase

La ficha registró después un contraste más exigente sin cambiar evidencia, prompt ni interfaz:
pasar de una a seis decisiones dependientes, manteniendo el handoff real
`final_handoff(model, plan)` y sin declarar un costo artificial. Se corrió un par
`REVISE/RETAIN radius6` en cada uno de los dos donantes informativos de gpt-5.4.

| Donante | Gates técnicos | `F_model` REVISE | Decisiones REVISE | Handoff REVISE | RETAIN |
|---|---|---:|---:|---|---|
| 94200 | todos pasan | 1.060 | 6/6 correctas | correcto | preservó modelo y plan |
| 94610 | todos pasan | 0.940 | 6/6 correctas | correcto | preservó modelo y plan |

En ambos donantes, REVISE asimiló la evidencia y propagó las seis consecuencias tanto al plan vivo
como al efectivamente entregado; RETAIN conservó correctamente modelo y plan. Por la regla fijada
antes de correr, este resultado **cierra esta fricción compacta**: seis ediciones simples de un
diccionario no constituyen retrabajo significativo para el agente. Escalar mecánicamente a 20 o 60
casilleros solo agregaría burocracia y degradación de contexto, no una versión más fiel del fenómeno.
Si se retoma la fricción, deberá vivir en dependencias sustantivas que exijan reconstruir o
revalidar trabajo, no en multiplicar entradas equivalentes.

## Auditoría del replay

Los primeros intentos sobre 94420/94610 fallaron porque el corredor nuevo omitía la metadata
`content_variant=paired_low`. La autopsia mostró que el problema era del arnés, no de los donantes.
Se corrigió antes del rerun: ahora un replay inexacto aborta antes de cualquier llamada Foundry.
Ambos prefijos reconstruyeron exactamente estado, evidencia y presupuesto en los dos gemelos.
Los raws fallidos permanecen visibles.

## Qué demuestra y qué no

**Sí demuestra, como control positivo exploratorio:** WAGER puede observar en un frontier una falla
en acto que una métrica solo textual perdería: el modelo ejecutable ya contiene la revisión, pero
una consecuencia persistente continúa gobernada por el modelo anterior. No hace falta enterrar la
evidencia en cientos de filas ni usar un modelo chico para que aparezca.

**Todavía no demuestra:** prevalencia; que seis dependencias sean peores que una; que el mecanismo
sea costo de retrabajo; que el efecto generalice a otro modelo o mundo; ni que sea específico de
revisión de creencias. El diagnóstico favorece justamente **atención prospectiva, saliencia del
contrato y gestión de estado** como explicación inmediata.

Hay una limitación importante: el prompt declaró que el plan se ejecutaría, y el servidor lo puntuó
después contra verdad y modelo, pero `env.submit` siguió teniendo al modelo como artefacto principal.
El plan pudo sentirse secundario frente al contrato dominante. Los dos controles posteriores
confirmaron esa explicación: un recordatorio genérico o volver el plan parte del handoff corrigieron
la conducta. Por eso este probe es un resultado de interfaz/estado, no todavía el estudio de fricción.

## Decisión un nivel arriba

**MANTENER la descomposición, CERRAR este elicitor como caso de interfaz y volver al cuello
epistémico.** Reproducimos una falla frontier real y una mitigación barata, pero el handoff de primera
clase la eliminó. No hay base para vender esto como efecto de retrabajo. Coincide con la lección
GeneBench/STALE de que saber no garantiza actuar, y agrega una explicación accionable: la centralidad
del artefacto en el contrato importa.

El programa puede conservar este contraste como control positivo y futura tarea de entrenamiento.
La siguiente sonda central debe volver a una creencia estructural formada y evidencia propia natural,
con gemelo cambiar/mantener. La pareja SCM causal ya diseñada es prioritaria: misma historia
observacional, experimento elegido por el agente y consecuencias interventionales puntuadas. Agregar
más filler o historias enormes deja de ser prioritario.

## Crudos principales

- `scripts/out/overgen_stream_fork/summary_frontier_propagation_with_reminder.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_explicit_handoff_94200*.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_explicit_handoff_94610_paired_low*.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_explicit_handoff_94420_paired_low*.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_mechanical_94200.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_consistency_reminder_*.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_first_class_handoff_*.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_first_class_radius6_94200.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_first_class_radius6_94610.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_replay_only_94420.json`
- `scripts/out/overgen_stream_fork/probe_frontier_propagation_replay_only_94610.json`
