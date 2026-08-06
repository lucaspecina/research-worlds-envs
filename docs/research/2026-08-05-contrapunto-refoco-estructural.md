# Contrapunto — por qué WAGER todavía no cierra, y el refoco que propongo

> **Fecha:** 2026-08-05 · **Autor:** Claude (rol contrapunto, ADR 0172) · **Encargo:** Lucas pidió
> repensar críticamente qué hace que el proyecto "todavía no funcione", con libertad para redefinir
> objetivos, y encontrar un nicho publicable, defendible y útil.
> **Estado:** posición independiente PARA DECIDIR. No modifica roadmap, nota de dirección ni ADRs;
> eso corresponde a Codex/Lucas si aceptan. Leído antes de escribir: nota de dirección, cabecera
> completa del roadmap, posicionamiento (mapa de competidores), tablero de vicios + vicio-4,
> red-team (ataques + supuestos), cómo-medimos, reassessment Codex 2026-07-31, resultados de
> topología v1 + réplica gpt + control 2D + ODE v0/v1 + estrategia de modelos chicos.

---

## 1. Diagnóstico: por qué todavía no hay "algo que analizamos y reproducimos"

El proyecto tiene maquinaria excepcional (fork apareado desde checkpoint vivido, reward cero-LLM,
certificados, disciplina de fichas/resultados) y **~20 probes con agentes reales cuyo saldo es:
la mayoría nulos**. Cinco razones, de la más superficial a la más estructural:

**D1. El blanco se definió como un fenómeno que los frontier casi no tienen a la escala que
podemos pagar.** "Revisión de creencias" se ancló por fidelidad a casos reales (KellyBench, Corral,
RadLE) cuyas *condiciones* — trayectorias de semanas, memoria que se pierde, compromiso real,
dependencias materiales — los hosts chicos no materializan. La propia doctrina lo reconoce
("auditoría fundamental del mundo") y aún así el ciclo siguió probando elicitores en microscopios.
Resultado predecible: DeepSeek y gpt-5.4 revisan bien parámetros, no tienen sunk cost medible,
propagan cuando es saliente, no se anclan con filler. Cada nulo fue diagnosticado correctamente…
y el programa siguió en la misma cinta.

**D2. El reflejo de descalificación.** Cada vez que una señal sobrevivió, se la reclasificó:
"puede ser dificultad general de modelado, no resistencia a revisar lo propio"; "no es anclaje;
causa general". Correcto como lectura del constructo vicio-1 — pero el efecto acumulado es que
**el hallazgo más robusto del proyecto viene siendo tratado como confound de otro claim** en vez
de como el claim. El control de analista fresco que lo "descalifica" como vicio de compromiso es
exactamente lo que lo vuelve un hallazgo *más grande*: no es apego — es una política de inferencia
sistemática del agente.

**D3. La vara del catálogo filtra qué cuenta como éxito.** El vocabulario ("vicio",
"revisión de creencias") hace que un fenómeno descubierto por autopsia — no listado con ese nombre
en el catálogo — no dispare la promoción. ADR 0173 ya legalizó elevarlo como pivote; falta
ejecutar esa cláusula.

**D4. Deuda de medición en la métrica cabecera.** En el microscopio SCM, `R` global no ordenó el
fenómeno (RETAIN y LATENT dieron 0; REVISE 0.136): el reward configurado no ve lo que nos importa.
Es el ataque #5 del red-team otra vez (energía sobre marginales ciega a multimodalidad) — ya se
resolvió una vez con score combinado + certificado de visibilidad (ADR 0026, `latent_mix_v2`),
pero el microscopio nuevo no reusó ese fix. Para un benchmark, el score TIENE que rankear el
fenómeno; hoy solo lo rankean las firmas locales (`A3`, partición).

**D5. Nada es confirmable aún.** Donantes n=1–3 por celda, dos familias de modelo (DeepSeek,
gpt-5.4), formación de donantes inestable (seeds censuradas por interfaz). La transición
descubrimiento→confirmación de ADR 0173 está diseñada y no ejecutada.

