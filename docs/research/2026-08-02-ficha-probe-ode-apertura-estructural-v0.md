# Ficha congelada — probe ODE de apertura estructural v0

**Estado:** exploración registrada antes de llamar agentes. No es pre-registro del
estudio principal ni estimación de prevalencia.

## Pregunta

¿Un agente que ya construyó una explicación dinámica logra conservarla cuando sigue
siendo correcta y retocar sus parámetros cuando eso alcanza, pero deja de ampliar la
familia del modelo cuando un reporte rutinario exige una segunda fase?

Esta es una versión precisa de «le cuesta pivotear». No prueba todavía que la causa sea
el volumen de retrabajo. Tampoco presupone que sea la hipótesis definitiva del proyecto.

## Contraste

Un único agente investiga la Línea A y mantiene un modelo ejecutable para A y para la
futura Línea B. Ese prefijo vivido se reproduce exactamente en tres mundos. Luego llega
el mismo tipo de reporte rutinario de B, con igual grilla, cantidad, ruido y posición:

| Brazo | Qué ocurre en B | Respuesta adecuada |
|---|---|---|
| RETAIN | Continúa la dinámica de A | Conservar |
| PARAM | Una sola fase, con otros parámetros | Retocar |
| STRUCT | La fase original continúa y aparece una segunda ola tardía | Ampliar estructura |

PARAM y STRUCT terminan en el mismo nivel y están igualados aproximadamente en distancia
respecto del modelo previo. La evidencia STRUCT confirma el modelo viejo hasta tarde y
luego salta; por eso el primer resultado se describirá honestamente como **sorpresa
estructural tardía**, no como efecto puro de estructura versus saliencia.

## Compuertas previas sin LLM

Antes de una corrida paga deben cumplirse:

- pasado de A y superficie visible idénticos entre brazos;
- reportes con formato, grilla, unidades y ruido iguales;
- un ajustador independiente elige una fase en RETAIN/PARAM y dos en STRUCT;
- la única fase pierde materialmente solo en STRUCT;
- la actualización alcanzable ofrece headroom en el reward real;
- un modelo PARAM de una fase, aun alcanzando el mismo nivel final, pierde score en STRUCT;
- los `truth_code` ejecutables coinciden con la verdad server-side.

## Agente y mediciones

Primera minería: `gpt-5.4-mini`, un donante y sus tres ramas, con semillas exploratorias
que no se reutilizarán en confirmación. Se usa el protocolo real de WAGER: conversación,
Python persistente, compras, reporte rutinario y modelo ejecutable puntuado sin juez-LLM.

Se guardan:

- `Mpre`: último `working_model` válido antes del reporte;
- `Mpost`: primer modelo distinto después de inspeccionarlo;
- entrega final;
- score global, fidelidad separada A/B y firma predictiva de una o dos fases;
- trazas completas, fallas de protocolo y si el agente examinó la región tardía.

El donante es inelegible si `Mpre` no compila, no explica A competentemente, no transfiere
una fase de A hacia B o no existe antes del reporte. Eso no cuenta como vicio.

## Lectura fijada antes de ver resultados

- Pasa RETAIN y PARAM, pero en STRUCT corrige el nivel y deja una fase: **candidata real**
  de actualización paramétrica sin apertura estructural.
- Falla también PARAM o no entiende el reporte: dificultad general/interfaz, no vicio.
- Cambia en RETAIN: reflejo de cambiar siempre.
- No mira la zona tardía: problema de saliencia/atención; candidato distinto.
- Pasa los tres: esta versión extrema no elicita el fallo; se vuelve al banco de
  hipótesis (mezcla conflictiva, propagación/retrabajo, historia larga u otro patrón).

Si aparece la candidata, se permite un único control posterior con las mismas filas y
una consigna genérica de comprobar si una fase alcanza. Si tampoco puede representarla,
se clasifica como incapacidad estructural, no resistencia espontánea a pivotear.

## Regla de avance

Esta corrida decide **mantener, modificar o abandonar** la candidata; no “demuestra” el
paper. No se construye un generador general ni se ajusta el mundo para conseguir un
resultado bonito. Tras leer traza y artefactos se vuelve un nivel arriba y se compara
esta señal con las otras hipótesis del mapa.
