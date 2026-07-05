# WAGER — North Star
## Worlds As Generators of Epistemic Reward
### Mundos sintéticos para entrenar juicio investigativo

> **Qué es este documento.** La constitución del proyecto: el porqué (ethos), el qué (diseño) y el cómo se valida (programa experimental). Está pensado para ser leído y **mantenido** tanto por humanos como por Claude Code. No es un plan de sprint ni documentación de API.
>
> **Estado**: v0.69 (2026-07-05). El changelog versión-a-versión (v0.1→v0.68) está en [`docs/archived/NORTH_STAR_changelog.md`](docs/archived/NORTH_STAR_changelog.md); el detalle de cada decisión, en [`DECISION_LOG.md`](DECISION_LOG.md). Esta constitución refleja las decisiones hasta esa versión.
>
> **Relación con SREG**: este proyecto nace como pivot de SREG. `PROJECT.md` y `CURRENT_STATE.md` siguen siendo válidos como documentación de SREG v1/v1.5 (repo de referencia, solo lectura). Ante conflicto conceptual entre aquellos docs y este, **manda este**.

---

## 0. Instrucciones de mantenimiento (leer antes de editar nada)

Para Claude Code y cualquier colaborador:

1. **Jerarquía de autoridad**: §2 (Ethos) > §3–5 (Diseño) > specs en issues > código. El código nunca contradice este doc en silencio. Si la implementación revela que algo del doc está mal, lo correcto es **proponer la edición del doc + registrar en el Decision Log (`DECISION_LOG.md`)**, no desviarse calladamente.
2. **Tags de madurez**: cada sección lleva `[ESTABLE]` (cambiarla requiere justificación fuerte y entrada en el Decision Log) o `[EN DEBATE]` (se espera que evolucione).
3. **Nada se borra, se supersede.** Las decisiones viejas quedan en el Decision Log con fecha y razón del cambio.
4. **§10 (Open Questions) es el inbox** de dudas no resueltas. Al resolverse una, migra al Decision Log con su resolución.
5. **Estilo**: español directo, sin humo. Concreto > elegante. Si una sección puede decirse en la mitad de palabras, hacerlo.
6. **Antes de tocar código que afecte el reward path**, releer §2.2, §2.3 y §4.4. Son los puntos donde el proyecto vive o muere.
7. **Unidad de avance**: el slice vertical más chico que ejercite el reward path completo (mundo → episodio → submission → score). El orden de trabajo lo define el programa experimental (§6); E1 no requiere entrenar nada.
8. **El repo SREG es referencia de solo lectura.** Las piezas que sirvan (digestion, architect, validators, kernel runtime) se **portean deliberadamente** cuando un slice las necesita; nunca se importan por arrastre.
9. **§1 y §5 son el embrión del paper** (introducción + related work + justificación). Estándar de edición en esas secciones: cada claim debe ser defendible con evidencia citable o argumento estructural — nunca con entusiasmo.
10. **Mapa de documentos**: `NORTH_STAR.md` (constitución: por qué y qué) → `ARCHITECTURE.md` (diseño técnico: contratos, librería de operadores, semántica de rivales, algoritmo de batería, harness, scoring) → `CLAUDE.md` (operativa del repo) → `CURRENT_STATE.md` (estado vivo del repo: qué corre hoy, qué falta; lo mantiene Claude Code SIEMPRE al día) → `DECISION_LOG.md` (el registro append-only de decisiones, fecha — decisión — razón; movido acá desde §11 en v0.69) → `docs/archived/` (histórico: changelogs de header, narrativa vieja de CURRENT_STATE — nada se borra). Los detalles de implementación viven en ARCHITECTURE; este documento no los duplica.

---

## 1. La apuesta `[ESTABLE]`

### El objetivo final

> **Diseñar el juego para que comportarse como un buen científico sea la estrategia óptima para ganarlo.**

No le enseñamos el método científico al agente: construimos entornos donde hipotetizar, discriminar con experimentos, actualizar ante la evidencia, calibrar la confianza y parar a tiempo es lo que maximiza el score — y donde cualquier atajo paga menos. Todo lo demás de este documento es instrumentación de esta frase.

Esto hereda directamente el principio de **presiones evolutivas** del `PROJECT.md` original de SREG ("¿un agente SIN la propiedad X obtiene un score más bajo? Si no, hay que rediseñar"), que sobrevive al pivot como alma del proyecto — ahora con **certificados computables** (las cuatro brechas, §4.6) en lugar de checklist aspiracional.

### El problema

Los modelos frontier ya ejecutan bien tareas de research bien especificadas. Lo que nadie puede entrenar hoy es el **juicio investigativo**: qué vale la pena medir, cuándo un resultado es artefacto, cuándo pivotear, cuándo parar, cuándo abstenerse, cómo pesar priors contra evidencia. La razón es estructural:

- En ciencia real, el feedback sobre el juicio llega tarde, ruidoso o nunca. No se puede hacer RL contra "la historia te dará la razón en cinco años".
- El sustituto universal — LLM judges — se degrada bajo presión de optimización justo cuando el modelo se vuelve bueno, que es cuando más importa.

### El activo único: los tres oráculos

Ser **dueño del mundo** (el mundo es un programa que nosotros escribimos) no da un oráculo: da tres.

| Oráculo | Qué permite | Análogo en ciencia real |
|---|---|---|
| **De verdad** | Scorear las apuestas del agente contra regímenes held-out: condiciones nunca vistas, counterfactuals, queries no-identificables | Imposible: la verdad nunca se conoce con certeza |
| **De valor de decisión** | Anotar cada movida del agente como un engine de ajedrez: cuánta información valía cada experimento posible en cada momento | Imposible por definición: nunca conocés el valor del experimento que no hiciste |
| **De fallas** | Buscar la configuración de perillas donde la policy actual falla **por juicio** (no por ruido) y fabricar el próximo lote de mundos ahí | Imposible: la naturaleza no se adapta a tus debilidades |

**El generador no es una fábrica de tareas: es el stack de feedback completo del método científico.** Eso es lo único que un top lab no puede comprar a ningún precio.

### La hipótesis madre (falsable)

> El juicio investigativo es una habilidad **abstracta**: entrenable en mundos sintéticos con las presiones evolutivas correctas, y **portable** a investigación real.

Probabilidad honesta asignada hoy: ~50/50. Es buena apuesta igual, por **asimetría de pagos**: si la hipótesis falla, el subproducto es el primer eval de juicio investigativo con ground truth formal — algo que los labs quieren hoy y nadie tiene. Cada pelfalla del programa experimental (§6) es publicable por sí solo.

### Las frases que comprimen todo

- *No le enseñamos a investigar: hacemos que investigar sea la única forma de ganar.*
- *Si el agente gana sin investigar, el bug es del entorno.*
- *No corregimos el ensayo: corregimos las apuestas.*
- *NL entra, código sale; la verdad nunca habla en prosa.*
- *La relación presupuesto/complejidad no es un hiperparámetro: es el curriculum.*
- *La honestidad epistémica no es una virtud declarada: es la estrategia óptima bajo el score.*
- *La evaluación es ciega a los motivos: no hay grammar que meta-aprender.*
- *La estructura correcta no es el criterio de evaluación: es la única forma conocida de pasar el criterio.*
- *Las conductas se observan, nunca se premian.*

---

## 2. Ethos — principios innegociables `[ESTABLE]`

