# Resultado tanda D1 "El turno de calibración" — compran el test, no escriben lo que creen

> **Titular con alcance (ADR 0152)**: gpt-5.4 × par D1 (d1_proceso/d1_instrumento, instancia
> 99600) × n=15/polo × seeds 99661-99675 × wording v1: **el triage se ejecuta siempre (30/30
> compran evidencia discriminante ≥ 0.25 bits, 29/30 ANTES de que llegue la anomalía) y la
> evidencia comprada resuelve la horquilla (posterior server-side al lado correcto en 15/15 de
> proceso y 12/15 de instrumento) — pero la estructura no llega a la entrega: en el mundo donde
> la verdad exige AGREGAR estructura (mezcla), solo 2/15 la escriben (1/15 bien parametrizada,
> Y=7%); en el mundo donde la verdad coincide con el default (limpio), Y=60%.** Asimetría
> gemela apareada: 8 pares gana-solo-instrumento vs 0 gana-solo-proceso (McNemar descriptivo
> p=0.008). Un solo modelo, un wording, una instancia — nada de esto viaja más allá.

Ficha congelada: [2026-08-10-ficha-mundo-d1-calibracion.md](2026-08-10-ficha-mundo-d1-calibracion.md)
(+ addendum técnico 99660). Crudos: `scripts/out/d1_calibracion/`. Análisis pre-registrado:
`scripts/analyze_d1_calibracion.py` (commiteado ANTES de la tanda, commit `db66f38`).

## 1. Primario (pre-registrado, congelado)

| polo | Y | H0 p=0.25, binomial exacto | conducta (D_pre≥τ) | gate | S medio |
|---|---|---|---|---|---|
| **proceso** (verdad = mezcla real) | **1/15 = 7%** | p=0.987, no rechaza | **15/15** | 1/15 | 0.653 |
| **instrumento** (verdad = limpio) | **9/15 = 60%** | **p=0.0042, RECHAZA** | **15/15** | 9/15 | 0.472 |

Apareo gemelo (15 pares, misma seed): ambos ganan 1 · solo instrumento 8 · solo proceso 0 ·
ninguno 6. McNemar exacto (descriptivo) p=0.008.

Higiene: 0 submits tempranos aceptados; 30/30 terminan en submit propio (ningún tope de
turnos/tokens); gasto medio 532/633 de 800; D_pre mediana 0.41/0.64 bits.

## 2. La descomposición (dónde muere el ciclo — post-hoc rotulado)

La cadena tiene cuatro eslabones; midieron así (proceso / instrumento):

1. **¿Compra evidencia discriminante?** 30/30 (100% ambos polos). La hipótesis heredada de
   Dunbar y del rung 0 ("no pagan el test") **NO se reproduce acá**: todos midieron el
   estándar certificado sin que nadie les dijera "calibración" (el brief no usa la palabra).
   29/30 lo hicieron ANTES del monitoreo — chequeo proactivo del instrumento al armar el
   baseline, no triage disparado por la anomalía. (El único post-monitoreo: instrumento 99666.)
2. **¿La evidencia resuelve la horquilla?** El posterior mecánico server-side (por historia de
   compras) terminó del lado correcto en **15/15 proceso** — pero con matiz que marcó Codex y
   verifiqué: la mayoría FAVORECE débilmente (w_v 0.21-0.34, LR ~2-4×), solo 2 resuelven
   fuerte (99668/99675, w_v≈0). En instrumento, **9/15 mecánico** (w_v ≥ 0.5; mi primera
   versión decía 12/15 mezclando posterior con entrega — corregido). Nota: 4 de las 9
   victorias de instrumento son con w_v < 0.5 — ganaron porque el default coincidió con la
   verdad, no por resolución. Los torcidos de instrumento:
   99661 (w_v 0.001 — lotes flaggeados por cola de ruido q, el re-vial reprodujo el valor bajo
   y la evidencia REAL apuntó a material: mala suerte legítima del mundo, no bug), 99674
   (w_v 0.02), 99662 (absorbió el artefacto en el nivel: media contaminada 91.7 + varianza
   gigante → S=0).
