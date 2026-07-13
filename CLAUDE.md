# CLAUDE.md — WAGER

Operativa del repo para Claude Code.

**▶ Al arrancar una sesión**: leé **`docs/roadmap.md`** (sección *Estado actual*, que incluye el próximo paso)
para saber dónde estamos y qué sigue — es la única fuente de verdad del estado. Si no conocés el proyecto, leé
**`WIKI.md`** primero.

Mapa de docs (abrí el que la tarea pida, no todos):

- **`WIKI.md`** — entender de cero, sin jerga: qué es, cómo funciona, dónde estamos.
- **`ARCHITECTURE.md`** — índice de la referencia técnica → **`docs/reference/`** (contratos, operadores, rivales, batería, scoring, harness; abrí el archivo del tema).
- **`docs/roadmap.md`** — estado vivo + cartera E1 + programa E1→E4 (dónde estamos, qué falta, el plan).
- **`docs/failure-modes.md`** — el corazón. La **definición operativa** del juicio (§0, dos polos) +
  el catálogo de failure modes (vicios) Y operaciones de aha, de a **PARES**, + scaffold de diseño
  (de un vicio/aha documentado → un mundo puntuable; taxonomía por dinámica de mundo).
- **`docs/vicios/`** — la DESCOMPOSICIÓN FINA de cada vicio (ADR 0140): un doc por vicio con sus
  **sub-formas** (mecanismo · disparador · firma · borde operación/juicio) y casos reales
  etiquetados (verificación × tipo-de-evidencia × estado generacional). Su **`README.md` es EL
  TABLERO**: la vista de síntesis para razonar el conjunto (estado de todos en una tabla + marco
  transversal + cola de lecturas + contrato de mantenimiento con su tabla de gatillos).
  **La evidencia nueva de vicios entra SOLO acá.** Guardia de consistencia en pre-commit
  (`tests/test_vicios_consistency.py`): un doc olvidado o desincronizado ROMPE el commit.
- **`docs/mundos-por-vicio.md`** — la derivación oficial vicio→mundo EN LLANO (ADRs 0113/0114):
  por cada vicio, sus estructuras y el mundo que lo caza (exista o no) + estado de los mundos.
  **Catálogo-primero: lo construido no manda.** El fenómeno fino vive en `docs/vicios/`; este
  doc deriva mundos.
- **`docs/lectura-de-fuentes.md`** — registro AUDITABLE de qué papers/artículos de fallas de AI
  researchers se leyeron a TEXTO COMPLETO (con cita real), qué falta, y las correcciones que la
  lectura destapó (ADR 0115). Evidencia cruda de las búsquedas: **`docs/research/`** (JSON).
- **`docs/como-medimos.md`** — el problema más difícil: CÓMO se mide (cada vicio, cada aha, la
  generación de ideas). Registra el MÉTODO de medición de cada paper que mide juicio + la reflexión
  para WAGER (distinción medir-para-describir [juez-LLM validado OK] vs medir-para-premiar [cero-LLM]).
- **`docs/adr/`** — decisiones (una por archivo, append-only)
  · **`docs/open-questions.md`** (lo sin decidir) · **`docs/red-team.md`** (amenazas del proyecto)
  · **`docs/archived/`** (histórico; el `NORTH_STAR_full.md` original vive acá — citas "NORTH_STAR §N" resuelven ahí).

**Jerarquía de autoridad**: Ethos (Reglas duras, abajo) > `ARCHITECTURE` > `docs/adr/` > issues > código.
El código nunca contradice los docs en silencio: si la implementación revela un error de diseño, se
propone la edición del doc + un ADR nuevo en `docs/adr/`.

## Reglas duras

- **JAMÁS un LLM en el cómputo del reward.** Si una solución lo requiere, frenar y discutir. Se protege con
  **test de CI que falla el build si hay llamadas a LLM en el reward path** (ARCHITECTURE §13-L0). Ídem sandbox:
  tests que intentan escapar y deben fallar cerrado (`tests/test_sandbox_redteam.py` = el checklist).
- **Integración LLM primero** (ADR 0014): todo subsistema con superficie hacia un LLM tiene como PRIMER milestone
  un smoke con LLM real del camino más fino — nunca como último. El reward path sigue cero-LLM (excepción que no
  se mueve con el apuro).
