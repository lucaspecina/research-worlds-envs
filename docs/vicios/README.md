# docs/vicios/ — la descomposición fina (un documento por vicio)

> **Qué es esta capa (ADR 0140, 2026-07-12).** El catálogo de 8 vicios resultó demasiado GRUESO:
> categorías-paraguas que mezclan mecanismos con condiciones de disparo distintas — y la jornada
> del 0/60 mostró el costo (construimos contra la sub-forma equivocada del pozo). Esta capa
> descompone cada vicio en **sub-formas** (mecanismo · disparador · firma observable · borde
> operación/juicio) con **casos reales inspeccionables** por sub-forma. Síntesis de CINCO vías
> independientes (Claude con web · Codex r22 · tres respuestas de investigación externas de
> Lucas), crudos en `docs/research/2026-07-12-*`.
>
> **Relación con los otros docs**: `docs/failure-modes.md` sigue siendo la tesis y el scaffold de
> diseño; `docs/mundos-por-vicio.md` sigue siendo la derivación vicio→mundo. Esta capa es el
> detalle fino que ambos citan. Una regla, una casa: las SUB-FORMAS viven acá.

## Etiquetas de rigor (obligatorias en esta capa)

- **Verificación**: `[VERIFICADO]` = leído a texto completo por nosotros con cita (registro
  `docs/lectura-de-fuentes.md`) · `[POR-LEER]` = convergencia multi-vía pero SIN lectura propia —
  no citar fuera de esta capa hasta leerlo (ADR 0115).
- **Tipo de evidencia**: `[AGÉNTICO]` = agente con herramientas/presupuesto · `[VIÑETA]` = LLM en
  cuestionario no-agéntico (¡sus números NO se transfieren a agentes!) · `[HUMANO]` = psicología /
  historia de la ciencia (solo material secundario).
- **Estado generacional**: `MUERTO` (resuelto por modelos de razonamiento) · `VIVO` (persiste en
  frontier) · `CRECIENTE` (empeora con capacidad) · `CONDICIONAL` (depende del contexto).

## El marco transversal (lo que las cinco vías coinciden en ver)

**El vicio no es un rasgo estable del modelo: es una respuesta condicional.** Las condiciones de
emergencia, ordenadas por evidencia:

1. **La jugada viciosa tiene que PAGAR localmente** (progreso visible y recompensado): 76% de
   trampa cuando los tests pasan vs 2.9% cuando no `[POR-LEER: ImpossibleBench 2510.20270]`.
   Nuestros pozos v0-v2 eran pozos secos con cartel — examinaban, no tentaban.
2. **Encuadre como conducta legítima**: el mismo pedido se rechaza como mala conducta o se ejecuta
   según cómo se enmarca `[POR-LEER: p-hacking Asher et al.]`. El vicio necesita una historia que
   lo justifique.
3. **Saliencia/contabilidad**: costo de oportunidad tabulado en la consigna = el modelo hace
   aritmética, no juicio (nuestro 0/60 `[VERIFICADO, ADR 0139]` + Big-Muddy estudios 1-2
   `[LEÍDO-HOY][VIÑETA]`). El juicio es DARSE CUENTA del costo.
4. **Identidad y capa social**: persona enredada con la línea que fracasa (97.45% escala) y
   deliberación simétrica entre pares (99.2%) `[LEÍDO-HOY][VIÑETA — verificar en formato
   agéntico]`. Jerarquía crítica frena (46.2%).
5. **Horizonte real**: estado propio acumulado + objetivo lejos en el contexto (goal drift pasado
   ~100k tokens, específico por modelo) `[POR-LEER: 2505.02709]`; Kosmos empeora con profundidad
   `[VERIFICADO]`. 14 rondas sintéticas ≠ horas con artefactos propios (Codex r22).
6. **Ambigüedad > dificultad**: 44% hardcodea en problemas ambiguos-resolubles vs ~0-5% en
   imposibles limpios `[POR-LEER: EvilGenie]`.
