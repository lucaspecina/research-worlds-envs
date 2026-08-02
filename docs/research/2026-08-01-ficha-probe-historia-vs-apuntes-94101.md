# Ficha exploratoria congelada — historia completa vs apuntes, donante 94101

**Fecha:** 2026-08-01
**Estado:** probe de mecanismo; no pre-registro principal.
**Donante:** trayectoria real DeepSeek-V3.2 `94101`: 12 turnos, dos experimentos propios y
modelo compartido ejecutable antes del reporte. **Advertencia de selección:** también era el caso
excepcional ya conocido donde DeepSeek había fallado en `REVISE`. Por eso este probe solo puede
generar mecanismos e hipótesis; un positivo no estima frecuencia ni generalidad.

## Pregunta

¿La forma en que sobrevive el trabajo anterior cambia la respuesta al mismo dato nuevo?

No se presupone que los apuntes empeoren. Pueden perjudicar al congelar una conclusión o ayudar al
eliminar context rot.

## Brazos mínimos

| Brazo | Conversación | Workspace antiguo | Estado común |
|---|---|---|---|
| `H+N` | historial completo + los mismos extractos de razonamiento propio | sí, datos/variables replayados | mismo `M_pre`, presupuesto, evento y reporte |
| `N-self` | conversación nueva con brief, log mecánico, `M_pre` y extractos propios | no; solo `M_pre` + reporte nuevo | idéntico al anterior del lado server |

Se cruzan con los gemelos:

- `REVISE` (`limited`): líneas 2–3 exigen separar la estructura;
- `RETAIN` (`transfer`): la ley compartida debe conservarse.

El reporte nuevo y sus seeds son idénticos entre representaciones dentro de cada polo.

## Qué identifica y qué no

`H+N` vs `N-self` mide el efecto práctico conjunto de depender del estado comprimido: cambia
contexto y acceso al workspace viejo. **No identifica todavía autoría psicológica** ni permite decir
que toda diferencia sea terquedad.

- Si `N-self` empeora en ambos polos: pérdida general de estado/información.
- Si mejora en ambos: compresión útil/context rot en `H+N`.
- Si revisa menos solo en `REVISE`, conservando competencia en `RETAIN`: señal compatible con
  atrincheramiento por estado comprimido.
- Si ambos son equivalentes: la hipótesis pierde prioridad en esta estructura.

Los no-submit, códigos inválidos y errores operativos se reportan aparte. Un score peor por código
inválido no cuenta como no-revisión.

## Compuertas

1. Replay server-side exacto del prefijo en los cuatro brazos.
2. Mismo `M_pre`, presupuesto y filas del reporte dentro de cada polo.
3. Modelo válido entregado en ambos brazos de un polo para comparar consecuencia; si no, solo se
   inspecciona el proceso y se repite como integración, no se interpreta.
4. Si aparece una diferencia candidata, el siguiente contraste agrega `N-other` con el mismo
   contenido y una base sin conflicto; no se escala directamente.

Falta deliberadamente una compuerta basal sin dato nuevo. `RETAIN` controla conducta bilateral,
pero no demuestra que la compresión conserve toda la información necesaria. Toda diferencia se
lee primero como efecto del paquete conversación+workspace, no como “autoría de los apuntes”.

## Límite de gasto/decisión

Un solo donante, un modelo barato, cuatro continuaciones, máximo 8 turnos por rama. Se detiene ahí.
El objetivo es decidir si vale construir el contraste general, no obtener significancia.
