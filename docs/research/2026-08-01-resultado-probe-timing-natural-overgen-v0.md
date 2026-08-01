# Resultado — probe real de timing natural en `overgen_stream`

> **Alcance:** 4 intentos DeepSeek y 3 gpt-5.4, con 4 forks interpretables; varias versiones
> prospectivas explícitas del calendario. Evidencia de diseño, no estimación poblacional.

## Por qué se corrió

Se interrumpió el diseño de un piloto grande para responder primero una duda más barata: si la
evidencia llega por calendario, sin esperar a que el detector encuentre una creencia conveniente,
¿el mundo todavía produce trayectorias reales e interpretables?

## Lo que falló y se corrigió

1. Reporte después de ocho turnos: un DeepSeek no tenía modelo y otro entregó justo antes.
2. Al moverlo al comienzo del turno 8, dos DeepSeek produjeron forks íntegros.
3. gpt-5.4 entregó antes de la comisión. Era un defecto del mundo: el brief prohibía de hecho esa
   entrega, pero el servidor la aceptaba. Ahora esos mundos rechazan `submit()` hasta que se cumple
   el hito, sin terminar el episodio ni revelar el contenido del reporte.
4. Con ese arreglo, se volvió al evento nativo y más simple: reporte automático en turno 5.

Cada cambio quedó escrito antes de su corrida y las semillas fallidas permanecen quemadas.

## Resultados interpretables

| Modelo/semilla | Evento | Estructura previa | Final limitado | Final transferencia | Consecuencia |
|---|---:|---:|---:|---:|---|
| DeepSeek 94302 | t8 | compartida `0.033` | diferenciada `3.60` | compartida `0.035` | `R 0.847 / 0.908` |
| DeepSeek 94303 | t8 | compartida `0.046` | diferenciada `3.25` | compartida `0.207` | `R 0.877 / 0.000` |
| gpt-5.4 94311 | t8 | diferenciada `1.90` | diferenciada `1.94` | compartida `0.104` | `R 0.811 / 0.841` |
| gpt-5.4 94312 | t5 nativo | diferenciada `6.27` | diferenciada `2.81` | compartida `0.364` | `R 0.868 / 0.693` |

`ratio <= 1` significa forma compartida; `ratio > 1`, diferenciación material entre líneas.

### El caso 94303

No sobrerrevisó la estructura en transferencia: la conservó compartida. La caída a `R=0` vino de
inflar la incertidumbre al propagar por separado errores de parámetros ignorando sus covarianzas.
Esto demuestra que revisión estructural y calibración distribucional son cuellos distintos; un
score final solo los habría mezclado.

### Los casos SOTA

Ambos usaron correctamente la evidencia para distinguir los polos, pero ya habían fragmentado la
ley antes de recibirla. Por eso validan actualización bilateral natural, no resistencia de un SOTA
casado con una generalización compartida.

## Gate un nivel arriba

- **Pregunta:** sigue siendo interesante.
- **Instrumento:** pasa; el evento natural, replay y modelo ejecutable distinguen estructura y
  consecuencia sin juez LLM.
- **Esta versión como experimento principal:** no pasa todavía. En gpt-5.4 la creencia objetivo no
  apareció de forma estable al momento fijo; escalar semillas condicionadas volvería artificial el
  fenómeno.
- **Decisión:** **MANTENER la pregunta y la maquinaria; NO ESCALAR; INVESTIGAR EL NEGATIVO.** Las
  trazas sugieren dos causas de diseño antes de cuestionar el vicio: el modelo sobreajusta curvas
  por línea con poco soporte inicial y el retraso hasta t8 agrega espera, no trabajo ni compromiso.
  Se probarán por separado variantes mínimas de esas dos condiciones con agentes reales. Corral
  queda como segunda estructura, no como salto automático.

Crudos y trayectorias estructurales: `scripts/out/overgen_stream_fork/technical_*943*.json`,
`probe_structure_94302_94303_scheduled_v1.json`, `probe_structure_gpt94311_scheduled_v1.json` y
`probe_structure_gpt94312_fixed_v1.json`.
