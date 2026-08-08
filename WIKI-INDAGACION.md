# WIKI — Indagación: el marco teórico del proyecto

> **Qué es este documento.** El marco conceptual de WAGER en una sentada: qué tipo de tarea
> estudiamos, cómo se llama, cuál es su ciclo, y dónde entran los saltos. Lenguaje llano.
> Los hermanos de este wiki: [WIKI.md](WIKI.md) (la máquina WAGER) ·
> [WIKI-SALTOS.md](WIKI-SALTOS.md) (los tipos de salto) · [WIKI-FALLAS.md](WIKI-FALLAS.md)
> (cómo se rompe la indagación). El detalle profundo con fuentes: [docs/saltos.md](docs/saltos.md).

## 1. El nombre: INDAGACIÓN (inquiry)

Nuestro objeto de estudio tiene nombre con un siglo de pedigrí: **inquiry** — lo usó Peirce
(el que inventó "abducción") y Dewey le dedicó su lógica entera. En castellano: **indagación**.
La definición de casa: **el trabajo de inferir una verdad oculta que ya existe, comprando
evidencia con presupuesto limitado**. No usamos "investigación" (ambiguo: también significa
"research" en general) ni "razonamiento" (demasiado general — ver §5).

Una frase para presentar el proyecto: *WAGER estudia la indagación — el razonamiento
explicativo sobre sistemas con estructura oculta — midiendo dónde se rompe y si aparecen los
saltos creativos.*

## 2. Las tres familias de "resolver" (no toda tarea es lo mismo)

| Familia | Qué es | Ejemplos | ¿Verdad oculta? |
|---|---|---|---|
| **A. Ejecutar / buscar** | Reglas y meta conocidas; encontrar el camino | Rubik, ajedrez, implementar lo ya diseñado | No — pura combinatoria |
| **B. Diseñar / construir** | La "respuesta" no existe hasta que la hacés | una app, un puente, una canción | No — se crea, no se descubre |
| **C. INDAGAR** | Hay una verdad oculta que YA existe; se infiere desde observaciones compradas | detective, médico, científico, analista, **debuggear** | **SÍ — es la definición** |

Las tareas reales mezclan familias: programar es B… hasta que aparece el bug — debuggear es C
metida adentro de B (por eso "se siente" detectivesco). La ciencia es C en el núcleo con B en
el diseño de instrumentos. **WAGER trabaja en la familia C, destilada.**

## 3. El ciclo de la indagación (el proceso que comparten todos)

El juez, el médico, el detective y el científico ejecutan EL MISMO lazo (lo describió Peirce;
Klahr & Dunbar lo midieron en laboratorio como búsqueda en dos espacios — hipótesis ×
experimentos):

1. **ABDUCIR** — generar explicaciones candidatas: *"¿y si los lotes vienen de DOS máquinas?"*
2. **DEDUCIR** — derivar qué se vería si cada candidata fuera cierta: *"entonces el histograma
   debería tener dos jorobas, y lotes del mismo tipo deberían parecerse entre sí."*
3. **TESTEAR / INDUCIR** — comprar la evidencia y actualizar: *"compro mediciones repetidas
   del mismo lote y miro."*
4. **Volver al paso 1** — con **economía**: cada dato cuesta; parte del arte es gastar el
   presupuesto en evidencia que DISCRIMINA entre candidatas (no en "fiebre": evidencia
   consistente con todas, que no vale nada — el concepto de *diagnosticity* de Heuer).

## 4. Las tres herramientas, bien separadas (y la zona que parecía difusa)

- **DEDUCCIÓN**: de la regla al caso. *"Todos los lotes de la máquina A salen fallados; este
  es de A ⇒ saldrá fallado."* Cero riesgo; no agrega conocimiento del mundo — solo despliega
  lo que ya afirmaste. En la indagación sirve para derivar predicciones testeables.
- **INDUCCIÓN**: repartir credibilidad **DENTRO de un espacio dado** de hipótesis. Estimar
  parámetros, testear, generalizar. **Bayes es la matemática de la inducción**: P(modelo |
  datos) te dice cuánto creerle a cada modelo… **pero solo reparte entre los modelos que YA
  están en la lista**. Es la limitación famosa del bayesianismo puro (el problema del
  "catch-all"): condicionar jamás agranda el espacio.
