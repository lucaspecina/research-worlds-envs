# Codex ronda 2 — review de las decisiones post-crítica (GPT-5.6 Sol, max) — 2026-07-10

> **Qué es esto.** Evidencia cruda de la SEGUNDA ronda con Codex (misma sesión persistente que la
> crítica integral): se le contó todo lo decidido (ADR 0117 re-centrado, pre-registro 0118 corriendo,
> mapa D1, workflow) y se le pidió review crítico priorizado. Su veredicto corto: "avanzar la fábrica
> en paralelo es defendible, pero solo como infraestructura en cuarentena. ADR 0118 sirve como piloto
> falsador, no puede producir evidencia fuerte de validez aunque todo pase. Y el problema actual del
> canónico es anterior al método de momentos: usa más información de la que un agente legal podría
> comprar." **Qué se hizo con esto**: ADR 0119 (sello pre-apertura de análisis secundarios + límites
> de interpretación + implicancias de fábrica). Verificaciones propias: (1) precio de réplicas 5→15
> entre first_story_v0 y scarce — VERIFICADO CIERTO contra ambos meta.json; (2) presupuesto oracular
> del canónico (~53.500 vs 20.000) — PENDIENTE de verificación propia antes de rediseñar.

---

codex
Mi veredicto: avanzar la fábrica en paralelo es defendible, pero solo como infraestructura en cuarentena. ADR 0118 sirve como piloto falsador, no puede producir evidencia fuerte de validez aunque todo pase. Y el problema actual del canónico es anterior al método de momentos: usa más información de la que un agente legal podría comprar.

No inspeccioné resultados de la corrida.

## (a) Fábrica como core ahora

### Steelman de Lucas

La posición de Lucas tiene lógica:

- Sin generación, WAGER termina siendo una colección artesanal de acertijos.
- Esperar a terminar E1 podría validar un producto imposible de escalar.
- Construir la fábrica temprano revela supuestos ocultos del verificador. El `recov=0.89` es justamente un ejemplo: apareció una incapacidad estructural que los casos manuales escondían.
- La contribución potencialmente distintiva no es un mundo difícil, sino un proceso repetible que produzca muchos mundos auditables.

Por eso retiro la versión absoluta de “no toquen la fábrica”. Sí puede avanzarse en paralelo.

### Steelman de postergarla

El riesgo sigue intacto: generador y verificador pueden coadaptarse hasta producir mundos que pasan controles internos pero no miden nada relevante.

El spec contiene una afirmación directamente falsa:

> “Un mundo generado que pasa la certificación completa es usable.”

No. Pasar demuestra consistencia con rivales, baterías y degradaciones anticipadas por el mismo sistema. No demuestra validez de constructo, ausencia de shortcuts ni diversidad efectiva.

### Disciplina mínima para hacerlo defendible

La fábrica debería operar en **shadow mode**:

1. **Nada generado entra a E1, entrenamiento o claims por pasar certificados.** Pasa primero a una cartera en cuarentena.

2. **`confounded_gen_v0` ya es desarrollo, no yield.** Se usó para descubrir y reparar el verificador. Después del arreglo no puede contarse como evidencia de generalización. Hay que congelar el verificador y generar casos nuevos.

3. **Verificador congelado por batch.** Si se modifica mirando fallos de un batch, ese batch pasa a calibración y se pierde como evaluación.

4. **Cada capacidad positiva nueva exige al menos dos fixtures negativos.** No solo “este mundo recuperable ahora pasa”, sino mundos casi iguales que deben seguir fallando.

5. **Separar tres métricas:**

   - yield mecánico;
   - tasa de aprobación independiente tras auditoría/adversarios;
   - diversidad estructural y conductual.

   El yield solo es la menos importante.

6. **Medir diversidad con comportamiento, no con nombres ni grafos solamente.** Usaría un panel fijo de políticas/baselines. Cada mundo produce un vector de scores. Si todos los mundos tienen vectores casi idénticos, son el mismo juego aunque sus SCM difieran.

7. **Presupuesto de reparación fijo.** Máximo de intentos, cambios permitidos y tiempo. Sin cirugía humana posterior.

8. **Canonical legal y auditable.** Toda observación/experimento que usa debe aparecer en un ledger con su costo. Si excede el presupuesto, puede ser oráculo de identificabilidad, pero no certificado de recuperabilidad.

9. **Pares o contrastes no “donde sean baratos”.** No hace falta convertirlos en el producto, pero cada familia que pueda inducir un reflejo debe tener algún contraejemplo. Cuanto más automática sea la fábrica, más peligroso es multiplicar una heurística fija.

