# WIKI — Las fallas de la indagación

**La indagación es un ciclo** (generar candidatos → deducir qué se vería → comprar evidencia →
actualizar → entregar) **y cada falla clásica es el ciclo rompiéndose en un paso específico.**
Lo que aprendimos midiendo agentes — y confirmamos en cuatro literaturas profesionales — es
que se puede tener casi todo el ciclo sano con UNA bisagra rota. Este wiki recorre el ciclo
paso por paso, con la falla de cada uno, nuestro espécimen medido, y lo que documentaron las
profesiones que investigan por oficio (espías, jueces, médicos).

**Salto y falla no son lo mismo.** El salto nombra la jugada que hacía falta —por ejemplo,
separar una población en dos grupos—; la falla dice **dónde se perdió** esa jugada. El
experimento se construye y valida primero para observar si el agente descubre y realiza el salto.
Después, las subpreguntas científicas y la autopsia localizan si no nació al generar candidatos,
fue descartado al actualizar o quedó afuera de la entrega. Por eso un resultado siempre debe
nombrar las dos cosas.

---

**Para profundizar**: [docs/vicios/](docs/vicios/README.md) (el catálogo canónico con
evidencia por vicio) · [índice de hallazgos](docs/research/README.md) (nuestros números) ·
[extracciones de lecturas](docs/research/2026-08-07-lecturas-programa-saltos.md) (las 17
fuentes) · [WIKI-INDAGACION](WIKI-INDAGACION.md) (el ciclo sano).

## ① Al generar candidatos — el menú que no crece (la falla madre)

**Qué es**: la explicación correcta exige un candidato que el repertorio no trae — y no nace.
El agente (o el humano) considera solo las hipótesis de siempre; si la respuesta no está en esa
lista, ninguna cantidad de datos la salva.

**Nuestro espécimen**: **0 de 9** agentes postuló los grupos escondidos en **Conteos por lote:
tipos discretos o variación continua** (alias técnico `count_mix`) — todos entregaron la
versión continua de siempre, que ajusta bien los promedios. Y el detalle
revelador: hasta cuando la evidencia discriminante estaba IMPRESA en su propia pantalla (el
histograma con dos jorobas), no la vieron — se mira a través de los resúmenes que el modelo
vigente considera relevantes.

El control más limpio nuevo es **Perfiles persistentes**. Allí separar la población mejora mucho
el modelo y, en las 400 filas exactas de cada una de diez partidas, la división en dos era
abrumadora. `gpt-5.4` vio las dependencias, pero **9/10** las licuó dentro de una sola campana;
**0/10** construyó espontáneamente la explicación compacta de dos tipos. Con la idea nombrada,
el mismo modelo sí la construyó 2/3. Un caso sin ayuda preservó la forma copiando perfiles
completos: éxito predictivo funcional, pero no compresión conceptual. Esto localiza la falla
principal entre **ver la dependencia** y **generar/probar la partición correcta**.

**Las profesiones**: la CIA lo llama “no generar el conjunto completo de hipótesis” y encontró
que las personas generan muy pocas alternativas; el menú además lo trunca el HÁBITO (cada
analista usa casi siempre una sola estrategia). La teoría del insight marca el **impasse** —un
fracaso persistente y visible— como un gatillo fuerte de reestructuración. Nuestro salto de
0/9 a 30/30 muestra que puede funcionar; no demuestra que sea el único motor. También puede
haber presión interna por coherencia o simplicidad, aun sin una predicción fallida.

**El corolario medido tres veces**: ORDENAR el procedimiento no lo arregla. Nosotros mandamos
"ajustá ≥2 familias y compará" → obedecieron y compararon… dentro del menú de siempre (0/3,
con tests de validación y todo: teatro metodológico). El método ACH de la CIA (la versión
formalizada de esa orden) dio **nulo** en el mejor test con 50 analistas reales. La medicina
enseña sesgos hace décadas con efecto flaco. La conciencia y la orden no funcionan; la
estructura sí (ver el final).

## ② Al comprar evidencia — comprar fiebre

**Qué es**: gastar el presupuesto en evidencia consistente-con-todas-las-hipótesis, que no
discrimina nada (la fiebre prueba que estás enfermo, no QUÉ tenés — el concepto de
*diagnosticity*). Firma acompañante documentada: la información extra **no mejora la precisión
pero sube la confianza** (probado con expertos: de 5 a 40 variables, precisión igual,
confianza por las nubes).

**Nuestro matiz**: en mundos simples los agentes COMPRAN BIEN (11/12 eligieron solos el
ensayo discriminante; en **Proceso con umbral: el fallo propio provoca el salto**, los que
saltaron hicieron zoom fino alrededor del
umbral). El cuello no es el shopping — es qué hacen con lo comprado. Pero la métrica queda:
fracción del gasto en evidencia-fiebre vs discriminante, computable sin jueces.

## ③ Al testear — la verificación de paja

