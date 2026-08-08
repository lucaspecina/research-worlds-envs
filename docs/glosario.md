# Glosario — los nombres de la casa, en llano

> Chuleta de una página (pedido de Lucas, 2026-08-07). Si un término nuevo entra al proyecto,
> entra acá con una línea. Para el detalle de cada cosa: el link de su línea.

## El proyecto en una frase

Construimos mundos simulados con una verdad escondida y ponemos agentes LLM a investigarlos,
para medir — sin jueces LLM — dónde exactamente se les rompe el proceso de descubrir.

## Las piezas del juego

- **Mundo**: un programa que genera datos con una verdad escondida adentro. El agente nunca ve
  el código — solo compra datos y entrega su propio modelo.
- **Gemelo**: el mundo espejo donde la estructura escondida NO está. Todo se mide de a pares:
  el que ve fantasmas pierde en el gemelo; el que no ve nada pierde en el principal.
- **Encargo (brief)**: la consigna que lee el agente ("sos analista de calidad…"). Se escribe a
  ciegas de la evaluación para no regalar pistas.
- **Episodio**: una partida completa: leer el encargo → comprar datos → experimentar → entregar
  el modelo. Con presupuesto finito.
- **Perillas (regime del episodio)**: los diales que el agente puede fijar al experimentar (en
  count_mix: `speed`, `repeats_per_unit`). ⚠️ No confundir con el OPERADOR "régimen oculto"
  (abajo) — colisión de nombres heredada de la plataforma.
- **Seeds quemadas**: cada corrida usa un número de semilla nuevo, anotado para siempre; nunca
  se re-corre "hasta que dé".

## Saltos y operadores

- **Refinamiento**: ajustar los NÚMEROS de un modelo sin cambiarle la forma.
- **Salto**: cambiarle la FORMA al modelo (qué variables existen, cómo se conectan). Lo que
  medimos. **Distinción que manda (Lucas, 2026-08-07): GENERAR el candidato cuando nada lo
  dicta (= creatividad, la vara del programa) ≠ ACEPTARLO cuando la evidencia lo grita (= 
  revisión de creencias, vicio 1).** Un mundo mide creatividad solo si el candidato tiene que
  NACER del agente.
- **Operador (de salto)**: cada TIPO de cambio de forma. La lista 10+1 — **contada con
  historia y fuentes en [el libro de los saltos](saltos.md)**;
  [justificación formal](research/2026-08-05-fundamentos-taxonomia-de-saltos.md): 1 entidad oculta ·
  2 grupos escondidos (count_mix) · 3 régimen/fase oculto (dos leyes con umbral) · 4 geometría ·
  5 unificación · 6 invariante promovido (simetría) · 7 proceso del observador · 8 realimentación
  oculta · 9 conservación/cuantización · 10 memoria oculta · 11 transferencia estructural
  (analogía tipo Darwin).
- **Menú de hipótesis**: las familias de modelos que el agente considera de entrada. **El
  hallazgo central hasta ahora: la juntura rota es que el candidato correcto no ENTRA al menú**
  — todo lo demás (comprar datos, ajustar, chequear) lo hacen bien.
- **Juntura**: eslabón específico de la cadena de investigar (comprar → mirar → postular →
  testear → entregar). Medimos cuál se rompe, no "si es bueno o malo".

## La escalera de ayudas (etiquetas del Explorer)

- **no**: solo el encargo. — **poca**: pista vaga vieja ("puede haber subpoblaciones").
- **media (concepto)**: "considerá que los lotes vengan en unos pocos tipos" — dice QUÉ buscar.
- **mucha (receta)**: "probá una mezcla finita de 2-3 grupos" — dice QUÉ HERRAMIENTA usar.
- **procedimiento**: "ajustá ≥2 familias y compará" — ordena el ACTO, sin contenido.
  Resultado clave: no/0-de-9 · concepto rescata a gpt 4/4 · receta rescata a DeepSeek 3/3 ·
  procedimiento 0/3 (comparan… dentro de su menú).

## Métricas (las columnas del Explorer)

- **S_valley_fuerte** (mundo principal, 0→1): ¿capturó los grupos escondidos? 0 = igual que el
  mejor rival continuo, 1 = igual que la verdad. LA vara del salto.
- **S_clean** (gemelo, 0→1): limpieza — qué tan cerca de la verdad simple quedó.
- **espurio** (gemelo): ¿inventó grupos que no existen? (bandera sí/no).
- **F_mean**: ¿clavó el promedio? (chequeo básico, casi siempre ≈1).
- **ICC**: persistencia por lote — cuánto se parecen mediciones del mismo lote.
- **R**: parecido global de los datos generados (0→1). ⚠️ Deuda conocida: hoy castiga al que
  descubre los grupos; no usarla para rankear salto.
- **Censura**: corrida inválida (se quedó sin tokens, no entregó código) — se reporta, no cuenta
  ni a favor ni en contra.

## Reglas de juego de la investigación

- **Certificados**: pruebas automáticas que un mundo pasa antes de usarse — necesidad (el salto
  hace falta de verdad contra un rival fuerte), alcanzabilidad (un robot mecánico puede lograrlo
  con los datos comprables), gemelo (bilateral), anti-memorización.
- **Rival fuerte**: el mejor modelo SIN el salto (en count_mix: gamma continua con persistencia).
  Toda vara se ancla contra él, no contra un rival de paja.
- **Pre-registro**: predicciones y reglas de decisión escritas y commiteadas ANTES de correr.
  Una-frase-una-corrida: las ayudas se congelan textualmente; no se escalan sobre la marcha.
- **Descubrimiento vs confirmación** (fases que no se mezclan): ahora estamos en descubrimiento
  (barato, exploratorio); confirmación = pregunta congelada + seeds frescas + modelos held-out.
- **Cero-LLM en el reward**: ningún juez LLM toca el puntaje, jamás.

## Los vicios (catálogo, por número — [tablero](vicios/README.md))

1 calibración de creencias (rigidez / influenciable) · 2 calibración de parada (cierre
prematuro↔pozo) · 3 no verificar / fabricar · 4 **no postular la estructura escondida** (el de
count_mix) · 5 perder el hilo · 6 adivinar en vez de preguntar · 7 correlación vs causa ·
8 perder el objetivo · 9 **verificación de paja** (testea con tests que no pueden fallar — el
del "teatro de comparación"). **Ahas**: las operaciones espejo (notar la anomalía, pivotar a
tiempo, pedir el dato que discrimina) — siempre medidas de a pares con su vicio.

## Dónde vive cada cosa

Estado y próximo paso: [roadmap](roadmap.md) · hallazgos: [índice](research/README.md) ·
evidencia de vicios: [docs/vicios/](vicios/README.md) · cómo se mide: [como-medimos](como-medimos.md) ·
mundos por vicio: [derivación](mundos-por-vicio.md) · corridas navegables: `explorer.command`.
