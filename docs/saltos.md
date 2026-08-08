# El libro de los saltos — cada uno contado en llano, con su historia y sus fuentes

> **Qué es esto** (pedido de Lucas, 2026-08-07): la versión narrada de la taxonomía — cada tipo
> de salto contado como historia, con sus casos históricos, su jugada creativa, su espejo (la
> forma de equivocarse en la dirección opuesta) y su estado en WAGER. La versión formal (matriz
> componente×edición, regla de entrada, triangulación) vive en
> [fundamentos-taxonomia-de-saltos](research/2026-08-05-fundamentos-taxonomia-de-saltos.md).
>
> **Honestidad de fuentes**: los episodios históricos son conocimiento general verificable pero
> AÚN NO fichado con lectura propia (la casa distingue: solo se cita en el paper lo leído a
> texto completo — esa cola está declarada en fundamentos §8). Lo que SÍ está leído completo
> con citas: el paper can't-jump, Chen/Zhao/Cohan, DiscoverPhysics, NewtonBench/LLM-SRBench
> (registro en [lectura-de-fuentes](lectura-de-fuentes.md)).

## Antes de la lista: qué es un salto (y el paper que le da nombre al problema)

**La idea central viene de Peirce** (lógico, ~1900): hay tres formas de razonar. **Deducción**:
tengo la regla, aplico ("todos los lotes de la máquina A salen fallados; este es de A; va a
salir fallado"). **Inducción**: veo casos, saco el patrón ("estos 200 lotes promedian 6
defectos; el proceso promedia 6"). Y **abducción**: pasa algo sorprendente e **invento la causa
que lo explicaría** ("¿y si en realidad son dos máquinas mezcladas?"). La abducción es la única
de las tres que CREA — las otras dos ordenan lo que ya está.

**Precisión que importa (pregunta de Lucas): salto ≠ toda abducción — salto = abducción
CREATIVA.** La filosofía tiene EXACTAMENTE nuestra distinción, con nombres (Magnani,
*Abduction, Reason and Science* 2001 `[POR-LEER]`): **abducción selectiva** = elegir la
hipótesis de un repertorio que ya tenés (el médico que diagnostica elige entre enfermedades
conocidas) vs **abducción creativa** = la explicación exige una hipótesis que el repertorio NO
contiene — hay que agrandarlo. Nuestro hallazgo empírico dicho en ese idioma: los LLMs hacen
abducción SELECTIVA bien (eligen, ajustan y comparan dentro del menú) y la CREATIVA no arranca
(el menú no crece — 0/9 en count_mix). Y sí hay teoría de TIPOS: **Schurz, "Patterns of
Abduction" (Synthese 2008)** `[LEÍDO completo 2026-08-07]` — taxonomía sistemática (abducción de
hechos / de leyes / de modelos teóricos / **existencial** [postular entidades: Neptuno] / de
**causa común** [unificación] / **analógica** [Darwin]) que mapea directo a operadores
nuestros. **La tabla de alineación (leída) dio:** correlato EXACTO en unificación (su causa común — Newton es su ejemplo) y transferencia (su abducción analógica); parcial en entidad oculta y grupos; y en 7 de 11 operadores NUESTRO grano es más fino que el suyo (taxonomías ortogonales: él clasifica el tipo epistémico, nosotros la edición al programa). Bonus: su 'abducción ESPECULATIVA' (una entidad por fenómeno, ad hoc) es el anti-patrón de nuestros gemelos, con criterio de demarcación contable sin LLM (¿cuántos fenómenos independientes unifica lo postulado?). [Detalle](research/2026-08-07-lecturas-programa-saltos.md). Alrededor: Thagard (4 tipos
computacionales, 1988), Aliseda (*Abductive Reasoning* 2006 — abducción COMO revisión de
creencias: nuestras dos líneas en un marco), Gabbay & Woods, Hintikka `[POR-LEER todos]`.

**El paper "Position: LLMs can't jump"** (OpenReview klU4737opt; LEÍDO completo 2026-07-10)
sostiene que los LLMs dominan la inducción, mejoran en deducción, y son *"structurally
incapable of the abductive jump"* — el salto de la experiencia a **axiomas nuevos**. Su caso de
estudio es Einstein, y su ejemplo central es nuestro par de siempre: ante la anomalía de
Mercurio, una IA compresora prefiere **parchar** (postular el planeta Vulcano — un parámetro
más) antes que **reestructurar** (geometría del espacio-tiempo — que complica antes de
simplificar). Dos puntos más del paper que nos ordenan el programa: (1) los saltos más grandes
ocurrieron **sin señal de error** (la gravedad de Newton estaba confirmada a 10⁻⁹ y Einstein
reestructuró igual) — ese techo es impuntuable para cualquiera (puntuar ES prometer un examen);
lo medible es la escalera de abajo: *cuánta evidencia hace falta para que compren el salto*.
(2) Proponen como laboratorio los mundos interactivos con intervención — que es exactamente lo
que construimos.

**Nuestra definición operativa** (la que permite puntuar sin poesía): un mundo es un programa
que genera datos. **Refinar** = cambiarle los números. **Saltar** = cambiarle la FORMA: qué
variables existen, cómo se conectan, bajo qué restricciones, cómo se convierte en datos. Cada
tipo de salto de abajo es UNA forma concreta de cambiar la forma. Y la distinción que manda
(Lucas, 2026-08-07): medimos **GENERAR** el candidato cuando nada lo dicta (creatividad), no
aceptarlo cuando la evidencia lo grita (eso es revisión de creencias — se anota aparte).

