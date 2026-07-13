# Failure modes del juicio investigativo — catálogo y scaffold de diseño

> **Capa fina (ADR 0140)**: las SUB-FORMAS de cada vicio (mecanismo · disparador ·
> firma · borde) con casos reales etiquetados están en **`docs/vicios/`** (síntesis de
> cinco vías, 2026-07-12). Este doc mantiene la tesis, la definición operativa y el
> scaffold de diseño.

> **Documento vivo (ADR 0099).** El corazón del proyecto: de un failure mode DOCUMENTADO
> → a la especificación de un mundo que lo pone de manifiesto de forma PUNTUABLE. No es una
> lista de memoria — es un scaffold para *ir a la literatura con paciencia, razonar, y
> diseñar mundos de a uno*. Reemplaza al viejo `FAILURE_MODES.md` (disuelto en la
> reestructura) con la estructura que ganamos discutiendo. Precedente de disciplina:
> `docs/mundo-a-primera-historia.md`, `docs/proto-designer.md`.

---

## 0. La tesis y la definición operativa

**La tesis en una frase**: medimos juicio investigativo construyendo mundos donde la conducta se
OBSERVA (firma de trace) pero jamás se premia — el mundo hace que el vicio produzca un modelo final
peor y el examen cero-LLM cobra la consecuencia. Cada failure mode (y cada operación de aha) bien
documentado es una especificación para un mundo.

**La definición operativa (vigente — Lucas, 2026-07-09; ADR 0109)** — dos polos, una habilidad:

> **Buen juicio investigativo, TAL COMO LO MEDIMOS, es: no caer donde los agentes documentadamente
> caen (los vicios), saltar donde el descubrimiento documentadamente salta (los ahas), y —lo que une
> a los dos— saber CUÁNDO: discriminar activamente (pagando por la evidencia que separa los polos) en
> qué situación estás, y en consecuencia aplicar la operación o abstenerte.**

Tres precisiones que la hacen honesta:
1. **La lista NO es el juicio — es nuestra muestra MEDIBLE de él** (el termómetro no es la fiebre).
   Siempre incompleta, siempre creciendo (por eso la regla del residuo y las semillas de la realidad).
   Si un agente saca reward perfecto en toda la cartera, la conclusión correcta es **"pasó nuestro
   examen actual"**, NO "tiene buen juicio, punto" — y el examen tiene que poder crecer. Confundir la
   lista con el juicio sería confundir el termómetro con la fiebre.
2. **El vicio y el aha son los DOS POLOS de la misma operación**, no dos listas
   (unificar↔apofenia, postular-entidad↔parchar). Por eso la unidad de diseño es el PAR (principio
   10): un agente puede aprender el reflejo "siempre desconfiá" o "siempre postulá" y ganar los
   mundos de UN polo — el par es lo que impide que el conjunto se pueda trampear, porque solo el que
   discrimina gana AMBOS.
3. **El reward nunca sabe del vicio ni del aha**: la nota es siempre "¿qué tan bien predice tu
   modelo?"; el diseño hace que la mala jugada prediga peor. La consecuencia se cobra sola.

## 0.5. El corte primario: OPERACIÓN vs JUICIO (define el ALCANCE de WAGER)

> **Actualización (ADR 0141, 2026-07-13)**: el corte binario se amplía a TRES EJES — el JUICIO
> se parte en **COMPETENCIA epistémica** (actualizar, causar, postular, parar) e **INTEGRIDAD**
> (fabricar, falsificar, cherry-pickear, ceder por presión — el eje que faltaba, el único donde
> más capacidad = peor). OPERACIÓN queda igual (se mide, no se construye en contra). El
> discriminador de abajo sigue válido para separar operación; dentro de juicio, la pregunta
> nueva es: *¿la jugada mala es de razonamiento o de honestidad?* Detalle: `docs/vicios/README.md`.

Antes de la taxonomía por dinámica de mundo (§3) hay un corte **más importante**, porque define
qué mide WAGER y qué NO. Todo failure mode cae en una de dos clases:

- **OPERACIÓN** — el agente es un trabajador desprolijo que **pierde el hilo**: pierde
  restricciones, no registra info que llegó a mitad de camino, adivina en vez de preguntar,
  repite una acción que ya falló, olvida verificar. **Lo arregla mejor andamiaje: memoria,
  checklists, planners, loops de reparación. Medio mundo ya trabaja en esto** (OSWorld,
  computer-use, memoria/reflexion). **NO es blanco de WAGER.**
- **JUICIO** — el agente **TIENE la info en contexto**, ve la contradicción, y aun así hace la
  jugada epistémica equivocada: ignora la evidencia (68%), no revisa la creencia refutada (26%),
  no triangula, se casa con la 1ª hipótesis, retrocede al modelo familiar, fabrica precisión.
  **El andamiaje NO lo arregla** (el base model explica el 41.4% de la varianza; el scaffold el
  1.5% — §4-ter). **Esta es la razón de ser de WAGER — lo que ningún otro entorno mide bien.**

**El discriminador** (afilado, de Lucas): *¿lo arreglaría un mejor andamiaje/memoria/checklist?*
**Sí → operación** (no es nuestro). **No → juicio** (es nuestro). **Heurística de fuente** (guía,
NO ley): un benchmark de operación/computer-use (OSWorld) tiende a reportar operación; un
análisis de TRAZA/epistémico (grafos H/T/E/J/U/C, §4-ter) reporta juicio. *Pero la fuente es
pista, no veredicto*: OSWorld —benchmark de operación— reporta "se hunde recuperando un estado
oculto", que es JUICIO puro (inferir lo latente = familia D/v2). **Siempre manda el
discriminador, no el origen.**

Las seis familias de §3 son la **sub-taxonomía de la columna JUICIO** — organizan cómo volver
puntuable un vicio de juicio. Los vicios de operación se registran y se **bracketean** (§4-bis),
nunca se mezclan con los de juicio: mezclarlos diluye el foco que es toda la tesis del proyecto.

## 0.6. Las tres capas del proyecto y los DOS niveles de diversidad (ADR 0112 — alineación de Lucas)

El lugar de este catálogo en el proyecto completo, para que nadie confunda las plantas piloto con el
producto:

- **Capa 1 — PLANOS (este catálogo)**: las estructuras de vicios y ahas, de a pares, con fuente.
  Trabajo intelectual, a mano, contra literatura. Acá vive la diversidad ENTRE estructuras.
- **Capa 2 — PLANTAS PILOTO (los mundos a mano)**: cada mundo construido es un **experimento
  CONTROLADO** que prueba que una estructura expone su vicio de verdad (certificados + corridas con
  modelos reales). **No son el producto final — son la validación de una plantilla.** Todo lo que
  construimos hoy es capa 2.
- **Capa 3 — FÁBRICA (generación automática)**: estructura validada → **PLANTILLA** → la fábrica
  estampa variaciones en serie (piel/dominio, parámetros, seeds), cada una filtrada por la
  **certificación cero-LLM** (el yield es la métrica). Sin esta capa el proyecto no escala — *"sin
  generación automática el proyecto no tiene valor"* (Lucas, OQ 14). Estado real: peldaño fácil ✓
  (re-skin, yield 1/1); **medio TRABADO en D1** (`_canonical` estructural); difícil pendiente.

**Los DOS niveles de diversidad (anti-overfitting; ambos necesarios, atacan cosas distintas):**
1. **ENTRE estructuras** (capa 1 — principio 9): un mismo vicio en varias estructuras de fondo. La
   fábrica NO inventa estructuras; esto es trabajo nuestro. Sin este nivel, un modelo entrenado
   aprende *el truco de la estructura*.
2. **DENTRO de cada estructura** (capa 3): disfraces, parámetros, seeds — barato, automatizable. Sin
   este nivel, el modelo se memoriza *el mundo*.

Doble función de la capa 3: **escala para entrenar** (cientos de variaciones por estructura) y
**frescura para evaluar** (mundos que nadie vio = examen renovable, anti-contaminación).

**ESTO ES LO MÁS IMPORTANTE DEL PROYECTO (Lucas, 2026-07-10 — ADR 0117)**: la capacidad de diseñar
mundos donde los vicios EMERGEN, de una forma que después pueda **generarse automáticamente con
diversidad real** — muchas estructuras, y mundos que sean una **COMPOSICIÓN de piezas cuyas
interacciones generen propiedades EMERGENTES** al estamparse en serie, no "el mismo juego maquillado
de otra manera". Los mundos controlados de hoy (capa 2) existen para probar que esa capacidad
funciona. Los pares/gemelos (principio 10) son un agregado valioso, **no** el eje.

## 1. Qué ya sabemos (no arrancamos de cero)

