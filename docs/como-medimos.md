# Cómo medimos — registro y reflexión sobre métodos de MEDICIÓN del juicio

> **Por qué existe este doc (Lucas, 2026-07-10).** El problema más difícil e importante del proyecto
> es **CÓMO MEDIR**: cómo medimos cada vicio, cómo medimos los aha / las formas de generar ideas e
> hipótesis. Cuando aparece un paper que MIDE alguna de estas cosas, acá anotamos **cómo lo mide** (el
> método concreto, no el hallazgo — el hallazgo va a `lectura-de-fuentes.md`) y **reflexionamos** sobre
> qué podemos robar, qué evitar, y qué nos dice sobre nuestra propia medición.
>
> **La distinción que ordena todo: MEDIR-PARA-DESCRIBIR vs MEDIR-PARA-PREMIAR.**
> - *Describir* (caracterizar una población, un modelo, una distribución): un juez-LLM VALIDADO
>   está bien — no hay presión de optimización que lo engañe, porque nadie entrena contra él.
> - *Premiar* (dar reward para entrenar/rankear): **debe ser cero-LLM** — bajo presión de
>   optimización, cualquier juez-LLM se gamea (se actúa la forma sin el fondo). Esta es la regla dura
>   de WAGER.
>
> Casi todos los papers de la literatura miden PARA DESCRIBIR. WAGER mide PARA PREMIAR. Por eso muchos
> métodos lindísimos de la literatura NO se pueden portar al reward path — pero **sí** se pueden usar
> como instrumento DESCRIPTIVO para VALIDAR que un mundo elicita el vicio (off-reward). Tenerlo claro
> evita dos errores: copiar un juez-LLM al reward (prohibido), y descartar un método útil solo porque
> usa un LLM (sirve para describir/validar, no para premiar).

---

## 1. Chen, Zhao & Cohan 2026 — "Measuring the Gap..." (2607.01233) — cómo midieron la generación de ideas

**Qué miden**: no la calidad de UNA idea, sino la **distribución de "movidas de investigación"** que
un modelo produce vs la que producen los humanos, sobre el mismo contexto. Es medición de *generación
de ideas/hipótesis* — justo el polo aha que a nosotros nos cuesta puntuar.

### El método, paso a paso (la anatomía de la medición)

1. **Anclaje al MISMO input (el truco de comparabilidad)**: por cada paper humano real, reconstruyen
   4-8 trabajos previos que "razonablemente precedieron" a la idea (de la sección related-work del
   paper), y dan SOLO esos títulos+abstracts como input. La idea HUMANA = la que realizó el paper; la
   idea LLM = la que el modelo genera desde ese mismo contexto. Así, cualquier diferencia no es por
   elegir otro tema — es por **cómo cada uno enmarca el hueco y construye la contribución**.
   → *espejo de lo nuestro*: nosotros anclamos naive/canónico/agente al MISMO mundo. Misma jugada de
   comparabilidad, distinto objeto.
2. **Descomponer la salida en partes estructuradas**: cada idea = (motivación, método). No prosa
   libre: dos casilleros. → *espejo*: nuestra submission es un programa con contrato (estructura fija).
3. **Etiquetar con una TAXONOMÍA de 2 ejes, construida con rigor** (esto es lo más transferible):
   - *Opportunity Pattern* (POR QUÉ vale la idea; 7 etiquetas): puzzle/contradicción · hueco de
     explicación · desajuste de alcance · hueco de evidencia · **oportunidad-puente** · hueco de
     falla/riesgo · cuello de botella de recursos.
   - *Method Paradigm* (CÓMO se convierte en contribución; 7 etiquetas): **síntesis/unificación** ·
     relajar/extender alcance · robustificación · derivación formal · mapeo empírico · artefacto/
     sistema · optimización/búsqueda.
   - **Cómo construyeron la taxonomía** (la receta de rigor): partieron de las guías de formulación de
     proyectos de **NSF, NIH, AHRQ y DARPA** → 11 patrones + 9 métodos iniciales → los **refinaron
     sobre 150 papers held-out** (hasta 2 etiquetas por eje + "otro"; fusionaron duplicados, separaron
     etiquetas que mezclaban motivación con método, sacaron las atadas a un dominio) → final 7×7. Tres
     requisitos: que sean marcos recurrentes, generalizables entre dominios, sin colapso sistemático
     de categorías.
