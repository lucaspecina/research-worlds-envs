# Hallazgos — índice vivo de lo que fuimos viendo

> **Para qué existe** (Lucas, 2026-08-07: "vayamos anotando todas estas conclusiones para tener
> a mano cosas interesantes que fuimos viendo"). Una línea por hallazgo, con su alcance y el
> link al doc que tiene la evidencia completa (citas textuales, seeds, números). **Cómo se
> navega la casa**: este índice → el doc fechado de `docs/research/` con el detalle → si el
> hallazgo es evidencia de un vicio, su registro canónico vive en `docs/vicios/` (el tablero
> [`docs/vicios/README.md`](../vicios/README.md) es la síntesis). El estado del proyecto y el
> próximo paso viven SOLO en [`docs/roadmap.md`](../roadmap.md).
>
> **Convención**: cada doc nuevo de resultado/autopsia agrega su línea acá (titular CON alcance,
> ADR 0152). Esto es un índice: puntero y una frase — el contenido vive en el doc linkeado.

## Era programa de saltos (2026-08-05 →)

| Fecha | Hallazgo (titular con alcance) | Evidencia |
|---|---|---|
| 08-07 | **La juntura rota GENERALIZA al segundo operador — con tasa distinta** (mundo 2, régimen oculto: 2/5 salto espontáneo parcial vs 0/9 en mezclas; n=3/celda, 2 modelos, sin ayuda) — la "distancia-al-menú por operador" existe y es medible; gemelo 0/6 espurio | [resultado mundo 2](2026-08-07-resultado-smoke-count-regime-v0.md) · canónico: [vicio-4](../vicios/vicio-4-estructura-escondida.md) |
| 08-07 | **Nombra el candidato correcto y lo mata sin test** — DeepSeek ve la anomalía, compra más datos de ella, confirma, escribe "perhaps piecewise… two segments?" y entrega la suave llamando "outlier" al punto real; gpt re-etiqueta la discontinuidad como "muestra ruidosa" | [resultado mundo 2](2026-08-07-resultado-smoke-count-regime-v0.md) |
| 08-07 | **Primer mundo donde R premia el descubrimiento** (count_regime: oracle 1.0 vs rival suave 0.0; agentes que saltan 0.88-0.94 vs 0 los que no) — la deuda "R anti-rankea" era del diseño del mundo 1, no de R | [ficha](2026-08-07-ficha-mundo-count-regime-v0.md) · [resultado](2026-08-07-resultado-smoke-count-regime-v0.md) |
| 08-07 | **Zoom adaptativo de compra** — los que saltan conjeturan el umbral y compran grilla fina alrededor (9-10 velocidades); los que no, grilla gruesa (3-5); la conjetura precede al zoom en traza | [resultado mundo 2](2026-08-07-resultado-smoke-count-regime-v0.md) |
| 08-07 | **La comparación MANDADA se ejecuta como teatro** — orden explícita "ajustá ≥2 familias y compará" (sin contenido): los 3 válidos obedecen y comparan… dentro de su menú de siempre (NB vs ZINB con KS held-out incluido); **0/3 salta**. Mandar el acto no desbloquea un menú capturado — refutación pre-registrada de nuestra propia teoría "falta el acto" | [pre-registro](2026-08-07-preregistro-canales-vs-wording.md) · [resultado](2026-08-07-resultado-preregistro-canales-vs-wording.md) · canónico: [vicio-9](../vicios/vicio-9-overtrust-verificacion.md) |
| 08-07 | **Las puertas de la ayuda son por-modelo y ESTOCÁSTICAS** (n=4/celda) — robusto: gpt+concepto 4/4 y DeepSeek+receta 3/3 válidas; cruzado: 1/4 y 1/4 (ni cero ni regla); lo que rige es si el CANDIDATO entra al menú de hipótesis. Supersede el titular determinista "canales, no dosis" | [resultado del pre-registro](2026-08-07-resultado-preregistro-canales-vs-wording.md) · canónico: [vicio-1 §1.C](../vicios/vicio-1-calibracion-de-creencias.md) |
| 08-07 | **Verificación de paja en vivo** — gpt-5.4 con la receta en mano (3/4): la adjudica sin ajustarla, con chequeos que la rival también pasa y "parsimonia" en lugar del test; la evidencia discriminante IMPRESA en su propia salida y no procesada ("mirar sin ver") | [autopsia](2026-08-07-autopsia-canales-de-ayuda.md) · canónico: [vicio-9](../vicios/vicio-9-overtrust-verificacion.md) |
| 08-07 | **0/9 espontáneo** — nadie postula los grupos con el encargo justo (2 modelos, v0.2, seeds frescas); capturan persistencia (ICC≈verdad) sin discretitud (valle≈0) | [resultado](2026-08-07-resultado-smoke-count-mix-v0.md) · canónico: [vicio-4](../vicios/vicio-4-estructura-escondida.md) |
| 08-07 | **Casi nadie corre comparaciones de modelos** — 1 celda de 28 ajustó formalmente la alternativa; candidata a métrica conductual primaria (cero-LLM, de trazas) | [resultado](2026-08-07-resultado-smoke-count-mix-v0.md) · [auditoría §B1](2026-08-07-auditoria-critica-slice-count-mix.md) |
| 08-07 | **El shopping no es el cuello** — 11/12 compran el experimento discriminante (repeats) sin que nadie lo sugiera; la falla queda aislada en hipótesis/crítica | [resultado](2026-08-07-resultado-smoke-count-mix-v0.md) |
| 08-07 | **El gemelo bilateral funciona** — 0/10 espurio; ni las ayudas inducen clases fantasma (misma política correcta del otro lado = la escalera no mide obediencia) | [resultado](2026-08-07-resultado-smoke-count-mix-v0.md) |
| 08-07 | **R (energía) anti-rankea al descubridor** — captura 1.00 → R 0.712 vs 0.888/0.919 sin captura; deuda ADR 0026 para versión benchmark | [resultado](2026-08-07-resultado-smoke-count-mix-v0.md) |
| 08-07 | **Tres fallas de diseño cazadas por revisión** — stakes vacíos (el objetivo no requería el salto), estructura que no paga en extrapolación (ADR 0150), ancla débil que inflaba el "medio-salto"; lección: leer el brief con los ojos del agente racional | [auditoría crítica](2026-08-07-auditoria-critica-slice-count-mix.md) |
| 08-06 | **Ficha congelada del primer mundo de salto** (mezcla en conteos) + escalera de ayudas por niveles | [ficha](2026-08-06-ficha-mundo-count-mix-v0.md) |
| 08-05 | **Decisión de dirección** — máquina de saltos como línea primaria; taxonomía de saltos justificada (componente × edición, 10+1 operadores); revisión de creencias queda de paraguas | [menú estratégico](2026-08-05-menu-estrategico-y-maquina-de-saltos.md) · [fundamentos de la taxonomía](2026-08-05-fundamentos-taxonomia-de-saltos.md) |

## Eras anteriores

Los hallazgos de la era revisión-de-creencias (julio → 2026-08-02: 0/60 overstay, aplanamiento
de estructura latente, propagación/saliencia, cierre procedural ODE, etc.) están registrados
como bloques RESULTADO fechados en la sección *Estado actual* de
[`docs/roadmap.md`](../roadmap.md), cada uno con link a su doc de `docs/research/`; su evidencia
de vicios, en los docs de [`docs/vicios/`](../vicios/README.md).