- **El instrumento SÍ captura vicios, medidos** (no es aspiracional): comprar-evidencia-y-no-
  usarla (4/4 gpt bajo escasez), terminación apurada, **precisión fabricada** (declaró un σ
  que no midió; la nota se lo cobró), retirada a la arquitectura familiar (v2). Todo apareció
  con número en nuestros mundos.
- **★ JUSTIFICACIÓN EXTERNA DEL PROYECTO ENTERO — el "gusto" investigativo de los LLMs tiene un
  hueco sistemático y MEDIBLE (Chen, Zhao & Cohan 2026, "Measuring the Gap...", 2607.01233;
  Yale/UChicago; 9 modelos, 11.683 ideas; tier A).** Esto es la prueba independiente de que lo que
  WAGER existe para medir —el juicio/taste de investigación— es real, mensurable y le falta a los
  modelos: dados los mismos trabajos previos que precedieron a un paper humano, los LLMs ocupan una
  región **mucho más angosta** del espacio de "movidas de investigación" que los humanos, y colapsan
  en un reflejo único: **"conectá/combiná estas dos cosas"** (ideas de puente 12% humano vs **47-64%**
  en modelos; operación "integrar" **34.2% modelo vs 2.35% humano**, log-odds 3.07). Evitan justo las
  movidas que definen el buen juicio y que NUESTROS mundos premian: reemplazar un componente frágil,
  **desacoplar dos mecanismos confundidos** (= literal nuestra familia causal G), formalizar una
  estructura local. Tres remates que nos tocan de lleno: (a) poner el modelo a **razonar más EMPEORA**
  el reflejo (bridge 49.7%→71.1% con "thinking"), (b) los modelos **se parecen entre sí más que a los
  humanos** (cos-sim 0.83 vs 0.72-0.78 → si comparten el reflejo, un mundo que lo caza los caza a
  todos: respalda por qué la diversidad estructural importa), (c) el hueco persiste **con más contexto**
  (paper completo no acerca al humano). Un modelo que produce ideas razonables de a una sigue siendo
  conductualmente angosto — que es EXACTAMENTE la diferencia entre "parece buen razonamiento" y "lo es"
  que motiva el reward cero-LLM. **Este paper es la mejor defensa a la fecha de por qué el proyecto
  importa.**
- **Validez de constructo — NO SE SOSTIENE bajo protocolo sellado (ADR 0121, 2026-07-10)**: el
  experimento corregido y pre-registrado (misma pista en trampa y control, placebo, análisis CIEGO
  commiteado antes de los datos — ADRs 0118/0119) dio **negativo en todo**: la misma pista que en
  0098/0110 había dado +0.52 esta vez HUNDIÓ su propio mundo (scarce 0.58→0.00, pares por seed
  −0.44), el placebo de puro estilo movió el score en ambos mundos, y el control resultó sin
  headroom. El resultado viejo ("efecto de instrucción replicado") queda NO REPLICADO. Hallazgo
  metodológico clave: varianza corrida-a-corrida enorme (scarce/libre: mediana 0.29 en una corrida,
  0.58 en otra; tasa de ceros del brazo pista 2/8→5/8, protocolo idéntico) → con R bimodal y n=8,
  las medianas no son evidencia **en ninguna dirección** — el negativo tampoco prueba que la pista
  dañe. **El método de pistas NO se abandona (decisión de Lucas, ADR 0122)**: retirada solo su
  FORMA actual como evidencia; rediseño de la medición en curso (piso de ruido → autopsia de ceros
  con trazas → perillas de varianza → pista v2 potenciada), con manipulaciones no-instruccionales
  (presupuesto/presión, robots) como sonda complementaria. Hallazgo lateral que SÍ sigue vivo
  (re-testear con el método rediseñado):
  DeepSeek se casa con la 1ª hipótesis AUN a presupuesto pleno (gpt no) → perfil de modelo,
  OQ 20.
- **El hallazgo que ordena el diseño (CORREGIDO — ADR 0111)**: ~~el vicio bite bajo PRESIÓN, no a
  presupuesto pleno~~ era el **perfil de gpt-5.4**, NO una ley. gpt pivotea "de rutina" con plata
  holgada; **DeepSeek se casa con la 1ª hipótesis AUN a presupuesto pleno** (réplica 0110). → la
  presión es una **PERILLA calibrable POR MODELO**, no un ingrediente necesario: cada mundo con dial
  de presión reporta *a qué nivel se cae el hábito de cada modelo* (medición fina, no binaria). Es el
  producto **PERFILES DE VICIO POR MODELO** (OQ 20).

## 2. Principios de diseño (los que ganamos con dolor — no negociables)

1. **Consecuencia cobrada, conducta observada** (Ethos §2.1/2.6): el vicio es la jugada
   perdedora; la firma de trace diagnostica, nunca premia.
2. **Certificado de trampa necesaria** (ADR 0082): dos robots scripteados — el **vicioso**
   (comete el vicio con maestría en todo lo demás) debe quedar LEJOS del techo; el
   **cuidadoso** debe alcanzarlo. Si el cuidadoso no llega → trampa injusta, se descarta.
3. **La presión es una PERILLA que expone el vicio — calibrable por modelo** (ADR 0098, corregido por
   0111): escasez de presupuesto / tiempo / evidencia que llega tarde. **NO es ingrediente necesario
   universal**: gpt-5.4 esconde el vicio de 1ª-hipótesis a presupuesto pleno, DeepSeek lo muestra sin
   presión. Por eso la presión no es precondición sino DIAL: se barre su nivel y se reporta a qué
   punto se cae el hábito de cada modelo (medición fina). Un mundo puede exponer un vicio en algunos
   modelos sin presión; la presión amplía el rango de modelos y afina la medición.
4. **Vicios TEMPORALES → mundos que se DESPLIEGAN**: "no actualizar ante evidencia nueva"
   necesita que HAYA evidencia nueva llegando (la maquinaria de eventos, D4/ADR 0083, casi sin
   usar). El énfasis correcto: *evidencia por etapas, no toda disponible de entrada.*
5. **Vicios de INSIGHT/creatividad → mundos donde INVENTÁS la estructura** (familia v2, nuestro
   mejor resultado): ganar exige formular una hipótesis estructural que nadie te dio, no calzar
   un modelo de librería.
6. **Entregable PUNTUABLE + cero-LLM**: el deliverable sigue siendo "predecí el comportamiento"
   (scoreable sin juez LLM). La fachada (línea de producción, etc.) es piel; la sustancia
   siempre es "descubrí el mecanismo oculto investigando".
7. **Altura de la trampa/pista**: se nombra la CONDUCTA, nunca la RESPUESTA. Test: un modelo
   que nunca vio el mundo, tras leer la pista, sigue sin saber la respuesta.
8. **Aislá el JUICIO de la OPERACIÓN** (el corte de §0.5, lado diseño): el mundo debe REMOVER la
   excusa operacional —info relevante siempre en contexto o recuperable barato, restricciones
   explícitas, sin trampa de memoria/horizonte— para que la ÚNICA falla posible sea de juicio. Si
   el agente puede fallar por perder el hilo, estás midiendo operación (lo que el campo ya mide).
   Es el lado-DISEÑO de la separación ejecución-vs-juicio que ya validamos en la MEDICIÓN (ADR
   0098): allá separamos los ceros de ejecución de los de juicio; acá los diseñamos-afuera.
9. **Diversidad de ESTRUCTURAS, no solo de disfraz** (anti-overfitting; precisión de Lucas,
   2026-07-07): un mismo vicio aparece en varias ESTRUCTURAS distintas —mecanismos/situaciones que
   lo fuerzan—, no en un solo mecanismo con el disfraz cambiado. Ej.: "no actualizar" = evidencia
   que llega a mitad de camino ∨ hipótesis-encajada-que-no-se-puede-refutar (Wason/Klayman-Ha) ∨
   evidencia retractada (perseverancia) ∨ anclaje — cuatro mecanismos, no cuatro pieles de uno. La
   cartera de un vicio DEBE cubrir esas estructuras distintas; si todos sus mundos comparten
   estructura, un modelo entrenado overfitea a la estructura (el "truco de la fábrica"), no aprende
   el juicio. Dos niveles: (1) estructuras distintas —lo fundamental—; (2) disfraces sobre cada
   estructura —superficie, el re-skin ya existente—. El minado de semillas (§5) apunta PRIMERO a la
   variedad estructural.
