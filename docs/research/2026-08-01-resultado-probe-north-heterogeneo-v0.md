# Resultado — North heterogéneo: la media se revisa, la estructura se aplana

> **Alcance:** cuatro forks vividos: DeepSeek-V3.2 (`97400–97401`) y gpt-5.4
> (`97500–97501`). Cada fork replayó exactamente la primera campaña North en tres polos:
> REVISE, MIXED 75/25 y RETAIN. Es evidencia exploratoria entre dos agentes reales,
> no una tasa de prevalencia. Cada seed sigue siendo un solo donante (`n=1` para una
> autopsia individual; `n=2` donantes por modelo en el agregado).

> **Corrección de auditoría:** los valores de DeepSeek `97400` que figuraban en una
> versión anterior provenían de otro artefacto del dossier. Abajo se usan exclusivamente
> el raw nombrado `probe_DeepSeek-V3.2_seed97400_mixed.json` y su análisis reproducible.

> **Incidente de procedencia (`97500`):** a las 21:34 se relanzó por error el mismo seed y
> se sobreescribió su raw original, que aún no estaba versionado. El relanzamiento quedó
> preservado como `probe_gpt-5.4_seed97500_rerun1_mixed.json`. Los números originales de
> `97500` que siguen en este informe no pueden regenerarse desde aquel raw perdido; sobreviven
> como resultados derivados en el informe y en `reflection_handoff_gpt-5.4_seed97500.json`.
> Por eso la réplica emparejada sobre el donante intacto `97501`, abajo, es la evidencia
> primaria para interpretar el mecanismo.

## Resultado corto

La manipulación pasó todas las compuertas. South, el modelo previo, la transición, la
celda de experimentos, las solicitudes y el presupuesto fueron iguales dentro de cada
fork. Los polos eran indistinguibles en todo lo no diagnóstico. Solo cambió qué mecanismo
generaba `outcome` en las unidades North.

Ambos modelos revisaron la **media causal** en la dirección y magnitud aproximadamente
correctas:

| Modelo | Seed | Polo | Verdad: efecto `G` North | Efecto previo | Efecto final | Fracción de revisión media `U` |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek-V3.2 | 97400 | REVISE | 0.00 | 8.12 | 0.01 | 1.00 |
| DeepSeek-V3.2 | 97400 | MIXED | 2.00 | 8.12 | 2.10 | 0.74 (objetivo 0.75) |
| DeepSeek-V3.2 | 97400 | RETAIN | 8.00 | 8.12 | 7.45 | 0.07 (objetivo 0) |
| DeepSeek-V3.2 | 97401 | REVISE | 0.00 | 8.15 | 0.00 | 1.00 |
| DeepSeek-V3.2 | 97401 | MIXED | 2.03 | 8.15 | 1.46 | 0.82 (objetivo 0.75) |
| DeepSeek-V3.2 | 97401 | RETAIN | 8.00 | 8.15 | 7.94 | 0.01 (objetivo 0) |
| gpt-5.4 | 97500 | REVISE | 0.00 | 8.11 | 0.12 | 0.98 |
| gpt-5.4 | 97500 | MIXED | 2.03 | 8.11 | 2.35 | 0.71 (objetivo 0.75) |
| gpt-5.4 | 97500 | RETAIN | 8.00 | 8.11 | 8.11 | −0.01 (objetivo 0) |
| gpt-5.4 | 97501 | REVISE | 0.00 | 8.05 | 0.05 | 0.99 |
| gpt-5.4 | 97501 | MIXED | 2.03 | 8.05 | 1.80 | 0.78 (objetivo 0.75) |
| gpt-5.4 | 97501 | RETAIN | 8.00 | 8.05 | 7.96 | 0.01 (objetivo 0) |

En `97400`, REVISE corrigió prácticamente toda la media y MIXED llegó al objetivo intermedio;
el desvío mayor quedó en RETAIN (`7.45` frente a `8.00`, menos de 0.07 del recorrido total).
No se registra un vicio robusto de no-pivoteo en la media.

## La falla que sí se repitió

En MIXED, 75% de las unidades seguían `H→Y` y 25% conservaban `G→Y`. La predicción correcta
no era una única Normal ruidosa: en intervenciones off-manifold había dos componentes y una
asimetría que cambiaba de signo entre `G=3` y `G=7`. La firma server-side orientada era
`A3≈0.324`; una Normal con la misma media y varianza da `A3≈0`.

