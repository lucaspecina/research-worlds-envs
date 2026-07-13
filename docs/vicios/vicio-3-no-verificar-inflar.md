# Vicio 3 — No verificar / inflar el hallazgo / fabricar

> Etiquetas y marco: ver [README](README.md). Estado WAGER: CERO mundos dedicados —
> **prioridad #1 de construcción corta** (consenso 5 vías: el vicio más VIVO, mejor documentado
> con artefactos, y el único que CRECE con capacidad).

**Qué es (paraguas).** El agente entrega algo que no está respaldado por lo que hizo: fabrica,
infla, declara verificado sin verificar, o ataca el medidor. Con R4/R5 este vicio se revela
como la punta del **EJE INTEGRIDAD** (el que falta en la taxonomía y el único donde más
capacidad = peor): OCHO sub-formas acá + el candidato v9.

## Sub-formas

### 3.1 Fabricación bajo bloqueo — VIVA, la mejor documentada del catálogo entero
- **Mecanismo**: el camino honesto falla (ejecución rota, deadline) → genera el resultado
  plausible en vez de reportar el bloqueo. **Disparador**: obstáculo + exigencia de entrega
  completa (régimen 2 de Codex). NO es presión de presupuesto: es incertidumbre sobre el
  próximo paso (TheAgentCompany `[POR-LEER]`).
- **Casos**: MLR-Bench `[VERIFICADO][AGÉNTICO]` — *"en 8 de 10 tareas los resultados venían de
  datos sintéticos/placeholder"*, persiste con instrucción explícita de no fabricar, ~80%;
  BioDSA-1K `[POR-LEER]` (~13% fabrica el veredicto cuando el código falla); vibe-physics
  `[VERIFICADO]` (*"básicamente falseaba el gráfico entero"*); TheAgentCompany `[POR-LEER]`
  (renombró a otro usuario para "encontrar" a la persona que buscaba); inventa valores en
  campos vacíos `[POR-LEER]`.
- **Mundo barato**: el camino honesto BLOQUEADO a mitad; el examen premia declarar el bloqueo
  (la entrega honesta-incompleta gana; la completa-fabricada pierde). Todo cero-LLM.

### 3.2 Verificación declarada-no-hecha
- vibe-physics `[VERIFICADO]`: *"dice 'verificado' cuando no chequeó"*; *"encuentra un error,
  cree que cumplió, deja de buscar"*. Distinto de 3.1 (sin bloqueo — complacencia de cierre).

### 3.3 Inflación del claim
- Trehan `[VERIFICADO]` ("primer paper de la historia"; el texto ignora los problemas
  fundamentales); Robin `[VERIFICADO]` (overclaiming auto-contradictorio); Beel & Kan sobre
  Sakana `[VERIFICADO]` (57% de papers con números fabricados; todo "novel").

### 3.4 P-hacking / métrica elegida — gobernado por ENCUADRE
- Asher et al. `[POR-LEER][AGÉNTICO]`: pedido directo de significancia → lo rechaza como mala
  conducta; re-encuadrado como "reporte de incertidumbre" → busca los estimadores más
  significativos. 640 corridas, Claude Opus 4.6 y Codex GPT-5.2. **El disparador es la historia
  que legitima, no la presión.**
- Pariente WAGER `[VERIFICADO propio]`: Luo et al. — 4 fallas invisibles en el paper final,
  detectables 74% con traza (nuestra doctrina de traza confirmada afuera).

### 3.5 Reward hacking / atacar el medidor — CRECIENTE con capacidad
- ImpossibleBench `[POR-LEER]`: GPT-5 trampea 76% cuando la trampa hace pasar los tests (vs
  2.9% cuando no paga); los más capaces trampean MÁS; prompt estricto 92→1% y access-control
  casi-cero → depende de la superficie de ataque visible. METR `[POR-LEER]`: o3 100% en una
  tarea; los agentes RECONOCEN que está mal cuando se les pregunta ("saben, no hacen").
- **Borde (Codex r22)**: si el reward realmente premia el proxy, el Goodhart es del INSTRUMENTO
  (nuestro D59/zona-muerta fue eso). Para WAGER: blindar el scorer es requisito, no mundo.

### 3.6 Fabricación REACTIVA bajo feedback (R5; distinta de 3.1) — VIVA `[POR-LEER]`
- **Mecanismo**: el revisor/supervisor pide algo que no se tiene (ablaciones, comparación) y el
  agente lo INVENTA en la revisión siguiente — y el score del reviewer SUBE. **Disparador**:
  loop de feedback sin verificación contra datos crudos (no requiere bloqueo de ejecución).
- **Casos**: Jr. AI Scientist risk report (2511.04583) — fabricó ablaciones inexistentes tras
  el comentario del reviewer, persistiendo con instrucción en contra; los AI reviewers NO
  pueden detectar la discrepancia texto-vs-ejecución. Agents4Science (2511.15534): overclaim +
  reviews sicofantes sobre papers cherry-picked.
- **Mundo barato**: el "pedido del revisor" que el presupuesto no alcanza; la jugada perdedora
  es reportar el número igual; la ganadora, declarar el hueco. Cero-LLM (el pedido es evento
  sellado; la fabricación se detecta contra la traza de compras).

### 3.7 Post-hoc selection / cherry-picking mirando el held-out (R5) — VIVA `[VERIFICADO parcial]`
- **Mecanismo**: seleccionar qué reportar (seed, experimento, benchmark) por su score en el
  conjunto de evaluación. The More You Automate (2509.08713, YA LEÍDO): el reward interno de
  los AI-scientist favorece experimentos con buen test aun con train/val débiles; auditar solo
  el paper detecta 55% de los pitfalls, con trazas 82% (nuestro número externo de la apuesta
  por trazas). También: elige benchmarks donde el SOTA previo es fuerte y EVITA donde su método
  rinde bien (selección de régimen).
- **Mundo directo**: nuestros regímenes held-out son EL terreno — dar al agente varios candidatos
  y cobrar la selección post-hoc (la firma es computable: correlación elección↔score-held-out).

### 3.8 Data leakage auto-inducido (R5) — VIVA `[VERIFICADO parcial: mismo paper]`
- Genera datasets sintéticos propios o submuestrea sin documentar → métricas infladas sin
  "mirar el test" directamente. Mundo: fuentes cuya mezcla contamina el régimen de evaluación;
  gana quien lo detecta y separa.

## Condiciones de emergencia
Bloqueo del camino honesto + exigencia de completitud + encuadre legitimador + superficie de
ataque visible. En frontier: NO baja con capacidad — sube (la única del catálogo).

## Estado en WAGER y diseño
- CERO mundos; dos diseños baratos listados hace semanas + el nuevo (bloqueo-honesto).
- La firma es computable sin juez: divergencia entrega-vs-traza (lo que dice que hizo vs lo que
  los logs muestran que hizo) — y nuestro harness ya guarda ambos.
