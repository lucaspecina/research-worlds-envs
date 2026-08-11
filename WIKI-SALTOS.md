# WIKI — Los saltos

**Un salto es cambiarle la FORMA al modelo de un sistema, no los números.** Si tu explicación
de una fábrica es "los lotes tienen en promedio 6 defectos" y ajustás ese 6 a 6.3, refinaste.
Si te das cuenta de que en realidad hay DOS tipos de lotes mezclados, saltaste: ahora tu modelo
tiene una pieza que antes no existía. El salto es el momento creativo de la indagación — la
**abducción creativa**: fabricar un candidato de explicación que tu repertorio no contenía
(ver [WIKI-INDAGACION.md](WIKI-INDAGACION.md)).

**Para profundizar**: [docs/saltos.md](docs/saltos.md) (el libro: historias completas, fuentes
y estado de lectura) · [fundamentos formales](docs/research/2026-08-05-fundamentos-taxonomia-de-saltos.md)
(la matriz componente×edición) · [WIKI-INDAGACION](WIKI-INDAGACION.md) (dónde encaja el salto
en el ciclo de indagar) · [WIKI-FALLAS](WIKI-FALLAS.md) (por qué no aparece).

**El salto es siempre el punto de partida.** Después construimos un experimento: un mundo, una
tarea y un puntaje donde cambiar la forma del modelo sea necesario para encontrar la respuesta
buena. La pregunta principal es siempre si el agente descubre y realiza ese salto. Las preguntas
sobre cuándo, por qué o con qué ayuda aparecen después, como subpreguntas del mismo experimento.
La gramática completa está en
[WIKI — Cómo ordenamos una investigación](WIKI.md#cómo-ordenamos-y-nombramos-una-investigación).

### Foco actual

- **Salto:** grupos escondidos — pasar de una población aparente a dos tipos persistentes.
- **Estado:** los dos experimentos de la planta química están cerrados; el último no llegó a
  su tanda principal.
- **Qué estamos haciendo:** diseñar desde cero un mundo y una tarea donde representar dos tipos
  persistentes sea la manera de llegar al modelo bueno.
- **Pregunta principal:** ¿el agente descubre y realiza el salto de una población aparente a dos
  tipos persistentes?
- **Primer control de construcción:** con la idea de “dos tipos” nombrada, pero sin la solución,
  ¿puede investigarla, implementarla y mejorar claramente? Es una prueba de resolubilidad, no la
  pregunta principal.
- **Gemelo:** fuera de esta etapa; podrá agregarse después como control anti-reflejo.
- **Corridas autorizadas ahora:** ninguna.

## La lista, de un vistazo

| # | Salto | La idea que hay que parir | Ancla histórica |
|---|---|---|---|
| 1 | Entidad oculta | "hay un actor invisible" | Neptuno; el neutrino |
| 2 | Grupos escondidos | "no es una población: son dos" | Mendel; Pearson 1894 |
| 3 | Régimen oculto | "no es una ley: son dos, con un umbral" | Reynolds; Onnes |
| 4 | Geometría | "la relación simple vive en otro espacio" | Kepler |
| 5 | Unificación | "estas dos cosas son la misma" | Newton; Maxwell |
| 6 | Invariante promovido | "eso que siempre da igual ES la regla" | Einstein; Noether |
| 7 | Proceso del observador | "el patrón está en cómo mirás" | Wald |
| 8 | Realimentación oculta | "la causa es el bucle" | Lotka-Volterra |
| 9 | Conservación / cuantos | "hay una cantidad fija (o en paquetes)" | Lavoisier; Planck |
| 10 | Memoria oculta | "el sistema arrastra su historia" | Ewing; Hurst |
| +1 | Transferencia estructural | "este sistema es AQUEL, con otra piel" | Darwin × Malthus |

Ahora sí, uno por uno:

---

## 1. La entidad oculta — "hay un actor invisible"

**La idea**: la anomalía no es error ni falla de tu teoría — es la sombra de algo que falta en
tu inventario del mundo.

**La historia**: 1846 — Urano no se mueve como Newton manda. Le Verrier, en vez de dudar de la
ley, postula **un planeta que nadie vio**, calcula dónde debería estar, manda la carta al
observatorio de Berlín — y Galle encuentra Neptuno **esa misma noche**, a menos de un grado de
lo predicho. Pauli repite la jugada en 1930: postula el neutrino ("un remedio desesperado":
una partícula invisible para salvar la conservación de la energía) — lo detectan 26 años
después. Y la materia oscura es la versión en curso: las galaxias giran como si hubiera seis
veces más masa de la que se ve.

**El riesgo opuesto**: el MISMO Le Verrier, envalentonado, postuló "Vulcano" para la anomalía de
Mercurio — y Vulcano no existía: la respuesta era cambiar la teoría (relatividad). Mismo
científico, misma jugada, un triunfo y un fiasco. **La jugada no es buena ni mala; el juicio
es saber cuándo.** Más adelante un gemelo puede convertir ese riesgo en un control, pero primero
validamos el mundo donde el salto sí hace falta.

**En WAGER**: pariente medido (latent_mix, era anterior: 0/10 postularon la composición);
mundo dedicado pendiente.

## 2. Los grupos escondidos — "no es una población: son dos"

**La idea**: lo que parece una población con mucha variabilidad es en realidad una MEZCLA de
tipos distintos.

**La historia**: Mendel cruza arvejas y ve proporciones raras pero repetidas (3 a 1) —
postula **unidades discretas invisibles** (los "factores", hoy genes) donde todos veían mezcla
continua: la herencia venía en paquetes, no en licuado. Y el primer capítulo de la estadística
moderna es este mismo salto: Pearson, 1894, ajusta la primera mezcla de dos campanas de la
historia a mediciones de cangrejos, sospechando que "una especie" eran dos. La versión
cotidiana: los pacientes que "responden a veces" al fármaco — hasta que alguien postula
respondedores y no-respondedores.

**El espejo**: ver grupos donde hay continuo (cualquier dataset "tiene clusters" si los buscás
con ganas).

**En WAGER**: el experimento **Grupos escondidos — Conteos por lote** (alias técnico histórico:
`count_mix`). En partidas sin ayuda, **0 de 9 agentes generó la idea** — el
único número de creatividad espontánea medido hasta hoy. Todos entregaron la versión “licuada”
(variación continua), que clava los promedios y jamás postula clases. La planta química probó
después otras situaciones y subpreguntas sobre este mismo salto; están separadas en la tabla final.

## 3. El régimen oculto — "no es una ley: son dos, con un umbral"

**La idea**: el sistema obedece una regla hasta cierto punto crítico, y OTRA regla de ahí en
más. El salto es partir el rango en dos.

**La historia**: Reynolds, 1883 — la resistencia del agua en cañerías daba resultados que
parecían contradecirse, hasta que postuló DOS regímenes (flujo ordenado / turbulento)
separados por una velocidad crítica, y lo demostró con un hilo de tinta que se mantiene nítido…
hasta que estalla. Kamerlingh Onnes, 1911 — la resistencia del mercurio helado desaparece DE
GOLPE y su equipo primero lo descarta como *"cortocircuito del equipo"* (¡el "debe ser un
error" está en la historia real!): era la superconductividad. La familia es enorme: el agua
que se congela, el imán que muere pasada la temperatura de Curie, los lagos que colapsan, las
recesiones, y todo el control de calidad industrial (Shewhart: detectar que el proceso cambió).

**El detalle fino**: en la realidad las transiciones casi nunca avisan por el promedio —
avisan por el TEMBLOR (la variabilidad cambia antes que la media). Mirar solo promedios es
cómo los observadores reales se las pierden.

**El espejo**: inventar quiebres en procesos suaves (ver escalones en el ruido).

**En WAGER**: el experimento **Régimen oculto — Proceso con umbral** (alias técnico histórico:
`count_regime`) tuvo dos situaciones. En v0, el escalón estaba a la vista, así que observamos
ACEPTACIÓN —la mitad lo llamó “outlier”—, no creatividad. Después se estudió la subpregunta del
fallo visible del propio modelo y apareció el cambio más grande observado: 0/9 sin fallo visible
y 30/30 con el fallo a la vista.

## 4. La geometría — "la relación simple existe, pero en otro espacio"

**La idea**: los datos no cambian — cambia el espacio donde los mirás, y lo retorcido se
vuelve recto.

**La historia**: Kepler peleó años contra las órbitas circulares (el prejuicio de mil años)
hasta rendirse a la evidencia de Marte: eran elipses. Y su tercera ley la encontró buscando
relaciones no entre las cantidades crudas sino entre sus **logaritmos** (T² ∝ a³ — invisible
en el espacio original, una recta en el otro). Minkowski, 1908: las fórmulas raras de la
relatividad se vuelven geometría limpia si aceptás que vivimos en espacio-TIEMPO.

**El espejo**: transformar por deporte hasta que algo dé lineal (con suficientes
transformaciones, cualquier cosa parece ley).

**En WAGER**: sin mundo aún.

## 5. La unificación — "estas dos cosas distintas son la misma"

**La idea**: dos fenómenos que parecían de mundos separados comparten UN mecanismo.

**La historia**: la luna que orbita y la manzana que cae eran DOS fenómenos de DOS mundos (el
celeste y el terrestre) — hasta que Newton dijo: es la misma fuerza, con la misma ley.
Maxwell, 1865: jugando con sus ecuaciones de electricidad y magnetismo aparece una onda que
viaja a… la velocidad de la luz. Conclusión: **la luz ES electromagnetismo** — tres fenómenos,
un mecanismo.

**El espejo** — y ojo, es EL espejo más peligroso para las IAs: el "todo está conectado" —
unir por parecido superficial cosas que no comparten mecanismo. Está medido: los LLMs producen
"conectá estas dos cosas" 4 veces más que los humanos al proponer ideas.

**En WAGER**: sin mundo aún; el par unificar↔conectar-de-más está doctrinado.

## 6. El invariante promovido — "eso que siempre da igual no es casualidad: ES la regla"

**La idea**: una regularidad que todos tratan como molestia o coincidencia se PROMUEVE a
axioma — y se deja caer lo que tenga que caer.

**La historia**: todos los experimentos daban la misma velocidad de la luz, te movieras como
te movieras — un fastidio que intentaban parchar (el éter). Einstein, 1905, hace la jugada
inversa: promueve el fastidio a **regla constitutiva** ("c es constante, PUNTO") y deja que
caiga lo que caiga (cayó el tiempo absoluto). En 1907 repite: "el que cae en caída libre no
siente su peso" — una obviedad de feria — se vuelve el principio de equivalencia, y de ahí
sale la relatividad general. Noether, 1918, lo eleva a teorema: cada simetría ES una ley de
conservación.

**El espejo**: promover a "ley" cualquier regularidad casual de la muestra (sobreajustar).

**En WAGER**: sin mundo aún. (La literatura reciente le puso nombre al paso que falta en las
IAs: "symmetry abduction" — usan la simetría para ajustar, nunca la proponen como principio.)

## 7. El proceso del observador — "el patrón no está en el mundo: está en cómo mirás"

**La idea**: entre el mundo y tus datos hay un FILTRO (qué sobrevive, qué se reporta, qué mide
tu instrumento) — y el patrón que ves puede ser del filtro, no del mundo.

**La historia**: Segunda Guerra — la fuerza aérea quería blindar los aviones donde volvían más
agujereados. Wald, estadístico, dio vuelta el tablero: los agujeros que ves son de los aviones
que VOLVIERON; blindá donde los que volvieron están intactos, porque los tocados ahí no
volvieron. Parientes cotidianos: el sesgo de publicación ("los estudios que fallan no se
publican"), las encuestas que solo oyen a quien atiende el teléfono.

**El espejo**: culpar al instrumento de todo patrón incómodo (la paranoia del sesgo).

**En WAGER**: sin mundo aún; candidato fuerte. El control opuesto también es nítido si más
adelante se decide construirlo.

## 8. La realimentación oculta — "la causa es el bucle"

**La idea**: nadie externo mueve al sistema — la salida vuelve a alimentar la entrada, y el
lazo solo genera el patrón.

**La historia**: los tramperos de la Hudson Bay registraron 90 años de pieles: linces y
liebres suben y bajan en ondas de ~10 años, desfasadas. ¿El clima? ¿El sol? Lotka y Volterra
(años 20) mostraron que NADA externo hace falta: dos poblaciones que se comen una a la otra
oscilan SOLAS — más liebres→más linces→menos liebres→menos linces→… La familia: el regulador
de Watt, el termostato, las burbujas financieras.

**El espejo**: ver bucles donde hay un tercero común que mueve a ambos.

**En WAGER**: sin mundo aún.

## 9. La conservación / los cuantos — "hay una cantidad fija (o que viene en paquetes)"

**La idea**: postular la cantidad que no se crea ni se destruye — o que lo continuo es en
realidad granulado.

**La historia**: Lavoisier pesa TODO — reactivos, productos, el vaso cerrado — y descubre que
la masa se conserva (y con eso mata al flogisto). Proust: los compuestos se combinan siempre
en proporciones FIJAS — y Dalton salta: porque la materia viene en paquetes (átomos). Planck,
1900, "en un acto de desesperación": la energía también viene en paquetes — nace la cuántica
contra la voluntad de su propio autor. Millikan: la carga eléctrica solo aparece en múltiplos
enteros de algo — el electrón.

**El espejo**: inventar cantidades conservadas que no existen (numerología).

**En WAGER**: sin mundo aún; candidato fuerte a mundo 3.

## 10. La memoria oculta — "el sistema arrastra su historia"

**La idea**: el estado visible no alcanza para predecir — hay una variable escondida que
acumula el pasado.

**La historia**: Ewing (1880s) magnetiza hierro y descubre que al apagar el campo el hierro NO
vuelve: recuerda por dónde pasó (inventa la palabra "histéresis"). Hurst (1950s), diseñando la
represa del Nilo, estudia 800 años de crecidas y encuentra que los años secos y húmedos se
AGRUPAN — el río tiene memoria larga, y las fórmulas estándar (que asumían independencia)
subdimensionaban la represa.

**El espejo**: ver rachas y "memoria" en el azar puro (la falacia del apostador).

**En WAGER**: sin mundo aún.

## +1. La transferencia estructural — "este sistema es AQUEL, con otra piel"

**La idea**: reconocer que el sistema que investigás comparte ESQUELETO con otro ya entendido
— y transplantar el mecanismo.

**La historia**: septiembre de 1838 — Darwin, con el problema de la evolución atascado, lee
"por entretenimiento" a Malthus: un ensayo de ECONOMÍA sobre poblaciones humanas que crecen
más rápido que la comida. Y ahí está: lucha por recursos + variación heredable = selección. El
mecanismo que le faltaba a la biología estaba escrito en otro dominio. Shannon repite la
jugada en 1948: su fórmula de la información ES la entropía de Boltzmann, transplantada de la
física al telégrafo.

**El espejo**: la analogía falsa — parecido de superficie sin esqueleto común (el átomo como
"sistemita solar": útil un rato, falso en el fondo). Dato medido clave: la memoria humana
recupera análogos por parecido superficial (70% con parecido vs 30% sin él) — y los
descubrimientos reales usan analogías CERCANAS, no el salto romántico lejano (de 99 analogías
grabadas en laboratorios de élite, solo 2 fueron lejanas y ninguna descubrió nada).

**En WAGER**: la línea overgen (era anterior) ya construyó este par.

---

## Estado de medición, en una mirada

Los nombres legibles van primero; los códigos entre paréntesis solo sirven para encontrar los
archivos históricos.

| Salto | Experimentos y situaciones estudiadas | Qué sabemos |
|---|---|---|
| **Grupos escondidos** | ✅ **Grupos escondidos — Conteos por lote** (`count_mix`; observación sin ayuda) · ✅ **Grupos escondidos — Planta química** (`D1`; modelo final) · ⛔ **Grupos escondidos — Planta a alta temperatura** (`D2`; subpregunta de error visible, cancelada antes de la tanda principal) | **0/9** generaron los grupos espontáneamente. En la planta, con la disyuntiva disponible y evidencia comprada por ellos, los escribieron **2/15**; un aviso neutral no cambió eso (**1/15**). Pero Lucas encontró que allí una buena campana simple ya sacaba **0.986/1.0**: el salto casi no mejoraba la vara y no tenía una consecuencia visible. El intento siguiente tampoco quedó validado: un rival de un solo grupo llegó a **0.67/1.0**, el evento casi no lo distinguía de la verdad (débito esperado **31.1 vs 30.0**) y el aviso de error no podía ocurrir en 5/6 pruebas. **Conclusión: el 0/9 espontáneo es real; la planta todavía no demuestra que evitar el salto sea irracional.** |
| **Régimen oculto** | ✅ **Régimen oculto — Proceso con umbral** (`count_regime`; v0: quiebre visible · v1: fallo del propio modelo visible) | La primera situación midió aceptación, no generación. En la segunda: **0/9 sin fallo visible → 30/30 con el fallo del propio modelo a la vista**. Sabemos que el choque puede disparar este salto en ese modelo y ese mundo; todavía no que sea el único motor. |
| **Transferencia estructural** | ✅ **Transferencia de la regla local — Dos dominios gemelos** (`overgen`) | Par medido en su era. |
| **Entidad oculta, geometría, unificación, invariante, observador, realimentación, conservación y memoria** | Sin experimento todavía | — |

---

## Comentarios (el meta: de dónde sale esto, cuánto confiar)

- **¿La lista es inventada?** No: **curada** — con regla de entrada explícita (≥2 tradiciones
  independientes + ≥2 casos históricos documentados) y cinco pilares de justificación por
  operador. El más contundente: **cada salto nombra una estructura tan real que la estadística
  tuvo que inventar una familia de métodos para detectarla** (mezclas→EM; quiebres→changepoint;
  observador→corrección de Heckman, premio Nobel; memoria→exponente de Hurst). Y el careo con
  TODO lo publicado dio: la lista única curada **no existe en el campo** (sus referentes lo
  declaran); donde lo publicado se cruza con lo nuestro, coincide (la filosofía de la abducción
  calza exacto en unificación y transferencia; el caso ancla de Darden ES nuestro salto 2); en
  los 6 saltos "dinámicos" vamos más allá de los espacios formales existentes. Estado honesto:
  **bien fundada, no firmada** (falta el expediente de ≥2 casos con fuente por operador y la
  validación con anotadores en etapa paper).
- **Candidatos a la lista** (del careo con la literatura, en evaluación): **borrar estructura**
  (todos los nuestros agregan piezas; "sobra una pieza" no está — de Darden) y **reemplazar
  mecanismo** (flogisto→oxígeno — de Chen).
- **La distinción que manda**: medimos **GENERAR** el candidato cuando
  nada lo dicta (creatividad) — no aceptarlo cuando la evidencia lo grita (eso es revisión de
  creencias y se registra aparte).
- **Para profundizar**: las historias completas con fuentes y estado de lectura:
  [docs/saltos.md](docs/saltos.md) (el libro) · la justificación formal (matriz
  componente×edición): [fundamentos](docs/research/2026-08-05-fundamentos-taxonomia-de-saltos.md) ·
  hermanos: [WIKI-INDAGACION](WIKI-INDAGACION.md) · [WIKI-FALLAS](WIKI-FALLAS.md) · [WIKI](WIKI.md).
