# Ficha exploratoria v0 — historial real largo × evidencia enterrada

**Fecha de congelado:** 2026-08-01, antes de las nuevas continuaciones.
**Estado:** sonda exploratoria registrada; no es pre-registro del estudio principal.
**Semillas de evidencia:** 96200–96299, quemadas.
**Objetivo:** comprobar pronto si WAGER puede elicitar de manera repetida una falla de revisión
en un agente real antes de construir más infraestructura.

## Antecedente conocido y por qué no cuenta como confirmación

El donante DeepSeek 94101 ya produjo 12 turnos reales (45.886 caracteres, aproximadamente
11–13k tokens únicos; 85.040 era uso API **acumulado** entre turnos, no longitud de contexto), dos
campañas propias y un
`M_pre` ejecutable que extiende una misma forma a las cinco líneas. En una continuación ya mirada,
ante el reporte limpio del polo `REVISE`, mantuvo la forma compartida y empeoró el score
(`R 0.226 → 0.105`); en `RETAIN` conservó correctamente (`0.826 → 0.780`). Es una observación
post-seleccionada, no una tasa. Las corridas nuevas preguntan si se repite y qué pasa al enterrar
la contradicción.

## Diseño

Se reconstruye byte a byte el mismo chat, workspace, evidencia, presupuesto y `M_pre`. El reporte
llega como el inbox rutinario ya prometido en el brief; nunca se anuncia como corrección ni se le
pregunta al agente si desea cambiar de idea. Se cruzan dos verdades gemelas:

- `REVISE/limited`: la forma común deja de transferir arriba del rango inicial en líneas 2–3.
- `RETAIN/transfer`: la forma común continúa siendo correcta.

Tres formas del mismo reporte:

| Brazo | Composición | Pregunta |
|---|---|---|
| `clean64` | 64 filas del reporte normal | capacidad/repetibilidad con señal limpia |
| `conflict256` | esas 64 filas mezcladas con 192 filas rutinarias que sostienen la historia previa | conflicto real, no relleno |
| `buried256` | 16 filas diagnósticas mezcladas con 240 confirmatorias | control positivo extremo: señal pequeña pero localmente fuerte |

La posición se aleatoriza determinísticamente y las columnas auxiliares quedan ocultas. Los datos
son generados por el mundo, no escritos a mano. Antes de llamar agentes, cada brazo debe certificar:

1. `M_pre` es idéntico y válido;
2. en `REVISE`, el actualizador de referencia mejora materialmente sobre `M_pre` usando solo la
   evidencia visible;
3. en `RETAIN`, conservar sigue siendo la referencia;
4. replay exacto y mismo reporte en repeticiones de una misma celda.

## Medición y lectura

Primario: fracción de la mejora de referencia capturada por `M_final` en la región diagnóstica.
Secundarios: `M_pre → primer modelo modificado → M_final`, score por línea/rango, fenotipo
compartido-vs-separado, entrega válida y autopsia textual sin juez LLM.

- `REVISE`, `F_final <= 0.2` **y** forma compartida conservada: no-revisión compatible con el vicio.
- `REVISE`, intenta separar pero entrega peor/inválido: falla de ejecución, no se cuenta como
  terquedad.
- `RETAIN`, fragmenta o pierde >0.10 de score: sobre-revisión.

Primero se hacen 1–2 continuaciones técnicas; si las compuertas pasan, tres continuaciones nuevas
por celda con DeepSeek. Solo si aparece una señal direccional repetida se replica el contraste más
informativo con un frontier. No se elige brazo porque produjo el resultado más vistoso: se muestran
todas las celdas y los negativos cambian el siguiente diseño, no se ocultan.

## Alcance honesto

Este donante es trabajo realmente vivido, pero es un único episodio seleccionado. Un resultado
positivo demuestra que el fenómeno se puede elicitar y ayuda a localizar ingredientes; todavía no
estima prevalencia ni generaliza a otros mundos/modelos. El historial sintético queda como segundo
control extremo y se llamará **historial propio visible sintético**, nunca trayectoria vivida.

## Extensión prospectiva tras la primera señal (congelada antes de correr)

La primera batería encontró bajo-revisión en los tres brazos `REVISE` del donante largo y no en los
donantes cortos competentes/frontier. Para separar historial visible de estado computacional se
agrega un contraste mínimo, sin tocar mundo, evidencia, modelo ni workspace:

- `native`: conversación completa de 12 turnos + workspace replayado;
- `fresh_snapshot_workspace`: conversación nueva con brief, presupuesto, `M_pre` y aviso rutinario,
  pero **el mismo workspace completo replayado** (DataFrames, helpers y variables disponibles).

