# Mundos por vicio — la derivación oficial (de la lista a los mundos)

> **Qué es este documento (ADR 0113).** La síntesis EN LLANO, error por error: qué es cada failure
> mode, **de dónde sale** (fuentes), **en qué contextos aparece documentado** (cuantos más contextos
> independientes, más seguro que es un error de fondo y no una anécdota — y más variedad estructural
> para construir), **qué estructuras tiene**, y **qué mundo lo caza** — exista o no ese mundo hoy.
> Derivado **catálogo-primero** (orden de Lucas, 2026-07-09): *lo construido antes NO manda* — los
> mundos existentes solo cuentan como "ya cubierto" donde les toca. La evidencia detallada con citas
> vive en `docs/failure-modes.md` (el catálogo); esto es la destilación para pensar y diseñar.
> Nada entra a la cola de trabajo por este documento (la cola vive en `docs/roadmap.md`).

**La vara de validación, común a todos** (cómo sabemos que un mundo de verdad caza su error):
1. **Dos jugadores-robot**: uno que comete el error (debe perder) y uno cuidadoso (debe poder ganar).
   Si no se cumple, el mundo está mal hecho y se descarta.
2. **IAs reales jugando libres**: ¿caen solas? (si nadie cae nunca, el mundo no muerde).
3. **La prueba de la frase** (validada 2 veces, con 2 modelos): advertirle al jugador sobre *ese*
   error se lo arregla — y no mueve nada en mundos sin ese error.
4. Ideal, **con dos IAs distintas**: ya sabemos que cada modelo tiene su propio perfil de mañas
   (GPT esconde el vicio con plata de sobra; DeepSeek cae igual).

---

## Vicio 1 — No cambiar de idea ante la evidencia

**Qué es.** Formarse una explicación temprano y no soltarla, aunque la evidencia la contradiga:
buscar solo lo que confirma, descontar lo que molesta, ajustar de menos.

**Dónde está documentado (5 contextos independientes — el más respaldado de la lista):**
- *Laboratorio cognitivo*: Wason 1960 (el juego 2-4-6); Klayman & Ha 1987 (por qué confirmar no
  refuta nunca si tu regla es un caso particular de la verdadera); Anderson, Lepper & Ross 1980 (la
  creencia sobrevive a que te digan que la evidencia era ficticia — y EXPLICAR por qué creés te
  blinda más); Teovanović 2019 (anclaje: el ajuste queda ~21% corto).
- *Científicos reales trabajando*: Dunbar 1997 (ignoran la anomalía si llega temprano y toca una
  hipótesis secundaria; la atienden si toca el corazón o llega tarde); Mitroff 1974 (los 42
  científicos del programa Apollo: 3.5 años de datos lunares no movieron sus hipótesis favoritas).
- *Historia de la ciencia*: el agujero de ozono casi descartado porque el patrón de referencia
  estaba mal (la anomalía real parecía error de instrumento); la deriva continental rechazada con
  doble vara (a la teoría rival le exigían un mecanismo que la propia tampoco tenía).
- *Respuestas a datos anómalos*: Chinn & Brewer 1993 — de 7 reacciones posibles a un dato que te
  contradice, SOLO 1 es "aceptar y cambiar"; las otras 6 lo descartan de formas distintas.
- *Agentes IA (medido en modelos)*: la evidencia contradictoria se ignora en el **68%** de los
  casos; la creencia refutada se revisa solo el **26%** (análisis de trazas, 2026). Y nuestra propia
  mesa: DeepSeek se casa con la 1ª hipótesis aun con presupuesto de sobra (réplica 2026-07-09).

**Estructuras (≈8 — cada una es un mundo distinto porque el mecanismo es distinto):**
1. *La contradicción llega a mitad de camino* — hay que incorporarla en caliente.
2. *La trampa de solo-confirmar* — tu idea es un caso particular de la verdad: TODA prueba
   confirmatoria la confirma; solo probar donde NO esperás efecto revela el error.
3. *El espejo* — tu idea es más amplia que la verdad: ahora confirmar es lo único que refuta.
   (2 y 3 juntas son el par perfecto: ningún reflejo fijo gana ambas.)
4. *Te retiran la evidencia* — un dato que compraste se invalida después: ¿tu creencia vuelve atrás?
5. *El ancla* — un número prominente al inicio, corrido; ajustar "un poco" nunca llega.
6. *Buscar confirmar, no refutar* — corrés solo los tests que dan la razón.
7. *El blanco borroso* — la afirmación fuerte se repliega a una trivial bajo presión y vuelve a
   inflarse (infalsificable por diseño).
8. *La referencia corrupta* — descartás la anomalía real porque el patrón de comparación está mal.

