# WIKI — Indagación: el marco teórico

**WAGER estudia la indagación** (*inquiry*): el trabajo de **inferir una verdad oculta que ya
existe, comprando evidencia con presupuesto limitado**. Es lo que hacen el detective, el
médico, el científico, el analista de inteligencia y el programador cuando debuggea. El nombre
tiene un siglo de pedigrí: lo usó Peirce (el que inventó "abducción") y Dewey le dedicó su
lógica entera.

Una frase para presentar el proyecto: *WAGER estudia la indagación — el razonamiento
explicativo sobre sistemas con estructura oculta — midiendo dónde se rompe y si aparecen los
saltos creativos.*

**Para profundizar**: [WIKI-SALTOS](WIKI-SALTOS.md) (los tipos de salto) ·
[WIKI-FALLAS](WIKI-FALLAS.md) (dónde se rompe el ciclo) · [WIKI](WIKI.md) (la máquina que
lo mide) · [docs/saltos.md](docs/saltos.md) (el fondo con fuentes).

**Cómo se conectan los nombres:** el **salto** es la jugada conceptual que queremos observar;
el **experimento WAGER** construye un mundo, una tarea y un puntaje donde esa jugada permite
encontrar el modelo bueno; su pregunta principal es si el agente la descubre y la realiza; y
las **fallas** localizan en qué paso del ciclo se perdió. Antes de observar al agente, las
preguntas de diseño comprueban que el mundo vuelve el salto necesario y descubrible. Después,
preguntar cuándo aparece, qué lo dispara o por qué falla produce subpreguntas científicas y
condiciones dentro de ese experimento. El
vocabulario completo y la forma de nombrar corridas están en
[WIKI — Cómo ordenamos una investigación](WIKI.md#cómo-ordenamos-y-nombramos-una-investigación).

## 1. No todo problema es igual: las tres familias de "resolver"

| Familia | Qué es | Ejemplos | ¿Verdad oculta? |
|---|---|---|---|
| **A. Ejecutar / buscar** | Reglas y meta conocidas; encontrar el camino | Rubik, ajedrez, implementar lo ya diseñado | No — pura combinatoria |
| **B. Diseñar / construir** | La "respuesta" no existe hasta que la hacés | una app, un puente, una canción | No — se crea, no se descubre |
| **C. INDAGAR** | Hay una verdad oculta que YA existe; se infiere desde observaciones compradas | detective, médico, científico, **debuggear** | **SÍ — es la definición** |

Los problemas reales mezclan familias: programar es B… hasta que aparece el bug — debuggear es C
metida adentro de B (por eso "se siente" detectivesco). La ciencia es C en el núcleo con B en
el diseño de instrumentos. **WAGER trabaja en la familia C, destilada.**

## 2. El ciclo de la indagación (el proceso que comparten todos)

El juez, el médico, el detective y el científico ejecutan EL MISMO lazo (lo describió Peirce;
la psicología lo midió en laboratorio como búsqueda en dos espacios — hipótesis ×
ensayos):

1. **ABDUCIR** — generar explicaciones candidatas: *"¿y si los lotes vienen de DOS máquinas?"*
2. **DEDUCIR** — derivar qué se vería si cada candidata fuera cierta: *"entonces el histograma
   debería tener dos jorobas, y las mediciones del mismo lote deberían parecerse entre sí."*
3. **TESTEAR / INDUCIR** — comprar la evidencia y actualizar: *"compro mediciones repetidas
   del mismo lote y miro."*
4. **Volver al paso 1** — con **economía**: cada dato cuesta. Parte del arte es gastar en
   evidencia que DISCRIMINA entre candidatas, no en "fiebre" — evidencia consistente con
   todas, que no vale nada (el concepto de *diagnosticity*: la fiebre prueba que estás
   enfermo, no QUÉ tenés).

Para medirlo no alcanza con mirar la entrega. Desplegamos el lazo en una ficha observable:
**adquirir evidencia → notar una grieta → formular una hipótesis específica → ponerla en juego →
deducir una prueba → contrastarla → seleccionar → realizarla en código → propagarla**. La
generación abductiva expresada ocurre al formular la nueva explicación; realizar el salto en el
modelo viene después. Así, un agente puede ser creativo y poco riguroso, o no narrar la idea pero
realizarla funcionalmente. [Protocolo operativo v1](docs/como-medimos.md#21-protocolo-v1--validar-el-caso-y-leer-la-trayectoria-del-agente).

## 3. Las tres herramientas, bien separadas

- **DEDUCCIÓN**: de la regla al caso. *"Todos los lotes de la máquina A salen fallados; este
  es de A ⇒ saldrá fallado."* Cero riesgo; no agrega conocimiento del mundo — solo despliega
  lo que ya afirmaste. En la indagación sirve para derivar predicciones testeables.
- **INDUCCIÓN**: repartir credibilidad **DENTRO de un espacio dado** de hipótesis. Estimar
  parámetros, testear, generalizar de la muestra al proceso. **Bayes es la matemática de la
  inducción**: P(modelo | datos) te dice cuánto creerle a cada modelo… **pero solo reparte
  entre los modelos que YA están en la lista**. Es la limitación famosa del bayesianismo puro:
  condicionar jamás agranda el espacio.
- **ABDUCCIÓN**: **poner candidatos EN la lista**. Dos grados: *selectiva* — traer uno del
  repertorio que ya tenés (el médico eligiendo entre enfermedades conocidas) — y *creativa* —
  **fabricar un candidato que el repertorio no contiene** (postular clases ocultas, un umbral,
  una entidad invisible). La creativa es EL SALTO ([WIKI-SALTOS](WIKI-SALTOS.md)).

**El criterio que corta limpio** (cuando la frontera parece difusa, usá este):

> ¿Tu movida **reparte probabilidad dentro** del espacio de hipótesis, o **agranda** el
> espacio? Lo primero es inducción/selección. Lo segundo es abducción creativa.

Con eso, "crear un modelo a partir de datos" se descompone sin misterio:

| Movida | Qué es |
|---|---|
| Elegir la FORMA del modelo ("¿una población o dos mezcladas?") | **Abducción** |
| Ajustar sus números (medias, pesos, tasas) | **Inducción** (estimación) |
| Comparar formas de un menú FIJO por BIC/Bayes | Abducción **selectiva** mecanizada (elegís, no inventás) |
| Agregar al menú una forma que no estaba | Abducción **creativa** — el salto |

**¿Y si el agente ya conocía la idea?** La creatividad es relativa a su repertorio. Si el nombre
"neurona" le alcanza para recitar el canal correcto antes de mirar un dato, medimos recuerdo o
selección, no descubrimiento creativo. Si conocía los ingredientes pero la evidencia lo lleva a
armar una combinación que no estaba en su modelo del caso, sí observamos una expansión estructural
durante la investigación, aunque no podamos probar que la pieza era inédita en todo su
entrenamiento. WAGER separa esos alcances con un baseline sin datos y con versiones neutralizadas o
trasplantadas de dominio: la versión familiar mide recuperación y transferencia; la neutralizada,
reconstrucción desde la evidencia. No se titulan igual.

**La conexión con nuestros hallazgos**: en **Conteos por lote**, nuestros agentes hicieron
inducción casi impecable (ajustaron, estimaron y compraron evidencia), pero 0/9 expresó la
partición que faltaba. En **Perfiles persistentes**, en cambio, varias trazas evocaron mezclas y
una encontró los grupos pero no los hizo competir justamente; allí la atribución generativa queda
abierta hasta aplicar la ficha v1. El déficit puede estar en escribir una entrada nueva en el menú
o en desarrollarla, probarla, elegirla y realizarla. La entrega final sola no distingue esos casos.

**La misma idea, dicha con la fórmula de Bayes** (la formulación de la casa, útil para gente
de ML). P(hipótesis | evidencia) admite dos lecturas, y las dos son inducción:

1. **hipótesis = los parámetros de un modelo de forma fija** → estimar los números (nivel 1);
2. **hipótesis = una lista de modelos distintos ya definidos** → comparar formas de un menú
   cerrado (nivel 2). Bien hecho, este nivel ya trae el costo adentro: el modelo recargado
   tiene que repartir su apuesta entre muchísimas configuraciones y pierde densidad en cada
   una — la "navaja de Occam bayesiana", que es la misma vara de dos bolsillos de §6.

En los dos niveles la mesa está puesta de antemano: **condicionar solo REPARTE probabilidad
entre los candidatos que ya están; la regla de Bayes por sí sola no AGREGA un candidato.** El
paso que falta — modificar la estructura de los candidatos, o meter en la lista uno que no
estaba, empujado por la evidencia — **ese paso ES la abducción.**

⚠️ **Precisión obligatoria** (Codex 2026-08-09): esto vale para el CONDICIONAMIENTO dentro de
un espacio fijo, y NO es una afirmación sobre la estadística bayesiana en general. Hay
maquinaria bayesiana que pone masa sobre espacios estructurados infinitos (priors
no-paramétricos, gramáticas generativas de teorías, búsqueda de modelos tipo MCMC sobre
programas): ahí el conjunto ACTIVO sí crece durante la corrida. Lo que sigue en pie es que
alguien tuvo que escribir el generador del espacio — el paso de proponer no desaparece, se
muda al diseño del prior.

**La trampa formal (y por qué no salva)**: se puede declarar la lista infinita ("mi espacio
es el de todos los programas posibles") y entonces "todo es inducción"… sobre una lista que
nadie puede recorrer. En la práctica solo se pueden ESCRIBIR y puntuar un puñado de
candidatos, y elegir cuáles escribís es de vuelta el problema original: la abducción no
desaparece con la lista infinita — se esconde en el paso de proponer. Por eso el programa
mide al PROPONEDOR, no solo al puntuador. En **Conteos por lote: tipos discretos o variación
continua** (`count_mix`), 0/9 trazas expresó la entrada de dos tipos; en otros anfitriones la idea
puede aparecer y perderse después. La ficha de trayectoria evita convertir toda mala entrega en
“nunca propuso”.

### Un vecino muy cercano: Model Discovery Agent (MDA)

El paper [*Model Discovery Agent*](https://arxiv.org/abs/2608.09696), de Kevin Murphy
(`[LEÍDO completo 2026-08-13]`), construye una máquina que a primera vista se parece muchísimo
a WAGER: hay una verdad oculta, un simulador, pocos experimentos comprables y un examen en
situaciones nuevas. La diferencia decisiva es **quién hace cada parte de la investigación**.

MDA reparte el trabajo así:

1. un LLM propone varias formas de modelo ejecutables;
2. una rutina matemática ajusta sus números, compara las formas y cobra la complejidad extra;
3. otra rutina elige la prueba donde los modelos predicen cosas más diferentes;
4. si el mejor modelo todavía falla demasiado, un controlador declara que la lista actual no
   alcanza y **obliga** al LLM a proponer formas nuevas;
5. el modelo elegido predice experimentos ocultos y se puntúa matemáticamente.

Sus mundos tienen tres trajes:

| Familia | Qué esconden | Qué puede hacer el investigador | Dónde vive la prueba decisiva |
|---|---|---|---|
| **Física** | una ley de fuerzas, una masa invisible o especies ocultas | lanzar partículas desde distintas posiciones, velocidades y perillas | por ejemplo, la fuerza Yukawa parece una potencia simple cerca y se separa recién con un lanzamiento lejano |
| **Química** | una de 57 leyes, hechas con 9 mecanismos conocidos y sus combinaciones | elegir siete variables como concentraciones, temperatura y pH; observar la velocidad de reacción | buscar el punto donde dos mecanismos candidatos predicen velocidades distintas |
| **Neuronas** | una neurona normal más un mecanismo eléctrico escondido | elegir entre nueve secuencias de corriente y observar su respuesta | cinco mecanismos están hechos para parecer normales en las pruebas de manual y revelarse solo bajo una secuencia especial |

La receta de construcción es valiosa para WAGER: **lo rutinario deja vivos varios modelos y una
intervención alcanzable los separa con fuerza**. Eso aparece muy limpio en Yukawa —cerca todos
parecen iguales, lejos divergen— y en las neuronas —los estímulos comunes no dicen nada, pero una
secuencia temporal precisa revela el mecanismo oculto—.

Pero MDA **no demuestra que un LLM dé el salto espontáneamente**. El sistema le resuelve desde
afuera varios de nuestros eslabones difíciles:

| Pregunta | WAGER | MDA |
|---|---|---|
| ¿Quién nota que el modelo no cierra? | debe notarlo el agente, salvo en una condición de ayuda declarada | un chequeo matemático lo decide con un umbral |
| ¿Quién decide volver a pensar la forma? | el agente | el controlador lo obliga |
| ¿Quién inventa candidatos? | el mismo agente dentro de su investigación | un LLM especializado solo en proponer |
| ¿Quién elige el próximo experimento? | el agente, con su presupuesto | una optimización matemática elige donde los candidatos discrepan más |
| ¿Quién compara y conserva creencias? | el agente debe reflejarlo en su modelo ejecutable | inferencia bayesiana mantiene y pesa toda la lista |
| Pregunta principal | ¿descubre y realiza por sí mismo la edición necesaria? | ¿cuántos experimentos ahorra el sistema híbrido al identificar el mecanismo? |

Además, sus ayudas son fuertes. En física el prompt nombra incluso fuerzas apantalladas y la forma
Yukawa; en química entrega la gramática de los nueve mecanismos y dice cómo combinarlos; en
neuronas fija el marco Hodgkin–Huxley y ofrece un menú que contiene las pruebas reveladoras. Es
principalmente **abducción selectiva bien orquestada**: traer, combinar y elegir piezas cuyo
vocabulario ya fue preparado. Puede haber expansión real cuando un residuo obliga a agregar otra
combinación, pero el gatillo y la obligación vienen de la máquina.

Lo más útil no es copiar todo el sistema, sino usarlo como **bisturí diagnóstico** en el próximo
anfitrión interactivo del mismo salto. Después de que un agente registre una campana, un control
podría mostrarle, sin nombrar
dos grupos: *“tu modelo produce muchos perfiles intermedios que no aparecen en los datos
reservados”*. Si entonces abre dos familias, antes fallaba en **detectar el impasse o decidir
reabrir**; si propone la idea pero no la adopta, falla la **selección o el compromiso**; si ni así
la genera, falla la **creación de la alternativa**. Esa ayuda no reemplaza la prueba principal sin
pistas: sirve para localizar por qué falló. No reabre ni modifica la tanda ya cerrada de Perfiles
persistentes.

Hay otra coincidencia importante: Murphy encuentra inestable el juez-LLM textual heredado de
DiscoverPhysics y lo excluye de su criterio numérico de aprobación. Las trayectorias ocultas, las
predicciones y la equivalencia de fórmulas se evalúan con cómputo. Es la misma razón por la que
WAGER protege el reward cero-LLM.

La extracción técnica completa, incluidos mundos, prompts, resultados y límites, está en
[Lectura de fuentes — MDA](docs/lectura-de-fuentes.md#mda-model-discovery-agent-arxiv-260809696).

## 4. Las cuatro perillas (por qué el juez, el médico y el detective no son idénticos)

Mismo ciclo, distinto punto del espacio de configuraciones:

1. **¿El menú está cerrado o abierto?** El médico casi siempre elige de la nosología; el
   científico en la frontera tiene que inventar el candidato.
2. **¿Podés experimentar, o solo evaluar lo que te traen?** El médico pide estudios; el
   científico interviene; **el juez no experimenta** — evalúa evidencia producida por otros.
3. **¿La fuente puede mentir?** La naturaleza no engaña; el sospechoso y el adversario sí.
4. **¿Con qué vara se decide?** "Más allá de duda razonable" ≠ "p<0.05" ≠ "empezar el
   tratamiento ya".

**La frase que ata todo: nuestra máquina de mundos ES ese espacio de perillas.** Cada
profesión es un punto en él; WAGER fabrica los puntos a voluntad, con la verdad bajo control y
el puntaje sin jueces LLM.

## 5. Indagar no es solo razonar

El razonamiento (deducir/inducir/abducir) es la caja de herramientas central, pero la
indagación usa más músculos — y las fallas reales viven también ahí:

- **Memoria**: el detective que vio el nombre clave y no lo conectó — falla de recuperación
  (la memoria trae por parecido superficial, no por estructura: 70% recupera el análogo con
  parecido de superficie vs 30% sin él), no de lógica.
- **Percepción**: nuestro agente que IMPRIMIÓ el histograma con las dos jorobas y no lo vio —
  se mira a través de los resúmenes que el modelo vigente considera relevantes.
- **Economía**: saber gastar — evidencia que discrimina, cuándo replicar el dato raro, cuándo
  parar.
- **El gatillo del insight NO es deliberado**: la reestructuración aparece tras un IMPASSE
  (fracaso persistente y visible), no porque la invoques. "Sé creativo" no funciona; fabricar
  la pared sí ([WIKI-FALLAS](WIKI-FALLAS.md)).

## 6. El fondo del marco: editar modelos — y la vara que decide si la edición vale

Todo investigador carga un **modelo** de cómo funciona su pedazo del mundo (a veces escrito,
casi siempre mental). Indagar es mejorar ese modelo comprando evidencia; **refinar** es
ajustarle los números; **el salto** es editarle la FORMA.

**Las dos mitades del descubrimiento (2026-08-21 — [enunciado maestro](docs/research/2026-08-21-marco-dos-mitades-ediciones-y-flujo.md), ADR 0187).**
Un descubrimiento tiene dos mitades que conviene no mezclar: **la MODIFICACIÓN** (qué edición
se le hizo al modelo — el salto propiamente dicho; de esto hay tipos, y la lista de
[WIKI-SALTOS](WIKI-SALTOS.md) es el catálogo para DISEÑAR mundos) y **el FLUJO** que la
produce: ver que algo no cierra → que te moleste → generar el candidato (la creatividad en
sentido estricto, el "aha") → correr el test que discrimina → jugarse a reconstruir. **Lo que
medimos es el flujo** (la cadena de eslabones del Protocolo v1); los fallos que encontramos
viven ahí y — apuesta falsable del marco — no dependen del tipo de edición. Y una precisión
que ordena todo: una edición es salto **relativa al repertorio del que busca** — la misma
edición es salto para un agente y consulta de memoria para otro; por eso el test de
contaminación es parte constitutiva de cualquier claim de creatividad. La sospecha
anti-romántica vigente: en nuestros datos los descubrimientos no mueren en el "aha" — mueren
antes (no dudan) y después (no chequean, no se juegan); si generar es lo barato y la economía
alrededor lo caro, el programa entero cambia de blanco. Sigue abierta: ¿la semilla o la
tierra? Hasta la "invención absoluta" se
descompone así cuando se la mira de cerca: Planck aplicó una técnica de conteo que ya existía
(la de Boltzmann) donde "no correspondía"; Einstein combinó un hecho conocido desde Galileo
con una geometría publicada 60 años antes (que le tuvo que enseñar un amigo). **No hay magia:
hay ediciones a distintas DISTANCIAS** — de qué tan lejos traés la pieza, cuánto del marco
vigente hay que romper para encajarla, y cuánta señal te empujaba. "Salto supremo" = distancia
enorme + mucha rotura + cero señal empírica. Es un continuo — y un continuo se puede medir
con una escalera de mundos; una magia no.

**¿Cuándo una edición es MEJORA y no un parche?** La vara de dos bolsillos (la teoría formal
de la creatividad de Schmidhuber; en estadística, MDL):

> bolsillo 1: costo de DESCRIBIR el modelo (su simplicidad, hecha número)
> bolsillo 2: costo de describir lo que el modelo NO explica (los residuos)
> **mejora = la SUMA baja.**

"Ajusta mejor", solo, no alcanza: el epiciclo y el planeta Vulcano siempre ajustan mejor —
mejoran el bolsillo 2 pagando el bolsillo 1 a escondidas. La vara de dos bolsillos cobra las
dos cosas en la misma moneda, y el parche deja de ganar. **Nuestra vara ya es una versión
operativa de esto**: el BIC de los testigos es literalmente ajuste-menos-castigo-por-
parámetros, y R premia capturar la forma. Consecuencia elegante: el descubrimiento SIN
anomalía queda bien definido (Newton comprimió milenios de manzanas perfectamente
predecibles; los dígitos de π no tienen ninguna anomalía estadística y sin embargo existe el
programa corto que los genera todos).

**Disparador ≠ criterio.** El criterio (comparar candidatos y que gane el que comprime) se
computa recién DESPUÉS de tener el candidato en la mano — la ganancia de compresión de
reemplazar a Newton estuvo disponible 200 años sin que nada en los datos la gritara. El
problema del salto es el DISPARADOR: qué te pone a buscar cuando lo de siempre anda bien.

**Saber que el modelo no cierra ≠ sentir presión por mejorarlo.** Son dos ejes. **Saber** es
que la señal de desajuste llegó al agente — porque la encontró, se la mostraron o sufrió una
consecuencia. **Presión** es cuánto empuje tiene para seguir buscando, incluso si ninguna
predicción falló: autoexigencia, coherencia o simplicidad. Una pista cambia qué idea tiene
disponible; un aviso cambia lo que sabe; una consecuencia puede cambiar también la presión.
No forman una sola “escalera de ayuda”. Cada experimento debe decir cuál de esos ejes cambia.

Dos canales pueden disparar la búsqueda:

- **Impasse por datos**: el modelo de siempre falla a la vista, persistente y barato de
  verificar. Es el gatillo que ya sabemos fabricar y que produjo nuestro cambio más grande
  ([WIKI-FALLAS](WIKI-FALLAS.md)).
- **Impasse por coherencia**: nada predice mal, pero las piezas del propio modelo se
  contradicen ENTRE SÍ — el canal Einstein (mecánica y electromagnetismo no podían ser
  ciertos a la vez; el mismo fenómeno con dos explicaciones según el marco). Los agentes
  auditan ajuste-a-datos y JAMÁS la coherencia y economía interna de su propio modelo —
  observable nuevo, fabricable en mundos futuros.

**Predicción ≠ intervención.** Dos modelos pueden empatar prediciendo lo ya visto y separarse
recién cuando MOVÉS una perilla del mundo (un régimen no visitado, una extrapolación). Por
eso el examen se toma en regímenes que el agente no visitó: el modelo que solo ajusta muere
ahí; el que capturó la estructura sobrevive. Es, además, el remedio que el propio paper
can't-jump receta — mundos interactivos con intervención — o sea, esta máquina.

---

## 7. Los hombros: quién sostiene qué pieza del marco (y qué nos corrigió cada uno)

Nada de lo de arriba lo inventamos nosotros. Cada pieza está parada sobre alguien que la
pensó antes, casi siempre con experimentos. Acá va, en llano, quién sostiene qué — y la
**corrección** que cada lectura nos obligó a hacer, porque ese es el valor real de leer.
Todos leídos a texto completo salvo donde se marca *(resumen)*; el registro auditable está en
[docs/lectura-de-fuentes.md](docs/lectura-de-fuentes.md), las extracciones verbatim en
[docs/saltos.md → biblioteca](docs/saltos.md#recursos-para-leer-más-la-biblioteca-del-programa),
y las definiciones puestas lado a lado en
[el doc del 23-09](docs/research/2026-09-23-que-es-el-salto-definiciones-canonicas-y-supuestos.md).

**A. Los que dicen qué es el salto.**

- **Peirce (1903)** — la *abducción*: "veo algo sorprendente; si X fuera cierto, dejaría de
  ser sorprendente; entonces sospecho X". Sostiene: el salto es una **inferencia** (inventar
  la explicación), no magia; y la sorpresa es su gatillo. Es el origen de todo el vocabulario.
- **Magnani (2001)** — la abducción **selectiva** (elegir la explicación de una caja que ya
  tenías: el médico que diagnostica) vs **creativa** (fabricar una que no estaba). Sostiene:
  nuestra definición de salto *relativa al repertorio*; el test de contaminación como parte
  del claim; y la pregunta "¿existe, o es todo memoria?" ya tiene nombre: "¿es selectiva?".
  Nos corrigió: lo que medimos es abducción *existencial* (postular un tipo o entidad nueva),
  la misma en la que fallaban los programas de descubrimiento de los 80; "lo ve y lo descarta
  como outlier" es un paso legítimo — el vicio es descartarlo *sin test de fecundidad*; y
  detectar la anomalía sin poder explicarla es lo esperable de una máquina selectiva, así que
  para reclamar déficit creativo hay que mostrar que el agente tenía los ingredientes.
- **Boden (2004)** — creativo = nuevo, sorprendente y valioso; **P-creatividad** (nuevo para
  vos) vs **H-** (nuevo para la humanidad); y tres formas: **combinar** cosas conocidas,
  **explorar** dentro de tu espacio, **transformar** las reglas del espacio. Sostiene: refinar
  = explorar; saltar = transformar; y solo podemos reclamar P-creatividad. Nos corrigió: medir
  contra el espacio *efectivo* del agente (lo que parece salto puede ser exploración de otra
  representación → elicitar el menú previo); "combinación a distancia" no alcanza si no incluye
  operadores sobre las reglas; y separar generar de reconocer (Copérnico tachó las elipses).
- **Runco & Jaeger (2012), Simonton (2012)** *(resumen)* — la definición estándar del campo:
  creatividad = originalidad + efectividad (Simonton: novedad × utilidad × sorpresa). Sostiene:
  "creatividad" es el paraguas; lo nuestro es una especie (la transformacional), no el género.
- **Aliseda (2006)** — la lógica de la revisión: revisar = contraer + expandir; y "hacer una
  distinción" (partir un átomo en dos) como el operador que agranda el vocabulario. Sostiene:
  dónde termina lo mecanizable — su generador es cerrado por vocabulario, así que formaliza la
  **frontera** del salto, no el salto. Nos corrigió: novelty/anomaly tipifica el disparador,
  no nuestro par generar/aceptar.
- **Thagard (1992)** — grados de cambio conceptual, de agregar una instancia a reorganizar el
  árbol entero. Sostiene: la escala de severidad. Nos corrigió: "entidad oculta" es su escalón
  *barato* — que los agentes fallen justo ahí afila el hallazgo en vez de debilitarlo.

**B. Los que miraron cómo pasa adentro de una cabeza.**

- **Ohlsson (1984-2011) y Knoblich et al. (1999)** — el insight: te trabás (impasse) y salís
  cambiando la representación: relajando una restricción que te impusiste solo, o partiendo un
  bloque que veías entero. Con fósforos lo midieron: la dificultad se predice del **alcance**
  de la restricción (95 / 78 / 45% a los 5 minutos) y, una vez relajada, queda relajada.
  Sostiene: "ingeniar el impasse desde el mundo" y el molde de las primitivas (una restricción
  = una primitiva aislable). Nos corrigió: el gatillo no es "el impasse" sino el fallo del
  propio intento, persistente, *detectado* y fuerte; y el propio Ohlsson declara sus tests
  débiles, con una prevalencia impasse→insight de 3 a 41%.
- **Kaplan & Simon (1990)** *(leído en parte)* — insight = encontrar la **representación**
  (la paridad en el tablero mutilado); se predice de qué generadores y restricciones tenés para
  esa búsqueda; probaron cuatro ayudas: saliencia de la clave, conocimiento previo, pistas por
  tiempo, heurísticas ("buscá lo que no cambia"). Sostiene: nuestra escalera de pistas existía
  en 1990 con regla de tiempo; y el peldaño **saliencia** — cambiar cómo se ve el dato, sin
  decir nada, bajó el tiempo de notar de 33 a 6 minutos. Nos corrigió: notar ≠ perseguir (11 de
  23 notaron y tardaron 12 minutos más en usarlo) → la "grieta" son dos eslabones.
- **Weisberg (1981, 1995)** *(resumen)* — el escéptico: decirle a la gente el truco ayudó poco
  en los nueve puntos; muchos problemas de insight son "híbridos" (después del aha queda
  trabajo); el genio es un mito. Sostiene: el lado deflacionario de la pregunta del mito y el
  eslabón de "realización". Nos corrigió: la pista no basta como único control.
- **Klein (2013)** — 120 insights reales de campo: se disparan por conexión, contradicción o
  desesperación; solo el 25% pasa por impasse; el 44% son graduales; ninguno de sus casos
  descartó la anomalía — pero es un corpus de *ganadores*. Sostiene: el contrapeso a Ohlsson
  (tensiones #1-3 del registro). Nos corrigió: no absolutizar el impasse.
- **Schmidhuber (2009)** — el aha como progreso de compresión: los mismos datos, de golpe,
  descritos más corto. Sostiene: la vara de dos bolsillos de §6; el descubrimiento sin anomalía
  (Newton y las manzanas). Lo cuestiona el paper del jump: con error casi cero, la compresión
  prefiere parchar (Vulcano) antes que reestructurar.
- **Simon (Newell & Simon; BACON)** — descubrir es resolver problemas: búsqueda con heurísticas,
  también en el meta-espacio de las representaciones; "las representaciones nuevas no brotan de
  la frente de Zeus: emergen por etapas graduales y muy lentas". Sostiene: no hay magia, hay
  búsqueda a dos niveles. Nos cuestiona: si BACON redescubre a Kepler con búsqueda ordinaria,
  ¿qué queda del salto? (la respuesta de Magnani: BACON fallaba justo en la existencial).

**C. Los que miraron científicos de verdad.**

- **Klahr & Dunbar (1988)** — descubrir = buscar en **dos espacios** a la vez, el de las
  hipótesis y el de los experimentos; el insight = instanciar un *marco* nuevo (cambiar tres
  cosas juntas, no un número). Números: retienen la hipótesis desconfirmada el 56% de las veces;
  "teóricos" (cambian de marco desde la memoria) vs "experimentadores" (lo inducen del dato, el
  doble de lento); y si los obligás a **enumerar hipótesis antes de tocar nada**, 5 de 10
  aciertan sin experimentar y aparecen solos los tests que discriminan. Sostiene: medir el
  contraste por *diagnosticidad*, no por forma (su estrategia "positiva" dio 60% de
  desconfirmaciones y sirvió); la intervención "enumerá antes". Nos corrigió: el menú no era el
  problema; tener *una sola* hipótesis, sí.
- **Dunbar (1993; 1995-97)** — en un laboratorio simulado de genética, solo los que se pusieron
  como *meta* explicar el dato raro descubrieron la inhibición; y un año adentro de cuatro
  laboratorios reales: el científico solo atribuye la anomalía a error por defecto, y el
  insight es distribuido (se arma en la reunión de grupo, por analogías encadenadas). Sostiene:
  la grieta como eslabón; el revisor como canal. Pendiente: el paper de 1993 sigue sin leerse
  completo.
- **Kuhn (1962)** *(resumen del paper de Science)* — ciencia normal casi siempre; la anomalía
  como motor; y "el descubrimiento no es un evento": no tiene cuándo ni dónde (el oxígeno).
  Sostiene: medir el flujo, no el momento; la sospecha anti-romántica de §6.
- **Darden (1991-2006)** — estrategias de cambio de teoría sacadas de casos reales (genética
  mendeliana): exprimir la anomalía para elegir dónde editar, barrido sistemático, doce
  transformaciones, monster-barring. Sostiene: la taxonomía de ediciones como *biblioteca de
  diseño*; el pipeline de anomalías. Nos corrigió: alineación fuerte en 5 de nuestras 11
  ediciones y sin correlato en las demás — nuestra lista es más ancha de lo que la historia
  respalda.

**D. Los que miden en modelos de lenguaje.**

- **"Position: LLMs can't jump"** — la tesis blanco: los LLMs inducen y deducen pero no
  abducen; Vulcano (parchar con un parámetro) vs relatividad (reestructurar). Sostiene: el par
  Neptuno/Vulcano de nuestros gemelos; los mundos interactivos con intervención como el
  laboratorio que ellos mismos piden. Nos cuestiona: los saltos más duros ocurren *sin* señal
  de error — nuestros mundos modelan el caso con señal (tensión #7).
- **Chollet / ARC (2019)** *(resumen)* — inteligencia = eficiencia para adquirir habilidad ante
  lo nuevo; ARC son tareas mínimas con una regla que hay que captar. Sostiene: el estilo
  "juegos mínimos". Nos delimita: ARC dice *si* encontraste la regla, no *dónde* te trabaste;
  no tiene pista soplada ni gemelo; es un marcador, no un laboratorio.
- **NazoNazo (2025), Failing to Falsify (2026), NewtonBench (2026)** — tres eslabones nuestros
  medidos aislados en LLMs: endosar el candidato correcto (25-39% de los errores lo tenían
  escrito y no lo eligieron); elegir el test que refuta (pedir "el opuesto" mejora 11 de 11
  modelos, 42→56%); y comprometerse antes de tiempo (el intérprete de código empeora a los
  modelos fuertes). Sostiene: que medir por eslabón es informativo y que hay intervenciones con
  número. Nos corrigió: "nadie más mide el proceso mecánicamente" ya no es cierto.

**Lo que ninguno tiene y nosotros sí** (la frase honesta, después de Astra): no los
simuladores ni las pistas, sino la combinación de verdad fabricada + gemelo donde revisar sobra
+ el mejor rival sin salto optimizado + la pista como compuerta de diseño + puntaje sin LLM.
**Lo que todos ellos tienen y nosotros no**: sujetos humanos en la misma tarea.

---

## Comentarios (el meta)

- **¿Por qué "indagación" y no otro nombre?** "Investigación" es ambiguo (también significa
  *research* en general); "razonamiento" es demasiado general (incluye deducir, planificar,
  calcular — ver §5); "abducción" es solo una fase del ciclo. *Inquiry* es el término con
  pedigrí (Peirce, Dewey) y describe exactamente la familia C.
- **El borde filosófico existe**: la "inferencia a la mejor explicación" mezcla generación con
  selección, y los filósofos debaten dónde termina la abducción. Nuestro corte operativo
  (¿reparte o agranda el espacio?) es medible y no ambiguo — con eso trabajamos.
- **Este wiki resume**; el fondo con fuentes leídas a texto completo:
  [docs/saltos.md](docs/saltos.md) (marco + historia) y las
  [extracciones de lecturas](docs/research/2026-08-07-lecturas-programa-saltos.md).
  Hermanos: [WIKI-SALTOS](WIKI-SALTOS.md) · [WIKI-FALLAS](WIKI-FALLAS.md) · [WIKI](WIKI.md).