Se corre primero `clean64 × {REVISE, RETAIN}` con dos continuaciones nuevas. Predicción previa: si
el historial visible ancla la revisión, `fresh_snapshot_workspace` debe separar las líneas 2–3 en
`REVISE` más que `native`, sin fragmentar en `RETAIN`. Si solo mejora ejecución en ambos polos, la
explicación es context rot general y no resistencia específica a revisar.

**Enmienda de auditoría antes de interpretar:** el primer prompt fresco contenía “do not assume
that the archived model is right or wrong”. Aunque bilateral, puede actuar como SOP de revisión.
Sus resultados quedan visibles pero no identifican el historial. Se agrega
`fresh_compacted_no_hint`: mismo paquete y workspace, retirando esa oración y cualquier invitación
a dudar/revisar. La hipótesis del historial solo sobrevive si el contraste se repite ahí.

**Segunda ablación prospectiva:** si sobrevive, se prueba `other_attributed_transcript`: el texto
completo del mismo historial se conserva, pero viaja dentro del mensaje actual como archivo de un
analista independiente, no como turnos `assistant` propios. Workspace, `M_pre`, reporte y contenido
histórico se conservan. Si revisa como el chat fresco, la firma apunta a trayectoria propia visible;
si falla como el nativo, apunta a carga/semántica del contexto, no autoría.

**Tercera ablación prospectiva:** `neutral_length_matched_archive` reemplaza el transcript por un
archivo administrativo/calibración sin información sobre la ley, con exactamente la misma cantidad
de caracteres que el archivo atribuido a otro. Si revisa, el ingrediente es la evidencia/conclusión
vieja relevante; si falla, longitud/distracción bastan. Se guardan tokens de prompt por llamada para
auditar el igualado real (caracteres iguales no garantizan tokens iguales).

**Cuarta ablación prospectiva, agregada después de observar 1/2 fallas con el archivo neutral:**
el contraste anterior igualó caracteres, pero no estructura ni posiciones, y además mostró
variabilidad entre repeticiones. Se congela antes de correr una familia más estricta,
`matched_relevance_archive`, con 24 ranuras y 45.554 caracteres exactos en todos los brazos. Cada
mensaje omitido se reemplaza carácter por carácter por prosa administrativa en la misma posición:

| Perfil | Contenido científico preservado | Interpretación buscada |
|---|---|---|
| `neutral` | ninguno | carga/longitud pura |
| `early` | turnos 1–6 | datos y exploración antes del compromiso final |
| `commitment` | turnos 9–12 | consolidación, uso y codificación del modelo compartido |
| `full` | turnos 1–12 | historial relevante completo |

Todo se atribuye al mismo analista independiente; mundo, workspace replayado, `M_pre`, reporte,
posición del reporte y longitud en caracteres quedan fijos. Se usan dos continuaciones por perfil
en `clean64`, siempre con el gemelo `RETAIN`. Las corridas ya hechas del archivo completo no se
reutilizan porque su encabezado no era byte-idéntico al de esta nueva familia. Predicción previa:
si domina solo la carga, los cuatro perfiles fallarán a tasas parecidas; si domina la conclusión
previa, `commitment/full` fallarán más que `neutral/early`. Con n=2 esto sigue siendo localización
exploratoria, no estimación de una tasa. Cualquier patrón no monotónico obliga a mirar las trazas y
replicar, no a escoger retrospectivamente el contraste más favorable.

## Réplica prospectiva en donantes independientes

Después de completar la familia anterior, la señal todavía depende de un único donante
seleccionado. Antes de generar candidatos nuevos se fija este procedimiento:

1. semillas `96300–96307`, quemadas, en orden;
2. cada agente construye libremente un prefijo con `checkpoint=eligible`, sin ejecutar todavía
   ninguna continuación;
3. elegibilidad puramente pretratamiento: artefacto válido con fenotipo de transferencia
   compartida, `R_pre >= 0.15` en `REVISE` y `R_pre >= 0.60` en `RETAIN`;
4. se aceptan todos los candidatos que pasen, sin mirar resultados posteriores, hasta obtener
   tres donantes o agotar las ocho semillas;
5. en cada aceptado se corre una continuación por `native` y una por
   `fresh_compacted_no_hint`, siempre `clean64 × {REVISE, RETAIN}`.

Predicción: si el efecto es una propiedad replicable del historial científicamente relevante,
`native` capturará menos mejora que `fresh` en `REVISE`, sin una pérdida paralela en `RETAIN`.
La unidad sigue siendo el donante; dos ramas del mismo donante no son dos observaciones
independientes. Si no aparecen al menos dos donantes elegibles, el resultado principal queda
explícitamente restringido al caso 94101 y el siguiente trabajo es mejorar cómo se forma la
creencia, no multiplicar forks de ese único caso.
