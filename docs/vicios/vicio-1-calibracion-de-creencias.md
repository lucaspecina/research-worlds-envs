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
from normative Bayesian updating"* (verbatim del abstract) `[LEÍDO cuerpo 2026-07-14: 2.58× confirmado (favorable 1.095×); ver-su-propia-respuesta
baja el cambio 32.5%→13.1% y DESAPARECE si la respuesta "es de otro LLM" — es identidad, no contenido]`.

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
- **Condiciones FINAS del disparo (3ª oleada: tres investigaciones externas, 2026-07-13 —
  crudos en `../research/2026-07-13-vicio1-investigacion-externa-{A,B,C}.md`; 21 IDs
  verificados título↔claim el mismo día)**:
  - **La evidencia tiene que ser MIXTA, no solo ambigua** — [Xie et al., arXiv 2305.13300](https://arxiv.org/abs/2305.13300)
    (ICLR 2024 Spotlight) `[POR-LEER][VIÑETA]`: ante contradicción ÚNICA y coherente el modelo
    es "camaleón" (se mueve); el sesgo confirmatorio aparece cuando llegan confirmación Y
    contradicción JUNTAS — elige la que confirma (*"strong confirmation bias when the external
    evidence contains some information that is consistent with their parametric memory"*).
  - **El auto-condicionamiento por la propia historia**: se sobre-compromete con el error
    temprano y fabrica justificaciones — pudiendo reconocer 67–87% de esas afirmaciones como
    falsas por separado ([snowballing, Zhang et al., arXiv 2305.13534](https://arxiv.org/abs/2305.13534)
    `[POR-LEER][VIÑETA]`); y el estado conductual previo se ARRASTRA turno a turno, más fuerte
    a mayor cercanía temática ([Old Habits Die Hard, Simhi et al., arXiv 2603.03308](https://arxiv.org/abs/2603.03308)
    `[POR-LEER]`).
  - **La variable escondida candidata: el COSTO DE RE-TRABAJO** (hipótesis de la vía A,
    testeable): el mismo modelo que se mueve gratis en QA ignora el 68% en agente — en QA
    actualizar es cambiar una palabra; en agente es re-modelar, tirar experimentos comprados,
    re-planificar. Nuestro mundo puede manipular ese costo como dial (evidencia que pide tocar
    UN parámetro vs re-estructurar el modelo entregable).
  - **Disparador NUEVO no catalogado: el mundo que CAMBIA debajo del agente** —
    [KellyBench, Grady et al., arXiv 2604.27865](https://arxiv.org/abs/2604.27865)
    `[POR-LEER][AGÉNTICO]`: temporada simulada de apuestas (500–1000 tool-calls); TODOS los
    frontier pierden plata (el mejor −8%) y fallan en adaptar la estrategia al fracaso —
    rigidez ESTRATÉGICA ante no-estacionariedad, distinta de la nuestra (mecanismo fijo +
    evidencia nueva). Candidato a arquetipo propio: "el mecanismo cambia a mitad del episodio".
  - **Separar creencia-no-movida de creencia-movida-acción-no**: el cuello frontier es la
    CONVERSIÓN evidencia→acción, no la adquisición ([RetailBench, arXiv 2606.15862](https://arxiv.org/abs/2606.15862)
    `[POR-LEER]`); y las confidencias declaradas contradicen las acciones — abandona respuestas
    de ALTA confianza bajo desafío y defiende las de baja ([Pal et al., arXiv 2511.13240](https://arxiv.org/abs/2511.13240)
    `[POR-LEER]`). Instrumento nuestro YA construido: el diff mecánico entre modelo provisional
    registrado (verbo register) y modelo entregado separa las dos sub-formas sin LLM.
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
    `[VERIFICADO — leído 2026-07-13][VIÑETA]`: 58.19% de sycophancy (regresiva — te empuja a lo
    incorrecto — 14.66%); **persistencia 78.5%** [77.2–79.8] a lo largo de la cadena de
    rebuttals; preventivo > en-contexto (61.75 vs 56.52); y **el rebuttal CON CITA es el que
    más empuja a lo incorrecto** (Z=6.59) — lo que PARECE evidencia persuade más que la
    persona (converge con el piso-sin-hablante y con nuestro nota>persona de la sonda 0143).
    Modelos 2024-25 (ChatGPT-4o / Claude-Sonnet / Gemini-1.5-Pro) — caveat generacional.
  - **When Truth Is Overridden** — [arXiv 2508.02087](https://arxiv.org/abs/2508.02087)
    `[POR-LEER][VIÑETA]`: una opinión simple del usuario ("creo que la respuesta es X") induce
    acuerdo con creencias incorrectas 63.7% promedio (46.6–95.1 según familia; 7 familias).
  - **El circuito de la deferencia** — [The Shared Sycophancy-Lying Circuit, arXiv 2604.19117](https://arxiv.org/abs/2604.19117)
    `[VERIFICADO — leído 2026-07-13]`: *"Silencing these heads in Gemma-2-2B flips sycophancy
    from 28% to 81% while factual accuracy moves only from 69% to 70%"* — *"the circuit
    controls deference, not knowledge"*: el modelo SABE que está mal y cede igual (12 modelos,
    1.5B–72B). (Resuelto: el 28→81 es de ESTE paper; el 63.7% es del de arriba.)
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
    `[VERIFICADO][AGÉNTICO-conversacional]` (r24 lo propuso; **LEÍDO 2026-07-13**): diagnóstico
    técnico interactivo sobre hilos reales resueltos; el usuario sugiere una causa EQUIVOCADA —
    desafío espontáneo: **Gemini 1/30, ChatGPT 2/30**; con chequeo de consistencia explícito
    sube a **28/30 y 27/30** (la capacidad está; el acto espontáneo no — la brecha
    reconocer↔ejecutar, cuantificada). Su agente evidence-first (hipótesis en competencia +
    preguntas + updating) casi duplica el diagnóstico (≈33→≈64). Caveats: el usuario lo simula
    un LLM, sin costo/presupuesto, sin modelo ejecutable entregado — el hueco nuestro sigue
    abierto. La cifra que manda diseño: **el mundo debe premiar el chequeo NO pedido**.
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
- **La 3ª oleada AFINA el canal (2026-07-13)**:
  - **EL CONFOUND MAYOR — la mayor parte de la "conformidad" NO necesita hablante**:
    [Hu et al., arXiv 2607.05545](https://arxiv.org/abs/2607.05545) `[POR-LEER]` — la misma
    respuesta afirmada SIN hablante explícito ya causa revisión dañina en el **66.5%** de los
    casos inicialmente correctos; la etiqueta social agrega un plus MENOR que ese piso.
    Consecuencia de diseño: **fuente y payload como factores ORTOGONALES** (mismo contenido
    con y sin hablante), o el "canal social" mide en realidad contenido.
  - **El PAR genérico puede ser DÉBIL en frontier**: la deferencia escala con la etiqueta de
    EXPERTO, no de amigo/par ([Bajaj et al., arXiv 2602.13568](https://arxiv.org/abs/2602.13568)
    `[POR-LEER]`: se mueve hacia el "experto humano" incluso cuando está mal); la refutación
    CASUAL persuade más que la crítica formal, y el razonamiento detallado persuade aunque
    concluya mal ([Kim et al., arXiv 2509.16533](https://arxiv.org/abs/2509.16533)
    `[POR-LEER]`); y NO es (solo) el RLHF: los modelos BASE flipean igual o más que los
    instruct ante el desacuerdo de pares ([Kumarappan et al., arXiv 2605.12991](https://arxiv.org/abs/2605.12991)
    `[POR-LEER]`). Justicia medible: la confiabilidad del par se ENSEÑA programáticamente
    (historial de aciertos observable — 50% = testimonio sin poder, 80% = testimonio que SÍ
    discrimina), jamás descripta ("es confiable").
  - **Contraevidencia que BAJA la predicción**: GPT-5 fue post-entrenado explícitamente contra
    la sycophancy (system card de OpenAI: prevalencia −69–75% en A/B; números del dossier
    externo, link a verificar) `[POR-LEER]`; el modelo acepta MENOS el contraargumento cuando
    su respuesta original era correcta (Kim et al., arriba) — y nuestro agente tiene 60
    réplicas encima: esperar tasas MENORES que las de viñeta. La escalada individual con
    contabilidad es racional también afuera ([Big-Muddy, Barkett et al., arXiv 2508.01545](https://arxiv.org/abs/2508.01545)
    `[POR-LEER][VIÑETA]`: *"strong rational cost-benefit logic with minimal escalation"* en
    decisión individual, N=4.000 — replica nuestro 0/60; el vicio social vive en la
    deliberación ENTRE PARES).
  - **Una vez cedido, persiste**: 78.5% de persistencia (SycEval, cuerpo — vía C) `[POR-LEER]`.

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
- **La 3ª oleada AFINA el canal (2026-07-13) — con la advertencia MÁS seria del foco**:
  - **El priming por mera saliencia SE ESTÁ MURIENDO en frontier cuando la relevancia se
    resuelve "desde el sillón"**. El linaje: una oración irrelevante degrada la resolución
    ([GSM-IC, Shi et al., ICML 2023, arXiv 2302.00093](https://arxiv.org/abs/2302.00093)
    `[POR-LEER][VIÑETA]`) → una cláusula que PARECE relevante tira hasta 65% a todos los SOTA
    ([GSM-Symbolic, Mirzadeh et al./Apple, arXiv 2410.05229](https://arxiv.org/abs/2410.05229)
    `[POR-LEER]`) → **NO sobrevivió la auditoría 2026**: re-generando y AUDITANDO los
    distractores, toda caída auditada es estadísticamente indistinguible de CERO en frontier —
    y los dos auditores frontier acordaron entre sí apenas κ=0.32
    ([Sturgeon, LessWrong 2026](https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail)
    `[POR-LEER]`). **Dos lecciones para nuestro mundo**: (1) el canal vive SOLO si la
    relevancia del material es IRRESOLUBLE sin investigar — la única forma de saber si el
    paper aplica tiene que ser COMPRAR el dato; la trampa griceana ("si me lo mostraron, por
    algo será") no se desactiva razonando, se desactiva investigando; y la entrega debe ser
    ecológica (carpeta heredada del equipo anterior — que "me lo dieron" no implique
    "importa"). (2) La celda "no-discriminante" NO puede certificarse por juicio (ni humano ni
    LLM: κ=0.32) — **se certifica COMPUTACIONALMENTE desde la verdad del mundo** (condicionar
    en el material mostrado no cambia la posterior sobre mecanismos ni el score alcanzable).
    Nosotros podemos; los benchmarks estáticos no. Va al certificado del mundo ANTES de
    construir.
  - **El vecino agéntico más cercano** — [When Context Hurts, Vigraham, arXiv 2605.04361](https://arxiv.org/abs/2605.04361)
    `[POR-LEER][AGÉNTICO; preprint de autor único, sin repo]`: en diseño multi-agente de
    software, un documento IRRELEVANTE rinde igual o mejor que todo artefacto relevante en
    varias tareas; el mismo artefacto mejora hasta 20× o degrada 46% según la tarea, y la
    dirección la predice UNA variable — la exploración de base sin contexto (r=−0.82). El
    material mostrado curva SIEMPRE; si para bien o para mal depende del estado del agente —
    validación independiente del principio de PARES.
  - **El TIMING y la política invisible**: la creencia PRE-CARGADA al inicio cambia la
    conducta del agente (−26.9% búsquedas, −16.9% fuentes únicas) mientras la persuasión a
    mitad de tarea hace poco — y el output final puede verse NORMAL con la política de
    exploración ya curvada ([Jeong et al., arXiv 2602.00851](https://arxiv.org/abs/2602.00851)
    `[POR-LEER][AGÉNTICO]`) → medir las COMPRAS, no solo la entrega. Y el material puede
    RE-ENTRAR por memoria/RAG ([MemSyco-Bench, Xiang et al., arXiv 2607.01071](https://arxiv.org/abs/2607.01071)
    `[POR-LEER]`).
  - **Advertencia [HUMANO]**: la analogía humana de ESTE canal es la más débil de las tres —
    el priming social conductual humano NO replicó (de 70 réplicas cercanas, 94% con efectos
    menores al original y solo 17% significativas en la dirección esperada — Mac Giolla et
    al. 2024, link a verificar). El efecto agéntico se demuestra de nuevo o no existe; no
    apoyarse en la analogía.

## ¿No está ya hecho? — los vecinos que miden actualización de creencias (pregunta de Lucas, 2026-07-13)

**Respuesta con el mapa en la mano: hay MUCHOS midiendo PEDAZOS; nadie mide nuestro objeto.**
- **Update bayesiano medido y hasta ENTRENADO** — [Qiu et al., arXiv 2503.17523](https://arxiv.org/abs/2503.17523)
  (Nature Communications) `[POR-LEER]`: *"LLMs fall far short of the standard defined by the
  Bayesian framework"* — y enseñarles a imitar al modelo bayesiano normativo mejora
  dramáticamente Y generaliza. **La objeción de review que nos regala, con su respuesta**: "si
  destilar Bayes lo arregla, ¿para qué mundos con reward?" → el teaching necesita un ORÁCULO
  normativo computable (posterior conocida); en investigación abierta no existe — la única
  señal disponible es la fidelidad en regímenes held-out, que ES WAGER. Regímenes
  complementarios; y un experimento-puente barato: ¿un modelo bayesiano-enseñado transfiere a
  un mundo WAGER con posterior tractable?
- **Creencia declarada vs ACCIÓN** — [Pal et al., arXiv 2511.13240](https://arxiv.org/abs/2511.13240)
  `[LEÍDO 2026-07-14]` (⚠ resuelto: título/autores confirmados — Pal, Flach, Liang, Potti,
  Goldblum; apuesta en dirección OPUESTA a su confianza declarada, no invoca la búsqueda con
  confianza ~0, y defiende lo que duda / suelta lo que confía — ver anatomía abajo). Y [Yang et al., arXiv 2505.16170](https://arxiv.org/abs/2505.16170) `[POR-LEER]`: la
  retractación la gobierna la creencia INTERNA momentánea (probe + steering causal).
- **Diseño experimental bayesiano en agentes** (lo que Lucas recordaba): BoxingGym
  ([arXiv 2501.01540](https://arxiv.org/abs/2501.01540) — prior-vs-no-prior, regret de
  información esperada) y BED-LLM ([arXiv 2508.21184](https://arxiv.org/abs/2508.21184),
  leído) — miden ELEGIR la pregunta; no manipulan una hipótesis rival ni cobran el modelo
  entregado. (CausaLab es OTRO vecino — SCM+presupuesto, vicios 2/7 — no éste.)
- **Los huecos DECLARADOS por las vías externas** (vía C, verbatim): *"NADIE manipuló una
  hipótesis inicial específica y competidora como variable experimental en un agente
  científico y midió el cambio downstream en el plan de compras/experimentos"*; y la
  distinción saliencia-vs-discriminancia *"NO está operacionalizada en ningún paper (ni
  siquiera en la literatura humana)"* — nuestro aporte más original Y nuestro mayor riesgo. El
  campo sigue desenredando el confound social-vs-contenido HOY (el paper del piso-sin-hablante
  es de julio 2026).

**Conclusión**: el objeto WAGER — agente con evidencia COMPRADA propia + modelo ENTREGADO
ejecutable cobrado en held-out + pares gemelos + cero-LLM en el reward + la INTERACCIÓN
fuente×discriminancia — **no está publicado**. Los vecinos aportan instrumentos de medición
(probes, pisos-sin-hablante, oráculos normativos) para VALIDAR nuestros mundos, no el
instrumento mismo. Métodos robables: `como-medimos.md` §3.

## La conclusión en llano (2026-07-14) — el fenómeno contado sin jerga

> Para entender el estado del conocimiento sin leer los 50 papers. Escrito a pedido de Lucas,
> en el idioma en que se lo contamos a él. La tabla con los detalles finos está en la sección
> siguiente; los números de cada paper, en [lectura-de-fuentes.md](../lectura-de-fuentes.md).

**Primero: el vicio NO es "los modelos ignoran la evidencia".** Cuando la contradicción es
limpia y única, la aceptan casi siempre (91-96% de las veces). Cuando el error es duro — el
código explota, el test falla — lo usan y lo arreglan (el self-debug casi duplica el éxito).
Ahí no hay vicio. Por eso las trampas baratas en mundos cortos no muerden: son versiones
demasiado limpias del fenómeno.

**El vicio aparece cuando se juntan tres cosas, y las tres tienen que estar:**
1. **Ya hay obra propia — y el agente sabe que es suya.** En el experimento de DeepMind, si el
   modelo ve su propia respuesta anterior se aferra (cambia de opinión 13% en vez de 32%)...
   pero si le dicen que esa misma respuesta la dio OTRO modelo, el efecto desaparece por
   completo. No defiende la idea: se defiende a sí mismo. Y el compromiso nace ridículamente
   temprano — en la primera palabra de la respuesta, antes de razonar (el snowball).
2. **La evidencia en contra llega sucia**: mezclada con algo que confirma, o discutible
   ("puede ser ruido del sensor"). Ante la mezcla elige leer la mitad que le conviene: con una
   pieza a favor y una en contra vuelve a su idea la mitad de las veces; con dos y dos, el
   99.8% (la tabla de Xie).
3. **Cambiar cuesta algo**: rehacer el modelo, tirar trabajo comprado, quedar mal con lo que
   ya firmó.

**Y aparece en un lugar preciso de la trayectoria: después del compromiso, con pico en el
momento de CERRAR.** El radiólogo digital ve el hallazgo correcto en su propio razonamiento y
en la conclusión vuelve a su primera idea. El químico escribe "esto no cuadra con mi
estructura" y la entrega igual. El apostador ajusta su modelo estadístico UNA vez al principio
de la temporada y nunca más — y llegó a escribir tres documentos de autocrítica diagnosticando
exactamente por qué perdía plata... y siguió apostando con el modelo roto.

**La conclusión más importante: la brecha entre lo que DICE y lo que HACE es el fenómeno
mismo.** Saben la estrategia correcta y no la ejecutan (Kelly escrito en el razonamiento,
apuestas planas en la mesa). Saben que su respuesta está mal — verificable — y no la retractan
(11-26%). Apuestan plata en dirección contraria a su propia confianza declarada. Pueden hacer
el chequeo si se lo pedís (28 de 30) y no lo hacen solos (1 de 30). Por eso la medición va en
TRES vistas separadas — qué declara, qué compra, qué entrega — y ninguna alcanza sola.

**El amplificador que no teníamos en el radar: identidad y consenso.** Solo y con contabilidad
delante, el modelo decide racional (casi cero escalada — igual que nuestro pozo 0/60). Pero
deliberando entre pares iguales: 99.2% escala la apuesta perdedora. Con la identidad fusionada
al proyecto ("hace 20 años que defendés esta división"): 97%. El gatillo no es la plata — es
la identidad y el consenso.

**¿Y los modelos de frontera?** Resisten las versiones baratas (nuestras sondas: 0/19 en
formación, 0/20 en el medio) pero los casos donde caen son de frontera y de este año: el
apostador es GPT-5.4 y Opus 4.6 (2026), el radiólogo es GPT-5, el químico es frontier. Lo que
los alcanza es la CARGA: trayectoria larga + obra propia + ambigüedad. Esa carga es
exactamente lo que el mundo v1 del pivoteo tiene que tener — y por diseño tiene.

## La anatomía REAL de los casos (relectura a texto completo, 2026-07-14 — orden de Lucas)

> 11 papers del núcleo leídos COMPLETOS hoy (fila por fila con números en
> [lectura-de-fuentes.md](../lectura-de-fuentes.md)); Codex corrió una lectura INDEPENDIENTE
> en paralelo para cruce de extracciones (r31). Esta tabla es el mapa de escenarios exactos:
> tarea · tamaño de trayectoria · lugar del flujo · gatillo · conducta observada.

| Caso | Tarea y tamaño de trayectoria | Lugar del flujo | Gatillo | Qué hace (lo real) |
|---|---|---|---|---|
| **Corral** (frontier, agéntico) | elucidar estructura química con herramientas, flujo multi-paso | mitad | **SU dato comprado** contradice (el doblete) | anota la discrepancia y entrega la misma estructura — ignora el 68% |
| **KellyBench** (frontier 2026, agéntico) | temporada de apuestas: ~100-150 fechas, 500-1000 tool-calls, sandbox propio | todo el arco post-ajuste | datos frescos cada fecha + pérdidas + **sus propios diagnósticos escritos** | ajusta el modelo UNA vez y nunca más; 3 autocríticas correctas + sigue con el modelo roto; Kelly escrito → apuestas planas |
| **RadLE** (GPT-5) | diagnóstico por imagen única, razonamiento largo | **transición hallazgos→conclusión** | sus hallazgos intermedios contradicen la 1ª hipótesis | ve lo correcto y concluye lo inicial (30% vs 83% radiólogos) |
| **Jeong** (chicos, agéntico) | agente web ≥5 fuentes → informe | la política entera, desde FORMACIÓN | creencia pre-cargada al inicio | −26.9% búsquedas, −16.9% fuentes, informe "fluido y plausible"; a mitad de tarea: débil |
| **Investigator** (conversacional) | diagnóstico técnico guiado sobre hilos reales | todo el diálogo | causa equivocada sugerida al INICIO y sostenida | desafío espontáneo 1-2/30; con chequeo pedido 27-28/30 |
| **Xie** (viñeta 1-turno) | QA con evidencia externa | — | contradicción **MEZCLADA** con confirmación | única coherente → acepta 91-96%; mixta 1+1 → vuelve a la suya 43-65%; 2+2 → 99.8%; orden ±49.5pp |
| **Kumaran** (viñeta 2-turnos) | binaria + consejo con precisión declarada | 2º turno | **ver su propia respuesta** / consejo contrario | cambia 13.1% vs 32.5% sin verse (desaparece si "es de otro LLM"); contrario sobre-pesado 2.58×; acantilado en confianza 0.77 |
| **snowball** (viñeta) | Sí/No + justificación (primalidad/grafos) | **el PRIMER token** | pregunta que exige cómputo secuencial | se compromete antes de razonar (95-98%) y fabrica justificaciones que reconoce falsas aparte (67-87%) |
| **Yang** (7-8B) | QA + continuación libre | inmediatamente post-respuesta | error propio que SABE incorrecto | retracta 11-26%; lo gobierna la creencia interna momentánea (steering la enciende/apaga) |
| **SycEval / speaker-free / circuito** (viñetas) | QA + rebuttals en cadena | post-respuesta | rebuttal con **CITA** / contenido afirmado sin hablante | regresiva 14.66% con persistencia 78.5%; sin hablante ya 66.5% (parecer-evidencia 80.4%); sabe-y-cede (28→81% con conocimiento intacto) |
| **Pal** (7 modelos) | confianza declarada vs acción (apuestas/tool/desafío) | la acción posterior | — | apuesta CONTRA su confianza; defiende lo que duda y suelta lo que confía; calibración estática no predice (r=0.17) |
| **Barkett** (o4-mini, N=6.500) | inversión Staw en 2 etapas | la 2ª decisión (reinversión) | **pares simétricos** deliberando / **identidad fusionada** | individual racional (~0 escalada; asesor 5.6%); pares 99.2%; identidad (20 años defendiéndola + acciones + reputación) 68.95% del presupuesto a la perdedora, 97.45% |
| **When Truth** (7-8B, viñeta) | MCQ un turno | ANTES de responder (**formación**) | "creo que la respuesta es X" | 63.7% acuerdo con lo incorrecto (46.6–95.1); la experticia declarada no suma (~4.4pp); 3ª persona −13.6pp |

**Las 7 condiciones recurrentes** (lo que el mundo calca):
1. **Obra propia visible e identificada como propia** (Kumaran: el efecto desaparece si "es de otro"; snowball: el compromiso precede al razonamiento; Corral/KellyBench: estructura/modelo ya elegidos; Barkett: identidad).
2. **Evidencia MEZCLADA o ambigua, jamás limpia** (tabla de Xie; el error duro SÍ se usa: ScienceAgentBench 16.7→32.4).
3. **Lugar: post-compromiso, pico en la transición a la conclusión/entrega** (RadLE; nuestro mapa de timing terminal 8.7-26%).
4. **Parecer-evidencia > quién-lo-dice** (la cita de SycEval; 66.5% sin hablante; nuestra nota>persona).
5. **La política se curva antes que el output** (Jeong; nuestras compras arrastradas 7/19 en formación) → medir COMPRAS siempre.
6. **La brecha dice-hace ES el fenómeno** (KellyBench autocríticas+modelo-roto; Pal; Yang sabe-no-retracta; circuito sabe-y-cede; Investigator puede-y-no-chequea) → tres vistas obligadas: declara / compra / entrega.
7. **Amplificadores documentados: consenso entre pares (99.2%) e identidad fusionada (97.45%)** (Barkett) — candidatos v2.

**Dónde NO aparece** (contraevidencia, sellada): contradicción única y coherente (Xie) · error duro de ejecución (ScienceAgentBench) · decisión individual fría con contabilidad (Barkett, replica nuestro 0/60) · señuelo barato suelto en mundo corto (nuestras sondas: formación 0/19 · medio 0/20 · terminal 8.7-26%).

**Eje de honestidad generacional/formato**: los porcentajes escandalosos de viñetas vienen mayormente de modelos chicos abiertos y un turno (When Truth, Yang, Jeong, circuito); frontier resiste lo barato (nuestras sondas) pero **cae en los casos con carga real** (KellyBench = GPT-5.4/Opus 4.6 en 2026 · RadLE = GPT-5 · Corral = frontier). La carga — largo + obra propia + ambigüedad — es lo que iguala.

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

**Y la 3ª oleada AGREGA a la mesa (a decidir junto con lo anterior)**: (8) **sonda v2 "de
descomposición"** — los mismos ~20 estados, SEIS brazos: sin-mensaje · nota-sin-hablante ·
par-neutral · par-autoridad × con/sin-evidencia donde aplica — un solo experimento (~US$8–10)
separa el PISO del contenido (66.5% en viñeta) del PLUS social, y disuelve la disputa de orden
(las vías B y C dicen "contenido primero"; r24 dijo "social como está firmada" — la v2 mide
ambos a la vez sin romper el pre-registro: los 4 brazos firmados son subconjunto). (9) El
**certificado de no-discriminancia COMPUTACIONAL** antes de construir el mundo del canal
contenido (lección GSM-NoOp: sin él la celda "no-discriminante" es atacable — a dos frontiers
auditando les dio κ=0.32; nosotros lo computamos desde la verdad del mundo). (10) Expectativa
re-calibrada: el plus social probablemente CHICO en frontier (GPT-5 post-entrenado en contra;
el par genérico débil; el agente con datos propios protege) y el piso de contenido
probablemente GRANDE — la sorpresa esperable es que el canal de Lucas (contenido) sea el
principal. (11) **El brazo-PISTA como control de capacidad (directiva de Lucas, 2026-07-13:
las pistas NO se descartan)**: en toda sonda y todo mundo del foco, un brazo extra con el
chequeo PEDIDO explícitamente ("verificá la consistencia antes de entregar") — si CON pista
acierta y SIN pista cae, el mundo capturó la ausencia del acto espontáneo (el vicio), no una
falta de capacidad. Es nuestra lógica de pistas de siempre (la pista dirigida al vicio AÍSLA
el vicio — validez replicada en 2 modelos, ADRs 0097/0098/0110; lo retirado en ADR 0121 fue UN
protocolo de medición ruidoso, no el método), y ahora con la cifra externa exacta: desafío
espontáneo 1-2/30 vs 27-28/30 con el chequeo pedido
([LLM-as-an-Investigator](https://arxiv.org/abs/2606.13220), leído).

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
- Los experimentos de pistas (ADRs 0118/0121/0129, links arriba) = evidencia propia de
  sensibilidad al contexto (justifica la sonda del canal-contenido).
- Crudos de la 3ª oleada: `../research/2026-07-13-vicio1-investigacion-externa-{A,B,C}.md`
  (+ Codex r24 en `../research/2026-07-13-codex-r24-foco-vicio1-mapa-evidencia.md`).
- **SONDA 0143 CORRIDA Y CERRADA (2026-07-13 noche; [resultados](../research/2026-07-13-sonda-0143-resultados.md),
  ADR 0144; 156 celdas, 23 donantes, 2 mundos, ~US$7)**: **K1 ROJO** (el estatus agrega +4.3pp,
  no 20) · **K2 ROJO** (EL CONTENIDO DOMINA: la nota sin firma daña 8.7% sellado / 26%
  exploratorio, vía MEZCLAS DE COMPROMISO — "la nota es evidencia débil, PERO con n chico la
  unificación parcial es atractiva" — mientras las personas dañan 0-4%) · **K3 VERDE** (la
  pista de Lucas rescata 23/23 y hasta mejora la media) · K4 no (la influencia existe, chica,
  concentrada en la nota). Colaterales: el consejo VERDADERO también se ignora (0/18 — el
  anti-sycophancy sobre-generalizado: "usar el consejo cuando discrimina" hoy no pasa);
  first_story con entrega bimodal (inestabilidad de mundo, a revisar). Predicciones: Codex
  clavó nota y pista; ambos sobreestimamos las personas.
- **Pivote PRE-AUTORIZADO ejecutado (ADR 0144)**: mundo del colega-autoridad DESCARTADO; el
  foco de construcción pasa a ESTE canal (1.C).
- **SONDA DE FORMACIÓN 0145 CORRIDA Y CERRADA (misma noche; [resultados](../research/2026-07-13-sonda-0145-resultados.md),
  ADRs 0145/0146; 100 episodios frescos, ~US$9)**: la nota falsa SOLA al arranque NO muerde
  (0/19 daños, 0 adopciones, 0 caídas de cobertura — canal débil sellado); la VERDADERA
  arrastra compras (7/19) sin pagar ("el contenido como prior, no como vicio"); y el hallazgo
  nuevo: **CAPTURA DE AGENDA** (sub-forma candidata, exploratoria) — pista+falsa produce
  colapsos severos (hasta −0.88) SIN adopción: el agente RECHAZA el claim con datos pero la
  verificación le come el presupuesto (*"la evidencia rechaza claramente la unificación, PERO
  con una sola campaña ya no puedo estimar las cuatro formas"*). La pista queda especificada
  POR TIMING: protege en la entrega (23/23), doble filo en formación con material falso.
- **EL MAPA (0143+0145) — INCOMPLETO, corregido por Lucas**: las dos sondas midieron las
  PUNTAS (arranque 0/19; entrega 8.7-26% por mezclas de compromiso) porque eran las baratas —
  pero **el MEDIO, donde los casos reales reportan el vicio (Corral compra el espectro a mitad
  de flujo; el usuario del Investigator sugiere DURANTE el diagnóstico; vibe-physics empuja a
  mitad de sesión; las cadenas de SycEval son mid-conversación), quedó sin medir**. La
  hipótesis mecánica (re-abrir caro → conceder barato) predice medio ENTRE las puntas; la
  chequeabilidad barata del medio predice lo contrario. Lo decide la **sonda 0147 (medio)**.
- **SONDA DEL MEDIO CORRIDA Y CERRADA (misma noche; [resultados](../research/2026-07-13-sonda-0148-resultados-medio.md),
  ADRs 0148/0149; 120 celdas, ~US$10)**: en el medio la nota falsa NO toca NADA (0/20 daño;
  compras idénticas a los controles 19/20 — métrica potente); la VERDADERA induce chequeos
  GENUINOS (3-4/20, cajones que ningún control compró, entrega correcta — el único momento del
  mapa donde el material bueno se usa); la pista en el medio inocua-a-positiva (la captura era
  específica de formación).
- **EL MAPA DE TIMING COMPLETO (ganado, no asumido — la corrección de Lucas)**: formación
  0/19 · **medio 0/20 (el momento FUERTE: el plan propio protege; ahí vive la virtud)** ·
  entrega 8.7-26% (mezclas de compromiso — el único momento donde re-abrir es caro y conceder
  es la salida barata). La vulnerabilidad del canal contenido en frontier-compacto es
  ESPECÍFICA DE LA REVISIÓN TERMINAL.
- **El mundo del foco queda determinado por DATOS (ADR 0149, GO de Lucas pendiente)**:
  nota-señuelo en la RONDA FINAL (donde muerde) — par: discrimina-de-verdad (incorporarla gana;
  hoy nadie la incorpora: headroom real) vs saliente-sin-respaldo (conceder mezcla pierde —
  firma medida); + nota-de-medio VERDADERA como oportunidad puntuable (la virtud con headroom:
  3-4/20 espontáneo). Firmas = las clases de las sondas; esqueleto v2 + eventos D4; días.
