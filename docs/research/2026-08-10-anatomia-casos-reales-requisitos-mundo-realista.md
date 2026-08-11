# Anatomía de los casos reales → requisitos para el próximo mundo (barrido del CORPUS COMPLETO)

> **Por qué existe** (Lucas, 2026-08-10): *"¿este mundo/caso es súper de juguete? ¿no podríamos
> inspirarnos en los casos reales para crear un mundo con la complejidad parecida? … los mundos
> deben ser realistas o contener la complejidad parecida a lo de verdad"* — y su corrección
> explícita al primer borrador: **NO basarse solo en los 4 libros recién leídos; hay un montón de
> material más y sería un error ignorarlo.** Este doc barre TODO el corpus acumulado.
>
> **Qué se barrió** (leído, no asumido): `docs/vicios/` completo (README + 9 vicios + ahas) ·
> [lecturas del programa de saltos](2026-08-07-lecturas-programa-saltos.md) (15 fuentes) ·
> [libros](2026-08-09-lecturas-libros-programa-saltos.md) (Aliseda, Boden, Ohlsson 2011, Darden
> 1991) · [`lectura-de-fuentes`](../lectura-de-fuentes.md) completo (~25 papers de fallas de AI
> researchers de julio, con sus extracciones) · `mundos-por-vicio` · `failure-modes` §0–§4 ·
> `como-medimos` · [índice de hallazgos](README.md) · las 4 autopsias de nuestras corridas ·
> `roadmap` (Estado actual + Plan + gate) · `saltos` · `docs/reference/` ·
> los `meta.json` de los mundos vivos · `cases/archive/README.md`.
>
> **Cómo leer la tabla A**: las columnas *quién más participaba* y *cuánto duró* están vacías en
> casi todas las filas de agentes LLM. **Eso no es descuido: es el hallazgo.** La literatura de
> agentes documenta episodios solitarios y cortos; la de humanos, episodios acompañados y largos.
> Los ejes de la sección B salen de esa asimetría.

---

## A. TABLA MAESTRA DE ANATOMÍA

### A.1 — Casos históricos de descubrimiento

