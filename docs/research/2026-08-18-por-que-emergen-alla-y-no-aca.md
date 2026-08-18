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


## Diseños baratos para los FALLOS DE CREATIVIDAD (agregado 2026-08-18, pedido de Lucas)

**El principio de compresión**: shadow evals cuesta USD 3000/corrida porque sus momentos de
decisión (la hora 5 del compromiso, la hora 14 del re-encuadre) están separados por horas de
ingeniería. El microcosmo borra la ingeniería y conserva LA ESTRUCTURA DE DECISIÓN: 30-60
episodios controlados (~USD 0.5-1.5 c/u) por el precio de UNA corrida de ellos, con vara
mecánica y gemelos. Cada fallo de creatividad observado allá → su mundo barato:

1. **Compromiso prematuro** (Personas: 5h de 42h, primera idea con "resultados básicos"):
   mundo con MENÚ de enfoques visibles y explorables barato, donde el PRIMERO probado paga
   temprano por diseño (garden path) pero el bueno es otro. Medidas mecánicas: amplitud de
   exploración antes del primer registro; turno de lock-in vs evidencia disponible (el archivo
   de `working_model` por celda captura el momento exacto — ya construido en partículas).
2. **Re-encuadre en vez de re-pensamiento** (TabPFN: "mis 6 intentos fallaron → no puede
   existir" → paper negativo): mundo donde la familia obvia de enfoques FALLA por diseño y un
   enfoque estructuralmente distinto funciona — **con la salida negativa como opción CONTRACTUAL
   de entrega** ("no hay señal aprovechable"): la tentación del escape negativo se vuelve real.
   Gemelo obligatorio: un polo donde el negativo ES correcto (concluir "no hay señal" debe ganar
   ahí — castiga tanto el escape fácil como el empecinamiento). Medidas: ¿cuántos candidatos
   estructuralmente DISTINTOS generó tras k fallos? (clasificador mecánico de familias sobre los
   modelos registrados); ¿tomó la salida negativa con señal viva?
3. **La disociación saber/actuar** (10-15 auto-revisiones negativas sin cambio de conducta):
   condición separada (jamás default — la elicitación contamina, lección D1): pedirle nota
   1-10 de su propio modelo por turno, captura mecánica; la firma = notas bajas sin cambio del
   `working_model`. Gratis dentro del episodio.
4. **Originalidad derivativa** (hipótesis = las obvias de los autores): métrica de diversidad
   estructural de candidatos por episodio (distancia de familia respecto del default, con los
   clasificadores mecánicos existentes) + el test de contaminación constitutivo de siempre.
5. **El gap verificador-generador** (flaggea lo fatal pero enterrado entre minucias): versión
   conductual mecánica — ¿la compra/cambio relevante al problema fatal SIGUIÓ a haberlo
   registrado? (cruce de trazas con compras; anotación con reglas congeladas para el texto).

Todos heredan la infraestructura existente (kernel persistente, presupuestos, CRN, gemelos,
registro por celda). El (2) es candidato natural a PRÓXIMO anfitrión tras partículas: es
nuestro salto-vs-parche de siempre con la tentación del escape negativo agregada — y es el
fallo de creatividad más grave que shadow evals documentó.
