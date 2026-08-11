# WIKI — WAGER, explicado desde cero

> **Qué es este documento.** El lugar para entender el proyecto **sin saber nada de
> antemano**, en profundidad y sin jerga. Si es tu primera vez, leelo de arriba a abajo.
> Para el *por qué* filosófico terso está la constitución; para los *contratos técnicos*,
> la referencia de arquitectura; para las *decisiones*, los ADRs. Acá está el mapa mental.
>
> **La familia de wikis** (los cuatro documentos principales, cortos y en llano — 2026-08-08):
> **[WIKI-INDAGACION.md](WIKI-INDAGACION.md)** — el marco teórico: qué estudiamos (la
> indagación), su ciclo (abducir·deducir·inducir), las perillas, dónde entran los saltos ·
> **[WIKI-SALTOS.md](WIKI-SALTOS.md)** — los 11 tipos de salto y su estado de medición ·
> **[WIKI-FALLAS.md](WIKI-FALLAS.md)** — dónde se rompe el ciclo (los failure modes) ·
> **este WIKI** — la máquina WAGER y el vocabulario común: mundos, tareas, experimentos,
> partidas, gemelos, puntaje y estado.
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

**Y una definición más precisa de "juicio", que ganamos con el tiempo** (porque "juicio" a secas es
vago): lo medimos como dos caras de una misma habilidad. Una cara **defensiva** — *no caer* en los
errores típicos donde los investigadores, humanos y IA, tropiezan una y otra vez (casarse con la
primera idea, no cambiar de opinión ante la evidencia, confundir correlación con causa). Una cara
**creativa** — *dar el salto* que hace un descubrimiento (ver que dos cosas muy distintas comparten
la misma estructura de fondo, inventar algo que no se ve para explicar los datos). Y lo que une a las
dos: **saber cuándo** — porque la misma jugada es genialidad en una situación y macana en otra
(unir dos cosas es Newton si de verdad son lo mismo, y delirio si no), así que el buen investigador
**gasta un poco averiguando en cuál está** antes de decidir. Una honestidad importante: esta lista de
errores y saltos es *nuestra forma de medir* el juicio, no el juicio entero — pasar nuestro examen es
pasar nuestro examen, no la última palabra. Por eso el examen tiene que poder crecer.

## 2. El problema que ataca (y por qué nadie lo mide bien)

Las IAs de hoy se evalúan sobre todo con problemas que **tienen respuesta**: matemática,
programación, preguntas de examen. Eso mide ejecución, no juicio. Pero la parte más valiosa
—y menos medida— del trabajo científico o de ingeniería es **el medio**: formular una
hipótesis, decidir qué ensayo vale la pena, darse cuenta de que los datos te están
engañando, cambiar de idea cuando la evidencia contradice tu corazonada, saber cuándo parar.

Medir eso es difícil por una razón profunda: **si el juez es otra IA que opina "esto parece
buen razonamiento", el sistema se puede engañar**. Bajo presión de optimización, la IA que
juega aprende a *actuar* el buen razonamiento —a producir la forma sin el fondo— y el juez
se lo compra. Ese es el error que este proyecto existe para no cometer.

**¿Y hace falta medir esto? Sí, y hay prueba dura.** Un estudio grande de 2026 (Chen, Zhao y
Cohan, Yale/UChicago; 9 modelos, casi 12.000 ideas) dio a los modelos los mismos trabajos previos
que precedieron a un paper humano real y comparó qué ideas proponen. Resultado: los LLMs ocupan un
espacio **mucho más angosto** de "movidas de investigación" que los humanos y caen todos en el mismo
reflejo — *"conectá estas dos cosas"* (ideas de puente: 12% en humanos, **hasta 64%** en modelos).
Justo evitan las movidas que definen el buen juicio y que nuestros mundos premian: reemplazar una
pieza frágil, **desacoplar dos causas confundidas**, formalizar. Y —clave— poner el modelo a *pensar
más* **empeora** el reflejo, y los modelos se parecen entre sí más que a un humano. O sea: el hueco
de juicio es real, sistemático y medible. Eso es exactamente lo que este proyecto existe para medir
y entrenar.