## 2. La inversión: el fenómeno ya apareció — hace un mes que lo estamos mirando

Junto lo que **sí** sobrevivió a todo:

| Evidencia | Resultado | Estado |
|---|---|---|
| `latent_mix_v2` (época 1, ~4-5 jul; ex `mendel_subtypes`) | **0/10 episodios** (DeepSeek + gpt-5.4, seeds 0–7, harness viejo) promovieron la anomalía a composición oculta; techo R=0.096 | Avistamiento independiente ANTERIOR con otro instrumento — no evidencia con el instrumento actual. OJO: el doc vicio-4 dice "0/10 modelos"; el ledger crudo (`cases/latent_mix_v2/E0_LEDGER.md`) dice 10 trazas de 2 modelos |
| SCM North heterogéneo | Media revisada bien; mezcla 75/25 aplanada a una Normal en **4/4 forks**, 2 modelos | Replicado |
| SCM topología LOCAL vs LATENT | Partición **visible** capturada 83–96%; la misma estructura **latente**: `A3≈0` en ambos modelos | Replicado + controles |
| Control analista fresco | Aplana igual sin trayectoria previa | No es compromiso/anclaje |
| Testigo cero-LLM (BIC+CV) | Selecciona la mezcla correcta desde **las mismas filas servidas** en 3/3 donantes + holdouts | No es límite de información |
| Control criticism genérico | Pedir chequear residuos/adecuación: compara colas pesadas, **jamás propone subpoblaciones** | No es falta de instrucción |
| Control de turno real | Con sus propias tablas delante, reenvía el modelo unimodal **byte-idéntico** | No es un olvido de mirar |
| Familias declaradas legales | Implementa la mezcla pero la estima mal y degrada el resto | El menú no basta; falta el gatillo |
| ODE STRUCT | Falla de 1 fase… que **se rescata sola** al leer su stdout (MAE 5.43→0.90) | Cuando el desajuste vive en la MEDIA, sí abre |
| Externo: DiscoverPhysics `[VERIFICADO]` | Frontier falla justo en mundos con estructura latente; "lock in a candidate law early and refine parameters rather than revise its conceptual picture" | Convergencia externa |
| Externo: Chen/Zhao/Cohan `[VERIFICADO]` | Los modelos evitan decouple/replace/formalize; el thinking lo empeora | Convergencia externa |

**El enunciado unificado (candidato a claim del paper):**

> Los agentes LLM hacen model criticism espontáneo **solo al primer momento**: revisan su modelo
> cuando el desajuste aparece en medias/ajuste visible, y **no generan jamás la hipótesis de
> estructura** (mezclas, subpoblaciones, regímenes) cuando la señal vive en forma/dispersión —
> aunque la evidencia esté en su mano, el presupuesto sobre, las herramientas alcancen y un
> selector mecánico (BIC/CV) la prefiera desde exactamente las mismas filas.

Esto **unifica** los dos candidatos líderes del embudo: "apertura estructural latente" (SCM) y
"cierre/autoridad del diagnóstico" (ODE) dejan de ser dos fenómenos — ODE se rescató porque su
señal estructural era de primer momento; SCM no se rescata porque detectarla exige un test de
forma que el agente nunca corre. La cadena de la nota de dirección queda localizada con precisión:
el corte **no** está en *notar* (escribió "varianza residual 22.5 vs 7.0") ni en *asimilar
parámetros* (F≈1) — está en **interpretar→hipotetizar**: la anomalía de forma nunca se convierte
en candidato estructural.

Y conecta limpio con el catálogo: es el **vicio 4** (que ya tenía el trofeo y la validación
externa) *medido con la instrumentación del vicio 1* (gemelos bilaterales, fork vivido, update
legal). La caminata de un mes no fue en círculo: volvió al vicio 4 con instrumentos que nadie
más tiene.

## 3. El nicho

**Nombre de trabajo del fenómeno:** *aplanamiento estructural* (structural flattening) /
claim: "agents fit, but don't look for form".

**Por qué está vacante** (contra el mapa de posicionamiento, actualizado):

