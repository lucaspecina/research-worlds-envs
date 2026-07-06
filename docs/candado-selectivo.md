# Candado selectivo — spec de trabajo (COMPUERTA CERRADA: NO se implementa)

> **Estado: CERRADO POR LA COMPUERTA (ADR 0092).** La compuerta de necesidad (Lucas,
> pre-build, antes de tocar el reward path) probó que **el candado NO hace falta**: en el
> mundo ancho, el ajuste-tramposo de referencia más fuerte (funcional PERFECTO |ΔP|≈0,
> cero mecanismo conjunto) saca **R = −0.53** — la energía, aun diluida, caza la ceguera de
> mecanismo GLOBAL. La dilución solo esconde el error QUIRÚRGICO de una relación (el
> confound), que la opción (d) ya certifica en la variante angosta. **Resultado: (d) puro +
> funcional. El candado NO se implementa.** Este doc queda como registro del diseño y de la
> compuerta que lo frenó (con las correcciones de D1 de Lucas archivadas abajo, §5). Nada
> de esto tocó el reward path.
>
> **Por qué el freeze de c_F=0.25 es doblemente correcto (hallazgo de la compuerta)**: a
> c_F alto (el ×7 que el techo de anchura rechazó) el funcional dominaría y el
> oracle-gamer ganaría (|ΔP|=0 → R→1). c_F=0.25 bajo mantiene la energía al mando → el
> funcional NO es gameable. El techo de anchura y la no-gameabilidad apuntan al mismo c_F.

---

## COMPUERTA (ADR 0092) — el registro

Reference gamers en el mundo ancho, c_F=0.25 frozen (scratchpad/gate_wide.py):

| player | R_combinado | R_energía | \|ΔP\| do2/do5/do8 |
|---|---|---|---|
| naive_record | +0.000 | +0.000 | 0.220/0.108/0.000 |
| **oracle_functional_gamer** (perfecto funcional, cero joint) | **−0.529** | −0.598 | 0.018/0.005/0.000 |
| twin_deriva (confound-blind, joint OK) | +0.874 | +0.895 | 0.285/0.003/0.007 |
| canonical_understander | +1.000 | +1.000 | 0.022/0.002/0.001 |

Lectura: el gamer con funcional PERFECTO y cero mecanismo saca −0.53 → **no se puede sacar
nota alta sin entender el mecanismo** → compuerta cerrada. (twin_deriva alto = el confound
quirúrgico diluido = la trampa-de-canal, resuelta por (d) en el angosto, no por el candado.)

---

## Diseño archivado (lo que el candado HABRÍA sido)

> Todo lo de abajo es el diseño que la compuerta volvió innecesario. Se conserva por si un
> mundo futuro reabre la pregunta con un mecanismo que la compuerta NO cierre. Ante
> conflicto con el repo, manda el repo.

## 1. La idea en una frase

La energy distance deja de computarse sobre la nube COMPLETA de columnas y se computa
sobre el **subconjunto declarado "río arriba del outcome"** — el mecanismo causal que
sostiene la pregunta del cliente. El término funcional (la pregunta) queda igual. Las
columnas mudas dejan de entrar al promedio, así que la anchura deja de diluir el filo.

## 2. Por qué (el diagnóstico, ADR 0090 + 0091)

La energy distance sobre TODAS las columnas es **model-recovery indiscriminado**: paga
por reproducir las columnas irrelevantes igual que las que importan. Eso coincide con
"investigar de verdad" solo cuando el mundo es chico y todo importa; **diverge apenas hay
ruido de fondo** — el piloto ancho lo midió: recuperar el filo de una trampa que vive en
1 columna exige ×7 de peso funcional, y ahí choca con el techo de ruido. El funcional NO
se diluye (apunta a lo que importa; |ΔP| idéntico a 3 y 19 columnas). El candado lleva esa
propiedad — *apuntar a lo relevante* — a la base energética misma, sin matarla como
guardián universal (solo se acota el dominio sobre el que guarda).

## 3. Lo que NO cambia (el contrato)

- **El entregable del agente NO cambia**: `model(regime, n, seed)` sigue devolviendo
  TODAS las columnas. El agente NUNCA sabe cuál subconjunto se scorea — saber qué columnas
  importan ES la investigación; declararlo al agente sería un leak del mecanismo (la misma
  lógica del handle opaco y del brief ciego). El candado es 100% server-side.
- **El funcional** (pregunta cliente) intacto — sigue apuntando al outcome/su cola.
- **Cero-LLM en el reward, D_MAX, anclas, CRN, energy distance como métrica** — todo
  igual. Lo único que cambia es el CONJUNTO DE COLUMNAS sobre el que la energía se evalúa.
- **La base energética sigue siendo el guardián universal anti-Goodhart** — pero sobre el
  conjunto relevante, no sobre el ruido de fondo. No es "pesar por stakes" (rechazado en
  ADR 0090-b, que mata la cobertura): es acotar el DOMINIO a lo declarado-mecanismo, con
  cobertura plena (peso uniforme) dentro de él.

## 4. Lo que SÍ cambia (server-side, una pieza)