**¿Y si con el RL sobre tareas verificables ya alcanza?** (la pregunta existencial — vuelve seguido,
y tiene respuesta escrita: ADR 0126). El RL sobre concursos tipo AtCoder produjo saltos brutales
(2026: una IA le ganó ~7× al campeón humano), y la creatividad *instrumental* emerge de una única
métrica (Move 37). Pero mirá qué entrena ese camino y qué no: allá el mundo **no esconde nada y
jamás miente** — el generador de problemas es público y verificar es gratis e infinito. Del camino al
premio emergen buscar bien, iterar, pivotear; el camino **jamás atraviesa** desconfiar de un dato,
decidir qué evidencia comprar, inferir un mecanismo oculto, o elegir entre dos historias que explican
lo mismo. Peor: respecto de los datos, la política óptima allá es la **opuesta** a la de la ciencia —
credulidad total allá, desconfianza calibrada acá. WAGER no compite con ese motor: **es el mismo
motor** (corrector insobornable + generador de mundos + examen fresco) apuntado a lo único que
importa: *qué te esconde el mundo* — AtCoder puntúa tu solución a un problema declarado; WAGER puntúa
tu **creencia** sobre un mundo oculto. Estado honesto: que entrenar acá transfiera es la apuesta
declarada, con su experimento (mismo cómputo: entrenar allá vs acá, examen congelado externo) y sus
criterios de muerte.

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
verdadero, en muchos casos de evaluación, y mide la distancia. **Cero IA en ese cómputo, para
siempre** ✅ (hay un test de integración continua que rompe el build si una IA se cuela en el camino de
la nota). Esto es lo que permite usar la nota como recompensa de entrenamiento sin que se pueda
hacer trampa: no hay opinión que engañar, solo comportamiento que reproducir.

### Cómo ordenamos y nombramos una investigación

Llamamos **experimento** al paquete completo que queremos diseñar, validar y, si Lucas da el
GO, ejecutar. No es solamente el mundo ni solamente la tanda. Todo experimento contiene:

- **salto**: el cambio de forma que queremos medir;
- **pregunta**: una sola pregunta científica principal;
- **mundo o par de mundos**: las verdades ocultas donde la jugada correcta cambia;
- **tarea**: qué debe hacer y entregar el agente, con qué herramientas, presupuesto y turnos;
- **condiciones**: qué cambia de manera controlada entre partidas;
- **medida principal**: qué número responderá la pregunta;
- **tanda**: qué agentes jugarán cuántas partidas.

Una **partida / episodio** es una sola ejecución dentro del experimento. Dentro de esa partida,
lo que el agente compra para poner una hipótesis a prueba se llama **ensayo**. Así “experimento”
siempre significa nuestro paquete científico y nunca una compra del agente.

La **validación previa** tiene dos partes. La **certificación matemática** comprueba que el salto
mejora claramente frente al mejor rival sin ese salto y que la evidencia necesaria existe. La
**prueba de resolubilidad con agente** comprueba que el mismo agente, con la idea nombrada pero
sin la solución, puede investigar e implementar el salto. Su comparación con el agente sin
ayuda mide la **prima de descubrimiento**. Una solución casi regalada es solo un **control de
techo**, nunca una medida de descubrimiento.

#### Cómo se nombra un experimento

Cada experimento tiene dos nombres:

1. **Nombre humano**, para conversar y recordar:

   > **Salto — qué ponemos a prueba — familia de mundo**

2. **ID estructurado**, estable y legible para archivos:

   > `exp__<salto>__<mundo>__<tarea>__<contraste>__v<n>`

El viejo `D2` queda entonces así:

> - **Nombre:** Grupos escondidos — Error del modelo a la vista — Planta a alta temperatura
> - **ID:** `exp__grupos-escondidos__planta-alta-temperatura__modelo-para-piloto__error-explicito__v1`
> - **Pregunta:** ¿mostrar la comparación entre lo predicho y lo ocurrido provoca el salto?
> - **Estado:** cancelado antes de la tanda principal.

Los códigos mudos (`D1`, `D2`, `P1`, `P2`) quedan solo como alias históricos. **Versión**
(`v1`, `v2`) nombra una revisión técnica del mismo experimento. Si cambia la pregunta principal,
es otro experimento.

#### El perfil del mundo: la complejidad no cabe en el nombre

El nombre identifica; el **perfil del mundo** describe. Cada experimento declara:

> - **Nombre de mundo:** Familia — verdad oculta
> - **ID de mundo:** `world__<familia>__<verdad>__v<n>`
> - **ID del par:** `pair__<familia>__<contraste>__v<n>`

Ejemplo: **Planta a alta temperatura — degradación real creciente** =
`world__planta-alta-temperatura__degradacion-real-creciente__v1`; su espejo es
`world__planta-alta-temperatura__sensor-por-vial__v1`.

