# Reorganización: el motor WAGER vs. los estudios que lo consumen

> **Estado: PROPUESTA NO DECIDIDA.** Trabajo futuro, deliberadamente pospuesto.
> Origen: conversación Lucas–Claude del 2026-08-05, al retomar el proyecto tras la pérdida de la
> máquina de trabajo. Nada de lo que sigue está aprobado ni ejecutado. Si se aprueba, sale un ADR
> nuevo con la decisión y este doc queda como su fundamentación.
>
> **Regla que gobierna este doc: no se borra nada.** Ver §5.

## 1. El diagnóstico, en una frase

El repo mezcla cuatro cosas que tienen ciclos de vida distintos: un **motor** reutilizable, un
**método** de certificación, los **estudios** concretos, y la **bitácora** de lo aprendido. Están
acopladas por sedimentación histórica, no por diseño. Eso se paga cada vez que alguien —humano o
agente— tiene que reconstruir dónde está parado el proyecto.

## 2. Las cuatro capas

| Capa | Qué es | Dónde vive hoy | Ciclo de vida |
|---|---|---|---|
| **1. Motor** | Contratos (qué es un mundo, un episodio, una entrega), harness (loop, sandbox, kernel, world server, cliente LLM), juez cero-LLM | `wager/` | Cambia poco; crece **solo a demanda de un caso real** |
| **2. Método** | Gemelos, escalera de verdades degradadas, robots anti-reflejo, batería y rivales derivados, certificados, tests de contaminación | Esparcido entre `wager/factory/`, `docs/failure-modes.md` y fichas sueltas | Es la contribución metodológica; hoy **no tiene casa** |
| **3. Estudios** | La investigación concreta: qué vicio, qué mundos, qué probes | `cases/` + `scripts/` mezclados, sin separación por línea | Nacen, se cierran, se archivan |
| **4. Bitácora** | ~20 probes con agentes reales, 32 fichas / 33 resultados, casi todos nulos preservados con autopsia | Enterrada en ~280 líneas de cabecera cronológica de `docs/roadmap.md` | Solo crece; es el activo acumulado |

La capa 2 es probablemente lo más transferible y publicable del proyecto —"cómo certificás que un
mundo no premia un reflejo" le sirve a cualquiera que evalúe agentes, sea cual sea el vicio— y es
justamente la que hoy no está nombrada como cosa separada.

## 3. La dirección de la flecha (corrección conceptual importante)

Es tentador leer las capas como *"tenemos una herramienta (WAGER) e investigamos dónde aplicarla"*.
**Esa flecha está invertida** respecto de la doctrina vigente del proyecto:

- Regla dura de **fidelidad a los casos reales** (ADR 0147): los mundos reproducen los fenómenos como
  aparecen en los casos reportados.
- Regla dura: *"la librería de operadores crece a demanda de semillas reales, nunca por imaginación
  suelta"*.

La flecha real es:

```
caso real documentado  →  qué debe poder expresar el mundo  →  qué le falta al motor
```

El estudio de vicios no es investigación de mercado para una herramienta: es **la fuente de verdad
que restringe qué tiene que poder expresar el motor**. La diferencia no es semántica. Si fuera
"dónde aplico WAGER", se generalizaría el motor por anticipado; como es "qué debe poder expresar",
el motor solo crece cuando un caso real lo exige. Cualquier reorganización debe preservar esta
asimetría, no borrarla en nombre de la simetría arquitectónica.

## 4. Evidencia medida (2026-08-05)

Números tomados del repo en `main` @ `71e4eb1`, no estimados.

**Tamaños:**

```
wager/     9.5k LOC   ← el "motor" es el 15% del código
cases/    24.3k LOC
scripts/  25.9k LOC
tests/     3.8k LOC
```

**A favor de que el motor es real: la cintura existe y es delgada.** Los 66 scripts de probe
consumen una API estrecha y estable, atravesando tres eras conceptuales distintas (catálogo de
vicios → overgen → revisión de creencias) sin romperla:

| import | scripts que lo usan |
|---|---|
| `wager.harness.case_episode.build_world_server` | 39 |
| `wager.harness.kernel_proc.KernelClient` | 23 |
| `wager.agent.llm_client.FoundryChat` | 22 |
| `wager.agent.cells.extract_cell` | 21 |
| `wager.reward.sandbox.SandboxedSubmission` | 12 |