**El mundo que lo caza (ingredientes):** (a) una primera explicación tentadora que la historia del
mundo te planta sola; (b) esa explicación está mal; (c) la evidencia que la desmiente está
disponible pero no regalada — hay que ir a buscarla (y en las variantes 2/3, saber DÓNDE buscarla).

**Estado:** `first_story` (hecho, validado con 2 modelos — la prueba de la frase funciona);
el par confirmar/espejo tiene diseño escrito (en cantera); retracción y ancla: sin mundo.

---

## Vicio 2 — El pozo: no saber soltar ni parar

**Qué es.** Meterse en algo fascinante que no paga; o seguir invirtiendo en un camino muerto porque
ya se invirtió mucho; o "hacer algo" ante la mala noticia aunque lo activo sea lo equivocado.

**Dónde está documentado (4 contextos):**
- *Laboratorio de decisiones*: Arkes & Blumer 1985 (costo hundido: lo ya gastado — que es
  irrecuperable — sesga la decisión de seguir); meta-análisis 2015 (efecto real y mediano, ~0.5).
- *Psicología de la escalada*: Feldman & Wong 2018 — la receta de 3 ingredientes (inversión previa +
  señal negativa + punto de decisión seguir/soltar) y el hallazgo fino: la mala noticia empuja a
  ACTUAR, sea lo que sea — si "seguir" es la opción activa, se escala; si reformulás para que
  "soltar" sea lo activo, el sesgo SE INVIERTE.
- *Historia de la ciencia*: la deriva continental — un solo hueco sin resolver (el mecanismo) vetó
  una teoría con evidencia convergente de sobra; y el caso del flogisto como ADVERTENCIA (ver abajo).
- *Agentes IA (medido)*: el loop de acción-fallida-repetida — tras un fallo, el agente repite la
  MISMA acción una y otra vez (benchmarks 2026); el 67% repite la acción que acaba de fallar.

**Estructuras (5):** el señuelo fascinante (pozo puro) · costo hundido (continuar-vs-abandonar) ·
escalada (los 3 ingredientes) · el empuje-a-actuar (inaction effect) · un-hueco-veta-todo.

**El mundo que lo caza (ingredientes):** un señuelo GENUINAMENTE fascinante (un patrón intrincado
que parece la clave y no aporta al examen) cuyo costo es de oportunidad — lo que quemaste ahí te
falta para lo que importa; O una línea de investigación pagada que deja de rendir, con la señal
clara y el punto de decisión explícito.
**⚠ La advertencia del flogisto (Chang 2010):** persistir es vicio SOLO si soltar es CLARAMENTE
mejor. Si las dos opciones empatan en evidencia, aferrarse es prudencia — un mundo que castiga eso
está midiendo mal. El certificado de robots obliga a que esto se cumpla.

**Estado: CERO mundos. El hueco más grave de la cartera** — y uno de los errores más típicos de
agentes IA investigando.

---

## Vicio 3 — Inflar significancia / no verificar

**Qué es.** De todas las formas legítimas de mirar los datos, terminar (sin mala intención) en la
que "da algo" — y entregar ese hallazgo, que es ruido. O directamente afirmar sin verificar.

**Dónde está documentado (3 contextos + nuestra propia mesa):**
- *Metaciencia (la crisis de replicación)*: Simmons et al. 2011 — usando los 4 grados de libertad
  típicos a la vez, la chance de un falso hallazgo sube del 5% al **60.7%** (más probable falso que
  verdadero); Gelman & Loken (el jardín de senderos: pasa AUN sin intención, porque cada decisión
  analítica "parece la única razonable" mirando estos datos); Stefan & Schönbrodt 2023 (12
  estrategias, una sola — elegir la métrica que dio — infla 5%→~40%); Nagy et al. 2025 (40 prácticas
  cuestionables, indexadas por fase).
- *Agentes IA*: los experimentos con agentes AMPLIFICAN estos grados de libertad (elección de
  modelo, prompt, re-diseño según el resultado — "fáciles de explotar, difíciles de detectar",
  2026); y la fabricación directa: **~80%** de resultados fabricados/inválidos cuando el experimento
  falla (MLR-Bench 2025), aun instruyendo "no fabriques".
- *Nuestra propia mesa (medido en vivo)*: un modelo declaró una precisión que jamás midió
  (la "precisión fabricada") — la nota se lo cobró.

**Estructuras (4 + 1):** elegir la métrica que dio · parar de muestrear cuando conviene · meter/sacar
variables de control hasta que cruce el umbral · reportar solo las condiciones que "funcionaron" ·
(+) fabricar el número que falta.

