# Ficha congelada — fork técnico `overgen_stream` v0

> **Estado:** integración exploratoria; escrita antes de correr. No es pre-registro del probe.  
> **Modelo:** DeepSeek-V3.2. **Donante/semilla quemada:** `91000`.

## Pregunta

¿Puede un único trabajo previo vivido continuar desde exactamente el mismo historial
conversacional y estado de Python en los dos polos, recibir el reporte ordinario correspondiente
y producir una trayectoria medible `M_pre → M_post → M_final`?

## Procedimiento congelado

1. Ejecutar una sola conversación durante los turnos 1–4 sobre el prefijo común.
2. Guardar mensajes, celdas, salidas y último `working_model`.
3. Crear dos servidores frescos con el mismo `seed_offset` y reproducir las cuatro celdas sin
   LLM. Exigir coincidencia de stdout, error y modelo capturado.
4. Clonar la lista exacta de mensajes del chat; desde el turno 5 continuar una copia en alcance
   limitado y otra en transferencia.
5. En ambas ramas el evento del turno 5 inyecta el mismo tipo de reporte en
   `commissioning_report`; solo los outcomes y la verdad posterior difieren.
6. Guardar trazas completas, modelos y scores full/diagnóstico para `M_pre`, primer modelo
   posterior y entrega.

## Gates técnicos

- el donante no entrega antes del reporte;
- existe un `M_pre` string (su calidad se reporta, no se usa para excluirlo);
- replay exacto en las dos ramas;
- un único reporte se inyecta en cada rama;
- ambas ramas producen entrega válida dentro de 18 turnos totales;
- ningún score o diagnóstico vuelve al agente;
- los crudos se conservan aunque los scores sean feos.

## Regla de decisión

- **PASS:** todos los gates técnicos; se escribe recién después la ficha del probe pequeño.
- **MODIFICAR:** falla mecánica o de UX que puede corregirse sin cambiar el fenómeno; repetir
  con otra semilla quemada y registrar ambas.
- **NO-GO:** el fork altera el prefijo, no conserva el estado o requiere un snapshot resumido
  que ya no representa trabajo vivido.

El patrón conductual y la diferencia de `R` **no** deciden el PASS técnico.

## Resultado de la corrida congelada y addendum previo al segundo intento

DeepSeek `seed=91000` dio **NO-GO**: replay exacto 2/2 y un reporte por rama, pero no existía
`M_pre` al turno 4; alcance limitado entregó `R=0.895` y transferencia agotó 18 turnos sin
entregar. Los crudos se preservan en
`scripts/out/overgen_stream_fork/technical_DeepSeek-V3.2_seed91000.json`.

No se modifica timing, mundo, turnos ni gates después de verlo. Para separar “fork roto” de
“donante/modelo inelegible a este timing”, antes de abrir otra salida se fija un segundo intento:

- modelo `gpt-5.4`, seed nueva quemada `91001`;
- exactamente el mismo script, cuatro turnos de prefijo y máximo 18;
- mismos gates y misma regla de decisión;
- aunque pase, el negativo de DeepSeek permanece y prohíbe incluirlo en un probe a este timing
  sin diseñar prospectivamente una condición de horizonte distinta.
