# Glosario — los nombres de la casa, en llano

> Chuleta de una página (pedido de Lucas, 2026-08-07). Si un término nuevo entra al proyecto,
> entra acá con una línea. Para el detalle de cada cosa: el link de su línea.

## El proyecto en una frase

Construimos mundos simulados con una verdad escondida y ponemos agentes LLM a investigarlos,
para medir — sin jueces LLM — dónde exactamente se les rompe el proceso de descubrir.

## Las piezas del experimento

- **Experimento WAGER**: el paquete construido alrededor de un salto: un mundo, una tarea y un
  puntaje donde realizar ese salto permite encontrar un modelo claramente mejor que cualquier
  buen rival que no lo realiza. Incluye además sus condiciones, controles y tandas.
- **Salto**: el cambio de forma que queremos medir. Es el punto de partida de todo nombre y
  diseño. Ejemplo: **grupos escondidos**, pasar de una población a dos tipos.
- **Pregunta principal**: siempre tiene la misma forma: **¿el agente descubre y realiza el
  salto?**
- **Subpregunta**: pregunta cuándo, por qué o bajo qué condición aparece el salto. “Con pista”,
  “con error visible” y “con más presión” son subpreguntas o controles; no experimentos nuevos.
- **Mundo**: un programa que genera datos con una verdad escondida adentro. Si cambia la verdad,
  cambia el mundo.
- **Gemelo**: control anti-reflejo que puede agregarse después: un mundo parecido donde realizar
  el mismo salto sería un error. No es requisito de la etapa actual.
- **Tarea**: qué debe lograr el agente, con qué herramientas, presupuesto, turnos y tipo de
  entrega. El **encargo (brief)** es solo el texto con que se la contamos.
- **Perfil del mundo**: su ficha de forma oculta, verdad, dinámica, llegada de
  evidencia, horizonte, profundidad, interacción, dependencias, complejidad efectiva y
  dificultad observada por agente × tarea × ayuda.
- **ID de mundo**: `world__<familia>__<verdad>__v<n>`. Cambiar solo números crea otra
  instancia; cambiar la verdad o la forma crea otro mundo o una nueva versión explícita.
- **Condición**: la combinación exacta de los ejes manipulados: ayuda, aviso, consecuencia,
  etc. Para un contraste causal, dos condiciones deben diferir en un solo eje. Una consecuencia
  fija pertenece a la tarea; solo es condición si se manipula.
- **Episodio / partida**: una ejecución completa de un agente en un mundo, tarea y condición
  exactos: leer el encargo → comprar datos o ensayos → entregar el modelo.
- **Tanda**: el conjunto operativo de partidas que mandamos a correr. Una tanda implementa
  todo o parte de un experimento.
- **Instancia del mundo**: los parámetros concretos congelados de un mundo. Varias partidas
  pueden usar la misma instancia.
- **Semilla de partida**: identifica el azar de una ejecución. Puede compartirse entre partidas
  apareadas; una vez corrida queda quemada y nunca se repite “hasta que dé”.
- **Ensayo**: la intervención que compra el agente dentro de una partida. En el código todavía
  se llama `experiment`; en los documentos reservamos **experimento** para el paquete científico.
- **Perillas del mundo**: los diales que el agente puede fijar al hacer un ensayo (por ejemplo,
  velocidad o cantidad de repeticiones). No confundir con el salto **régimen oculto**.
- **Agente**: la IA que juega (por ejemplo GPT-5.4). **Modelo entregado**: el programa predictivo
  que esa IA produce. Evitamos llamar “modelo” a ambos en la misma frase.

Regla de identidad de una partida:

> **ID del experimento · mundo · tarea · condición · agente · instancia · semilla**

Regla del nombre humano: **Salto — situación investigativa**.

Regla del ID:

> `exp__<salto>__<situacion>__v<n>`

La **dificultad observada** no entra al nombre: se reporta por agente, tarea y ayuda. Un mismo
mundo puede ser fácil para un agente y difícil para otro.

Los códigos históricos (`D1`, `D2`, `P1`, `P2`), “brazo” y “polo” quedan solo como alias para
encontrar archivos viejos. Los títulos visibles dicen qué significan. **Variante** no se usa
sola: se aclara si es otro mundo, otra tarea u otra condición. **Versión** (`v1`, `v2`) nombra
solo una revisión técnica del mismo artefacto.

## Los saltos