O sea: el motor genérico **ya existe empíricamente**. Lo que no existe es que esté *declarado* ni
que haya nada que lo haga cumplir.

**En contra: la frontera ya está perforada.** ~2.8k LOC de código específico de un caso viven
*adentro* del motor — el 30% de `wager/`:

```
wager/factory/plan_probe_v0.py        1270   ← un probe puntual
wager/harness/plan_probe_v0.py         814   ← el MISMO probe, duplicado en otro módulo
wager/factory/overgen_stream_tools.py  488   ← overgen, línea congelada
wager/report/overgen_belief.py          80
wager/factory/rival_c_panel.py         109
wager/harness/c1_env.py                 80
```

La duplicación de `plan_probe_v0` en dos módulos distintos es la firma clásica de una frontera que
nadie hace cumplir.

## 5. Sobre los casos "viejos": NO HAY NADA PARA BORRAR

Un primer análisis (grep del nombre del caso en `scripts/` y `tests/`) marcó 16 casos como
huérfanos. **Ese análisis era incorrecto y queda registrado como error para que nadie lo repita:**
cada caso trae su propio `build_and_certify.py` / `build_and_check.py` adentro, es autocontenido, y
por diseño no necesita un script externo que lo nombre. Buscar en `scripts/` era el test equivocado.

La foto real, verificada caso por caso:

| Grupo | Casos | Qué son |
|---|---|---|
| Completos y documentados | `twotank_clearance_v0`, `survivorship_censor_v0`, `prior_sweetspot_v0`, `batch_confound_v0`, `batch_confound_wide_v0`, `rabbit_hole_v0`, `overgen_v0`, `lab_largo_v0`, `final_note_true_v0` | Eras cerradas, con hasta 10 docs y 6 ADRs referenciándolos |
| Barrido de parámetros | `rabbit_hole_v2_{poc,hot,difuso,largo}` | Variantes de `rabbit_hole_v2`, que está vivo. Un mundo, cuatro configuraciones |
| Superados, con sucesor presente | `latent_mix_v0` (→ `v1`, `v2`), `overgen_twin_v0` (→ `overgen_stream_twin_v0`) | La versión nueva convive con la vieja |
| Genuinamente incompletos | `latent_mix_v0` (sin `battery.json`, sin `ladder/`, sin certificados) | Quedó a medio construir |

**Regla para cualquier archivado futuro:** el proyecto estuvo *en medio del desarrollo* cuando cada
una de estas líneas se pausó. Un caso sin referencias puede ser una era cerrada, un barrido, una
versión superada **o trabajo inconcluso al que se pensaba volver**. Antes de mover cualquier cosa se
verifica caso por caso (git log + ADRs + docs + completitud de artefactos), nunca con un grep.
Archivar significa **etiquetar la era en un `_attic/`, jamás borrar**.

## 6. Layout objetivo

Un solo repo. Ver §7 para por qué no dos.

```
wager/       ← motor. Cero conocimiento de qué vicio se estudia.
method/      ← capa 2 con casa propia: certificación, gemelos, robots, escalera
studies/
  belief-revision/    cases/  probes/  docs/     ← la línea viva
  _attic/             overgen, rabbit_hole, lab_largo, batch_confound...
docs/        ← solo transversal: método, ADRs, operativa, bitácora
```

**La frontera se hace cumplir con un test, no con buena voluntad.** Un test que falle si `wager/`
importa de `studies/`, o si un `case_id` aparece hardcodeado dentro del motor. Es la jugada marca de
la casa (ADR 0057, *guardias con autotest*: toda guardia llega con su par should-pass/should-fail
corrido ANTES de instalarse). Sin ese test la frontera se pudre en una semana — la fuga de §4 es la
prueba. Lo primero que cazaría son esos 2.8k LOC.

## 7. Por qué NO repos separados (todavía)

La tentación es publicar `wager` como paquete y que cada estudio lo consuma. Tres razones para no:

1. **Sería extraer una librería con n=1.** Hoy hay *una* línea viva. La prueba honesta de "¿WAGER es
   una herramienta general?" es que un **segundo fenómeno distinto** la consuma sin modificarla, y
   ese test no se corrió. Partir ahora congela una API con la forma de una sola investigación y le
   pone el cartel de general.