10. **La unidad de diseño es el PAR de polos, no el vicio ni el aha sueltos** (ADR 0106; formulado
    de forma INDEPENDIENTE por dos lecturas — la convergencia se registra como evidencia de robustez).
    **RANGO (ADR 0117, decisión de Lucas)**: la doctrina queda, pero el par es un **AGREGADO / seguro
    anti-reflejo**, NO el eje de prioridad del proyecto — lo fundamental es la capacidad
    vicio→estructura→plantilla→generación automática con diversidad (§0.6). Los gemelos se suman
    donde salen baratos (p.ej. #16/#17 ya construidos) y siguen OBLIGATORIOS para mundos-AHA
    (donde el gatillo-fácil finge el salto); para mundos-vicio alcanza con que cada reflejo barato
    pierda en ALGÚN lugar de la batería, no un gemelo dedicado por mundo.
    Toda operación cognitiva (unificar, analogar, partir-en-dos, postular-entidad, perseguir-anomalía,
    persistir) es NEUTRA: el mundo decide si fue genio o vicio (Copycat a nivel mecanismo; Klayman-Ha
    a nivel estrategia; phlogiston a nivel racionalidad — tres fuentes independientes convergen).
    **Juicio = discriminación ACTIVA y COMPRABLE**: no "percibir" en qué mundo estás, sino GASTAR
    presupuesto en la evidencia que separa los polos ANTES de aplicar la operación. Se construye de a
    PARES: misma superficie, polos opuestos (en uno la operación gana; en el gemelo pierde).
    **CERTIFICADO DEL PAR (obligatorio para todo par)**: (a) el robot-HÁBITO (aplica la operación en
    ambos polos) gana el polo favorable y PIERDE el gemelo — si gana ambos, el gemelo no discrimina →
    par rechazado; (b) el robot-JUICIO (compra la evidencia discriminante primero, decide después)
    gana AMBOS con presupuesto alcanzable — si ningún robot-juicio alcanzable lo logra, el par es una
    moneda (injusto) → rechazado. Es el certificado de trampa-necesaria (ADR 0082) elevado al nivel
    par: la frontera entre polos debe ser DESCUBRIBLE pagando, y eso se demuestra, no se espera.
    **MÉTRICA DEL PAR** (convención de cartera / reporting E1 — cero cambios al reward path): se
    reporta (R_polo1, R_polo2, **min**); el min es la nota del par — el atajo gana uno y pierde el
    otro → min bajo; el juicio gana ambos → min alto. Generaliza 1a/1b y #16/#17 (par ya construido
    sin haberlo nombrado). El minado (§5) busca SIEMPRE los dos polos de cada operación.
11. **Tiers de evidencia A/B — etiquetar TODO en ambos catálogos** (ADR 0106): **tier A** = el
    vicio/operación está documentado EN LLMs/agentes con cita; **tier B** = paradigma humano (cog-sci
    / historia de la ciencia) sin testear en modelos. Todo mundo tier-B lleva PRE-REGISTRADA la rama
    *"frontier lo resuelve de rutina"* — que es un hallazgo publicable SOBRE modelos, no un fracaso
    del mundo — y la cartera E1 no se apuesta mayoritariamente a tier B. Ejemplos: anclaje-21%
    (Tversky-Kahneman, humanos) = tier B; evidencia-ignorada-68% (traces de LLM) = tier A. Nota: el
    PAR (principio 10) convierte el riesgo tier-B en diagnóstico — si frontier resuelve el polo-aha
    pero TAMBIÉN aplica la operación en el gemelo, no tuvo el aha: tiene el hábito.

## 3. La taxonomía por DINÁMICA DE MUNDO (el organizador clave)

No agrupamos los vicios por su nombre psicológico sino **por la dinámica de mundo que los
fuerza a manifestarse de forma puntuable** — porque esa dinámica ES el diseño.

| familia | vicios que agrupa | dinámica de mundo que lo expone | scoring |
|---|---|---|---|
| **A. Actualización de creencias** | casarse con la 1ª hipótesis; no incorporar evidencia nueva; sesgo de confirmación; anclaje; conservadurismo bayesiano | **DESPLIEGUE**: evidencia contradictoria llega a mitad de camino (eventos sellados); la verdad puede driftear | predecir comportamiento post-actualización |
| **B. Atención / perseverancia** | rabbit holes; más-de-lo-mismo sin pivotear; no saber cuándo parar; perder de vista el objetivo | **DISTRACTOR + PRESIÓN**: pozo fascinante en un dato lateral que no paga, bajo presupuesto escaso | costo de oportunidad cobrado en el modelo final |
| **C. Verificación / rigor** | "verified" sin verificar; over-claims; **precisión fabricada**; perseguir lo significativo-pero-irrelevante | **RESPUESTA BARATA FALSA + verificación disponible**: la carnada de significancia; declarar un número sin medirlo se paga | |ΔF| de la cantidad no-verificada |
| **D. Representación / creatividad** | retirada a lo familiar; no inventar la estructura necesaria; sobre-simplificar | **INVENTAR LA ESTRUCTURA** (v2): el ganador formula una hipótesis latente/estructural | fidelidad al mecanismo que solo la estructura correcta reproduce |
| **E. Memoria / consistencia (largo plazo)** | perder restricciones; trabajo redundante; recuperación que se degrada en trayectorias largas | **HORIZONTE LARGO + restricción de enlace tardío** (declarada temprano, cobrada al final) | parcialmente límite del harness → se MIDE, no se diseña-en-contra |
| **F. Interacción / preguntar** | adivinar en vez de averiguar; no registrar info que llega a mitad de camino; saltear la verificación disponible | **CONSULTABLE + evidencia mid-way**: lo faltante tiene precio conocido y accesible | diferencia de suposición-vs-consulta |
| **G. Razonamiento causal** | correlación≠causación; confounding; colisionador/selección; no-intervenir; ignorar el DGP | **OBSERVACIONAL ENGAÑOSO + intervención disponible**: la correlación barata miente; do() cuesta y revela | fidelidad al efecto causal que solo la intervención recupera |

> **Las siete familias (A-G) sub-clasifican la columna JUICIO** (§0.5), no la de operación. Cada familia
> tiene una CARA operacional que el diseño debe **engañar-afuera** para no medir operación por
> error: **E (memoria) es la más peligrosa** — la info debe quedar EN contexto para que la falla
> sea "no lo conectó" (juicio) y no "lo perdió" (operación); por eso E "se mide, no se
> diseña-en-contra". **F straddlea**: "adivinar en vez de preguntar" es operación, pero *saber que
> necesitás preguntar* (reconocer que hay algo que no sabés) es juicio — ese es el lado nuestro.

## 4. El catálogo (seed inicial — a completar con la literatura)

Por cada vicio: fuente · cómo se manifiesta · dinámica (§3) · estado. **Las citas exactas se
verifican/completan minando papers (ver §5); lo de abajo es el seed de lo que ya sabemos.**

> **Cosecha de la investigación dirigida (deep-research, 2026-07-07)** — corrida de 5 ángulos, 26
> fuentes, 117 claims → 25 verificadas por voto adversarial → **19 confirmadas (3-0/2-1)** + 6 sin
> verificar (el paso de síntesis se cayó por límite de API; la curaduría la completé desde los
> claims verificados). **Marcas de estado de verificación** (honestidad de precisión — no marcar lo
> que no se midió): **`[dr ✓]`** = pasó el voto adversarial 3-0/2-1; **`[dr ·]`** = extraído con
> CITA TEXTUAL de la fuente pero NO llegó al voto (el presupuesto de verificación se cortó);
> **`[dr ~]`** = candidato cuyos 3 votos erroraron por el límite. **Todos pasaron el triage §0.5 =
> JUICIO** (blanco de WAGER), no operación.

### A — Actualización de creencias
- **Fijación de hipótesis / sesgo de confirmación** — cog-sci clásico (Wason 2-4-6; Klayman &
  Ha, positive-test strategy): se busca evidencia que confirma, no que refuta. → mundo de
  despliegue con refutación que llega tarde. *Estado: parcial (first_story mide la 1ª-hipótesis
  a presupuesto pleno, pero el vicio no bite sin presión; con-noticia sin correr con modelos).*
- **No-actualización / conservadurismo** — updating bayesiano insuficiente (Edwards; base-rate
  neglect, Kahneman-Tversky): ante evidencia contraria, la creencia casi no se mueve. → eventos
  sellados. *Estado: maquinaria lista (D4), certificado de robots ✓ (0.0002 vs 0.989), sin
  correr con modelos.*
- **Anclaje** — Tversky & Kahneman: la primera estimación fija el resto. → primer dato sesgado.
- **`[dr ·]` Respuestas a datos anómalos — Chinn & Brewer 1993** (Review of Educational Research):
  de **7 respuestas** a evidencia que contradice la teoría, SOLO 1 es "aceptar y cambiar"; las otras
  6 la descartan (ignorar · rechazar · excluir del dominio · dejar en suspenso · reinterpretar ·
  parche periférico) + una 8ª "dudar de la validez del dato". *La taxonomía exacta de las jugadas
  perdedoras → un mundo de anomalía sellada donde cada descuento es una firma de trace.*