- **Refinamiento**: ajustar los NÚMEROS de un modelo sin cambiarle la forma.
- **Salto**: una clase de cambio de forma del modelo —y también el acto de hacerla en una
  partida—: qué variables existen, cómo se conectan. **Grupos escondidos** es el nombre de un
  salto; un agente puede darlo o no. Eso es lo que medimos. **Distinción que manda (Lucas,
  2026-08-07): GENERAR el candidato cuando nada lo dicta (= creatividad, la vara del programa)
  ≠ ACEPTARLO cuando la evidencia lo grita (= revisión de creencias, vicio 1).** Un mundo mide
  creatividad solo si el candidato tiene que
  NACER del agente. ⚠️ **No son dos fenómenos separados** (Aliseda; ratificado Codex
  2026-08-09): son **momentos operacionalmente separables** de un solo proceso —
  revisar = soltar (contracción) + incorporar (expansión), y generar el candidato ocurre en
  las dos. Lo que separamos server-side es el MOMENTO (antes/después de que la evidencia
  discrimine), y eso prueba activación-antes-de-discriminación, no que el candidato estuviera
  fuera del espacio efectivo del agente.
- **Lista de saltos** (alias técnico histórico: operadores): las 10+1 clases están
  **contadas con historia y fuentes en [el libro de los saltos](saltos.md)** y su
  [justificación formal](research/2026-08-05-fundamentos-taxonomia-de-saltos.md): 1 entidad oculta ·
  2 grupos escondidos (`count_mix`) · 3 régimen/fase oculto (dos leyes con umbral) · 4 geometría ·
  5 unificación · 6 invariante promovido (simetría) · 7 proceso del observador · 8 realimentación
  oculta · 9 conservación/cuantización · 10 memoria oculta · 11 transferencia estructural
  (analogía tipo Darwin).
- **Menú de hipótesis**: las familias de modelos que el agente considera de entrada. **Lo
  observado en trazas: el candidato correcto no llega a compararse ni implementarse** — todo lo
  demás (comprar datos, ajustar, chequear) lo hacen bien. ⚠️ "No ENTRÓ al menú" es
  interpretación post-hoc, no variable observada (Codex 2026-08-09); se vuelve observable con
  la cadena registrada de la ficha v1 (candidata registrada ANTES del punto de discriminación
  = expansión generativa).
- **Juntura**: eslabón específico de la cadena de investigar (comprar → mirar → postular →
  testear → entregar). Medimos cuál se rompe, no "si es bueno o malo".

## La vara y las señales (el fondo del marco — [WIKI-INDAGACION §6](../WIKI-INDAGACION.md))

- **Vara de dos bolsillos (compresión / MDL)**: una edición al modelo es MEJORA si baja la
  suma "costo de describir el modelo" (simplicidad) + "costo de lo que no explica" (residuos).
  El parche (epiciclo, Vulcano) mejora el ajuste pagando complejidad escondida — esta vara lo
  cobra. Nuestro BIC de testigos y R son la versión operativa, cero-LLM.
- **Disparador vs criterio**: el criterio de mejora se computa DESPUÉS de tener el candidato;
  el disparador es lo que te pone a buscarlo ANTES (con lo de siempre andando bien). Dos
  canales: **impasse por datos** (el modelo falla visible y persistente) e **impasse por
  coherencia** (las piezas del propio modelo no cierran entre sí — el canal Einstein; los
  agentes jamás lo auditan).
- **Predicción vs intervención**: modelos que empatan sobre lo ya visto se separan al mover
  una perilla; por eso el examen incluye regímenes que el agente no visitó.

## Las ayudas, nombradas por lo que contienen

- **Sin ayuda**: solo el encargo.
- **Dirección general**: señala dónde mirar, sin nombrar la idea.
- **Idea nombrada**: dice qué posibilidad considerar, pero el agente debe investigarla,
  estimarla y convertirla en un modelo. Esta es la prueba real de resolubilidad con agente.
- **Herramienta indicada**: sugiere una familia de método, sin dar los números ni el resultado.
- **Solución servida — control de techo**: describe casi toda la respuesta. Solo comprueba que
  la interfaz y la entrega admiten la solución; no mide descubrimiento.
- **Procedimiento pedido**: ordena un acto (“compará al menos dos familias”) sin nombrar una
  idea. Es otro tipo de condición, no un peldaño de “más ayuda”.

Los nombres numéricos viejos se retiran porque escondían el contenido y chocaban con otra
escalera anterior. Resultado histórico que motivó la separación: nombrar la idea rescató a GPT
4/4; indicar la herramienta rescató a DeepSeek 3/3; pedir solo el procedimiento dio 0/3.

## Métricas (las columnas del Explorer)

- **S_valley_fuerte** (mundo principal, 0→1): ¿capturó los grupos escondidos? 0 = igual que el
  mejor rival continuo, 1 = igual que la verdad. LA vara del salto.
