# Auditoría de cobertura y elección del primer slice

> **Estado:** etapa 0 cerrada, sin correr agentes.  
> **Propósito:** comprobar cuánto de la nueva guía ya existe de verdad y elegir el primer caso
> por fidelidad científica, no por inercia del código disponible.

## Veredicto corto

WAGER **no empieza de cero**. Ya tiene el núcleo difícil: mundos con verdad oculta, compra de
experimentos, entregas probabilísticas ejecutables, scoring sin juez-LLM, eventos sellados,
presupuestos, corridas largas y ejecución con agentes reales.

Lo que todavía no existe como pieza general es un episodio donde:

1. el agente forme una explicación durante trabajo ordinario;
2. información posterior aparezca sin anunciarse como “corrección”;
3. su modelo ejecutable quede fotografiado rutinariamente durante la trayectoria; y
4. un gemelo determine si correspondía cambiar o conservar.

Por eso la decisión correcta es **adaptar un mundo existente**, no continuar el probe
explícito ni construir otra plataforma desde cero.

## 1. Matriz de capacidades

| Capacidad necesaria | Estado real | Activo reutilizable / brecha |
|---|---|---|
| Verdad oculta y datos generados por el mundo | **Lista** | `WorldServer` + `world.py` por caso |
| Modelo probabilístico ejecutable como entrega | **Lista** | Contrato histórico `model(regime, n, seed)` |
| Score contra verdad, sin LLM | **Lista** | Baterías y scoring distribucional |
| Observación, experimentos y presupuesto | **Lista** | Harness común; ya usado por agentes reales |
| Trayectorias cortas o largas | **Lista** | Runner común; `lab_largo_v0` llega a 40 turnos |
| Datos o fuentes habilitados durante el episodio | **Lista, adaptar narrativa** | Eventos sellados; varios casos actuales los anuncian demasiado |
| Fork/replay desde un checkpoint | **Parcial** | Funciona en `exp_mapa_0154.py`, pero es específico y un snapshot no equivale automáticamente a experiencia vivida |
| Registro silencioso del modelo completo | **Parcial** | El probe técnico lo implementó; el `REGISTER` del lab largo es por línea, da feedback y no sirve tal cual |
| Gemelos con la misma superficie inicial | **Parcial** | Existe el par `overgen`, pero el gemelo no está certificado y el diseño actual no es longitudinal |
| Actualización legal para cualquier mundo | **Parcial** | Hay recetas/oráculos en experimentos concretos; falta una interfaz general y una convención por familia |
| Medir incertidumbre a lo largo del tiempo | **Parcial** | El modelo generativo permite hacerlo; falta el registro rutinario y el análisis temporal |
| Evidencia elegida por el propio agente | **Lista a nivel mecánico** | `experiment()` ya existe; falta diseñar el contraste causal sin confundir búsqueda con asimilación |
| Fricción real por dependencias | **Por construir** | No está representada por los costos artificiales del probe suspendido |
| Generador dinámico de estas trayectorias | **Por construir después** | La fábrica actual genera otros tipos de mundo y aún repite estructura; no cubre esta familia completa |

## 2. Qué aporta cada mundo existente

| Activo | Sirve para | No resuelve todavía |
|---|---|---|
| `overgen_v0` + gemelo | Caso propio de extrapolar una ley local; contraste bilateral; cinco líneas; experimentos y entrega completa | Toda la evidencia está disponible desde el comienzo; no hay creencia previa registrada; el vice aún falla su certificación y el gemelo está incompleto |
| `lab_largo_v0` | Trayectoria real larga, compras ordinarias, eventos y presupuesto | El evento anuncia una decisión importante; el registro da tutoría y ningún agente de las diez trazas lo usó espontáneamente |
| `rabbit_hole_v2` | Esqueleto corto certificado de cinco líneas | No hay trayectoria de revisión ni checkpoints |
| `final_note_*` | Evidencia tardía y gemelos ya medidos | La nota formula explícitamente la tesis; mide una intervención saliente de cierre, no evidencia natural intermedia |
| `first_story_v0` | Una fuente nueva aparece durante el trabajo | No registra la evolución del modelo y estudia otro failure mode |
| Probe modelo+plan | Sandbox y versionado de modelos completos | Su protocolo señala el momento importante y su tarifa de reapertura no representa la fricción que ahora queremos estudiar |