**El mundo que lo caza (ingredientes):** 2-3 métricas alternativas legítimas donde UNA muestra un
efecto llamativo que es casualidad y la aburrida es la real — el examen fuera de muestra cobra al
que entregó lo vistoso; O el corte oportunista: el agente decide cuándo dejar de juntar datos, y
cortar "cuando se ve bien" infla el efecto (chico, barato, angosto — no necesita el mundo ancho, que
murió como anfitrión).

**Estado:** cero mundos dedicados (el sobre-afirmar retórico ya vale cero por construcción; la
fabricación ya se cobra). Los dos diseños de arriba son de los más baratos de construir.

---

## Vicio 4 — No inventar la explicación escondida

**Qué es.** Quedarse con el modelo de manual cuando los datos solo cierran si imaginás algo que
nadie te dio (una variable oculta, dos mecanismos donde parecía uno, otra representación).

**Dónde está documentado (4 contextos):**
- *Científicos reales*: Dunbar 1997 — un lab asumía UNA causa; una anomalía los forzó a partirla en
  DOS mecanismos; y el descubrimiento real corre sobre analogías CERCANAS (de 99 analogías en 16
  reuniones, solo 2 lejanas — el "salto lejano" romántico es mito).
- *Laboratorio cognitivo*: Klahr & Dunbar 1988 — para entender un aparato había que reconcebir un
  parámetro de "contador" a "selector": 17 de 20 no cruzaron nunca; cruzar exige cambiar ≥3 cosas A
  LA VEZ (por eso revisar de a una no llega). Y el efecto Einstellung: una solución conocida, cebada,
  BLOQUEA una mejor que está disponible.
- *Historia de la ciencia*: Neptuno (postular el planeta invisible que explica el bamboleo — y
  encontrarlo esa noche) como el polo genial; Vulcano como su gemelo malo (misma jugada, y la
  respuesta verdadera era cambiar la teoría).
- *Agentes IA (nuestra mesa, medido)*: el trofeo — 10 partidas, 2 familias de modelos, NADIE intentó
  inferir la composición oculta del lote; el mejor jugó "técnicamente perfecto" y sacó 0.096.
  Ejecutar la idea cuesta 10 líneas; CONCEBIRLA es lo que faltó. También: los agentes se hunden
  cuando la tarea exige recuperar un estado oculto (benchmarks 2025-26).

**Estructuras (6):** postular la variable oculta · partir-en-dos · re-representar (cambiar el marco,
≥3 casilleros a la vez) · la solución cebada que bloquea (Einstellung) · analogía cercana correcta ·
anomalía atendida-o-ignorada según cuán central y cuán tarde.

**El mundo que lo caza (ingredientes):** los datos parecen ruido o contradicción con el modelo de
manual; ese modelo toca un techo medible; el techo solo se cruza postulando la estructura no dada.
El robot "revisor-de-a-pasitos" DEBE fallar (el salto es discontinuo); el dial de dificultad es
cuántas cosas hay que cambiar a la vez.

**Estado:** v2 HECHO — el trofeo del proyecto, la familia con margen demostrado. Variantes
partir-en-dos y Einstellung: sin mundo. El gemelo Vulcano: decidido como primer PAR (viabilidad
pendiente, gratis).

---

## Vicio 5 — Perder el hilo en tareas largas → NO se construye en contra (a propósito)

Es el error de "trabajador desprolijo" (pierde restricciones, olvida, repite): lo arregla mejor
memoria/andamiaje, no juicio — y medio campo ya trabaja en eso. **Decisión vigente: se MIDE si
aparece, no se diseña en contra.** (Documentado en benchmarks de agentes 2025-26: caída monótona con
el largo; colapso de fase; la variante interesante — "la regla sigue EN contexto y la viola igual" —
es de juicio, pero exige horizontes que nuestros episodios no fuerzan.)

---

## Vicio 6 — Adivinar en vez de preguntar → BLOQUEADO por una regla del juego (decisión de Lucas, sin apuro)

**Qué es.** Falta información; en vez de conseguirla (preguntando, que es barato), la inventa.

**Dónde está documentado (el MEJOR material medido-en-modelos de toda la lista):** Su & Cardie
2026 — los modelos DETECTAN la ambigüedad (60-80%) pero preguntan <5%: la falla es de acción, no de
detección; darles contexto los hace preguntar MENOS (falsa sensación de suficiencia); BED-LLM 2025 —
en un juego de preguntas, proponen hipótesis incompatibles con lo ya observado y eligen preguntas
que no discriminan (45% vs 93% con estrategia).

