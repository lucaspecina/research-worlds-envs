# 0179 — El experimento se centra en el salto; las demás preguntas son subordinadas

**Fecha**: 2026-08-11 · **Estado**: vigente · **Refina y supersede parcialmente**: ADR 0178
en la definición, el nombre y la regla de identidad del experimento. Conserva sus nombres
semánticos y su distinción entre experimento, partida, tanda y ensayo.

## Problema

ADR 0178 ordenó los niveles, pero dejó que una manipulación particular —por ejemplo mostrar el
error del modelo— definiera la pregunta principal y el nombre de un experimento. Eso invirtió la
jerarquía del proyecto: una subpregunta de diseño pasó a parecer el objetivo científico.

También se venía tratando al gemelo como requisito del primer mundo. Para el foco actual eso
agrega una segunda verdad antes de demostrar que el anfitrión básico representa bien el salto.

## Decisión

Todo experimento WAGER parte de **un salto objetivo** y construye un **mundo + tarea + puntaje**
donde realizar ese salto permite encontrar un modelo claramente mejor que los buenos modelos que
no lo realizan.

La pregunta principal tiene siempre esta forma:

> **¿el agente descubre y realiza el salto?**

Las preguntas sobre cuándo, por qué o bajo qué condición aparece son **subpreguntas**. Ayudas,
avisos, consecuencias y presión son condiciones o controles dentro del experimento. Cambiarlas no
crea otro experimento.

La validación previa demuestra, en este orden:

1. **necesidad matemática**: el modelo con el salto supera materialmente al mejor rival fuerte
   sin el salto;
2. **evidencia alcanzable**: el agente puede comprar u observar datos que permiten descubrirlo;
3. **resolubilidad con agente**: con la idea nombrada, pero sin la solución, el agente puede
   investigarla, implementarla y mejorar.

El tercer punto es un control de construcción. Compararlo con la condición sin ayuda informa la
dificultad de descubrir la idea, pero no reemplaza la pregunta principal.

El **gemelo** queda como control anti-reflejo posterior y opcional. No es requisito para validar el
mundo base del foco actual. Lucas decidirá si se agrega una vez que el anfitrión principal esté
validado.

## Nombres

Nombre humano:

> **Salto — situación investigativa**

ID:

> `exp__<salto>__<situacion>__v<n>`

Una condición o tanda se describe aparte, por su contenido. La identidad de una partida sigue:

> **ID del experimento · mundo · tarea · condición · agente · instancia · semilla**

Los IDs ya usados no se renombran: quedan como alias históricos para preservar trazabilidad.

El paquete antes llamado `D2` se lee ahora como el experimento histórico **Grupos escondidos —
Planta a alta temperatura**. “Error del modelo a la vista” era la subpregunta de una tanda, no el
objetivo principal. El paquete quedó cancelado antes de su tanda principal y no es plantilla para
el próximo mundo.

## Foco inmediato

Diseñar desde cero un solo mundo para **grupos escondidos** donde pasar de una población aparente
a dos tipos persistentes sea necesario para encontrar el modelo bueno. Primero se valida ese mundo;
después se estudian pistas, conocimiento del error, presión u otras subpreguntas. El gemelo queda
fuera de esta etapa.