1. **La estrategia ganadora debe ser investigar bien.** El objetivo final del proyecto. Todo elemento del entorno — costos, presupuesto, batería, trampas, revelación secuencial — existe para que la conducta de un buen científico sea el óptimo del juego, no una virtud pedida. Corolarios: (a) cuando un agente gana sin investigar, no hizo trampa — **encontró un bug del entorno**, y la respuesta es parchear el juego, no penalizar la conducta; cada hack es un bug report gratis; (b) las conductas observadas en traces son **diagnóstico**; los actuadores del rediseño son las brechas y la economía del juego (§4.6), **jamás rewards conductuales**.
2. **Cero LLM en el camino del reward.** Ningún judge, compiler ni evaluador semántico toca la señal de entrenamiento. Los LLMs son legítimos **en la fábrica** (escribir mundos, vestirlos, filtros de plausibilidad, panel de prior) porque ahí nadie los optimiza en contra. La frontera es **temporal, no ontológica**: ningún LLM puede ejecutarse entre el inicio del episodio y la emisión del reward; todo artefacto de fábrica producido por LLM (mundo, piel, rivales, batería) queda congelado en disco antes del episodio. (Supersede la formulación "ninguna salida de LLM influye en el número que recibe el gradiente", que leída literal era inimplementable — el rival prior-evocado y los mundos escritos por LLM influyen por construcción; ver Decision Log v0.10. El CI la hace cumplir: ARCHITECTURE §13-L0.)
3. **Formalidad solo en los bordes.** Las interfaces formales viven en el I/O: la API del mundo (entrada) y el contrato de submission (salida). El contrato es **conductual, no representacional**: fija la firma y el esquema, jamás la estructura interna de la maqueta. El proceso intermedio del agente es código libre. **Enumerar semánticas** (tipos de pregunta, slots de claims, taxonomías de respuesta) **= regreso al template = muerte.** Lección fundante del compiler v1: el lenguaje formal en el medio, traduciendo significado ajeno sin incentivos de fidelidad, toca techo siempre. Acá el traductor es el agente mismo, traduciendo sus propias creencias a un lenguaje que habla nativamente (código), y la fidelidad de esa traducción es exactamente lo que se le paga.
4. **La evaluación es ciega a los motivos.** El funcional de score no menciona trampas, fenómenos ni tipos. Los motivos existen solo del lado de la generación. Aunque la librería de operadores fuera finita, no habría template de evaluación que aprender.
5. **Diversidad composicional, no catálogo.** La librería son operadores con perillas continuas que se componen sobre familias de mecanismos diversas, no una lista de casos. Quince operadores componibles no son quince casos, como veinte aminoácidos no son veinte proteínas.
6. **El oráculo de valor jamás entra al reward.** Tampoco las firmas de conducta extraídas de traces. Premiar "moverse como el óptimo" o "parecer científico" enseña a imitar la forma de la búsqueda en vez de razonar. Diagnóstico y curriculum, nunca señal de entrenamiento.
7. **Transfer como parte constitutiva del método**, no como anexo. El protocolo sim2real (§6, E4) se diseña junto con el sistema, con controles de cómputo igualado y anti-memorización.
8. **Criterios de muerte explícitos.** Cada experimento lleva escrito qué resultado lo mata. No se testea la droga sin validar el ensayo: primero se demuestra que el score *mide* juicio, después se pregunta si el entrenamiento lo mejora.
9. **Scope honesto: el medio de la ciencia.** Esto entrena inferencia bajo restricciones, diseño experimental, calibración y honestidad epistémica. NO entrena elección de problemas, integración de literatura ni comunicación/persuasión. Es una decisión explícita (la evidencia indica que el "medio" es lo que está roto en los agentes actuales: overclaiming, fabricación, reward hacking), no una omisión. Límite adicional declarado: **techo de universo cerrado** — un mundo sintético contiene solo lo que su programa contiene; el agente puede descubrir todo lo que está en el programa, jamás trascenderlo. Entrenamos los *movimientos* del descubrimiento en universos cerrados apostando a que transfieren al abierto: eso es la hipótesis madre mirada de frente, no un defecto escondido.

### Jerarquía de decisión ante conflictos

1. Integridad del reward > todo lo demás.
2. Apertura del proceso > comodidad de evaluación.
3. Diversidad del espacio de mundos > calidad de un mundo individual.
4. Falsabilidad del programa > elegancia del diseño.
5. Simplicidad > capacidad especulativa.

---

## 3. El diseño en una vista `[ESTABLE]`

```
                    ┌─────────────────────────────────────────────┐
                    │ DESIGNER (búsqueda evolutiva → luego policy)│
                    │ objetivo: maximizar las cuatro brechas      │
                    │ sujeto a: validez + learnability + novelty  │
                    └────────┬───────────────────▲────────────────┘
                             │ genera            │ señales: brechas, varianza
                             ▼                   │ de éxito, perfil de fallas
        ┌────────────────────────────────────┐   │
        │ MUNDO = programa                   │   │
        │   mecanismo                        │   │
        │ + canal de observación             │   │
        │ + proceso de muestreo              │   │
        │ + piel semántica (perilla priors)  │   │
        │ + superficie de control declarada  │   │
        └────────┬───────────────────────────┘   │
                 │ episodio interactivo          │
                 │ (REPL sandbox + budget)       │
                 ▼                               │
        ┌─────────────────────┐  submission  ┌───┴─────────────────────┐
        │ AGENTE              │ ───────────▶ │ SCORE                   │
        │ observe / experiment│  programa o  │ fidelidad distribucional│
        │ python libre / stop │  ensemble    │ en batería secreta      │
        └─────────────────────┘              │ − λ·MDL(programa)       │
                                             └─────────────────────────┘
```

**Cuatro bucles anidados.** (1) El **episodio**: el agente investiga un mundo. (2) El **entrenamiento**: RL sobre episodios. (3) La **coevolución**: el designer automático mueve la distribución de mundos hacia la frontera epistémica de la policy. (4) El **loop maestro**: el bucle externo donde humanos + Claude Code juegan partidas, leen traces y parchean el juego. Los tres primeros son el sistema; el cuarto es **el método de trabajo del proyecto**.

```
LOOP MAESTRO:
  jugar partidas → leer traces (firmas vía oráculo de valor) →
  ¿la estrategia ganadora coincide con buena ciencia?
     sí → escalar diversidad / subir dificultad
     no → localizar el bug del juego → parchear ACTUADORES
          (costos, batería, perillas, revelación, brechas) →
          verificar brechas > 0 → volver a jugar
  Regla de oro: las conductas se OBSERVAN, nunca se premian.
```

---

## 4. Componentes `[EN DEBATE — diseño cerrado a nivel concepto, abierto a nivel spec]`

### 4.1 Mundo = programa

Un mundo es cualquier programa ejecutable que implemente `sample(regime, n, seed) -> tabla`. La verdad **es** el programa. Familias iniciales: SCM (causal estático) y ODE (dinámica); extensible a colas, sistemas multi-compartimento, redes de reacción, agent-based models. El formalismo es un detalle de implementación detrás de la interfaz, no una categoría del sistema.

Todo mundo se descompone en **tres capas** — y esta descomposición es lo que vuelve generativa a la librería de trampas:

| Capa | Qué es | Dónde viven las trampas |
|---|---|---|
| **Mecanismo** | El programa generativo de base (ecuaciones, grafo, dinámica) | Casi nunca |
| **Canal de observación** | Qué se mide, con qué ruido, qué proxies, qué no se ve | Frecuentemente (error de medición, proxies sesgados, latentes) |
| **Proceso de muestreo** | Quién/qué entra a cada dataset, cuándo, por qué | Frecuentemente (selección, colliders, censura, immortal time, missingness informativo) |

**Las trampas viven en las fuentes, no en el mecanismo** (`sources.yaml`: cada fuente observacional declara costo + filtros de muestreo + corrupciones de canal). El agente recibe vistas corrompidas; la corrección corre el mecanismo limpio. Por eso copiar los datos pierde: copiás la corrupción.

**Superficie de control.** Cada mundo **declara** qué perillas externas existen y sus rangos: variables fijables, señales temporales (dosis en el tiempo), reglas/políticas condicionales ("cerrar escuelas si incidencia > X"), cambios estructurales (agregar un servidor), elección de población/época/instrumento. Un **régimen** es un punto de esa superficie + contexto + horizonte. `do(X=x)` es el caso degenerado más simple, **no el primitivo**. Mundos puramente observacionales (cosmología-like): superficie mínima (qué población/instrumento observar) y batería de **contextos held-out** — el forecasting reemplaza a la intervención sin cambiar una línea de la corrección.

**Sin variable target.** La maqueta reproduce la **distribución conjunta** de los observables. Los stakes del brief pesan *condiciones* en la batería; no eligen columnas. Es la diferencia entre un target de ML y un cliente con intereses.

**Piel semántica y perilla de priors.** Cada mundo lleva nombres, dominio y narrativa encima del programa. La **confiabilidad del prior es un parámetro de diseño**: pieles donde el conocimiento de dominio evocado es correcto con probabilidad controlada. Definición operacional: correlación entre lo que un panel de LLMs frescos espera del mundo dado solo el naming, y la verdad del programa. Sin esta perilla, randomizar pieles entrena **nihilismo semántico**; con ella, el agente aprende a *pesar* priors contra evidencia.