| Vecino | Qué tiene | Qué le falta que nosotros tenemos |
|---|---|---|
| DiscoverPhysics | Frontier falla en estructura latente, agéntico | Juez-LLM en la explicación; sin gemelo bilateral; sin testigo de recuperabilidad; sin aislamiento causal de *cuándo* abre |
| BoxingGym | Model discovery generativo | Sin fork apareado, sin certificados, `[POR-LEER]` |
| BeliefTrack | stay/update/isolate con oráculo simbólico | Hipótesis discretas de menú; nunca hay que INVENTAR estructura |
| BayesBench | Estructura inferida vs usada | Sin agencia de compra, sin entrega ejecutable en nuestro sentido, carga cero |
| Chen/Zhao/Cohan | La movida faltante (decouple), descriptivo | Mide texto de ideas con anotador LLM; sin consecuencia ejecutable |
| GeneBench-Pro | Grader determinista, notice–act | Todo-o-nada; sin estructura latente que postular |
| Autonomous Model Discovery | Modelo ejecutable vs verdad, cero juez | Una corrida; sin revisión, sin gemelos, sin testigo |

La combinación vacante que ya tenemos construida en borrador: **(a)** entrega = modelo ejecutable
puntuado cero-LLM con funcionales de estructura orientados (`A3`); **(b)** gemelos bilaterales —
el polo donde postular estructura gana Y el polo donde postularla pierde (anti-apofenia, par
Vulcano del vicio 4); **(c)** el **testigo de recuperabilidad**: cada instancia viaja con la
prueba mecánica (BIC/CV sobre las filas exactamente servidas) de que la estructura era
estadísticamente preferible — mata para siempre la objeción "la tarea era imposible/subdeterminada";
**(d)** fork desde checkpoint vivido — separa política de inferencia de compromiso con lo propio
(control fresco); **(e)** escalera de momentos — localiza DÓNDE muere el criticism espontáneo.

Los primitivos (b) y (c) son contribuciones metodológicas reutilizables por sí mismas:
**fallas con testigo** — todo claim de falla viaja con la prueba de que el éxito era alcanzable
desde los mismos bits, y con el gemelo donde el reflejo opuesto pierde.

**Por qué es útil** (no solo publicable): agentes-científicos se están desplegando ya; un modelo
que ajusta medias perfectas y aplana subpoblaciones produce conclusiones científicamente falsas de
la peor clase — las que los chequeos estándar de fit no detectan (flaw of averages; responders vs
non-responders; Simpson). El testigo es accionable: un "structure-opening check" mecánico que
cualquier harness puede correr sobre los datos que su agente ya sirvió. Y los brazos de
intervención (qué lo rescata: re-entrada del stdout; qué no: prompts genéricos de criticism)
son guía práctica inmediata para builders.

## 4. Objeciones duras y respuestas (pre-referee)

| Objeción | Respuesta (evidencia ya existente o brazo planificado) |
|---|---|
| "Es un benchmark de capacidad, no un 'vicio'" | Correcto — y no importa: el paper no necesita vocabulario psicológico. Es una **política de inferencia sistemática** caracterizada con controles causales. (Para el programa interno sigue siendo la punta del eje "revisión estructural" de la nota §6.) |
| "Con mejor prompt se arregla" | Brazos negativos ya corridos: criticism genérico NO abre; turno extra NO abre; menú declarado no basta. Brazo positivo: saliencia de stdout SÍ (ODE). Eso es la sección de intervenciones, no una debilidad |
| "El agente no tenía herramientas para mezclas" | Tenía kernel con scipy y presupuesto sobrante; conductualmente **jamás intentó** ningún test de forma. Para confirmación: garantizar sklearn en el kernel y registrar si lo usa |
| "Mundos de juguete, no generaliza" | 2 formalismos ya (SCM sí; ODE explica el rescate); confirmación exige un 3º con señal en forma (conteos sobredispersos / cambio de régimen); convergencia externa en física alterada (DiscoverPhysics) |
| "Solo 2 familias de modelo" | Agregar 3ª familia (Claude vía API nativa — lado agente, no reward path — o deployment compatible) antes de congelar |
| "La información no alcanzaba" | El testigo: BIC/CV la seleccionan desde las MISMAS filas, 3/3 donantes + holdouts honestos |
| "Premian cambiar/postular siempre" | Gemelos: RETAIN limpio en todos los resultados citados; falta instanciar el gemelo anti-apofenia (postular-siempre PIERDE) en el host nuevo — va en fase A |
| "n chico, selección post hoc" | Exactamente por eso: ADR 0173 — los datos que encontraron la firma no confirman; grilla congelada con seeds frescas y regla de decisión pre-registrada |

