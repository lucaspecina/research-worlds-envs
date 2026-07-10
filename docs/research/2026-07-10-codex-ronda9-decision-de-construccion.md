# Codex ronda 9 — decisión de construcción (delegada por Lucas) — 2026-07-10

> Lucas delegó a Claude+Codex decidir qué construir, mirando alto nivel. Veredicto: GO al caso fresco (como "piloto post-freeze de instanciación automática de plantilla causal tipada", 8 requisitos, sin segundo operador); SÍ a rigor-estadístico antes que pozo (pozo degradado a perilla/distractor posterior); y el agregado clave: MICRO-BATCH N=5 congelado entre el piloto y la plantilla nueva — "el norte 0117 no es lograr un caso: es multiplicar; sin ese intermedio, fábrica-core seguiría apoyada en dos anécdotas 1/1". Crudo:

codex
Decisión: **sí al caso fresco ahora; sí a adelantar rigor sobre pozo; pero entre ambos falta un micro-batch del peldaño medio**. Un 1/1 solo prueba que el tubo no está muerto.

### 1. Caso fresco del peldaño medio: GO

Debe quedar descrito como:

> Piloto post-freeze de instanciación automática de una plantilla causal tipada.

No prueba yield, diversidad real, composición emergente ni validez del vicio. Prueba que una instancia nueva puede atravesar el pipeline congelado sin que el pipeline se adapte a ella.

**No agregaría un segundo operador ahora.** Confounding + selección/canal chocaría con D10 y la ruta admisible congelada; otro wiring convertiría el ensayo en medio+/difícil. Si falla, no sabrían si falló la generación fresca o la composición nueva. Primero contesten la pregunta firmada.

Lo mínimo para que sea informativo:

1. **Contexto limpio del generador:** llamada stateless que vea solo plantilla tipada, roles, rangos y contrato. No mostrarle `confounded_gen_v0`, batería, rivales, thresholds ni diagnósticos históricos.

2. **Dominio admisible explícito:** fuente identidad, `obs_half=true`, confounding en mechanism layer, contexto aditivo e invariancias soportadas. Cualquier salida fuera de esa clase cuenta como fallo, no como “unsupported interesante”.

3. **Algo más que maquillaje:** antes de llamar al LLM, congelar por seed un estrato paramétrico distinto del fixture —por ejemplo otra banda de fuerza del confounder y otra relación signo/asociación observacional–efecto causal— pero dentro de la clase soportada. No hace falta otro operador; sí evitar el mismo punto central con nombres nuevos.

4. **Libertad exacta:** el LLM elige dominio, semántica y parámetros dentro de ese estrato. La plantilla y el wiring no cambian. Writer separado y ciego.

5. **Presupuesto de intento:** un artefacto inicial + las ≤3 reparametrizaciones numéricas ya firmadas. Nada de cambiar estructura, prompt o prosa al ver gates. Congelar qué diagnóstico recibe el autoajuste: idealmente gate y margen agregado, nunca ítems de batería.

6. **Resultados exhaustivos:** guardar prompt, modelo/snapshot, temperatura/seed, salida cruda, cada intento y ledger. Clasificar `pass`, `fallo dentro de clase`, `salida fuera de clase` o `fallo de plumbing`.

7. **Regla de quema:** cualquier cambio posterior en generador, verificador, thresholds o consigna convierte ese caso en fixture y obliga a correr una seed fresca.

8. **Lectura sellada:** `1/1 = existe una segunda instanciación fresca certificable de esta plantilla`; `0/1 = piloto fallido`. Ninguno estima yield.

### 2. Rigor antes que pozo: sí

Respaldo el cambio de cola. **No eliminaría el pozo; lo degradaría de “próxima plantilla” a perilla/composición posterior.**

El pozo sigue siendo valioso porque AHC no reproduce exactamente persistencia bajo evidencia ambigua, pero su núcleo —local optima, sunk cost, pivotear bajo presupuesto— ya recibe presión genérica fuerte. WAGER aportaría aceleración y diagnóstico, no cobertura especialmente distintiva.

Rigor estadístico ofrece más:

- una situación poco presente en code/math/AHC;
- una nueva clase de presión epistémica;
- reutilización de maquinaria ya existente de mediciones replicadas, ruido y presupuesto;
- scoring natural sobre la distribución predictiva, sin juez LLM.

Empezaría por una plantilla dedicada de **precisión fabricada / decisión de replicar**: sin réplicas, el agente no puede separar variación real de error de medición; declarar una distribución demasiado estrecha pierde en batería oculta. Debe hacer que comprar **y usar** las réplicas sea necesario, no un detalle incidental como ocurrió antes.

Dejaría optional stopping después: agrega temporalidad, sesgo condicionado a la parada y costo de oportunidad; es más novedoso, pero también más fácil de ganar con la regla trivial “siempre agotà el presupuesto” si no se diseña cuidadosamente. La carnada de significancia también puede degenerar en el checklist “mirá magnitud, no p-value”.

El pozo puede volver luego como presión sobre causal o rigor: un distractor atractivo que compite por el presupuesto. Ahí aporta más que como mundo aislado.

### 3. Lo que falta entre ambos

Antes de autorar la plantilla de rigor, correría un **micro-batch medio congelado de al menos N=5** —el piloto más cuatro encargos frescos— con seeds y estratos paramétricos predefinidos.

Eso es más importante que saltar inmediatamente a otro mundo porque el norte 0117 no es “lograr un caso”: es multiplicar. El batch permite observar:

- fracaso sistemático frente a accidente;
- threshold hugging;
- colapso de dominios/parámetros;
- modos de fallo del generador;
- primer indicio, todavía impreciso, de yield.

Después sí: auditoría y panel conductual sobre los aceptados, sin alterar el numerador mecánico. Si los cinco producen vectores conductuales casi iguales, tienen una plantilla repetible, no diversidad. Recién entonces construiría rigor. Sin ese intermedio, “fábrica core” seguiría apoyada en dos anécdotas `1/1`.
