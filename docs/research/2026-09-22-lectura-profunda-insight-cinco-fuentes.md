# Lectura profunda (texto completo): lo que dicen DE VERDAD las fuentes del marco "sin el truco mal / con el truco soplado bien"

> **Pedido de Lucas (2026-09-22):** "profundizá y leé bien los materiales prometedores; no te quedes
> solo con abstracts, pero tampoco leas todos". Se eligieron cinco (más NewtonBench de paso) y se
> leyeron **página por página desde el PDF** (no vía resumen). Este doc corrige y completa
> [el doc de la mañana](2026-09-22-problemas-de-insight-sin-truco-mal-con-truco-bien.md), que era
> de abstracts. Notas crudas con cifras: `scratch/` de la sesión (`NOTAS-LECTURA.md`, no versionado).
> Registro formal por fuente en [`docs/lectura-de-fuentes.md`](../lectura-de-fuentes.md).

## 0. Qué se leyó, cuánto, y qué había ya en la casa

| Fuente | Páginas leídas hoy | Estado previo en la casa |
|---|---|---|
| Kaplan & Simon 1990, *In search of insight* (Cog. Psych. 22:374-419) | 374-395 de 419 (abstract, teoría, el experimento BREAD & BUTTER completo con tablas 1-4, protocolos, SWITCH) | **no estaba registrado** |
| Klahr & Dunbar 1988, *Dual space search* (Cog. Sci. 12:1-48) | 18-42 de 48 (espacios, teóricos/experimentadores, Estudio 2, modelo SDDS, sesgo de confirmación) | ya LEÍDO 48/48 el 2026-08-07 por la otra sesión — **confirmado** |
| Knoblich, Ohlsson, Haider & Rhenius 1999 (JEP:LMC 25:1534-1555) | 1534-1539 y 1549-1555 de 22 (teoría, tipos A-D, Exp. 1A, Exp. 3, discusión general) | ya LEÍDO 22/22 el 2026-08-07 — **confirmado** (el 95/78/45% de la casa = Fig. 2: 19/20, ~15.5/20, 9/20) |
| Jhaveri, GX-Chen, Sucholutsky & Choi 2026, *Failing to Falsify* (arXiv 2604.02485) | 1-10 de 10 (completo, sin apéndices) | figuraba `[ ]` sin leer → **LEÍDO** |
| NazoNazo (arXiv 2509.14704, versión zenodo) | 3-13 de 18 (resultados, tablas 1-2, discusión) + abstract | **no estaba registrado** |
| NewtonBench (ICLR 2026, arXiv 2510.07172) | 1-11 (cuerpo completo) | ya LEÍDO 2026-08-06 (extracción dirigida) — **confirmado** |

No leídos (siguen siendo resumen o abstract): Weisberg & Alba 1981, MacGregor/Ormerod/Chronicle
2001, Gilhooly & Murphy 2005, Dunbar 1993 (paywall Wiley), FALSIFYBENCH, BoxingGym completo.

## 1. Lo que CAMBIA respecto del doc de la mañana

1. **"La pista no alcanza" estaba mal calibrado.** Kaplan & Simon muestran que la pista **sí
   funciona cuando nombra el invariante**: los 11/23 sujetos que necesitaron la pista PARITY
   mencionaron la paridad recién después de recibirla y llegaron a la prueba. Lo que falla es otra
   cosa, más fina: **notar ≠ usar**. "Twelve of the 23 subjects did, in fact, generate a Rough Proof
   almost immediately after their first mention of parity; but the remaining 11 subjects mentioned
   parity some time before generating a proof, with an average gap of about 12 min" — "parity
   competes with other cues in the search for a new representation". → Para nuestra rúbrica: la
   "grieta expresada" no es un eslabón único; hay *mencionar* y hay *perseguir*, y la brecha entre
   ambos es de minutos en humanos. (Coincide con una de las 8 ambigüedades ya coleccionadas.)
