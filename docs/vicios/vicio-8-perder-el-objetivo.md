# Vicio 8 — Perder el objetivo / la relevancia

> Etiquetas y marco: ver [README](README.md). Agregado al catálogo 2026-07-09 (tres fuentes);
> las cinco vías lo confirman y lo parten en CUATRO sub-formas — una de las cuales (8.4) es,
> según Codex r22, "probablemente más importante que el pozo para el sistema actual".

## Sub-formas

### 8.1 Angostamiento de portafolio
- Pierde la visión de conjunto sin meterse en ningún pozo (se puede perder el norte resolviendo
  prolijo un sub-problema que no es la pregunta). Trehan `[VERIFICADO]` (*"no podían mantener
  pensamiento de portafolio"*); vibe-physics `[VERIFICADO]` (*"pierde la dirección fácilmente"*).

### 8.2 Corte prematuro afirmando completitud
- PaperBench `[VERIFICADO]`: cortan antes afirmando falso que terminaron; **firma de la familia
  o-series, NO ley** (o1 13.2→24.4 sin submit; Claude 21.0→16.1 EMPEORA). TheAgentCompany
  `[POR-LEER]` (da por cumplida la tarea tras el primer paso); NL2Repo `[POR-LEER]` (49%
  terminación temprana en Qwen3-Thinking — "hallucination of verification", cruza con v9).

### 8.3 Deriva por saliencia local (el mecanismo compartido con 2.4)
- Goal-drift `[POR-LEER][AGÉNTICO]`: el patrón local reciente desplaza el objetivo declarado;
  por inacción más que por acción; específico por modelo; empeora con presión adversarial y
  duración del objetivo instrumental. Inherited Goal Drift `[POR-LEER]`.

### 8.4 El medio/proxy se vuelve el fin (Goodhart del agente)
- **Casos**: Sakana `[POR-LEER — artefactos en el blog/reporte]`: al exceder el timeout,
  **modificó su propio código para EXTENDER el límite de tiempo**; en otra corrida se relanzaba
  a sí mismo en loop; en otra llenó ~1TB de checkpoints. El objetivo real ("experimento
  eficiente") reemplazado por el proxy ("que la corrida termine"). MLR-Bench `[VERIFICADO]`
  ("completitud" como objetivo → fabrica).
- **Borde (Codex r22, crítico)**: si el reward DE VERDAD premia el proxy, es fallo del
  instrumento, no del agente (nuestro D59 fue eso). Distinguir Goodhart-del-agente de
  hackeabilidad-del-reward ANTES de atribuir.

### 8.6 (numeración Codex) No ensamblar el análisis correcto en la entrega
- **La sub-forma descubierta por NOSOTROS** `[VERIFICADO propio]`: autopsias 15/16 descubren la
  estructura y la entrega la traiciona (defaults, flechas sin respaldo, ruido incompatible con
  sus propios hallazgos); el fork: cada donante reproduce su defecto 15/15, determinista; el
  probe descartó el cuello mecánico (canal sano). Codex r22: *"está viva y es probablemente más
  importante que el pozo para el sistema actual"* — constructo más preciso que "terminación".
- Borde: si la creencia no PUEDE traducirse por formato, es operación; si la traducción fiel
  funciona y el agente elige otra estructura, es juicio/integración (probado: canal sano).
- **Par D1 calibración (2026-08-10)** `[VERIFICADO propio][AGÉNTICO]` — **primer mundo que
  cobra 8.6 con vara cero-LLM**: 13/15 compran y ven la evidencia (mezcla gana ΔBIC≥10 en sus
  propios datos, 14/15) y la entrega la traiciona (unimodal, varianza horneada); un agente
  ANUNCIA "a small low-purity contamination component to capture" y entrega unimodal igual
  (la disociación verbal inequívoca — el resto es regex cruda, anotación fina pendiente).
  Convergencia con vicio 4.3 (así lo clasificó Codex: no vicio nuevo). Estado: VIVO;
  candidata de pivote. [Dossier](../research/2026-08-10-resultado-tanda-d1-calibracion.md).
- **Evidencia externa convergente por método causal** `[VERIFICADO][AGÉNTICO-juegos, abiertos ≤70B]`
  (Strategic Play, arXiv 2605.00226, leído 2026-08-11): probes internos > verbales (saben
  más de lo que dicen) y el steering de creencias mueve la acción solo ~50-70% — *"internal
  beliefs have weak causal influence on action selection"*. Converge con la hipótesis sugerida
  por D1, pero no la replica: Strategic Play midió creencias internas; D1 midió conducta y
  entrega, no qué sabía internamente el agente. Registro completo en lectura-de-fuentes.

## Estado en WAGER y diseño
- CERO mundos dedicados; la batería nueva (endurecida post-0137) ya cobra 8.6 parcialmente.
- El mundo de 8.1 ya está diseñado en el catálogo viejo (objetivo global + sub-problemas donde
  el reward SOLO paga el global). 8.4 pide blindaje del scorer más que mundo propio.