- Todo mundo nuevo pasa la **escalera de verdades degradadas** (ARCHITECTURE §13-L1) + sus **certificados**
  (ARCHITECTURE §7, carga diferencial ≥2 coordenadas) antes de entrar a una suite.
- Las conductas del agente se **observan** (traces, firmas), nunca se premian (el vicio se vuelve la jugada
  perdedora del mundo; el juez cobra la consecuencia).
- **FIDELIDAD A LOS CASOS REALES** (Lucas 2026-07-13, regla dura): los mundos y experimentos reproducen los
  fenómenos **como aparecen en los casos reales reportados — en sus condiciones, situaciones y momento del
  flujo** (con los links de esos casos citados en el diseño). La conveniencia de implementación NO es criterio
  de diseño; toda desviación de las condiciones reportadas se declara y justifica en el pre-registro.
- Rivales y batería se **derivan** del caso declarado en `meta.json`; nunca se autorean a mano por caso.
- La librería de operadores **crece a demanda de semillas reales**, nunca por imaginación suelta. El solver jamás
  ve la taxonomía de operadores.
- Casos con semilla investigativa: **test de contaminación obligatorio** antes de certificar; trasplante cruzado
  de dominio por defecto para semillas famosas.
- El handle del mundo es **opaco server-side**: el agente jamás lee `world.py`, `battery.json` ni `ladder/` (anclas/rivales).
  El brief lo escribe un proceso **ciego** a batería y rivales (anti-leak).

## Workflow

- Unidad de avance: el **slice vertical más chico** que ejercite el reward path completo (mundo → episodio →
  submission → score). El orden lo define la escalera experimental (`docs/roadmap.md`).
- Tests de wiring por componente; tests E2E con LLM real solo cuando el wiring está verde.
- Toda decisión de diseño no trivial → **ADR nuevo** en `docs/adr/` (fecha — decisión — razón).
- Open questions nuevas → `docs/open-questions.md` (inbox); al resolverse, migran a un ADR con su resolución.
- **Checklist de supersesión** (regla dura, ADR 0030): todo ADR que **supersede** una decisión previa hace
  **grep de la regla vieja en TODOS los docs** y enumera cada ubicación que edita. Principio **"una regla, una casa"**.
- **Auditoría código-vs-docs por iniciativa propia**: ante una inconsistencia, **reportar con ubicación exacta +
  fix propuesto, nunca arreglar en silencio**; aplicar recién con aprobación.
- **LEDGER DE PENDIENTES ABIERTOS** (ADR 0086, reclamo repetido → estructura): todo reporte de
  cierre a Lucas TERMINA con el ledger — pre-registros firmados sin correr, autopsias sin
  partir, GOs sin ejecutar — cada ítem tildado ✓ o explícitamente VIVO con su próximo paso.
  Un pendiente que no aparece en el ledger es un pendiente caído en silencio.

## Codex (GPT-5.6 Sol) — segunda opinión / pensar juntos (ADR 0116)

Codex es un **compañero de pensamiento y crítica**, NO un escritor de código. Su rol es **segunda
opinión, crítica y pulido de ideas** en cuestiones de **diseño / reflexión / análisis** — una tercera
lectura independiente (como el "otro feedback"), no un ejecutor. **También sirve para criticar y ayudar
a DIRECCIONAR el CORE del proyecto** — su dirección, su rol, su objetivo — y proponer mejoras,
**pivoteos o cambios grandes**, no solo decisiones puntuales.

- **Cuándo consultarlo**: ante una **decisión importante y no trivial** (diseño, interpretación de un
  resultado, repensar un enfoque, pulir una idea), o **cuando Lucas lo pide**. Claude puede
  **preguntarle a Lucas "¿querés que le consulte a Codex?"** antes de hacerlo. **JAMÁS para que
  escriba el código** — la solución la pensamos y la escribimos nosotros; a Codex se le pide *pensar
  la solución, analizar, criticar, reflexionar*.
- **Cómo — sesión PERSISTENTE (ida y vuelta con memoria, no mensajes aislados)**: modelo
  `gpt-5.6-sol` / esfuerzo `max` (default en `~/.codex/config.toml`; el ID correcto es **`gpt-5.6-sol`**,
  NO `gpt-5.6`, que el login ChatGPT rechaza). Arrancar con `codex exec --skip-git-repo-check "..."`
  y **continuar la misma sesión** con `codex exec resume --last "..."` — retiene todo el hilo.