- **ABDUCCIÓN**: **poner candidatos EN la lista**. Dos grados (Magnani): *selectiva* — traer
  uno del repertorio que ya tenés (el médico eligiendo entre enfermedades conocidas) — y
  *creativa* — **fabricar un candidato que el repertorio no contiene** (postular clases
  ocultas, un umbral, una entidad invisible). La creativa es EL SALTO.

**El criterio operativo que corta limpio** (cuando la filosofía se pone difusa, usamos este):
> ¿Tu movida **reparte probabilidad dentro** del espacio de hipótesis, o **agranda** el espacio?
> Lo primero es inducción/selección. Lo segundo es abducción creativa.

Con eso, "crear un modelo a partir de datos" se descompone sin misterio: **elegir la FORMA**
del modelo (¿una población o mezcla de dos? ¿una ley o dos con umbral?) = abducción; **ajustar
sus números** = inducción; **comparar formas de un menú fijo** por BIC/Bayes = abducción
selectiva mecanizada (elegís, no inventás). Sí existe debate filosófico en el borde (la
"inferencia a la mejor explicación" mezcla generación con selección) — pero nuestro corte
operativo es medible y no ambiguo.

**Y la conexión con nuestros hallazgos**: nuestros agentes hacen inducción casi impecable
(ajustan, estiman, hasta comparan si se lo ordenás) **sobre un espacio que jamás agrandan**.
El déficit no está en Bayes — está en quién escribe la lista sobre la que Bayes corre.

## 5. Las cuatro perillas (por qué el juez, el médico y el detective no son idénticos)

Mismo ciclo, distinto punto del espacio de configuraciones:

1. **¿El menú está cerrado o abierto?** El médico casi siempre elige de la nosología; el
   científico en la frontera tiene que inventar el candidato.
2. **¿Podés experimentar, o solo evaluar lo que te traen?** El médico pide estudios; el
   científico interviene; **el juez no experimenta** — evalúa evidencia producida por otros.
3. **¿La fuente puede mentir?** La naturaleza no engaña; el sospechoso y el adversario sí.
4. **¿Con qué vara se decide?** "Más allá de duda razonable" ≠ "p<0.05" ≠ "empezar el
   tratamiento ya".

**La frase que ata todo: nuestra máquina de mundos ES ese espacio de perillas.** Cada
profesión es un punto en él; WAGER fabrica los puntos a voluntad, con la verdad bajo control
y el puntaje sin jueces LLM.

## 6. Indagar no es solo razonar

El razonamiento (deducir/inducir/abducir) es la caja de herramientas central, pero la
indagación usa más músculos, y las fallas reales viven también ahí:

- **Memoria**: el detective que vio el nombre clave y no lo conectó — falla de recuperación
  (la memoria trae por parecido superficial, no por estructura: Gentner, 70/30), no de lógica.
- **Percepción**: nuestro agente que IMPRIMIÓ el histograma con las dos jorobas y no lo vio —
  se mira a través de los resúmenes que el modelo vigente considera relevantes.
- **Economía**: saber gastar (evidencia que discrimina; cuándo replicar; cuándo parar).
- **El gatillo del insight NO es deliberado**: la reestructuración aparece tras un IMPASSE
  (fracaso persistente y visible — Ohlsson), no porque la invoques. "Sé creativo" no funciona;
  fabricar la pared sí.

## 7. Dónde seguir

- **Los tipos de salto** (la abducción creativa, clasificada): [WIKI-SALTOS.md](WIKI-SALTOS.md)
- **Cómo se rompe la indagación** (los failure modes): [WIKI-FALLAS.md](WIKI-FALLAS.md)
- **La máquina que lo mide** (mundos, gemelos, puntaje): [WIKI.md](WIKI.md)
- **El fondo con fuentes leídas**: [docs/saltos.md](docs/saltos.md) y
  [docs/research/2026-08-07-lecturas-programa-saltos.md](docs/research/2026-08-07-lecturas-programa-saltos.md)
