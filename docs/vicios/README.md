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

| Doc | Vicio | Estado generacional (global) | Mundos WAGER |
|---|---|---|---|
| [vicio-1](vicio-1-no-cambiar-de-idea.md) | No cambiar de idea ante la evidencia | VIVO (no-uptake 68%) con sub-formas muertas | first_story (control) |
| [vicio-2](vicio-2-el-pozo.md) | El pozo / no soltar | CONDICIONAL (identidad/social/largo) | v0, v2, lab_largo + hallazgo 0/60 |
| [vicio-3](vicio-3-no-verificar-inflar.md) | No verificar / inflar / fabricar | **CRECIENTE** | ninguno (prioridad #1) |
| [vicio-4](vicio-4-estructura-escondida.md) | No postular la estructura escondida | VIVO (frontier agéntico) | latent_mix v2 (trofeo) |
| [vicio-5](vicio-5-perder-el-hilo.md) | Perder el hilo (operación) | VIVO pero fuera de alcance | no se construye |
| [vicio-6](vicio-6-adivinar-vs-preguntar.md) | Adivinar en vez de preguntar | VIVO | bloqueado (verbo ASK) |
| [vicio-7](vicio-7-correlacion-causa.md) | Correlación vs causa | probablemente MUERTO en viñeta; vivo en dato observacional | 5 mundos (controles) |
| [vicio-8](vicio-8-perder-el-objetivo.md) | Perder el objetivo / relevancia | CONDICIONAL (largo/proxy) | ninguno |
| [vicio-9 CANDIDATO](vicio-9-overtrust-verificacion-CANDIDATO.md) | Over-trust en la verificación propia | **VIVO, dominante en frontier** | ninguno — **candidato a agregar (decisión de Lucas)** |
| [ahas](ahas.md) | Las operaciones espejo | evidencia positiva POBRE (hallazgo en sí) | pares en v2/lab_largo |

## Deudas de esta capa

- Cola de lectura [POR-LEER] priorizada: DiscoverPhysics (2605.26087, el vecino más cercano) ·
  ImpossibleBench · Corral-artefactos (HF jablonkagroup/corral) · Big-Muddy (verificar formato) ·
  MAST (HF mcemri/MAD, corpus minable) · ProcCtrlBench/TIDE (firmas robables) · goal-drift
  (2505.02709) · RadLE · BAGEN · mARC follow-up.
- Tensión abierta a resolver leyendo: anclaje (Vaccaro dice frágil `[VERIFICADO]`; R1 dice
  robusto-y-peor-con-capacidad `[POR-LEER]`) — probablemente se resuelve por sub-forma/formato.
- Verificar el 76% exacto de ImpossibleBench (figura por variante) antes de citarlo en el paper.
