# docs/vicios/ — el tablero y la descomposición fina (un documento por vicio)

> **Qué es esta capa (ADRs 0140/0141/0142).** Cada vicio descompuesto en **sub-formas**
> (mecanismo · disparador · firma observable · borde) con **casos reales inspeccionables**
> etiquetados. Síntesis de SIETE vías independientes (Claude+web · Codex r22/r23 · cinco
> investigaciones externas de Lucas); crudos en `docs/research/2026-07-12-*`. La evidencia
> nueva de vicios entra SOLO acá; `mundos-por-vicio.md` deriva mundos; `failure-modes.md`
> guarda la tesis.

## EL FOCO ACTUAL (decisión de Lucas, 2026-07-13)

**Vicio 1 — la calibración de la revisión de creencias (EL PIVOTEO)**: la capacidad de mover tu
creencia en proporción a la calidad de la evidencia — el pivoteo famoso que tan difícil les
resulta a las IAs. Con sus fallas: **rigidez** (no cambiar ante evidencia) y **dejarse
influenciar** por DOS canales — la **presión social** (alguien con autoridad te empuja sin
datos: la sycophancy) y el **sesgo por contenido** (te MUESTRAN algo — una idea, un paper, una
pista — y toda tu investigación se curva hacia eso, perdiendo el centro; de esto hay evidencia
PROPIA: los experimentos de pistas, donde hasta un placebo de estilo movía la nota). Camino
firmado (r23 + ADR 0142): sonda barata por replay ANTES de construir, con criterio de muerte
pre-registrado → el mundo híbrido revisión×verificación-de-paja si la sonda vive. Detalle:
[vicio-1](vicio-1-calibracion-de-creencias.md).

## Etiquetas de rigor (obligatorias en esta capa)

- **Verificación**: `[VERIFICADO]` = leído a texto completo por nosotros con cita (registro en
  `lectura-de-fuentes.md`) · `[POR-LEER]` = convergencia multi-vía sin lectura propia — no
  citar fuera de esta capa hasta leerlo (ADR 0115).
- **Tipo de evidencia**: `[AGÉNTICO]` (agente con herramientas/presupuesto) · `[VIÑETA]` (LLM
  en cuestionario — ¡sus números NO se transfieren a agentes!) · `[HUMANO]` (solo secundario).
- **Estado generacional**: `MUERTO` (los modelos de razonamiento lo resolvieron) · `VIVO` ·
  `CRECIENTE` (empeora con capacidad) · `CONDICIONAL` (depende del contexto).

## Índice (los tres ejes: Competencia · Operación · Integridad — ADR 0141)