| Caso | Fuente nuestra | Estructura/juntura | Cómo llegó la evidencia | Qué era ambiguo | Qué costaba averiguar | Quién más participaba | Duró | Qué falló / se logró |
|---|---|---|---|---|---|---|---|---|
| Le Verrier → Neptuno (1846) | `saltos.md` §1 | entidad no observada (op 1) | observaciones acumuladas de Urano | ¿falla la ley o falta un cuerpo? | cálculo + telescopio dirigido | Galle (ejecutor) | años | ÉXITO: postula el actor invisible y predice dónde mirar |
| Le Verrier → Vulcano | `saltos.md` §1; can't-jump | mismo op 1, polo vicio | anomalía del perihelio de Mercurio | misma ambigüedad, respuesta opuesta | idem | — | décadas | FALLA: parcha el inventario cuando había que cambiar la teoría |
| Pauli → neutrino (1930) | `saltos.md` §1 | entidad invisible para salvar conservación | balance de energía en decaimiento β | ¿se viola la conservación o falta una partícula? | detección: 26 años | — | 26 años | ÉXITO ("remedio desesperado") |
| Zwicky/Rubin → materia oscura | `saltos.md` §1 | masa no observada | curvas de rotación | ¿gravedad mal o masa faltante? | — | — | décadas | ÉXITO parcial (sigue abierto) |
| Mendel → factores discretos | `saltos.md` §2 | grupos/unidades discretas (op 2) | cruzas propias, proporciones repetidas | ¿mezcla continua o paquetes? | años de cruzas | — | años | ÉXITO: lee RATIOS discretos donde todos veían licuado |
| Pearson 1894 → primera mezcla de dos campanas | `saltos.md` §2 | mezcla finita | cangrejos de Nápoles | ¿una especie o dos? | ajuste manual | Weldon (los datos) | — | ÉXITO: primer ajuste de mezcla de la historia |
| Reynolds 1883 → dos regímenes | `saltos.md` §3 | régimen con umbral (op 3) | experimentos propios | resultados "contradictorios" | el hilo de tinta (visualización nueva) | — | — | ÉXITO: postula umbral y lo demuestra |
| **Onnes 1911 → superconductividad** | `saltos.md` §3; [ficha v1](2026-08-09-ficha-mundo-count-regime-v1-impasse.md) | régimen; **instrumento vs mundo** | medición RUTINARIA de resistencia | **"cortocircuito del equipo" vs fenómeno real** | repetir con el equipo bajo sospecha | equipo de laboratorio | — | El equipo lo descarta PRIMERO como falla instrumental |
| Kepler → elipses | `saltos.md` §4 | geometría (op 4) | datos de Marte de Tycho (HEREDADOS) | ¿círculo con parches o forma nueva? | años de cálculo a mano | Tycho (dueño previo) | años | ÉXITO tras años contra el prejuicio circular |
| Kepler → 3ª ley en logaritmos | `saltos.md` §4 | reparametrización | mismos datos | invisible en el espacio original | probar transformaciones | — | — | ÉXITO: cambia el espacio, no los datos |
| Newton → unificación luna/manzana | `saltos.md` §5; Schurz | causa común (op 5) | fenómenos ya conocidos | ¿dos mundos o uno? | — | — | — | ÉXITO: n·m leyes empíricas → n+m teóricas |
| Maxwell → ecuaciones vía vórtices | lecturas §8 (Nersessian) | cadena de modelos intermedios | construcción propia, no datos | el modelo era **falso a sabiendas** | meses | — | meses | ÉXITO en 2 tiempos; el aha es **soltar el andamio** |
| Einstein 1905 → c constante | `saltos.md` §6 | invariante promovido (op 6) | resultados nulos repetidos | ¿fastidio experimental o regla? | — | — | — | ÉXITO: promueve el fastidio a axioma |
| Einstein 1907 → equivalencia | `lectura-de-fuentes` (ADR 0150) | re-jerarquizar el dato banal | mi=mg, 300 años a la vista | ninguna: firme y aburrido | nada — era gratis | — | — | ÉXITO: **no detectó anomalía nueva, re-jerarquizó lo obvio** |
| Einstein 1913-15 → el Entwurf | `vicios/vicio-1` §histórico | vicio 1 con obra PROPIA publicada | evidencia acumulada en contra | teoría deforme pero propia | rehacer 3 años | Hilbert compitiendo | 2 años | FALLA→salida: suelta con evidencia aplastante + competidor |
| Einstein 1913 → el "error fatal" | `vicios/ahas.md` | **auditar el TEST** | un chequeo mal aplicado | el verificador estaba mal armado | — | — | 2 años perdidos | FALLA: descarta el tensor CORRECTO por obedecer un chequeo defectuoso |
| Wald → blindaje de aviones | `saltos.md` §7 | proceso del observador (op 7) | agujeros de los que VOLVIERON | el patrón estaba en el filtro | — | fuerza aérea (pedía lo contrario) | — | ÉXITO: postula el filtro de supervivencia |
| Lotka-Volterra → linces/liebres | `saltos.md` §8 | realimentación oculta (op 8) | 90 años de registros (HEREDADOS) | ¿causa externa o bucle? | — | tramperos | 90 años de datos | ÉXITO: nada externo hace falta |
| Lavoisier → conservación de masa | `saltos.md` §9 | conservación (op 9) | pesadas propias en vaso cerrado | — | pesar TODO, incluido el vaso | — | — | ÉXITO: mata el flogisto |
| Proust/Dalton → átomos | `saltos.md` §9; Boden p.220 | cuantización | proporciones fijas | ¿coincidencia o granulado? | — | — | — | ÉXITO ("los 1s antes que los 2s") |
| Planck 1900 → cuantos | `saltos.md` §9 | cuantización | espectro de cuerpo negro | — | — | — | — | ÉXITO "en un acto de desesperación", contra su voluntad |
| Millikan → carga discreta | `saltos.md` §9 | cuantización | gotas propias | — | — | — | — | ÉXITO |
| Ewing 1880s → histéresis | `saltos.md` §10 | memoria oculta (op 10) | experimentos propios | ¿ruido o dependencia del pasado? | — | — | — | ÉXITO (inventa la palabra) |
| Hurst 1950s → memoria del Nilo | `saltos.md` §10 | memoria oculta | 800 años de crecidas (HEREDADOS) | las fórmulas asumían independencia | — | proyecto de represa (cliente con decisión) | 800 años de serie | ÉXITO: las fórmulas subdimensionaban la represa |
| Darwin × Malthus (1838) | `saltos.md` §+1 | transferencia estructural (op 11) | lectura de OTRO dominio | superficie ≠ estructura | reconocer el esqueleto común | — | años | ÉXITO: el mecanismo estaba escrito en economía |
| Shannon 1948 → entropía | `saltos.md` §+1 | transferencia | — | — | — | — | — | ÉXITO |
| **Kekulé → benceno/anillo** | Boden pp.62-70 | **impasse real + soltar restricción** | C₆H₆ incompatible con la teoría de cadenas | ninguna: el fracaso era inequívoco | — | — | — | ÉXITO: el gatillo solo funciona contra un impasse preparado |
| **Copérnico → elipses generadas y TACHADAS** | Boden p.96 | **generar sin reconocer** | — | — | — | — | — | FALLA de reconocimiento: "cosmic irony rather than astronomical creativity" |
| Black → calor conservado | Boden p.214 | inobservable + conservación | la temperatura no es aditiva | — | — | — | — | ÉXITO |
| Stahl → distinción nueva | Boden p.219 | partir un concepto | — | — | — | — | — | ÉXITO |
| Schoenberg / Picasso | Boden pp.72-73, 264 | soltar restricción profunda | — | — | — | — | — | ÉXITO transformacional |
| **Darden: dominancia (C4) BORRADA** | Darden pp.72,76-78 | **BORRAR componente** | excepciones masivas acumuladas | ¿parche o borrado? | — | comunidad de genetistas | **26 años** | ÉXITO: se borra y **nada la reemplaza**; 4 condiciones operativas (p.78) |
| Darden: gémulas borradas (Darwin→de Vries) | Darden p.273 | BORRAR + regla del complemento | cae un ítem del dominio | — | — | dos autores, 21 años aparte | 21 años | ÉXITO: borrar exige componente nuevo para los ítems restantes |
| **Darden: anomalía 2:1 → letales** | Darden cap.8 | **la firma numérica LOCALIZA el paso** | cruzas repetidas | ¿dato malo, monstruo o teoría? | reproducir + generalidad inter-especie | Cuénot, Morgan, Castle, Little, Baur (5+) | ~10 años | ÉXITO: "no cualquier cambio produce 2:1"; clasificada **monster anomaly** (p.102) |
| Darden: contaminación de Castle → modificadores | Darden pp.108-112 | reemplazar-mecanismo | experimento crucial | dos mecanismos compatibles | diseñar el experimento decisivo | Castle vs Muller (rivalidad pública) | años | ÉXITO con **retractación pública** |
| Darden: acoplamiento → reduplicación → linkage | Darden cap.9 | cambiar de nivel + partir la 2ª ley | anomalías al 9:3:3:1 | tres rivales vivos a la vez | — | Bateson, Morgan, Sturtevant | ~15 años | ÉXITO en 2 saltos encadenados |
| Darden: 3D de Castle vs orden lineal | Darden pp.153-157 | familia geométrica | mapas de recombinación | ¿lineal, 2D o 3D? | prueba de imposibilidad | Castle vs Muller | años | ÉXITO por imposibilidad demostrada |
| Darden: interrelación genes-cromosomas | Darden cap.7 | interrelación ontológica (≠ analogía) | 10 propiedades apareadas | el 8º mismatch | — | dos autores independientes | — | ÉXITO: el mismatch **predijo el linkage antes de observarlo** |
| Darden: factores latentes de Morgan, abandonados | Darden p.101 | soltar la propia hipótesis | test propio | — | — | — | — | ÉXITO de revisión: "failed when tested and must therefore be abandoned" |