2. **"Contraste con poder" no es "test que parece refutatorio".** Klahr & Dunbar (§6.2.1): sus
   sujetos usaron casi siempre la *positive test strategy* ("si BigTrak hace esto, mi hipótesis es
   correcta") y **aun así ~60% de los experimentos dieron evidencia desconfirmatoria**, porque el
   espacio estaba lleno de hipótesis falsas (Klayman & Ha 1987). El poder de un test depende de la
   distribución de hipótesis vivas, no de su forma. → Nuestra vara del contraste debe medir
   *diagnosticidad relativa al espacio de hipótesis del mundo* (la del certificado), no "si el
   agente buscó confirmar".
3. **El "8/9 mencionaron mezcla eran MENÚS" tiene espejo humano con número.** Klahr & Dunbar,
   Estudio 2: cuando se obligó a los sujetos a **enumerar todas las formas posibles ANTES de
   experimentar**, 5/10 propusieron la regla correcta con cero experimentos, 10/10 la descubrieron,
   en 6.2 min y 5.7 experimentos (vs 19.4 min y 15.2 en el Estudio 1), y **empezaron a diseñar
   experimentos que discriminaban entre hipótesis** ("subjects in Study 1 rarely designed
   hypothesis-discriminating experiments, for they usually were dealing with only a single
   hypothesis at a time"). El menú no es el problema: el problema es tener UNA hipótesis. Con varias
   vivas, el contraste aparece solo.
4. **Knoblich y Klahr & Dunbar no eran novedad**: la otra sesión los leyó completos en agosto y la
   casa ya tenía "ingeniar el impasse desde el mundo" y "insight = instanciar un frame nuevo". Mi
   relectura los confirma con las páginas a la vista y agrega los números de abajo.

## 2. Fuente por fuente: qué hicieron, qué número, qué nos dice

### 2.1 Kaplan & Simon 1990 — la escalera de pistas y la saliencia, en 1990

**Qué es.** El tablero mutilado (8×8 sin dos esquinas opuestas; ¿se cubre con 31 dominós?).
Requiere cambiar de representación: de "cubrimientos" a **paridad** (cada dominó tapa un negro y un
blanco; faltan dos del mismo color → imposible). Un estudiante de posgrado dedicó **18 horas y 61
páginas** y no lo resolvió; un programa necesitó **758.148 colocaciones** para probarlo por
agotamiento. Abstract: *"performance on insight problems can be predicted from the availability of
generators and constraints in the search for such a representation... four potential sources of
search constraint: cue salience manipulations, prior knowledge, hints, and heuristics... noticing
invariants proved to be a particularly powerful means for focusing search."*

**El experimento BREAD & BUTTER** (23 estudiantes CMU, 4 condiciones de *saliencia* de la paridad,
sin cambiar el problema): BLANK (tablero liso) / COLOR (blanco-negro) / BLACK & PINK (las palabras
escritas en las casillas) / BREAD & BUTTER (las palabras "bread"/"butter"). Y una **escalera de
pistas** que se daba solo si se trababan: IMPOSSIBLE (~15 min: "es imposible, hace falta una
prueba") → INSIGHT (~15 min: "hay un truco, miralo distinto") → PARITY (~30 min: "mirá los
colores/palabras") → COUNT (~40 min: "contá cuántas hay de cada tipo").

| Condición | Tiempo a 1ª mención de paridad | Tiempo a prueba | Enfoques probados |
|---|---|---|---|
| BLANK | 1980 s | 2242 s | 9.14 |
| COLOR | 1265 s | 1375 s | 5.80 |
| BLACK & PINK | 905 s | 1378 s | 5.16 |
| BREAD & BUTTER | 342 s | 995 s | 4.00 |

(F(3,19)=11.09, p<.002 para la primera mención; F=4.08, p<.025 para la prueba.) El **77% del tiempo
se va antes de mencionar la paridad** y el **3%** en construir la prueba una vez atendida. 12/23 la
notaron solos; 11/23 necesitaron la pista PARITY.

**Qué nos dice.** (a) La escalera IMPOSSIBLE → INSIGHT → PARITY → COUNT es, casi literal, nuestra
escalera P3 dirección → P2 idea → P1 copia, con una regla de tiempo. (b) Hay un **peldaño que no
tenemos**: la *saliencia* — cambiar cómo se muestra el dato, no qué se dice. Bajó el tiempo de
notar de 1980 a 342 s **sin ninguna frase**. Es una pista que no viola "no le demos pistas" porque
no es texto: es diseño del mundo, declarable en el certificado. (c) El cuello no es "no notar" a
secas: 11 sujetos notaron y tardaron 12 minutos más en usarlo.

### 2.2 Klahr & Dunbar 1988 — dos espacios, teóricos vs experimentadores, y el efecto de enumerar

**Qué es.** BigTrak (robot programable); descubrir qué hace la tecla RPT N. Las hipótesis se
organizan en **marcos**: *N-role:counter* (repite N veces) vs *N-role:selector* (repite los últimos
N pasos una vez — la correcta). Cambiar de marco exige cambiar ≥3 atributos a la vez: eso es el
"cambio de representación". El **espacio de experimentos** es N–λ (N = argumento; λ = largo del
programa); solo la **Región III** (N<λ, ≥3 instrucciones) discrimina la regla correcta de todas las
comunes.

**Números del Estudio 1** (20 adultos): dado que el resultado *confirma* la hipótesis, la cambian
igual 21/84 veces (25%); dado que *desconfirma*, la **retienen 76/136 (56%)**. 28% de los 304
experimentos se corrieron sin hipótesis. **Teóricos** (7): cambian de marco buscando en memoria;
**Experimentadores** (13): lo inducen tras un experimento en Región III. Tiempo 11.4 vs 24.5 min;
experimentos 9.3 vs 18.4; sin hipótesis 0.8 vs 6.1. *Todos* los teóricos sabían programar; un solo
experimentador.

**Estudio 2** (10): enumerar hipótesis antes de tocar nada → 4.2 hipótesis promedio; 5/10 la regla
correcta sin experimentos; 10/10 descubren; 6.2 min; 5.7 experimentos; diseñan experimentos
discriminatorios.

**La frase que importa (§6.1):** *"None of our subjects started with the correct general frame.
However, once they were driven to it by earlier failed hypotheses and observation of results, they
were able to form the correct hypothesis... Insight is not merely the change of values in slots of
a pre-existing frame, rather it is the instantiation of a new frame."* Y Simon: *"new
representations, like new problems, do not spring from the brow of Zeus, but emerge by gradual—and
very slow—stages."*

**Qué nos dice.** (a) Nuestra "creatividad = cambiar de marco, no de parámetros" es su definición
literal. (b) Hay **dos rutas** al marco nuevo — memoria (teóricos) o inducción desde datos
(experimentadores) — y la segunda es más lenta pero *funciona*: nuestros agentes que "compran el
test pero no la estructura" no usan ninguna: no inducen del dato ni evocan de memoria. (c) El
"modo sin hipótesis" (experimentar para *ver qué pasa*) es una vía de escape legítima en el modelo
SDDS; nuestros agentes casi no la usan (ya lo tenía la casa). (d) La intervención "enumerá antes"
es **estructura sin contenido**: no sopla la idea y sin embargo cambia todo. Candidata directa para
el experimento del revisor.

### 2.3 Knoblich et al. 1999 — la dificultad se predice antes de correr

**Teoría.** Impasse → dos mecanismos: **relajar restricciones** (probabilidad inversa al *alcance*
de la restricción) y **descomponer chunks** (probabilidad inversa a la *cohesión* del chunk: loose
VII → V,I,I; tight V, X, I, "−"; intermedios "+", "="). "We do not claim that constraint relaxation
is deliberate or voluntary... expanding the set of options... is one of the mind's responses to
persistent failure."

**Aplicación.** Aritmética con fósforos (numerales romanos; mover UN fósforo; solución única). Tres
restricciones que el novato trae: **valor** (VI = VII + I → VII = VI + I; tipo A), **operador**
(I = II + II → I = III − II; tipo B), **tautología** (III = III + III → III = III = III; tipo C).
Tipo D = valor con chunks tight (XI = III + III → VI = III + III, deslizando la X a V). "Types A
through C form a ladder where the constraints become wider or the chunks tighter for each rung."

**Resultados.** Exp. 1A (20, 5 min por problema): a los 5 min A 19/20, B ~15/20, C 9/20 (≈95/78/45%);
el orden predicho se sostuvo en cada minuto y en los 4 experimentos ("the predicted order of task
difficulty was never violated"). Exp. 3: la exposición previa a la forma tautológica hizo el tipo C
trivial (mediana 175 s → 11 s) y **no tocó el tipo D** (61%/69%) → relajar restricciones y
descomponer chunks son fuentes *distintas* de dificultad. Transferencia mayor en los tipos difíciles.

**Qué nos dice.** Es el molde de las **primitivas**: (1) cada restricción implícita es una primitiva
aislable; (2) su dificultad se predice del *alcance* antes de medir; (3) la transferencia diferencial
es la firma de que se relajó *esa* restricción y no otra. Para agentes nadie lo hizo.

### 2.4 Failing to Falsify (2026) — nuestro "contraste" medido aislado, con intervención

**Qué es.** Wason 2-4-6 interactivo para LLMs: 45 turnos alternando *Guess* (enunciar la regla) y
*Test* (proponer un triple; feedback sí/no). 80 episodios de evaluación; reglas generadas por LLM
más una de origen humano por set. **Métrica de proceso I:C** = tests *incompatibles* con la
hipótesis vigente / tests *compatibles* — la compatibilidad se computa **ejecutando la regla como
función Python** (mecánico). El éxito lo juzga un LLM (validado a mano).

**Números.** Wason 1960 (humanos, 29): 6/29 aciertan al primer anuncio; 21/29 al final; I:C 1.79 en
los que aciertan primero vs 0.24. LLMs (Tabla 2, baseline): no-thinking 0.06 (Qwen3-8B) … 0.33
(Qwen3-32B), GPT-4o 0.11; thinking Qwen3-32B 0.41, QwQ 0.50, Gemini-2.5-Pro 0.73. **Correlación I:C ×
éxito**: thinking ρ=0.75 (p=0.0003), non-thinking ρ=0.54 (p=0.039). **Intervenciones** (prompts
humanos): *Think-in-Opposites* ("identificá una propiedad saliente del último test y construí el
opuesto") mejora el éxito en 11/11 escenarios; *Dual-Goal* (enunciar la regla DAX y su complemento
MED) en 8/11; promedio 42% → 56%; Qwen3-32B thinking 0.41 → 0.61. Destilar la conducta (SFT sobre
turnos Test) la internaliza (0.41 → 0.64*) y **transfiere al Blicket test** (0.57 → 0.77*). Hallazgo
incómodo: pasar de non-thinking a thinking mejora el éxito **sin subir I:C** ("these gains are not
driven by reduced confirmation bias").

**Qué nos dice.** (a) Es el eslabón "contraste con poder" medido solo, en 11 modelos, con intervención
y transferencia. (b) Sus dos prompts son **el wording de referencia** para "duda servida": no dicen
qué buscar, dicen *cómo* testear. (c) I:C es computable en nuestros mundos **si el agente enuncia su
modelo de trabajo por celda** — y nuestros 0/10 de Perfiles sin hipótesis específica son, en su
lenguaje, "I:C indefinido": no hay hipótesis contra la cual el test pueda ser incompatible. Eso es
lo mismo que los 6.08 experimentos-sin-hipótesis de los Experimentadores de Klahr & Dunbar.

### 2.5 NazoNazo (2025) — el eslabón "endosar" medido solo, mecánicamente

**Qué es.** 201 acertijos infantiles japoneses (reestructuración representacional + evaluación
metacognitiva), 38 LLMs zero-shot sin retrieval, subset de 120 con humanos (n=126: media 52.9%,
IC95 46.6-59.2; **dificultad por ítem gaussiana en humanos, puntajes individuales bimodales**).
LLMs: no-razonadores 7.6%, razonadores 17.6%; GPT-5 dentro del IC humano; la dificultad por ítem
para LLMs está apilada en 0.

**"Verification failure"** (Tabla 2: % de respuestas incorrectas donde una variante literal de la
respuesta correcta aparece en el thought-log antes de la línea final): DeepSeek-R1 30.6%, Claude
Opus 4 25.0%, Grok 4 39.3%, Gemini 2.5 Flash 5.2%. Es **cota inferior** (conteo literal). También
describen *false insight*: convergencia confiada a una reinterpretación incorrecta. Su argumento
contra "la traza es post-hoc": un log escrito para justificar la respuesta no tendría por qué
exhibir un candidato correcto que la contradice. Few-shot con demostraciones de razonamiento mejora
en 4/4 (significativo en 2; no en el más fuerte).

**Qué nos dice.** (a) Nuestro caso 05 (construyó k-means y lo descartó a ojo) tiene nombre y tasa:
25-39% de los errores en modelos fuertes. (b) Su detector es **mecánico** (búsqueda literal): para
nosotros el equivalente es "¿alguna celda ajustó un modelo de dos tipos?" sobre el working_model
por celda — un detector de cota inferior del eslabón *selección* sin leer prosa. (c) Los humanos son
bimodales y los LLMs están apilados en cero: la distribución, no el promedio, es la firma.

### 2.6 NewtonBench (ICLR 2026) — confirmación de lo que la casa ya tenía

Cuerpo completo leído: 324 tareas (108 leyes mutadas × 3 sistemas), 11 LLMs, ~USD 10k. GPT-5 75.9%
promedio, no-razonadores <10%; Complex-hard GPT-5 40.3%, resto <6%; ruido 1e-4 → −12-16%. **Código
ayuda a los <40% y perjudica a los ≥40%**: la "exploration rate" (tokens *What if / Alternatively*
vs *Confirm / Verify*) cae de golpe al primer uso de código en Gemini-2.5-flash; GPT-5-mini usa el
código 68.9% para ajustar funciones (GPT-4.1: 25.9%). Scoring simbólico por juez-LLM (98.3% acuerdo)
— **no cero-LLM**. Nada nuevo respecto de la entrada del 06-08; se confirma.

## 3. Tres cosas que quedan listas para usar (ideas, no decisiones)

**A. La escalera de pistas tiene un peldaño por debajo del texto: la saliencia** (Kaplan & Simon).
Manipular *cómo se presenta el dato* (qué columna se ve primero, qué se rotula, qué agrupación
sugiere la interfaz) sin decir nada. Redujo el tiempo de notar ×5.8 (1980 → 342 s). Para nosotros:
un brazo "saliencia" en el certificado de cada mundo — declarado, sin frase en el brief, compatible
con "no le demos pistas". Mide si el problema es *ver* la anomalía o *usarla*.

**B. El experimento del revisor tiene tres intervenciones con precedente y número:**
| Intervención | Precedente | Efecto medido | Qué eslabón consume / qué mide aguas abajo |
|---|---|---|---|
| "Enumerá todas las formas posibles antes de comprar" | Klahr & Dunbar Est. 2 | 5/10 aciertan sin experimentos; 10/10 descubren; experimentos 15.2 → 5.7; aparecen tests discriminatorios | consume *generación*; mide si aparece el *contraste* |
| "Construí el test opuesto al último" (Think-in-Opposites) | Failing to Falsify | 11/11 modelos mejoran; 42 → 56% | consume *contraste*; mide *selección/realización* |
| "Enunciá tu regla y su complemento" (Dual-Goal) | Failing to Falsify | 8/11 mejoran | consume *contraste* por otra vía |
Ninguna sopla contenido. Las tres son "estructura del proceso", no "idea del mundo".

**C. Dos detectores mecánicos de eslabón, tomados prestados:**
- **I:C por partida** (Failing to Falsify): ejecutar el modelo de trabajo enunciado contra cada
  test comprado y contar compatibles/incompatibles. Requiere que el agente *enuncie* el modelo por
  celda — y si no lo enuncia, "I:C indefinido" es en sí el dato (Perfiles: 0/10).
- **Fallo de verificación** (NazoNazo): ¿el candidato correcto apareció en código y no fue
  elegido? Cota inferior del eslabón *selección*, sin rúbrica.

## 4. Las primitivas, ahora con paradigma humano y número

| Primitiva | Paradigma humano | El número | Mundo de centavos (boceto) |
|---|---|---|---|
| Notar la discrepancia y *perseguirla* | Kaplan & Simon; Dunbar 1993 [S] | 77% del tiempo antes de mencionar; 12 min entre mencionar y usar | un dato que no cierra + un test barato que lo confirma; se mide si lo compra |
| Relajar una restricción de valor / operador / forma | Knoblich tipos A/B/C | 95 / 78 / 45% a 5 min | tres mundos gemelos donde el modelo bueno viola una restricción de alcance creciente |
| Descomponer un chunk | Knoblich tipo D | independiente de las restricciones (Exp. 3) | una variable que "viene pegada" y hay que partir |
| Enumerar hipótesis antes de comprar | Klahr & Dunbar Est. 2 | 5/10 sin experimentos; 15.2 → 5.7 experimentos | menú de tests + medir cuántas hipótesis enuncia antes del primer gasto |
| Elegir el test que puede refutar | Wason; Failing to Falsify | I:C ρ=0.75 con el éxito | dos historias dadas + cinco tests, uno discrimina |
| Endosar el candidato correcto | NazoNazo | 25-39% de los errores | el candidato correcto ya construido en el sandbox; ¿lo entrega? |

Cada fila tiene que pasar los dos controles (sin truco mal / con truco soplado bien) antes de existir.

## 5. Tensiones nuevas para la tabla anti-recencia

- **¿El test "confirmatorio" es malo?** Failing to Falsify: I:C alto correlaciona con éxito (ρ=0.75).
  Klahr & Dunbar: la estrategia positiva dio 60% de desconfirmaciones y fue *útil* (Klayman & Ha).
  Y en Failing to Falsify mismo, thinking mejora sin subir I:C. → Se lleva midiendo *diagnosticidad*
  respecto del espacio de hipótesis del certificado, no la forma del test.
- **¿Notar la anomalía es el cuello?** Dunbar 1993 / CSP: la meta de explicar la discrepancia es
  la palanca. Kaplan & Simon: 11/23 la notaron y tardaron 12 minutos más en usarla. → La rúbrica
  separa *mencionar* de *perseguir* (ya era ambigüedad #? de la re-anotación; ahora con precedente).

## 6. Qué NO se leyó (honesto)

Kaplan & Simon pp. 396-419 (detalle de SWITCH, heurísticas, discusión); Klahr & Dunbar pp. 1-17
(intro, método, Tabla 2 de hipótesis; la casa ya los tenía); Knoblich pp. 1540-1548 (Exp. 1B y 2 en
detalle; sus tablas 4-10); NazoNazo apéndices (SI 3-6: ejemplos de fallo de verificación y método
few-shot); Weisberg & Alba 1981; MacGregor et al. 2001; Gilhooly & Murphy 2005; Dunbar 1993
(paywall); FALSIFYBENCH; BoxingGym completo. Las citas a esos siguen en nivel resumen [S].
