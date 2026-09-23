# ¿Qué es "el salto"? Las definiciones canónicas de cada nombre, puestas lado a lado, y los supuestos nuestros que hay que examinar

> **Pedido de Lucas (2026-09-23):** "sigamos profundizando en QUÉ ES ese salto/innovación/descubrimiento;
> qué nombre le ponemos; y pensemos las suposiciones que hacemos nosotros, por ejemplo las definiciones;
> quizás haya que volver a buscar lo que dicen otros, aunque ya tenemos mucha teoría". Hallazgo de
> inventario: **la casa ya tiene leídos a texto completo casi todos los cánones** (Magnani 2001, Boden 2004,
> Ohlsson 2011, Aliseda 2006, Schurz 2008, Thagard, Klein, Darden, "LLMs can't jump"). Lo que NO había
> era ponerlos lado a lado como DEFINICIONES y decidir. Eso hace este doc. Fuentes marcadas: **[casa]** =
> leído completo y registrado en `docs/lectura-de-fuentes.md`; **[S]** = definición tomada hoy de
> búsqueda web (abstract/enciclopedia), no del texto completo. Ideas, no decisiones.

## 1. Cada nombre, su tradición, su definición textual, y qué pregunta responde

| Nombre | Tradición | Definición canónica | La pregunta que responde |
|---|---|---|---|
| **Abducción** | Peirce (lógica), 1903 | *"The surprising fact, C, is observed. But if A were true, C would be a matter of course. Hence, there is reason to suspect that A is true."* (CP 5.189) [S] | ¿Qué **tipo de inferencia** es? De un hecho sorprendente a la hipótesis que lo explicaría. No dice nada de súbito ni de nuevo. |
| **Abducción selectiva vs creativa** | Magnani 2001 [casa] | Selectiva: elegir la hipótesis dentro de un repertorio ya disponible (el diagnóstico médico). Creativa: generar una hipótesis que **no estaba** en el repertorio. La creatividad es **relativa al repertorio del agente** (p. 48); la creativa es "segunda línea": se activa cuando la localización dentro del repertorio fracasa (p. 132). Lo que WAGER mide es abducción **existencial** (postular una entidad/tipo nuevo; Thagard, p. 49), especie de la creativa — la misma en la que fallaban BACON y GLAUBER (p. 50). | ¿La explicación **ya estaba en tu caja** o la fabricaste? Es exactamente la pregunta "¿existe, o es todo memoria asociativa?" |
| **Jump / salto** | "Position: LLMs can't jump" [casa] | El "Salto" (J) de la experiencia sensible (E) a los axiomas (A): los LLMs dominan inducción y deducción pero son *"structurally incapable of the abductive 'jump' required for scientific invention"*. Es **abducción** con otro nombre; el ejemplo es Vulcano vs Relatividad: parchar con un parámetro vs reestructurar la teoría. | Mismo que abducción creativa, con énfasis en que el destino está **afuera del espacio** donde buscabas. |
| **Insight / aha** | Psicología Gestalt → Ohlsson 2011 [casa]; Knoblich 1999 [casa]; Kaplan & Simon 1990 [casa parcial] | Impasse (fallo persistente, detectado, del propio intento) → cambio de representación (relajar una restricción / descomponer un chunk) → solución rápida y sin vacilación. Kaplan & Simon: insight = descubrir la **representación** efectiva; se predice de los generadores y restricciones de esa búsqueda. | ¿Qué pasó **adentro** y con qué **forma temporal**? Atasco y reordenamiento. Es sobre el proceso y la experiencia, no sobre la verdad. |
| **Descubrimiento** | Kuhn 1962, *Science* [S]; Klahr & Dunbar 1988 [casa] | Kuhn: muchos descubrimientos *"are not the sort of event about which the questions 'Where?' and, more particularly, 'When?' can appropriately be asked"*; descubrir = darse cuenta de **que** algo es y de **qué** es, y eso se extiende en el tiempo (oxígeno: Priestley/Lavoisier). Klahr & Dunbar: insight = *"the instantiation of a new frame"*, y Simon: las representaciones nuevas *"emerge by gradual—and very slow—stages"*. | ¿Qué relación tiene con **el mundo**? Encontraste algo verdadero. Es un **resultado**, y no es un instante. |
| **Creatividad (definición estándar)** | Runco & Jaeger 2012 [S] | *"Creativity requires both originality and effectiveness."* Originalidad = novedad (personal o histórica); efectividad = valor, utilidad, ajuste. | ¿Es **nuevo Y sirve**? El paraguas más ancho. |
| **Creatividad (Boden)** | Boden 2004 [casa] | *"ideas or artifacts that are new, surprising and valuable"*. **P-creatividad** (nueva para vos) vs **H-creatividad** (nueva para la humanidad). Tres formas: **combinacional** (juntar familiares), **exploratoria** (buscar dentro del espacio conceptual), **transformacional** (cambiar las reglas del espacio). La casa ya anotó: nuestro corte refinar/saltar = su explorar/transformar, PERO medido contra el espacio **efectivo** del agente. | ¿Nuevo **para quién**, y de qué **tipo**? La transformacional es la que cambia la forma del espacio. |
| **Creatividad (Simonton)** | Simonton 2012 [S] | Tres criterios multiplicativos: c = (1−p)·u·(1−v): originalidad (improbabilidad p), utilidad u, sorpresa (1−v). Inspirado en los criterios de la oficina de patentes de EE.UU. | Igual que Boden pero **cuantificable** e independiente por eje. |
| **Innovación / invención** | Patentes; Schumpeter [M] | Una construcción nueva que satisface restricciones funcionales y se adopta. **No necesita verdad escondida** (Astra 23-09). | ¿**Sirve y lo adoptan**? |
| **Progreso de compresión** | Schmidhuber 2009 [S] | Los datos se vuelven interesantes *"exactly when it allows a sharp improvement in the compressor's predictive power"*; el aha = re-codificar de golpe los mismos datos de forma más simple; creatividad = generar datos que fuercen ese progreso. | Una definición **mecánica** del aha: caída súbita de la longitud de descripción. (Advertencia de "LLMs can't jump" [casa]: con loss≈0 la compresión prefiere parchar — Vulcano — a reestructurar.) |
| **Inteligencia (Chollet / ARC)** | Chollet 2019 [S] | *"skill-acquisition efficiency over a scope of tasks, with respect to priors, experience, and generalization difficulty"*. ARC mide eficiencia de adquisición ante novedad. | ¿Cuán rápido aprendés lo nuevo? **No** es una definición de insight ni de descubrimiento: ARC te dice si encontraste la regla, no cómo. |
| **Revisión de creencias** | Aliseda 2006 [casa] | Revisión = contracción + expansión (identidad de Levi); el operador p′ "hacer una distinción" = partir un átomo en dos = **agrandar el vocabulario**; su generador mecánico es cerrado por vocabulario → formaliza la **frontera** del salto, no el salto. | ¿Qué le pasa al **conjunto de creencias**? Y dónde termina lo mecanizable. |

