# NOTAS p2 — ModelSMC (2602.18266, Macke lab / Tübingen, ICML 2026) — LEÍDO COMPLETO (cuerpo 1-1043 + apéndice mapeado + prompts F.4/H leídos)

## Qué es
Recasta el "descubrimiento automático de modelos" (agente LLM que propone/revisa código de un
simulador para explicar datos) como INFERENCIA PROBABILÍSTICA: muestrear de p(m|xo) = posterior
sobre modelos-programa que explican los datos. Instanciado como ModelSMC (Sequential Monte Carlo):
una POBLACIÓN de N "partículas" = modelos-código, iteradas por resample→propagate(LLM)→weight(likelihood).
Backbone Claude Sonnet 4.6 (también GPT-5-mini). ICML 2026.

## Diferencia clave con el resto (y con AUTOCOG)
- El peso de cada modelo = LIKELIHOOD MARGINAL p(xo|m) (integra sobre parámetros θ), NO una distancia
  ad-hoc (MSE/MMD/Wasserstein). "the weighting step is derived from the model posterior... a
  principled probabilistic objective rather than relying on alternative discrepancy measures".
- MARGINALIZA sobre parámetros en vez de optimizar un punto → menos sensible a incertidumbre de
  params. Likelihood estimada sin entrenar (TabPFN, foundation model tabular = NLE training-free).
- Devuelve una DISTRIBUCIÓN (población pesada) de modelos, no un ganador único → "reveals which
  hypotheses concentrate posterior mass, which remain uncertain, and which are non-identifiable".

## Citas / hechos clave
- Tarea: dado datos xo generados por m* bajo contextos c, inferir un modelo-programa m. "A model m
  is an algorithm written in code that probabilistically maps context c and parameters θ to data x".
  = NUESTRA submission EXACTA (programa generativo que mapea régimen→datos).
- 3 sistemas REALES: SIR (epidemia sintética), riñón/aldosterona (R, farmacología QSP), Hodgkin-Huxley
  (neurona). Datos EXTREMADAMENTE escasos (riñón: 4 escenarios × 5 puntos temporales).
- Misspecificación estructural DELIBERADA como diseño de tarea: "We intentionally replace the
  aldosterone mechanism with a constant term, thereby introducing a targeted structural
  misspecification. ModelSMC is tasked with inferring the missing regulatory dynamics from the data."
  → RECETA de cómo construir un mundo: tomás un simulador real correcto, le ROMPÉS una pieza a
  propósito, y el agente tiene que recuperar la pieza faltante.
- El posterior como DIAGNÓSTICO de identificabilidad: "posterior mass serves as a diagnostic:
  low-weight regions indicate genuine structural mismatch, while clusters of high-probability models
  reveal symmetries and ambiguities that are invisible to single-model discovery." En HH: mezcla de
  canales queda NO-identificable, pero la conclusión robusta (agregar corriente lenta IM) sí se sostiene.
- Análisis del posterior por TAXONOMÍA (3 pasos, con LLM): muestra estratificada de partículas →
  extrae descripciones → taxonomía de 11 subtipos → clasifica las 1445 partículas → compara pesos por
  subtipo. IM primero en 9/10 seeds. = medir-para-DESCRIBIR (nuestra distinción), y un patrón de
  "auditar la población de soluciones" que nos sirve para el panel conductual de la fábrica.
- Validación LLM-free: en espacio finito (20 modelos gaussianos) concentra en el verdadero (tope ~80%
  por el kernel) → aísla que el motor de inferencia FUNCIONA, separado del LLM. = nuestro certificado
  de recuperabilidad, hecho como control aislado.
- Ablaciones (Table 2): likelihood marginal > MSE weights; N=5,K=150 (profundidad) mejor que
  N=150,K=5 (diversidad) a presupuesto fijo; robusto al backbone (GPT-5-mini ok) y al prompt reducido.
- El PROMPT de tarea (App H, HH) es una PLANTILLA con: OBJECTIVE, BASE MODEL, EXTENSIBILITY (slots
  X1/X2 con params tuneables), EVALUATION METRICS (7 summary stats), DATA CONTEXT con "important data
  characteristics" que ACOTAN el espacio ("avoid channels that produce bursting"). + "BEGIN EDITABLE
  SECTION (only modify within this block)" → el generador solo edita un bloque; el resto congelado.
  → es LITERAL la anatomía de una consigna de fábrica con andamiaje que acota sin filtrar la respuesta.