**Por qué está bloqueado:** casi todas sus estructuras exigen el verbo **PREGUNTAR** (un oráculo
consultable con costo) — y nuestro juego solo tiene "comprar datos" y "experimentar". Agregar ese
verbo cambia el contrato de TODOS los mundos → decisión grande, de Lucas, sin apuro. La única
estructura construible hoy (elegir la pregunta/experimento que de verdad discrimina) **ya tiene
mundo diseñado: el Mundo B**.

---

## Vicio 7 — Confundir "pasan juntas" con "una causa la otra"

**Qué es.** Leer causalidad en una correlación; no ver el tercer factor; no darse cuenta de que
mirar no alcanza y hay que intervenir.

**Dónde está documentado (4 contextos):**
- *Agentes IA (medido)*: Corr2Cause 2023 — 17 modelos (hasta GPT-4) infieren causalidad desde
  correlación AL NIVEL DEL AZAR.
- *Ciencia patológica*: Elton & Spencer 2020 — el MISMO mecanismo (un factor escondido que acompaña
  la manipulación) explica 4 episodios famosos de "descubrimientos" falsos en la ciencia del agua.
- *Ciencia de datos / ML*: Kapoor & Narayanan 2023 — 8 tipos de fuga/desajuste que inflan resultados
  aun con partición limpia (generalizar más allá del proceso que generó los datos).
- *Historia*: la referencia corrupta del ozono (cruza con el vicio 1).

**Estructuras:** el confusor (tercer factor) · la referencia corrupta · **faltan por minar**: el
sesgo del colisionador/selección (Berkson) y el caso "mirar-no-alcanza-ni-en-principio".

**El mundo que lo caza:** la familia MÁS cubierta (5 mundos hechos: confusor por asignación, sesgo
de selección ×2, supervivencia, efecto-lote). **El que falta, derivado de la lista:** el mundo donde
la observación es estructuralmente insuficiente — gana el que interviene o el que se abstiene con
honestidad; pierde el que entrega una respuesta confiada mirando.

---

## Los saltos creativos (el espejo — SIEMPRE de a pares)

Cada operación creativa tiene su gemelo malo: la MISMA jugada, genial cuando la situación la pide,
desastre cuando no. Por eso se construyen de a pares (misma fachada, polos opuestos): el reflejo
"aplicá siempre la jugada" gana un mundo y pierde el gemelo; solo el que paga por averiguar en cuál
está gana ambos.

- **Postular lo invisible ↔ parchar** (Neptuno ↔ Vulcano; el mismo Le Verrier, misma jugada, un
  acierto glorioso y un fracaso total): PAR BANDERA, decidido; falta el test de viabilidad del
  gemelo (gratis).
- **Unificar ↔ ver patrones donde no hay** (la teoría ondulatoria de la luz ↔ apofenia): mundo
  barato — dos anomalías que parecen separadas con UNA causa común; el que parcha cada una por
  separado paga doble. (Falta el caso histórico nombrado del lado malo — hueco de la búsqueda.)
- **Analogía estructural ↔ analogía de superficie** (Darwin ↔ dejarse llevar por el parecido; en
  humanos 70/30; en modelos: colapsan en variantes retorcidas donde el humano aguanta — hallazgo
  2024, en disputa): mundo — transferir el mecanismo de un sistema conocido a uno nuevo que solo
  comparte la estructura profunda.
- **Buscar en dos espacios** (diseñar el experimento que separa, no solo pensar hipótesis): ES el
  Mundo B, ya diseñado.
- **Re-representar** (cambiar el marco destapa la predicción): ES la familia del trofeo (v2).

---

## Estado global (la foto en una tabla)

| Error | Contextos doc. | Estructuras | Mundos hechos | El hueco |
|---|---|---|---|---|
| 1. No cambiar de idea | 5 | ≈8 | 1 (+1 spec) | retracción, ancla, par confirmar/espejo |
| 2. El pozo / no soltar | 4 | 5 | **0** | TODO — el hueco más grave |
| 3. Inflar significancia | 3 + propia | 4+1 | 0 dedicados | los 2 diseños baratos |
| 4. Inventar la estructura | 4 | 6 | 1 (el trofeo) | partir-en-dos, Einstellung, el PAR Vulcano |
| 5. Perder el hilo largo | (benchmarks) | 7 | — | no se construye (a propósito) |
| 6. Adivinar vs preguntar | LLM-nativo | 4 | Mundo B (diseñado) | bloqueado por el verbo "preguntar" |
| 7. Causa y efecto | 4 | 2 (+2 por minar) | **5** | "mirar no alcanza"; colisionador |
| Saltos (pares) | — | 5 operaciones | v2 instancia una | Vulcano (bandera), consiliencia, analogía |
