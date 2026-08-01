# Resultado — gate de creencia objetivo y fork prospectivo DeepSeek

> **Estado:** validación técnica prospectiva; `n=1`, no resultado del paper.
> **Contrato:** `2026-08-01-contrato-gate-fenotipo-overgen-v0.md`.

## Resultado corto

La semilla 93000 quedó quemada por el bug de persistencia de timeout descrito en la enmienda.
Con el manejo corregido y semilla nueva 93001, todos los gates pasaron:

- `M_pre` elegible en turno 3;
- creencia objetivo presente: `shape_spread_noise_ratio=0.023` (umbral `1.0`);
- replay exacto de chat, kernel y evidencia en 2/2 ramas;
- un reporte ordinario por rama;
- entrega válida 2/2;
- `R_final=0.879` en alcance limitado y `0.899` en transferencia.

Crudo: `scripts/out/overgen_stream_fork/technical_DeepSeek-V3.2_seed93001_eligible.json`.

## Referencia legal desde el ledger

El ledger contiene exactamente dos objetos por rama: las 96 filas de calificación y las 64 del
reporte. El actualizador congelado, sin verdad oculta:

- especializó solo líneas 2–3 en alcance limitado;
- mantuvo la estructura compartida en las cinco líneas del gemelo;
- alcanzó `R_diagnostic=0.920` y `0.939`, respectivamente.

Fracción de la mejora diagnóstica de referencia capturada:

| Checkpoint | Alcance limitado | Transferencia |
|---|---:|---:|
| Primer modelo realmente cambiado | 0.669 | 0.275 |
| Entrega final | 0.983 | 0.989 |

Esto muestra que mirar solo la entrega habría ocultado una asimilación gradual distinta entre
ramas.

## Lo incómodo, que queda visible

1. `M_pre` contenía la forma compartida, pero era muy ancho (`SD` predictiva mediana `4.33`) y
   puntuaba al piso. El gate certifica la **estructura de la creencia**, no competencia ni alta
   confianza. La confianza/compromiso deberá medirse como moderador, no esconderse con exclusión.
2. En alcance limitado, la entrega final fue buena globalmente pero la línea 4 diagnóstica quedó
   en `R=0.101`, mientras 2–3 quedaron en `0.931/0.957`. Es una falla local que la nota global
   habría tapado.
3. La corrida no demuestra resistencia, superioridad de modelos ni prevalencia. Solo demuestra
   que el pipeline ya puede distinguir formación de la creencia, cambio gradual, selectividad y
   consecuencia final con un agente real.

## Gate superior

**MANTENER instrumento; no escalar todavía.** No se modifica el mundo para embellecer este caso.
Se autoriza un probe exploratorio de tres donantes baratos, todos contabilizados aunque no sean
elegibles. Después se vuelve a evaluar pregunta, fidelidad, medición y costo antes de una corrida
SOTA.
