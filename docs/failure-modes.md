# Failure modes del juicio investigativo — catálogo y scaffold de diseño

> **Documento vivo (ADR 0099).** El corazón del proyecto: de un failure mode DOCUMENTADO
> → a la especificación de un mundo que lo pone de manifiesto de forma PUNTUABLE. No es una
> lista de memoria — es un scaffold para *ir a la literatura con paciencia, razonar, y
> diseñar mundos de a uno*. Reemplaza al viejo `FAILURE_MODES.md` (disuelto en la
> reestructura) con la estructura que ganamos discutiendo. Precedente de disciplina:
> `docs/mundo-a-primera-historia.md`, `docs/proto-designer.md`.

---

## 0. La tesis en una frase

Medimos juicio investigativo construyendo mundos donde **cada vicio documentado es la jugada
perdedora** — la conducta se OBSERVA (firma de trace), jamás se premia; el mundo hace que el
vicio produzca un modelo final peor y el examen cero-LLM cobra la consecuencia. Cada failure
mode bien documentado que encontramos **es una especificación para un mundo**.

## 1. Qué ya sabemos (no arrancamos de cero)

- **El instrumento SÍ captura vicios, medidos** (no es aspiracional): comprar-evidencia-y-no-
  usarla (4/4 gpt bajo escasez), terminación apurada, **precisión fabricada** (declaró un σ
  que no midió; la nota se lo cobró), retirada a la arquitectura familiar (v2). Todo apareció
  con número en nuestros mundos.
- **Validez de constructo — señal positiva (ADR 0098)**: una pista DIRIGIDA al vicio
  específico restaura el puntaje SOLO donde el vicio vive (first_story escaso: mediana
  0.00→0.87) y ≈0 en el control → el instrumento separa juicio, con la métrica correcta
  (mediana + separar ceros de ejecución de ceros de juicio). Caveat: n=5, replicar.
- **El hallazgo que ordena el diseño**: **el vicio bite bajo PRESIÓN, no a presupuesto pleno.**
  gpt pivotea "de rutina" con plata holgada; se le cae el buen hábito cuando el recurso
  aprieta. → *el mundo tiene que CREAR la presión, no solo pedir un análisis prolijo.*

## 2. Principios de diseño (los que ganamos con dolor — no negociables)

1. **Consecuencia cobrada, conducta observada** (Ethos §2.1/2.6): el vicio es la jugada
   perdedora; la firma de trace diagnostica, nunca premia.
2. **Certificado de trampa necesaria** (ADR 0082): dos robots scripteados — el **vicioso**
   (comete el vicio con maestría en todo lo demás) debe quedar LEJOS del techo; el
   **cuidadoso** debe alcanzarlo. Si el cuidadoso no llega → trampa injusta, se descarta.
3. **La presión expone el vicio** (ADR 0098): escasez de presupuesto / tiempo / evidencia que
   llega tarde. Un vicio dormido a presupuesto pleno no se mide sin presión.
4. **Vicios TEMPORALES → mundos que se DESPLIEGAN**: "no actualizar ante evidencia nueva"
   necesita que HAYA evidencia nueva llegando (la maquinaria de eventos, D4/ADR 0083, casi sin
   usar). El énfasis correcto: *evidencia por etapas, no toda disponible de entrada.*
5. **Vicios de INSIGHT/creatividad → mundos donde INVENTÁS la estructura** (familia v2, nuestro
   mejor resultado): ganar exige formular una hipótesis estructural que nadie te dio, no calzar
   un modelo de librería.
6. **Entregable PUNTUABLE + cero-LLM**: el deliverable sigue siendo "predecí el comportamiento"
   (scoreable sin juez LLM). La fachada (línea de producción, etc.) es piel; la sustancia
   siempre es "descubrí el mecanismo oculto investigando".
7. **Altura de la trampa/pista**: se nombra la CONDUCTA, nunca la RESPUESTA. Test: un modelo
   que nunca vio el mundo, tras leer la pista, sigue sin saber la respuesta.

## 3. La taxonomía por DINÁMICA DE MUNDO (el organizador clave)

No agrupamos los vicios por su nombre psicológico sino **por la dinámica de mundo que los
fuerza a manifestarse de forma puntuable** — porque esa dinámica ES el diseño.

