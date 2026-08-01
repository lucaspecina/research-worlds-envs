# Contrato corto — `overgen` longitudinal v0

> **Estado:** contrato de construcción exploratoria; no es pre-registro del estudio principal.  
> **Deriva de:** `overgen_v0` / `overgen_twin_v0`; no es una familia conceptual nueva.  
> **Regla:** construir lo mínimo, usar agentes reales temprano y volver un nivel arriba.

## 1. Pregunta exacta

> Un agente aprende una explicación que funciona en el dominio inicialmente observado. Cuando
> el trabajo se amplía y llegan datos rutinarios de otros dominios, ¿calibra correctamente el
> alcance de esa explicación —corrigiéndola donde deja de transferir y conservándola donde sí—
> en su modelo de trabajo y en la entrega final?

Este slice mide **sobre-generalización y revisión intermedia**. No pretende medir todavía
KellyBench, Corral puro, trayectoria muy larga ni fricción de dependencias.

## 2. La situación que vive el agente

El agente asesora la puesta en marcha gradual de cinco líneas relacionadas. Debe mantener un
pronóstico probabilístico ejecutable para todas y entregar su versión final cuando termina la
puesta en marcha.

### Prefijo común

- La línea 1 ya opera en todo el rango y ofrece un historial rico.
- Las líneas 2–5 solo están habilitadas inicialmente en el rango bajo.
- En esa región, los cinco mecanismos y todos los datos visibles son **idénticos entre polos**
  y compatibles con una ley compartida.
- Antes de la ampliación no se permite consultar ni experimentar en la región aún no puesta en
  marcha. Por eso cualquier acción legal produce el mismo prefijo en ambos mundos.

### Llegada ordinaria de nueva información

La puesta en marcha sigue un calendario conocido. Al habilitarse el rango restante, el sistema
entrega el reporte normal de comisionamiento de las líneas 2–5. El reporte:

- usa el mismo canal y formato que los reportes rutinarios anteriores;
- mezcla puntos de control ya conocidos con puntos del rango nuevo;
- no contiene las palabras “evidencia”, “anomalía”, “refutación”, “pivotear” ni una pregunta
  sobre si el agente quiere cambiar;
- llega automáticamente: en v0 se mide incorporación, no si recordó abrir una fuente;
- habilita después campañas normales en todo el rango, de modo que el agente puede verificar
  lo que considere necesario.

El momento exacto se expresa como una **etapa operativa**, no como una tesis sobre “12–16
rondas”. La cantidad de turnos se ajustará solo para que un agente pueda trabajar sin apuro y
se reportará como horizonte corto de instrumentación.

## 3. Los dos polos

| Polo | Verdad oculta | Respuesta correcta |
|---|---|---|
| **Transferencia** | La ley aprendida continúa funcionando en todas las líneas, admitiendo offsets menores | Conservar la estructura compartida y actualizar solo lo que los datos justifican |
| **Alcance limitado** | Algunas líneas se apartan sistemáticamente en el rango nuevo; al menos una conserva la ley | Separar/corregir únicamente las líneas afectadas; no fragmentar todas por reflejo |

Los polos comparten byte por byte el brief, el prefijo de datos, costos, interfaces, calendario
y ruido aleatorio previo a la ampliación. La diferencia comienza únicamente en los valores del
reporte del rango nuevo y en la verdad que luego se puntúa.

No se agrega todavía un tercer polo de “dudar más”: primero se demuestra que el instrumento
separa cambio y conservación. La incertidumbre se observa, pero no se construye otro escenario
hasta pasar el gate.

## 4. Cómo se fotografía el modelo sin señalar el dato

La creencia operacional sigue siendo el mismo objeto que la entrega:
`model(regime, n, seed) -> DataFrame[outcome]`.

Durante todo el episodio el agente mantiene ese programa en una variable estándar
`working_model`. Después de cada celda, el harness guarda silenciosamente su valor si existe:

- no hay verbo `REGISTER` que el agente deba recordar;
- no se devuelve score, diagnóstico ni confirmación;
- el mecanismo funciona igual antes y después del reporte;
- una versión ausente o inválida se registra como tal y no se descarta;
- la entrega final continúa siendo `env.submit(working_model)` o un programa equivalente.

Así obtenemos una secuencia `M1…Mt`, no un ritual especial alrededor de la nueva información.
En el probe posterior habrá un brazo pequeño sin archivo rutinario para medir cuánto altera la
conducta esta obligación; no hace falta construirlo antes del smoke técnico.

