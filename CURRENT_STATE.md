# CURRENT_STATE — WAGER

> Estado vivo del repo: qué corre hoy, qué falta. Lo mantiene Claude Code al día en cada
> sesión de trabajo (regla: NORTH_STAR §0.10). Última actualización: **2026-07-02**.

## Migración de repo (2026-07-02)

El proyecto vive ahora en `research-worlds-envs`
(github.com/lucaspecina/research-worlds-envs). La **historia git previa** — incluidos los
hashes de pre-registro citados en el Decision Log (`30365fa`, `255d781`, `7ccaf23`) — queda
en el repo viejo `../wager/.git` (NO borrar); los **traces de episodios** (E0/E0.5) están
archivados en `../wager_traces_archive/` (fuera del repo por diseño, ver `.gitignore`).
Copia verificada: suite completa verde en venv fresco. Detalle en Decision Log v0.32.

## Qué corre hoy

**Slice 1 (reward path), Slice 2 (harness C1+C2+C3) y slice de derivación (rivales+batería+
certificados) completos y verdes.** `pip install -e .[dev,agent,report]` + `pytest` →
**86 verdes, 2 skip** (tests LLM opt-in; correr con `RUN_LLM_TESTS=1`). Python 3.13.

**Última sesión (v0.32–v0.33)**: migración al repo nuevo (arriba) + sincronización de headers
+ **hardening post-re-skin** (v0.33): trazabilidad post-skin verificada (cláusula de v1
verbatim ✓), **brief de v0 autorado** (misma cláusula/skin que v1; marker limpio y en la
fuente barata), footnotes de procedencia de artefactos semánticos pre-skin (abajo), y **lint
de headers + trazabilidad en CI** (`tests/test_doc_headers.py`). Antes (v0.30–v0.31):
auditoría código-vs-docs + cierres v0.31 (banda 20–35% canonizada; protocolo de calibración
de `c_F` PRE-REGISTRADO). **Próximo paso de trabajo: (2) calibrar `c_F` mínimo-suficiente**
(ver "Orden del slice" abajo; la grilla la detalla Lucas antes del verbatim al log).

- `wager/contracts/` — contratos Pydantic v2 (world, case, episode, reports).
- `wager/reward/` — **zona cero-LLM** (allowlist de imports en CI + no importa
  `wager.agent`/`wager.harness`): `seeds`, `distance`, `mdl`, `sandbox`, `scorer`
  (R, D_MAX), `ladder` (L1), `variance` (L2), `episode_score` (R de submission).
- `wager/factory/` — `case_loader`, `world_lint` (lado fábrica; LLM permitido acá).
- `wager/agent/` — **lado solver (LLM)**: `llm_client` (Foundry v1 multi-turn),
  `cells`. Nunca importado por `wager.reward`.
- `wager/harness/` — `world_server` (autoridad del episodio: verbos + ledger +
  humo + scoring), `kernel_proc` (kernel en proceso separado + env proxy data-only),
  `episode` (loop LLM + guardas + trace), `env`/`case_episode`, `kernel`/`c1_env` (C1).
- `cases/dummy_dose_v0/` — `world.py`, `battery.json`, `meta.json` (+ episode),
  `ladder/`, `brief.md` (cara pública, ASCII), `solvers.py`, runners
  (`run_slice`, `c1_smoke`, `c2_pair`, `e0_episode`, `e05_episodes`,
  `make_ladder_fixtures`, `ablate_m`, `diagnose`), `traces/` (E0/E0.5).

### Entregables medidos (`python cases/dummy_dose_v0/run_slice.py`, defaults v0 K=16 n=1000 m=2)

- **L1**: orden total de las 6 verdades degradadas con todos los márgenes ≥5%,
  cada pelfalla anotado como ancla (R fijo) o medición. R = {verdad 1.000
  (anchor:S_truth), perturbado 0.942, linealizado 0.728, gemelo 0.344, ingenuo
  0.000 (anchor:S_naive), nulo 0/−2.53 (reference:S_null)}. Margen más ajustado:
  verdad→perturbado 5.85%.