2. **Le cobra peaje a la velocidad justo donde el proyecto la necesita.** La metodología vigente es
   *caso real → mundo mínimo → agente real → autopsia → cambio → nueva prueba* en ciclos cortos. Que
   un probe necesite tocar el harness a mitad de ciclo pasa seguido en descubrimiento; con dos repos
   eso es version bump + release + PR cruzado. En fase de **confirmación** el split se justifica; en
   descubrimiento es veneno.
3. **Arrancar un repo desde cero ya se hizo dos veces** (`synthetic-research-envs` → `wager` →
   `research-worlds-envs`, este último por una restricción externa de nombre, no por contenido). Es
   el reflejo del proyecto ante el desorden y no conviene repetirlo. Este refactor va **in place**.

**Criterio de disparo para reconsiderar el split:** cuando una segunda investigación consuma
`wager/` sin modificarlo durante un ciclo completo. Ahí el split se vuelve trivial y además está
respaldado por evidencia de que la cintura aguanta, en vez de por una apuesta.

## 8. Orden de ejecución propuesto

Ordenado por *valor devuelto / costo*, no por prolijidad.

| # | Trabajo | Costo | Por qué en este orden |
|---|---|---|---|
| 1 | **Partir la cabecera del roadmap**: ~30 líneas de estado real + `docs/bitacora-de-probes.md` con la cronología | ~2 h | Hoy toda sesión lee 280 líneas cronológicas para saber dónde está. Es lo que más cuesta al retomar, y **lo único que devuelve tiempo en vez de cobrarlo** |
| 2 | **Test de frontera** motor↔estudios (con su par should-pass/should-fail) | ~1 h | Sin esto lo demás se deshace. Es barato y es doctrina existente |
| 3 | **Mover la fuga**: los 2.8k LOC case-specific salen de `wager/` a `studies/` | ~2 h | Mecánico, guiado por el test del paso 2 |
| 4 | **Etiquetar eras** en `cases/`: `_attic/` con una línea por caso (era + ADR que la cerró + si quedó inconclusa) | ~2 h | Verificación caso por caso obligatoria (§5) |
| 5 | **Dar casa al método** (`method/`) | ~medio día | El más valioso a largo plazo y el menos urgente. Requiere criterio, no mecánica |

Los pasos 1–4 son ~medio día en total. El 5 puede esperar indefinidamente.

## 9. El riesgo de hacer esto — declarado

**ADR 0173 y `AGENTS.md` prohíben específicamente construir infraestructura en vez de probar el
mundo**: *"preferir un slice vertical temprano con agente real a infraestructura general construida
sin señal"*. Esta reorganización produce **cero evidencia científica**.

La defensa es acotarla: medio día para los pasos 1–4, empezando por el que devuelve tiempo. Si se
come dos días y la etapa 6t se corre igual esa semana, valió. Si se come dos semanas, el proyecto
hizo exactamente lo que sus propias reglas dicen que no haga, y este párrafo es la evidencia de que
se sabía de antemano.

**Explicación rival que conviene testear primero, y es gratis:** que la sensación de "está todo
mezclado" no venga del código sino de la **documentación** — 280 líneas de cabecera cronológica más
tres eras de docs conviviendo. Si es eso, el refactor de código no cura nada y el paso 1 alcanza.
Hacer el paso 1 y medir si el malestar baja **es el experimento**, y cuesta dos horas.

## 10. Pendientes relacionados

- `lucaspecina/wager` (el repo #2, 37 commits) **no tiene política de cuarentena declarada**, a
  diferencia de SREG (`synthetic-research-envs`), que sí la tiene en `CLAUDE.md` con allowlist y
  denylist. Decidir: ¿queda algo por rescatar, o se marca muerto explícitamente?
- Si esta propuesta se aprueba, el ADR resultante debe hacer el **checklist de supersesión**
  (ADR 0030): grep de las rutas viejas en TODOS los docs y enumerar cada ubicación editada.
  `ARCHITECTURE.md`, `WIKI.md` y `CLAUDE.md` se tocan con ediciones quirúrgicas (ADR 0056).
