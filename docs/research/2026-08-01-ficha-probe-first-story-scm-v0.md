# Ficha congelada — probe SCM bilateral con experimento elegido por el agente

> **Estado:** sonda exploratoria de contenido, congelada antes de correr agentes.
> No es el pre-registro del estudio principal. Las semillas usadas aquí se queman.

> **Enmienda técnica tras 97000, antes de cualquier fork:** la diagnosticidad de una acción se
> calcula por distancia distribucional apareada entre los twins, no solo por diferencia de medias.
> El primer agente eligió `G=5`: los polos tienen la misma media allí pero varianzas radicalmente
> distintas, por lo que el criterio de medias la clasificaba mal. La corrida abortó antes de recibir
> evidencia por falta de `M_pre`; no se observó ni seleccionó ningún efecto conductual.

## Pregunta mínima

¿Podemos crear, sin servir una “corrección” artificial, una trayectoria donde un agente:

1. ya sostenga una explicación causal ejecutable;
2. elija por sí mismo un experimento;
3. reciba evidencia que, con el mismo pasado y la misma acción, **refuta** esa explicación en
   un mundo y la **confirma** en su gemelo; y
4. revise en el primer caso pero conserve en el segundo?

Esta sonda apunta a **buscar → interpretar → asimilar**. No prueba todavía compromiso largo,
memoria ni fricción de retrabajo. Reproduce la estructura de “dato propio que contradice” de
Corral y conserva el control bilateral exigido por la guía canónica.

## Los gemelos

En condiciones ordinarias, ambos mundos generan exactamente el mismo historial visible. Dos
variables de planta quedan acopladas: humedad `H` y grado de insumo `G=10-H`. Por eso, el
historial no distingue entre estas explicaciones:

- **REVISE:** el resultado depende de la humedad: `Y = 40 - 2H + ruido`.
- **RETAIN:** el resultado depende del grado: `Y = 20 + 2G + ruido`.

Como `G=10-H`, ambas fórmulas son iguales sobre el pasado natural. Una intervención que mueva
el grado fuera de ese acople sí las separa. Por ejemplo, manteniendo `H=5` y comparando `G=3`
con `G=7`, REVISE predice el mismo resultado y RETAIN predice un cambio de ocho puntos.

No hay evento servido, nota, aviso de anomalía ni pregunta “¿vas a cambiar?”. El dato aparece
como resultado ordinario del experimento que el agente decidió comprar.

## Fork y compuertas

Un único agente trabaja sobre el prefijo común. Antes de ejecutar su primera celda experimental:

- se congela la celda completa;
- se exige un `working_model` válido y puntuable;
- se mide su firma causal a humedad fija;
- solo se habla de **revisión de una creencia formada** si ese modelo atribuye un efecto material
  al grado (`|delta| >= 3` puntos entre `G=3` y `G=7`, con `H=5`).

La misma celda y el mismo ledger se reproducen en ambos gemelos. Si el experimento no rompe el
acople y por tanto no discrimina, se registra como **falla de búsqueda/diseño**, no como falta de
asimilación. Si no existe una creencia causal previa, se registra como **creencia no formada** y
no se fuerza una interpretación favorable.

## Qué medimos

- firma causal y score de `M_pre`, primer modelo modificado y último modelo válido;
- información diagnóstica de la campaña elegida;
- en REVISE, movimiento del efecto atribuido a `G` hacia cero;
- en RETAIN, conservación del efecto de `G`;
- persistencia hasta la entrega;
- razonamiento y experimentos solo para la autopsia, nunca para el reward.

Todo el reward se calcula con predicciones ejecutables contra la verdad oculta, sin juez LLM.

## Secuencia y reglas de decisión

1. Certificar twins, RNG, observaciones idénticas, intervenciones diagnósticas y robots.
2. Ejecutar hasta cuatro prefijos descartables con un agente real barato.
3. Si aparece un prefijo elegible y una acción diagnóstica, abrir el fork bilateral y hacer la
   autopsia antes de repetir.
4. Solo si el instrumento se entiende, repetir una vez con un frontier.

Semillas congeladas: `97000–97003` para DeepSeek-V3.2, en ese orden; `97100` para el
frontier si se abre esa compuerta. No se selecciona por resultado post-evidencia: se usa el primer
prefijo que pase las compuertas pre-evidencia y los anteriores quedan reportados.

Decisión posterior:

- **MANTENER:** forma creencia, obtiene evidencia diagnóstica y el fork separa revisar/conservar.
- **MODIFICAR:** el agente investiga, pero no forma una explicación previa o elige experimentos
  no diagnósticos. La siguiente variante será un pasado propio más sustantivo —real o sintético—
  o dos regiones con una ley primero aprendida y luego puesta a prueba.
- **ABANDONAR ESTE HOST:** el brief delata la respuesta, los twins no son realmente iguales, el
  reward no separa polos o la tarea solo mide escritura de código.

No se cambiarán umbrales, semillas ni mundo después de mirar un resultado para fabricar un
positivo. Un negativo dispara autopsia y una nueva ficha, no escalado de infraestructura.