- **L2**: CV(R) = 1.17% sobre 20 seed-sets (objetivo <5%); CV(S_verdad) = 0.54%;
  descomposición std(R) total 0.0084 = lado-mundo 0.0075 ⊕ lado-maqueta 0.0039.
- **Costo K×n×m** (16×1000×2): L1 6.4s, L2 27.1s.
- **Ablación de m** (`ablate_m.py`): CV(R) 1.17/1.13/1.10% para m=2/3/5 → m=2
  default v0 (el lado-mundo domina; subir m casi no mueve el total).

## Hallazgos del Slice 1 (Decision Log v0.12)

La escalera L1 destapó tres bugs de **maquinaria** (no de fixtures) al fallar el
orden total; se diagnosticó per-ítem (`diagnose.py`) antes de tocar nada:
1. D_MAX clampeaba toda distancia (debía asignarse solo en crash).
2. D_MAX referenciaba el null equivocado (permutación de la verdad, no el null model).
3. Los márgenes L1 se medían contra S_verdad−S_nulo (un outlier patológico);
   ahora contra el rango de normalización S_verdad−S_ingenuo (unidades de R).
Fixtures de la escalera intactos.

## Resultados del Slice 2 (C2 + C3, Decision Log v0.15–v0.16)

> **Footnote de procedencia (v0.33)**: E0/E0.5 y la firma conductual se jugaron contra los
> briefs PRE-skin (re-skin 2026-07-02). Historia válida; NO comparable con episodios futuros
> sin re-correr contra el brief actual.

- **C2**: naive R=0.044 vs canonical R=1.000 por el juego real (investigar gana).
- **E0** (gpt-5.4): R=0.895, 4 turnos — jugable; 1 submit falló humo y se corrigió.
- **E0.5 (corregido, seeds arreglados)**: gpt-5.4 R∈{0.000, 0.960}, DeepSeek-V3.2
  R∈{0.915, 0.919}. Todos honestos, 0 crashes. Firma conductual v0.1
  (attribution_before_experiment) = True en los 4.
- **RETRACTADO (v0.16)**: el "DeepSeek R=0 = brecha de teoría" de v0.15 era un
  **artefacto de rango de seed** (legacy `np.random.seed` rechaza ≥2³²;
  `derive_seed` daba 64 bits → 16/16 crashes → D_MAX → R=0). Fix: seeds 32-bit +
  smoke reforzado. R real de DeepSeek ≈0.98. El dummy NO muestra brecha de teoría
  (un modelo sin latente saca ~0.92). Reportar SIEMPRE R_uncl (clips≠mediciones).
- Fricciones resueltas: no-ASCII en briefs; `hasattr` faltaba; seeds 64-bit.

## Slice de derivación automática (EN CURSO, Decision Log v0.17–v0.18)

Pre-registración v0.17 (predicciones dummy/Latent ANTES de correr). Hecho:
- **Mundo estructurado** (`world.py` PARAMS + mechanism; meta declara `ablation`).
- **`score_callable`** (reward): scoring in-process de rivales callable de fábrica.
- **Rivales a/d** (`wager/factory/derive_rivals.py`) + **certificados**
  (`certificates.py`): brecha de teoría + mecanística.
- **Certificado dummy ✅ (predicción i CONFIRMADA)**: theory gap **0.062** (no-latente
  recupera R=0.938), mechanistic gap **0.990**. El dummy es trampa de confounding,
  no de latente. La disciplina cazó 2 artefactos de rival débil (predicción registrada).
  - **Procedencia (footnotes v0.30, NO correcciones):** theory gap 0.062 = vs
    **proto-(d-exp)** (grilla `do(dose)` ad-hoc, `standardized=false`); re-correr UNA
    vez cuando exista la (d-exp) estandarizada (paso 3) — pre-registro: cambia poco.
    Mechanistic gap = vs **(a) solo**; bajo v0.29 = vs best{(a),(d-obs)}; recomputar
    cuando nazca (d-obs) — pre-registro: el dummy se mueve poco (movimiento grande →
    investigar (a), no retunear). El acceso de cada rival viaja ahora EN el
    `certificates.json` y el dossier (certificados auto-descriptivos).
