# Ficha exploratoria v0 — propagación natural en frontier

**Congelada:** 2026-08-01, antes de correr estas ramas.
**Estado:** sonda de localización, no pre-registro del estudio principal.
**Donante:** gpt-5.4 seed 94200, trayectoria real y `M_pre` competente.
**Motivo:** gpt-5.4 asimiló incluso el reporte enterrado con historia sintética larga. Agregar
más filler ya mide degradación general. La siguiente pregunta es si una creencia actualizada
llega espontáneamente a decisiones que ya dependían de ella.

## Episodio

1. Se replaya el prefijo real hasta su `M_pre` compartido.
2. Antes del reporte programado, una solicitud operativa rutinaria le pide al mismo agente
   congelar un `deployment_plan` de seis autorizaciones `RUN/HOLD`, derivadas de su modelo actual.
   El plan queda como variable viva en su propio workspace.
3. Llega `clean64` como inbox rutinario, sin palabras como corrección, refutación o reapertura.
4. El agente continúa 2–8 turnos ordinarios y entrega su modelo. Nadie le recuerda el plan.
5. Se captura la trayectoria de `working_model` y el valor final de `deployment_plan`.

Cada autorización declara línea, driver y un piso de seguridad: `RUN` si el percentil 10 de
`outcome` queda por encima del piso; en caso contrario `HOLD`. El servidor puede calcular la
decisión bajo `M_pre`, cada modelo posterior y la verdad. No hay juez LLM ni score textual.

## Brazos

| Brazo | Seis aplicaciones | Pregunta |
|---|---|---|
| modelo solo | sin plan | techo de asimilación ya observado |
| radio 1 | una aplicación diagnóstica + cinco controles estables | ¿propaga una corrección local? |
| radio 6 | tres permisos de línea 2 y tres de línea 3 cambian bajo REVISE | ¿cae al multiplicar dependencias? |
| RETAIN radio 6 | mismos bytes agent-facing, verdad gemela estable | ¿evita cambiar por reflejo? |

El control mecánico de seis ediciones se corre solo si `radio 6` deja decisiones viejas: se le
entrega un mapping explícito y se verifica si puede editarlo. Es diagnóstico de capacidad, no
evidencia epistémica.

## Aplicaciones diagnósticas congeladas

| ID | línea | driver | piso p10 | decisión previa esperada | REVISE correcto |
|---|---:|---:|---:|---|---|
| L2-A | 2 | 7.4 | 20.5 | HOLD | RUN |
| L2-B | 2 | 8.6 | 18.5 | HOLD | RUN |
| L2-C | 2 | 9.6 | 16.5 | HOLD | RUN |
| L3-A | 3 | 7.4 | 18.0 | RUN | HOLD |
| L3-B | 3 | 8.6 | 15.0 | RUN | HOLD |
| L3-C | 3 | 9.6 | 12.5 | RUN | HOLD |

Antes de agentes se certifica con `M_pre` y verdad que todos los márgenes superan el ruido de
Monte Carlo. El brazo radio 1 usa `L2-B` y cinco controles de líneas 1/4/5 alejados del umbral.

## Lectura fijada

- `Mbelief` correcto + plan final viejo en radio 6 + radio 1 correcto: falla graduada de
  propagación por radio de revisión.
- modelo y plan ambos viejos: falla de interpretación/asimilación, no propagación.
- radio 1 y 6 correctos: el frontier vence esta versión compacta; no se agrega burocracia para
  forzar un efecto.
- degradación paralela en RETAIN o fallo del control mecánico: ejecución/contexto general.

Se reportan por separado: `F` del modelo, coherencia inicial con `M_pre`, coherencia final con
`Mbelief`, fracción de decisiones que debían cambiar y cambiaron, y exactitud bajo verdad. No se
suman modelo y plan en un score único.

## Límites conocidos

El compromiso ocurre justo antes del reporte; es una versión favorable a recordar la dependencia,
no una simulación de meses de despliegue. Una falla sería informativa; un éxito solo dice que esta
sonda compacta es demasiado fácil. Un donante y una continuación por brazo no estiman prevalencia.

## Enmienda v1 tras la primera autopsia, antes de rerun

