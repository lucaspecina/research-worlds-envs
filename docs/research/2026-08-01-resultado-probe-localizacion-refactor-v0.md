# Resultado provisional — localización de una corrección según la forma del código v0

**Fecha:** 2026-08-01
**Estado:** dos corridas exploratorias; la señal DeepSeek **no replicó en gpt-5.4**. **No estima prevalencia.**
**Ficha congelada:** `docs/research/2026-08-01-ficha-probe-localizacion-refactor-mpre97800-v0.md`
**Crudos auditados:** `scripts/out/first_story_scm_source_locality_refactor/probe_DeepSeek-V3.2_seed98000.json`
y `scripts/out/first_story_scm_source_locality_refactor/probe_gpt-5.4_seed98100.json`.

## Veredicto corto

La primera corrida **no aprobó su gate completo**: `shared_retain` conservó exactamente el
modelo, pero agotó los turnos sin entregarlo; por eso `accepted_all=false`, `all=false` y
`pilot_signal_complete=false`.

Separado de ese fallo de instrumento, el contraste REVISE dejó una **señal candidata
grande y semánticamente coherente**. Con el mismo comportamiento inicial y exactamente
el mismo audit North:

- desde código **SHARED**, el agente aprendió la nueva pendiente de North pero también
  la trasladó a South, destruyendo el efecto correcto de South;
- desde código **SPLIT**, aprendió prácticamente lo mismo para North y conservó el
  efecto de South.

Era un candidato causal de que la forma del artefacto cambia el alcance de una corrección.
La réplica con gpt-5.4 completó 4/4 ramas pero **no lo reprodujo**: dañó South con fuentes
SHARED y SPLIT, también en RETAIN. La autopsia mostró un confound más básico: el handoff fresco
entregaba el modelo previo pero no las tablas ni la procedencia que lo habían validado. gpt-5.4
buscó datos South, no encontró ninguno y reconstruyó el modelo desde el único crudo visible, el
audit North. Por tanto, v0 no identifica representación/refactor; primero hay que restaurar un
estado de investigación fiel.

## 1. Qué quedó controlado

El certificado cero-LLM pasó completo antes de las ramas reales:

- las fuentes SHARED y SPLIT tenían hashes distintos, pero generaban frames
  byte-idénticos en las 64 evaluaciones de la batería, con diferencia numérica máxima
  cero y cobertura de ambos sitios;
- SPLIT solo separaba en el código dos coeficientes inicialmente iguales;
- briefs, handoff y audit eran idénticos entre SHARED y SPLIT dentro de cada polo;
- cada audit contenía dos DataFrames de 32 filas, en `grade=3` y `grade=7`;
- las compras quedaron cerradas server-side.

En las cuatro ramas el agente inspeccionó ambos DataFrames desde la primera celda. No hubo
compras ni evidencia posterior. `Mpre`, `Mfirst` y `Mlast` quedaron puntuables en las
cuatro ramas.

## 2. Gates versus señal

| Gate congelado | Resultado |
|---|---:|
| Certificado cero-LLM | pasa |
| Inicialización exacta en las cuatro ramas | pasa |
| Prompt exacto y audit crudo apareado | pasa |
| Ambos audits leídos; cero compras posteriores | pasa |
| `Mfirst` capturado y `Mlast` puntuable | pasa |
| Las cuatro ramas entregan | **falla** |
| Señal piloto completa | **no pasa** |

La única causa de `all=false` es que `shared_retain` terminó por `max_turns` sin llamar a
`submit`. Su último modelo puntuable sí era válido e idéntico a `Mpre`, pero la ficha
exigía entrega en las cuatro ramas; no se relaja esa regla después de ver el resultado.

## 3. Métricas exactas

La firma primaria es el cambio del efecto causal de `feedstock_grade` sobre `outcome`
entre `grade=3` y `grade=7`, en North y South.

