# Menú estratégico (decisión de Lucas 2026-08-05) + diseño v0 de la máquina de saltos

> **Estado:** dirección elegida por Lucas en sesión; pendiente de cruce con Codex (ADR 0172) y de
> ADR formal si se confirma. Este doc registra (1) el menú de líneas con su estado, (2) el diseño
> v0 de la máquina generadora de escenarios de salto creativo, (3) el paisaje externo relevado hoy
> con links, (4) los problemas abiertos honestos y el prototipo propuesto.
> Contexto previo: [contrapunto-refoco-estructural](2026-08-05-contrapunto-refoco-estructural.md).

---

## 1. El menú de líneas y su estado

| Línea | Qué es (en llano) | Estado decidido | Condición de retoma / muerte |
|---|---|---|---|
| **A. La máquina de saltos** | Escenarios generados automáticamente donde entender el sistema EXIGE un salto creativo (postular lo no observado); diverso por tipo de salto | **ACTIVA — PRIMARIA** (lo que más motiva a Lucas: creatividad para descubrimiento) | Muere si el prototipo de 3 operadores no genera mundos certificables con huellas conductuales distintas |
| **D. ¿Cuándo se enciende la falla de revisión?** | Los ~20 nulos solo cubren mundos chicos/limpios/quietos; buscar la CONDICIÓN que enciende la falla documentada (primera candidata: el mundo que cambia debajo del agente) | **ACTIVA — SECUNDARIA** | Se abandona solo tras probar las condiciones documentadas no testeadas, con criterios escritos antes |
| **B. Autoescepticismo** (cierre prematuro + verificación de paja + poder de refutación del chequeo propio) | ¿El agente intenta refutarse antes de entregar, y su intento tiene poder? | **ESTACIONADA** | Se retoma si A/D pierden interés o si las trazas de A/D la muestran gratis (instrumentarla barato en toda corrida) |
| **C. Integridad** (fabricar/inflar) | Mundos donde la honestidad gana puntos; detección entrega-vs-traza | **ESTACIONADA** (candidata de pivote explícita) | Se retoma por decisión de Lucas; implica cambiar de comunidad/conversación |

**Principio rector confirmado por Lucas:** proyecto de investigación — se dejan líneas abiertas y
se cambia el foco según resultados intermedios. Nada de esto es un compromiso irreversible.

**Sobre D — la corrección de fondo (pregunta textual de Lucas):** *"¿para que todo sea nulo, es
porque las AIs son perfectas actualizando creencias por evidencia?"* — **NO.** Los nulos muestran
"buenas en mundos chicos, limpios y estáticos" (lo único que construimos). Las fallas documentadas
viven en condiciones largas, sucias y **cambiantes** que nunca reprodujimos. Bonus verificado hoy:
**KellyBench ya está LEÍDO a texto completo (2026-07-14** — registro en lectura-de-fuentes; ojo:
`vicio-1` todavía lo etiqueta `[POR-LEER]`, desincronización a corregir) y su detalle es oro puro
para D: *"la mayoría ajustó su modelo UNA vez al inicio y jamás lo re-entrenó pese a datos frescos
cada fecha; GLM-5 escribió TRES autocríticas diagnosticando la causa exacta de sus pérdidas y
siguió con el modelo roto"*. Ésa es la anatomía exacta de la condición a reproducir: temporada
larga + datos frescos rutinarios + modelo propio que envejece + adaptación con costo.

---

## 2. El problema que define la máquina (planteo de Lucas, verbatim en esencia)

> "No he podido definir bien QUÉ CASOS serían los que debería descubrir, y cómo generarlos
> automáticamente (sin que terminen siendo 4 o 5 casos hechos por nosotros y disfrazados
> distintos). Si vamos a tener una máquina que GENERE ESCENARIOS DONDE EL AGENTE TIENE QUE DAR UN
> SALTO DE CREATIVIDAD para entender el sistema, y esa máquina funciona bien, genera casos muy
> diversos y con tipos de creatividad distintas — ME PARECE FANTÁSTICO."

