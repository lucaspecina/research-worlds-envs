# Resultado exploratorio — dato propio, DeepSeek 94700

**Alcance:** una corrida de integración/contenido con DeepSeek-V3.2. No estima una tasa ni
autoriza inferencia causal sobre revisión.

## Veredicto corto

El escenario consiguió que el agente buscara evidencia por campañas ordinarias, pero **no produjo
un episodio interpretable del vicio**. Tampoco pasó la integridad completa del fork ni la entrega.

## Qué ocurrió

- El prefijo se declaró elegible muy temprano, en turno 2: había un modelo compartido ejecutable,
  pero casi nada de obra o compromiso acumulado.
- Al habilitarse el rango sin reporte, el agente eligió espontáneamente una campaña completa en
  línea 2; después gastó el resto en líneas 3 y 4. No apareció una falla de búsqueda/falsificación.
- En alcance limitado, notó que las líneas tenían conductas distintas —incluida pendiente negativa
  en línea 3— y abandonó la unificación. La revisión conceptual ocurrió, pero entregó un ajuste
  lineal pobre (`R=0.000`). Eso es modelización/implementación, no terquedad.
- En transferencia, descubrió la curva cuadrática común y trató de entregarla. El código contenía
  `true` en vez de `True`, el servidor lo rechazó, y el agente no inspeccionó `.accepted`; pasó los
  turnos restantes afirmando erróneamente que ya había terminado. Es una falla de protocolo y
  monitoreo, no revisión de creencias.

## Por qué el fork no identifica el efecto

La celda congelada contenía primero una consulta inválida a `env.budget_remaining`; falló antes de
alcanzar `env.experiment`. Por eso la “misma acción por construcción” fue solo el mismo string, no
la misma campaña ejecutada. Las campañas reales fueron elegidas después en continuaciones separadas,
aunque ambas terminaron eligiendo las mismas líneas. El gate del runner quedó corregido para exigir
que la celda congelada efectivamente registre el mismo experimento en ambos brazos.

## Lectura un nivel arriba

La corrida refuerza la autopsia general:

- al tener todos los datos accesibles y una regresión compacta, el agente vuelve a combinarlos,
  compra chequeos amplios y mueve la estructura;
- las 156 filas efectivas siguen siendo cognitivamente pequeñas: se reducen a pocos fits;
- quitar el cartel del reporte mejora fidelidad, pero no crea por sí solo memoria, compromiso,
  dependencias ni una explicación semántica difícil de abandonar.

**Decisión:** no replicar este resultado con SOTA todavía y no seguir maquillando `overgen` para
fabricar una falla. Se conserva como control y como activo de búsqueda natural. La próxima prueba
de mayor información es la representación del pasado (`historia + cuaderno / solo cuaderno`) con
controles de fidelidad, seguida de una estructura causal distinta si el mecanismo no aparece.

Crudo: `scripts/out/overgen_stream_fork/probe_own_experiment_DeepSeek94700.json`.