## 2. Las capas encajadas (el mapa que le cerró a Lucas)

```
DESCUBRIR / INVENTAR  (resultado: algo nuevo que sirve — Runco & Jaeger; con o sin verdad escondida)
 └─ los que necesitaron CAMBIAR LA FORMA del modelo, no sus números
     (= abducción CREATIVA de Magnani = creatividad TRANSFORMACIONAL de Boden = "jump" del paper
      = cambio de representación de Ohlsson/Kaplan & Simon = agrandar el vocabulario de Aliseda)
      └─ los que se vivieron como un golpe súbito (el aha; Schmidhuber: compresión de golpe)
```

- La capa de afuera es demasiado ancha para nosotros (incluye ajustar un parámetro o descubrir que
  el sensor está sesgado — Astra tiene razón en que nuestra definición actual "deja afuera demasiada
  ciencia legítima" **si** pretendemos que "salto" = "descubrir").
- La capa de adentro (el aha vivido) no es medible en un LLM y no es necesaria para descubrir.
- **Lo nuestro es la capa del medio**, y tiene el mismo objeto con cinco nombres en cinco tradiciones.

## 3. Propuesta de nombre y definición (para discutir, no decidida)

**Nombre de la casa:** seguir diciendo **"salto"** en llano — es corto, ya está en toda la casa (ADR 0179),
y no arrastra la connotación de instante del "aha" ni la de mérito histórico de "descubrimiento".
**Nombre técnico (para el paper):** *abducción creativa* (Magnani) o *creatividad transformacional*
(Boden) — son intercambiables; la primera dice qué inferencia es, la segunda dice contra qué espacio.

**Definición operativa propuesta:**
> Un agente da un salto en un episodio cuando, a partir de evidencia que no cierra con su modelo,
> **construye una hipótesis que cambia la forma del modelo** (qué variables existen, cómo se
> conectan), **que no estaba en el repertorio efectivo que mostró en el episodio**, y **que después
> acierta donde las alternativas difieren** (fuera de muestra / bajo intervención).

Tres piezas, tres controles: (i) "cambia la forma" se certifica contra el mejor rival de la misma forma
(ADR 0175); (ii) "no estaba en el repertorio efectivo" se certifica con el test de contaminación / priming
y con el menú previo elicitado (Boden: espacio efectivo; Magnani: relativo al repertorio) — y solo se
puede afirmar **P-creatividad**, nunca H-; (iii) "acierta donde difieren" es el examen fuera de muestra
con gemelo negativo (Astra). Lo que NO exige la definición: que sea súbito, que se sienta como aha, que
haya una única verdad escondida, ni que el agente lo verbalice.

## 4. La pregunta "¿existe, o es todo memoria asociativa?" ya tiene nombre: selectiva vs creativa

Magnani la formuló hace 25 años: la abducción **selectiva** ES memoria (elegir de la caja); la
**creativa** es fabricar lo que no estaba. Y su punto del "caso de los patos" (p. 109) es el que nos
frena: *detectar la anomalía sin poder explicarla es el comportamiento ESPERADO de una máquina
selectiva* — para reclamar déficit creativo hay que mostrar que el agente TENÍA los ingredientes.
Traducido a experimento: la tesis "LLMs can't jump" = "todo salto de un LLM es selectivo". Se prueba
haciendo tareas donde la respuesta no se pueda recuperar sino construir (verdad aleatorizada
post-entrenamiento; variantes contrafácticas tipo Wu et al.), y separando dos tipos de pista: **"acordate
de algo parecido"** (activa memoria) vs **"mirá la estructura"** (fuerza construcción). Si solo la primera
ayuda, es memoria. Si la segunda ayuda sola, hay algo más que memoria.

## 5. Los supuestos nuestros que hay que examinar (con quién los cuestiona)

| # | Supuesto que veníamos haciendo | Quién lo cuestiona | Qué haríamos |
|---|---|---|---|
| 1 | "Forma vs números" es un corte limpio | Boden (depende del espacio efectivo del agente); Aliseda (la frontera es el vocabulario); una mezcla es "solo parámetros" en una familia suficientemente grande | Definir la forma **relativa a la familia declarada en el certificado**, y elicitar el menú previo del agente |
| 2 | El salto es un evento (tiene "cuándo") | Kuhn 1962; Simon ("gradual and very slow stages"); Klein: 44% graduales | Medir el flujo con registro temporal; el "instante" es dato, no supuesto |
| 3 | No lo expresó = no lo tuvo | ADR 0186 (nuestra propia prohibición); Astra; Codex | "Candidato no expresado" ≠ "no generado"; los artefactos de código cuentan (NazoNazo) |
| 4 | La pista aísla el salto | Astra (una pista reduce búsqueda, activa conocimiento, aclara el objetivo); Kaplan & Simon (la saliencia también ayuda) | Control activo de esfuerzo/atención; registrar qué se dio y qué hizo el agente igual |
| 5 | Descubrir necesita verdad escondida | Astra (inventar no); Boden (valor sin verdad) | Nuestro objeto es descubrir; inventar queda declarado como fuera del alcance por ahora |
| 6 | El insight existe en un LLM como algo distinto de recuperar | Magnani (selectiva vs creativa); R1: las palabras "aha" están en el modelo base | Sección 4: tareas no recuperables + dos tipos de pista |
| 7 | Hace falta una señal de error para que haya salto | "LLMs can't jump" (los saltos más duros ocurren con loss≈0: Vulcano); Ohlsson exige impasse; Klein: impasse solo en 25% | Declarar que nuestros mundos modelan el caso "hay señal"; el caso "loss≈0, reestructurá igual" es otro mundo, todavía no construido |
| 8 | Comprimir mejor = ser creativo | Schmidhuber a favor; "LLMs can't jump" en contra (la compresión parcha antes que reestructura si el horizonte es corto) | Si usamos MDL/BIC como vara, declarar el horizonte y el gemelo donde parchar es lo correcto |
| 9 | Podemos afirmar novedad | Boden P vs H; Astra: solo "relativa al episodio" | Nunca reclamar H-creatividad; el claim es P-creatividad certificada por contaminación |
| 10 | "Creatividad" es lo más cercano a lo nuestro | Sí como paraguas (estándar: nuevo + sirve), pero solo su forma **transformacional**; la combinacional y la exploratoria son "refinar" | Usar "creatividad" solo con el adjetivo |

## 6. Lo que sigue abierto

- ¿Cuál es la **unidad mínima** de "cambiar la forma"? Aliseda ya tiene un operador ("hacer una
  distinción": partir un átomo en dos). Knoblich tiene tres restricciones y dos tipos de chunk. Darden
  tiene 12 transformaciones. Nuestra taxonomía tiene 11. ¿Se reducen a pocas operaciones sobre el
  vocabulario del modelo? (candidata a "primitiva": *partir* / *juntar* / *agregar variable* / *borrar* /
  *cambiar la conexión*).
- ¿Se puede medir "relativo al repertorio" en un LLM sin acceso a los pesos? Solo relativo al episodio
  (Astra); el priming lo altera (Astra) — es intervención, no medición.
- Si el aha vivido no es medible, ¿qué observable mecánico lo reemplaza? Candidatos: caída súbita de
  longitud de descripción (Schmidhuber), o el momento en que el modelo de trabajo cambia de familia.

## Fuentes de hoy [S]
[Peirce CP 5.189 (SEP)](https://plato.stanford.edu/entries/abduction/peirce.html) · [Boden, resumen de definiciones](https://arxiv.org/pdf/2304.00008) · [Runco & Jaeger 2012](https://www.tandfonline.com/doi/abs/10.1080/10400419.2012.650092) · [Simonton 2012, tres criterios](https://www.tandfonline.com/doi/abs/10.1080/10400419.2012.676974) · [Kuhn 1962, Historical Structure of Scientific Discovery](http://www.compilerpress.ca/Competitiveness/Anno/Anno%20Kuhn%20History%20of%20Discovery.htm) · [Schmidhuber 2009](https://arxiv.org/abs/0812.4360) · [Chollet 2019](https://arxiv.org/abs/1911.01547)