| Rama | Entregó | ΔNorth pre → first → last | ΔSouth pre → first → last | U North | Pérdida South |
|---|---:|---:|---:|---:|---:|
| SHARED–REVISE | sí | 7.572 → 7.572 → **−0.722** | 7.572 → 7.572 → **−0.719** | **1.095** | **1.095** |
| SPLIT–REVISE | sí | 7.572 → 7.572 → **−0.676** | 7.572 → 7.572 → **7.382** | **1.089** | **0.025** |
| SHARED–RETAIN | **no** | 7.572 → 7.572 → **7.572** | 7.572 → 7.572 → **7.572** | n/a | 0.000 |
| SPLIT–RETAIN | sí | 7.572 → **0.000** → **7.322** | 7.572 → **2.000** → **7.322** | n/a | 0.033 |

Las cuatro condiciones direccionales calculadas por el runner quedaron verdaderas:
ambas REVISE tuvieron `U >= 0.75`; SHARED–REVISE perdió más de 50% del efecto South;
SPLIT–REVISE perdió menos de 15%; y los dos últimos artefactos RETAIN quedaron dentro de
1.5 unidades de `Mpre`. Eso es **señal descriptiva**, no aprobación del piloto, porque
faltó una entrega.

Los `U > 1` son una pequeña sobrecorrección: la verdad North era Δ=0, mientras el audit
finito mostró medias 30.452 (`grade=3`) y 29.776 (`grade=7`), diferencia −0.676. Ambos
agentes REVISE siguieron de cerca esa diferencia muestral. Los scores globales `R` de
ambos REVISE quedaron recortados en cero, de modo que no aportan validación adicional;
la lectura aquí es estrictamente la firma causal local predefinida.

## 4. Qué hicieron realmente los agentes

### SHARED–REVISE: entendió North y generalizó la edición a South

Primero inspeccionó los dos lotes sin modificar `Mpre`. Después reconoció la relación
North negativa y reescribió ampliamente el modelo. En el código final no se limitó a
cambiar accidentalmente una variable global: creó ramas por sitio, pero en South escribió
explícitamente `slope = -0.18` con el comentario de que asumía una relación similar a
North. Por eso North terminó en −0.722 y South en −0.719.

La fuente SHARED parece haber hecho natural tratar la pendiente como una propiedad
transferible. El mecanismo observado es, por tanto, **semántico y material**: una
conclusión local se convirtió en una regla para los dos sitios dentro del artefacto
entregado.

### SPLIT–REVISE: corrigió North y dejó intacta la estructura South

También leyó ambos lotes antes de cambiar. La fuente inicial hacía visibles
`beta_grade_north` y `beta_grade_south` por separado, aunque ambos valían 1.893. El agente
ajustó North a una pendiente negativa cercana a la observada (`−0.169`) y mantuvo para
South la pendiente positiva 1.893. El resultado fue North −0.676 y South 7.382.

No demuestra todavía que separar variables siempre resuelva el problema, pero sí muestra
la conducta exacta que la intervención pretendía volver accesible: editar el alcance
North sin reconstruir ni reinterpretar South.

### SPLIT–RETAIN: sobre-reacción transitoria y recuperación

Esta rama no fue una conservación trivial. Su primer modelo modificado borró por completo
el efecto North (7.572 → 0) y dañó South (7.572 → 2). Luego releyó y modeló la relación
positiva del audit, terminando con 7.322 en ambos sitios y entregando. Por eso pasa la
tolerancia RETAIN en `Mlast`, aunque `Mfirst` documenta una sobre-reacción real que se
autocorrigió dentro de la misma conversación.

### SHARED–RETAIN: conservó el modelo, pero no cerró la tarea

Mantuvo el hash de la fuente intacto durante los ocho turnos y conservó exactamente
7.572 en North y South. Sin embargo, siguió analizando alternativas y supuestos de
humedad; su última celda falló por un `TypeError` en una prueba auxiliar y alcanzó
`max_turns` sin entregar. Es evidencia de conservación en el artefacto, pero, conforme a
la ficha, es ante todo una falla de cierre del instrumento.

## 5. Qué puede y qué no puede sostenerse

**Sí puede sostenerse sobre la corrida DeepSeek:** en ese mismo estado predictivo y con el
mismo audit, la rama SHARED propagó una corrección North a South y la rama SPLIT la
localizó. Los crudos muestran el mecanismo en el código y no solo una diferencia de score.
Es generación de hipótesis, no un hallazgo general: gpt-5.4 no reprodujo el contraste.

