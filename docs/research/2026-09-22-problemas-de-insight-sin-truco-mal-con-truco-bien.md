# El marco "sin el truco te va mal, con el truco soplado te va bien" ya tiene nombre: PROBLEMA DE INSIGHT. Qué aprendió la psicología en 90 años y qué miden hoy los benchmarks de LLM

> **Pregunta de Lucas (2026-09-22):** ¿hay casos, proyectos, ideas o teoría sobre este tipo de
> diseño — mundos donde sin un truco/insight te va mal, y sabiéndolo de antes te va bien, con un
> "aha" entre medio? **Respuesta corta: sí, es un paradigma entero.** En psicología cognitiva se
> llama *problema de insight* y nuestra ley de dos controles (ADRs 0175/0176/0177) es, casi
> palabra por palabra, su definición operativa. Este doc reúne lo que ya se sabe, para no
> redescubrirlo, y lo que nadie hizo todavía (nuestro hueco).
>
> **Nivel de verificación (ADR 0115):** nada de esto fue leído a texto completo en esta sesión.
> Marcado por fuente: **[A]** abstract oficial leído (arXiv/editorial); **[S]** resumen de búsqueda
> sobre la página del paper; **[M]** de memoria del modelo, sin verificar. Antes de citar algo de
> acá en un doc con autoridad, pasa por `docs/lectura-de-fuentes.md`.

## 1. Resumen en diez líneas

1. Un **problema de insight** es un problema que no se resuelve avanzando paso a paso desde la
   representación inicial: hay que **cambiar la representación** (relajar una restricción que uno
   se impuso solo, o descomponer un "bloque" que veía como indivisible). Weisberg (1995) [S] los
   clasifica en puros, híbridos y no-insight; Gilhooly & Murphy (2005) [S] mostraron con 60
   sujetos y 34 tareas que forman un grupo empíricamente separable.
2. **La prueba de la pista es su criterio clásico**: si contarle el truco cambia drásticamente el
   éxito, el problema era de insight. Nuestro control "con la idea nombrada" es exactamente eso.
