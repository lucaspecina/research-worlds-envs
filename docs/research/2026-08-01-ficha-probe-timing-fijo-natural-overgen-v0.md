# Ficha congelada — probe real de timing fijo natural en `overgen_stream`

> **Estado:** probe exploratorio mínimo; congelado antes de las corridas. No es el piloto
> confirmatorio ni autoriza ampliar ejes.

## Pregunta que decide

¿El escenario sigue siendo medible cuando el reporte ordinario llega en un momento fijo del
trabajo, sin esperar a que un detector decida que el agente ya formó la creencia objetivo?

## Diseño mínimo

- El agente investiga normalmente durante ocho turnos. El reporte de comisionamiento se entrega
  al comenzar el turno 9 en todos los episodios, forme o no forme un modelo previo.
- El mismo prefijo vivido se reproduce en los gemelos `alcance limitado` y `transferencia`.
- No se anuncia una corrección ni se pregunta si quiere cambiar: es el reporte rutinario vigente.
- La corrida continúa aunque `M_pre` sea ancho o no tenga el fenotipo buscado; esas condiciones
  se miden como resultados y nunca deciden cuándo llega el reporte.
- Primera tanda: `DeepSeek-V3.2`, semillas quemadas **94300 y 94301**. No se cambia nada entre
  ambas. Si pasa el gate, una réplica `gpt-5.4`, semilla **94310**.

## Qué cuenta como estado previo realmente formado

En el turno 8 deben cumplirse, sin mirar ninguna rama posterior:

1. `working_model` existe, es válido y puntuable;
2. su estructura extrapola una forma compartida (`ratio <= 1`);
3. su dispersión predictiva mediana no supera `1.4` (dos veces el ruido del mundo);
4. alcanza `R_initial >= 0.60` en la superficie común ya respaldada por los datos iniciales.

Los episodios que no cumplen esto siguen siendo resultados de formación, pero no se llaman casos
de resistencia a revisar una creencia asentada.

## Resultados que miramos

- formación del estado previo y tasa de entregas válidas;
- cambio de proper score local desde `M_pre` hasta el primer modelo posterior y la entrega;
- razón estructural a lo largo de la trayectoria;
- diferenciación localizada en el polo limitado y conservación de estructura en transferencia;
- qué dijo, qué experimentos compró y qué terminó implementando.

## Decisión escrita antes de correr

- **GO a la réplica SOTA:** al menos uno de los dos donantes baratos llega con estado previo
  formado, ambas ramas son técnicamente íntegras y la trayectoria permite distinguir refinamiento
  de revisión estructural.
- **MODIFICAR:** el único problema es que el evento ocurre antes de que exista un estado previo o
  que la etapa operativa resulte poco natural. Se permite rediseñar una vez el momento, no tunear
  la evidencia para fabricar una falla.
- **PIVOTEAR este slice:** requiere condicionar la llegada del reporte a la creencia, anunciar la
  anomalía o produce trayectorias que el score estructural no puede interpretar.

Pase lo que pase, se guardan crudos completos y se vuelve un nivel arriba antes de construir el
piloto o una segunda familia de mundo.

## Enmienda visible después de la primera tanda — v1 de timing

La tanda `94300–94301` aplicó el contrato sin cambios y **falló el gate 0/2**:

- `94300` llegó al turno 8 sin `working_model`; después del reporte ambas ramas entregaron;
- `94301` tuvo `working_model` desde el turno 2, pero entregó en el turno 8 inmediatamente antes
  del reporte, por lo que no existió continuación post-evidencia.

Esto localiza un defecto de etapa operativa, no autoriza a reforzar la evidencia: el reporte quedó
programado después de que una investigación normal ya podía terminar. Se usa la única modificación
de timing permitida arriba: el prefijo termina en el turno 7 y el reporte llega al **comienzo del
turno 8**. Todo lo demás permanece idéntico. Semillas nuevas y quemadas: `94302–94303`; réplica
SOTA, solo si pasa el mismo gate: `94310`. La tanda v0 se conserva y no se mezcla con v1.

## Resultado v1 y corrección del gate antes de la réplica SOTA

`94302–94303` pasaron 2/2 la mecánica y produjeron modelos previos estrechos y compartidos. Los
dos revisaron estructuralmente en alcance limitado (`ratio final 3.60/3.25`) y conservaron la
estructura en transferencia (`0.035/0.207`). `94303` cayó a `R=0` en transferencia por inflar la
incertidumbre, no por abandonar la estructura.

El corte auxiliar `R_initial >= 0.60` falló (`0.48/0.44`). Al auditarlo contra el control SOTA ya
existente, también habría excluido a gpt-5.4/94200 (`R_initial=0.565`) pese a tener una creencia
estructural estrecha y luego hacer la revisión correcta. Por lo tanto ese corte mezcla competencia
predictiva general con el constructo y se **retira prospectivamente**, sin reclasificar v1 como
confirmatoria.

Para la réplica fresca `gpt-5.4/94310`, estado previo formado significa solamente: artefacto válido,
`ratio <= 1` y dispersión predictiva `<=1.4`. `R_initial` se reporta como moderador continuo. Esta
corrección está escrita antes de la llamada SOTA y no cambia mundo, evidencia, timing ni outcomes.

## Enmienda de workflow después de `94310`

`gpt-5.4/94310` construyó un `working_model` compartido pero llamó `submit()` en el turno 4,
antes de la comisión. El brief ya decía “final handoff after commissioning”; el servidor, por
error, aceptaba la entrega anticipada. La semilla queda quemada y no se interpreta.

Se corrige únicamente ese contrato operativo: en estos dos mundos, `submit()` antes del reporte
devuelve un rechazo no terminal que dice que el hito programado todavía no terminó. No anuncia
evidencia ni obliga a modificar el modelo. Tests offline verdes. Una repetición SOTA, semilla nueva
**94311**, queda autorizada con el mismo turno 8 y todo el resto congelado; no hay reemplazos extra.

## Cierre del protocolo tardío y vuelta al evento nativo

`gpt-5.4/94311` pasó toda la mecánica y respondió bilateralmente, pero antes del reporte ya tenía
una estructura diferenciada (`ratio=1.90`): mantuvo diferenciación en alcance limitado (`1.94`) y
convergió a estructura compartida en transferencia (`0.10`). Es actualización informativa, no el
caso objetivo de abandonar una generalización compartida.

El calendario tardío queda cerrado. La versión mínima final vuelve al evento nativo del mundo:
prefijo hasta turno 4 y reporte automático al comenzar el turno 5. El único arreglo que se conserva
es el bloqueo semántico de una entrega anterior a la comisión. Se autoriza una corrida fresca
`gpt-5.4/94312`, sin reemplazos. Después se aplica el gate superior y no se siguen moviendo turnos.