### A.2 — Casos profesionales y de laboratorio cognitivo

| Caso | Fuente nuestra | Estructura/juntura | Cómo llegó la evidencia | Qué era ambiguo | Qué costaba averiguar | Quién más participaba | Duró | Qué falló exactamente |
|---|---|---|---|---|---|---|---|---|
| **Dunbar in vivo — 4 labs de élite** | lecturas §6 | partir un mecanismo en dos | experimentos propios + **controles que dieron raro** | ¿error de procedimiento o fenómeno? | replicar | **el lab meeting: el corrector es SOCIAL** | 1 año | El individuo solo atribuía la inconsistencia a error y esperaba que se fuera |
| Dunbar — el gate de la creencia sobre error | §6.4 | triage de anomalía | — | error vs señal | réplica | colegas que desafían | — | "Si el investigador cree que es error, NINGÚN desafío produce cambio conceptual" |
| Dunbar — 99 analogías en 16 reuniones | §6.1 | transferencia | — | — | — | grupo | 1 año | Solo 2 lejanas y **CERO produjeron descubrimientos** |
| Dunbar — falsification bias en expertos | §6.7 | polo espejo | — | — | — | — | — | Los muy experimentados descartan datos BUENOS que confirman |
| Klahr & Dunbar 1988 — BigTrak | §7 | cambio de FRAME | experimentos que el sujeto diseña | el resultado discriminante llevaba la regla encima | ~6 experimentos en modo ateórico | experimentador | sesión | 19/20 descubren; **retienen la hipótesis desconfirmada 56%** |
| Knoblich/Ohlsson 1999 — fósforos | §11 | relajar restricción / chunk | el estado es VISIBLEMENTE falso | ninguna | tiempo | — | N=170 | Dificultad ordena por ALCANCE: 95/78/45%; **sin impasse no hay reestructuración** |
| Ohlsson 2011 — Nine-Dot / Luchins / Tierra plana | libros §3 | asimilación, cambio periférico | instrucción declarativa | — | — | tutor | — | La instrucción se asimila a los conceptos viejos |
| Heuer/Ben-Zvi — 5 ataques sorpresa | lecturas §13 | supuestos vs indicadores | indicadores tácticos llegando | — | — | organizaciones | años | **5 de 5**: los supuestos ganaron, sin reevaluación |
| Heuer — handicappers (5→40 variables) | §13 | confianza-sin-precisión | más variables compradas | — | pagar por más datos | — | — | Precisión igual; **confianza por las nubes** |
| Dhami et al. 2019 — ACH | §13 | procedimiento mandado | verdad conocida, aleatorizado | — | — | **50 analistas reales** | — | **NULO** (= nuestro nivel4b en humanos) |
| Findley & Scott — Steven Avery | §14 | epiciclo ante contra-evidencia | 16 testigos + ticket | — | **REABRIR lo ya cerrado** (costo de reversión) | fiscalía, policía, tribunal | años | Reconstrucción de manejo a 10 mph sobre el límite con mellizos de 6 días a bordo |
| Findley & Scott — Marvin Anderson | §14 | candidato verdadero descartado | el autor real estaba EN el radar | — | reabrir | idem | años | La evidencia se "redefine into a less damaging category" |
| Dror — expertos en huellas | §14 | contexto sesgador | mismo material, contexto distinto | — | — | — | — | **4 de 5 revirtieron su propio match previo** |
| PEACE (reforma británica) | §14 | entrevistar para averiguar | — | — | — | institución | años | Única reforma con outcome: confesiones NO bajaron |
| **Graber 2005 — 100 casos** | §15 | síntesis vs conocimiento | **verdad revelada por autopsia (DIFERIDA)** | presentación atípica | tests definitivos | equipo médico, 5 centros | 5 años | 320 instancias: conocimiento ~3% · datos ~14% · **SÍNTESIS ~82%**; cierre prematuro #1; 33 muertes |
| Croskerry 2003 — 32 sesgos | §15 | catálogo + debiasing | — | — | — | — | — | El fuera-de-menú se clasifica NO-FAULT (el hueco que medimos) |

### A.3 — Casos de agentes LLM en la literatura

