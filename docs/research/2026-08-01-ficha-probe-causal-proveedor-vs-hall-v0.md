# Ficha exploratoria congelada — gemelos causales proveedor vs hall

**Fecha:** 2026-08-01
**Estado:** diseño de smoke congelado antes de correr agentes; no pre-registro principal.
**Objetivo:** probar contenido científico con un agente real antes de construir infraestructura general.

## Pregunta

¿Un agente que formó un modelo causal provisional a partir de datos históricos revisa —o conserva—
esa estructura cuando un experimento elegido por él mismo produce evidencia discriminante como parte
ordinaria de la investigación?

No se manipulan memoria, autoridad, tarifas ni un reporte anunciado. Este slice aísla una revisión
conceptual con toda la historia disponible.

## Gemelos

Los dos mundos muestran el mismo brief y exactamente los mismos registros observacionales de
`feedstock` y `outcome`. Históricamente, grado de proveedor y humedad están confundidos, por lo que
dos explicaciones causales producen la misma distribución visible.

| Mundo | Verdad interventional | Respuesta correcta tras discriminar |
|---|---|---|
| `REVISE` | la humedad causa la calidad; cambiar proveedor mueve el intake, no el outcome | abandonar la flecha proveedor/feedstock → outcome y modelar el hall |
| `RETAIN` | el grado del proveedor causa la calidad; la humedad es el correlato histórico | conservar la explicación del proveedor y no inventar efecto del hall |

La evaluación ejecuta el modelo entregado bajo intervenciones de grado y humedad, sin juez LLM.

## Secuencia y fork

1. Un único agente inspecciona el historial compartido y mantiene un `working_model` ejecutable como
   estado rutinario de laboratorio.
2. Cuando elige su primer cell con `env.experiment(...)`, el cell se congela antes de ejecutarlo.
3. Se reproduce byte a byte el prefijo en ambos mundos y se ejecuta **el mismo cell**.
4. Desde esos resultados distintos continúan dos conversaciones con el mismo prefijo de chat.
5. Se guardan `M_pre`, primer modelo cambiado y entrega/último modelo puntuable.

Si el agente no deja un `M_pre` antes de experimentar, el smoke no mide revisión y se modifica la
cadencia; no se interpreta como virtud ni como falla.

## Qué se observará

- **Búsqueda:** qué intervención eligió y si era discriminante.
- **Notar/interpretar:** qué lectura hizo del resultado, solo para autopsia.
- **Asimilar:** cambio de sensibilidad causal del modelo ejecutable a grado y humedad.
- **Entregar:** score interventional final y validez del artefacto.
- **Bilateralidad:** cambiar en `REVISE` y conservar en `RETAIN`; cambiar siempre no gana.

Una mala entrega por código inválido o mala distribución se separa de una estructura causal
equivocada.

## Corrida barata y criterios

- Modelo inicial: `DeepSeek-V3.2`.
- Una seed quemada de la banda `94800–94899`.
- Máximo 14–18 turnos totales; sin réplica automática.
- SOTA solo si pasan las compuertas mecánicas y aparece un fenómeno que valga estimar.

Compuertas obligatorias:

1. brief, prefijo, observaciones y `M_pre` idénticos;
2. `M_pre` válido y puntuable antes de la acción;
3. mismos pedidos experimentales en ambos gemelos;
4. el resultado tiene información discriminante server-side;
5. entrega o último `working_model` puntuable en ambos brazos.

Decisión después de la autopsia:

- **MANTENER:** el escenario forma una creencia y separa limpiamente búsqueda, revisión y entrega;
- **MODIFICAR:** la idea causal sirve, pero brief, cadencia o acción no crean el contraste;
- **RETIRAR:** aun con evidencia propia discriminante, el escenario solo produce un refit mecánico o
  el contrato ejecutable no expresa la diferencia causal.

Nunca se elige una variante porque “dio más vicio”; se elige por fidelidad ecológica, identificación
y capacidad de producir tanto conducta correcta como incorrecta de forma interpretable.
