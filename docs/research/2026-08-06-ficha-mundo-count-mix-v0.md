# Ficha exploratoria congelada — mundo `count_mix_v0` / gemelo `count_mix_twin_v0` (slice 1 de saltos, operador mezcla)

**Fecha:** 2026-08-06 · **Firmada ANTES de escribir `world.py`** (orden estricto: esta ficha
precede a toda construcción). **Estado:** diseño exploratorio congelado — fase DESCUBRIMIENTO
(ADR 0173): microhipótesis + compuertas + lectura fija; NO es pre-registro confirmatorio ni
estima prevalencia. Plan padre: [slice mezcla](2026-08-05-plan-slice-salto-mezcla-v0.md) ·
insumos de lectura: [NewtonBench + LLM-SRBench](2026-08-06-lectura-newtonbench-llm-srbench.md).

## 1. Pregunta y microhipótesis

**Pregunta del slice:** ¿el aplanamiento de estructura latente (A3≈0, replicado en SCM gaussiano)
generaliza a un formalismo de conteos — y el kit de saltos (gemelo + testigo + brecha + sondas +
robots + mapa de menú) funciona como instrumento?

**Microhipótesis (firmada):** DeepSeek-V3.2 y gpt-5.4 corregirán el NIVEL (tasa media) y NO
abrirán espontáneamente la estructura de mezcla (S_struct ≤ 0.25) aunque el testigo la seleccione
desde filas comprables y sobre presupuesto; en el gemelo conservarán el proceso único. Con la
pista, la abrirán (la capacidad está; el acto espontáneo no).

## 2. El mundo (receta generativa exacta)

**`count_mix_v0` (polo MIX).** Unidades = lotes con identidad persistente. Cada lote i tiene tipo
oculto Z_i ∈ {A, B}, P(Z=B) = w. Defectos por medición: `y ~ Poisson(λ_{Z_i} · s)` donde s =
perilla de velocidad. Parámetros por instancia (quemados a construcción con seed de mundo, regla
abajo): w ∈ [0.35, 0.65]; λ_A, λ_B con separación CALIBRADA por compuerta (no a mano): la
instancia se acepta si y solo si (i) el testigo selecciona mezcla con margen (compuerta G1) desde
muestras de tamaño comprable, y (ii) la bimodalidad no es caricatura: el valle de la marginal no
cae por debajo del 20% de la altura del pico menor (anti-póster). Instancias elegidas por REGLA
pre-declarada, jamás por resultados de agentes.

**`count_mix_twin_v0` (polo SINGLE).** Idéntico brief, menú, precios y superficie; un solo
proceso: `y ~ Poisson(λ_0 · s)` con λ_0 = w·λ_A + (1−w)·λ_B (media apareada al MIX). La
diferencia vive SOLO en la forma (Fano≈1, sin valle, sin exceso de ceros).

**Superficie de control:** perilla única `speed` ∈ [0.8, 1.2], multiplicativa sobre las tasas
(ambas componentes escalan igual: la estructura es invariante entre regímenes). Sin contexto, sin
horizonte (mundo estático).

**Piel:** línea de proceso neutra (lotes/defectos). Sin narrativa que sugiera subpoblaciones —
el brief lo escribe el proceso ciego a batería/rivales, como siempre.

## 3. Menú y precios (estructura declarada; precios finales calibrados por compuertas G2–G3)

| Acción | Qué devuelve | Costo relativo |
|---|---|---|
| `observe(archivo, n)` | filas históricas (unit_id, y) a speed=1.0, unidades frescas | barato |
| `experiment(speed=s, n)` | corridas nuevas al speed elegido, unidades frescas | medio |
| `experiment(repeats_per_unit=R, n_units)` | R mediciones del MISMO lote (unit_id repetido) | medio |
| `submit(model)` | entrega | — |

Presupuesto total del episodio: fijado a construcción tal que el robot-cuidadoso gana con ≤70%
del presupuesto y el discriminante (repeats) cuesta ≤30%. **Restricción anti-chivato (G3):** el
precio NO puede rankear la informatividad (el mapa de valor es secreto server-side).