## 5. Qué se redefine (honesto)

1. **La pregunta del paper se congela sobre el fenómeno descubierto**, no sobre el paraguas:
   de "¿cuándo se pierde la revisión?" a "¿cuándo un agente ABRE la estructura de su modelo —
   y por qué el criticism espontáneo muere fuera del primer momento?". El paraguas
   revisión-de-creencias queda como programa (la nota de dirección ya contiene la distinción
   refinamiento/revisión-estructural en §6 — no es traición, es colapsar sobre la rama con señal).
2. **La regla de fidelidad se reinterpreta sin romperse:** de "reproducir el caso documentado en
   sus condiciones" a "aislar y certificar una falla recurrente **descubierta**, y conectarla a los
   síntomas documentados" (DiscoverPhysics/Chen como síntomas externos del mismo mecanismo).
   Esto necesita bendición explícita de Lucas porque toca una regla dura (ADR 0147).
3. **La etapa 6t no muere: se absorbe.** "Corrección local vs reabrir estructura propia
   compartida" se vuelve el brazo de endogeneidad de la fase A (¿abre menos cuando la estructura
   es suya?), en el host nuevo, en vez de un gate suelto en ODE.
4. **El candidato "cierre/autoridad del diagnóstico" baja a mecanismo**, sección del mismo paper
   (la escalera de momentos lo subsume), no paper aparte.
5. **Alternativas consideradas y por qué no:** (i) seguir minando elicitores del paraguas — la
   cinta ya consumió ~20 probes; valor esperado marginal bajo; (ii) pivotar a propagación/saliencia
   — real pero superficial (un recordatorio lo cura; GeneBench ya documentó notice–act
   cualitativo); queda como hallazgo secundario; (iii) paper solo-metodología — más débil sin
   fenómeno; los primitivos viajan DENTRO del paper del fenómeno (y un release de benchmark
   después); (iv) construir el host largo tipo KellyBench para cazar compromiso — caro, y
   Big-Muddy advierte que el apego puede requerir bundles sociales; no rescatar.

## 6. Programa propuesto

**Fase 0 — decisión y entorno (esta semana, ~0 costo API).**
Cruce de esta posición con Codex (ADR 0172) → decisión de Lucas: promover o no. Si GO: ADR nuevo +
edición de cabeceras (Codex/Lucas). En paralelo, mecánico: `.env`, `.venv` 3.13, sklearn (también
en el kernel del agente), hooks. Nada de esto espera la decisión.

**Fase A — restos de descubrimiento (1–2 semanas, agentes baratos, ~USD 50–120 est.).**
Cada ítem con microhipótesis previa + autopsia, disciplina de siempre:
- **A1. Escalera de momentos en SCM** (host ya validado): misma masa de evidencia, moviendo dónde
  vive la señal discriminante — (i) media [control, ya sabemos que abre], (ii) solo-varianza,
  (iii) forma/bimodalidad [actual], (iv) etiqueta visible [control, ya sabemos que abre].
  Microhipótesis: la revisión espontánea muere entre (i) y (ii). Es EL test de
  "criticism de primer momento".
- **A2. Tercer host con señal en forma, formalismo distinto:** conteos con sobredispersión/
  inflación de ceros (Poisson vs mezcla) o serie con cambio de régimen donde la media ajusta.
  Con testigo BIC/CV y gemelo sin-estructura. Si `A3`-análogo ≈ 0 replica → generalización
  que ODE no podía dar (su señal era de primer momento).