`WorldSide` computa `distance_to` sobre las columnas de **S** (scored set), declarado en
`meta` y **verificado pre-build** (D2). Hoy `TruthSide(real, columns)` ya toma un
`columns` — la cirugía es mínima en superficie (pasar S en vez de todas), pero su
SEMÁNTICA es tripwire-1: define qué "reproducir el mundo" significa. Por eso spec-first.

---

## 5. LAS TRES DECISIONES ABIERTAS

### [D1] — DÓNDE CAE LA LÍNEA

**El sándwich a evitar**: *outcome-pelado* reabre la trampa LOCAL (un ajuste tramposo
clava pocas columnas sin entender el mecanismo — exactamente lo que la base energética
existe para castigar); *dataset-completo* es la dilución que acabamos de medir. La línea
cae en el medio: **cubrir el mecanismo causal aguas arriba de la pregunta**. Falta el
criterio EXACTO de "aguas arriba", y encontré que no es obvio.

**La tensión que descubrí (importa para D2)**: hay TRES tipos de columna, no dos.
- **Ancestros causales del outcome** (el driver; y los latentes u/shift que lo producen).
  Los latentes no son columnas; sus **proxies observables** (signal↔u, hall_rh↔shift) NO
  son ancestros (son *descendientes* del latente), pero son la HUELLA observable del
  mecanismo — un modelo que reproduce el joint (signal, outcome) demostró que entendió el
  rol de u. **Deben entrar.**
- **Distractoras puras**: hijas de un latente que NO alimenta el outcome (el cluster de
  mantenimiento w → torque/wear/feed_counter), o co-ajustes del driver sin efecto propio
  (pressure/flow/rpm). Condicional al driver, ⊥ outcome. **Deben quedar afuera.**
- **El caso incómodo**: una distractora que comparte un latente CON el outcome aunque sea
  parcialmente (en el mundo ancho, `grain = 0.6u + 0.4w` comparte u). Condicional al
  driver, `grain` ES informativa del outcome (vía u). Un criterio ingenuo "informativa →
  entra" **re-infla** a casi todo lo que toca un latente compartido. Un criterio ingenuo
  "do(col) no mueve outcome → afuera" (el do-test) **excluye los proxies buenos** (do(signal)
  no mueve nada, pero signal es la huella de u). **Ningún test PURO da la línea.**

**Candidatos (marcar el elegido):**
- **(A) Ancestros causales solo** {outcome, decision}: demasiado fino → reabre la trampa
  local. Descartado salvo como piso.
- **(B) Manto de Markov observable del outcome**: outcome + decision + los proxies
  MÍNIMOS que identifican cada latente que alimenta el outcome (un proxy canónico por
  latente relevante, no todos). Excluye redundancias (surface_gloss si signal ya cubre u).
  Elegante; el problema es "cuál proxy canónico" y cómo declarar minimalidad sin arbitrio.
- **(C) DECLARADO-Y-VERIFICADO (recomendado)**: el mundo declara S = {outcome} ∪
  {decision vars} ∪ {columnas-mecanismo} (los proxies de los latentes que alimentan la
  pregunta, elegidos por el autor como la huella observable del mecanismo). NO se confía en
  la etiqueta: se verifica por ejecución (D2). Criterio operacional de "mecanismo" que
  propongo: **una columna entra a S sii NO es condicionalmente independiente del outcome
  dado {decision}** — PERO con la sub-batería de la pregunta (los regímenes do que el
  cliente paga), y con el desempate del do-test para separar proxy-de-causa (entra) de
  hijo-de-causa-sin-efecto (afuera). Esto encaja con la cultura declarar+verificar de todo
  el proyecto.

**CRITERIO FIRMADO (correcciones de Lucas, ADR 0092)** — reemplaza mi "latentes disjuntos"
(que mataba la carnada más realista):
- **El "tercer tipo" NO se prohíbe por regla de diseño.** Si una columna lleva información
  GENUINA y NO-REDUNDANTE sobre el outcome, va ADENTRO del candado (es mecanismo, aunque
  incómodo). Su rol de carnada se cumple igual: **tienta porque PARECE más conectada de lo
  que su peso justifica**. El diseñador NO queda obligado a latentes disjuntos.
- **La línea limpia**: el candado cubre **todo lo que lleva información no-redundante sobre
  el outcome** (proxies incluidos), y deja afuera **solo lo condicionalmente independiente
  del outcome dado {ese conjunto}**. El do-test se RETIRA como criterio primario (excluye
  proxies buenos — hallazgo correcto) y queda como **diagnóstico secundario, no definición**.
- **Compuerta de viabilidad** (habría aplicado): si "información no-redundante" no se
  computa limpio y estable → no se implementa, (d) puro. (Moot: la compuerta de necesidad
  cerró antes.)

### [D2] — VERIFICABILIDAD DE LA DECLARACIÓN (cero-confianza)