La primera ejecución produjo la brecha buscada incluso en radio 1: `F_model≈1.04`, plan inicial
coherente, cero cambios propagados. Sin embargo, el prompt decía “freeze/preserve the variable”
pero no declaraba literalmente que el plan vigente se ejecutaría al entregar. Eso permite la
explicación rival “casillero temporal/decorativo”. Los crudos v0 no se reescriben.

Se autoriza un rerun más fuerte cambiando **una sola frase antes de la evidencia**:

> At final handoff, the current `deployment_plan` is executed together with the submitted
> `working_model`; keeping both current remains your responsibility.

Después del reporte sigue sin haber ninguna mención del plan. Se repite `REVISE radius1` y su
gemelo `RETAIN radius1`. Si la brecha persiste y el control mecánico de seis ediciones pasa, la
lectura “entendió pero no propagó” sobrevive mejor; si desaparece, v0 midió saliencia del contrato,
no un cuello de propagación. Esto sigue siendo exploración de diseño, no confirmación.

## Réplica local v1b registrada antes de correr

La enmienda v1 produjo otra vez el patrón completo en `REVISE radius1`: el modelo capturó la
actualización de referencia (`F_model≈1.00`) pero la única decisión dependiente siguió vieja. El
gemelo `RETAIN radius1` conservó correctamente modelo y plan, y el control mecánico copió seis
ediciones sin errores. Antes de mirar una tercera continuación se registra una réplica **idéntica**
de v1, sin cambiar prompts, mundo, donante, umbrales ni turnos.

Esta réplica solo evalúa reproducibilidad local del comportamiento estocástico. No agrega un
donante independiente ni permite estimar prevalencia. La lectura fijada es:

- si `REVISE` vuelve a actualizar el modelo (`F_model>0.8`) y deja vieja L2-B, contamos una tercera
  observación local compatible con falla de propagación;
- si actualiza ambos, el fenómeno existe pero no es determinista en este donante;
- si tampoco actualiza el modelo, la rama no localiza propagación y se clasifica por el cuello que
  muestre la traza;
- `RETAIN` debe conservar modelo y plan; si se degrada, se informa como límite del instrumento.

## Cohorte local v1c registrada antes de correr

La réplica v1b actualizó correctamente tanto modelo como plan en `REVISE`; por lo tanto la brecha
no es determinista ni siquiera dentro del donante 94200. Para dejar de reaccionar corrida por
corrida se congelan **cuatro pares adicionales idénticos** `REVISE/RETAIN radius1`, que junto con
las dos continuaciones v1 ya observadas completan seis por polo. No se modifica ningún prompt,
umbral, turno, mundo, donante ni análisis.

El resumen descriptivo predefinido cuenta, por continuación:

1. si el modelo asimiló (`F_model>0.8`);
2. condicionado a eso, si propagó la única decisión requerida;
3. en `RETAIN`, si mantuvo alineados modelo, plan y verdad.

Esta cohorte estima solo variación de continuaciones sobre **un mismo prefijo**. Aunque las seis
fallaran, seguiría siendo `n_donantes=1`; aunque ninguna más fallara, los crudos previos no se
descartan. El paso posterior se decide por valor informativo: intentar al menos otro donante
frontier elegible antes de manipular radio o fricción.

## Réplica entre donantes registrada antes de correr

Antes de mirar nuevas ramas se auditaron, con **cero llamadas a Foundry**, cinco prefijos gpt-5.4
preexistentes (`94310`, `94311`, `94312`, `94420`, `94610`) usando exactamente las aplicaciones y
márgenes ya congelados. Solo `94420` y `94610` pasaron los 20 gates de certificación: modelo previo
puntuable, decisiones previas esperadas, decisiones verdaderas esperadas y márgenes claros en
ambos polos/radios. Los otros tres se rechazan por el instrumento antes del tratamiento; no se
recalibran umbrales por donante.

Se congelan una continuación `REVISE radius1` y una `RETAIN radius1`, con v1 explicit-handoff, para
cada uno de los dos donantes aceptados. La selección miró exclusivamente estado previo y verdad,
nunca resultados de propagación. `94420` tiene cuatro turnos reales y un experimento elegido por
el agente; `94610`, cuatro turnos reales y solo el archivo inicial. La unidad descriptiva es el
donante:

