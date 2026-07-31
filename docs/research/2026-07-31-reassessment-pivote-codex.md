# Reevaluación independiente de WAGER y propuesta de refoco — Codex

**Fecha:** 2026-07-31  
**Alcance:** reflexión científica y estratégica posterior al pivote del mapa de carga y al repaso final de literatura.  
**No incluye:** implementación, nuevas corridas ni revisión de código.  
**Propósito:** producir una posición independiente para comparar después con la reevaluación de la otra AI.

---

## Veredicto ejecutivo

Mi recomendación es **continuar, pero con un refoco importante**.

No abandonaría la pregunta general. Medir si la evidencia llega hasta un modelo ejecutable sigue siendo relevante y potencialmente publicable. Sí abandonaría tres formulaciones actuales:

1. que existe una sola magnitud llamada **carga** que ordena señal, trayectoria y costo;
2. que comparar un mundo corto con un lab largo identifica causalmente trabajo “vivido”;
3. que una única fracción `F` puede representar a la vez mejora contra la verdad, adherencia al update legal y proporcionalidad.

El proyecto actual contiene en realidad tres preguntas distintas:

- **asimilación:** ¿el agente entiende e incorpora la evidencia en su modelo registrado?;
- **dependencia de trayectoria:** ¿haber llegado endógenamente a un modelo modifica esa asimilación?;
- **propagación/reparación:** ¿una revisión ya comprendida logra atravesar las dependencias hasta la entrega final bajo presupuesto?

La literatura reciente ocupa mucho de la primera en tareas sin carga. La segunda sigue abierta, pero su constructo es difícil y hoy no está identificado. La tercera es la oportunidad más fuerte y aplicada.

Por eso propondría pivotear desde:

> “mapa de carga de la revisión de creencias”

hacia:

> **“descomposición causal de la transferencia evidencia→modelo→artefacto bajo dependencia de trayectoria y costo de reparación”.**

Una formulación más corta para el paper sería:

> **¿Dónde se pierde una actualización justificada cuando un agente debe convertir evidencia nueva en una revisión de un artefacto ya construido?**

El proyecto conservaría la respuesta bilateral —alejarse, reforzar o conservar— y la magnitud graduada, pero dejaría de tratar `PARTIAL` como una categoría y “carga” como una escala psicológica.

Mi juicio de publicación es **GO condicionado**. El programa revisado puede producir un paper fuerte. El programa sin revisar corre un riesgo alto de terminar como una combinación de context rot, prompts de ownership y dificultad de editar código.

---

## 1. Qué queda científicamente vivo después de la literatura

La literatura ya ocupa las piezas aisladas:

- [BeliefTrack](https://arxiv.org/abs/2605.30219) ocupa `stay/update/isolate` en mundos cerrados con verificador simbólico.
- [BayesBench](https://arxiv.org/abs/2606.30850), [Bayesian Teaching](https://arxiv.org/abs/2503.17523), [BASIL](https://arxiv.org/abs/2508.16846) y [LLMs Are Not Consistently Bayesian](https://arxiv.org/abs/2605.06915) ocupan buena parte de la actualización normativa y la separación under/over/wrong-direction.
- [Agentic Forecasting](https://arxiv.org/abs/2604.18576) ya tiene un agente que investiga y entrega una distribución verificable.
- [Autonomous Model Discovery](https://arxiv.org/abs/2607.06413) ya puntúa un modelo ejecutable contra verdad oculta con métricas distribucionales y cero juez LLM.
- [GeneBench-Pro](https://cdn.openai.com/pdf/21938268-21af-442f-af93-3b2249afb241/genebench-pro.pdf) ya puntúa trabajo científico largo mediante graders deterministas y documenta un `notice→act gap`.
- [Causal Agent Replay](https://arxiv.org/abs/2606.08275) ocupa el replay contrafactual.
- [BACKTRACE](https://arxiv.org/abs/2607.27484) ocupa la brecha entre dependencia causal y uso declarado mediante comparaciones apareadas.
- [STALE](https://arxiv.org/abs/2605.06527) y [Seeing Isn't Believing](https://arxiv.org/abs/2604.17252) muestran que reconocer una corrección no garantiza aplicarla.
- [FCPAgent](https://arxiv.org/abs/2607.24167) ya conecta contradicción, compromisos falsables y reparación de dependencias.

Lo que ninguna de estas fuentes permite estimar es:

> **La interacción causal entre valor probatorio, historia de construcción y costo material de propagación sobre la distancia entre la actualización legal y el artefacto ejecutable final.**

Ésa es la ventana. La novedad no está en juntar muchas features sino en identificar un estimando que las evaluaciones existentes no recuperan.

---

## 2. Lo mejor del proyecto actual

### 2.1 Puntuar la entrega y no la narración

Éste sigue siendo el activo conceptual más fuerte. El agente puede declarar que entendió una corrección y entregar el mismo modelo. WAGER puede observar esa diferencia sin pedir a otro LLM que interprete el razonamiento.

La entrega ejecutable permite:

- evaluar consecuencias contra una verdad oculta;
- medir cambios locales y colaterales;
- detectar incorporación parcial;
- separar una explicación convincente de una revisión efectivamente implementada.

### 2.2 Mundos con DGP conocido y actualización legal computable

La norma no depende de lo que el propio modelo diga que eran su prior o sus likelihoods. Esto es una ventaja frente a benchmarks declarativos, siempre que el mundo sea fresco y el oráculo utilice sólo información legalmente disponible.

### 2.3 Checkpoints y continuaciones apareadas

Comparar ramas desde el mismo modelo previo reduce gran parte de la varianza entre trayectorias. Es una base metodológica fuerte para estimar el efecto de una inyección o de una manipulación genuinamente randomizada.

### 2.4 Respuesta bilateral

El proyecto ya entiende que actualizar bien no equivale a cambiar siempre. Debe premiar:

- alejarse ante refutación;
- reforzar ante confirmación informativa;
- conservar ante placebo o evidencia no diagnóstica;
- moverse en magnitud proporcional en ambos sentidos.

Esto evita entrenar reflejos de paranoia o complacencia.

### 2.5 Disciplina anti-rabbit-hole

La regla “una discrepancia entre escenarios se lee primero como falta de generalización, no como un eje nuevo” es correcta y debería endurecerse, no abandonarse.

---

## 3. Problemas conceptuales que requieren refoco

### 3.1 “Carga” no es hoy una variable ordenada

El mapa agrupa bajo una sola palabra mecanismos distintos:

- menor valor probatorio;
- peor accesibilidad o presentación de una señal;
- mayor cantidad de historial;
- autoría atribuida;
- construcción endógena;
- dependencias técnicas;
- costo presupuestario de reparación.

No existe una razón teórica para que todos formen una escala monotónica. Más trayectoria puede producir rigidez, pero también mejor comprensión y resistencia correcta al ruido. Más costo puede reducir la reparación final aunque la creencia haya cambiado correctamente. Más filler puede degradar retrieval sin tocar el juicio epistémico.

Hablar de “curva dosis-respuesta de carga” promete una ley unidimensional que el diseño no justifica. Usaría **superficie de respuesta** o **descomposición de cuellos de botella**.

### 3.2 Valor de evidencia y accesibilidad están confundidos

El ADR 0154 construyó:

- `CLEAN`: veinte observaciones en regiones altamente diagnósticas;
- `MIXED`: diez de esas observaciones diagnósticas y diez en regiones de bajo valor.

Por lo tanto, CLEAN y MIXED tienen longitud similar, pero no contienen la misma información. CLEAN lleva al menos el doble de LLR esperada. La pasada 1 identifica el efecto de un **bundle con mayor concentración/dosis diagnóstica**, posiblemente combinado con interferencia semántica. No identifica “la misma evidencia ignorada porque estaba rodeada de relleno”.

La nota de dirección ya exige correctamente dos comparaciones separadas:

1. misma evidencia, con/sin filler → accesibilidad/contexto;
2. mismo formato y longitud, distinta LLR → sensibilidad a valor probatorio.

Esta distinción debe gobernar cualquier claim futuro y la relectura de la pasada 1.

### 3.3 “Vivido” no está operacionalizado

Una conversación nueva que recibe un snapshot no “vivió” el trabajo en un sentido fuerte. Recibe una representación textual de ese trabajo. Incluso un historial completo sólo demuestra exposición al historial, no inversión psicológica.

Además, comparar pasada 1 en el mundo corto con pasada 2 en el lab largo cambia simultáneamente:

- mundo;
- duración;
- checkpoint;
- dificultad;
- cantidad y formato del contexto;
- oportunidad de actuar;
- historia de selección de experimentos.

Esa comparación sirve para preguntar si un resultado generaliza. No identifica el efecto causal de construir el modelo.

El eje debería llamarse **endogeneidad/exposición de trayectoria**, con condiciones como:

- construcción endógena y continuación nativa;
- observación yoked paso a paso de la misma construcción, sin elegir las acciones;
- adopción del mismo estado mediante snapshot.

Sólo una manipulación dentro del mismo mundo puede sostener un claim causal sobre trayectoria.

### 3.4 La fricción cambia la conducta óptima

Si corregir una entrega consume presupuesto, invalida otros módulos o sacrifica experimentos valiosos, no reparar todo puede ser racional. Una métrica que trate cualquier distancia al update informacional como terquedad confunde epistemología con decisión bajo recursos.

Se necesitan dos targets:

- `M*belief`: actualización informacional correcta inmediatamente después de la evidencia;
- `M*deliver,budget`: mejor artefacto alcanzable con todos los datos legales y el presupuesto restante.

La distancia entre el registro inmediato y `M*belief` mide asimilación. La distancia entre la entrega y `M*deliver,budget` mide ejecución bajo restricciones.

### 3.5 El artefacto final no es una lectura pura de creencia

Una mala entrega puede provenir de:

- no entender la evidencia;
- actualizar el modelo conceptual pero no registrar el cambio;
- registrar bien pero elegir no invertir en reparación;
- intentar reparar y fallar operativamente;
- obtener nueva evidencia downstream que vuelve obsoleto el oráculo inicial;
- no entregar o producir un artefacto inválido.

Esto no debilita WAGER. Sugiere que su contribución más fuerte no es leer una “creencia interna”, sino **descomponer la transferencia desde evidencia hasta artefacto**.

### 3.6 La brecha dice–hace es un mecanismo, no la definición del paper

Puede haber una curva importante de revisión aplicada aunque declaración y entrega fallen juntas. Exigir una brecha verbal como condición de interés descartaría fallas reales de asimilación.

La descomposición `Mbelief → Mdeliver` **formaliza la parte aplicada de la brecha dice–hace**: separa lo que el agente dejó asentado como modelo revisado de lo que finalmente consiguió implementar. La declaración verbal sigue siendo un outcome secundario útil para localizar mecanismos, no el criterio constitutivo del fenómeno.

### 3.7 El factorial amenaza con convertirse en benchmark soup

Señal × autoría × compromiso × momento × fricción × modelos × mundos produce muchas celdas y poca potencia por contraste. Sin una hipótesis estructural, el “mapa” puede convertirse en inventario de efectos heterogéneos.

La publicación necesita una regularidad compacta, no una taxonomía exhaustiva.

### 3.8 `REGISTER` mide y a la vez interviene

Obligar al agente a exteriorizar un modelo ronda a ronda puede mejorar su disciplina epistémica. HEP, Bayesian Teaching y el scaffold de Seeing Isn't Believing sugieren que representar explícitamente el estado de creencia modifica la conducta.

Esto no impide usar `REGISTER`, pero exige:

- mantenerlo idéntico entre brazos;
- reconocer que se mide al agente bajo ese scaffold, no necesariamente su conducta espontánea;
- dejar cualquier ablación con/sin registro para otro estudio.

---

## 4. Problemas de medición

### 4.1 `F` no mide todo lo que hoy se le atribuye

La fracción basada en mejora del proper score contra la verdad puede ser útil en celdas donde existe una mejora legal grande. Pero no distingue:

- cercanía al oráculo legal;
- mejora casual contra la verdad;
- dirección correcta con magnitud equivocada;
- cambio colateral;
- estabilidad correcta cuando el target es no cambiar.

Además, en `RETAIN`, el denominador puede ser cercano a cero.

### 4.2 Separación propuesta de outcomes

Con pérdida menor-es-mejor y dos continuaciones base apareadas:

**Consecuencia contra la verdad**

`Δtruth = promedio Ltruth(Mbase) - Ltruth(Mtreat)`

Mide si el tratamiento mejoró la entrega respecto de la continuación natural.

**Adherencia al target legal**

Definir una divergencia inducida por el proper score:

`Dlegal(M; M*) = E_{Y~M*}[L(M,Y) - L(M*,Y)]`

y luego:

`Δlegal = promedio Dlegal(Mbase; M*) - Dlegal(Mtreat; M*)`

Mide cuánto cerró el tratamiento la distancia a la respuesta legal. Sólo cuando la distancia basal supera un umbral puede expresarse como fracción del gap cerrado.

**Dirección y magnitud**

Sobre predicciones pre-registradas:

- proyección sobre la dirección legal;
- overshoot o signo contrario;
- movimiento ortogonal o colateral.

En `RETAIN` se reportan distancia y deriva absolutas, sin dividir por un denominador diminuto.

### 4.3 El momento de medición debe congelarse

La actualización limpia debe medirse inmediatamente después de la inyección y antes de nuevas acciones. Si las ramas compran datos distintos, el mismo `M*` deja de ser válido para ambas entregas finales. El outcome final necesita un oráculo condicionado a la información legal de cada rama o debe interpretarse solamente como consecuencia total contra la verdad.

### 4.4 No-entregas e inválidos son outcomes

Excluirlos seleccionaría post-tratamiento. Deben reportarse como tasa co-primaria y recibir una utilidad/penalización pre-registrada cuando se agregan al score.

### 4.5 Cuatro cantidades que no deben llamarse “dosis” indistintamente

- `KL(verdad || M0)`: oportunidad o error previo disponible para corregir;
- LLR esperada del bundle: información que aporta la evidencia;
- `Dlegal(M0; M*)`: tamaño de la actualización legal inducida;
- movimiento observado: respuesta efectiva del agente.

Separarlas evita concluir que una condición produjo mayor sensibilidad cuando simplemente partía de un modelo peor o tenía más mejora disponible.

---

## 5. Relectura honesta de la pasada 1

La pasada 1 fue útil y disciplinada, pero el claim debe estrecharse.

### Lo que sí mostró

En gpt-5.4, un mundo, un checkpoint de cierre y catorce donantes:

- el artefacto respondió mucho mejor a un bundle de alta concentración diagnóstica que a uno con mitad de observaciones de bajo valor;
- las etiquetas de autoría y compromiso, aisladas de costo material, no produjeron un efecto claro;
- el placebo fue inerte;
- hubo 28 no-entregas que forman parte del resultado.

### Lo que no mostró

No demostró todavía:

- que la misma evidencia se pierde por estar rodeada de filler;
- que el efecto sea específicamente revisión de creencias y no gestión de contexto;
- que el trabajo propio vivido produzca rigidez;
- una interacción causal entre trayectoria y fricción;
- una ley general entre modelos o mundos;
- 252 observaciones independientes: la unidad sigue siendo catorce donantes.

### Valor real del resultado

Es un buen piloto del instrumento y una primera señal de **sensibilidad de la entrega a concentración/accesibilidad de evidencia**. No debería cargar por sí solo la contribución final.

---

## 6. Cuatro direcciones posibles

### Opción A — Continuar el mapa de carga tal como está

**No recomendada.**

Ventaja: aprovecha toda la infraestructura y el lenguaje existente.  
Riesgo: mezcla mecanismos, multiplica celdas y produce claims débiles de “más carga, menos update”.

### Opción B — Pivotear a evidencia limpia versus evidencia diluida

**No recomendada como paper principal.**

Es fácil de ejecutar y la pasada 1 dio señal. Pero el espacio está muy cerca de Context Rot, BeliefTrack, OAKS y forecasting con evidencia acumulada. Sería un estudio útil de evals, no la contribución más única de WAGER.

### Opción C — Transferencia evidencia→artefacto bajo dependencia de trayectoria y costo de reparación

**Recomendada.**

La pregunta pasa de “¿cuánta carga soporta una creencia?” a:

> **Dada una actualización normativa conocida, ¿en qué etapa deja de propagarse hasta la entrega cuando existe un artefacto previo con dependencias y costos de modificación?**

Ventajas:

- conserva el artefacto ejecutable, verdad oculta y fork apareado;
- convierte la brecha dice–hace en una descomposición causal más precisa;
- distingue asimilación epistémica de reparación operativa;
- conecta directamente con agentes científicos y de largo horizonte;
- tiene menos solapamiento con benchmarks declarativos;
- permite resultados positivos y negativos interpretables.

### Opción D — Validez predictiva de micro-evals sobre conducta agéntica larga

**Interesante, pero futura.**

Comparar una microviñeta hermanada con el episodio largo podría producir otro buen paper, incluso con correlación nula. Pero abrirlo ahora duplicaría la pregunta, el diseño y la muestra. Debe quedar como extensión posterior, no como rescate del proyecto actual.

---

## 7. Propuesta revisada

### 7.1 Pregunta principal

> **Cuando evidencia nueva justifica una revisión conocida, ¿cómo se reparte el error entre asimilación de la evidencia, decisión de reabrir y propagación de la revisión hasta un artefacto ejecutable?**

### 7.2 Pregunta causal secundaria

> **¿Cómo modifican esa transferencia la construcción endógena de la trayectoria y el costo material de reparar dependencias?**

### 7.3 Objeto de estudio

No “creencia psicológica”, sino tres estados observables:

1. `M0`: modelo predictivo registrado antes de la evidencia;
2. `Mbelief`: modelo registrado inmediatamente después de la evidencia y antes de reparar;
3. `Mdeliver`: artefacto ejecutable final.

La cadena es:

`evidencia → Mbelief → decisión/acciones de reparación → Mdeliver`

### 7.4 Factores principales

**Factor 1 — Target epistémico**

- dirección: alejar / reforzar / cero;
- magnitud: débil a fuerte, determinada server-side.

**Factor 2 — Endogeneidad de trayectoria**

- construcción/continuación nativa;
- observación yoked de la misma trayectoria;
- adopción por snapshot, usada primero como control de representación.

**Factor 3 — Costo de propagación**

- reparación local/barata;
- reparación con dependencias reales;
- control mecánico de igual dificultad sin revisión epistémica.

**Accesibilidad de evidencia** queda como control o moderador, no como sinónimo de valor probatorio.

### 7.5 Contribución buscada

No un ranking de modelos ni un catálogo de sesgos, sino:

> **Una descomposición causal y cuantitativa de dónde se pierde una actualización legal entre evidencia, modelo registrado y artefacto final.**

---

## 8. Hipótesis compactas

No pre-registraría más de cinco hipótesis principales:

### H1 — Calibración normativa

En ausencia de trayectoria y fricción, el movimiento sigue correctamente dirección y magnitud del target.

### H2 — Cuello de asimilación

La endogeneidad de trayectoria aumenta `Dlegal(Mbelief)` especialmente bajo evidencia intermedia, no bajo refutación aplastante.

### H3 — Cuello de propagación

La fricción aumenta la distancia `Mdeliver − Mbelief` aun cuando `Mbelief` se actualizó correctamente.

### H4 — Interacción

Trayectoria endógena y fricción producen una pérdida mayor que la suma de sus efectos simples, sobre todo en la zona intermedia.

### H5 — Bilateralidad

El mismo mecanismo que genera rigidez bajo refutación puede producir estabilidad útil bajo placebo; el outcome relevante es distancia al target legal, no cantidad bruta de cambio.

La brecha entre declaración y entrega queda como mecanismo secundario. No es una hipótesis necesaria para justificar el paper.

---

## 9. Programa experimental mínimo

### Gate 1 — Fidelidad de estado

Comparar, desde los mismos donantes y sin tratamiento:

- continuación nativa;
- historial completo replayado;
- snapshot canónico.

Si snapshot altera sustancialmente registro, compras o entrega, no usarlo para representar “trayectoria vivida”.

### Gate 2 — Instrumento bilateral

En el mismo mundo y con longitud/formato controlados:

- refutación;
- confirmación;
- placebo;
- dosis intermedias en ambos sentidos.

Medir `Mbelief` antes de cualquier acción downstream.

### Experimento principal mínimo

Cruzar dentro del mismo mundo/checkpoint:

`target epistémico × trayectoria × fricción`

No usar pasadas en mundos distintos para estimar la interacción. Si el factorial es demasiado grande, reducir targets o contrastes, no fingir una interacción a partir de estudios separados.

### Replicación

Sólo después de identificar una regularidad:

- segunda familia de mundo;
- segunda familia de modelo;
- análisis explícito de heterogeneidad.

---

## 10. Inferencia y escala

Los forks de un mismo donante no son observaciones independientes. Catorce donantes son insuficientes para sostener interacciones múltiples con intervalos precisos.

Antes de correr:

- estimar varianza donante-a-donante usando la pasada 1;
- fijar un efecto mínimo relevante (`SESOI`);
- simular potencia al nivel de donante;
- reducir brazos o aumentar donantes;
- mostrar contrastes individuales por donante;
- usar inferencia por randomización cuando el esquema lo permita.

Un resultado nulo es interesante sólo si los intervalos descartan efectos científicamente relevantes. “No significativo” no prueba ausencia.

---

## 11. Qué resultados serían publicables

### Resultado positivo fuerte

> La evidencia se incorpora adecuadamente en el modelo registrado, pero deja de propagarse a la entrega a medida que aumenta el costo de reparar dependencias; la pérdida es mayor tras una trayectoria endógena y bajo evidencia intermedia.

Esto demostraría un cuello de botella aplicado que no aparece en benchmarks declarativos.

### Resultado positivo alternativo

> La trayectoria afecta ya la asimilación inmediata, incluso antes de existir costo de implementación, y el efecto cambia de signo entre refutación y placebo.

Esto sería evidencia real de path dependence epistémica, sin necesidad de lenguaje psicológico.

### Resultado negativo fuerte

> Una vez controlados valor probatorio, presentación y costo de reparación, construir el modelo propio no tiene un efecto relevante; casi toda la aparente “carga” se explica por accesibilidad y costo operativo.

Un null bien potenciado derribaría una intuición antropomórfica y también sería publicable.

### Resultado débil

- CLEAN gana a MIXED con distinto contenido diagnóstico.
- Un label `SELF` cambia o no cambia una respuesta.
- Un lab largo difiere de un mundo corto.
- El artefacto final empeora, pero no sabemos si falló inferencia, decisión o implementación.
- El efecto aparece en un único modelo/mundo/wording.

Eso no alcanza para un paper principal.

---

## 12. Qué conservar, qué reformular y qué pausar

### Conservar

- mundos con verdad oculta;
- modelo ejecutable;
- scoring cero-LLM;
- registro pre/post;
- forks apareados;
- bundles cuantificados server-side;
- respuesta bilateral;
- bases dobles;
- no-entregas como outcome;
- regla anti-rabbit-hole.

### Reformular

- `carga` → mecanismos separados o superficie de respuesta;
- `vivido` → trayectoria endógena/exposición al historial;
- `PARTIAL` → magnitud, no dirección;
- `F` → métrica secundaria condicionada a denominador estable;
- dice–hace → mecanismo secundario;
- momento → consecuencia de trayectoria/costo, no eje primario.

### Pausar

- presión social e identidad;
- no-estacionariedad;
- micro-vs-macro validity;
- Martingale Score;
- entrenamiento/mitigación;
- expansión de mundos antes de validar el constructo;
- nuevos ejes que no resuelvan una discrepancia replicada.

### Abandonar

- autoría puramente atribuida como proxy suficiente de trabajo propio;
- lenguaje de ego, terquedad o sunk cost sin manipulación operacional;
- claim de “misma evidencia diluida” para la pasada 1;
- idea de una ley unidimensional de carga sin evidencia empírica;
- comparación entre mundos como prueba causal de trayectoria.

---

## 13. Secuencia de decisión y gobernanza

Este refoco no debería abrir otra rama paralela del proyecto. Debería convertirse en la **única rama científica activa** hasta validarla o cerrarla.

La secuencia mínima es:

1. **Etapa 0 — validez y potencia.** Pre-registrar el estimando, el `SESOI`, la unidad independiente, los criterios de muerte y un tope de gasto. Ejecutar Gate 1 y simular potencia antes de fijar el número de donantes.
2. **Etapa A — instrumento bilateral.** Ejecutar Gate 2 y comprobar que el sistema distingue refutación, confirmación y placebo, además de intensidades intermedias. Medir `Mbelief` inmediatamente. Si esta etapa falla, no interpretar trayectoria ni fricción.
3. **Etapa B — experimento principal.** Cruzar sólo los contrastes mínimos de trayectoria y fricción, incluyendo el control mecánico de igual dificultad. No sumar scaffolds, nuevos mundos ni ejes sociales al factorial principal.
4. **Etapa C — replicación dirigida.** Replicar únicamente una regularidad ya identificada en otra familia de mundo y otra familia de modelo.

Cada ciclo debería terminar en una decisión explícita: **avanzar, reformular, detener o escribir**. El esqueleto del paper debe actualizarse con resultados y falsaciones durante el proceso; la búsqueda bibliográfica pasa a vigilancia periódica, no a actividad permanente.

Las compuertas son bloqueantes, pero no deben convertirse en estudios largos independientes. Gate 1 puede reutilizar donantes existentes; la simulación de potencia usa la varianza ya observada; y Gate 2 debe ser el piloto mínimo capaz de validar dirección y magnitud. Deben ejecutarse en un calendario corto y, donde sea posible, en paralelo. La urgencia de publicación justifica reducir brazos y reutilizar evidencia, no interpretar un instrumento que todavía no pasó sus controles.

---

## 14. Criterios de corte

Pivotear o detener el programa si ocurre cualquiera de estos patrones:

1. el efecto de evidencia desaparece al separar LLR de filler;
2. snapshot y continuación nativa no son equivalentes y no puede instrumentarse continuidad;
3. no puede construirse `M*belief` para casos parciales;
4. no puede definirse una referencia factible bajo presupuesto;
5. la trayectoria sólo produce efectos mediante wording o etiquetas;
6. toda la diferencia se explica por dificultad de edición;
7. los efectos cambian de signo sin estructura entre donantes o mundos;
8. no hay recursos para obtener suficiente unidad independiente a nivel donante.

No detener automáticamente si trayectoria da nulo. Si la prueba tiene potencia, se cierra ese eje y se publica la descomposición negativa.

---

## Conclusión

WAGER no necesita otro pivot total. Necesita dejar de prometer un “mapa de carga” demasiado amplio y convertir su maquinaria en una medición causal de un cuello de botella preciso.

La tesis que defendería es:

> **Los agentes no sólo pueden fallar al interpretar evidencia; también pueden fallar al transferir una revisión correctamente entendida hacia un artefacto ya construido. WAGER separa ambos fallos y mide cómo cambian bajo trayectoria endógena y costo real de reparación.**

Ese encuadre es más estrecho que el actual, pero científicamente más fuerte. Está mejor diferenciado de BeliefTrack y BayesBench, aprovecha la ventaja de la entrega ejecutable frente a STALE/LURE, y convierte a GeneBench-Pro/FCPAgent en anclas aplicadas en lugar de amenazas.

Mi recomendación final es:

> **GO con refoco: de “mapa de carga” a “transferencia evidencia→artefacto bajo path dependence y switching costs”.**

No ejecutaría la pasada 2 anunciada en ADR 0155 **tal como está formulada**. El próximo artefacto debería ser un pre-registro revisado de la Etapa 0 y la Etapa A; sólo si ambas pasan se habilita el experimento causal principal.
