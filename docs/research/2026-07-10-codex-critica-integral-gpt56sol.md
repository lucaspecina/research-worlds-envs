# Crítica integral de Codex (GPT-5.6 Sol, esfuerzo max) — 2026-07-10

> **Qué es esto.** Evidencia cruda de la PRIMERA consulta a Codex como segunda opinión (ADR 0116):
> se le pidió leer WIKI.md, docs/roadmap.md, docs/failure-modes.md y docs/mundos-por-vicio.md
> completos y dar una devolución crítica objetiva en 5 puntos (core/dirección · problemas ·
> pivoteos · publicabilidad · mejoras). Sesión persistente 019f4a37-2a60-7d51-8ecd-a989ba8767bb
> (continuable con `codex exec resume --last`). ~196k tokens usados.
> **Qué se decidió con esto**: ADR 0117 (se adoptan las correcciones al experimento de pista y la
> higiene de claims; se SOBRESEE "postergar la fábrica" por decisión de Lucas). Verificación propia:
> el punto "trampa y control recibieron pistas DISTINTAS" se chequeó contra ADR 0097 y ES CIERTO.

---

Veredicto corto: WAGER tiene un núcleo defendible, pero la tesis actual está sobredimensionada. Hoy existe un entorno prometedor para evaluar **identificación activa de sistemas bajo datos engañosos y presupuesto limitado**. Todavía no existe evidencia suficiente para afirmar que mide “juicio investigativo” como constructo general, mucho menos que entrenarlo ahí vaya a transferir a investigación real.

## 1. El core y la dirección

La dirección básica tiene sentido:

- Un mundo ejecutable permite experimentar y conocer la verdad de referencia.
- Una entrega ejecutable permite medir generalización fuera de los datos observados.
- Un reward sin LLM elimina arbitrariedad, fragilidad y gaming retórico del juez.
- El presupuesto convierte la selección de evidencia en parte del problema.

Pero hay una diferencia enorme entre estas tres afirmaciones:

1. “El score mide qué tan bien predice el modelo entregado.” Esto sí.
2. “Los mundos contienen trampas que perjudican a ciertos agentes.” Hay evidencia preliminar.
3. “El score mide juicio investigativo y entrenarlo produce mejor juicio general.” Esto no está demostrado.

El problema de fondo es que **calidad predictiva final no equivale a calidad del juicio que la produjo**. Un agente puede llegar a una buena maqueta por AutoML, fuerza bruta, suerte o un template aprendido. Otro puede investigar correctamente y fallar implementando el código. Por eso no compraría la frase “entiende cómo funciona de verdad”: como está definido, WAGER prueba equivalencia conductual sobre una batería finita, no comprensión ni mecanismo correcto.

El rol correcto hoy es:

- Primero, benchmark diagnóstico y banco de stress tests epistemológicos.
- Después, si pasa E1 de verdad, entorno de entrenamiento experimental.
- Solo con transferencia entre estructuras y formalismos, método para entrenar juicio.

Presentarlo ya como plataforma de entrenamiento debilita el proyecto porque pone la apuesta más especulativa adelante del activo que realmente existe.

La regla zero-LLM es útil, pero no debería convertirse en religión. Garantiza que el score no contiene una opinión de otro modelo; **no garantiza validez, objetividad semántica ni ausencia de gaming**. La subjetividad no desaparece: se desplaza al diseño del mundo, los rivales, la batería, los stakes, los funcionales y sus pesos.

## 2. Problemas potenciales

### El agujero principal: score alto ≠ buen juicio

Los certificados con robots prueban algo mucho más débil de lo que el proyecto les atribuye:

- Un robot diseñado para cometer cierto error pierde.
- Otro robot diseñado con conocimiento de la solución gana.

Eso demuestra sensibilidad interna del mundo a esas dos políticas. No demuestra que:

- todo agente que cometa el vicio vaya a perder;
- todo agente que gane haya realizado el “ahá”;
- el vicio sea la causa de que un modelo real haya perdido;
- no exista un pipeline genérico que gane sin ninguna de las operaciones cognitivas postuladas.

Es un test unitario del mundo, no validación del constructo.