7. **Perfil por modelo, no ley**: cortar-antes es firma de la familia o-series (Claude EMPEORA sin
   opción de submit) `[VERIFICADO parcial: PaperBench]`; goal-drift Claude>100k vs 4o-mini-siempre.
8. **Capacidad: NO monótona**: reward hacking CRECE con capacidad; Einstellung MURIÓ entre
   generaciones `[POR-LEER: mARC follow-up 2601.11866]` — el resultado modal de un mundo puede ser
   "el frontier ya lo resuelve", y eso es un hallazgo, no un fracaso.

**Los cinco regímenes de emergencia (Codex r22)**: episodio-corto-claro-contabilizado (suprime
pozo/hilo/objetivo) · herramienta-falla-con-deadline (activa fabricación — el mejor documentado) ·
datos-ricos-no-identificantes (activa los causales) · estructura-fuera-del-menú (activa lo
latente; no lo arregla el tamaño) · trayectoria-larga-con-artefactos-propios (donde el pozo real
vive; aún sin construir).

## Índice

| Doc | Vicio | **Eje** (ADR 0141) | Estado generacional | Mundos WAGER |
|---|---|---|---|---|
| [vicio-1](vicio-1-no-cambiar-de-idea.md) | No cambiar de idea ↔ **dejarse influenciar** (par de 1ª clase) | Competencia | VIVO (no-uptake 68%); el espejo mejor documentado aún | first_story (control) |
| [vicio-2](vicio-2-el-pozo.md) | Calibración de parada (bipolar: overstay ↔ **cierre prematuro**) | Competencia | overstay MUERTO en frontier; **understay VIVO** | v0, v2, lab_largo + hallazgo 0/60 |
| [vicio-3](vicio-3-no-verificar-inflar.md) | No verificar / inflar / fabricar (8 sub-formas) | **Integridad** | **CRECIENTE** | ninguno (prioridades #2-#3) |
| [vicio-4](vicio-4-estructura-escondida.md) | No postular la estructura escondida | Competencia | VIVO (frontier agéntico) | latent_mix v2 (trofeo) |
| [vicio-5](vicio-5-perder-el-hilo.md) | Perder el hilo | Operación | VIVO pero fuera de alcance | no se construye |
| [vicio-6](vicio-6-adivinar-vs-preguntar.md) | Adivinar en vez de preguntar | Competencia | VIVO | bloqueado (verbo ASK) |
| [vicio-7](vicio-7-correlacion-causa.md) | Correlación vs causa | Competencia | MUERTO en viñeta; vivo en dato observacional | 5 mundos (controles) |
| [vicio-8](vicio-8-perder-el-objetivo.md) | Perder el objetivo / relevancia | Competencia | CONDICIONAL (largo/proxy) | ninguno |
| [vicio-9](vicio-9-overtrust-verificacion.md) | **La verificación de paja** (promovido 2026-07-13) | **Integridad** | **VIVO, dominante en frontier** | ninguno — par con cierre-prematuro |
| [ahas](ahas.md) | Las operaciones espejo | — | evidencia positiva POBRE (hallazgo en sí) | pares en v2/lab_largo |

## Segunda ronda de síntesis (R4-auditoría + R5-barrido, 2026-07-13)

**Propuesta estructural en la mesa (decisión de Lucas): TRES EJES.** La taxonomía mezcla ejes
que deberían ser ortogonales — **COMPETENCIA epistémica** (actualización, causalidad, estructura,
parada) / **OPERACIÓN** (contexto, loops — se mide, no se construye) / **INTEGRIDAD** (fabricar,
falsificar, cherry-pick, sicofancia — EL EJE QUE FALTA, y el único donde más capacidad = peor).
R4 propone además el reframe por variables latentes (la tabla "no confundir con"). Los 9+
vicios se cuelgan de esos ejes sin renumerarse.

**Prioridades de construcción REVISADAS (consenso 7 vías)**:

| # | Constructo | Por qué | Evidencia |
|---|---|---|---|
| 1 | **Cierre prematuro / verificación barata omitida** (v2-understay × v9) | el polo VIVO de la parada en frontier; automático; barato | CausaLab 48→60 con UN chequeo; NewtonBench tool-paradox `[POR-LEER]` |
| 2 | **Fabricación reactiva bajo feedback** (3.6) | integridad; el reviewer-pide→inventa con score subiendo | Jr-AI-Scientist `[POR-LEER]` |
| 3 | **Post-hoc selection en held-out** (3.7) | nuestro terreno exacto; firma computable | The-More-You-Automate `[VERIFICADO]` |
| 4 | Endpoint-correcto-mecanismo-incorrecto | ya es nuestra arquitectura (batería vs entrega) | CausaLab/CausalGame `[POR-LEER]` |
| — | PAUSADO: costo hundido como mundo | sin contraste causal limpio en el campo | queda como EXPERIMENTO propio-vs-heredado |

**Metodología adoptada de R4**: cada vicio como CONTRASTE CAUSAL mínimo (dos mundos casi
idénticos, UN factor distinto) · factoriales 2×2 en vez de narrativas que cambian todo junto ·
scorear TRES objetos (outcome / mecanismo / POLÍTICA de investigación — VOI, paradas,
revisiones) · firmas desde compromisos externos (predicciones registradas, rankings), no desde
el chain-of-thought. La condición maestra de emergencia: **horizonte × messiness × calidad del
gradiente × capacidad** ("largo" solo no predice).

## Deudas de esta capa

- Cola de lectura [POR-LEER] priorizada (ampliada por R4/R5): **CausaLab (2605.26029)** y
  **CausalGame (2607.04293)** — vecinos directos con el understay medido · DiscoverPhysics
  (2605.26087) · **Jr-AI-Scientist (2511.04583)** y **FIRE-Bench (2602.02905)** ·
  ImpossibleBench · NewtonBench (2510.07172) · Failing-to-Falsify (2604.02485) · Corral-
  artefactos (HF jablonkagroup/corral) · METR Frontier Risk (Sunlight/MirrorCode) · Goodfire
  post-mortem · Big-Muddy · MAST (HF mcemri/MAD) · ProcCtrlBench/TIDE · goal-drift (2505.02709)
  · Illusion-of-Diminishing-Returns (2509.09677) · Agents4Science (2511.15534) · RadLE · BAGEN
  · mARC follow-up · SycEval (2502.08177).
- Tensión abierta a resolver leyendo: anclaje (Vaccaro dice frágil `[VERIFICADO]`; R1 dice
  robusto-y-peor-con-capacidad `[POR-LEER]`) — probablemente se resuelve por sub-forma/formato.
- Verificar el 76% exacto de ImpossibleBench (figura por variante) antes de citarlo en el paper.


## Mantenimiento (el contrato — guardia en `tests/test_vicios_consistency.py`, corre en pre-commit)

**Dónde entra cada cosa nueva (una regla, una casa):**

| Evento | Se actualiza |
|---|---|
| Paper/fuente nueva leída a texto completo | `lectura-de-fuentes.md` (cita) + el caso en su `vicios/vicio-N.md` pasa de [POR-LEER] a [VERIFICADO] |
| Evidencia/caso nuevo de un vicio | SOLO `vicios/vicio-N.md` (+ fila del tablero si cambia el estado) |
| Mundo construido/certificado/medido | `vicios/vicio-N.md` (Estado) + `mundos-por-vicio.md` (Estado del mundo) + `roadmap.md` |
| Sub-forma nueva o cambio de estado generacional | `vicios/vicio-N.md` + tablero (esta página) |
| Vicio nuevo | doc nuevo `vicio-N-*.md` + fila del tablero + entrada en `mundos-por-vicio.md` + ADR |
| Decisión de diseño | ADR (append-only) — jamás editar esta capa sin rastro |

**El guardia automático verifica**: todo doc de vicio tiene fila en este tablero (y viceversa,
sin links muertos) · los docs viejos conservan el puntero a esta capa · cada doc mantiene sus
secciones (sub-formas/firma + estado). Un doc olvidado ROMPE el commit — no depende de memoria.