| Modelo | Seed | Media final | Varianza `G=3` final / verdad | Captura de la firma de mezcla |
|---|---:|---:|---:|---:|
| DeepSeek-V3.2 | 97400 | 2.10 | 22.85 / 6.98 | ≈0% |
| DeepSeek-V3.2 | 97401 | 1.46 | 16.13 / ≈7.00 | ≈0% |
| gpt-5.4 | 97500 | 2.35 | 25.14 / ≈7.00 | ≈0% |
| gpt-5.4 | 97501 | 1.80 | 5.18 / ≈7.00 | ≈0% |

Los cuatro hicieron lo mismo: **promediaron el conflicto y lo absorbieron como ruido simétrico**.
Vieron que North era distinto y movieron correctamente el efecto medio, pero entregaron una sola
familia gaussiana: tres sobredispersaron y uno subdispersó. Ninguno representó que coexistían dos
mecanismos. South quedó causalmente preservado en los forks MIXED de ambos modelos.

La separación media/forma es especialmente limpia en la autopsia `97400`: en `G=3`, la verdad
tuvo media `28.99`, varianza `6.97` y skew `−0.326`; la entrega dio `28.96`, `22.28` y `0.009`.
En `G=7`, verdad y entrega tuvieron medias `30.99/31.02`, pero skews `0.331/0.018`. Es decir,
acertó el desplazamiento medio y falló tanto la forma orientada como la dispersión. Además, una
Normal con los momentos correctos quedó mucho más cerca de la verdad que la entrega: distancia
de energía local `0.090/0.094` contra `0.567/0.574` en `G=3/G=7`.
Estas cuatro distancias son `scipy.stats.energy_distance` sobre 30 000 muestras por régimen;
se reportan como diagnóstico local y no en la escala del `R` global.

El certificado confirma que el instrumento sí puede cobrar esta diferencia: la distancia de
energía media del oráculo MIXED es `0.0032` y la Normal con momentos iguales obtiene `0.0223`
(`6.95×` peor); en el score de producción reciben `R=1.00` y `R=0.762`, respectivamente.
Por lo tanto, el cero de forma del agente no es invisibilidad del scorer.

Esto es una falla predictiva real y graduada, medida en lo entregado y sin juez-LLM. Pero **no es
todavía una falla causalmente identificada de revisión de creencias o apego a South**. La lectura
más austera es una debilidad de crítica/generación de modelos: el agente detectó medias, varianzas
e interacciones, pero restringió espontáneamente su entrega a una gaussiana. Los controles frescos
de abajo refuerzan esa explicación rival.

## Control causal: reflexión extra y analista fresco

Se usó el donor gpt-5.4 `97500`, cuyo North completo estaba contenido en la celda final. Se
reconstruyeron byte a byte sus 19 campañas y el presupuesto restante (`1540`) en dos condiciones:

- **native_reflection:** misma conversación y workspace; la entrega de la celda se difirió para
  que el LLM leyera el stdout y tuviera un turno real de reflexión;
- **fresh_data_only:** conversación y kernel nuevos, solo los 19 DataFrames con nombres neutrales
  y un manifiesto `site/config/n`; sin `Mpre`, código, conclusiones ni transcript.

Los hashes de evidencia y presupuestos coincidieron y ambas entregas fueron válidas.

**Corrección de auditoría:** una versión anterior de este documento decía `21` campañas y
presupuesto `30`. El JSON persistido y el prompt ejecutado muestran `19/1540`; el error era solo de
redacción. No altera el contraste porque los brazos reusaron el mismo ledger y presupuesto exactos.

| Condición | Efecto medio final (verdad ≈2.03) | Varianza `G=3` | Captura de mezcla |
|---|---:|---:|---:|
| Nativa + reflexión | 2.35 | 5.59 | ≈0% |
| Fresca, datos solamente | 2.33 | 30.84 | ≈0% |

La continuación nativa intentó una regresión con ruido heteroscedástico; la fresca reconstruyó
todo desde los crudos. Las dos siguieron entregando una familia unimodal. **Este control retira la
interpretación de confirmation bias o compromiso para este resultado.** El fenómeno que sobrevive
es más básico: búsqueda/model criticism insuficiente ante conflicto estructurado. El próximo control
pregunta si un recordatorio científico genérico de inspeccionar residuos y forma distribucional lo
corrige; no dice que haya mezcla ni cuál es la respuesta.

