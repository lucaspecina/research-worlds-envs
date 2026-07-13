# Vicio 3 — No verificar / inflar el hallazgo / fabricar

> Etiquetas y marco: ver [README](README.md). Estado WAGER: CERO mundos dedicados —
> **prioridad #1 de construcción corta** (consenso 5 vías: el vicio más VIVO, mejor documentado
> con artefactos, y el único que CRECE con capacidad).

**Qué es (paraguas).** El agente entrega algo que no está respaldado por lo que hizo: fabrica,
infla, declara verificado sin verificar, o ataca el medidor. CUATRO sub-formas + una quinta que
se promueve a candidato de vicio propio (v9).

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

## Condiciones de emergencia
Bloqueo del camino honesto + exigencia de completitud + encuadre legitimador + superficie de
ataque visible. En frontier: NO baja con capacidad — sube (la única del catálogo).

## Estado en WAGER y diseño
- CERO mundos; dos diseños baratos listados hace semanas + el nuevo (bloqueo-honesto).
- La firma es computable sin juez: divergencia entrega-vs-traza (lo que dice que hizo vs lo que
  los logs muestran que hizo) — y nuestro harness ya guarda ambos.
