# Mundos dinámicos (ODE) — contexto completo para la próxima sesión
### Qué son, por qué van ahora, y cómo se construyen sin romper nada

> **Cómo usar este doc.** Es el contexto autocontenido para arrancar una sesión nueva (de dirección o de Claude Code) sobre el mundo #11 de la matriz E1: el primer mundo dinámico. Asume que conocés WAGER en general (si no, leer `WAGER_HANDOFF.md` primero). Ante conflicto con el repo, manda el repo.

---

## 1. La idea en una frase: de la foto a la película

Todos los mundos construidos hasta hoy son **fotos**: le pedís al mundo un régimen (perillas fijas — dosis, contexto) y te devuelve una tabla donde cada fila es una unidad independiente. Causa → efecto, sin tiempo.

Un mundo dinámico es una **película**: el mecanismo es un proceso que evoluciona — algo que crece, se propaga, se agota, satura. La unidad de datos ya no es una fila: es una **trayectoria**, una curva de valores en el tiempo. El agente observa curvas, decide *cuándo* medir además de *qué* medir, y entrega un modelo que reproduce la dinámica.

El primer mundo dinámico (#11) usa el proceso más simple con historia real: **crecimiento logístico** — la curva de todo lo que primero crece como si no tuviera límite y después se topa con uno. Cultivos de bacterias, adopción de productos, poblaciones, producción acumulada de un yacimiento. Dos parámetros con significado físico: la velocidad de crecimiento (r) y el techo o capacidad (K). Tiene solución en fórmula cerrada (no hace falta integrador numérico: determinismo perfecto, ejecución barata) y trae incorporada la trampa epistémica más documentada de la historia: **en la fase temprana, una curva logística es indistinguible de una exponencial**. Todo el que extrapoló una curva de hype conoce el error.

---

## 2. Por qué este mundo va ahora (y qué NO le pedimos)

Tres razones, en orden de importancia:

**Primera: validar que la maquinaria no está casada con las fotos.** Todo lo construido en dos meses — el score combinado, los rivales derivados, la batería, los certificados, las sub-baterías de visibilidad, la escalera L1 — se desarrolló sobre mundos estáticos de tablas causa-efecto. E1 y E3 necesitan al menos dos formalismos distintos para poder afirmar que medimos "juicio" y no "juicio sobre SCMs estáticos". Si la maquinaria sobrevive al segundo formalismo con cambios menores, creemos que generaliza; si necesita cirugía mayor, es infinitamente mejor saberlo ahora con 6 mundos que con 15. **Este es el trabajo del mundo #11: es un test de la fábrica, no un candidato al trofeo.**

**Segunda: abre un eje de juicio genuinamente nuevo — cuándo medir.** En las fotos, el diseño experimental es "qué perillas mover". En una película, aparece la dimensión que los experimentalistas reales sufren: ¿mido temprano o tarde? ¿denso o espaciado? ¿corto la corrida o la dejo correr (y pago el tiempo de reactor)? En el logístico esto tiene estructura preciosa y conocida: los puntos tempranos informan sobre r, pero **K es literalmente invisible hasta que la saturación empieza** — ningún dato de la fase exponencial, por preciso que sea, te dice dónde está el techo. Un agente con buen juicio asigna presupuesto de medición en el tiempo; uno malo mide denso donde es barato y extrapola.

**Tercera: es el anfitrión natural del futuro mundo de pivoteo.** La brecha de adaptividad (ningún mundo la ejercita aún) y el mecanismo de "el mundo te interrumpe" (spec en papel) encajan naturalmente en dinámicas: las cosas cambian a mitad de trayectoria. No se implementa nada de eso en #11 — pero conviene no tomar decisiones que lo bloqueen.

**Expectativa honesta, pre-registrada:** #11 puede saturar como el mundo 3 (un frontier con las movidas de manual puede resolverlo). Está bien: su trabajo es validar formalismo, no producir headroom. Los candidatos al trofeo siguen siendo v2 y el futuro mundo anti-vicio. Si además resulta difícil, bonus.

---

## 3. Lo que NO cambia (el contrato es el mismo)

Esto es lo primero que hay que tener claro para no sobre-diseñar:

- **El entregable es el mismo**: un programa `model(regime, n, seed) → tabla`. La tabla ahora tiene columnas de tiempo, pero sigue siendo una tabla. Identidad conductual intacta: comparamos las distribuciones de sus salidas contra las del mundo verdadero, en regímenes que nunca vio.
- **Cero LLM en el reward**, como siempre. CI lo protege.
- **Las anclas son las simples**: #11 no tiene estado oculto por-ítem (no hay mix secreto ni ventana). `world.py` vuelve a ser el techo legal R=1, el ingenuo sobre el pool corrupto es R=0. Toda la maquinaria Bayes-adaptiva de v2 queda afuera de este mundo — no la necesita.
- **Las tres capas siguen**: mecanismo limpio / canal de observación / proceso de muestreo. Las trampas viven en las fuentes; `world.sample()` es la verdad.
- Brief ciego, funcionales trazables al brief, certificados, L1 derivada, sub-baterías de visibilidad, CRN con seeds apareados: todo igual.

---

## 4. Lo que SÍ cambia, pieza por pieza

### 4.1 La forma de la muestra: la unidad es una trayectoria

Decisión de contrato: el formato del entregable. La opción natural es **formato largo**: cada fila es `(unit_id, t, y)` — una lectura de una unidad en un tiempo. El régimen de cada ítem de batería declara, además de las perillas, una **grilla de tiempos** (`t_grid`): en qué timestamps debe reportar el modelo. La grilla viaja en `regime.context`, igual que la ventana de v2 viajó en context — el precedente ya existe y funcionó.

Punto fino: el mundo verdadero genera trayectorias con **heterogeneidad poblacional** — cada unidad tiene su (r, K) levemente distinto, muestreado de una distribución poblacional. Sin eso, todas las curvas serían idénticas y la "distribución" por timestamp sería un punto (varianza cero → problemas de escala, ver 4.3). La variabilidad entre unidades es lo que hace que comparar distribuciones tenga sentido.

### 4.2 El scoring: columnas-por-tiempo + funcionales de trayectoria

Acá vive el known-unknown declarado, así que la estrategia es conservadora: **reusar la maquinaria existente con la lectura más natural, y frenar solo si no alcanza.**

La lectura natural: para un ítem de batería con grilla de k tiempos, cada timestamp es una **columna** del vector de salida por unidad. La energy distance ya compara distribuciones conjuntas multi-columna con estandarización por columna (σ de la verdad por columna) — las columnas de tiempo son columnas. Que estén autocorrelacionadas no molesta: la energía trabaja sobre la conjunta.

Encima de eso, los **funcionales de stakes** son donde el formalismo brilla, porque las preguntas del cliente en dinámicas son *funcionales de trayectoria por naturaleza*: "¿cuándo llegamos al 80% de la capacidad?" (tiempo-de-cruce), "¿cuál es el rendimiento final?" (valor de plateau), "¿qué probabilidad hay de no llegar al deadline?" (exceedance sobre un tiempo-de-cruce). Todos computables de las muestras del modelo, todos en la librería tipada existente o extensiones triviales de ella, todos trazables a cláusulas verbatim del brief. Ambas monedas (R y |ΔF|) en todos los reportes, como quedó canónico.

**El tripwire, explícito:** si esta combinación (columnas-por-tiempo + funcionales de trayectoria) resulta insuficiente — por ejemplo, si aparece la necesidad de alinear curvas desfasadas (DTW), o de scorear la dinámica latente en vez de los observables — eso es **semántica nueva de scoring** → tripwire-1, frenar y discutir. La apuesta pre-registrada es que NO va a hacer falta para el logístico.

### 4.3 La trampa de escala esperada (pre-registrada como sexta de la familia)

La familia de patologías de escala ya nos mordió cinco veces, y acá hay una esperándonos que conviene nombrar ANTES de que muerda: **a tiempos tempranos, la varianza de la verdad puede ser casi cero** (todas las curvas arrancan cerca del mismo x₀). Estandarizar por columna divide por esa σ minúscula → errores absolutos insignificantes se inflan a distancias gigantes. Es exactamente el patrón del bug del clamp de std (v0.21).

Mitigaciones, en orden: (a) la suite de sanidad de escala ya tiene el clamp relativo — verificar que cubre columnas-de-tiempo con test explícito; (b) diseño del mundo: condición inicial x₀ con variabilidad poblacional declarada, para que ninguna columna sea degenerada; (c) la grilla de la batería no pone ítems en t≈0 puro salvo que un stake lo pida. Pre-registro: el test de sanidad sobre el mundo #11 debe pasar sin tocar el clamp; si pide tocarlo, se investiga (familia escala = investigar, no retunear).

### 4.4 El tiempo como presupuesto: la economía nueva

`experiment(design)` en un mundo dinámico declara: condiciones iniciales / perillas de entorno (lo que la superficie de control permita), y un **cronograma de medición** — qué timestamps leer, cuántas unidades. Los costos tienen dos ejes nuevos declarados en la fuente: costo por corrida (lanzar una tanda) y costo por lectura (cada punto medido — los sensores no son gratis). Opcionalmente, costo por horizonte (dejar correr el reactor más tiempo cuesta más) — esta es LA perilla que hace caro conocer K y barato conocer r, o sea la que le pone precio al juicio temporal.

La regla v0.9 sigue intacta: el experimento esquiva el proceso de muestreo histórico, **jamás el canal de medición** — las lecturas experimentales llegan con el mismo ruido de sensor que las históricas.

### 4.5 Dónde viven las trampas: el histórico truncado es la mentira canónica

La composición de operadores de #11, usando solo piezas que ya existen o extensiones declaradas de la capa de fuentes (que quedó genérica en el mundo 3):

- **Fuente barata (histórica): trayectorias truncadas temprano.** Los registros viejos cubren solo la fase de crecimiento — los estudios se cortaron antes de la saturación (pasa en la realidad todo el tiempo: los proyectos se miden mientras crecen). Consecuencia epistémica: en el pool barato, **K es no-identificable** y la historia que los datos cuentan es "esto crece exponencial". El ingenuo que le cree al pool extrapola el crecimiento sin techo → falla catastróficamente en toda pregunta de plateau — que es exactamente donde el brief pone los stakes. Esa es la brecha mecanística del mundo: para responder lo que importa hay que **pagar experimentos largos** (o inferir el inicio de saturación de las colas del histórico, si el diseño deja esa punta).
- **Canal: ruido de medición zero-mean en y(t)**, con σ_med declarada vía la fuente de réplicas (la lección de identificabilidad del mundo 3 aplica idéntica: sesgo constante = indescubrible = prohibido en v0; réplicas = σ estimable). La maquinaria es la misma `MeasurementChannel` — la capa genérica se reusa sin código nuevo, y eso mismo es parte del test de generalización.
- **Fuera de v0 (registrado, no implementado):** saturación de sensor (lecturas clipeadas arriba de un umbral — haría que el plateau *parezca* más bajo; trampa hermosa pero segunda vuelta), jitter en los tiempos de muestreo, proceso estocástico en el mecanismo (ruido de proceso además de heterogeneidad poblacional). Cada uno es una perilla futura declarada del operador.

### 4.6 Rivales derivados: qué encarna cada uno acá

- **(a) Ingenuo** = ajuste flexible sobre el pool truncado+ruidoso → aprende crecimiento sin techo → ancla R=0 y pierde donde los stakes viven. Encarna "los datos dicen lo que parecen decir", versión temporal.
- **(b) Gemelos por operador**, vía la ablación consciente-de-capa que el mundo 3 estrenó (`source_layer_twins` — reuso directo, test de que generaliza): el gemelo de truncación cree "los datos que veo cubren toda la historia" (fit completo sobre el pool con horizonte corto, extrapolación de su familia); el gemelo del canal cree "la dispersión que veo es real".
- **(d) Escalera de capacidad** sobre trayectorias: polinomios en t, splines/suavizadores, familia exponencial, y — importante — **una familia saturante genérica** (logística de 3 parámetros por unidad, sin mecanismo poblacional). Ojo con la expectativa: una saturante genérica bien fiteada con datos completos ES casi el mecanismo. Por eso el **pre-registro honesto: theory gap ≈ 0 en #11** — este mundo no carga en representación; carga en canal-sesgado (truncación + ruido) y sondas-caras (el tiempo cuesta). La carga diferencial (≥2 coordenadas) se cumple por esas dos, y se declara así en meta.
- **(c) Prior evocado**: el logístico es conocimiento de manual — el panel va a proponer "crecimiento que satura". Está bien: la brecha de prior de este mundo no vive en la *forma* sino en los *números* (¿dónde está K? ¿cuándo satura?) — el manual no trae los parámetros del mundo. Se mide y se reporta como está definido.

### 4.7 La batería: el tiempo gana su banda "fuera de registro"

Los ítems de batería ahora son (perillas, grilla de tiempos, peso), y el mapa de cobertura gana una dimensión temporal con una simetría linda con lo ya canonizado: **"tiempos más allá del horizonte que el histórico mostró" es el nuevo fuera-de-registro**, y le aplica la misma banda canonizada (20-35% del peso, trazable al checklist de promesas del brief — que va a prometer explícitamente interés en el largo plazo). La sub-batería de visibilidad de la truncación vive precisamente ahí (ítems de horizonte largo); la del canal, en los ítems con réplicas/dispersión. El desacuerdo se computa en el score combinado, como siempre. Dedup y stakes operan sobre (perillas × banda temporal).

### 4.8 Ergonomía pre-escrita (#19, la lección que ya pagamos dos veces)

Antes del primer E0, el brief y la ficha documentan sin ambigüedad: (1) el formato exacto del entregable (largo: `unit_id, t, y`; la grilla llega en `regime.context["t_grid"]` y el modelo debe reportar exactamente esos tiempos); (2) que las mediciones incluyen error de instrumento y el entregable modela **el proceso, no el medidor** (línea verbatim del mundo 3, reusada); (3) qué entrega cada verbo (`observe` = trayectorias históricas truncadas con ruido; `experiment` = corridas frescas con el cronograma pedido, mismo sensor). El humo valida shape contra `t_grid`. Sin esto, el E0 mide comprensión lectora.

---

## 5. Orden de construcción firmado y pre-registros

El orden es el estándar de la casa, con los números a llenar antes de mirar:

1. **Contrato de fuentes**: histórica truncada (horizonte declarado, n, costo) + experimental (costos por corrida/lectura/horizonte) + réplicas para σ_med. Todo en `SourceConfig` existente — si algo pide código nuevo en la capa de fuentes, se registra como hallazgo (la capa se declaró genérica; esto la testea).
2. **world.py + meta**: logístico cerrado, heterogeneidad poblacional en (r, K, x₀), superficie de control con rangos experimentables declarados, operadores con knobs, ablaciones declaradas.
3. **Brief** ciego: historia (cultivo/adopción/producción — elegir skin), stakes temporales con cláusulas verbatim (tiempo-a-umbral, plateau, deadline), la línea proceso-no-medidor, el formato del entregable.
4. **Derivación completa** sin código nuevo (rivales, batería, certificados) — cada pieza que pida código es un dummy-ismo temporal y se registra como los siete anteriores.
5. **L1 derivada** — orden esperado pre-registrado: verdad > perturbado > gemelo-canal > gemelo-truncación > ingenuo-truncado > nulo (el gemelo de truncación cerca del ingenuo es esperable: creen casi lo mismo; si empatan, se reporta, no se retunea).
6. **Sanidad de escala** sobre columnas temporales (el clamp relativo debe alcanzar sin tocarse).
7. **Certificados**: mecanística grande (vía truncación), teoría ≈ 0 (declarado), visibilidad por sub-batería temporal, recuperabilidad con σ_med estimable, carga diferencial por canal+sondas.
8. **Headroom pre-registrado antes de mirar** + **E0-probe** (2 episodios frontier, ambas monedas, traces al repo). Vara de velocidad: 1-2 sesiones, como el mundo 3; el exceso se reporta como dato.

**Compuerta de decisión al final (la que importa):** si la maquinaria pasó con cambios menores → el formalismo está validado, se sigue llenando cartera. Si pidió cirugía en el scoring → tripwire, frenar, rediseñar ANTES de sumar más formalismos. Cualquiera de las dos salidas es información; la segunda, más barata ahora que nunca.

---

## 6. Perillas de dificultad (para el gimnasio de después, no para ahora)

Registradas para cuando llegue el entrenamiento: el **horizonte del histórico** (cuán temprano se truncó — más temprano = K más invisible), el **costo del tiempo experimental** (cuán caro es ver la saturación con tus propios ojos), el **ruido del sensor**, y en segunda vuelta la saturación de sensor. La escalera de dificultad del mundo es continua y declarada — exactamente lo que el requisito "cada mundo de entrenamiento trae su dial identificado" pide.

---

## 7. El resumen para retener

#11 es la película más simple posible (crecer y saturar), construida para responder una sola pregunta: **¿la fábrica de exámenes sobrevive al cambio de formalismo?** El contrato del agente no cambia, el reward no cambia, las trampas se declaran con la capa genérica que ya existe, y las dos novedades reales — la grilla de tiempos como parte del régimen, y los funcionales de trayectoria como stakes — son extensiones naturales de piezas probadas (el context de v2, la librería de funcionales). El riesgo conocido tiene nombre (escala en columnas tempranas) y guardia pre-registrada. La expectativa honesta es que el mundo funcione y quizás sature con un frontier — su trofeo es la generalización de la maquinaria, no el headroom. Y de yapa deja sembrado el terreno donde el mundo de pivoteo va a vivir.