4. **Anotador automático = un LLM, VALIDADO contra humanos** (el punto clave de método, y el límite):
   GPT-5.4-mini recibe la taxonomía + el contexto + (motivación, método) y devuelve etiqueta primaria
   y secundaria por eje + scores. **Validación**: sobre los 150 held-out, dos autores auditaron;
   **Cohen's κ entre el LLM y cada humano = 0.84, 0.81, 0.93** (acuerdo alto); revisaron matrices de
   confusión para asegurar que los errores caen en etiquetas ADYACENTES, no en colapso de categorías.
   → *acá está la línea*: es un JUEZ-LLM. Legítimo porque MIDE-PARA-DESCRIBIR (nadie entrena contra
   él) y está validado. **NO portable a nuestro reward** (se gamearía). SÍ portable como instrumento
   descriptivo para validar mundos (ver §2).
5. **Métricas DISTRIBUCIONALES, no puntuales** (la lección grande para nosotros): por cada modelo y
   eje estiman la distribución empírica de etiquetas y la comparan con la humana con **TVD** (cuánta
   masa de etiquetas habría que mover para igualar al humano), **JSD** (divergencia acotada simétrica)
   y **entropía normalizada** (qué tan concentrado está — bajo = pocos movimientos repetidos). El
   argumento explícito: *"una sola idea puede parecer novedosa y coherente, mientras que el conjunto
   de ideas de la misma fuente refleja un rango angosto de taste."*
6. **Análisis de mecanismo (cómo abren la caja)**:
   - *Archetype clustering*: reescriben cada propuesta a una frase-arquetipo de una línea (un LLM,
     abstrae el dominio), la clusterizan (TF-IDF + MiniBatchKMeans, k=30) y **normalizan el verbo
     principal a una "familia de operación"** (integrar, unificar, reemplazar, desacoplar,
     formalizar...). Después: log-odds modelo-vs-humano por operación (integrar 34.2% vs 2.35% →
     log-odds 3.07). → una forma de medir "¿QUÉ MOVIDA hizo?" desde salida libre.
   - *Representación*: embeddings compartidos (Qwen3-Embedding-4B) → similitud modelo-modelo 0.83 vs
     humano-modelo 0.72-0.78 (los modelos se parecen entre sí más que a un humano), + una métrica de
     cuán difusamente se posiciona la propuesta respecto de sus trabajos previos.
7. **Scores diagnósticos ordinales (0-3)** del anotador: *surface stitching* (¿es combinación
   superficial?), **bottleneck specificity** (¿identifica el mecanismo/factor limitante preciso?),
   *boilerplate* (fraseo genérico). → conceptos medibles que nos importan, aunque acá salgan de un LLM.

### Reflexión — qué nos enseña sobre CÓMO MEDIMOS

- **Robamos: pensar DISTRIBUCIONALMENTE.** Nuestra crisis de la semana (medianas de n=8 son ruido, la
  varianza corrida-a-corrida ahogó la señal) es EXACTAMENTE lo que este paper resuelve mirando la
  distribución completa, no puntos. Para el próximo control de resolubilidad con pistas y para E1: reportar
  **distribuciones de R + tasas con intervalos**, no medianas sueltas; y pensar el perfil de un modelo
  como una **distribución de movidas/firmas** entre muchos mundos, no un número por mundo.
- **Robamos: la receta de taxonomía con rigor.** Nuestra taxonomía de vicios/ahas se construyó de
  papers; su método (fuentes autoritativas → refinar en held-out → validar con κ contra humanos → sin
  colapso de categorías) es un estándar que podemos adoptar/citar cuando formalicemos la nuestra.
- **Robamos (para DESCRIBIR, no premiar): la abstracción a "familia de operación".** Medir "¿qué
  movida hizo el agente?" (integrar vs desacoplar vs reemplazar) desde su traza/entrega, con un LLM
  anotador OFF-reward, es una forma legítima de **validar que un mundo elicita el vicio** — sin tocar
  la nota. Es el complemento descriptivo de nuestro certificado (que es operacional).
