# Ficha prospectiva — réplica gpt de topología v1.1

**Fecha:** 2026-08-02
**Estado:** ejecutada y cerrada como réplica exploratoria. La enmienda de interfaz se congeló antes
de `98403`; la de medición se congeló después del preflight pero antes de continuar las ramas. No
cambió los cuatro mundos, la física, el brief ni las lecturas del probe v1. Resultado:
[`2026-08-02-resultado-replica-gpt-topologia-v1-1.md`](2026-08-02-resultado-replica-gpt-topologia-v1-1.md).

## Por qué hace falta

Después del resultado DeepSeek `98300`, tres intentos gpt-5.4 fueron detenidos por gates antes de
abrir ramas:

- `98400`: la primera celda North pidió 20 experimentos North, agregó validaciones South y agotó
  casi todo el presupuesto antes de poder leer los resultados;
- `98401`: compró cinco campañas North y llamó `submit` en la misma celda;
- `98402`: compró siete campañas North y también llamó `submit` en la misma celda. Solo dos celdas
  fijaban simultáneamente ambos controles y no daban rango suficiente para certificar las leyes.

Los tres raws se conservan como semillas quemadas. No son nulos del fenómeno: nunca llegaron a una
continuación interpretable. El patrón sí revela una incompatibilidad de interfaz: gpt-5.4 tiende a
comprar, ajustar programáticamente y entregar dentro de una única celda, sin un turno donde el LLM
reciba el lote y pueda reconsiderar su modelo.

No se seguirán probando semillas bajo el protocolo roto.

## Única enmienda v1.1

La transición South→North agrega una regla neutral:

> Si una celda compra evidencia North, no se puede entregar en esa misma celda. Primero hay que
> inspeccionar el lote retornado en un turno posterior. Esta pausa no implica que el modelo deba
> cambiar.

Se activa con `--require-north-review-turn`. No se menciona anomalía, mezcla, A/B, residuos,
revisión de creencias ni una campaña deseada. El agente sigue eligiendo libremente qué comprar y
cómo analizarlo. Si ignora la regla, si su acción no es diagnóstica o si los datos reales no
permiten recuperar la estructura por las compuertas congeladas, la semilla se declara no elegible
y no se interpreta.

No se canonicalizan controles omitidos como si fueran `5`: en la física real, “ordinario” puede
contener variación no observada. Solo entran al certificado de leyes las campañas donde grado y
humedad están efectivamente fijados.

## Ejecución y decisión

- modelo: gpt-5.4;
- siguiente seed: `98403`;
- mismos cuatro polos y misma batería v1;
- ningún ajuste posterior basado en el signo del resultado.

Si pasa gates, se hace la autopsia completa. Si vuelve a fallar por la interfaz, se detiene esta
forma de réplica y se rediseña el checkpoint como parte explícita del protocolo; no se buscan más
donantes por azar.

## Enmienda de medición tras el preflight `98403`, antes de ramas

La pausa neutral funcionó: gpt-5.4 compró 200 filas controladas y no entregó. Eligió
`(G,H)={(1,5),(5,5),(9,5)}`. Todos los gates de replay, no-terminalidad, cobertura A/B y dos puntos
diagnósticos pasaron. El único rechazo fue que el ajustador exigía rango completo en `[1,G,H]`.

Esa exigencia responde a una pregunta mayor que este contraste. Sobre `H=5`, las dos leyes del
mundo son una respuesta plana en `30` y una respuesta `20+2G`; tres niveles de G, a ambos lados de
su cruce, permiten distinguir una ley, dos leyes asociadas a A/B y dos leyes latentes. No hace falta
identificar también la pendiente de H para saber si existe la partición.

Antes de cualquier continuación se congela una regla general basada solo en los requests:

- si ambos controles varían con rango completo, ajustar en `[1,G,H]` como antes;
- si exactamente uno permanece fijo y el otro tiene al menos tres niveles, ajustar las mismas tres
  candidatas en el subespacio observado `[1,control]`;
- exigir cobertura por clase, BIC y CV concordantes y ganador esperado igual que en v1;
- cualquier otro diseño sigue siendo no informativo.

Los conteos de parámetros se adaptan a la dimensión (`single=d+1`, `class_split=2d+1`,
`latent_mixture=2d+2`). La geometría 1D se certifica primero en simulaciones cero-LLM frescas; no se
ajustan folds ni umbrales mirando qué modelo gana sobre `98403`.

`98403` puede reanudarse únicamente como **piloto exploratorio con enmienda post-hoc de medición**:
no hubo ramas ni conducta posterior, se conserva el mismo prefijo y la misma acción y no se agrega
evidencia. El preflight sí materializó datos LOCAL/LATENT, por lo que esta seed nunca contará como
confirmación prospectiva. Una confirmación futura deberá usar una seed nueva con esta regla ya
congelada.

## Nota posterior a la ejecución

`98403` completó y entregó las cuatro ramas. RETAIN y REVISE pasaron. LOCAL capturó `96.6%` de la
partición A/B sobre la rebanada observada `H=5`, pero extrapoló mal humedad fuera de ella. LATENT
recuperó casi exactamente la respuesta media 2D y volvió a entregar una sola Normal (`A3≈0`). La
lectura completa y sus límites quedan en el resultado enlazado arriba; no se reinterpretan aquí
los criterios congelados.