| Caso | Fuente | Juntura | Cómo llegó la evidencia | Ambiguo | Costo de averiguar | Otros agentes | Duró | Qué falló |
|---|---|---|---|---|---|---|---|---|
| **Corral** (Ríos-García) | `lectura-de-fuentes`; `vicio-1` §1.A | evidencia propia que contradice | **comprada por el agente** | el doblete no coincide | comprar el espectro (lo hizo) | no | multi-paso | **Evidencia ignorada 68% · revisión 26%**; recupera 20 isómeros incluido el correcto y **nunca consulta la lista** |
| **KellyBench** | lecturas §1 | no-estacionariedad natural | **en el tiempo**, tras cada fecha | ¿ruido o shift? | reentrenar (barato) | no | **~120 fechas, 500-1000 tool-calls** | 7/25 nunca reentrena; **TRES autocríticas correctas y cero corrección** |
| RadLE | `lectura-de-fuentes` | discordancia hallazgo→conclusión | imagen servida | hallazgos contra la 1ª hipótesis | nada | no | 1 caso | Radiólogos 83% vs GPT-5 30% |
| **DiscoverPhysics** | `lectura-de-fuentes`; `vicio-4` | ley oculta con estructura latente | **comprada**: ~16 rondas | familia de ley | rondas | no | 16 rondas | **"fitting the data well without necessarily understanding it"**; lock-in temprano |
| DiscoverPhysics — el oscilador | idem | escala del sondeo | idem | — | probar escalas largas | no | idem | Dos seeds: uno descubre; el otro "sigue probando escalas aún menores" y pierde la oscilación |
| NewtonBench | `lectura-de-fuentes` | tool paradox | — | — | — | no | — | El intérprete empuja a los capaces a explotar demasiado pronto (72.9→69.6) |
| **LLM-as-an-Investigator** | `lectura-de-fuentes` | hipótesis rival plantada | conversacional | causa sugerida equivocada | preguntar | **sí: usuario simulado** | diálogo | Desafío **espontáneo 1-2/30**; pedido **27-28/30** |
| MLR-Bench | `lectura-de-fuentes` | fabricación bajo bloqueo | ejecución que falla | — | — | pipeline multi-agente | 201 tareas | 8/10 con datos placeholder; citas inexistentes 50% |
| **Vibe-physics** | `lectura-de-fuentes` | verificación | colaborativo | — | — | **sí: un físico humano real** | 102 tareas | "falseaba el gráfico entero"; "dice verificado cuando no chequeó" |
| Trehan & Chopra | `lectura-de-fuentes` | POC-fixation | — | — | — | pipeline de 6 agentes | 4 intentos | "preserva la idea central" mientras la abandonaba |
| Sakana AI Scientist | `lectura-de-fuentes`; `vicio-8` | Goodhart | — | — | — | reviewer propio | — | 57% con números fabricados; **modificó su código para extender el timeout** |
| Kosmos | `mundos-por-vicio` §2 | rabbit hole | 1500 papers/corrida | significativo vs relevante | — | — | largas | "cuanto más larga la corrida, más probable el rabbit hole" |
| PaperBench | `lectura-de-fuentes` | corte prematuro | — | — | — | — | larga | o1 13.2→**24.4%** solo por sacarle la opción de cortar |
| **OSWorld 2.0** | `lectura-de-fuentes` | estado implícito | **en el tiempo, no anunciada** | ruido vs actualización | — | no | 318 tool-calls, 1.6h | "pierde info que llega a mitad de tarea, tratándola como ruido de fondo" |
| HORIZON | idem | restricción visible violada | — | — | — | no | 200+ pasos | La condición sigue EN contexto y la viola: "desatención, no olvido" |
| SciAgentGym | idem | señal de error | ejecución | — | — | no | multi-paso | Responden a **32.9%** de las señales de error |
| BED-LLM | idem | pregunta que discrimina | respuestas acumuladas | — | — | no | 20 preguntas | Hipótesis **incompatibles con lo ya observado**; empeora al crecer el historial |
| Su & Cardie | idem | adivinar vs preguntar | contexto | ambigüedad | preguntar | no | 1 turno | Detecta 60-80%, pregunta **<5%**; más contexto → MENOS preguntas |
| Chen/Zhao/Cohan | `failure-modes` §1 | movidas de ideación | literatura | — | — | no | 1 idea | Puente 47-64% (vs 12% humano); **el thinking lo EMPEORA** |
| Si/Yang/Hashimoto | `mundos-por-vicio` §4 | mode collapse | — | — | — | 100+ humanos evaluando | — | 4000 ideas → 200 únicas (~5%) |
| **Big-Muddy / Barkett** | `lectura-de-fuentes` | escalada de compromiso | feedback | — | — | **sí: pares simétricos** | 2 etapas | Individual ~0; **pares 99.2%**; identidad fusionada 97.45% |
| Xie et al. | idem | evidencia mezclada | servida | confirmación + contradicción JUNTAS | — | no | 1 turno | Contradicción única → acepta 91-96%; mixta → vuelve a la suya 43-65% |
| Kumaran | idem | obra propia visible | consejo | — | — | asesor | 2 turnos | Cambia 13.1% viendo su respuesta vs 32.5% sin verla; **desaparece si es "de otro LLM"** |
| Jeong | idem | creencia pre-cargada | web | — | buscar | no | 3 tareas | −26.9% búsquedas; informe "fluent and superficially plausible" |
| Pal | idem | confianza vs acción | — | — | — | no | 3 diseños | Apuesta CONTRA su confianza |
| Yang | idem | retractación | error propio conocido | — | — | no | inmediato | Retracta 11-26% |
| Zhang — snowball | idem | compromiso pre-razonamiento | — | — | — | no | 1 respuesta | Se compromete en el **primer token** (95-98%) |
| SycEval | `vicio-1` §1.B | rebuttal en cadena | — | — | — | interlocutor | cadena | 58.19%; **persistencia 78.5%**; el rebuttal CON CITA el más regresivo |
| Hu — piso sin hablante | `lectura-de-fuentes` | contenido vs fuente | afirmación insertada | — | — | variable | 1 turno | Contenedor tipo referencia 80.4%: **persuade PARECER EVIDENCIA** |
| **ScienceAgentBench** | idem | error duro | stack trace | ninguna | — | no | — | **CONTRAEVIDENCIA**: self-debug casi duplica el éxito — el vicio NO vive en la señal dura |
| ImpossibleBench | `vicio-3` §3.5 | reward hacking | — | — | — | no | — | 76% de trampa cuando paga vs 2.9% cuando no |
| Luo et al. | `lectura-de-fuentes` | selección post-hoc | — | — | — | no | — | Cherry-picking 82.4%; auditar solo el informe lo ve 55%, con trazas 82% |
| Jr. AI Scientist | `vicio-3` §3.6 | fabricación reactiva | **pedido del revisor** | — | — | **sí: revisor** | ronda | Inventa ablaciones inexistentes y **el score SUBE** |
| **MORPHEUS** | `lectura-de-fuentes` | reglas que cambian SIN AVISO | **en el tiempo**, persistente | ¿falla puntual o cambio de régimen? | — | no | persistente | Siguen con la política vieja; el reward decae a ~0 sin que lo detecten |
| LHTB | idem | horizonte real | — | — | — | no | **120-320 pasos, ~90 min** | 29/46 nunca resueltas; **79% muere trabajando con el tiempo agotado** |
| Taxonomía de agentes de terminal | `vicio-9` | verificación de paja | test propio | — | ejecutar el verificador | no | — | "Inline Self-Test Over-trust" 29.5% = la firma MÁS frecuente |
| **AUTOCOG** | `lectura-de-fuentes` | loop cerrado con humanos | experimentos en Prolific | — | plata y tiempo real | **sí: 2 teorías + árbitro** | ciclos | POSITIVO: descubre una teoría nueva confirmada en pre-registro |

