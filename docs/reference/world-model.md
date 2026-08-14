# El mundo y la anatomía de un caso

> Referencia técnica (ex ARCHITECTURE.md). Los números de sección (§N) se
> preservan; las citas '§N' de otros docs resuelven acá o en los hermanos de
> `docs/reference/`. El *por qué* llano está en `WIKI.md`.

## 1. Anatomía de un caso `[ESTABLE]`

Un caso es una carpeta autocontenida:

```
cases/<case_id>/
  world.py          # mecanismo + superficie de control + sample()  — la verdad (OCULTO)
  meta.json         # operadores instalados + perillas + ablaciones, stakes/funcionales,
                    #   scoring (c_f, λ), FUENTES observacionales del episodio (costos, canal
                    #   de medición, filtro de selección), suite, semilla de origen, prior
  brief.md          # narrativa + stakes + ficha técnica — lo ÚNICO que ve el agente
  battery.json      # [(peso, regime, seed_mundo), ...] — OCULTO (seeds lado-maqueta se
                    #   derivan: derive_seed(seed_mundo, j), §9)
  ladder/           # fixtures de la escalera L1 = anclas (ingenuo/nulo) + rivales — OCULTOS
  certificates.json # gates computados en design time
  traces/           # episodios corridos (evidencia; gitignored salvo ejemplares)
```

Regla de visibilidad: el agente ve `brief.md` y el handle `env`. Todo lo demás es lado fábrica.

> **Nota de implementación (doc-vs-código)**: las fuentes observacionales y sus corrupciones
> (canal de medición, filtro de selección, `pipeline_order`) se declaran **dentro de `meta.json`**
> (`episode.observe_sources`), no en un `sources.yaml` aparte. Los rivales se **derivan** en la
> fábrica; los que se persisten son los fixtures de `ladder/`. La spec original hablaba de
> `sources.yaml`/`rivals/` (ver `docs/archived/NORTH_STAR_full.md`); el código consolidó ambos en
> `meta.json` + `ladder/`.

---

## 2. El mundo `[ESTABLE en interfaz, EN DEBATE en detalles]`

### 2.1 Interfaz

```python
class World:
    schema: list[ColumnSpec]            # observables: nombre, tipo, unidad, rango plausible
    control_surface: ControlSurface     # perillas externas declaradas + rangos + costos
    sources: dict[str, SourceSpec]      # fuentes observacionales (ver §3)

    def sample(self, regime: Regime, n: int, seed: int) -> Table
        # corre el MECANISMO LIMPIO bajo el régimen; devuelve tabla con schema exacto

# Regime = {"config": {...},      # punto de la superficie de control (do() es el caso mínimo;
#                                 #  también señales temporales, políticas condicionales)
#           "context": {...},     # condiciones no intervenibles
#           "horizon": int|None}  # para mundos dinámicos
```

### 2.2 Las tres capas

| Capa | Implementación | Estructuras que puede esconder |
|---|---|---|
| Mecanismo | `world.py` (ecuaciones/dinámica) | grupos, regímenes, memoria, feedback, entidades o mecanismos faltantes |
| Canal de observación | operadores declarados en `meta.json` | error de medición, proxies, batch effects, observador |
| Proceso de muestreo | operadores declarados en `meta.json` | selección, survivorship, censura |

**Invariante**: las corrupciones observacionales viven en las fuentes; el salto objetivo puede
vivir en cualquiera de las tres capas. `world.sample()` (lo que usa el scorer) conserva la verdad
limpia del mecanismo. El agente recibe las vistas legales vía `observe`; la corrección conoce qué
proceso las produjo.

### 2.3 Familias de mecanismos v0 (el catálogo de motores)

| Familia | Ejemplos de instancia | Formalismo |
|---|---|---|
| SCM estático | entrada-respuesta, riesgo operativo, scoring | ecuaciones estructurales |
| Compartimental | flujo entre compartimentos, mezcladores, tanques | ODE |
| Crecimiento/saturación | logístico, Gompertz, adopción | ODE |
| Colas/servicio | M/M/k, triage de tickets, soporte | simulación de eventos discretos |
| Feedback/regulación | termostato, mercado con ajuste de precios | ODE |

Fuentes posibles: libros de modelado aplicado, motores publicados portados y mecanismos sintéticos
controlados. El catálogo v0 evita inventar física innecesaria, pero **no es una lista cerrada**:
cualquier motor entra si pasa las compuertas del caso; ninguno entra por realismo o fama solamente.
Post-v1: redes de reacción, agent-based, N-body, SBML y autómatas/SCMs generados.