## 5. Evidencia controlada y búsqueda propia

El reporte automático garantiza un mínimo común y permite preguntar si el agente lo incorpora.
Las campañas posteriores siguen siendo elegidas por él y permiten observar si busca
confirmación o falsación adicional.

Se analizan por separado:

1. **asimilación condicional al reporte común**;
2. **búsqueda posterior elegida por el agente**;
3. **persistencia hasta la entrega**.

No se interpretará “no compró la campaña ideal” como “ignoró evidencia que nunca recibió”.

## 6. Medición

Cada modelo válido guardado se puntúa en privado sobre:

- la región inicial, donde no debería destruir lo ya aprendido;
- la región nueva, donde los polos se separan;
- cada línea por separado;
- distribución completa: centro, dispersión y colas.

Resultados principales del slice:

- dirección y magnitud del cambio de `M_pre` al primer modelo posterior y al modelo final;
- mejora o daño de proper score en la región diagnóstica;
- calibración bilateral: corregir en *alcance limitado* sin fragmentar en *transferencia*;
- heterogeneidad por línea: cambiar solo donde corresponde;
- reversión: corregir y luego volver al modelo inicial;
- validez y actualización efectiva de `working_model`;
- campañas elegidas y momento de compra.

Una receta de actualización de referencia, congelada y alimentada solo con datos legales,
normaliza cuánto de la mejora alcanzable capturó el agente. En v0 se la llamará
**actualizador de referencia**, no “posterior racional único”. El proper score contra verdad y
el contraste entre gemelos no dependen de ese lenguaje. Si más adelante se quiere un claim
bayesiano normativo, deberá declararse una familia/prior o demostrarse robustez entre varias
recetas antes del estudio principal.

## 7. Certificaciones antes de llamar un agente

La instancia no puede correr si no pasan todos estos checks:

1. cualquier observación o experimento legal del prefijo es idéntico entre polos;
2. el reporte nuevo tiene fuerza diagnóstica mínima predefinida sin ser un cartel obvio;
3. un actualizador legal mejora claramente sobre **nunca cambiar** en el polo limitado;
4. **fragmentar siempre** pierde claramente en transferencia;
5. **cambiar todas las líneas** pierde frente a corregir solo las afectadas;
6. el modelo verdad corre y los hacks triviales permanecen bajos;
7. cada línea y la región nueva tienen peso suficiente en el score;
8. el archivo automático recupera programas válidos sin exponer verdad ni feedback;
9. los datos del reporte y las campañas usan únicamente información disponible al agente.

La certificación roja actual de `overgen_v0` obliga a ajustar curvas, datos y anclas antes de
cualquier interpretación conductual. No se relajan umbrales después de ver agentes.

## 8. Orden de construcción y prueba

1. Derivar `overgen_stream_v0` y `overgen_stream_twin_v0`, preservando los casos históricos.
2. Construir prefijo idéntico, reporte rutinario y restricciones de comisionamiento.
3. Agregar captura automática opcional de `working_model` al runner común.
4. Crear actualizador de referencia, robots reflejos y certificación completa.
5. Correr el camino técnico scripted.
6. Correr **un episodio real barato por polo** para UX y comprensión.
7. Si es interpretable, correr **un episodio SOTA por polo**.
8. Recién entonces congelar una ficha de probe apareado con semillas quemadas y techo de gasto.

## 9. Criterios de decisión después del smoke real

**Mantener** si el agente entiende la tarea, conserva modelos válidos, el reporte parece parte
normal del trabajo y los dos polos ofrecen decisiones medibles.

**Modificar** si el problema es UX, timing, fuerza de evidencia o geometría de score y puede
corregirse sin cambiar el fenómeno.

**Pivotear/abandonar este slice** si necesita avisar que llegó una corrección, si
`working_model` domina la conducta, si no puede distinguir actualización de incapacidad de
programación o si los gemelos solo separan por pistas superficiales.

## Gate al cerrar selección

- **Pregunta:** sigue siendo valiosa y este slice responde una parte necesaria, no todo.
- **Fidelidad:** mejora claramente sobre la nota y el probe explícitos; la ampliación de una
  puesta en marcha es una fuente natural de información nueva.
- **Constructo:** los riesgos principales quedan visibles: archivo rutinario, código y
  adquisición versus asimilación.
- **Alcance:** el claim queda limitado a generalización local→amplia en horizonte corto.
- **Decisión:** **MANTENER la dirección y pasar a slice mínimo**, con gate obligatorio después
  del primer agente real.