### A.4 — Casos de NUESTRA propia mesa

| Caso | Fuente | Juntura | Cómo llegó la evidencia | Ambiguo | Costo | Otros | Duró | Qué falló |
|---|---|---|---|---|---|---|---|---|
| **latent_mix v2 — el trofeo** | `vicio-4`; `mundos-por-vicio` §4 | composición latente | comprada | — | 10 líneas de código | no | compacto | **0/10 postulan**; el mejor "técnicamente perfecto" saca 0.096 |
| **count_mix_v0 — 0/9** | [resultado](2026-08-07-resultado-smoke-count-mix-v0.md) | mezcla discreta vs frailty | comprada | discretitud vs dispersión | **11/12 compran el discriminante solos** | no | 6-19 turnos | Capturan persistencia y **0/6 postulan clases**; "mixture" aparece 5/6… siempre como negative binomial |
| count_mix — la comparación que no corre | idem §B1 | test discriminante | — | — | presupuesto sobrante siempre | no | — | **0 de 11 corrieron comparación alguna** |
| count_mix — verificación de paja | [autopsia](2026-08-07-autopsia-canales-de-ayuda.md) | test sin poder | **impresa en su propia salida** | — | mirar su propio histograma | no | — | Imprime el valle y los cuartiles bimodales, **cero comentarios** |
| count_mix nivel4b — comparación mandada | [pre-registro](2026-08-07-resultado-preregistro-canales-vs-wording.md) | orden explícita | — | — | — | no | — | 3/3 obedecen y **0/3 saltan** |
| count_mix — canales de ayuda | autopsia; `vicio-1` §1.C | por dónde entra la hipótesis | pista congelada | — | — | no | — | gpt+mundo 4/4 · gpt+método 1/4 · DeepSeek al revés: **canal × modelo** |
| **count_regime_v0 — DeepSeek 99502** | [resultado](2026-08-07-resultado-smoke-count-regime-v0.md) | quiebre de régimen | **compra MÁS datos del punto anómalo** | outlier vs discontinuidad | ya pagado y confirmado | no | 12 turnos | Confirma, escribe "perhaps piecewise… two segments?" y entrega la suave llamando **"outlier"** al punto confirmado |
| count_regime_v0 — gpt técnico | idem | idem | comprada | idem | — | no | — | "the historical sample at 1.0 was **noisy**… not that the process is discontinuous" |
| count_regime_v0 — DeepSeek 99500 | idem | idem | comprada | idem | — | no | — | Tercer refugio: **interpola los puntos sin postular ley** |
| count_regime_v0 — gpt 99503/99505 | idem | idem | zoom adaptativo | — | — | no | — | ÉXITO PARCIAL (S≈0.65): la conjetura **precede** al zoom |
| rabbit_hole — el 0/60 | `vicio-2` §2.1 | pozo | contabilidad visible | — | — | no | 6×60 | **0 caídas**: des-invierte racionalmente |
| first_story_v0 | `vicio-1` | primera historia | escasez | — | — | no | compacto | gpt 1/8; DeepSeek 0.36→0.89 con advertencia |
| Sondas 0143/0145/0148 | `vicio-1` §Estado | influencia por momento | nota insertada | — | — | par/autoridad simulados | ~376 celdas | Formación **0/19** · medio **0/20** · entrega 8.7-26% |
| North heterogéneo | `roadmap` | mezcla 75/25 | campaña propia | — | — | no | — | **4/4 aplanan la mezcla en una Normal ancha** |
| Topología visible vs latente | `roadmap` | partición | mismas 80 filas | — | un ajustador cero-LLM la elige por BIC | no | — | Visible 83-95%; **LATENTE ≈0 aun releyendo sus outputs** |
| Propagación frontier | `roadmap` | revisión→acción | reporte | — | — | no | — | Asimila y **deja vieja la decisión dependiente 4/6** |
| WAGER mismo (ADR 0152/0161) | `vicio-1` | alcance del claim | resultado local propio | — | la contradicción estaba comprada | Lucas (lo cazó) | — | Promovimos un hallazgo local a conclusión general |
| Auditoría del slice count_mix | [auditoría](2026-08-07-auditoria-critica-slice-count-mix.md) | diseño del mundo | revisión | — | — | Lucas (las preguntas) | — | A1 stakes vacíos · A2 no paga en extrapolación · A3 ancla débil |

---

## B. LOS EJES DE COMPLEJIDAD REAL QUE NUESTROS MUNDOS NO TIENEN

Cada eje sale de la tabla A. Formato: **evidencia · casos · juntura que habilita medir**.

**B1 — El modelo tiene PIEZAS separables, no una curva.** Darden: el cambio de teoría es edición
incremental y localizada de componentes modulares, y **sin modularidad no hay localización**
(p.272). Su Tabla 15-3 da 8 verbos + agregar + monster-bar + narrow-scope + shelve + abandon:
**rúbrica ordinal completa, computable cero-LLM** sobre el diff. *Juntura*: el **verbo de edición**
y el **sitio** — hoy la submission es un programa monolítico y solo medimos "acertó/no".