#### 2.3.1 Motor reemplazable; situación causal no reemplazable

El **motor** es el procedimiento forward que genera resultados. El **mundo WAGER** agrega la
estructura escondida, las vistas y acciones legales, la historia, el presupuesto, la tarea y la
batería. Portar un N-body, un modelo SBML, Hodgkin–Huxley o un SCM no crea por sí solo un
experimento sobre saltos.

Dos motores son intercambiables para un claim únicamente si preservan estas compuertas:

1. **Necesidad:** el mejor rival serio sin el salto sobrevive en la rutina pero pierde de forma
   material en el examen.
2. **Identificabilidad activa:** existe al menos una observación o intervención legal que separa
   las explicaciones; tamaño o caos sin una prueba discriminante no cuentan.
3. **Accesibilidad y expresión:** el agente puede conseguir esa evidencia y representar la forma
   ganadora con su presupuesto, interfaz y cómputo.
4. **Visibilidad conductual:** el reward premia la consecuencia del salto, no una etiqueta ni una
   forma particular de código.
5. **Anti-atajo:** brief, piel y fama del simulador no permiten resolver sin datos. Baseline
   `DataBlind`/sin-datos obligatorio para motores o mecanismos conocidos; si gana, neutralizar,
   trasplantar de dominio o reclasificar como tarea de recuperación.

La complejidad forward y la dificultad inversa son ejes distintos. Ejecutar una verdad puede ser
barato aunque inferirla desde evidencia parcial sea difícil porque muchas causas producen salidas
parecidas. El diseño buscado no maximiza oscuridad: fabrica una **equivalencia rutinaria** y deja
una **prueba decisiva alcanzable** que la rompa. Replicar un salto en motores distintos es el
control de que medimos la edición estructural y no una peculiaridad del anfitrión.

### 2.4 Piel semántica y perilla de prior

Cada mundo lleva naming + dominio + narrativa. `meta.json` registra `prior_reliability ∈ [0,1]`: correlación entre lo que un panel de LLMs frescos espera del mundo dado solo el naming, y la verdad del programa. El curriculum controla la *base rate* de sorpresa con esta perilla (`docs/archived/NORTH_STAR_full.md` §4.6, anti-contrarian).

Para un claim de abducción creativa, `prior_reliability` no basta: se registra además el desempeño
sin evidencia y, cuando el mecanismo sea público o canónico, una piel neutral/trasplantada. La
condición familiar mide recuperación y aplicación de conocimiento; la neutral mide reconstrucción
estructural desde la evidencia. Ambas son válidas, pero autorizan titulares diferentes.

---

## 10. Tipos de caso = regiones del espacio producto `[ESTABLE]`

Un caso = elección en 5 ejes: **motor × operadores × superficie × forma de batería × stakes**. Sin maquinaria por tipo — apodos de esquinas:

| Apodo (suite) | Motor | Operadores típicos | Superficie | Batería | Stakes |
|---|---|---|---|---|---|
| Causal con cliente | SCM | 1,2,6,7 | intervenible | concentrada en decisiones | cliente decide |
| Anomalías (**Anomaly**) | cualquiera | 12 (+5) | mixta | consecuencias de la contaminación | "algo anda mal, ¿qué?" |
| Constructos latentes (**Latent**) | SCM/ODE | 8 | intervenible | regiones donde el promedio engaña | grados |
| Prior vs evidencia (**Prior**) | cualquiera | cualquiera + prior_reliability baja | mixta | donde intuición y verdad chocan | move 37 |
| Observacional/forecast (**Horizon**) | ODE | 4,5,9 | solo elección de qué mirar | horizontes y contextos held-out | predecir lo no visto |
| System mapping | cualquiera | 2–3 variados | amplia | plana y ancha | sin cliente |
| Diagnóstico/causa raíz | compartimental/colas | 12 variantes | reparaciones | contrafactuales de reparación | "¿cuál proceso está activo?" |
| Identificabilidad | SCM | acceso restringido | mínima | queries no-identificables | gana el ensemble ancho honesto |

**Triangulación como patrón de primera clase** (enriquece la suite Horizon): mundos con 2–3 fuentes cuyos sesgos difieren de modo que solo cruzándolas se identifica la verdad sin experimentos — exactamente cómo identifica la ciencia observacional real. Junto con el certificado de recuperabilidad (§7), evita que Horizon degenere en entrenar pura abstención.