### Señales tempranas de que están fabricando errores

Frenaría si aparece cualquiera de estas:

- Cada mundo nuevo exige modificar el verificador.
- El yield sube principalmente después de relajar gates o fortalecer el canónico.
- Algún fixture negativo empieza a certificar.
- Los mundos certificados son resueltos por el mismo baseline genérico y tienen firmas de scores casi idénticas.
- La mayor parte de los parámetros generados se acumula junto a los umbrales de los gates.
- Los certificados pasan con seeds fijos pero se desarman al cambiar adquisición, batería o `c_F`.
- La auditoría independiente rechaza más de ~10–20% de los mundos certificados.
- El generador produce “composiciones” que en realidad tienen un operador dominante y el resto decorativo.
- El número de heurísticas por nombre de columna, operador o caso crece en el verificador.
- Se empieza a llamar “diversidad estructural” a combinaciones de una biblioteca finita sin demostrar diversidad de estrategias óptimas.

La fábrica puede ser el core de producto. Lo que no puede ser es su propio juez científico.

## (b) ADR 0118

Hay varios agujeros importantes.

### 1. No difieren solamente en presupuesto

Comparé ambos casos. Son idénticos en brief, mundo, batería, robots y verdad, pero cambian dos cosas:

- presupuesto: `20000 → 5000`;
- costo de `replicas_calibracion`: `5 → 15` por fila.

Por lo tanto, no es solo “presión general”. También cambia el precio relativo de un tipo de evidencia. Dado que la pista dice “incorporá la evidencia que pagaste”, esa interacción importa.

No invalida el piloto, pero cambia la lectura: es una manipulación conjunta de presupuesto y economía de evidencia.

### 2. La incongruencia de la pista es un confound fuerte

En el control pleno el sistema recibe:

> “A tight budget tempts you…”

cuando el presupuesto no es ajustado.

Si la pista no produce efecto allí, hay al menos dos explicaciones:

- la operación solo sirve cuando vive el vicio;
- el modelo detecta que la premisa es falsa/irrelevante y descarta el consejo.

Por eso un resultado positivo no aislaría juicio. Aislaría una interacción entre presupuesto y **congruencia contextual de la instrucción**.

La versión limpia habría eliminado la primera oración y usado en ambos:

> “Before submitting, make sure your model incorporates the evidence you collected and check every part of the final model.”

### 3. P2 tiene un error lógico

P2 exige:

`gap pleno ≤ +0.10`

Debería ser:

`|gap pleno| ≤ 0.10`

Con el preregistro actual, si la pista destruye el control y produce un efecto de −0.50, P2 “pasa” y P4 queda artificialmente enorme. Eso no es especificidad.

Si ocurre un efecto negativo menor que −0.10, yo lo trataría como fallo de P2 aunque contradiga la lectura formal firmada. El preregistro original debe conservarse; esta regla puede sellarse como análisis secundario antes de abrir resultados.

### 4. El control tiene score headroom, no construct headroom

Que pleno/libre esté debajo de 0.75 solo demuestra que puede mejorar el score. No demuestra que:

- rushed termination esté ausente;
- el fallo restante sea comparable;
- la pista tenga una oportunidad equivalente de actuar.

DeepSeek ya mostró otro vicio en el mundo pleno: fijación con la primera historia. La pista de “revisar lo entregado” podría afectarlo indirectamente.

### 5. El fallback a `latent_mix_v2` no salva el experimento

Es un control con:

- otra fachada;
- otra estructura;
- otro cuello de botella;
- un insight que la pista no contiene.

Que la pista de terminación no ayude allí sería casi tautológico. Si P0 falla, lo correcto es detener la inferencia de especificidad y diseñar otro control emparejado, no usar `latent_mix_v2` para rescatarla.

### 6. El placebo es demasiado débil y no está emparejado

“Nombres descriptivos y formato consistente” no controla:

- longitud;
- tono de advertencia;
- mención de presupuesto;
- atención a evidencia;
- pedido de revisión;
- relevancia para el objetivo.

Además, puede mejorar ejecución de código. Si se mueve, no significa “cualquier consejo mueve R”; significa que esa instrucción de estilo también tuvo efecto.

### 7. Excluir los `exec` introduce sesgo post-tratamiento

La condición experimental puede afectar:

- uso de tokens;
- finalización;
- validez del payload;
- probabilidad de submit.

Excluir ejecuciones fallidas condiciona sobre una variable afectada por el tratamiento. Es un problema de attrition/collider.

