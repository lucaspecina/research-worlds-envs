# Red-team — modos de falla conocidos y defensas

> Registro vivo de los ataques al proyecto y sus defensas (ex NORTH_STAR §7).
> Las citas '#N' de otros docs y ADRs refieren a los ataques numerados acá.
> `[ESTABLE como registro; ampliar siempre]`

| # | Ataque | Mecanismo | Defensa | Estado |
|---|---|---|---|---|
| 1 | **Nihilismo semántico** | Pieles randomizadas enseñan a ignorar todo prior de dominio | Perilla de confiabilidad de priors (`docs/archived/NORTH_STAR_full.md` §4.1) | Diseñada |
| 2 | **Pipeline maestro** | Un pipeline de sysID reusable scorea alto sin juicio | Presupuesto/complejidad ajustado + brecha de adaptividad + coevolución + operadores abiertos | Diseñada; carrera armamentista, no fix |
| 3 | **Gemelo obeso** | Simulador inflado que predice sin explicar | Término λ·MDL en el score | Diseñada; medir MDL es open question |
| 4 | **Ruido del reward** | Distancias muestrales tienen varianza; RL con reward ruidoso aprende mal | Muchos ítems, seeds apareados, n grande, repeticiones | Estadística conocida; laburo real |
| 5 | **Puntos ciegos de D** | El agente vive donde la distancia elegida no ve. v0.16: en el dummy la energía pesa las marginales y subpesa el joint. **Avistamiento DECISIVO (v0.25, Latent)**: la energía sobre marginales casi no ve multimodalidad a momentos fijos — un oráculo Gaussiano unimodal saca R=0.96 contra una verdad máximamente bimodal → la heterogeneidad latente es invisible al reward. | **Cazado por el certificado ANTES de entrenar** (el `theory_gap_probe` con el control oráculo). **Fix (ADR 0026): score COMBINADO** = energía + funcionales de decisión declarados en stakes (`docs/reference/scoring.md` §9.3) + **certificado de Visibilidad** (`docs/reference/certificates.md` §7: toda estructura instalada debe separarse en el reward, o el mundo se rechaza) + el probe como diagnóstico permanente de fábrica (gap energético vs combinado). | **Realizado y mitigado** — el certificado cumplió su función |
| 6 | **Designer gotcha / baseline espantapájaros** | Brechas infladas por mundos-acertijo o baselines débiles | Baseline asociacional fuerte + filtro LLM de plausibilidad (fábrica) | Diseñada |
| 7 | **Leer el código del mundo** | El agente hace `cat` del programa | Handle opaco server-side | Requisito duro de implementación |
| 8 | **Goodhart sobre la batería** | Si la distribución de regímenes es angosta, el template vuelve por la ventana | Randomización rica + off-support + differential testing + cola de auditoría | **Punto de presión #1; vigilancia permanente** |
| 9 | **Inestabilidad RL multi-turno** | Régimen documentado de problemas de estabilidad/generalización | Stack y recetas de la literatura; no innovar acá | Riesgo asumido |
| 10 | **Scope: el medio, no las puntas** | "Mi cuello de botella es elegir problemas/comunicar" | Decisión explícita (`docs/archived/NORTH_STAR_full.md` §2.9); la evidencia dice que el medio está roto | Asumido y declarado |
| 11 | **Sorpresa fabricada (contrarian)** | Si todos los mundos son raros, el meta es "la respuesta siempre es la contraintuitiva" | Base rate de sorpresa vía perilla de priors; curriculum mayormente confirmatorio; la sorpresa se gana con evidencia | Diseñada |
| 12 | **Goodhart del loop maestro** | Rediseñar hasta que los traces *parezcan* ciencia, en vez de hasta que la ciencia sea óptima | Actuadores = brechas y economía del juego, jamás rewards conductuales; E3 (familias held-out) como control externo | Disciplina declarada (`docs/archived/NORTH_STAR_full.md` §2.1) |
| 13 | **Cobertura de rivales / rivales débiles** | Malentendidos no encarnados pesan poco; un gemelo inocente degenerado corrompe los pesos de la batería *en silencio* — el sistema corre, los scores salen, la relevancia apunta a cualquier lado | Cola de auditoría + rival ingenuo siempre presente + **escalera de verdades degradadas** (certificado de monotonía por mundo, automático) + **auditoría humana de baterías** en E1 | Punto a vigilar; OQ #11 |
| 14 | **Techo de lo comprensible** | La profundidad efectiva del entorno está acotada por los malentendidos que el diseñador anticipa: discriminación autorada, dificultad inyectada ≠ dificultad emergente; riesgo de destilar la epistemología del generador en el solver | Rivales por optimización (receta d: malentendidos descubiertos por búsqueda, no imaginados) + cola de auditoría + brechas computadas. **Mitigación parcial — límite declarado, no resuelto** | Abierto; el más profundo |
| 15 | **Economía de diversidad / problema del mix** | Millones de episodios aprenden *al generador* (un adversario más débil que la naturaleza); la diversidad significativa está acotada por autoría de familias; al 1% de un mix de RL el delta es inmedible → catch-22 de adopción para training | Producto de entrada = eval + demo obs→experimento (transfer evidence producida por nosotros); familias paramétricas + operadores abiertos; training = fase dos | Estratégico; redefine la secuencia de adopción |
| 16 | **Contaminación por fama de la semilla** | Las semillas documentadas viven en el pretraining: el solver recupera la moraleja de memoria sin investigar — el modo con semilla, en su versión más fiel, viola la invariante "forzar investigación" | Test de contaminación obligatorio (brecha de prior > umbral para casos investigativos con semilla) + trasplante cruzado de dominio por defecto + tasa de novedad estructural como métrica de salud del pipeline | Diseñada |
| 17 | **Confound juicio-vs-ejecución** | El instrumento mide saber pandas, no juicio: un modelo torpe con herramientas scorea bajo aunque juzgue bien | Mundos de control sin trampas + perfil condicional a la ejecución + baseline humano (E1.4–5) | Diseñada |
| 18 | **El juez vuelve por la puerta de atrás** | En implementación, la tentación de "que un LLM chequee si la submission es razonable" en algún rincón del scorer | **Test de CI cero-LLM en el reward path**: el build falla si se viola — disciplina convertida en código | Regla de CLAUDE.md |
| 19 | **Ergonomía diferencial del contrato** (primo del #17) | Una fricción model-family-specific (p.ej. una elección de RNG legítima que el instrumento no tolera) se disfraza de spread de juicio: el modelo crashea en silencio → D_MAX → R=0, indistinguible de "juzgó mal". **Avistado empíricamente** (Decision Log v0.16: DeepSeek con `np.random.seed` legacy + seeds de 64 bits) | Smoke con seeds/regímenes representativos (hecho); **breakdown crash-vs-distancias-honestas POR MODELO como default del reporte**; conformance separado de juicio en E1 | Diseñada; vigilar |
| 20 | **Búsqueda bruta contra el verificador** (primo del #2, con precedente EXTERNO duro) | La lección AtCoder Heuristic 2025→2026: donde hay corrector ejecutable barato + generador de instancias + examen fresco, "búsqueda masiva contra el verificador + destilación" pasó de perder por 5.5% contra el campeón humano a ganarle **7×** en DOCE meses — sin ingeniería de dominio. Si un mundo nuestro se puede ganar "buscando sin entender", el RL lo va a encontrar y el score deja de medir juicio | La defensa ESTRUCTURAL que AHC no tiene: nuestro mundo está OCULTO y el feedback en-mundo es CARO (cada experimento cuesta presupuesto; no hay simulador local gratis de la verdad — el agente solo puede buscar contra sus propias creencias, que es justamente el cuello epistémico). Complementos: presupuesto ajustado en [T] + baselines destructores (BOED/AutoML, ronda 2 de Codex) ANTES de llamar "juicio" a un mundo + panel de conducta de la fábrica | Registrada 2026-07-10; conecta con #2 y con los baselines de Codex |

---

## Supuestos que cargan el edificio `[VIVO — semáforo con alcance; revisar al cerrar cada experimento]`

> Complemento del catálogo de ataques de arriba (aquello es *quién nos ataca*; esto es *qué asumimos
> que, si es falso, tumba el piso*). Pedido por Lucas (2026-07-11) tras el fork (ADR 0134) y el probe
> de traducción (ADR 0136); revisado por Codex r13 (crudo en
> `docs/research/2026-07-11-codex-ronda13-critica-mapa-supuestos.txt`). Reglas de la tabla (r13):
> el estado JAMÁS sin alcance (un verde local no es una propiedad del sistema) · una proposición por
> fila · "tenemos mitigación" no cuenta como evidencia · estados: ✅ verde (probado en ese alcance) ·
> 🟡 amarillo (parcial/vigilado) · 🔴 rojo (falsado o bloqueante) · ⬜ gris (no probado aún).

**La cadena causal que todo lo demás asume** (el probe 0135/0136 volvió verde UN tramo — la entrega):

`mundo recuperable → vicio vivo en el modelo → la investigación cambia la creencia → la entrega la conserva → la batería la cobra → la señal es aprendible → transfiere`

| ID | Supuesto (falsable) | Alcance | Estado | Evidencia | Próximo falsificador | Si falla |
|----|--------------------|---------|--------|-----------|---------------------|----------|
| S1a | La implementación de la verdad es correcta (world.py sin bugs; determinismo) | por mundo; probado en los 11 hechos | ✅ | certificados + replays byte-exactos (fork 60/60) | escalera de degradadas en cada mundo nuevo | todo lo medido es ruido |
| S1b | Los regímenes de la batería son científicamente relevantes | por mundo | 🟡 | auditoría humana NO sistemática (E1.7 pendiente) | auditar los ~10 regímenes de mayor peso por mundo | nota sobre preguntas sin sentido |
| S1c | La verdad es RECUPERABLE con el presupuesto y fuentes legales (identificabilidad) | por mundo | 🟡 | gates de recuperabilidad existen; no re-verificados contra conducta real | robot cuidadoso scriptado alcanza R alto con presupuesto legal | el examen no tiene respuesta alcanzable |
| S2 | El vicio del mundo está VIVO en el modelo evaluado (apareamiento mundo×modelo) | por par | 🔴 first_story×DeepSeek (falsado: 15/16 investigan bien) · ⬜ resto | ADRs 0129/0130/0134 | chequeo causal por par: firma objetiva + tasa basal + asociación con R (bloques temporales, no n=8) | el mundo no mide nada para ese modelo |
| S3 | Los rivales representan las historias equivocadas REALES de los modelos | por mundo | 🔴 first_story (forma-reducida/defaults/ruido-inflado no están como rivales) · 🟡 resto | ADRs 0134/0136 (conducta real medida) | derivar rivales desde los defectos frecuentes medidos | certificados contra fantasmas |
| S4 | La batería COBRA los defectos conductualmente grandes | por mundo | 🔴 first_story, con receta | audit D59: comprime 143× en 13 milésimas (ADR 0136; `scripts/out/probe_0135/audit_d59.json`) | regímenes histórico+extremos con peso; re-certificación | nota alta con razonamiento podrido |
| S5 | La GEOMETRÍA del score preserva orden/magnitud/dirección (normalización, D_MAX, agregación) | global | 🔴 | la batería PREMIA sobre-varianza (fix-ruido baja R 0.9866→0.9793) | red-team adversarial del score; gate: ningún aumento de varianza mejora R | RL aprende el hack; el orden se invierte |
| S6 | Anti-leak: el brief/nombres no soplan la trampa | por mundo; reabre con la fábrica | ✅ vigilado | writer ciego + señuelos + probe del generador | probe de leak en cada mundo generado | medimos lectura de pistas |
| S7 | Anti-contaminación: el modelo no se sabe la respuesta | por mundo; CRÍTICO en vía Tübingen | 🟡 | test + trasplante de dominio (doctrina) | baseline SIN datos por mundo (si completa sin investigar = memoria) | scores = recuerdo |
| S8 | Los precios crean la presión correcta (escasez calibrada) | por mundo, dial permanente | 🟡 | A-escasa (ADR 0087): la escasez cambia conductas | barrido de presupuesto en certificación | no hay decisión que medir |
| S9 | El harness no mete fricción no-epistémica | DeepSeek-grande × first_story × DeliverySpec-v1 | ✅ local (75/75 limpio) · 🟡 global | probe 0135 etapa 1 | repetir chequeo mecánico por modelo/mundo nuevo (ataque #19) | medimos manejo de herramientas |
| S10a | Simulador/replay/reward deterministas por seed | global | ✅ | 60/60 + 75/75 byte-exactos | ODEs stiff de la vía Tübingen | nada es auditable |
| S10b | El comportamiento del PROVEEDOR es estable/estimable | por proveedor | 🟡 | 3 corridas idénticas con signos opuestos (ADR 0129); los bloques ESTIMAN la deriva, no la eliminan | monitoreo de deriva entre bloques en cada experimento | conclusiones aleatorias |
| S11 | La entrega CONSERVA la creencia (el canal) | DeepSeek-grande × first_story × creencias explícitas | ✅ local (45/45; orden 5/5) · 🟡 4-8B de E2 y simuladores complejos | probe 0135 (ADR 0136) | probe reducido (verdad+intermedio+folklore, 10-15 bloques) en el 4-8B ANTES de E2 | la nota mide traducción, no juicio |
| S12 | El puente investigación→creencia (mejor investigar ⇒ mejor creencia, y la diferencia llega a R) | por par | 🔴 first_story×DeepSeek (investigaron bien, creencias defectuosas igual) · ⬜ general | fork (ADR 0134): defectos epistémicos post-investigación | mundo×modelo con vicio vivo + firmas de creencia estructuradas (vía belief/spec de r12) | el RL no puede mejorar lo que la nota no distingue |
| S13 | La nota no es hackeable (gaming del score) | bloqueante para E2; en E1 solo diagnóstico en cuarentena | 🔴 | premio a sobre-varianza = hack disponible; oracle-gamer (ADR 0092) | mismo red-team de S5 + baselines destructores (ataque #20) | se entrena el hack |
| S14 | Cero-LLM en el reward path | invariante de INGENIERÍA (no evidencia de validez) | ✅ | test de CI que rompe el build | — (se mantiene por construcción) | reward no auditable |
| S15 | El catálogo apunta a vicios que importan afuera | estructural; ojo circularidad (defectos internos ∈ catálogo no valida importancia externa — r13) | 🟡 | fuentes a texto completo; convergencia interna | validez convergente E1.6 (otros benchmarks) + baseline humano | cazamos vicios irrelevantes |
| S16a | La fábrica produce mundos VÁLIDOS sin humano (yield mecánico) | plantilla actual | ✅ limitado | 5/5 ALL-PASS (ADR 0131) | repetir por plantilla nueva | no escala |
| S16b | La fábrica produce DIVERSIDAD estructural | plantilla actual | 🔴 | colapso medido (ADR 0131): pearson≈1.0, dominios repetidos | arreglo dado+dominios dirigidos + panel conductual | el entrenamiento aprende al generador (ataque #15) |
| S16c | Los mundos generados son válidos como instrumentos (no solo internamente consistentes) | por mundo generado | 🟡 | cuarentena + auditoría (ADR 0119) | auditoría humana de batería por mundo generado | instrumentos corruptos en masa |
| S17 | Generalización DENTRO de WAGER (lo aprendido sobrevive a estructuras nuevas, no solo re-skins) | pre-E3 | ⬜ | el micro-batch mostró duplicación conductual | probes de transfer in-context entre estructuras (barato, sin entrenar) | E3 muere antes de empezar |
| S18 | La señal es aprendible por RL (densa, estable) | E2 | ⬜ condicionado a S4/S5/S11/S13 | — | E2 chico tras endurecer el score | máquina de templates (muerte parcial E2) |
| S19 | El juicio transfiere entre familias (la hipótesis central) | E3 | ⬜ por diseño | criterio de muerte propio (roadmap E3) | E3 | queda un benchmark, no un método |
| S20 | Sim2real (predice experimentos reales) | E4 | ⬜ por diseño | controles diseñados (roadmap E4) | E4 | el titular no llega |

**Los 3 falsificadores prioritarios (r13, en orden)**: (1) **red-team adversarial del score** (S4/S5/S13:
barrido de ruido alrededor de la verdad, D59 reparado/no, defaults, mediadores, flechas inventadas; gate:
ningún aumento de varianza independiente puede mejorar R, y cada defecto conductualmente grande pierde más
que el piso numérico, estable entre seeds) · (2) **probe reducido en el 4-8B real de E2** (S11) · (3)
**chequeo causal mundo×modelo formalizado** (S2: firma objetiva del vicio + tasa basal con headroom +
asociación con R, por bloques temporales — nunca n=8).

**Nota Tübingen (sellada con las correcciones de r13)**: ModelSMC NO es plan B del formato (usan el mismo
formato entrega=programa; evalúan por likelihood marginal vía TabPFN — si el formato fallara, les fallaría
igual). Para WAGER es: (a) **cantera de mundos** — *"cantera sí, realidad no"*: son simuladores publicados,
no naturaleza; su verdad es la del modelo de referencia; (b) **model-repair como TAREA** legítima pero
estrecha (mide reparación dentro-de-clase, no descubrimiento abierto; exige baseline sin-datos contra
memoria/completado rutinario); (c) su **likelihood marginal NO castiga sobre-varianza automáticamente**
(surrogate aprendido: sigue siendo cero-LLM pero ya no "reward puramente mecánico", y también es
explotable) → candidata de certificación COMPARATIVA junto a proper scoring rules y barridos explícitos de
varianza — no solución asumida. El plan B real si el canal falla en el 4-8B: la **vía declarativa** (spec
estructurado + compilador propio), NEUTRAL respecto de la estructura científica (si entrega los slots
causales correctos, deja de ser formato y empieza a soplar la hipótesis).