3. **¿La estructura creída llega a la entrega?** **Acá muere.** En proceso: 13/15 entregan
   gaussiana unimodal (skew ≈ −0.04) con la subpoblación **horneada en la varianza** — el
   mismo movimiento que el técnico 99660. Solo 99664 (skew −0.55, S=0.56, ÚNICO Y=1) y 99671
   (skew −0.87 — estructura real pero mal parametrizada, S=0.39) escriben mezcla.
4. **¿Lo dicen aunque no lo escriban?** Regex cruda sobre los textos (método grueso, cuenta
   de menciones, no anotación fina): 6/15 de proceso mencionan mezcla/subpoblación/contaminación
   en algún turno; 99665 llega a anunciar *"a small low-purity contamination component to
   capture"* — y entrega unimodal igual. La anotación fina por reglas congeladas queda como
   pendiente offline (como en el rung 0).

**Lectura**: el cuello de botella NO fue generar el candidato (la horquilla venía desplegada
en el diseño), NI pagarlo (lo pagan todos), NI resolverlo (la evidencia decide bien) — fue
**propagar la estructura ya resuelta al modelo entregado**. Y la asimetría gemela lo firma:
cuando "no propagar" coincide con la verdad (instrumento → limpio), ganan; cuando la verdad
exige escribir la estructura nueva (proceso → mezcla), 7%. Es el mismo fenómeno que el 0/9 de
count_mix (nadie escribe la mezcla espontáneamente) reproducido en un mundo distinto, con
dinámica distinta, y con el candidato YA resuelto por evidencia propia — la versión más
incriminante hasta ahora: **no es que no se les ocurre; es que no lo escriben ni habiéndolo
comprado y resuelto.**

## 3. Explicaciones rivales que NO descartamos (declaradas)

- **La vara S + flag es dura con parametrizaciones intermedias**: una mezcla tímida
  (skew −0.22, 99665) cuenta como unimodal. El flag exige skew ≤ −0.4; la verdad da −0.97.
  Corrimiento del umbral cambia 1-2 celdas, no la asimetría 8:0.
- **Incentivo percibido**: el brief pide "sustituto fiel del proceso" — un agente puede creer
  que una gaussiana ancha ES un sustituto suficiente (la estructura como detalle). Contra esto:
  el examen castiga p10/sd (la mezcla muerde), y S medio 0.65 muestra que dejaron puntos reales
  sobre la mesa; pero el argumento "no sabían que la estructura pagaba" no está 100% cerrado
  por diseño (el brief no dice CÓMO se mide la distancia).
- **Un solo modelo/wording/instancia**: gpt-5.4, wording v1, instancia 99600. Nada generaliza
  todavía.

## 4. Notas de harness (integridad)

- Técnico 99660 (quemada): validó E2E; destapó el fix del flag (asimetría vs varianza
  inflada, test adversarial en suite) y el fix de contabilidad de tokens — ambos PRE-tanda,
  documentados en addendum 1 de la ficha.
- Byte-identidad de rutina verificada en dry-run scripted (archivo/experimento/monitoreo
  idénticos entre polos; diagnósticos difieren).
- 30/30 celdas sin errores de harness; la única S=0.0 (99662-B) es entrega real del agente,
  no crash. Costo total de la tanda ≈ 1.0M tokens (~USD 12-15), dentro de lo aprobado.
- Bug latente reportado (no tocado): el runner del rung 0 lee `total_tokens` de `Turn`
  (siempre 0); el host está cerrado, se corrige solo si se reabre.

## 5. Nivel arriba

- **Aprendizaje real**: la falla viva en este escalón no es el triage (se ejecuta solo) sino
  la **supresión de estructura en la entrega** — "lo creo, no lo escribo". Es un fenómeno
  nuevo respecto del catálogo activo: no es vicio 1 (no absolutizan la primera explicación:
  la abandonan bien), ni el impasse del rung 0 (acá no hace falta impasse). Candidato a
  entrada/actualización en `docs/vicios/` tras careo con la tabla de casos reales.
- **Límite del claim**: un modelo, un wording, una instancia, K=2 desplegada. La conducta
  100% pre-anomalía sugiere que el estándar en catálogo hace el triage DEMASIADO natural
  (¿affordance? el robot ciego ya lo anticipó) — el claim "triage espontáneo" quedó sin
  tensión: se confirmó trivialmente.