El mundo declara S y su complemento M (mudas). No se confía en la etiqueta: se verifica
ejecutando, **pre-build, automático** (mismo espíritu que el test de contaminación y el de
viabilidad de #12). Una columna en M es genuinamente muda sii pasa AMBOS:
- **do-test**: `do(col=valor)` sobre un barrido no mueve la pregunta del cliente (el
  funcional) más allá del piso → sin efecto causal sobre la pregunta.
- **info-test**: `col ⊥ outcome | S` en la sub-batería de la pregunta (condicional al
  scored set ya declarado, no solo al decision) → sin información residual sobre el outcome
  una vez que tenés S.

**Por qué AMBOS (la tensión de D1 resuelta acá)**: el do-test solo dejaría pasar como
"muda" a un proxy informativo (do(signal) no mueve outcome → lo llamaría mudo, MAL). El
info-test lo caza (signal ⊥̸ outcome | S es falso si S no incluye ya la info de u). Y el
info-test solo dejaría pasar como "no-muda" a algo con efecto causal nulo pero correlación
espuria; el do-test confirma que no hay palanca. **Una muda genuina no tiene NI palanca NI
información residual.** Si una declarada-muda falla cualquiera de los dos → se caza → entra
a S (o el mundo se marca para rediseño). Guardia con su par should-pass/should-fail, como
toda guardia (ADR 0057).

**Abierto**: el umbral del info-test (una MI condicional o una R-parcial con piso de
resolución, reusando la doctrina significancia+magnitud de v0.38); y si la sub-batería del
test es la de la pregunta o una propia. **[D2: firmar los dos tests + sus umbrales.]**

### [D3] — ENCASTRE CON LA CARNADA (que no se pisen)

La carnada (el señuelo tentador del mundo rabbit-hole) es, técnicamente, **una columna que
PASA el chequeo de muda** (do no mueve el outcome, ⊥ outcome | S) **PERO está correlacionada
con algo real** — parece conectada, tienta a gastar presupuesto investigándola. El candado
selectivo la deja AFUERA de S (correcto: es genuinamente muda para el scoring). La carnada
hace su trabajo aparte (atención/presupuesto, medido por firma de trace + el costo de
haberla investigado, jamás premiado).

**La condición de compatibilidad que encontré (la clave de D3)**: para que la carnada sea
a la vez *tentadora* (correlacionada con el outcome) y *muda* (⊥ outcome | S), su
correlación con el outcome debe estar **SCREENED-OFF por S** — es decir, correlaciona con
la pregunta SOLO a través de columnas que ya están en S (redundante), NO por un camino
fresco. Ejemplo limpio: una carnada = copia ruidosa de `signal` (que ya está en S). Dado
signal, la carnada no agrega nada → muda → excluida del scoring; pero marginalmente
correlaciona con outcome (a través de signal) → tienta. **Las dos piezas NO se pisan sii
la carnada está screened-off por S.** Si la carnada correlacionara con el outcome por un
camino que S no captura, el info-test la metería en S (dejaría de ser carnada y pasaría a
ser mecanismo) — que es el comportamiento correcto, no una colisión.

**Verificación de encastre (pre-build)**: (i) la carnada ∈ M por D2; (ii) la carnada
marginalmente correlacionada con el outcome ≥ un piso (tentadora de verdad); (iii) la
carnada screened-off: `carnada ⊥ outcome | S`. Las tres juntas garantizan que candado y
carnada conviven. **[D3: firmar la condición screened-off como invariante de diseño de
mundos con carnada.]**

---

## 6. Pre-registros firmables (antes de cualquier build de mundo que use el candado)

- El candado se VERIFICA como no-op sobre los mundos ya certificados donde S = todas las
  columnas (dummy, latentes, los sampling angostos de 3 columnas): pin byte-idéntico de sus
  certificados. Si mueve un número en un mundo donde todo es mecanismo, hay un bug.
- El candado RECUPERA el filo en el mundo ancho: re-scoreado sobre S (que excluye los
  clusters driver-linked y w-linked, y — según D1 — quizás incluye u-cluster y shift-cluster),
  el twin de offsets vuelve a separar ≥ piso a c_F=0.25 (SIN el ×7). Firmar la predicción
  ANTES de mirar.
- La guardia de D2 llega con su par should-pass (una muda real pasa) / should-fail (una
  distractora-con-efecto o un proxy informativo se cazan).

## 7. Secuencia (spec-first)

1. **Estresar este spec juntos** — firmar D1/D2/D3. (Ahora.)
2. Recién con las tres firmadas: implementar el candado server-side (S en meta, verificación
   pre-build con su guardia, `WorldSide` sobre S) + el par de tests + el pin no-op sobre los
   mundos existentes.
3. Recién ahí: re-abrir el eje de anchura del diseñador (la anchura vuelve a ser un dial de
   dificultad legítimo, porque el candado le devolvió el filo) y correr el E0-ancho que
   quedó en suspenso, ahora con S.

**Compuerta**: si al estresarlo aparece que "aguas arriba" no tiene criterio limpio y
verificable (D1 sin cierre), el candado NO se implementa — se queda en (d) puro (anchura =
atención) y se reporta que la dificultad de trampa-de-canal vive solo en mundos angostos.
Esa salida también es información, no fracaso.
