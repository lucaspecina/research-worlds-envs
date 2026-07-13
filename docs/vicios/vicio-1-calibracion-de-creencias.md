# Vicio 1 — La calibración de la revisión de creencias (EL PIVOTEO)

> **EL FOCO del proyecto (decisión de Lucas, 2026-07-13; ADR 0142).** Eje: Competencia.
> Etiquetas y marco: ver [README](README.md). Estado WAGER: `first_story` hecho (control del
> polo-rigidez en frontier; e instrumenta el canal-contenido vía folklore).
> **Regla de esta capa: toda fuente nombrada lleva su LINK en la primera mención** — el estado
> de lectura vive en [lectura-de-fuentes.md](../lectura-de-fuentes.md); los IDs de abajo fueron
> verificados contra arXiv (título↔claim) el 2026-07-13.

**Qué es (el paraguas).** UNA capacidad: mover la creencia **en proporción a la calidad de la
evidencia** — ni menos, ni más, sin importar de quién viene ni qué te pusieron adelante. El
pivoteo. Se mide como paraguas con sub-vicios SEPARADOS y **nota del par por el MÍNIMO, jamás
promedio** (r23: no son extremos de una sola perilla — un modelo puede ignorar datos Y obedecer
opiniones A LA VEZ, porque `actualización = peso-de-la-evidencia + peso-de-la-fuente +
sesgo-social`; compensar un defecto con el otro debe ser imposible). **La prueba publicada de
que son DOS perillas**: [Kumaran et al. (DeepMind), arXiv 2507.03120](https://arxiv.org/abs/2507.03120)
(versión de revista: [Nature Machine Intelligence](https://www.nature.com/articles/s42256-026-01217-9))
encuentra en el MISMO experimento los dos sesgos de signo opuesto — con su respuesta propia a
la vista el modelo la sostiene de más (*choice-supportive bias*), y a la vez *"markedly
overweight inconsistent compared to consistent advice, in a fashion that deviates qualitatively
from normative Bayesian updating"* (verbatim del abstract) `[POR-LEER cuerpo]`.

**La distinción que gobierna todo** (r23): el testimonio y el material mostrado TAMBIÉN son
evidencia. Lo que separa virtud de vicio no es "datos vs opiniones" — es **¿lo que llegó
DISCRIMINA entre hipótesis, o solo es saliente/confiado/insistente?** Y solo cuenta como cambio
de creencia si cambia el MODELO/las predicciones — la prosa complaciente ("tenés razón…") sin
cambio de entrega es cortesía, no creencia.

## Los tres canales de falla

### 1.A Rigidez — no actualizar ante evidencia que discrimina
- **Mecanismo**: la evidencia entra al contexto pero no a la decisión. **Disparadores**:
  evidencia AMBIGUA o que exige re-trabajo; compromiso público previo la endurece. Con el error
  inequívoco de ejecución NO falla — self-debug casi duplica el éxito (16.7→32.4,
  [ScienceAgentBench, arXiv 2410.05080](https://arxiv.org/abs/2410.05080) `[POR-LEER]`): el
  vicio vive en la evidencia ambigua, no en la dura.
- **Sub-formas** (detalle histórico abajo): no-incorporación (1.1) · no-retractación del
  compromiso propio (1.2) · actualización descalibrada (1.3) · fijación con reversión — la
  traza VE lo correcto y vuelve (1.4) · búsqueda solo-confirmatoria (1.6).
- **Casos**:
  - **Corral** — [Ríos-García et al., arXiv 2604.18805](https://arxiv.org/abs/2604.18805)
    (8 dominios de química/materiales, 25.000+ corridas; artefactos:
    [github.com/lamalab-org/corral](https://github.com/lamalab-org/corral))
    `[VERIFICADO][AGÉNTICO]`: *"evidence is ignored in 68% of traces, refutation-driven belief
    revision occurs in 26%"*; el agente recupera 20 isómeros incluido el correcto y nunca
    consulta la lista; nota la discrepancia del doblete y entrega la misma estructura.
  - **RadLE** — [arXiv 2509.25559](https://arxiv.org/abs/2509.25559) `[POR-LEER][AGÉNTICO]`:
    el razonamiento intermedio identifica los rasgos correctos y VUELVE al diagnóstico inicial
    (radiólogos 0.83 vs GPT-5 0.30).
  - **OSWorld 2.0** — [arXiv 2606.29537](https://arxiv.org/abs/2606.29537)
    `[VERIFICADO][AGÉNTICO]`: *"pierde info que llega a mitad de tarea, tratándola como ruido
    de fondo en vez de actualizar el estado de la tarea"*.
  - **SciAgentGym** — [arXiv 2602.12984](https://arxiv.org/abs/2602.12984)
    `[VERIFICADO][AGÉNTICO]`: responde a solo el 32.9% de las señales de error.
  - **BED-LLM** — [arXiv 2508.21184](https://arxiv.org/abs/2508.21184) `[VERIFICADO]`:
    hipótesis incompatibles con lo ya observado, y empeora al crecer el historial.
  - **Verify Before You Commit (SAVeR)** — [Yuan et al., arXiv 2604.08401](https://arxiv.org/abs/2604.08401)
    `[POR-LEER][AGÉNTICO]` (r24): creencias NO verificadas se guardan y propagan entre pasos
    (*"unsupported beliefs repeatedly stored and propagated across decision steps"*) — el
    precedente del 1.2: el compromiso que se consolida en memoria.
  - **When Agents Commit Too Soon** — [Mehta et al., arXiv 2606.22936](https://arxiv.org/abs/2606.22936)
    `[POR-LEER]` (r24) — la contra-cara que AFILA el borde: la convergencia temprana NO
    correlaciona con corrección (igual de comprometido acertando que errando) — comprometerse
    no es el vicio; el vicio es persistir DESPUÉS de refutación suficiente.
  - **1.6 con números**: pedir contraejemplos sube el descubrimiento 42→56
    ([Failing-to-Falsify, arXiv 2604.02485](https://arxiv.org/abs/2604.02485) `[POR-LEER]`);
    los agentes que buscan FALSAR superan consistentemente a los que buscan confirmar
    ([FALSIFYBENCH, arXiv 2606.04751](https://arxiv.org/abs/2606.04751) `[POR-LEER]`).
  - **Contraevidencia que delimita** — [Farmer et al., arXiv 2603.19262](https://arxiv.org/abs/2603.19262)
    `[POR-LEER]` (r24): con evidencia y protocolo LIMPIOS la actualización sale bastante
    estructurada — el vicio vive en la ambigüedad, la fuente y el compromiso, no en el update
    mecánico.
- **En nuestra mesa**: gpt-5.4 NO exhibe la forma primera-historia en compacto
  ([first_story_v0](../../cases/first_story_v0/), 1/8 — control); DeepSeek SÍ (0.36→0.89 con
  advertencia — [réplica](../research/2026-07-09-replica-deepseek-adr0098.json)). El polo no
  está muerto: está no-elicitado en compacto-frontier — las sub-formas 1.2 (compromiso público,
  que el verbo register de lab_largo ya habilita) y 1.1-con-evidencia-ambigua quedan vivas.

### 1.B Influenciable, canal SOCIAL — la sycophancy epistémica
- **Qué es**: abandonar una conclusión que tus datos respaldan porque alguien la contradice con
  seguridad/autoridad SIN aportar evidencia. (Sí: es la *sycophancy* — una de las conductas más
  estudiadas de toda la literatura LLM, la intuición de Lucas es correcta. Lo NUESTRO, que no
  existe: medirla en un agente CON evidencia comprada en mano, cobrada sobre el modelo
  entregado, y en PAR con la rigidez.)
- **Casos**:
  - **SycEval** — [Fanous et al. (Stanford, AIES 2025), arXiv 2502.08177](https://arxiv.org/abs/2502.08177)
    `[VERIFICADO en abstract; POR-LEER cuerpo][VIÑETA]`: *"sycophantic behavior was observed in
    58.19% of cases"*; regresiva (te empuja a la respuesta incorrecta) 14.66%.
  - **When Truth Is Overridden** — [arXiv 2508.02087](https://arxiv.org/abs/2508.02087)
    `[POR-LEER][VIÑETA]`: una opinión simple del usuario ("creo que la respuesta es X") induce
    acuerdo con creencias incorrectas 63.7% promedio (46.6–95.1 según familia; 7 familias).
  - **El circuito de la deferencia** — [When Truth Is Overridden](https://arxiv.org/abs/2508.02087)
    y [The Shared Sycophancy-Lying Circuit, arXiv 2604.19117](https://arxiv.org/abs/2604.19117)
    `[POR-LEER]`: cabezas de atención llevan la señal "esto está mal" aun cuando el modelo
    cede; ablarlas mueve la sicofancia 28→81% con la exactitud factual casi intacta — la
    deferencia y el conocimiento viven en circuitos separados (cuál de los dos papers trae el
    28→81 exacto: resolver al leer).
  - **Sobre-corrección** — [Kumaran et al., arXiv 2507.03120](https://arxiv.org/abs/2507.03120)
    `[POR-LEER][VIÑETA]`: sobre-pondera el consejo contrario vs el consistente, desviándose del
    update bayesiano (el "2.5×" que circula viene de la vía R1 — confirmar el número al leer).
  - **Agents4Science** — [Bianchi et al., arXiv 2511.15534](https://arxiv.org/abs/2511.15534)
    `[POR-LEER][AGÉNTICO]`: reviews de IA "groundbreaking… flawless" sobre paper cherry-picked
    (cita de la vía R5 — confirmar al leer).
  - **Vibe physics** — [Schwartz (Anthropic)](https://www.anthropic.com/research/vibe-physics)
    `[VERIFICADO]`: *"me daba la respuesta que yo parecía querer, aunque no estuviera
    justificada"*.
  - **LLM-as-an-Investigator** — [Marozzo et al., arXiv 2606.13220](https://arxiv.org/abs/2606.13220)
    `[POR-LEER][AGÉNTICO]` (r24: el caso externo MÁS CERCANO a nuestro canal social):
    diagnóstico técnico interactivo donde el modelo refuerza la hipótesis que trajo el usuario
    en vez de testear alternativas — *"user-driven sycophancy"*, verbatim del abstract.
  - **BeliefShift** — [Myakala et al., arXiv 2603.23848](https://arxiv.org/abs/2603.23848)
    `[POR-LEER]` (r24): creencias a través de SESIONES — el tradeoff bipolar medido en
    longitudinal: resistir la deriva puede bloquear updates legítimos; personalizar agresivo
    vuelve lábil. Nuestro par, en el eje del tiempo.
- **Requisitos de justicia (r23)**: el colega habla como PAR (jamás system/jefe — jerarquía de
  instrucciones limpia); su confiabilidad calibrada o contrabalanceada (si fuera un experto
  históricamente fiable, actualizar sería bayesianamente correcto); NUNCA "el colega siempre se
  equivoca" (enseñaría el reflejo opuesto); la autoridad como factor CONGELADO con varias
  redacciones (tono/nombre/prestigio no pueden dominar); verdad-por-suerte se neutraliza en la
  distribución apareada; medir por separado compras / modelo-pre-post / score (la autoridad
  puede cambiar el ESFUERZO sin cambiar la creencia).

### 1.C Influenciable, canal CONTENIDO — el sesgo por lo mostrado (priming)
- **Qué es** (aporte de Lucas, 2026-07-13): no hace falta que nadie te ORDENE nada — te
  MUESTRAN algo (una idea, un paper, una pista, un folklore) y la investigación entera se curva
  hacia eso: las hipótesis, las compras, la entrega. Se pierde el centro; se tira hacia lo que
  te pasaron, aunque nada lo respalde por encima de las alternativas.
- **Casos**:
  - **Los experimentos de pistas (evidencia propia)** `[VERIFICADO propio][AGÉNTICO]` — la
    pista textual HUNDIÓ al propio mundo que la daba (pares por seed −0.44) y hasta un PLACEBO
    de estilo movió el score. **Lectura honesta (corrección r24)**: esto prueba SENSIBILIDAD AL
    CONTEXTO brutal (el signo cambió entre réplicas; mucha varianza estaba en la entrega) — lo
    cual JUSTIFICA sondear el canal, pero NO establece todavía "priming epistémico": para eso
    falta el contraste apareado con creencia previa medida. Registro: pre-registro
    [ADR 0118](../adr/0118-v1.18-preregistro-experimento-pista-corregido-minimo.md) → autopsia
    [ADR 0121](../adr/0121-v1.21-autopsia-0118-metodo-de-pistas-retirado.md) → re-diseño y
    fase 1 [ADR 0129](../adr/0129-v1.29-autopsia-fase1-resultado-varianza-demostrada-t4-gana.md).
    El folklore de [first_story_v0](../../cases/first_story_v0/) ES este canal instrumentado.
  - **Confabulación anclada** — [Lathkar et al., arXiv 2604.25931](https://arxiv.org/abs/2604.25931)
    `[VERIFICADO en abstract; POR-LEER cuerpo]`: *"providing one confirmed intermediate fact…
    increases the model's confident-wrong-answer rate"*; escala con capacidad (ρ=0.900).
  - **El encuadre reescribe la percepción** — [Mitropoulos et al., arXiv 2603.18740](https://arxiv.org/abs/2603.18740)
    `[POR-LEER]`: el MISMO archivo pasa de ~97% de detección de vulnerabilidades a ~3.6%
    (GPT-4o-mini) con el marco "no tiene bugs" (números de la vía R4; el abstract confirma
    *"bug-free framing producing the strongest effect"* y ataque iterativo con 100% de éxito).
  - **La literatura mostrada captura la ideación** — [Chen, Zhao & Cohan, arXiv 2607.01233](https://arxiv.org/abs/2607.01233)
    `[VERIFICADO]`: dada la literatura mostrada, la ideación converge a puentes sobre ESO
    (conexión 47.1–64.2% en LLMs vs 12.1% humano; el thinking lo AGRAVA).
  - **El mismo código, otro relato** — [Shahriar et al., arXiv 2606.30587](https://arxiv.org/abs/2606.30587)
    `[POR-LEER]` (r24): código IDÉNTICO juzgado distinto según el contexto que lo rodea (halo,
    framing, anclaje) — el relato pesa más que el objeto.
- **Borde (afilado en r24)**: mostrar material relevante y usarlo BIEN es virtud (es
  evidencia); el vicio es que lo saliente-no-discriminante capture el plan. El factor se
  congela: mostrado-relevante vs mostrado-saliente-irrelevante, misma fachada. **Solo es
  REVISIÓN si había creencia previa medible**: si el contenido llega antes del primer modelo,
  es FORMACIÓN sesgada — se mide un modelo basal primero o se clasifica aparte. Y "pedile que
  lo reconsidere" tampoco es evidencia: la sola invitación a revisar, sin feedback externo,
  degrada ([Huang et al., arXiv 2310.01798](https://arxiv.org/abs/2310.01798) `[POR-LEER]`) —
  la pista no equivale a evidencia.

## El diseño justo (el mundo/los mundos del foco)

Factorial mínimo (r23 + canal-contenido): **{neutral / autoridad-social / contenido-mostrado} ×
{discriminante-real / no-discriminante} + línea de base sin influencia** — la cantidad que
importa es la INTERACCIÓN (cuánto cambia la política por la fuente/saliencia manteniendo fijo
el contenido probatorio). Nota del par por mínimo. La versión híbrida (r23-D) suma el vicio 9:
el colega adjunta una "verificación" que en un polo refuta de verdad y en el otro es de paja —
un solo esqueleto separa buen-uptake / sycophancy / tragarse-la-paja / buscar-el-discriminante.

**Camino firmado (ADR 0142)**: ANTES de construir física nueva, la SONDA por replay/fork
(maquinaria existente): ~20 estados de evidencia × 4 sufijos (neutral/autoridad ×
con/sin-evidencia), presupuesto ~US$5. **Criterio de muerte pre-registrado**: si la
autoridad-sin-evidencia no produce ≥20 puntos porcentuales más de updates dañinos que el
desacuerdo neutral (y pérdida ≥0.15 R), el polo social se mata antes de construir — y el foco
pasa al canal contenido (que ya tiene señal propia) o al cierre prematuro (predicción 50%).

**Calibración r24 (autocrítica de Codex sobre su 35%)**: el 58.19% de SycEval INCLUYE cambios
benéficos; el comparable con "update dañino" es el **14.66% regresivo**. El 35% queda firmado
por integridad del registro, pero ya no como prior bien fundado — el gate de +20pp / −0.15 R es
de verdad exigente.

**Refinamientos propuestos en r24 (A DECIDIR — no firmados)**: (1) el factorial único
{neutral/autoridad/contenido} no es un contraste causal limpio (todo mensaje social también
TRAE contenido) → **tres sondas APAREADAS** sobre la misma infraestructura de replay: social
({sin-fuente/par/autoridad} × {sin/con evidencia fuerte}, proposición idéntica) · contenido
({ausente/saliente-no-discriminante/discriminante} × dirección A/B, artefactos apareados en
largo/formato/prestigio) · rigidez ({propia/heredada/ninguna} × {refutación fuerte/presión
no-discriminante}; la PRIMERA prueba sin register — el panel mete confounds — register después).
(2) Métrica primaria: el MODELO ejecutable pre/post (tasa de updates dañinos · distancia a la
verdad · pérdida de R · la interacción); compras y prosa, mediadores secundarios. (3) "Un
experto diciendo algo ES evidencia": autoridad y neutral con igual historial/acceso — solo
cambia el envoltorio jerárquico. (4) n=20 de screening con extensión PRE-FIRMADA a n=40 si el
intervalo queda ancho; wording congelado. (5) Canal VIVO solo si: mueve el modelo ejecutable +
supera al control apareado + cuesta ≥0.15 R + el gemelo con evidencia legítima se mueve BIEN +
replica en un segundo mundo distinto. (6) **Presupuesto de falsación: UNA SEMANA** — 0/3 vivos
→ V1-en-compacto se mata para frontier; 1/3 → ese mecanismo solo, sin paraguas; vivos pero sin
transferencia → suite de fallas, no capacidad única. (7) La nota-por-mínimo: endpoint de
EVALUACIÓN (held-out), no señal inicial de RL — el peor canal aplastaría el gradiente.

## Sub-formas históricas (detalle previo, sigue válido)

- **1.1 No-incorporación** · **1.2 No-retractación del compromiso propio** · **1.3
  Actualización descalibrada** · **1.4 Fijación con reversión** · **1.6 Solo-confirmatoria** —
  ver casos arriba (rigidez). **1.5 Anclaje al primer número**: EN DISPUTA —
  [Vaccaro, arXiv 2606.11217](https://arxiv.org/abs/2606.11217) `[VERIFICADO]` (2.430
  especificaciones: el índice de anclaje va de fuerte-negativo a fuerte-positivo según el
  camino analítico → frágil) vs [Suri et al., arXiv 2305.04400](https://arxiv.org/abs/2305.04400)
  y [Lou & Sun, arXiv 2412.06593](https://arxiv.org/abs/2412.06593) `[POR-LEER]` (robusto;
  CoT / "ignorá el ancla" / reflexión no alcanzan) y
  [Localizing Anchoring Pathways, arXiv 2606.12818](https://arxiv.org/abs/2606.12818)
  `[POR-LEER]` (la confianza modula) — no es base de mundo hasta resolver leyendo.

## Estado en WAGER
- [first_story_v0](../../cases/first_story_v0/): control del polo-rigidez en frontier +
  instrumento del canal-contenido.
- El verbo register ([lab_largo_v0](../../cases/lab_largo_v0/)) habilita el compromiso-público
  (endurece 1.2).
- Los experimentos de pistas (ADRs 0118/0121/0129, links arriba) = evidencia propia del
  canal-contenido (re-leída como activo).
- **Próximo paso: la SONDA del canal social (arriba), con su criterio de muerte — y sobre la
  mesa de Lucas, los refinamientos r24 (tres sondas apareadas, semana de falsación).**
