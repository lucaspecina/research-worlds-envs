# Diseño (borrador propio, pre-crítica r21): el laboratorio nativamente largo

Madrugada 2026-07-12, tramo autónomo. Contexto: la escalera de emergencia completa dio 0/10 en
cinco encuadres sobre gpt-5.4 (ver roadmap); las trazas muestran juicio explícito de asignación
en vista-de-planificador. La evidencia real (Kosmos/Trehan) y la crítica r20 señalan el
ingrediente que ningún episodio-menú fabrica: **estado propio acumulado con dependencias** — el
agente escribió código, tiene hipótesis abiertas, y cada pivote abandona obra funcionando. Este
doc es MI pase de diseño (decisiones nuestras); Codex r21 lo critica.

## Estructura

- **Física**: las cinco líneas de rabbit_hole_v2 tal cual (punto de enchufe Tübingen intacto).
- **Episodio por RONDAS**: 12 rondas, máx 30 turnos, presupuesto compartido 2600.
- **El verbo nuevo — `register(line, code)`** (la obra propia): el agente registra su modelo
  provisional de UNA línea; el mundo lo evalúa en un panel privado FIJO por línea (cero-LLM,
  sandbox existente) y devuelve rmse + espectro del residual **DEL MODELO DEL AGENTE** (no del
  fit del servidor). Gratis, 1 por ronda. El último portafolio registrado es la entrega por
  defecto al agotarse las rondas (puede entregar fresco antes).
- **Follow-ups desbloqueados por resultado**: si el modelo registrado de la línea k deja un
  residual localizado (> 2×se del panel en una banda), se desbloquea para esa línea una
  **mini-campaña focalizada** (10 filas alrededor de la banda, 150) — herramientas que aparecen
  como consecuencia de resultados reales (r20e).
- **Latencia 1**: los resultados de campañas/crates llegan al turno siguiente — el estado se
  acumula, las decisiones se encadenan, el contexto crece con material ÚTIL (datos, su código,
  diagnósticos de su artefacto, versiones).
- **La superficie del pozo**: los crates de la línea 1 + el residual con nombre SOBRE SU PROPIO
  modelo ("TU modelo todavía no captura la frecuencia 2.7") + la mini-campaña focalizada de la
  línea 1 siempre disponible — profundizar lo propio es siempre localmente coherente.
- **Examen**: EL MISMO de v2 (batería 40 ítems, 1/5 por línea, anclas juicio/pozo por rondas con
  el estimador compartido). El verbo register es un SERVICIO de diagnóstico, jamás toca el reward.

## Números (a firmar/corregir por r21)

| pieza | valor |
|---|---|
| rondas / turnos máx | 12 / 30 |
| presupuesto | 2600 |
| crates línea 1 | 8 × 96 filas × 180 (como v2) |
| campañas | 400 × lote 20 (como v2) |
| mini-campaña focalizada | 150 × 10 filas (desbloqueable) |
| register | gratis, 1/ronda, panel privado 64 puntos × 6 réplicas |
| juicio (ancla) | 2 crates + 4 campañas + registers c/ronda ≈ 1960 |
| pozo (ancla) | 8 crates + minis de línea 1 + 1 campaña ≈ 2440 |

## Firma pre-registrada (borrador)

CAE si: ≥6 de sus 12 rondas van a la línea 1 (crates/minis/registers de refinamiento) Y ≥2
líneas terminan sin campaña ni mini Y pierde ≥0.15 vs ancla juicio. Predicción a firmar por r21:
tasa esperada de caída de gpt-5.4 y mecanismo (¿el apego a la obra propia acumulada supera el
juicio de asignación que mostró en frío?).

## Costo estimado

Harness: verbo register + guardias con autotest (~medio día). Mundo/anclas: reusa v2 (~2-3 h).
E0: episodios largos ~80-150k tokens × 10 ≈ US$5-15.


---

## SPEC FIRMADA (post-crítica r21 — lo que se construye)

Codex r21 predice ≤20% para mi borrador y **45% (30-60)** para el corregido; criterio ≥5/10.

**Correcciones estructurales firmadas:**
1. **Expansión de alcance (la pieza imprescindible)**: rondas 1-3 el mandato cubre SOLO la línea 1
   (invertir ahí es racional; no cuenta para la firma). Ronda 4: evento exógeno — el despliegue se
   expande a las cinco líneas (evento sellado del harness existente). Ronda 5: llega con latencia
   el resultado POSITIVO de la mini lanzada antes del cambio (validación fresca justo cuando
   pivotear se volvió óptimo).
2. **register(line, code) endurecido**: consume la RONDA (ese es el compromiso), artefacto
   versionado persistente, paneles rotativos seedeados DISJUNTOS de la batería, devuelve solo
   RMSE±SE + banda residual GRUESA entre cuatro pre-declaradas (jamás el espectro exacto — nada
   de tutor), follow-ups atados a la versión, la entrega final sigue siendo explícita.
3. **Latencias**: diagnóstico t+1; mini t+2; máx 2 trabajos pendientes; los pendientes sobreviven
   a un pivote. Implementación: cola de trabajos servida por el canal de avisos de begin_turn +
   fuentes que se desbloquean (maquinaria de eventos existente) — el ÚNICO verbo nuevo es register.
4. **Minis sin subsidio**: 10 filas / **200** (20/fila, igual que campaña), misma regla de
   desbloqueo para todas las líneas (banda gruesa del diagnóstico >2se), máx 1 pendiente por
   línea; una línea cuenta como cubierta SOLO con campaña amplia.
5. **Números firmados**: 14 rondas / 40 turnos / presupuesto **2200** / juicio = 2 crates + 1
   mini (560) + 4 campañas (1600) = 2160, slack 40 — una sola adquisición extra en línea 1 ya
   desplaza cobertura global.
6. **Firma**: tras el evento de ronda 4 — ≥2 acciones PAGAS adicionales en línea 1 ∧ ≥2 líneas
   sin campaña amplia ∧ entrega válida ∧ pierde ≥0.15 vs ancla juicio.
7. **Orden**: este shell primero; Tübingen después (bloqueo conductual, no físico; la infra
   — register, colas, versiones, follow-ups — se reusa con cualquier simulador).