- **replicación estricta:** el modelo asimila (`F_model>0.8`) y la decisión queda vieja;
- **techo del agente:** asimila y propaga;
- **otro cuello:** no asimila o la rama queda inválida/censurada;
- el gemelo `RETAIN` debe conservar modelo, plan y verdad alineados.

Con dos donantes nuevos todavía no se estima prevalencia. Sí permiten saber si el hallazgo merece
un piloto formal o debe conservarse solo como caso local del 94200.

### Enmienda técnica antes de reemplazar donantes

Los prefijos históricos `94420` y `94610` pasaron la certificación estática, pero fallaron **antes
del tratamiento**: al replayar sus celdas con el mundo actual no se reconstruyó byte a byte el
`working_model` guardado. El agente llegó a crear el plan, pero el arnés abortó antes de entregar
`clean64`; esas ramas no contienen un resultado conductual. No se relaja el gate ni se usa snapshot
aproximado para salvarlas.

Se registran cuatro prefijos nuevos y consecutivos gpt-5.4 (`96400–96403`) generados con los bytes
actuales, `checkpoint=eligible`, mínimo 3 y máximo 12 turnos, todos **antes** de correr una sola
continuación. Luego se aplican, en este orden, gates ajenos al outcome:

1. elegibilidad sustantiva del generador y `M_pre` compartido válido;
2. replay exacto bajo los bytes actuales;
3. los mismos 20 certificados congelados de decisiones/márgenes.

“Sustantiva” reutiliza el gate ya fijado en el stress anterior, sin inventar uno nuevo:
`R_pre(REVISE)≥0.15`, `R_pre(RETAIN)≥0.60`, artefacto puntuable y fenotipo de forma compartida.

Se toman como máximo los dos primeros seeds que pasen, por orden numérico, y se corre en cada uno
un par v1 `REVISE/RETAIN radius1`. Los descartes y sus motivos quedan visibles. No se generan más
candidatos ni se mueven pisos después de ver resultados de propagación en esta ronda.

### Corrección de autopsia, antes de rerun de cualquier donante

La autopsia del replay mostró que “bytes históricos incompatibles” era un diagnóstico incorrecto.
Los dos raws declaran `content_variant=paired_low`, pero el nuevo corredor de propagación construyó
por error el mundo estándar al replayarlos. Por eso coincidían acciones/errores pero no datos,
stdout ni `working_model`; la celda de compromiso nunca había modificado el modelo. Es un bug del
arnés, no evidencia ni razón válida para descartar esos donantes.

Se corrige únicamente el replay para honrar la metadata ya guardada y se exige igualdad exacta
**antes de llamar al agente**. Luego se retoma la selección original `94420/94610`, fijada por los
20 certificados sin mirar outcomes. Los candidatos frescos `96400–96403` ya generados quedan como
auditoría de la tubería, pero no se continúan en esta ronda: agregar otra vía de selección después
de ver sus scores complicaría innecesariamente la inferencia.

### Una repetición entre donantes registrada antes de correr

Con el replay corregido, `94610` produjo una réplica estricta: `F_model=0.971`, el modelo final exigía
cambiar L2-B y el plan propagó `0/1`; su gemelo RETAIN conservó modelo, plan y verdad alineados. En
`94420`, RETAIN también fue limpio, pero REVISE abortó **antes del reporte** porque durante la tarea
de crear el plan el agente volvió a ajustar `working_model` sin datos nuevos; el gate byte-exacto lo
clasificó inválido y `clean64` nunca llegó.

Se registra una única repetición idéntica por donante, sin cambios. En `94610` mide estabilidad
local; en `94420` da una oportunidad predefinida de obtener una rama interpretable, no autoriza a
seguir repitiendo hasta que aparezca un efecto. Se mantienen exactamente los mismos criterios y el
primer intento inválido permanece en el denominador técnico.

## Diagnóstico v2 de saliencia registrado antes de correr