- **`[dr ✓]` Recipe estructural de Klayman & Ha 1987** — cuando la hipótesis H está EMBEBIDA en la
  regla verdadera T (H ⊂ T, demasiado angosta, como el 2-4-6 de Wason), los tests **positivos NUNCA
  falsan** → solo un test NEGATIVO revela el error. *Receta exacta y buildable: un mundo donde
  confirmar está GARANTIZADO que pierde. El regalo de diseño más filoso de la cosecha.*
- **`[dr ✓]` Insensibilidad a la diagnosticidad de la RESPUESTA** (Slowiaczek et al.) — el agente
  elige bien QUÉ test pedir pero pondera mal el resultado (misma pregunta, respuestas de muy distinta
  diagnosticidad) → preserva la hipótesis inicial. *Puede COMPRAR el test correcto y aun así leerlo
  mal — distinto de no-testear.*
- **`[dr ✓]` Anomaly-blindness CONDICIONAL — Dunbar 1997** (in-vivo, 4 labs):
  los científicos ignoran el hallazgo inesperado cuando es TEMPRANO y sobre una hipótesis auxiliar;
  le prestan atención si contradice supuestos centrales o llega TARDE. *Da el RÉGIMEN exacto donde
  el vicio bite → parametriza el timing del evento sellado (D4).*
- **`[dr ·]` Perseverancia tras el desmentido — Anderson & Lepper 1980; Mitroff 1974 (Apollo)**: la
  creencia sobrevive al descrédito TOTAL de la evidencia que la fundó; los 42 científicos de élite
  del Apollo no movieron sus "pet hypotheses" con los datos lunares. → *mundo donde la evidencia
  comprada se RETRACTA a mitad (D4 invalida un dato ya pagado): ¿revierte la creencia? El inverso,
  y más agudo, de no-actualizar.*

