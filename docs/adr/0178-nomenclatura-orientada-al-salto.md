# 0178 — Nomenclatura orientada al salto y nombres semánticos

**Fecha**: 2026-08-11 · **Estado**: vigente · **Refina**: ADR 0177. Conserva la obligación de
probar con agentes con pistas, pero reemplaza `P1/P2/P3` y otros códigos como nombres visibles.

## Problema

`D1`, `D2`, `P1`, `P2`, “brazo”, “polo”, “variante” y “experimento” llegaron a nombrar cosas
de niveles distintos. Un código podía mezclar el mundo, la tarea, la ayuda y la pregunta
científica. Lucas no podía saber qué se iba a ejecutar leyendo el nombre.

## Decisión

**Experimento WAGER** es el nombre del paquete científico completo. Contiene:

1. **Salto**: cambio de forma que se quiere medir.
2. **Pregunta**: una pregunta científica principal.
3. **Mundo o par de mundos**: verdades ocultas donde el salto corresponde o sería un error.
4. **Tarea**: objetivo, herramientas, presupuesto, turnos y entrega del agente.
5. **Condiciones**: combinaciones exactas de los ejes manipulados. Para una afirmación causal,
   las condiciones comparadas difieren en un solo eje.
6. **Medida principal**: número que responde la pregunta.
7. **Tanda**: conjunto operativo de partidas que ejecuta el experimento.

Una **partida / episodio** es una sola ejecución de un agente dentro del experimento. Un
**ensayo** es una intervención que compra el agente durante esa partida; no se llama
experimento.

La **instancia del mundo** fija sus parámetros concretos. La **semilla de partida** identifica
el azar de la ejecución. No son sinónimos y pueden compartirse deliberadamente en comparaciones
apareadas.

La **validación previa** del experimento incluye:

- certificación matemática contra el mejor rival sin el salto;
- prueba de resolubilidad con el mismo agente y la **idea nombrada**, sin regalar la solución;
- comparación contra ese mismo agente **sin ayuda** para medir la prima de descubrimiento;
- opcionalmente, una **solución servida — control de techo**, que prueba solo capacidad de la
  interfaz y de la entrega, nunca descubrimiento.

La resolubilidad queda validada únicamente para la combinación concreta de mundo, tarea,
agente y ayuda; no es una propiedad del mundo en abstracto.

Las condiciones se nombran por contenido y por eje: `Ayuda: idea nombrada`, `Aviso: error
señalado`, `Consecuencia: pérdida operativa`. No forman necesariamente una sola escalera. Una
orden de procedimiento no equivale a nombrar una idea.

Se reserva **caso de evaluación** para un punto de la batería secreta.

## Regla de nombres

Cada experimento tiene dos nombres. El nombre humano sigue:

> **Salto — qué ponemos a prueba — familia de mundo**

El ID estructurado sigue:

> `exp__<salto>__<mundo>__<tarea>__<contraste>__v<n>`

Partida:

> **ID del experimento · mundo · tarea · condición · agente · instancia · semilla**

Como el nombre del experimento comienza por el salto, toda identidad de partida también lo
muestra.

El experimento antes llamado `D2` queda:

> **Nombre:** Grupos escondidos — Error del modelo a la vista — Planta a alta temperatura
>
> **ID:** `exp__grupos-escondidos__planta-alta-temperatura__modelo-para-piloto__error-explicito__v1`

## Perfil obligatorio del mundo

El nombre identifica al experimento; no intenta codificar todas las propiedades del mundo. La
cabecera declara por separado: forma oculta, verdades del par, dinámica, llegada de evidencia,
horizonte, profundidad, interacción, dependencias y complejidad efectiva.

Cada mundo usa nombre humano **Familia — verdad oculta** e ID
`world__<familia>__<verdad>__v<n>`. El par usa `pair__<familia>__<contraste>__v<n>`. Cambiar
solo parámetros crea otra instancia; cambiar la verdad o la forma crea otro mundo o una nueva
versión explícita.

La dificultad se reporta como **dificultad observada** por agente × tarea × ayuda. No se incluye
como “fácil/difícil” en el ID porque no es una propiedad absoluta del mundo.

## Compatibilidad e historia

Los IDs viejos no se borran ni se renombran en masa: quedan en rutas, datos y documentos
históricos para conservar trazabilidad. Cuando aparezcan, van después del nombre descriptivo,
entre paréntesis. Ninguna solicitud de GO ni titular nuevo puede depender solo de un código.
Cada pedido de GO muestra primero el nombre del experimento y luego la composición completa de
la tanda: mundos × condiciones × agentes × instancias × semillas = partidas totales.

La cabecera de cada experimento declara, sin crear otro tipo de documento: nombre, ID, salto,
pregunta, perfil de mundos, tarea, condiciones, medida principal, agentes, instancias, semillas
y estado.

Reglas rápidas:

- cambia la verdad → otro mundo;
- cambia el objetivo o la entrega → otra tarea;
- cambia ayuda, aviso o consecuencia → otra condición;
- cambia la pregunta científica → otro experimento;
- cambia agente, instancia o semilla → otra partida.