- **Rival (c) panel ✅** (LLM-first milestone, `rival_c_panel.py`): 3/3 LLMs frescos
  compilan a programa ejecutable; el prior aterriza < ingenuo (R≈0). **Footnote (v0.33)**:
  elicitado del brief PRE-skin (ídem brecha de prior 1.011 de v0.19); el rival (c) no se
  persiste → **re-elicitar el panel con el brief actual antes de cualquier reuso**.

**Hecho desde entonces (v0.20–v0.24)**:
1. ✅ `battery_builder` (candidatos + `disagreement_norm`=D/D_MAX + piso de elegibilidad +
   `stakes_relevance` + dedup) → batería 100%-derivada; **aceptación (i) MET** (criterio de
   producción: monotonía + extremos).
2. ✅ Rival (b) gemelo (ablación de operador + refit) + **escalera de capacidad completa**
   (a + linear + GBM + gemelos = 5 rivales del desacuerdo; `build_standard_rivals`).
3. ✅ Ronda de hardening v0.24: cola de cohort fuera-de-registro, robustez al seed
   (~6.5pp estructural → producción necesita ~200 ítems), checklist de promesas del brief
   en el dossier. **Retractación de Claude** (item 5): out-of-record discrimina el rung
   linealizado → suba de peso a discutir con Lucas.

**Pendientes v0.24 — CERRADOS/ENCAMINADOS (v0.31)**:
- ✅ **Peso out-of-record DECIDIDO**: mantener y canonizar **banda 20–35%** fuera-de-registro
  (ARCHITECTURE §6; los stakes fijan el nivel, la discriminación es constraint ya satisfecho).
- Re-auditoría del mapa de cobertura: **la hace Lucas** con el checklist de promesas → con su
  APROBADO expira el bootstrap (battery.json de mano → derivada). Sigue gateado en Lucas.

## Latent (2º mundo) — predicción (ii) REFUTADA, hallazgo de scoring (Decision Log v0.25)

`cases/mendel_subtypes_v0/world.py` (grados latentes con efecto de dosis de signo
opuesto + lectura de sensor bimodal) + `theory_gap_probe.py`. **Pre-registro `30365fa` antes del
código.** Resultado: **el control decisivo (oráculo Gaussiano de momentos por-régimen,
unimodal) saca R=0.963** → gap irreducible **0.037** (≈ dummy). El "gap" de 0.35 vs el
no-latente homoscedástico era artefacto de heteroscedasticidad. **La distancia de energía
sobre marginales casi no ve multimodalidad a momentos fijos** → la heterogeneidad latente
NO es recompensable con el scoring actual. PERO un funcional `P(falla)` muestra brechas
0.16–0.29 → el latente SÍ es decision-relevante.

