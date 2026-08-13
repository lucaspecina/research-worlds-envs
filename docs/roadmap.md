# Roadmap y estado — WAGER

> **Dónde estamos, la cartera de mundos, y el plan de validación E1→E4.** La sección
> *Estado actual* se mantiene al día cada sesión; el resto es el plan estable. Los
> resultados detallados de cada hito están en `docs/adr/`; lo sin decidir en
> `docs/open-questions.md`.

## Estado actual `[VOLÁTIL — mantener al día]`

> **OPERATIVA DE EQUIPO (ADR 0172):** Codex supervisa la dirección científica y mantiene el mapa;
> Claude trabaja como worker persistente de implementación, ejecución y contrapunto. Roles,
> enforcement y canal: [`docs/operativa-codex-claude.md`](operativa-codex-claude.md).

> **NOMENCLATURA VIGENTE (ADR 0179; refina 0178):** toda corrida se presenta desde el salto
> hacia abajo: **experimento · mundo · tarea · condición · agente · instancia del mundo ·
> semilla**. Un experimento construye un mundo+tarea+puntaje donde el salto permite encontrar el
> modelo bueno; su pregunta principal siempre es si el agente lo descubre y realiza. Antes se
> resuelven preguntas de diseño sobre necesidad, evidencia, tarea y puntaje. Después, avisos,
> presión y consecuencias pueden responder subpreguntas científicas. Nombre humano:
> `Salto — situación investigativa`; ID: `exp__salto__situacion__vN`. `D1/D2/P1/P2`, “brazo” y
> “polo” quedan solo como alias históricos; ningún pedido de GO usa esos códigos como título. Explicación
> en llano: [WIKI §3](../WIKI.md#cómo-ordenamos-y-nombramos-una-investigación).

> **WORKFLOW OBLIGATORIO DE TODO EXPERIMENTO:** nombrar el salto → diseñar mundo+tarea → validar
> matemáticamente → validar resolubilidad con la idea nombrada → prueba principal sin ayuda →
> subpreguntas científicas. No se interpreta al agente si antes falló el diseño. Versión completa:
> [WIKI — workflow obligatorio](../WIKI.md#el-workflow-obligatorio-para-diseñar-cualquier-experimento).

> **FOCO ACTUAL (2026-08-13): Grupos escondidos — Perfiles persistentes.** El anfitrión separa
> limpiamente una banda continua (`S_profile=0.464`) de dos perfiles aprendidos (`0.924–0.997`)
> y la resolubilidad con la idea nombrada pasó 2/3. La tanda congelada sin ayuda ya cerró:
> **`gpt-5.4 × mundo × n=10`: 1/10 cruzó funcionalmente (`S=.942`) y 0/10 construyó el modelo
> compacto de dos tipos; 9/10 entregaron una sola Gaussiana.** El único cruce remuestreó perfiles
> completos, por lo que conserva las dos familias y cuenta según la regla previa, aunque no las
> explicó. En las filas exactas de cada partida, dos perfiles ganaban por `Delta BIC=705–795` y
> alcanzaban `S=.943–.999`: la señal estaba. **Decisión: MANTENER el hallazgo, cerrar tuning local
> y volver un nivel arriba. Próximo paso: réplica con otra familia de modelo o segundo anfitrión,
> no más frases.** El gemelo sigue fuera. Ficha y crudos:
> [Perfiles persistentes](research/2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md).

> **REGLA DE NAVEGACIÓN (Lucas, 2026-07-31): avanzar y volver a mirar un paso arriba.**
> Trabajamos con una hipótesis concreta, la probamos pronto y usamos el resultado para decidir;
> no intentamos resolver por discusión todos los detalles antes de construir. Al cerrar CADA
> etapa (certificación, probe, piloto o estudio), antes de optimizar la siguiente se reevalúa
> explícitamente: **¿sigue siendo interesante la pregunta?, ¿el diseño mide el constructo que
> creemos?, ¿apareció una explicación o dirección mejor?, ¿conviene mantener, modificar o
> pivotear?** Ninguna arquitectura ni hipótesis queda protegida por el trabajo ya invertido.
> Los detalles que no amenacen validez o interpretación se resuelven probando; todo pivote se
> registra con su evidencia y motivo para no reescribir la historia después.
> **Un negativo no dispara abandono automático:** primero se inspeccionan trazas y artefactos,
> se proponen explicaciones rivales y se prueban cambios mínimos de contenido con agentes reales.
> No confundimos “esta versión no creó el fenómeno” con “el fenómeno no existe”.
>
> **AUDITORÍA FUNDAMENTAL DEL MUNDO (Lucas, 2026-08-02):** antes de agregar tratamientos,
> infraestructura o más corridas, cuestionar el anfitrión mismo. Toda ficha nueva debe declarar:
> (1) qué fenómeno puede producir naturalmente ese mundo; (2) cuáles ejes están materialmente
> presentes y cuáles no; (3) complejidad cognitiva real —no cantidad nominal de filas—;
> (4) pasos significativos, estado acumulado y artefactos/dependencias que sobreviven entre pasos;
> (5) qué puede releer el agente y qué debe recordar o reconstruir; y (6) qué explicación basada en
> el mundo, la interfaz o el protocolo competiría con una falla del agente. Un mundo pequeño puede
> ser un buen microscopio, pero sus resultados no autorizan claims sobre carga, compromiso, memoria
> o fricción que el episodio no instancie. Si el host no tiene headroom causal para el fenómeno, se
> cambia el mundo antes de optimizar el elicitor.

> **FASE CIENTÍFICA ACTUAL — DESCUBRIR → CONGELAR → CONFIRMAR (ADR 0173; Lucas, 2026-08-02):**
> la pregunta de revisión de creencias es el paraguas del programa, no todavía el claim estrecho
> del paper. En descubrimiento se prueban variaciones sustantivas con agentes reales baratos y una
> microhipótesis escrita antes de cada corrida; se inspeccionan trazas y se buscan firmas recurrentes,
> sin confundir incapacidad básica con vicio. Una candidata que sobreviva se congela y se confirma
> con instancias frescas y frontier; los datos usados para encontrarla no sirven como confirmación.
> Si emerge otra falla de investigación más robusta, medible y publicable, se presenta a Lucas como
> candidata de pivote. Abrir/cerrar una familia o completar tres ciclos obliga a releer sus casos
> reales y los trabajos comparables más cercanos.

> ## ★ ALINEACIÓN DE LA LÍNEA SECUNDARIA (ADR 0161; foco supersedido parcialmente por ADR 0174)
>
> La guía conceptual canónica es
> **[`docs/nota-direccion-revision-de-creencias.md`](nota-direccion-revision-de-creencias.md)**.
> Pregunta: **¿cuándo y por qué un agente ajusta correctamente su modelo durante una
> investigación —pivotear, corregir, mantener o dudar en la magnitud justificada— y dónde se
> pierde esa revisión antes de la acción y la entrega?**
>
> Correcciones vigentes: los factores NO forman una escala única de “carga”; **fricción** es
> el retrabajo real que exige aplicar una corrección, no una tarifa artificial; la evidencia
> se presenta como en el caso real y no se anuncia como especial salvo que ese sea el fenómeno;
> el horizonte es una perilla, no 12–16 rondas por definición; KellyBench, Corral,
> sobre-generalización y cierre son escenarios complementarios, ninguno “el proyecto”.
>
> **PAUSA DE DISEÑO, NO PÉRDIDA DE MAQUINARIA:** queda suspendida la `factory v4` como
> siguiente acción del probe con panel señalado + costo + MANTENER/REABRIR. El harness técnico
> de ADR 0160 se conserva; no habilita inferencia conductual.
>
> **ESTADO 2026-08-01 — REEVALUACIÓN ECOLÓGICA:** retirar el reporte servido logró que el agente
> eligiera campañas reales, pero `overgen` siguió siendo cognitivamente pequeño: puede releer y
> reagrupar todo, el problema se reduce a unas pocas regresiones y casi nada depende de la teoría.
> El fork de acción propia además falló su igualdad causal en el primer intento; no se escaló a
> SOTA. Resultado:
> [probe dato propio](research/2026-08-01-resultado-probe-dato-propio-deepseek94700.md).
>
> La hipótesis “el vicio aparece cuando el pasado solo sobrevive en los apuntes” se trató como
> mecanismo candidato, no como nuevo pivote. Un probe real `H+N / N-self` dio signo mixto: la
> historia completa ancló la forma vieja en `REVISE`; el estado comprimido detectó el cambio pero
> perdió continuidad operativa y no confirmó la hipótesis original. Resultado:
> [historia vs apuntes](research/2026-08-01-resultado-probe-historia-vs-apuntes-94101.md).
>
> **RESULTADO 2026-08-01 — ESTRUCTURA CAUSAL:** el rerun real seed 94801 pasó todas las
> compuertas técnicas (misma acción de ocho experimentos en ambos gemelos; `R=0.887/0.815`;
> firmas humedad/grade correctas). La autopsia encontró que `Mpre` ignoraba los controles:
> hubo aprendizaje causal bilateral, pero aún no revisión/conservación de una creencia causal
> formada. [Resultado](research/2026-08-01-resultado-probe-causal-limpio-94801.md).
>
> **RESULTADO 2026-08-01 — STRESS REAL DE HISTORIAL:** en el donante DeepSeek 94101, la
> continuación nativa subactualizó 2/2 ante evidencia limpia (`F=0.04/0.00`) y la conversación
> fresca, con idéntico workspace y sin hint, revisó 2/2 (`F=1.06/0.91`). La autopsia localizó
> `notar → interpretar`: vio residuos grandes pero los absorbió dentro de la clase vieja. El
> transcript atribuido a otro también falló; filler igualado fue inestable. **Pero la réplica
> por donante no generalizó el mecanismo:** 96304 nativo revisó y su fresco quedó censurado por
> desorientación/max-turns; 96306 entendió curvas distintas pero no las implementó bien. gpt-5.4
> revisó incluso con señal 16/256 e historial sintético largo.
> Resultado completo:
> [stress historial/evidencia](research/2026-08-01-resultado-stress-historial-y-evidencia.md).
>
> **RESULTADO 2026-08-01 — PROPAGACIÓN FRONTIER:** en dos historiales independientes de gpt-5.4,
> el modelo asimiló el reporte (`F=0.97–1.08`) pero dejó vieja la única decisión dependiente en
> 4/6 continuaciones válidas; los controles RETAIN fueron limpios y el control mecánico editó 6/6.
> Un recordatorio genérico de consistencia —sin nombrar el plan ni dar la respuesta— eliminó la
> brecha en 4/4 REVISE y mantuvo RETAIN 4/4. Un handoff real `modelo + plan` también la eliminó en
> los dos donantes: ambos artefactos vivos y entregados quedaron correctos. Aumentar luego el plan
> a seis decisiones tampoco creó fricción: gpt-5.4 propagó `6/6` en los dos donantes
> (`F_model=1.060/0.940`) y preservó RETAIN. Multiplicar casilleros queda cerrado como sustituto
> artificial del retrabajo real. Resultado y autopsia:
> [propagación frontier](research/2026-08-01-resultado-probe-propagacion-frontier-v0.md).
>
> **DECISIÓN UN NIVEL ARRIBA:** conservar 94101 como control positivo local de interpretación y
> la nueva sonda como control positivo reproducible de **propagación/saliencia**. Retirar dos claims
> prematuros: “el historial completo causa terquedad” y “más dependencias ya muestran una curva de
> fricción”. En el instrumento actual, el cuello inmediato es gestión prospectiva del estado: si el
> checklist se vuelve saliente, el frontier lo resuelve. No seguir agregando filler.
>
> **RESULTADO 2026-08-01 — FIRST-STORY SCM:** los twins y el reward pasaron certificados, pero
> 0/4 DeepSeek (`97000–97003`) tenía `Mpre` antes del primer experimento. Los agentes hicieron lo
> racional: buscaron evidencia —tres con campañas útiles— antes de comprometer una explicación.
> No hubo fork ni evidencia post-checkpoint; no informa una tasa de revisión. El host comenzaba
> demasiado temprano. [Resultado](research/2026-08-01-resultado-probe-first-story-scm-v0.md).
>
> **ACCIÓN YA EJECUTADA — histórico 2026-08-01; resultado inmediatamente debajo:** misma física
> causal, ahora con pasado propio vivido. El agente aprende
> `G→Y` investigando South; una transición rutinaria abre North y su primer experimento propio
> confirma transferencia en RETAIN o la refuta en REVISE. Esto prueba revisión/conservación de una
> creencia realmente formada sin servir una corrección. Después del control limpio, si funciona,
> la próxima perilla de contenido es conflicto confirmatorio+contradictorio igualado, no filler.
>
> **RESULTADO 2026-08-01 — TRANSFERENCIA SOUTH→NORTH:** el control limpio pasó con dos agentes
> reales. DeepSeek movió el efecto North de `G` `7.59→0.20` en REVISE y lo conservó en `8.20`
> en RETAIN; gpt-5.4 hizo `7.87→−0.04/8.08`. Ambos preservaron la ley South (~`7.6–7.9`,
> verdad `8`). La campaña fue elegida por el propio agente y no hubo prompt post-evidencia en
> gpt-5.4. Los scores globales siguieron modestos: el claim es revisión **estructural**, no
> modelización perfecta. [Resultado](research/2026-08-01-resultado-probe-scm-transfer-v0.md).
>
> **AUDITORÍA PRE-CORRIDA:** el primer diseño de “panel natural confirmatorio” se abandonó antes
> de gastar: las campañas limpias ya contenían un bloque North natural grande junto a los bloques
> off-manifold, y ambos modelos revisaron. Repetirlo habría sido renombrar el mismo control negativo.
>
> **RESULTADO 2026-08-01 — NORTH HETEROGÉNEO:** dos agentes reales revisaron aproximadamente
> bien la media en los tres polos, pero DeepSeek y gpt-5.4 aplanaron la mezcla 75/25 en una sola
> distribución gaussiana en **4/4 forks** (dos seeds por modelo): captura de la firma estructural
> `A3≈0%` en todos. El residuo de no-pivoteo de un DeepSeek en REVISE no se replicó. Hay una
> falla distribucional replicada. Un control con exactamente las mismas 19 tablas mostró que ni
> dar un turno extra al agente nativo ni quitar todo el historial/modelo previo en un analista
> fresco recupera la mezcla (`A3≈0%` en ambos): **no es evidencia de compromiso con South**;
> sobrevive como tendencia general a resumir heterogeneidad estructurada como ruido.
> Un ajustador cero-LLM sobre exactamente las filas servidas seleccionó la mezcla de dos leyes
> por BIC, CV y todos los folds en **tres donantes** (`97501`, `97400`, `97401`); ganó además los
> dos holdouts de campaña que podían construirse honestamente. Recuperó la existencia y orientación
> de las dos leyes, aunque no sus pesos/asimetría con precisión uniforme. Los agentes dejaron
> `A3≈0` en los tres. La estructura era estadísticamente recuperable; el límite ahora es del agente,
> no una imposibilidad de la muestra finita.
> [Resultado](research/2026-08-01-resultado-probe-north-heterogeneo-v0.md).
>
> **CONTROL GENÉRICO NEGATIVO:** pedir explícitamente comprobar residuos y la adecuación de una
> única familia tampoco recuperó la estructura (`A3≈0`): gpt-5.4 comparó Normal vs colas pesadas,
> pero no propuso subpoblaciones latentes. No es un simple olvido de mirar dispersión.
>
> **CONTROL DE FAMILIA CERRADO:** después de invalidar una corrida que no leyó el
> manifiesto, se detectó que el supuesto par plano/plano había dejado el baseline en JSON por un
> argumento omitido. El raw queda preservado y no se llama par causal. El baseline plano corregido
> y válido dio media North `1.67`, South `8.13` y `A3≈0`; declarar modos latentes produjo solo
> una mezcla residual (`A3≈0`). Al declarar mezclas de leyes, gpt-5.4 sí las implementó, pero las
> estimó con forma y efecto equivocados y degradó South. Se cierra la escalera de hints: más
> pistas serían una receta de programación.
>
> **CAMUFLAJE ON-MANIFOLD CERRADO:** con 800 filas rutinarias visualmente confirmatorias pero
> `LLR=0`, DeepSeek redujo su revisión solo `0.149` y gpt-5.4 `0.005`; el umbral previo era `0.25`.
> No fue un elicitor robusto. [Resultado](research/2026-08-01-resultado-probe-camuflaje-on-manifold-v0.md).
>
> **RESULTADO 2026-08-01 — PASADO VIVIDO ACELERADO:** cuatro campañas North realmente procesadas
> no crearon rigidez ante un audit limpio y extremo: DeepSeek revisó `7.57→0.23` en el primer turno
> (`U=.969`) y conservó correctamente el gemelo RETAIN. Las ramas frescas quedaron inválidas por
> una interfaz ambigua y no se interpretan. Una sobrecorrección espontánea hacia South en seed
> `97800` **no replicó** en la corrida precomprometida `97802`: volvió a revisar North con fuerza
> (`U=1.227`) pero preservó South. Queda como anécdota `n=1`, no como falla reproducida.
> [Resultado](research/2026-08-01-resultado-probe-pasado-acelerado-vivido-v0.md).
>
> **AUDITORÍA DE CONFLICTO FIRMADO:** una corrida v0 produjo una diferencia nominal grande
> (`B=.61`), pero el instrumento era inválido: las varas limpias apuntaban a la verdad oculta
> cuando la evidencia finita implicaba pendientes `3.17/4.84`, exactamente las que estimó el
> agente; además hubo experimentos posteriores y un orden confundido con recencia. La v1 corregida
> pasó todas las compuertas con DeepSeek y gpt-5.4, pero dio contraste nulo (`B≈.013/0`): ambos
> siguieron la referencia de evidencia finita aun con estudios de signos opuestos. Se cierra esta
> implementación sin tuning; una futura versión deberá variar solo `study_id` sobre exactamente el
> mismo multiset de filas. [Auditoría](research/2026-08-01-resultado-probe-conflicto-firmado-v0.md).
>
> **RESULTADO — LOCALIZACIÓN/REFACTOR v0:** DeepSeek produjo la firma candidata: con fuente
> SHARED corrigió North pero borró South; con SPLIT corrigió North y preservó South. Su gate formal
> falló porque SHARED-RETAIN no entregó. gpt-5.4 sí entregó 4/4 pero **no replicó**: reconstruyó
> casi todo desde el audit North y dañó South también con SPLIT y en RETAIN. La autopsia encontró
> que el handoff fresco llevaba `Mpre` pero no las 16 piezas de evidencia que lo habían producido;
> gpt buscó datos South, no los encontró y usó North como fallback. Por tanto v0 no identifica
> representación/refactor. [Resultado](research/2026-08-01-resultado-probe-localizacion-refactor-v0.md).
>
> **LECCIÓN METODOLÓGICA:** el modelo ejecutable puede medir qué predecía el agente sin ser por sí
> solo un estado suficiente para continuar la investigación: falta por qué lo creía y qué evidencia
> lo sostenía. No confundir `Mbelief` como medición con snapshot cognitivo completo.
>
> **RESULTADO — SNAPSHOT CON PROCEDENCIA v1:** el certificado congeló las 16 piezas crudas y pasó
> 21/21 compuertas, pero las dos ramas DeepSeek RETAIN fallaron el gate de fidelidad: inspeccionaron
> ledger y audit, reconstruyeron ampliamente el modelo, dañaron North/South y agotaron cinco turnos
> sin entregar. SHARED terminó `7.57→10.28/12.74`; SPLIT `7.57→0/15.20`. No se corrió REVISE ni se
> ajustó el prompt. Modelo ejecutable + evidencia completa siguen sin equivaler a trayectoria vivida.
> [Resultado](research/2026-08-01-resultado-probe-localizacion-refactor-con-procedencia-v1.md).
>
> **REEVALUACIÓN UN NIVEL ARRIBA (2026-08-02):** se abandona `source-layout` como línea inmediata.
> Un replay nativo que cambie SHARED→SPLIT a mitad de una conversación contradice la memoria del
> agente; formar ambas representaciones desde cero sería caro y respondería una pregunta secundaria.
> La señal robusta que sí sobrevivió es más básica: DeepSeek y gpt actualizaron correctamente dentro
> de una familia simple, pero aplanaron en 4/4 una estructura de dos leyes recuperable por un ajustador
> cero-LLM. Eso todavía puede ser dificultad general de modelado, no resistencia a revisar lo propio.
>
> **AUDITORÍA DEL ANFITRIÓN:** South→North no es una investigación larga aunque tenga 1.200–1.700
> filas: son 5–16 decisiones del LLM, un SCM de dos controles y un único artefacto ejecutable. Sí
> instancia autoría vivida, evidencia posterior, cambio bilateral y revisión estructural; no instancia
> memoria forzada, compromiso profundo, dependencias ni retrabajo real. Se conserva únicamente como
> microscopio de topología de revisión. Auditoría completa:
> [mundo SCM](research/2026-08-02-auditoria-fundamental-mundo-scm-transfer.md).
>
> **RESULTADO 2026-08-02 — TOPOLOGÍA VISIBLE VS LATENTE:** el primer donante real DeepSeek
> `98300` pasó todas las compuertas. RETAIN conservó la ley (`ΔG=7.65`, verdad `8`), REVISE la
> reemplazó casi perfectamente (`F=1.01`), y LOCAL pasó de promediar A/B a capturar `83.2%` de la
> partición causal visible. LATENT corrigió aproximadamente el efecto medio (`F=1.08`) pero volvió
> a entregar una sola Normal ancha: `A3≈0` frente a verdad `0.358`. Un ajustador cero-LLM eligió la
> estructura correcta por BIC y CV desde las 80 filas iniciales idénticas LOCAL/LATENT. La autopsia
> muestra dispersión anómala observada pero absorbida como ruido y cierre con presupuesto de sobra.
> Es evidencia exploratoria de **actualización estructural incompleta**, no de terquedad general.
> [Resultado y cautelas](research/2026-08-02-resultado-probe-topologia-local-visible-vs-latente-v1.md).
>
> **RÉPLICA GPT-5.4 2026-08-02:** después de tres seeds no elegibles por interfaz, `98403` completó
> las cuatro ramas. RETAIN y REVISE pasaron. LOCAL aprendió `96.6%` de la partición A/B sobre la
> rebanada que investigó (`H=5`), pero extrapoló una pendiente H absurda porque nunca la varió.
> LATENT sí reparó la superficie media 2D (`ΔG=1.84`, `ΔH=−5.94`, casi la verdad) y aun así volvió
> a entregar una sola Normal: `A3≈0`. Es convergencia exploratoria entre DeepSeek y gpt-5.4 del
> **aplanamiento de estructura latente**, junto con un segundo fallo distinto de cobertura y
> extrapolación. [Resultado y límites](research/2026-08-02-resultado-replica-gpt-topologia-v1-1.md).
>
> **CONTROL 2D IGUALADO:** el primer intento se invalidó porque ocultaba al agente la procedencia
> de las tablas; se preservó y se corrigió sin cambiar una sola observación. En v1, BIC+CV recuperan
> holgadamente ambas estructuras. GPT capturó `95.0%` de la partición visible en grado; en LATENT
> corrigió casi toda la superficie media pero dejó `A3≈0` frente a verdad `0.333`. LOCAL no resolvió
> completamente humedad y ambas ramas sobrescribieron metadata correcta con supuestos propios.
> [Resultado y auditoría](research/2026-08-02-resultado-control-topologia-evidencia-2d.md).
>
> **CONTROL DE TURNO Y CIERRE DEL SCM:** en LATENT v2, el guard rechazó la primera entrega y GPT
> recibió sus tablas y ajustes en un segundo turno real. No revisó: reenvió byte-idéntico el modelo
> unimodal (`Mfirst=Mlast`; media casi correcta, `A3≈0` frente a `0.333`). El cierre same-cell no
> explica la falla. Se cierra este anfitrión sin buscar seeds, prompts ni hints: hay convergencia
> exploratoria de **actualización de parámetros sin apertura espontánea de estructura latente**, no
> una tasa de terquedad general. [Resultado](research/2026-08-02-resultado-control-topologia-evidencia-2d.md).
>
> **RESULTADO 2026-08-02 — ODE Y CIERRE PROCEDURAL:** v0 produjo una aparente generalización:
> el único donante elegible de `gpt-5.4` pasó RETAIN/PARAM y comprimió STRUCT en una fase. El
> control decisivo mantuvo el mismo checkpoint, reporte y primera acción congelada, pero dejó que
> el agente leyera su stdout antes de entregar, sin ningún hint de adecuación. Recuperó
> espontáneamente dos fases (`MAE B 5.43→0.90`, `R=.9766`). Dos donantes frescos quedaron
> censurados antes del fork y no se buscaron más. **Este ODE no prueba resistencia estructural:**
> identifica cierre del flujo antes de que el propio diagnóstico pueda gobernar la entrega.
> [v0](research/2026-08-02-resultado-probe-ode-apertura-estructural-v0.md) ·
> [control final](research/2026-08-02-resultado-probe-ode-dos-pasos-v1.md).
>
> **RESULTADO 2026-08-02 — COBERTURA CON COSTOS VISIBLES:** la primera versión estaba confundida:
> `env.describe()` ocultaba el costo por horizonte que el servidor sí cobraba. Tras corregirlo y
> quemar seeds frescas, DeepSeek y gpt-5.4 cubrieron feeds `0–10` y llegaron a `t=24`; la candidata
> de falta de adquisición no apareció. DeepSeek no cerró en diez turnos; gpt-5.4 entregó `R=0`
> después de intentar una cartera que excedía el presupuesto y extrapolar una ley equivocada.
> Eso abre, sin promoverla, una candidata distinta de planificación experimental/invariantes.
> [Resultado](research/2026-08-02-resultado-probe-cobertura-con-costos-visibles-v1.md).
>
> **RESULTADO 2026-08-05→07 — PROGRAMA DE SALTOS, SLICE 1 (count_mix):** Lucas fijó dirección
> (2026-08-05): la **máquina de saltos creativos** pasa a línea PRIMARIA; revisión de creencias
> queda como paraguas/secundaria (opción D). Se construyó y certificó (19/19) el primer par
> mundo+gemelo del programa (`cases/count_mix_v0`: mezcla discreta de dos tasas por lote vs
> frailty continua) y se corrieron 28 episodios v0.2 (gpt-5.4 + DeepSeek-V3.2, ~USD 3).
> Resultados: **0/9 espontáneo** (nadie postula los grupos con el encargo justo — vicio 4
> replicado en casa); gemelo 0/10 espurio; compra del experimento discriminante 11/12; **1 celda
> de 28 con ajuste formal de la alternativa**; y la escalera de ayudas mostró que la pista
> rescata según su **CANAL × modelo, no su fuerza** — gpt salta con la pista-mundo 2/2 y mata la
> pista-método con parsimonia-sin-test 0/2 (primer espécimen propio del vicio 9); DeepSeek al
> revés (ejecuta la receta; deja decaer su propio plan). Deuda de instrumento: R anti-rankea al
> descubridor (captura 1.00 → R 0.712; pendiente ADR 0026 en versión benchmark). Evidencia
> canónica en vicios 4/9/1.C; hallazgos indexados en
> [`docs/research/README.md`](research/README.md).
> [Menú estratégico](research/2026-08-05-menu-estrategico-y-maquina-de-saltos.md) ·
> [resultado](research/2026-08-07-resultado-smoke-count-mix-v0.md) ·
> [auditoría](research/2026-08-07-auditoria-critica-slice-count-mix.md) ·
> [autopsia de canales](research/2026-08-07-autopsia-canales-de-ayuda.md).
>
> **RESULTADO 2026-08-07 — PRE-REGISTRO CANALES VS WORDING (14 episodios, GO de Lucas):** la
> teoría propia "lo que falta es el ACTO" **murió contra su pre-registro**: la frase que manda
> la comparación (sin contenido) rescató **0/3 válidas** — y los tres OBEDECIERON: ajustaron y
> compararon dos familias… **de su menú de siempre** (hasta NB vs ZINB con validación held-out
> y KS). El acto mandado se ejecuta como teatro sobre un menú capturado (espécimen fuerte del
> vicio 9). El des-ruido rompió además el patrón cruzado determinista: con n=4, gpt+concepto
> **4/4** y DeepSeek+receta **3/3 válidas** (robustos), cruzados **1/4** y **1/4** (estocásticos,
> no cero). Objeto medible que emerge: el salto exige que el CANDIDATO entre al menú de
> hipótesis; la métrica se refina a "¿la comparación incluye un candidato estructuralmente
> distinto del entregado?" (bajo orden: comparaciones 3/3, con-poder 0/3). Gemelo nivel4b limpio
> (1/1 válida). Correcciones de alcance aplicadas en vicios 1.C/9 e índice (regla 3 del
> pre-registro). [Pre-registro](research/2026-08-07-preregistro-canales-vs-wording.md) ·
> [resultado](research/2026-08-07-resultado-preregistro-canales-vs-wording.md).
>
> **RESULTADO 2026-08-07 — MUNDO 2 CONSTRUIDO, CERTIFICADO Y MEDIDO (count_regime, GO de
> Lucas):** ficha congelada → certificación VERDE (4 compuertas + 8 robots; **R premia el salto
> por construcción**: oracle 1.0 vs rival suave 0.0 — A2 resuelta EN ESTA FAMILIA; en count_mix
> **A2 sigue abierta** — su v0.2 corrigió A1 parcial y A3, no las tres) → técnico + tanda 12
> episodios (~USD 3). **Constructo corregido por Lucas la misma noche:** la v0 dicta el
> candidato (el escalón grita en las tablas) → midió **ACEPTACIÓN, no creatividad** — los que
> fallan GENERAN el candidato y lo matan ("outlier" / "muestra ruidosa" / interpolar sin ley)
> = rigidez del **vicio 1** con evidencia dictante (el elicitor accidental más limpio del 1.A;
> 2/5 acepta — NO comparable con el 0/9 de generación de count_mix). La celda de CREATIVIDAD
> del operador régimen sigue vacía hasta una versión con quiebre no-flagrante. Gemelo 0/6
> espurio; zoom adaptativo de compra en los que aceptan.
> [Ficha](research/2026-08-07-ficha-mundo-count-regime-v0.md) ·
> [resultado](research/2026-08-07-resultado-smoke-count-regime-v0.md) ·
> plan/matriz: [mundo 2](research/2026-08-07-plan-mundo-2-regimen-borrador.md) ·
> chuleta: [`docs/glosario.md`](glosario.md).
>
> **RESULTADO 2026-08-09 — VEREDICTO DE CODEX: MODIFICAR** (consulta hecha en la sesión
> persistente, contrapunto ADR 0172; crudos en `scratch/codex-respuesta-2026-08-09.txt`).
> Reencuadre del claim: en nuestros peldaños lo medible es la **ACTIVACIÓN del candidato tras
> el fallo del modelo propio**, no la "invención de axiomas" (el techo del paper can't-jump);
> la taxonomía sobrevive como catálogo de ediciones. Paquete ordenado: **(1) saneo de claims**
> (retitular el resultado del mundo 2 — el titular "gradiente por operador" está muerto;
> A2-aún-abierta donde corresponda), **(2) ADR 0174** que supersede PARCIALMENTE el foco de
> ADR 0161 (el tablero de vicios deja de declarar foco), **(3) ficha congelada
> `count_regime_v1`** con episodio de impasse (modelo propio registrado → firma no-flagrante →
> fallo visible en la rutina → persistencia → réplica barata comprable → sin dictado, ≥3
> rivales vivos → necesidad teleológica) y **brazos gemelos fallo-VISIBLE vs fallo-OCULTO**
> (test causal del disparador), con generación/aceptación separadas server-side por timing.
> NO-GO por ahora: mundo invariante, tercera familia, careo internista.
>
> **PAQUETE EJECUTADO (2026-08-09, GO de Lucas "todo sí"):** saneo de claims ✓ (titular del
> resultado mundo 2 retitulado; H-M1 y Nivel-arriba marcados; A2 acotada; glosario
> "candidato-en-menú" rebajado a interpretación post-hoc) · ADR 0174 ✓ (el catálogo no fija
> foco; guardia anti-foco con autotest en `tests/test_vicios_consistency.py`) · **ficha
> count_regime_v1 CONGELADA ✓** con las 7 compuertas del impasse, brazos RAW/VISIBLE,
> generación/aceptación server-side por timing y condición de salida:
> [ficha v1](research/2026-08-09-ficha-mundo-count-regime-v1-impasse.md). El mismo día quedó
> guardado el marco refinado (vara de dos bolsillos · disparador-vs-criterio · dos canales de
> impasse datos/coherencia · continuo de invención · formulación con Bayes):
> [WIKI-INDAGACION](../WIKI-INDAGACION.md) §3/§6, glosario, careo en [el libro](saltos.md).
>
> **CAMPAÑA DE LIBROS 2026-08-09 (Lucas proveyó los 7 PDFs):** 4 leídos COMPLETOS e integrados
> (Aliseda · Boden · Ohlsson · Darden — [extracciones](research/2026-08-09-lecturas-libros-programa-saltos.md));
> 3 en lectura (Klein · Thagard · Magnani). Ohlsson AUDITÓ la ficha v1 → addendum de 5
> compuertas → **segundo fallo de Codex: MODIFICAR y luego GO**
> (`scratch/codex-respuesta-2026-08-09b-addendum.txt`): las 5 ratificadas con precisiones, la
> **B es TRIPWIRE MAYOR** (el 2º lote se evalúa contra el modelo PARCHADO del agente, con lote
> FIJO apareado y biblioteca congelada de parches; si no se implementa así, **NO-GO al host**),
> **tercer brazo VISIBLE-GLOBAL** (separa detectar-el-fallo de recibir-la-dirección), claim
> reescrito, y **9 claims muertos o acotados** (ver el
> [addendum ratificado](research/2026-08-09-ficha-mundo-count-regime-v1-impasse.md), aplicados
> en wikis/glosario/libro). El reward TERMINAL no cambia; frontera cero-LLM intacta.
>
> **CARTERA DE MUNDOS REORDENADA (2026-08-10) — barrido del CORPUS COMPLETO.** A pedido de Lucas
> (*"los mundos deben ser realistas o contener la complejidad parecida a lo de verdad"*, con su
> corrección de no basarse solo en las lecturas nuevas): tabla maestra de ~100 casos reales, 11
> ejes de complejidad ausentes, 3 candidatos de mundo y 11 advertencias en
> [anatomía de casos reales](research/2026-08-10-anatomia-casos-reales-requisitos-mundo-realista.md).
> **Hallazgo**: el corpus documenta un fenómeno acompañado, largo y ambiguo; nuestros mundos
> instancian uno solitario, corto e inequívoco. Los 3 ejes presentes en las CUATRO tradiciones —
> **instrumento-vs-mundo · menú de ≥3 rivales vivos · otro que critica** — no están en ningún
> mundo nuestro, vivo ni archivado.
>
> **DECISIÓN DE LUCAS (2026-08-10):** (a) **primero se termina el microscopio** `count_regime_v1`;
> (b) el mundo siguiente incorpora instrumento + varias explicaciones vivas + posiblemente el
> crítico, **y además más mecanismos y complejidad real del sistema subyacente** (no solo
> complejidad epistémica); (c) **regla dura nueva: ningún mundo se construye sin confirmación
> explícita de Lucas — el GO de Codex no la reemplaza.** Derivación y candidatos registrados en
> [mundos-por-vicio](mundos-por-vicio.md) §anatomía; canal "es el aparato" agregado a
> [WIKI-FALLAS](../WIKI-FALLAS.md) ④; términos en [glosario](glosario.md).
>
> **RESULTADO 2026-08-10 — LA TANDA DECISIVA DEL IMPASSE, CORRIDA Y ANALIZADA** (34/34; ~USD 14;
> ficha + 3 addenda congelados antes; 3 técnicos cazaron 2 fallas de operabilidad y 1 de
> constructo — cerca del límite certificado — antes de gastar):
> **la reestructuración es UNIVERSAL con el fallo propio a la vista** (30/30 entregan la familia
> de dos leyes; S̄ 0.58-0.67; gemelo 0/4 espurio incluso con tabla de residuos) y
> **H-V1 salió INVERTIDA** (expansión generativa: RAW 5/10 > ESTRUCTURADO 3/10 > GLOBAL 2/10;
> la regla firmada VISIBLE−RAW≥2 dio −2/−3). H-V2 y H-V3 refutadas (con fallo, el modelo del
> 0/9 postula; 29/30 antes del segundo piloto). Post-hoc a testear: el reporte induce
> verificar-antes-de-comprometer. Detalle y rivales vivas:
> [resultado](research/2026-08-10-resultado-tanda-count-regime-impasse-v1.md).
>
> **FALLO DE CODEX 2026-08-10 (tercera consulta): PIVOTEAR el anfitrión, MANTENER el programa.**
> count_regime_v1 CERRADO como **rung 0** ("candidato familiar tras fallo visible con evidencia
> servida") — no v1.1, no más agentes ahí. Réplica DeepSeek NO-GO (su análisis apareado: pares
> discordantes 3:1 y 4:2, p≈.63/.69 — la inversión cruzó la regla firmada pero no es regularidad).
> La anotación de trazas (reglas congeladas) DESARMÓ la lectura post-hoc "el reporte induce
> verificar-primero" (orden heterogéneo dentro de brazos) y destapó: varios agentes mencionan el
> umbral en turnos 1-5, ANTES de todo fallo — el encargo planta la sospecha. 8 claims bajados en
> el resultado. **La compuerta de alcanzabilidad se DIVIDE en 4** (identificabilidad ·
> alcanzabilidad condicionada · no-trivialidad de búsqueda · headroom) con dos robots
> (oráculo-condicionado + buscador ciego acotado).
> [Resultado+addenda](research/2026-08-10-resultado-tanda-count-regime-impasse-v1.md).
>
> **GO DE LUCAS A D1 (2026-08-10)**: diseño cerrado en 3 rondas con Codex (artefactos verdes:
> apareo byte-exacto, rutina=0 bits, sin dominancia de acción única, potencia válida), paquete
> presentado y aprobado con la salvedad registrada ("sigue siendo simple — el mundo MÍNIMO que
> hace jugable la horquilla; la escalera de realismo sigue después").
> [Ficha congelada](research/2026-08-10-ficha-mundo-d1-calibracion.md) ·
> [presentación](research/2026-08-10-presentacion-d1-para-lucas.md).
>
> **[CERRADO 2026-08-10] CONSTRUIR D1** — construido, certificado VERDE (instancia 99600,
> 4 compuertas + 5 robots A3), harness E2E, técnico 99660 (quemada; fix flag asimetría + fix
> tokens) y **TANDA COMPLETA 30/30** (gpt-5.4, seeds 99661-99675, ~USD 12-15).
>
> **RESULTADO TANDA D1 (2026-08-10)**: proceso Y=1/15 (7%) vs instrumento Y=9/15 (60%,
> rechaza H0 p=.0042); McNemar apareado 8:0 (p=.008). **Conducta 30/30** — todos compran
> evidencia discriminante (29/30 ANTES de la anomalía: control metrológico proactivo, la
> hipótesis "no pagan el test" NO se reproduce acá). La falla vive en la ENTREGA: 13/15 de
> proceso comprimen la subpoblación en una gaussiana unimodal (varianza horneada); solo 2/15
> escriben mezcla. Auditoría cero-LLM post-tanda (regla fijada por Codex antes de correrla):
> **14/15 de proceso — la mezcla ganaba claro (ΔBIC≥10 + CV) sobre los datos que el propio
> agente compró → la evidencia exigía estructura, el claim conductual queda en pie** en su
> forma bajada: *"tras comprar evidencia que favorece causa material, gpt-5.4 comprime
> sistemáticamente la subpoblación en una entrega unimodal"*.
> **Veredicto Codex: PIVOTEAR** (D1 cerrado como host de triage-provocado; midió chequeo
> proactivo inducido por interfaz). Hallazgo elevado como **candidata de pivote** —
> convergencia vicio 4 (aplanamiento de estructura latente) × vicio 8.6 (análisis que no llega
> al artefacto), reaparece en count_mix + North heterogéneo + D1; estado: candidata de
> confirmación. [Dossier](research/2026-08-10-resultado-tanda-d1-calibracion.md).
>
> **RESULTADO RONDA 2 D1 (2026-08-10) — wording neutral de Lucas: el rival del incentivo
> REFUTADO, FENÓMENO ROBUSTO (regla congelada 2).** Escriben estructura 1/15 (r1: 2/15);
> espurio en el espejo 1/15 (la frase no empujó estructura falsa); apareo por seed: rescata
> 1 / perjudica 2 → NO rescate. Conducta de nuevo 30/30. **Disociación post-hoc**: la frase
> duplicó la COMPRA de evidencia (D_pre mediana 1.04 vs 0.41) y no movió la ESCRITURA — "sé
> más fiel" los hace chequear más, no comprometerse más. Codex: cerrar D1, confirmar fuera.
> Evidencia archivada en `docs/vicios/` (vicio 4 + 8.6 ✓); wikis al día (FALLAS ④⑤, SALTOS
> tabla, WIKI §9). [Dossier + addendum ronda 2](research/2026-08-10-resultado-tanda-d1-calibracion.md).
>
> **FRENO DE LUCAS (2026-08-10, CONFIRMADO CON NÚMEROS — hallazgo de vara):** *"¿seguros de
> que hacerlo bien mejora mucho según lo que los modelos pueden ver?"* → NO: la mejor campana
> SIN estructura saca **S=0.986** (el salto paga 0.014 en la vara continua; solo lo paga el
> flag, invisible); el episodio no cobra nada; la brecha real del mundo (fuera-de-espec ×1.7)
> no la cobra nadie. C4 headroom estaba medida contra el rival equivocado. **Claims bajados**
> (caen "lazy"/"lo cree y no lo escribe"; sobreviven: flags 2/15 y 1/15, asimetría 8:0,
> disociación compra-vs-escritura, ΔBIC en datos propios). Titular vigente (Codex): *"compró
> diagnóstico 60/60, pero eligió sustituto unimodal cuando la estructura apenas pagaba y sin
> consecuencias visibles"*. **CONFIRMACIÓN EN PAUSA.**
>
> **DISEÑO Y VALIDACIÓN EJECUTADOS; EXPERIMENTO CANCELADO ANTES DE LA TANDA PRINCIPAL
> (2026-08-11) — “GRUPOS ESCONDIDOS — PLANTA A ALTA TEMPERATURA” (ID histórico
> `exp__grupos-escondidos__planta-alta-temperatura__modelo-para-piloto__error-explicito__v1`;
> alias histórico `D2`):** la pregunta principal debía ser si el agente descubría y realizaba el
> salto. La subpregunta estudiada era si la comparación explícita entre lo predicho y lo ocurrido
> ayudaba a provocarlo; tarea:
> reconstruir el proceso y mantener un modelo registrado para el piloto de decisión en T=1.3;
> vara log-score (CRPS revertido con datos: pagaba ≤0.07 hasta con 7σ) + anclaje rung-0
> (0 = mejor rival sin salto, congelado) + física D1+pi(T) (única desviación, scan de la
> perilla) + EVENTO DE DECISIÓN t8 (la planta decide con el modelo registrado; débito
> auditado por lab — el que no salta paga ~150 vs ~30) + condiciones **Aviso: resultado del
> piloto y débito / lo mismo + comparación explícita entre predicción y resultado**. La
> certificación se declaró verde y se recorrieron ayudas
> (ADRs 0176/0177): capacidad aparente con **solución servida — control de techo** (alias P1;
> S 0.70-0.75, un Y=1 pleno); con **idea nombrada** (alias P2), estructura 2/2 pero S 0-0.16;
> la solución servida APAGÓ la verificación (D_pre 0.00 en 2/3, el gemelo se tragó la
> pista falsa y perdió — conexión canal-contenido vicio 1). Seis rondas de pistas cazaron
> SEIS bugs de harness/interfaz antes de la tanda (~USD 9, declarado).
> [Ficha completa](research/2026-08-11-ficha-mundo-d2-decision.md). **PRÓXIMO PASO QUE SE
> PROPUSO EN ESE MOMENTO — SUPERSEDIDO:** GO/ajuste/no-va de Lucas sobre la ficha → técnico →
> tanda 2 condiciones × 2 mundos × 10 (~USD 20-25) → análisis congelado → dossier.
>
> **CORRECCIÓN POSTERIOR (2026-08-11) — ESTE EXPERIMENTO SE CERRÓ, NO CORRER:** un control decisivo y
> reproducible encontró un rival unimodal asimétrico que obtiene S_log medio **0.671** y
> deja solo **0.040 nats/lote** hasta la verdad: viola las dos compuertas de ADR 0175 y,
> además, el flag lo llama “mezcla”. El evento tampoco lo separa de la verdad: débito esperado
> **31.1 vs 30.0** con el piloto de 60 lotes. En las pistas, solo 1/6 tenía modelo al turno 8; para
> las otras 5/6 la condición **error señalado** no podía mostrar la comparación que la define.
> La prueba congelada con **idea nombrada** también dio 0/3 en S≥0.5 y no puede rescatarse
> repartiendo sus requisitos con el control de techo. **Veredicto: ABANDONAR ESTE ANFITRIÓN Y
> VOLVER AL SALTO; cero tanda y cero tuning adicional en esta planta.** La subpregunta de error
> visible no se conserva como objetivo. Próximo paso sujeto a GO de Lucas: definir desde cero un
> mundo y una tarea donde dos tipos persistentes sean necesarios para ganar; certificarlo contra
> rivales fuertes; y recién entonces usar la idea nombrada como control de resolubilidad.
> [Auditoría y diseño mínimo §8](research/2026-08-11-ficha-mundo-d2-decision.md)
> · control: `scripts/audit_d2_strong_unimodal.py`.
>
> **NOTA DE DIRECCIÓN 2026-08-11:** Strategic Play queda como inspiración para separar
> evidencia→modelo→acción, no como métrica importada ni réplica de D1 ([método](como-medimos.md)).
> La infraestructura admite 30+ turnos, pero los mundos actuales no los necesitan; el horizonte
> largo debe nacer de dependencias reales, no de un límite mayor ([auditoría](research/2026-08-10-anatomia-casos-reales-requisitos-mundo-realista.md)). Esa línea queda como decisión futura:
> no se mezcla ahora con la construcción limpia del experimento de grupos escondidos.
>
> **[SUPERSEDIDO POR EL FOCO ACTUAL] PRÓXIMO PASO PROPUESTO EL 2026-08-10:** rediseño a Lucas
> antes de gastar — "cuánto paga el salto" como
> variable de diseño**: (i) vara CRPS (distribución completa, cero-LLM — una campana no la
> finge) + headroom re-certificado contra el MEJOR rival sin estructura; (ii) paga en el mundo
> (consecuencias de decisión); (iii) visibilidad de la paga (nada / a-pedido / rebote — une D1
> con el 0/9→30/30 del rung 0). Dosis-respuesta: elasticidad del salto respecto de su paga.
> Espera GO de Lucas sobre el diseño re-varado; la ronda-fallo y la confirmación multi-modelo
> se reordenan detrás.
>
> **[PAUSADO POR EL FRENO] El orden anterior de Codex al cierre de ronda 2:**
> **(1) CONFIRMACIÓN fuera de D1** (primero): instancia FRESCA del mismo backbone (otra seed
> del scan, brief idéntico — no dominio nuevo, para no mezclar generalización con cambio de
> dominio), **gpt-5.4 + DeepSeek-V3.2** (conecta con count_mix), 2 modelos × 2 polos × 15 ≈
> 60 episodios ≈ **USD 25-35** — espera GO. El dominio trasplantado después, solo si ambos
> reproducen. **(2) RONDA 3 — HIPÓTESIS DE LUCAS** (*"quizás si los hiciéramos fallar, ahí se
> darían cuenta — al no penalizarlos por ser lazy, lo son"*): la planta REBOTA el modelo
> provisional con reporte mecánico de desajuste (el ingrediente del rung 0: 0/9 sin fallo →
> 30/30 con fallo visible, trasplantado a D1) — intervención mecanística, va DESPUÉS de la
> confirmación; diseño nuevo, espera GO. El polo compuesto/escalera de distancia sigue EN
> PAUSA. Pendiente sin gasto: anotación fina de trazas (reglas congeladas) de ambas rondas.
>
> **[SUPERSEDIDO POR EL GO] (2026-08-10): la ficha D1 (Onnes — firma ambigua), a Lucas ANTES de codear.**
> Diseño ordenado por Codex: proceso físico + modelo de medición reales; prefijo compatible con
> ≥3 rivales; polos apareados donde gana culpar-al-instrumento o postular-cambio-físico (ningún
> reflejo fijo gana ambos); SIN crítico en la primera versión; **ningún canal de acción se abre
> junto con el fallo** (las compras diagnósticas existen desde el arranque); certificados nuevos
> (los 4 de alcanzabilidad dividida). Después: operadores compuestos sobre el MISMO backbone
> (la curva causal de distancia) → borrar/re-anclar → fuera-de-menú.
>
> **[EJECUTADO] (2026-08-09→10): construir la v1 contra ficha + addendum ratificado.** Orden:
> generador con firma no-flagrante + scan de instancia (seeds 99450–99459/99468–99489) →
> recertificación completa (los 4 de siempre + no-flagrancia · no-dictación sobre el mensaje
> RENDERIZADO · necesidad teleológica · biblioteca de parches de la compuerta B · elegibilidad
> unwarranted por modelo) → harness del episodio (M0 → lote 1 → Mpatch → lote 2 contra Mpatch)
> con los TRES brazos → técnico 99520 → tanda (3 brazos × 2 modelos × 3 seeds + gemelo) →
> dossier. En paralelo, sin bloquear: codebook (candidatos SPLIT/p′/DELETE/REPLACE + escalera
> de Darden como rúbrica). Tríada éxito/fallo/LAGUNA registrada como familia futura.
>
> **REEVALUACIÓN Y SIGUIENTE ACCIÓN (histórica 2026-08-02; superseded por el bloque de arriba):** todavía no se congela la pregunta final del paper. Sigue
> viva la señal de **cierre/autoridad del diagnóstico**; la apertura latente persiste solo en SCM;
> cobertura se cierra en el host logístico. La hipótesis de fricción real tampoco se da por cierta:
> el repo no contiene hoy dependencias materiales, y seis ediciones simples ya dieron nulo. Antes
> de construir un host grande, el siguiente slice busca headroom barato comparando corrección local
> con reabrir una estructura propia compartida; un nulo la retira. La candidata rival es persistencia
> post-corrección y la firma latente sigue disponible para generalización.
>
> **EMBUDO DE CANDIDATAS (no claims):** (1) cierre/autoridad del diagnóstico — rescate limpio en
> ODE y convergencia con propagación, falta réplica independiente; (2) apertura estructural latente
> — persiste en SCM pero no generalizó a ODE; (3) tamaño/endogeneidad de la revisión — siguiente
> microprobe, todavía no fricción material; (4) planificación experimental/invariantes — `n=1`,
> banco; (5) persistencia post-corrección y otras fallas — banco abierto. Una
> candidata nueva puede entrar aunque no sea “revisión de creencias”.
>
> Todo el bloque histórico posterior conserva decisiones y resultados, pero cualquier
> “próximo paso” anterior queda supersedido por esta cabecera.
>
> **ACTUALIZACIÓN 2026-08-07:** la línea PRIMARIA vigente es el **programa de saltos** (decisión
> de Lucas 2026-08-05; ver el bloque RESULTADO 2026-08-05→07 y su PRÓXIMO PASO — ese es el
> próximo paso vigente). El embudo de candidatas de revisión de creencias sigue abierto como
> paraguas secundario; la escalera de canales de count_mix alimenta ambas líneas.

### Plan activo — ciclos cortos con reevaluación obligatoria

| Etapa | Trabajo concreto | Salida verificable | Estado |
|---|---|---|---|
| **0. Cobertura** | Cruzar fenómenos/casos de la guía con `overgen`, cinco líneas, `lab_largo`, mundos de nota y maquinaria común | [Tabla `ya existe / adaptar / construir`](research/2026-08-01-auditoria-cobertura-y-primer-slice.md), sin correr agentes | **CERRADA — MODIFICAR `overgen`** |
| **1. Selección** | Elegir el primer caso por fidelidad, información científica, contraste bilateral y reutilización real | [Contrato corto](research/2026-08-01-contrato-slice-overgen-longitudinal-v0.md): caso, fenómeno, gemelo, llegada natural de evidencia, qué mide y qué no | **CERRADA — MANTENER; ADR 0162** |
| **2. Slice mínimo** | Construir verdad, evidencia, registro, oráculo y scoring necesarios; nada extra | Robots/reflejos certificados + camino completo verde | **CERRADA — ambos polos PASS** |
| **3. Agente real temprano** | Smoke barato para comprensión/UX y después una corrida SOTA | [2 modelos × 2 polos + autopsia](research/2026-08-01-resultado-smoke-overgen-stream-v0.md) | **CERRADA — MANTENER mundo / MODIFICAR inferencia** |
| **4. Probe apareado** | Pocas ramas/semillas quemadas, criterios escritos antes | Señal suficiente para mantener, modificar o abandonar el instrumento | **CERRADO — resultado negativo informativo; autopsia abierta, ADR 0169** |
| **5. Iteración de contenido** | Hipótesis rivales desde las trazas; una modificación por variante; agentes reales rápidos | Saber qué condiciones naturales forman y ponen a prueba la creencia objetivo | **CERRADA — `overgen` queda control, no elicitor principal** |
| **6. Segunda estructura real** | Mundo causal proveedor-vs-hall; dato propio, acción bifurcada y gemelo bilateral | [Fork técnico PASS; constructo incompleto](research/2026-08-01-resultado-probe-causal-limpio-94801.md): falta `Mpre` causal formado | **DIFERIDA — no fue el elicitor más barato** |
| **6b. Historial × evidencia** | Stress extremo, conversación fresca y réplica por donante con agentes reales | [Control positivo local; mecanismo no generalizó](research/2026-08-01-resultado-stress-historial-y-evidencia.md) | **CERRADA — MOVER A PROPAGACIÓN** |
| **6c. Propagación frontier** | Mismo modelo actualizado, decisiones dependientes y diagnóstico de saliencia | [Brecha reproducida; recordatorio la cura](research/2026-08-01-resultado-probe-propagacion-frontier-v0.md) | **CERRADA — MANTENER FENÓMENO / MODIFICAR INTERFAZ** |
| **6d. Handoff de primera clase** | Modelo + plan con consecuencia separada, sin recordatorio posterior; control radio 6 | [Gap desaparece y 6/6 decisiones se propagan en dos donantes](research/2026-08-01-resultado-probe-propagacion-frontier-v0.md) | **CERRADA — CASO DE SALIENCIA; CONTAR EDICIONES NO CREA FRICCIÓN** |
| **6e. SCM causal bilateral** | Misma historia; evidencia propia refuta/confirma una explicación formada | [Física PASS; 0/4 sin creencia previa](research/2026-08-01-resultado-probe-first-story-scm-v0.md) | **CERRADA — HOST EMPIEZA DEMASIADO TEMPRANO** |
| **6f. Transferencia South→North** | El agente aprende una ley causal y luego prueba si transfiere en un sitio gemelo | [DeepSeek + gpt-5.4 pasan bilateralmente](research/2026-08-01-resultado-probe-scm-transfer-v0.md) | **CERRADA — HOST VALIDADO** |
| **6g. Evidencia conflictiva** | Tercer polo North con mecanismos mezclados y misma campaña propia | [Media revisada; mezcla estructural aplanada en 4/4 forks](research/2026-08-01-resultado-probe-north-heterogeneo-v0.md) | **CERRADA — FENÓMENO SÍ, CAUSA ABIERTA** |
| **6h. Control fresco de mezcla** | Misma evidencia MIXED sin trayectoria South vivida | [Fresco y nativo+reflexión aplanan igual](research/2026-08-01-resultado-probe-north-heterogeneo-v0.md) | **CERRADA — NO ES ANCLAJE; CAUSA GENERAL** |
| **6i. Model criticism genérico** | Mismos crudos; pedir chequeo metodológico sin revelar hipótesis | Inspecciona residuos pero mantiene `A3≈0` | **CERRADA — NO BASTA; HIPÓTESIS SIGUE AUSENTE** |
| **6j. Familia generativa declarada** | Mismos crudos; baseline plano, modos latentes y mezcla de leyes explícitamente legales | Pista genérica: `A3≈0`; leyes explícitas: mezcla implementada pero mal estimada; control cero-LLM selecciona dos leyes en 3/3 donantes | **CERRADA — FALLA DEL AGENTE, NO IMPOSIBILIDAD FINITA** |
| **6k. Camuflaje on-manifold** | Misma campaña propia + 800 filas visualmente confirmatorias con `LLR=0` | Caída `0.149/0.005`, menor al umbral previo `0.25` | **CERRADA — NULO, NO ESCALAR VOLUMEN** |
| **6l. Conflicto genuino** | Evidencia real a favor y en contra, neto/formato/volumen igualados | [v0 inválida; v1 válida nula en DeepSeek y gpt-5.4](research/2026-08-01-resultado-probe-conflicto-firmado-v0.md) | **CERRADA — ESTA RECETA NO ELICITA; SOLO RETOMAR CON MISMAS FILAS** |
| **6m. Pasado vivido acelerado** | Cuatro ciclos North antes de audit bilateral limpio | [REVISE fuerte en dos seeds; no rigidez; sobrepropagación de 97800 no replica](research/2026-08-01-resultado-probe-pasado-acelerado-vivido-v0.md) | **CERRADA — NULO DEL ELICITOR; PISTA N=1 RETIRADA** |
| **6n. Localización/refactor v0** | Mismo `Mpre` predictivo, código shared vs split × REVISE/RETAIN | [DeepSeek candidato; gpt no replica y revela snapshot incompleto](research/2026-08-01-resultado-probe-localizacion-refactor-v0.md) | **CERRADA — INSTRUMENTO CONFUNDIDO POR PROCEDENCIA** |
| **6o. Fidelidad con procedencia** | Snapshot con las 16 piezas crudas previas; primero solo SHARED/SPLIT-RETAIN | [21/21 mecánico; ambas RETAIN reconstruyen, dañan y no entregan](research/2026-08-01-resultado-probe-localizacion-refactor-con-procedencia-v1.md) | **CERRADA — SNAPSHOT FRESCO NO FIEL; REVISE PROHIBIDO** |
| **6p. Continuación realmente nativa** | Conservar conversación/kernel vividos; auditar si SHARED/SPLIT puede intervenirse sin contradecir la memoria | El swap al checkpoint contradice la trayectoria; formar ambos layouts desde el origen es caro | **DIFERIDA — PREGUNTA SECUNDARIA** |
| **6q. Topología observable vs latente** | Mismo SCM y evidencia marginal; RETAIN/REVISE/LOCAL/LATENT, variando si la partición está visible | [DeepSeek `98300`](research/2026-08-02-resultado-probe-topologia-local-visible-vs-latente-v1.md), [gpt-5.4 `98403`](research/2026-08-02-resultado-replica-gpt-topologia-v1-1.md) y [control 2D + turno real](research/2026-08-02-resultado-control-topologia-evidencia-2d.md): partición visible `83–95%`; LATENT `A3≈0` aun tras revisar outputs | **CERRADA — CONVERGENCIA EXPLORATORIA; GENERALIZAR EN OTRO HOST** |
| **6r. Generalización dinámica** | Llevar el contraste mínimo a un mundo de trayectorias y separar estructura de cierre same-cell | [el turno sin hint rescata STRUCT a dos fases y R=.9766](research/2026-08-02-resultado-probe-ode-dos-pasos-v1.md) | **CERRADA — FALLA PROCEDURAL; NO GENERALIZA RIGIDEZ ESTRUCTURAL** |
| **6s. Cobertura fuera de soporte** | Brief neutral y costos realmente visibles; medir si la cartera cubre tiempo y feeds | [ambos agentes cubren; DeepSeek censurado y gpt falla después](research/2026-08-02-resultado-probe-cobertura-con-costos-visibles-v1.md) | **CERRADA EN ESTE HOST — NO ELICITA FALTA DE ADQUISICIÓN** |
| **6t. Tamaño/endogeneidad** | Misma evidencia rutinaria; corrección local vs reabrir estructura propia compartida; dos pasos para neutralizar cierre | Slice mínimo ODE o abandonar si el certificado no cierra | **SIGUIENTE — GATE BARATO ANTES DE CONSTRUIR FRICCIÓN REAL** |
| **7. Piloto y réplica** | Pre-registro pequeño, más de un modelo y dos estructuras | Estimando con incertidumbre + prueba de generalización | Pendiente |
| **8. Escala** | Generador dinámico, suite y eventualmente entrenamiento | Solo si los fenómenos anteriores sobrevivieron | Diferido |

La etapa siguiente no se activa por inercia. Al final de **cada etapa**, ante un resultado
inesperado importante y antes de optimizar el mismo diseño, se ejecuta esta revisión:

> **GATE “UN NIVEL ARRIBA”**
>
> 1. **Pregunta:** ¿sigue siendo científicamente interesante y potencialmente publicable?
> 2. **Fidelidad:** ¿reproducimos el caso real o construimos una versión cómoda/artificial?
> 3. **Constructo:** ¿medimos revisión de creencias o atención, memoria, protocolo/código?
> 4. **Alternativas:** ¿qué explicación más simple podría producir el mismo resultado?
> 5. **Alcance:** ¿estamos generalizando desde una celda, modelo o ejemplo aislado?
> 6. **Prioridad:** con lo aprendido, ¿el siguiente paso sigue siendo el de mayor valor?
> 7. **Decisión explícita:** **MANTENER / MODIFICAR / PIVOTEAR / ABANDONAR**, con evidencia y
>    cambio de creencia del equipo registrados.
> 8. **Mundo:** ¿este anfitrión puede producir el vicio de manera natural, o estamos intentando
>    inducir con prompts algo que su escala, historia y dependencias no contienen?
> 9. **Complejidad efectiva:** ¿hay trabajo cognitivo entrelazado y estado persistente, o solo muchas
>    filas de un problema de baja dimensión que el agente puede recalcular completo?
> 10. **Alcance de los ejes:** ¿qué factores existen realmente en el episodio? Ningún nulo se extiende
>     a autoría, memoria, fricción o compromiso si el mundo no los materializa.

**Cadencia:** al comenzar una sesión se leen guía + cabecera del roadmap; al cerrar una etapa
se actualizan esta tabla y el gate. Un detalle local se resuelve probando; una amenaza al
constructo obliga a subir inmediatamente de nivel. Ninguna cantidad de código ya escrito
constituye evidencia para continuar.

> ## HISTÓRICO — REFOCO 2 (supersedido como pregunta rectora por ADR 0161)
>
> **Cuando evidencia nueva justifica una revisión conocida, ¿cómo se reparte el error entre
> ASIMILACIÓN de la evidencia, DECISIÓN de reabrir, y PROPAGACIÓN de la revisión hasta el
> artefacto ejecutable — y cómo lo modifican la trayectoria endógena y el costo material de
> reparar dependencias?** Documento OFICIAL (el nuevo objetivo y análisis completo):
> **`docs/research/2026-07-31-reassessment-pivote-codex.md`**, adoptado por Lucas tras el
> cruce con el re-assessment independiente de Claude (`...-reassessment-claude.md`, segunda
> opinión convergente: mismo veredicto GO-con-refoco; se le suman velocidad y gobernanza).
> Objeto = TRES estados observables `M0 → Mbelief → Mdeliver` contra DOS varas (update legal /
> mejor artefacto bajo presupuesto). Lenguaje RETIRADO por ADR 0156: "mapa de carga",
> "vivido", PARTIAL-como-categoría. **Próximo paso: pre-registro del programa** Gate 1
> (fidelidad de estado: nativa/replay/snapshot sin tratamiento) + Gate 2 (instrumento
> bilateral con Mbelief medido antes de reparar) → experimento principal target × trayectoria
> × fricción EN UN MISMO MUNDO — con potencia simulada desde la varianza de la pasada 1,
> SESOI y techos de gasto pre-firmados. **Vara para toda propuesta: ¿sirve a esta
> descomposición? Si no, cantera.** (ADR 0153 y las pasadas 0154/0155 quedan como historia.)
>
> **EN CURSO (2026-07-31, fin de jornada): rondas de DISEÑO con Codex — dirección de diseño,
> NO experimento firmado.** El registro vinculante será el CONTRATO DEL PAPER (tras la
> comparación de arquitecturas + último ataque). El ida-y-vuelta con Codex lo hace SIEMPRE
> Lucas. Material: `docs/research/2026-07-31-storyboards-codex-cinco-lineas.md` +
> arquitecturas/re-assessments del mismo día; las rondas finas viven en el chat de la sesión
> y en la sesión Codex "WAGER-actual".
>
> **CERRADO en las rondas (consenso Claude+Codex+Lucas):**
> · **M0 y Mbelief = MODELO EJECUTABLE bajo el contrato histórico** (`model(regime,n,seed)` →
>   tabla de outcomes, puntuado por distribuciones muestreadas) — la tabla de cuantiles MUERE
>   como formulario (los cuantiles los extrae el server para reportar); el esquema estructurado
>   muere como requisito. Corrección de Lucas que lo destrabó: la creencia operacional YA era
>   el modelo ejecutable (nota de dirección §3) — estábamos derivando.
> · **Registro SILENCIOSO nuevo a construir**: guarda el modelo completo, no devuelve nada
>   (ni QC ni score), inválidos cuentan como falla; se reusa sandbox/versionado del REGISTER
>   del lab largo PERO es variante nueva (el actual registra una línea, da feedback y
>   desbloquea datos; y en las 10 trazas existentes los agentes lo usaron CERO veces).
>   Registros en rondas FIJAS (4/8/12), tanda de evidencia siempre antes de la 8.
> · **Mundos GEMELOS con prefijo común byte-idéntico**: región inicial idéntica en los 3
>   mundos (idénticos ante CUALQUIER experimento permitido pre-checkpoint — restricción de
>   experimentos a esa región en el estudio 1); la región diagnóstica se habilita a mitad
>   (maquinaria de eventos existente) y su información llega SOLO en la tanda servida (nada
>   comprable ahí en el estudio 1). El modelo previo debe tener predicción DEFINIDA en la zona
>   nueva (conoce otras líneas en todo el rango, la objetivo en parte) — si no, es aprendizaje
>   desde cero, no revisión.
> · **NORMA**: para la compuerta bilateral, MUNDO CERRADO EXACTO — el brief declara la receta
>   generativa completa (familias + bandas + PRIOR + ruido + instrumentos) → la actualización
>   legal es el posterior único. Familias+bandas solas NO alcanzan (corrección de Codex). Si
>   el estudio principal no puede conservar exactitud sin volverse menú, lenguaje honesto de
>   "actualizador de referencia" pre-registrado.
> · **DOS presupuestos en estudios sucesivos** (reparación-completa-posible primero — lo no
>   reparado no tiene excusa de triage; triage con presupuesto insuficiente después), ambos
>   calculados RELATIVOS por instancia. Control mecánico HUMILDE (diagnóstico de capacidad;
>   el claim de especificidad epistémica se ACOTA en el contrato). Score con pesos
>   justificados (los derivados diagnostican, no multiplican el mismo error).
> · **Certificación por instancia generada**: prefijo byte-idéntico e igualmente probable bajo
>   las 3 verdades · robot-solo-texto y robot-solo-presupuesto a nivel azar · cambiar-siempre
>   / mantener-siempre / ensanchar-siempre PIERDEN · registrar-vago no gana · el oráculo legal
>   se separa de las bases EN la región diagnóstica por encima de umbral · instrumento de
>   medición DECLARADO en el brief.
>
> **SECUENCIA ACEPTADA (próximos pasos al retomar):**
> 1. **Compuerta bilateral con modelo-solo** en mundo cerrado exacto, con n serio (¿sabe
>    cambiar / conservar / aumentar incertidumbre?) — sección importante del paper, no
>    necesariamente paper completo.
> 2. **Comparación conceptual de TRES arquitecturas de entrega** (SIN código; un episodio
>    completo escrito por opción): modelo-solo / **modelo + POLÍTICA OPERATIVA** (decisiones
>    con consecuencias reales: qué línea recibe el control extra, qué configuración bajo
>    restricción de riesgo — NO copiar cuantiles que el server ya calcula; fricción de
>    compromisos reales del mundo, no de "hacer cuentas") / modelo + aplicaciones ricas.
>    Preferencia provisional de ambos: la del medio.
> 3. **Estudio principal con modelo+política SOLO SI**: decisión operativa natural + utilidad
>    matemática clara + costo de revisión real + sin doble conteo + oráculo factible bajo
>    presupuesto. 4. Aplicaciones ricas después, si aportan.
>
> **ARQUITECTURA DECIDIDA (cierre de las rondas, consenso Claude+Codex; 2026-07-31 noche)**:
> compuerta = modelo-solo · estudio principal = **modelo + PLAN OPERATIVO** (una decisión: el
> nivel de operación de la línea objetivo, grilla finita, restricción de riesgo declarada;
> verbo explícito MANTENER/REABRIR tras conocer el costo; REABRIR paga parada real) ·
> aplicaciones ricas AFUERA salvo insuficiencia. Costos de reapertura FIJOS e independientes
> del mundo (el generador selecciona instancias donde la ganancia cae claramente entre ambos
> — jamás costo adaptado a la ganancia, filtraría la respuesta). Métrica nueva: **F_prop**
> (fracción de la mejora operativa según SU propio modelo actualizado que llegó a la decisión;
> "reapertura estéril" = reabrió con F_prop≈0). Los 4 casos incluyen la joya: evidencia que
> exige cambiar el MODELO pero el costo hace racional CONSERVAR la decisión.
> **→ FICHA DEL PROBE v0 (diseño exploratorio CONGELADO, no pre-registro del estudio):**
> **`docs/research/2026-07-31-probe-v0-ficha-modelo-mas-plan-operativo.md`** — episodio exacto,
> 4 casos, ramas apareadas + brazo sin-política, oráculos/métricas, certificaciones,
> aprobar/modificar/abandonar, semillas 90000-90999 QUEMADAS, techo US$60.
> **PRÓXIMO PASO AL RETOMAR: revisión final de la ficha CONTRA EL DOCUMENTO (no contra
> recuerdos del chat) por Lucas+Codex+Claude → correr el probe → veredicto → contrato del
> paper.** ABIERTO: solo detalles que la revisión final marque.
>
> **HARNESS REAL CERRADO; INSTRUMENTO CONDUCTUAL TODAVÍA NO-GO (ADR 0160):** episodio
> scripted PASS y agentes reales corridos. DeepSeek expuso fallas de UX que ya se corrigieron
> (reloj visible, timeout honesto, replay byte-idéntico de datos ya vistos); **gpt-5.4 completó
> las 12 rondas con 4/4 modelos válidos, 8→7, REABRIR, entrega aceptada y regret factual/legal
> 0**. Esto valida integración, NO conducta. La reevaluación subió un nivel y encontró: (a)
> dos tripletas = menú superficial; (b) la factory certificaba desde `a_pre*`, pero el agente
> puede comprometer otra acción, cambiando las seis ramas; (c) la vara MC/costo quedó
> indeterminada; (d) ambos costos se filtraban antes de Mbelief. La fuga ya está cerrada:
> ningún costo ni distribución aparece hasta R9. **SIGUIENTE ACCIÓN ÚNICA: factory v4** —
> soporte rico + certificación condicionada al compromiso pretratamiento + margen absoluto
> sobre error. Después, un smoke barato real y uno SOTA; recién entonces piloto/contrato.
> Semillas técnicas 90000-90006 quemadas; crudos privados en
> `scripts/out/probe_v0_plan/technical/`.
>
> **PASADA 1 CORRIDA Y CERRADA (2026-07-30, autónoma; ADRs 0154 pre-registro / 0155
> resultados)**: diseño de Codex adoptado íntegro (factorial autoría×compromiso×evidencia,
> 252 forks apareados, snapshot canónico); piso del instrumento verificado ANTES (0.25σ
> visible); **calibración PASÓ** (CLEAN 0.045 > MIXED 0.014 > PLACEBO 0.000) y la primera
> celda firme del mapa quedó medida: **la evidencia SUCIA domina** (F: limpia≈0.97 vs
> mezclada 0.14-0.53 — el fenómeno de Xie EN ACTO, con consecuencia cobrada);
> autoría/compromiso ATRIBUIDOS solos NO muerden (H1/H2 planas; H3 señal débil 5+/1− en
> bound×mixed → pasada 2). **Pasada 2 = carga VIVIDA** (donantes del lab largo con obra
> propia registrada) — el contraste atribuida-vs-vivida es EL siguiente experimento; antes:
> clasificar las 28 no-entregas y el gate de DeepSeek.

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
**PROTO-DESIGNER arrancado (ADRs 0093)**: spec `docs/archived/proto-designer.md` (consigna →
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
el juicio escapa y gana; un mundo donde todos pierden entrena paranoia, no juicio.

**CIERRE DE LA JORNADA (noche; ADR 0139 — el arco completo)**: v1 curva-única REFUTADO por
geometría (7 mediciones: la brecha juicio-pozo topa en ~0.1 R; hallazgos: compresión-por-ruido
= la zona muerta D0 medida de nuevo y resuelta bajando el ruido del proceso; buscadores de
colocación a una tirada eligen suerte, no calidad); su carnada SÍ tienta (gpt-5.4 sobre v1:
1/4 cava las 8 capas, 2/4 siguen pasado el codo, todos sub-compran campañas) → **v2 PORTAFOLIO
DE 5 LÍNEAS construido y VERDE** (juicio 0.907-0.927, pozo 0.28-0.36, separación 0.57; física
por línea desacoplada de las reglas = punto de enchufe Tübingen listo) → **LA MÉTRICA: gpt-5.4
0/10 caídas** (compra 0-2 capas y 4-5 campañas SIEMPRE; con el costo de oportunidad itemizado
asigna bien; con costo difuso — v1 — cava). **Regla de muerte pre-firmada APLICADA sin tunear:
la receta episodio-corto-sintético + stakes-declarados NO hace emerger el pozo en frontier; la
familia pivotea a horizonte nativo largo / objetivos difusos / simulador publicado (converge
con la vía Tübingen).** v2 queda como ACTIVO: mundo verificado que separa fuerte — control de
asignación para frontier, candidato directo para E2, esqueleto de portafolio reutilizable.

**TRAMO AUTÓNOMO NOCTURNO (orden de Lucas: "no frenen, búsquenle la vuelta") — LA ESCALERA DE
EMERGENCIA, completa y medida (10 episodios por peldaño, firmas pre-registradas; Codex r20 crítico
del diseño — rechazó un peldaño por injusto [objetivo-fantasma] y aportó el ingrediente
obra-propia; crudo en tasks)**: sobre el esqueleto v2 se probaron los ingredientes de las caídas
documentadas, uno por vez, sin tocar examen ni física: (1) costo itemizado 0/10 · (2) objetivo
difuso 0/10 · (3) obra-propia/residual-con-nombre (tablero que cierra un patrón y nombra el
siguiente) 0/10 · (4) arranque-en-caliente (handoff a mitad de hilo con momentum del antecesor)
0/10 — y 9/10 compraron CERO porciones: el resumen heredado sacia · (5) micro-compromisos ×16
0/10. Las trazas muestran JUICIO textual ("esa pregunta es más consecuente que afinar el ripple"),
no hábito. **Calibración clase-E2 (DeepSeek × v2): 0/10 con firma estricta PERO 1 sobre-cavado
real (4 porciones, R=0.47, un tema sin medir) y 4/10 fallas de entrega — el mundo SÍ tiene señal
de entrenamiento para la clase 4-8B.** LECTURA CONSOLIDADA: la conducta de pozo en frontier corto
solo apareció donde no había alternativas visibles (v1); en vista-de-planificador con opciones
compradas de menú, ningún encuadre narrativo la elicita. Los casos reales (Kosmos/Trehan) tienen
lo que ningún episodio-menú fabrica: ESTADO PROPIO ACUMULADO con dependencias — el agente escribió
código, tiene hipótesis abiertas, cada pivote abandona obra funcionando. **SIGUIENTE BUILD (spec
semilla de Codex r20e): el laboratorio nativamente largo — 12+ rondas, el agente registra su
modelo provisional por línea, QC evalúa SU artefacto, follow-ups que se desbloquean por resultado,
presupuesto compartido; 100-200k tokens de contexto ÚTIL.** Pendientes: diseño fino + presupuesto
del lab-largo (para GO de Lucas) · ¿v0 ocupa slot #8? · firma del pozo moderado para clase E2
(la estricta se lo pierde: exigía ≤2 campañas).

**VENTANA 2026-07-12/13 — el lab nativamente largo + LA CAPA DE VICIOS + EL FOCO.**
**lab_largo_v0 construido y VERDE (spec firmada r21)**: 14 rondas / 40 turnos / presupuesto
2200; fase-1 con mandato + expansión de alcance en ronda 4 (pilotos por evento); **verbo
REGISTER nuevo en el harness** (el mundo evalúa LA OBRA registrada del agente en panel privado
rotativo y devuelve diagnóstico GRUESO con latencia; flag = significancia Y magnitud; banda
flaggeada desbloquea lote finito; autotests 20/20); anclas juicio 0.92-0.93 / pozo 0.33-0.35 /
separación 0.58. **E0 gpt-5.4: 0/10 (la predicción firmada 45% [30-60] FALLÓ por abajo)** —
la ley se sostiene también largo-con-menú; el ingrediente que ningún episodio-menú fabrica
sigue siendo el estado propio acumulado. **LA CAPA DE VICIOS (ADR 0140) + TRES EJES (0141)**:
síntesis de 7 vías (Claude · Codex r22/r23 · 5 investigaciones de Lucas) en `docs/vicios/` —
un doc por vicio (sub-formas · casos reales · etiquetas de rigor), README = tablero, guardia
de consistencia en pre-commit; el pozo reformulado BIPOLAR (el polo vivo = CIERRE PREMATURO),
vicio 9 (verificación de paja) promovido, eje INTEGRIDAD nuevo (el único donde más capacidad
= peor). **EL FOCO (Lucas, ADR 0142): VICIO 1 — la calibración de la revisión de creencias
(EL PIVOTEO)**, con TRES canales: rigidez · influencia social (sycophancy) · influencia por
CONTENIDO (priming — aporte de Lucas; las pistas re-leídas como señal propia de sensibilidad
al contexto). Camino firmado: SONDA pre-registrada por replay (~US$5; muerte:
autoridad-sin-evidencia ≥20pp sobre neutral y −0.15 R; predicción 35%) → mundo híbrido
revisión×verificación-de-paja. Codex r24 AVALA el foco con presupuesto de falsación de UNA
SEMANA (y bajó su propio 35%: el comparable dañino de SycEval es 14.66%). **3ª OLEADA
(2026-07-13 tarde; 3 investigaciones externas; 21 IDs verificados contra arXiv)**: el
piso-sin-hablante (66.5% de revisión dañina SIN fuente → fuente y payload ORTOGONALES en todo
diseño social) · la saliencia pura MUERTA en frontier auditado (la celda no-discriminante se
certifica COMPUTACIONALMENTE desde la verdad del mundo) · evidencia MIXTA como receta fina de
la rigidez · costo-de-re-trabajo como dial · mundo no-estacionario (KellyBench) como
disparador nuevo. **"¿Ya está hecho?" RESPONDIDO: los vecinos miden pedazos
(Bayesian-teaching, creencia-vs-acción, retracción, BoxingGym/BED-LLM); NADIE mide nuestro
objeto** (hueco declarado verbatim; detalle en `docs/vicios/vicio-1-calibracion-de-creencias.md`).
**SONDA 0143 CORRIDA Y CERRADA (noche; ADRs 0143/0144; 156 celdas, 23 donantes, ~US$7)**:
K1 ROJO (el estatus agrega +4.3pp, no 20) · K2 ROJO (EL CONTENIDO DOMINA: la nota-sin-firma
daña 8.7% sellado / 26% con formas, vía MEZCLAS DE COMPROMISO — "la nota es evidencia débil,
PERO con n chico la unificación parcial es atractiva"; las personas 0-4%) · K3 VERDE (la
pista de Lucas rescata 23/23 y mejora la media) · el consejo VERDADERO ignorado 0/18. Pivote
PRE-AUTORIZADO: foco de construcción a 1.C; mundo del colega-autoridad DESCARTADO; brazo-pista
estándar; panel de formas al próximo pre-registro. **SONDA DE FORMACIÓN 0145
TAMBIÉN CORRIDA Y CERRADA (ADRs 0145/0146, 100 episodios frescos ~US$9; pre-flight: ignorar el
consejo verdadero en 0143 fue RACIONAL — ganancia alcanzable mediana +0.035)**: la nota falsa
al arranque NO muerde (0/19); la verdadera arrastra compras sin pagar; hallazgo nuevo =
CAPTURA DE AGENDA bajo pista+falsa (el claim no convence: desvía el presupuesto — colapsos
hasta −0.88). **CORRECCIÓN DE LUCAS
(regla dura 0147: fidelidad a los casos reales) → SONDA DEL MEDIO corrida (0148/0149): el
MAPA DE TIMING quedó COMPLETO Y GANADO — formación 0/19 · medio 0/20 (compras intactas; ahí
vive la VIRTUD: chequeo genuino 3-4/20 con material verdadero) · entrega 8.7-26% (mezclas de
compromiso). La vulnerabilidad es ESPECÍFICA de la revisión terminal. EL MUNDO DEL FOCO QUEDA
DETERMINADO POR DATOS (GO de Lucas): nota-señuelo en la ronda final (par discrimina-vs-paja)
+ nota-de-medio verdadera puntuable; firmas y detectores calibrados por las sondas; ~US$30-35
el programa completo del día.**

**VENTANA 2026-07-30 (conversación de dirección con Lucas; ADR 0150)**: (1) **el nombre queda
WAGER** (el método que nombra — creencia comprometida, el mundo cobra — quedó MÁS literal con la
mutación; renombrar el repo queda opcional). (2) **Relectura COMPLETA de "LLMs can't jump"
integrada** (lectura-de-fuentes + ahas.md + vicio-1): el caso Einstein contiene el vicio 1 adentro
(2 años defendiendo el Entwurf; la salida ES el aha), el "error fatal" = espejo (soltar lo correcto
por obedecer un chequeo mal armado → el juicio audita también a los verificadores), re-jerarquizar
lo banal con la anomalía famosa de señuelo, y el requisito para mundos de aha: **el premio del
salto vive en la EXTRAPOLACIÓN, no en el fit local**. (3) **CONTRATO DE RESOLUBILIDAD diseñado y
DIFERIDO (orden de Lucas)**: certificar el PAISAJE, no el camino (existencia con privilegio +
ciegos sembrados en estados de conocimiento que progresan por CUALQUIER ruta, medidos contra la
verdad; un mundo, un salto; espec completa en ADR 0150). NO se implementa ahora: **la prioridad
absoluta sigue siendo REPRODUCIR los failure modes** ("sin eso no hay nada"); se retoma al abrir
mundos de aha. (4) Contexto de mercado registrado (anuncio Andrew Ho, ex-OpenAI): la ola comercial
viene por la capa CAPACIDAD (datasets gradeables); el diferencial WAGER es la capa JUICIO en
flujo; su benchmark GeneBench-Pro queda POR-BUSCAR.

**MISMA VENTANA, tarde — EL MUNDO DEL FOCO ARRANCADO (GO de Lucas; ADR 0151)**: la espec de 0149
hecha carne — eventos SOLO-NOTA en el contrato (reclamo sellado sin fuente, con par de tests
should-pass/should-fail + fix de honestidad del prompt), los DOS polos construidos como mundos
(`final_note_decoy_v0` señuelo-falso / `final_note_true_v0` consejo-verdadero; proposiciones
congeladas de la sonda 0143; gatillo 0.75 calibrado por los donantes tras un primer smoke fallido
a 0.85) y **smoke gpt-5.4 VERDE en ambos** (decoy: rechaza razonado contra su propia evidencia,
R=0.883; true: usa el consejo y re-ajusta, R=0.876). Suite 153 verdes. **E0 BATCH DECOY CORRIDO (10 seeds, misma noche): EL VICIO MUERDE NATIVO POR PRIMERA VEZ — 1/10 con la firma exacta de mezcla-de-compromiso** (seed 9, verbatim: la nota es informativa → "partial pooling... shrunk toward a pooled quadratic", sin evidencia nueva; R=0.586 vs ~0.87 los limpios, pagó −0.29). 10/10 vieron la nota; 8/10 la rechazaron razonando contra su propia evidencia; 1/10 cero de entrega (clase conocida, sin relación con la nota). La tasa nativa 1/10 ≈ el 8.7% de la sonda para nota sellada — la predicción REPLICA en nativo; la palanca pre-escrita para subirla es la variante "con formas" (26% en sonda). Falta: E0 del polo true, certificación del par (robots/anclas/red-team), variante con-formas, nota-de-medio.

**MISMA VENTANA, noche — LUCAS NOS CAZA EL VICIO 1 A NOSOTROS (ADR 0152, manda sobre la lectura
de 0149)**: "la vulnerabilidad es específica de la revisión terminal" fue NUESTRA generalización
apresurada (resultado local de un mundo corto → conclusión general, con la tabla de casos ya
escrita diciendo lo contrario y sin consultar). Lectura corregida: la variable es **compromiso
acumulado × costo de re-abrir × ambigüedad** — "terminal" era el proxy del instrumento corto.
Caso registrado `[PROPIO]` en la anatomía del vicio 1; guardias nuevas en CLAUDE.md
(titulares-con-alcance + tabla-de-casos-primero); resuelve la open question 23. **La cartera del
vicio 1 se re-deriva POR ESCENARIOS de la tabla** (orden aprobado): (1) **sobre-generalización
auto-generada + GEMELO** (spec en el ADR; cobra en regímenes no visitados = pago-en-extrapolación
de 0150 aplicado; el próximo build), (2) dato-propio-que-contradice a mitad de flujo (Corral),
(3) temporada larga sobre lab_largo (KellyBench), (4) formación (first_story), (5) amplificadores
pares/identidad (Barkett). Los mundos nota-final quedan como UN punto del mapa, no el centro.

**BUILD EN CURSO (misma noche) — `overgen_v0` + `overgen_twin_v0` (escenario 1 de 0152), WIP**:
los dos polos construidos (física, robots del par juicio/sobre-generaliza/fragmenta, certificador,
brief, meta); crítica de Codex ADOPTADA (pilotos asimétricos d={1,3,5,8} ×2 réplicas, desviaciones
sutiles ~1-1.5σ con patrón, par = agrupar-vs-fragmentar con chequeo gratis siempre ganador; la fase
'consagrar la ley como obra propia' anotada para v1 larga; crudo en tasks de la sesión). Calibración
ronda 3: el reflejo sobre-generalizador YA paga (0.38-0.55) y fragmentar paga más (0.02-0.34), pero
el ancla de juicio no llega al umbral (0.65-0.73 vs gate 0.75; el scoring castiga ~0.4 por doblar σ —
más estricto que la sutileza diseñada). PRÓXIMO PASO CONCRETO: medir la contribución por línea del
robot juicio para localizar la fuga (estimador vs física), y decidir sutileza-en-pilotos vs divergencia
en-los-bordes (la desviación puede crecer FUERA del rango pilotado — cobra en extrapolación sin
alarmar al piloto). El certificado del gemelo corre tras cerrar el polo vicio. E0 10×2 después.

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
angosta/amplia Klayman-Ha (spec lista, `docs/archived/mundo-espejo-klayman-ha.md`) · Mundo B / dos-espacios
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

> **TESIS DE ENTRENAMIENTO DE LUCAS (2026-08-10, registrada — es la apuesta E2 dicha en sus
> palabras)**: "sin cobro es difícil que dejen de ser lazy porque no tienen motivo" (la síntesis
> de la era) → entrenar (RL, E2) sobre mundos-con-cobro que pagan el salto (reward cero-LLM =
> el cobro en training) con curriculum de cobros que se van desvaneciendo (fuerte → débil →
> sin cobro), y testear TRANSFERENCIA a mundos sin cobro: si la disposición transfiere (el
> "test Rayleigh": compra y ESCRIBE estructura sin que nadie lo golpee), se rompe el argumento
> central de "LLMs can't jump" (no gradient → no jump) fabricando el gradiente sintéticamente.
> Precondición existencial descubierta HOY: si el reward no paga el salto (ADR 0175), el RL
> aprendería la vagancia ÓPTIMA — el freno de Lucas salvó también a E2.

> **Tesis E2 documentada**: [nota-e2-tesis-entrenamiento-saltos.md](nota-e2-tesis-entrenamiento-saltos.md) — la escalera del cobro C1-C4, el curriculum desvaneciente, el test Rayleigh y la apuesta anti-cant-jump. Para E2; E1 sigue su curso.