**ENMIENDAS VISIBLES PRE-CORRIDA (2026-08-07 — mecánicas, ANTES de todo agente; causa: choques
con contratos existentes del harness descubiertos por los robots, no resultados):**
1. **Semántica de `n` = MEDICIONES (filas).** El contrato del server exige que `model(regime,n,seed)`
   devuelva exactamente n filas. Con `repeats_per_unit=R` las filas se agrupan de a R por lote
   (el último puede quedar corto). El precio queda POR FILA como estaba originalmente congelado;
   el discriminante (repeats) cuesta lo mismo que comprar filas frescas — sin prima ni descuento:
   no comprarlo sigue sin excusa económica.
2. **S_struct/S_clean restringidos al par certificable-estructural (valle, ICC).** Un programa de
   un componente iid no puede producir ICC>0 ni vaciar el valle conservando ambos picos; en cambio
   fano/p0/cola le dan crédito parcial a un NegBin bien ajustado (lo mostró el robot nunca-mezcla:
   S=0.269 con la definición ancha, 0.000 con la restringida). El vector completo de funcionales
   queda como descriptivo.
3. **G3 medido sobre VALOR-POR-COSTO con razón ≥3** (la heterogeneidad real del menú: 3.6×; el
   valor bruto por acción no baja de 2.2× porque la señal marginal viaja en toda fila). El
   anti-chivato quedó FUERTE: corr(precio, valor) = −0.86 — lo caro es peor.
4. **Plantillas de entrega sandbox-legales** (el lint del server prohíbe `getattr` — correcto — y
   las plantillas de robots lo usaban).

## 4. Batería y funcionales (cero-LLM; score combinado estilo ADR 0026)

Regímenes: grilla de `speed` incluida una región held-out no visitable barata. Funcionales de
estructura (computados muestreando entrega y verdad): media · **Fano (var/media)** · **P(y=0)** ·
**masa del valle** (banda fija entre modas de la verdad) · masa de cola alta ·
**ICC de repeats** (varianza entre-lotes / total, sobre el diseño repeats). Energía sobre
marginales + funcionales con peso (certificado de visibilidad: la estructura instalada DEBE
separarse en el reward, o el mundo se rechaza).

**Métrica primaria de estructura (definición congelada):**
`S_struct = clip[ (D(base_single, verdad) − D(entrega, verdad)) / D(base_single, verdad), 0, 1 ]`
computada SOLO sobre los funcionales de forma (Fano, P0, valle, cola, ICC), donde `base_single` =
mejor ajuste de UN componente con acceso legal completo (la brecha de necesidad ancla el 0).
S≈0 → entregó forma de proceso único; S≈1 → capturó la estructura. Nivel aparte:
`F_mean` = fracción de la media capturada (estándar de la casa).

## 5. Brazos y seeds (quemados: familia 99200–99399)

- **Instancias de mundo:** seeds 99200–99249 (se aceptan las primeras que pasen G1–G5, en orden;
  las rechazadas se listan con causa).
- **Brazo principal:** 2 modelos (DeepSeek-V3.2, gpt-5.4) × {MIX, SINGLE} × 3 seeds de episodio =
  12 episodios. Seeds: 99300–99311 en orden fijo.
- **Brazo pista (contingente, off-score):** SOLO si un modelo da "no abrió" en ≥2/3 en MIX →
  2 seeds frescas MIX + 2 SINGLE con la frase única: *"considerá que los datos pueden venir de
  más de una subpoblación"*. Seeds: 99350–99365. La pista clasifica; jamás rescata el claim.
- **Episodio técnico previo:** 1–2 corridas de interfaz (seed 99290–99291) sin lectura conductual.

## 6. Compuertas (todas ANTES de leer conducta; si falla una, se arregla el mundo o se descarta — no se interpreta)

