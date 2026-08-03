# Resultado — probe ODE con revisión en dos pasos v1

**Estado:** diagnóstico exploratorio cerrado. Resuelve la principal explicación
rival de v0 dentro del único donante elegible; no es réplica entre donantes.

## Resultado corto

El aparente fallo estructural de ODE desapareció cuando `gpt-5.4` pudo leer el
output de su propia celda antes de entregar. Sin decirle que revisara la familia,
que buscara dos fases ni cuáles parámetros usar, pasó de:

| Momento | Fases efectivas | MAE de B | Reward |
|---|---:|---:|---:|
| Primera acción congelada | 1 | `5.43` | — |
| Después de leer su output | 2 | `0.90` | `0.9766` |

La segunda fase del artefacto final representó `43.0%` del plateau, prácticamente
la magnitud estructural verdadera. El modelo mantuvo A (`MAE=1.16`) y la entrega
fue válida.

## Qué se mantuvo idéntico

Se cargó el donante elegible `gpt-5.4/seed1` de v0, se reprodujo el mismo reporte
STRUCT y se ejecutó **la misma primera celda congelada** (`Mfirst` conservó el hash
`8fe4bf8cd6eb`). Su intento de entrega se bloqueó neutralmente. El turno siguiente
recibió solo el feedback ordinario, incluido el stdout con la tabla de ajuste y
residuos; no recibió ninguna consigna adicional de model criticism.

El ledger del prefijo fue idéntico y las acciones/entregas coincidieron. El flag
global `replay_exact` quedó falso porque dos `working_model` intermedios y un stdout
no fueron byte-idénticos al recargar la traza; en los dos turnos finales del prefijo
el `working_model`, la trayectoria y el estado sí coincidieron. Por eso el claim es
un control fiel del **checkpoint final**, no byte-identidad completa de todo el
historial serializado.

## Qué hizo el agente

En la primera celda eligió una logística, calculó una tabla de residuos y trató de
entregarla. En el turno siguiente, al ver esos resultados, escribió espontáneamente
que B tenía «una transición en dos etapas» y que una logística única fallaba. Sin
usar una receta paramétrica, construyó una interpolación ejecutable que preservó
ambas subidas y la entregó correctamente. La medición es sobre sus predicciones,
no sobre el nombre de la familia en el código.

## Intento de donantes frescos

No se buscaron seeds favorables:

- seed 3 quedó censurada porque el selector confundió una microcurvatura de `4.7%`
  con una fase sustantiva. Se fijó prospectivamente un mínimo de `15%`; STRUCT
  verdadero está cerca de `41%`;
- seed 4, ya con esa corrección, modeló A competentemente pero inventó para B una
  curva distinta antes de observar B (`gap A/B=305.9`). Rompió el fork y quedó
  censurada sin abrir ramas.

Esto muestra que la formación libre de donantes en este host es inestable. No se
justifica seguir gastando hasta encontrar otro elegible.

## Revisión un nivel arriba

**El ODE no sostiene por ahora “se resiste a un pivote estructural grande”.** La
falla v0 se explica mejor por cierre procedural: el agente programó diagnóstico y
entrega en una misma acción, por lo que el resultado del diagnóstico no podía
influir en la decisión ya escrita.

Esto no borra el aplanamiento de mezclas latentes en SCM: allí un segundo turno real
no lo rescató. Sí elimina la afirmación de que ya generalizó causalmente de SCM a ODE.

La candidata nueva y más concreta es:

> **cierre prematuro del ciclo de investigación:** el agente produce información
> capaz de corregirlo, pero compromete la entrega antes de observarla o darle
> autoridad.

Converge con la brecha de propagación previa, que también desapareció al volver
saliente un estado dependiente. Puede ser una contribución de protocolo de agentes,
pero necesita repetirse en más donantes y tareas antes de convertirse en claim.

## Decisión

- cerrar este host y no buscar más seeds;
- degradar apertura estructural a candidata SCM-específica aún abierta;
- promover cierre/autoridad del diagnóstico como mecanismo candidato;
- pasar al probe independiente de **cobertura fuera del soporte**, para no hacer
  del hallazgo recién aparecido la única hipótesis del proyecto.

Crudo: `scripts/out/ode_second_wave_v0/control_struct_plain_gpt-5.4_seed1.json`.
Las seeds censuradas 3 y 4 están en la misma carpeta.
