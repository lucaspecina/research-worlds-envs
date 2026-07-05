# Librería de operadores y generación de un caso

> Referencia técnica (ex ARCHITECTURE.md). Los números de sección (§N) se
> preservan; las citas '§N' de otros docs resuelven acá o en los hermanos de
> `docs/reference/`. El *por qué* llano está en `WIKI.md`.

## 3. Librería de operadores v0 `[EN DEBATE — lista inicial, set abierto]`

**Principio: la librería es el alfabeto, no el contenido.** Los operadores son el vocabulario interno de la fábrica para expresar estructuras epistémicas — no un temario. El solver jamás ve la taxonomía (evaluación ciega a motivos, `docs/archived/NORTH_STAR_full.md` §2.4): desde su lado solo existe un mundo cuyos datos no cierran. La diversidad fenomenológica sale del producto motor × composición × perillas × piel — el mismo operador sobre motores distintos produce superficies de datos irreconocibles entre sí; lo único compartido es la *movida* que lo detecta, y esa movida es lo que debe generalizar (E3 es la alarma si no).

**Operador** = transformación parametrizada que se aplica sobre fuentes (capas 2–3) o, raramente, sobre el mecanismo (capa 1). Firma conceptual: `apply(target, **knobs)`. Cada operador declara: capa, perillas con rangos, el malentendido canónico que induce, y su fuente histórica.

| # | Operador | Capa | Perillas principales | Malentendido que induce | Fuente minada |
|---|---|---|---|---|---|
| 1 | `confounding_por_asignacion` | mecanismo (asignación) / muestreo (selección) | fuerza de asignación | "la intervención empeora/mejora" (espurio) | discrepancias obs-vs-experimento; catálogos de sesgo |
| 2 | `survivorship` | muestreo | tasa + criterio de filtrado | "los sobrevivientes representan a todos" | aviones WWII; finanzas |
| 3 | `collider_seleccion` | muestreo | regla de entrada al dataset | correlaciones espurias intra-muestra | sesgo de admisión |
| 4 | `error_de_medicion` | canal | varianza, sesgo, proxy | atenuación / efectos fantasma | psicometría |
| 5 | `batch_effect` | canal | drift por lote/fecha/sitio | "señal" que es instrumento | mediciones de alto volumen por lote |
| 6 | `censura_informativa` | muestreo | mecanismo de dropout ligado al outcome | efectos inflados | estudios longitudinales con dropout |
| 7 | `immortal_time` | muestreo | desfase de inclusión | intervenciones "milagrosas" | estudios de seguimiento con tiempo de inclusión |
| 8 | `heterogeneidad_latente` | mecanismo | k subpoblaciones, proporciones, signos | efecto promedio engañoso (Simpson) | suite Latent |
| 9 | `regime_shift` | mecanismo/canal | punto de quiebre, magnitud | extrapolar el pasado | econometría |
| 10 | `umbral_no_lineal` | mecanismo | posición y filo del threshold | linealizar lo no lineal | estudios dosis-umbral / saturación |
| 11 | `missingness_informativo` | canal | MNAR dependiente del valor | imputación ingenua | encuestas |
| 12 | `contaminacion_anomala` | mecanismo+muestreo | proceso espurio inyectado, tasa | alisar la anomalía como ruido | fraude, sensores — suite Anomaly |
| 13 | `revelacion_secuencial` | meta | qué se observa tras qué hallazgo | el plan batch pierde | brecha de adaptividad |

**Regla de capa (v0.4)**: la capa de un operador la define el **proceso que lo encarna**, no su nombre. `confounding_por_asignacion` es de **mecanismo** cuando la asignación del tratamiento es un proceso del mundo — el tratamiento lleva ecuación estructural propia (`D := g(S) + ruido`) que `do()` reemplaza, semántica SCM estándar — y de **muestreo** solo cuando el confounding lo induce la selección del dataset (tipo collider). Consecuencia: `world.sample()` bajo régimen observacional genera la asignación natural confundida; el "mecanismo limpio" de §2.2 significa limpio de corrupciones de canal/muestreo, no sin estructura de asignación.