**Anatomía de un caso (carpeta):** `world.py` (mecanismo + superficie de control), `sources.yaml` (fuentes, costos, trampas), `brief.md` (narrativa + stakes + ficha técnica), `battery.json` (oculta al agente; ver §4.4).

### 4.2 Operadores epistémicos (la librería que no es catálogo)

Un **operador** es una transformación sobre programas-mundo, con perillas continuas, que introduce estructura epistémica: cirugías de grafo (confounder latente, mediador, feedback), corrupciones del canal (error de medición, proxy, batch effect), filtros del muestreo (selección, censura, immortal time, missingness informativo), no-estacionariedad (regime shift, drift), heterogeneidad latente (subpoblaciones con efectos opuestos), no-linealidades críticas (thresholds, saturaciones, equilibrios), **revelación secuencial** (estructura que solo se vuelve visible tras un hallazgo intermedio; ver brecha de adaptividad, §4.6).

Reglas:

- Los mundos se generan **componiendo 2–4 operadores** sobre un mecanismo base de una familia de dominio, con perillas sampleadas y piel semántica encima. El espacio es combinatorio, no enumerable.
- El **corpus histórico de fallas científicas** (discrepancias observacional-vs-experimento, batch effects, survivorship, replicaciones fallidas, Retraction Watch) NO es el contenido de la librería. Es (a) el **prior** sobre qué composiciones son científicamente significativas, y (b) el **test de cobertura** del set de operadores.
- El set es **abierto**: el designer puede escribir operadores nuevos como código, filtrados por ejecución + validators, archivados si sobreviven. La carrera armamentista contra el "pipeline maestro" (§7) depende de esta apertura.
- **La librería es el alfabeto, no el contenido.** El solver jamás ve la taxonomía (§2.4); la diversidad fenomenológica sale de motor × composición × perillas × piel. **Tres fuentes de generación con roles distintos**: semillas reales (autoridad sobre la estructura), composición+perillas (volumen), búsqueda del designer (frontera — irreemplazable: cubre lo que el corpus documentado estructuralmente no contiene). Los casos con semilla investigativa pasan **test de contaminación** (las semillas famosas viven en el pretraining del solver), con trasplante cruzado de dominio como práctica por defecto. Detalle en `ARCHITECTURE.md` §3–4.

### 4.3 El episodio (el juego interactivo)

**El prompt del agente tiene cuatro bloques** — se le explican todas las reglas del juego, jamás los puntos del examen:

1. **Brief narrativo** con los stakes ("el operador controla X e Y, quiere bajar Z").
2. **Ficha técnica**: esquema de observables (nombres, tipos, unidades — el agente sabe *qué columnas existen*, no cómo se relacionan), fuentes con costos y descripción, superficie de control con rangos (qué es configurable, qué es contexto físico intocable), presupuesto.
3. **Contrato de entrega**: "al terminar, `env.submit(codigo)` donde el código define `model(regime, n, seed) -> tabla` con exactamente estas columnas; `regime` es un punto de la superficie de control; sandbox sin red, timeout, numpy/pandas/scipy/sklearn; podés entregar una lista `[(peso, codigo)]` para sostener hipótesis rivales con incertidumbre".
4. **Aviso de la forma del examen**: será evaluado comparando su maqueta contra el mundo en condiciones no reveladas, cargadas hacia las decisiones del brief.

**La interacción** es un loop estilo Jupyter (kernel persistente): el agente escribe celdas de Python, ve outputs, las variables persisten. Verbos del entorno:

- `env.describe()` — gratis; devuelve la ficha.
- `env.observe(source, n)` — debita según `sources.yaml`; devuelve DataFrame ya corrompido por las trampas de esa fuente.
- `env.experiment(design)` — caro; `design` = población + regla de asignación (puede ser estratificada o condicional: diseño experimental real) + configuración de la superficie de control + horizonte + qué medir, cada pieza con su costo. Corre el mecanismo fresco bajo esa configuración.
- `env.submit(codigo)` — terminal (tras pasar la validación de humo, §4.4).

**Ledger de presupuesto.** El episodio termina por submission o por quiebra. Los costos hacen entrenables el stopping y la eficiencia. La relación **presupuesto/complejidad del mundo es el dial central del curriculum**: presupuesto holgado → gana la fuerza bruta (system identification exhaustiva); presupuesto ajustado → gana la atención selectiva, que es donde vive el juicio. La escasez es además lo que vuelve rentables a las hipótesis: comprimir creencias en mecanismos rivales es lo que hace computable "¿qué experimento conviene?", y la plata solo alcanza para los experimentos que discriminan finalistas.

### 4.4 Submission, batería y score (el corazón — máxima protección)

**La submission.** La respuesta del agente **no se traduce: se ejecuta**. Entrega un programa que define `model(regime, n, seed) -> tabla` con el esquema fijo de observables — o un ensemble `[(peso, codigo)]`, que es literalmente una posterior sobre mecanismos rivales. Los matices de la prosa científica ("creemos X pero no descartamos Y", "esto no es identificable con estos datos") se vuelven **el ancho del ensemble**. El contrato es **conductual**: por dentro puede haber ecuaciones estructurales, un gradient boosting envuelto en generador, un ABM, un híbrido — la libertad es interna, **el borde está clavado**.