| Rasgo | Pregunta simple |
|---|---|
| **Forma oculta** | ¿grupos, umbral, memoria, observador, bucle…? |
| **Verdades del par** | ¿qué es real en cada mundo? |
| **Dinámica** | ¿la verdad queda fija o cambia durante la partida? |
| **Llegada de evidencia** | ¿está disponible enseguida o llega por goteo? |
| **Horizonte** | ¿la tarea necesita pocos turnos o una trayectoria larga? |
| **Profundidad** | ¿hay una sola pregunta o problemas anidados? |
| **Interacción** | ¿solo observa, interviene, decide y/o recibe consecuencias? |
| **Dependencias** | ¿qué decisiones o artefactos usan el modelo y sobreviven? |
| **Complejidad efectiva** | ¿se resuelve con un resumen pequeño o exige mantener mucho estado? |
| **Dificultad observada** | ¿qué tasa logra cada agente, con y sin ayuda? |

La dificultad **no es una propiedad absoluta del mundo**: depende del agente, la tarea y la
ayuda. Por eso se mide después de validar y no se incrusta como “fácil/difícil” en el ID.
Cambiar solo los números produce otra **instancia** del mismo mundo; cambiar su verdad o su
forma produce otro mundo o una nueva versión explícita.

#### Cómo se identifica una partida y cómo se pide un GO

Dos números distintos se conservan: la **instancia del mundo** fija sus parámetros concretos;
la **semilla de partida** identifica el azar de la ejecución. Pueden compartirse deliberadamente
en comparaciones apareadas; una semilla ya corrida queda quemada.

Una partida se identifica así:

> **ID del experimento · mundo · tarea · condición · agente · instancia · semilla**

Y todo pedido de GO muestra, antes del costo: nombre e ID del experimento, salto, pregunta,
perfil de los mundos, tarea, condiciones, medida principal y composición exacta de la tanda.
Nunca más “corramos D2”.

## 4. Una partida, paso a paso ✅

Así se juega un **episodio** (todo esto funciona hoy):

1. **El encargo (brief).** La IA recibe una historia como se la daría un cliente: *"Sos asesor
   de una línea de proceso. Cada lote de material entra con una composición que no está
   registrada. Tenés que entregarme un modelo que prediga la calidad del producto según el
   nivel de entrada que yo elija — y me importa especialmente el riesgo de que salga por debajo
   de la línea de rechazo."* Le decimos las reglas del juego, jamás los puntos del examen.

2. **Investiga con un presupuesto.** Tiene "plata" y puede gastarla:
   - `observe` — comprar datos históricos baratos (que pueden venir sesgados).
   - `experiment` — pagar caro por hacer un **ensayo** bajo valores que ella elige.
   Cada acción cuesta. El presupuesto se acaba. Eso hace que **decidir qué ensayo vale la
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

**Y la vista de fábrica, que ordena todo el proyecto en tres capas.** Los mundos que construimos a
mano son **casos piloto**: pruebas controladas de que una estructura de trampa
funciona de verdad (el que cae en el vicio pierde, el cuidadoso gana, y una IA real muerde). **No
son el producto final.** Cuando una estructura queda validada se convierte en **plantilla**, y una
**fábrica automática** la multiplica: misma estructura de fondo, muchos disfraces, números y
semillas distintas — cada variación filtrada por la certificación matemática (sin ninguna IA
opinando). De ahí sale la escala para entrenar y el examen siempre fresco para evaluar. La
diversidad tiene entonces **dos niveles, y los dos hacen falta**: *estructuras distintas* para el
mismo vicio (trabajo intelectual nuestro — la fábrica no inventa estructuras) y *variaciones dentro*
de cada estructura (trabajo de la fábrica, barato). Sin lo primero, una IA entrenada aprende el
truco de la estructura; sin lo segundo, se memoriza el mundo. Estado honesto de la fábrica: el paso
fácil (cambiar el disfraz) ya funciona; el paso medio está trabado en una pieza del verificador; el
difícil ni arrancó.

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
no premiar el azar ni castigar torpezas de interfaz. Antes de usarlo hacemos la **validación del
mundo y la tarea**: certificación matemática y después resolubilidad con un agente ayudado. La
parte matemática incluye:

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

## 8. Las dos caras: los vicios que cazamos y los saltos que exigimos 🔨

