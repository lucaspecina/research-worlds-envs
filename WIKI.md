# WIKI — WAGER, explicado desde cero

> **Qué es este documento.** El lugar para entender el proyecto **sin saber nada de
> antemano**, en profundidad y sin jerga. Si es tu primera vez, leelo de arriba a abajo.
> Para el *por qué* filosófico terso está la constitución; para los *contratos técnicos*,
> la referencia de arquitectura; para las *decisiones*, los ADRs. Acá está el mapa mental.
>
> **Marcadores de estado** (esto es investigación en desarrollo, así que somos honestos
> sobre qué es piso firme y qué es andamio):
> **✅ hecho y verificado** · **🔨 en construcción** · **❓ sin decidir / pregunta abierta**

---

## 1. Qué es esto, en un párrafo

Queremos **medir y entrenar el juicio investigativo de las IAs**: la capacidad de agarrar un
sistema desconocido, con datos que quizás mienten y un presupuesto limitado, e **investigarlo**
hasta entender qué pasa de verdad. No "resolvé este problema que tiene respuesta conocida",
sino "acá hay algo que no entendés — averiguá cómo funciona y entregá un modelo que sirva".
Para eso fabricamos **mundos sintéticos**: pequeños universos ejecutables con una verdad
oculta adentro y trampas realistas. Una IA los juega; un juez **puramente matemático** (jamás
otra IA opinando) le pone una nota. Esa nota puede usarse para entrenar.

## 2. El problema que ataca (y por qué nadie lo mide bien)

Las IAs de hoy se evalúan sobre todo con problemas que **tienen respuesta**: matemática,
programación, preguntas de examen. Eso mide ejecución, no juicio. Pero la parte más valiosa
—y menos medida— del trabajo científico o de ingeniería es **el medio**: formular una
hipótesis, decidir qué experimento vale la pena, darse cuenta de que los datos te están
engañando, cambiar de idea cuando la evidencia contradice tu corazonada, saber cuándo parar.

Medir eso es difícil por una razón profunda: **si el juez es otra IA que opina "esto parece
buen razonamiento", el sistema se puede engañar**. Bajo presión de optimización, la IA que
juega aprende a *actuar* el buen razonamiento —a producir la forma sin el fondo— y el juez
se lo compra. Ese es el error que este proyecto existe para no cometer.

## 3. La idea central

Tres piezas.

**Un mundo es un programa.** No una base de datos, no un texto: un programa que, cuando lo
corrés, genera datos según reglas ocultas. La "verdad" del mundo *es* ese código. Como es un
programa, podemos correrlo bajo cualquier condición —incluso condiciones que la IA nunca vio—
y ver qué pasa. Eso es lo que hace imposible ganar de memoria.

**La IA entrega otro programa.** Su respuesta no es prosa ("creo que la relación es lineal").
Es un **modelo ejecutable**: un pedacito de código que, corrido bajo cualquier condición,
intenta reproducir el comportamiento del mundo verdadero. Sus dudas se expresan como código
(por ejemplo, una mezcla de modelos rivales con pesos). El contrato es de comportamiento: por
dentro puede tener lo que quiera, pero el borde —qué entra, qué sale— está clavado.

**El juez es matemática pura.** Compara las salidas del modelo de la IA contra las del mundo
verdadero, en muchas condiciones, y mide la distancia. **Cero IA en ese cómputo, para siempre**
✅ (hay un test de integración continua que rompe el build si una IA se cuela en el camino de
la nota). Esto es lo que permite usar la nota como recompensa de entrenamiento sin que se pueda
hacer trampa: no hay opinión que engañar, solo comportamiento que reproducir.

## 4. Una partida, paso a paso ✅

Así se juega un **episodio** (todo esto funciona hoy):

1. **El encargo (brief).** La IA recibe una historia como se la daría un cliente: *"Sos asesor
   de una línea de proceso. Cada lote de material entra con una composición que no está
   registrada. Tenés que entregarme un modelo que prediga la calidad del producto según el
   nivel de entrada que yo elija — y me importa especialmente el riesgo de que salga por debajo
   de la línea de rechazo."* Le decimos las reglas del juego, jamás los puntos del examen.

2. **Investiga con un presupuesto.** Tiene "plata" y puede gastarla:
   - `observe` — comprar datos históricos baratos (que pueden venir sesgados).
   - `experiment` — pagar caro por correr el sistema bajo condiciones que ella elige.
   Cada acción cuesta. El presupuesto se acaba. Eso hace que **decidir qué experimento vale la
   pena** sea parte del juego.

3. **Entrega.** Cuando cree que entendió, entrega su modelo (un programa).

4. **Se puntúa, del lado del servidor.** El juez matemático corre el modelo de la IA contra el
   mundo verdadero en condiciones que la IA nunca vio, y calcula la nota. La IA nunca ve la
   nota ni las condiciones del examen (si las viera, estudiaría para el examen en vez de
   entender el sistema).

