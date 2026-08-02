# Ficha exploratoria congelada — dato propio con fork después de elegir la acción

**Fecha:** 2026-08-01
**Estado:** probe exploratorio de contenido; no pre-registro del estudio principal.
**Semillas:** frescas y quemadas al usarse. Se conservan todos los intentos.

## Pregunta

Cuando el reporte anunciado desaparece y la evidencia solo puede surgir de una campaña ordinaria,
¿el agente busca un chequeo útil y usa su resultado de forma distinta en los dos gemelos?

## Qué cambia y qué no

- Se conservan el mundo, el prefijo, el modelo ejecutable, el presupuesto y el scoring actuales.
- El hito solo informa que la extensión de rango ya está operativa. No entrega datos ni usa las
  palabras anomalía, corrección, evidencia o revisión.
- El brief deja de prometer un reporte automático.
- Después del hito se usa feedback neutral sobre el próximo paso; no se pregunta explícitamente si
  algo confirma o refuta la hipótesis.
- Las ramas comparten el prefijo y, si el agente pide una campaña, comparten exactamente la misma
  celda/acción. El fork ocurre antes de devolver el resultado de esa acción.

## Polos

- **Alcance limitado:** líneas 2–3 se separan en el rango alto; 4–5 conservan la ley.
- **Transferencia:** las cinco líneas conservan la ley.

Cambiar siempre y mantener siempre pierden en algún polo.

## Lecturas antes de resultados

1. **No experimenta:** informa sobre búsqueda, no sobre asimilación. Siguiente control: resultado
   ordinario apareado/yoked para comprobar capacidad.
2. **Experimenta solo una línea no diagnóstica:** el probe no identifica asimilación; informa sobre
   diseño experimental.
3. **Obtiene dato diagnóstico y corrige limitado/conserva transferencia:** control bilateral pasa;
   no perseguir artificialmente una falla en esta estructura.
4. **Obtiene dato diagnóstico, lo menciona pero conserva la estructura en limitado:** señal de
   asimilación candidata; replicar con acción igualada y un modelo SOTA.
5. **Actualiza y luego revierte:** señal de persistencia; medir trayectoria completa.

## Secuencia y gasto

1. Integración y un agente real barato.
2. Inspección de acción, datos, `M_pre → M_post → M_final` y consecuencia.
3. Una réplica SOTA solo si la mecánica funciona y la acción fue informativa.

No se escala n en esta ficha. El resultado termina en un gate “un nivel arriba”: mantener
`overgen` como control, modificar una sola decisión de contenido, o pasar a la segunda estructura.