- **A3. Tercera familia de modelo** (smoke primero): cliente Anthropic lado-agente o deployment
  compatible. Sin esto no hay claim "frontier agents".
- **A4. Gemelo anti-apofenia** (par Vulcano, vicio 4): el polo donde declarar mezcla PIERDE.
  Certificado: postular-siempre pierde; robots de reflejo.
- **A5. (absorbe 6t) Brazo de endogeneidad:** estructura propia vs heredada en el host A2 —
  ¿la autoría cambia la tasa de apertura? (Predicción desde el control fresco: no. Un nulo acá
  es un RESULTADO del paper: "no es apego".)
- **Reparación de medición (D4):** funcional de estructura al score combinado del host nuevo +
  certificado de visibilidad (reusar ADR 0026), para que `R` ordene el fenómeno.

**Gate de salida de fase A** (criterios de muerte pre-escritos): si A2 no replica el aplanamiento
en el host nuevo con testigo válido, la candidata vuelve al banco y NO se adapta el host para
rescatarla (ADR 0173 literal). Si A1 no muestra el corte de momento, el claim se reduce a
"apertura estructural" sin la escalera.

**Fase B — congelar y confirmar (tras GO de Codex/Lucas sobre resultados de A).**
Pre-registro: pregunta, 2–3 hosts, 3 familias, brazos, métricas primarias (`A3`-familia, captura
de partición, F secundaria), n por celda desde la varianza de A, regla de decisión, techo de gasto
(estimar en serio antes: orden grueso USD 300–600 para ~300 ramas; la regla de CLAUDE.md manda
presupuestar primero). Seeds frescas, donantes no usados en iteración.

**Fase C — el "so what" (con B corriendo o después).**
- Brazos de intervención: re-entrada de diagnóstico; herramienta de shape-check provista; scaffold
  Estimate→Verify→Update (el comparador de Seeing-Isn't-Believing del posicionamiento).
- **Idea nueva para discutir (una vuelta de tuerca, opcional):** el testigo como herramienta
  COMPRABLE dentro del episodio — un "model criticism scan" con costo en presupuesto. ¿El agente
  lo compra cuando el gemelo hace que pague y lo saltea cuando no? Convierte el fenómeno en
  decisión económica con oráculo cero-LLM (¿era racional comprarlo?) y conecta vicios 2 y 6 sin
  cambiar de proyecto. Nadie mide "¿los agentes compran criticism?".
- Release del benchmark: familias con testigos + gemelos + funcionales cero-LLM (acá la capa
  "método" de `docs/reorganizacion-motor-vs-estudios.md` se vuelve producto).

## 7. Riesgos del refoco

- **Scoop:** DiscoverPhysics/BoxingGym están cerca; nuestros diferenciales (testigo, bilateral,
  cero-LLM, fork vivido) son defendibles pero la ventana no es infinita. El refoco ACELERA
  (colapsa el espacio de búsqueda); quedarse minando el paraguas la quema.
- **Que A2 no replique:** entonces el aplanamiento es idiosincrático del SCM y lo aprendemos por
  ~USD 60 en dos semanas — barato, y el banco de candidatas sigue (ADR 0173 lo prevé).
- **Circularidad de importancia** (S15 del red-team): que el fenómeno nos importe no prueba que
  importe afuera — mitigación: la conexión a síntomas externos verificados y el caso de uso
  concreto (flaw of averages en agentes desplegados).
- **El reward que no ordena (D4)** es deuda real para la versión benchmark; el fix tiene
  precedente probado (ADR 0026).

## 8. Decisión pedida

1. ¿Se promueve **aplanamiento estructural / criticism de primer momento** a candidata única de
   congelamiento, con el paraguas como programa? (MANTENER la fase de descubrimiento pero
   COLAPSADA sobre esta línea: fase A.)
2. ¿Se acepta la reinterpretación de fidelidad (§5.2)? — toca regla dura, decide Lucas.
3. ¿6t absorbida como brazo A5 en host nuevo (en vez de gate suelto en ODE)?
4. Cruce con Codex antes de tocar roadmap/nota (ADR 0172): esta nota es el insumo.
