# Resultado — conflicto firmado: v0 inválido; v1 válido y nulo en dos modelos frontier

> **Alcance:** una sonda exploratoria. Primero se auditó un v0 inválido con
> `DeepSeek-V3.2` (`97801`). Después se ejecutó la corrección v1 válida con el mismo paquete
> de informes (`package_seed=1`) en `DeepSeek-V3.2` (`97810`) y `gpt-5.4` (`97910`). No estima
> prevalencia.

## Veredicto corto

La implementación corregida v1 dio un **nulo en las dos corridas frontier válidas**. DeepSeek
actualizó casi igual ante el informe limpio y el conflictivo (`B=0.01255`; `0.01542` si ambas
actualizaciones se normalizan contra la referencia finita). GPT-5.4 terminó sobre la referencia
finita en las cuatro ramas, con contrastes indistinguibles de cero. En este formato, presentar
conflicto entre estudios como un reporte rutinario aislado **no elicita una falla de revisión**.

La señal grande anterior (`B=0.610`) pertenece solo al v0 inválido: fallaron sus compuertas,
una rama compró cuatro experimentos después del reporte y la vara confundía la verdad oculta
con lo inferible de una muestra finita. Se conserva abajo como autopsia histórica, no como
evidencia positiva.

## Resultado válido v1

### Compuertas técnicas

Ambos raws tienen `all=true`. En los dos fueron exactamente `true` las 16 compuertas guardadas:

- `local_certificate`, `transferable_model_formed`, `south_prefix_evidence_present` y
  `all_prefix_evidence_south`;
- `replay_exact_all`, `prefix_ledger_exact_all`, `handoff_prompt_exact_all`,
  `report_event_once_all`, `report_injected_free_all` y `report_hash_matches_audit_all`;
- `zero_post_report_experiments_all`, `no_post_report_non_report_evidence_all` y
  `collection_window_enforced_all`;
- `accepted_all`, `last_artifact_scoreable_all`, `first_artifact_scoreable_all` y
  `M_first_captured_on_first_post_report_turn_all`.

Los cuatro hashes de informes también coinciden entre modelos: ambos vieron byte por byte el
mismo paquete de evidencia. Los LLR totales fueron `31.98224`, `31.88653`, `-31.79865` y
`-31.94318` para REVISE limpio, REVISE conflictivo, RETAIN limpio y RETAIN conflictivo,
respectivamente.

### Comparación contra la referencia finita

La vara primaria de v1 es la pendiente pooled/MLE de las filas realmente servidas,
`delta_ref = 4 - LLR/12`; no es la verdad oculta ni incorpora una prior privada del agente.

| Modelo | Rama | `delta_ref` | `delta_final` | Error absoluto |
|---|---|---:|---:|---:|
| DeepSeek-V3.2 | REVISE limpio | 1.33481 | 1.26685 | 0.06797 |
| DeepSeek-V3.2 | REVISE conflictivo | 1.34279 | 1.32160 | 0.02119 |
| DeepSeek-V3.2 | RETAIN limpio | 6.64989 | 6.21520 | 0.43469 |
| DeepSeek-V3.2 | RETAIN conflictivo | 6.66193 | 6.66200 | 0.00007 |
| gpt-5.4 | REVISE limpio | 1.33481 | 1.33481 | `<1.1e-14` |
| gpt-5.4 | REVISE conflictivo | 1.34279 | 1.34279 | `<3.6e-15` |
| gpt-5.4 | RETAIN limpio | 6.64989 | 6.64989 | `<7.2e-15` |
| gpt-5.4 | RETAIN conflictivo | 6.66193 | 6.66193 | `<1.1e-14` |

Las cuatro ramas de DeepSeek quedaron a menos de `0.435` de la referencia y, en particular,
pasaron los controles limpios con margen frente al corte predeclarado de `1.5`. Su contraste
REVISE guardado contra la verdad fue `B=0.0125467`, muy por debajo del umbral candidato `0.25`;
normalizado contra la referencia finita da `B=0.0154239`, la misma lectura nula. En RETAIN, el
informe conflictivo quedó incluso más cerca de la referencia que el limpio, por lo que tampoco
hay una penalización bilateral escondida.

GPT-5.4 capturó prácticamente el 100% del movimiento hacia la referencia finita en las cuatro
ramas. Los contrastes guardados fueron `-2.89e-15` en REVISE y `-7.11e-15` en RETAIN: cero a
precisión numérica. Pasaron sus dos controles limpios y fallaron, como debía ocurrir bajo el
nulo, las dos compuertas de señal candidata `B>=0.25`.

El raw de DeepSeek conserva en `predeclared_reading` las antiguas compuertas secundarias contra
la verdad oculta. Las cifras de referencia finita anteriores se recalculan determinísticamente
con la fórmula ya fijada para v1 y los LLR guardados; no requieren releer la conducta ni elegir
una nueva vara después del resultado.

### Decisión después de v1

**Cerrar esta implementación sin tuning.** Dos exposiciones válidas, con dos modelos frontier y
el mismo paquete, no apoyan que el conflicto firmado aislado frene la actualización. Ajustar
magnitudes, orden o redacción hasta obtener el efecto sería perseguir ruido.

Si la hipótesis se revisita, el próximo contraste admisible debe conservar el **mismo multiset
exacto de filas** y variar únicamente su agrupación o `study_id`. Solo así se podrá atribuir una
diferencia a la estructura entre estudios en vez de a diferencias residuales entre paquetes.

Raws v1 auditados:

