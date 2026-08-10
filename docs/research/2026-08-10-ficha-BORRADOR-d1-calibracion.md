# BORRADOR v2 (ronda 2) — Ficha D1 "El turno de calibración"

> **Estado: BORRADOR EN DISEÑO — no congelado, no construible.** Claude diseña y manda; Codex
> critica. Ronda 1: crítica completa en `scratch/codex-respuesta-2026-08-10-d1critica.txt`
> ("no presentable: mide triage instrumental, no salto; los botones nombrados regalan la
> hipótesis; siempre-calibrar gana bilateral"). Esta v2 la incorpora casi entera y contraataca
> en dos puntos (marcados ⚔). Se presenta a Lucas ANTES de codear.

## 0. El claim, reescrito (acepto el ataque al constructo)

D1 **NO mide salto distante ni creatividad abductiva**. Mide la juntura B3 del corpus —
la más citada por las cuatro tradiciones y ausente de todos nuestros mundos:

> **Triage de anomalía ambigua + búsqueda diagnóstica multicanal**: ante una anomalía cuya
> firma no dicta su causa, ¿el agente COMPRA evidencia con poder de discriminación real entre
> los rivales vivos (y propaga el resultado a su entrega), o resuelve la atribución por
> reflejo — en cualquiera de las dos direcciones?

La distancia de edición NO se manipula acá (radio chico a propósito): el peldaño de distancia
es el POLO COMPUESTO sobre este mismo esqueleto, después. **Explicación rival declarada para
Lucas desde ya** (exigencia de Codex): *"lo que mide puede reducirse a affordance/checklist
profesional"* — las defensas contra eso son §3 (acciones genéricas sin nombre diagnóstico) y
el ROBOT-CHECKLIST de §7, que debe PERDER para que el mundo certifique.

## 1. Fidelidad (igual que v1 del borrador)

Onnes 1911 (la sospecha del "cortocircuito" = **contacto intermitente** — literal en nuestro
mecanismo del polo B) · Dunbar (el triage real es replicar; el gate de la creencia-en-error) ·
Darden paso 1 · nuestros especímenes ("the sample was noisy"). Dominio trasplantado: planta
química, pureza por lote (nada de superconductividad en la piel).

## 2. El sistema subyacente — DAG y ecuaciones (lo que faltaba: especificación real)

**Estado persistente**: lotes con identidad. El lote `j` existe, tiene una calidad latente, y
puede volver a medirse, re-prepararse o mandarse al laboratorio — SIEMPRE el mismo material.

```
temperatura T (perilla) ──────────────┐
                                      ▼
calidad latente del lote  q_j ──► pureza real  p_ij = μ0 + β·(T−T0) + q_j + ε_p
      (persistente)                   │                     ε_p ~ N(0, σ_p)  (medición i, lote j)
                                      ▼
                     vial del lote ──► SENSOR ──► lectura_ij = p_ij + δ_j·f + ε_m
                                                  ε_m ~ N(0, σ_m)
```

- **Mecanismo 1 (temperatura)**: μ depende de T linealmente (β<0: más caliente, menos pureza).
- **Mecanismo 2 (lote persistente)**: q_j ~ N(0, σ_q) compartido por todas las mediciones del
  lote (ICC alto — como count_mix; el modelo entregado debe reproducirlo).
- **Mecanismo 3 (la anomalía, por polo, A NIVEL LOTE en ambos — clave del apareo)**:
  - **Polo A (proceso)**: desde el punto t* del calendario, una fracción π=0.2 de los lotes
    NUEVOS nace degradada: q_j ~ N(−d, σ_q2). El sensor está sano: δ_j = 0 siempre.
  - **Polo B (instrumento)**: el proceso sigue idéntico al histórico; el **autosampler del
    sensor encaja mal ciertos VIALES** (falla mecánica intermitente a nivel vial/lote): para
    una fracción π=0.2 de los lotes nuevos, TODAS las lecturas de ese vial salen corridas
    (δ_j = 1, f = −d con ruido extra). La pureza real no cambió.

**Apareo EXACTO por construcción (resuelve la exigencia de igualdad de ley conjunta + CRN)**:
la distorsión de B es a nivel LOTE (vial), igual que la mezcla de A — por lo tanto la ley
conjunta de TODAS las lecturas rutinarias (incluidas repeticiones del mismo lote) es idéntica
entre polos, y con acoplamiento de números aleatorios comunes el stream es **byte-idéntico**
(verificado numéricamente en ronda 1). Los polos difieren SOLO en: (i) qué pasa cuando el
sensor mide un material de valor conocido, (ii) qué dice el laboratorio del MISMO material,
(iii) qué pasa al re-preparar el vial de un lote corrido, y (iv) la verdad del proceso que
puntúa la entrega.

## 3. Acciones — GENÉRICAS, sin botones que nombren la hipótesis (acepto el defecto 1)

No existe ningún verbo "chequeo de calibración". Hay UNA acción de medir y UNA de laboratorio,
sobre materiales que el agente elige:

| Acción (genérica) | Config | Costo | Latencia | Qué la vuelve diagnóstica (o no) |
|---|---|---|---|---|
| `experiment(T, n_lotes, reps)` | temperatura, lotes nuevos, repeticiones por lote | fijo 40 + 1/medición | 0 | reps altas separan lote-vs-medición; NO separa aparato-vs-proceso |
| `measure(material, reps)` | **cualquier material del catálogo de insumos**: lote ya existente (re-medir) · lote re-preparado en vial nuevo · **estándar de pureza conocida** (un insumo más del catálogo, con su valor de etiqueta) | 15 + 1/rep | 0 | medir un material de valor CONOCIDO por el sensor separa aparato-vs-proceso; re-vial separa falla-de-vial; re-medir el mismo vial separa ruido-vs-persistente |
| `lab_extern(lot_ids)` | re-análisis del MISMO material, solo lotes ya medidos, máx 6 por pedido | 60 + 25/lote | 1 turno | confirma/desmiente lecturas de lotes ELEGIDOS; **no puede correr condiciones nuevas ni identificar estructura por sí solo** (restricción de Codex §2b) |
| `register(model)` / `submit(model)` | — | 0 / — | — | el monitoreo rutinario corre en calendario fijo DESPUÉS de M0 y reporta contra el último registrado |

El estándar certificado es **un ítem del catálogo de insumos** (junto a solventes, viales,
material de re-preparación) — está disponible desde el turno 1, no se llama "calibración", y
usarlo es una COMPOSICIÓN que el agente tiene que concebir: *medir algo cuyo valor ya conozco*.

⚔ **Contraataque 1 (a "los botones nombran la hipótesis")**: con acciones genéricas y el
estándar como insumo más del catálogo, la hipótesis instrumental ya no es una affordance — es
una composición. El residuo de affordance que queda (el catálogo EXISTE) es fidelidad: toda
planta real tiene estándares en el armario; un mundo sin ellos no sería más puro, sería
irreal. La no-trivialidad se certifica aparte (§7), no escondiendo las herramientas.

## 4. La anomalía y el calendario (acepto §2c)

Los canales diagnósticos existen desde el turno 1. La anomalía llega por el **monitoreo
rutinario programado post-M0** (misma maquinaria del rung 0: aviso de calendario, reporte
contra el modelo registrado). Ninguna capacidad nueva se abre con el fallo — nada de
autorizaciones (la lección del confound del rung 0).

## 5. Outcome primario — la conjunción mecánica de Codex (acepto §5 entero)

```
Y = 1  sii
  ∃ compra ANTES de submit con DIAGNOSTICIDAD PRECOMPUTADA ≥ τ
  Y
  la entrega pasa el gate estructural y de score de SU polo
```

- **Diagnosticidad precomputada, por acción concreta**: para cada compra ejecutada (con su
  config, N, reps e historia), el server computa la separación esperada que esa acción produce
  entre los rivales congelados vivos en ese momento (distribuciones bajo cada rival →
  discriminación esperada). **Nada de etiquetas** ("calibración = diagnóstica"): una medición
  del estándar con 2 reps puede no llegar a τ; un diseño cruzado de re-viales puede llegarle.
  τ se congela en la ficha final con el análisis de potencia.
- **Gate de entrega por polo**: polo A = estructura de mezcla presente + S ≥ umbral; polo B =
  proceso simple SIN estructura horneada (espurio=0) + S ≥ umbral.
- Los dos ejes (conducta / entrega) se reportan TAMBIÉN por separado.
- La tabla estilo Dunbar queda como **tabla mecánica 2×2** (compró-diagnóstico × entrega
  correcta), sin nombres de estados mentales.

## 6. Matriz de decisión del ciclo (exigida en §4)

| Resultado agregado | Lectura | Acción |
|---|---|---|
| Todos compran diagnóstico y aciertan ambos polos | el mundo es checklist pese a §3/§7 | ABANDONAR el host (condición de salida) |
| Nadie compra diagnóstico; atribución por reflejo | la juntura B3 se reproduce en agentes | MANTENER; medir la dirección del reflejo por polo |
| Compran pero NO propagan (diagnóstico correcto, entrega vieja) | knowledge-action gap en triage | el hallazgo pasa a la línea de creencias |
| Aciertan el polo B por inercia (entregan lo histórico sin diagnosticar) | defecto 2 de Codex: inercia gana | ver ⚔2; si el gate no lo separa, REDISEÑAR |
| Asimetría fuerte entre polos (p.ej. nunca culpan al aparato) | dirección del sesgo de atribución | titular con alcance |

⚔ **Contraataque 2 (a "en el polo B la inercia acierta gratis")**: cierto si el gate de B fuera
solo "proceso simple". Defensa YA en el diseño: (i) la conjunción exige la compra diagnóstica
≥ τ — la inercia pura da Y=0 aunque la entrega acierte; (ii) el eje de entrega en B exige
además **rechazar activamente** la estructura: el examen de B incluye la banda post-t* donde
un modelo que horneó la mezcla falla fuerte (espurio bilateral), y el reporte del monitoreo
sigue mostrando el corrimiento — entregar lo histórico SIN haber diagnosticado es apostar a
que el corrimiento es irreal sin evidencia: Y=0 por la pata conductual, y el eje-entrega se
reporta aparte precisamente para ver cuánta "suerte de inercia" hay. La inercia no queda
premiada en el outcome primario; queda MEDIDA en el eje secundario.

## 7. Certificados — alcanzabilidad dividida + el robot nuevo

1. **Identificabilidad**: por cada par de rivales, existe una compra legal que los separa
   (enumerada en la tabla de §3, columna derecha) — certificado por cómputo.
2. **Alcanzabilidad condicionada**: el oráculo-dado-el-candidato valida e implementa dentro
   del presupuesto, en ambos polos.
3. **No-trivialidad de búsqueda**: **tres robots con políticas explícitas** (ya no nombres):
   - *oráculo condicionado*: recibe el candidato correcto; debe ganar (justicia);
   - *buscador ciego acotado*: política fija "comprar de todo un poco en orden aleatorio
     hasta agotar presupuesto, ajustar el mejor menú cerrado" — debe PERDER o quedarse sin
     plata antes de discriminar;
   - **robot-CHECKLIST** (la reducción del revisor hostil, hecha política): "medir el estándar
     siempre en el turno 2, después default histórico + outlier-clipping" — debe PERDER
     materialmente en el polo A (gastó en diagnóstico que no propagó y no modeló la mezcla) y
     NO alcanzar Y=1 en B si su compra no llega a τ o su entrega no pasa el gate. **Si el
     checklist gana en ambos polos, el mundo NO certifica.**
4. **Headroom**: mejor-parche y robot de menú cerrado pierden contra el oráculo en ambos polos.
5. Heredados: apareo exacto por CRN (constructivo, §2) · brief byte-idéntico · no-dictación
   (≥4 rivales vivos al llegar la anomalía, ΔBIC < 6 entre top-2) · anti-memorización ·
   **ablación por mecanismo** (batería donde cada mecanismo — T, lote, anomalía — aparece
   separado y quitarlo del modelo pierde: la "complejidad real" demostrada, no declarada).

## 8. Presupuesto, potencia y alcance

- Outcome primario Y (conjunción) por polo; potencia calculada ANTES sobre Y con τ congelado
  (análisis en la ficha final; n por brazo ~10-12, 2 polos, 1 modelo primero: ~USD 15-20).
- Seeds: familia 99600-99799. Modelo: gpt-5.4 (continuidad), réplica DeepSeek si hay señal.
- SIN crítico social. SIN polo mixto (es el peldaño compuesto siguiente — NO-GO de Codex).
- **Condición de salida**: se abandona el host si una única acción domina la discriminación
  (checklist gana) o si los mecanismos base resultan separables por ajustes independientes
  (la complejidad era decorado).

## 9. Qué falta antes de presentar a Lucas (checklist de la ronda 3)

- [ ] Ecuaciones con valores numéricos + demostración de apareo CRN corrida (código, no prosa)
- [ ] Tabla de diagnosticidad PRECOMPUTADA de ~10 acciones típicas (que muestre que el
      estándar-con-pocas-reps NO llega a τ y que hay ≥2 rutas distintas que sí)
- [ ] Los tres robots implementados en pseudocódigo ejecutable
- [ ] Análisis de potencia sobre Y
- [ ] El texto del brief (byte-idéntico, sin palabra filtrada)

---

# ENMIENDA v2.1 (ronda 2 de Codex: "supera la objeción de constructo; falta cierre formal, no ronda 3")

Crudos: `scratch/codex-respuesta-2026-08-10-d1ronda2.txt`. Contraataques: **ambos aceptados**
(el catálogo es fidelidad — con la reserva de que "checklist" queda como rival EMPÍRICO a
vencer; la inercia excluida por la conjunción es correcto — y se elimina "rechazar
activamente" del gate B: el gate observa geometría ejecutable, no intención).

## 1. Robots de verdad (los míos eran espantapájaros)

- **Robot-checklist CONDICIONAL** (el adversario real): mide el estándar con reps suficientes
  → si el estándar FALLA, conserva el modelo de proceso simple (culpa al canal); si el
  estándar PASA, investiga lote/proceso (compra reps por lote y ajusta mezcla si mejora BIC).
  **Si este checklist condicional gana en AMBOS polos, se abandona el host.**
- **Robot greedy-EIG**: en cada turno compra la acción legal de mayor ganancia esperada de
  información (con la fórmula de abajo) hasta agotar presupuesto — el techo de la búsqueda
  dirigida mecánica.
- Se mantienen: oráculo-condicionado (justicia) y buscador ciego acotado.

## 2. Diagnosticidad — la definición formal congelada (de Codex, se implementa tal cual)

K rivales congelados al llegar la anomalía, prior uniforme w_k(h0)=1/K; posterior normativo
w_k(h_t) ∝ w_k(h0)·p_k(h_t). Para la acción concreta a_t (material, IDs, T, lotes, viales,
reps): **d_t = I(H; Z_t | h_t, a_t)** — la información mutua esperada entre el rival verdadero
y el resultado de ESA compra, computada ANTES de observar. **La adquisición es ACUMULATIVA**:
D_pre = Σ d_t hasta el submit (diez compras débiles = una fuerte: misma evidencia, misma
cuenta). **τ = 0.25·log₂K** (con K=4: **0.5 bits** = reducir un cuarto de la incertidumbre
inicial); τ se fija por significado epistémico y la potencia se calcula DESPUÉS. Estimación
por Monte Carlo con seeds/M congelados y criterio conservador LCB₃SE(D̂_pre) ≥ τ.

**Y = 1[D_pre ≥ τ] · 1[G_polo = 1]**. Eficiencia η = D_pre / gasto queda como métrica
secundaria. Regla anti-tuning explícita de Codex: **si el estándar cruza los 0.5 bits fácil,
NO se sube τ** — eso demostraría que el checklist es fuerte, y se acepta el resultado o se
abandona el host.

## 3. Lote ≠ vial (estaban conflados) + los 4 canales de apareo cerrados

IDs separados: `lot_id` (material) y `vial_id` (preparación). Reglas: el stream rutinario usa
**exactamente un vial por lote**; re-preparar un vial nuevo del mismo lote es SOLO una acción
diagnóstica; la API separa `reps_sensor` (mismo vial) de `n_viales` (preparaciones). Cierres:

1. **ICC apareado**: la varianza extra del polo B se inyecta A NIVEL VIAL (compartida por
   todas las lecturas del vial), con Var(q_j + u_vial) = σ_q2² — jamás ruido independiente
   por medición (delataría la covarianza entre reps).
2. **Un vial por lote en rutina** (arriba).
3. **Asignación del indicador degradado/mal-vial**: misma probabilidad condicional a (T, t)
   en ambos polos, mismo CRN — nada de tandas/posiciones/temperaturas correlacionadas.
4. **Bordes**: trabajar lejos de los límites de pureza (sin clipping) o certificar la igualdad
   DESPUÉS de todas las transformaciones.

## 4. El nulo no se sobreinterpreta

"Nadie compra diagnóstico → B3 reproducida" SOLO tras el control de capacidad: demostrar en
sesión aparte que el modelo puede componer `material-conocido + measure`, usar IDs y operar el
presupuesto. Sin eso, un nulo es fallo de interfaz (regla ADR 0173).

## Estado: falta el checklist §9 (artefactos reproducibles) → PRESENTACIÓN A LUCAS

(1) apareo CRN corrido en código con los 4 cierres; (2) tabla de diagnosticidad d_t de ~10
acciones típicas (el estándar-con-pocas-reps NO debe llegar a τ; ≥2 rutas sí); (3) los 4
robots ejecutables; (4) potencia sobre Y con τ=0.5 bits; (5) brief byte-idéntico sin
filtraciones. Después: **la ficha se presenta a Lucas con contexto completo; nada se
construye sin su GO explícito.**