**B2 — La anomalía tiene FIRMA que localiza la pieza culpable.** "El 2:1 no solo guió la
localización, también guió la naturaleza de los cambios… si hubiera sido 1:1, las hipótesis
habrían sido distintas" (Darden p.105), con su límite declarado ("no era suficiente"). Converge
con Ohlsson: la señal binaria no informa; la información está en la naturaleza CUALITATIVA del
error (pp.222-228). *Juntura*: **dirección de la revisión** — es el tercer brazo ya ratificado,
pero hoy solo existe en un mundo de una sola pieza.

**B3 — Ambigüedad instrumento-vs-mundo CON COSTO de desambiguar.** En las cuatro tradiciones a la
vez: Onnes ("cortocircuito del equipo"); Darden pone confirmar-la-anomalía como paso 1 obligatorio;
Dunbar da el gate duro (**si cree que es error, ningún desafío lo mueve**); y nuestros propios
especímenes usan literalmente esa salida ("noisy", "outlier"). *Juntura*: la firma de tres estados
— descartar-sin-replicar / replicar-confirmar-y-descartar-igual / replicar-y-perseguir. **Hoy el
agente no puede creer que es el aparato**: la excusa más usada por humanos y agentes reales ni
siquiera es jugable en nuestros mundos.

**B4 — Evidencia que llega EN EL TIEMPO con una decisión que no espera.** KellyBench (7/25 nunca
reentrenan), MORPHEUS (siguen con la política vieja), OSWorld ("trata la info nueva como ruido de
fondo"), Jeong (la creencia curva la POLÍTICA antes que el output). Doctrina propia:
`failure-modes` §2 principio 4 — *"la maquinaria de eventos (D4) casi sin usar"*. *Juntura*:
conversión evidencia→acción bajo compromiso ya ejecutado + el knob **recurrencia** (n=1 es
barrable como monstruo; la clase que reaparece obliga a editar).

**B5 — Más de una estructura escondida (rivales que no colapsan).** La compuerta 6 de la ficha v1
ya lo exige; Darden documenta 4 hipótesis simultáneas sobre 4 pasos distintos (p.202) **y el
hallazgo negativo**: *"No one scientist systematically generated a large set of competing
hypotheses"* (p.277); Heuer: menú "woefully inadequate". Estado real: `count_mix_v0` y
`count_regime_v0` instalan **UN** operador cada uno, contra la regla de 2-4 de
`reference/operators.md` §3. *Juntura*: **cardinalidad y diversidad del menú generado** — separa
"no se le ocurre" de "se le ocurre una sola cosa".

**B6 — Otros agentes: crítica, revisión, propiedad de la teoría.** Apunta en **dos direcciones
opuestas**, lo que la vuelve diseñable: a favor, Dunbar (el corrector es el meeting) y Ohlsson
(p.157, la crítica mutua está "well supported"); en contra, Barkett (pares simétricos **99.2%** de
escalada), Jr. AI Scientist (el pedido del revisor produce fabricación y **sube** el score);
Findley & Scott: lo que sí funciona es el **fresh look SIN propiedad de la teoría**. Estado:
**ningún mundo, vivo ni archivado, tiene otro agente**.

**B7 — Teoría HEREDADA de otro.** Kumaran: el aferrarse **desaparece** si le dicen que es de otro
modelo — "es identidad, no contenido". Kepler heredó los datos de Tycho; Lotka-Volterra, 90 años
de registros; Hurst, 800 años de crecidas. `vicio-2` §2.2 lo declara **"NUNCA probada"** y ya tiene
el diseño escrito (aleatorizar SOLO la historia, mismo estado presente).

**B8 — Verdad DIFERIDA y consecuencia que se cobra tarde.** Graber: la verdad la revela la
autopsia. Findley & Scott: mundos donde el error parece no cobrarse a corto plazo — por eso el
vicio persiste en profesionales. *Nota*: es el único eje **sin firma cero-LLM resuelta** → motivo
para postergarlo.

**B9 — Presupuesto que compra COSAS DISTINTAS.** Heuer regala la métrica: **diagnosticity** — la
evidencia consistente con todas las hipótesis vale cero, y en nuestros mundos P(dato|H1) vs
P(dato|H2) es **computable exacto server-side**. Aliseda da la base formal (los hechos
no-sorprendentes no son problema abductivo). Y nuestro dato propio: el shopping **no es el cuello**
(11/12) — un mundo con un solo tipo de compra ya no informa.

**B10 — Ruta periférica abierta y CON DEUDA.** Ohlsson: "peripheral change… path of least
cognitive effort" (p.327); Aliseda formaliza el costo asimétrico (expandir = colgar una hoja;
contraer = reconfiguración en cascada). Es la **compuerta B (tripwire mayor)** ya ratificada.
*Juntura*: **contracción vs expansión** — "¿retractó algo?" es más nítido que "¿actualizó?".

**B11 — El tipo de disparador: anomalía vs LAGUNA.** Aliseda parte los disparadores en tres
estados computables (éxito / anomalía / **laguna**: la teoría no opina nada). En la laguna no hay
contradicción que resolver: el agente solo puede EXTENDER. *Juntura*: **separa experimentalmente
generar de soltar** — las dos líneas del programa, con respaldo formal.

---

## C. QUÉ EJES YA ESTÁN CUBIERTOS (para no reconstruir)