Ese control genérico también falló: el analista inspeccionó residuos y comparó una Normal con una
familia de colas pesadas, pero mantuvo `A3≈0`, con efecto medio `2.32` y varianza `27.52`. El cuello
no es simplemente “se olvidó de mirar residuos”: aun al hacerlo, su espacio espontáneo de hipótesis
siguió siendo unimodal. Queda separar (a) no proponer una estructura latente de (b) no poder
implementarla. El siguiente control declara como documentación de dominio que son legales modos
latentes con mezcla estable y peso desconocido, sin revelar el peso ni las leyes verdaderas.

Ese control exigió dos enmiendas auditadas. La primera corrida no expandió el JSON del manifiesto y
perdió incluso South, por lo que quedó inválida. Luego, un bug de argumentos hizo que el archivo
`flat_family_pair` fuera plano solo en el brazo declarado, no en `data-only`; ambos dieron `A3≈0`,
pero no se interpreta como par igualado. El brazo con familia declarada recuperó media North `1.95`
y mantuvo `A3≈0`. Un control positivo final aclaró además que los modos podían tener coeficientes
distintos y que una mezcla debía ser sobre leyes completas, sin revelar sitio, peso ni coeficientes.
El agente nombró y ensayó mezclas, pero volvió a entregar una sola ley simétrica: media `1.95`,
`A3≈0`. Por tanto, en este donor no basta hacer disponible la hipótesis: falla su traducción a la
predicción ejecutable. Con un solo agente/control no se etiqueta esto como incapacidad general.

El baseline plano corregido necesitó un rerun porque la primera entrega referenciaba un objeto del
notebook no incluido en el código. El rerun válido obtuvo media North `1.67`, South `8.13` y
`A3≈0`; por tanto, la conclusión de forma sí sobrevive con la interfaz igualada. Un ajuste mecánico
en las celdas extremas favorece dos componentes sobre una Gaussiana por `ΔBIC≈30` aun con 30 filas:
la señal existe. La autopsia muestra el cuello concreto: el agente llegó a escribir “two-mode
outcome residual”, pero ajustó offsets de ruido constantes entre controles; al poolar celdas donde
las leyes se separan en sentidos opuestos, canceló la estructura y eligió un componente.

### Réplica emparejada sobre el donante intacto `97501`

Para retirar el problema de procedencia de `97500`, se reconstruyó `97501` en conversaciones y
kernels nuevos. En los tres primeros brazos coincidieron exactamente los 19 DataFrames, su hash
agregado (`2ef5…70d9`) y el presupuesto (`480`). El cuarto usó esos mismos datos y presupuesto
en un raw separado. Todas las compuertas mecánicas pasaron.

| Condición fresca | Efecto North (verdad ≈2.03) | `A3` (verdad ≈0.324) | Varianza `G=3` (verdad ≈7) | Efecto South (verdad 8) |
|---|---:|---:|---:|---:|
| Solo datos | 2.1045 | 0.000 | 30.25 | 8.025 |
| Chequeo científico genérico | 1.8505 | 0.000 | 20.44 | 8.051 |
| Se declara que una mezcla latente es legal | 1.8749 | 0.000 | 15.13 | 7.493 |
| Se declaran mezclas de **leyes de respuesta** legales | −0.3397 | −0.156 | 76.03 | 6.165 |

La declaración genérica de familia no alcanzó: el agente implementó una mezcla constante de
**residuos**, que puede cambiar colas pero no hacer que el efecto causal dependa del componente;
por eso `A3` siguió en cero. Cuando la documentación aclaró que cada modo podía tener una ley de
respuesta distinta, sí construyó una mezcla de tres regresiones. La clase pasó a ser representable,
pero la estimó y seleccionó mal: obtuvo la asimetría con signo incorrecto, perdió la media North,
sobredispersó (`76.03/50.99` en `G=3/G=7`) y dañó South.

El diagnóstico preciso ya no es “no puede implementar mezclas”. Es: **sin ayuda aplana la
heterogeneidad; con la clase correcta disponible, no recupera establemente sus componentes**.
Todavía no sabemos cuánto de lo segundo es una falla del agente y cuánto es dificultad estadística
del conjunto finito. Antes de hacer un claim fuerte, un ajustador cero-LLM debe demostrar que la
familia correcta es recuperable desde exactamente esos mismos 19 DataFrames.

