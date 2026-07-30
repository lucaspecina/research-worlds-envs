# Las operaciones de aha (los espejos) — y el hallazgo incómodo sobre su evidencia

> Etiquetas y marco: ver [README](README.md). Doctrina intacta: SIEMPRE de a pares (el vicio y
> el aha son polos de la misma operación; el par impide ganar con un reflejo fijo).

## El hallazgo transversal (Codex r22, confirmado por las vías externas)

**La evidencia positiva es mucho más pobre que la negativa**: los papers documentan agentes
fallando; casi ninguno identifica trazas reproducibles de un salto EXITOSO autónomo y
verificable. Consecuencia doble: (a) medir los ahas es terreno más virgen aún que medir vicios
— nuestra oportunidad; (b) los pares no pueden calibrarse solo con literatura: hay que
generarlos en casa (robots + protocolos).

## A1 — Notar la anomalía (y jerarquizarla)

- **A1.1 Detectar el residuo**: VIVO en frontier — nuestras autopsias (15/16 descubren la
  estructura) `[VERIFICADO propio]`; las trazas de anoche (gpt-5.4 detecta explícito que afinar
  el ripple vale menos que cubrir líneas) `[VERIFICADO propio]`; motivos productivos en Corral
  (raros pero existen) `[VERIFICADO]`.
- **A1.2 Juzgar que la anomalía es CENTRAL** (vs ruido periférico): evidencia agéntica directa
  INSUFICIENTE (Codex). Estructura humana: Dunbar (centralidad×timing) `[HUMANO]`. WAGER no
  tiene aún el par anomalía-real/ruido validado — hueco propio.
- **A1.3 Promoverla a hipótesis nueva**: **el cuello real**. Contraevidencia nuestra: el trofeo
  (0/10 promovieron la anomalía a composición oculta) `[VERIFICADO propio]`; DiscoverPhysics
  (fallan justo donde hay que postular lo latente) `[VERIFICADO — leído 2026-07-13]`; "LLMs can't jump"
  `[VERIFICADO]` (abducción como el faltante estructural; parche-Vulcano como la jugada
  perdedora). No se conocen 2 casos verificables de agentes logrando esto autónomo.

## A2 — Pivotear (creencia / método / línea)

- **A2.1 Pivot de creencia**: VIVO en frontier con evidencia propia — gpt-5.4 rompe la primera
  historia rutinariamente (first_story E0/vicio-vivo) `[VERIFICADO propio]`; revisión/reranking
  en los motivos productivos de Corral (raros) `[VERIFICADO]`.
- **A2.2 Pivot de línea/asignación**: NUESTRO dato es de los pocos que existen — el 0/60 ES
  evidencia positiva masiva de pivot correcto bajo contabilidad visible (60 trazas). El campo
  no tiene esto medido; el paper puede darlo vuelta como hallazgo de aha.
- **Gemelo del pivot**: pivotear-de-más (abandonar líneas vivas — paranoia). Documentado por
  nosotros como riesgo de diseño (flogisto); DeltaLogic `[POR-LEER]` lo ve en viñeta
  (sobre-flip).

## A3 — Síntesis / unificación (y su gemelo, la apofenia)

- Chen/Zhao/Cohan `[VERIFICADO]`: el reflejo "integrá dos cosas" domina la ideación LLM
  (bridge 47-64% vs 12% humano; el thinking lo AGRAVA); las movidas humanas evitadas:
  replace / decouple / formalize — decouple es literalmente nuestra familia causal.
- Par vigente: unificación-real ↔ apofenia. El mundo consiliencia (dos anomalías sembradas
  con causa común) sigue en cartera; el scoring ya la premia.

## A4 — Pedir el dato que discrimina (el aha del diseño experimental)

- BED-LLM `[VERIFICADO]` (45%→93% adaptando la pregunta); Mundo B diseñado (bloqueado con v6).
- Nuestro robot-cuidadoso lo instancia (menú discriminante completo) `[VERIFICADO propio]`.

## El caso Einstein releído (2026-07-30) — refinamientos del par (ADR 0150)

Relectura completa de ["LLMs can't jump"](https://openreview.net/forum?id=klU4737opt) (citas en
[lectura-de-fuentes](../lectura-de-fuentes.md)):

- **A1 se afila**: el salto histórico NO detectó una anomalía nueva — RE-JERARQUIZÓ el dato más
  banal y verificado (la caída igual de los cuerpos, 300 años a la vista); la anomalía famosa
  (Mercurio) fue certificado de aterrizaje, no motor. Diseño: la clave vive en lo
  obvio-que-nadie-mira; lo llamativo, de señuelo.
- **Cara nueva del par: auditar el TEST.** El "error fatal" de 1913 (descartar el tensor correcto
  por un chequeo mal aplicado) es el espejo de la terquedad: obedecer ciego al verificador también
  es vicio. Candidato: mundo/rama donde el chequeo oficial tiene un supuesto roto y la jugada
  ganadora es dudar del instrumento, no del candidato.
- **A2 con autoría**: el pivote de 1915 fue volver a la intuición PROPIA descartada. En el
  checkpoint de pivote, medir QUÉ suelta y qué retiene: soltar la obra reteniendo el criterio =
  aha; soltar el criterio reteniendo la obra = vicio 1.
- **La terquedad alimenta ambos polos**: Einstein terco con ideales de forma (unificación),
  desprendido con productos (tiró el Entwurf); el vicio 1 es la configuración inversa.

## Consecuencia de diseño

Los mundos de aha deben generar su PROPIA evidencia positiva (robots que logran el salto +
protocolos que detectan cuándo un modelo real lo logra), porque la literatura no la trae. El
par mínimo por mundo sigue siendo obligatorio — con el agregado (jornada 0/60) de que el
"éxito del examen" para frontier puede ser evidencia de aha, no solo ausencia de vicio.

**Requisito nuevo (relectura 2026-07-30, ADR 0150): el premio del salto vive en la
EXTRAPOLACIÓN.** El camino real es anti-MDL (la complejidad sube antes de bajar): si el mundo paga
por fit del régimen visitado, el parche-Vulcano gana siempre. El pago del salto debe vivir en el
régimen NO visitado (held-out de régimen, computable cero-LLM desde la verdad). El **contrato de
resolubilidad** ("certificar el paisaje, no el camino"; espec en ADR 0150) queda diseñado y
**DIFERIDO** por orden de Lucas: primero reproducir los failure modes; se retoma al abrir mundos
de aha.