**DECISIÓN (v0.26→v0.27): (A) funcionales de stakes, SPEC-FIRST — APROBADA (triangulada con
2ª IA) con 2 correcciones de mi estrés-test.** Spec escrito (ARCHITECTURE §9.3 + certificado
de Visibilidad §7 + rung-diagnóstico oráculo §13-L1 + red-team de 5 ataques) + Decision Log
v0.26/v0.27. Correcciones v0.27: **(Q4)** el oráculo de momentos es **diagnóstico** ("¿el
metro ve?"), NO el proxy de brecha de teoría — esa va contra el **mejor sin-latente FLEXIBLE**
(mixturas/GBM condicional). **(Q5)** **Latent v0 no tiene latente genuino** (el lectura de sensor
limpio lo proxia) → **Latent v1**: lectura de sensor ruidoso + ausente de la fuente barata
(comprable) + batería con shifts de mix fuera de soporte; v0 queda como **control negativo**.
Reglas nuevas: separación calibración/validación + banda de sensibilidad (`c_F` ×2/÷2);
completitud = certificado de visibilidad (no whack-a-mole); VoI prohibido en reward.

**Orden del slice (v0.27, EN CURSO)**: **(0)** ✅ brief+meta de Latent v1 con trazabilidad
(`255d781`; FunctionalSpec en contratos) → **(1)** ✅ score combinado en `wager/reward/`
(`7ccaf23`; functionals.py cero-LLM + D_MAX combinado amendment 4 + P1 identidad-por-
construcción verificado; suite 85 verde) → **(2)** calibrar `c_F` mínimo-suficiente +
congelar → **(3)** P2-v1 con el par de control v0/v1 → **(4)** P3 → **(5)** P4 + banda de
sensibilidad.

**Preparación del paso 2 (v0.33–v0.34, HECHA)**: brief de v0 ✅ (excepción de bootstrap
registrada; self-check anti-susurro ✓) · **ladder de v1 ✅** (`make_ladder_fixtures.py`:
7 rungs 2–8, determinístico byte-exacto, ablaciones desde meta, rationale por par;
smoke 7/7 + momentos del oráculo verificados vs verdad) · `battery_derived` verificado
NO texto-derivado (el rival (c) no entra a `build_standard_rivals`) · **grilla de
calibración PRE-REGISTRADA verbatim ✅** (Decision Log v0.34: 27 ítems, bandas en ambos
ejes contra el registro histórico [dosis central-95% = 2.00–8.46], 27.9% fuera-de-registro,
pesos = `stakes_relevance` del builder, `experimentable_range` de mix declarado en meta
v0/v1, CV pre-fijado) + enmiendas pre-ejecución: línea base por-rung (B), gate (ii) de
heterogeneidad sobre el ORÁCULO (C, principio momento-calzado → ARCHITECTURE §7), bug del
refit del gemelo (b) registrado (D, gate antes de P3; NO bloquea el barrido).

**BARRIDO 1 (v0.35)**: guardia disparada (confounding diluido globalmente + bug de escala
CV-relativo → 5ª de la familia); funcional confirmado (oráculo 0.952→0.672 monótono).
**Decisiones v0.36 (Lucas)**: umbral absoluto 3×std; visibilidad POR SUB-BATERÍA
(instrumento-vs-stakes → ARCHITECTURE §7); margen-vs-verdad solo visibilidad+anclas.
**DO-OVER (v0.37) corrido**: sub-batería VALIDADA (conf-ablación separa 1.723 local,
R_obs=−0.723 — peor que el ingenuo localmente); todos los gates pasan en TODO el rango →
`c_F*=0` → **guardia ANTI-COLAPSO disparó**. Hallazgo: **significancia ≠ suficiencia**
(toe-hold real del oráculo: 0.048 = 37× su std 0.0013). **DECISIÓN v0.38 (Lucas): opción
1 — gate = max(3×std propio, PISO DE RESOLUCIÓN 5% [constante L1 v0.10]) → `c_F* = 0.25`
CONGELADO** en ScoringParams (campo nuevo) de v0/v1 + lint de suite en el mismo commit +
corrida confirmatoria bajo el spec final (banda asimétrica pre-declarada: ÷2 falla el piso
por definición; ×2 debe pasar sin inversiones). Replicación del punto ciego v0.25 anotada
(0.952 ≈ 0.952, otra grilla/skin). Pregunta κ-stakes viva → evidencia (P2/E2; gaps
comprimidos o gradiente insuficiente → do-over registrado).

**GENERALIZACIÓN DE LA FACTORY (v0.39, HECHA)**: la clase "recita el schema del dummy"
matada como clase — `CaseSchema` desde meta (decisión/contexto/columnas/rangos), refit
del twin = Gauss-Newton sobre knobs DECLARADOS de operadores no-ablados (self-describing
`refit_knobs`), miembro `logistic_ctx_no_latent` (equidad v0.29), sampler/estratos/dedup
del builder y dossier de certificados genéricos. **Test estructural + audit-guard en CI**
(`test_factory_generalization.py`) — y ya cazó su primer incidente: fallback de 3 niveles
de contexto → no-latente débil → gap del dummy 0.062→0.234; fix por declaración
(`experimentable_range` en el meta del dummy) → ~0.06 de vuelta. Suite **98 verdes**.
**P2 CORRIDO (v0.40)** — celda **AMBOS GRANDES** (v0=0.987/v1=1.052, ratio 1.1×; los tres
(d-exp) al nivel del ancla ingenua; share funcional ≈0) → **guardia del árbol firmado:
investigación de equidad de la escalera, CERO lectura sustantiva**. Diagnóstico: (1)
residual global homoscedástico (la dispersión de outcome crece con dosis en Latent —
trampa v0.18 del lado de la escalera; el dummy homoscedástico nunca la vio); (2) falta
el miembro marker-condicionado que la expectativa "v0 chico" (v0.27-Q5) supone.
**VERIFICACIÓN v0.41 (hecha)**: mecanismo del colapso CONFIRMADO — firma **all-capped**
(v1 33/33, v0 29/33 ítems en D_MAX; outputs por miembro genuinamente distintos → fallback
descartado); columna **outcome** carga (energía 1-D ≈2.0 vs marker 0.03–0.26); peores
ítems todos en dose=0 con d/dmax ~10³–10⁴ (residual global std≈8 vs verdad std≈0.5:
heteroscedasticidad extrema). **Doctrina registrada** (línea sin-latente afilada →
ARCHITECTURE §7). **Miembros implementados**: `hetero_no_latent` (std condicional) +
`marker_conditional_no_latent` (re-muestreo empírico por celda de contexto + interpolación
suave). **P2 CORRIDAS 2–3 (v0.42)**: la corrida 2 destapó el **bug del null de permutación en
`p2_table.py`** (WorldSide sin `null_sample` → D_MAX diminuto → all-capped; regla v0.12
violada en tooling — 6ª captura de la familia de escala; corregido). **Corrida 3
(instrumento sano): celda AMBOS CHICOS** — v0=0.033 (✓ (i): `marker_conditional` cierra,
R=0.967) / v1=0.036 (✗ (ii): `hetero` 0.964, el funcional no lo atrapa; (iii) no
alcanzado; mecanística grande en ambos ✓ 0.859/0.866). **Dato de las dos unidades**: el
best sin-latente de v1 pierde 0.036 en R (bajo el piso) pero mispricea P(scrap) hasta
|ΔP|=0.48 (media 0.134) → **la pregunta κ (v0.38-c) se activa con evidencia**.
**LECTURA v0.43 (Lucas)**: "la 2×2 cambió de moneda — el cuello de botella es el tipo de
cambio del reward, no (todavía) el mundo". Retractación simétrica de (ii) registrada
(off-support sub-preciado a c_F=0.25). **Cuadrante |ΔP| PRE-REGISTRADO** (ramas firmadas:
v0-chico-en-todos-lados + v1-concentrado-en-|mix|>experimentable → mundo vindicado →
κ-do-over; v0 también grande → (a)/(b) y κ espera) — ojo: corrida 3 ya insinúa tensión
(v0 |ΔP| max=0.389, ¿dónde vive?). Spec κ-do-over condicional en v0.43-3 (ancla
`ΔP_decisivo` en meta, regla pricing ≥ piso, `c_F* = max(c_F_vis, c_F_stakes)`,
validación no-circular). Concepto v2 encolado (mix como contexto NO declarado, decide
post-κ).

**CUADRANTE CORRIDO (v0.44, n=4000, `p2_dp_quadrant.json`)**: **ambas predicciones
REFUTADAS** — v0-|ΔP| NO chico (in-exp max 0.302; centro del registro dec4/mix0 = 0.214);
v1 NO concentrado afuera (in-exp media 0.137 > beyond 0.107; max 0.49 afuera pero
0.40/0.31 adentro). Contraste v1/v0 en |ΔP|: ~1.3–1.5× (no ≥3×). **Rama firmada
ejecutada: (a)/(b) activadas, κ-do-over EN ESPERA.** Hallazgo: mispricing de cola
**ubicuo y simétrico** (residual gaussiano cerca del umbral, en ambos mundos). **GO v0.45 (Lucas)**:
retractación doble registrada (mecanismo: umbral cerca de la mediana ⇒ FORMA del
residual; corolario: |ΔP| resuelve cola mejor que R) + sonda `empirical_residual_no_latent`
implementada (supremo práctico de la clase admisible; banco por bins declarados
(d, ctx, cuartil-marker); interpola en rango, CONGELA afuera) + TRES salidas firmadas
(A: v0 cierra + v1 falla beyond-exp → κ re-abre / B: v0 no cierra → mundo-funcional /
C: ambos cierran → clase AGOTADA → v2 mix-no-declarado ACTIVO) + localización c1/c2 de
la peor celda de v0 (¿kurtosis por decil fino? ¿sigma vs forma?). Python pineado
(`.python-version`=3.13.13). (Nota infra: venv recreado — base de uv desapareció; suite
verde post-rebuild, pin 0.0624 reproduce.) **RONDA DE CIERRE CORRIDA (v0.46)**: salida **(C) con matiz** — supremo R=0.984 en AMBOS
mundos (escalera monótona ✓), |ΔP| con **cero contraste** en todas las bandas (in-exp
0.041 vs 0.047; beyond 0.065 vs 0.064 — donde el banco congelado debía morder, no mordió)
→ clase admisible AGOTADA sin separar → **v1 no fuerza representación**. Mecanismo: el
dial `mix_logit` DECLARADO permite extrapolación suave de la media condicional aun con
residuos congelados (confirma v0.43-4). Localización: (c1) condicional de v0 dado marker
fino ES unimodal (kurt −0.12 ≈ gaussiano — diseño de v0 verificado); (c2) el error
gaussiano era σ/condicionamiento (+0.182), no forma (0.039). Residuo compartido
(~0.05–0.12 medias) = piso del miembro, idéntico en ambos → no afecta la conclusión.
κ EN ESPERA.
Arco fortalecer-rivales: CERRADO con piso demostrado (la escalera actual es la vara).

**SPEC-FIRST v2 REGISTRADO (v0.47)**: vara canonizada (escalera-de-6 = bar permanente;
tríptico v0/v1/v2 con pre-registro estructural gap(v0)≈gap(v1)≈0 < gap(v2)); definición
afilada de brecha de teoría (→ NORTH_STAR §4.6); **contrato de ventana en ARCHITECTURE
§10.1** (mix oculto por lote de prior no visible; ventana `n_cal` sin etiquetar en
`regime.context` con seed lado-mundo/CRN; firma de model() intacta; techo R=1 =
Bayes-adaptivo, world.py-con-oráculo = cota diagnóstica; ingenuo = pooled; miembro
PLUG-IN obligatorio — el gap verdadero es contra él, en n_cal chico + mixes extremos;
curva gap(n_cal) ES el resultado; pre-compromiso honesto si cierra: latente escalar
posiblemente inconmensurable → repensar arquetipo). `cases/mendel_subtypes_v2/brief.md`
escrito (misma cláusula, ventana narrada, anti-susurro ✓).

**ORDEN v0.48 (Lucas): MUNDO 3 PRIMERO, v2 segundo.** Razones: cartera (3 rediseños en
un slot de ~20); segundo ejercicio del test estructural sobre capa nueva (dummy-ismos
baratos ANTES del contrato v2); v2 toca la familia anclas/escala → sesión propia.
**Pre-registros del mundo 3** (collider_seleccion + error_de_medicion — PRIMERA vez que
las trampas viven en FUENTES, no en mecanismo): (1) "experiment nunca esquiva el canal"
muerde por primera vez → test que lo afirme; (2) visibilidad del collider por
SUB-BATERÍA observacional desde el día uno (ruido local); (3) el gemelo del collider
("la correlación seleccionada es real") debe salir de la factory generalizada SIN tocar
código — si pide código = dummy-ismo encontrado y registrado; (4) L1 100% derivado +
E0-probe frontier apenas pase L1, con headroom pre-registrado ANTES del probe; (5) ambas
monedas si el brief declara funcional (si no, registrar por qué). **Gates de v2 (después)**:
ancla Bayes-adaptiva a revisión nivel-artefacto (R_uncl>1 esperado = piso de inferencia
visible, no bug); smoke de ventana como primer milestone (misma ventana bajo CRN,
afirmado por test); el brief ya escrito ES el contrato.

**v0.49 (HECHO)**: lint de headers movido a **PRE-COMMIT** (hook versionado `hooks/pre-commit`
+ `core.hooksPath hooks`; paso post-clone en CLAUDE.md; el CI queda de segunda red) +
**plan corto del mundo 3 (`selection_bias_v0`) registrado**: mecanismo SCM limpio
(driver→outcome; signal sin arista directa) + trampas por PRIMERA vez en capa FUENTE —
pipeline de corrupción declarado en `SourceSpec` (filtro collider `f(signal,outcome)>umbral`
+ canal σ_med/sesgo que muerde TAMBIÉN en experiment, regla v0.9 con test) — maquinaria
nueva DECLARADA de antemano (es la anatomía §1 pendiente, no dummy-ismo); predicción
honesta: el test del gemelo destapa el **dummy-ismo #7 (mechanism-only twins)** → fix =
ablación por capa (fuente = re-muestrear pool con operador off); certificados con
sub-batería observacional día uno; funcional de cola en el brief (ambas monedas).
**CIERRES v0.50 (decididos, pre-registrados)**: (1) canal: **sesgo=0 en v0** (solo ruido
zero-mean en outcome, σ_med knob; hetero diferido; (b) spec-instrumento y (c) gold-standard
= perillas futuras — la (c) es perilla de VoI) + recuperabilidad cuantifica el de-noising;
(2) **gemelo del collider = esqueleto + arista `signal→outcome` sugerida-por-patrón (coef
del pool) + refit sobre knobs** (la ablación de capa sola da twin degenerado — rival débil);
(3) **batería: observacionales = POBLACIÓN COMPLETA** (≠ pool filtrado; skill = des-sesgar
la vista); sub-batería collider = población-completa + do(signal); **driver observable**
(clase de dificultad declarada; theory gap ~0 condicionado a eso). **CIERRE #4 (v0.51)**: σ_med
no identificable con una medición por unidad (Var_obs = σ_true² + σ_med²) → **fuente de
mediciones REPLICADAS** (dos lecturas/unidad, n chico, costo declarado; σ_med vía
Var(Y₁−Y₂)/2 — skill real: estimar el error del propio instrumento; techo alcanzable).
**Gate**: el certificado de recuperabilidad debe mostrar techo ≈ world.py bajo la elección.
**CERO decisiones entre el mundo 3 y el código. VARA DE VELOCIDAD: cierres + build ≤ ~2
sesiones o se reporta como señal — el reloj CORRE.** **SESIÓN 1 DEL RELOJ (HECHA, v0.52–v0.53)**: contrato de fuentes REAL — `SourceConfig` con
`SelectionFilter` + `MeasurementChannel` (réplicas ocultan la columna verdadera) +
**`pipeline_order`** (select_then_measure = survivorship, default v0 a conciencia;
measure_then_select = admisión por valor medido, filtra la PRIMERA lectura) —
`source_view()`/`experiment_view()` en harness (el experimento esquiva selección, JAMÁS
el canal — test pre-registrado ✓), 5 tests de wiring verdes (collider pc −0.35 vs 0.02
limpio; σ_med por Var(diff)/2 al 10%; determinismo byte-exacto). Registros v0.53:
ergonomía del entregable (describe() separa schemas; humo referencia entregable; NO
exponer tasa de aceptación) — se implementa con el meta del caso. **SESIÓN 2: world+meta
→ brief (línea proceso-no-medidor + funcional de cola) → derivación (#7 espera) → L1 →
headroom pre-registrado → E0-probe. Desborde a sesión 3 = dato contra la vara.**

**v0.29 (acceso de rivales, β)**: la variación de mix entra por EXPERIMENTOS (fuente barata
sigue single-mix); escalera (d) en dos modos — **(d-obs)** ancla la brecha mecanística,
**(d-exp)** (presupuesto experimental estandarizado y scripteado, acceso igualado al agente)
ancla la brecha de teoría. Principio: *brecha de teoría = contrafáctico con acceso igualado*.
Línea sin-latente = sin cabezal de mezcla (MDN/GMM condicional NO cuentan); escalera con
miembros de extrapolación SUAVE en mix (árboles plateau-ean = razón tonta). Pre-registro
P2-v1 completo (tabla 2×2: v0 chico / v1 grande ≥3×v0 con el funcional cargando la mayor
parte / mecanística grande en ambos / banda c_F ×2÷2 / guardia si v0 sale grande).

**v0.30 (auditoría código-vs-docs por iniciativa propia, HECHA)**: una verificación de
alineación destapó una **deriva doc-código v0.18→v0.29** — ARCHITECTURE §5 decía "(a) y (d)
cero experimentos" pero el código entrena (d) sobre grilla experimental desde v0.18 (el código
se adelantó a la doctrina; el papel quedó atrás). Tres contramedidas: **(1)** fix de §5 ((a)
verbatim intocable; (d) → referencia a los dos modos de §7); **(2)** checklist de supersesión
→ CLAUDE.md (grep obligatorio de cada ubicación de la regla vieja; "una regla, una casa");
**(3)** **certificados auto-descriptivos** — el acceso del rival (modo/presupuesto/seeds) es
campo Pydantic OBLIGATORIO del certificado (`RivalAccess`) con guarda (teoría=experimental,
mecanística=observacional) e impreso en el dossier → una deriva se ve en cada dossier, no solo
leyendo código. Footnotes de procedencia de los números históricos (arriba). Suite 86 verde.
**(d-exp) NO participa de la calibración de `c_F`** (la brecha de teoría queda independiente).

**v0.31 (cierres + pre-registro del paso 2)**: out-of-record decidido (banda 20–35% canonizada
en ARCHITECTURE §6); re-auditoría del dummy queda en manos de Lucas (con su OK expira el
bootstrap). **Protocolo de calibración de `c_F` PRE-REGISTRADO** (Decision Log v0.31): barrido
log-grid con D_MAX recomputado por candidato; gates = orden canónico ≥3×CV (a c_F=0 DEBE
fallar) + ablación de cada operador ≥3×CV (visibilidad, gate primario) + oráculo < verdad
(diagnóstico, sin rank requerido); mini-L2 (B=20) dentro del barrido (el ruido binomial del
funcional acota c_F por arriba → sándwich = hallazgo); **grilla de calibración FIJA** (la
batería derivada es función de c_F → circular; P3 queda como validación independiente);
Latent v0 se AUTORA como caso (brief+meta, mismo funcional que v1). Banda ×2/÷2 al cierre.

**Después**: detector de contaminación v1 = contraste-gemelo (sobre el dummy) — su
pre-registro se **RE-DECLARA contra el skin actual** antes de implementarlo (v0.33).
Stretch: E0-Latent.

## Qué falta (más allá del slice)

- E1: ~20 mundos a mano en 2 familias, ≥5 suites (ARCHITECTURE §12).
- Hardening del handle opaco (gaps en `REDTEAM.md`); mejor extractor de firmas.
- Collider+medición (3er mundo, ejercita la capa de muestreo).

## Deuda / pendientes

- Sandbox v0 es honesto pero no es jaula real: gaps declarados en `REDTEAM.md`
  (C-extensions, rlimit de memoria, fork). Se cierran con el harness interactivo.
- λ es **provisional** (calibrado al 5% del rango de normalización del dummy);
  se recalibra sobre la suite E1.
- Issue conocido E2 (diferido): clip(R,0,1) y sparsity de gradiente; rotación de
  seed-sets durante entrenamiento.
- Ensembles `[(peso, code)]`: `mdl_bytes` ya los soporta; el scoring de mezcla
  muestreada falta (no hay fixtures de ensemble en el Slice 1).