**Receta del operador 8, `heterogeneidad_latente` (v0.29 — encuadre teórico reusable).** Formalmente: **label shift con proxy** — las invariantes del mundo son las **condicionales POR CLASE** `P(outcome | dose, Z)`; lo que cambia entre poblaciones es el prior `P(Z)` (el mix); el proxy observable del latente (`marker`) tiene una **fidelidad** que es la **perilla crítica** del operador. Proxy limpio → la invarianza es alcanzable A NIVEL OBSERVABLES (`P(outcome|dose,marker)` es mix-invariante; sin-latente alcanza; brecha de teoría chica — Latent v0, el control negativo). Proxy ruidoso → la invarianza solo es alcanzable A NIVEL LATENTE (el posterior `P(Z|marker)` depende del prior → la condicional sobre observables se corre con el mix; hay que positar la mezcla — Latent v1). **La brecha de teoría mide EN QUÉ NIVEL es alcanzable la invarianza.** Regla de batería para este operador: **DEBE incluir shifts de prior (mix) MÁS ALLÁ del rango experimentable** — dentro del rango, una condicional flexible con el mix como feature interpola y la brecha desaparece por la razón equivocada.

**Lección del operador 3, `collider_seleccion` (v0.56 — el alfabeto aprende del caso)**: un filtro que carga sobre la **causa común** (p.ej. `signal+outcome` cuando ambos suben con `driver`) produce **restricción de rango** sobre la causa — un sesgo distinto y más débil que la colisión. Para colisión genuina, **parametrizar el filtro sobre RESIDUALES** respecto de la causa común ("superó la vara ajustada": `signal+outcome−k·driver > umbral`), que además es la historia survivorship natural. Primera vez ejercida en `selection_bias_v0` (pc −0.06 → −0.29 con rango completo).

**Composición**: un caso instala 2–4 operadores con perillas sampleadas; las **interacciones** entre operadores (p.ej. survivorship encima de asignación confundida) producen patrones que ningún operador genera solo — es donde muere lo "de manual". **Apertura del set**: el designer puede proponer operadores nuevos como código; entran si (a) ejecutan contra ≥2 motores, (b) inducen brechas > umbral en al menos uno, (c) no duplican el archivo (similitud de firma conductual). El canal de crecimiento principal es **a demanda de semillas**: cuando la moraleja de un caso real no puede expresarse con el vocabulario actual, eso — no la imaginación — dispara la propuesta de un operador nuevo. Así la librería converge hacia "el vocabulario necesario para expresar cómo la realidad engaña a los científicos" (el Catalogue of Bias sugiere que son decenas de entradas, no miles — pero tampoco trece). Si el flujo de semillas se corta y la librería se congela, se materializa el ataque #15.

---

## 4. Generación de un caso — los dos modos `[ESTABLE]`

```
MODO CON SEMILLA (paper / informe NTSB / case study de investigación / par obs→experimento / post-mortem):
  semilla → [digestion] → moraleja epistémica
          → [architect] → motor del catálogo + operadores TRASPLANTADOS de la moraleja
          → perillas + piel (anti-leak: el writer del brief NO ve batería ni rivales)

MODO SIN SEMILLA (sampleo):
  prior de la librería → motor ~ catálogo, operadores ~ composiciones plausibles,
  perillas ~ rangos, piel ~ generador de dominios
```

En ambos modos los operadores instalados quedan **declarados en `meta.json`** (jamás en el brief): rivales, batería y certificados se computan desde esa declaración — es la hoja de respuestas del examinador.

