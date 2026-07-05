# Scoring — implementación

> Referencia técnica (ex ARCHITECTURE.md). Los números de sección (§N) se
> preservan; las citas '§N' de otros docs resuelven acá o en los hermanos de
> `docs/reference/`. El *por qué* llano está en `WIKI.md`.

## 9. Scoring — implementación `[EN DEBATE en elección de D y λ]`

```python
def score(submission, world, battery, lam, m):
    fid = 0.0
    for w, regime, seed_w in battery:
        real = world.sample(regime, n=1000, seed=seed_w)   # lado mundo: seed fijo por ítem,
                                                           # compartido entre submissions (CRN)
        d = 0.0
        for j in range(m):                                 # m repeticiones lado maqueta
            seed_m = derive_seed(seed_w, j)                # ≠ seed_w, determinístico
            pred = run_sandboxed(submission, regime, n=1000, seed=seed_m)  # crash → D_MAX_item
            d += energy_distance(standardize(real), standardize(pred)) / m
        fid -= w * min(d, d_max_item(regime, seed_w))      # D_MAX_item = 1.5 × D(verdad, nulo)
    return fid - lam * mdl(submission)   # mdl v0 = len(zlib(AST minificado)); ensembles: §9.2
```

**Semántica de seeds (v0.3).** Lado mundo: un seed por ítem, persistido en `battery.json`, compartido entre todas las submissions — common random numbers: las comparaciones entre submissions y contra las anclas son de baja varianza. Lado maqueta: `derive_seed(seed_item, j)` por repetición, **nunca** el seed del mundo — si coincidieran, entregar `world.py` literal daría D=0 exacto y el techo S_verdad perdería su semántica de "solo ruido de muestreo" (bug del pseudocódigo v0.2). Producción scorea con seeds fijos (reproducible); L2 (§13) estima el ruido re-scoreando con B sets re-sampleados. **Nota para E2 (diferida)**: los seed-sets de batería rotan periódicamente durante el entrenamiento — con realizaciones eternamente fijas, la policy puede sobreajustarlas (leakage lento).

- `D` default: **energy distance** (basada en muestras, propia). Alternativas en evaluación: MMD, CRPS por marginales. Estandarización por columna con estadísticas de la verdad.
- **Mundos-trayectoria (v0.68-R1)**: el entregable es formato LARGO (`unit_id, t, y`; la grilla del ítem viaja DECLARADA en `regime.context["t_grid"]`) y **`n` cuenta UNIDADES** — la tabla trae `n × len(t_grid)` filas. Antes de D, TODA muestra (verdad, nulo, rivales, submissions) cruza el pivot largo→ancho (`wager.reward.trajectory.pivot_trajectories`, función pura con tests de propiedad): una fila por unidad, una columna por timestamp de la grilla (`y@t`) — los timestamps son columnas y D opera como siempre. Tabla que viola la grilla (lecturas faltantes/duplicadas/fuera de grilla) = crash → D_MAX (§8). La sanidad de escala corre sobre la salida PIVOTEADA (columnas tempranas de varianza chica = la 6ª patología esperada de la familia escala). Mundos estáticos: protocolo ausente, maquinaria inerte, byte-idéntico.
- Ensemble: `[(peso, code)]` → D sobre la mezcla muestreada según pesos.
- `λ` calibrado empíricamente sobre la suite E1 para que MDL pese 5–10% del rango de score.
- **Differential testing**: búsqueda (random restarts / CEM) de `r* = argmax D(submission, world)` — auditoría y engrosamiento de batería.
- **PROHIBIDO**: cualquier salida de LLM en este cómputo (regla dura, `CLAUDE.md`).

### 9.1 Normalización del reward entre mundos (obligatoria para RL)

La distancia cruda depende de dimensionalidad, escala de ruido y composición de la batería — scores de mundos distintos NO son comparables, y RL sobre escala caótica rompe la advantage estimation. Anclar con los rivales, que ya se computan para los certificados:

```
R = clip( (S_agente − S_ingenuo) / (S_verdad − S_ingenuo), 0, 1 )
```

