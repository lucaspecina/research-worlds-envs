# Roadmap y estado — WAGER

> **Dónde estamos, la cartera de mundos, y el plan de validación E1→E4.** La sección
> *Estado actual* se mantiene al día cada sesión; el resto es el plan estable. Los
> resultados detallados de cada hito están en `docs/adr/`; lo sin decidir en
> `docs/open-questions.md`.

## Estado actual `[VOLÁTIL — mantener al día]`

**Verde**: reward path (Slice 1) + harness (C1+C2+C3) + factory de derivación completos;
`pytest` ~127 verdes. Infra de mundos-trayectoria lista (ADR 0068). Docs reestructurados
(ADR 0070) + re-skin a "línea de proceso" (ADR 0071).

**Hitos**: **v2 (trofeo)** — tríptico confirmado con solver real; en 10 episodios / 2
familias nadie infiere composición por-lote, máx R=0.666 (falta juicio, no ejecución).
**#6** — el presupuesto discrimina estilos. **#11 (ADR 0074) — el formalismo 2 VALIDADO**:
gates all-PASS a la primera, K̂=2000 certificado (la invisibilidad de K medida), E0
0.763/0.894 con cero crashes en el contrato de trayectorias; residuo = triangulación del
régimen histórico. Dos deudas de factory registradas (ladder/battery foto-only).

**Próximo**: **EVENTOS D4 HECHOS (ADR 0083)** — la noticia sellada funciona punta a
punta: contrato `EpisodeEvent` + `hidden_columns` + fuentes desbloqueables + aviso en
prompt; certificado de incorporación ALL-PASS (ignora 0.0002 vs incorpora 0.989);
first_story completo en sus DOS variantes (pin no-op verificado byte-idéntico). E0 con
noticia: 0.991 (incorporó y clavó) y 0.000/R_uncl −2.97 (incorporó PERO fabricó
causalidad en señuelos + payload 59KB — otro vicio del catálogo preciado en vivo, dato
para el mundo carnada-de-significancia). **Orden vigente (ADRs 0084-0087)**: A-escasa ✓ EJECUTADA (ADR 0087: los hábitos
sobreviven a la escasez, la TERMINACIÓN no — R 0.925/0.000/0.308/0.088, 4/4 con
investigación completa; mecanismo real por partición: rama histórica rota 2/4 +
payload 1/4). PILOTO ANCHO fase-instrumento ✓ EJECUTADA (ADR 0089: **LA ANCHURA
DILUYE LOS DIENTES** — twin de deriva −0.115→0.874 a 19 cols, vis_offsets FALLA;
CV(R) 0.18% y canonical 0.998 estables; la moneda-cliente NO se diluye; el mundo ancho
NO certifica como está; E0 en suspenso). BARRIDO c_F sampling ✓ CORRIDO (ADR 0090:
v0.55-2 disparó → NO es semántica nueva, es el barrido pre-firmado). **TECHO DE ANCHURA
confirmado** (pre-registro ii): ningún c_F da margen robusto a la trampa-de-canal ancha
(piso c_F≳1.75) Y al techo de censura de survivorship a la vez — colisionan en ~0.055≈piso.
c_F* del subconjunto CERTIFICABLE narrow = **0.25 VINDICADO** por su propio barrido.
Mecanismo verificado (twin 96.4% en outcome; dilución del contraste, no D_MAX). Rechazos
(a)/(b)/(c) con rationale. **(d) FIRMADA + c_F=0.25 CONGELADO narrow** (ADR 0091).
**CANDADO SELECTIVO — COMPUERTA CERRADA (ADR 0092)**: el ajuste-tramposo más fuerte
(funcional PERFECTO, cero joint) saca R=−0.53 → la energía caza la ceguera de mecanismo
global sin candado → **NO se implementa; (d) puro + funcional**. Hallazgo colateral: c_F
alto haría gameable el funcional (oracle-gamer→1) → el freeze de 0.25 es doblemente
correcto (techo de ruido ∧ no-gameabilidad → mismo c_F). Anchura = dial de ATENCIÓN.
**PROTO-DESIGNER arrancado (ADRs 0093)**: spec `docs/proto-designer.md` (consigna →
generador LLM → certificación cero-LLM → yield; 4 decisiones A/B/C/D). **Peldaño FÁCIL
(re-skin) corrido: yield 1/1** — gpt-5.4 re-skineó #16 a un dominio de secado
(`dryer_setting/moisture_probe/shelf_life`) con R byte-idénticos + gates PASS a la primera
(`wager/factory/proto_designer.py`; `cases/reskin_pilot_v0` = artefacto de yield, no slot
nuevo). **CHEQUEO DE CIENCIA — 1er experimento de validez CORRIDO (ADRs 0095/0096)**: libre vs
cuidadoso, trampas vs controles, pre-registro firmado antes de mirar. **La predicción
primaria FALLÓ**: el control mostró la MISMA brecha que las trampas (resta de diferencias
−0.02, se firmó ≥0.15) → el cuidado mueve fiabilidad de ejecución GENERAL, no un vicio
específico (alarma pre-registrada). Subpotenciado (n=3, R bimodal); los ceros confunden
ejecución con juicio. Se sostuvieron las 2 predicciones "el cuidado no ayuda acá" (v2
profundo ≈0, first_story sin brecha). NO es doom (v2 se comportó como se predijo; la
disciplina funcionó) — empuja hacia la pista ESPECÍFICA de Lucas sobre el prompt general.
**→ RESUELTO del lado SEGUIR (ADRs 0097/0098) — ver el cierre "LÍDER DE ESTADO" al final de esta sección.**

