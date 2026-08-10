# Ficha congelada — count_regime_v1 (el episodio del impasse; brazos RAW/VISIBLE)

> **Congelada 2026-08-09 ANTES de construir y de correr** (GO de Lucas: "todo sí"; diseño =
> veredicto de Codex 2026-08-09, sesión supervisora ADR 0172 — crudos en
> `scratch/codex-respuesta-2026-08-09.txt`). Nada de esta ficha se edita después de correr;
> cambios de Codex/Lucas superseden por addendum fechado. Es **la única prueba decisiva** de
> esta familia: no hay v1.1/v1.2 ni escalera de frases — después de esta corrida se vuelve
> arriba (MANTENER/MODIFICAR/PIVOTEAR).

## Pregunta (el claim reencuadrado — ADR 0174)

> ¿Cuándo un agente amplía su conjunto activo de hipótesis durante una indagación, **después
> de que su modelo vigente falla**, y qué tipos de estructura logra o no logra activar?

**Estimando de esta corrida**: ¿hacer VISIBLE el fallo del modelo propio (mismos datos,
mismo contenido) aumenta la aparición de una familia estructural nueva? — el test causal de
la teoría del impasse (Ohlsson), que hoy es teoría rival prometedora, NO doctrina confirmada
en LLMs.

**Qué NO afirma**: nada sobre "creatividad general" ni invención fuera del repertorio
(novedad relativa: quiebre de régimen es estructura de manual — lo que se mide es la
ACTIVACIÓN de esa estructura tras el fallo, no su invención). La celda de count_mix (0/9,
generación espontánea) queda intocada como fenómeno aparte.

## Constructo: generación vs aceptación, separadas SERVER-SIDE por timing (cero-LLM)

Para cada episodio se computa mecánicamente el **punto de discriminación**: el primer momento
en que la evidencia acumulada disponible al agente da al modelo de régimen ventaja clara y
sostenida sobre los rivales congelados (regla congelada: ΔBIC ≥ 6 contra el mejor rival, y
que no se revierta con la compra siguiente). Entonces:

- candidata de régimen **registrada ANTES** de ese punto = **expansión generativa** (el
  fenómeno que buscamos);
- registrada **DESPUÉS** = **aceptación** (lo que midió la v0; se reporta aparte, no compite).

La clasificación semántica de trazas puede validarse offline con lectura humana; **el reward
y esta clasificación primaria siguen cero-LLM** (timing + artefactos ejecutables).

## Verdad (polo principal `brk`) — la firma NO flagrante

Cada lote i entrega `y_i ~ Poisson(λ(speed))`, una medición por lote.

- **Ley A** (s < s*): `λ_A(s) = lam0 · s^alpha`.
- **Ley B** (s ≥ s*): `λ_B(s) = lam0 · s^alpha + delta1 · (s − s*)` — **la media es CONTINUA
  en s*** (sin salto de nivel: delta0 = 0); lo que cambia es la PENDIENTE. Nada de 5.5→11.5
  en una tabla: un spline/interpolador ajusta lo visto razonablemente y falla en condiciones
  nuevas relevantes (extrapolación más allá de lo comprado).

**Gemelo `smooth`**: ley de potencia única apareada en nivel sobre la grilla de examen (sin
quiebre) — castiga el régimen fantasma, ahora también bajo VISIBLE (¿mostrar residuos induce
quiebres imaginarios? — chequeo bilateral obligatorio).

Historia física (fidelidad a casos reales, regla dura 2026-07-13): transición de régimen al
superar velocidad crítica (caso canónico Reynolds; la línea vibra y aparece un modo nuevo de
defectos — mismo anclaje que la v0). El lado del descarte ancla en Onnes (la
superconductividad descartada como "cortocircuito del equipo"): por eso el fallo llega en el
**monitoreo rutinario**, sin anuncio — como en los casos reportados.

## El episodio (las 7 compuertas de diseño — Codex 2026-08-09)

