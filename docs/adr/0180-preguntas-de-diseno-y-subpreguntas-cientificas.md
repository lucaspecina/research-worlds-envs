# 0180 — Separar preguntas de diseño de subpreguntas científicas

**Fecha**: 2026-08-11 · **Estado**: vigente · **Aclara**: ADR 0179.

## Problema

ADR 0179 subordinó pistas, avisos y presión a la pregunta principal del salto, pero todavía llamó
“subpreguntas” tanto a las decisiones para construir un mundo válido como a las preguntas sobre la
conducta del agente. Eso mezcla la validez del instrumento con el fenómeno que queremos medir.

## Decisión

El orden experimental es:

> **salto → preguntas de diseño → mundo y tarea → validación del diseño → pregunta principal →
> subpreguntas científicas**

Las **preguntas de diseño** comprueban si:

- el salto mejora materialmente frente al mejor rival sin salto;
- la evidencia necesaria existe y está al alcance;
- la tarea permite investigar y expresar el salto;
- el puntaje reconoce su consecuencia;
- un agente con la idea nombrada, pero sin la solución, puede resolverlo.

Si una de estas pruebas falla, se modifica o abandona el diseño. Ese resultado no se interpreta
todavía como incapacidad del agente para saltar.

La **pregunta principal** sigue siendo: “¿el agente descubre y realiza el salto?”. Las
**subpreguntas científicas** estudian, sobre un diseño ya validado, cuándo y por qué ocurre: error
visible, presión, ayudas, horizonte u otras condiciones.

Una misma manipulación puede cambiar de función según el momento. La idea nombrada usada antes de
validar el mundo es una prueba de resolubilidad del diseño. Una comparación pre-registrada con y
sin esa ayuda, después de validar el mundo, puede responder una subpregunta científica.

## Consecuencia inmediata

Para el próximo experimento de grupos escondidos se responderán primero las preguntas de diseño.
Solo después se interpretarán partidas sin ayuda o contrastes sobre el comportamiento del agente.