### Control cero-LLM de recuperabilidad sobre `97501`

El ajustador recibió solo las filas North de campañas que fijaban ambos controles; no vio la
verdad, el peso 75/25 ni los coeficientes. Comparó una Gaussiana afín, una mezcla de residuos con
pendientes compartidas y una mezcla de dos leyes afines, usando arranques no privilegiados, BIC,
validación cruzada y, cuando había celdas repetidas, holdout de campañas completas. En `97501`
fueron 280 filas y 24 arranques. Al replicar se descubrió una limitación computacional: `97400`
tiene 13 celdas y enumerarlas como arranques crecía exponencialmente. La enmienda mecánica puntúa
todas las alineaciones con likelihood inicial y optimiza como máximo las mejores 32, más las 16
aleatorias; no cambia candidatas, objetivo, datos ni umbrales, y deja idénticos los donantes de
cuatro y seis celdas.

| Candidata | BIC ↓ | log-likelihood CV/fila ↑ | holdout posterior/fila ↑ | `A3` | error W1 local ↓ |
|---|---:|---:|---:|---:|---:|
| Una ley gaussiana | 1764.2 | −3.137 | −3.026 | 0.000 | 0.833 |
| Mezcla de residuos | 1628.3 | −2.864 | −2.687 | 0.000 | 0.684 |
| Dos leyes afines | **1474.8** | **−2.598** | **−2.494** | **0.300** | **0.126** |
| Agente final | — | — | — | 0.001 | 0.180 |

La tercera candidata ganó en cada fold y recuperó, desde los datos, leyes casi verdaderas:
`20.13 + 1.97G + 0.07H` con peso `0.262`, y `40.21 − 0.00G − 1.98H` con peso `0.738`.
Capturó 93% de `A3` y el efecto medio `2.12` (verdad empírica `2.03`). Entrenada solo en las
primeras 240 filas, predijo las 40 posteriores mejor que las alternativas y capturó 98% de `A3`.
Por tanto, **en este donante la forma no estaba oculta por falta de información**: un procedimiento
estadístico honesto la recupera y el agente la aplana. Cautela: al retirar 20% de las filas, cuatro
de cinco fits conservaron al menos media señal de forma pero uno cayó a 13%; la existencia de dos
leyes es robusta, su geometría precisa es moderadamente sensible al tamaño muestral. Esto valida
este donante y esta familia, no una capacidad general.

La réplica cero-LLM en los dos donantes DeepSeek conservó el resultado de selección:

| Donante | Filas / celdas | `ΔBIC` vs mezcla residual ↑ | ventaja CV/fila ↑ | holdout de campañas | `A3` fit (% verdad) | `A3` agente |
|---|---:|---:|---:|---|---:|---:|
| GPT `97501` | 280 / 4 | 153.5 | 0.266 | gana dos leyes | 0.300 (93%) | 0.001 |
| DeepSeek `97400` | 160 / 13 | 71.4 | 0.220 | gana dos leyes | 0.405 (125%) | 0.000 |
| DeepSeek `97401` | 190 / 6 | 32.7 | 0.082 | no disponible | 0.676 (209%) | 0.000 |

Dos leyes ganó BIC, CV agregado **y cada fold** en los tres donantes. En `97400` también ganó el
holdout de campañas, aunque por margen chico y con asimetría sobreestimada; `97401` no tenía una
misma celda repetida en otra campaña, por lo que no se inventó un holdout cronológico comparable.
Los dos fits DeepSeek recuperaron pendientes cercanas a las leyes verdaderas, pero exageraron
`A3`, especialmente `97401`: la evidencia identifica la **existencia y orientación** de leyes
distintas mucho más robustamente que el peso y la asimetría exactos. Los agentes, en cambio,
dejaron `A3≈0` en ambos. El claim defendible sube de “recuperable en un donante” a “la estructura
es estadísticamente preferida en tres donantes”; todavía no a “sus parámetros se recuperan con
precisión uniforme”.

## Dos cautelas de medición

1. `M_first` en este runner puede nacer dentro de la misma celda que compra los experimentos.
   El código puede usar las filas, pero el LLM recién ve el `stdout` en el turno siguiente.
   Por eso no se interpreta automáticamente `M_first` sin cambio como “vio y no asimiló”.
