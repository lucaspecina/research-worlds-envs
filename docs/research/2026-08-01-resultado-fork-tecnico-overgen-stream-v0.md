# Resultado — fork técnico `overgen_stream` v0

> **Estado:** validación de método; no evidencia conductual.  
> **Ficha previa:** `2026-08-01-ficha-fork-tecnico-overgen-stream-v0.md`.

## Veredicto

La mecánica de **historial vivido apareado** funciona: una conversación se ejecuta una sola vez
hasta el checkpoint, sus celdas se reproducen byte-exactas en ambos servidores y las dos ramas
continúan con la lista completa de mensajes, no con un resumen nuevo.

La primera corrida, DeepSeek, dio NO-GO por elegibilidad del donante/timing. El segundo intento,
gpt-5.4 bajo addendum previo y sin cambiar ninguna otra regla, pasó todos los gates.

| Corrida | `M_pre` | Replay 2/2 | Reporte 1/1 | Entrega 2/2 | Resultado |
|---|---:|---:|---:|---:|---|
| DeepSeek-V3.2, `91000` | No | Sí | Sí | No | **NO-GO** |
| gpt-5.4, `91001` | Sí | Sí | Sí | Sí | **PASS técnico** |

Crudos:

- `scripts/out/overgen_stream_fork/technical_DeepSeek-V3.2_seed91000.json`
- `scripts/out/overgen_stream_fork/technical_gpt-5.4_seed91001.json`

## DeepSeek: qué falló

Al turno 4 todavía no había materializado `working_model`. La rama limitada finalmente modeló
y entregó `R=0.895`; la rama transferencia siguió investigando y corrigiendo código hasta el
límite de 18 turnos sin entregar. El replay y la inyección funcionaron.

Lectura honesta: turno 5 es demasiado temprano para usar DeepSeek como donante con creencia
ejecutable formada, y 18 turnos puede ser corto para su estilo. No se extendió el límite ni se
movió el reporte después de mirar. Este modelo/timing queda fuera de un probe hasta diseñar otra
condición prospectiva de horizonte o una regla de elegibilidad declarada.

## gpt-5.4: qué mostró el fork

El mismo `M_pre` continuó en ambos polos. Resultados finales:

- alcance limitado: `R=0.837`, `R_diagnóstico=0.837`;
- transferencia: `R=0.550`, `R_diagnóstico=0.478`.

El número menor del gemelo no significa que “mantener” haya sido incorrecto: la rama preservó
la estructura compartida pero hizo una estimación más compleja/ruidosa. Con una sola rama no se
interpreta magnitud.

La trayectoria sí aporta dos observaciones:

1. `M_pre` era un modelo real formado desde el prefijo, aunque su score en la región nueva era
   `0`: había mucho por aprender.
2. En ambas ramas, el primer snapshot posterior al reporte era todavía `M_pre`: el agente usó
   ese turno para inspeccionar los datos y recién en el siguiente actualizó/entregó. Por eso
   “primer post” no equivale automáticamente a “evidencia asimilada”.

## Gate “un nivel arriba”

| Pregunta | Veredicto |
|---|---|
| ¿El fork conserva experiencia vivida? | **Sí para APIs de chat stateless:** misma historia completa + replay exacto del kernel. |
| ¿El checkpoint fijo sirve para cualquier modelo? | **No.** DeepSeek no tenía modelo formado. |
| ¿La trayectoria es necesaria? | **Sí.** La actualización apareció un turno después de leer el reporte. |
| ¿Ya corresponde correr una tanda? | **No todavía.** Falta descomposición eficiente por línea/región y una regla prospectiva de elegibilidad/horizonte. |
| Decisión | **MANTENER el fork; MODIFICAR el análisis y la elegibilidad antes del probe.** |

## Siguiente paso

Las dos primeras piezas ya quedaron implementadas después del gate en
`wager/report/checkpoint_score.py`: una sola `WorldSide` puntúa artefactos únicos y descompone
full, región inicial/nueva, línea y línea×región. Reanalizar el fork gpt tomó ~16 segundos.

Resultado ilustrativo del donante gpt (todavía n=1): `M_pre` tenía `R_initial=0.846` pero
`R_diagnostic=0`; en alcance limitado el final llegó a `0.820/0.832`, con las mayores mejoras
en líneas 2/3. En transferencia llegó a `0.771/0.481` y sobreajustó al menos una línea pese a
preservar verbalmente la estructura común. Esto confirma que el score agregado solo no basta.

Pendiente antes del probe:

1. Definir `M_pre` elegible prospectivamente: programa válido, turno sin adquisición nueva y
   cobertura de modelo formada; reportar tasa/tiempo de elegibilidad.
2. Tratar timing fijo y “checkpoint al formarse la creencia” como protocolos distintos, no
   ajustar uno silenciosamente.
3. Recién después firmar un probe pequeño, inicialmente gpt-5.4; DeepSeek requiere su propio
   gate de horizonte.
