# Resultado — probe pequeño DeepSeek `overgen_stream`

> **Estado:** exploratorio, tres donantes; no inferencia poblacional.
> **Unidad:** donante/historial, no seis ramas independientes.

## Integridad

La tanda 94000–94002 quedó inválida por `plt.show()` bloqueante en el kernel headless. Se fijó
`MPLBACKEND=Agg`, se agregó un test offline y se usaron las semillas nuevas registradas
94100–94102. En la tanda válida:

- 3/3 formaron la creencia objetivo;
- 3/3 tuvieron replay y ledger exactos en ambos gemelos;
- 3/3 recibieron un reporte por rama y entregaron 2/2 modelos válidos.

## Resultado por donante

| Donante | Turno `M_pre` | SD previa | `R` limitado | `R` transferencia | Diferencia apareada |
|---|---:|---:|---:|---:|---:|
| 94100 | 4 | 2.47 | 0.913 | 0.916 | -0.003 |
| 94101 | 12 | 0.72 | 0.114 | 0.727 | -0.613 |
| 94102 | 4 | 2.51 | 0.934 | 0.929 | +0.005 |

Los dos donantes tempranos tenían modelos previos muy anchos y malos. El reporte funcionó
también como oportunidad de completar el modelo; ambos terminaron bien en los dos mundos. Esto
es conducta ecológica válida, pero no aísla resistencia de revisión.

94101 llegó mucho más tarde con un modelo estrecho y competente en el gemelo (`R_diag=0.816`).
Es el caso informativo:

- en alcance limitado, la referencia podía subir de `0.161` a `0.855`, pero la entrega bajó a
  `0.107`: fracción capturada `-0.078`;
- en transferencia, conservar era la referencia exacta; el agente cambió igualmente y bajó de
  `0.816` a `0.696`;
- el razonamiento notó que líneas 2–3 tenían peor ajuste y que la variación alta había crecido,
  pero entregó un único cuadrático con offsets + heterocedasticidad. Es compatible con
  sobre-generalización/implementación inadecuada, no con falta de acceso a la evidencia.

## Corrección de la referencia, visible y posterior

La referencia v0 reconstruía desde cero y podía quedar peor que un buen `M_pre`. Después de
detectar el defecto se creó la versión **prior-preserving** y se recalcularon los tres crudos:

- evidencia compatible: devuelve el `M_pre` byte por byte;
- refutación parcial: actualiza media y dispersión solo en líneas 2–3 para `driver>4`;
- región vieja y líneas 1/4/5 quedan idénticas.

Esta reparación no altera agentes ni scores contra verdad. Las fracciones v3 son las vigentes;
v1/v2 se conservan como auditoría del desarrollo del instrumento.

## Gate superior

**MANTENER la dirección.** El mundo produjo tanto revisión competente como una falla bilateral
rica y localizable; el pipeline reveló cuándo el modelo previo aún era demasiado débil para
atribuir resistencia. No hay base para prevalencia ni comparación de modelos.

Siguiente paso autorizado: una sola réplica gpt-5.4 fresca con el protocolo ya congelado. Luego
se detienen agentes y se decide el diseño de un piloto multi-modelo o un pivote de este slice.

Crudos y síntesis: `scripts/out/overgen_stream_fork/technical_DeepSeek-V3.2_seed9410*.json`,
`probe_DeepSeek-V3.2_seed9410*_scores_v3.json` y
`probe_DeepSeek-V3.2_94100_94102_summary_v1.json`.