- **Explicación rival principal**: "no sabían que la estructura pagaba" (incentivo percibido,
  §3) — cerrable con un wording que declare la vara (¿o con stakes que la impliquen?), sin
  tocar reward.
- **¿Sigue siendo el mayor valor?** El programa pedía "¿alcanza el impasse cuando el candidato
  está LEJOS?" — D1 respondió otra cosa más básica: ni siquiera CERCA la escriben si hay
  escape unimodal. El polo compuesto (distancia 2) sobre este esqueleto hereda esta
  contaminación: antes de subir distancia hay que decidir qué hacer con la supresión de
  estructura (¿es EL hallazgo y pivoteamos a confirmarlo, o se parchea la vara y seguimos la
  escalera?). Veredicto de ciclo: Codex abajo.

## 6. Veredicto de Codex (cierre de ciclo, gpt-5.6-sol/max — crudo en `scratch/codex-respuesta-2026-08-10-cierre-d1.txt`)

**PIVOTEAR.** Cerrar D1 como host de *triage provocado por anomalía* (29/30 compraron ANTES:
midió control metrológico proactivo inducido por la interfaz, no triage disparado). No
construir el polo compuesto ni subir distancia todavía.

**El claim baja un escalón** (correcciones que verifiqué contra mis crudos — tenía razón):
sobreviven adquisición 30/30, estructura explícita 2/15, asimetría ejecutable 8:0; NO
sobrevive "lo cree pero no lo escribe" (w_v es el posterior normativo del servidor, no la
creencia del agente; 0.21-0.34 favorece débil; solo 99665 muestra disociación verbal
inequívoca; mi 12/15 de instrumento era 9/15). **Titular defendible**: *"tras comprar
evidencia que favorece una causa material, gpt-5.4 comprime sistemáticamente la subpoblación
en una entrega unimodal"* — compatible con propagación fallida, inferencia estructural
incompleta, parsimonia o incentivo ambiguo.

**Orden de pasos de Codex**: (1) SIN gastar: auditoría cero-LLM condicionada a la evidencia
legal de cada episodio (§7 — corrida, PASA); (2) si pasa: ÚNICO control adicional en D1 —
mismas 15 seeds, ambos polos, wording que declare que se puntúa la distribución completa y
que igualar media/varianza no basta, SIN nombrar mezcla, sin tocar reward (si rescata proceso
sin inducir estructura espuria en instrumento → era especificación/saliencia; si no rescata →
promover y confirmar fuera de D1 con otro modelo e instancia fresca); (3) otro modelo/más
instancias NO cierran el rival de incentivo ahora.

**Candidata de pivote: SÍ** — elevar a Lucas, pero NO como vicio nuevo: convergencia entre
**vicio 4** (aplanamiento de estructura latente) y **vicio 8.6** (análisis que no llega al
artefacto ejecutable); reaparece en count_mix, North heterogéneo y D1; gemelo bilateral y
vara cero-LLM. Estado: **candidata de confirmación**, no "propagación demostrada".

## 7. Auditoría de evidencia (post-hoc, cero-LLM, regla fijada por Codex ANTES de correrla)

`scripts/audit_d1_evidencia.py`: por celda, mezcla 2-comp (EM) vs unimodal sobre los lotes
que el agente REALMENTE vio (experimentos + monitoreo, detrend en T) → ΔBIC + CV 5-fold;
"gana claro" = ΔBIC ≥ 10 y CV > 0.

- **proceso: 14/15 mezcla gana claro** (ΔBIC 12.5-25.4; único no-claro: 99661, ΔBIC 8.7) y
  además estiman bien la estructura que no escriben (π̂ 0.12-0.20 vs verdad 0.20; corrimiento
  3.7-4.9 vs verdad ≈3.9). **≥12/15 → CERTIFICADO: la evidencia disponible exigía estructura;
  el claim conductual queda en pie** (en la forma bajada del §6).
- **instrumento: 14/15 la misma flagrancia en lecturas** — el control gemelo confirma que las
  lecturas NO deciden la entrega (rutina byte-idéntica); la horquilla decide. Con horquilla
  además favoreciendo material: 5/15.