| Eje | ¿Cubierto? | Mundo / límite |
|---|---|---|
| Estructura latente escondida (una) | ✅ | `latent_mix_v2` (0/10) · `count_mix_v0`+twin (0/9) · `count_regime_v0`+twin; gemelo certificado en los tres |
| Evidencia COMPRADA con presupuesto | ✅ | Todos los mundos vivos. Y el dato: **no es el cuello** (11/12) |
| Compromiso propio registrado | ✅ parcial | Verbo `register` en `count_mix_v0`/`count_regime_v0`; estrenado en `lab_largo_v0` (archivado) |
| Anomalía visible que grita | ✅ (y es el piso) | `count_regime_v0`: midió ACEPTACIÓN |
| Anomalía no flagrante + impasse ingeniado | 🟡 diseñado, no construido | ficha v1 + addendum ratificado — próximo paso vigente |
| Causalidad / confounding / selección | ✅ (5 mundos, control) | `confounded_gen_v0`, `selection_bias_v0`, `dummy_dose_v0` + archivados |
| Sesgo del observador (op 7) | 🟡 parcial, como sesgo a corregir | `selection_bias_v0` tiene `error_de_medicion` + `replicas_calibracion`. **Falta como hipótesis rival de una anomalía** |
| Transferencia estructural | ✅ | `overgen_stream_v0` + twin |
| Primera historia / rigidez | ✅ control | `first_story_v0` |
| Pozo / overstay | ✅ **cerrado** | 0/60 en frontier; `vicio-2`: "no construir más contra esto" |
| Horizonte largo con estado propio | 🟡 quedó corto | `lab_largo_v0`: corto en TOKENS, no en rondas (≥100k útiles) |
| Evidencia por eventos | 🟡 maquinaria sí, uso no | `events` presente y sin usar |
| **B1 piezas separables** | ❌ | ningún mundo tiene submission modular |
| **B2 firma que localiza** | ❌ | un solo operador → no hay "dónde editar" |
| **B3 instrumento-vs-mundo** | ❌ | el ruido es de muestreo; no se puede culpar al aparato |
| **B4 decisión periódica** | ❌ | todos terminan en un único `submit` |
| **B5 ≥3 estructuras vivas** | ❌ en los mundos de saltos | 1 operador, contra la regla de 2-4 |
| **B6 otros agentes** | ❌ | cero mundos; diseño anotado sin construir |
| **B7 teoría heredada** | ❌ | "NUNCA probada" |
| **B8 verdad diferida** | ❌ | el score se computa al final |
| **B9 diagnosticity** | ❌ como métrica | 1 fuente observacional en casi todos |
| **B10 ruta periférica con deuda** | 🟡 diseñada (tripwire) | nunca implementada |
| **B11 mundos tipo-laguna** | ❌ | familia futura registrada |
| Vicios 3, 8, 9: mundos dedicados | ❌ cero | `mundos-por-vicio` §Estado global |

---

## D. TRES CANDIDATOS DE MUNDO REALISTA (ordenados por valor/costo)

### D1 — "El turno de calibración": la anomalía que puede ser el aparato

**Caso ancla**: Onnes 1911 — el laboratorio descarta la superconductividad como *cortocircuito del
equipo*. Anclas secundarias: Darden paso 1 (confirmar la anomalía: reproducir / reanalizar) y el
gate de Dunbar (si cree que es error, ningún desafío lo mueve). Especímenes propios que ya usan
esa salida: *"the historical sample was noisy"*, *"maybe the true mean is an outlier"*.

- **Salto**: op 7 (proceso del observador) como **hipótesis viva DENTRO del episodio** + op 3 o 2 en el polo-mundo.
- **Ejes**: B3 · B5 · B9 · parcialmente B2.
- **Qué mide** (cero-LLM): la firma de Dunbar en tres estados · **diagnosticity del gasto** (canal vs mecanismo, computable exacto) · entrega contra batería y gemelo bilateral (en el gemelo la anomalía SÍ es el instrumento y corregirla es la jugada ganadora).
- **Costo**: BAJO. `error_de_medicion` y `batch_effect` ya están en la librería; `selection_bias_v0` ya tiene la doble fuente. Lo nuevo: el operador de canal como **candidato explicativo**, réplica <10% del presupuesto (ya es compuerta 5), y certificar que ningún candidato saca ΔBIC≥6 en el punto de la anomalía (compuerta 6 escrita).
- **Riesgo**: que degenere en aritmética (si comprar la calibración es obviamente lo próximo, mide un checklist). Mitigación: la réplica es una entre varias compras razonables y su necesidad no está señalizada.

### D2 — "El modelo heredado en piezas": anomalía con firma sobre una teoría de otro

**Caso ancla**: Darden cap. 8 — la anomalía 2:1 sobre la teoría mendeliana heredada; el patrón
numérico **localiza el paso a editar** y las 4 hipótesis históricas corresponden a los 4 pasos del
proceso (p.202). Secundario: Graber (82% síntesis sobre un cuadro que el médico no generó).

- **Salto**: la **escalera ordinal completa** de Darden, incluidos los dos operadores que no tenemos (SPLIT/DELINEATE y BORRAR).
- **Ejes**: B1 · B2 · B7 · B5 · B10.
- **Qué mide**: rúbrica ordinal cero-LLM sobre el diff contra el modelo heredado (qué verbo, sobre qué componente) · ¿localizó el componente correcto? · el **conjunto** (cuántas alternativas en cuántos sitios) · entrega en el régimen no visitado.
- **Costo**: ALTO — exige **contrato de submission modular** (hoy la entrega es monolítica y `reference/world-model.md` §1 no contempla componentes).
- **Riesgo**: que la modularidad **regale la respuesta** (listar 6 componentes = menú de 6 opciones = repartir, no agrandar — la advertencia de Boden con el geometry-program). Mitigación obligatoria: al menos una falla cuya única solución exige **explicitar un supuesto que el brief nunca enunció**.

### D3 — "La línea que corre": evidencia en el tiempo, decisión que no espera, y un colega que critica

**Caso ancla**: KellyBench (temporada, apuesta obligatoria por fecha, tres autocríticas y cero
corrección) + MORPHEUS + el componente social con sus dos direcciones (Dunbar a favor, Barkett en
contra, Findley & Scott con el fresh look sin propiedad).

- **Ejes**: B4 · B6 · B8 · B10. Fenómeno primario: **conversión diagnóstico→acción**.
- **Qué mide**: brecha escrito-vs-hecho (el `register` ya existe) · tasa y latencia de reajuste · efecto causal del crítico-robot **sin propiedad** vs par-que-valida.
- **Costo**: MUY ALTO (bucle periódico con estado, colega-robot, horizonte ≥100k tokens útiles).
- **Riesgo**: **duplicar lo publicado** (KellyBench y MORPHEUS ya lo midieron) y **medir operación en vez de juicio** — con 500-1000 tool-calls la falla más probable es perder el hilo, que `failure-modes` §2 principio 8 prohíbe explícitamente.

