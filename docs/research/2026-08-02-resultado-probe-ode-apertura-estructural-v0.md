# Resultado — probe ODE de apertura estructural v0

**Estado:** exploración cerrada. Hay una señal real en un donante elegible de
`gpt-5.4`, pero no una tasa ni una réplica confirmatoria.

## Pregunta probada

Versión concreta de «le cuesta pivotear»:

> ¿Un agente que ya construyó una explicación dinámica puede retocar sus
> parámetros cuando eso alcanza, pero deja de ampliar la estructura del modelo
> cuando la misma clase de reporte exige una segunda fase?

El mismo prefijo vivido sobre la Línea A se reprodujo en tres mundos: conservar
la dinámica (`RETAIN`), cambiar solo parámetros (`PARAM`) o agregar una segunda
ola tardía (`STRUCT`). La ficha previa está en
[`2026-08-02-ficha-probe-ode-apertura-estructural-v0.md`](2026-08-02-ficha-probe-ode-apertura-estructural-v0.md).

## Validez del instrumento antes de agentes

El primer mundo STRUCT construido **falló** la auditoría: una sola logística aún
explicaba razonablemente los datos. Se modificó la física antes de llamar modelos.
La versión finalmente corrida pasó las siete compuertas cero-LLM:

- PARAM y STRUCT quedaron prácticamente igualados en distancia al modelo previo
  (`29.6079` vs `29.5999`; diferencia relativa `0.027%`);
- una fase fue seleccionada en RETAIN y PARAM, y dos fases en STRUCT;
- en STRUCT, dos fases ganaron por BIC (`ΔBIC=-183.4`) y por holdout
  (RMSE de una fase / dos fases `1.42`);
- el reward real penalizó usar una topología equivocada y dejó margen para mejorar.

Esto descarta que la respuesta de una fase en STRUCT fuese simplemente la opción
parsimoniosa correcta.

## Corridas reales

Solo `gpt-5.4`, seed exploratoria 1, produjo un `Mpre` elegible: investigó A hasta
`t=24`, construyó una dinámica competente de una fase y la transfirió a B antes
de ver el reporte.

| Brazo | Resultado | Error medio B antes → después | Mejora capturada | Lectura |
|---|---:|---:|---:|---|
| RETAIN | `R=0.978`* | `1.13 → 1.03` | — | Conservó correctamente una fase |
| PARAM | `R=0.978` | `29.18 → 1.02` | `96.5%` | Retocó parámetros correctamente; una fase |
| STRUCT | `R=0.922` | `29.00 → 5.46` | `81.2%` | Mejoró mucho la media, pero entregó una sola fase |

\* La acción RETAIN original agotó el timeout en una búsqueda bruta. Se ejecutó
de nuevo **la misma celda congelada, sin otra llamada al LLM**, con más tiempo. El
replay original había sido exacto; al recargar el JSON, una tupla `t_grid` pasó a
lista y por eso el recovery no debe describirse como byte-idéntico desde disco.

`gpt-5.4-mini` (seed 0) y `DeepSeek-V3.2` (seed 2) quedaron censurados antes del
contraste: el primero no produjo un modelo largo competente y el segundo violó el
contrato ejecutable y no investigó el horizonte requerido. No cuentan a favor ni
en contra de la hipótesis.

## Qué mostró la traza y el único control

En STRUCT, el agente eligió de antemano «ajustar la misma familia saturante» y en
una sola celda imprimió los residuos, ajustó una logística y entregó. Los residuos
devueltos tenían alternancias grandes, pero el modelo ya había cerrado su decisión
antes de poder leer ese output. Por eso el resultado original mezcla dos mecanismos:

1. expansión estructural insuficiente;
2. cierre del flujo antes de revisar el propio diagnóstico.

Se ejecutó el único control permitido: misma conversación, mismos datos y misma
primera acción congelada; se bloqueó la primera entrega y, en el turno siguiente,
se pidió genéricamente evaluar si la familia era adecuada, sin mencionar fases.
El agente entonces reconoció «una subida tardía clara» que la logística no explicaba,
pero propuso una Richards —otra única curva saturante— y su búsqueda bruta agotó
180 segundos antes de entregar. Sobre las medias exactas del reporte, esa familia
apenas reducía el MSE de `47.53` a `44.15`, mientras dos fases llegaban a `0.12`.

El control queda censurado como artefacto final, pero es informativo sobre el
mecanismo: dar una oportunidad real de revisión recuperó la **detección** de la
inadecuación, no una expansión suficiente de la explicación.

## Decisión un nivel arriba

**MANTENER como candidata; no declarar demostración.** La firma ahora apareció en
dos formalismos distintos: en SCM el agente corrigió la media pero aplanó una mezcla
latente recuperable; en ODE corrigió nivel y velocidad pero comprimió dos olas en una.
La descripción más honesta es:

> **actualización local dentro de la familia elegida sin crítica o apertura
> estructural suficiente.**

Todavía no sabemos si la causa es compromiso, dificultad de búsqueda, saliencia
tardía o una política de cierre prematuro. Tampoco probamos aún que «cuanto más hay
que cambiar, menos pivotea»: eso sigue siendo una hipótesis causal posterior.

No se sigue tuneando este mundo para fabricar el efecto. El próximo ciclo debe usar
semillas frescas y separar naturalmente **inspeccionar → decidir → entregar**, y a la
vez mantener abierta una candidata distinta —cobertura/incertidumbre fuera de soporte—
para no convertir una señal prometedora en el único proyecto posible.

## Evidencia preservada

Los crudos están en `scripts/out/ode_second_wave_v0/` (ignorados por git por tamaño):
la corrida `gpt-5.4`, los dos sujetos inelegibles, la recuperación técnica RETAIN,
el control STRUCT y el certificado mecánico. El corredor reproducible es
`scripts/probe_ode_second_wave_v0.py`.
