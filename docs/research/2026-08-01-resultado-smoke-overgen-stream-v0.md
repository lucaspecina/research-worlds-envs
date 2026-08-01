# Resultado exploratorio — `overgen_stream` v0

> **Fecha:** 2026-08-01  
> **Estado:** integración + UX con agentes reales; **no es evidencia del paper**.  
> **Semillas quemadas:** `90000` (DeepSeek), `90001` (gpt-5.4).

## Resultado corto

El primer slice longitudinal funciona de extremo a extremo y produce fallas localizables sin
preguntarle al agente si quiere cambiar de opinión.

| Modelo | Polo alcance limitado | Polo transferencia |
|---|---:|---:|
| DeepSeek-V3.2 | `R=0.365`, 7 turnos, 7 snapshots | `R=0.811`, 9 turnos, 6 snapshots |
| gpt-5.4 | `R=0.890`, 5 turnos, 5 snapshots | `R=0.771`, 6 turnos, 6 snapshots |

Crudos:

- `cases/overgen_stream_v0/smoke_90000.json`
- `cases/overgen_stream_twin_v0/smoke_90000.json`
- `cases/overgen_stream_v0/smoke_90001.json`
- `cases/overgen_stream_twin_v0/smoke_90001.json`

## Certificación previa

Ambos polos comparten un prefijo byte-idéntico y dieron `truth_R=1`. Los robots separan las
respuestas reflejas:

- alcance limitado: adaptativo `0.832–0.898`; nunca actualizar `0.155–0.228`; fragmentar todo
  `0.741–0.787`;
- transferencia: adaptativo = mantener `0.825–0.938`; fragmentar todo `0.316–0.435`.

La primera versión del polo limitado había fallado por margen mínimo contra “fragmentar todo”.
No se bajó el umbral: se corrigió un defecto conceptual previo a agentes —el mundo exigía
cambiar 3 líneas y conservar solo 1— a un contraste genuinamente parcial 2/2. La cohorte nueva
pasó completa.

## Qué hicieron los agentes

### DeepSeek-V3.2

- En transferencia reconoció la forma cuadrática compartida, hizo ajustes menores y entregó
  un modelo razonable.
- En alcance limitado **vio** que las líneas 2 y 3 diferían y cambió su programa. La falla no
  fue atención ni inmovilidad: representó desviaciones dependientes del rango como offsets
  globales e infló la varianza. Es una falla interpretable de lectura/asimilación estructural.

### gpt-5.4

- En alcance limitado usó el reporte para ajustar curvas por línea y alcanzó el robot legal.
- En transferencia concluyó que el reporte confirmaba una estructura compartida y conservó un
  modelo pooled con diferencias menores. No gastó campañas sin una razón clara.

## Qué funcionó

- El reporte llegó como parte de una puesta en marcha prevista, sin mencionar corrección,
  refutación, creencias ni un verbo MANTENER/REABRIR.
- Los cuatro agentes leyeron el reporte y la tarea fue operativamente comprensible.
- `working_model` se capturó sin llamadas ni feedback y la entrega fue válida 4/4.
- El gemelo evita interpretar “cambiar más” como virtud universal.
- El score bajo de DeepSeek puede localizarse en interpretación/modelado, no solo describirse
  como mala entrega.

## Problemas observados

1. **La existencia de un string no garantiza una creencia asentada.** DeepSeek usó un
   placeholder válido durante parte del prefijo en un polo y no creó el string durante los
   primeros turnos del otro. gpt-5.4 sí mantuvo una versión útil desde el comienzo.
2. El evento es natural para este caso, pero la evidencia es limpia y fuerte. Esto valida el
   instrumento; no reproduce aún el dato sutil/mezclado de Corral, OSWorld o KellyBench.
3. Las cuatro corridas son episodios completos independientes. Aunque los datos iniciales son
   iguales por seed, sus historiales cognitivos difieren; **no identifican causalmente el efecto
   del polo**.
4. `R` resume la entrega final; falta puntuar automáticamente `M_pre`, el primer `M_post` y la
   persistencia por región/línea.

## Gate “un nivel arriba”

| Pregunta | Veredicto |
|---|---|
| ¿Sigue siendo interesante? | **Sí.** Ya diferencia notar, interpretar y aplicar dentro de trabajo con entrega ejecutable. |
| ¿Es fiel al caso elegido? | **Sí para ampliación local→global corta.** No se vende como Corral/Kelly. |
| ¿Mide solo obediencia al protocolo? | **No parece**, porque los polos provocan lecturas distintas; pero el efecto de mantener `working_model` sigue abierto. |
| ¿Hay explicación más simple? | Capacidad de ajuste/código y calidad del modelo previo; ambas deben medirse, no descartarse. |
| ¿Generaliza? | **No se sabe:** 2 modelos × 1 corrida × polo. |
| Decisión | **MANTENER el mundo; MODIFICAR la inferencia.** Siguiente: fork apareado desde el mismo prefijo + scoring temporal. |

## Siguiente paso congelado

Antes de más episodios independientes:

1. implementar un fork que clone el mismo historial conversacional y reproduzca el mismo kernel
   hasta inmediatamente antes del reporte;
2. continuar ese mismo donante en ambos polos;
3. puntuar `M_pre`, primer `M_post` y entrega en la región diagnóstica;
4. reportar missing/placeholder/inválido sin excluirlos silenciosamente;
5. hacer un fork técnico barato; solo si es interpretable, firmar la ficha del probe pequeño.

No se cambia la fuerza de evidencia ni la geometría para producir una tasa de falla más linda.