**Peldaño MEDIO INTENTADO (ADR 0094)**: A/B firmados; gpt-5.4 generó un mundo confundido
válido (injection-molding) — **el generador ANDA**; el verificador genérico
(`wager/factory/generic_certify.py`, nuevo) destapó una cadena de deudas: canónico grado-2
✓, visibilidad sub-batería ✓, cupo observacional ✓, **canónico estructural PENDIENTE**
(de-confunde do() pero no reproduce la asignación confundida → recov 0.89). **Freno antes
del rabbit-hole** (nuestro propio vicio-objetivo). **(1º) completar `_canonical` a
estimador estructural → re-correr medio → yield** → difícil (Mundo B) → resto de cartera. (eje anchura en la consigna; writer ciego; yield sin-retoque;
auditoría humana pre-E1) con escalera: fácil (re-skin) → medio (estático nuevo) →
difícil (**Mundo B**, tres decisiones de ADR 0084 en la consigna; timebox + fallback
manual). Partición seed31 EJECUTADA (ADR 0086): R_fid +1.005 / R_mdl −3.975 — era el
gamble de payload; lecturas de ADR 0083/0085 sobre seed31 retractadas. Después: colas
(#13), #12 no-lineal, Anomaly, κ (7 casos); cola conocida #8/#10. Cartera 11/20. Re-lectura #6 (ADR 0088): bought_unused_evidence re-etiquetada rushed_termination (gpt 4/4 compró Y midió, jamás integró); firma nueva al catálogo; corrección a ADR 0067 (DS-seed3 sí compró 20 filas — chequeo-de-valor pendiente).

**LÍDER DE ESTADO (2026-07-07) — el corazón documentado.** Cerrado el chequeo de ciencia del
lado SEGUIR y documentado el catálogo (evolución, no refundación):
- **Validez de constructo — REPLICADA en 2 modelos (ADRs 0097/0098 + réplica 0110)**: la pista
  DIRIGIDA al vicio AÍSLA el vicio (levanta el mundo del vicio, deja plano el control). gpt-5.4:
  scarce 0.00→0.87. **DeepSeek (8 seeds + clasificador de ceros AUTOMÁTICO): scarce 0.29→0.81
  (+0.52), control −0.005, resta de diferencias +0.52.** Caveats: 2 modelos; el control cerca del
  techo → falta un control con headroom (requisito de la batería E1). **Hallazgo de perfil**:
  DeepSeek se casa con la 1ª hipótesis AUN a presupuesto pleno (gpt no) → el "vicio solo bajo presión"
  es de gpt, no universal (OQ 20). El label del catálogo baja de "preliminar" a "replicada, con
  caveats" — NO "validado".
- **El catálogo = el corazón (ADR 0099)**: `docs/failure-modes.md`, vivo — de un failure mode
  documentado → mundo puntuable; taxonomía por **DINÁMICA DE MUNDO** (6 familias) + 7 principios
  + scaffold de diseño.
- **Corte primario (ADR 0100, corrección de Lucas)**: **OPERACIÓN** (la arregla el andamiaje →
  NO es blanco de WAGER) **vs JUICIO** (la razón de ser). Principio 8 (aislar juicio de operación)
  + triage obligatorio §0.5. Respaldado por base-42%/scaffold-1.5%: el scaffold no mueve el juicio.
- **Cosecha deep-research integrada (ADR 0101)**: 26 fuentes → **19 claims verificados** (voto
  adversarial) + 4 con cita textual; **todo JUICIO**, integrado a §4. Recetas buildables
  destacadas: **Klayman-Ha embedding** (H⊂T ⇒ el test positivo NUNCA falsa → confirmar pierde
  garantizado), **7 respuestas a datos anómalos de Chinn-Brewer**, **perseverancia-tras-retracción**
  (evento D4 que invalida evidencia YA comprada). **Familia G (razonamiento causal) ADOPTADA como
  grupo propio (Lucas, 2026-07-07 — ADR 0102)**: la cura es una movida distinta (intervenir), no
  verificar más; ya hay maquinaria (`confounded_gen_v0`). Ahora son 7 familias (A-G).
- **Diversidad ESTRUCTURAL — principio 9 + mapa (ADRs 0103/0104/0105, precisión de Lucas)**: un
  vicio se fractura en estructuras distintas (no en disfraces); la cartera debe cubrirlas o el
  entrenamiento overfitea. TRES búsquedas mapearon las estructuras por vicio: **1≈8, 2=5, 3=4, 4=6,
  5=7, 6=4, 7=2** (6 de 7 vicios con variedad). Puntos ciegos ya LLENADOS (4/5/2); **único hueco:
  vicio 7 sub-tipos colisionador/selección (0 casos)**. Caveat de diseño (phlogiston): persistir es
  vicio solo si la alternativa es decididamente superior. Ver ★ Mapa en §4.
- **CATÁLOGO ESPEJO + DOCTRINA DE PARES (ADR 0106, 2026-07-09)**: la 4ª búsqueda trajo las
  estructuras de AHA (5, de a pares con su polo vicio; ★★ en `docs/failure-modes.md` §4; crudo en
  `docs/research/`). Doctrina nueva: **principio 10** (el PAR es la unidad — juicio = discriminación
  activa comprable; CERTIFICADO DEL PAR robot-hábito/robot-juicio; métrica (R1,R2,min) solo
  reporting) y **principio 11** (tiers A/B con rama pre-registrada "frontier lo resuelve de rutina").
  Convergencia independiente del principio de pares registrada como robustez. El catálogo es
  CANTERA, no cola (línea de llegada sigue en 12 mundos). Dos-espacios = Mundo B (pedigrí
  Klahr-Dunbar, no se abre mundo nuevo). ECHO = tarea con timebox, no muro caído.
**AUDITORÍA CRUZADA cartera-vs-catálogo (ADR 0112, 2026-07-09)**: dos lecturas independientes, mismo
diagnóstico (convergencia registrada) — la cartera es pre-catálogo: fuerte en causal (5) y
estructura-escondida (trofeo), VACÍA en atención (0/5) e interacción (0/4). Posición actualizada:
**tres capas** (planos=catálogo → plantas piloto=mundos controlados a mano → fábrica=generación
automática desde plantillas) + **dos niveles de diversidad** (ENTRE estructuras [intelectual] y
DENTRO de cada una [fábrica]) — §0.6 del catálogo. Decisiones: retro-cert de los 5 causales (robots
derivados de twins, fase de rigor de P2) · vicio 3 re-alojado (optional stopping temporal;
variable-elegida 2-3 outcomes; el mundo ancho ya no es anfitrión) · familia F fuera de v1 (exige el
verbo PREGUNTAR = semántica nueva = tripwire) · anomalías #14/#15 re-espec propagada · twotank CAE ·
colas DEGRADADO a held-out E3 · tabla de re-derivación de slots = PAPEL a validar por Lucas (nada
entra a la cola por esta vía).

**DERIVACIÓN OFICIAL VICIO→MUNDO (ADR 0113)**: `docs/mundos-por-vicio.md` — la síntesis en llano por
error (fuentes · contextos · estructuras · el mundo que lo caza · estado), **catálogo-primero** (lo
construido no manda). Supersede como referencia de diseño a la tabla de re-derivación por slots de
ADR 0112 (que anclaba en la cartera vieja — el vicio de costo hundido, cazado por Lucas).

**RONDA CODEX + RE-CENTRADO (ADR 0117, 2026-07-10) — el estado que manda.** Primera consulta a Codex
(ADR 0116; crudo en `docs/research/2026-07-10-codex-critica-integral-gpt56sol.md`): núcleo defendible,
tesis sobredimensionada; su golpe verificado — en el experimento de pista **la trampa y el control
recibieron pistas DISTINTAS** (chequeado contra ADR 0097: cierto) + control al techo + "la pista
positiva es un checklist ⇒ podría ser OPERACIÓN por nuestro propio corte 0100". Se re-etiqueta el
resultado como **"efecto de instrucción sobre desempeño, replicado en 2 modelos"** (la validez de
constructo vuelve a hipótesis, a probar con diseño corregido). **DECISIÓN DE LUCAS (sobresee el
"posterguen la fábrica" de Codex y el rango del principio 10)**: los gemelos son AGREGADO, no eje;
**lo fundamental del proyecto = diseñar mundos-vicio que después se generen AUTOMÁTICAMENTE con
diversidad real** (estructuras + composición con propiedades emergentes, no re-skins) — la cola de
abajo re-centrada en eso. Vulcano (par de aha) → cantera.

**TRES VÍAS DE GENERACIÓN — REGISTRADAS; TÜBINGEN PREFERIDA Y DIFERIDA (ADR 0132, 2026-07-10)**: la
pregunta de Lucas por los "seeds de papers" destapó vías dispersas en tres docs; quedan comparadas en
`operators.md` §4 + `proto-designer.md` §3 — (1) plantilla+composición [actual; arreglo dado+dominios
DISEÑADO, alcanza para hoy], (2) semilla-paper [doctrina original, fallback], (3) semilla-simulador
[Tübingen: "romper"=ESCONDER una pieza de un sim real portado; preferida para diversidad profunda;
piloto de 1 mundo cuando se abra el slot]. Decisión de Lucas: motores = CONTENIDO, no instrumento →
la fábrica se PAUSA post-batch y el slot vuelve a VALIDAR (P1).

**RONDA 11 + GO DE LUCAS (ADR 0133, 2026-07-10)**: Codex corrigió el rationale de 0132 (la
distribución de mundos ES parte del instrumento — los manuales calibran, no prueban no-circularidad)
y Lucas lo aceptó con su matiz de secuencia: **un único fork diagnóstico acotado → se reabre
construcción CALIBRAR-MUNDOS-PRIMERO** (mundos concretos a mano para saber qué se puede medir;
el piloto Tübingen timeboxed es parte de esa tanda), la industrialización de diversidad
dentro-de-tipo después. El fork queda re-encuadrado: mide integración análisis→entrega (NO
terminación — ésa queda hipótesis aparte) y aplica el corte operación-vs-juicio ADENTRO (brazo
scaffold como techo operacional). Pre-registro completo firmado en ADR 0133; corrida ~US$1.

### Cola de trabajo ÚNICA (ADR 0107; **reordenada por VALOR, ADR 0108** — no por orden de llegada)

**Regla de trabajo-en-curso (WIP)**: máximo **1 validar + 1 construir + 1 investigar** en vuelo a
la vez. Todo lo demás espera acá — visible, no caído. Antes había 4 listas desparramadas (PRÓXIMO,
deudas vivas, deudas sin gatillar, minados pendientes); esta cola las reemplaza a TODAS.

**Criterio de valor (ADR 0108, orden de Lucas)**: valor = reducción del riesgo-de-que-todo-sea-en-
vano (¿el instrumento MIDE?) + generación del activo único (evidencia tier-A sobre modelos), por
unidad de costo. Consecuencia: **la validación COMPONE (todo lo posterior hereda su credibilidad);
el inventario sin validar NO compone** → validar-lo-existente > construir-lo-nuevo > investigar-más.

| P | Etapa | Ítem | Por qué acá (valor) | Próximo paso concreto | Estado |
|---|-------|------|---------------------|----------------------|--------|
| 0 | **validar** | Réplica DeepSeek + clasificación automática de ceros (ADR 0098) | mata-o-confirma el claim central | ~~48 episodios DeepSeek~~ | ✅ **HECHO (ADR 0110)**; re-etiquetado por ADR 0117: "efecto de instrucción, replicado" — la validez de constructo la prueba P1 |
| 1 | **validar** | Experimento de pista CORREGIDO y MÍNIMO (ADRs 0117/0118/0119) | el claim central no podía apoyarse en pistas desparejas + control al techo | ~~48 episodios DeepSeek corridos (~US$2)~~ | ✅ **CERRADO — VEREDICTO NEGATIVO (ADR 0121)**: P0/P1/P3/P4 fallaron; la pista HUNDIÓ su propio mundo (pares por seed −0.44), el placebo de estilo movió el score, el control sin headroom (0.958). El resultado viejo queda NO REPLICADO; varianza corrida-a-corrida documentada (0.29 vs 0.58; ceros del brazo pista 2/8→5/8) → invalida el positivo Y el negativo. **El método NO se abandona (Lucas, ADR 0122)**; rediseño CONCRETADO con Codex ronda 5 → **ADR 0124/0125: protocolo honesto de 3 fases**. **Fase 1 HECHA (ADR 0129)**: 3 corridas idénticas dieron +0.52/−0.58/+0.64 → varianza DEMOSTRADA (ninguna corrida n=8 es evidencia); clasificación ciega: 15/16 descubren la estructura, los catastróficos aparecen en AMBOS brazos (T4 atractor preexistente > T2) — el fallo vive en la ENTREGA (calibración/mediador espurio); matizado por 0130 (cuello heterogéneo, fork = experimento central). **GO DADO (ADR 0133)** y **CERRADO (ADR 0134)**: 60/60 entregas, replays byte-exactos, ~US$0.6. Lectura prefirmada que aplicó: **"manipulación fallida"** — ni el principio ni el checklist mueven la entrega (limpias 0%/0%/5.3%). Hallazgos: defectos de integración UNIVERSALES (59/60) y deterministas POR DONANTE; **el score NO los ve** (R≈0.98 con flechas sin respaldo → coordenada de diseño de batería); la línea pistas-textuales queda CERRADA; el corte operación-vs-juicio queda abierto solo por la vía de andamiaje PROGRAMÁTICO (no probado). **Se disparó el límite duro → slot construir REABIERTO (calibrar-mundos-primero, piloto Tübingen)**. La pregunta bloqueante de Lucas (¿la nota refleja la creencia?) se respondió con el PROBE DE TRADUCCIÓN (ADRs 0135/0136): canal SANO (45/45 al piso, orden verdad<intermedio<folklore preservado 5/5); el desacople era BATERÍA INSUFICIENTE (comprime 143× en milésimas, premia ruido inflado — receta de endurecimiento + alerta E2 + DeliverySpec v1 adoptado) |
| 2 | **construir** | **CAMINO DE LA FÁBRICA (ADR 0117 — el core)**: destrabar D1 → re-correr proto-designer MEDIO → yield | **lo más importante del proyecto** (Lucas): vicio→estructura→plantilla→generación automática con diversidad; sin esto no escala | **D1 ✓ (0120) · PILOTO FRESCO ✓ PASS 1/1 · MICRO-BATCH ✓ 5/5 (ADR 0131)** — el panel midió el colapso: 4/5 dominios iguales, params idénticos por estrato → "plantilla repetible, no diversidad". Arreglo DISEÑADO (params por RNG en código + dominios dirigidos); vías de motor comparadas y decididas en ADR 0132 (Tübingen preferida, diferida) | **PAUSADA (ADR 0132) — el slot vuelve a validar (P1); arreglo diseñado, se implementa cuando la fábrica reabra** |
| 3 | **construir** | ~~Mundo del POZO~~ → **SUPERSEDIDO (ADR 0128)**: secuencia = piloto fresco (8 requisitos r9) → **micro-batch N=5 congelado** → auditoría + panel conductual → **plantilla de RIGOR ESTADÍSTICO** (precisión fabricada / decisión de replicar — cobertura genuina por r8). El pozo se degrada a PERILLA/distractor dentro de mundos causales o de rigor (su núcleo ya recibe presión genérica en AHC) | los builds van donde somos únicos (cobertura) y el multiplicador se prueba con N que informa (5, no 1) | implementar `medio()` congelado → piloto → batch | **decidido con Codex (r9), delegado por Lucas** |
| 4 | **validar** | Retro-cert de los 5 causales (CPU, gratis) → **mini-spread multi-modelo** (perfiles de vicio por modelo, OQ 20) | bandas de referencia + el activo único (evidencia tier-A sobre modelos) | (i) CPU puro; (ii) presupuestar ANTES + auditoría humana de baterías (Lucas) | tras P1 |
| 5 | **construir** (oportunista) | Par terco↔paranoico desde las DOS mitades YA construidas (#16/#17, re-skin a fachada común) | el gemelo casi GRATIS — seguro anti-reflejo (agregado, no eje; ADR 0117) | re-skin validado + robots-reflejo cruzados + métrica min | cuando se libere slot construir |
| 6 | **investigar** | Minado combinado: colisionador/Berkson · apofenia nombrada · pares faltantes · **baseline genérico fuerte no-LLM (Codex)** | congelado por rendimiento decreciente; el baseline entra cuando P1 cierre | no se abre salvo que un build lo NECESITE | congelado |

**VENTANA AUTÓNOMA 2026-07-11 (corte 8am ART; ADRs 0137 + resultados sellados)**: (1) red-team del
score CERRADO — zona muerta confirmada, deuda D0 con gatillo pre-E2, gate nuevo rige para mundos
nuevos; (2) protocolo VICIO-VIVO estrenado: **gpt-5.4 × first_story = vicio NO vivo** (1/8 con la
firma; 8/8 usan la escapatoria; los 2 ceros son de entrega) → first_story queda control-de-facto
para frontier actuales; el par con vicio vivo se busca en mundos nuevos. Decisiones para Lucas:
GO receta D0 · ¿first_story reclasificado [C]?

**VENTANA 2026-07-11 (continuación, tarde): `rabbit_hole_v0` CERTIFICADO 19/19 (ADR 0138)** — el
primer mundo del vicio 2, con historia honesta de tres rondas: r14 falló 15/17 (66 filas directas
solas recuperan la curva a 0.955 — la "fuente cara" era escapatoria potente), el correctivo 45/fila
r15 quedó REFUTADO en sus dos objetivos (pozo moderado = lotería de rescate), y el veredicto r16
selló: rollback a 15/fila + **claim ESTRECHO (solo POZO PROFUNDO)**: perseverancia extrema hasta
consumir el presupuesto de la investigación útil (robot profundo 0.51-0.57 estable, desperdicia
~70% del beneficio disponible; disciplinado 0.97; curva de profundidad controlada 0.97→0.88→0.77→
0.55→plateau). Pozo moderado = diagnóstico sin gate. Primer caso con el gate red-team 0137 de
serie (limpio). **E0 gpt-5.4: 0.808/0.766 — NO cae en el pozo a horizonte corto** (pierde por no
cubrir el extremo alto): segunda vez que el vicio no está vivo en frontier en corto. **DOCTRINA
FIJADA POR LUCAS (2026-07-11, prevalece)**: el objetivo es que **EL MUNDO GENERE el vicio** —
siempre o casi siempre, o al menos en muchos casos. Si el vicio no emerge, **lo que se cambia es
EL MUNDO**, no se sale a buscar un modelo débil que sí caiga (eso sería tramposo: encontrar "algún
modelito" susceptible no es el activo; el activo es el mundo que reproduce las CONDICIONES bajo
las que agentes reales caen — y la evidencia de campo dice que caen: Kosmos, Trehan, SciAgentGym).
Es ITERATIVO: construir → sondear → reconstruir. La autocrítica de Codex r17 (crudo en
`docs/research/`) da la dirección del rediseño y CONVERGE con esto: los mundos actuales
sobre-limpian la señal — el rabbit hole real tiene **progreso local GENUINO** (cada paso mejora
algo, pero menos que la alternativa), **retornos decrecientes RUIDOSOS** (no retorno marginal
cero), **señal negativa ambigua** (no un falsificador barato y contundente) y **escalada por
compromisos chicos** (foot-in-the-door: K decisiones sucesivas de continuar, no una compra
grande). Esos cuatro ingredientes son la spec del **pozo v1**. Los diagnósticos de r17 se reciclan
AL SERVICIO del rediseño (no de la caza): el fork-desde-checkpoint (brazo señuelo-agotado vs
control con telemetría-que-sí-paga) mide si la tentación actual siquiera llega al punto de
decisión y qué ingrediente falta; el dial K∈{1,4,8} de capas se convierte en PERILLA DEL MUNDO
(escalada), con su control de horizonte (chunks útiles) para separar pozo de degradación de
contexto. El barrido multi-modelo queda DEGRADADO a calibración posterior (bandas por modelo
cuando un mundo ya elicite), no es la estrategia. Restricción que no se negocia (flogisto): el
mundo debe seguir siendo JUSTO — "genera el vicio" = la tentación es real y fuerte y el que tiene
el juicio escapa y gana; un mundo donde todos pierden entrena paranoia, no juicio. Próximo paso:
**spec del pozo v1 con los 4 ingredientes (Codex r18, números firmados) + fork-probe como
herramienta de diseño**. Pendientes menores: ¿rabbit_hole ocupa el slot #8? (Lucas) · protocolo
vicio-vivo formal sobre rabbit_hole v0 (8 seeds) — vale como línea de base ANTES del v1.

**Cantera adicional (ADR 0117)**: par NEPTUNO/VULCANO (aha — estacionado; su test de viabilidad gratis
queda listo para un rato ocioso) · mundo causa-efecto familia G (sigue tras D1, compite con P3) ·
higiene de claims + 2 inconsistencias entre docs señaladas por Codex (ubicar y reportar antes de tocar) ·
**piloto semilla-simulador Tübingen (ADR 0132)**: UN mundo punta a punta desde el sim publicado más
simple, para medir el costo real de porteo — LA vía preferida de diversidad profunda cuando se abra
el slot construir (fallbacks: semilla-paper → plantilla+arreglo).

**Deudas técnicas (ordenadas por qué desbloquean, no por antigüedad)**:
**D0 — ZONA MUERTA del score (ADR 0137, GATILLO: bloqueante ANTES de E2/entrenamiento; orden de
Lucas 2026-07-11: "hay que retomarlo más adelante, ahora otras prioridades")**: la batería de
first_story da R=1.0000 exacto a defectos de 17-90× el piso de fidelidad (meter sd=3, varianza
×0.7, default-histórico-fijo) — un RL lo explotaría gratis. Receta lista en el ADR (peso al
histórico + régimen de dispersión + revisar D_MAX); el gate del red-team (`redteam_score_0137.py`,
~20 min CPU por mundo) ya rige para mundos nuevos; el arreglo de casos certificados espera GO. ·
D1 `_canonical` estructural (ADR 0094 — desbloquea P3 + proto-designer MEDIO) · D2 definición
mecánica del robot incremental (ADR 0106 — desbloquea certificados de mundos-aha) · D3 timebox ECHO
(ADR 0106) · D4 κ (4 divergencias R vs |ΔP|) · D5 DS-seed3 chequeo-de-valor σ (ADR 0088) · D6
variante dominio-pareado #16/#17 · D7 re-elicitación rival (c) · D8 barrido c_F suite sampling ·
D9 derivación automática para mundos-ventana.

**Cantera (no cola — de acá se saca SOLO cuando el slot "construir" se libera)**: los 8 slots por
autorar de la cartera (#8, #10, #13-15, #18-20) · #12 rediseño no-lineal (ADR 0076) · par
angosta/amplia Klayman-Ha (spec lista, `docs/mundo-espejo-klayman-ha.md`) · Mundo B / dos-espacios
(pedigrí Klahr-Dunbar, ADR 0106) · proto-designer DIFÍCIL.

## Cartera E1 (20 slots; 11 hechos · 1 bloqueado · 8 por autorar)

> El mundo = **composición de operadores** con dificultad declarada, no trampas sueltas.
> Buckets: **[C]ontrol** (frontier debe aprobar) / **[T]rampa** (headroom buscado).
> Presupuesto holgado en [C], ajustado en [T] (el dial central).

| # | Slot | Suite | Formalismo | Bucket | Estado |
|---|------|-------|-----------|--------|--------|
| 1 | dummy_dose_v0 | causal-cliente | SCM | C | HECHO |
| 2 | latent_mix_v0 | Latent | SCM | C | HECHO (control negativo) |
| 3 | latent_mix_v1 | Latent | SCM | C | HECHO |
| 4 | selection_bias_v0 | sampling | SCM | C | HECHO (saturado) |
| 5 | latent_mix_v2 | Latent | SCM | T | HECHO (tríptico confirmado) |
| 6 | selection_bias_scarce_v0 | sampling | SCM | T | HECHO (presupuesto discrimina) |
| 7 | survivorship_censor_v0 | sampling | SCM | T | **HECHO** (ADR 0077: capa archival nueva; naive malaprecia reclamos 5×; E0 0.975/0.818) |
| 8 | immortal-time | sampling | SCM longitudinal | T | por autorar — reasignación propuesta (0112, a validar): **pozo-señuelo con costo hundido** (vicio 2, hoy con CERO mundos) |
| 9 | batch_confound_v0 | canal | SCM | T | **HECHO** (ADR 0078: pendiente espuria +87%; twin deriva −0.115; E0 0.890/0.933) |
| 10 | missingness informativo | canal | SCM | T | por autorar — reasignación propuesta (0112, a validar): **escalada de compromiso** (vicio 2: inversión previa + señal negativa + punto seguir/pivotear, con evento D4) |
| 11 | logistic_yield_v0 | Horizon | **ODE** | C→T | **HECHO** (formalismo validado, ADR 0074) |
| 12 | twotank_clearance_v0 | Horizon | ODE | T | **CAÍDO (ADR 0112)** — su hallazgo ya pagó (ADR 0076: test de viabilidad + regla de degeneración); slot liberado → propuesta 0112: **par 1a/1b Klayman-Ha** (spec lista) |
| 13 | colas M/M/k | diagnóstico | eventos discretos | T | **DEGRADADO a held-out de E3 (ADR 0112)** — formalismo fresco para el examen de generalización; construirlo para E1 lo quema. Slot E1 liberado → propuesta 0112: **consiliencia** (dos anomalías sembradas; el scoring ya la premia) |
| 14 | anomalía plantada | Anomaly | SCM | T | por autorar — **re-espec PROPAGADA (ADR 0112, clase registrado≠integrado)**: deliverable = predicción bajo regímenes contrafácticos declarados en stakes (sin-anomalía / onset-distinto / post-horizonte), cero jueces |
| 15 | anomalía temporal | Anomaly | ODE | T | por autorar — misma re-espec propagada que #14 |
| 16 | prior_sweetspot_v0 | Prior | SCM | C | **HECHO** (ADR 0079: prior verdadero; twin lineal −0.315; E0 1.000/0.985 — techo tocado) |
| 17 | first_story_v0 (Mundo A anti-vicio) | Prior | SCM | T | **HECHO** (ADR 0082: 1er certificado de trampa necesaria — terco 0.005 vs cuidadoso 0.960; E0 0.804/0.953, frontier rompe su hipótesis de rutina) |
| 18 | identificabilidad | identificabilidad | SCM | T | por autorar — re-mapeo propuesto (0112, a validar): **"intervenir-o-fallar"** (la sub-estructura causal FALTANTE del vicio 7) + abstención honesta |
| 19 | triangulación | Horizon | SCM/ODE | T | por autorar — re-mapeo propuesto (0112, a validar): **convergent multi-test** (raro en modelos: 6-13%, tier A) |
| 20 | revelación secuencial | causal-cliente | SCM | T | por autorar — re-mapeo propuesto (0112, a validar): vicio 1 estructura **evidencia mid-way** (D4 nativo) |

Reglas: ningún [T] se certifica sin visibilidad de TODOS sus operadores + E0-probe con
headroom pre-registrado; cada [T] carga ≥2 coordenadas; los [C] son ~25% y ya están.

**Deudas**: consolidadas en la **Cola de trabajo única** (sección *Estado actual*, D1-D9) — esta
lista ya no se mantiene acá (una regla, una casa).

---

# Programa experimental — la escalera E1→E4 `[ESTABLE]`

> El plan de validación del proyecto (ex NORTH_STAR §6). De barato a caro; cada escalón con
> criterio de muerte explícito.

Principio rector: **no se testea la droga sin validar el ensayo.** Orden de barato a caro; cada pelfalla con criterio de muerte explícito; cada pelfalla publicable por sí solo. E2 y E3 son, además, **el sensor del loop maestro**: sus firmas dicen dónde parchear el juego.

La validación es una **pirámide**: los niveles L0–L2 (tests de contrato + sandbox red-team, escalera de verdades degradadas, protocolo de varianza del reward) validan la *maquinaria* y viven en `docs/reference/certificates.md` §13; la escalera E1→E4 de abajo valida el *constructo* (L3) y la *hipótesis* (L4–L5).

### E1 — Validez del instrumento (sin entrenar nada)

Decenas de mundos hechos a mano (dos formalismos) **+ mundos de control sin trampas** (para aislar el confound juicio-vs-ejecución); pasar por ellos modelos frontier existentes. Predicciones y chequeos que deben cumplirse:

1. El spread entre modelos respeta el orden conocido de capacidad de research.
2. **Manipulación de constructo**: el mismo modelo prompteado descuidado/overclaimer se desploma; prompteado metodológicamente prolijo, sube.
3. El score correlaciona con las firmas del trace (información por unidad de presupuesto, vía oráculo de valor).
4. **Mundos de control**: sin trampas, los modelos con buena ejecución convergen; el spread de juicio aparece solo con trampas. El perfil de juicio se reporta *condicional a la ejecución*, y la ejecución por separado (réplica interna del contraste ScienceWorld/DiscoveryWorld).
5. **Baseline humano**: 3–5 personas con formación en causal/estadística juegan ~10 mundos en el mismo REPL. Si los humanos competentes no superan a los frontier, el constructo está en duda.
6. **Validez convergente y discriminante**: los mismos modelos corridos en BoxingGym/DiscoveryBench/QRData — la correlación valida, la divergencia es hallazgo. Discriminante: el perfil debe agregar varianza más allá de un score de capacidad general (correlación parcial).
7. **Auditoría humana de baterías** (obligatoria): por cada mundo, leer los ~10 regímenes de mayor peso y verificar que son científicamente significativos — el único detector confiable de corrupción silenciosa de la relevancia a esta escala.

**Muerte**: si el eval no separa a un agente deliberadamente chapucero de uno cuidadoso, se frena todo — no hay instrumento.

### E2 — ¿Juicio o template?

RL con un modelo abierto mediano. La mirada NO va al score (sube seguro) sino a las **firmas**: ¿sube la información por experimento? ¿mejora la calibración (descomposición del proper score)? ¿aprende a abstenerse en lo no-identificable? ¿pesa priors adaptativamente al mover la perilla? ¿aparecen hipotetizar-discriminar-actualizar en los traces (backtracking, testeo de implicancias, pivoteo ante anomalías)? Diagnóstico de template: secuencias ritualizadas idénticas entre mundos, ganancia concentrada en motivos vistos.

**Muerte (parcial)**: score sube + firmas planas = máquina de templates; el loop maestro parchea curriculum/diversidad/brechas antes de seguir.

### E3 — Abstracción (decisivo y 100% interno — no necesita datos reales)

Entrenar reteniendo **familias enteras de operadores** y hasta **formalismos enteros** (entrenar en SCMs, testear en ODEs/colas). Lo convincente no es el efecto principal sino las dos **interacciones que nuestra propia teoría predice**:

1. El transfer escala con la **diversidad** de operadores de entrenamiento, no con la cantidad de mundos (la memorización predice lo contrario).
2. Las firmas de juicio emergen solo cuando presupuesto/complejidad es ajustado.

**Muerte**: sin transfer entre familias retenidas tras esfuerzo honesto en diversidad → la hipótesis de habilidad abstracta está muerta; queda un benchmark, no un método de entrenamiento. Se dice sin vergüenza.

### E4 — Sim2real (el titular)

- **Eval primario**: pares **observacional→experimento** — datasets observacionales reales cuya verdad la zanjó después un experimento aleatorizado (canónico: un análisis observacional revertido por un experimento posterior; curar casos oscuros y experimentos posteriores al cutoff, renovables en el tiempo). Secundario: predicción de replicación (SCORE / Replication Markets).
- **Anti-memorización**: delta **con-datos vs sin-datos** — si predice el experimento aleatorizado sin mirar el dataset, es memoria; importa cuánto gana por analizar.
- **Controles (cómputo igualado)**: (a) modelo base; (b) RL sobre math/código — el contrafáctico honesto de qué haría un lab con esas GPUs; (c) **ablación del ingrediente activo**: los mismos mundos con reward naive de preguntas fijas estilo v1.5.
- **Puente sin costura**: el agente investiga el dataset observacional real *en el mismo harness* (una fuente, presupuesto) y entrega su maqueta como siempre; predecir el experimento aleatorizado = **consultar la maqueta en el régimen del ensayo**. Cero mismatch de formato entre entrenamiento y demo.

**El número que decide todo**: el delta en obs→experimento contra el control de cómputo igualado.

### Notas de honestidad sobre la prueba misma

- Un nulo a escala chica (ej. 8B) es evidencia débil: el juicio podría "prender" a cierta escala. Mitigación: E1 ya da señal con frontiers sin entrenar; versión intermedia barata: experiencia in-context sobre mundos (sin tocar pesos) como sonda de transfer.
- Un positivo a escala chica con los controles bien hechos ya es enorme.
- Precedente a favor de E2: el RL de matemática con reward de outcome puro hizo emerger verificación y backtracking sin pedirlos; nuestro reward es más denso que un binario.