## ¿La lista es inventada? — la formalidad y sus antecedentes (pregunta de Lucas, 2026-08-07)

**Confesión primero: la lista EXACTA de 11 es síntesis nuestra** — ningún paper publicó "estos
son los 11 saltos". Lo que NO es intuición suelta:

**¿Y no existe YA una lista curada de tipos de saltos/insights/abducciones?** (segunda pregunta
de Lucas, misma noche). **NO — y el propio campo lo declara.** El estado del arte, verificado
por lectura: Schurz `[LEÍDO]` clasifica QUÉ se abduce, no la movida, y es grueso donde importa
("no hay patrón general" para la abducción de modelos teóricos); Darden `[5 artículos LEÍDOS 2026-08-08; libro POR-LEER]` es lo más
cercano pero un solo dominio y sin validación; Thagard = escala de severidad, no tipología;
Boden = 3 baldes; Ohlsson = mecanismos de proceso mental (en acertijos, no en ciencia); Kemp &
Tenenbaum `[LEÍDO]` = formas estáticas, y ELLOS piden la "Universal Structure Grammar" que no
existe; Chen et al. `[LEÍDO]` = la única validada con anotadores, pero de operaciones sobre
ideas de papers — y tuvieron que construirla de cero en 2026 porque no había ninguna que
heredar. **Consecuencia: la taxonomía no es background del paper — es una de sus
contribuciones**, y se construye con el método de las taxonomías buenas (regla de entrada
explícita + expedientes de casos + falsabilidad del marco + anotadores en etapa paper), no por
gusto.

1. **El marco tiene linaje formal — VERIFICADO A TEXTO COMPLETO** (2026-08-07): Ullman,
   Goodman & Tenenbaum 2012 `[LEÍDO]` formaliza EXACTAMENTE "teoría = programa; aprender =
   ediciones estructurales" (MCMC sobre agregar/borrar/cambiar leyes y predicados, con los
   conceptos nuevos naciendo EN BLANCO y ganando significado por su rol); Kemp & Tenenbaum
   2008 `[LEÍDO]` da el espacio formal de FORMAS (gramáticas de grafos: árbol/anillo/cadena/
   grilla) descubribles desde datos. **El veredicto de la alineación**: cubren sólido 2 de
   nuestros 11 operadores y parcial 3; los 6 dinámicos (régimen, feedback, memoria, observador,
   reparametrizar, cuantizar) NO existen en sus espacios — Ullman mismo nombra la extensión
   necesaria ("a functional language… much more expressive"). Nuestra taxonomía = la lista de
   ediciones que ese lenguaje necesita: ni huérfana ni ya-hecha. DreamCoder/LILO (en cola) son
   la versión moderna. [Detalle](research/2026-08-07-lecturas-programa-saltos.md).
2. **Existen taxonomías con análisis de casos, y una es casi hermana:** **Darden** — sus 5
   artículos accesibles `[LEÍDOS completos 2026-08-08]` (el libro 1991 sigue POR-LEER, espera
   PDF): estrategias de cambio de teoría desde casos reales. **El careo dio**: coincidencia
   fuerte en ops 1/2/7/8/11 — su caso ancla (postular genes letales para la anomalía 2:1) ES
   literalmente nuestro operador 2; su schema-instantiation es nuestro 11 con mecánica más
   fina. Sin correlato en ella: nuestros 3/4/6/9/10 (saltos de estructura matemática — su
   catálogo es de mecanismos biológicos por etapas; el nuestro es más ancho). **Candidatas que
   ella tiene y nosotros no**: BORRAR estructura (¡todos nuestros operadores agregan!),
   systematic scan (cobertura anti-fijación), ensamblado modular, y la localización guiada por
   la FIRMA de la anomalía (2:1 pide una edición distinta que 1:0:1). Más su tipología
   monster/model/special-case para el lado de los vicios.
   [Extracción](research/2026-08-07-lecturas-programa-saltos.md). También: Thagard (*Conceptual Revolutions*, 9 grados de
   cambio conceptual con casos) `[POR-LEER]`; Boden (3 tipos; la transformacional = cambiar el
   espacio) `[POR-LEER]`; y en era-LLM la taxonomía de operaciones de Chen `[LEÍDO]` —
   **validada con anotadores independientes**, el estándar que copiamos como receta.

