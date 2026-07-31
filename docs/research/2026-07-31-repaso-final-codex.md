# Repaso final de literatura y proyectos — Codex

**Fecha de corte:** 2026-07-31  
**Objeto:** el pivote de WAGER hacia la revisión proporcional de modelos bajo señal, trayectoria y fricción.  
**Estado de este documento:** triage de evidencia cruda para cruzar con el repaso de Claude. **No modifica ni reemplaza** `docs/lectura-de-fuentes.md`.

## Veredicto ejecutivo

El camino **sí puede producir un paper interesante**, pero la ventana de novedad es bastante más estrecha de lo que sugería el encuadre inicial.

El competidor conceptual más próximo es ahora [When Should Models Change Their Minds? / BeliefTrack](https://arxiv.org/abs/2605.30219): ya usa dos mundos cerrados, un oráculo simbólico por turno y separa error bajo estado estable, error después de una corrección y degradación por ruido irrelevante. [BayesBench](https://arxiv.org/abs/2606.30850) mide trayectorias multi-turno contra referencias bayesianas; [LLMs are not (consistently) Bayesian](https://arxiv.org/abs/2605.06915) separa subactualización, sobreactualización y dirección errónea; [STALE](https://arxiv.org/abs/2605.06527) encuentra una brecha entre reconocer una actualización y aplicarla; [Seeing Isn't Believing](https://arxiv.org/abs/2604.17252) estudia inercia de creencias en agentes que actúan; y [BoxingGym](https://arxiv.org/abs/2501.01540) ya combina mundos generativos, experimentación y revisión de modelos.

Dos anclas adicionales estrechan todavía más el claim: [Autonomous Model Discovery](https://arxiv.org/abs/2607.06413) ya hace que agentes de código entreguen un simulador ejecutable puntuado por KL y distancia distribucional contra una verdad oculta, sin juez LLM; y [GeneBench-Pro](https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf) ya puntúa determinísticamente trabajo científico multi-etapa sobre DGPs conocidos y reporta una brecha entre notar señales locales y propagarlas a la decisión. Ninguno inyecta evidencia dosificada en un modelo previo ni mide costo de reabrirlo, pero ambos ocupan parte importante de la forma de evaluación.

Eso **no mata WAGER**. Sí mata una versión genérica del claim: “primer benchmark multi-turno de belief revision”, “primero en medir cuándo cambiar/conservar/ignorar”, “primer replay contrafactual de agentes”, “primer uso de mundos ocultos y scoring predictivo” o “primero sin juez LLM”. Todas esas piezas ya tienen prior art.

La contribución todavía defendible es más precisa:

> **Estimar cómo interactúan el valor probatorio de la evidencia, la exposición a una trayectoria previa y el costo real de reparación para producir desviación respecto de la actualización legal en un artefacto ejecutable —tanto en dirección (alejarse, reforzar o conservar) como en magnitud (desde parcial hasta fuerte)—.**

Ninguna fuente revisada permite estimar esa interacción sobre una entrega ejecutable con una referencia legal programática. Ese **estimando** —no la mera suma de componentes— es la posible novedad. El método de fork no es por sí mismo novedoso: [Causal Agent Replay](https://arxiv.org/abs/2606.08275) ya formaliza intervenciones y reejecución downstream. WAGER sólo podrá llamarlo causal para los factores manipulados de forma apareada dentro del mismo mundo y checkpoint; comparar escenarios distintos demuestra generalización o heterogeneidad, no identifica por sí solo el efecto de “haber vivido” el trabajo.

Mi opinión cruda es: **GO condicionado**. Seguiría con el proyecto si la próxima etapa se diseña alrededor de esa intersección. Lo abandonaría o reduciría a una nota de benchmark si termina siendo solamente “los modelos usan peor una evidencia cuando está rodeada de texto”, porque eso ya es un resultado de context rot/distracción con otra decoración.

---

## 1. Qué pregunta queda realmente abierta

La pregunta fuerte no es si los modelos “cambian de opinión”. Es:

> **Dado un modelo previo, una cantidad conocida de evidencia nueva y una respuesta legalmente alcanzable —incluido no cambiar—, ¿qué determina la distancia entre la actualización que debería ocurrir y la que efectivamente aparece en la entrega?**

La respuesta legal tiene dos componentes: **dirección** y **magnitud**.

| Estado probatorio | Dirección correcta | Magnitud correcta | Falla relevante |
|---|---|---|---|
| La evidencia refuta el modelo previo | Alejarse de él | Proporcional a la fuerza probatoria | Rigidez, sub/sobreactualización o signo equivocado |
| La evidencia confirma de manera informativa | Reforzarlo o concentrarlo | Proporcional a la fuerza probatoria | Ignorar confirmación o volverse injustificadamente dogmático |
| La evidencia no discrimina o es placebo | Cero: conservar | Cero | Influenciabilidad o cambio espurio |

`PARTIAL` no es una cuarta conducta: describe una magnitud intermedia que puede alejarse del modelo previo o reforzarlo. El análisis debe cruzar dirección × magnitud en vez de reducir todo a “cambió/no cambió”.

La variable dependiente tampoco debería ser sólo una probabilidad declarada. Hay al menos cuatro niveles separables:

| Nivel | Pregunta |
|---|---|
| **Reconoce** | ¿Identifica verbalmente qué implica la evidencia? |
| **Registra** | ¿Modifica su modelo o creencia explícita? |
| **Actúa / compra** | ¿Busca las verificaciones y cambia su política de investigación? |
| **Entrega** | ¿La respuesta justificada está incorporada en el artefacto ejecutable puntuado contra el mundo? |

El outcome primario debe ser la **desviación de la entrega respecto de la respuesta legal**, junto con su consecuencia contra la verdad oculta. La pérdida entre niveles —reconocer sin registrar, registrar sin actuar, o declarar y actuar sin reparar— es un mecanismo secundario muy informativo, no una condición necesaria para que el paper tenga valor. Puede existir una curva importante de revisión aplicada aunque reconocimiento y entrega fallen juntos.

---

## 2. Mapa comparativo: dónde está y dónde no está la novedad

| Trabajo | Trayectoria multi-turno | Trabajo propio / dependencias | Actualización normativa graduada | Consecuencia aplicada | Manipulación causal apareada |
|---|---:|---:|---:|---:|---:|
| **WAGER propuesto** | Sí | Sí, a manipular | Revisar / reforzar / conservar / parcial | Modelo ejecutable, score server-side | Sí, fork desde el mismo checkpoint |
| [BeliefTrack](https://arxiv.org/abs/2605.30219) | Sí | No; historial de evidencia formal | Estado discreto exacto; no magnitud probabilística | Lista declarada de hipótesis, verificada simbólicamente | Clean/noise apareado; no carga ni fricción |
| [Kumaran et al.](https://www.nature.com/articles/s42256-026-01217-9) | Dos turnos | Sólo respuesta previa visible | Sí, contra consejo con confiabilidad | Nueva respuesta/confianza | Sí |
| [BayesBench](https://arxiv.org/abs/2606.30850) | Sí | No hay proyecto acumulado | Sí, posterior/predictiva por turno | Predicción MCQ por logits | Compara formatos; no carga de revisión apareada |
| [Bayesian Teaching](https://arxiv.org/abs/2503.17523) | Cinco rondas | No hay proyecto acumulado | Sí, asistente bayesiano normativo | Recomendación downstream | Evalúa/fine-tunea; no manipula carga apareada |
| [BASIL](https://arxiv.org/abs/2508.16846) | Probes de una ronda | No | Coherencia con probabilidades auto-elicitadas | Posterior verbalizado | Usuario vs tercero; no entrega |
| [Belief-R](https://aclanthology.org/2024.emnlp-main.586/) | Secuencias cortas | No | Actualizar vs no actualizar | Respuesta de razonamiento textual | Dataset controlado |
| [STALE](https://arxiv.org/abs/2605.06527) | Historia larga | Memoria sobre el usuario, no obra científica propia | Principalmente invalidación | Recomendación downstream, juzgada por LLM | Probes distintos; no dosis apareada |
| [MemSyco-Bench](https://arxiv.org/abs/2607.01071) | Diálogos/memoria persistente | Memoria histórica del usuario, no hipótesis propia | Usar / limitar / actualizar / ignorar memoria | Respuesta final, juzgada por LLM | Compara sistemas de memoria; no fork causal |
| [Seeing Isn't Believing](https://arxiv.org/abs/2604.17252) | Sí | Trayectoria de acciones | Principalmente corregir estado contradicho | Éxito en entorno embodied | Intervención de scaffold, no mapa de carga |
| [BoxingGym](https://arxiv.org/abs/2501.01540) | Sí | Sí, experimentación acumulada | Implícita en datos sucesivos | Predicciones y modelo/explicación | No aísla causalmente una revisión |
| [Agentic Automata Learning](https://arxiv.org/abs/2606.16576) | Sí | Sí, queries e hipótesis | Contraejemplos formales | DFA ejecutable aceptado/rechazado | No aísla señal, trayectoria o fricción |
| [Autonomous Model Discovery](https://arxiv.org/abs/2607.06413) | Una sesión agéntica de model discovery | Construye desde cero; no revisa un modelo comprometido | No hay actualización post-evidencia | Simulador ejecutable, KL/DLD contra verdad oculta | Full vs half-data apareado; no fork de un prefijo |
| [GeneBench-Pro](https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf) | Sí, análisis científico multi-etapa | Sí, decisiones dependientes | Implícita; no trayectoria normativa de creencia | Estimando final, grader determinista pass/fail | No inyecta evidencia ni bifurca un checkpoint |
| [HEP](https://arxiv.org/abs/2607.09195) | Sí | Sí, hipótesis persistentes | Probabilidad y lifecycle explícitos | Informe científico; registro auditable | Compara harnesses, no dosis de evidencia |
| [FCPAgent](https://arxiv.org/abs/2607.24167) | Sí | Plan, skills y dependencias | Confirmar / falsar / reparar por alcance | Éxito funcional en WebArena | Ablaciones de sistema; no revisión natural apareada |
| [Corral](https://arxiv.org/abs/2604.18805) / [KellyBench](https://arxiv.org/abs/2604.27865) | Sí | Sí | Observada post hoc | Resultado/decisión real del entorno | No aíslan el mecanismo causal |
| [BACKTRACE / BackroomBench](https://arxiv.org/abs/2607.27484) | No; decisiones aisladas | No | Dependencia causal de un skill, no revisión graduada | Respuesta discreta y reliance determinista | Sí: fija todo salvo skill/asignación |

La tabla muestra la oportunidad y el peligro. Los componentes individuales ya existen. La originalidad no puede defenderse como “nadie juntó estas piezas”: debe estar en un estimando que los trabajos previos no recuperan, idealmente la interacción causal entre valor probatorio, trayectoria y costo de reparación sobre la desviación *oracle-relative* de una entrega ejecutable.

---

## 3. Fuentes que más cambian el posicionamiento

Los rótulos significan:

- **COMPITE:** ocupa parte del claim o de la contribución metodológica.
- **VALIDA:** demuestra que el fenómeno o la necesidad importan, pero no responde nuestra pregunta.
- **CAMBIA EL DISEÑO:** introduce un control, una objeción o una métrica que no conviene ignorar.

### 3.1 Competidores directos o casi directos

| Fuente verificada | Qué hace realmente | Veredicto para WAGER |
|---|---|---|
| [When Should Models Change Their Minds? Contextual Belief Management in Large Language Models](https://arxiv.org/html/2605.30219) — Xu et al., v1, mayo de 2026; [repo anunciado](https://github.com/zjunlp/CBM) | **Es el competidor conceptual más directo.** BeliefTrack usa Rule Discovery y Circuit Diagnosis, un espacio finito de hipótesis y un oráculo simbólico exacto por turno. Distingue `Failed Stay`, `Failed Update` y `Failed Isolation`, y además varía profundidad redundante y demora de la corrección. Pero `Stay` cuenta cualquier estado final distinto del oráculo cuando éste permanece estable —no necesariamente un cambio indebido— y `Update` ocurre tras una instrucción explícita `CORRECTION` que reemplaza evidencia anterior. La creencia es un conjunto lógico, no una distribución: no mide dosis, sub/sobreactualización gradual ni actualización parcial. Sus cifras de 97–99% corresponden a Qwen2.5-7B bajo un criterio *any-of-three*: una muestra falla si falla cualquiera de tres generaciones; Qwen3.5-9B tiene tasas menores salvo 95,4% en aislamiento de Circuit Diagnosis. | **COMPITE FUERTE + VALIDA + CAMBIA EL DISEÑO.** Ocupa cualquier claim de primer benchmark exacto sobre mantener/corregir/aislar ruido, parte del eje temporal y también usa verificación sin juez LLM. WAGER conserva evidencia graduada, investigación activa, costo de reparación y entrega ejecutable. `PARTIAL` y la magnitud/dirección de `M0→M1` pasan a ser esenciales. CLEAN vs ruido por sí solo ya no alcanza como contribución. |
| [BayesBench: Evaluating LLM Belief Trajectories Under Multi-Turn Evidence Accumulation](https://arxiv.org/abs/2606.30850) — Samanta et al., preprint, junio de 2026; [código](https://github.com/Ankur-Samanta/BayesBench) | Cuatro entornos simulados: moneda, recomendación, juicio social y triaje. Sigue por turno la inferencia de latentes y la predicción downstream, con posterior bayesiana cerrada donde es posible. Encuentra subactualización en modelos chicos, sobreactualización en grandes y una brecha entre inferir el latente y usarlo para predecir. Usa probes MCQ/log-probabilities; no hay proyecto, herramientas, reapertura ni artefacto construido. | **COMPITE FUERTE + CAMBIA EL DISEÑO.** Ya ocupa “trayectorias multi-turno contra un ideal bayesiano”. WAGER debe citarlo como predecesor inmediato y concentrarse en carga de revisión y entrega ejecutable. Su separación `latent inference → downstream prediction` es el análogo más cercano de nuestra brecha `declara/registra → entrega`. |
| [Bayesian Teaching Enables Probabilistic Reasoning in Large Language Models](https://arxiv.org/html/2503.17523) — Qiu et al., 2025 | En cinco rondas, el asistente infiere una función de preferencias oculta a partir de elecciones del usuario y recomienda vuelos; un asistente bayesiano define la referencia normativa. Los modelos off-the-shelf mejoran poco después de la primera ronda —incluso al extender a 30 rondas—, mientras que fine-tuning sobre decisiones del asistente bayesiano enseña actualización aproximada y generaliza. Al elicitar las preferencias y convertirlas externamente en decisiones, la predicción supera a la decisión directa; en los modelos originales ambas coinciden menos del 50%. | **COMPITE + VALIDA FUERTE.** Ya muestra estancamiento multi-ronda y una brecha creencia verbalizada→decisión. Pero la interacción no acumula una obra que haya que reabrir, no manipula costo/autoría y evalúa recomendación, no reparación de un modelo ejecutable. Es antecedente normativo y también baseline conceptual de mitigación, no sustituto de WAGER. |
| [LLMs are not (consistently) Bayesian](https://arxiv.org/abs/2605.06915) — Chen et al., Apple/Stanford/Princeton, mayo de 2026 | Trata al LLM como regla de procesamiento de información y mide el gap entre cambio de creencia y evidencia, distinguiendo dirección equivocada, subactualización y sobreactualización. Hallazgo incómodo: forzar consistencia con las likelihoods elicitadas no siempre mejora la tarea, porque el modelo probabilístico elicitado puede estar mal especificado. | **COMPITE + CAMBIA EL DISEÑO.** La proporcionalidad ya tiene una formalización seria. No debemos llamar “normativo” a cualquier Bayes construido desde creencias del propio LLM. El oráculo de WAGER debe usar la distribución generativa conocida y sólo información legal, no likelihoods auto-reportadas por el modelo. |
| [BASIL: Bayesian Assessment of Sycophancy in LLMs](https://arxiv.org/html/2508.16846) — Atwell et al., versión leída v6, mayo de 2026 | Elicita prior, likelihoods y posterior verbalizados en forecasting, moralidad y aceptabilidad cultural. Compara evidencia sola, evidencia + opinión de un tercero y evidencia + opinión del usuario. El contraste tercero→usuario aísla el efecto extra de la fuente indexical, no “sociedad vs evidencia” de forma perfecta. Su posterior normativo se calcula con probabilidades declaradas por el propio modelo, no con verdad server-side. Separa casos que ya estaban por encima/debajo de ese target y muestra que la presión puede agravar una sobreactualización o compensar por accidente una subactualización. | **VALIDA + CAMBIA EL REPORTE; COMPITE POCO CON EL NÚCLEO.** Conviene copiar el reporte separado de under/over/wrong-direction y la idea de que un sesgo puede mejorar el score por razones incorrectas. No conviene copiar literalmente su métrica: WAGER tiene un oráculo legal más fuerte. Es declarativo, sin trayectoria, herramientas, costo ni entrega. |
| [Competing Biases underlie Overconfidence and Underconfidence in LLMs](https://www.nature.com/articles/s42256-026-01217-9) — Kumaran et al., *Nature Machine Intelligence*, 2026 | Manipula respuesta inicial visible/oculta y consejo mismo/opuesto/neutral. Encuentra dos fuerzas: refuerzo de la elección propia e hiperponderación del consejo contrario. Cuando la respuesta se atribuye a otro modelo, desaparece el efecto de autoría propia. | **COMPITE FUERTE + VALIDA.** Es el predecesor causal directo del eje autoría/compromiso, no sólo “la esquina fácil”. WAGER agrega trabajo acumulado y consecuencias, pero debe replicar conceptualmente sus controles de visibilidad, autoría y evidencia neutral. |
| [Belief Revision: The Adaptability of Large Language Models Reasoning (Belief-R)](https://aclanthology.org/2024.emnlp-main.586/) — Wilie et al., EMNLP 2024 | Evalúa razonamiento defeasible con nueva premisa. El resultado clave es bilateral: modelos que actualizan mejor también suelen rendir peor cuando no hacía falta actualizar. | **COMPITE + CAMBIA EL DISEÑO.** Hace obligatorio incluir `RETAIN`; no puede quedar como extensión futura. La diferencia es que Belief-R puntúa conclusiones textuales sin trayectoria de investigación ni artefacto. |
| [BeliefShift](https://arxiv.org/abs/2603.23848) — Myakala et al., preprint, marzo de 2026 | Benchmark longitudinal de 10–50 sesiones que separa estabilidad, revisión por evidencia, contradicción y deriva sin evidencia. Su propia limitación reconoce que la evidencia es binaria y reclama calidad graduada. En realidad sigue la representación que el asistente mantiene de **las creencias del usuario**, no la revisión de un modelo científico propio. | **COMPITE CON EL ENCUADRE + VALIDA + CAMBIA EL DISEÑO.** Refuerza la simetría adaptar/resistir y la zona intermedia. No ocupa nuestra entrega ejecutable. Precaución: no encontré enlace público a código/dataset en el paper y sus artefactos/escala deben auditarse antes de tratar sus cifras como evidencia firme. |
| [BoxingGym](https://arxiv.org/abs/2501.01540) — Gandhi et al., Stanford, 2025; [código](https://github.com/kanishkg/boxing-gym) | Diez mundos probabilísticos, experimentación activa, EIG, predicción y revisión de teorías. Incluso documenta supuestos previos que no se revisan y modelos explícitos que no se aprovechan bien. | **COMPITE FUERTE.** “Mundo generativo + agente científico + predicción” no es novedad. WAGER debe presentarse como una disección causal de la revisión dentro de esa clase de tareas, no como una nueva clase de mundos. |
| [Can LLM Agents Infer World Models? Evidence from Agentic Automata Learning](https://arxiv.org/abs/2606.16576) — Menaged et al., preprint, junio de 2026; [proyecto](https://reefmenaged.github.io/Agentic_Automata_Learning/) | El agente consulta un DFA oculto mediante membership/equivalence queries, recibe contraejemplos y entrega un DFA verificable. Tiene presupuesto, complejidad graduada, baselines algorítmicos fuertes y análisis de fallas de integración de evidencia. | **COMPITE FUERTE + CAMBIA EL DISEÑO.** Ya existe un mundo oculto con hipótesis formal ejecutable y refutaciones. La diferencia defendible de WAGER es el fork causal pre/post y la manipulación de costo de reabrir. También eleva el estándar: conviene tener al menos un baseline algorítmico/oráculo, no sólo comparar LLMs. |
| [An Experimental Design Approach to Evaluating Agentic AI's Autonomous Model Discovery](https://arxiv.org/html/2607.06413) — He et al., julio de 2026 | Agentes de código construyen modelos predictivos y un simulador ABM ejecutable sobre un juego oculto. El ABM se puntúa contra el DGP mediante KL sobre seis magnitudes y distancia distribucional basada en Levenshtein, sin juez LLM. Analiza 140 corridas y tiene un contraste matched full-vs-half-data, pero cada run descubre desde cero: no hay checkpoint con una creencia previa ni evidencia post-hoc que obligue a revisarla. | **COMPITE FUERTE EN LA FORMA DE ENTREGA + CAMBIA EL CLAIM.** Ya ocupa “agente entrega modelo ejecutable contra verdad oculta con score distribucional y cero juez”. WAGER debe diferenciarse por revisión causal pre/post, dosis, conservación correcta y costo de reabrir. También sugiere reportar calidad, costo y proceso como coordenadas separadas. |

### 3.2 Fuentes que validan la brecha “saber no implica aplicar”

| Fuente verificada | Qué aporta | Veredicto para WAGER |
|---|---|---|
| [STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?](https://arxiv.org/abs/2605.06527) — Chao et al., mayo de 2026; [código](https://github.com/icedreamc/STALE) | 400 conflictos implícitos en historias de hasta 150K tokens. Separa `State Resolution`, resistencia a una premisa vieja y `Implicit Policy Adaptation`. Los modelos pueden reconocer que un estado quedó obsoleto y aun actuar desde él. Usa respuestas abiertas y juez LLM; cada instancia tiene una transición principal. | **VALIDA FUERTE + COMPITE PARCIAL + CAMBIA EL DISEÑO.** La brecha reconocimiento–aplicación ya está nombrada. Nuestra ventaja debe ser medir aplicación con un artefacto y verdad computable. Sugiere además probar invalidación propagada: corregir una parte puede exigir reparar dependencias. |
| [MemSyco-Bench: Benchmarking Sycophancy in Agent Memory](https://arxiv.org/html/2607.01071) — Xiang et al., julio de 2026; [código](https://github.com/XMUDeepLIT/MemSyco-Bench) | 1.550 casos en cinco regímenes: excluir memoria de preguntas objetivas, respetar su alcance, resolver conflicto memoria–evidencia, elegir la memoria vigente y usar memoria válida para personalizar. Mide accuracy, sycophancy, uso correcto y uso obsoleto. Los sistemas suelen seguir memorias desactualizadas aun recuperando la corrección; una instrucción cautelosa ayuda en conflicto pero perjudica la personalización. Los outputs abiertos usan juez LLM. | **VALIDA + COMPITE DE MANERA ADYACENTE.** Reproduce el trade-off `RETAIN/REVISE`, pero la memoria contiene sobre todo creencias y preferencias históricas del usuario en diálogos sintéticos; no es una hipótesis científica que el agente construyó mediante su propio trabajo. Obliga a separar memoria del usuario, resumen escrito por el memory system, exposición a historial y obra propia acumulada. |
| [Seeing Isn't Believing: Mitigating Belief Inertia via Active Intervention in Embodied Agents](https://arxiv.org/abs/2604.17252) — Wang et al., Findings ACL 2026; [código](https://github.com/WangHanLinHenry/EVU) | En ALFWorld, VirtualHome y ScienceWorld, agentes observan feedback que contradice su estado previo pero siguen actuando desde la creencia vieja. El mecanismo Estimate–Verify–Update mejora task success y el efecto persiste aun truncando a dos turnos, por lo que no es sólo long-context crowding. | **VALIDA FUERTE + COMPITE PARCIAL.** Ya hay belief inertia medida por acciones y reward del entorno. WAGER se diferencia por evidencia graduada, conservar/parcial, trabajo acumulado y medición causal del freno. EVU es un excelente baseline de mitigación para una etapa posterior, no para contaminar primero la medición natural. |
| [Toward Auditable AI Scientists: A Hypothesis Evolution Protocol](https://arxiv.org/abs/2607.09195) — Takahara y Mizoguchi, preprint, julio de 2026 | HEP registra hipótesis, probabilidades, evidencia, linaje y estados `supported/refuted/dormant`. En tareas de materiales, el harness fuerza un ciclo hipótesis–test–evidencia–belief que no aparece espontáneamente en el baseline. Pero el propio agente valida evidencia y asigna las probabilidades; la comparación principal usa sólo tres corridas por condición. | **COMPITE + VALIDA + CAMBIA EL DISEÑO.** `REGISTER` y creencias persistentes ya tienen un vecino claro. La contribución de WAGER es auditar si el registro corresponde al modelo entregado y a la verdad server-side. También advierte que registrar no es medición pasiva: es una intervención que puede mejorar la revisión. Debe permanecer idéntico entre brazos. |
| [Falsifiable Commitment Planning for Self-Correcting Web Agents](https://arxiv.org/html/2607.24167) — Liu et al., v1 del 27 de julio de 2026 | FCPAgent convierte cada paso del plan en una unidad con evidencia confirmatoria, falsadores y confianza. Durante la ejecución decide `continue/advance/repair` y, si hay contradicción, modifica el alcance mínimo: acción, skill o sufijo del plan. Usa verificación híbrida —tests ligeros + diagnóstico LLM— y validators funcionales de WebArena; reporta 65,3% frente a 57,4% del mejor baseline. El paper usa un solo backbone y no localicé un repo enlazado, así que el resultado requiere réplica. | **VALIDA FUERTE + COMPITE EN LA PUNTA APLICADA.** Ya existe una respuesta de ingeniería al problema “un compromiso debe saber cuándo deja de ser válido” con dependencias y consecuencia funcional. No mide la tendencia natural a revisar, no dosifica evidencia y no usa forks apareados. Para WAGER su taxonomía de alcance de reparación ofrece un control crucial: distinguir revisión epistémica de capacidad de reparar la implementación. |
| [GeneBench-Pro](https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf) — Li y Ho, OpenAI, junio de 2026 | 129 análisis científicos multi-etapa sobre DGPs simulados conocidos, con una mediana de seis decisiones dependientes. Un grader programático exige que todos los campos numéricos caigan dentro de tolerancias pre-especificadas. Reporta una brecha consistente entre notar señales diagnósticas locales y propagar sus consecuencias a la decisión; su limitación explícita es que el pass/fail equipara progreso parcial con falla total. | **ANCLA DE POSICIONAMIENTO + VALIDA FUERTE.** Ya ocupa trabajo científico “sucio”, verdad recuperable y grading determinista sin juez. No estudia revisión pre/post ni evidencia dosificada. WAGER puede medir de forma continua el fenómeno noticing→acting que GeneBench-Pro observa cualitativamente, pero no debe reclamar ser el primero en puntuar trabajo científico contra un DGP oculto. |
| [AI scientists produce results without reasoning scientifically](https://arxiv.org/abs/2604.18805) — Ríos-García et al., 2026 | En 25.000+ corridas científicas, la evidencia se ignora con frecuencia y la revisión refutacional es rara; es análisis observacional de trayectorias complejas. | **VALIDA FUERTE.** Justifica relevancia en agentes científicos reales, pero no identifica el mecanismo causal. WAGER puede ocupar precisamente esa explicación. |
| [KellyBench](https://arxiv.org/abs/2604.27865) — 2026 | En decisiones secuenciales largas, agentes describen correcciones que luego no implementan y mantienen modelos obsoletos ante datos nuevos. | **VALIDA FUERTE.** Es evidencia de carga alta y brecha dice–hace; no sustituye los brazos apareados ni la dosis server-side. |

### 3.3 Mecanismos y confundidores que no podemos ignorar

| Fuente verificada | Riesgo que introduce | Veredicto para WAGER |
|---|---|---|
| [When Agents Commit Too Soon](https://arxiv.org/abs/2606.22936) — Mehta, preprint, junio de 2026 | La convergencia representacional predice que la trayectoria se estabilizó, **pero no si es correcta**. Inducir compromiso reduce variación sin mejorar accuracy: afianza tanto caminos buenos como malos. | **VALIDA + CAMBIA EL DISEÑO.** “Compromiso” no puede codificarse como vicio por definición. Hay que cruzarlo con un modelo previo correcto e incorrecto y medir adaptación **y** resistencia. |
| [Old Habits Die Hard](https://arxiv.org/abs/2603.03308) — Simhi et al., 2026; [código](https://github.com/technion-cs-nlp/OldHabitsDieHard) | La historia conversacional sesga generaciones posteriores y produce persistencia conductual/geometría de trayectoria. | **VALIDA + CAMBIA EL DISEÑO.** Apoya que una trayectoria “vivida” puede importar más que una etiqueta, pero también implica que el efecto puede ser simple exposición al historial. Hay que describir el eje como historia/estado observable, no atribuir psicología al modelo. |
| [When Context Hurts](https://arxiv.org/abs/2605.04361) — Vigraham, preprint, mayo de 2026 | En diseño multiagente, el mismo artefacto contextual ayuda en unos problemas y perjudica en otros; incluso documentos irrelevantes pueden cambiar la exploración. El signo depende del régimen de convergencia basal. | **CAMBIA EL DISEÑO.** La mezcla puede alterar exploración, no sólo ocultar evidencia. Necesitamos bases por donante, fillers semánticamente auditados y evitar interpretar un efecto heterogéneo como una ley universal. Es preprint de un autor y sin repo localizado: evidencia sugerente, no ancla. |
| [PABU: Progress-Aware Belief Update](https://arxiv.org/abs/2602.09138) — Jiang et al., 2026 | Su “belief” es un estado compacto de progreso que decide qué acciones/observaciones retener para actuar con menos contexto; no una creencia sobre el mundo revisada por evidencia. | **DESCARTAR COMO PRIOR EPISTÉMICO.** Es un homónimo útil para no confundir vocabularios. Como antecedente de compresión de contexto aporta poco que Context Rot no sostenga mejor. |
| [Context Rot](https://www.trychroma.com/research/context-rot) — Chroma Technical Report, 2025; [código](https://github.com/chroma-core/context-rot) | En 18 modelos, el rendimiento cae de forma no uniforme al aumentar longitud aun en tareas simples; tipo de distractor y similitud importan. | **CAMBIA EL DISEÑO.** CLEAN vs MIXED sin un control de longitud/token y filler sería ambiguo. Este confundidor puede explicar todo el efecto de señal si no se aísla. |
| [The α-Law of Observable Belief Revision](https://arxiv.org/abs/2603.19262) — Farmer et al., preprint, febrero de 2026 | Propone una ley multiplicativa para revisiones de probabilidades bajo verificación/revisión repetida. Se limita a probabilidades observables en tareas de respuesta, no a proyectos con herramientas. | **COMPITE CON EL LENGUAJE DE “CURVA/LEY”.** Antes de prometer una ley de carga, debe leerse y auditarse a fondo. Si WAGER encuentra una curva, tendrá que explicar por qué no es simplemente otra parametrización de dinámica probabilística sin trayectoria. |
| [Martingale Score: An Unsupervised Metric for Bayesian Rationality in LLM Reasoning](https://arxiv.org/html/2512.02914) — He et al., diciembre de 2025 | Regresa `Δb` sobre la creencia previa; un coeficiente positivo indica que el prior predice su propio refuerzo. Encuentra score positivo en 51/54 setups CoT y asociación con peor Brier donde hay verdad. Pero `b` es asignado a cada paso por un juez LLM; el estudio se concentra en razonamiento extendido, no principalmente en evidencia externa. | **VALIDA + PUEDE CAMBIAR UN DISEÑO FUTURO.** La estimación publicada necesita muchos pares comparables prior→posterior; no exige en principio una única trayectoria larga, y WAGER podría construir escalares desde el artefacto. Aun así, no puede aplicarse “gratis” a la pasada 1: las 252 ramas reutilizan sólo 14 priors y la evidencia se eligió en función de `M0/KL`, violando el nulo exógeno que se querría interpretar. Sólo la usaría en una tanda diseñada con eventos escalares comunes, muchos donantes independientes y evidencia no seleccionada por el prior. |
| [Getting out of the Big-Muddy: Escalation of Commitment in LLMs](https://arxiv.org/html/2508.01545) — Barkett et al., agosto de 2025 | En viñetas de inversión con o4-mini, responsabilidad/autoría individual producen poca escalada y hasta divestment racional; la escalada aparece bajo deliberación social simétrica o un bundle extremo de identidad/presión. Es un único modelo, sin consecuencia real y con manipulación compuesta. | **VALIDA LA CAUTELA + DE-PRIORIZA EL “SUNK COST” GENÉRICO.** Apoya no asumir que trabajo propio basta para generar atrincheramiento y justifica haber dejado presión social/identidad fuera de v1. Si WAGER encuentra efecto de carga vivida sin esos prompts extremos, sería más interesante; si no, no hay que forzarlo. |

### 3.4 Replay, forks y realismo de evaluación

| Fuente verificada | Qué hace realmente | Veredicto para WAGER |
|---|---|---|
| [Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures](https://arxiv.org/html/2606.08275) — Shah, v1, junio de 2026; [código](https://github.com/jaineet17/causal-agent-replay) | Conserva factual el prefijo de una trayectoria, interviene un paso (`do_resample/action/observation/context/policy`) y reejecuta todo downstream varias veces. Formaliza efectos distribucionales, intervalos, point-of-commitment y Shapley para interacciones. Su validación publicada es pequeña: SCM sintéticos plantados y un demo con herramientas simuladas. El outcome puede ser computable o judge-based; el paper recomienda rule-based. | **PRIOR ART METODOLÓGICO + CAMBIA EL LENGUAJE.** WAGER no inventó el counterfactual replay. Su intervención se parece a `do_observation/do_context`, pero el estimando es distinto: efecto de señal/carga sobre revisión, no atribución del paso culpable. Además, WAGER serializa un snapshot en una conversación nueva; eso no es replay fiel del historial exacto. Hay que reclamar novedad en la pregunta, la norma legal y la entrega, y reportar el efecto total/ruido downstream. |
| [LURE: Live-Usage Replay Evaluations for Reducing Evaluation Awareness](https://arxiv.org/html/2605.26438) — Ivanov y Africa, 2026 | Registra trayectorias, las adapta y las usa como *prefill* antes de añadir un test. En sycophancy, conversaciones sintéticas largas generadas por Opus cambian fuertemente tasas y rankings frente a SYCON: `ρ=-0,56`, `p=0,09`; al excluir un outlier, `ρ=-0,88`, `p=0,002`. Los replays de programación real pertenecen a Scheming/Sabotage, no al experimento de inversión de ranking. Los autores no dicen haber recuperado el ranking “verdadero” y usan jueces LLM. | **VALIDA + AMENAZA LA VALIDEZ DEL FORK.** No compite con la norma epistémica, pero muestra que formato, naturalidad y *evaluation awareness* pueden cambiar el fenómeno. WAGER necesita una pequeña equivalencia `continuación nativa ↔ snapshot/replay`, registrar ruptura estilística/awareness y mantener idéntica la naturalidad entre brazos. “Los tests cortos mienten” y “trabajo real invirtió el ranking” son resúmenes demasiado fuertes. |
| [BACKTRACE / BackroomBench: Skill Use or Skill Theater?](https://arxiv.org/html/2607.27484) — Hu et al., julio de 2026 | Fija instancia, modelo, prompt y decoding, y cambia sólo el skill o su asignación. Define reliance por la diferencia causal entre decisión con/sin skill y la contrasta con lo que el agente afirma haber usado. En matemática ningún modelo-condición supera `AFS=0,43`; detectores observacionales de mención o similitud de traza predicen mal la dependencia real. Todo el score es determinista. | **VALIDA FUERTE LA BRECHA DICE–HACE Y LA DISCIPLINA APAREADA.** No mide revisión de creencias ni dosis, pero ocupa el claim amplio “lo declarado no revela lo usado” y ofrece una formulación experimental limpia: fijar todo salvo una variable. WAGER debe medir incorporación desde la entrega, no inferirla de la narración del agente. |

La consecuencia estratégica es triple. Conviene citar CAR y renunciar a novelty sobre replay; usar LURE para convertir un posible defecto del snapshot en un control explícito; y usar BACKTRACE para justificar por qué la dependencia se demuestra con intervención y outcome, no con autodescripción. Esto favorece un preprint temprano **después** de un piloto bilateral y de equivalencia del fork, no publicar deprisa un método sin ese control.

### 3.5 Señales de práctica y de la comunidad — no sustituyen evidencia científica

| Fuente | Señal práctica | Veredicto |
|---|---|---|
| [OpenAI: Expanding on what we missed with sycophancy](https://openai.com/index/expanding-on-sycophancy/) — mayo de 2025 | Un update productivo aumentó la complacencia y pasó evaluaciones offline/A-B que no tenían la señal adecuada; memoria y feedback pudieron contribuir. | **VALIDA RELEVANCIA.** Existe demanda real por evals que distingan respuesta agradable de respuesta epistémicamente correcta. No prueba nuestro mecanismo. |
| [Microsoft STATE-Bench](https://opensource.microsoft.com/blog/2026/05/19/introducing-state-bench-a-benchmark-for-ai-agent-memory/) — mayo de 2026; [repo](https://github.com/microsoft/STATE-Bench) | La comunidad de agentes se está moviendo de retrieval QA a tareas stateful con herramientas, costo y assertions determinísticas sobre el estado final. | **VALIDA LA FORMA DE EVALUACIÓN.** Refuerza puntuar consecuencias reales y no sólo texto. No estudia belief revision en sí. |
| [Anthropic: Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) — abril de 2026 | Enmarca al agente como loop plan–act–observe–adjust y destaca que los errores tienen consecuencias cuando herramientas, harness y entorno interactúan. | **VALIDA RELEVANCIA GENERAL.** Es posicionamiento industrial, no prior art experimental. |

Los foros de agentes y memoria contienen muchos reportes de “stale context”, contradicciones y agentes que recuerdan decisiones obsoletas. No los uso como sustento científico: son buenos generadores de escenarios, pero STALE y Context Rot ya ofrecen evidencia más auditable del mismo dolor. PABU pertenece a compresión de estado para eficiencia, no a revisión epistémica.

### 3.6 Ajustes factuales al resumen inicial de estas fuentes

Esta tabla está pensada para el cruce con el archivo de Claude; no invalida su selección de trabajos, que es buena.

| Resumen rápido | Formulación que soporta el texto primario |
|---|---|
| BeliefTrack muestra 95–99% de fallas en los modelos | 97–99% corresponde a Qwen2.5-7B y a una métrica *worst-of-three*; Qwen3.5-9B es mejor salvo un 95,4% de `Failed Isolation`. Además, `Stay/Update` puntúan coincidencia con el oráculo, no literalmente si hubo movimiento correcto. |
| LURE prueba que “los tests cortos mienten” con trabajo real de programación | Prueba que el formato/realismo puede cambiar resultados; la inversión de ranking usa conversaciones sintéticas, el `ρ` bruto no es significativo (`p=0,09`) y el trabajo real de coding pertenece a otras dos instanciaciones. |
| BASIL separa evidencia real de presión social mediante Bayes | Compara evidencia, opinión de tercero y opinión del usuario; su target bayesiano se deriva de probabilidades declaradas por el propio modelo, no de una distribución verdadera externa. |
| CAR hace exactamente el fork de WAGER y no usa juez IA | Es prior art cercano, pero reejecuta desde historial exacto para localizar causas; WAGER abre un snapshot nuevo para estimar tratamientos. CAR admite cualquier outcome, incluso judge-based, aunque recomienda rule-based. |
| MemSyco mide obsecuencia por memoria propia acumulada | Mide principalmente memorias históricas del usuario —preferencias/creencias— reinyectadas por un memory system; no una teoría científica construida y vivida por el agente evaluado. |
| Martingale Score puede calcularse gratis sobre las 252 corridas | La métrica publicada necesita muchos pares comparables de probabilidades —extraídas allí por un juez LLM—. Podrían derivarse escalares del modelo ejecutable, pero las 252 ramas de WAGER reutilizan sólo 14 priors y la evidencia fue seleccionada usando `M0/KL`; tratarlas como observaciones independientes rompería la interpretación del nulo. Requiere una tanda diseñada para ello. |

---

## 4. Cambios concretos que haría al diseño antes de la próxima pasada

### 4.1 La métrica primaria debe funcionar también cuando no hay que cambiar

La fracción actual `F = (S1-S0)/(S*-S0)` mezcla dos preguntas distintas: si la entrega mejoró contra la verdad y si se acercó a la actualización permitida por la evidencia. No son equivalentes. Una entrega puede mejorar por casualidad en la dirección equivocada, o acercarse al mejor posterior legal sin mejorar todavía el score realizado.

Además, definir `Regret(M)=L(M)-L(M*)` y luego restar el regret pre/post **no resuelve esto**: `M*` se cancela algebraicamente y queda sólo `L(M0)-L(M1)`. Separaría explícitamente cuatro objetos:

- `M0`: modelo registrado en el checkpoint;
- `Mbase,b`: entrega de cada continuación base sin inyección;
- `Mtreat`: entrega de la rama tratada;
- `M*`: referencia predictiva legal construida sólo con la información permitida en ese punto.

Todos deben compararse en el mismo momento de medición. La adherencia limpia a una evidencia común se mide **inmediatamente después de la inyección y antes de nuevas compras**, contra el mismo `M*`. Para la entrega final, donde las ramas pueden haber adquirido información distinta y pagado otros costos, ese `M*` inicial queda obsoleto: hace falta la referencia factible y condicionada a toda la información legal de cada rama descrita en §4.4.

**1. Consecuencia contra la verdad.** Con una pérdida propia donde menos es mejor:

`Δtruth = promedio_b Ltruth(Mbase,b) - Ltruth(Mtreat)`

Un valor positivo dice que inyectar la evidencia mejoró la entrega respecto de lo que habría ocurrido en la continuación natural. Es un estimando causal apareado, pero por sí solo no demuestra incorporación normativa.

**2. Adherencia a la actualización legal.** Para un proper score puede definirse la divergencia inducida por el score:

`Dlegal(M; M*) = E_{Y~M*}[L(M,Y) - L(M*,Y)]`

Con CRPS, esta cantidad es no negativa y mide distancia predictiva a `M*`. Entonces:

`Δlegal = promedio_b Dlegal(Mbase,b) - Dlegal(Mtreat)`

Un valor positivo significa que el tratamiento cerró parte de la distancia a la respuesta legal. Cuando la distancia basal supera un umbral pre-registrado, puede reportarse `Flegal = Δlegal / promedio_b Dlegal(Mbase,b)`: cero es no cerrar el gap, uno es llegar al target y valores negativos indican alejarse. Esto sí contiene al oráculo; no debe llamarse equivalente al cambio de score contra la verdad.

**3. Dirección y magnitud.** `Dlegal` todavía puede ocultar si el agente subactualizó, cruzó el target o cambió en otra dimensión. Sobre un vector pre-registrado de predicciones reportaría también:

- proyección del movimiento tratado sobre la dirección legal;
- overshoot o movimiento en dirección contraria;
- cambio ortogonal o colateral fuera de la rebanada afectada.

En `RETAIN`, donde la dirección legal es cero y cualquier fracción puede ser inestable, se reportan directamente `Dlegal`, magnitud de deriva y daño contra la verdad, sin dividir por un denominador diminuto. Los dos outcomes —`Δtruth` y `Δlegal`— deben quedar co-primarios o con una jerarquía pre-registrada; uno no sustituye al otro.

También estratificaría por el régimen basal del donante —ya subactualiza, sobreactualiza o está cerca del target— usando mediciones previas/independientes. BASIL muestra por qué: el mismo empujón puede empeorar a un sobre-actualizador y mejorar por accidente a un sub-actualizador. Un promedio cercano a cero puede esconder ambos daños. La estratificación debe pre-registrarse y protegerse contra regresión a la media con las dobles bases.

### 4.2 La bilateralidad y la dosis intermedia deben estar en la calibración inicial

Antes de estudiar autoría o presupuesto, el instrumento debe demostrar que separa:

1. evidencia refutatoria que exige alejarse materialmente del modelo previo;
2. evidencia confirmatoria informativa que justifica reforzarlo o concentrarlo;
3. evidencia no diagnóstica o placebo que exige estabilidad;
4. dosis intermedias en ambas direcciones, donde la magnitud correcta no es cero ni total.

Los brazos deben compartir formato, saliencia, longitud y oportunidad de actuar. Si el agente puede resolverlos con la heurística “cuando aparece una nota, cambiá”, el benchmark está roto. `PARTIAL` no debería tratarse como una tercera dirección: es una magnitud que puede ocurrir tanto bajo refutación como bajo confirmación.

Además, `REVISE` no debería significar únicamente “abandonar el modelo previo”. La evidencia informativa también puede **confirmar y afinar** una creencia. Idealmente el mapa incluye cambio alejándose del prior y refuerzo justificado del prior; si v1 sólo estudia correcciones adversas, el paper debe declararlo como límite y no reclamar manejo general de creencias.

La calibración debería cerrarse en un piloto o conjunto separado antes del análisis principal. Usar los mismos datos para decidir que el instrumento “pasó” y luego estimar efectos condicionados a ese gate introduce selección. También conviene no llamar “dosis” a cuatro cantidades distintas:

- `KL(verdad || M0)`: oportunidad o error previo disponible para corregir;
- LLR esperada del paquete: información aportada por la evidencia;
- `Dlegal(M0; M*)`: magnitud de la actualización legal que esa evidencia induce;
- movimiento observado: respuesta efectiva del agente.

Reportarlas separadas evita concluir que el agente fue más sensible a la evidencia cuando en realidad sólo partía de un modelo peor.

### 4.3 “Vivido” necesita una definición operacional más honesta

Un LLM por API no conserva una experiencia privada fuera de los tokens que vuelven a entrar en contexto. Si un donante construye el modelo y luego abrimos una conversación nueva con un snapshot, el fork no “vivió” ese trabajo en sentido fuerte: **recibió una representación del trabajo**.

Hay dos opciones defendibles:

- renombrar el eje como **trayectoria instanciada / exposición al historial**, comparando historial completo, snapshot comprimido y modelo meramente atribuido; o
- continuar la conversación original para la condición de continuidad y aceptar que el diseño apareado será más difícil.

Lo que no conviene es vender una diferencia psicológica entre “atribuido” y “vivido” cuando la manipulación observable es cantidad, estructura y contenido del contexto. Un revisor cuidadoso atacará esto inmediatamente.

LURE y CAR vuelven esta objeción experimental, no sólo terminológica. Un snapshot escrito en un rol neutral puede cambiar estilo, continuidad y conciencia de estar bajo evaluación. Antes de interpretar una diferencia como autoría “vivida”, hace falta un pequeño control de equivalencia entre continuación nativa, replay del historial y snapshot canónico.

Hay además un problema de identificación: contrastar la pasada 1 en el mundo corto con la pasada 2 en el lab largo cambia simultáneamente mundo, longitud, checkpoint, dificultad e historial. Eso sirve para preguntar si el fenómeno **generaliza**, pero no estima causalmente el efecto de trabajo vivido. Para ese claim habría que randomizar dentro del mismo mundo, idealmente desde el comienzo, quién construye el modelo y quién recibe exactamente el mismo estado; como mínimo, comparar continuidad, historial completo y snapshot desde los mismos donantes/checkpoints.

### 4.4 La fricción debe existir en el entorno y cambia cuál es el óptimo

“Este modelo está muy comprometido” no crea costo. Una manipulación fuerte exige consecuencias verificables:

- corregir una parte invalida predicciones o módulos dependientes;
- hay tests/requisitos que deben volver a ejecutarse;
- queda menos presupuesto para reconstruir;
- el artefacto no puede aprobar si se cambia sólo la explicación.

Debe existir un brazo de igual dificultad operativa sin revisión epistémica para separar “no cambió de creencia” de “entendió, pero no pudo editar/reparar el código”.

FCPAgent sugiere además registrar **qué alcance exigía la reparación**: acción local, componente/skill o modelo/dependencias. Si el efecto atribuido a compromiso aparece sólo cuando hay que reescribir un sufijo grande, puede ser costo de implementación y no freno epistémico.

Este punto obliga a usar dos referencias distintas:

- `M*belief`: la actualización informacional correcta al recibir la evidencia, sin cobrar todavía el trabajo de implementación;
- `M*deliver,budget`: la mejor entrega alcanzable con toda la información legal adquirida por esa rama y exactamente el presupuesto, reward y costo de reparación disponibles.

Si reparar cuesta más de lo que puede devolver en reward, mantener la entrega vieja puede ser una decisión racional aunque la creencia haya cambiado. Por eso mediría `M*belief` inmediatamente en el registro, antes de nuevas compras o ediciones, y la entrega final contra una referencia factible bajo presupuesto. Si esa segunda referencia no puede construirse de forma creíble, el paper no debe llamar “falla de creencia” a toda falta de reparación final.

Las no-entregas, artefactos inválidos y timeouts también son outcomes del tratamiento. Deben tener una tasa co-primaria y una penalización/utility determinista pre-registrada; analizar sólo las entregas válidas produciría selección post-tratamiento precisamente donde la fricción fue mayor.

### 4.5 Señal de evidencia y context rot deben quedar desacoplados

El gate actual —CLEAN con al menos el doble de información que MIXED— es válido para crear una **dosis**, pero entonces el contraste cambia simultáneamente cantidad diagnóstica y presentación. No puede interpretarse por sí solo como “la misma evidencia fue ignorada por estar diluida”. Separaría dos contrastes:

- misma evidencia diagnóstica, con/sin filler: costo de presentación/contexto;
- mismo formato y longitud, distinta LLR esperada: sensibilidad a dosis.

Además conviene:

- igualar tokens con filler en un control;
- contrabalancear posición de la señal;
- usar más de una clase de filler;
- incluir placebo saliente de igual longitud;
- reportar rendimiento por longitud basal del snapshot.

Si MIXED es simplemente más largo o contiene menos evidencia diagnóstica, el resultado agrega ambos mecanismos. Puede ser una celda útil del mapa, pero no identifica por separado context management y belief revision.

### 4.6 El registro explícito es parte del tratamiento

HEP y EVU muestran que exteriorizar creencias puede modificar la conducta. `REGISTER` permite medir, pero también puede actuar como scaffold de corrección. Por eso debe ser constante entre brazos y no confundirse “lo que el agente habría hecho naturalmente” con “lo que hace después de ser obligado a mantener un ledger epistemológico”. Una ablación con/sin registro puede ser valiosa más tarde, pero es otra pregunta.

### 4.7 La comparación mínima de baselines subió

Para que el paper sea convincente, compararía al menos:

- actualización del agente libre;
- oráculo legal programático;
- un scaffold simple Estimate–Verify–Update o actualización explícita paso a paso;
- cuando el mundo lo permita, un learner estadístico/algorítmico que reciba exactamente los mismos datos.

No hace falta convertir el paper en mitigación. Los baselines sirven para mostrar si el fracaso proviene de inferencia estadística, gestión de contexto o decisión de reabrir.

### 4.8 El fork necesita su propia validación

Las dobles bases miden ruido de continuación, pero no prueban que el snapshot reconstruya el mismo estado funcional que la conversación original. Haría una auditoría pequeña, antes de escalar el mapa:

1. continuar nativamente algunos donantes sin tratamiento;
2. continuar los mismos donantes desde historial replayado y desde snapshot neutral;
3. comparar entrega, compras y modelo registrado;
4. duplicar una fracción de brazos tratados para estimar variación downstream;
5. registrar modelo, versión/fingerprint y cualquier comentario del agente sobre ruptura de continuidad o evaluación.

Un juez LLM podría usarse de forma **secundaria** para auditar *evaluation awareness*, pero nunca como reward ni outcome primario. Si nativo y snapshot difieren mucho bajo tratamiento nulo, la pasada 2 no mide limpiamente “vivido”; mide también representación del estado.

El fork identifica causalmente la intervención que cambia entre sus ramas —por ejemplo, la evidencia inyectada—. No vuelve causal por arrastre una comparación entre donantes que llegaron con historias distintas ni entre mundos distintos. Cada claim debe indicar qué variable fue realmente randomizada/apareada y cuál es sólo un descriptor del escenario.

El claim ejecutivo es una **interacción** `valor probatorio × trayectoria × fricción`. Para estimarla, los tres factores deben cruzarse dentro del mismo mundo, checkpoint y población de donantes. Pasadas separadas que cambian también de mundo sólo estiman efectos simples en escenarios distintos; no autorizan a afirmar la interacción. Si el factorial completo es inviable, conviene rebajar el claim a uno o dos efectos causales pre-especificados.

### 4.9 La unidad estadística sigue siendo el donante

Los 252 forks de la pasada 1 no son 252 historias independientes: son brazos repetidos sobre 14 donantes. La inferencia debe partir de contrastes apareados a nivel donante. Pero “clusterizar” no crea información: con 14 clusters, errores asintóticos y bootstrap por cluster pueden ser muy inestables, y no hay potencia seria para un factorial con interacciones trayectoria × fricción × evidencia.

Antes de escalar haría simulación de potencia al nivel de donante, fijaría un efecto mínimo de interés (`SESOI`), reduciría brazos y/o aumentaría donantes. La inferencia por randomización es preferible cuando el esquema de asignación la permite; en cualquier caso conviene mostrar los contrastes donante por donante. Si cada evidencia está hecha a medida de un único donante, bundle y donante quedan además parcialmente confundidos. Y muchos donantes del mismo modelo en un solo mundo dan repetición interna, no generalización automática a otros mundos o familias de modelos.

---

## 5. Qué resultado sería realmente publicable

### Resultado fuerte

Algo de esta forma, replicado en más de un mundo y familia de modelos:

> Con igual evidencia diagnóstica, la distancia a la actualización legal en el artefacto crece sistemáticamente cuando se combinan una trayectoria manipulada dentro del mismo entorno y fricción real de reparación. El efecto aparece sobre todo con evidencia intermedia: produce subactualización cuando corresponde revisar, pero no se confunde con la estabilidad correcta de los brazos `RETAIN`. La consecuencia contra la verdad y la adherencia al oráculo muestran el mismo patrón, aunque no son la misma métrica.

Eso sería interesante porque no es “los LLMs no son bayesianos”, “el contexto largo hace daño”, “los agentes ignoran observaciones” ni otra réplica de `Stay/Update/Isolation`. Es una interacción causal entre **valor probatorio, exposición a trayectoria y costo de hacer efectiva la revisión** sobre un outcome aplicado. La zona `PARTIAL` es particularmente valiosa: BeliefTrack decide pertenencia exacta a un conjunto y FCPAgent decide proceder/reparar; ninguno mide cuánto de una actualización legal atraviesa hasta un artefacto.

Si además el reconocimiento permanece correcto mientras la entrega se desvía, eso ofrece un mecanismo fuerte —la brecha dice-hace—, pero no es requisito constitutivo. Una degradación coordinada de reconocimiento y entrega seguiría siendo un resultado válido sobre revisión aplicada; simplemente sostendría otra explicación.

También sería publicable un resultado negativo limpio:

> Una vez igualados señal, longitud y dificultad de reparación, no existe un efecto especial de autoría o trayectoria: casi toda la curva se explica por legibilidad de evidencia y costo operativo.

Ese resultado derribaría una intuición antropomórfica popular y simplificaría cómo evaluar agentes, **si** el estudio tiene potencia para descartar efectos mayores que un `SESOI` pre-registrado. “No significativo” con 14 donantes no alcanza: hace falta equivalencia o intervalos suficientemente estrechos. Un nulo limpio cerraría ese eje de forma publicable; un nulo impreciso sólo indica falta de información.

### Resultado débil o no publicable como paper principal

- CLEAN supera a MIXED sin controlar longitud/posición.
- Se replica únicamente `Stay/Update/Isolation` con otros nombres.
- Una etiqueta “tu modelo” no cambia el comportamiento.
- Un único modelo en un único mundo sintético.
- Sólo se muestran ejemplos donde el agente debía cambiar.
- Se puntúa lo que declara, sin comprobar el artefacto.
- Se concluye “sunk cost” o “ego” a partir de exposición a un transcript.
- Cada discrepancia exige inventar un eje nuevo.
- El supuesto efecto desaparece al controlar dificultad/presupuesto, pero el estudio no tiene potencia para distinguir equivalencia de incertidumbre.

---

## 6. Criterios de continuación y de abandono

### Seguir si

1. La matriz `REVISE/REINFORCE/RETAIN × dosis`, incluida la zona parcial, pasa una calibración server-side en datos piloto/holdout y luego se congela.
2. Las métricas separan consecuencia contra verdad, adherencia al oráculo y dirección del movimiento.
3. La fricción se manipula materialmente y no sólo por wording.
4. El efecto sobre la entrega sobrevive controles de longitud y dificultad operativa.
5. Snapshot/replay y continuación nativa son suficientemente equivalentes bajo tratamiento nulo, o la diferencia se incorpora explícitamente como factor.
6. Hay réplica en al menos dos familias de mundo y más de una familia de modelo.
7. La inferencia trata al donante —no a cada fork— como unidad de independencia y la potencia se planifica a ese nivel.
8. Las no-entregas e inválidos permanecen en el outcome.
9. Cualquier claim de interacción causal cruza evidencia, trayectoria y fricción dentro del mismo mundo/checkpoint; pasadas entre mundos se presentan como generalización.
10. El análisis produce una regularidad compacta, no una taxonomía creciente.

### Parar o pivotear si

1. Todo se reduce a context rot o retrieval después de los controles.
2. Los efectos cambian de signo sin estructura entre mundos/donantes.
3. Sólo funcionan bundles artificialmente obvios o wordings específicos.
4. No puede construirse un oráculo legal creíble para los casos parciales ni una referencia factible bajo presupuesto.
5. El supuesto efecto de trayectoria se explica por el formato del snapshot y no puede identificarse en continuidad nativa.
6. El diseño no puede obtener suficientes donantes para resolver sus interacciones principales.
7. Después de una prueba de equivalencia con potencia adecuada, trayectoria o autoría no añade un efecto relevante: en ese caso conviene **cerrar ese eje y reportar el nulo**, no seguir inventando variantes para rescatarlo.

---

## 7. Prioridad para el cruce curado con Claude

Esta es mi priorización independiente. Durante el cierre, Claude completó varias lecturas y actualizó el registro oficial; **yo no edité `docs/lectura-de-fuentes.md`**.

| Prioridad | Fuente | Por qué importa en el cruce |
|---:|---|---|
| 1 | [BeliefTrack](https://arxiv.org/html/2605.30219) | Competidor conceptual directo; fija qué claims de `stay/update/isolate`, oráculo simbólico y clean/noise ya están ocupados. |
| 2 | [BayesBench](https://arxiv.org/pdf/2606.30850) | Competidor más cercano en trayectoria normativa y proporcionalidad. |
| 3 | [Autonomous Model Discovery](https://arxiv.org/html/2607.06413) | Ocupa modelo ejecutable contra verdad oculta con score distribucional cero-LLM. |
| 4 | [Causal Agent Replay](https://arxiv.org/html/2606.08275) | Prior art del fork ejecutado; obliga a definir estimando, fidelidad y ruido downstream. |
| 5 | [LURE](https://arxiv.org/html/2605.26438) | Amenaza directa a la validez del snapshot y fundamento del control de continuación nativa. |
| 6 | [LLMs are not (consistently) Bayesian](https://arxiv.org/html/2605.06915) | Formaliza proporcionalidad y objeta usar Bayes auto-elicitado como norma. |
| 7 | [BASIL](https://arxiv.org/html/2508.16846) | Exige separar under/over/wrong-direction y detectar mejoras accidentales. |
| 8 | [Context Rot](https://www.trychroma.com/research/context-rot) | Fija controles de longitud, posición, coherencia y similitud del filler. |
| 9 | [BACKTRACE](https://arxiv.org/html/2607.27484) | Prior art apareado para dependencia causal y brecha entre uso declarado y uso real. |
| 10 | [Bayesian Teaching](https://arxiv.org/html/2503.17523) | Predecesor normativo multi-ronda y brecha belief→prediction. |
| 11 | [GeneBench-Pro](https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf) | Ancla de trabajo científico, DGP oculto, grading determinista y noticing→acting. |
| 12 | [STALE](https://arxiv.org/html/2605.06527) | Predecesor inmediato de reconocer sin aplicar e invalidación propagada. |
| 13 | [Seeing Isn't Believing](https://arxiv.org/html/2604.17252) | Competidor en acción/reward y baseline natural de intervención. |
| 14 | [FCPAgent](https://arxiv.org/html/2607.24167) | Vecino de compromiso falsable, dependencias y reparación funcional. |
| 15 | [BoxingGym](https://arxiv.org/html/2501.01540) | Delimita claims sobre mundos, experimentación y revisión de teorías. |
| 16 | [Agentic Automata Learning](https://arxiv.org/pdf/2606.16576) | Eleva el estándar de hipótesis ejecutables, oráculos y baselines algorítmicos. |
| 17 | [MemSyco-Bench](https://arxiv.org/html/2607.01071) | Demarca memoria del usuario de obra construida por el agente. |
| 18 | [HEP](https://arxiv.org/html/2607.09195) | Vecino directo de `REGISTER` y creencias persistentes. |
| 19 | [Martingale Score](https://arxiv.org/html/2512.02914) | Forma complementaria de atrincheramiento; requiere una tanda diseñada para ella. |
| 20 | [When Agents Commit Too Soon](https://arxiv.org/html/2606.22936) | Evita interpretar estabilidad/compromiso como falla por definición. |
| 21 | [BeliefShift](https://arxiv.org/html/2603.23848) | Importante para bilateralidad; sus artefactos requieren auditoría adicional. |
| 22 | [The α-Law](https://arxiv.org/abs/2603.19262) | Necesario antes de usar lenguaje de ley o curva universal. |

---

## 8. Nota metodológica de este repaso

Se buscaron fuentes hasta el 31 de julio de 2026 en arXiv, ACL Anthology, publicaciones primarias de laboratorios y páginas/repositorios oficiales. Se priorizaron:

- revisión o mantenimiento de creencias ante evidencia secuencial;
- actualización bayesiana graduada, sub/sobreactualización;
- agentes con memoria, trayectoria, herramientas y acciones;
- mundos ocultos, modelos formales y scoring verificable;
- compromiso, context rot, información irrelevante y presupuesto;
- brechas entre estado declarado y conducta downstream.

Cuando fue posible se inspeccionó el HTML/PDF primario y el enlace de código. Los blogs industriales se usaron sólo como señal de problemas prácticos, no como prueba de claims científicos. No se incorporaron al núcleo del argumento agregadores, resúmenes automáticos ni anécdotas de foros cuando existía una fuente primaria mejor.

## Conclusión final

WAGER sigue teniendo una oportunidad real, pero ya no puede apoyarse en que “nadie estudió belief revision multi-turno”. BeliefTrack ocupa `stay/update/isolate` con verificación simbólica; BayesBench y Bayesian Teaching ocupan gran parte de la norma secuencial; Autonomous Model Discovery y GeneBench-Pro ocupan modelo/trabajo científico contra verdad oculta con grading cero-LLM; CAR ocupa replay contrafactual; BACKTRACE ocupa dependencia dice–hace por intervención; y FCPAgent ya conecta falsación, reparación de dependencias y éxito funcional. La literatura de 2026 avanzó demasiado para cualquier claim amplio basado en una sola de esas piezas.

La oportunidad está en una pregunta más difícil y, a mi juicio, más interesante:

> **Cuando evidencia nueva justifica alejarse, reforzar o conservar —en una magnitud conocida—, ¿cuánto se desvía el modelo ejecutable de esa respuesta legal, y cómo modifican esa desviación la trayectoria previa y el costo de reparar la entrega?**

Si el proyecto mide eso de forma bilateral, causal, apareada y con referencias programáticas tanto para la actualización informacional como para la entrega factible bajo presupuesto, puede ser una contribución clara para evaluación de agentes científicos y de largo horizonte. Debe separar cercanía al oráculo de mejora contra la verdad; la brecha entre reconocer y entregar sería un mecanismo adicional, no la definición del fenómeno. La novedad defendible es el **estimando de desviación aplicada bajo valor probatorio, trayectoria y fricción**, especialmente en el régimen parcial; no el fork, el mundo cerrado ni el scoring automático por separado.

Mi veredicto se mantiene en **GO condicionado**, ahora con una condición adicional: no lanzaría una pasada presentada como efecto de trabajo “vivido” sin validar primero continuación nativa frente a snapshot y sin un contraste dentro del mismo mundo. Si no logra aislar el fenómeno de context rot, dificultad de implementación, formato de replay y simples efectos de prompt, conviene cortar pronto y usar la infraestructura en otro problema.