- **G1 testigo:** BIC+CV sobre lattice {Poisson, NegBin, ZIP, mezcla-2-Poisson} con muestras de
  tamaño comprable BAJO el ruido del mundo: selecciona mezcla en MIX (ΔBIC ≥ 10 y todos los folds)
  y proceso único en SINGLE. [Lección NewtonBench: calibrar bajo ruido real, no en abstracto.]
- **G2 robots:** `siempre-mezcla` pierde en SINGLE · `nunca-mezcla` pierde en MIX ·
  `compra-lo-más-caro` pierde en al menos un polo · `todo-barato` y `azar` quedan bajo el
  cuidadoso · el **cuidadoso** (guion = solución canónica del plan) gana AMBOS con ≤70% del
  presupuesto.
- **G3 mapa de valor:** heterogéneo (razón valor máx/mín ≥ 5) · discriminante pagable (≤30%) ·
  correlación |precio↔valor| no perfecta (el reflejo caro pierde por G2).
- **G4 anti-disfraz:** huella (vector de escalera de degradadas + qué baselines fallan) distinta
  de `latent_mix_v2` y de la familia SCM.
- **G5 mecánica:** determinismo por seed · escalera de verdades degradadas monótona · smoke de
  interfaz limpio (entrega válida, sin fricción no-epistémica).

**DECISIÓN POST-SMOKE (Lucas, 2026-08-07 — registro visible):** el resultado principal cayó en
INDETERMINADO (media-apertura: frailty continua 6/6, clases discretas 0/6), no en "no abrió", por
lo que el gatillo original del brazo pista no disparó. Lucas autoriza ejecutar el brazo pista como
**EL control único post-señal** (ADR 0172) — misma frase congelada, seeds reservadas 99350–99357,
ambos polos y ambos modelos (2×2×2) — porque discrimina la localización que ahora importa:
repertorio-ausente-pero-disponible-a-demanda vs incapacidad. El control de dosis NO se corre en
este host (chocaría con el certificado anti-póster); la perilla de solapamiento pasa al diseño de
confirmación. El mundo, los instrumentos y las lecturas quedan sin tocar.

## 7. Lectura congelada (por modelo, sobre el brazo principal)

Con `F_mean ≥ 0.6` (corrigió el nivel; si no, el episodio no informa estructura y se reporta):

| Celda | Condición (≥2/3 seeds) | Lectura |
|---|---|---|
| **No abrió** | S_struct ≤ 0.25 en MIX | Aplanamiento generaliza de formalismo → candidata fortalecida |
| **Abrió** | S_struct ≥ 0.6 en MIX | El fenómeno era del formalismo anterior → acotar claim, subir un nivel |
| **Espurio** | en SINGLE entrega mezcla sustantiva (dos componentes con peso ≥0.15 y separación > ruido) | Sobreapertura — polo espejo, hallazgo nuevo |
| **Indeterminado** | S_struct ∈ (0.25, 0.6) o seeds partidas | Se reporta tal cual; UNA autopsia; sin tuning |

Brazo pista: lectura según la tabla del plan (§pisos): con-pista-abre + sin-pista-no = firma del
salto ausente · ni-con-pista = capacidad insuficiente (dato de dificultad) · la frase NO debe
inducir mezcla en SINGLE (si la induce: sugestibilidad, se documenta como hallazgo separado).

**Observado-jamás-premiado (línea B gratis):** secuencia de compras vs mapa de valor (¿compró
repeats? ¿cuándo?) · qué chequeos corrió en el kernel (¿miró dispersión/histograma?) · tool
paradox local (¿ajustó y cerró?). Solo descriptivo.

## 8. Techo de gasto y reglas de aborto

Techo del smoke completo (principal + técnico + pista contingente): **USD 50**. Un solo reintento
mecánico por episodio ante error de infraestructura; censura por interfaz se reporta censurada
(jamás se interpreta ni se re-rollea buscando resultado). Tras señal válida: como máximo UN
control decisivo en este host antes de subir de nivel (ADR 0172).

## 9. Qué NO autoriza este slice

