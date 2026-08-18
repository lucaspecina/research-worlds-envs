# ¿Por qué los vicios emergen ALLÁ y no acá? — las características del hábitat (análisis con Lucas, 2026-08-18)

> Disparador: shadow evaluations (2607.27191) muestra a escala real varios modos que NOSOTROS
> no logramos reproducir en mundos controlados (overstay 0/60; deriva; recursos). Pregunta de
> Lucas: ¿qué características tenían esas tareas para que emergieran ahí, por qué no en las
> nuestras, y cómo diseñar mundos donde emerjan CONTROLADAMENTE? Análisis, no decisión.

## El principio general que ordena todo

**Cada vicio emerge cuando su tentación es la política localmente atractiva.** En shadow evals
todas las tentaciones existen gratis porque la realidad es cara y el feedback ausente; en
nuestros mundos, varias conductas correctas eran tan baratas (o la incorrecta tan imposible)
que el vicio no tenía hábitat. No reprodujimos vicios porque les faltaba SU tentación.

## Las cinco características de su hábitat vs el nuestro

| Característica de shadow evals | Nuestros mundos | Vicio que habilita |
|---|---|---|
| **Horizonte largo con inversión hundida** (6 días; abandonar = perder días de trabajo propio) | 5-16 turnos; nada que abandonar | overstay/pozo (nuestro 0/60), backtracking local-vs-proyecto |
| **Vara tácita** (¿"publicable"? nadie la declara; la única brújula es la auto-revisión, indulgente) | vara oculta pero EXISTE y es computable | juicio de la vara (resultados flojos como hallazgos) |
| **Jerarquía de decisiones** (proyecto > diseño > experimento > análisis) | espacio de acción plano, una pregunta | "pivots chicos, jamás repensar" — solo observable si HAY niveles |
| **Autoría/propiedad del enfoque** (ellos diseñaron su approach → apego) | el encargo viene dado | escalada por identidad (v2.2 — VIVA solo en viñeta, jamás testeada agéntica: shadow evals es su primera evidencia agéntica indirecta) |
| **Cero confrontación del mundo** (la realidad nunca te dice "mal"; solo tus propias revisiones, que descontás) | desde D2 el mundo confronta (monitoreo, débito) | la deriva y el no-backtrack florecen sin cobro — su setting es el hábitat C3/C4 puro |
| **Fases con recursos** (explorar/medir/escribir compiten por tiempo y cómputo) | presupuesto de una sola fase, planificación trivial | calibración de recursos (<50% gastado) |

Coincide con el diagnóstico que ya teníamos escrito (anatomía 2026-08-10): el fenómeno real es
**largo, acompañado y ambiguo**; nuestros mundos, cortos, solitarios e inequívocos. Shadow evals
es el extremo largo+ambiguo — y ahí los vicios florecen solos.

## Palancas de diseño: cada vicio no-reproducido → su tentación fabricable

1. **Overstay/pozo**: episodio multi-fase donde el agente CONSTRUYE infraestructura propia
   (pipeline armado en turnos) antes de que lleguen respuestas; un ramal garden-path que paga
   goteo temprano y se seca; cambiar = re-armar (costo hundido real). Exige el mundo-largo con
   goteo ya direccionado.
2. **Juicio de la vara**: mantener la vara oculta PERO dar un canal tácito inferible — archivo
   histórico de entregas aceptadas/rechazadas por la planta (¿calibra la vara desde ejemplos?).
   Mecánico.
3. **Recursos**: presupuesto con estructura de fases (la ventana de exploración cierra; medir
   se encarece tarde; acciones con vencimiento) → planificar se vuelve real; se mide asignación
   vs óptimo con la maquinaria de información esperada.
4. **Drift**: horizonte largo + pedidos del mundo que EVOLUCIONAN a mitad de corrida (la planta
   cambia la especificación); mecánico: ¿la entrega honró el pedido vigente?
5. **Backtracking multi-nivel**: elección de ENFOQUE al inicio (familia de instrumento / marco
   de modelado) con un camino garden-path diseñado; medir si retrocede a nivel proyecto o solo
   parchea. Exige jerarquía en el espacio de acciones.

Todo converge en la misma dirección ya declarada (mundo largo secuencial con goteo) — shadow
evals valida que ESOS ejes faltantes son donde viven los vicios que no pudimos reproducir.

## Dónde se documenta cada cosa (la convención, para no perderla)

Evidencia de vicios (papers o propia) → SOLO `docs/vicios/` (hecho: v2 candidatas, v4, v5, v9)
· lectura con citas → `lectura-de-fuentes.md` (hecho) · fila cronológica → `research/README.md`
(hecho) · derivación vicio→mundo → `mundos-por-vicio.md` (las palancas de arriba, cuando se
decida construir) · las WIKIs solo absorben lo que cambia la HISTORIA en llano (WIKI-FALLAS:
puntero agregado hoy).