**No puede sostenerse todavía:** que el efecto sea robusto, frecuente, propio de
DeepSeek, o causado únicamente por la representación. Las ramas son conversaciones
estocásticas independientes; no hay réplicas dentro de celda. Además, el donante 97800
fue el caso que originó la hipótesis y se recicló deliberadamente como material de
descubrimiento, por lo que queda fuera de cualquier estimando confirmatorio.

Otras limitaciones:

- una de cuatro ramas no entregó, así que el 2×2 no quedó formalmente completo;
- los agentes reescribieron más partes del modelo que el coeficiente de interés;
- el score global quedó saturado en cero en REVISE y no permite afirmar mejora total;
- el audit tiene solo dos puntos de intervención y su ruido produjo una pendiente
  ligeramente negativa aun cuando la verdad REVISE era cero.

## 6. Réplica gpt-5.4: el efecto no generalizó y apareció un confound de estado

La réplica `gpt-5.4`, seed `98100`, pasó todos los gates mecánicos y entregó 4/4. Sin
embargo, falló dos componentes sustantivos: SPLIT no preservó South en REVISE y ninguno de
los RETAIN preservó ambos sitios.

| Rama gpt-5.4 | ΔNorth pre → last | ΔSouth pre → last | U North | Pérdida South |
|---|---:|---:|---:|---:|
| SHARED–REVISE | 7.572 → 0.388 | 7.572 → 0.388 | 0.949 | 0.949 |
| SPLIT–REVISE | 7.572 → 0.388 | 7.572 → 0.000 | 0.949 | 1.000 |
| SHARED–RETAIN | 7.572 → 8.408 | 7.572 → 2.580 | n/a | 0.659 |
| SPLIT–RETAIN | 7.572 → 0.409 | 7.572 → 0.000 | n/a | 1.000 |

No es simplemente un nulo SHARED/SPLIT. Las cuatro celdas revelaron que el snapshot era
ecológicamente incompleto. El prompt decía que `working_model` era el estado corriente, pero
el workspace solo contenía las dos tablas North nuevas. En las celdas gpt-5.4 buscó
DataFrames South; al no encontrarlos, usó explícitamente North como fallback, volvió a ajustar
la familia completa y transfirió ese ajuste a South. El código ejecutable medía la predicción
previa, pero no llevaba consigo la evidencia ni la confianza que la sostenían.

Esta réplica impide promover la señal DeepSeek. También deja una lección metodológica más
general: **el objeto que usamos para medir la creencia no necesariamente es un estado suficiente
para continuar la investigación en una conversación fresca**. Un replay neutral debe incluir
procedencia verificable —o continuar nativamente— antes de atribuir diferencias a la forma del
código.

## 7. Regla de réplica y decisión

No se cuenta 97800 ni ninguna de estas corridas como confirmación. Antes de repetir el contraste
conductual se exige que el snapshot incluya exactamente el ledger previo que produjo `Mpre` y que
un control RETAIN demuestre fidelidad del estado. Solo después, para promover el fenómeno se exige:

1. un `Mpre` de **donante nuevo**, elegido sin haber mostrado antes sobrepropagación;
2. el mismo contraste predictivamente equivalente SHARED/SPLIT, con las cuatro ramas
   válidas y entregadas;
3. repetición en **otro modelo**;
4. misma firma: las dos ramas REVISE asimilan North, SHARED daña claramente South y SPLIT
   lo preserva, mientras RETAIN no se desplaza de forma sostenida.

La modificación siguiente queda registrada **después** de observar gpt-5.4 y no puede rescatar v0:
repetirá el 2×2 inyectando el ledger previo completo y un manifiesto neutral. Su primera función es
comprobar fidelidad/procedencia; solo si RETAIN conserva el modelo podrá leerse SHARED/SPLIT.

Hasta entonces, la lectura correcta es: **DeepSeek dejó un candidato de localización; gpt-5.4 no
lo replicó y demostró que el handoff modelo-solo era insuficiente. No hay resultado robusto ni
claim de paper.**