3. **Pero la pista no siempre alcanza** (Weisberg & Alba 1981 [S], nueve puntos: decirles "podés
   salir del cuadrado" ayudó poco). Después del insight queda búsqueda. Esto es lo que vimos en
   Partículas (idea nombrada 1/3) y en P2 (la idea transfiere, la estimación falla).
4. Hay **dos teorías rivales de por qué uno se traba**, y son *nuestras* dos hipótesis: cambio de
   representación (Ohlsson; Knoblich et al. 1999 [S]) vs. **criterio de progreso satisfactorio**
   (MacGregor, Ormerod & Chronicle 2001 [S]): uno no busca alternativas hasta que *nota* que no
   está progresando. La segunda es nuestra "grieta".
5. Knoblich et al. (1999) [S] construyeron una **escalera graduada de dificultad dentro de un solo
   tipo de insight** (aritmética con fósforos): la dificultad se predice del *alcance* de la
   restricción a relajar. Es el modelo para las "primitivas" que pide Lucas.
6. Los **micromundos de descubrimiento** de los 80-90 (Klahr & Dunbar 1988 [S]; Dunbar 1993 [S];
   Mynatt et al. 1977 [S]) ya tenían nuestra estructura: verdad escondida, experimentos que cuestan,
   una hipótesis default que falla. Dunbar 1993: **solo los sujetos que se pusieron como META
   explicar el dato discrepante descubrieron la inhibición.** Es la grieta, medida en humanos en
   1993.
7. La camada LLM (2023-2026) tiene vecinos cercanos: NewtonBench [A], Gravity-Bench [S],
   BoxingGym [S] (ley escondida + experimentación interactiva + variantes contrafácticas), y
   pruebas de insight puro: NazoNazo [A], BRAINTEASER [S], MacGyver [S], Wason 2-4-6 en LLMs [A].
8. Dos hallazgos de esa camada son **nuestros eslabones medidos aislados**: NazoNazo encontró
   "fallo de verificación" (el modelo genera el candidato correcto y no lo endosa; 5-39% de los
   errores) = nuestro caso 05; "Failing to Falsify" encontró sesgo de confirmación en 11 LLMs y que
   *pedirles contraejemplos* sube el descubrimiento de 42% a 56% = nuestro "contraste" y el
   experimento del revisor ("duda servida").
9. Cautela heredada: la palabra "aha"/"wait" en una traza **no es evidencia** de reestructuración —
   los análisis de R1-Zero muestran que esas palabras ya están en el modelo base (época 0) y no
   correlacionan con acierto [S]. Nuestra rúbrica nunca puntúa la palabra; bien.
10. **Nadie combina** las cuatro cosas que nosotros sí: headroom certificado contra el mejor rival
    sin truco *optimizado*, la idea nombrada como *compuerta de diseño*, el proceso puntuado por
    artefactos mecánicos (no por respuesta final ni por juez-LLM), y gemelos.

## 2. La estructura tiene nombre y criterio

**Definición operativa (Weisberg 1995 [S]; Ohlsson [M]).** Un problema es de insight si (i) la
representación inicial no contiene la solución en su espacio de búsqueda, (ii) hace falta un cambio
de representación, y (iii) ese cambio se puede *inducir* con una pista. La taxonomía de Weisberg
distingue **puros** (la reestructuración es la solución: nueve puntos), **híbridos** (después de la
reestructuración queda búsqueda no trivial) y **no-insight** (solo búsqueda). Gilhooly & Murphy
(2005) [S]: 24 tareas "de insight" y 10 "no-insight" a 60 sujetos; el análisis de clusters las
separó, y las de insight se asociaron a flexibilidad ideacional.

**Traducción a la casa.** Nuestra ley de dos controles es esa definición hecha compuerta:

| Psicología | WAGER |
|---|---|
| sin cambio de representación no se resuelve | el mejor rival sin salto, optimizado, saca mala nota (ADR 0175) |
| la pista induce el cambio | el agente con la idea nombrada resuelve (ADRs 0176/0177) |
| puro vs. híbrido | cuánto trabajo queda *después* del salto: nuestro eslabón "realización" |

Lo que la psicología no tenía y nosotros sí: un puntaje mecánico continuo y gemelos. Lo que
tenían y nos falta: 90 años de casos calibrados en humanos.

## 3. Los casos clásicos (la mina)

| Caso | El truco | Sin truco | Con pista | Lo que enseñó |
|---|---|---|---|---|
| **Nueve puntos** (Maier 1930 [M]; Weisberg & Alba 1981 [S]) | las líneas pueden salir del cuadrado | ~0% | **poca mejora** | la pista no basta: después del insight sigue habiendo búsqueda (Kershaw & Ohlsson 2004 "múltiples causas de dificultad" [S]) |
| **Dos cuerdas** (Maier 1931 [M]) | usar la pinza como péndulo | pocos | rozar la cuerda "sin querer" ayudó a muchos, que no reportaron haber visto la pista | la pista puede ser **implícita** y actuar sin conciencia |
| **Vela** (Duncker 1945 [M]) | la caja es una repisa, no un envase | pocos | presentar la caja vacía sube mucho el éxito | *fijeza funcional*: el objeto viene con un rol pegado |
| **Tablero mutilado** (Kaplan & Simon 1990 [S]) | paridad de colores: cada dominó cubre uno de cada color | casi nadie | manipular la **saliencia de la clave** (cómo se muestra el tablero), pistas explícitas y heurísticas ("buscá invariantes") | el rendimiento se predice de los generadores y restricciones disponibles para buscar *la representación*, no la solución |
| **Aritmética con fósforos** (Knoblich, Ohlsson, Haider & Rhenius 1999 [S]) | relajar una restricción sobre qué se puede mover (un valor / un operador / la forma de la ecuación) o descomponer un "bloque" perceptual | la dificultad crece con el **alcance** de la restricción | (la escalera está en el diseño) | **dificultad predicha por teoría y verificada** en 4 experimentos: primer modelo graduado de un tipo de insight |
| **BigTrak, tecla RPT** (Klahr & Dunbar 1988 [S]) | la tecla "repeat N" no hace lo que uno supone | la hipótesis default falla | — | **búsqueda en dos espacios**: hipótesis y experimentos; "teóricos" vs. "experimentadores" (los que no generan hipótesis inducen desde datos) |
| **Genética simulada / inhibición** (Dunbar 1993 [S]; Schunn & Dunbar 1996 [S]) | los genes pueden *inhibir*, no solo activar (Jacob-Monod) | casi todos arrancan con activación y se quedan | **haber resuelto un problema con inhibición el día anterior** (otro dominio) → más descubren, más temprano, sin notar la analogía | (a) solo los que se ponen como **meta explicar la discrepancia** descubren; (b) la pista funciona como **priming**, sin conciencia |
| **Wason 2-4-6** (Wason 1960 [M]; revisiones [S]) | la regla es más general que tu hipótesis ("ascendente" vs. "múltiplos de 2") | la mayoría confirma y falla | pedir "pensar en opuestos" / dos reglas (DAX/MED) mejora mucho | **sesgo de confirmación**: eligen tests que no pueden refutar |
| **Universo artificial** (Mynatt, Doherty & Tweney 1977 [S]) | leyes de movimiento en un mundo simulado | — | — | los sujetos **no eligen entornos que permitan probar alternativas** |

## 4. Cinco lecciones que ya están aprendidas (y nos aplican una por una)

**L1 — La pista es necesaria, no suficiente.** Nueve puntos: contar el truco ayudó poco. Weisberg
llama "híbridos" a los problemas donde después del insight hay trabajo. → Nuestro control con la
idea nombrada tiene que declarar cuánto queda después (Partículas: 1/3 con la idea; las dos caídas
fueron *después* del salto). No es un fallo del control: es la distinción puro/híbrido.

**L2 — Dos razones distintas para trabarse.** (a) *Cambio de representación* (Ohlsson; Knoblich):
la restricción o el bloque no te dejan ver la salida; (b) *Criterio de progreso satisfactorio*
(MacGregor, Ormerod & Chronicle 2001): uno sube la colina con heurísticas de maximizar progreso y
**no busca alternativas hasta que un criterio de progreso se viola**; el paso crucial es
*abandonar* la escalada. Jones (2003) [S] probó ambas y las dos aportan. → (b) es nuestra
"grieta" y nuestra hipótesis anti-romántica; (a) es nuestro eslabón de generación. Que la
psicología no haya podido decidir entre ambas con problemas de papel es, justamente, lo que
nuestros mundos con presupuesto y feedback pueden separar.

**L3 — Se puede graduar la dificultad por teoría.** Knoblich et al.: el *alcance* de la restricción
a relajar (un valor < un operador < la forma entera) y la *cohesión* del bloque a descomponer
predicen la dificultad antes de correr. → Es el molde para las **primitivas**: cada restricción
que hay que relajar es una primitiva aislable; un mundo chiquito por restricción, con dificultad
predicha *antes* y verificada después. Lo mismo que hacemos con headroom, pero para el eslabón de
generación.

**L4 — La grieta y el contraste ya se midieron en humanos.** Dunbar 1993: la variable que separó a
los que descubrieron la inhibición fue **ponerse como meta explicar el dato que no encajaba**.
Klahr & Dunbar 1988: los que no generan hipótesis buscan en el espacio de experimentos y aun así
inducen. Wason/Mynatt: la gente compra tests que confirman. → Nuestros 0/10 de grieta y 0/10 de
contraste con poder no son rarezas de LLM: son los dos fallos humanos mejor documentados del
descubrimiento. Eso legitima medirlos por eslabón y sugiere las intervenciones (abajo).

**L5 — La pista puede ser implícita.** Maier (rozar la cuerda), Schunn & Dunbar (haber resuelto
inhibición ayer, sin notar la analogía), Kaplan & Simon (saliencia de la clave). → Nuestra escalera
de pistas (P1 copia / P2 idea / P3 dirección) tiene un peldaño más abajo que no usamos: **priming**
— exponer al agente al concepto en otro dominio, antes, sin decirle nada. Es el control más limpio
de "¿estaba en su repertorio?" y no contamina el brief.

## 5. La camada LLM (2023-2026): vecinos y qué encontraron

| Trabajo | Qué es | Hallazgo que nos toca |
|---|---|---|
| **Reasoning or Reciting** (Wu et al., NAACL 2024) [S] | 11 tareas en variante *default* y *contrafáctica* (mismo razonamiento, supuestos cambiados) | rendimiento "nontrivial" en las contrafácticas pero **cae sustancial y consistentemente** vs. default → el "truco" como salida del default tiene costo medible |
| **BRAINTEASER** (SemEval-2024 T9) [S] | acertijos de pensamiento lateral, opción múltiple | tarea que "desafía el sentido común"; 182 equipos |
| **MacGyver** (Tian et al., NAACL 2024) [S] | 1.600 problemas cotidianos que exigen uso no convencional de objetos | divergente + convergente; mejora con reflexión paso a paso y pensamiento divergente-convergente |
| **NazoNazo** (2025, arXiv 2509.14704) [A] | acertijos infantiles japoneses = "reestructuración representacional tipo insight + evaluación metacognitiva"; renovable, anti-contaminación | humanos 52.9% (n=126); 38 LLMs: no-razonadores 7.6%, razonadores 17.6%; **"fallo de verificación": generan el candidato correcto y no lo endosan (5-39% de los errores)** |
| **Failing to Falsify** (2026, arXiv 2604.02485) [A] | Wason 2-4-6 interactivo en 11 LLMs | sesgo de confirmación (proponen triples para confirmar); **intervención "considerá contraejemplos" sube el descubrimiento de 42% → 56%**; destilarla generaliza al test del Blicket |
| **FALSIFYBENCH** (2026) [S] | juegos de descubrimiento de reglas | el sesgo de confirmación es predictor negativo fuerte del éxito |
| **NewtonBench** (ICLR 2026, arXiv 2510.07172) [A] | 324 tareas, 12 dominios de física, **leyes contrafácticas** (alteraciones sistemáticas de leyes canónicas) descubiertas por experimentación interactiva | capacidad "clara pero frágil": cae con la complejidad y con el ruido; **dar un intérprete de código EMPEORA a los modelos más capaces: "premature shift from exploration to exploitation, causing them to satisfice on suboptimal solutions"** |
| **Gravity-Bench-v1** (ICML 2025) [S] | descubrir física gravitatoria en simulación, con presupuesto y casos fuera de distribución | difícil para agentes base; soluciones de referencia humanas |
| **BoxingGym** (2025) [S] | 10 entornos de diseño experimental + descubrimiento de modelos, métrica de información esperada | GPT-4o "struggles" en ambos |
| **No Evidence for LLMs in Problem Reframing** (2025, arXiv 2503.01631) [A] | 280 diseñadores, tres formas de usar LLMs para *reencuadrar* un problema | **ninguna mejora**; amplía la brecha experto/novato |
| **"Aha moment" de R1-Zero** (Sea AI Lab; arXiv 2503.20783) [S] | análisis del "momento aha" del entrenamiento RL | las palabras de auto-reflexión ya están en el modelo base (época 0) y **no se asocian a mayor acierto** |

**Lectura transversal.** Tres de estos miden *un eslabón nuestro aislado* y encuentran lo mismo que
nosotros: NazoNazo → selección/endoso (nuestro caso 05); Failing to Falsify → contraste con poder
(nuestros 0/10) *y* que servir la duda lo mejora; NewtonBench → compromiso prematuro / vara floja
(y una perilla que no habíamos considerado: **más herramienta puede empeorar**). Eso valida que el
análisis por eslabón es informativo y que las intervenciones del experimento del revisor tienen
precedente.

## 6. Nuestro hueco (lo que nadie hizo)

- **Headroom certificado** contra el mejor rival sin truco *optimizado* (ADR 0175). NewtonBench y
  Gravity-Bench puntúan la ley recuperada; ninguno reporta cuánto saca "la mejor ley equivocada".
- **La idea nombrada como compuerta de diseño**, no como ablación de prompt: si con la idea no se
  resuelve, el mundo se cambia antes de culpar al agente.
- **Proceso puntuado por artefactos mecánicos** (modelo de trabajo por celda, qué test compró, qué
  predijo antes de ver) y no por respuesta final ni por juez-LLM. NazoNazo y NewtonBench leen
  "thought-logs" a mano o con LLM.
- **Gemelos** (misma rutina byte a byte, distinta verdad) para atribuir.
- **La escalera de Knoblich para agentes**: nadie construyó problemas de insight para LLM con
  dificultad *predicha por el alcance de la restricción*. Es barato y es exactamente "primitivas".

## 7. Implicaciones para nosotros (ideas; NO decisiones)

1. **Adoptar la palabra**: nuestros mundos son *problemas de insight híbridos con presupuesto*. Nos
   deja heredar criterio, casos y críticas ya hechas (Weisberg & Alba: la pista no basta; CSP: no
   se busca hasta notar).
2. **Declarar el residuo post-insight** en cada certificado: cuánto trabajo queda después del truco
   (puro vs. híbrido). Partículas es híbrido; su 1/3 con la idea nombrada se lee distinto.
3. **Primitivas = restricciones aislables (Knoblich).** Candidatas con paradigma humano detrás:
   (i) *notar la discrepancia* (CSP; Dunbar 1993), (ii) *relajar una restricción de valor / de
   operador / de forma* (Knoblich), (iii) *descomponer un bloque* (Knoblich), (iv) *elegir el test
   que puede refutar* (Wason; Mynatt), (v) *endosar el candidato correcto* (NazoNazo: verificación),
   (vi) *transferir por priming* (Schunn & Dunbar). Cada una cabe en un mundo de centavos con los
   dos controles.
4. **El experimento del revisor tiene precedente directo**: "considerá contraejemplos" 42→56% en
   LLMs; "meta: explicá la discrepancia" en humanos. Diseñar "duda servida" con ese wording de
   referencia (sin pistas de contenido).
5. **Peldaño nuevo en la escalera de pistas: priming** (exposición previa en otro dominio). Mide
   repertorio sin contaminar el brief.
6. **Perilla nueva: herramientas.** NewtonBench: el intérprete de código induce explotación
   prematura. Nosotros damos código siempre; vale una celda sin código o con código restringido.
7. **Nunca puntuar la palabra "aha"** (lección R1). Ya es así en la rúbrica; que quede escrito.

## 8. Qué NO se verificó

- Ninguna fuente a texto completo (ADR 0115 exige registro en `docs/lectura-de-fuentes.md` antes
  de citarlas con autoridad). Abstracts oficiales leídos: 2604.02485, 2509.14704, 2503.01631,
  2510.07172. El resto, resúmenes de búsqueda sobre la página del paper.
- De memoria, sin verificar: Maier 1930/1931, Duncker 1945, Wason 1960 original, los detalles de
  la teoría de Ohlsson, y el detalle "bread/butter" de Kaplan & Simon (por eso no figura).
- Un paper sobre pistas y el "efecto aha-precisión" (escholarship qt638489j1) no se pudo leer (PDF
  ilegible); queda en la cola.

## Fuentes

Psicología: [Weisberg & Alba 1981](https://www.semanticscholar.org/paper/1c8a1d24a03db57fa80c6bae9cdfb9b0a3324d43) · [Kershaw & Ohlsson 2004](https://www.researchgate.net/publication/8909474_Multiple_Causes_of_Difficulty_in_Insight_The_Case_of_the_Nine-Dot_Problem) · [Knoblich et al. 1999](https://www.kognition.uni-koeln.de/literature/Knoblich_etal_1999.pdf) · [Kaplan & Simon 1990](https://www.sciencedirect.com/science/article/abs/pii/001002859090008R) · [MacGregor, Ormerod & Chronicle 2001](https://www.researchgate.net/publication/12127302_Information_Processing_and_Insight_A_Process_Model_of_Performance_on_the_Nine-Dot_and_Related_Problems) · [Jones 2003, dos teorías](https://www.researchgate.net/publication/5756000_Testing_Two_Cognitive_Theories_of_Insight) · [Weisberg 1995](https://www.semanticscholar.org/paper/c9f4da578db7877e72e4efdb12476c1bba08b2c7) · [Gilhooly & Murphy 2005](https://www.tandfonline.com/doi/abs/10.1080/13546780442000187) · [Klahr & Dunbar 1988](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1201_1) · [Dunbar 1993](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1703_3) · [Schunn & Dunbar 1996](https://link.springer.com/article/10.3758/BF03213292) · [Mynatt, Doherty & Tweney 1977](https://journals.sagepub.com/doi/abs/10.1080/00335557743000053)

LLM: [Wu et al. 2024](https://aclanthology.org/2024.naacl-long.102/) · [BRAINTEASER](https://arxiv.org/pdf/2404.16068) · [MacGyver](https://aclanthology.org/2024.naacl-long.297/) · [NazoNazo](https://arxiv.org/abs/2509.14704) · [Failing to Falsify](https://arxiv.org/abs/2604.02485) · [FALSIFYBENCH](https://arxiv.org/pdf/2606.04751) · [NewtonBench](https://arxiv.org/abs/2510.07172) · [Gravity-Bench-v1](https://arxiv.org/abs/2501.18411) · [BoxingGym](https://arxiv.org/abs/2501.01540) · [Problem reframing](https://arxiv.org/abs/2503.01631) · [Understanding R1-Zero-Like Training](https://arxiv.org/pdf/2503.20783) · [Sea AI Lab: There may not be aha moment](https://sail.sea.com/blog/articles/62)