Dos sub-problemas distintos:
1. **El QUÉ**: una tipología de saltos — qué clases de "cosa que hay que imaginar" existen.
2. **El CÓMO sin disfraces**: generación automática con diversidad REAL, no 4 plantillas maquilladas
   (la falla ya medida del proyecto: ADR 0131 — la fábrica v1 colapsó, pearson≈1.0 entre mundos
   generados, dominios repetidos; supuesto S16b en ROJO del red-team).

Lo que el repo YA tenía esperando esto (no arrancamos de cero):
- **OQ #24 ("el mundo del salto")** — reencuadre de Lucas del paper can't-jump: el ancla ingenua
  puede ajustar BIEN lo observado; la nota se cobra en regímenes NO vistos donde solo la
  estructura verdadera generaliza. La maquinaria de batería held-out ya existe.
- **OQ #18 ("fronteras descubribles")** — "cada par es artesanía hasta el aha: las fronteras
  descubribles tienen esta estructura general". Los certificados de §4 son una propuesta de
  respuesta a esa pregunta.
- **ADR 0150 — contrato de resolubilidad** ("certificar el paisaje, no el camino"; el premio del
  salto vive en la EXTRAPOLACIÓN; el camino real es anti-MDL: la complejidad sube antes de bajar).
  Estaba **DIFERIDO por orden de Lucas "hasta abrir mundos de aha" — esta decisión lo REACTIVA.**
- **OQ #13 (brecha de teoría)** — "el mejor modelo restringido a funciones de los observables"
  como baseline: es exactamente el certificado de necesidad del salto.
