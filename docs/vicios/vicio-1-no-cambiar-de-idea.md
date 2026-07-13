# Vicio 1 — No cambiar de idea ante la evidencia

> Etiquetas y marco: ver [README](README.md). Estado WAGER: `first_story` hecho y validado; el
> protocolo vicio-vivo dio "NO vivo en gpt-5.4" (1/8) → control de facto para frontier.

**Qué es (paraguas).** La evidencia está disponible o comprada y la creencia no se mueve — o se
mueve mal. Se parte en SEIS sub-formas con mecanismos distintos; dos están bien vivas en
frontier, una probablemente no existe robusta, y el polo espejo (moverse DE MÁS) está mejor
documentado que el vicio mismo.

## Sub-formas

### 1.1 No-incorporación de evidencia comprada (no-uptake)
- **Mecanismo**: la evidencia entra al contexto pero no a la decisión (nodo E sin arista a la
  hipótesis posterior). **Disparador**: evidencia ambigua o que exige re-trabajo; NO aparece con
  errores de ejecución inequívocos. **Firma**: computable — dato comprado jamás citado/usado
  aguas abajo ("Dead Step" de ProcCtrlBench `[POR-LEER]`). **Borde**: si el formato de entrega
  impide traducir la creencia, es integración (v8.6-Codex), no uptake.
- **Casos**: Corral/Ríos-García `[VERIFICADO][AGÉNTICO]` — *"evidence is ignored in 68% of
  traces, refutation-driven belief revision occurs in 26%"* (25.000+ corridas, 8 dominios;
  cita re-verificada 2026-07-12 contra el abstract; trazas navegables HF jablonkagroup/corral);
  caso concreto: recupera 20 isómeros incluyendo el correcto y nunca consulta la lista
  `[POR-LEER el caso puntual]`. OSWorld-V2 `[VERIFICADO][AGÉNTICO]` — *"pierde info que llega a
  mitad de tarea, tratándola como ruido de fondo"*. SciAgentGym `[VERIFICADO][AGÉNTICO]` —
  responde a solo 32.9% de las señales de error.
- **Contraevidencia**: feedback de ejecución duro SÍ se usa (self-debug casi duplica el éxito:
  16.7→32.4 en ScienceAgentBench `[POR-LEER]`). El vicio vive en la evidencia AMBIGUA.
- **Estado**: **VIVO** en frontier 2026. WAGER: la maquinaria de noticias lo instrumenta.

### 1.2 No-retractación del compromiso propio
- **Mecanismo**: la retractación depende causalmente de la "creencia interna" sobre la respuesta
  ya emitida; el compromiso público la endurece. **Disparador**: haber AFIRMADO antes (distinto
  de 1.1: acá hay autoría). **Firma**: verifica-que-está-mal y no corrige; o corrige el relato
  en vez del claim (vibe-physics: *"la Etapa 1 tiene 14 tareas, no 7"* `[VERIFICADO]`).
- **Casos**: "When Do LLMs Admit Their Mistakes" `[POR-LEER][VIÑETA]` (recall de retractación
  ≤25% aun sabiendo); Corral caso éster `[POR-LEER][AGÉNTICO]` (nota la discrepancia 6H-vs-3H y
  mantiene la estructura); RCA-cloud `[POR-LEER][AGÉNTICO]` (no revisa claims ante evidencia
  posterior; PDF guardado).
- **Estado**: VIVO. WAGER: nuestros mundos casi no generan compromiso público temprano — el
  verbo register (lab_largo) lo habilita. **Palanca de diseño directa.**

### 1.3 Actualización descalibrada
- **Mecanismo**: se mueve, pero sin proporción bayesiana (poco acoplada a la fuerza de la
  evidencia; a veces inflada). **Firma**: la magnitud del update no escala con la evidencia.
- **Casos**: BED-LLM `[VERIFICADO][AGÉNTICO]` (hipótesis incompatibles con lo YA observado,
  empeora con el historial); Miscalibrated Belief Updates `[POR-LEER][AGÉNTICO]`.

### 1.4 Fijación con reversión (la traza ve lo correcto y VUELVE)
- **Mecanismo**: el razonamiento intermedio identifica los rasgos de la respuesta correcta y la
  conclusión regresa a la hipótesis inicial. **Firma**: preciosa e inspeccionable — el momento
  exacto está en la traza.
- **Casos**: RadLE `[POR-LEER][AGÉNTICO-multimodal]` — *"although its intermediate reasoning
  briefly identified features of proximal femoral deficiency... it ultimately returned to its
  initial diagnosis"* (radiólogos 0.83 vs GPT-5 0.30); DeltaLogic `[POR-LEER][VIÑETA]` separa
  tres modos (aferrarse / colapsar / sobre-corregir).

### 1.5 Anclaje al primer número — EN DISPUTA, probablemente degradada
- Vaccaro `[VERIFICADO]`: 2.430 especificaciones y el índice de anclaje va de fuerte-negativo a
  fuerte-positivo según el camino del jardín de senderos → NO robusto. R1/R3 `[POR-LEER][VIÑETA]`:
  anclaje 22-61%, peor con capacidad, mitigaciones inefectivas; y 2606.12818: los modelos
  CONFIADOS resisten anclas. **Resolución probable**: depende de formato y confianza — sub-forma
  condicional, NO base de mundo hasta resolver la tensión leyendo.

### 1.6 Búsqueda solo-confirmatoria
- **Mecanismo**: elige el experimento que confirma, no el que discrimina. **Firma**: menú
  discriminante disponible y no usado (first_story lo instrumenta `[VERIFICADO propio]`).
- **Casos**: BED-LLM (45% naive vs 93% con diseño) `[VERIFICADO]`; nuestra mesa.

### El polo espejo (mejor documentado que el vicio): sobre-actualizar ante OPINIONES
- Sicofancia: 58.2% en casos médicos/matemáticos; *"creo que la respuesta es X"* induce acuerdo
  63.7% promedio; circuito mecanístico identificado (silenciarlo: 28→81%) `[POR-LEER][VIÑETA]`.
  Sobre-corrección: actualiza 2.5× más fuerte ante feedback contrario que ante apoyo
  `[POR-LEER]`. Confabulación anclada (2604.25931): UN hecho intermedio confirmado AUMENTA las
  respuestas confiadas-incorrectas; escala con capacidad `[POR-LEER]`.
- **EL PAR NUEVO (consenso R1+R5 + nuestra doctrina): sub-actualizar-ante-DATOS ↔
  sobre-actualizar-ante-OPINIONES (sicofancia epistémica).** Mismo canal superficial ("llega
  algo que contradice tu modelo"), polos opuestos según la fuente (evidencia vs testimonio).
  R5 lo eleva a cara B formal del vicio: SycEval 58.19% `[POR-LEER][VIÑETA]`; Agents4Science —
  reviews "groundbreaking... flawless" sobre paper cherry-picked `[POR-LEER][AGÉNTICO]`. Mundo:
  el "supervisor" robot empuja con autoridad/citas hacia la conclusión equivocada; ceder pierde;
  la firma computable = cambio de conclusión SIN evidencia nueva en la traza. Ningún benchmark
  explota la asimetría. **Candidato a contribución original de WAGER.**

## Estado en WAGER y consecuencias de diseño
- first_story queda como control (vicio de primera-historia NO vivo en gpt-5.4 en compacto).
- Diseño que las sub-formas piden: (a) compromiso público temprano (habilita 1.2 — register ya
  existe); (b) el par datos-vs-opiniones como DOS mundos con la misma fachada; (c) evidencia
  ambigua, no dura (1.1 vive ahí).