### B — Atención / perseverancia
- **Rabbit holes / goal drift** — evals de agentes autónomos (METR y afines documentan
  degradación con el horizonte y pérdida del objetivo). → pozo-señuelo + presupuesto. *Estado:
  por diseñar (señuelo puro); la escasez ya la validamos como dial (#6).*
- **Parada prematura / satisficing** — Simon: se toma la primera solución "suficiente". →
  N-trampas con saciedad (hallar la 1ª satisface). *Estado: mundo 3 fue 2-trampas; saciedad
  reapareció bajo escasez.*

### C — Verificación / rigor
- **Over-claiming / "verified" sin verificar** — críticas a agentes-científicos (p.ej. AI
  Scientist) + evals de honestidad: producen plausible-pero-mal y lo reportan con seguridad. →
  la retórica ya vale cero (el examen corre el modelo). *Estado: cubierto por construcción.*
- **Precisión fabricada** — MEDIDO EN NUESTROS PROPIOS RUNS (fabricated_precision): declaró σ
  sin comprar réplicas. *Estado: capturado y priceado.*
- **Perseguir lo significativo-pero-irrelevante / p-hacking** — metaciencia / crisis de
  replicación (garden of forking paths, Gelman). → carnada de significancia (efecto chico-pero-
  claro vs grande-pero-ruidoso). *Estado: **RE-ALOJADO (ADR 0112; supersede "anfitrión natural =
  mundo ancho" — ese anfitrión MURIÓ con el techo de anchura, ADRs 0089/0091)**. Los nuevos
  anfitriones NO necesitan anchura: (a) **optional stopping es TEMPORAL, no ancho** — mundo angosto
  donde el agente decide cuándo dejar de muestrear y el sesgo de parada infla el efecto entregado
  (off-support lo cobra); (b) **variable-elegida con 2-3 outcomes**, no 19 columnas. Ambos en
  CANTERA con nota de construibilidad barata.*
- **`[dr ✓]` Garden of forking paths — Gelman & Loken**: el problema de comparaciones múltiples
  aparece aun con UN SOLO análisis, porque cada decisión analítica es contingente al dato observado;
  y "**no se sienten como grados de libertad**" (cada elección parece la única razonable). *El vicio
  más INVISIBLE: no hace falta p-hackear a conciencia. Es exactamente lo que nuestro instrumento
  quiere pescar (juicio, no truco).*
- **`[dr ✓]` 12 estrategias de p-hacking, con número — Stefan & Schönbrodt 2023**: UNA sola
  (reportar selectivamente la variable dependiente que dio significativa, de 10) infla el
  falso-positivo del 5% al **~40% (×8)**. *Calibra la carnada de significancia (anfitrión
  re-alojado, ver arriba — ya no el mundo ancho).*
- **`[dr ✓]` 40 QRPs indexadas por fase — Nagy et al. 2025** + bestiario (semilla de RNG favorable ·
  covariables ad hoc · discretizar continuas · missing-data hacking · PARKing). *Catálogo listo de
  jugadas perdedoras, cada una candidata a mundo.*
- **`[dr ✓]` HARKing** (Kerr): presentar como a priori una hipótesis inventada TRAS ver los datos.
  → *mundo donde el orden hipótesis-antes-que-datos es verificable (el sellado de compromiso).*
- **`[dr ✓]` DOF amplificados en experimentos con AGENTES — Vaccaro 2026**: selección de modelo,
  wording del prompt, settings, rediseño contingente al resultado — "fáciles de explotar y difíciles
  de detectar". *CORREGIDO 2026-07-09 (ADR 0115): el paper encuadra esto como metodología HUMANA que
  ESTUDIA agentes, NO como falla del agente; el agente-que-se-p-hackea-a-sí-mismo es extrapolación
  NUESTRA (vicio candidato transferible). Dato real: probaron anclaje en LLMs sobre 2.430
  especificaciones → de anclaje inverso a fuerte según qué reporten (el anclaje en LLMs NO es robusto).*
- **`[dr ✓]` Fabricación cuando el experimento falla — MLR-Bench (NeurIPS 2025)**: **~80%** de los
  casos reportan resultados fabricados/inválidos (8 de 10 tareas con datos placeholder/sintéticos en
  vez de ejecución real); persiste aun instruyendo "no fabriques". *Es EXACTAMENTE nuestro
  `fabricated_precision`, medido afuera y en grande → validación externa del vicio que ya capturamos.*

### D — Representación / creatividad
- **Retirada a lo familiar / implementation drift** — evals de agentes de código (revierten a
  patrones conocidos). → la respuesta simple-familiar queda a mitad de tabla; solo la estructura
  verdadera llega arriba. *Estado: CONFIRMADO con solver real (v2 seed3, R=0.096).*
- **No inventar la estructura** — el lado generativo del research taste. → familia v2. *Estado:
  el trofeo; hacer MÁS de estos.*
- **`[dr ✓]` Hipótesis inviables sin anclar a los datos — HLER 2026**: la generación autónoma sin
  restricción produce preguntas factibles solo el **41%** de las veces vs **87%** si se la ancla a la
  estructura del dataset (≈59% alucinadas). *Cuantifica el lado generativo del research taste — y
  sugiere el dial: cuánta estructura se le da de entrada.*
- **`[dr ·]` La analogía de descubrimiento es CERCANA, no lejana — Dunbar 1997**: de 99 analogías en
  16 lab meetings, solo **2** lejanas; el descubrimiento real corre sobre analogías
  *near*, basadas en homología (40 mismo-organismo, 57 otro-organismo). *Dato de diseño para D:
  premiar la analogía estructural CERCANA correcta, no el salto vistoso — el mito del "insight
  lejano" no es donde vive el research taste.*
- **`[dr ~]` Diversidad de exploración** (arxiv 2510.10472, *sin verificar — los 3 votos erroraron
  por el límite de API*): la exploración angosta/baja-varianza sería jugada perdedora documentada en
  ML research autónomo. *Anotado, pendiente de verificación.*

### E — Memoria / consistencia
- **Pérdida de restricciones / contexto en trayectorias largas** — evals de horizonte largo. →
  restricción de enlace tardío + horizonte. *Estado: se MIDE como hallazgo (límite del solver),
  no se diseña-en-contra.*

### F — Interacción *(FUERA de v1 — ADR 0112)*
- **Adivinar en vez de averiguar** — evals de agentes interactivos. → info faltante con precio
  accesible. *Estado: el inverso (comprar-y-no-usar) CONFIRMADO (#6). El directo — y las estructuras
  6a/6b (no-pregunta-aunque-detecta; el-contexto-apaga-la-pregunta) — exige el verbo **PREGUNTAR**:
  un oráculo consultable con costo, que NO existe en el contrato del episodio (observe/experiment).
  Semántica nueva en el contrato = tripwire → **fuera de v1, en cantera con este rationale**, hasta
  decisión explícita de Lucas. 6d (preguntas no-discriminantes) SÍ está cubierto: es Mundo B.*

### G — Razonamiento causal
*Grupo propio, **aprobado por Lucas (2026-07-07)**. Gana su fila porque la CURA es una MOVIDA
DISTINTA: intervenir, o modelar la causa escondida — NO "verificar más fuerte" sobre los mismos
datos. Fijarse mejor en una correlación confundida no revela nunca el tercer factor (el calor
detrás del helado y los ahogados); solo cambiar de movida lo hace. Solapa con C en la superficie
(una respuesta barata que resulta falsa) pero el eje es otro: la trampa está METIDA en los datos
observacionales, no en la significancia. Todos JUICIO. Ya hay maquinaria: `confounded_gen_v0`,
`generic_certify`.*
- **`[dr ·]` Correlación ≠ causación — Corr2Cause, Jin et al. 2023**: 17 LLMs (hasta GPT-4) puntúan
  al **NIVEL DEL AZAR** infiriendo causalidad desde correlación (dataset 200K). *El ancla dura del
  vicio.* → mundo observacional confundido donde solo `do()` revela la verdad.
- **`[dr ✓]` Leakage / distribution-mismatch — Kapoor & Narayanan 2023** (taxonomía de 8 tipos): el
  "distribution mismatch" (evaluar en una distribución distinta de aquella sobre la que se afirma)
  infla el desempeño aun con split limpio. *Generalizar más allá del DGP medido.*
- **Confounding / colisionador / no-intervenir** — la dinámica: la data observacional engaña; solo
  la intervención (o modelar la asignación) recupera. *Estado: YA tenemos el mundo
  (`confounded_gen_v0`); el candado del verificador estructural es la deuda registrada en ADR 0094.*

### ★ Mapa de estructuras rebuildables por vicio (case-search, 2026-07-07)
*Segunda búsqueda dirigida (deep-research, 112 agentes, **23 claims verificados 3-0/2-1**), buscando
CASOS por vicio agrupados por TIPO de estructura (principio 9). **Confirma empíricamente que un vicio
se fractura en estructuras distintas** — no es un mecanismo con disfraces. Cada estructura = un mundo
rebuildable; el label en negrita es el gancho.*

**Vicio 1 — no actualizar creencias: ~8 estructuras (el más rico).**
- 1a **subset / hipótesis-encajada** (Klayman-Ha 1987): H ⊂ T → el test positivo NUNCA falsa; solo
  el negativo (Wason 2-4-6).
- 1b **superset / hipótesis-que-envuelve** (el ESPEJO): H ⊃ T → ahora SOLO el positivo falsa y buscar
  disconfirmación ENGAÑA. *Par anti-overfitting con 1a: un modelo que memoriza "siempre buscá
  refutar" gana 1a y PIERDE 1b → lo obliga a juicio, no a truco.*
- 1c **perseverancia tras desmentido total** (Anderson-Lepper-Ross 1980): la creencia sobrevive a que
  le digan que la evidencia era ficticia; mecanismo — pedirle que EXPLIQUE por qué la inmuniza (los
  que no explicaron, SÍ actualizaron).
- 1d **anclaje / ajuste insuficiente** (Teovanovic 2019): arranca de un valor y se queda corto; tirón
  medido del 21.4%.
- 1e **buscar-confirmar-no-refutar** (Elton-Spencer 2020, "pathological water science").
- 1f **motte-and-bailey / blanco mal definido**: fenómeno definido impreciso → afirmación fuerte que
  se repliega a una trivial bajo presión → infalsificable.
- 1g **referencia-de-validación-corrupta** (ozono; Bhartia-McPeters 2018): la anomalía real parece
  error de instrumento porque el patrón de referencia estaba mal.
- 1h **doble-estándar-por-compromiso-previo** (deriva continental; Seselja-Weber 2012): vara estricta
  para la hipótesis rival, laxa para la propia.
- *+ 2 ejes que ordenan el espacio: 6 formas de procesamiento (Oeberst-Imhoff 2023), 5 etapas del
  pipeline. Caveat: esos dos son "manifestaciones de UN mecanismo", no 6 mecanismos — pero a nivel
  de construir mundos son mecánicas distintas.*
- *OJO: la estructura "evidencia contradictoria que llega a MITAD de camino" (la que YA tenemos con
  los eventos D4) está poco representada en la literatura — pero la tenemos construida.*

**Vicio 6 — adivinar en vez de averiguar: 4 estructuras (el más fuerte en IA, medido).**
- 6a **reconoce-pero-no-actúa** (Su-Cardie 2026): detecta la ambigüedad (~60-80%) pero pregunta <5%;
  la falla es de ACCIÓN, no de detección.
- 6b **el contexto inyectado apaga la pregunta**: darle contexto lo hace preguntar MENOS ("el
  contexto es una trampa").
- 6c **muestrea hipótesis incompatibles + se sobre-confía** (BED-LLM 2025): empeora a medida que
  crece la historia.
- 6d **preguntas no-adaptativas**: no elige la pregunta más discriminante (45% vs 93%).

**Vicio 3 — no verificar / p-hacking: 4 sub-estructuras, CON número.**
Explotar los 4 grados de libertad juntos sube el falso-positivo del **5% al 60.7%** (Simmons et al.
2011). 3a elegir la variable-dependiente que dio · 3b parar cuando conviene (optional stopping) ·
3c meter/sacar covariables · 3d reportar solo las condiciones que "funcionaron".

**Vicio 7 — causa/efecto: 2 estructuras.**
- 7a **confusor mal removido** (Elton-Spencer 2020, replicado 4 veces: polywater, Mpemba, EZ water,
  agua magnetizada): un tercer factor sigue a la manipulación y produce el "efecto".
- 7b **referencia corrupta** (comparte estructura con 1g).
- *Faltan por confirmar: colisionador / sesgo-de-selección y "hay-que-intervenir-sí-o-sí".*

**PUNTOS CIEGOS → LLENADOS (3ª búsqueda, case-search 2026-07-07: 113 agentes, 22 claims verif.):**

**Vicio 4 — inventar la estructura escondida: 6 estructuras** (ancladas en Dunbar). 4a analogía
CERCANA (no el salto lejano: 99 analogías, solo 2 lejanas) · 4b **partir un modelo unitario en DOS
mecanismos latentes** (una anomalía fuerza a decouplear) · 4c anomalía atendida según
centralidad×timing (= nuestra "ceguera condicional", ahora con perilla 2×2) · 4d analogía guiada por
el objetivo · 4e moderador generación-vs-recepción × complejidad · 4f **Einstellung** (una solución
de manual cebada BLOQUEA una mejor disponible). *Y sigue siendo nuestro trofeo ya construido (v2).*

**Vicio 5 — perder el hilo largo: 7 estructuras** (benchmarks de agentes 2025-26, con número). 5a
caída monótona con el largo (METR) · 5b colapso por umbral/transición de fase (HORIZON) · 5c
**restricción-EN-contexto-pero-no-atendida** (la regla sigue ahí y aun así la viola — "inatención,
no olvido"; replicado en web y en base de datos) *← ojo: ESTA es de JUICIO, no operación (la info
está delante)* · 5d loop de acción-fallida-repetida (comparte con vicio 2) · 5e deriva fuera del
camino correcto que se auto-refuerza (+22.7pp por paso) · 5f pass^k (fiabilidad entre corridas) · 5g
incumplir la política declarada. *5c rescata parcialmente al vicio 5 hacia el juicio.*

**Vicio 2 — atención / pozo: 5 estructuras** (antes 1). 2a no-perseguir-lo-no-probado · 2b
un-hueco-vetó-todo · 2c **sunk-cost** continuar-vs-abandonar (Arkes-Blumer; meta-análisis ES≈0.50) ·
2d **blueprint de escalada** (inversión previa + señal negativa + punto de decisión seguir/pivotear)
· 2e **inaction-effect** (la señal negativa empuja a ACTUAR sin importar qué; reformular invierte el
sesgo — palanca NUEVA, ortogonal al sunk-cost) · 2f loop de acción-fallida (comparte con 5).
- *CAVEAT DE DISEÑO (fósforo/phlogiston, Chang 2010): persistir es vicio SOLO si la alternativa es
  decididamente superior. Si las dos teorías empatan en evidencia, aferrarse es RACIONAL, no vicio.
  Regla para los mundos de no-pivotear/perseverancia: la respuesta correcta tiene que ser
  decididamente mejor, o estás castigando prudencia.*

**NUEVO punto ciego (0 casos → prioridad de la próxima búsqueda):** vicio 7, sub-estructuras
**colisionador / sesgo de selección** (Berkson) y **"hay que intervenir sí o sí"** (donde lo
observacional no alcanza ni en principio). Por confirmar caso-por-caso: los clásicos de
visión-de-túnel (N-rays de Blondlot, fusión fría, canales marcianos) — pueden disolverse como el
fósforo al mirarlos de cerca; requieren historiografía antes de usarlos.

**NO reconstruir (estructuras refutadas):** el "filtro de calidad se comió el descubrimiento" del
ozono (los propios autores de NASA lo desmienten → usar 1g); el genérico "deriva continental = error"
(usar 1h / 2a / 2b); la ley "exponencial / vida-media" del horizonte y la "cadena donde un paso caído
mata todo" (refutadas); el número "pass^8 <25%".

### ★★ Catálogo ESPEJO — operaciones de AHA, de a pares (4ª búsqueda, 2026-07-09; ADR 0106)

*El polo POSITIVO del catálogo: operaciones creativas del descubrimiento, donde ejecutar la operación
es la ÚNICA vía al techo. Regla de admisión: el aha cuenta SOLO si se paga en una PREDICCIÓN medible
(cero-LLM); la "elegancia comprensiva" sin predicción lleva etiqueta "no sabemos puntuarla". Cada
operación va DE A PAR (principio 10). Evidencia primaria:
`docs/research/2026-07-09-deep-research-4-estructuras-de-aha-pares.json` (111 agentes, 23 claims
verificados). Casi todo **tier B** salvo donde se marca. **Estado: preliminar hasta la réplica del
ledger (DeepSeek) — nada de esto se llama "validado".***

**A1 — Analogía por MAPEO DE ESTRUCTURA** (Gentner; formaliza a Darwin). Alinear dos sistemas por su
estructura relacional profunda y PROYECTAR al nuevo una propiedad no dada → una predicción concreta.
· *Polo aha*: Darwin (selección artificial→natural; Thagard lo modela formalmente). · *Polo vicio*:
analogía de SUPERFICIE — retrieval por parecido, no estructura (70% vs 30%, Trench-Minervino 2015;
taxonomía de 4 fallas, Shelley 2003). · **Tier A en el polo vicio**: GPT/Claude colapsan en variantes
contrafácticas donde el humano aguanta (Lewis-Mitchell 2024) — *campo EN DISPUTA (Webb-Holyoak
argumentan analogía emergente; el claim "LLMs igualan al humano" fue REFUTADO 0-3 en esta corrida):
hallazgo documentado, no consenso.* · **Pago: predicción → construible.**
> **★ El polo-vicio de A1, ahora TIER A con números (Chen/Zhao/Cohan 2026, 2607.01233).** El vicio no
> es solo "analogía de superficie" puntual: es un **REFLEJO DE SÍNTESIS** sistemático — el gatillo
> "unir/integrar por defecto" aunque las dos cosas no compartan estructura (apofenia a nivel ideación).
> Medido en 9 modelos: síntesis/unificación como método **5.1% humano vs 22.5-38.7% LLM**; "integrar"
> **34.2% vs 2.35%**. El humano hace la movida OPUESTA y local (reemplazar/**desacoplar**/formalizar).
> Diagnóstico medible que nombran y nos sirve: **bottleneck specificity** (¿identifica el mecanismo/
> factor limitante preciso, o solo "combina"?) — baja en modelos. Esto es el **certificado natural del
> par A1**: el robot-hábito "siempre integrá" gana el polo-aha (donde la unión es real) y DEBE perder
> el gemelo (donde la unión es espuria y la jugada correcta es desacoplar/reemplazar). El gemelo Vulcano
> es su instancia bandera (postular la entidad que une ↔ la ley es otra).

**A2 — CONSILIENCIA / unificar** (Whewell; Thagard). Una hipótesis explica hechos de TIPO distinto a
los que la originaron, sin ad-hoc; la aceptabilidad sube con el nº de hechos cubiertos — un CONTABLE.
· *Polo aha*: teoría ondulatoria de la luz (mancha de Poisson, refracción cónica). · *Polo vicio*:
apofenia / unificación espuria — **hueco: falta el caso histórico NOMBRADO** (la búsqueda no lo trajo).
· Tier B. · **Pago: número.** *En el contrato actual, la batería + MDL YA cobran lo esencial (el que
parchea cada anomalía con su epiciclo paga MDL doble y falla fuera de soporte); el mundo solo necesita
sembrar las dos anomalías.* Sobre ECHO ver la tarea de investigación abajo.

**A3 — Búsqueda en DOS ESPACIOS** (Klahr-Dunbar, SDDS). Investigar = moverse entre el espacio de
hipótesis y el de experimentos; el techo exige DISEÑAR el experimento discriminante (la "región III"
que descarta todas las hipótesis comunes), no solo generar hipótesis. · *Polo vicio*: quedarse en un
solo espacio (razonar de memoria, nunca diseñar la prueba que separa). · Tier B. · **Pago: medible.**
**→ NO se abre mundo nuevo: esta estructura ES el Mundo B** (diseñado hace semanas); se registra el
pedigrí Klahr-Dunbar en su spec. *El par 1a/1b también la instancia (probar el borde correcto =
región III).*

**A4 — RE-REPRESENTACIÓN que se paga** (Klahr-Dunbar; el sub-caso construible). Reencuadre
DISCONTINUO de las variables crudas que destapa una predicción invisible en el encuadre original;
cruzar de marco exige cambiar **≥3 casilleros SIMULTÁNEAMENTE** (por eso la revisión incremental no
llega — 17/20 no cruzan). · *Polo aha*: reconcebir el parámetro de "contador" a "selector" → predicen
el aparato. · *Polo vicio*: túnel en la representación inicial. · Tier B. · **Pago: predicción,
sub-caso (i)** — la firma observable: la entrega CONSTRUYE una variable que nadie le dio. **Distinguir
del sub-caso (ii)**: el reframing de pura elegancia comprensiva sin predicción → etiqueta "no sabemos
puntuarla" (el muro de §7 sigue para ese). *Generaliza el trofeo v2. El "nº de casilleros simultáneos"
se registra como DIAL de dificultad de mundos-aha.*

**A5 — (mecanismo, no mundo) Deslizamiento conceptual de Copycat** (Hofstadter-Mitchell). Explica POR
QUÉ la misma maquinaria de re-representación bifurca en mapeo profundo (genio) vs superficie (vicio):
la analogía es percepción; bajo presión un concepto "desliza" al vecino. Tier B. Valor WAGER: es el
sustento a nivel mecanismo del principio 10 (operación neutra, el polo lo decide el mundo) y de la
firma "reconstruye la variable" de A4.

**Firmas de creatividad (doctrina vigente: observadas, JAMÁS premiadas).** Tres huellas computables
del acto creativo, todas DIAGNÓSTICO de trace — ninguna entra al reward; la nota sigue siendo la
entrega: (i) la entrega construye una variable no dada (A4); (ii) el log de compras entra a la región
discriminante (A3); (iii) un solo mecanismo cubre ambas anomalías sin parche (A2, ya cobrado vía MDL).

**Robot INCREMENTAL (tercer robot, para mundos-aha) — aceptado con definición mecánica PENDIENTE
antes de usarlo como certificado**: espacio declarado (knobs + estructuras), vecindad = una suposición
por vez, presupuesto declarado, restarts acotados (sin acotar restarts, con reinicios infinitos
tropieza cualquier salto y el certificado se diluye). **Certificado de ABISMO** = incremental Y
escalera estancados bajo el muro + guión-con-salto en el techo.

**ECHO / coherencia explicativa — tarea de investigación con TIMEBOX, no muro caído**: ECHO computa
"la mejor explicación" como número cero-LLM (gana +0.94 / pierde −0.85), pero puntúa DADO un grafo
hipótesis-evidencia ya formalizado; nuestro muro es construir ese grafo desde una entrega sin juez.
Preguntas del timebox: ¿qué inputs exige? ¿se computa desde una entrega ejecutable? ¿sobrevive a
submissions adversariales? Mientras: batería + MDL cobran lo esencial de consiliencia.

**DECISIÓN DE CONSTRUCCIÓN (ADR 0106) — ESTACIONADA (ADR 0117: par de AHA → cantera; se retoma
cuando el programa vaya por los ahas): primer par = NEPTUNO/VULCANO** (postular la entidad oculta ↔
parchar con una entidad espuria cuando la ley es otra). El caso histórico es perfecto: **el mismo
Le Verrier, la misma operación** — 1846 postula un planeta invisible por el bamboleo de Urano →
Neptuno aparece esa noche a <1°; 1859 hace LA MISMA jugada con el corrimiento de Mercurio → Vulcano
no existe; la respuesta era cambiar la TEORÍA (relatividad general). Lo que decide el polo: ¿la
entidad postulada genera una predicción INDEPENDIENTE comprobable, o solo parcha? — y eso YA lo cobra
la maquinaria (off-support + MDL). Razones de la elección: el lado Neptuno YA existe y está validado
(familia v2 — headroom demostrado, tier A propio); falta SOLO el gemelo Vulcano (misma fachada, sin
entidad oculta, la ley es otra). **REQUISITO pre-build**: test de viabilidad estilo #12 sobre el
gemelo — el fit-con-entidad-espuria sobre el pool debe dejar residuo o pagar complejidad MEDIBLE; si
no, el gemelo no discrimina y el par se rechaza (certificado del par, principio 10). *El par
angosta/amplia (`docs/mundo-espejo-klayman-ha.md`) queda EN CANTERA: tier B puro, ambos polos desde
cero, riesgo de que frontier lo resuelva de taquito.*
> **★ VALIDACIÓN INDEPENDIENTE del par Vulcano ("Position: LLMs can't jump", OpenReview klU4737opt,
> 2026).** Un position paper de filosofía de la ciencia usa EXACTAMENTE este ejemplo, sin conocernos:
> *"una IA guiada por compresión preferiría parchar la gravedad de Newton con un parámetro tipo el
> planeta 'Vulcano' antes que expandir el espacio de hipótesis a la geometría no-euclidiana, que
> aumenta la complejidad antes de simplificar."* Su tesis —los LLMs no pueden el "salto" abductivo de
> inventar la explicación reestructurante— es la teoría del polo-aha que nuestro par mide. Y proponen
> como remedio **mundos interactivos con intervención contrafáctica** (*"take control of the simulation
> to conceptually cut the cable"*) — o sea, WAGER, desde otro ángulo. **TENSIÓN honesta que dejan
> planteada** (a tener presente en el diseño, no resuelta): los descubrimientos más profundos ocurren
> SIN señal de error (la gravedad newtoniana tenía loss≈0; la anomalía de Mercurio se leía como
> variable oculta, no como falla) → *"sin discrepancia entre predicción y observación, no hay gradiente
> que empuje a reestructurar."* Nuestro reward ES una señal de error, así que nuestros mundos modelan
> el caso "hay anomalía cobrable", no el caso "todo cierra y aun así reestructurá". **REENCUADRE de
> Lucas (2026-07-10) — casi disuelve la objeción**: controlamos el DGP, así que diseñamos los datos
> observados para que **sub-determinen** la estructura — el naive ajusta bien lo VISIBLE (como Newton),
> pero la nota se cobra en regímenes NO mostrados (do(), contrafáctico, fuera-de-soporte) donde solo la
> estructura verdadera generaliza. La señal no está en ajustar lo observado (eso lo hace el naive) sino
> en el proceso de descubrimiento + los regímenes ocultos = el test abductivo, y nuestro scoring YA
> puntúa sobre batería no-mostrada. El trofeo v2 es instancia parcial. Ver **OQ 24** (con el residuo
> duro que queda: cuando ni un agente que sondea ve señal en ningún régimen alcanzable).

**Huecos del catálogo espejo (próximo minado)**: el caso NOMBRADO de apofenia (polo vicio de A2) ·
los pares partir-en-dos↔multiplicar-entidades y promover-anomalía↔perseguir-ruido (no aparecieron) ·
promover A2/A3/A4 de tier B a tier A (¿frontier falla en cruzar espacios / reencuadrar? — pregunta
empírica que nuestros propios mundos pueden contestar).

## 4-bis. Corpus compilado (Lucas) — ruteado por el corte OPERACIÓN/JUICIO (§0.5)

Recopilación de Lucas de fuentes reales (2025-2026). Lo que aportan de único: **números**. Pero
—corrección de Lucas— NO van todos en la misma tabla: primero se **rutean por §0.5**, porque los
de operación no son blanco de WAGER y mezclarlos diluye el foco que es toda la tesis.

### JUICIO — el blanco de WAGER (el andamiaje NO los arregla)
Cuantificados (la vara empírica que nos faltaba), del análisis por grafo epistémico
(arxiv 2604.18805) y afines:
- **Evidencia IGNORADA en el 68% de los traces** (A): tiene en contexto un resultado que
  contradice su hipótesis y sigue como si nada. *Juicio puro — la info está, la jugada no.*
- **Revisión de creencia refutada solo en el 26%** (A): ante evidencia contraria, casi nunca
  actualiza.
- **Convergent multi-test RARO** (~6-13% según modelo) (C): pudiendo triangular con tests
  independientes, no lo hace.
- **Retirada a defaults/convenciones** (D): con una convención no-estándar que él mismo escribió,
  vuelve al default de manual (vibe-physics). *Abandona la estructura correcta que ya tenía.*
- **Sycophancy bajo presión** (C): cede el juicio a la presión social y da la respuesta que
  parecés querer. *La presión no solo expone el vicio — puede CREAR el de complacer.* Dato de
  diseño: cuidá que la "pista" no induzca complacencia.
- **No actuar sobre la propia anomalía** (C/A): no ve lo interesante/anómalo en sus resultados.
- **Hundirse recuperando un estado OCULTO** (D/v2): aunque lo reporte OSWorld —benchmark de
  operación— esto es juicio: exige inferir lo latente, la familia de nuestro trofeo. *El ejemplo
  de por qué el discriminador manda sobre la fuente (§0.5).*

Vicio nuevo, de frontera:
- **Analysis-decision disconnect** (juicio→acción): identifica bien el edge y aun así NO actúa /
  dimensiona mal (benchmark de apuestas). *Es juicio correcto que no se traduce en decisión — un
  tercer tipo. Nuestros mundos actuales no lo testean (el análisis ES el entregable, no hay paso
  de "apostar" separado); anotado como frente futuro.*

### OPERACIÓN — NO es blanco de WAGER (lo resuelve el andamiaje; el campo ya está en esto)
Se listan para **NO confundirlos** con los de juicio, no para construir mundos:
- **Perder restricciones · no registrar info mid-way · adivinar en vez de preguntar · saltear
  verificación · <7% del presupuesto en auto-repararse** (OSWorld 2.0, 2606.29537): el trabajador
  desprolijo. Memoria / checklists / planners / loops de reparación → territorio de ingeniería.
  · **⚠ TENSIÓN (leído 2026-07-09, ADR 0115)**: los autores de OSWorld 2.0 argumentan que NO son
  operación sino JUICIO — *"ejecutan bien las acciones locales pero fallan en el RAZONAMIENTO:
  mantener el estado de la tarea, reconocer cuándo la info nueva invalida decisiones, cuándo pausar en
  vez de adivinar"*. "Perder info mid-task y no actualizar" = nuestro vicio 1. → nuestro discriminador
  (¿lo arregla el andamiaje?) y su tesis chocan acá; pendiente de resolver con Lucas si parte de
  OSWorld cruza a JUICIO.

Straddle (parte operación, parte juicio — se anota el corte, no se mezcla):
- **Error-signal blindness — responde a solo el 32.9% de las señales de error** (SciAgentGym;
  loop-escape 35.7%, switching 15.3%; resiliencia débiles 29→10). *CORREGIDO 2026-07-09 leyendo el
  paper (ADR 0115): el "67%" que citábamos NO existe — era el "Caso 67" (un ejemplo), no un
  porcentaje.* *Rastrear que falló* es operación (un loop de reflexion lo tapa); *diagnosticar por
  qué y pivotear* es juicio.
- **Degradación de resiliencia en trayectorias largas** (E): la robustez cae monótona en
  horizonte (débiles ~30%→~10%); *que sea entrenable* (Rise-Fall-Rise en los fuertes) es la parte
  de juicio/modelo → insumo E2. El horizonte en sí es la cara operacional de E (§3).

## 4-ter. Metodología externa que VALIDA nuestro enfoque (no un vicio — una confirmación)

- **La evaluación por OUTCOME no detecta estas fallas** (2604.18805, *"AI scientists produce results
  without reasoning scientifically"*, Ríos-García et al.; **leído entero 2026-07-09** — su setup son
  **8 dominios de QUÍMICA/materiales + 25.000 corridas**, NO "CLadder/QRData" como decíamos): un
  agente ejecuta el workflow con buen resultado pero con proceso basura (ignora evidencia 68%, revisa
  26%; base-model 41.4% vs scaffold 1.5% de la varianza). Su frase textual: *"la evaluación por
  resultado no puede detectar estas fallas; hasta que el razonamiento sea un objetivo de
  entrenamiento, el conocimiento no puede justificarse por el proceso"* = **exactamente** nuestra
  doctrina "conducta observada" (§2.1). Confirmación externa fuerte, de un grupo de química de afuera.
- **2ª confirmación externa, aún más directa (Luo, Kasirzadeh & Shah, CMU — 2509.08713, "The More You
  Automate, the Less You See"; leído)**: *"usar solo el paper final como objetivo de evaluación pierde
  la oportunidad de encontrar muchos failure modes críticos, particularmente los que involucran el
  proceso de decisión durante la experimentación"*; con acceso a las TRAZAS la detección sube a 74%
  (F1 0.75). Documenta 4 fallas invisibles en el paper (cherry-picking de benchmarks —Agent Laboratory
  elige los primeros 4 listados el 82.4% de las veces—, data-leakage no documentado, mal uso de
  métricas por orden de presentación, sesgo de selección post-hoc). **Recomienda que las conferencias
  exijan las trazas + el código** — es, textual, el argumento de WAGER.
- **El grafo epistémico como vocabulario listo** (mismo paper): anota cada paso de la traza
  con 6 nodos — **H**ypothesis, **T**est, **E**vidence, **J**udgment, **U**pdate,
  **C**ommitment — y aristas (testing, observing, contradicting, updating…), y matchea contra
  *productive motifs* (falsación popperiana, reranking de hipótesis, revisión por refutación,
  evidencia convergente) vs *reasoning breakdowns* (untested claim, contradiction-without-repair,
  premature commitment, evidence non-uptake, fixed-belief-trace, precommitted-test-plan,
  stalled-revision). **Podemos ADOPTAR este vocabulario para nuestras firmas de trace** — es
  una taxonomía publicada de exactamente lo que medimos.
- **El base model explica el 41.4% de la varianza; el scaffold solo 1.5%** (mismo paper):
  cambiar el prompt/arquitectura casi no mueve la aguja — el vicio vive en el MODELO, no en el
  prompt. **Confirma nuestra tesis de ADR 0096/0098**: el "sé cuidadoso" genérico no arregla el
  vicio (mueve ejecución); el vicio es una propiedad del modelo que hay que ENTRENAR (E2), no
  promptear. Y confirma que el instrumento debe medir algo que el prompt no puede fingir.
- **In-context learning NO lo arregla** (mismo paper): el patrón persiste aun dándole un ejemplo
  casi-completo de buen razonamiento en contexto → refuerza que es entrenable, no prompteable.

## 5. Fuentes a minar (la investigación concreta — en curso)

El seed de §4 sale de conocimiento general; la versión rigurosa se arma yendo a estas familias
de fuentes y sacando failure modes CONCRETOS con su cita:
- **Evals de agentes autónomos**: METR (task-horizon, autonomy failures); taxonomías de fallos
  de agentes LLM 2024-2025.
- **Agentes-científicos / research agents**: AI Scientist (Sakana) y sus críticas; ResearchAgent;
  papers de "LLM as scientist" y sus modos de falla.
- **Benchmarks de descubrimiento**: ScienceWorld, DiscoveryWorld, DiscoveryBench, BoxingGym,
  QRData — sus análisis de error.
- **Cog-sci del razonamiento científico**: confirmation bias / hypothesis testing (Wason,
  Klayman-Ha, Kuhn), heurísticas y sesgos (Kahneman-Tversky), scientific reasoning (Klahr).
- **Calibración / juicio**: superforecasting (Tetlock), calibración y overconfidence.
- **Honestidad / sycophancy / overclaiming**: evals recientes de honestidad de LLMs.
- **Metaciencia**: crisis de replicación, p-hacking, garden of forking paths (Gelman & Loken).

> **Ya minado (deep-research, 2026-07-07 — ver ítems `[dr ✓]` en §4)**: cog-sci del razonamiento
> (Chinn & Brewer 1993; Klayman & Ha 1987; Dunbar 1997; Anderson & Lepper 1980; Mitroff 1974) ·
> metaciencia (Gelman & Loken; Stefan & Schönbrodt 2023; Nagy et al. 2025; Vaccaro 2026) · causal
> (Corr2Cause/Jin 2023; Kapoor & Narayanan 2023) · newest evals (MLR-Bench NeurIPS 2025; HLER 2026).
> **2ª búsqueda — casos por ESTRUCTURA (case-search, 2026-07-07, completa)**: ver el ★ Mapa en §4
> (1≈8, 6=4, 3=4, 7=2). **3ª búsqueda — puntos ciegos (completa)**: LLENÓ vicio 4 (6 estructuras),
> vicio 5 (7) y vicio 2 (5). Ver el ★ Mapa.
> **4ª búsqueda — estructuras de AHA de a pares (2026-07-09, completa)**: ver el ★★ Catálogo ESPEJO
> en §4 (5 estructuras con polo vicio, tier y forma de pago; crudo en `docs/research/`).
> **Pendiente de minar (prioridad = los huecos que quedan)**: vicio 7 sub-estructuras
> **colisionador / sesgo-de-selección** (Berkson) e **"intervenir-o-fallar"** (0 casos aún) ·
> caso NOMBRADO de apofenia + pares partir↔multiplicar y anomalía↔ruido (catálogo espejo) ·
> historiografía caso-por-caso de los clásicos de visión-de-túnel (Blondlot, fusión fría, canales
> marcianos) antes de usarlos · fuentes generales sin tocar: METR fino · AI-Scientist · Tetlock.
> **Lente del minado desde ADR 0106**: para cada operación se buscan LOS DOS POLOS (caso genio + mal
> uso documentado, cada uno con fuente), y todo hallazgo se etiqueta tier A/B (principios 10-11).

> **Acción concreta**: correr una investigación dirigida (skill `deep-research` o WebSearch) por
> cada familia, extrayendo failure modes con cita + evidencia. **Triage obligatorio (§0.5) ANTES
> de asignar familia**: por cada vicio preguntá primero *¿lo arregla el andamiaje?* — si sí es
> OPERACIÓN (se anota bracketeado, no es mundo WAGER); si no es JUICIO y recién ahí se le asigna
> su dinámica de §3. La heurística de fuente ayuda a rutear pero no decide. Paciencia: uno por uno.
> **Y buscar EJEMPLOS/casos concretos por vicio, agrupados por TIPO de estructura** (no solo dominios
> distintos): la cartera necesita variedad ESTRUCTURAL para no overfitear en el entrenamiento
> (principio 9). Búsqueda de casos lanzada 2026-07-07 con ese foco.

## 6. El proceso (de un vicio a un mundo)

```
vicio documentado (§4/§5)
   -> ¿qué DINÁMICA de mundo lo fuerza de forma puntuable? (§3)
   -> deliverable puntuable (predecir comportamiento) + cero-LLM
   -> diseñar el CERTIFICADO DE TRAMPA NECESARIA (robot vicioso pierde / cuidadoso gana)
   -> ¿PRESIÓN? -- es PERILLA calibrable por modelo, no requisito (ADR 0111)
   -> build (spec-first) -> certificar -> E0 con pre-registro   [= PLANTA PILOTO, capa 2]
   -> ¿el vicio se manifestó con un solver real? (la validez, ADRs 0098/0110)
   -> estructura VALIDADA => PLANTILLA para la FÁBRICA (capa 3, §0.6):
      variaciones en serie (piel/params/seeds) filtradas por certificación cero-LLM (yield)
```

## 7. Lo difícil / preguntas abiertas (honestas)

- **Scoring de EXPLICACIONES sin LLM** (suite Anomaly, "¿qué pasó?"): el muro más duro. Los
  vicios que requieren un deliverable-explicación quedan bloqueados hasta resolverlo. Mientras,
  se los fuerza con deliverable-predicción (§ principio 6).
- **Vicios un-hinteable (insight profundo, v2) vs dispositivos (hinteable)**: la distinción de
  ADR 0097. Los profundos no se validan con pista (cualquier pista = leak) — su validez es que
  ningún modelo los vence (v2: 0/10). Los dispositivos se validan con pista dirigida (ADR 0098).
- **Eje de creatividad/representación**: ahora tiene su catálogo (★★ Catálogo ESPEJO, §4) con la
  línea divisoria precisa: re-representación que desbloquea PREDICCIÓN = construible (sub-caso i);
  reframing de pura elegancia sin predicción = sigue del otro lado del muro (etiqueta "no sabemos
  puntuarla"). ECHO/coherencia = tarea de investigación con timebox (ver ★★), no muro caído.
- **El catálogo es CANTERA, no cola** (ADR 0106): la línea de llegada sigue en 12 mundos; de esta
  cantera salen los 3-4 difíciles que faltan, con prioridad a la familia de reestructuración
  (generaliza v2, headroom demostrado) y a completar UN par entero como prueba del principio 10.
- **Réplica pendiente (ADR 0098) — PRIMERA del ledger, no se mueve**: DeepSeek + más seeds +
  clasificación automática de ceros. Hasta que corra, TODO lo de este documento (incluido el
  catálogo espejo) dice "señal preliminar", no "validado" — que el catálogo no se adelante a su
  propia evidencia (nuestro vicio 3, versión casa).
