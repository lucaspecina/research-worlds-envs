# Resultado — transferencia causal South→North con agentes reales

> **Alcance:** un fork DeepSeek-V3.2 (`97200`) y uno gpt-5.4 (`97300`), cada uno con
> prefijo propio vivido y ramas REVISE/RETAIN apareadas. Es una validación de contenido,
> no una estimación de prevalencia.

## Resultado corto

El instrumento limpio funciona. Ambos agentes:

1. investigaron South y construyeron un modelo que atribuía a `G` un efecto cercano a 8;
2. transfirieron esa ley a North antes de ver datos North;
3. eligieron una campaña North diagnóstica;
4. ante la misma acción, revisaron solo cuando los datos la refutaron y conservaron solo cuando
   la confirmaron;
5. mantuvieron intacta la ley correcta de South.

| Modelo | Polo | Efecto `G` North antes | Efecto final | Verdad | South final |
|---|---|---:|---:|---:|---:|
| DeepSeek-V3.2 | REVISE | 7.59 | 0.20 | 0 | 7.59 |
| DeepSeek-V3.2 | RETAIN | 7.59 | 8.20 | 8 | 7.59 |
| gpt-5.4 | REVISE | 7.87 | −0.04 | 0 | 7.87 |
| gpt-5.4 | RETAIN | 7.87 | 8.08 | 8 | 7.87 |

La primera acción North fue elegida una sola vez y replayada exactamente. El pasado South, el
ledger, la celda, las solicitudes y el presupuesto fueron iguales entre ramas; solo cambió el
resultado oculto del mundo. No hubo nota, corrección servida ni pregunta sobre cambiar de idea.

## Qué no conviene inflar

El código global de ambos agentes quedó lejos del techo. DeepSeek mejoró mucho en REVISE
(`R_unclipped −2.67 → 0.002`) pero su aproximación distribucional siguió mediocre; gpt-5.4 llegó
a `R=0.106` en REVISE. La firma causal local, no el score global, demuestra la revisión estructural.
Esto separa una virtud epistémica de una implementación predictiva imperfecta.

En 97200 una compuerta exigía artificialmente no volver nunca a South después de la transferencia.
La rama RETAIN volvió para validar alcance y por eso el JSON quedó `all=false`, aunque todo el fork
causal pasó. El gate fue retirado para corridas futuras: después del fork, volver explícitamente a
South es ciencia sensata y no rompe apareamiento. Se conservó el raw original.

## Decisión un nivel arriba: MANTENER EL HOST, SUBIR LA DIFICULTAD

No apareció terquedad con evidencia limpia y fuerte; coincide con nuestros datos previos y con la
literatura frontier. Pero ahora tenemos algo que antes faltaba: una creencia propia formada, una
acción propia, un gemelo bilateral y una métrica estructural que efectivamente responden.

El siguiente contraste usa este mismo host, sin rediseñarlo: evidencia conflictiva y menos saliente.
Primero mezcla causal honesta —North contiene observaciones que confirman y refutan la transferencia,
con posterior/verdad computables— y luego un archivo rutinario grande que parece confirmar la ley
vieja junto a una intervención pequeña que la discrimina. Cambiar siempre y mantener siempre siguen
perdiendo en polos distintos.

Crudos:

- `scripts/out/first_story_scm_transfer_fork/probe_DeepSeek-V3.2_seed97200.json`
- `scripts/out/first_story_scm_transfer_fork/probe_gpt-5.4_seed97300.json`