**Declarado = certificado, no = único.** La declaración no acota lo que el agente puede o debe descubrir: el agente debe modelar el mundo ENTERO, y la batería sondea todas las regiones donde los rivales discrepan — típicamente varias por caso (2–4 operadores en interacción + estructura del mecanismo: heterogeneidad, umbrales, dinámica). El crédito es graduado: entender parte de la estructura paga parte del score. Lo que la declaración habilita es la *garantía*: solo sobre lo declarado podemos derivar rivales y certificar que el caso lo testea discriminativamente. Estructura no declarada igual queda sondeada (cola de auditoría; los rivales (a)/(d) fallan donde fallan), pero sin certificado.

**Tres fuentes de generación, con roles distintos — ninguna reemplaza a las otras.**

1. **Semillas reales** (papers, NTSB, investigaciones, obs→experimento, post-mortems): la *autoridad sobre la estructura* — anclan el soporte de la distribución a cómo la realidad engaña de verdad. No son la fuente de volumen.
2. **Composición + perillas** (librería sobre el catálogo de motores): el *volumen* — convierten cada estructura en una familia paramétrica de mundos re-sampleables.
3. **Búsqueda del designer** (oráculo de fallas, regret sobre perillas, operadores nuevos): la *frontera* — regiones que ningún corpus documentó, en el borde de la policy actual. Mitigación activa del ataque #14 y motor de la coevolución; el modo con semilla no la veta.

**Test de contaminación (obligatorio para casos con semilla investigativa).** Las semillas famosas viven en el pretraining del solver: el riesgo es que recupere la moraleja de memoria sin investigar (viola la invariante "forzar investigación"). El instrumento ya existe: si el rival (c) *prior evocado* — compilado por un panel fresco desde brief+schema, sin datos — ya contiene la estructura de la trampa (brecha de prior ≈ 0), el caso NO certifica como investigativo: se re-skinea, se re-estructura, o se clasifica en el bucket confirmatorio del curriculum. **Práctica por defecto para semillas conocidas: trasplante cruzado de dominio** — la moraleja "el tratamiento se daba a los más graves" (medicina) expresada en un mundo de colas ("los upgrades se daban a los servidores más cargados"): conserva la estructura del engaño, destruye la recuperabilidad por memoria, y testea exactamente la abstracción que queremos entrenar.

**Sesgo del propio corpus de semillas (declarado).** El archivo del error documentado tiene survivorship: solo contiene los engaños que alguien detectó, en campos que se auto-auditan (medicina, aviación). Las trampas que engañan para siempre, o las de campos sin cultura de auditoría, no están — por eso la fuente 3 es irreemplazable. **Métrica de salud del pipeline de semillas: tasa de novedad estructural** — fracción de semillas nuevas que exigen un operador o una composición no vista. Si colapsa, el stream está agotado y el peso de generación migra a búsqueda.

El principio de SREG sobrevive en todas las fuentes: *el caso real inspira la estructura del engaño; el mundo es nuevo*.

**Columnas señuelo (anti-leak de esquema).** El esquema lo elige quien conoce la trampa → es un canal de leak no auditado: una columna `fecha_de_entrada_al_lote` susurra immortal time. Reglas: los esquemas se samplean de plantillas por dominio con independencia de las trampas instaladas, y todo mundo lleva columnas plausibles e irrelevantes. El probe del generador (§14) se extiende al nivel esquema. **Mismo tratamiento para las fuentes (v0.3)**: los nombres y descripciones de fuentes (lo que muestra `env.describe()`) se generan desde plantillas neutrales por el mismo proceso ciego — una fuente llamada `registro_de_sobrevivientes` susurra la trampa igual que una columna delatora — y el probe del generador se extiende también a nombres y descripciones de fuentes.

Pipeline completo: semilla? → digestion → architect (motor+operadores+perillas) → piel → compilación (`world.py` + `sources.yaml`) → **rivales (§5)** → **batería (§6)** → brechas/certificados (§7) → validación → brief (writer ciego).

---