- **La diferencia de fondo: MOVIDA vs CONSECUENCIA.** El paper mide la movida upstream (qué idea
  proponés) directamente del texto. WAGER mide la consecuencia downstream (¿tu modelo reproduce el
  mundo en regímenes no vistos?). Son complementarios: ellos ven "sobre-produce síntesis" sin correr
  ningún experimento; nosotros vemos "su modelo se cae fuera de soporte" sin nombrar la movida. El
  ideal a futuro: **medir las dos** — la consecuencia con el reward cero-LLM (para premiar), la movida
  con un anotador descriptivo (para validar/diagnosticar que el mundo pega donde debe).
- **Lo que NO copiamos: el juez-LLM en la nota.** Toda su medición pasa por un LLM (anota las
  etiquetas, extrae la idea humana del paper, reescribe los arquetipos). Impecable para describir una
  población; imposible para nuestro reward. Es la confirmación por contraste de por qué WAGER es
  cero-LLM: ellos pueden porque nadie optimiza contra su anotador.
- **Un caveat honesto de su método** (no es crítica destructiva, es límite): la "idea humana" también
  la extrae un LLM del paper, y las etiquetas las pone un LLM. Validaron con κ alto, pero la medición
  es LLM-mediada de punta a punta. Para nuestra tesis eso refuerza el valor de tener AL MENOS un lado
  (la nota) que no dependa de ningún LLM.

---

## 2. Implicancia para WAGER — CÓMO medimos cada cosa (el marco, informado por lo de arriba)

- **Cómo medimos un VICIO (hoy, operacional/reward)**: mundo donde la jugada viciosa tiene una
  consecuencia perdedora → la entrega ejecutable se puntúa contra el mundo verdadero en regímenes
  no mostrados → R baja = **fracaso funcional**, no diagnóstico automático del vicio. La ficha de
  trayectoria y los controles causales localizan qué falla lo produjo. R por episodio además puede
  ser ruidoso: se informa distribucionalmente (tasa de caída, no solo mediana).
- **Cómo medimos un AHA (hoy)**: mundo donde la operación-aha es necesaria para superar el techo
  del rival incremental. Llegar arriba prueba que la **consecuencia funcional** fue capturada; no
  demuestra por sí solo qué idea expresó ni qué representación interna usó. La ficha registra por
  separado generación abductiva expresada y realización. *Lo que el paper agrega*: una forma de
  describir la movida generativa a nivel distribución, siempre fuera del reward.