| familia | vicios que agrupa | dinámica de mundo que lo expone | scoring |
|---|---|---|---|
| **A. Actualización de creencias** | casarse con la 1ª hipótesis; no incorporar evidencia nueva; sesgo de confirmación; anclaje; conservadurismo bayesiano | **DESPLIEGUE**: evidencia contradictoria llega a mitad de camino (eventos sellados); la verdad puede driftear | predecir comportamiento post-actualización |
| **B. Atención / perseverancia** | rabbit holes; más-de-lo-mismo sin pivotear; no saber cuándo parar; perder de vista el objetivo | **DISTRACTOR + PRESIÓN**: pozo fascinante en un dato lateral que no paga, bajo presupuesto escaso | costo de oportunidad cobrado en el modelo final |
| **C. Verificación / rigor** | "verified" sin verificar; over-claims; **precisión fabricada**; perseguir lo significativo-pero-irrelevante | **RESPUESTA BARATA FALSA + verificación disponible**: la carnada de significancia; declarar un número sin medirlo se paga | |ΔF| de la cantidad no-verificada |
| **D. Representación / creatividad** | retirada a lo familiar; no inventar la estructura necesaria; sobre-simplificar | **INVENTAR LA ESTRUCTURA** (v2): el ganador formula una hipótesis latente/estructural | fidelidad al mecanismo que solo la estructura correcta reproduce |
| **E. Memoria / consistencia (largo plazo)** | perder restricciones; trabajo redundante; recuperación que se degrada en trayectorias largas | **HORIZONTE LARGO + restricción de enlace tardío** (declarada temprano, cobrada al final) | parcialmente límite del harness → se MIDE, no se diseña-en-contra |
| **F. Interacción / preguntar** | adivinar en vez de averiguar; no registrar info que llega a mitad de camino; saltear la verificación disponible | **CONSULTABLE + evidencia mid-way**: lo faltante tiene precio conocido y accesible | diferencia de suposición-vs-consulta |

## 4. El catálogo (seed inicial — a completar con la literatura)

Por cada vicio: fuente · cómo se manifiesta · dinámica (§3) · estado. **Las citas exactas se
verifican/completan minando papers (ver §5); lo de abajo es el seed de lo que ya sabemos.**

### A — Actualización de creencias
- **Fijación de hipótesis / sesgo de confirmación** — cog-sci clásico (Wason 2-4-6; Klayman &
  Ha, positive-test strategy): se busca evidencia que confirma, no que refuta. → mundo de
  despliegue con refutación que llega tarde. *Estado: parcial (first_story mide la 1ª-hipótesis
  a presupuesto pleno, pero el vicio no bite sin presión; con-noticia sin correr con modelos).*
- **No-actualización / conservadurismo** — updating bayesiano insuficiente (Edwards; base-rate
  neglect, Kahneman-Tversky): ante evidencia contraria, la creencia casi no se mueve. → eventos
  sellados. *Estado: maquinaria lista (D4), certificado de robots ✓ (0.0002 vs 0.989), sin
  correr con modelos.*
- **Anclaje** — Tversky & Kahneman: la primera estimación fija el resto. → primer dato sesgado.