La regla central: **el impasse debe FALSIFICAR el modelo vigente; no debe NOMBRAR su
reemplazo.** Achicar el escalón de la v0 no alcanza (sería "candidato un poco menos
dictado").

1. **Prefijo y M0 rutinario.** Tras el archivo y las primeras compras, el agente **registra
   un modelo provisional ejecutable (M0)**. Si ya propone régimen ahí, cuenta como salto
   espontáneo (celda aparte, comparable con count_mix).
2. **Firma no flagrante** (compuerta de instancia): sobre las compras típicas del prefijo, el
   mejor suave/spline deja residuos no flagrantes (máximo |z| < 2 en lo visto) y la media es
   continua en s*. Si el quiebre grita en la tabla, la instancia se descarta.
3. **Calificación rutinaria.** El mundo ejecuta el M0 sobre un **lote de control
   preprogramado, idéntico en calendario entre polos y brazos**, y devuelve predicción y
   resultado crudo. Nada de "detectamos un quiebre" — cero lenguaje de anomalía.
4. **Persistencia.** Tras reajustar la misma familia, un **segundo lote independiente**
   vuelve a fallar con la misma firma. Un residuo puede ser ruido; dos fallos frescos y
   estructurados crean el impasse.
5. **Verificación comprable.** Replicar el control o probar una referencia instrumental
   cuesta **< 10% del presupuesto**. Separa "creyó que era error" de "confirmó y aun así
   descartó" (el gate de Onnes).
6. **No-dictación certificada.** En el momento del primer fallo siguen vivas **≥ 3
   explicaciones estructuralmente distintas** — deriva instrumental, mezcla cambiante,
   heteroscedasticidad, régimen — separables por un experimento posterior. Regla congelada:
   en ese punto, ningún candidato le saca al segundo ΔBIC ≥ 6 con la evidencia disponible.
   Si changepoint ya gana aplastante, volvimos a medir aceptación → instancia descartada.
7. **Necesidad teleológica** (certificado, ANTES de gastar en agentes): el régimen gana en un
   contexto no visitado donde un spline o parche suave comprable **pierde**, contra el rival
   fuerte congelado. Si no se puede certificar, **se abandona el host** y se sube de nivel —
   no se corre.

## Los dos brazos (misma información; manipulan VISIBILIDAD, no evidencia)

- **`RAW`**: recibe las filas crudas del lote de control.
- **`VISIBLE`**: recibe las MISMAS filas **más un resumen mecánico** de residuos/calibración
  de su propio M0 (generado por código, formato fijo, sin interpretación).

Seeds apareadas entre brazos; el contraste RAW-vs-VISIBLE es el estimando primario.

## La cadena mínima registrada (verbos del harness)

`M0 → reconoce/rechaza M0 → registra candidata → compra test discriminante → M1 → entrega`

- **No se penalizan candidatas provisionales** (Nersessian: no cobrar los andamios).
- **"Sin hipótesis" es estado válido y registrable** — Klahr–Dunbar predice que puede ser la
  vía de escape del marco viejo; prohibirlo mataría el fenómeno.

## Métricas

- **Primaria conductual**: expansión generativa (candidata de familia nueva registrada ANTES
  del punto de discriminación) — por brazo.
- **Entrega**: S_quiebre_fuerte (0 = rival suave fuerte, 1 = verdad; misma construcción que
  v0 adaptada a quiebre de pendiente) + sub-métrica **error-en-huecos** aparte (caza la
  interpolación-sin-ley de la v0).
- **R direccional** (premia el descubrimiento por construcción, como v0) · **espurio**
  bilateral en gemelo (por brazo — VISIBLE no debe fabricar fantasmas).
- Cadena de eventos con timestamps (M0, fallos servidos, réplicas compradas, registro de
  candidatas, M1) — el "instrumento de cadena" que reemplaza la lectura retrospectiva de
  prosa.

## Microhipótesis pre-registradas (firmadas antes de mirar, MODO AUTONOMÍA)

- **H-V1 (test causal del impasse)**: VISIBLE > RAW en expansión generativa. Regla de
  decisión: señal si VISIBLE−RAW ≥ 2 episodios con expansión en n=6 por brazo (polo brk);
  diferencia 0 con capacidad OK = **Ohlsson muere para este sustrato** (condición de salida).
- **H-V2**: en RAW (sin resumen del fallo), la tasa de familia nueva ≈ 0 — la continuación
  del 0/9.
- **H-V3**: las expansiones que aparezcan serán mayoritariamente DESPUÉS del segundo fallo
  (persistencia), no del primero.
- **Control de capacidad** (obligatorio para interpretar cualquier nulo): con el concepto
  dado explícitamente, el modelo implementa el régimen y S sube — separa "no lo activa" de
  "no puede escribirlo".

## Condición de salida (falsabilidad del programa — Codex H)

Si v1 pasa el control de capacidad pero el impasse visible NO aumenta la expansión: la
explicación Ohlsson muere para este sustrato. Si después proceso-del-observador (el tercer
operador ordenado — NO invariante) tampoco reproduce la firma: **se abandona el claim general
de "falla de salto"** y se conserva count_mix como fenómeno específico de mezcla discreta.

## Presupuesto, seeds y modelos

- Familia de seeds del caso: 99400–99599. Ya quemadas (v0): 99400–99449 · 99460–99467 ·
  99490 · 99499 · 99500–99511. **Asignación v1**: scan de instancia 99450–99459 y 99468–99489
  (la primera que pasa TODAS las compuertas se congela en `instance.json`); testigo 99512;
  batería 99513–99519; episodio técnico 99520; tanda 99521–99544.
- Tanda mínima informativa: 2 modelos (gpt, DeepSeek) × 2 brazos × 3 seeds en `brk` (12) +
  2 brazos × 2 seeds en `smooth` (4, un modelo) = **16 episodios ≈ USD 5–8**. Primera pasada,
  la mínima informativa (regla de infraestructura).
- Certificados previos a agentes: los 4 de siempre (necesidad vs rival fuerte ·
  alcanzabilidad con witness · gemelo bilateral · anti-memorización) + compuertas 2/6/7 de
  esta ficha (no-flagrancia · no-dictación · necesidad teleológica).

## Qué se decide con el resultado

Una sola corrida decisiva → dossier a Codex/Lucas → MANTENER (escalar con instancias
frescas) / MODIFICAR / PIVOTEAR (si la señal está en otra juntura) / ABANDONAR el host. La
firma de la taxonomía (codebook, unidad = edición-dentro-de-cadena) corre EN PARALELO sin
bloquear esta prueba.

---

## ADDENDUM PROPUESTO 2026-08-09 `[SUPERSEDIDO por el ADDENDUM RATIFICADO de abajo]` — auditoría de las 7 compuertas por la lectura COMPLETA de Ohlsson 2011

La lectura del libro entero ([extracción](2026-08-09-lecturas-libros-programa-saltos.md))
valida la orientación de las 7 compuertas y detecta faltantes. Todo lo de abajo AGREGA
compuertas o registro; no relaja ninguna regla ya congelada.

**Tres compuertas nuevas propuestas:**

- **A. Certificado de impasse "unwarranted"** (pp. 91-92): verificar FUERA del episodio que
  el agente puede representar/ajustar la familia de régimen si se le presenta (el control de
  capacidad ya pre-registrado, promovido a compuerta PREVIA con test de reconocimiento). Sin
  esto, un nulo no distingue "no puede" (sin interés) de "no recupera" (nuestro fenómeno).
- **B. Cerrar la ruta periférica** (p. 327; Dunbar vía p. 157): el lote de persistencia
  (compuerta 4) se evalúa contra el modelo PARCHADO del agente (su M0 revisado), no contra el
  M0 original — si el parche absorbe el primer fallo y el segundo lote no lo castiga, el
  mundo PREMIA la diferenciación ("outlier") en vez de cazarla.
- **C. Grano del resumen VISIBLE congelado** (pp. 222-228): la dirección del salto viene de
  la estructura CUALITATIVA del residuo. Formato fijo: residuos por punto en orden de
  velocidad (sin ordenar por magnitud, sin marcar patrones, sin lenguaje interpretativo) —
  suficiente para DETECTAR el fallo, insuficiente para dictar la forma.

**Dos registros nuevos (observar, jamás premiar):** D. firma de auto-cómputo en RAW (¿el
agente computa residuos por su cuenta? — mediador causal predicho: RAW-que-computa ≈
VISIBLE); E. presupuesto de persistencia explícito (el abandono es salida legítima, p. 92;
la tasa depende del presupuesto — fijarlo y reportarlo).

**Avisos de interpretación (no cambian reglas):** (i) **dosis** — con 2 lotes, un nulo
VISIBLE≈RAW no mata la teoría (feedback insuficiente contra el sesgo push-forward es rival,
p. 117c); la condición de salida de H-V1 vale PARA ESTE SUSTRATO Y ESTA DOSIS y el dossier lo
dice con ese alcance; lo que testea la teoría es la curva de dosis (1/2/4 lotes — futuro).
(ii) **registro de creencias** — si el episodio se lee también para la línea de aceptación,
la predicción de Ohlsson se INVIERTE (anomalía visible sin rival exitoso → más re-etiquetado,
no más conversión; resubsumption pp. 348/358): no mezclar los dos claims en un titular.
(iii) **salidas a registrar: cinco, no dos** — perseverar / re-rank dentro de la familia /
familia nueva correcta (full-partial) / familia nueva incorrecta (falso insight, outcome
predicho p. 115) / abandono. (iv) **cita doctrinal**: el trigger se cita por Ohlsson 2011
pp. 107/109/117/222-228 (no solo Knoblich 1999); portar la honestidad del autor (tests
débiles, prevalencia 3-41%, progress criterion vivo).

---

# ADDENDUM RATIFICADO 2026-08-09 (fallo de Codex: **MODIFICAR y luego GO**)

> **Estatus de la ficha**: la versión de arriba DEJA DE ESTAR CONGELADA. Este addendum altera el
> constructo, la supersede formalmente, y obliga a **recertificar y volver a firmar ANTES de
> construir**. Crudos del fallo: `scratch/codex-respuesta-2026-08-09b-addendum.txt`.
> **Tripwires declarados** (van a Lucas en el reporte, no se ejecutan en silencio): compuerta A
> (cambia elegibilidad, reemplaza el certificado de capacidad), **compuerta B (TRIPWIRE MAYOR:
> cambia harness y feedback path; invalida la compuerta 4 original; obliga a recertificar
> necesidad teleológica, no-dictación y timing)**, y el tercer brazo (cambia seeds, tamaño,
> hipótesis y certificados bilaterales). **El reward TERMINAL no cambia** (R/S siguen evaluando
> el modelo final en held-out); lo que cambia son compuertas/registros intermedios calculados
> contra M0, que pasan a calcularse contra Mpatch. Frontera cero-LLM intacta.

## 1. El claim, reescrito (ya no se llama "test del disparador del insight")

> **Efecto de la TRANSPARENCIA y la ESTRUCTURA del feedback negativo dentro de episodios de
> indagación impulsados por anomalías.**

Alcance: una ruta de activación bajo anomalía — NO una teoría universal del insight (Klein
puede matar la necesidad universal del impasse; no puede matar este contraste local).

## 2. Compuertas A–E, ratificadas con modificación

**A. Compuerta de ELEGIBILIDAD UNWARRANTED** (renombrada: un control en otra sesión prueba
capacidad del modelo, no el estado cognitivo del episodio). Por modelo, exige: (i) implementación
correcta cuando se NOMBRA la familia; (ii) reconocimiento en un dominio ISOMORFO, contexto
fresco, entre ≥3 rivales; (iii) cero exposición al mundo, vocabulario o seeds principales. Si un
modelo falla, **sus nulos no entran al contraste teórico**.

**B. Cerrar la ruta periférica — OBLIGATORIA.** Secuencia nueva del episodio:

`M0 → lote 1 → registro de Mpatch → lote 2 ejecutado contra Mpatch → candidata / M1`

Condiciones duras: el **segundo lote queda FIJO y apareado entre brazos** (no se elige
adaptativamente contra cada parche — rompería la igualdad de evidencia); antes de correr agentes
se certifica contra una **biblioteca congelada de parches periféricos plausibles** (refit ·
outlier · heteroscedasticidad · spline/polinomio · recalibración); si un parche real SOBREVIVE al
lote 2, cuenta como **resolución dentro de familia** (no se censura ni se fabrica otro fallo); si
el agente no registra nada nuevo, `Mpatch = M0`. **Si no se puede implementar conservando un
segundo lote fijo → NO-GO al host.**

**C. Grano del resumen VISIBLE, congelado con precisión**: residuo **firmado y estandarizado**
(deviance/Pearson, no crudo); fórmula, redondeo y columnas congeladas; **orden natural por
velocidad**; mismo formato para M0 y Mpatch; sin ranking, color, etiqueta de patrón ni
interpretación. La no-dictación se recertifica **sobre el mensaje renderizado exacto**.

**D. Auto-cómputo en RAW — registro DESCRIPTIVO.** Cuenta solo el auto-cómputo *observable*
(tool-call o artefacto con comparación predicción-resultado/residuos); una mención en prosa no
alcanza. **No se lo llama "mediador causal"**: `RAW-que-computa ≈ VISIBLE` es selección
post-tratamiento y puede reflejar competencia general. No condiciona el análisis primario ni el
reward.

**E. Persistencia.** Se congelan server-side oportunidades, costo, turnos y presupuesto restante,
**iguales entre brazos**; se registra cuánto usa después del primer fallo. **No** se le pide al
agente que declare cuánto va a persistir (sería otra intervención). Se separa **abandono
epistémico explícito** de timeout / error técnico / agotamiento.

**Cinco salidas adoptadas** (perseverar · re-rank dentro de la familia · familia nueva correcta ·
familia nueva incorrecta = falso insight · abandono), con la **escalera ordinal de Darden**
(monster-bar → tweak → specialize → split → delete → add → abandonar) **anidada dentro** de
ellas como rúbrica de respuesta — no como reward escalar universal, y solo cero-LLM donde el diff
ejecutable identifica la edición.

**Regla de cierre de ciclo**: "dosis insuficiente" queda como rival interpretativo, pero **NO
autoriza una v1.1 de 1/2/4 lotes después de un nulo**. Este ciclo termina en este host.

## 3. Tercer brazo: VISIBLE-GLOBAL (NO prompt-warning)

| Brazo | Qué recibe |
|---|---|
| **RAW** | filas del control + predicciones de su modelo |
| **VISIBLE-GLOBAL** | lo mismo + estadístico GLOBAL de desajuste y su umbral |
| **VISIBLE-ESTRUCTURADO** | lo mismo + global + residuos ordenados (grano de la compuerta C) |

Separa causalmente **detectar el fallo** de **recibir la dirección cualitativa** — el contraste
RAW/VISIBLE original mezclaba las dos cosas. **NO-GO a prompt-warning** (no es falsificador
limpio: induce cómputo/búsqueda/priming, y aporta poco sobre el pre-registro de "compará" que ya
dio 0/3). **NO-GO a resubsumption como brazo** (es otro experimento, otro mecanismo, probable
otro reward path → candidato separado, después de decidir v1).

## 4. Claims corregidos (contabilidad — ADR 0152)

| Claim | Corrección ratificada |
|---|---|
| "Si el impasse visible no aumenta la expansión, **Ohlsson muere**" | Insostenible con n=6 y 2 lotes. Muere **esta operacionalización en este sustrato y esta dosis**; y se abandona el host. |
| Los brazos reciben "**la misma información**" | Falso cognitivamente. Mismas **observaciones**; distinta **representación y trabajo computacional**. |
| "Candidata registrada antes del punto de discriminación = **expansión generativa**" | El timing prueba **activación/propuesta antes de discriminación**, NO que el candidato estuviera fuera del espacio efectivo. |
| H-V2 como "**continuación del 0/9**" | Inválido: count_mix no estima RAW en count_regime. Queda **exploratoria**. |
| Generación y aceptación como **dos fenómenos** | No: son **momentos operacionalmente separables** dentro de contracción-expansión (Aliseda). |
| "**Darden confirma** la taxonomía de 11" | Demasiado fuerte: confirma **componente×verbo** y demuestra que la lista plana mezcla verbos, objetos y celdas. |
| "**Boden demuestra** que la activación es el mecanismo **mayoritario**" | "much" ≠ mayoría → "mecanismo **importante y frecuente**". |
| "**Bayes nunca agranda**" | Correcto solo para **condicionamiento dentro de un espacio fijo**; no como afirmación sobre búsqueda de modelos ni expansión del lenguaje. |
| Clasificación "**cero-LLM**" de la cadena | Vale **solo si `register` deja familia/estructura en un schema ejecutable**; si depende de interpretar prosa, es anotación humana. |

## 5. Codebook de taxonomía (en paralelo, como CANDIDATOS — sin numerar todavía)

`SPLIT/DELINEATE` y el `p′` de Aliseda son **el mismo verbo sobre componentes distintos** → los
ops 2 y 3 se releen como `población×split` y `tiempo×split`. `EXPLICITAR-SUPUESTO` es operación
de cadena/representación (puede no editar todavía el programa). `DELETE` entra como **verbo
primitivo** con las 4 condiciones de Darden. `REPLACE` queda **provisionalmente** como
composición `delete+add`, salvo casos que demuestren irreducibilidad. La tríada
**éxito/fallo/LAGUNA** entra como **eje de disparador y familia futura** (no se construye ahora):
una laguna permitiría estudiar **expansión sin contracción** — el mejor contrapunto posterior a v1.

## 6. Orden de ejecución ratificado

1. Re-firmar esta ficha con el addendum incorporado (hecho con este bloque).
2. Recertificar: necesidad teleológica · no-dictación (sobre el mensaje renderizado) · timing de
   discriminación · gemelo bilateral por brazo · biblioteca congelada de parches (compuerta B) ·
   elegibilidad unwarranted por modelo (compuerta A).
3. Construir. **No esperar** a Klein/Thagard/Magnani (deben cerrar antes del codebook definitivo,
   no antes de v1).
4. Una sola corrida decisiva → dossier → MANTENER / MODIFICAR / PIVOTEAR / ABANDONAR el host.

---

# ADDENDUM 2 — 2026-08-10: potencia y validación de la vara (ANTES de correr; nada se ha corrido)

> Dos bloqueantes que las lecturas de Klein y Thagard pusieron sobre la mesa, resueltos con
> cómputo, sin gastar API. Se declaran ANTES de la corrida porque uno de ellos **cambia la regla
> de decisión pre-registrada** — que es exactamente para lo que existe el pre-registro. Esto NO es
> la "v1.1 tras un nulo" que Codex prohibió: no hay nulo todavía porque no hay corrida.

## A. La regla de decisión pre-registrada NO tiene potencia (Klein)

Klein documenta que nuestro episodio cae en la intersección **contradicción × desesperación**, la
celda menos poblada de su corpus de 120 casos ("only a few cases") → **predice tasa base baja**.
Calculado sobre la regla congelada (*señal si #expansiones VISIBLE − #RAW ≥ 2*, n=6 por brazo):

| n por brazo | p(RAW) | p(VISIBLE) | **potencia** | falso positivo |
|---|---|---|---|---|
| **6** (lo pre-registrado) | 0.05 | 0.35 | **58,6%** | 2,5% |
| **6** | 0.10 | 0.40 | **58,7%** | 6,6% |
| **6** | 0.15 | 0.30 | **33,4%** | 10,4% |
| 10 | 0.05 | 0.35 | 81,9% | 5,5% |
| 15 | 0.05 | 0.35 | 93,4% | 9,3% |

**Consecuencia dura: con n=6 un nulo NO es informativo** — entre 41% y 67% de probabilidad de
perder un efecto real. La condición de salida tal como está firmada ("si el impasse visible no
aumenta la expansión, muere esta operacionalización") **no es sostenible con esta n**, ni siquiera
en la versión ya acotada por Codex.

> ⚠️ **Corrección anti-recencia (Lucas, 2026-08-10: "no caigamos en el error de considerar lo
> último leído como absoluto")**: la primera versión de este addendum decía "Klein PREDICE tasa
> base baja" y promovía el ordinal a outcome PRIMARIO. Las dos cosas eran recencia. (a) El corpus
> de Klein NO puede dar tasas base — es de éxitos publicados, y su propio lector lo advirtió
> ("esa pregunta su método no puede responderla"): Klein MOTIVA la sospecha; **la falta de
> potencia se sostiene por aritmética sola** (un binario con n=6 está sub-potenciado para casi
> cualquier tamaño de efecto plausible, lo diga Klein o nadie). (b) **El binario pre-registrado
> SIGUE siendo el outcome primario** — un pre-registro firmado no se cambia por una lectura; y
> además hay tensión REAL entre autores que no nos toca arbitrar: Klein cuenta 44% de insights
> graduales, pero la teoría que este experimento testea (Ohlsson) es precisamente de
> reestructuración; Nersessian pide medir la cadena. El ordinal entra como outcome SECUNDARIO
> pre-declarado — cubre la tensión sin arbitrarla, y es consistente con las "cinco salidas +
> escalera de Darden anidada" que Codex ya ratificó.

**Dos correcciones, ambas necesarias:**

1. **Outcome ordinal SECUNDARIO pre-declarado** (gratis): la **escalera de Darden** ya ratificada
   (monster-bar → tweak → specialize → split → delete → add) se registra por episodio junto al
   binario primario. Aporta potencia descriptiva y cubre el desacuerdo Klein-gradual vs
   Ohlsson-súbito sin resolverlo por decreto.
2. **Subir n, con decisión de costo para Lucas** (es un cambio de gasto → se eleva, no se ejecuta):
   - *Como está*: 3 brazos × 2 modelos × 3 seeds = 18 + gemelo ≈ **USD 8-12**, potencia 33-59%.
   - *Opción A*: 3 brazos × 2 modelos × 6 seeds = 36 + gemelo ≈ **USD 18-22**, potencia ~80%.
   - *Opción B* (recomendada): **un solo modelo** en el contraste principal × 3 brazos × 10 seeds
     = 30 + gemelo ≈ **USD 15**, potencia ~82%, y el segundo modelo queda para réplica si la señal
     aparece. Cambia el alcance del titular (un modelo) pero compra un resultado interpretable en
     vez de tres celdas ruidosas.

## B. Nuestra vara SOBREVIVE la Objeción 2 de Thagard (verificado, no supuesto)

Thagard levanta cinco tests contra el conteo "evidencia − hipótesis", que es la compresión de dos
partes en crudo. Los dos que nos podían morder, corridos contra la vara real:

| Test | Resultado |
|---|---|
| **"Being explained"** (una hipótesis explicada por otra debe GANAR, no perder): mismo modelo escrito como fórmula plana vs como pila de 4 hipótesis encadenadas | S = 0.9379 vs 0.9379 — **diferencia 0.000000** |
| **Unificación** (a igual conteo de parámetros, compartir una auxiliar debe ganarle a no compartir) | comparte S = 0.9379 vs separado S = 0.6748 — **+0.263 a favor del que comparte** |

**Por qué**: nuestra S es distancia de CURVA sobre la grilla de examen — **puntúa predicciones, no
estructura de hipótesis**. Es constitutivamente inmune a la penalización por profundidad (el
riesgo de "penalizar la forma del argumento de Darwin" **no aplica**), y premia el compartir por la
razón correcta: el modelo que reusa la auxiliar **predice mejor** en la banda de decisión.

El riesgo residual vive solo en el **testigo BIC** (que sí cuenta parámetros) usado para las
compuertas y el punto de discriminación — pero ahí los candidatos son familias planas, no pilas de
hipótesis, así que la penalización por profundidad no se instancia. Queda registrado como límite
conocido si alguna vez comparamos modelos en capas.

---

# ADDENDUM 3 — 2026-08-10: la cerca del límite certificado (fix de constructo, ANTES de la tanda)

**Qué destapó el técnico 2 (seed 99555, quemada)**: con la ventana de compra abierta hasta 1.4
desde el turno 1, el agente compró velocidades altas en el prefijo, vio el cambio de ley con sus
propios experimentos y registró el régimen en el turno 4 con ΔBIC=12.6 — **el impasse nunca llegó
a existir**. El mundo regalaba el descubrimiento por otra puerta.

**La corrección (server-side y procedural, brief intacto byte-idéntico)**: la línea está
**certificada hasta velocidad 1.2** — las corridas propias no pueden excederla; las velocidades
altas corren SOLO como pilotos programados. Tras el piloto 1, ingeniería **autoriza** corridas
altas con premium (2/fila), avisado en la notice del piloto (idéntica entre brazos y polos).

**Los números que cierran el constructo** (recomputados, certificación VERDE):
gap tras piloto 1 = **0.7** (nada dicta — ventana de generación abierta) · tras pilotos 1+2 =
**6.4** (la evidencia discrimina SOLA: alcanzabilidad servida por el calendario) · con zoom
premium = **9.1** · réplica n=20 = 80 < 100 (compuerta 5 OK).

**Protocolo agregado en el camino** (técnicos 1-2): aviso de calendario en turno 2 (pide modelo
registrado antes de los pilotos) · la entrega final se acepta tras el piloto 2 (intentos
tempranos rebotan con mensaje procedural y quedan en la cadena como observable) · captura exacta
de los lotes que el agente vio (la tabla de calibración jamás re-muestrea).

**Técnico 3 (seed 99556): el protocolo entero funciona y produjo una instancia POSITIVA** —
M0 suave registrado (T3) → piloto 1 lo falla a la vista (T6) → compra el zoom autorizado →
**postula las dos leyes en T8 con ΔBIC=4.0 (< 6: expansión GENERATIVA)** → re-registra → piloto 2
valida el remiendo (T10) → entrega S=0.696, umbral estimado 1.22 (verdad 1.237). Seeds quemadas
acumuladas: 99520 (bug de compras) · 99555 (sin cerca). La tanda usa 99521-99554 como estaba.