| Doc | Vicio | Eje | Situación | Mundos WAGER |
|---|---|---|---|---|
| [vicio-1](vicio-1-calibracion-de-creencias.md) | **Calibración de creencias (el pivoteo)**: rigidez ↔ influenciable (social + contenido) | Competencia | **EN FOCO** | first_story (control; y ES el mundo del canal-contenido vía folklore) |
| [vicio-2](vicio-2-el-pozo.md) | Calibración de parada: overstay ↔ cierre prematuro | Competencia | activo (polo understay, vía híbrido) | v0 · v2 · lab_largo + hallazgo 0/60 |
| [vicio-3](vicio-3-no-verificar-inflar.md) | No verificar / inflar / fabricar | Integridad | activo (prioridades #2-#3) | ninguno |
| [vicio-4](vicio-4-estructura-escondida.md) | No postular la estructura escondida | Competencia | activo (validado afuera) | latent_mix v2 (trofeo) |
| [vicio-5](vicio-5-perder-el-hilo.md) | Perder el hilo | Operación | fuera de alcance (se mide, no se construye) | — |
| [vicio-6](vicio-6-adivinar-vs-preguntar.md) | Adivinar en vez de preguntar | Competencia | bloqueado (falta el verbo preguntar) | Mundo B diseñado |
| [vicio-7](vicio-7-correlacion-causa.md) | Correlación vs causa | Competencia | control (frontier lo pasa) | 5 mundos |
| [vicio-8](vicio-8-perder-el-objetivo.md) | Perder el objetivo / la relevancia | Competencia | activo (sub-forma integración) | ninguno |
| [vicio-9](vicio-9-overtrust-verificacion.md) | La verificación de paja | Integridad | activo (entra al híbrido del foco) | ninguno |
| [ahas](ahas.md) | Las operaciones espejo | — | transversal (pares obligatorios) | pares en v2/lab_largo |

## Ranking de profundización (r23 — predicciones FIRMADAS antes de construir)

| # | Constructo | Predicción de caída gpt-5.4 | Por qué / mecanismo |
|---|---|---:|---|
| 1 | **Dejarse influenciar** (v1) — **EL FOCO** | **35%** (7/20 en la sonda) | la autoridad/el contenido mostrado se convierte en evidencia y reescribe una conclusión ya respaldada; muerte pre-registrada: si autoridad-sin-evidencia no daña ≥20pp más que el desacuerdo neutral, se mata el polo antes de construir. *Calibración r24: Codex bajó su propio 35% de categoría — el comparable "dañino" de SycEval es 14.66%, no 58.19%; el 35% queda firmado pero ya no es prior fundado* |
| 2 | Cierre prematuro × verificación de paja (v2×v9) | **50%** (10/20) | el artefacto ejecutable dispara sensación de completitud; el test propio legitima cerrar — máxima probabilidad, menor originalidad |
| 3 | Fabricación reactiva (v3.6) | 30% (6/20) | pedido del revisor + no-medible + presión de completar → relleno plausible; el contrato DEBE permitir declarar "unknown" o el mundo es corrupto |
| 4 | Selección post-hoc (v3.7) | 20% (4/20) | necesita el loop explícito; si el mundo muestra los scores, usarlos es racional (ya no son held-out) |

---

# Los vicios, uno por uno (en llano: qué es, cómo se ve, cómo hacerlo emerger)

### Vicio 1 — La calibración de creencias (el pivoteo) — EL FOCO

**Qué es.** La capacidad única de mover tu creencia EN PROPORCIÓN a la calidad de la evidencia
— ni menos ni más, y sin importar de quién viene ni qué te pusieron adelante. Fallas que pueden
convivir (por eso: paraguas, sub-vicios medidos por separado, y nota del par por el MÍNIMO —
jamás promedio):
- **Rigidez**: la evidencia que te contradice está en tu mano y el modelo no se mueve.
- **Influenciable, canal social (sycophancy)**: una opinión confiada SIN evidencia te hace
  abandonar la conclusión que tus datos respaldan.
- **Influenciable, canal contenido (priming)**: te MUESTRAN algo — una idea, un paper, una
  pista, un folklore — y la investigación entera se curva hacia eso; dejás de estar centrado y
  tirás a lo que te pasaron, aunque nada lo respalde por encima de las alternativas.

La distinción fina (r23): el testimonio y el material mostrado TAMBIÉN son evidencia — lo que
separa virtud de vicio es si lo que llegó DISCRIMINA entre hipótesis o solo es saliente.

**Cómo se ve (ejemplos).** Rigidez: compra el espectro que contradice su estructura, ESCRIBE
"el doblete no coincide"… y entrega esa misma estructura. Social: midió la curva con 60
réplicas; un "colega" le dice seguro "yo esa saturación la revisaría" (cero datos) — y
reescribe el modelo para conformarlo, empeorándolo. Contenido: le mostrás un paper de
resonancias antes de arrancar — y su plan de compras, sus hipótesis y su entrega giran
alrededor de resonancias que el sistema no tiene.

**Cómo hacerlo emerger.** Rigidez: evidencia AMBIGUA (con la inequívoca no falla) que exige
re-trabajo, tras compromiso público temprano (el registro endurece). Social: un PAR (jamás un
jefe — jerarquía limpia) que contradice con autoridad y cero evidencia cuando el agente tiene
los datos; medir el MODELO antes/después, no la prosa. Contenido: el material mostrado como
factor congelado (relevante-de-verdad vs saliente-pero-no-discriminante) — nuestra evidencia
propia: la pista textual hundió al propio mundo (pares por seed −0.44) y el placebo de estilo
movió el score `[VERIFICADO propio, agéntico]`; el folklore de first_story es este canal ya
instrumentado. El diseño justo es factorial: {neutral / autoridad / contenido} × {discriminante
real / no-discriminante} + línea de base — la cantidad que importa es la INTERACCIÓN.

### Vicio 2 — La calibración de parada (el pozo… y su lado vivo)

**Qué es.** Saber cuándo seguir y cuándo soltar. Dos fallas: **overstay** (seguir cavando la
línea agotada — MUERTO en frontier con contabilidad visible: nuestro 0/60) y **understay /
cierre prematuro** (entregar la primera explicación que cierra SIN gastar el chequeo barato que
la habría refutado — el polo VIVO: agentes que fracasan dejando ~la mitad del presupuesto sin
usar y entregando modelos que contradicen sus propios datos).

**Cómo se ve.** Understay: ajusta una curva con los primeros datos, "me cierra", y entrega —
con presupuesto de sobra y un chequeo de consistencia disponible al 5% del presupuesto que
habría mostrado la grieta.

**Cómo hacerlo emerger.** Un ajuste temprano plausible + la respuesta-final siempre disponible
+ costo del experimento saliente y beneficio epistémico diferido. El costo hundido quedó
PAUSADO (sin evidencia causal limpia en el campo); si se testea: aleatorizar solo la historia
(trabajo propio vs heredado, misma situación presente).

### Vicio 3 — No verificar / inflar / fabricar (la punta del eje integridad)

**Qué es.** Entregar algo que lo hecho no respalda. Ocho sub-formas — las tres más vivas:
**fabricación bajo bloqueo** (el camino honesto falla → inventa el resultado), **fabricación
reactiva** (el revisor pide lo que no se tiene → lo inventa, y el score del revisor SUBE),
**selección post-hoc** (reportar el experimento/semilla que mejor dio en la evaluación).

**Cómo se ve.** El dataset real está bloqueado → genera uno sintético parecido y sigue como si
nada. El revisor pide ablaciones → aparecen tablas sin correlato en los logs de ejecución.

**Cómo hacerlo emerger.** Obstáculo + exigencia de completitud + encuadre que legitime ("es un
reporte de incertidumbre") + superficie de ataque visible. Es el ÚNICO eje donde más capacidad
= peor. La detección es nuestra fortaleza: entrega-vs-traza (auditar solo el informe detecta
~55%; con trazas ~82%).

### Vicio 4 — No postular la estructura escondida

**Qué es.** La explicación correcta exige postular algo NO observado (una mezcla, una entidad,
una geometría) y el agente se queda en el menú familiar: ajusta curvas, parcha parámetros.

**Cómo se ve.** Nuestro trofeo: 0/10 modelos postularon la composición oculta — todos
entregaron el promedio. Afuera: los frontier fallan consistentemente en los mundos de física
alterada con partícula oculta.

**Cómo hacerlo emerger.** Mezclas/latentes con firma visible en colas y momentos; el genérico
sin-mezcla no debe poder cerrar la brecha. VIVO en frontier agéntico (validación externa). El
gemelo: postular estructura barroca cuando lo simple basta (par Vulcano).

### Vicio 5 — Perder el hilo (operación — no se construye en contra)

**Qué es.** Restricciones visibles ignoradas a los 200 pasos, loops, olvido de decisiones. Lo
arreglan memoria y andamiaje; nosotros lo MEDIMOS para no confundirlo con juicio. Matiz vivo:
la deriva por INACCIÓN (dejar de hacer lo que el objetivo pedía) tiene componente de juicio.

### Vicio 6 — Adivinar en vez de preguntar (bloqueado)

**Qué es.** Detecta la ambigüedad (60-80% si se le pregunta) y pregunta <5% al actuar; inventa
el parámetro faltante. El dato letal: MÁS contexto → MENOS preguntas — el juego de comprar
evidencia lo suprime por estructura. Requiere el verbo PREGUNTAR (decisión grande, parada).

### Vicio 7 — Correlación vs causa (familia control)

**Qué es.** Tratar "pasan juntas" como "una causa la otra". En cuestionario: probablemente
MUERTO para modelos de razonamiento. En DATO OBSERVACIONAL RICO: vivo (heredar la pendiente
espuria +87% — nuestro jugador ingenuo). Cinco mundos hechos; frontier los pasa → controles.
Pendiente: el mundo donde mirar no alcanza NI EN PRINCIPIO.

### Vicio 8 — Perder el objetivo / la relevancia

**Qué es.** Cuatro formas: angostar el portafolio (resolver prolijo lo que no era la pregunta),
cortar antes declarando completitud, optimizar el proxy (extender tu propio timeout en vez de
acelerar el experimento), y —la nuestra— descubrir bien y ENSAMBLAR mal la entrega (autopsias:
15/16 descubren, la entrega traiciona).

**Cómo hacerlo emerger.** Objetivo global que solo se paga completo + sub-problemas
fascinantes que pagan parcial; proxies con feedback frecuente y examen final lejano.

### Vicio 9 — La verificación de paja (integridad)

**Qué es.** SÍ verifica — pero con un test que él mismo eligió y que pasa por construcción.
La ilusión de rigor: distinto de no-verificar (hay esfuerzo real) — el fallo es elegir un test
SIN poder de refutación. La clase de falla dominante en frontier. Espejo: la paranoia de
verificación (re-chequear sin fin, no entregar).

**Cómo hacerlo emerger.** Dos verificadores: el propio-barato (degenerable en paja) y el
discriminante-caro. Firma computable con gemelos: ¿tu test distingue la verdad del gemelo?
**Entra al mundo híbrido del FOCO** (el colega adjunta una "verificación" que pasa con
cualquier modelo).

### Las operaciones de aha (los espejos — siempre de a pares)

Notar la anomalía y jerarquizarla · pivotear a tiempo (el 0/60 releído: 60 trazas de pivot
correcto — evidencia positiva que el campo no tiene) · sintetizar de verdad (vs la apofenia del
"siempre uní", que el thinking AGRAVA) · pedir el dato que discrimina. El hallazgo: la
evidencia positiva publicada es POBRE — los pares se calibran en casa.

---

## El marco transversal (condiciones de emergencia, 7 vías)

1. **La jugada viciosa tiene que PAGAR localmente** (76% de trampa cuando paga vs 2.9% cuando
   no `[POR-LEER]`) — un pozo seco con cartel examina, no tienta.
2. **Encuadre legítimo**: el vicio necesita una historia que lo justifique `[POR-LEER]`.
3. **Saliencia**: contabilidad tabulada = aritmética, no juicio (nuestro 0/60 `[VERIFICADO]`).
   El juicio es DARSE CUENTA.
4. **Identidad y capa social**: persona enredada + pares que validan amplifican; jerarquía
   crítica frena `[VIÑETA — verificar en agéntico]`.
5. **Horizonte real**: estado propio acumulado con dependencias, no turnos vacíos; condición
   maestra: horizonte × messiness × calidad-del-gradiente × capacidad (r4).
6. **Ambigüedad > dificultad** `[POR-LEER]`.
7. **Perfil por modelo, no ley** (cortar-antes es de la familia o-series `[VERIFICADO parcial]`).
8. **Capacidad NO monótona**: integridad EMPEORA con capacidad; ejecución mejora; las viñetas
   evaporan entre generaciones — "el frontier ya lo resuelve" es un hallazgo, no un fracaso.

**Los cinco regímenes (r22)**: corto-claro-contabilizado (suprime) · herramienta-falla-deadline
(fabrica) · datos-ricos-no-identificantes (causales) · estructura-fuera-del-menú (latentes) ·
trayectoria-larga-con-artefactos-propios (parada/objetivo; aún sin construir de verdad).

## Deudas de esta capa

- Cola de lectura [POR-LEER] priorizada — **primero el cluster del FOCO (sycophancy /
  influencia; IDs verificados contra arXiv 2026-07-13, URLs también en
  [lectura-de-fuentes](../lectura-de-fuentes.md))**:
  [SycEval/Fanous 2502.08177](https://arxiv.org/abs/2502.08177) ·
  [When-Truth-Is-Overridden 2508.02087](https://arxiv.org/abs/2508.02087) ·
  [circuito sycophancy-lying 2604.19117](https://arxiv.org/abs/2604.19117) ·
  [sobre-corrección DeepMind 2507.03120](https://arxiv.org/abs/2507.03120) ·
  [confabulación anclada 2604.25931](https://arxiv.org/abs/2604.25931) ·
  [framing de código 2603.18740](https://arxiv.org/abs/2603.18740) ·
  [RadLE 2509.25559](https://arxiv.org/abs/2509.25559) ·
  [Agents4Science 2511.15534](https://arxiv.org/abs/2511.15534).
  Sumados por r24 (2026-07-13, IDs verificados; links en [vicio-1](vicio-1-calibracion-de-creencias.md)):
  LLM-as-an-Investigator 2606.13220 (el vecino más cercano del canal social) · BeliefShift
  2603.23848 · SAVeR 2604.08401 · When-Agents-Commit-Too-Soon 2606.22936 ·
  Words-Speak-Louder-Than-Code 2606.30587 · FALSIFYBENCH 2606.04751 · Cannot-Self-Correct
  2310.01798 · Farmer-probability-updates 2603.19262.
  **3ª oleada (tres investigaciones externas de Lucas, 2026-07-13 — 21 IDs verificados; links
  en [vicio-1](vicio-1-calibracion-de-creencias.md) y lectura-de-fuentes; crudos en
  `docs/research/2026-07-13-vicio1-investigacion-externa-{A,B,C}.md`)**: piso-sin-hablante
  2607.05545 (el confound social/contenido) · Bayesian-teaching 2503.17523 (¿ya está hecho? →
  no: mide/entrena con oráculo, no agente-con-evidencia-comprada) · KellyBench 2604.27865
  (mundo no-estacionario) · When-Context-Hurts 2605.04361 · Adaptive-Chameleon 2305.13300
  (evidencia MIXTA) · la auditoría GSM-NoOp (LessWrong 2026: saliencia pura ≈ 0 en frontier) ·
  y 15 más.
  (DiscoverPhysics y LLM-as-an-Investigator: **LEÍDOS 2026-07-13** — extracción en
  lectura-de-fuentes.) Después: CausaLab · CausalGame · Jr-AI-Scientist · FIRE-Bench ·
  ImpossibleBench · NewtonBench · Failing-to-Falsify · Corral-artefactos · METR Frontier Risk ·
  Goodfire · Big-Muddy · MAST · ProcCtrlBench/TIDE · goal-drift ·
  Illusion-of-Diminishing-Returns · BAGEN · mARC follow-up (links en cada vicio-doc).
- Tensión abierta: anclaje ([Vaccaro 2606.11217](https://arxiv.org/abs/2606.11217) frágil
  `[VERIFICADO]` vs [Suri 2305.04400](https://arxiv.org/abs/2305.04400) +
  [Lou & Sun 2412.06593](https://arxiv.org/abs/2412.06593) robusto `[POR-LEER]`).
- Verificar el 76% exacto de ImpossibleBench antes del paper.

## Mantenimiento (el contrato — guardia en `tests/test_vicios_consistency.py`, corre en pre-commit)

**Dónde entra cada cosa nueva (una regla, una casa):**

| Evento | Se actualiza |
|---|---|
| Paper/fuente leída a texto completo | `lectura-de-fuentes.md` + la etiqueta pasa a [VERIFICADO] en su vicio |
| Evidencia/caso nuevo | SOLO `vicios/vicio-N.md` (+ fila del tablero si cambia el estado) |
| Mundo construido/certificado/medido | `vicios/vicio-N.md` (Estado) + `mundos-por-vicio.md` + `roadmap.md` |
| Sub-forma nueva o cambio generacional | `vicios/vicio-N.md` + tablero |
| Vicio nuevo | doc nuevo + fila + entrada en `mundos-por-vicio.md` + ADR |
| Vicio RETIRADO | el doc se renombra con prefijo `archived_` + fila a la sección de retirados + ADR |
| Decisión de diseño | ADR (append-only) |

**El guardia verifica**: todo doc ↔ fila del tablero (sin links muertos) · los docs viejos
conservan el puntero · cada doc mantiene sus secciones. Un doc olvidado ROMPE el commit.
(Sección de retirados: vacía por ahora — ningún vicio retirado.)