## 3. Candidatos para empezar

| Candidato | Fidelidad al caso | Contraste bilateral | Reutilización | Riesgo principal | Decisión |
|---|---:|---:|---:|---|---|
| Nota final | Baja para evidencia ordinaria | Alta | Alta | Demasiado explícita y terminal | No primero |
| Probe modelo+plan | Baja bajo la guía actual | Alta | Media | Efecto de demanda y fricción artificial | Suspendido |
| KellyBench sintético largo | Potencialmente alta | Media | Media | Mucho diseño antes de saber si el instrumento básico funciona | Después |
| Corral, experimento autogenerado | Alta | Media | Media | Mezcla búsqueda, adquisición y asimilación; fork más complejo | Segundo caso fuerte |
| **`overgen` longitudinal + gemelo** | **Alta para el caso propio** | **Alta** | **Alta** | Hay que corregir la geometría y hacer natural la llegada de datos | **Primero** |

## 4. Primer slice elegido: `overgen` longitudinal

No se convierte todo WAGER en “sobre-generalización”. Se elige esta celda porque es la forma
más barata y limpia de validar la medición longitudinal bilateral.

La idea mínima es:

- el episodio comienza únicamente con un dominio rico donde una ley realmente funciona;
- el agente investiga y mantiene su modelo ejecutable como parte rutinaria del trabajo;
- más adelante entran en operación otros dominios y sus datos aparecen como reportes normales,
  sin palabras como *evidencia*, *refutación*, *pivotear* o *revisar*;
- en el polo vice la ley local no transfiere; en el gemelo sí transfiere;
- el agente puede hacer campañas ordinarias y finalmente debe modelar todos los dominios;
- se comparan el modelo anterior, los modelos posteriores, lo que investigó y la entrega.

El primer slice debe aislar una sola pregunta:

> Después de haber construido una explicación válida localmente, ¿el agente calibra su alcance
> cuando datos ordinarios amplían el dominio, tanto cuando debe corregirse como cuando debe
> conservarla?

### Lo que este slice no autoriza a afirmar

No mide todavía trayectoria muy larga, no-estacionariedad, presión social, fricción de
dependencias ni el caso Corral puro donde el dato contradictorio nace de un experimento elegido
por el agente. Un resultado aquí es una celda del mapa y una validación de infraestructura, no
una teoría general.

## 5. Gate “un nivel arriba” al cerrar cobertura

| Pregunta | Evaluación |
|---|---|
| ¿La pregunta sigue siendo interesante/publicable? | **Sí.** La actualización aplicada durante trabajo con consecuencias y trayectoria sigue siendo el vacío; una sola celda no basta para el paper. |
| ¿Los mundos existentes ya la miden? | **No por sí solos.** Poseen la maquinaria, pero la evidencia actual es inicial o demasiado señalada. |
| ¿Qué constructo amenaza contaminarla? | Registro que funcione como recordatorio, saliencia artificial del evento, dificultad de escribir código y confundir “no buscó” con “leyó pero no asimiló”. |
| ¿Explicaciones más simples? | Olvido, mala lectura del protocolo, falta de datos, incapacidad de modelado o geometría de score defectuosa. Deben quedar observables/certificadas. |
| ¿Estamos sobre-generalizando el último ejemplo? | **No si se mantiene como primer slice.** Se elige por reutilización y bilateralidad; Corral y Kelly siguen como pruebas estructurales posteriores. |
| ¿Siguiente paso de mayor valor? | **Sí:** contrato corto del episodio longitudinal antes de implementar. |
| Decisión | **MODIFICAR** `overgen`; no pivotear el programa, no continuar el probe explícito y no crear un mundo nuevo desde cero. |

## 6. Registro de proceso

- No se corrieron agentes ni tests para elegir la arquitectura.
- La selección no depende de que el caso produzca un efecto “lindo”.
- La certificación roja actual de `overgen_v0` se trata como brecha real, no se oculta.
- Después del contrato se construye solo el camino mínimo y se prueba temprano con un agente
  barato real; luego con uno SOTA.
- Si el slice necesita carteles artificiales para funcionar, no separa cambio/mantenimiento o
  solo mide obediencia al registro, la decisión prevista es **MODIFICAR o ABANDONAR**, no
  seguir invirtiendo por inercia.