La dirección más fuerte del proyecto: en vez de "medir juicio" a lo vago, bajarlo a dos listas
concretas y documentadas, y construir mundos que las vuelvan medibles. La regla de oro se respeta
siempre — **nada se castiga ni premia con una opinión; se construye el mundo para que la mala jugada
prediga peor**, y el juez matemático cobra la consecuencia sola.

**Cara defensiva — los vicios (no caer).** Fuimos a la literatura (psicología del razonamiento,
historia de la ciencia, análisis de fallas de agentes reales) y sacamos una lista con fuentes de los
errores donde los investigadores tropiezan. Ejemplos:
- No cambiar de idea ante evidencia que contradice la hipótesis.
- Meterse en un pozo (rabbit hole) y no salir; encontrar un error y darse por satisfecho.
- Comprar evidencia y no usarla; inventar números que no midió.
- Refugiarse en la arquitectura familiar cuando la correcta es más incómoda.
- Confundir "estas dos cosas pasan juntas" con "una causa la otra".

**Cara creativa — los saltos / "aha moments" (descubrir).** El otro lado: las operaciones creativas
del descubrimiento, también tipificadas en la literatura. El mundo se arma para que el único camino a
la nota alta *pase por* hacer ese salto. Ejemplos: ver que dos sistemas distintos comparten la misma
estructura y traer el mecanismo de uno al otro (lo que hizo Darwin); postular algo invisible para
explicar los datos (así se descubrió Neptuno); reencuadrar las variables de una forma nueva que
destapa un patrón invisible. La regla de admisión es dura: **el salto solo cuenta si se paga en una
predicción medible** (si el premio es solo "qué elegante", no lo sabemos puntuar sin un juez, y queda
afuera).

**La pieza que une los dos — los pares.** El descubrimiento más lindo: el vicio y el salto suelen ser
*la misma jugada* vista de los dos lados. "Unir dos cosas en una" es Newton si de verdad son lo mismo,
y delirio (ver patrones que no están) si no. Entonces no alcanza con "saber unir" ni con "saber
desconfiar" — hay que saber **cuándo**. Por eso construimos de a **pares**: dos mundos que se ven
iguales por fuera, en uno la jugada gana y en el gemelo pierde. Un modelo que aprendió el reflejo
"uní siempre" gana uno y pierde el otro; solo el que **paga por averiguar en cuál está** gana los dos.
El par es lo que impide que el examen se pueda trampear con un truco. (Prioridad honesta: los pares
son un **agregado** que sumamos donde sale barato — imprescindibles recién para los mundos de saltos;
lo fundamental del proyecto es la capacidad de diseñar los mundos de los vicios y multiplicarlos
automáticamente con diversidad, §5.)