### B — Atención / perseverancia
- **Rabbit holes / goal drift** — evals de agentes autónomos (METR y afines documentan
  degradación con el horizonte y pérdida del objetivo). → pozo-señuelo + presupuesto. *Estado:
  por diseñar (señuelo puro); la escasez ya la validamos como dial (#6).*
- **Parada prematura / satisficing** — Simon: se toma la primera solución "suficiente". →
  N-trampas con saciedad (hallar la 1ª satisface). *Estado: mundo 3 fue 2-trampas; saciedad
  reapareció bajo escasez.*

### C — Verificación / rigor
- **Over-claiming / "verified" sin verificar** — críticas a agentes-científicos (p.ej. AI
  Scientist) + evals de honestidad: producen plausible-pero-mal y lo reportan con seguridad. →
  la retórica ya vale cero (el examen corre el modelo). *Estado: cubierto por construcción.*
- **Precisión fabricada** — MEDIDO EN NUESTROS PROPIOS RUNS (fabricated_precision): declaró σ
  sin comprar réplicas. *Estado: capturado y priceado.*
- **Perseguir lo significativo-pero-irrelevante / p-hacking** — metaciencia / crisis de
  replicación (garden of forking paths, Gelman). → carnada de significancia (efecto chico-pero-
  claro vs grande-pero-ruidoso). *Estado: por diseñar; anfitrión natural = mundo ancho.*

### D — Representación / creatividad
- **Retirada a lo familiar / implementation drift** — evals de agentes de código (revierten a
  patrones conocidos). → la respuesta simple-familiar queda a mitad de tabla; solo la estructura
  verdadera llega arriba. *Estado: CONFIRMADO con solver real (v2 seed3, R=0.096).*
- **No inventar la estructura** — el lado generativo del research taste. → familia v2. *Estado:
  el trofeo; hacer MÁS de estos.*

### E — Memoria / consistencia
- **Pérdida de restricciones / contexto en trayectorias largas** — evals de horizonte largo. →
  restricción de enlace tardío + horizonte. *Estado: se MIDE como hallazgo (límite del solver),
  no se diseña-en-contra.*

### F — Interacción
- **Adivinar en vez de averiguar** — evals de agentes interactivos. → info faltante con precio
  accesible. *Estado: el inverso (comprar-y-no-usar) CONFIRMADO (#6); el directo por diseñar.*

## 4-bis. Corpus compilado (Lucas) — hallazgos CITADOS y CUANTIFICADOS

Recopilación de Lucas de fuentes reales (2025-2026). Lo que estas fuentes aportan de único:
**números** y una **metodología externa que valida nuestro enfoque**. Cada ítem → su familia
de §3.

**Cuantificados (los que dan la vara empírica)** — de un análisis por grafo epistémico
(arxiv 2604.18805 y afines) y de SciAgentGym:
- **Evidencia IGNORADA en el 68% de los traces** (A): ve un resultado que contradice su
  hipótesis y sigue como si nada.
- **Revisión de creencia refutada solo en el 26%** (A): ante evidencia contraria, casi nunca
  actualiza.
- **Error-signal blindness: 67%** repite exactamente la misma acción fallida sin cambiar nada
  (SciAgentGym) (A/F). Cascada: no detecta → no diagnostica → no pivotea → repite.
- **Convergent multi-test RARO** (~6-13% según modelo) (C): no triangula con tests
  independientes.
- **Degradación irreversible de resiliencia** (E): la recuperación de errores baja monótono en
  trayectorias largas (modelos débiles ~30%→~10% sin rebotar); los fuertes muestran
  Rise-Fall-Rise → **la resiliencia es entrenable** (implicación para E2).
- **<7% del presupuesto en detectar/reparar sus propios errores** (OSWorld-V2) (C/B); se hunden
  donde la tarea depende de **recuperar un estado oculto** (D — la familia v2).

**Vicios distintos que suman al catálogo (§4)**:
- **Analysis-decision disconnect** (F/nuevo): identifica correctamente el edge y aun así NO
  actúa (o dimensiona mal) — desconexión entre el módulo analítico y el de decisión (benchmark
  de apuestas por temporada). *No lo teníamos: el juicio correcto que no se traduce en acción.*
- **Sycophancy bajo presión** (C/F): si lo presionás, termina dando la respuesta que parecés
  querer aunque no esté justificada (Anthropic vibe-physics). *La presión no solo expone el
  vicio — puede CREAR uno (complacer).* Dato de diseño: cuidado con que la "pista" no induzca
  complacencia.
- **Reversión a convenciones/defaults** (D): con convenciones no-estándar, vuelve a los
  defaults de manual aunque lo obligues a escribir la convención y sostenerla (vibe-physics).
- **No actuar sobre la propia anomalía** (C/A): no ve lo interesante/anómalo en sus propios
  resultados (varias fuentes).

## 4-ter. Metodología externa que VALIDA nuestro enfoque (no un vicio — una confirmación)

- **La evaluación por OUTCOME no detecta estas fallas** (arxiv 2604.18805): un agente puede
  sacar 80% de accuracy en CLadder/QRData/DiscoveryBench y tener un proceso de razonamiento
  basura. **Por eso hay que analizar la TRAZA, no solo el resultado** — exactamente nuestra
  doctrina "conducta observada" (§2.1) y las firmas de trace. Confirmación externa fuerte.
- **El grafo epistémico como vocabulario listo** (mismo paper): anota cada paso de la traza
  con 6 nodos — **H**ypothesis, **T**est, **E**vidence, **J**udgment, **U**pdate,
  **C**ommitment — y aristas (testing, observing, contradicting, updating…), y matchea contra
  *productive motifs* (falsación popperiana, reranking de hipótesis, revisión por refutación,
  evidencia convergente) vs *reasoning breakdowns* (untested claim, contradiction-without-repair,
  premature commitment, evidence non-uptake, fixed-belief-trace, precommitted-test-plan,
  stalled-revision). **Podemos ADOPTAR este vocabulario para nuestras firmas de trace** — es
  una taxonomía publicada de exactamente lo que medimos.
- **El base model explica el 41.4% de la varianza; el scaffold solo 1.5%** (mismo paper):
  cambiar el prompt/arquitectura casi no mueve la aguja — el vicio vive en el MODELO, no en el
  prompt. **Confirma nuestra tesis de ADR 0096/0098**: el "sé cuidadoso" genérico no arregla el
  vicio (mueve ejecución); el vicio es una propiedad del modelo que hay que ENTRENAR (E2), no
  promptear. Y confirma que el instrumento debe medir algo que el prompt no puede fingir.
- **In-context learning NO lo arregla** (mismo paper): el patrón persiste aun dándole un ejemplo
  casi-completo de buen razonamiento en contexto → refuerza que es entrenable, no prompteable.

## 5. Fuentes a minar (la investigación concreta — en curso)

El seed de §4 sale de conocimiento general; la versión rigurosa se arma yendo a estas familias
de fuentes y sacando failure modes CONCRETOS con su cita:
- **Evals de agentes autónomos**: METR (task-horizon, autonomy failures); taxonomías de fallos
  de agentes LLM 2024-2025.
- **Agentes-científicos / research agents**: AI Scientist (Sakana) y sus críticas; ResearchAgent;
  papers de "LLM as scientist" y sus modos de falla.
- **Benchmarks de descubrimiento**: ScienceWorld, DiscoveryWorld, DiscoveryBench, BoxingGym,
  QRData — sus análisis de error.
- **Cog-sci del razonamiento científico**: confirmation bias / hypothesis testing (Wason,
  Klayman-Ha, Kuhn), heurísticas y sesgos (Kahneman-Tversky), scientific reasoning (Klahr).
- **Calibración / juicio**: superforecasting (Tetlock), calibración y overconfidence.
- **Honestidad / sycophancy / overclaiming**: evals recientes de honestidad de LLMs.
- **Metaciencia**: crisis de replicación, p-hacking, garden of forking paths (Gelman & Loken).

> **Acción concreta**: correr una investigación dirigida (skill `deep-research` o WebSearch) por
> cada familia de §3, extrayendo failure modes con cita + evidencia, y volcarlos a §4 con su
> dinámica de mundo asignada. Paciencia: uno por uno.

## 6. El proceso (de un vicio a un mundo)

```
vicio documentado (§4/§5)
   -> ¿qué DINÁMICA de mundo lo fuerza de forma puntuable? (§3)
   -> deliverable puntuable (predecir comportamiento) + cero-LLM
   -> diseñar el CERTIFICADO DE TRAMPA NECESARIA (robot vicioso pierde / cuidadoso gana)
   -> ¿hace falta PRESIÓN? (escasez / tiempo / evidencia tardía) -- casi siempre sí
   -> build (spec-first) -> certificar -> E0 con pre-registro
   -> ¿el vicio se manifestó con un solver real? (la validez, ADR 0098)
```

## 7. Lo difícil / preguntas abiertas (honestas)

- **Scoring de EXPLICACIONES sin LLM** (suite Anomaly, "¿qué pasó?"): el muro más duro. Los
  vicios que requieren un deliverable-explicación quedan bloqueados hasta resolverlo. Mientras,
  se los fuerza con deliverable-predicción (§ principio 6).
- **Vicios un-hinteable (insight profundo, v2) vs dispositivos (hinteable)**: la distinción de
  ADR 0097. Los profundos no se validan con pista (cualquier pista = leak) — su validez es que
  ningún modelo los vence (v2: 0/10). Los dispositivos se validan con pista dirigida (ADR 0098).
- **Eje de creatividad/representación**: inventar la estructura es research taste generativo y
  es lo que mejor funciona (v2), pero es lo más difícil de generar y de puntuar. Merece su
  propia línea de pensamiento.
- **Réplica pendiente** (ADR 0098): DeepSeek + más seeds + clasificación automática de ceros,
  antes de un claim firme de validez.
