# Codex ronda 8 — veredicto sobre la formulación de Lucas (targeted curriculum) + velocidad/cobertura por vicio — 2026-07-10

> Se le pasó la formulación textual de Lucas ("entornos genéricos en teoría, diseñados para que ganarlos mejore lo que sabemos de antemano") y el split velocidad/cobertura de Claude. Veredicto: la formulación es CORRECTA como descripción del propósito, no como resultado demostrado. Nombre del patrón: targeted curriculum / environment design (no open-endedness aún). El split es real pero por SITUACIÓN no por vicio; "único proveedor" → "presión selectiva directa". Mapeo por vicio (causal+rigor=cobertura; pozo+representación=velocidad; actualización+verificación=mixtos; taste completo fuera de ambos). Criterio mejorar-vs-trampear: invariancia + sensibilidad estructural. Respuesta directa a Lucas en (d). Integrado a ADR 0126. Crudo:

codex
Veredicto: la formulación de Lucas es correcta como descripción del propósito, no como resultado demostrado. WAGER intenta concentrar gradiente sobre conductas epistémicas elegidas. Todavía no sabemos si efectivamente las mejora, si solo enseña shortcuts WAGER ni si supera a entrenamiento genérico con igual cómputo.

### (a) Qué es exactamente

El nombre más preciso es:

- **Targeted curriculum design**: selección deliberada de tareas para acelerar capacidades concretas.
- **Environment/task-distribution design**: se diseña la distribución, no el reward intermedio.
- **Procedural environment generation**: la fábrica produce variaciones.
- **Automatic curriculum/UED** si el generador se adapta a las debilidades actuales del agente.
- **Open-endedness**, todavía no. WAGER parte de vicios y estructuras definidos por humanos dentro de un DSL acotado. POET es open-ended porque coevoluciona problemas y soluciones y encuentra stepping stones no anticipados; WAGER hoy es un curriculum dirigido y finito. [POET](https://arxiv.org/abs/1901.01753), [PAIRED/UED](https://aima.eecs.berkeley.edu/~russell/papers/neurips20-paired.pdf).

Le falta afilar tres cosas:

1. Los mundos no son “genéricos” distribucionalmente: están sesgados a propósito. Lo genérico es el algoritmo RLVR y la forma del reward.
2. “Preparar tareas para mejorar X” no implica que se aprenda X: puede aprenderse una pista superficial correlacionada.
3. WAGER incorpora conocimiento humano sobre qué practicar. Eso puede acelerar mucho con cómputo limitado, pero también imponer un techo humano. La literatura encuentra beneficios modestos del curriculum en benchmarks estándar y beneficios mayores con presupuesto limitado o datos ruidosos. [When Do Curricula Work?](https://arxiv.org/abs/2012.03107).

La bitter lesson no dice “no diseñes entornos”; Go también fue elegido por humanos. Dice que no codifiques manualmente la solución ni dependas de conocimiento que no escala. WAGER es compatible con ella si los humanos diseñan experiencia diversa y dejan que un método general descubra la política. La contradice si el catálogo termina siendo un repertorio fijo de “lecciones correctas”.

### (b) Velocidad vs cobertura

El split es real, pero no se aplica limpiamente por vicio sino por **situación de entrenamiento**.

Formalmente:

- Si la situación aparece con probabilidad baja \(p\), concentrarla compra eficiencia de muestra: aproximadamente necesitás muchas menos muestras que esperando encontrarla incidentalmente.
- Si está fuera del soporte de entrenamiento, dos políticas que difieren solamente allí reciben exactamente el mismo reward. Ninguna cantidad de RL sobre esa distribución puede preferir directamente la política correcta. Puede emerger por transferencia o inductive bias, pero no está siendo seleccionada.

Por eso “único proveedor” es demasiado fuerte. WAGER sería un proveedor de **presión selectiva directa**, no necesariamente el único ni una garantía de aprendizaje.

| Vicio | En AHC/code/math estándar | Lectura |
|---|---|---|
| **Actualización** | Fallos, scores y tests contradicen hipótesis constantemente. | **Velocidad** para actualizar en general. **Cobertura** para evidencia tardía, de confiabilidad incierta, que contradice un prior fuerte o llega por fuentes distintas. |
| **Pozo/pivoteo/parada** | AHC está lleno de local optima, enfoques muertos, tiempo limitado y costo de oportunidad. | Casi enteramente **velocidad/diagnóstico**. Es el peor candidato para reclamar exclusividad. |
| **Verificación/rigor** | Tests y verificadores ya castigan código o respuestas incorrectas. | **Velocidad** para verificar corrección. **Cobertura** para replicación costosa, optional stopping, error de medición, precisión fabricada y significancia irrelevante. |
| **Representación/creatividad** | Inventar algoritmos, abstraer y reformular es central en AHC. | Principalmente **velocidad**. WAGER especializa la presión hacia representar un DGP oculto, pero no monopoliza la capacidad. |
| **Causal** | Normalmente no existe diferencia observacional/intervencional ni selección/confounding: las reglas son conocidas y ejecutar el simulador da feedback limpio. | El caso más claro de **cobertura** dentro de AHC estándar. Deja de ser exclusivo si otros entornos incluyen causal discovery o system identification. |
| **Síntesis-reflejo** | AHC puede premiar descomponer, reemplazar o reformular frente a una idea habitual. | **Velocidad** para flexibilidad representacional. Pero el “research taste” amplio —qué problema merece investigarse, novedad y valor científico— está fuera de AHC **y también mayormente fuera del WAGER actual**. WAGER solo captura la parte que termina afectando predicción ejecutable. |

La afirmación más defendible es: causalidad y rigor estadístico tienen un verdadero argumento de cobertura; pozo y representación tienen sobre todo un argumento de eficiencia. Actualización y verificación son mixtos. “Taste” completo todavía no está resuelto por WAGER.

### (c) Mejorar vs trampear

La condición correcta tiene dos mitades:

1. **Invariancia:** cambiar dominio, nombres, números, orden, fachada y demás nuisance variables no debe cambiar la política ganadora.
2. **Sensibilidad estructural:** manteniendo la fachada, invertir el mecanismo epistémico debe invertir qué conducta gana.

Un agente aprende la capacidad solo si pasa ambas. Si pasa únicamente variaciones superficiales, aprendió el dialecto. Si aplica siempre “desconfiá”, “intervení” o “seguí investigando”, los contrafácticos deben destruirlo.

La maquinaria actual no alcanza todavía:

- La diversidad estructural es una doctrina y un catálogo, no un resultado demostrado a escala.
- La fábrica genera sobre todo diversidad dentro de estructuras conocidas.
- Los pares no son universales.
- Un held-out del mismo generador puede conservar exactamente el mismo shortcut.
- No hubo entrenamiento seguido de transferencia externa.
- La validez por pistas falló en su primer protocolo serio.

Hace falta split por **familia estructural/composición**, no por seed; generadores o autores independientes para evaluación; pares que reviertan cada heurística barata; y ataques con optimizadores entrenados específicamente para ganar sin la conducta pretendida. La generación procedural mejora generalización solo hasta donde llega el soporte del generador. [Procgen](https://proceedings.mlr.press/v119/cobbe20a.html).

### (d) Respuesta directa a Lucas

Sí: WAGER es, en gran parte, identificar antes ciertas fallas y fabricar práctica verificable para corregirlas con menos cómputo. Donde esas situaciones ya aparecen en RLVR genérico, es un acelerador; donde no aparecen, agrega presión de entrenamiento que hoy falta, aunque la misma capacidad podría emerger indirectamente o ser entrenada por otros entornos. No inventa otro principio de aprendizaje ni garantiza juicio: su valor depende de demostrar que sus mundos enseñan una política que sobrevive fuera de WAGER. Si con igual cómputo no supera a RLVR genérico en tareas externas y estructuralmente nuevas, entonces es solo un benchmark artesanal bien instrumentado.