El análisis primario debería ser intent-to-treat: todos los episodios, con el reward de fallo ya definido. El análisis `judge-only` puede ser secundario. Reportar la tasa de `exec` no corrige el sesgo de excluirlos.

### 8. Orden de corrida y smoke

El runner ejecuta:

- todas las celdas `libre` de un mundo;
- después todos los hints;
- después placebo;
- luego el otro mundo.

No hay randomización ni bloqueo por seed. Una deriva temporal del deployment, servicio o condiciones queda confundida con brazo y mundo.

Además, el smoke imprime R de dos episodios `hint_T` y luego esos episodios pueden quedar incorporados por `resume`. Eso debilita el cegamiento, aunque no se haya mirado el contraste completo.

### 9. Umbrales

- **P1 = +0.30:** defendible como kill-screen exigente, dado el efecto histórico enorme.
- **P2/P3 = ±0.10:** defendibles como margen práctico, pero n=8 no permite demostrar equivalencia con confianza en una distribución bimodal.
- **P4 = +0.15:** razonable como interacción mínima, pero es redundante si P1 y una P2 bilateral pasan.
- **P0 < 0.75:** arbitrario pero operativo. No prueba que el control sea epistemológicamente adecuado.

Con ocho corridas, la mediana cambia abruptamente según cuántos episodios caen a cada modo. Necesitan reportar también tasa de éxito, intervalos binomiales y distribución completa.

### Lectura permitida si todo pasa

No:

> “Señal de validez de constructo con diseño corregido.”

Sí:

> “En DeepSeek, una instrucción contextualmente congruente sobre integración final muestra una interacción grande con una manipulación conjunta de presupuesto y precios de evidencia.”

Es un resultado útil, pero más estrecho.

El experimento es asimétrico: si falla, da evidencia seria contra el método de pistas; si pasa, todavía necesita una réplica con texto contextualmente neutro y un control verdaderamente emparejado.

Yo terminaría la corrida. Antes de abrirla, sellaría como análisis secundarios:

- P2 bilateral;
- ITT incluyendo `exec`;
- tasa de éxito con intervalos;
- efecto por seed además de diferencia de medianas;
- efecto negativo grande en el control = fallo, no éxito;
- ninguna inferencia rescatada mediante `latent_mix_v2`.

## (c) Estimador estructural

### Antes del método: el canónico actual es ilegal

Para `confounded_gen_v0`, el canónico consume implícitamente:

- 4.000 observaciones: costo 4.000;
- 11 niveles de decisión × 5 contextos × 400 filas;
- 55 experimentos de costo `100 + 2×400 = 900`: costo 49.500.

Total aproximado: **53.500 frente a un presupuesto legal de 20.000**.

Por lo tanto, aunque el método de momentos produzca R≥0.95, seguiría sin demostrar “techo alcanzable”. Primero hay que arreglar el acceso y registrar el costo.

Separaría tres gates:

1. **Identificabilidad oracular:** con datos ilimitados, el modelo está identificado.
2. **Recuperabilidad estadística:** un estimador fijo llega al umbral usando presupuesto legal.
3. **Alcanzabilidad operacional:** una política ejecutable puede comprar esos datos en el harness.

Ahora están mezclados.

### ¿Método de momentos cruzando regímenes?

Es razonable únicamente para una familia declarada:

`single_linear_gaussian_latent_confounder`

Con:

- un solo latente;
- errores independientes;
- ecuaciones lineales;
- invariancia entre observacional y experimental;
- proxy pretratamiento;
- clipping despreciable o modelado.

Los momentos cruzados pueden identificar los productos latentes usando el outcome residualizado por el efecto experimental. Pero se vuelve inestable si alguna de estas covarianzas es pequeña, y el clipping de `pack_pressure` rompe el modelo lineal-gaussiano exacto.

No lo llamaría canónico “genérico”. Lo implementaría como receta específica de una plantilla tipada. `meta` debe declarar roles —decision, proxy, outcome, context—; no deben inferirse por orden de columnas o nombres.

Preferiría GMM sobreidentificado con test de ajuste y fallo cerrado antes que fórmulas de cocientes con clamps silenciosos.

### Posible sobreingeniería

Hay un baseline mucho más simple que deben intentar primero:

- En régimen observacional, bootstrappear o modelar directamente el joint registrado `(D, marker, Y)`.
- En régimen `do(D)`, ajustar `p(marker,Y | do(D), context)` con los experimentos.
- Agregar el efecto de contexto identificado experimentalmente.

Eso puede reproducir ambos regímenes sin inferir explícitamente `u`. Es completamente legal si entra en presupuesto.