**Chen vs nuestra lista — la comparación fina (pregunta de Lucas, 2026-08-08).** Clasifican
OBJETOS distintos: Chen etiqueta qué le hace una IDEA DE PAPER a la literatura previa (2 ejes
de 7: por qué vale — puzzle, hueco de explicación, oportunidad-puente… × cómo se vuelve
contribución — síntesis/unificación, extender alcance, derivación formal, artefacto…);
nosotros etiquetamos qué le hace una EXPLICACIÓN al modelo del sistema investigado. El mapeo
donde se cruzan: su *síntesis/unificación* y *oportunidad-puente* ↔ nuestros 5/11 — y son
las que los LLMs SOBRE-usan (¡el lado del gemelo!); su *derivación formal* ↔ nuestros 4/9
(sub-usada); su *desacoplar* ↔ nuestra familia partir-en-dos 2/3 (10× menos que humanos). La
asimetría clave: la mayoría de sus etiquetas NO son saltos (robustificar, mapear, optimizar —
ciencia normal) y la mayoría de nuestros saltos no tienen etiqueta ahí (régimen, memoria,
observador, feedback, conservación — la idea-de-paper no descompone la estructura del
sistema). **Veredicto: referencia principal para el MÉTODO de validación (su receta 7×7:
fuentes autoritativas → refinar en 150 papers held-out → κ 0.81-0.93 con anotadores) y para
la EVIDENCIA del sesgo LLM; NO como taxonomía madre — mide otro nivel del mismo fenómeno.**
Importación candidata: su *reemplazar* (swap de mecanismo entero — flogisto→oxígeno,
calórico→cinética, éter→campo) no tiene operador nuestro limpio → candidato a la matriz, con
casos históricos fuertes. Extracción completa del método: [como-medimos §1](como-medimos.md).
**Los cinco pilares, operador por operador** (pregunta de Lucas: "¿cómo sabemos que no son
invención nuestra?"). El pilar más fuerte es el ③: **cada operador nombra una estructura tan
real que la estadística tuvo que inventar una FAMILIA DE MÉTODOS para detectarla** — nadie
funda una industria de métodos alrededor de una estructura sin sentido:

| Operador | ① Casos históricos | ② Filosofía (Schurz) | ③ El método que la estadística tuvo que inventar | ④ Modelo computacional corrido | ⑤ Evidencia LLM |
|---|---|---|---|---|---|
| 1 entidad oculta | Neptuno · neutrino · materia oscura | existencial 1er orden (parcial) | variables latentes, factor analysis | parcial (Ullman: predicado en blanco) | DiscoverPhysics ✓ |
| 2 grupos escondidos | Mendel · Pearson 1894 | causa común estricta (parcial) | **modelos de mezcla + algoritmo EM** | ✓ (Kemp partition; Ullman tipos) | nuestro 0/9 ✓ · Chen ✓ |
| 3 régimen oculto | Reynolds · Onnes · Curie | — | **changepoint detection: Shewhart, CUSUM (Page 1954), Markov-switching (Hamilton)** | — | nuestro mundo 2 ✓ |
| 4 geometría | Kepler · Minkowski | — | transformaciones, manifold learning | — | — |
| 5 unificación | Newton · Maxwell | **causa común (EXACTO)** | principio de Reichenbach, causa común | — | Chen (espejo: sobre-conectar) ✓ |
| 6 invariante | Einstein · Noether | — (Footsteps: "symmetry abduction") | teorema de Noether; invariance en ML | — | Footsteps ✓ |
| 7 observador | Wald | — | **corrección de Heckman (Nobel), censura, datos faltantes (Rubin)** | — | — |
| 8 realimentación | Lotka-Volterra · Watt | — | teoría de control, cibernética (Wiener) | — | — |
| 9 conservación | Lavoisier · Planck · Millikan | — | leyes de conservación; physics-informed ML | — | — |
| 10 memoria | Ewing · Hurst | — | **exponente de Hurst**, HMM, memoria larga | — | — |
| 11 transferencia | Darwin · Shannon | **analógica (EXACTO)** | transfer learning; Structure-Mapping Engine | parcial (templates de Ullman) | Gentner + Lewis & Mitchell ✓ |

Lectura honesta de la tabla: **① y ③ están llenos para los 11** (pendiente: fichar las fuentes
de ① — eso es "firmar"); ② cubre 4; ④ es la vara más exigente (2 sólidos) y su vacío es
NUESTRA contribución, no nuestra debilidad; ⑤ crece con cada mundo que medimos.

**El reencuadre que resume todo (2026-08-08):** la "lista curada de saltos" que buscamos
existe implícita desde hace décadas — es **el ÍNDICE de un manual de modelado estadístico**
(mezclas · puntos de cambio · variables latentes · selección/censura · realimentación ·
memoria · transformaciones · restricciones/conservación). Cada capítulo existe porque la
ciencia se topó tantas veces con ESA estructura que hubo que darle método propio. Nadie leyó
nunca ese índice como "el catálogo de los saltos posibles". **Nuestra taxonomía es esa
relectura**: el inventario implícito del manual, vuelto explícito, ejecutable (cada operador
compila a un mundo con certificados) y validable. Lo más cercano publicado en nuestro nivel:
las estrategias de Darden (en lectura de sus artículos accesibles; el libro espera PDF).

3. **Qué le falta a la nuestra para estar FIRMADA** (el trabajo declarado en fundamentos §8):
   (a) leer Darden/Thagard/Boden/Ohlsson a texto completo y hacer la **tabla de alineación**
   operador-por-operador (cobertura, sobras, faltantes contra lo que ellos hallaron en casos
   reales); (b) el expediente de **≥2 casos históricos con fuente por operador**; (c) en etapa
   paper, validación con anotadores independientes (κ) a la Chen. Hasta entonces el estado
   honesto es: **bien fundada, no firmada** — y la incompletitud es detectable (un salto
   histórico que no sea edición de ningún componente rompe el marco, y eso sería un hallazgo).

---

## 1. La entidad oculta — "hay un actor invisible"

**La historia.** 1846: Urano no se mueve como Newton manda. Le Verrier, en vez de dudar de la
ley, postula **un planeta que nadie vio**, calcula dónde debería estar, manda la carta a
Berlín — y Galle encuentra Neptuno esa misma noche, a menos de un grado de lo predicho. La
jugada: la anomalía no es error ni falla de la teoría — es la sombra de algo que falta en el
inventario del mundo. Otros dos de la familia: Pauli 1930 postula el neutrino ("un remedio
desesperado": una partícula invisible para salvar la conservación de la energía — la detectan
26 años después); Zwicky/Rubin postulan la materia oscura (las galaxias giran como si hubiera
seis veces más masa de la que se ve).

**El espejo.** El MISMO Le Verrier, envalentonado, postula "Vulcano" para la anomalía de
Mercurio — y Vulcano no existía: la respuesta era cambiar la teoría (relatividad). Mismo
científico, misma jugada, un triunfo y un fiasco: **la jugada no es buena ni mala — el juicio
es saber cuándo**. Por eso todo mundo nuestro viene con gemelo.

**En LLMs / en WAGER**: DiscoverPhysics (LEÍDO): los frontier fallan justo en los mundos con
especies/materia oscura latentes. Nuestro trofeo de julio (latent_mix: 0/10 postulan la
composición). Mundo dedicado del programa: pendiente (el par Neptuno/Vulcano está doctrinado).

## 2. Los grupos escondidos — "no es una población, son dos"

**La historia.** Mendel cruza arvejas y ve proporciones raras pero repetidas (3 a 1). La jugada:
postular **unidades discretas invisibles** (los "factores", hoy genes) donde todos veían mezcla
continua — la herencia venía en paquetes, no en licuado. Y el primer capítulo de la estadística
moderna es literalmente este salto: Pearson 1894 ajusta la PRIMERA mezcla de dos campanas de la
historia a mediciones de cangrejos de Nápoles, sospechando que "una especie" eran dos. Versión
moderna cotidiana: los pacientes que "responden a veces" al fármaco — hasta que alguien postula
respondedores y no-respondedores (y el gen que los separa).

**El espejo.** Ver grupos donde hay continuo (la apofenia del clustering: cualquier dataset
"tiene clusters" si los buscás con ganas).

**En WAGER**: ES nuestro mundo 1 (count_mix). Resultado: **0/9 lo genera** — entregan
heterogeneidad continua (la versión licuada) que clava los promedios y jamás postula clases.
El único número de creatividad medido hasta hoy.

## 3. El régimen oculto — "no es una ley: son dos, con un umbral"

**La historia.** Reynolds 1883: la resistencia del agua en cañerías da resultados que parecen
contradecirse — hasta que postula DOS regímenes (laminar/turbulento) separados por una
velocidad crítica, y lo demuestra con un hilo de tinta que se mantiene nítido… hasta que
estalla. Kamerlingh Onnes 1911: la resistencia del mercurio helado desaparece DE GOLPE — y su
equipo primero lo descarta como **"cortocircuito del equipo"** (¡el "debe ser un error" está en
la historia real!). La familia: el agua que se congela, el imán que muere pasada la temperatura
de Curie, los lagos que colapsan, las recesiones (modelos de cambio de régimen en economía
desde los 80), y TODO el control de calidad (Shewhart, años 20: detectar que el proceso
cambió).

**El detalle fino para diseñar**: en la realidad las transiciones casi nunca avisan por el
promedio — avisan por el TEMBLOR (opalescencia crítica; "señales tempranas" en ecología/clima:
la variabilidad cambia antes que la media). Mirar solo promedios es cómo los observadores
reales se las pierden.

**En LLMs**: dos piezas, de papers DISTINTOS — (1) [Chen, Zhao & Cohan, arXiv 2607.01233](https://arxiv.org/abs/2607.01233)
`[LEÍDO completo]` (el paper que linkeó Lucas en julio): los LLMs evitan la operación
"desacoplar/partir en dos" al proponer ideas (2.3% humanos vs 0.2% modelos — ~10×
menos), y este salto es esa operación aplicada a un rango; (2) [KellyBench, arXiv 2604.27865](https://arxiv.org/abs/2604.27865)
`[LEÍDO completo 2026-08-07]` (temporada EPL simulada, 500–1000 tool-calls): todos pierden en
promedio (mejor −7.9%); OJO, sin switch inyectado — la no-estacionariedad es la natural del
dominio; 7/25 nunca reentrena, adaptativos −11.1% vs estáticos −70.0%, y la firma fina es el
**knowledge-action gap**: diagnostican su falla POR ESCRITO y no corrigen (uno escribió tres
documentos de autocrítica y no cambió nada) — la versión a escala de nuestro espécimen
"outlier". [Extracción](research/2026-08-07-lecturas-programa-saltos.md).

**El espejo.** Inventar quiebres en procesos suaves (ver escalones en el ruido).

**En WAGER**: mundo 2 (count_regime) construido y certificado — pero la v0 tenía el escalón a
la vista, así que midió aceptación, no invención (la mitad lo descartó como "outlier"/"ruido" —
Onnes en versión LLM). La versión que mide INVENCIÓN (cambio escondido en el carácter, promedio
suave) está diseñada y pendiente de GO.

## 4. La geometría — "la relación simple existe, pero en otro espacio"

**La historia.** Kepler pelea AÑOS contra las órbitas circulares (el prejuicio de mil años)
hasta rendirse a la evidencia de Marte: son elipses. Y su tercera ley la encuentra buscando
relaciones no entre las cantidades crudas sino entre sus **logaritmos** (T² ∝ a³ — invisible en
el espacio original, una recta en el otro). Minkowski 1908: las fórmulas raras de la
relatividad se vuelven geometría limpia si aceptás que vivimos en espacio-TIEMPO. La jugada
común: los datos no cambian — **cambia el espacio donde los mirás**, y lo retorcido se vuelve
recto.

**El espejo.** Transformar por deporte hasta que algo dé lineal (con suficientes
transformaciones, cualquier cosa parece ley).

**En WAGER**: sin mundo aún. Candidato natural de la matriz.

## 5. La unificación — "estas dos cosas distintas son la misma"

**La historia.** La luna que orbita y la manzana que cae eran DOS fenómenos de DOS mundos (el
celeste y el terrestre) — hasta que Newton dice: es la misma fuerza, con la misma ley. Maxwell
1865: jugando con sus ecuaciones de electricidad y magnetismo aparece una onda que viaja a…
la velocidad de la luz. Conclusión: **la luz ES electromagnetismo** — tres fenómenos, un
mecanismo. La jugada: fundir dos ramas del árbol causal en una.

**El espejo.** El "todo está conectado": unir por parecido superficial cosas que no comparten
mecanismo. Ojo acá — es el espejo MÁS peligroso para LLMs: Chen/Zhao/Cohan (LEÍDO) midieron
que sobre-producen "conectá estas dos cosas" (47-64% de sus ideas vs 12% en humanos) y que
razonar MÁS lo empeora.

**En WAGER**: sin mundo aún; el par unificar↔apofenia-de-conexión está doctrinado en el
catálogo de pares.

## 6. El invariante promovido — "eso que siempre da igual no es casualidad: es LA regla"

**La historia.** Todos los experimentos daban la misma velocidad de la luz, te movieras como te
movieras — un fastidio experimental que intentaban parchar (el éter, contracciones ad hoc).
Einstein 1905 hace la jugada inversa: promueve el fastidio a **axioma** ("c es constante,
PUNTO") y deja que caiga lo que tenga que caer (cayó la simultaneidad, el tiempo absoluto…).
En 1907 repite: "el que cae en caída libre no siente su peso" — una obviedad de feria — se
vuelve el principio de equivalencia y de ahí sale la relatividad general. Y Noether 1918 lo
eleva a teorema: cada simetría ES una ley de conservación. La jugada: darle jerarquía de regla
constitutiva a lo que parecía coincidencia banal.

**El espejo.** Promover a "ley" cualquier regularidad de la muestra (sobreajustar la
casualidad).

**En LLMs**: [Einstein's Footsteps](https://arxiv.org/abs/2607.27794) `[LEÍDO completo
2026-08-07]` le pone NOMBRE al paso faltante: **"symmetry abduction"** — los métodos actuales
usan la simetría como filtro para ajustar datos; falta proponerla como principio GENERADOR
("the crucial step"). De 4 casos reales (Laughlin, Bethe, Ginzburg-Landau, Parisi) abstrae la
estructura: *"imponer una hipótesis estructurada extra (ansatz, simetría, gauge) — forzando
simplicidad ANTES de deducir consecuencias falsables"*. Y agrega la media naranja de la vara:
*"Novelty is cheap"* — lo difícil no es generar la idea sino estimar su rendimiento
(payoff-per-effort, el "taste") → nuestros mundos deberían cobrar también la mala SELECCIÓN de
saltos. Bonus: endosa textualmente nuestra metodología ("We can give AI systems artificial
worlds with hidden laws and test whether they can invent simple theories inside those worlds").

**En WAGER**: sin mundo aún.

## 7. El proceso del observador — "el patrón no está en el mundo: está en cómo mirás"

**La historia.** Segunda guerra: la fuerza aérea quiere blindar los aviones donde vuelven más
agujereados. Wald, estadístico, da vuelta el tablero: los agujeros que ves son de los aviones
que VOLVIERON — blindá donde los que volvieron están intactos, porque los tocados ahí no
volvieron. La jugada: postular que entre el mundo y tus datos hay un FILTRO (supervivencia,
selección, censura, el instrumento) y modelarlo. Parientes cotidianos: el sesgo de publicación
("los estudios que fallan no se publican"), el amigo que dice "los tele-encuestados apoyan X"
(¿quién atiende encuestas?).

**El espejo.** Culpar al instrumento de todo patrón incómodo (la paranoia del sesgo).

**En WAGER**: sin mundo aún; candidato fuerte porque su gemelo es nítido.

## 8. La realimentación oculta — "la causa es el bucle"

**La historia.** Los tramperos de la Hudson Bay registran 90 años de pieles: los linces y las
liebres suben y bajan en ondas de ~10 años, perfectamente desfasadas. ¿Qué las mueve? ¿El
clima? ¿El sol? Lotka y Volterra (años 20) muestran que NADA externo hace falta: dos
poblaciones que se comen una a la otra oscilan SOLAS — **la causa es el circuito** (más
liebres→más linces→menos liebres→menos linces→…). La jugada: cerrar la flecha causal en un
lazo, cuando todo el instinto busca un culpable externo. Familia: el regulador de Watt, el
termostato, la cibernética de Wiener, las burbujas financieras (la reflexividad de Soros).

**El espejo.** Ver bucles donde hay un tercero común que mueve a ambos.

**En WAGER**: sin mundo aún.

## 9. La conservación / cuantización — "hay una cantidad que no se crea ni se destruye (o que viene en paquetes)"

**La historia.** Lavoisier pesa TODO — reactivos, productos, el vaso cerrado — y descubre que
la masa ni aparece ni desaparece: se conserva (y con eso mata al flogisto). Proust: los
compuestos se combinan siempre en proporciones FIJAS — y Dalton salta: porque la materia viene
en paquetes (átomos). Planck 1900, "en un acto de desesperación": la energía también viene en
paquetes — y nace la cuántica contra la voluntad de su propio autor. Millikan: la carga
eléctrica solo aparece en múltiplos enteros de algo — el electrón. La jugada doble: postular la
cantidad que se conserva, o postular que lo continuo es en realidad granulado.

**El espejo.** Inventar cantidades conservadas que no existen (numerología).

**En WAGER**: sin mundo aún; con el 3 y el 6, el candidato más fuerte a mundo 3.

## 10. La memoria oculta — "el sistema no depende solo de su presente: arrastra su historia"

**La historia.** Ewing (1880s) magnetiza hierro y descubre que al volver el campo a cero el
hierro NO vuelve: recuerda por dónde pasó (histéresis — él inventa la palabra). Hurst (1950s),
diseñando la represa del Nilo, estudia 800 años de crecidas y encuentra que los años secos y
húmedos se AGRUPAN — el río tiene memoria larga, y las fórmulas estándar (que asumían
independencia) subdimensionaban la represa. La jugada: el estado visible no alcanza — hay una
variable escondida que acumula el pasado.

**El espejo.** Ver rachas y "memoria" en el azar puro (la falacia del apostador).

**En WAGER**: sin mundo aún.

## +1. La transferencia estructural — "este sistema es AQUEL, con otra piel" (Darwin)

**La historia.** Septiembre de 1838: Darwin, con el problema de la evolución atascado, lee "por
entretenimiento" a Malthus — un ensayo de ECONOMÍA sobre poblaciones humanas que crecen más
rápido que la comida. Y ahí está: la lucha por recursos + la variación heredable = selección.
El mecanismo que le faltaba a la biología estaba escrito en otro dominio; el salto fue
reconocer que los dos sistemas comparten ESQUELETO (variación + competencia + herencia) y
transplantar. Shannon 1948 repite la jugada: su fórmula de información ES la entropía de
Boltzmann, transplantada de la física al telégrafo. La teoría formal de esta jugada existe:
structure-mapping de Gentner (mapear RELACIONES, no parecidos superficiales).

**El espejo.** La analogía falsa: parecido de superficie sin esqueleto común (el átomo como
"sistemita solar" — útil un rato, falso en el fondo). Lewis & Mitchell midieron que la
analogía de los LLMs colapsa justo cuando el problema deja de parecerse superficialmente a lo
conocido.

**La teoría, ahora fichada** ([Gentner OECS 2025](https://groups.psych.northwestern.edu/gentner/papers/Gentner-Analogy-OECS2025.pdf)
`[LEÍDO completo 2026-08-07]`): la transferencia va en tres etapas (recuperar el análogo →
mapear → evaluar), y el dato duro para nuestro gemelo es que **la recuperación espontánea está
dominada por la SUPERFICIE** (70% recupera el análogo con parecido superficial vs 30% sin él —
Trench & Minervino 2015). Criterios computables de transferencia válida: correspondencias 1-a-1
por ROL, que lo compartido sea un SISTEMA causal (no rasgos sueltos), y que lo transplantado no
contradiga lo ya sabido del destino — el check que la analogía falsa saltea. Regla de diseño
que la teoría obliga: en la vida real superficie y estructura correlacionan, así que el mundo
del gemelo debe DESCORRELACIONARLAS a propósito. Y existe implementación sin LLM de estos
criterios (el Structure-Mapping Engine) — compatible con nuestro reward.
[Extracción](research/2026-08-07-lecturas-programa-saltos.md).

**En WAGER**: nuestra línea overgen (sobre-generalización y su gemelo) ya es este par,
construida y certificada en la era anterior.

---

## El mismo juego con otros trajes (pregunta de Lucas, 2026-08-08)

**¿La investigación detectivesca es lo nuestro? SÍ — y no por analogía: por identidad.** Peirce
inventó la abducción pensando en detectives (el volumen clásico *The Sign of Three*, Eco &
Sebeok 1983, lee a Sherlock Holmes como abducción peirceana; y Ginzburg, "Clues", funda el
"paradigma indiciario": leer el detalle marginal como firma). La estructura es la nuestra:
verdad oculta + comprar evidencia con costo + entregar la explicación + que la realidad corrija.
**Ciencia, detective, diagnóstico médico y debugging = el mismo juego con cuatro disfraces.**

**El failure mode del "nombre visto y no conectado"** (el caso que trajo Lucas) ya está en
nuestro mapa con mecanismo medido: recuperación relacional fallida (Gentner: la memoria
recupera por superficie, 70/30) + codificación bajo el marco equivocado (Klahr & Dunbar: lo
anotado bajo otro frame se etiqueta con los atributos que ese frame considera relevantes y se
vuelve invisible después) + asimilación oportunista que no disparó (Seifert: los problemas
pendientes se resuelven cuando un encuentro posterior los reactiva — acá no reactivó).

**La CUARTA tradición (la que no habíamos tocado): las profesiones de investigar** — gente cuyo
trabajo es descubrir y que documentó métodos Y fallas con casos reales:
- **Inteligencia**: Heuer, *Psychology of Intelligence Analysis* (CIA 1999) `[LEÍDO
  completo 2026-08-08, 216 pp.]` — nuestra tríada de hallazgos (una-hipótesis-confirmada /
  menú truncado / anomalía descartada como "outlier") YA estaba descompuesta como las tres
  patas del *satisficing*; su **diagnosticity** (la evidencia consistente-con-todo vale
  cero) nos da una métrica cero-LLM del gasto experimental; y el nulo empírico de ACH
  (Dhami 2019: 50 analistas reales, no mejoró) es nuestro "teatro de nivel4b" en humanos —
  nuestros mundos son el banco de pruebas que esa literatura declara faltante.
- **Medicina**: la literatura de **error diagnóstico** (Graber 2005; Croskerry 2003)
  `[LEÍDOS completos 2026-08-08]` — 100 casos reales con 33 muertes: la falla dominante NO
  es conocimiento (~3%) ni datos (~14%) sino SÍNTESIS (~82%), con el **cierre prematuro
  como falla #1**; lo fuera-de-menú se clasifica como no-fault (la medicina no culpa el
  polo creativo — el hueco que nosotros medimos); y el careo de mixes
  agente-vs-internista queda como experimento barato y publicable.
- **Derecho**: **visión de túnel** en condenas erróneas (Findley & Scott 2006) `[LEÍDO
  completo 2026-08-08, 107 pp.]` — la forma canónica de nuestro hallazgo estrella en
  profesionales: la contra-evidencia se examina INTENSAMENTE y se "redefine en una
  categoría menos dañina" (= "outlier"); la firma del epiciclo (la corrida de 57 minutos
  con mellizos); el autor real "ya descartado" a un paso; y contramedidas con evidencia
  (la conciencia NO funciona; los ciegos SÍ — valida nuestro anti-leak; la reforma PEACE
  desarmó el túnel sin perder rendimiento).
- **Insight de campo**: Klein, *Seeing What Others Don't* `[POR-LEER — libro]` — ~120 casos
  reales de insight (bomberos, militares, detectives) con SU lista de disparadores
  (conexiones, coincidencias, contradicciones, desesperación creativa).

**¿Es todo "el razonamiento"? No — y el recorte importa.** Hay un núcleo común real:
*investigar bajo incertidumbre* = el lazo de dos espacios (hipótesis × evidencia; Klahr &
Dunbar) con la abducción generando candidatos. Ese núcleo es el mismo bajo todos los
disfraces — por eso nuestros saltos (movidas en el espacio de hipótesis) y nuestros vicios
(fallas del lazo) DEBERÍAN transferir entre disfraces, **y eso es testeable con nuestra
máquina** (mismo operador, disfraz detective vs disfraz fábrica → ¿mismas firmas?). Pero
"razonamiento" a secas incluye más (deducir, planificar, calcular): lo nuestro es una tajada
específica y honda — **el razonamiento explicativo sobre sistemas con estructura oculta**.

## Recursos para leer más (la biblioteca del programa)

**El estado de cada uno**: `[LEÍDO]` = leído a texto completo por nosotros, con extracción en
[lectura-de-fuentes](lectura-de-fuentes.md) · `[EN LECTURA]` = lectores corriendo ahora ·
sin marca = puntero curado, pendiente de fichar (no se cita en el paper hasta leerlo).

### El marco (qué es un salto, abducción)
- **Peirce — abducción**: la entrada "Abduction" de la *Stanford Encyclopedia of Philosophy*
  (gratis online) es el mejor arranque; Hanson, *Patterns of Discovery* (1958) es el clásico
  que la vuelve lógica del descubrimiento.
- **"Position: LLMs can't jump"** (OpenReview klU4737opt) `[LEÍDO 2026-07-10]` — el paper del
  programa: abducción como el salto E→axiomas; Vulcano vs relatividad; mundos interactivos
  como laboratorio.
- **The Einstein Test** ([arXiv 2501.06948](https://arxiv.org/abs/2501.06948)) `[LEÍDO 2026-08-07]` —
  position puro: re-descubrir breakthroughs desde el corpus PRE-descubrimiento, con brief
  ciego de historiadores y derecho a declarar "no hay respuesta"; inviable sin re-entrenar por
  descubrimiento → el hueco que llenamos con verdad sintética.
- **Can AI Follow in Einstein's Footsteps?** ([arXiv 2607.27794](https://arxiv.org/abs/2607.27794))
  `[LEÍDO 2026-08-07]` — "symmetry abduction" como el paso faltante; el cuello es la SELECCIÓN
  ("novelty is cheap"); endosa los mundos con leyes ocultas.

### Creatividad e insight (ciencia cognitiva)
- **Schmidhuber**, "Formal Theory of Creativity" (IEEE TAMD 2010) `[LEÍDO completo
  2026-08-07]` — la teoría matemática: creatividad = progreso de COMPRESIÓN; el
  descubrimiento no necesita anomalía (Newton comprime manzanas predecibles); su MDL de
  dos partes castiga al modelo que ajusta sin comprimir y cobra los bits del parche —
  respaldo formal directo de nuestra vara (puntuar, no entrenar).
  [Extracción](research/2026-08-07-lecturas-programa-saltos.md).
- **Boden, *The Creative Mind*** (2ª ed. 2004) — la distinción combinacional / exploratoria /
  **transformacional** (cambiar el espacio mismo: nuestros saltos).
- **Ohlsson** — teoría del cambio representacional; su operacionalización experimental
  (Knoblich, Ohlsson et al. 1999, JEP:LMC) `[LEÍDO completo 2026-08-07]`: el insight =
  resolver un IMPASSE relajando restricciones auto-impuestas o descomponiendo chunks; la
  dificultad ordena por el alcance de lo que hay que revisar (95/78/45%); **sin impasse no
  hay reestructuración** — la explicación teórica de nuestro 0/9 (la familia default nunca
  falla visiblemente) y la palanca de diseño #1: ingeniar el impasse desde el mundo. El
  libro de 2011 sigue [POR-LEER]. [Extracción](research/2026-08-07-lecturas-programa-saltos.md).
- **Klahr & Dunbar**, "Dual Space Search During Scientific Reasoning" (*Cognitive Science*
  1988) `[LEÍDO completo 2026-08-07]` — descubrir = buscar en dos espacios (hipótesis ×
  experimentos); el insight = instanciar un FRAME nuevo; y tres regalos: la evidencia
  comprada bajo el frame equivocado INHIBE el salto (nuestros agentes, dicho en 1988); la
  vía de escape es el modo SIN hipótesis (que los agentes nunca usan — siempre tienen un
  candidato); y no-generar-la-alternativa es causa documentada de no-revisar (nuestras dos
  líneas conectadas). [Extracción](research/2026-08-07-lecturas-programa-saltos.md).
- **Dunbar**, "How scientists really reason" (1995, los laboratorios in vivo)
  `[LEÍDO completo 2026-08-07, + el paper 1997]` — un año DENTRO de 4 labs de élite: las
  analogías que descubren son CERCANAS (2/99 lejanas, cero descubrimientos); el individuo
  solo atribuye la anomalía a error y espera que desaparezca (= nuestros agentes); el
  corrector es el GRUPO; la serendipia vive en los CONTROLES; y el cambio conceptual real
  del corpus fue partir-un-mecanismo-en-dos (nuestra operación 2). La lectura más
  importante para diseñar mundos fieles.
  [Extracción](research/2026-08-07-lecturas-programa-saltos.md).

### Filosofía e historia de la ciencia
- **Nersessian** — razonamiento basado en modelos (analogía, experimento mental, casos
  límite; Maxwell como caso). Su paper canónico 1992 `[LEÍDO completo 2026-08-07]`: el
  cambio conceptual es una CADENA de modelos intermedios — Maxwell construyó un híbrido
  falso-a-sabiendas (vórtices + ruedas locas) y de ahí extrajo estructura más general; el
  "aha" es soltar el andamio, no crear. Implicación dura: el binario salta/no-salta es el
  error de los endpoints — medir la cadena. El libro de 2008 sigue [POR-LEER].
  [Extracción](research/2026-08-07-lecturas-programa-saltos.md).
- **Darden, *Theory Change in Science*** (1991) — estrategias CONCRETAS de cambio de teoría en
  la genética temprana (agregar variable, dividir, alterar observación) — casi una taxonomía
  hermana de la nuestra.
- **Thagard, *Conceptual Revolutions*** (1992) — reclasificaciones (el árbol conceptual que se
  reordena).
- **Kuhn, *La estructura de las revoluciones científicas*** (1962) — el telón de fondo de todo.

### Analogía (el salto +1)
- **Gentner**, "Structure-Mapping: A Theoretical Framework for Analogy" (*Cognitive Science*
  1983) y su resumen autoritativo 2025 en la *Open Encyclopedia of Cognitive Science*
  `[LEÍDO 2026-08-07]` — analogía = mapear relaciones, no parecidos; criterios computables sin LLM (SME).
- **Hofstadter & Sander, *Surfaces and Essences*** (2013) — la analogía como motor de todo
  pensamiento, con cientos de casos.
- **Lewis & Mitchell** (tareas contrafactuales) `[fichado]` — dónde colapsa la analogía LLM.

### Historias puntuales por salto (fuentes lindas y accesibles)
- Reynolds: su paper de 1883 es legible; van Delft & Kes, "The discovery of superconductivity"
  (*Physics Today* 2010) cuenta la historia de Onnes CON el episodio del "cortocircuito".
- Wald: Mangel & Samaniego (*JASA* 1984) reconstruyen el memo real de los aviones.
- Pearson 1894 ("Contributions to the Mathematical Theory of Evolution") — la primera mezcla
  de dos poblaciones de la historia (los cangrejos).
- Hurst y el Nilo: Mandelbrot lo cuenta en *The (Mis)Behavior of Markets*.
- Señales tempranas de transiciones (la base de nuestro "el temblor avisa antes que el
  promedio"): Scheffer et al., "Early-warning signals for critical transitions" (*Nature*
  2009).

### Era LLM (lo empírico fichado nuestro)
- Chen, Zhao & Cohan ([2607.01233](https://arxiv.org/abs/2607.01233)) `[LEÍDO]` — el sesgo de
  operaciones (sobre-conectar, sub-desacoplar) medido a escala; nuestra receta de validación.
- DiscoverPhysics ([2605.26087](https://arxiv.org/abs/2605.26087)) `[LEÍDO]` — frontier falla
  justo donde hay estructura latente.
- NewtonBench / LLM-SRBench `[LEÍDOS 2026-08-06]` — el estado del arte en descubrimiento de
  ecuaciones; qué miden y qué no ([extracción](research/2026-08-06-lectura-newtonbench-llm-srbench.md)).
- KellyBench ([2604.27865](https://arxiv.org/abs/2604.27865)) `[LEÍDO 2026-08-07]` —
  no-estacionariedad natural + knowledge-action gap (diagnostican y no corrigen).

## El estado del tablero, en una mirada

| Salto | Historia ancla | ¿Mundo WAGER? | ¿Creatividad medida? |
|---|---|---|---|
| 1 entidad oculta | Neptuno / Vulcano | pendiente (latent_mix = pariente) | — (pariente: 0/10) |
| 2 grupos escondidos | Mendel; Pearson 1894 | ✅ count_mix | **0/9** |
| 3 régimen oculto | Reynolds; Onnes | ✅ count_regime v0 | NO aún (v0 midió aceptación) |
| 4 geometría | Kepler | no | — |
| 5 unificación | Newton; Maxwell | no | — |
| 6 invariante | Einstein 1905/07; Noether | no | — |
| 7 observador | Wald | no | — |
| 8 realimentación | Lotka-Volterra | no | — |
| 9 conservación/cuantos | Lavoisier; Planck | no | — |
| 10 memoria | Ewing; Hurst/Nilo | no | — |
| +1 transferencia | Darwin×Malthus | ✅ overgen (era anterior) | par medido en su era |