- **S_clean** (gemelo, 0→1): limpieza — qué tan cerca de la verdad simple quedó.
- **espurio** (gemelo): ¿inventó grupos que no existen? (bandera sí/no).
- **F_mean**: ¿clavó el promedio? (chequeo básico, casi siempre ≈1).
- **ICC**: persistencia por lote — cuánto se parecen mediciones del mismo lote.
- **R**: parecido global de los datos generados (0→1). ⚠️ Deuda conocida: hoy castiga al que
  descubre los grupos; no usarla para rankear salto.
- **Censura**: corrida inválida (se quedó sin tokens, no entregó código) — se reporta, no cuenta
  ni a favor ni en contra.

## Microscopio vs mundo realista ([anatomía de casos reales](research/2026-08-10-anatomia-casos-reales-requisitos-mundo-realista.md))

- **Mundo microscopio**: chico a propósito — una perilla, una estructura escondida, sin colegas
  ni instrumentos. Si el agente falla, no hay dónde esconderse (por eso el 0/9 vale). Su límite:
  el claim no viaja más allá de lo que el episodio instancia.
- **Mundo realista**: instancia las CONDICIONES de los casos reales, no su fachada. Los tres ejes
  que el corpus entero pide y ningún mundo nuestro tiene: **instrumento-vs-mundo** (¿es el aparato
  o el fenómeno?, con costo de averiguarlo) · **menú de rivales** (≥3 explicaciones vivas) ·
  **otro que critica** (con la advertencia de que los pares simétricos ESCALAN el compromiso; lo
  que funciona es el revisor sin propiedad de la teoría).
- **Diagnosticity** (Heuer): cuánto DISCRIMINA una compra entre las hipótesis vivas. La evidencia
  consistente con todas vale cero ("la fiebre prueba enfermedad, no cuál"). Computable exacto
  server-side → métrica de economía de la investigación.
- **Fidelidad de condiciones, no de fachada** (regla dura): más piel industrial con las mismas
  junturas no es más realista.

## Reglas de juego de la investigación

- **Validación del mundo y la tarea**: el control previo completo. Reúne las dos pruebas
  siguientes; ninguna reemplaza a la otra.
- **Certificación matemática**: pruebas automáticas de necesidad (el salto mejora de verdad
  contra el mejor rival fuerte), alcanzabilidad de la evidencia y anti-memorización.
- **Prueba de resolubilidad con agente**: el mismo agente, con la idea nombrada pero sin la
  solución, debe poder investigar, implementar el salto y mejorar. Complementa la matemática;
  no la reemplaza. Su diferencia frente al mismo agente sin ayuda informa cuánto costó descubrir
  la idea, pero es una subpregunta de validación. Su alcance es siempre mundo + tarea + agente +
  ayuda concretos; no valida “el mundo” en abstracto.
- **Rival fuerte**: el mejor modelo SIN el salto (en **Conteos por lote**, `count_mix`: gamma
  continua con persistencia).
  Toda vara se ancla contra él, no contra un rival de paja.
- **Pre-registro**: predicciones y reglas de decisión escritas y commiteadas ANTES de correr.
  Una-frase-una-corrida: las ayudas se congelan textualmente; no se escalan sobre la marcha.
- **Descubrimiento vs confirmación** (fases que no se mezclan): ahora estamos en descubrimiento
  (barato, exploratorio); confirmación = pregunta congelada + seeds frescas + modelos held-out.
- **Cero-LLM en el reward**: ningún juez LLM toca el puntaje, jamás.

## Los vicios (catálogo, por número — [tablero](vicios/README.md))

1 calibración de creencias (rigidez / influenciable) · 2 calibración de parada (cierre
prematuro↔pozo) · 3 no verificar / fabricar · 4 **no postular la estructura escondida**
(**Conteos por lote**, `count_mix`) · 5 perder el hilo · 6 adivinar en vez de preguntar ·
7 correlación vs causa · 8 perder el objetivo · 9 **verificación de paja** (testea con tests
que no pueden fallar — el “teatro de comparación”). **Ahas**: los saltos positivos (notar la
anomalía, pivotar a tiempo, pedir el dato que discrimina). Sus controles opuestos pueden agregarse
después de validar el mundo base.

## Dónde vive cada cosa

Marco teórico: [WIKI-INDAGACION](../WIKI-INDAGACION.md) · saltos de bolsillo:
[WIKI-SALTOS](../WIKI-SALTOS.md) · fallas de bolsillo: [WIKI-FALLAS](../WIKI-FALLAS.md) ·
Estado y próximo paso: [roadmap](roadmap.md) · hallazgos: [índice](research/README.md) ·
evidencia de vicios: [docs/vicios/](vicios/README.md) · cómo se mide: [como-medimos](como-medimos.md) ·
mundos por vicio: [derivación](mundos-por-vicio.md) · corridas navegables: `explorer.command`.