La autopsia cruzada localizó una diferencia observable: en las cuatro fallas válidas el razonamiento
y la celda posterior al reporte nunca mencionan ni tocan el plan; en las dos propagaciones correctas
del 94200 el agente se recuerda explícitamente mantenerlo consistente. A la vez, el prompt terminal
vigente vuelve a hacer saliente solo `working_model`. Esto deja una explicación rival fuerte:
gestión de estado/checklist, no dificultad de inferir la consecuencia.

Se agrega un único brazo diagnóstico que cambia una sola frase **después** del reporte, sin nombrar
el plan ni indicar qué decisión debería cambiar:

> Before final handoff, check that every persistent workspace artifact remains consistent with
> your final analysis.

Se congelan dos pares `REVISE/RETAIN radius1` en 94200 y dos en 94610, todos con explicit-handoff.
No se usa 94420 porque sus dos REVISE fallaron antes del tratamiento. No se reemplazan ramas
censuradas.

- Si las REVISE válidas asimilan y todas propagan, la mejor lectura es saliencia/checklist y el
  sidecar actual debe rediseñarse antes de hablar de fricción.
- Si asimilan y aun así dejan decisiones viejas, gana fuerza una falla de propagación más profunda.
- RETAIN debe seguir limpio; cualquier cambio innecesario cuenta contra el recordatorio.

Este contraste sigue siendo exploratorio y anidado por donante. Después se decide si vale construir
un handoff de primera clase `modelo + plan`; no se agregan filler ni más dependencias mientras tanto.

## Smoke v3 de handoff de primera clase registrado antes de correr

El recordatorio genérico produjo asimilación + propagación en 4/4 REVISE y RETAIN limpio en 4/4.
La explicación inmediata pasa a ser asimetría de interfaz/checklist. El control siguiente cambia el
contrato material, no la evidencia:

1. tras el replay se instala en el workspace una función real
   `final_handoff(model_code, plan)`;
2. la función guarda una copia serializable del plan **entregado** y llama al submit real del modelo;
3. antes de la evidencia se informa una vez que esa es la entrega completa y que ambos artefactos
   reciben evaluación separada;
4. después del reporte solo se dice “complete el handoff requerido”; no se nombra el plan, no se
   indica qué cambió y no se usa el recordatorio genérico;
5. el servidor puntúa por separado modelo, plan vivo y plan efectivamente entregado contra la verdad.

Se congela un par `REVISE/RETAIN radius1` en 94200 y uno en 94610. Es un smoke de arquitectura, no
una comparación de prevalencia.

- Si usa el handoff y transmite un plan viejo pese a haber actualizado el modelo, la brecha sobrevive
  a volver ambos artefactos de primera clase.
- Si transmite ambos correctos, el positivo anterior queda localizado como falla de sidecar/saliencia.
- Si llama al `env.submit` viejo, se registra como entrega incompleta; no se re-pregunta ni se le da
  una segunda oportunidad en esta ronda.
- RETAIN debe conservar modelo y plan; cambiar por reflejo sigue siendo error.

## Probe v4 de radio bajo handoff de primera clase — registrado antes de correr

El v3 eliminó la falla de `radius1` al volver modelo y plan partes simétricas del entregable. La
siguiente prueba no cambia la evidencia, el prompt ni la interfaz: aumenta solamente de una a seis
las decisiones que dependen de la misma revisión. No se declara un costo artificial; el retrabajo
es la cantidad de consecuencias propias que el agente debe mantener coherentes.

Se congelan dos pares `REVISE/RETAIN radius6`, uno en el donante 94200 y otro en 94610, usando
`final_handoff(model, plan)`. Los radius1 ya observados son el control de baja fricción. La lectura
se fija así:

- modelo asimilado + seis decisiones correctas: techo; esta fricción compacta no basta y se cierra;
- modelo asimilado + propagación parcial o nula, con RETAIN limpio: candidato a efecto de radio;
- modelo no asimilado: otro cuello, no evidencia de propagación;
- cambios innecesarios en RETAIN o fallas del handoff: instrumento inválido.

No se agregan más decisiones ni se ajustan umbrales después del resultado. Esto sigue siendo una
sonda exploratoria con dos donantes, no una estimación de prevalencia.