**Postura epistemológica — instrumentalismo con dientes.** Lo que se evalúa es la **adecuación empírica bajo todos los regímenes**: identidad conductual con el mundo, no identidad estructural con `world.py`. Dos programas internamente distintos que generan el mismo comportamiento observable bajo toda configuración son equivalentes para el score — que es exactamente lo máximo que la ciencia misma puede reclamar (nadie compara su teoría contra el código fuente del universo; compara predicciones contra mediciones). La estructura importa muchísimo, pero como **medio, no como criterio**: la batería pesa regímenes intervenidos y off-support, donde el comportamiento correcto es en la práctica inalcanzable sin estructura causal correcta en los aspectos que la manipulación toca — no exigimos estructura por decreto, la inducimos por necesidad. Tres razones para no calificar estructura directamente: (a) *epistemológica* — la adecuación bajo regímenes es el criterio de la ciencia real; (b) *práctica* — distancias estructurales tipo SHD castigan parametrizaciones equivalentes, premian parecidos superficiales y reintroducen jueces; (c) *de incentivos* — premiar parecido estructural entrena "adiviná la representación del diseñador" (mímica), premiar comportamiento bajo regímenes adversariales entrena "entendé el sistema como sea que elijas representarlo" (transferible). Corolario sobre el esquema: las **columnas fijan la interfaz, no la ontología** — adentro de `model()` el agente postula los latentes que quiera (el gen de Latent, el electrón: la ciencia siempre inventó lo no-observado detrás de una interfaz de observables fija), y el MDL paga la compresión que los buenos constructos producen. Letra chica honesta: "todos los regímenes" es, en la práctica, "la batería + differential testing" — la garantía vale lo que vale la cobertura (presión #1, ataque #8).

**Validación de humo en el submit** (no es scoring): tres regímenes públicos triviales chequean columnas, tipos, n, timeout. Si falla, el harness **devuelve el error con el episodio abierto** (como un compilador) y el agente corrige y resubmitea. El esquema es obligatorio; las creencias son libres.

**Semántica de bordes:**
- Ignorar una key del régimen = claim implícito de "esa perilla no tiene efecto" — una creencia como cualquier otra, que la batería cotiza.
- Crash o NaN en un ítem de la batería → distancia máxima capeada en ese ítem; los demás siguen.
- Seeds apareados y repeticiones por ítem para que el ruido del propio score no ensucie la señal.

**El score** (literal, no esquemático):

```python
fidelidad = -sum(w_i * D(model(r_i, n=1000, seed=s_i), world.sample(r_i, n=1000, seed=s_i))
                 for w_i, r_i, s_i in bateria)
score = fidelidad - lambda_ * MDL(codigo_submission)     # λ·MDL ≈ 5-10% del rango
```

`D` = distancia distribucional basada en muestras (default candidato: **energy distance**; alternativas MMD, CRPS por marginales). Propia (proper): la honestidad sobre incertidumbre es la estrategia óptima. `MDL` anti **gemelo obeso** (candidato: longitud comprimida del código). **Prohibido para siempre en esta sección**: LLM judges en el cómputo del score; grammars de preguntas; matching semántico de claims.

**La batería secreta = la relevancia, formalizada.** Heredera directa de las GoldQuestions/DiscoveryTargets: mismo rol (codificar qué importa), otra forma (masa de probabilidad sobre regímenes, en vez de texto a matchear). Construcción en design time, algorítmica:

1. **Rivales por receta** (versiones equivocadas-pero-tentadoras del mundo, sin creatividad):
   (a) *ajuste ingenuo generativo*: regresión flexible ajustada a los datos corrompidos del propio mundo, usada generativamente — "lo que creerías analizando ingenuamente"; hereda todas las trampas juntas, gratis;
   (b) *trampa apagada*: la verdad con cada perilla de trampa en off — un rival por trampa instalada;
   (c) *prior evocado*: el mundo que un panel de LLMs frescos espera dado el naming, escrito como programa;
   (d) *rivales por optimización*: familias de aproximadores de capacidad creciente (lineal → boosting → red → híbridos con estructura parcial) ajustadas contra los datos y regímenes accesibles del mundo; la batería pesa donde cada nivel de aproximación falla. Malentendidos **descubiertos por búsqueda, no imaginados por el diseñador** — la mitigación parcial del techo de lo comprensible (ataque #14).
2. **Candidatos**: ~10³ regímenes sampleados de la superficie de control × stakes del brief, con ~20% off-support.
3. **Pesos**: `w(r) ∝ relevancia_de_decisión(r) × desacuerdo_entre_rivales(r)`. Top ~160 + **cola de auditoría** aleatoria (~40, peso bajo) para no dejar puntos ciegos donde ningún rival miró.

Consecuencias: la trivia pesa ~0 (donde todos los rivales coinciden, nada se discrimina); un "descubrimiento esperado" = región de regímenes consecuentes donde la verdad se separa de los rivales; **relevante = aquello que, si lo ignorás, te hace predecir mal donde importa**. Las **dos muertes de la batería**: demasiado angosta → examen cerrado por la ventana; uniforme → la trivia diluye. El diseño vive entre ambas, anclado en stakes + discriminación + randomización.

### 4.5 Los tres oráculos — uso operacional

| Oráculo | Implementación | Uso permitido |
|---|---|---|
| Verdad | `world.sample` sobre la batería + differential testing (búsqueda activa de regímenes de máxima discrepancia) | **Reward** (único) |
| Valor de decisión | EIG aproximado por Monte Carlo sobre el programa, o ensembles de reference solvers | Diagnóstico (firmas, sensor del loop maestro) y curriculum. **NUNCA reward** |
| Fallas | Búsqueda sobre perillas de operadores maximizando fallas-por-juicio de la policy actual | Generación del próximo lote (coevolución) |

### 4.6 Designer, curriculum y las cuatro brechas

Cada brecha es un **certificado computable** de que el mundo ejerce una presión evolutiva específica. Se computan en design time corriendo programas; ninguna requiere juez.

| Brecha | Definición | Qué certifica |
|---|---|---|
| **Mecanística** | score(mejor estrategia mecanística) − score(baseline asociacional FUERTE) | El mundo fuerza investigación (el curve-fitting pierde) |
| **De prior** | distancia entre el mundo evocado por la piel (panel LLM fresco → programa) y la verdad, condicionada a ser recuperable desde la evidencia con el presupuesto dado | El mundo fuerza evidencia > prior; fábrica de move 37 |
| **De adaptividad** | score(mejor política secuencial) − score(mejor diseño batch a presupuesto igual) | El mundo fuerza el loop hipótesis→experimento→actualización (el plan fijo pierde) |
| **De teoría** | score(sin restricción) − score(mejor modelo restringido a funciones de los observables, sin estado latente) | El mundo exige postular entes no-observados — inventar constructos (sin latentes no se puede ganar) |

- El designer **maximiza/filtra por las cuatro brechas** sujeto a: validez (el mundo corre y los fenómenos se materializan — los validators de v1.5 sobreviven acá como constraint set), learnability (varianza de éxito del solver actual) y novelty contra un archivo.
- **Carga diferencial** (filtro previo a todo): cada mundo debe cargar fuerte en al menos DOS de las cuatro coordenadas del feedback (§5.1) — verificador ruidoso, objetivo oculto, canal de evidencia sesgado, sondas caras. Sin esa carga, el mundo es un entorno de math peor y se descarta.
- **Receta para adaptividad**: operadores de revelación secuencial — la anomalía que recién al verla define cuál es la segunda pregunta.
- **Receta para teoría (riqueza latente)**: mundos cuya ontología natural NO coincide con el esquema de columnas — grados ocultos con efectos opuestos, dinámicas latentes, agregados que mezclan poblaciones. El esquema pobre respecto del mecanismo es un requisito de diseño, no una limitación. **Definición afilada (v0.47)**: bajo scoring conductual, la brecha de teoría solo vive en **(i) eficiencia de datos** y **(ii) corrección fuera de rango** — "necesitar teoría" = inferir estado latente mejor con menos evidencia y extrapolar la forma correcta. Corolario de diseño: un latente proxied por un observable limpio (v0) o expuesto como dial declarado (v1) es recuperable por la clase sin-latente; el latente debe ser **estado oculto por-ítem que se INFIERE de una ventana chica** (contrato §10.1 de ARCHITECTURE).
- El **baseline asociacional debe ser fuerte** (regresión flexible + model averaging), no un espantapájaros, o la brecha mecanística se infla sola.
- **Curriculum de sorpresa**: la perilla de priors define la *base rate* — la mayoría de los mundos son aburridos-confirmatorios, los move 37 son raros. La sorpresa se *gana* con evidencia, no se adopta como estrategia (anti-contrarian, ataque #11).
- Filtro de plausibilidad científica ("¿esto parece ciencia o un acertijo gotcha?"): LLM permitido — fábrica, no reward.
- Progresión: **archivo evolutivo primero** (búsqueda sobre perillas, sin gradientes en el designer), designer entrenado como policy después. UED (PAIRED/ACCEL) aplicado por primera vez a estructura epistémica.

### 4.7 El perfil de juicio (el eval — y el caballo de Troya de adopción)

Cada skill tiene su **receta de mundo que lo aísla** y su **métrica formal** (del outcome o del trace vía oráculo de valor). Output: un perfil por skill con ground truth formal. El perfil balancea **escudo** (rigor defensivo) y **espada** (capacidad generativa).

| Skill | Receta de mundo que lo aísla | Métrica formal |
|---|---|---|
| Calibración | Cualquiera | Componente de calibración del proper score |
| Abstención | Estructuras no-identificables dado el acceso | Ancho del ensemble en lo no-identificable vs lo identificable |
| Eficiencia informacional | Presupuesto ajustado | Información ganada por unidad de presupuesto (oráculo de valor) |
| Vigilancia de confounders/colliders | Operadores de muestreo/canal con piel neutra | Delta de score vs baseline asociacional |
| Stopping | Retorno marginal de experimentar colapsa en un punto | Distancia al stopping óptimo (oráculo de valor) |
| Peso de priors | Barrido de la perilla de confiabilidad semántica | Adaptatividad de la conducta al valor real de la perilla |
| Anti-snowballing | Anomalía temprana plantada que invalida el camino obvio | Detección + corrección en el trace |
| **Compromiso contraintuitivo** | Brecha de prior alta + recuperable | **Move 37 rate** (abajo) |
| **Diseño experimental discriminante** | Rivales que solo un experimento bien diseñado separa | EIG realizado / EIG disponible (oráculo de valor) |
| **Actualización / pivoteo** | Revelación secuencial | Delta de política post-anomalía (trace) |

**Move 37 rate** (métrica titular): fracción de mundos donde la submission ganadora del agente había sido calificada de *implausible-dado-el-brief* por un panel de modelos frontier frescos. Sorpresa por correctitud verificada, en un número. El panel opina **antes y fuera** del reward (fábrica).

**Estrategia de adopción (el camino SWE-bench)**: eval primero, training después. Se vende descubrimiento (move 37 rate, perfil), se construye juicio (el motor). El perfil revela agujeros que los labs ya sospechan por vibes; la correlación con sus diagnósticos internos compra la confianza; recién entonces el generador es el único lugar donde entrenar lo que el eval mostró.

**Secuencia estratégica (consecuencia de los ataques #14–15)**: el producto de entrada NUNCA es el training environment — es (1) el **eval** (perfil de juicio + move 37 rate, inmune al problema del mix) y (2) la **demo obs→experimento** (E4): transfer a ciencia real producido por nosotros, a nuestra escala, con nuestro cómputo — la única evidencia que rompe el catch-22 "para adoptar necesito la prueba que solo la adopción genera". El training environment es fase dos, condicionado a esa demo.

---

## 5. Posicionamiento — por qué este hueco existe `[ESTABLE]`

> Embrión de la introducción + related work del paper. Estándar: cada claim defendible con evidencia o argumento estructural, no con entusiasmo.

### 5.1 Las cuatro coordenadas del feedback (por qué math/código no cubren esto)

Todo entorno de RL queda caracterizado por la estructura de su señal. Cuatro ejes:

| Coordenada | Math / código | Investigación |
|---|---|---|
| **Verificador** | Certero: el test pasa o no pasa; el proof-checker es infalible | Ruidoso: una correlación en 400 filas es una pregunta, no un hecho |
| **Objetivo** | Visible: "hacé pasar los tests", "probá este teorema" | Oculto: la verdad es una estructura latente que nadie enunció |
| **Canal de evidencia** | Honesto: un test que falla es un hecho; la semántica del lenguaje no traiciona | Sesgado por construcción: el dataset llegó filtrado por quién entró y quién sobrevivió |
| **Sondas** | Gratis: la política óptima es iterar rápido y a lo bruto | Caras: cada experimento debita presupuesto |

Cada eje presiona skills distintas, y las skills de juicio viven exclusivamente en la columna derecha:

- **Verificador ruidoso** → calibración, saber cuándo la evidencia alcanza, actuar sin certeza. En math nada se actúa sin prueba; en ciencia nada se prueba y hay que actuar igual.
- **Objetivo oculto** → mantener una posterior viva sobre estados del mundo. Es una computación distinta de buscar un camino hacia una meta conocida: math es *search* en un sistema de reglas confiable; ciencia es *inferencia de estado oculto* a través de proyecciones ruidosas.
- **Canal sesgado** → dudar del proceso que generó la evidencia. Presión CERO en math/código: ahí el oráculo es confiable por definición.
- **Sondas caras** → economía de la información, diseño experimental discriminante, stopping. Código entrena el anti-hábito exacto: spam de sondas gratis.
- Transversal: en math/código los priors siempre valen (la semántica de Python no traiciona); el arbitraje prior-vs-evidencia — el músculo del move 37 — jamás se ejercita.

**Regla de diseño derivada — carga diferencial**: un mundo nuestro que no cargue fuerte en al menos DOS de las cuatro coordenadas es un entorno de math peor y no paga su lugar en el curriculum. (Filtro del designer, §4.6.)

### 5.2 El experimento natural (la evidencia de que el isomorfismo se rompe)

La hipótesis rival a este proyecto es: *"math/código ya presionan un loop isomorfo — hipótesis, prueba, backtrack, actualización — y las skills transferirán solas"*. Esa hipótesis ya corrió a escala planetaria: dos años de RL masivo en math/código en todos los labs frontier. Resultado:

- Lo que esas presiones SÍ pueden dar, emergió y transfirió: verificación, backtracking, ejecución procedural (ScienceWorld pasó de <10% a ~80 con el scaling general).
- Lo que su estructura de feedback NO puede presionar, no se movió: investigación abierta (DiscoveryWorld: ~20% en los mejores sistemas vs ~70% en científicos humanos), actualización de creencias ante evidencia (la falla central que mide BoxingGym), y en contextos con métricas gameables el régimen actual entrena hábitos **opuestos**: las auditorías de AI scientists encuentran QRPs emergentes — selección de benchmarks, leakage, mal uso de métricas, selección post-hoc — p-hacking reinventado porque es óptimo bajo reward de completar.

Conclusión: el **loop motor** (la sintaxis ejecutiva de investigar) ya está entrenado; la **capa epistémica** (qué creer, cuánto creerle, qué pagar por saber) no tiene señal en ninguna distribución de entrenamiento existente. Los failure modes documentados son los óptimos de los objetivos actuales.

### 5.3 Vecinos parciales — lo más cercano que existe

| Trabajo | Qué tiene | Qué le falta |
|---|---|---|
| **BoxingGym** (Stanford 2025) | Loop de Box: experimentar en mundos simulados, score predictivo | 10 entornos artesanales; benchmark, no generador; sin RL |
| **Dasgupta et al. 2019** (DeepMind) | Meta-RL que aprende a intervenir en grafitos causales — el juicio experimental es entrenable | Escala juguete, pre-LLM, sin semántica ni mundos ricos |
| **WorldCoder** (2024) | El agente induce modelos de mundo como código y planifica contra ellos | Para eficiencia de planning en juegos; no es interfaz de scoring científico |
| **AZR / SSR** (2025) | Self-play propose-solve con verificación por ejecución | Solo código/matemática; sin mundos, sin investigación |
| **UED: PAIRED, ACCEL, POET, OMNI-EPIC** | La matemática del designer adversarial (regret, archivos, learnability) | Aplicada a laberintos y terrenos, nunca a estructura epistémica |
| **AutoEnv / EnvScaler / OpenReward** (2025–26) | Generación de entornos a escala como infraestructura | Tool-use y web; sin verdad mecanística ni juicio |
| **Rubrics-as-rewards / v1.5-style** | Reward para trabajo abierto vía judge | El judge colapsa bajo optimización — el problema que este proyecto elimina |
| **Simuladores de dominio** (SERGIO, perturb-seq benches) | Verdad = simulador, por dominio | Un dominio cada uno; sin generador ni entrenamiento |
| **Juegos de información oculta** (poker-like RL) | Inferencia de estado latente bajo ruido — el pariente estructural más cercano en UN eje | Sin mecanismos que descubrir, sin canal sesgado, sin análisis de datos |
| **Forecasting RL** (proper scores) | Entrena calibración — otro eje suelto | Sin interacción, sin experimento, sin mecanismo |
| **Debugging salvaje** (heisenbugs, tests flaky) | Evidencia mentirosa *incidental* | Los entornos de entrenamiento la filtran como ruido de infra en vez de abrazarla como contenido; las sondas siguen gratis |

**El hueco**: nadie combina generador de mundos epistémicamente estructurados + interacción experimental con presupuesto + reward 100% ejecutable (sin judge) + coevolución designer-solver. Cada pieza existe; el cruce no. En coordenadas de §5.1: cada vecino cubre un eje suelto; **nadie ocupa la conjunción de los cuatro**.

### 5.4 Oferta, demanda y timing (la forma del hueco)

Dos planos que no hay que confundir — su conjunción es la definición de una oportunidad temprana:

- **Oferta (hueco técnico)**: la señal de entrenamiento para las skills de juicio no existe en ninguna distribución a escala (§5.1–5.3). Real, defendible con evidencia.
- **Demanda (hueco percibido)**: latente, no activada. El lab siente "ya tengo reward verificable" — métricas de ML-engineering (val loss, speedups, MLE/RE-bench) y simuladores de física real. Nuestra diferencia no es verificabilidad a secas: es **mecanismo oculto + trampas epistémicas diseñadas + oráculos** — entrenar descubrimiento, no hill-climbing sobre una métrica conocida. Esa diferencia se *demuestra* (E4), no se afirma. La secuencia eval → demo obs→experimento (§4.7) es el mecanismo que convierte hueco técnico en hueco percibido; si el lab ya sintiera la falta, llegamos tarde.
- **Timing**: no hay foso estructural — un lab puede llenar el hueco in-house el trimestre que decida mirarlo; este documento es el spec. La ventaja es de **anticipación y diseño acumulado**, no de barrera. Corolario operativo: velocidad de la escalera E1→E4 > perfeccionismo de componentes.

---

## 6. El programa experimental — la escalera `[ESTABLE]`

Principio rector: **no se testea la droga sin validar el ensayo.** Orden de barato a caro; cada pelfalla con criterio de muerte explícito; cada pelfalla publicable por sí solo. E2 y E3 son, además, **el sensor del loop maestro**: sus firmas dicen dónde parchear el juego.

La validación es una **pirámide**: los niveles L0–L2 (tests de contrato + sandbox red-team, escalera de verdades degradadas, protocolo de varianza del reward) validan la *maquinaria* y viven en `ARCHITECTURE.md` §13; la escalera E1→E4 de abajo valida el *constructo* (L3) y la *hipótesis* (L4–L5).

### E1 — Validez del instrumento (sin entrenar nada)

Decenas de mundos hechos a mano (dos formalismos) **+ mundos de control sin trampas** (para aislar el confound juicio-vs-ejecución); pasar por ellos modelos frontier existentes. Predicciones y chequeos que deben cumplirse:

1. El spread entre modelos respeta el orden conocido de capacidad de research.
2. **Manipulación de constructo**: el mismo modelo prompteado descuidado/overclaimer se desploma; prompteado metodológicamente prolijo, sube.
3. El score correlaciona con las firmas del trace (información por unidad de presupuesto, vía oráculo de valor).
4. **Mundos de control**: sin trampas, los modelos con buena ejecución convergen; el spread de juicio aparece solo con trampas. El perfil de juicio se reporta *condicional a la ejecución*, y la ejecución por separado (réplica interna del contraste ScienceWorld/DiscoveryWorld).
5. **Baseline humano**: 3–5 personas con formación en causal/estadística juegan ~10 mundos en el mismo REPL. Si los humanos competentes no superan a los frontier, el constructo está en duda.
6. **Validez convergente y discriminante**: los mismos modelos corridos en BoxingGym/DiscoveryBench/QRData — la correlación valida, la divergencia es hallazgo. Discriminante: el perfil debe agregar varianza más allá de un score de capacidad general (correlación parcial).
7. **Auditoría humana de baterías** (obligatoria): por cada mundo, leer los ~10 regímenes de mayor peso y verificar que son científicamente significativos — el único detector confiable de corrupción silenciosa de la relevancia a esta escala.

**Muerte**: si el eval no separa a un agente deliberadamente chapucero de uno cuidadoso, se frena todo — no hay instrumento.

### E2 — ¿Juicio o template?

RL con un modelo abierto mediano. La mirada NO va al score (sube seguro) sino a las **firmas**: ¿sube la información por experimento? ¿mejora la calibración (descomposición del proper score)? ¿aprende a abstenerse en lo no-identificable? ¿pesa priors adaptativamente al mover la perilla? ¿aparecen hipotetizar-discriminar-actualizar en los traces (backtracking, testeo de implicancias, pivoteo ante anomalías)? Diagnóstico de template: secuencias ritualizadas idénticas entre mundos, ganancia concentrada en motivos vistos.

**Muerte (parcial)**: score sube + firmas planas = máquina de templates; el loop maestro parchea curriculum/diversidad/brechas antes de seguir.

### E3 — Abstracción (decisivo y 100% interno — no necesita datos reales)

Entrenar reteniendo **familias enteras de operadores** y hasta **formalismos enteros** (entrenar en SCMs, testear en ODEs/colas). Lo convincente no es el efecto principal sino las dos **interacciones que nuestra propia teoría predice**:

1. El transfer escala con la **diversidad** de operadores de entrenamiento, no con la cantidad de mundos (la memorización predice lo contrario).
2. Las firmas de juicio emergen solo cuando presupuesto/complejidad es ajustado.

**Muerte**: sin transfer entre familias retenidas tras esfuerzo honesto en diversidad → la hipótesis de habilidad abstracta está muerta; queda un benchmark, no un método de entrenamiento. Se dice sin vergüenza.

### E4 — Sim2real (el titular)

- **Eval primario**: pares **observacional→experimento** — datasets observacionales reales cuya verdad la zanjó después un experimento aleatorizado (canónico: un análisis observacional revertido por un experimento posterior; curar casos oscuros y experimentos posteriores al cutoff, renovables en el tiempo). Secundario: predicción de replicación (SCORE / Replication Markets).
- **Anti-memorización**: delta **con-datos vs sin-datos** — si predice el experimento aleatorizado sin mirar el dataset, es memoria; importa cuánto gana por analizar.
- **Controles (cómputo igualado)**: (a) modelo base; (b) RL sobre math/código — el contrafáctico honesto de qué haría un lab con esas GPUs; (c) **ablación del ingrediente activo**: los mismos mundos con reward naive de preguntas fijas estilo v1.5.
- **Puente sin costura**: el agente investiga el dataset observacional real *en el mismo harness* (una fuente, presupuesto) y entrega su maqueta como siempre; predecir el experimento aleatorizado = **consultar la maqueta en el régimen del ensayo**. Cero mismatch de formato entre entrenamiento y demo.

**El número que decide todo**: el delta en obs→experimento contra el control de cómputo igualado.

### Notas de honestidad sobre la prueba misma

- Un nulo a escala chica (ej. 8B) es evidencia débil: el juicio podría "prender" a cierta escala. Mitigación: E1 ya da señal con frontiers sin entrenar; versión intermedia barata: experiencia in-context sobre mundos (sin tocar pesos) como sonda de transfer.
- Un positivo a escala chica con los controles bien hechos ya es enorme.
- Precedente a favor de E2: el RL de matemática con reward de outcome puro hizo emerger verificación y backtracking sin pedirlos; nuestro reward es más denso que un binario.

---

## 7. Modos de falla conocidos y defensas — registro del red-team `[ESTABLE como registro; ampliar siempre]`

| # | Ataque | Mecanismo | Defensa | Estado |
|---|---|---|---|---|
| 1 | **Nihilismo semántico** | Pieles randomizadas enseñan a ignorar todo prior de dominio | Perilla de confiabilidad de priors (§4.1) | Diseñada |
| 2 | **Pipeline maestro** | Un pipeline de sysID reusable scorea alto sin juicio | Presupuesto/complejidad ajustado + brecha de adaptividad + coevolución + operadores abiertos | Diseñada; carrera armamentista, no fix |
| 3 | **Gemelo obeso** | Simulador inflado que predice sin explicar | Término λ·MDL en el score | Diseñada; medir MDL es open question |
| 4 | **Ruido del reward** | Distancias muestrales tienen varianza; RL con reward ruidoso aprende mal | Muchos ítems, seeds apareados, n grande, repeticiones | Estadística conocida; laburo real |
| 5 | **Puntos ciegos de D** | El agente vive donde la distancia elegida no ve. v0.16: en el dummy la energía pesa las marginales y subpesa el joint. **Avistamiento DECISIVO (v0.25, Latent)**: la energía sobre marginales casi no ve multimodalidad a momentos fijos — un oráculo Gaussiano unimodal saca R=0.96 contra una verdad máximamente bimodal → la heterogeneidad latente es invisible al reward. | **Cazado por el certificado ANTES de entrenar** (el `theory_gap_probe` con el control oráculo). **Fix (v0.26): score COMBINADO** = energía + funcionales de decisión declarados en stakes (ARCHITECTURE §9.3) + **certificado de Visibilidad** (§7: toda estructura instalada debe separarse en el reward, o el mundo se rechaza) + el probe como diagnóstico permanente de fábrica (gap energético vs combinado). | **Realizado y mitigado** — el certificado cumplió su función |
| 6 | **Designer gotcha / baseline espantapájaros** | Brechas infladas por mundos-acertijo o baselines débiles | Baseline asociacional fuerte + filtro LLM de plausibilidad (fábrica) | Diseñada |
| 7 | **Leer el código del mundo** | El agente hace `cat` del programa | Handle opaco server-side | Requisito duro de implementación |
| 8 | **Goodhart sobre la batería** | Si la distribución de regímenes es angosta, el template vuelve por la ventana | Randomización rica + off-support + differential testing + cola de auditoría | **Punto de presión #1; vigilancia permanente** |
| 9 | **Inestabilidad RL multi-turno** | Régimen documentado de problemas de estabilidad/generalización | Stack y recetas de la literatura; no innovar acá | Riesgo asumido |
| 10 | **Scope: el medio, no las puntas** | "Mi cuello de botella es elegir problemas/comunicar" | Decisión explícita (§2.9); la evidencia dice que el medio está roto | Asumido y declarado |
| 11 | **Sorpresa fabricada (contrarian)** | Si todos los mundos son raros, el meta es "la respuesta siempre es la contraintuitiva" | Base rate de sorpresa vía perilla de priors; curriculum mayormente confirmatorio; la sorpresa se gana con evidencia | Diseñada |
| 12 | **Goodhart del loop maestro** | Rediseñar hasta que los traces *parezcan* ciencia, en vez de hasta que la ciencia sea óptima | Actuadores = brechas y economía del juego, jamás rewards conductuales; E3 (familias held-out) como control externo | Disciplina declarada (§2.1) |
| 13 | **Cobertura de rivales / rivales débiles** | Malentendidos no encarnados pesan poco; un gemelo inocente degenerado corrompe los pesos de la batería *en silencio* — el sistema corre, los scores salen, la relevancia apunta a cualquier lado | Cola de auditoría + rival ingenuo siempre presente + **escalera de verdades degradadas** (certificado de monotonía por mundo, automático) + **auditoría humana de baterías** en E1 | Punto a vigilar; OQ #11 |
| 14 | **Techo de lo comprensible** | La profundidad efectiva del entorno está acotada por los malentendidos que el diseñador anticipa: discriminación autorada, dificultad inyectada ≠ dificultad emergente; riesgo de destilar la epistemología del generador en el solver | Rivales por optimización (receta d: malentendidos descubiertos por búsqueda, no imaginados) + cola de auditoría + brechas computadas. **Mitigación parcial — límite declarado, no resuelto** | Abierto; el más profundo |
| 15 | **Economía de diversidad / problema del mix** | Millones de episodios aprenden *al generador* (un adversario más débil que la naturaleza); la diversidad significativa está acotada por autoría de familias; al 1% de un mix de RL el delta es inmedible → catch-22 de adopción para training | Producto de entrada = eval + demo obs→experimento (transfer evidence producida por nosotros); familias paramétricas + operadores abiertos; training = fase dos | Estratégico; redefine la secuencia de adopción |
| 16 | **Contaminación por fama de la semilla** | Las semillas documentadas viven en el pretraining: el solver recupera la moraleja de memoria sin investigar — el modo con semilla, en su versión más fiel, viola la invariante "forzar investigación" | Test de contaminación obligatorio (brecha de prior > umbral para casos investigativos con semilla) + trasplante cruzado de dominio por defecto + tasa de novedad estructural como métrica de salud del pipeline | Diseñada |
| 17 | **Confound juicio-vs-ejecución** | El instrumento mide saber pandas, no juicio: un modelo torpe con herramientas scorea bajo aunque juzgue bien | Mundos de control sin trampas + perfil condicional a la ejecución + baseline humano (E1.4–5) | Diseñada |
| 18 | **El juez vuelve por la puerta de atrás** | En implementación, la tentación de "que un LLM chequee si la submission es razonable" en algún rincón del scorer | **Test de CI cero-LLM en el reward path**: el build falla si se viola — disciplina convertida en código | Regla de CLAUDE.md |
| 19 | **Ergonomía diferencial del contrato** (primo del #17) | Una fricción model-family-specific (p.ej. una elección de RNG legítima que el instrumento no tolera) se disfraza de spread de juicio: el modelo crashea en silencio → D_MAX → R=0, indistinguible de "juzgó mal". **Avistado empíricamente** (Decision Log v0.16: DeepSeek con `np.random.seed` legacy + seeds de 64 bits) | Smoke con seeds/regímenes representativos (hecho); **breakdown crash-vs-distancias-honestas POR MODELO como default del reporte**; conformance separado de juicio en E1 | Diseñada; vigilar |

---

## 8. Relación con SREG v1.5 — qué sobrevive, qué muere `[ESTABLE]`

| Pieza de v1.5 | Destino | Por qué |
|---|---|---|
| **Presiones evolutivas + test de diseño operativo** (`PROJECT.md`) | **Sobrevive como ALMA del proyecto** | Ahora es el objetivo final (§1), operacionalizado con las tres brechas computables |
| Pipeline Digestion → Architect → Validators | Sobrevive entero (porteo deliberado) | Es el compilador de mundos; el activo que el campo está descubriendo que vale oro |
| Maquinaria anti-leak (capsule, forbidden_phrases, writers ciegos) | Sobrevive | La frontera de información sigue siendo crítica (brief no ve batería) |
| Runtime `python_exec` / kernel Jupyter persistente | Sobrevive y se extiende | Base del REPL interactivo con env handle |
| Contratos Pydantic (WorldSpec, IntendedPhenomenon, ValidatedPhenomenon) | Sobreviven adaptados | El mundo-como-programa los necesita |
| Validators por fenómeno | Sobreviven como **constraint set del designer** | De árbitros de scoring a filtros de validez |
| Compiler NL↔IR | Muerto (ya estaba) | Lección fundante: formalidad en el medio toca techo |
| Evaluator LLM-judge como reward | **Muere** | Principio §2.2 |
| Framing single-turn (CSV + brief) | Muere | El episodio es interactivo con presupuesto |
| GoldQuestions / DiscoveryTargets como interfaz de scoring | **Reencarnan** como masa de la batería | Un "descubrimiento esperado" = región de regímenes consecuentes donde la verdad se separa de los rivales (resuelto, ver Decision Log 2026-06-10) |
| Rubrics + answer keys | Mueren en el reward path | Posible uso diagnóstico secundario, nunca señal |

---

## 9. Glosario

- **Superficie de control**: las perillas externas que un mundo declara (variables fijables, señales temporales, políticas condicionales, cambios estructurales, elección de población/instrumento) con sus rangos.
- **Régimen**: un punto de la superficie de control + contexto + horizonte. `do(X=x)` es su caso degenerado más simple.
- **Submission**: el modelo del mundo entregado por el agente como programa ejecutable `model(regime, n, seed) -> tabla` (o ensemble pesado = posterior sobre mecanismos). Contrato **conductual**: borde clavado, internals libres.
- **Batería secreta**: lista pesada de regímenes held-out construida en design time (rivales × stakes × desacuerdo + cola de auditoría). Es la **relevancia formalizada** y la reencarnación de los DiscoveryTargets.
- **Rivales**: versiones equivocadas-pero-tentadoras del mundo, generadas por receta (ajuste ingenuo, trampa apagada, prior evocado, optimización por niveles de capacidad). Definen dónde discrimina la batería.
- **Brecha mecanística / de prior / de adaptividad / de teoría**: certificados computables de que el mundo fuerza investigación / evidencia sobre prior / el loop secuencial / la invención de constructos latentes. §4.6.
- **Adecuación empírica**: el criterio de verdad del juego — replicar el comportamiento de los observables bajo todos los regímenes (en la práctica: batería + differential testing). Identidad conductual, no estructural; la estructura es el medio inducido, no el criterio.
- **Cuatro coordenadas del feedback**: ejes que caracterizan la señal de un entorno de RL — verificador (certero↔ruidoso), objetivo (visible↔oculto), canal de evidencia (honesto↔sesgado), sondas (gratis↔caras). Math/código ocupan una esquina; la investigación, la opuesta. §5.1.
- **Carga diferencial**: requisito de que cada mundo cargue fuerte en ≥2 coordenadas diferenciales; filtro previo del designer. Sin ella, el mundo no paga su lugar en el curriculum.
- **Move 37 rate**: fracción de mundos donde la submission ganadora había sido calificada de implausible por un panel frontier fresco. Sorpresa por correctitud verificada.
- **Loop maestro**: el bucle externo del proyecto — jugar, leer traces, parchear el juego hasta que buena ciencia = estrategia óptima. Conductas se observan, nunca se premian.
- **Oráculo de valor**: cuánta información valía cada acción posible (engine de ajedrez para experimentos). Diagnóstico/curriculum, jamás reward.
- **Differential testing**: búsqueda activa de regímenes de máxima discrepancia entre submission y mundo.
- **Gemelo obeso**: submission que predice bien sin explicar; se castiga con MDL.
- **Pipeline maestro**: estrategia reusable de fuerza bruta que scorea sin juicio; se combate con escasez, adaptividad y coevolución.
- **Nihilismo semántico**: ignorar todo prior de dominio; efecto colateral de randomizar pieles sin perilla de priors.
- **Validación de humo**: chequeo de esquema/timeout en el submit; devuelve errores con el episodio abierto. No es scoring.
- **Las puntas / el medio**: elección de problemas y comunicación (puntas) vs inferencia, diseño experimental y honestidad (medio). Este proyecto entrena el medio.

---

## 10. Open Questions (inbox vivo) `[EN DEBATE]`

1. **Sampler de configuraciones por formalismo** — el punto de presión #1: cómo parametrizar la superficie de control y el sampler de regímenes candidatos por familia (qué es una configuración razonable en ODEs no lo es en colas), manteniendo riqueza + off-support sin absurdos ni Goodhart.
2. **Formato del ensemble y scoring estocástico**: cuántos programas, cómo se pesan, energy distance vs MMD vs CRPS por marginales, n de muestras y repeticiones para varianza aceptable del reward.
3. **MDL en la práctica**: medida de complejidad del programa entregado (longitud comprimida, parámetros, AST); λ fijo o por curriculum.
4. **Set mínimo de operadores para E3**: cuántas familias hacen falta para que el held-out de familias sea un test honesto de abstracción.
5. **Handle opaco**: arquitectura concreta (proceso separado, RPC, contenedor) sin matar la latencia del REPL.
6. **Unidades de presupuesto**: ¿costo en unidades abstractas, muestras, acciones? ¿El cómputo del agente (tokens) cuenta o solo el costo de datos?
7. **Stack de RL multi-turno**: elegir receta existente (no innovar acá).
8. **Pares obs→experimento**: curaduría concreta — fuentes, criterios de oscuridad anti-memoria, reconstrucción de datasets.
9. ~~Naming del proyecto~~ **RESUELTA (v0.6)**: WAGER = *Worlds As Generators of Epistemic Reward*. Suites de mundos con nombres de científicos arquetipo: Horizon (observacional puro), Anomaly (anomalías), Latent (constructos latentes), Prior (prior vs evidencia). Ver Decision Log.
10. **Firmas de conducta estandarizadas**: qué métricas de trace son robustas entre formalismos, como sensor del loop maestro (hipotetiza/discrimina/actualiza, legibles sin juez).
11. **Cobertura de rivales**: cómo medirla y garantizarla; ¿generación adversarial de rivales además de las tres recetas?
12. **Gramática de `experiment(design)`**: formato mínimo por familia de formalismo sin recrear un DSL semántico (el design describe el experimento, no las creencias).
13. **Baseline sin-latentes para la brecha de teoría**: cómo aproximar en la práctica "el mejor modelo restringido a funciones de los observables" (¿aproximadores flexibles entrenados solo sobre columnas? ¿con qué acceso a datos/regímenes se lo construye para que sea fuerte y no espantapájaros?).
14. **Proto-designer con yield como métrica (Lucas, 2026-07-05 — "sin generación automática el proyecto no tiene valor")**: la mitad VERIFICADORA del designer ya existe (rivales/batería/certificados derivan mecánicamente del meta; los gates son cero-LLM) — falta la mitad GENERADORA (world.py + brief + meta desde una composición declarada; LLM permitido, es lado fábrica). Hito propuesto: generar los próximos slots de la matriz vía proto-designer y medir el **yield** (fracción de mundos generados que pasan la certificación completa sin cirugía humana). Riesgos a resolver: writer del brief ciego (anti-leak, ya doctrina), contaminación, y que el generador no colapse a variaciones triviales del mismo mundo.
15. **Diseño de la información mid-trayectoria (Lucas, 2026-07-05)**: hoy la interacción es 100% pull (el solver compra; el mundo jamás empuja) y la verdad es estática durante el episodio — el único "pivot" que testeamos es el que nace de los propios datos comprados. ¿Qué eventos/revelaciones a mitad de episodio (artefactos PRE-escritos y ciegos, jamás LLM en runtime) harían medible la skill de actualizar/cambiar de opinión? Conecta con la suite Prior (prior evocado vs evidencia), el campo `horizon` (drift), y las firmas de conducta (#10 de esta lista). Evidencia fresca de que la superficie de interacción importa: presupuesto→profundidad de razonamiento (v0.65) y la semántica un-lote-por-llamada (v0.64-e).
16. **Mundos dirigidos a failure modes documentados (Lucas, 2026-07-05 — semillas conductuales)**: atacar a propósito los modos de falla conocidos de agentes-investigadores, diseñando mundos donde caer en el modo de falla tiene PRECIO en R (el examen cero-LLM cobra la consecuencia; la conducta se OBSERVA por firma de trace, jamás se premia — §2.1/§2.6 intactos). Lista de semillas (notas de Lucas, investigación de agentes): no actualizar ante evidencia contraria / quedarse con la primera hipótesis / no procesar feedback negativo; rabbit holes y loops de mas-de-lo-mismo sin pivotear; "encontró un error y deja de buscar" (¡ya instanciado: mundo 3, predicción "collider atrapado, deconvolución omitida"!); perseguir lo significativo-pero-irrelevante; claims excesivos y "verified" sin verificar; drift de implementación hacia lo simple/familiar (ya instanciado: v2, retirada a marker_conditional = R 0.096); atarse a decisiones de POC olvidando la visión; perder restricciones/contexto en trayectorias largas + degradación monótona de la recuperación de errores; no registrar información que llega a mitad de camino. **Patrones de trampa candidatos** (cada uno = operador/evento con consecuencia en R + firma mecánica): reversión de evidencia (fuente barata cuenta X convincente, fuente cara/evento revela Y; el examen cobra Y), profundidad señuelo (sub-puzzle seductor en columna decoy que no paga nada, bajo presupuesto escaso), N-trampas con saciedad (hallar la 1ª satisface; las demás quedan), carnada de significancia (efecto chico-pero-significativo como bait vs grande-pero-ruidoso load-bearing — la doctrina significancia≠magnitud v0.38 hecha mundo), restricción de enlace tardío (declarada temprano / cobrada al final; o actualizada mid-episodio), retirada a arquitectura familiar (la escalera sin-latente YA es esto; falta el diagnóstico mecánico "rung más cercano a la submission"). Conecta #14 (el proto-designer gana un OBJETIVO: generar mundos que maximicen elicitación del failure mode F pasando certificación) y #15 (eventos push). Decisión pendiente de Lucas: ¿re-orientar los slots restantes de la matriz E1 a cobertura de failure modes?
17. **Aprendibilidad / borde de capacidad (Lucas, 2026-07-05 — "si son demasiado difíciles no hay forma de entrenarlos")**: un mundo donde TODOS los rollouts puntúan igual (todo ~0 o todo ~1) da gradiente CERO — el valor de entrenamiento exige VARIANZA dentro de la distribución de rollouts de la policy actual. Distinción eval-vs-training: para el benchmark (E1) "ningún frontier lo resuelve" es exactamente el titular (headroom, anti-saturación); para RL (E2) el borde se ingenia a nivel CURRICULUM, no haciendo cada mundo borderline. Piezas que ya existen: R continuo (crédito parcial por construcción, no pass/fail), techo-alcanzable certificado (v0.47), perillas de dificultad por mundo (n_cal, marker_noise, presupuesto — v0.65), y el tríptico v0→v1→v2 RELEÍDO como rampa curricular (v0/v1 no son mundos fallidos: son los peldaños bajos del concepto que v2 fuerza). Lo que FALTA (propuesta a decidir): **certificado de aprendibilidad** — gate de entrada al set ACTIVO de entrenamiento: N rollouts de la policy en entrenamiento deben mostrar spread (std(R) > umbral); mundo sin spread queda en el "estante frontera" (solo eval) hasta que la policy crezca o sus perillas se ablanden; y regla "cada mundo difícil declara sus perillas de ablandamiento". Nota empírica: v2 consolidado YA muestra la estructura deseable para policies clase-frontier (bimodal 0 vs 0.62-0.67 = varianza; muro 0.67→1.0 = escalón conceptual con crédito parcial disponible); para la policy abierta de 4-8B de E2 el borde estará mucho más abajo (los controles pueden SER su borde) — se descubre empíricamente al arrancar E2.

---

## 11. Decision Log

El Decision Log (fundación v0.1 → última entrada) vive en **`DECISION_LOG.md`** —
movido desde acá en la reestructura de docs (v0.69) para mantener esta constitución
concisa. Es **append-only**: la guardia `scripts/check_decision_log.py` (pre-commit) y
los lints de header protegen ese archivo. La versión vigente está en **Estado** (arriba).