Todo esto corre hoy con modelos de frontera reales vía API, en aproximadamente un minuto por
partida. Y hay un **dossier visual** que muestra cada partida turno a turno: qué pensó la IA,
qué compró, qué entregó, y por qué sacó lo que sacó.

## 5. Cómo se construye un mundo ✅

Cada mundo tiene **tres capas**, y esta separación es la clave de todo:

| Capa | Qué es | Dónde viven las trampas |
|---|---|---|
| **Mecanismo** | Las reglas de fondo, limpias (las ecuaciones del sistema) | Casi nunca |
| **Canal de observación** | Cómo se mide: con qué ruido, qué proxies | Muy seguido (error de medición) |
| **Proceso de muestreo** | Quién/qué entra a cada registro de datos | Muy seguido (sesgos de selección) |

**Las trampas viven en las fuentes de datos, no en el mecanismo.** El mundo verdadero es
limpio; lo que la IA *ve* está corrompido (registros históricos sesgados, instrumentos
ruidosos). Por eso **copiar los datos pierde**: copiás la corrupción. Para ganar hay que
*deshacer* la corrupción, y para eso hay que entender el sistema.

Encima de las reglas va una **"piel" semántica**: el mismo mecanismo matemático puede vestirse
de línea de proceso, de cultivo, de mercado. La piel importa porque activa el conocimiento
previo de la IA — y una perilla de diseño controla si ese conocimiento previo es **correcto o
engañoso** (a veces lo que "suena razonable" es exactamente la trampa).

## 6. Cómo se puntúa, sin jerga ✅

La nota se llama **R** y va de **0 a 1**, calibrada con dos referencias:

- **R = 0** es "le creíste a los datos crudos tal como vinieron" (el jugador ingenuo).
- **R = 1** es "lo mejor que se podía saber jugando limpio" (el mejor jugador legal posible).

Entre esos dos anclas cae la nota de la IA. Un 0.9 es "casi tan bueno como el ideal"; un 0.1
es "apenas mejor que creer ciegamente". Las referencias no las inventamos a mano: se **derivan
automáticamente** del mundo (jugadores-robot que encarnan distintos niveles de error).

Hay una sutileza importante: medimos con **dos monedas** a la vez.
- **La forma de la distribución** (¿el modelo reproduce la nube de datos completa?).
- **Lo que le importa al cliente** (¿acierta la probabilidad de rechazo, que es donde está la
  plata?).
A veces **divergen** —un modelo puede tener buena forma y malapreciar el riesgo, o viceversa—
y esa divergencia es un hallazgo recurrente del proyecto (ver §10).

## 7. Qué hace bueno a un mundo ✅

No cualquier mundo sirve. Un buen mundo tiene que **forzar la habilidad que queremos medir**,
no premiar el azar ni castigar torpezas de interfaz. Antes de usar un mundo lo **certificamos**:
una batería de tests que demuestra que la nota mide lo que decimos. Los principales:

- **Techo alcanzable**: un investigador cuidadoso *puede* llegar a R=1. Si ni el mejor jugador
  legal lo alcanza, el mundo es tramposo y se descarta.
- **Trampas visibles**: cada trampa deja una firma detectable; no hay engaños imposibles.
- **Headroom (margen)**: existe una brecha real entre "creer los datos" y "entender el sistema".
  Sin brecha, el mundo no enseña nada.

La brecha se piensa en **cuatro sabores**, cada uno una presión distinta: ¿el mundo fuerza a
*investigar* (no alcanza con curve-fitting)? ¿a *pesar la evidencia contra el prior*? ¿a
*adaptar la estrategia* sobre la marcha? ¿a *postular cosas que no se observan* directamente?

**El trofeo del proyecto** ✅: construimos un mundo (lo llamamos internamente el mundo de
composición oculta por lote) donde cada lote de material trae una mezcla distinta de dos
variantes que responden de forma **opuesta** al nivel de entrada — y esa mezcla no está
registrada; solo llega una muestrita de sensor por lote. Para ganar hay que *inferir* la
composición de cada lote desde esa muestrita. En la partida más ilustrativa, el mejor modelo
disponible jugó **técnicamente perfecto, cero errores** — y sacó **0.096 sobre 1**. Y en las
diez partidas que corrimos (dos familias de modelo), el **máximo fue 0.666** — igual lejísimos
del techo (1.0): **nadie** intentó inferir la composición del lote. No por torpeza: porque no
se le ocurrió la idea. Ejecutar la jugada ganadora cuesta diez líneas de código; *concebirla*
es lo que faltó. **Ese es el trofeo: un mundo donde falta juicio, no ejecución.**

Y descubrimos que **el presupuesto es una perilla de dificultad gratis** ✅: al mismo mundo,
con la plata recortada a un cuarto, la escasez no bloquea el premio — **separa estilos**. Un
modelo compró la evidencia clave y no la usó (se apuró); otro, pensando el doble, la cobró
gastando un tercio del presupuesto.

