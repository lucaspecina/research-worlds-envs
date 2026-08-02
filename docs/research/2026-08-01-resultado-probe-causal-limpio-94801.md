# Resultado — probe causal limpio, DeepSeek seed 94801

> **Estado:** smoke exploratorio con agente real. Semilla quemada. Sirve para validar
> fork, comprensión y scoring; no estima prevalencia ni demuestra todavía revisión de una
> creencia causal formada.

## Resultado técnico

Raw: `scripts/out/first_story_causal_fork/probe_DeepSeek-V3.2_seed94801.json`.

Pasaron todas las compuertas:

- `M_pre` presente y válido;
- replay exacto en ambos polos;
- prefijo y evidencia previos idénticos;
- la misma celda ejecutó las mismas ocho solicitudes experimentales;
- los resultados de esa acción difirieron entre los mundos ocultos;
- ambas ramas terminaron y entregaron artefactos puntuables.

| Polo | R final | Firma verdadera | Firma final del agente |
|---|---:|---|---|
| REVISE | 0.887 | grado `0`; humedad `−12` | grado `+0.68`; humedad `−11.63` |
| RETAIN | 0.815 | grado `+12`; humedad `0` | grado `+12.74`; humedad `+0.42` |

El escenario permite aprender ambos mecanismos y el reward los distingue sin juez LLM.

## La autopsia que cambia la interpretación

El modelo previo era una regresión observacional
`outcome = 20.414 + 1.909*feedstock + ruido`. Ignoraba por completo `regime.config`:
su firma causal previa era grado `0`, humedad `0` en ambos mundos. Por lo tanto, al abrirse
el fork el agente todavía no había comprometido una explicación causal ejecutable.

La corrida demuestra **aprendizaje causal bilateral desde una creencia incompleta**, no
“revisar en REVISE y conservar en RETAIN”. Llamarla revisión de creencias sería inflar el
resultado. En RETAIN el primer modelo modificado ya alcanzó `R=0.833`; en REVISE hubo una
transición confundida y recién la entrega final capturó el mecanismo correcto.

## Decisión un nivel arriba: MODIFICAR

No escalar este caso ni agregar memoria. El próximo host debe crear primero una explicación
causal propia y puntuable sobre un prefijo realmente común. Propuesta mínima: dos regiones o
salas. En la región inicial, ambos mundos son idénticos y permiten investigar/usar una ley
causal; luego una segunda región entra al flujo normal y puede conservar esa ley o exigir una
revisión local. Sobre ese estado sí se compara evidencia limpia, conflictiva y neutral.

La lección no es técnica sino de constructo: **un modelo válido no equivale a una creencia
relevante ya formada**. Los próximos gates deben certificar la firma causal de `M_pre`, no
solo que el código compile.
