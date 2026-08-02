# Reassessment desde arriba — qué aprendimos realmente de `overgen`

**Fecha:** 2026-08-01
**Estado:** lectura de programa después de los probes reales; no es un pre-registro del paper.

## Veredicto

WAGER ya demostró que puede registrar modelos ejecutables, bifurcar una trayectoria y medir
actualización bilateral sin juez LLM. Todavía **no reprodujo de forma robusta la resistencia a
revisar** que motiva el programa.

La razón más simple es de contenido, no de infraestructura. El `overgen` reciente le entregó al
agente un reporte anunciado, grande, limpio y fácil de agrupar; después bastaba con reajustar cinco
curvas y entregar. Los frontier hicieron precisamente eso. La variante `mixed` tampoco produjo
ambigüedad real: conservó las filas diagnósticas dentro de otra tabla anunciada y agregó datos que
ayudaban a estimar.

Esto coincide con la evidencia externa ya documentada: la contradicción única y visible suele
incorporarse; las fallas fuertes aparecen cuando la evidencia forma parte del trabajo ordinario,
compite con señales compatibles, debe recuperarse o cruzarse con otros artefactos, llega después de
obra propia, o exige abandonar una explicación que ya gobierna acciones y dependencias.

## Qué sí observamos

- cambio y conservación correctos en los dos gemelos;
- sobrerrevisión y sobreajuste en algunos polos de transferencia;
- modelos previos heterogéneos: placeholders, fragmentación temprana y leyes compartidas reales;
- un caso especialmente informativo (`DeepSeek 94101`): tras doce turnos y dos experimentos, el
  agente vio que líneas 2–3 ajustaban peor, lo reinterpretó como offsets/heterocedasticidad y sostuvo
  una estructura que terminó mal en el polo limitado (`R=0.114`);
- errores de estructura e incertidumbre que un único score final habría mezclado.

Son señales y casos de diseño. No son todavía una tasa robusta del vicio.

## El error obvio al tomar distancia

Estábamos intentando medir varias cadenas distintas con una sola escena de “llega una tabla”:

1. **actualizar cuando el dato ya fue servido**;
2. **buscar o producir el dato que podría falsar la hipótesis**;
3. **notarlo e interpretarlo dentro del flujo ordinario**;
4. **hacer que la revisión sobreviva y gobierne trabajo posterior**.

El `overgen` actual mide bien sobre todo la primera. No puede mostrar “no buscó” porque el reporte
llega solo; difícilmente muestra “no notó” porque se anuncia como `COMMISSIONING INBOX`; casi no
puede mostrar reversión porque el agente reajusta y entrega enseguida; y no tiene dependencias que
vuelvan materialmente costoso un pivote estructural.

## Cambio de rol, no descarte

`overgen` pasa a ser la **compuerta bilateral/control positivo**: cuando la evidencia es visible y
reparar es fácil, el instrumento debe mostrar cambio en un polo y conservación en el gemelo.

Para buscar los vicios se usan escenarios complementarios:

| Escenario | Qué aísla | Inspiración principal |
|---|---|---|
| Dato de campaña propia | búsqueda, atención y asimilación de evidencia endógena | Corral / FALSIFYBENCH |
| Señal rutinaria acumulativa | cuándo un modelo queda viejo y si la revisión persiste | KellyBench / BayesBench |
| Cambio estructural con dependencias | revisión local frente a abandonar una explicación que ya gobierna trabajo | Corral / STALE |

No se construyen los tres ahora. Se prueba primero el cambio causal más pequeño y se deja de
optimizar `overgen` si vuelve a reducirse a “ver tabla → reajustar regresión”.

## Próxima prueba

La extensión de rango se habilita como un hito ordinario, sin reporte. El agente elige su próxima
acción. Si elige una campaña, se congela **esa misma acción** y recién entonces se bifurca el
resultado entre los gemelos. Así la adquisición queda igualada y el contraste empieza en el dato,
no en dos decisiones estocásticas distintas del agente.

La prueba distingue:

- no pidió una campaña diagnóstica: posible falla de búsqueda;
- pidió una campaña no informativa: problema de diseño experimental;
- recibió un dato incómodo y no movió el modelo: señal de asimilación;
- movió el modelo y luego volvió atrás: señal de persistencia;
- actualizó ambos polos correctamente: `overgen` cumplió como control y la prioridad pasa a una
  segunda estructura con semántica causal y dependencias reales.

Un negativo no se convierte en “el fenómeno no existe”, pero tampoco autoriza relleno infinito ni
selección de semillas hasta fabricar una caída.