- **El testigo de recuperabilidad (agosto)** — BIC/CV sobre las filas legalmente servidas.
- Re-skin (ADR 0071), trasplante de dominio y test de contaminación (red-team #16).

---

## 3. Diseño v0 de la máquina

### 3.1 El alfabeto de saltos (capa 0 — el QUÉ)

Cada operador es una **naturaleza distinta de "lo que hay que imaginar"**, con su ejemplo
histórico y su estado en WAGER. El alfabeto inicial (10), destilado del catálogo de ahas, la
historia de la ciencia y los casos del vicio 4:

| # | Operador (el salto) | Ejemplo histórico | Semilla WAGER existente |
|---|---|---|---|
| 1 | **Entidad oculta** — una variable/especie/cuerpo no observado influye en lo observado | Neptuno | par Neptuno/Vulcano (spec en cantera) |
| 2 | **Heterogeneidad oculta** — la población es una mezcla de tipos | subtipos de Mendel; responders/non-responders | `latent_mix_v2` + firma A3 (SCM, ago) |
| 3 | **Régimen/fase oculto** — la ley cambia entre regímenes/tiempos no anunciados | transiciones de fase | `ode_second_wave` |
| 4 | **Geometría/reparametrización** — la ley simple vive en otras coordenadas (log, recíproco, dimensión extra) | Kepler en log-log; espacio-tiempo curvo | LSR-Transform lo valida afuera |
| 5 | **Unificación** — dos fenómenos presentados como separados comparten mecanismo | Luna y manzana | mundo consiliencia (cartera); par unificar↔apofenia |
| 6 | **Re-jerarquización de lo banal** — la clave está en el invariante aburrido a la vista, no en la anomalía llamativa | caída igual de los cuerpos (Einstein) | ADR 0150 (relectura can't-jump) |
| 7 | **Proceso del observador** — selección/censura/instrumento genera el patrón | supervivencia de Wald | `survivorship_censor_v0`, `selection_bias_v0` |
| 8 | **Feedback oculto** — lo observado es artefacto de equilibrio de causas mutuas | depredador-presa | familia causal (parcial) |
| 9 | **Cuantización/conservación** — ratios discretos delatan una cantidad conservada subyacente | Mendel, estequiometría | — |
| 10 | **Memoria/retardo oculto** — histéresis o delay que rompe la lectura instantánea | histéresis | — |

> **ACTUALIZACIÓN (mismo día):** esta lista v0 fue intuición experta y NO está justificada aún.
> El método para justificarla (marco formal componente×edición, triangulación con 3 literaturas,
> receta de validación con held-out y κ) + el operador 11 (transferencia estructural, ejemplo
> Darwin de Lucas) viven en
> [fundamentos-taxonomia-de-saltos](2026-08-05-fundamentos-taxonomia-de-saltos.md). El alfabeto
> se congela recién después de correr esa receta.

Cada operador se implementa como **transformador mecánico**: toma un mundo base (de una librería
de formalismos: SCM, ODE, mezclas, colas, autómatas, campos) e **instala** la estructura latente,
emitiendo junto con el mundo: su **gemelo sin estructura**, su **lattice de testigo**, su
**familia baseline sin-salto** y su **máscara de canales de evidencia** (dónde vive la señal).

### 3.2 Los cinco certificados por mundo generado (capa 1 — cero-LLM todos)

Un mundo generado NO entra al archivo si no pasa los cinco. Esto convierte "el salto es necesario
y posible" de esperanza del diseñador en propiedad demostrada de la instancia:

1. **NECESIDAD (brecha de teoría, OQ #13):** la mejor familia de modelos SIN el salto — con acceso
   legal completo a la evidencia — toca techo medible por debajo de la verdad. Gap ≥ umbral.
   *Sin esto, el mundo no exige el salto (curve-fitting alcanza).*
2. **ALCANZABILIDAD (testigo):** un buscador mecánico sobre el lattice declarado, usando SOLO
   evidencia legalmente comprable con el presupuesto del episodio, encuentra la estructura
   (BIC/CV/holdout). *Sin esto, el mundo es una adivinanza injusta.*
3. **GEMELO ANTI-FANTASÍA:** existe el mundo superficie-similar donde la estructura NO está y
   postularla PIERDE (sobreajuste cobrado en held-out). Robots: `postular-siempre` pierde en el
   gemelo; `nunca-postular` pierde en el mundo. *Sin esto, entrenamos apofenia.*
4. **ANTI-MEMORIZACIÓN:** transformación sistemática de superficie (estilo LSR-Transform) +
   trasplante de dominio para semillas famosas + test de contaminación (regla #16). *Sin esto,
   medimos memoria.*
5. **NOVEDAD CONDUCTUAL (anti-disfraz — la lección del ADR 0131):** la huella mecánica del mundo
   nuevo — el vector de scores de su escalera de verdades degradadas + qué baselines fallan y
   cuánto — debe distar de las huellas ya archivadas. Huella ~idéntica ⇒ rechazado como disfraz.
   *Éste es el certificado que la fábrica v1 no tenía cuando colapsó.*

### 3.3 Diversidad por construcción (capa 2 — el CÓMO sin disfraces)

Importado de Quality-Diversity (MAP-Elites): el archivo tiene **celdas** =
`(tipo de salto × formalismo base × canal de evidencia × tamaño del salto)`. La fábrica no
"genera libre y esperamos variedad": **rellena celdas vacías**. Un LLM puede proponer (lado
fábrica, jamás juez — doctrina intacta); los certificados disponen. Métricas de salud: yield por
celda + cobertura del archivo + distancia entre huellas.

### 3.4 El objetivo del generador (capa 3 — importado de UED/PAIRED/POET)

La literatura de Unsupervised Environment Design genera entornos maximizando el *regret* entre un
protagonista y un antagonista. Nuestra versión epistémica: **buscar mundos que maximicen la brecha
certificada** — robot-con-salto ≈ techo, mejor baseline sin-salto ≪ techo — sujeto a testigo
válido. La brecha (certificados 1+2) deja de ser un filtro pasivo y pasa a ser la **función
objetivo de la búsqueda** de parámetros del mundo. Cero-LLM de punta a punta.

### 3.5 El dial de dificultad (capa 4)

La generalización de la escalera de momentos: **dónde vive la evidencia del salto** —
media → varianza → forma/colas → transferencia entre regímenes → solo bajo intervención. Más
profundo en la escalera = salto más difícil de disparar (nuestra evidencia de agosto: los agentes
revisan cuando la señal vive en la media; aplanan cuando vive en la forma). Perillas adicionales:
dosis/ruido, presupuesto, saliencia del canal.

### 3.6 Problemas abiertos declarados (no resueltos por este diseño)

- **El techo de lo comprensible (red-team #14):** el alfabeto lo escribimos nosotros ⇒ los saltos
  FUERA del alfabeto no aparecen. Mitigaciones parciales: composición de operadores (propiedades
  emergentes), **held-out de operadores** (iterar con ~7, confirmar con ~3 jamás usados — E3 a
  nivel operador), y a largo plazo operadores descubiertos por búsqueda. Límite declarado, no
  resuelto.
- **El residuo duro del can't-jump (OQ #24):** el caso donde ni un agente sondeando activamente ve
  error en ningún régimen alcanzable (Newton loss≈0 en TODO lo medible de su época). Nuestra
  maquinaria esquiva la versión práctica (cobramos en held-out); la versión filosófica queda.
- **Robots-de-salto:** el certificado 2 en su forma fuerte pide robots que EJECUTEN el salto
  (evidencia positiva casera — `ahas.md` ya lo exigía: "los mundos de aha deben generar su PROPIA
  evidencia positiva"). Trabajo real por operador.
- **Diversidad de superficie ≠ diversidad cognitiva:** el certificado 5 la vigila mecánicamente;
  la validación final es conductual (¿celdas distintas elicitan perfiles distintos en agentes
  reales?). Se mide en el prototipo.

### 3.7 Prototipo acotado (slice vertical, regla de la casa)

**3 operadores lo más lejanos entre sí, por el MISMO pipeline** — ninguno nuevo en su fenómeno,
dos con semilla ya construida:
1. **Heterogeneidad** (op. 2 — semilla: SCM/latent_mix, testigo ya probado),
2. **Régimen/fase** (op. 3 — semilla: ode_second_wave),
3. **Uno genuinamente nuevo** (op. 7 proceso-del-observador o op. 1 entidad-oculta) para probar
   que el pipeline no depende de lo ya construido.

Salida verificable: los 3 pasan los 5 certificados con yield razonable + huellas conductuales
distintas (robots) + un agente real barato por celda para el smoke. Si el pipeline exige cirugía
manual por mundo ⇒ la máquina no es máquina todavía; se reporta y se rediseña ANTES de escalar el
alfabeto.

---

## 4. Paisaje externo (relevado 2026-08-05, nivel abstract salvo indicación; entra a la cola de lectura)

| Proyecto | Qué hace | Qué tomamos | Qué le falta (nuestro hueco) |
|---|---|---|---|
| [NewtonBench](https://arxiv.org/abs/2510.07172) (2510.07172) | **324 tareas / 12 dominios generadas por "counterfactual law shifts"** — alteración sistemática de leyes canónicas; interactivo; scoring mecánico | La prueba de que la generación sistemática ESCALA y resiste memorización; su hallazgo del "tool paradox" | Sin tipología de saltos (altera formas, no instala estructura latente); sin gemelos/controles negativos; sin testigo ni brecha certificada |
| [LLM-SRBench](https://arxiv.org/abs/2504.10415) (ICML 2025 oral) | 239 problemas: LSR-**Transform** (ecuaciones conocidas → formas no familiares) + LSR-**Synth** (composición sintética); mejor sistema 31.5% | La receta anti-memorización por transformación (nuestro certificado 4) | Datos estáticos: sin agencia/presupuesto/experimentos; sin gemelos; un solo tipo de salto (forma simbólica) |
| [DiscoverPhysics](https://arxiv.org/abs/2605.26087) (leído completo 07-13) | 22 mundos de física alterada con estructura latente, hechos A MANO; frontier falla justo ahí | Validación del fenómeno en frontier | Generación manual (lo que Lucas no quiere); juez-LLM en explicaciones; sin gemelos ni testigo |
| [Auto-Bench / Auto-Discovery-Bench](https://arxiv.org/abs/2502.15224) | Descubrimiento de grafo causal oculto auto-generado (química/red social); LLMs solo pueden con complejidad muy limitada | Generación desde principios de grafo causal | Un solo tipo de estructura; oracle-guided; sin economía de evidencia ni gemelos |
| [CausaLab](https://arxiv.org/abs/2605.26029) | Entorno escalable de descubrimiento causal interactivo (SCM oculto + presupuesto) | Vecino directo de B (cierre prematuro); leer completo antes de citar números | Un formalismo; sin tipología ni gemelos |
| [OMNI-EPIC](https://arxiv.org/abs/2405.15568) (ICLR 2025) / POET / [UED task-level](https://arxiv.org/abs/2511.12706) | Generación abierta de entornos: LLM programa entornos en código, filtro de "interesantez"; UED = minimax regret | El patrón proponedor-LLM + filtro mecánico; el **regret como objetivo del generador** (nuestra §3.4) | Su diversidad es paramétrica/terreno, no conceptual-epistémica; sin verdad oculta que entender |
| [CreativeBench](https://huggingface.co/papers/2603.11863) (2026) | Creatividad de CÓDIGO vía desafíos auto-evolutivos (Combo=recombinación, Explore=constraints progresivos); hallazgo: la escala mejora lo combinatorio, **no el salto 0-a-1** | Convergencia independiente con can't-jump y con nuestra tesis; sus dos pipelines ≈ composición/búsqueda | Objeto distinto (código creativo, no mundos ocultos); sin evidencia comprable ni entrega ejecutable contra verdad |
| [StatefulDiscovery](https://arxiv.org/pdf/2606.11851) · [HeurekaBench](https://colmweb.org/AcceptedPapers.html) · [Traceable Latent Variable Discovery](https://dl.acm.org/doi/10.1145/3774904.3792244) | 2026, adyacentes (claims calibrados / co-scientist / latentes con multi-agente) | A la cola de lectura para vigilar scoop | — |

**El hueco que nadie ocupa** (y que la máquina llenaría): tipología de saltos como alfabeto
generativo × necesidad y alcanzabilidad **certificadas por instancia** × gemelos bilaterales
anti-fantasía × brecha como objetivo de búsqueda × scoring cero-LLM en regímenes no vistos.

**Cola de lectura nueva** (ADR 0115: texto completo antes de construir sobre ellos):
NewtonBench (completo) · LLM-SRBench (completo) · Auto-Bench · OMNI-EPIC · CreativeBench ·
StatefulDiscovery · HeurekaBench · CausaLab (ya estaba, sube prioridad si B revive).

---

## 5. Próximos pasos propuestos

1. **Cruce con Codex** de este menú + diseño (insumo: este doc). Si hay GO → ADR nuevo
   (reactivación del contrato de resolubilidad de ADR 0150 incluida).
2. **Lecturas a texto completo** (NewtonBench y LLM-SRBench primero — son los dos con maquinaria
   robable directa).
3. **Prototipo §3.7** — construible en gran parte sin `.env` (transformadores, certificados,
   robots, gemelos son cero-LLM); los smokes con agente real esperan credenciales.
4. **D en paralelo lento:** diseñar el mundo-que-cambia (anatomía KellyBench: temporada +
   datos frescos rutinarios + modelo que envejece + adaptación con costo) con ficha y criterios
   antes de correr. Sin construir hasta cerrar el prototipo de A o por decisión explícita.
5. **Sincronizaciones de docs pendientes de aprobación:** KellyBench `[POR-LEER]`→`[VERIFICADO]`
   en vicio-1 · "0/10 modelos"→"0/10 episodios (2 modelos)" en vicio-4.
