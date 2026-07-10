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
hipótesis, decidir qué experimento vale la pena, darse cuenta de que los datos te están
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

**Y la vista de fábrica, que ordena todo el proyecto en tres capas.** Los mundos que construimos a
mano son **plantas piloto**: experimentos controlados que prueban que una estructura de trampa
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

## 8. Los dos polos: los vicios que cazamos y los saltos que exigimos 🔨

La dirección más fuerte del proyecto: en vez de "medir juicio" a lo vago, bajarlo a dos listas
concretas y documentadas, y construir mundos que las vuelvan medibles. La regla de oro se respeta
siempre — **nada se castiga ni premia con una opinión; se construye el mundo para que la mala jugada
prediga peor**, y el juez matemático cobra la consecuencia sola.

**Polo defensivo — los vicios (no caer).** Fuimos a la literatura (psicología del razonamiento,
historia de la ciencia, análisis de fallas de agentes reales) y sacamos una lista con fuentes de los
errores donde los investigadores tropiezan. Ejemplos:
- No cambiar de idea ante evidencia que contradice la hipótesis.
- Meterse en un pozo (rabbit hole) y no salir; encontrar un error y darse por satisfecho.
- Comprar evidencia y no usarla; inventar números que no midió.
- Refugiarse en la arquitectura familiar cuando la correcta es más incómoda.
- Confundir "estas dos cosas pasan juntas" con "una causa la otra".

**Polo creativo — los saltos / "aha moments" (descubrir).** El otro lado: las operaciones creativas
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
(el trofeo del §7 *es* "refugiarse en lo familiar" — y a la vez el polo bueno de un par: "inventar la
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
