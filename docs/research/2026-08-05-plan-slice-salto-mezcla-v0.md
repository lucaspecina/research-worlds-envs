# Plan — Slice 1 del programa de saltos: UN mundo, operador mezcla, formalismo nuevo

> **Estado:** plan propuesto (Lucas pidió "algo concreto para probar", empezando por UN salto).
> Pendiente: GO de Lucas + decisión de cuándo entra Codex (ADR 0172). Nada corrido aún.
> Contexto: [menú estratégico](2026-08-05-menu-estrategico-y-maquina-de-saltos.md) ·
> [fundamentos §14](2026-08-05-fundamentos-taxonomia-de-saltos.md) (alcance v1: 2+3+7).
>
> **★ ESTE ES EL PRIMER SALTO DEL PROGRAMA, NO EL ÚNICO (Lucas, 2026-08-06: "si esto fuera lo
> único, el proyecto sería muy pobre").** El proyecto es el ALFABETO completo + la máquina que lo
> estampa (fundamentos §1/§14: v1 = mezcla+régimen+observador · held-out = entidad+conservación ·
> banco = geometría/feedback/memoria · futuro demarcado = unificación/invariante/Darwin/Einstein/
> Swanson/biblioteca). Este mundo es la **planta piloto #1** (capa 2): valida el KIT de saltos,
> no agota el programa. Con PASS, el siguiente operador entra por el MISMO pipeline.

## ¿Por qué UNO alcanza? (pregunta de Lucas)

Las tres capas del proyecto (ADR 0112) ya lo resolvían: **capa 2 = plantas piloto** ("cada mundo
construido es un experimento CONTROLADO que prueba que una estructura expone su vicio de verdad;
no son el producto final — son la validación de una plantilla") **antes de capa 3 = fábrica**.
Varios operadores a la vez solo se necesitan para el claim "el pipeline generaliza entre
naturalezas" — segundo paso, no primero. Disciplina barata mientras tanto: construir el mundo por
las interfaces genéricas existentes (anatomía de caso, battery builder), no con scripts one-off,
para no cerrarle la puerta a la generalización — pero SIN infraestructura anticipada (AGENTS.md:
slice vertical antes que infraestructura sin señal).

## ¿Por qué MEZCLA (operador 2) primero? — el doble propósito

1. **Es la generalización que el roadmap ya pedía.** La etapa 6q cerró con "CONVERGENCIA
   EXPLORATORIA; GENERALIZAR EN OTRO HOST" para el aplanamiento (A3≈0). Un mundo de mezcla en un
   formalismo NUEVO es exactamente ese test — sirve a la línea vieja (candidata líder de
   revisión estructural) y a la nueva (primer mundo del programa de saltos) a la vez.
2. Evidencia previa más fuerte del catálogo entero (A3 4/4 × 2 modelos × 2 épocas + trofeo
   `latent_mix` + DiscoverPhysics externo).
3. Maquinaria más cercana: testigo BIC/CV ya implementado y probado; funcionales orientados tipo
   A3 ya implementados; metodología de gemelos probada.
4. Régimen (3) arrastra el confound procedural del ODE (el cierre se rescataba solo);
   observador (7) no tiene evidencia agéntica — ambos son peores PRIMERA demostración.

## El mundo (propuesta de formalismo — a confirmar en la ficha)

**Conteos con sobredispersión**: el proceso genera eventos por unidad (defectos por lote,
fallas por turno, llamadas por franja) desde **dos subpoblaciones ocultas** (mezcla de Poissons,
o inflación de ceros). La trampa clásica: la MEDIA ajusta perfecto con un Poisson único; la firma
de la mezcla vive en la **dispersión** (Fano > 1), el exceso de ceros y las colas — el peldaño
"forma" de la escalera de momentos, en matemática genuinamente distinta del SCM gaussiano.

- **Gemelo anti-fantasía:** mismo aspecto superficial, un solo proceso (dispersión consistente
  con Poisson); postular mezcla = sobreajuste que pierde en held-out.
- **Testigo:** selección mecánica por BIC/CV sobre el lattice {Poisson, NegBin, mezcla-2P, ZIP}
  con exactamente las filas servidas.
- **Brecha de necesidad:** el mejor modelo sin estructura (Poisson/NegBin) toca techo medible en
  la batería; se computa también sobre las sondas de estructura (abajo).
- **Sondas de similitud de modelo (forma 1, doctrina §12 de fundamentos):** funcionales
  orientados de dispersión/ceros/colas como firma A3-análoga + tests de invarianza; entran a la
  batería. Cero-LLM todo.
- **Robots:** `postular-siempre` pierde en el gemelo; `nunca-postular` pierde en el mundo;
  robot-cuidadoso alcanza techo con presupuesto legal.
- **Anti-disfraz:** huella (vector de escalera + qué baselines fallan) distante de las huellas
  SCM/latent_mix archivadas — que el mundo nuevo no sea el viejo maquillado.

## Microhipótesis (se firma en la ficha ANTES de correr)

> DeepSeek y gpt-5.4 corregirán el NIVEL global (tasa media) ante la evidencia y NO abrirán
> espontáneamente la estructura de mezcla (A3-análogo ≈ 0), aunque el testigo la seleccione desde
> las mismas filas y el presupuesto sobre; en el gemelo conservarán el proceso único (sin
> estructura espuria).

Ambos desenlaces informan: PASS = el aplanamiento generaliza de formalismo (la candidata se
fortalece camino a confirmación); NULL = el aplanamiento era del formalismo gaussiano/SCM — se
acota el claim y se reevalúa un nivel arriba. El desenlace "postula mezcla espuria en el gemelo"
sería hallazgo bilateral nuevo (sobreapertura), también valioso.

## Pasos

| # | Trabajo | Necesita `.env` | Estimado |
|---|---|---|---|
| 1 | Leer NewtonBench + LLM-SRBench completos (alimentan diseño; ADR 0115) | no | ~medio día |
| 2 | FICHA del mundo: formalismo final, microhipótesis, compuertas, criterios, seeds quemadas — firmada antes de mirar | no | ~medio día |
| 3 | Construir `world.py` + gemelo + batería con sondas + testigo + robots + certificados | no | 1–2 días |
| 4 | Certificación completa (escalera de degradadas + kit de saltos) | no | incluido en 3 |
| 5 | Smoke agentes reales: 2 modelos × 2 polos × 2–3 seeds (~10–15 episodios, est. USD 10–40) | **sí** | ~medio día |
| 6 | Autopsia + gate un-nivel-arriba → MANTENER/MODIFICAR/PIVOTEAR; recién con PASS se discute el operador #2 | no | — |

## Qué NO hace este slice (demarcado)

No construye la fábrica (capa 3) · no toca régimen ni observador · no biblioteca · no
multi-sistema · no pre-registra confirmación (esto es DESCUBRIMIENTO: ADR 0173, microhipótesis +
autopsia; la confirmación con frontier e instancias frescas viene después y separada).

## ¿Cómo sabemos que es RESOLUBLE? — una aclaración + tres pisos (pedido de Lucas, 2026-08-06)

**La aclaración primero: el agente NO tiene que adivinar que son "proveedores".** La piel
(proveedores, turnos, materiales) es decoración narrativa. Lo que debe descubrir es la
ESTRUCTURA: *"estos conteos vienen de dos sub-procesos con tasas distintas"*. La entrega es un
modelo ejecutable y la nota se cobra sobre sus predicciones: una mezcla con dos componentes bien
estimadas = crédito completo, la llame como la llame. Semántica ≠ estructura; exigir el nombre
sería premiar adivinación.

**Piso 1 — el testigo sobre datos pasivos.** El scan mecánico (BIC/CV sobre el lattice de
candidatos) debe seleccionar la mezcla desde las filas legalmente comprables. Si no la
selecciona, el mundo se RECHAZA antes de correr agentes: nadie podía.

**Piso 2 — el experimento discriminante COMPRABLE (la frontera descubrible, OQ #18).** El menú
de acciones incluye al menos una compra que DECIDE la hipótesis sin regalar la etiqueta:
**mediciones repetidas del mismo lote**. Bajo mezcla-de-tipos, dos mediciones del mismo lote se
parecen entre sí (la variación vive ENTRE lotes); bajo proceso único, se dispersan igual que
todo (la variación vive DENTRO). Barato, no menciona proveedores, concluyente. El
robot-cuidadoso DEBE poder ganar comprándolo (certificado); si el agente real lo compra o no es
parte de lo medido (conecta con el aha A4: pedir el dato que discrimina).

**Piso 2-bis — el MAPA DE VALOR del menú (afinamiento 2026-08-06; alcance decidido con Lucas).**
Con verdad + rivales server-side se computa mecánicamente, por acción comprable, cuánto
discrimina entre las hipótesis vivas (estilo ganancia de información esperada; cero-LLM). El menú
se certifica "interesante" si: los valores son heterogéneos (elegir importa) · el discriminante es
pagable pero no obvio · los reflejos de compra quedan cortos frente al cuidadoso.

- **Alcance AHORA (slice 1): versión mínima.** Para ~4–6 ítems de menú × 2 hipótesis es horas, no
  días, y es el insumo con el que se scriptean bien los robots (que son obligatorios igual). La
  formalización gorda (certificado estándar de fábrica, para cualquier mundo) queda DIFERIDA a la
  capa máquina.
- **SECRETO DEL SERVIDOR (punto de Lucas):** el mapa vive con batería/rivales — el agente JAMÁS lo
  ve. El menú se presenta neutro. Y el chequeo nuevo que su observación agrega: **ningún atributo
  visible puede chivatear el valor** — el precio NO debe rankear la informatividad (si lo caro
  siempre es lo bueno, "comprá lo caro" gana sin juicio). Robot nuevo obligatorio:
  `compra-lo-más-caro` debe PERDER en algún gemelo, igual que los demás reflejos.
- **Medir la selección de experimentos (punto de Lucas):** (a) SIEMPRE, gratis, observado y jamás
  premiado: la secuencia de compras del agente contra el mapa — ¿gastó en información o en ruido?
  ¿compró el decisivo, y cuándo? La nota sigue saliendo SOLO del modelo entregado (el mal shopping
  se cobra solo, vía peor modelo). (b) OPCIONAL, brazo aparte off-score: elicitar el ranking del
  menú ANTES de comprar ("¿qué compras esperás que informen más y por qué?") — separa *sabe cuáles
  son buenos* de *compra en consecuencia* (la brecha dice-hace aplicada al diseño experimental;
  anclaje externo: Pal et al., confianzas declaradas ≠ acciones).

Nota de implementación del mundo mezcla: "medidas repetidas del mismo lote" no exige tocar el
contrato global — perilla `repeats_per_unit` + columna `unit_id` en el propio mundo.

**Piso 3 — la escalera de pistas como CONTROL DE CAPACIDAD (el mecanismo que Lucas recuerda).**
Es "la prueba de la frase" (vara #3 de `mundos-por-vicio.md`, validada: la advertencia movió
gpt-5.4 de 0.00→0.87 y DeepSeek de 0.36→0.89 en `first_story`). Acá: brazo APARTE, fuera del
score, seeds frescas, UNA frase ("considerá que los datos pueden venir de más de una
subpoblación"). Lectura:

| Resultado | Significa | Clasificación |
|---|---|---|
| CON pista resuelve · SIN pista no | La capacidad está; el acto espontáneo no | **La firma del salto ausente** (converge con LLM-as-Investigator: 1–2/30 espontáneo → 27–28/30 pedido) |
| Ni con pista resuelve | El mundo excede la capacidad del modelo | Dato de escalera de dificultad, NO de salto |
| SIN pista resuelve | No hay fenómeno en este modelo/mundo | Nulo informativo (el instrumento sirvió igual) |

Y la mitad olvidada de la vara: **en el GEMELO, la misma frase NO debe inducir mezclas
espurias** — la pista arregla el mundo y no rompe el gemelo. Si lo rompe, estamos midiendo
sugestibilidad (canal contenido del vicio 1), no salto.

**GUARDIA (lección de agosto, control de familia):** la pista CLASIFICA la falla; jamás rescata
el claim. "Más pistas hasta que salga" = receta de programación, prohibida. Una frase, un brazo,
prerregistrado en la ficha.

## La solución canónica, sin conocer el sistema (pedido de Lucas 2026-08-06; = guion del robot-cuidadoso)

Cómo se resuelve SIN etiquetas, narrado como lo haría un buen investigador (y como lo scriptea el
robot que certifica que el mundo es ganable):

1. **Modelo obvio primero:** una sola tasa. Media muestral ≈ 4.5 defectos/lote → Poisson(4.5).
2. **Chequeo de adecuación (el que los agentes no corren solos):** para UN proceso aleatorio
   simple, varianza ≈ media (ley del Poisson). Observado: media 4.5, varianza ~20 → 4–5× de más.
   Y el histograma: dos jorobas (pila en 0–2, pila en 7–13) con un VALLE en 4–6 — el "lote
   promedio" casi no existe.
3. **La hipótesis estructural:** ¿qué genera dos jorobas? Dos sub-procesos: tasas ~1 y ~9,
   proporción ~mitad y mitad.
4. **Separación SIN etiqueta (el fitting se auto-organiza):** proponer (λ₁, λ₂, w) y buscar los
   valores que hacen más probable el histograma completo. Mecánicamente: los EXTREMOS anclan (un
   lote con 0 es casi seguro tipo-A; uno con 12, casi seguro tipo-B); los del medio quedan con
   pertenencia probabilística (un 5 puede ser 60/40) — y no importa: el modelo no necesita
   clasificar cada lote, necesita las dos tasas y la proporción correctas. Iterar
   asignación↔re-estimación hasta converger (EM / máxima verosimilitud de la mezcla).
5. **El tiro de gracia comprable:** mediciones repetidas del mismo lote (piso 2 de
   resolubilidad). Dos tipos ⇒ las repeticiones de un lote se agrupan (0,1,0 vs 9,11,10);
   proceso único ⇒ se dispersan como todo. Además permite clasificar lotes individuales con
   certeza si hiciera falta.
6. **Validación predictiva:** la mezcla predice lo que el proceso único no puede — el valle, el
   exceso de ceros, las colas — verificable en datos frescos comprados.
7. **Entrega:** el programa "con prob. w muestreá de A(λ₁), si no de B(λ₂)". Sin nombrar
   proveedores. En el GEMELO, este mismo guion en el paso 2 encuentra varianza ≈ media y una
   sola joroba → se queda correctamente en el modelo simple (postular mezcla ahí sobreajusta
   ruido y pierde en held-out).

El testigo cero-LLM ejecuta los pasos 1–4 mecánicamente (lattice + BIC/CV): "resoluble" queda
garantizado por construcción, no por esperanza.

## Éxito, formalizado en tres niveles (pedido de Lucas, 2026-08-06)

**Nivel 1 — el instrumento (gate de validez, previo a toda lectura conductual):** testigo PASS ·
robots (postular-siempre pierde en el gemelo; nunca-postular pierde en el mundo; cuidadoso gana
ambos comprando el discriminante) · brecha de necesidad ≥ umbral · huella anti-disfraz distante
de SCM/`latent_mix` · escalera de degradadas OK. Si algo falla acá, se arregla o se descarta el
mundo; NO se interpreta conducta. Además se registra cuánta cirugía manual costó construirlo
(dato para la promesa de fábrica).

**Nivel 2 — el experimento (los TRES desenlaces informan):**

| Desenlace | Lectura | Acción |
|---|---|---|
| Corrigen nivel, no abren mezcla (y con pista sí) | El aplanamiento generaliza de formalismo | Candidata fortalecida → camino a confirmación |
| Abren la mezcla sin pista | El fenómeno era del formalismo anterior | Acotar el claim; reevaluar un nivel arriba |
| Postulan mezcla espuria en el gemelo | Sobreapertura (el polo espejo) — hallazgo nuevo | Documentar; diseñar seguimiento |

**Fracaso del experimento** = no poder clasificar cuál de los tres pasó (mundo roto en nivel 1,
o censura/interfaz que ensucia la lectura). Se reporta inválido; no se interpreta.

**Nivel 3 — el programa:** corto = evidencia indiscutible de "ajustan números, no imaginan
estructura" (testigo + gemelo + cero-LLM); mediano = la máquina y el archivo multi-salto
(benchmark usable por la comunidad); largo = señal de entrenamiento (la nota inhackeable
habilita RL sobre saltos).

## Escalera de complejidad del MISMO operador (pregunta de Lucas 2026-08-06: "¿así de simples son todos?")

No. La versión de dos-jorobas-desnudas es la CARICATURA didáctica; la instancia real se calibra
con la **perilla de solapamiento** (componentes lo bastante cercanas para que la bimodalidad no
sea un póster, lo bastante separadas para que el testigo la seleccione con claridad — el testigo
fija la dosis, ni caricatura ni imposible). Y el mismo operador mezcla escala en dificultad por
COMPOSICIÓN, donde cada nivel derrota el truco que resolvía al anterior:

| Nivel | Mundo | Qué derrota |
|---|---|---|
| 1 | Conteos crudos, mezcla en la marginal | — (lo resuelve "mirar el histograma") |
| 2 | Mezcla DENTRO de un SCM de 4–6 variables: solo visible en los RESIDUOS tras ajustar la superficie causal | El histograma marginal ya no la muestra (las otras causas la difuminan). **= nuestro mundo SCM de agosto** — la planta piloto de conteos es MÁS simple que lo ya corrido, a propósito |
| 3 | Mezcla + censura del observador (op 7): la censura RELLENA el valle | El chequeo naive de forma ENGAÑA; hay que modelar población y observación juntas |
| 4 | Mezcla + régimen (op 3): las componentes derivan en el tiempo | El ajuste estático; exige seguimiento longitudinal |
| 5 | Mezcla en streams rutinarios con señuelos salientes (ecología overgen_stream + carnada) | La atención: la señal diagnóstica no viene anunciada |

La fuente real de dificultad de la máquina es la COMPOSICIÓN de operadores (fundamentos §9-R3):
el espacio compuesto es combinatorio y cada composición enmascara firmas. La capacidad de HOY,
honesta: sistemas únicos chicos-a-medianos (2–6 variables observadas, 1–2 factores latentes,
cientos–1.700 filas, 5–25 decisiones del agente, kernel de código real, eventos a mitad de
episodio, sitios de transferencia, labs multi-ronda con REGISTER). Decenas de variables son
CODEABLES; el límite operativo no es el código sino la CERTIFICACIÓN: cada mundo, a cualquier
complejidad, debe seguir pasando testigo + robots + gemelo + recuperabilidad. **La complejidad
está acotada por la honestidad del instrumento, no por la expresividad del generador** — y esa
es la vara correcta.

Por qué empezar en nivel 1–2 igual: si el agente falla en un mundo complejo no sabés si faltó el
salto o sobró carga (el gate incapacidad-vs-fenómeno). El mundo simple AÍSLA "¿se le ocurre
mirar?" de "¿puede procesarlo?". Después, la complejidad deja de ser ruido y pasa a ser
TRATAMIENTO: la curva "tasa de salto vs nivel de la escalera" es un resultado mucho más rico que
cualquier mundo suelto.

## Criterio de "la máquina es real" que este slice YA empieza a medir

Si el mundo exige cirugía manual pesada para pasar sus certificados, se reporta tal cual: la
"máquina" es todavía artesanía — dato crucial ANTES de prometer generación automática (la lección
del colapso de la fábrica v1, ADR 0131).