## 8. Los vicios que cazamos 🔨

La dirección más nueva del proyecto: diseñar mundos **a propósito contra los modos de falla
conocidos** de los investigadores-IA. La regla de oro se respeta — **el vicio no se castiga
con una opinión; se construye el mundo para que caer en el vicio sea la jugada perdedora**, y
el juez matemático cobra la consecuencia. Ejemplos de vicios de la lista:

- No cambiar de idea ante evidencia que contradice la hipótesis.
- Meterse en un pozo (rabbit hole) y no salir; encontrar un error y darse por satisfecho.
- Comprar evidencia y no usarla; inventar números que no midió.
- Refugiarse en la arquitectura familiar cuando la correcta es más incómoda.
- Perseguir lo estadísticamente vistoso pero irrelevante.

Ya vimos varios de estos pasar en vivo con modelos reales (el trofeo del §7 *es* "refugiarse
en lo familiar"). El plan es tener un mundo por vicio, cada uno con un **certificado de trampa
necesaria**: se scriptea el mejor jugador que *comete* el vicio y se demuestra que queda lejos
del techo — así "solo se gana pivoteando" deja de ser deseo y pasa a ser propiedad probada.

## 9. Dónde estamos hoy ✅

> El estado **vivo y preciso** (qué corre, próximo paso, la cartera completa con cifras) está en
> **`docs/roadmap.md`** — es la única fuente que se mantiene al día. Acá va solo la foto de alto nivel.

**Lo que funciona:**
- El camino completo de la nota (juez matemático, cero-IA, con test que lo protege).
- El harness de partidas (una IA real juega de punta a punta).
- La fábrica que deriva rivales, batería y certificados desde la declaración de un mundo.
- El dossier visual para inspeccionar partidas.
- Varios mundos: unos de control (la vara) y los primeros de dificultad real (el trofeo de
  composición oculta y el de presupuesto escaso).

**Lo que todavía no:**
- No entrenamos nada aún (la fase de RL — la apuesta grande, no un hecho).
- No corrimos la evaluación multi-modelo en serio (hasta ahora, puñados de partidas con uno o
  dos modelos — prueba que los mundos muerden, no rankea IAs).
- Casi todos los mundos son del mismo tipo (causales estáticos); el primer mundo *dinámico*
  (con tiempo) es el próximo paso 🔨.

## 10. Qué falta y qué no está decidido ❓

Las preguntas grandes, abiertas de verdad:

- **El diseñador automático de mundos** ❓ — *la pieza existencial*. Hoy los mundos se autoran
  a mano. El valor a escala está en generarlos automáticamente (una IA del lado de la fábrica
  los escribe, la certificación mecánica los filtra). La mitad verificadora ya existe; falta la
  generadora. Sin esto, el proyecto no escala.
- **Eventos a mitad de partida** ❓ — hoy el mundo solo responde; nunca *empuja* información. La
  habilidad de pivotear ante una sorpresa necesita que el mundo pueda interrumpir con un dato
  nuevo a mitad de camino. Diseño pendiente.
- **La moneda del reward (la "pregunta κ")** ❓ — vimos varias veces que la nota R y el error
  económico del cliente **divergen**. ¿Es R la moneda correcta para entrenar, o hay que
  incorporar el costo del cliente? En espera, juntando evidencia.
- **Re-orientar la cartera a vicios** ❓ — decidir si los mundos que faltan apuntan cada uno a
  un modo de falla de la lista (§8).
- **La escalera experimental E1→E4** ❓ — el plan de validación: primero evaluar modelos (E1),
  después entrenar (E2), después probar transferencia a ciencia real (E4). Es el norte, no algo
  hecho.

## 11. Glosario (en llano)

- **Mundo**: un programa con verdad oculta que genera datos bajo reglas; lo que la IA investiga.
- **Episodio / partida**: una corrida donde una IA investiga un mundo con presupuesto y entrega
  un modelo.
- **Brief**: el encargo narrativo que ve la IA (las reglas del juego, no los puntos del examen).
- **Submission**: el modelo (programa) que entrega la IA.
- **R**: la nota, de 0 (creer los datos crudos) a 1 (el mejor jugador legal).
- **Rival / ancla**: jugador-robot de referencia que fija los extremos de la nota.
- **Batería**: el conjunto de condiciones sobre las que se puntúa (secreto para la IA).
- **Trampa / operador**: una corrupción realista de los datos (sesgo de selección, ruido de
  medición) que la IA tiene que descubrir y deshacer.
- **Piel**: el vestido semántico de un mundo (línea de proceso, cultivo, etc.).
- **Headroom**: el margen entre "creer los datos" y "entender el sistema"; lo que el mundo
  enseña.
- **Certificado**: la prueba, antes de usar un mundo, de que la nota mide lo que decimos.
- **Cero-IA en el reward**: la regla dura de que ninguna IA participa en el cómputo de la nota.