**Qué es**: verificar con tests que la hipótesis rival TAMBIÉN pasa — esfuerzo real, poder de
refutación cero. Se *siente* riguroso; no refuta nada.

**Nuestro espécimen** (el mejor que tenemos): gpt con la receta correcta EN LA MANO la
descartó diciendo *"gamma es una alternativa continua más parsimoniosa a la mezcla finita"* —
sin haber ajustado la mezcla NI UNA VEZ; y defendió su modelo con un chequeo que la rival
también pasaba ("el parámetro se mantiene estable ≈ lo que predice gamma" — igualmente cierto
bajo la mezcla). Parsimonia invocada EN LUGAR del test, no después.

**Las profesiones**: es la regla de decisión de Heuer dada vuelta — *"la hipótesis más
probable suele ser la que tiene MENOS evidencia en contra, no la que tiene más a favor"*; la
evidencia "a favor" que también es consistente con las rivales vale cero, y casi toda la
evidencia que uno junta para su favorita es de esa clase.

## ④ Al actualizar — el descarte de la anomalía (el hallazgo estrella)

**Qué es**: ver el dato incómodo, examinarlo… y re-etiquetarlo para no actualizar. NO es
ignorar: es escrutinio activo al servicio del descarte.

**Nuestro espécimen**: el agente ve el punto anómalo, **compra más datos de ese punto para
verificarlo**, confirma que es real, escribe *"¿y si son dos tramos?"*… y entrega la curva de
siempre llamando **"outlier"** al punto que él mismo confirmó.

**Actualización de la planta química (2026-08-10):** los agentes sí hicieron solos la parte
“chequear antes de culpar al aparato”: 30/30 verificaron el instrumento. Donde apareció la
separación fue después, entre lo investigado y lo entregado. Eso no prueba todavía que supieran
que su modelo final estaba mal; la cautela completa está en ⑤.

**Las profesiones lo tienen fotografiado**: en condenas erróneas, la contra-evidencia se
examina con lupa y *"se redefine en una categoría menos dañina"* ("el testigo es pariente",
"el ticket no prueba nada") — y ante contra-evidencia fuerte aparece **el epiciclo**: la
historia auxiliar cada vez más ridícula antes que soltar (la fiscalía "probando" que el
acusado llegaba a tiempo con una reconstrucción a toda velocidad y mellizos de seis días a
bordo). En medicina es la falla #1 con cadáveres: **cierre prematuro** — de 100 casos reales
de error diagnóstico (33 muertes), el error casi nunca fue falta de conocimiento (~3%) ni de
estudios (~14%): fue de SÍNTESIS (~82%), encabezada por "dejar de considerar alternativas
tras el primer diagnóstico". Y la historia real de la ciencia lo tiene también: el equipo de
Onnes descartó la superconductividad como "cortocircuito del equipo".

**La conexión causal clave** (medida en laboratorio): **no poder generar la alternativa CAUSA
no soltar la actual** — nadie reemplaza algo con nada. Las fallas ① y ④ son una sola, vista de
dos lados. (Y el gate: si el investigador cree que la anomalía es ERROR, ningún desafío lo
mueve — por eso la réplica del dato raro tiene que ser comprable y barata.)

**La excusa que usa TODO el mundo: "es el aparato, no el mundo".** Es la salida más
documentada del corpus entero, y aparece en las cuatro tradiciones a la vez: el equipo de
Onnes descartó la superconductividad como *cortocircuito del equipo*; Darden pone "confirmar
que la anomalía existe (¿es problema de datos?)" como **paso 1 obligatorio** de todo cambio de
teoría; Dunbar midió el gate más duro que tenemos (*si el investigador cree que es error,
ningún desafío produce cambio conceptual*); y nuestros propios agentes la usan literalmente
("la muestra histórica era ruidosa", "quizás ese punto es un outlier"). **El descarte por
instrumento es legítimo** — lo ilegítimo es descartar sin replicar, o replicar, confirmar y
descartar igual. Los mundos anteriores no tenían un instrumento separable; la **planta química:
¿lotes distintos o sensor engañoso?** lo volvió jugable por primera vez. Allí 30/30 agentes
pagaron el chequeo correcto. Ese éxito del diagnóstico se conserva aunque el mundo no haya
quedado validado para medir el salto de grupos escondidos.

## ⑤ Al entregar — el saber no llega a la acción

**Qué es**: diagnosticar correctamente la propia falla… y no corregir nada. El saber no
gobierna la acción.

**Especímenes**: en un benchmark de temporada de apuestas, un modelo escribió TRES documentos
de autocrítica identificando la causa raíz de sus pérdidas — y no cambió una línea de su
modelo. Nuestro "outlier" es lo mismo en chico: el diagnóstico está escrito en su propia traza
y la entrega lo ignora.