- Límites confesados: caro (simulación+likelihood repetidas); likelihood surrogate puede sesgar bajo
  misspecificación; cuello = capacidad del LLM de proponer estructuras relevantes; los modelos son
  "programas de alta dimensión sin geometría explícita" (no hay noción de similaridad entre modelos).

## Relevancia WAGER (para CÓMO CONSTRUIR MUNDOS)
1. RECETA DE CONSTRUCCIÓN por rotura deliberada: tomar un simulador REAL validado (SIR, farmacología,
   HH) y ROMPERLE una pieza estructural → el mundo es "recuperá lo que saqué". Escala la fábrica con
   REALIDAD como autora (nuestra doctrina "la realidad como autora de las trampas") sin inventar
   mecanismos: los mecanismos vetados salen de simuladores publicados.
2. LIKELIHOOD MARGINAL como scoring: refuerza (con teoría) por qué marginalizar params > punto, y por
   qué una distancia FIJA es ciega (coincide con AUTOCOG y con nuestro red-team #5). Candidato a
   revisar nuestro scorer: ¿el energy-distance es una distancia fija con puntos ciegos que una
   likelihood marginal no tendría? (no cambiar el reward path sin discutir — solo anotar).
3. NO-IDENTIFICABILIDAD como FEATURE, no bug: su posterior expone qué NO se puede distinguir con los
   datos. Es EXACTAMENTE nuestro vicio 7 sub-estructura "intervenir-o-fallar" + la abstención honesta
   (OQ). Un mundo donde la respuesta correcta es "estas dos estructuras son indistinguibles con lo
   observado; hay que intervenir/abstenerse" tiene aquí su vara: el buen agente devuelve una
   DISTRIBUCIÓN (mezcla de modelos rivales con pesos), no un punto — y nuestro contrato YA permite
   entregar mezclas con pesos. Sinergia fuerte.
4. Anatomía de consigna de fábrica (App H): OBJECTIVE + BASE MODEL + EXTENSIBILITY (slots) + METRICS +
   DATA CONTEXT que acota + EDITABLE SECTION. Modelo directo para la consigna del proto-designer:
   andamiaje que restringe el espacio SIN soplar la respuesta.
5. Depth-vs-diversity a presupuesto fijo (N=5,K=150 > N=150,K=5): dato para nuestro micro-batch y para
   el diseño del generador (más iteraciones de refinamiento sobre pocos > muchos de un tiro).
6. Es competencia/vecindad honesta: mismo formato de entrega (simulador en código), mismo dominio
   (sistemas reales), evaluación por likelihood. Diferencia: ellos INFIEREN el modelo con SMC+LLM (el
   sistema ES el descubridor); nosotros hacemos que un AGENTE investigue y medimos SU juicio. Su
   ModelSMC podría ser un RIVAL fuerte / baseline destructor (el "pipeline sin juicio" que resuelve
   por búsqueda poblacional) — anotarlo para red-team #2/#20.

## Diferencia entre los dos papers (para la síntesis)
- AUTOCOG: loop cerrado con HUMANOS, adversarial (2 teorías compiten), foco en DISEÑO EXPERIMENTAL
  discriminante y en descubrir teorías nuevas confirmadas pre-registro. Métrica ADAPTATIVA propuesta
  por LLM (y demuestra que la fija es ciega).
- ModelSMC: inferencia poblacional bayesiana sobre PROGRAMAS, foco en el POSTERIOR (identificabilidad,
  no-identificabilidad, familias de hipótesis). Likelihood marginal principiado. Datos fijos (no
  cierra loop experimental).
- JUNTOS enmarcan las dos mitades de lo que hacemos: AUTOCOG = cómo diseñar el experimento
  discriminante (el lado activo/adquisición); ModelSMC = cómo puntuar un modelo-programa contra datos
  con incertidumbre (el lado del reward/entrega). Los dos usan NUESTRO formato: entrega = simulador
  ejecutable, evaluación = comportamiento generativo, no fitting.
