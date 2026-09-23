# WAGER, definición de trabajo para el mes (PROPUESTA para el OK de Lucas — no decidida)

> Escrita a pedido de Lucas (2026-09-23): "explicame cómo definimos WAGER actualmente, para este mes:
> qué queremos lograr, cómo, qué asumimos, qué descartamos". Junta lo que quedó en pie después de tres
> voces (Codex, Claude, Astra ×2) y de las lecturas. Si Lucas da el OK, se convierte en ADR con su
> checklist de supersesión y en un prerregistro de dos páginas.

## 1. La definición, en una frase

**WAGER estudia cuándo un agente revisa la familia de modelos con la que arrancó, cuando la evidencia la
vuelve insuficiente — en juegos mínimos con verdad fabricada, puntaje sin LLM y controles
contrafácticos.**

En llano: medimos si el detective abandona su historia cuando las pistas la contradicen, qué le cuesta,
y qué lo ayuda — en juegos chiquitos donde todo lo demás está controlado.

Lo que la frase NO dice a propósito: "creatividad", "salto", "fundamentos", "primitivas". Son la pregunta
teórica de fondo; todavía no son capacidades que el instrumento certifique.

## 2. Qué queremos lograr en el mes (una sola cosa)

Demostrar, con un resultado que pueda equivocarnos, **que existe una "caja" que cambia la conducta del
agente** — que arrancar con una familia de modelos cuesta después revisarla — y medir ese costo en un
juego mínimo. Es la piedra sobre la que se apoya todo lo demás: antes de estudiar cómo se sale de la
caja, hay que probar que la caja está.

Entregable del mes: un instrumento calibrado + un experimento prerregistrado con su resultado (positivo,
negativo o inconcluso, los tres valen) + qué afirmaciones quedaron sin apoyo.

## 3. Cómo (el plan de Astra, que Claude suscribe)

| Semana | Qué | Cómo se sabe si salió bien |
|---|---|---|
| 1 | Construir el **juego binario de memoria** como instrumento de calibración, con sus referencias: mejor predictor sin memoria, solución legal con memoria, predictor sin datos, búsqueda enumerativa en la misma gramática, sustituto flexible permitido | Los ejemplos iniciales inducen una regla de trabajo; la evidencia crítica distingue los mundos; con una pista de dependencia temporal se resuelve; la interfaz no produce errores dominantes |
| 2 | **Experimento 2×2**: (regla inicial explícita + compromiso predictivo vs misma evidencia sin regla privilegiada) × (verdad con memoria vs gemelo sin); 12-16 instancias por celda; resultado primario = pérdida predictiva (Brier) con presupuesto fijo, separada por verdad | Prerregistro con umbral de efecto material (p. ej. 0.05 de Brier = 20% de la brecha), tope de gasto y criterios de abandono escritos ANTES |
| 3 | **Una sola bifurcación**: si aparece costo de revisión, pista de operación vs control activo en instancias reservadas; si la tarea está en techo, un segundo anfitrión de la misma operación | No se agregan mutaciones nuevas para "encontrar una que confirme" |
| 4 | **Transferencia chica** (dos operaciones × dos anfitriones, exposición por demostraciones en contexto) solo si hay dificultad reproducible y asistible; si no, **cierre honesto** | Se reporta la matriz completa, no un índice |

## 4. Qué asumimos (declarado, para poder equivocarnos)

1. Que un LLM con pesos congelados puede "tener una caja" **inducida por el episodio** (ejemplos iniciales
   compatibles con una regla simple + predicciones de compromiso). Es lo primero que se prueba; si no
   aparece, se abandona esa manipulación.
2. Que la revisión se mide por **conducta** (predicciones, programa entregado), nunca por creencia interna.
3. Que un juego binario mínimo **conserva el fenómeno**. Si está en techo para todos, aprendemos que esa
   operación no ofrece la dificultad buscada en esos agentes — y no se fabrica un impasse lingüístico.
4. Que la caja del certificado es **una familia declarada por nosotros**: solo afirmamos "revisó esa
   familia", nunca "salió de su repertorio". Lo no expresado se registra como no expresado.
5. Que "una edición" es **distancia en una gramática declarada**, no un átomo cognitivo.

## 5. Qué descartamos o dejamos en espera este mes

- Cambiar la **identidad** ("el ARC de la abducción creativa", "laboratorio de los fundamentos").
- Las otras **cuatro mutaciones** y la fábrica: quedan como boceto.
- La **sonda memoria/estructura**: no separa recuperación de construcción; si vuelve, vuelve como 2×2 de
  analogía (estructura × superficie).
- "**Transferencia diferencial = primitivas reales**" como claim; queda como matriz a comparar entre
  explicaciones rivales (plantilla, código, prior, operación).
- Reclamar **creatividad / P-creatividad**; se dice "expansión del modelo de trabajo observada en el
  episodio".
- **Perfiles** y el experimento del revisor ahí: en pausa (no cerrados).
- Casos **realistas** nuevos; hipótesis de independencia por tipo; el mito del aha como tesis.
- La frase "nadie lo midió en agentes" hasta auditar BoxingGym, DiscoveryWorld, ACRE, Automatic
  Statistician, DreamCoder.

## 6. El juego binario (lo que Astra propone construir primero)

Cada turno el mundo recibe un bit de entrada `u_t` (0 o 1) y devuelve un bit `y_t`.
- **Gemelo (la caja es correcta):** `y_t = u_t XOR b`, con `b` un bit secreto fijo por instancia. La salida
  depende solo de la entrada de ahora.
- **Mundo con memoria (la caja falla):** `y_t = u_t XOR u_{t-1} XOR b`. La salida depende también de la
  entrada anterior.
- **La caja de partida:** "la salida depende solo de la entrada actual". Se induce con ejemplos iniciales
  elegidos para ser compatibles con ella y se pide un compromiso predictivo.
- **Después:** evidencia nueva que en el mundo con memoria contradice la caja (y en el gemelo no); libertad
  explícita de revisar; entrega en un lenguaje chico con intérprete común.
- **Puntaje:** Brier sobre predicciones nuevas. Con historias equilibradas, el mejor predictor sin memoria
  queda en **0.25** en el mundo con memoria; la solución correcta, en **0**. Sin estadística, sin estimación,
  evaluable exhaustivamente. Si un LLM lo resuelve trivialmente, ese es el primer dato.

## 7. Qué NO cambia (las reglas duras siguen)

Reward cero-LLM · gemelos · mejor rival sin salto optimizado · idea nombrada como compuerta · reglas
congeladas antes de correr · ADRs append-only · nada se construye sin el GO de Lucas.
