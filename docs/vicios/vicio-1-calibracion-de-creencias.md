# Vicio 1 — La calibración de la revisión de creencias (EL PIVOTEO)

> **EL FOCO del proyecto (decisión de Lucas, 2026-07-13; ADR 0142).** Eje: Competencia.
> Etiquetas y marco: ver [README](README.md). Estado WAGER: `first_story` hecho (control del
> polo-rigidez en frontier; e instrumenta el canal-contenido vía folklore).

**Qué es (el paraguas).** UNA capacidad: mover la creencia **en proporción a la calidad de la
evidencia** — ni menos, ni más, sin importar de quién viene ni qué te pusieron adelante. El
pivoteo. Se mide como paraguas con sub-vicios SEPARADOS y **nota del par por el MÍNIMO, jamás
promedio** (r23: no son extremos de una sola perilla — un modelo puede ignorar datos Y obedecer
opiniones A LA VEZ, porque `actualización = peso-de-la-evidencia + peso-de-la-fuente +
sesgo-social`; compensar un defecto con el otro debe ser imposible).

**La distinción que gobierna todo** (r23): el testimonio y el material mostrado TAMBIÉN son
evidencia. Lo que separa virtud de vicio no es "datos vs opiniones" — es **¿lo que llegó
DISCRIMINA entre hipótesis, o solo es saliente/confiado/insistente?** Y solo cuenta como cambio
de creencia si cambia el MODELO/las predicciones — la prosa complaciente ("tenés razón…") sin
cambio de entrega es cortesía, no creencia.

## Los tres canales de falla

### 1.A Rigidez — no actualizar ante evidencia que discrimina
- **Mecanismo**: la evidencia entra al contexto pero no a la decisión. **Disparador**:
  evidencia AMBIGUA o que exige re-trabajo (con el error inequívoco de ejecución NO falla —
  self-debug duplica el éxito `[POR-LEER]`); compromiso público previo la endurece.
- **Sub-formas** (detalle histórico abajo): no-incorporación (1.1) · no-retractación del
  compromiso propio (1.2) · actualización descalibrada (1.3) · fijación con reversión — la
  traza VE lo correcto y vuelve (1.4) · búsqueda solo-confirmatoria (1.6).
- **Casos**: Corral `[VERIFICADO][AGÉNTICO]` — *"evidence is ignored in 68% of traces,
  refutation-driven belief revision occurs in 26%"* (25.000+ corridas; el agente recupera 20
  isómeros incluido el correcto y nunca consulta la lista; nota la discrepancia del doblete y
  entrega la misma estructura `[POR-LEER casos puntuales, trazas navegables]`). RadLE
  `[POR-LEER]` — el razonamiento intermedio identifica los rasgos correctos y VUELVE al
  diagnóstico inicial. OSWorld-V2, SciAgentGym, BED-LLM `[VERIFICADOS]`.
- **En nuestra mesa**: gpt-5.4 NO exhibe la forma primera-historia en compacto (1/8, control);
  DeepSeek SÍ (0.36→0.89 con advertencia). El polo no está muerto: está no-elicitado en
  compacto-frontier — las sub-formas 1.2 (con compromiso público, que el verbo register ya
  habilita) y 1.1-con-evidencia-ambigua quedan vivas como candidatas.

### 1.B Influenciable, canal SOCIAL — la sycophancy epistémica
- **Qué es**: abandonar una conclusión que tus datos respaldan porque alguien la contradice con
  seguridad/autoridad SIN aportar evidencia. (Sí: es la *sycophancy* — una de las conductas más
  estudiadas de toda la literatura LLM, la intuición de Lucas es correcta. Lo NUESTRO, que no
  existe: medirla en un agente CON evidencia comprada en mano, cobrada sobre el modelo
  entregado, y en PAR con la rigidez.)
- **Casos**: SycEval 58.19% `[POR-LEER][VIÑETA]`; *"creo que la respuesta es X"* induce acuerdo
  63.7% promedio (46.6-95.1 según familia) `[POR-LEER][VIÑETA]`; circuito mecanístico
  identificado (silenciarlo: 28→81% — controla deferencia, no conocimiento) `[POR-LEER]`;
  sobre-corrección 2.5× más fuerte ante feedback contrario que ante apoyo `[POR-LEER]`;
  Agents4Science `[POR-LEER][AGÉNTICO]` — reviews "groundbreaking… flawless" sobre paper
  cherry-picked; vibe-physics `[VERIFICADO]` — *"me daba la respuesta que yo parecía querer"*.
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
- **Casos — acá tenemos evidencia PROPIA fuerte** `[VERIFICADO propio][AGÉNTICO]`: los
  experimentos de pistas (ADRs 0117-0121): la pista textual HUNDIÓ al propio mundo que la daba
  (pares por seed −0.44) y hasta un PLACEBO de estilo movió el score — el contenido mostrado
  domina aunque no discrimine. El folklore de `first_story` ES este canal instrumentado (la
  historia plantada que el mundo cobra). Afuera: confabulación anclada `[POR-LEER]` — UN hecho
  intermedio confirmado AUMENTA las respuestas confiadas-incorrectas, escala con capacidad;
  framing de seguridad de código `[POR-LEER]` — el mismo archivo pasa de 97% de detección a
  3.6% según el marco declarado; Chen/Zhao/Cohan `[VERIFICADO]` — dada la literatura mostrada,
  la ideación converge a puentes sobre ESO (el thinking lo agrava).
- **Borde**: mostrar material relevante y usarlo BIEN es virtud (es evidencia); el vicio es que
  lo saliente-no-discriminante capture el plan. El factor se congela: mostrado-relevante vs
  mostrado-saliente-irrelevante, misma fachada.

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
pasa al canal contenido (que ya tiene evidencia propia) o al cierre prematuro (predicción 50%).

## Sub-formas históricas (detalle previo, sigue válido)

- **1.1 No-incorporación** · **1.2 No-retractación del compromiso propio** · **1.3
  Actualización descalibrada** · **1.4 Fijación con reversión** · **1.6 Solo-confirmatoria** —
  ver casos arriba (rigidez). **1.5 Anclaje al primer número**: EN DISPUTA (Vaccaro frágil
  `[VERIFICADO]` vs R1 robusto `[POR-LEER]`; 2606.12818: la confianza modula) — no es base de
  mundo hasta resolver leyendo.

## Estado en WAGER
- `first_story`: control del polo-rigidez en frontier + instrumento del canal-contenido.
- El verbo register (lab_largo) habilita el compromiso-público (endurece 1.2).
- Los experimentos de pistas = evidencia propia del canal-contenido (re-leída como activo).
- **Próximo paso: la SONDA del canal social (arriba), con su criterio de muerte.**