2. Los `R` globales están mal calibrados para comparar calidad fina en estos casos y a menudo
   clippean en cero. Los claims anteriores usan firmas locales predefinidas y distribuciones
   ejecutables; el score global queda descriptivo.

## Revisión un nivel arriba

- **Pregunta:** sigue siendo interesante. El polo intermedio revela un fenómeno que los extremos
  escondían: acertar el promedio puede coexistir con una creencia estructuralmente equivocada.
- **Constructo:** hay una falla predictiva replicada de representar conflicto/heterogeneidad; el
  control fresco descarta por ahora atribuirla a compromiso con South.
- **Decisión:** **MANTENER el fenómeno, RETIRAR el claim de anclaje.** No escalar todavía a una tasa.
- **Decisión:** cerrar la escalera de hints. Precisar “mezcla de leyes” activó la representación,
  pero produjo componentes erróneos y degradó North y South. Seguir dando pistas convertiría el
  probe en una receta de programación.
- **Validez finita replicada en tres donantes:** el ajustador cero-LLM prefirió dos leyes por
  BIC, CV agregado y todos los folds en `97501`, `97400` y `97401`; ganó además los holdouts
  honestos disponibles en los dos primeros. La existencia/orientación de dos leyes era
  recuperable, aunque el peso y la asimetría exactos fueron sensibles entre muestras.
- **Próximo contraste de mayor valor:** volver a revisión bilateral y comparar contradicción limpia
  con conflicto genuino posterior a una creencia propia; no seguir optimizando este mismo ejemplo.

## Reproducción cero-LLM

```powershell
python scripts/certify_first_story_scm_transfer_mixed.py
python scripts/analyze_first_story_scm_transfer_mixed.py scripts/out/first_story_scm_transfer_fork/probe_DeepSeek-V3.2_seed97400_mixed.json --n-samples 30000 --seed 1300001 --out scripts/out/first_story_scm_transfer_fork/analysis_DeepSeek-V3.2_seed97400_mixed.json
```

El primer comando debe terminar con `"all": true`. El segundo reconstruye las medias,
varianzas, `A3`, captura de forma y preservación de South citadas arriba sin volver a llamar
al agente.

## Artefactos

- `cases/first_story_scm_transfer_mixed_v0/`
- `scripts/certify_first_story_scm_transfer_mixed.py`
- `scripts/analyze_first_story_scm_transfer_mixed.py`
- `scripts/analyze_scm_mixed_finite_identifiability.py`
- `scripts/probe_scm_mixed_reflection_handoff.py`
- `scripts/out/first_story_scm_transfer_fork/probe_DeepSeek-V3.2_seed97400_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/probe_DeepSeek-V3.2_seed97401_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/probe_gpt-5.4_seed97500_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/probe_gpt-5.4_seed97501_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/analysis_DeepSeek-V3.2_seed97400_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/analysis_DeepSeek-V3.2_seed97401_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/analysis_gpt-5.4_seed97500_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/analysis_gpt-5.4_seed97501_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/reflection_handoff_gpt-5.4_seed97500.json`
- `scripts/out/first_story_scm_transfer_fork/generic_check_gpt-5.4_seed97500.json`
- `scripts/out/first_story_scm_transfer_fork/flat_family_pair_gpt-5.4_seed97500.json`
- `scripts/out/first_story_scm_transfer_fork/declared_mixture_laws_gpt-5.4_seed97500.json`
- `scripts/out/first_story_scm_transfer_fork/flat_data_only_corrected_gpt-5.4_seed97500_r1.json`
- `scripts/out/first_story_scm_transfer_fork/probe_gpt-5.4_seed97500_rerun1_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/analysis_gpt-5.4_seed97500_rerun1_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/fresh_controls_gpt-5.4_seed97501.json`
- `scripts/out/first_story_scm_transfer_fork/declared_mixture_laws_gpt-5.4_seed97501.json`
- `scripts/out/first_story_scm_transfer_fork/finite_identifiability_gpt-5.4_seed97501_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/finite_identifiability_DeepSeek-V3.2_seed97400_mixed.json`
- `scripts/out/first_story_scm_transfer_fork/finite_identifiability_DeepSeek-V3.2_seed97401_mixed.json`