**Observación de la planta química (2026-08-10; interpretación limitada)**: 30 de 30 agentes compraron
los chequeos correctos sin que nadie se los pidiera, sus propios datos mostraban clarísimo
"hay dos tipos de lotes" (verificado con matemática pura sobre lo que cada uno vio) — y 13 de
15 entregaron igual el modelo simple de un solo grupo, escondiendo los lotes malos en "más
ruido". Uno escribió "voy a agregar un componente de contaminación"… y entregó el simple.
Después vino el freno decisivo de Lucas: **¿estábamos seguros de que ese salto mejoraba mucho
desde adentro de la partida?** No. La mejor campana de un solo grupo ya obtenía **0.986/1.0**
y omitir los grupos no tenía una consecuencia visible. El hecho se conserva —investigaron y
entregaron el sustituto simple—, pero la lectura “sabían que estaba mal y no actuaron” **no está
demostrada**. Para separar “no lo supo”, “lo supo” y “actuó” necesitamos mundos donde la
diferencia sea material y una cadena observable entre evidencia, modelo y entrega.

**Convergencia externa, por otra vía:**
[*Why Do LLMs Struggle in Strategic Play?*](https://arxiv.org/abs/2605.00226) midió con
matemática pura que los modelos incorporan cada vez menos evidencia nueva a medida que avanzan
los turnos. Sus sondas internas también encontraron creencias mejores que las acciones que
producían. Se parece a nuestra separación evidencia→modelo→acción, pero entra como apoyo y
explicación rival, no como réplica exacta: ellos usan juegos repetidos y modelos abiertos;
nosotros, investigación de mundos ocultos y modelos ejecutables.

---

## Qué NO funciona y qué SÍ (evidencia convergente de 4 tradiciones)

**NO funciona:**
- **La conciencia del sesgo** — cuatro fuentes independientes (CIA, derecho, medicina, teoría
  del insight): saber que el sesgo existe no lo reduce; resiste la instrucción explícita.
- **Ordenar el método** — nuestra prueba de la "comparación mandada" (0/3), el nulo de ACH en analistas reales: el
  procedimiento impuesto se ejecuta sobre el mismo menú capturado.

**SÍ funciona (con evidencia):**
- **Trabajar a ciegas** — el perito de huellas que no conoce el contexto del detective
  REVIERTE sus propios errores previos (4 de 5 en el estudio clásico). Valida nuestra
  maquinaria anti-filtración.
- **El fresh look** — un revisor que NO parió la teoría, por escrito, ANTES del punto de
  compromiso (la inversión personal amplifica el sesgo).
- **Accountability** — saberse grabado/auditado cambia la conducta del interrogador; los
  agentes que saben que sus trazas se leen son la versión nuestra.
- **Fabricar el impasse** — para el salto: que el modelo de siempre falle de forma VISIBLE,
  persistente y barata de verificar (el análogo de "la ecuación sigue sin cerrar"). La
  reestructuración no obedece órdenes; responde al fracaso.
- **La reforma con outcome**: el modelo británico de interrogatorio (entrevistar para
  AVERIGUAR, no para confirmar) desarmó el túnel institucional **sin perder rendimiento** (las
  confesiones no bajaron).

**Ojo con "poner a otro a criticar": la evidencia va para los dos lados.** A favor: en los
laboratorios reales el corrector de la anomalía descartada es **la reunión de equipo**, no el
individuo. En contra: dos pares simétricos deliberando dan **99% de escalada de compromiso**
(vs casi cero decidiendo solos), y a un agente al que un revisor le pide más, **le sale
fabricar** — y encima le sube la nota. Lo único con evidencia a favor es un revisor que **no
sea dueño de la teoría** (el *fresh look*). Traducción de diseño: agregar "colegas" no es
automáticamente agregar corrección.

---

## Comentarios (el meta)

- **Este wiki es la entrada en llano.** El registro CANÓNICO de evidencia por vicio — con
  sub-formas, casos etiquetados y guardia de consistencia en pre-commit — vive en
  [docs/vicios/](docs/vicios/README.md) (su README es el tablero). Los hallazgos nuestros con
  números y seeds: [índice de hallazgos](docs/research/README.md). Las lecturas que respaldan
  este mapa (17 fuentes a texto completo): [extracciones](docs/research/2026-08-07-lecturas-programa-saltos.md).
- **Relación con el catálogo de vicios de la casa**: los 9 vicios del catálogo son estas
  fallas con más grano (el ① es el vicio 4; el ③ es el vicio 9; el ④ cruza los vicios 1 y 2;
  etc.) — este wiki los organiza por PASO DEL CICLO para que se entienda dónde golpea cada
  uno; el catálogo los organiza por fenómeno con su evidencia.
- **Advertencia metodológica que nos aplica**: el hindsight infecta también NUESTRAS
  autopsias — juzgamos los descartes del agente conociendo la verdad oculta del mundo. La
  protección: pre-registrar qué cuenta como "anomalía racionalmente descartable" antes de
  mirar la corrida.
- Hermanos: [WIKI-INDAGACION](WIKI-INDAGACION.md) · [WIKI-SALTOS](WIKI-SALTOS.md) · [WIKI](WIKI.md).