- `scripts/out/first_story_scm_signed_study_conflict/probe_DeepSeek-V3.2_seed97810_pkg1_v1.json`
- `scripts/out/first_story_scm_signed_study_conflict/probe_gpt-5.4_seed97910_pkg1_v1.json`

## Autopsia histórica del v0 inválido

| Rama | `ΔG` Mpre North | `ΔG` Mlast North | Fracción nominal de revisión | Lectura descriptiva |
|---|---:|---:|---:|---|
| REVISE + limpio | 8.124 | 3.170 | `U=0.610` | se movió hasta la pendiente empírica del reporte |
| REVISE + conflicto | 8.124 | 8.124 | `U≈0` | conservó el modelo previo |
| RETAIN + limpio | 8.124 | 4.838 | — | se movió hasta la pendiente empírica del reporte |
| RETAIN + conflicto | 8.124 | 4.843 | — | casi idéntico al limpio |

El contraste registrado fue `B = U_REVISE,clean - U_REVISE,conflict = 0.609812`. Superó el
umbral exploratorio `0.25`, pero no puede aislarse como efecto del conflicto con esta corrida.

### La corrección matemática que invalida las varas limpias

Cada reporte tenía 12 observaciones en grado 3 y 12 en grado 7. Con la parametrización y
varianza usadas por el instrumento, el LLR agregado entre los dos polos discretos satisface
exactamente:

`LLR = 12 × (mean_G3 - mean_G7 + 4)`.

Por lo tanto, un reporte con `LLR=+10` no implica que la pendiente continua observada sea cero:
implica `mean_G7 - mean_G3 = 4 - 10/12 = 3.167`. Del mismo modo, `LLR=-10` implica una
pendiente observada de `4 - (-10)/12 = 4.833`.

Los datos y los agentes siguieron esa identidad casi exactamente:

| Control limpio | LLR real | `mean_G7 - mean_G3` en las 24 filas | `ΔG` final del agente |
|---|---:|---:|---:|
| REVISE | +9.9626 | 3.1698 | 3.1698 |
| RETAIN | -10.0532 | 4.8378 | 4.8378 |

Así, el agente no “falló” las ramas limpias en el sentido que suponían las compuertas. Ajustó
un modelo continuo flexible a la evidencia finita disponible. La vara que exigía acercarse a la
**verdad oculta** (`ΔG=0` en REVISE y `ΔG=8` en RETAIN) confundía dos cosas: el mundo que generó
los datos y la actualización racional a partir de una muestra ruidosa. Sin una norma binaria
declarada o un actualizador continuo de referencia, `U` no tenía la interpretación normativa
que le dimos.

### Compuertas y problemas de ejecución

- `clean_revise_U_ge_075=false`: `U=0.610`, aunque el valor final coincide con la pendiente
  empírica de las filas.
- `clean_retain_abs_error_le_15=false`: el error nominal contra 8 fue `3.162`, también explicado
  por la pendiente empírica.
- `zero_post_report_experiments_all=false`: `retain_clean` ignoró el cierre de recolección e hizo
  cuatro experimentos adicionales. Las otras tres ramas no hicieron ninguno.
- El conflicto viejo tuvo orden `correcto, opuesto, correcto, opuesto`; el último estudio era
  opuesto. No se puede separar conflicto acumulado de recencia.
- Las ramas no fueron operacionalmente homogéneas. Por ejemplo, el primer modelo cambiado de
  `revise_clean` fue inválido por `NameError: nan`; luego produjo una entrega válida. Sumado a los
  experimentos extra de `retain_clean`, esto deja errores y oportunidades de reparación distintos
  entre celdas.
- Los cuatro reportes usaron filas diferentes. Igualar solo el LLR binario no iguala toda la
  evidencia relevante para un agente que puede estimar una pendiente continua.

Pasaron los controles mecánicos de replay, inyección única, hashes, artefacto final puntuable y
entrega aceptada en 4/4. Eso confirma que la corrida ocurrió y que la señal descriptiva es real;
no repara los defectos de identificación anteriores.

### Qué sí y qué no aprendimos

**Sí:** en esta trayectoria hubo una diferencia conductual grande entre el paquete limpio y el
paquete con estudios de signos opuestos, aun con LLR binario agregado parecido. Es una pista útil
para rediseñar el instrumento.

**No:** no demostramos que “el conflicto causa rigidez”. El orden, las filas, los errores de
ejecución y la referencia normativa cambiaron o fallaron de maneras que permiten explicaciones
alternativas. Esta corrida no debe contarse como reproducción del vicio ni entrar en una tasa de
prevalencia.

### Decisión tomada tras v0

**NO REEJECUTAR DE INMEDIATO Y NO RECLAMAR EFECTO CAUSAL.** La siguiente prueba prioritaria es el
contraste de alcance/refactor `shared` vs `split`, que nace de una falla de propagación ya observada
y tiene una intervención más limpia.

Si retomamos conflicto, hay dos rutas defendibles:

1. usar el **mismo multiset exacto de filas** en limpio y conflicto, variando únicamente cómo se
   agrupan o etiquetan por `study_id`; así se conserva toda la evidencia agregada y cambia solo la
   estructura de conflicto entre estudios;
2. declarar explícitamente una norma binaria con su prior y evaluar la decisión entre esos dos
   polos, sin fingir que esa vara es el posterior único de una pendiente continua libre.

### Artefacto v0 auditado

- Raw: `scripts/out/first_story_scm_signed_study_conflict/probe_DeepSeek-V3.2_seed97801.json`
