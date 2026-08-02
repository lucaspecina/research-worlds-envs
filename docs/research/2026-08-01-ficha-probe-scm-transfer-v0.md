# Ficha congelada — SCM transfer con pasado propio vivido

> **Estado:** variante exploratoria congelada antes de correr agentes. No es el estudio
> principal. Semillas quemadas. Nace de una autopsia, no de elegir el efecto más lindo.

> **Enmienda de protocolo tras 97200:** se retiró como gate que *todos* los experimentos
> posteriores fueran North. La rama RETAIN volvió explícitamente a South para comprobar que su
> modelo seguía extrapolando bien; eso es una validación científica razonable y ocurre después del
> fork, por lo que no amenaza el apareamiento causal. Siguen siendo obligatorios: pasado pre-acción
> solo South y primera acción congelada solo North. El prompt futuro permite revisitar South si se
> etiqueta el sitio. No se cambió la verdad, el reward ni la acción observada.

## Por qué existe

En el `first_story_scm_v0`, 4/4 DeepSeek (`97000–97003`) eligieron experimentar antes de crear
un modelo ejecutable. Eso es razonable: el problema comenzaba antes de que hubiera una creencia
causal que revisar. Las acciones fueron en general útiles; llamar a ese host “revisión” habría
sido un error de constructo.

Esta variante agrega justo lo que faltaba: **un pasado de investigación realizado por el propio
agente**. No se le pega una autobiografía inventada ni se le dice que algo cambió.

## Episodio

1. El agente empieza trabajando en la planta South. Allí puede observar y experimentar con
   humedad `H` y grado de insumo `G`; en ambos twins la ley verdadera es `G → Y`.
2. El agente trabaja con herramientas reales hasta producir un `working_model` válido que atribuya
   un efecto material a `G`. El modelo también debe predecir ese efecto en North antes de haber
   visto datos North: esto operacionaliza la hipótesis de transferencia que luego puede revisarse.
3. El coordinador anuncia una transición rutinaria de sitio: el trabajo sigue en North. No hay
   evidencia, anomalía, nota ni pregunta sobre cambiar de idea.
4. El agente elige su primer experimento North. Esa celda se congela y se ejecuta idéntica en:
   - **REVISE:** en North el resultado depende de `H`, no de `G`;
   - **RETAIN:** en North sigue dependiendo de `G`.
5. La evidencia aparece solo como output ordinario del experimento propio. Después el agente
   continúa y entrega un modelo para ambos sitios.

South y todo lo anterior a la primera acción North son byte-idénticos. En North, la historia
observacional también es idéntica; solo una intervención diagnóstica separa los polos.

## Gates e interpretación

- `M_pre` válido, efecto de `G` a `H=5` de al menos 3 puntos en South y North.
- Todas las acciones del pasado usan South; replay y ledger exactos en ambos twins.
- La acción North queda congelada antes de devolver sus resultados.
- Diagnosticidad por distancia distribucional apareada, no solo por diferencia de medias.
- Acción no diagnóstica = resultado de búsqueda, no de asimilación.
- REVISE debería mover el efecto North de `G` hacia cero; RETAIN debería conservarlo.
- South sirve como control de alcance: corregir North no debe borrar la ley aprendida en South.
- Reward únicamente sobre modelos ejecutables contra verdad oculta, cero juez LLM.

## Corridas y decisión

Semillas DeepSeek-V3.2 `97200–97203`, en orden. Se usa el primer prefijo que pasa las compuertas
pre-evidencia; todos los intentos quedan reportados. Si el camino completo funciona, una réplica
frontier usa `97300`.

- **MANTENER:** pasado vivido + acción propia producen un fork bilateral interpretable.
- **MODIFICAR:** no forma/traslada una creencia o no busca evidencia diagnóstica; autopsia antes de
  tocar complejidad. Una opción ya declarada es comparar pasado vivido con el mismo historial
  serializado sintéticamente, pero no se construye salvo que responda una duda concreta.
- **ABANDONAR ESTE HOST:** la transición delata el polo, South no es realmente común, la tarea solo
  mide protocolo/código o el reward no separa las verdades.

Si el control limpio funciona pero frontier actualiza perfectamente, la siguiente manipulación de
contenido será evidencia **conflictiva** (confirmación + refutación con volumen y posición igualados),
no relleno arbitrario ni longitud por sí misma.