- **La dinámica buscada**: que Codex CRITIQUE lo que estamos haciendo y genere el ida-y-vuelta que
  pule la idea. Lo que diga Codex se le reporta a Lucas **en llano** (memoria *comunicar-sin-jerga*).

## Referencia SREG — política de cuarentena

El repo SREG (proyecto anterior, mismo autor) es **referencia de SOLO LECTURA** en:
`C:\Users\YT40432\Desktop\lp\research\lucaspecina\synthetic-research-envs`.

- **Spec-first**: SREG se consulta SOLO cuando el spec WAGER del componente ya está escrito y aceptado. Responde
  "cómo implemento este spec", nunca "qué debería ser el spec".
- **Allowlist** (portear con mínima cirugía): kernel Jupyter persistente, cliente LLM Azure (fixes multi-turn de
  la Responses API), patrones de contratos Pydantic, maquinaria anti-leak, scaffolding de repo y tests.
- **Cirugía obligatoria** (reescribir contra el spec WAGER): digestion agent, architect + lints, validators.
- **Denylist** (NO leer — es la filosofía que matamos): evaluator/judge, restos del compiler NL↔IR, scoring por
  rubrics/SQ, formatos de claims. **Portear deliberadamente, nunca importar por arrastre.**

## Convenciones

- **Hook de pre-commit obligatorio** (ADR 0049): `git config core.hooksPath hooks` tras clonar — corre los lints
  de trazabilidad/secciones + la guardia de ADRs ANTES de que la deriva entre a la historia (el CI es 2ª red).
- **Docs constitucionales solo con herramientas quirúrgicas** (ADR 0056): `WIKI`/`ARCHITECTURE`/`CLAUDE` se editan
  con Edit/Write puntuales, JAMÁS con scripts bulk de regex. Los **ADRs son append-only** (archivos existentes
  inmutables; superseder = archivo nuevo) y el pre-commit lo verifica (`scripts/check_decision_log.py`).
- **Guardias con autotest** (ADR 0057): toda guardia nueva llega con su par should-pass/should-fail corrido ANTES
  de instalarse.
- **MODO AUTONOMÍA** (Lucas, 2026-07-05): tramos designados se ejecutan DE CORRIDO — guardias con salida en
  doctrina existente se resuelven/registran/siguen; los pre-registros los firma Claude ANTES de mirar.
  **Tripwires (únicos frenos)**: (1) semántica del reward path o de anclas, (2) frontera cero-LLM, (3)
  contradicción de pre-registro firmado que exija tocar algo certificado, (4) gasto material de API/infra fuera
  del alcance ordenado. El siguiente mensaje a Lucas es el dossier consolidado — o un tripwire.
- Python 3.13 (pineado en `.python-version`), Pydantic para contratos, pytest, dependencias mínimas (numpy/pandas/scipy).
- Docs en español, código e identificadores en inglés.
- Suites con nombres de científicos arquetipo: Horizon (observacional), Anomaly (anomalías), Latent (latentes),
  Prior (prior vs evidencia). Casos en `cases/<case_id>/` con la anatomía de `docs/reference/world-model.md` §1.

## Infraestructura

- **GPU**: VM Azure `lp-gpu-h100-x2-spot` (2× H100 94GB). Es **SPOT** → preemptible: checkpointing y reanudación
  obligatorios en todo job largo.
- **Qué corre dónde**: **E1 es API-bound** (frontier vía API; scoring/oráculos/rivales son CPU; GPU opcional para
  servir modelos abiertos). La GPU es central en **E2** (RL de una policy abierta ~4–8B).
- **Costos**: estimar el presupuesto de API de E1 ANTES de correr (~10³ episodios); la primera pasada, la mínima
  informativa.
- **Workflow y conexiones**: usar las **skills de usuario** de Lucas (Azure/VM, SSH) — no duplicar acá.

## Estado actual

El estado vivo, la cartera y el próximo paso viven en **`docs/roadmap.md`** (sección *Estado actual*) — **única
fuente de verdad; mantenerla al día al cerrar cada sesión.** No se duplica acá (un resumen en CLAUDE se
desactualiza — la lección de ADR 0072). Para el histórico de decisiones: `docs/adr/`.