Cada mundo (y cada par) lleva un **certificado**: se scriptean jugadores-robot — uno que comete el
vicio, uno cuidadoso, y para los pares uno que aplica la jugada a lo bruto — y se demuestra con
números que el bruto pierde el gemelo y el cuidadoso gana ambos. Así "solo se gana con juicio" deja
de ser deseo y pasa a ser propiedad probada. Ya vimos varios vicios pasar en vivo con modelos reales
(el trofeo del §7 *es* "refugiarse en lo familiar" — y a la vez el lado bueno de un par: "inventar la
estructura escondida").

**Y la honestidad de fondo** (§1): estas dos listas son *nuestra forma de medir* el juicio, no el
juicio entero. Crecen, y nunca lo cubren del todo.

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
- **Los primeros hallazgos del programa de saltos (agosto 2026)**: en **Grupos escondidos —
  ¿aparecen sin ayuda? — Conteos por lote**, 0/9 agentes propusieron los dos tipos; en
  **Régimen oculto — ¿el fallo propio provoca el salto? — Proceso con umbral**, el mismo
  modelo pasó de 0/9 sin fallo visible a 30/30 con su fallo a la vista. La planta química
  produjo un hecho interesante —investigaron pero casi nunca escribieron los grupos—, aunque
  después descubrimos que su vara casi no premiaba el salto. El intento de corregirla y mostrar
  el error se cerró antes de la tanda principal porque tampoco pasó la validación. **Ahora no
  hay ninguna tanda autorizada en esa planta.** El detalle: WIKI-FALLAS ⑤ y WIKI-SALTOS.

**Lo que todavía no:**
- No entrenamos nada aún (la fase de RL — la apuesta grande, no un hecho).
- **No validamos en serio todavía**: la evaluación multi-modelo (varias IAs sobre los mismos mundos)
  casi no arrancó — hasta ahora, puñados de partidas con uno o dos modelos, que prueban que los
  mundos muerden pero no rankean IAs ni confirman del todo que la nota mide juicio. **Es hoy la
  prioridad número uno** (ver `docs/roadmap.md`).
- Los mundos difíciles todavía son **artesanales**: la fábrica automática anda en lo fácil y se traba
  en lo medio.

## 10. Qué falta y qué no está decidido ❓

Las preguntas grandes, abiertas de verdad — y algunas necesitan un salto creativo **nuestro**:

- **El diseñador automático de mundos** ❓ — *la pieza existencial*. Hoy los mundos difíciles se
  autoran a mano. El valor a escala está en generarlos automáticamente (una IA del lado de la fábrica
  los escribe, la certificación mecánica los filtra). La mitad verificadora ya existe; falta la
  generadora. Sin esto, el proyecto no escala.
- **¿Los modelos tienen vicios y saltos PROPIOS?** ❓ — casi toda nuestra lista viene de humanos.
  Un modelo no es un humano: puede no fallar donde un humano falla, y puede tener modos de fallar (o
  de acertar) que ningún psicólogo catalogó, porque los humanos no los tienen. Si nuestros mundos
  revelan eso, es el descubrimiento más original que el proyecto puede dar — y nadie más está parado ahí.
- **¿Cómo se diseña una frontera "descubrible pero no obvia"?** ❓ — para los pares (§8) hace falta
  que la evidencia que separa los dos mundos gemelos exista, tenga precio justo, y no sea ni gratis
  ni imposible. Sabemos *verificar* si una frontera dada funciona; no tenemos la *teoría* de cómo
  construirlas. Hoy es artesanía.
- **Puntuar EXPLICACIONES sin un juez** ❓ — nuestro truco siempre termina en "predecí el sistema" →
  un número. Pero parte del juicio entrega explicaciones, no predicciones. Cómo cobrar eso sin una IA
  opinando es nuestro muro más viejo (retrocedió, no cayó).
- **La moneda del reward (la "pregunta κ")** ❓ — vimos varias veces que la nota R y el error
  económico del cliente **divergen**. ¿Es R la moneda correcta para entrenar, o hay que incorporar el
  costo del cliente? En espera, juntando evidencia.
- **La apuesta grande (la escalera E1→E4)** ❓ — que entrenar en estos mundos produzca juicio que
  *generalice* a problemas nunca vistos sigue siendo una **hipótesis**, con su experimento y su
  criterio de muerte escritos. Es el norte, no un hecho.

## 11. Glosario (en llano)

- **Salto**: el cambio de forma que queremos medir; todo experimento empieza nombrándolo.
- **Mundo**: un programa con verdad oculta que genera datos bajo reglas; lo que la IA investiga.
- **Tarea**: lo que debe hacer el agente dentro del mundo; el brief es cómo se lo contamos.
- **Experimento WAGER**: el paquete completo: salto, pregunta, mundo(s), tarea, condiciones,
  medida principal y tanda.
- **Condición**: la combinación exacta de ayuda, aviso y consecuencias de una partida.
- **Episodio / partida**: una corrida donde una IA investiga un mundo con presupuesto y entrega
  un modelo.
- **Tanda**: el conjunto de partidas que ejecuta todo o parte de un experimento.
- **Ensayo**: una prueba que compra el agente dentro de su partida.
- **Brief**: el encargo narrativo que ve la IA (las reglas del juego, no los puntos del examen).
- **Submission**: el modelo (programa) que entrega la IA.
- **R**: la nota, de 0 (creer los datos crudos) a 1 (el mejor jugador legal).
- **Rival / ancla**: jugador-robot de referencia que fija los extremos de la nota.
- **Batería**: el conjunto de casos de evaluación sobre los que se puntúa (secreto para la IA).
- **Trampa**: una corrupción o dificultad realista de los datos (sesgo de selección, ruido de
  medición) que la IA tiene que descubrir y deshacer. No es sinónimo de tipo de salto.
- **Piel**: el vestido semántico de un mundo (línea de proceso, cultivo, etc.).
- **Perfil del mundo**: su forma oculta, dinámica, llegada de evidencia, horizonte,
  profundidad, interacción, dependencias y complejidad efectiva.
- **Headroom**: el margen entre "creer los datos" y "entender el sistema"; lo que el mundo
  enseña.
- **Validación**: el control previo completo: certificación matemática + resolubilidad con un
  agente que recibe la idea, no la solución.
- **Cero-IA en el reward**: la regla dura de que ninguna IA participa en el cómputo de la nota.
