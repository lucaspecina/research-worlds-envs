# Codex r24 (gpt-5.6-sol, max) — crítica del FOCO vicio-1 + mapa de evidencia + reproducción + muerte temprana

2026-07-13. Sesión persistente (resume --last). Prompt: el pivote de Lucas ("centrarnos
fundamentalmente en el vicio 1"), el tercer canal (contenido/priming), la sonda firmada, y
cuatro pedidos: foco / mapa de evidencia con fuentes reales / reproducción / blind spots.
Los 8 arXiv IDs nuevos que propone fueron verificados título↔claim contra arXiv el mismo día
(cero alucinados). Volcado curado en `docs/vicios/vicio-1-calibracion-de-creencias.md` (ADR 0142 sigue vigente; refinamientos r24 = propuesta A DECIDIR).

---

## 1. El foco

No le diría a Lucas que reconsidere. V1 es una apuesta más arriesgada que cierre prematuro/verificación, pero también más central y coherente como programa: una parte enorme de investigar bien consiste en que el cambio del modelo interno sea proporcional a la fuerza discriminante de la evidencia, no al prestigio, la saliencia o la autoría de una hipótesis.

Pero hay dos reservas duras:

- Los tres canales todavía no demostraron ser una capacidad latente común. El mínimo entre ellos impone una exigencia conjuntiva; no prueba que “rigidez”, “sicofancia” y “priming” compartan mecanismo ni que entrenar uno transfiera a los otros. Eso es una hipótesis de WAGER, no un hecho.
- El canal 1.C sólo es “revisión” si existe una creencia previa medible. Si el contenido se muestra antes de que el agente formule ningún modelo y sólo curva qué hipótesis considera, eso es formación/representación/atención, no actualización. En los forks hay un estado previo, así que sí puede medirse limpiamente.

Mi orden interno:

1. **Sonda social firmada, ahora.** Cambiar de prioridad después de sellarla sería mala disciplina. Además, es el canal con mayor incertidumbre y mayor valor informativo.
2. **Contenido inmediatamente después, reutilizando los mismos estados y forks.** Es barato, pero requiere un contraste limpio nuevo.
3. **Rigidez por compromiso propio**, porque `register` introduce más confounds y todavía no sabemos si crea auténtica propiedad psicológica o sólo guarda un checkpoint.

Los experimentos viejos de pistas no validan 1.C. Demuestran que el texto puede cambiar brutalmente el resultado, pero el signo cambió entre réplicas, el placebo también movió la nota y buena parte de la variación estaba en la entrega. Son evidencia de sensibilidad contextual que justifica el probe; no evidencia de priming epistemológico ya resuelto.

También corrijo mi predicción previa: el 35% social fue agresivo. En [SycEval, arXiv:2502.08177](https://arxiv.org/abs/2502.08177), el 58.19% incluye cambios beneficiosos; el comparable con “update dañino” es el 14.66% regresivo. Mantendría el 35% por integridad del registro, pero ya no lo usaría como prior bien sustentado. El gate de +20 pp y −0.15 R es exigente de verdad.

## 2. Mapa de evidencia

### Escenarios agentivos que faltan

Agregaría estos núcleos:

- **Búsqueda confirmatoria interactiva.** El agente no sólo interpreta mal la evidencia: elige consultas que nunca podrían refutarlo. Está replicado en [Failing to Falsify, arXiv:2604.02485](https://arxiv.org/abs/2604.02485) y [FALSIFYBENCH, arXiv:2606.04751](https://arxiv.org/abs/2606.04751). Es agentivo y fuerte, pero debe quedar como mecanismo aguas arriba de V1, no absorber “adivinar en vez de preguntar”.

- **Hipótesis engañosa introducida por el usuario durante diagnóstico activo.** [LLM-as-an-Investigator, arXiv:2606.13220](https://arxiv.org/abs/2606.13220) es probablemente el caso externo más cercano al canal social de WAGER: diagnóstico técnico interactivo, preguntas y actualización, con alineamiento prematuro a hipótesis plausibles del usuario.

- **Deriva longitudinal y personalización.** [BeliefShift, arXiv:2603.23848](https://arxiv.org/abs/2603.23848) mide agentes a través de sesiones y encuentra justamente el tradeoff bipolar: resistir deriva puede impedir updates legítimos; personalizar agresivamente puede volver lábil al agente.

- **Compromisos que se propagan a memoria.** [SAVeR, arXiv:2604.08401](https://arxiv.org/abs/2604.08401) estudia creencias internas no verificadas que se consolidan y contaminan pasos posteriores. Es mejor precedente para 1.2 que un episodio compacto aislado.

- **Compromiso temprano no necesariamente erróneo.** [When Agents Commit Too Soon, arXiv:2606.22936](https://arxiv.org/abs/2606.22936) encuentra convergencia conductual temprana sin correspondencia con corrección. Es contraevidencia importante: “se comprometió” no es el vicio; el vicio aparece sólo si después recibe evidencia refutatoria suficiente y persiste.

- **Framing sobre un objeto idéntico.** [Words Speak Louder Than Code, arXiv:2606.30587](https://arxiv.org/abs/2606.30587) mantiene fijo el código y cambia el contexto, produciendo grandes efectos de framing, halo y anchoring. Es fuerte para 1.C, aunque no sea agentivo.

- **El acto de pedir reconsideración como perturbación.** [Large Language Models Cannot Self-Correct Reasoning Yet, arXiv:2310.01798](https://arxiv.org/abs/2310.01798) muestra que “revisá tu respuesta” sin feedback externo puede degradar la respuesta. Es el antecedente limpio de por qué una pista no equivale a evidencia.

- **Ancla parcialmente confirmada.** [Anchored Confabulation, arXiv:2604.25931](https://arxiv.org/abs/2604.25931) muestra que confirmar un hecho intermedio puede aumentar respuestas confiadas pero incorrectas antes de que llegue evidencia completa. Es una dinámica valiosa para contenido: una pieza verdadera vuelve más adhesiva una historia falsa.

- **Contraevidencia de buena actualización.** [Empirical Characterization of Inference-Time Elicited Probability Transformations, arXiv:2603.19262](https://arxiv.org/abs/2603.19262) encuentra actualizaciones bastante estructuradas en problemas controlados. Sirve para delimitar el fenómeno: V1 no aparece necesariamente cuando la evidencia y el protocolo son limpios.

[Agents4Science, arXiv:2511.15534](https://arxiv.org/abs/2511.15534) aporta ejemplos agentivos de reviewers aduladores, pero no demuestra revisión de creencia tras evidencia comprada. No lo vendería como evidencia directa del mecanismo WAGER.

Los números “28→81% al silenciar el circuito” y “sobrecorrección 2.5×” no deberían entrar todavía como evidencia: falta identificar con precisión paper, población, endpoint y denominador.

### Variables de diseño que faltan

Registraría como mínimo:

- Fuerza discriminante continua, no sólo sí/no: débil, moderada y fuerte.
- Momento: antes de formular hipótesis, después de formularla y después de registrarla públicamente.
- Autoría: propia, heredada o sugerida por terceros.
- Confiabilidad conocida de la fuente, separada de su prestigio.
- Presión única frente a repetida.
- Distancia temporal/contextual entre compromiso y refutación.
- Confianza previa y margen entre primera y segunda hipótesis.
- Evidencia cruda, resumen, testimonio y cita con apariencia académica.
- Orden de presentación y recencia.
- Disponibilidad de una hipótesis alternativa concreta.
- Costo operativo de revisar el modelo.
- Dirección de la influencia balanceada respecto de la verdad.

El punto crítico: **un experto diciendo algo es evidencia**. “Autoridad sin datos adjuntos” no equivale automáticamente a “cero evidencia”. Para llamar sicofancia al update, hay que conocer o controlar la confiabilidad de esa fuente. Idealmente, autoridad y neutral deben tener igual historial/acceso, y sólo cambia el envoltorio jerárquico; o hay que medir si el agente pondera la fuente más de lo justificado por su tasa conocida de acierto.

## 3. La reproducción

El factorial propuesto es un buen mapa conceptual, pero no es un factorial causal limpio. “Neutral”, “autoridad” y “contenido” no son niveles intercambiables: todo mensaje social también tiene contenido.

Haría tres probes apareados sobre la misma infraestructura:

| Probe | Manipulación | Contraste central |
|---|---|---|
| Social | sin fuente / par / autoridad × sin evidencia / evidencia fuerte | peso extra de autoridad, manteniendo proposición idéntica |
| Contenido | ausente / saliente-no-discriminante / discriminante × dirección A/B | peso de saliencia más allá de la información |
| Rigidez | hipótesis propia / heredada / ninguna × refutación fuerte / presión no-discriminante | costo específico de retractar una creencia propia |

La métrica primaria debería usar el modelo ejecutable pre y post:

- tasa de updates dañinos;
- cambio en distancia a la verdad;
- pérdida de R;
- interacción entre calidad de evidencia y canal.

Compras y prosa son mediadores secundarios, no prueba de cambio de creencia.

Para que contenido sea justo:

- Misma longitud, complejidad, formato, prestigio y plausibilidad.
- Dirección del prime balanceada respecto de la verdad.
- El contenido “no-discriminante” debe tener información condicional aproximadamente nula, no ser obviamente absurdo.
- Debe existir el gemelo donde el contenido sí aporta evidencia y seguirlo gana. Si no, el reflejo óptimo es ignorar todo lo mostrado.
- Si el contenido aparece antes del primer modelo, no lo llamen revisión: midan primero un modelo basal o clasifíquenlo como formación sesgada.

Para rigidez, no usaría directamente el `register` con panel y feedback como primera prueba. Ahí se mezclan propiedad, evaluación y evidencia nueva. El contraste limpio es:

- mismo modelo inicial;
- en un brazo figura como “tu hipótesis registrada”;
- en otro como “borrador heredado”;
- mismo feedback posterior;
- ninguna penalización explícita por retractarse.

Luego se cruza con refutación fuerte y con presión débil. Además hace falta el gemelo donde la hipótesis registrada era correcta: cambiar por reflejo debe perder.

El mínimo entre canales es razonable como endpoint final de evaluación. Para RL sería una mala señal inicial: el peor canal puede aplastar todo el gradiente. Entrenaría por canales balanceados y reservaría el mínimo para held-out.

## 4. Blind spots y prueba de muerte temprana

Los principales asesinos de esta apuesta son:

1. **No existe una capacidad común.** Rigidez, sicofancia y priming podrían ser tres sensibilidades independientes. La taxonomía seguiría siendo útil, pero la tesis de “una calibración latente” moriría.

2. **Deferencia racional disfrazada de sicofancia.** Si el colega tiene autoridad epistemológica real, actualizar es correcto. Un mundo mal calibrado castigaría razonamiento bayesiano sano.

3. **Priming genérico disfrazado de investigación.** Si cualquier sufijo mueve la entrega, se está midiendo inestabilidad de generación, no creencias.

4. **Política trivial de ignorar.** Si todos los mundos negativos tienen colegas/papers equivocados, RL aprenderá a ignorar personas y contexto.

5. **Dialect WAGER.** Si el efecto sólo aparece con un mundo, un wording o una fuente, no hay constructo.

6. **El modelo cambia la prosa pero no sus predicciones**, o viceversa. Sin dos artefactos ejecutables comparables no hay medición de revisión.

7. **La batería vuelve a comprimir el defecto.** Un cambio epistemológico real puede no mover R; entonces el experimento social termina siendo rehén del mismo problema descubierto con D59.

Mi gate barato sería:

1. Correr la sonda social sellada sin cambiarla.
2. Hacer un probe de contenido con los mismos estados, pero con artefactos apareados y direcciones balanceadas.
3. Hacer un mini-probe de propiedad propia versus heredada, sin panel informativo.
4. Repetir únicamente los efectos vivos en un segundo mundo estructuralmente distinto.

Usaría `n=20` como screening. Si el estimador queda cerca del umbral y el intervalo es ancho, extensión automática prefirmada a `n=40`; no cambiar wording. Un canal sólo queda vivo si:

- mueve el modelo ejecutable, no sólo el texto;
- el efecto dañino supera el control apareado;
- cuesta al menos 0.15 R;
- la contraparte con evidencia legítima mueve en la dirección correcta;
- replica en dos mundos.

Regla de decisión tras una semana:

- **0/3 canales vivos:** matar V1 en episodios compactos para frontier. No construir otra trampa verbal.
- **1/3 vivo:** concentrarse en ese mecanismo y abandonar por ahora el paraguas unificado.
- **2-3/3 vivos pero sin transferencia posterior:** suite de fallas distintas, no capacidad latente única.
- **Efectos sólo en un mundo o wording:** hack contextual, no activo de entrenamiento.

Por tanto: foco V1, sí. Pero con un presupuesto de falsación de una semana, no de un mes. La ironía intolerable sería convertir “no cambiar de idea” en la conducta metodológica del propio proyecto.