`S_verdad` = score de entregar `world.py` mismo (techo: solo ruido de muestreo, garantizado por la separación de seeds de §9); `S_ingenuo` = score del rival (a) en su serialización canónica (§5). **Las tres cantidades — S_verdad, S_ingenuo, S_agente — se computan con la MISMA función completa (fidelidad − λ·MDL)**: R(`world.py`) = 1 por construcción y la normalización es autoconsistente; una submission igual de fiel pero más corta que `world.py` puede superar el techo (clip en 1). **Excepción — mundos-ventana (suite Latent v2+)**: `world.py` lee estado oculto por-lote que ninguna submission puede ver → **NO es el techo alcanzable**; ahí `S_verdad` := **verdad Bayes-adaptiva** inferida desde la ventana de calibración (contrato completo en [`world-model.md`](world-model.md) §10.1(e)). Cambia SOLO el ancla del techo; la fórmula de normalización es la misma. *(Semántica de anclas = tripwire #1 de `CLAUDE.md`: no tocar sin releer §10.1(e).)* Beneficios: rewards comparables entre mundos, brechas adimensionales, dificultad interpretable. **El rango de normalización `S_verdad − S_ingenuo` es también el rango contra el que se miden los márgenes de L1** (§13, v0.12) — NO `S_verdad − S_nulo`: el nulo es un outlier patológico off-support (ignora la variable controlada) que infla el rango, y R clipea la región sub-ingenuo de todos modos. Caso borde: `S_verdad − S_ingenuo ≈ 0` → el mundo no discrimina → se rechaza (equivale a brecha mecanística ≈ 0). Issue conocido de E2 (decisión diferida, Decision Log v0.10): el clip en 0 aplana el gradiente debajo del rival ingenuo — candidatos: ancla nula para curriculum temprano / variante sin clip para RL.

### 9.2 Detalles de contrato que importan

- **Piso de varianza**: el apareamiento de seeds alinea el lado del mundo pero NO el lado maqueta (`derive_seed`, §9) → varianza irreducible que solo bajan las m repeticiones (costo total de scoring: K × n × m por episodio; medir CV en el primer slice y reportar la descomposición lado-mundo / solo-lado-maqueta).
- **Techo de tiempo por llamada** de `model()`: una maqueta lenta multiplica el costo de scoring ×K.
- **MDL v0 = `len(zlib.compress(ast_minify(code)))`** (anti code-golf; resuelve la contradicción zlib-crudo vs AST de v0.2). **Ensembles: `mdl = len(zlib.compress(concat(miembros minificados, orden canónico)))`** — la estructura compartida comprime una sola vez: un ensemble de variantes (incertidumbre honesta sobre parámetros/mecanismos) paga ~un miembro; uno de programas no relacionados paga completo. Resuelve la tensión MDL-vs-ensemble sin maquinaria extra (Decision Log v0.10).
- Energy distance con columnas mixtas (categóricas + continuas): codificación declarada y fija.

### 9.3 Score combinado — funcionales de stakes `[EN DEBATE — spec nuevo, Decision Log v0.26]`

**Por qué.** El probe de Latent (Decision Log v0.25) mostró que la energy distance sobre marginales casi no penaliza multimodalidad a momentos fijos: un oráculo Gaussiano (media+covarianza exactas por-régimen, **unimodal**) saca R=0.96 contra una verdad máximamente bimodal (clusters en ±12, ruido 0.5). La estructura latente, cuya firma observable es de orden superior (modos/colas), queda **invisible** al reward → la suite Latent (constructos latentes) no es recompensable con energía-sola. Es el **ataque #5 (Goodhart del proxy) realizado** y cazado por el certificado **antes de entrenar**. Fix: el score por ítem suma, a la energía, términos de **funcional de decisión declarado en stakes**.

**Encuadre (Decision Log v0.27, teoría de scoring rules).** No existe métrica libre-de-decisión: **toda `D` fija es un prior congelado sobre qué diferencias importan**, y la relevancia es dependiente del mundo. El score correcto se *deriva de los stakes* (un scoring rule propio se define respecto de la decisión/pérdida, no en abstracto). Por eso (A) no es un parche: es **base universal débil (energía) + amplificación declarada mínima-suficiente** donde los stakes dicen que importa. La energía sola era el caso degenerado "todas las diferencias pesan igual", que el hallazgo de Latent refutó. **La opción (B)** (una `D` más sensible, p.ej. MMD bandwidth fino) **queda reclasificada: vive como diagnóstico permanente de fábrica (el `theory_gap_probe`), JAMÁS como reward** — meter más sensibilidad cruda al reward premia estructura que la decisión no usa (el espejo del blind-spot).

**Score combinado por ítem.** Para cada ítem `(w, régimen, seed)`:
```
d_item = energy_distance(std(real), std(pred))            # identidad conductual (término base, como §9)
       + Σ_F  c_F · S_F( |F(pred) − F(real)| )            # funcionales declarados, ESTANDARIZADOS por tipo
d_item = min(d_item, D_MAX_item(c_F))                      # cap = 1.5×D_comb(verdad,null); FUNCIÓN de c_F
fid   -= w · d_item
```
- `F`: funcional de la biblioteca tipada (abajo), evaluado sobre **las muestras** (no sobre parámetros). `F(real)` se computa de la verdad con los mismos seeds apareados (CRN).
- **D_MAX bajo el combinado (amendment 4, Decision Log v0.28):** `D_MAX_item = 1.5 × D_combinada(verdad, null_model)` — el cap y el piso de crash se calibran en la **métrica real** (no en energía-sola), así `R(crash) < R(null)` se preserva término a término (null = cap/1.5 por construcción). **El cap es función de `c_F`** → en el barrido de calibración se **recomputa `D_MAX_item` para CADA `c_F` candidato** (jamás caps de energía-sola con un cap cambiado después). La suite de sanidad de escala (§13) se extiende al combinado y se afirma para `c_F` en todo el rango del barrido.
- **Estandarización del término funcional — POR TIPO en la librería (Q2, Decision Log v0.28), una sola vez**, para que `c_F` quede **adimensional y transferible** entre funcionales y suites: `exceedance` → `|ΔP|` crudo (nativo `[0,1]`); `quantile` / `subgroup_mean` → `|Δ|/σ_verdad(columna)` (misma jugada que la estandarización de la energía); `expected_loss` → `|ΔL|/rango_de_L declarado en el caso`. **Prohibida la normalización null-relativa por-ítem EN LA MÉTRICA** (`|ΔF|/|F(verdad)−F(null)|`): explota cuando `F(verdad)≈F(null)` — que es el **caso central**, no un borde (en el histórico de Latent v1, `P(falla)≈0.5≈null`) — y es doble normalización (R ya ancla globalmente contra las anclas). Distinción dura: **la batería puede normalizar para SELECCIONAR regímenes; el score NO puede normalizar para SCOREAR** (cuarta patología de escala, evitada en diseño — ver §13).
- `c_F`: peso relativo del término, **calibrado UNA vez por suite** con criterio **mínimo-suficiente** (el menor `c_F` que hace visible la estructura instalada), luego **congelado y registrado** — **NO por caso** (calibrar por caso sería autoría). Provisional hasta E1.
- **Separación calibración/validación (regla dura, Decision Log v0.27 — cierra la circularidad).** Los rungs/mundos usados para calibrar `c_F` quedan **INHABILITADOS como evidencia de validez**. La validez se gana en: L1 de los OTROS mundos (no calibrantes) + E1 + la predicción (iii) (la batería pesa donde los rivales discrepan en el funcional) + held-out. Y **toda conclusión sustantiva se reporta con BANDA DE SENSIBILIDAD** (re-scorear con `c_F` ×2 y ÷2): si la conclusión se da vuelta en esa banda, es filo de cuchillo y se declara. *Sin esto, "tuneo `c_F` hasta que la escalera separe" es tuning-to-pass disfrazado — exactamente lo que L1 debe detectar.*
- La energía **sigue siendo el término base**: ningún funcional la reemplaza. Es la identidad conductual completa; el funcional solo agrega sensibilidad al rasgo decision-relevante que la energía no ve. **Identidad por construcción**: un caso que no declara funcionales tiene score combinado ≡ score de §9 (la suite del dummy no cambia).

**Biblioteca tipada de funcionales** (hermana de la de operadores §3: minable, **crece a demanda de stakes reales, nunca por imaginación suelta**; el solver jamás la ve):

| Funcional | `F(muestras)` | Estandarización de `\|ΔF\|` (para que `c_F` sea adimensional) |
|---|---|---|
| Exceedance de umbral | `P(outcome ≷ θ)` | `\|ΔP\|` crudo (nativo `[0,1]`) |
| Cuantil | `q_τ(outcome)` | `\|Δ\|/σ_verdad(columna)` |
| Media condicional por subgrupo declarado | `E[outcome \| subgrupo]` | `\|Δ\|/σ_verdad(columna)` |
| Pérdida esperada bajo regla declarada | `E[loss(decisión(régimen), outcome)]` | `\|ΔL\|/rango_de_L declarado` |

**Preferencia de la librería (Decision Log v0.27).** Si el brief define una **decisión nítida** (una regla de acción única), se usa **UN solo funcional de pérdida esperada** `E[loss(decisión, outcome)]` — menos perillas, menos superficie de calibración. La suma de varios funcionales queda solo para mundos **sin regla de acción única** (stakes difusos). Y el **valor de información** de descubrir el latente (VoI) NO entra acá: es un **oráculo de valor** que vive en firmas/análisis, **PROHIBIDO en el reward** — recompensar VoI sería premiar una conducta (investigar), y las conductas se observan, jamás se premian (`docs/archived/NORTH_STAR_full.md` §2.1).

**Criterio de completitud (cierra "¿cuántos funcionales?", Decision Log v0.27).** No es whack-a-mole abierto: es un **invariante de fábrica POR-MUNDO y chequeable**. (1) Toda estructura que **instalamos** (operadores declarados) debe pasar el **certificado de visibilidad** (§7) bajo el score combinado — y nosotros instalamos todo lo del mundo. (2) El residuo emergente (estructura no instalada a mano, surgida de la composición) lo cubre el `theory_gap_probe` como diagnóstico permanente. (3) Lo que ni el probe ve es el **ataque #14** (techo de lo comprensible), ya declarado como límite abierto. Suficiencia = visibilidad de lo instalado, no enumeración infinita de funcionales.

**REGLA DE TRAZABILIDAD (anti-Goodhart del diseñador).** Cada funcional instanciado en un caso **DEBE citar la cláusula verbatim del brief que lo promete** — es el checklist de promesas (Decision Log v0.24) en reversa: el brief promete → el funcional lo codifica. Si el brief no enuncia el rasgo (p.ej. "falla" en Latent), se **corrige el CASO** (brief + `meta.json`) con registro y re-certificación; **no se inventa el funcional para que el gap aparezca**. El writer del brief sigue ciego a batería y rivales; la cláusula vive en `meta.json` y el writer la narra.

**Contrato del agente: INTACTO.** `model(regime, n, seed) → tabla`. Los funcionales se computan de SUS muestras, server-side, post-hoc; el agente nunca ve cuáles se scorean (como la batería). **Cero LLM** en el cómputo (los funcionales son numpy puro; CI §13-L0 sin cambios).

**Batería: UN solo método.** El desacuerdo entre rivales (§6 paso 2) se computa en el **mismo** score combinado, no en energía-sola → la batería concentra peso donde los rivales discrepan en el **funcional** (colas, shifts de grado), dándole a la predicción (iii) su test real.

**Normalización (§9.1): forma sin cambios.** S_verdad, S_ingenuo, S_agente con la MISMA función completa (ahora energía + funcionales − λ·MDL). `R(world.py)=1` se preserva (F(world.py)=F(verdad) salvo ruido de muestreo).

**Mini red-team — "cómo Goodharteo el funcional" (5 ataques + defensa):**
1. **Matchear el funcional, romper el resto** (ajustar P(falla) exacto con basura en lo demás) → lo paga la **energía base** (término aditivo dominante, no reemplazado).
2. **Funcional no promovido por el brief** (el diseñador lo declara para fabricar el gap) → **regla de trazabilidad**: cita verbatim o se corrige el caso.
3. **Colapsar el funcional a constante** (predecir siempre la media) → `|F(pred)−F(real)|` lo penaliza donde F es sensible al modo (P(falla) de un unimodal ≠ bimodal: la evidencia del probe, brecha 0.16–0.29).
4. **Gaming del cap** (inflar un término para saturar D_MAX y ocultar otro) → cap per-ítem sobre la **suma**; la suite de sanidad de escala (§13) verifica ninguna distancia > D_MAX y el orden sin clipear.
5. **Overfit a los seeds del funcional** (P̂ con n finito tiene ruido binomial) → seeds apareados (CRN) + m reps; **L2 verifica CV(R)<5% incluyendo los términos funcionales** (ruido binomial de P̂ con n=1000, m=2 ≈ 1.6 pts — dentro de presupuesto; verificar en el slice).

---
