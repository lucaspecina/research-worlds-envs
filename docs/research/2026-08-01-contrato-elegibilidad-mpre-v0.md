# Contrato — dos protocolos de timing y elegibilidad de `M_pre`

> **Estado:** decisión prospectiva, escrita antes de correr el protocolo condicionado.  
> **Motivo:** ADR 0164 mostró que timing=5 deja `M_pre` formado en gpt-5.4 pero no en DeepSeek.

## Decisión conceptual

No se mezclan dos preguntas distintas:

| Protocolo | Cuándo llega el reporte | Qué mide |
|---|---|---|
| **Timing fijo** | En el turno operativo predefinido, exista o no modelo | Cadena ecológica completa: formación, atención, revisión y entrega; `M_pre` ausente es un resultado |
| **Creencia formada** | En el turno siguiente al primer checkpoint elegible | Revisión condicional a que exista un artefacto previo que realmente pueda revisarse |

El segundo no reemplaza al primero. Condicionar el checkpoint cambia el estimando y se reporta.

## Elegibilidad prospectiva v0

Un prefijo queda elegible al final del primer turno que cumple **todo**:

1. leyó las 96 filas del reporte de calificación;
2. la celda terminó sin error;
3. ese turno no compró/recibió observaciones, experimentos ni eventos —es un turno de
   consolidación capaz de incorporar las salidas anteriores—;
4. existe un string `working_model`;
5. el artefacto apareció o cambió en ese turno, para no aceptar un placeholder persistente;
6. pasa el smoke de contrato en los regímenes declarados, sin score ni feedback al agente.

No se exige buen score contra verdad: una creencia equivocada también es una creencia y no debe
excluirse. Se reporta el turno de elegibilidad y la fracción que no llega antes del techo.

## Primera prueba técnica congelada

- Modelo: `DeepSeek-V3.2`.
- Semilla quemada nueva: `92000`.
- Prefijo máximo: 12 turnos; total máximo: 25.
- Los eventos automáticos quedan retenidos server-side; al elegirse `M_pre`, el mismo reporte
  autorado se dispara en el turno siguiente y el agente no ve por qué ocurrió allí.
- Luego, fork exacto a los dos polos y mismos gates de replay/reporte/entrega.

**PASS técnico:** prefijo elegible + replay exacto + un reporte por rama + dos entregas válidas.
La diferencia de score no decide el PASS. Si el prefijo no es elegible, se registra NO-GO y no
se reemplaza silenciosamente dentro de esta corrida.