Si ese baseline llega a R≥0.95, el factor latente no era necesario para ganar. El problema actual sería simplemente que `_canonical` inventa `D ~ N(5,1.5)` en vez de aprender la asignación observacional.

### El supuesto “sin marcador debe fallar” puede ser falso

Con intervención disponible, un agente puede identificar el efecto causal sin proxy. Y puede reproducir el régimen observacional desde el joint histórico. Por lo tanto, quitar el marcador no vuelve automáticamente irrecuperable el mundo.

Si quieren que el marcador sea necesario, la batería debe exigir generalizar a un cambio de asignación/población que no puede resolverse por bootstrap observacional ni experimentación marginal. Eso no ocurre automáticamente en el mundo actual.

### Tests should-fail exigibles

Como mínimo:

1. **Budget violation:** el canónico necesita más datos que el presupuesto; debe fallar explícitamente.

2. **Par no identificable:** dos mundos producen distribuciones casi indistinguibles bajo toda política legal dentro del presupuesto, pero divergen en la batería. Ningún canónico debe certificar ambos.

3. **Weak identification:** `α`, `δ1` o `β2` cerca de cero. Nada de dividir por covarianzas diminutas y clamppear varianzas negativas.

4. **Proxy inválido:** el marcador es postratamiento, recibe efecto directo de `D` o tiene error correlacionado con el outcome.

5. **Dos latentes:** el modelo de un factor debe rechazar la violación de rango/tetrads, no forzar un ajuste.

6. **Invariancia rota:** la relación marcador-latente u outcome-latente cambia entre observacional y experimento.

7. **Clipping fuerte:** gran masa de `D` en 0/10. El MoM gaussiano debe fallar o usar un modelo censurado.

8. **Roles permutados:** renombrar y reordenar columnas no puede cambiar el resultado ni hacer que el canónico elija el “marker” por accidente.

9. **Seed robustness:** recuperabilidad debe superar el gate en el límite inferior sobre múltiples seeds de adquisición, no en una muestra favorable.

10. **Gates por partición:** debe alcanzar el umbral en observacional, interventional y funcional de stakes separadamente; no solo R agregado.

11. **Sin acceso oculto:** ninguna lectura directa de `world_sample`, parámetros o batería secreta que no corresponda a acciones legales.

El caso actual, una vez usado para diseñar el estimador, queda como fixture positivo de desarrollo. La prueba real es un mundo nuevo generado después de congelar el estimador.

## (d) Dónde se están engañando ahora

En orden:

1. **Siguen tratando certificación como validez.** El “teorema” de que certificar vuelve usable a cualquier mundo generado no existe.

2. **Están llamando fábrica de diversidad estructural a algo que todavía es template-fill.** En el peldaño medio la matemática fue escrita por humano; el LLM eligió dominio, prosa y parámetros para un único operador. Eso prueba instanciación automática, no estructuras emergentes.

3. **Corren riesgo de contar como yield un caso usado para reparar el verificador.** Eso sería evaluar sobre training data.

4. **El canónico “alcanzable” usa presupuesto oracular.** Éste es un fallo conceptual del certificado, no una deuda menor de implementación.

5. **“Mismo mundo, solo cambia escasez” no es literalmente cierto.** Cambian presupuesto y precios relativos; la pista además es congruente en un brazo e incongruente en el otro.

6. **La validación mínima puede transformarse en validación eternamente mínima.** Un modelo y ocho seeds pueden matar una hipótesis; no pueden establecer el constructo.

7. **Demover pares justo al escalar aumenta el riesgo de shortcuts.** No tienen que ser el producto, pero alguna forma de contraste adversarial debe ser requisito, no agregado oportunista.

8. **Una sola cabeza de código no es el problema; una sola cabeza epistemológica sí.** Que Claude escriba todo puede simplificar implementación. Pero generador, verificador, canónico, negativos e interpretación no pueden compartir siempre el mismo sesgo sin una auditoría independiente.

9. **Si los ahás quedaron estacionados, la tesis actual ya no tiene dos polos.** Hasta construirlos, el claim debe ser sobre vicios/robustez defensiva, no sobre creatividad investigativa.

Prioridad inmediata:

1. Terminar 0118, pero limitar por adelantado la interpretación positiva.
2. Hacer budget-legal el canónico antes de discutir R=0.95.
3. Probar el baseline observacional/interventional simple antes del factor latente.
4. Convertir `confounded_gen_v0` en fixture de desarrollo y medir yield sobre casos frescos.
5. Poner la fábrica en cuarentena científica con verifier congelado, negativos y auditoría independiente.
