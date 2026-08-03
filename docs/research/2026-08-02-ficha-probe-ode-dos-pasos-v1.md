# Ficha congelada — probe ODE con revisión en dos pasos v1

**Estado:** diagnóstico exploratorio registrado antes de la primera llamada. Usa
seed fresca; no es confirmación del paper ni estimación de prevalencia.

> **Enmienda de instrumento, antes de la corrida interpretable:** la seed 3 quedó
> quemada en formación. Su modelo era una interpolación monótona competente de A,
> pero el ajustador sobre sus predicciones deterministas llamó “segunda fase” a un
> escalón que explicaba solo `4.7%` del plateau. No se abrió ninguna rama. Para no
> confundir microcurvatura numérica con el pivote objetivo, desde ahora una segunda
> fase del artefacto cuenta como estructural solo si representa al menos `15%` del
> plateau. El umbral queda fijado antes de la próxima seed; la verdad STRUCT está
> en torno a `41%`. La selección BIC/CV/holdout de la **evidencia** no cambia.

> **Cierre de formación:** la siguiente seed (4) también quedó censurada sin abrir
> ramas: modeló A competentemente, pero antes de recibir B le asignó una curva
> espuria distinta (`gap A/B=305.9`) al confundir objetos del workspace. No se
> buscan más donantes. El diagnóstico se completa sobre el donante elegible de v0:
> misma primera acción STRUCT congelada y un segundo turno que recibe solamente el
> output normal del notebook, sin la consigna de adecuación usada en el control v0.
> Esto no es una réplica; aísla el efecto procedural dentro del mismo donante.

## Explicación rival que decide

En v0, `gpt-5.4` ajustó y entregó en la misma celda que imprimía los residuos. El
LLM no pudo leer ese output antes de elegir la familia. Este probe pregunta:

> ¿La falta de segunda fase persiste cuando el flujo ordinario garantiza una
> separación `inspeccionar → leer resultados → decidir/entregar`?

## Único cambio respecto de v0

Se conserva la misma física certificada y el contraste RETAIN/PARAM/STRUCT, pero
se usa una seed no vista. En **todos** los brazos, el primer intento de entrega
después del reporte queda bloqueado por una regla neutral del notebook, anunciada
desde el inicio. La siguiente respuesta recibe el stdout real de la primera celda
y puede entregar. No se menciona adecuación, residuos, fases ni una anomalía.

No se cambian la evidencia, los umbrales, el reward ni el tiempo de ejecución para
favorecer STRUCT.

## Compuertas y lectura

- El `Mpre` debe volver a ser competente, transferir A→B y tener una fase.
- RETAIN y PARAM deben funcionar; de otro modo no se interpreta STRUCT.
- Si STRUCT entrega dos fases: el v0 fue principalmente un fallo de cierre del
  flujo antes de leer el diagnóstico.
- Si STRUCT sigue en una fase: queda una candidata más fuerte de apertura
  estructural insuficiente, pero todavía falta un control explícito de capacidad.
- Si un control que **nombra dos fases sin dar parámetros** tampoco puede completar
  un artefacto válido, se clasifica como dificultad/capacidad, no como vicio.

Se corre una sola seed interpretable después de la enmienda. La seed 3 es un
preflight censurado y no se recicla. Salga como salga, no se modifica esta física
ni se buscan seeds favorables. La candidata independiente de cobertura/horizonte
permanece en el banco y se diseña por separado.