El propio paper de Ríos-García et al. concluye que la evaluación por outcome no detecta razonamiento científicamente defectuoso. El repo lo presenta como confirmación externa, pero en realidad plantea una objeción directa a WAGER. Para responderla, WAGER debe demostrar empíricamente que cada mundo transforma el proceso defectuoso en pérdida de outcome; no alcanza con afirmarlo o mostrar dos robots escritos por el diseñador. [Ríos-García et al., 2026](https://arxiv.org/abs/2604.18805).

### El experimento de validez positivo no valida lo que dice validar

Los ADR 0098/0110 son bastante más débiles de lo que concluye el roadmap.

Primero, la resta de diferencias central compara tratamientos distintos:

- `first_story_scarce` recibe “incorporá la evidencia que compraste y verificá la entrega”.
- El control recibe otra pista, sobre buscar alternativas y pivotear.

Eso no es un difference-in-differences válido: cambiaron simultáneamente mundo y tratamiento. Para validar la pista de terminación hacía falta un control con headroom que recibiera **exactamente la misma pista**.

Segundo, el control de DeepSeek está en R≈0.997. Un efecto nulo ahí casi no informa nada porque hay ceiling effect.

Tercero, clasificar como “juicio” todo cero que entregó un programa válido es injustificado. Un programa válido puede estar mal por integración, código, modelado o mala gestión del tiempo. “Entregó algo” no convierte automáticamente el fallo en epistémico.

Más grave todavía: la pista positiva es literalmente un checklist —“usá la evidencia, verificá cada parte”—. Según el propio corte del catálogo, si un checklist o mejor scaffold arregla el problema, es **OPERACIÓN**, no juicio. Por la definición interna de WAGER, el resultado principal puede estar demostrando exactamente lo que dice excluir.

La réplica muestra un efecto real de prompting. No muestra todavía validez de constructo. Llamarla “replicada en dos modelos” es correcto solo si se completa la frase: **replicación de un efecto de instrucción sobre desempeño**, no del constructo “juicio”.

### La frontera operación/juicio no es estable

El criterio “¿lo arreglaría un mejor scaffold?” no define una clase natural:

- depende del modelo;
- depende del scaffold probado;
- depende del presupuesto;
- puede cambiar con futuras arquitecturas;
- es difícil demostrar un negativo: nunca sabés que ningún scaffold lo arreglaría.

El propio catálogo oscila sobre OSWorld, memoria, preguntar, terminación y error-signal blindness. Eso permite reetiquetar retrospectivamente fallos para mantenerlos dentro de la tesis. Necesitan criterios observables y preregistrados, no una clasificación basada en intuición causal posterior.

### Circularidad del diseñador

La batería pesa donde la verdad discrepa con rivales anticipados por el diseñador. Los funcionales se agregan cuando la distancia base no ve la estructura instalada. Los robots se construyen según la operación que el mundo pretende exigir.

Todo eso es razonable para construir un test controlado, pero genera una circularidad:

> diseño una estructura, diseño adversarios que no la ven, diseño una métrica que la ve y certifico que separa a esos adversarios.

Eso no prueba que el ítem capture una habilidad general. Prueba que el ítem codifica eficazmente el contraste que su autor quiso codificar.

La protección real contra esto no es otro certificado interno: son baselines adversariales no anticipados, mundos congelados, validación externa y transferencia estructural.

### El reward tiene demasiados grados de libertad

Energy distance + funcionales de stakes + `c_F` + MDL + caps + batería ponderada + anclas + clipping es un scorer complejo y parcialmente autorado.

Problemas concretos:

- `zlib(AST)` no es una medida seria de complejidad científica. Depende de librerías disponibles, boilerplate y trucos de codificación.
- El MDL puede penalizar incertidumbre honesta y favorecer programas compactos que delegan complejidad a una librería.
- Combinar fidelidad general y utilidad del cliente en un único número oculta tradeoffs que el propio repo ya observó.
- `clip(0,1)` aplana todo lo inferior al ingenuo, justo donde RL necesitaría señal.
- La normalización contra un ingenuo distinto por mundo no demuestra comparabilidad psicométrica entre ítems.
- Una batería finita no elimina equivalencia entre mecanismos ni overfitting.

Yo reportaría las monedas por separado y dejaría la complejidad como eje Pareto, no como un λ dentro del score principal.

### Confound ejecución/código

Obligar a entregar Python introduce una carga grande de:

- programación;
- manejo de RNG;
- contratos tabulares;
- estadística generativa;
- debugging;
- uso de librerías.

Los controles ayudan, pero no aíslan completamente estas habilidades. Para separar juicio de ejecución necesitan una condición de “ejecución oracular”: el agente elige hipótesis, variables y experimentos, pero un compilador/modelador común implementa la maqueta. Comparar esa condición con el modo end-to-end permitiría estimar cuánto se pierde por juicio y cuánto por ingeniería.

### Diversidad actual insuficiente

“11 mundos hechos” suena más avanzado de lo que es. La auditoría interna ya muestra:

- cinco causales;
- varios controles;
- un mundo fuerte de estructura escondida;
- cero mundos en varios vicios centrales;
- casi ningún par completo bajo la doctrina nueva.

Reskins, parámetros y seeds no crean diversidad de juicio. Crean réplicas del mismo truco. La fábrica no resuelve el problema intelectual esencial.

El riesgo es entrenar el reflejo “siempre buscá un confusor/latente/anomalía”. Los pares son una buena respuesta conceptual, pero hoy son mayormente doctrina y specs, no evidencia.

### Entrenamiento y sim2real

RL sobre episodios largos, código arbitrario y reward terminal será caro, ruidoso y con muy mala asignación de crédito. Ya hay evidencia reciente de que RL con reward de ejecución puede mejorar el promedio mientras colapsa hacia ideas simples, sin mejorar el máximo alcanzable. [Si et al., 2026](https://arxiv.org/abs/2601.14525).

E4 es todavía más incierto. El delta “con datos vs. sin datos” no elimina contaminación: los datos pueden actuar como clave que recupera de memoria el ensayo. Además, los mundos sintéticos son cerrados, estacionarios y completamente especificados; la ciencia real tiene misspecification, objetivos disputados, instrumentos desconocidos y verdad parcial.

**Lo más frágil de todo es el puente “predicción correcta en un mundo diseñado → juicio investigativo general”.** Si ese puente no se valida, queda un benchmark de system identification. Eso puede seguir siendo útil, pero es otra tesis.

Lo que podría hacer que no le importe a nadie es bastante claro: que un baseline genérico de Bayesian experimental design + AutoML alcance el techo, o que el ranking sea explicado casi enteramente por capacidad de código. En ese caso, toda la taxonomía de vicios sería una narrativa superpuesta a una tarea estándar.

## 3. Direcciones y pivoteos

Mi recomendación no es abandonar WAGER, sino achicar y afilar brutalmente la pretensión.

### Pivote principal: “paired epistemic stress tests”

Posicionaría WAGER como:

> Benchmark de identificación activa bajo ambigüedad, compuesto por pares contrafácticos donde una misma operación epistémica es correcta en un polo e incorrecta en el otro.

Ese es el diferencial más defendible. “Juicio general” quedaría como hipótesis a validar, no como definición consumada.

Durante el próximo tramo frenaría:

- RL;
- el diseñador automático difícil;
- la expansión a ocho vicios;
- nuevas pieles.

Y concentraría todo en cuatro a seis pares completos, realmente distintos:

- confirmar vs. buscar refutación;
- entidad latente real vs. parche espurio;
- anomalía estructural vs. ruido;
- unificación causal vs. apofenia;
- persistir vs. abandonar;
- intervenir vs. observar.

### Validación factorial de verdad

Para cada par:

- Misma superficie, presupuesto, interfaz y distribución de dificultad.
- Misma pista aplicada en ambos polos.
- Pista irrelevante/placebo.
- Control sin vicio pero con headroom.
- Condiciones libres, scaffold general y pista específica.
- Modelos, prompts y seeds preregistrados.
- Ítems congelados antes de correr los modelos principales.

La interacción relevante sería:

`polo × pista × modelo × presión`

No “una mediana subió en una tarea”.

### Baselines que intenten destruir la interpretación

Antes de llamar “juicio” a un mundo, deberían correr:

- Bayesian optimal experimental design;
- active learning genérico;
- symbolic regression;
- AutoML flexible;
- un agente “siempre sospechá latentes”;
- un agente “siempre intervení”;
- búsqueda masiva no semántica;
- un predictor que ignore la narrativa.

Si alguno gana ambos polos sin la discriminación postulada, el par no mide lo que dice.

### Separar capacidad de implementación

Evaluaría cada agente en dos condiciones:

1. End-to-end, escribiendo código.
2. Epistémica, con implementación común/oracular.

La diferencia mide ejecución. El score dentro de la segunda condición se acerca mucho más al constructo buscado.

### Pivote de respaldo

Si la validez discriminante falla, no tiraría la maquinaria. Renombraría el producto:

> Robust Active System Identification under Misleading Data.

Es más angosto, pero científicamente honesto y todavía útil para entrenar agentes que experimentan bajo selection bias, confounding, latentes y distribution shift.

## 4. ¿Es interesante/publicable?

Sí hay algo interesante, pero **el estado actual no alcanza para un paper fuerte de benchmark**. Yo hoy lo vería como workshop paper, demo técnica o preprint de método. No lo presentaría todavía como instrumento validado ni como método de entrenamiento.

El resultado más fuerte para mostrar no sería “un modelo sacó 0.096”. Eso solo demuestra dificultad. El resultado fuerte sería:

> En varios pares contrafácticos, un hábito fijo gana sistemáticamente un polo y pierde el otro; agentes mejores compran evidencia discriminante y ganan ambos; el efecto persiste con ejecuciones igualadas, controles con headroom, humanos y formalismos retenidos.

Eso sí sería un claim nuevo y limpio.

Lo que no es novedoso:

- Mundos científicos simulados e interactivos: ScienceWorld y [DiscoveryWorld](https://papers.nips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html).
- Mundos generativos, experimentación activa y evaluación predictiva: [BoxingGym](https://arxiv.org/abs/2501.01540).
- Tareas sintéticas y análisis por facets/failure modes: [DiscoveryBench](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0d70af566e69f1dfb687791ecf955e28-Abstract-Conference.html).
- Investigación evaluada mediante métricas objetivas o harness ejecutable: [MLRC-Bench](https://arxiv.org/abs/2504.09702), [ResearchGym](https://arxiv.org/abs/2602.15112) y [MLS-Bench](https://arxiv.org/abs/2605.08678).
- Rediscovery de insights con análisis de fallos del proceso: [FIRE-Bench](https://arxiv.org/abs/2602.02905), aunque su matching semántico sí usa LLM.
- Taxonomías de patrones epistemológicos en trazas: [Ríos-García et al.](https://arxiv.org/abs/2604.18805).

Por eso no es defendible decir “nadie está parado ahí”. El espacio está muy ocupado.

Lo potencialmente novedoso es la **combinación precisa** de:

- pares de polos;
- evidencia discriminante comprable;
- entrega ejecutable;
- reward primario completamente programático;
- mundos derivados de fallos documentados;
- certificados adversariales por par.

Pero hoy esa combinación está mayormente escrita como doctrina. Para ser contribución necesita una suite terminada y resultados que muestren que agrega información por encima de capacidad general, código y benchmarks vecinos.

Un paper de entrenamiento sería mucho más fuerte, pero requiere E3: transferencia a estructuras y formalismos completamente retenidos, contra controles de cómputo igualado. Sin eso, sería otro caso de RL aprendiendo el generador.

El catálogo de vicios, por sí solo, no es un dataset novedoso. Podría convertirse en un dataset interesante si publican trazas, intervenciones, etiquetas cegadas, contrafácticos y pares; actualmente es una taxonomía curada.

## 5. Qué mejoraría

En orden de prioridad:

1. **Bajaría el claim.** “Juicio investigativo” como hipótesis paraguas; “adaptación epistémica en identificación activa” como constructo realmente medido.

2. **Declararía no validado el experimento actual.** Es señal preliminar de sensibilidad a instrucciones, con tratamiento no emparejado y control saturado.

3. **Completaría pares antes de ampliar vicios.** Cuatro pares fuertes valen más que veinte mundos desbalanceados.

4. **Agregaría baselines no-LLM fuertes.** Si BOED/AutoML gana, hay que saberlo ahora.

5. **Separaría ejecución de juicio experimentalmente**, no solo clasificando ceros después.

6. **Simplificaría el leaderboard.** Predictive proper score y pérdida del cliente por separado; complejidad y costo como ejes separados. Nada de esconder toda la geometría en un único R.

7. **Usaría estadísticas apropiadas para resultados bimodales.** Tasa de éxito, intervalos binomiales y modelos jerárquicos; no medianas de cinco u ocho corridas presentadas como señal limpia.

8. **Congelaría un held-out estructural ya.** Todo lo que se retoca mirando frontier deja de servir como evidencia principal.

9. **Postergaría fábrica y RL.** Automatizar un instrumento no validado solo fabrica errores más rápido.

10. **Endurecería la higiene de claims.** Hay contradicciones entre documentos sobre qué tareas usó Ríos-García y sobre si la réplica DeepSeek sigue pendiente. En un proyecto cuya tesis es el rigor epistemológico, esas inconsistencias erosionan confianza más de lo normal.

Mi recomendación brutal: durante el próximo ciclo no construyan “más WAGER”. Intenten **refutar WAGER** con un par completo, controles bien emparejados, ejecución oracular y baselines genéricos. Si sobrevive, tienen una contribución real. Si no, descubrirán a tiempo que estaban midiendo system identification, obediencia al prompt o capacidad de código bajo una etiqueta demasiado grande.