Nada sobre "frontier agents" en general (2 modelos, fase descubrimiento) · ninguna tasa de
prevalencia · ningún ajuste de parámetros del mundo para rescatar la hipótesis (ADR 0173: si no
generaliza, vuelve al banco) · la lectura del brazo pista jamás sustituye al brazo principal ·
los datos de este slice no sirven como confirmación de la candidata (la confirmación usa
instancias y donantes frescos, congelados aparte).

**Firma:** Claude (worker), 2026-08-06, en MODO AUTONOMÍA dentro del alcance ordenado por Lucas
("dale, empecemos" → plan del slice). Ningún tripwire tocado: reward path con maquinaria
existente, cero-LLM intacto, gasto ≤ USD 50 declarado, sin contradicción de pre-registros.


---

## ADDENDUM v0.2 — escalera de ayudas sobre encargo corregido (2026-08-07; congelado ANTES de correr)

**Motivo (auditoría crítica del mismo día):** tres fallas de la v0 — (A1) el encargo no requería
el salto (stakes vacíos); (A2) el salto no paga en extrapolación; (A3) ancla de S débil. La v0.2
corrige SOLO A1-parcial y A3; A2 (estructura que pague fuera de soporte) queda para la versión de
confirmación con Codex.

**Cambio único al mundo (v0.2):** el párrafo final del brief se reemplaza por la sección "Cómo se
evalúa" — explica el MECANISMO real (el server genera datos con ambos programas y mide qué tan
parecidos son; objetivo: sustituto fiel, datos idealmente indistinguibles) SIN nombrar
distribuciones, formas, bandas ni estructura (decisión de Lucas: explicar la evaluación, no
soplar). Física, menú, precios, seeds de mundo: intactos. Byte-idéntico entre polos.

**Métrica primaria nueva (de la auditoría A3): `S_valley_fuerte`** — captura de discretitud
contra el rival FUERTE (frailty continua CON persistencia ajustada a la muestra del testigo);
solo el componente valle (lo único que un continuo-persistente no puede producir). Anclas:
rival fuerte = 0, verdad = 1. `S_struct` viejo queda como secundario/histórico. Métrica
conductual co-primaria: ¿alguna celda ajustó/comparó un modelo de mezcla finita? (de la traza).

**Brazos (frases CONGELADAS, una corrida, sin escalar después):**
- nivel0 (sin ayuda) — MIX 2 modelos × 2 seeds: 99360–99363. [Bonus: compara contra nivel0 de
  la v0 → efecto del encargo corregido solo.]
- nivel3 — *"Nota del encargo: considerá la posibilidad de que los lotes vengan en unos pocos
  tipos distintos."* — MIX 2×2: 99364–99367.
- nivel4 — *"Nota del encargo: considerá probar un modelo de mezcla finita: 2 o 3 grupos de
  lotes, cada grupo con su propia tasa."* — MIX 2×2: 99368–99371.
- Guardia bilateral: nivel3 y nivel4 sobre el GEMELO (1 seed por modelo por nivel: 99372–99375)
  — las frases NO deben inducir clases fantasma donde no las hay (espurio).

**Lectura congelada:** nivel4 DEBE abrir (S_valley_fuerte ≥ 0.6 o entrega de mezcla finita) — si
no, problema de mundo/capacidad y se frena todo. nivel3 = el escalón informativo (abre → faltaba
la palabra; no abre → falla de operacionalización). nivel0 = ¿el contrato de evaluación
clarificado alcanza solo? Gemelo: espurio esperado 0 (si nivel4 fuerza clases en el gemelo, se
reporta como sugestión bajo instrucción — lectura aparte, no falla del mundo). Techo del brazo:
USD 5. La autopsia de comparación-de-modelos se corre sobre TODAS las celdas.

**Autorización:** Lucas, 2026-08-07 ("dale implementemos y probemos"), como excepción explícita
al control-único ya gastado, vinculada al claim (validar diseño del mundo con un LLM + medir la
altura del salto).