---

## E. ADVERTENCIAS — qué complejidad NO agregar

- **E1 — La regla madre**: la AUDITORÍA FUNDAMENTAL DEL MUNDO (`roadmap.md`, Lucas 2026-08-02):
  declarar qué fenómeno produce naturalmente, qué ejes están materialmente presentes,
  **complejidad cognitiva real —no cantidad nominal de filas—**, y qué explicación del mundo/interfaz
  competiría con una falla del agente. *"Un mundo pequeño puede ser un buen microscopio, pero sus
  resultados no autorizan claims que el episodio no instancie."*
- **E2 — NO agregar volumen**: medido tres veces que no compra nada (800 filas con LLR=0 → "NULO,
  NO ESCALAR VOLUMEN"; "no seguir agregando filler"; "South→North no es una investigación larga
  aunque tenga 1.700 filas: son 5-16 decisiones"). Si igual se agrega texto, Context Rot obliga a
  igualar posición/coherencia/similitud entre brazos.
- **E3 — NO agregar complejidad que se pueda fallar por perder el hilo** (`failure-modes` §2
  principio 8): si un mejor andamiaje lo arregla, no es nuestro.
- **E4 — NO agregar estructura que el reward no pueda separar** (`reference/certificates.md` §7,
  Visibilidad): agregar una 2ª o 3ª estructura oculta obliga a certificar visibilidad **de cada
  una**, no del conjunto.
- **E5 — NO agregar estructura que no pague en el régimen no visitado** (`ahas.md`, ADR 0150): "el
  camino real es anti-MDL… si el mundo paga por fit del régimen visitado, el parche-Vulcano gana
  siempre". Es la falla A2 que ya nos costó un slice.
- **E6 — NO cobrar los andamios intermedios** (Nersessian): solo la adecuación final cobra; y
  **"sin hipótesis" debe ser estado legal y registrable** (Klahr & Dunbar).
- **E7 — NO soltar todas las restricciones a la vez** (Boden p.95): un mundo con siete ejes nuevos
  simultáneos no es más realista, es irreconocible — y su resultado no será atribuible a ninguno.
- **E8 — La tensión Scope / Multiple Difficulties** (Ohlsson pp.120/122) tira en direcciones
  opuestas: agregar ejes **de a uno**, con brazos apareados, pre-registrando cuál principio se testea.
- **E9 — NO poner un LLM en el reward**, ni para clasificar la operación. Todo eje entra con su
  firma cero-LLM: B1/B2 la tienen (rúbrica sobre el diff), B3 la tiene (tres estados de Dunbar),
  B6 la tiene (diff pre/post desafío); **B8 no la tiene resuelta** → postergarlo.
- **E10 — El realismo NO es fidelidad de fachada: es fidelidad de CONDICIONES** (regla dura de
  Lucas 2026-07-13). Un mundo con más piel industrial y las mismas junturas no es más realista.
- **E11 — Hindsight sobre nosotros mismos** (Findley & Scott): pre-registrar qué cuenta como
  "anomalía racionalmente descartable" ANTES de mirar la corrida — y ese pre-registro debe CRECER
  con la complejidad, o la autopsia se vuelve narrativa.

---

## Addendum 2026-08-11 — muchos turnos solo si el mundo los necesita

**Pregunta de Lucas:** ¿WAGER puede sostener una investigación interactiva de 30 o más turnos?

**La maquinaria sí.** El kernel conserva variables y modelos; los lotes mantienen identidad; hay
acciones con demora, calendario de eventos y modelos registrados que el mundo puede usar. El máximo
de turnos es configurable.

**Los mundos actuales no.** Se agotan en 5-8 turnos porque contienen una pregunta escondida, dos o
tres compras que la resuelven, evidencia inmediata, verdad fija y un solo nivel de mecanismo. Subir
el límite a 50 solo agregaría tiempo vacío.

Un mundo largo debe volver necesarios los pasos: evidencia que llega gradualmente; preguntas
encadenadas donde una respuesta abre la siguiente; un mecanismo que cambia durante la partida;
señuelos que cuesta descartar; un interlocutor guionado y mecánico; y análisis con demoras distintas
que obligan a planificar. No hace falta usar todas las palancas juntas.

**Regla de diseño:** la duración se deriva de dependencias reales del mundo, no de fijar un número
alto de turnos. Hay que agregar los ejes de a uno y comprobar que seguimos midiendo juicio, no olvido
o desorganización. D3 (“La línea que corre”) es la familia natural para esta dirección. Sigue abierta
la decisión de terminar primero el microscopio D2 o pasar antes a un primer slice largo.

---

## Nivel arriba

- **Aprendizaje real**: no es "faltan ejes". Es que **el corpus documenta un fenómeno acompañado,
  largo y ambiguo, y nuestros mundos instancian uno solitario, corto e inequívoco**. Los tres ejes
  que aparecen en las CUATRO tradiciones a la vez (histórica, cognitiva, profesional y de agentes)
  son **B3 (instrumento-vs-mundo), B5 (menú de rivales) y B6 (otro que critica)** — y ninguno está
  en ningún mundo nuestro, vivo o archivado.
- **Límite del claim**: esto es un mapa de ausencias derivado de la tabla A, no evidencia de que
  agregarlos produzca el fenómeno.
- **Explicación rival**: que la ausencia de esos ejes sea consecuencia y no causa — los
  construimos chicos porque el fenómeno **sí** aparecía en chico (0/9 en count_mix).
- **Consecuencia si el próximo mundo agrega ejes y el fenómeno DESAPARECE**: eso también es un
  resultado — querría decir que lo que medíamos era artefacto de la miniatura.
