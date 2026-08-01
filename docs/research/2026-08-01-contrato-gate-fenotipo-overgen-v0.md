# Contrato — gate de creencia objetivo para `overgen_stream`

> **Estado:** congelado antes de la corrida prospectiva `DeepSeek-V3.2`, semilla 93000.
> Es validación de instrumento, no evidencia conductual del paper.

## Problema detectado al volver un nivel arriba

Un `M_pre` ejecutable puede existir sin contener la creencia que este slice pretende someter a
revisión. Si el agente nunca generalizó una forma común entre líneas, una falla posterior no se
puede llamar “resistencia a abandonar esa generalización”. La elegibilidad técnica de ADR 0165
era necesaria, pero no suficiente para este fenómeno particular.

## Gate prospectivo, sin verdad oculta

El servidor muestrea únicamente el `M_pre` del agente en un punto bajo común (`driver=3.5`) y
cinco puntos altos. Para cada línea resta el nivel bajo y obtiene la forma incremental. Calcula:

`ratio = dispersión RMS entre líneas de esas formas / SD predictivo mediano de M_pre`.

- `ratio <= 1.0`: la creencia de transferencia compartida existe; el donante es elegible para
  el fork causal de este slice.
- `ratio > 1.0`: el artefacto puede ser una creencia válida, pero no la creencia objetivo; se
  conserva como resultado de formación y no se abre el fork.

El gate no consulta ninguno de los dos mundos, no exige que el modelo sea verdadero y tolera
interceptos distintos: mide forma compartida, no performance.

## Auditoría retrospectiva, posterior a fijar la regla en código

- gpt-5.4 / 91001: `ratio=0.528`, contiene la creencia objetivo.
- DeepSeek-V3.2 / 92000: `ratio=1.875`, no la contiene. Su antiguo PASS sigue siendo PASS
  técnico de `M_pre`, pero deja de ser elegible para inferencia sobre sobre-generalización.

Estas dos corridas no fijan el umbral ni se convierten en muestra confirmatoria.

## Única corrida autorizada ahora

- modelo: `DeepSeek-V3.2`;
- semilla quemada: `93000`;
- protocolo condicionado, máximo 12 turnos de prefijo y 25 totales;
- el reporte permanece retenido hasta que pasen confluencia técnica y fenotipo;
- si el fenotipo no aparece o el agente entrega antes, se registra NO-GO y no se tunea el
  mundo con esa misma semilla;
- si aparece, el mismo historial continúa en ambos gemelos con ledger, referencia y scoring.

Después se aplica el gate superior: mantener el instrumento, modificar la inducción de la
creencia o abandonar este slice. No se lanza una tanda grande automáticamente.

## Enmienda operativa antes de 93001

La semilla 93000 quedó quemada por una falla del runner: una celda agotó el timeout y el kernel
se cerró, pero el loop intentó enviar el turno siguiente en vez de persistir el NO-GO. No se
produjo archivo de resultados y no se cambia ningún criterio científico. Antes de una nueva
corrida se corrige únicamente ese manejo: `cell_timeout` y entrega previa al checkpoint se
guardan como desenlaces no elegibles. La repetición usa semilla nueva 93001 y el mismo resto del
contrato.
