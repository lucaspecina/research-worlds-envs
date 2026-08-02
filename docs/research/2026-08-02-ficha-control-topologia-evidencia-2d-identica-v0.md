# Ficha prospectiva — control LOCAL/LATENT con evidencia 2D idéntica v0

**Fecha:** 2026-08-02
**Estado:** ejecutada y declarada inválida por procedencia agent-facing incompleta. El raw se
preserva; no se interpreta como negativo. Corrección prospectiva:
[`2026-08-02-ficha-control-topologia-evidencia-2d-identica-v1.md`](2026-08-02-ficha-control-topologia-evidencia-2d-identica-v1.md).

## Pregunta mínima

En `98403`, gpt-5.4 distinguió casi perfectamente A/B en LOCAL sobre la rebanada observada
`H=5`, pero extrapoló mal al resto de la superficie. En LATENT recuperó la media 2D y volvió a
aplanar las dos leyes. Ese contraste mezcla dos cosas: topología y cobertura experimental.

Este control pregunta solamente:

> Si LOCAL y LATENT reciben la misma cobertura mínima en grado y humedad, ¿el agente usa la
> partición visible en LOCAL y sigue aplanando la estructura no observable en LATENT?

No prueba memoria, costo de retrabajo, compromiso profundo ni una tasa poblacional.

## Prefijo y acción inmutables

- modelo: `gpt-5.4`;
- seed: `98403`;
- fuente:
  `scripts/out/first_story_scm_transfer_topology_v1/probe_gpt-5.4_seed98403_resumed_preflight.json`;
- SHA-256 congelado:
  `f049262592a770a21c6d8feea35505b1e38d5d347733d1b788d647302a269acc`;
- se reconstruye el mismo historial y se reproduce byte a byte la misma primera acción North;
- se abren solo dos ramas: LOCAL y LATENT.

El lote elegido por el agente queda igual: ordinario `n=80` y tres celdas controladas en
`H=5`, con `G=1,5,9` (`n=60,80,60`).

## Única intervención

Después de ejecutar esa acción y antes de otra llamada al LLM, el servidor entrega como chequeo
rutinario dos campañas pooled adicionales:

| Variable en el notebook | Sitio | G | H | n | Costo |
|---|---:|---:|---:|---:|---:|
| `north_routine_humidity_low` | North | 5 | 2.5 | 60 | 220 |
| `north_routine_humidity_high` | North | 5 | 7.5 | 60 | 220 |

Quedan `1040` puntos de presupuesto. Las dos ramas usan exactamente los mismos requests, orden y
seeds del servidor. Como en el mundo gemelo ya certificado, `feedstock,outcome` debe coincidir
fila por fila entre LOCAL y LATENT; solo cambia si la etiqueta logística visible identifica la ley
o fue permutada y no la identifica. No se fija ni se nombra ninguna clase.

El aviso al agente es neutral: informa que terminó el chequeo programado, indica los nombres de
las dos tablas y cierra nuevas compras para aislar la evidencia común. No menciona mezcla,
subpoblaciones, A/B, anomalías, residuos, errores ni que el modelo deba cambiar.

## Continuación real

Los DataFrames se inyectan en el mismo kernel vivo. Después el agente recibe al menos un turno
LLM real; puede editar `working_model` y entregar. No habrá más evidencia, aunque podrá usar varios
turnos de cómputo si no entrega en el primero.

Se conservan por rama:

- modelo previo `Mpre`;
- modelo presente justo después de la acción congelada;
- primer modelo distinto de `Mpre` producido después del chequeo;
- primer artefacto observado en el primer turno post-chequeo;
- última entrega puntuable y entrega aceptada;
- transcript, celdas, ledger y scores cero-LLM.

## Compuertas mecánicas antes de gastar API

La corrida con agente queda prohibida salvo que `--cert-only` demuestre:

1. hash, modelo, seed y reconstrucción del prefijo exactos;
2. replay exacto de prefijo y acción en ambas ramas;
3. acción no terminal y mismo presupuesto antes del chequeo;
4. requests y seeds del chequeo iguales;
5. proyección `feedstock,outcome` exacta LOCAL↔LATENT en las 120 filas nuevas;
6. diseño combinado de rango completo en `[1,G,H]`;
7. con exactamente la evidencia combinada, BIC y CV eligen `class_split` en LOCAL y
   `latent_mixture` en LATENT;
8. queda presupuesto positivo y la continuación no puede comprar evidencia adicional;
9. el texto visible no contiene las pistas prohibidas.

## Lectura fijada antes de ver conducta

- **Control limpio:** LOCAL representa bien ambas dimensiones y LATENT no representa la mezcla.
  Refuerza una dificultad específica de descubrir/representar estructura latente.
- **Ambas pasan:** la falla anterior era cobertura o azar, no una limitación estable de topología.
- **Ambas fallan:** la dificultad dominante es modelar/generalizar la superficie 2D, y el contraste
  visible-vs-latente no queda identificado con este anfitrión.
- **LOCAL falla y LATENT pasa:** contradice la jerarquía esperada; se audita antes de interpretar.

No se cambiarán `n`, puntos, wording, número de turnos ni criterios después de mirar una rama. Los
dos resultados se publican juntos aunque sean incómodos.