- **Regla aprendida en D2: premiamos la CONSECUENCIA del salto, no su nombre.** Si un programa sin
  la estructura declarada reproduce todo lo que el mundo puede observar, la nota no puede distinguirlo
  del salto. Eso no prueba que el agente vaya a encontrar esa alternativa; prueba que el reward no
  aísla el constructo. Leer palabras o reconocer una forma dentro del código sería frágil y gameable.
  Por eso el mundo debe hacer que el salto cambie predicciones conjuntas, repetidas o bajo intervención,
  y la nota se ancla contra la mejor familia optimizada que no hace el salto objetivo. Un descriptor
  de forma como `has_mixture` puede servir para autopsia, no como prueba primaria de que hubo dos grupos.
  [El control que destapó el problema](research/2026-08-11-ficha-mundo-d2-decision.md#81-el-salto-todavía-no-paga-contra-un-rival-fuerte).
- **La pregunta abierta que este doc deja viva**: ¿cuál es el instrumento DESCRIPTIVO cero-costo-de-
  gaming que valida que un mundo pega donde debe? Candidatos: (a) la idea nombrada como pregunta de
  diseño y control de resolubilidad —no una subpregunta científica—; (b) modelos testigo que comparan
  salto vs mejor rival sin salto; (c) un anotador de movidas off-reward estilo §1.6. Los tres son descriptivos;
  ninguno toca la nota. Elegir/combinar es trabajo de diseño.

### 2.1 Protocolo v1 — validar el caso y leer la trayectoria del agente

> **Primera versión de trabajo, 2026-08-14.** Se aplica primero de manera retrospectiva a
> **Perfiles persistentes** y se modifica si esa prueba muestra ambigüedades. La primera aplicación
> es exploratoria: no convierte una rúbrica nacida después de la tanda en endpoint pre-registrado.

Hay dos preguntas distintas y una prueba-puente:

1. **¿El caso está bien construido?** El salto debe ganar, la evidencia debe ser alcanzable y la
   nota debe reconocer la consecuencia correcta.
2. **¿El agente puede resolverlo si la idea ya está disponible?** Es capacidad condicionada, no
   creatividad espontánea.
3. **¿Qué hizo el agente sin ayuda y dónde se rompió su investigación?** Es la pregunta científica.

Una misma partida puede informar varias de estas preguntas. La regla es simple: **solo el contenido
exactamente regalado se marca `N/A`, nunca como logro del agente**. Una partida con “dos tipos”
nombrado no mide la aparición espontánea de esa familia, pero sí puede medir cómo la concreta y si
deduce, prueba, selecciona e implementa algo que la pista no suministró. Cada mundo declara además
qué eslabones realmente instancia; lo ausente queda `N/A` incluso en la condición sin ayuda.
Si esa partida se usa para cambiar el mundo, la frase o la rúbrica, queda como descubrimiento
exploratorio y no se reutiliza como confirmación fresca.

#### A. Batería para validar el caso

| Compuerta | Pregunta concreta | Implementación mínima |
|---|---|---|
| **Salto definido** | ¿Qué cambio de forma buscamos y qué consecuencia observable lo delata? | Firma funcional congelada; el texto o el nombre de una clase nunca deciden la nota. |
| **Ventaja real** | ¿El salto supera claramente al rival más fuerte que no lo realiza? | Optimizar adversarialmente la clase rival declarada y comparar ambos sobre examen sellado. Congelar el margen mínimo antes de agentes. |
| **Evidencia alcanzable** | ¿Existe una campaña legal, dentro del presupuesto, que los separa? | Buscar offline sobre las acciones permitidas y correr un investigador mecánico que use solo información legal. La acción óptima no se le entrega al agente. |
| **Ventaja visible desde adentro** | ¿Con lo que podría observar el agente se puede demostrar que el modelo viejo no alcanza? | Comparar los rivales sobre evidencia legal o predicciones registradas, no solamente sobre el reward oculto final. |
| **Nota e interfaz sanas** | ¿La verdad puntúa alto, el rival pierde y la basura no pasa? | Robots/testigos: solución, rival fuerte, modelo sin datos y modelos basura; aceptar cualquier programa funcionalmente equivalente. |
| **Capacidad condicionada** | ¿El mismo agente puede investigar y construir la solución si le nombramos la idea? | Pocas partidas frescas, frase y gate congelados; sin fórmula, parámetros, experimento decisivo ni código. Debe superar el rival fuerte y el contraste neutral debe dejar una brecha funcional material. Solo el contenido suministrado queda `N/A`. |

La **solución servida** queda debajo de esta batería como control de techo: detecta fallas de
sandbox, contrato o scorer. No valida descubrimiento ni capacidad investigativa completa.

#### B. Qué puede medir cada condición con agente

| Condición | Qué queda medible | Qué queda anulado por la ayuda |
|---|---|---|
| **Sin ayuda** | Todos los eslabones que el mundo y la tarea realmente instancian | Nada; los eslabones ausentes del host siguen `N/A` |
| **Evidencia discriminante servida** | Notar, generar, probar, elegir y realizar | Adquisición de esa evidencia |
| **Desajuste explícito**: “predijiste X; ocurrió Y” | Respuesta al impasse, generación posterior y realización | Detección espontánea del fallo |
| **Pedido de alternativas estructurales** | Qué candidato genera bajo presión de reabrir | Decisión espontánea de reabrir el menú |
| **Idea nombrada** | Elaboración no suministrada, deducción, test, selección y realización | Aparición espontánea de la familia exactamente nombrada |
| **Comparación exigida** | Ejecución e interpretación de un contraste justo | Decisión espontánea de comparar |
| **Ayuda técnica o solución servida** | Implementación, interfaz y propagación | Los pasos conceptuales regalados |

Esto no se llama automáticamente “ablación”. Una ablación quita una pieza de un sistema completo.
Acá normalmente **agregamos una intervención por vez**; el nombre de la casa es **control de
capacidad** cuando valida resolubilidad y **fork diagnóstico** cuando localiza causalmente una
falla desde el mismo estado previo.

La diferencia de puntaje entre “idea nombrada” y “sin ayuda” es una **brecha funcional de ayuda**.
No es, por sí sola, una “prima pura de descubrimiento”: la ayuda puede cambiar atención, búsqueda,
testeo, selección e implementación además de poner una idea en el menú.

#### C. Ficha de trayectoria por partida

La salida no es una nota total. Es un **perfil de eslabones**, porque creatividad, rigor e
implementación pueden separarse. Cada mundo declara cuáles puede medir. Cada casillero usa
`sí / no / incierto / N/A`; los campos cuantitativos conservan además su valor continuo.

| Eslabón | Qué se registra | Tipo de evidencia |
|---|---|---|
| **1. Evidencia** | Si existía evidencia discriminante y si el agente la adquirió | Mecánica: acciones y datos vistos |
| **2. Grieta** | Si su modelo vigente quedó objetivamente en tensión y si el agente lo expresó | Tensión mecánica + cita descriptiva |
| **3. Creatividad** | `sin señal observable` · `evocación genérica` · `hipótesis estructural específica` · `candidato estructural ya construido` | Traza para lo expresado; artefacto ejecutable para lo construido |
| **4. Puesta en juego** | Si trató la hipótesis como rival vivo en vez de matarla al mencionarla | Plan, modelo candidato o criterio explícito para hacerla ganar/perder |
| **5. Desarrollo** | Si derivó una consecuencia que diferencia la nueva hipótesis de su rival | Traza/artefacto con predicción contrastable |
| **6. Contraste** | Si ejecutó una prueba con poder real de discriminación | Mecánica: prueba ejecutada y poder contra rivales |
| **7. Selección** | Si comparó e interpretó las alternativas de acuerdo con la evidencia legal | Comparación registrada + resultado objetivo |
| **8. Realización** | Si construyó un modelo ejecutable con la nueva estructura y si calibró bien sus números | Firma funcional y score mecánicos |
| **9. Propagación** | Si el cambio sobrevivió en la entrega, predicciones y decisiones dependientes | Artefactos y acciones mecánicas; `N/A` si el host termina al entregar |

Fuera de la cadena se informa el **resultado: ganancia real frente al rival fuerte**, medido sobre
el examen sellado y cero-LLM. Es la consecuencia obtenida, no un acto del agente.

**La bisagra creativa es el casillero 3, no el 7.** Una hipótesis cuenta como específica cuando
explica estructuralmente este caso —por ejemplo, “estos perfiles pueden venir de dos tipos
persistentes”— aunque todavía no tenga parámetros ni haya sido probada. Una lista de métodos o
palabras posibles (“mezcla, copula, colas, bootstrap…”) se registra como evocación genérica. Si la
hipótesis específica aparece y luego se descarta sin ponerla en juego, hubo generación abductiva
expresada y falló el rigor posterior. Si el código realiza la estructura sin narrarla, hubo
realización funcional aunque la generación verbal quede no observada.

No leemos la mente: la traza permite afirmar **“expresó la hipótesis”**, no “la creyó internamente”.
Las citas son descriptivas y jamás entran al reward. Los campos mecánicos siguen siendo los únicos
aptos para premiar o entrenar.

#### D. Fork diagnóstico después de un negativo

No se corre una escalera infinita. Se elige **como máximo un control decisivo en el mismo
anfitrión**, dirigido al primer eslabón roto y predeclarado antes de ejecutarlo:

| Primer quiebre observado | Intervención mínima | Qué mostraría un rescate |
|---|---|---|
| No adquirió evidencia discriminante | Servir la evidencia cruda, sin interpretarla | El cuello estaba en la búsqueda/adquisición |
| La evidencia contradijo su modelo, pero no expresó la grieta | Mostrar solo predicción vs resultado | Necesitaba un impasse explícito |
| Expresó la grieta, pero ninguna hipótesis específica | Pedir formas estructuralmente distintas, sin nombrar la correcta | Faltaba presión para reabrir el menú |
| La forma correcta sigue sin aparecer | Nombrar la idea, sin solución | Capacidad condicionada presente; la hipótesis específica no había sido expresada antes del control |
| La hipótesis apareció, pero nunca entró como rival vivo | Pedir qué la haría ganar o perder | Generación presente; faltó ponerla en juego |
| Entró como rival, pero no fue contrastada | Exigir una comparación directa con el rival | Faltó rigor de prueba o política de parada |
| Eligió la estructura, pero no la realizó | Dar un fitter o esqueleto técnico | El cuello era implementación/calibración |

Para una afirmación causal, ambas continuaciones parten del **mismo checkpoint** y difieren en una
sola intervención. Una pista dada desde el turno inicial sirve como control global de capacidad,
pero mezcla búsqueda, atención y generación. Placebos de atención o pistas falsas se agregan solo
si el claim requiere separar contenido, saliencia u obediencia; no bloquean el mundo base.

#### E. Registro concreto

Cada partida conserva, junto a sus métricas:

- identidad completa: experimento, mundo, tarea, condición, agente, instancia y semilla;
- qué pasos fueron regalados por la condición;
- los nueve casilleros de la ficha y la ganancia funcional como resultado separado;
- valores mecánicos y referencias exactas a acciones, modelos y fragmentos de traza;
- `incierto` en vez de forzar una interpretación;
- decisión final `MANTENER / MODIFICAR / PIVOTEAR / ABANDONAR` al nivel del anfitrión.

La implementación mínima es una tabla dentro de la ficha del experimento —no otro documento— con
una fila por episodio y estas columnas:

`episodio · condición · pasos_regalados · evidencia_disponible · evidencia_adquirida ·
grieta_objetiva · grieta_expresada · creatividad · puesta_en_juego · desarrollo · contraste ·
selección · realización · propagación · ganancia_funcional · citas · incertidumbres`.

Primero se completan los campos mecánicos desde acciones y artefactos; después se leen las trazas
para los campos expresados, siempre con cita. Nunca se cambia un resultado mecánico para hacerlo
coincidir con la narración. Los criterios específicos de cada casillero y cuáles aplican se congelan
en la ficha del mundo antes de una tanda confirmatoria.

La primera prueba del instrumento será re-anotar retrospectivamente las diez partidas de
**Perfiles persistentes**, con evidencia citada y sin cambiar su resultado funcional sellado.
Las ambigüedades encontradas sirven para revisar esta versión. En el próximo experimento la ficha,
los criterios y los checkpoints de modelos intermedios se congelan antes de correr.

*(Doc vivo. Cada paper nuevo que MIDA juicio/vicios/ideas entra acá con su método + reflexión, además
de a `lectura-de-fuentes.md` con su hallazgo.)*

## 3. Los que miden la ACTUALIZACIÓN DE CREENCIAS (el cluster del foco — 3ª oleada, 2026-07-13)

Métodos robables (todos DESCRIBEN; ninguno entra al reward — cero-LLM intacto). Links y
estado de lectura en `lectura-de-fuentes.md`; hallazgos en `vicios/vicio-1`.

- **Oráculo normativo + destilación** ([Qiu, 2503.17523](https://arxiv.org/abs/2503.17523)):
  computa la posterior bayesiana exacta del setting y mide la distancia del modelo; después
  ENTRENA imitando al normativo (y generaliza). Robable como VALIDADOR en mundos con posterior
  tractable; imposible como reward general — en investigación abierta no hay oráculo (nuestro
  lugar: fidelidad en held-out).
- **El piso sin hablante como brazo de control** ([Hu, 2607.05545](https://arxiv.org/abs/2607.05545)):
  mismo payload con y sin fuente — separa contenido de social. Obligatorio en toda sonda
  nuestra del canal social (sin ese brazo, "social" mide contenido).
- **Probe de creencia interna + steering causal** ([Yang, 2505.16170](https://arxiv.org/abs/2505.16170)):
  mide la creencia aparte de la salida y la manipula para probar causalidad. Necesita pesos →
  descriptivo puro, útil en E2 con modelos abiertos.
- **Creencia declarada vs ACCIÓN** ([Pal, 2511.13240](https://arxiv.org/abs/2511.13240)):
  confidencias elicitadas vs conducta (apostar, buscar info, defender bajo desafío) — la
  brecha reconocer→actuar como métrica separada de la creencia.
- **El predictor de crossover** ([Vigraham, 2605.04361](https://arxiv.org/abs/2605.04361)):
  la exploración de base SIN material predice si el material mostrado ayuda o daña (r=−0.82) —
  barato en nuestros mundos (correr la base sin material primero).
- **La lección del distractor auditado** ([Sturgeon 2026, LessWrong](https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail)):
  la celda "irrelevante" NO se certifica por juicio (a dos frontiers les dio κ=0.32) — en
  WAGER se certifica COMPUTABLE desde la verdad del mundo: condicionar en el material no
  cambia la posterior sobre mecanismos ni el score alcanzable. Diferencial nuestro; va al
  certificado del mundo del canal contenido.
- **Del dossier externo (vía B)**: puntuar la actualización en LOG-ODDS contra el generativo
  del mundo (rigidez = cambio < normativo · sobre-reacción = > · deriva = cambio con LR≈1 ·
  testimonio virtuoso = cambio ∝ confiabilidad demostrada de la fuente); verbo
  `registrar_creencia({H: p})` en checkpoints (la prosa no puntúa) contrastado con la creencia
  REVELADA (predicciones held-out + elección del próximo experimento bajo costo); confiabilidad
  del par ENSEÑADA programáticamente (historial 50% vs 80%, misma frase); y la nota del par
  por el mínimo de MEDIAS APAREADAS por subfamilia — jamás mínimo por episodio (amplifica
  ruido).

## 4. Los dos leídos del 2026-07-13 (pedido de Lucas) — DiscoverPhysics y el investigador evidence-first

- **DiscoverPhysics ([2605.26087](https://arxiv.org/abs/2605.26087)) — el vecino más cercano,
  ahora LEÍDO**: puntúa (a) MSE de trayectorias en HELD-OUT (mecánico — nuestra fidelidad con
  otro nombre) + (b) explicación 0-10 por juez-LLM con rúbrica (pass = ≤10% MSE Y ≥0.9). Su
  PROPIA limitación admitida: *"the explanation score relies on a single LLM judge"* — el
  diferencial cero-LLM nuestro, confirmado desde adentro. El desacople que ellos mismos
  reportan (mejor MSE sin mejor explicación: *"fitting the data well without necessarily
  understanding it"*) lo detectan SOLO gracias al juez; nosotros lo cobramos SIN juez con la
  batería multi-régimen (el que ajustó sin entender pierde en el régimen que no vio).
  Robables: pass@k sobre repeticiones · presupuesto fijo de rondas · su catálogo de leyes
  alteradas como cantera.
- **LLM-as-an-Investigator ([2606.13220](https://arxiv.org/abs/2606.13220))**: pipeline de
  TRES agentes (el usuario lo simula un LLM que conoce la solución — barato para generar
  interacción; PERO mete simulador/juez en el loop → descriptivo, jamás reward). La métrica
  robable: **tasa de desafío ESPONTÁNEO a la hipótesis plantada (1-2/30) vs bajo chequeo
  explícito (27-28/30)** — el par espontáneo-vs-forzado como medida de la brecha
  reconocer↔ejecutar. En WAGER el chequeo espontáneo se cobra solo (quien no lo hace entrega
  peor modelo), sin juez.

## 5. Strategic Play — medir por separado observación, creencia y acción

**Qué tiene de limpio** ([2605.00226](https://arxiv.org/abs/2605.00226), leído 2026-08-11): no
infiere “actualizó bien” desde la jugada final. Primero calcula, sin juez LLM, cuánto debería
cambiar una creencia según Bayes; después mide cuánto cambió realmente. Por separado, usa sondas
internas e intervenciones causales para preguntar si esa creencia gobierna la acción.

La enseñanza para WAGER no es copiar ahora su métrica, sino **separar los eslabones**:

1. **Evidencia disponible**: la verdad programada permite calcular mecánicamente cuánto distinguían
   los datos comprados entre explicaciones rivales.
2. **Modelo provisional**: los modelos registrados muestran qué predice el artefacto del agente en
   cada momento.
3. **Acción**: la siguiente compra, decisión y entrega muestran si actuó de acuerdo con ese modelo.
4. **Resultado**: el programa final permite verificar si el cambio fue realmente mejor.

Límite importante: un modelo registrado es conducta observable, **no una lectura de la creencia
interna**. Con modelos cerrados no tenemos las sondas del paper. WAGER sí puede medir limpiamente la
cadena `evidencia → modelo registrado → acción → entrega`, y describir aparte lo que el agente dijo,
sin poner ese texto en el reward. Esto queda como inspiración de diseño; no modifica D2 ni abre una
métrica nueva por decisión automática.