### 10.1 Contrato de ventana de calibración (suite Latent, v2+) `[ESTABLE en concepto — Decision Log v0.47; spec-first: este contrato y el brief preceden a todo código]`

El tríptico de controles de la suite Latent: **v0** = proxy limpio (el observable proxia al latente), **v1** = dial declarado (el prior es una perilla visible), **v2** = **el caso real**: estado latente por-lote que se INFIERE de una ventana chica. Pre-registro estructural: bajo la vara de la escalera-de-6, `gap(v0) ≈ gap(v1) ≈ 0` y `gap(v2) > 0`.

- **(a) Mix oculto**: desaparece de la superficie de control Y de los inputs de `model()`. Parámetro oculto por lote, muestreado de un prior que el agente no ve, con rango que excede el histórico.
- **(b) La ventana**: `regime.context` incluye una **muestra de calibración chica y sin etiquetar** del lote (lecturas de `marker`; `n_cal` declarado por ítem), generada por el mundo con el **seed lado-mundo** → CRN intacto: la MISMA ventana llega a submission, anclas y rivales. La firma `model(regime, n, seed)` NO cambia — el regime se enriquece. Protocolo versionado + regímenes de humo que lo ejerciten.
- **(c) `n_cal` es LA PERILLA de dificultad.** Batería: mix oculto (incluso fuera del rango histórico) × `n_cal` chico/grande. Pre-registro: la **curva gap(n_cal) decreciente ES el resultado**.
- **(d) Episodio**: la fuente histórica entrega lotes de composición variable **no etiquetada**; la superficie ofrece dosis y muestreo de lotes, jamás mix. **(d-exp) se re-estandariza**: grilla dosis × lotes (mix ya no es perilla experimentable).
- **(e) Anclas**: `world.py` necesita el mix oculto → **NO puede ser el techo alcanzable**. **Techo R=1 := verdad BAYES-ADAPTIVA** (mecanismo verdadero + posterior por likelihood del mix desde la ventana). `world.py`-con-mix-oráculo = **cota diagnóstica**; la distancia techo↔oráculo = **piso aleatorio de inferencia** (se reporta, no se scorea contra lo inalcanzable). Ingenuo = pooled que ignora la ventana.
- **(f) Equidad**: la media de marker del lote identifica el mix (lineal en p) → la escalera incluye **miembro PLUG-IN obligatorio** (estadístico de ventana → dial recuperado → reweighting suave). **El theory gap verdadero se mide CONTRA ese miembro** y vive en `n_cal` chico + mixes extremos, donde likelihood le gana a plug-in por eficiencia.
- **(g) Pre-registros del caso**: curva gap(n_cal) decreciente; gap vs plug-in ≥ piso de resolución en `n_cal` chico y mixes fuera de rango; v0/v1 cerrados bajo la vara; ambas monedas (R y |ΔP|); mecanística grande (el confounding sigue instalado).
- **(h) Pre-compromiso honesto**: si v2 también cierra a `n_cal` realistas → se registra que *forzar representación de un latente ESCALAR puede ser inconmensurable bajo scoring conductual* (hallazgo publicable) y se repiensa el arquetipo (latente multidimensional / ventana costosa) ANTES de otra vuelta ciega.
- **(i) Doctrina intacta** (§7): responsabilidades por muestra PROHIBIDAS; estadísticos de ventana ADMISIBLES.

---

## 11. Las tres bibliotecas minables (fuentes, no imaginación) `[ESTABLE]`

1. **Zoológico de motores**: textos de modelado aplicado — modelado dinámico multi-compartimento, teoría de colas, dinámica de sistemas, ecología cuantitativa.
2. **Biblioteca del error científico** (→ operadores): Catalogue of Bias (Oxford, ~60 entradas documentadas), el catálogo clásico de Sackett (1979), taxonomías de sesgo de estudios observacionales, literatura de discrepancias observacional-vs-experimento, Retraction Watch, post-mortems de replicación.
3. **Archivo de investigaciones resueltas** (→ semillas para digestion): informes NTSB (mecanismo adjudicado por investigación formal), case studies de investigaciones con respuesta conocida, post-mortems de incidentes SRE, pares observacional→experimento (también eval E4).

El designer LLM solo *propone* (operadores nuevos, composiciones); ejecución + brechas + archivo *deciden*.

---
