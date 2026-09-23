# Boceto: un generador de mundos mínimos — UNA base y CINCO mutaciones (cada mutación = un salto = una primitiva)

> **Pedido de Lucas (2026-09-23):** "bajá esto a un boceto concreto: la base y las cinco mutaciones,
> escritas como programitas; sobre todo ahora que tenemos teoría sobre cuántas ediciones".
> Es un boceto para pensar, **no una ficha de experimento** (esa lleva reglas congeladas y GO). La idea
> viene de juntar tres cosas que ya teníamos: (1) "saltos = ediciones estructurales de un programa
> generativo" ([fundamentos 08-05](2026-08-05-fundamentos-taxonomia-de-saltos.md) §1); (2) el
> generador por mutaciones de NewtonBench (leído completo el 22-09), pero aplicado a *programas* y no
> a fórmulas; (3) la escalera de dificultad por *alcance* de la edición (Knoblich et al. 1999).

## 1. La base: "una población medida con ruido"

Es el programa que el agente va a **suponer** sin que nadie se lo diga (su caja de partida). Cada
mundo se genera con una semilla fresca; el agente nunca ve este código.

```
para cada unidad i = 1..N:
    x_i  ~ Normal(mu, sigma)             # el valor verdadero de la unidad (nunca observado)
    para cada medición k = 1..K:
        y_ik = x_i + Normal(0, tau)      # lo que el agente puede comprar
```

- **Acciones del agente**: comprar mediciones (unidad, repetición) con costo; correr código sobre lo
  comprado; registrar su modelo de trabajo; entregar un programa que prediga.
- **Entrega**: un programa ejecutable que predice mediciones nuevas de unidades vistas y de unidades
  nuevas (y, cuando aplique, bajo una intervención).
- **Examen** (mecánico, cero LLM): log-score sobre unidades no vistas + una perilla movida.
- **La caja de partida certificada**: la mejor versión de ESTE programa, con mu, sigma, tau óptimos.
  Es el "mejor rival sin salto" (ADR 0175). Todo lo que sigue se mide contra él.

## 2. Las cinco mutaciones (una sola edición cada una)

| # | Salto de la lista | La edición al programa | Qué símbolo nuevo aparece |
|---|---|---|---|
| M1 | **Partir en dos tipos** (grupos escondidos) | `t_i ~ Bernoulli(p)` y `x_i ~ Normal(mu[t_i], sigma[t_i])` | una variable discreta latente por unidad |
| M2 | **Agregar una variable escondida** (entidad oculta) | `z_b ~ Normal(0,1)` por lote/día; `x_i = Normal(mu, sigma) + beta * z_{lote(i)}` | una causa común no medida |
| M3 | **Régimen** (dos leyes con umbral) | `y_ik = x_i + ruido` si `x_i < theta`, si no `g(x_i) + ruido` | un umbral y una segunda función |
| M4 | **Memoria** (el sistema arrastra su pasado) | `x_{i,k} = rho * x_{i,k-1} + (1-rho) * mu + ruido` | una dependencia temporal |
| M5 | **El aparato** (proceso del observador) | `y_ik = min(x_i, tope) + ruido` (saturación) o `y_ik` solo se ve si supera un umbral (selección) | una distorsión entre el mundo y el dato |

Cada mutación deja **todo lo demás idéntico**: mismas unidades, mismas semillas de ruido, mismos
costos. Por eso base vs base+M es un **gemelo** gratis, y M1 vs M2 comparten hasta el ruido.

## 3. La escalera de dificultad (Knoblich, traducida a programas)

Knoblich et al. (1999) predijeron la dificultad de un insight ANTES de correr el experimento a
partir del **alcance** de la restricción que hay que soltar (un valor < un operador < la forma
entera; 95 / 78 / 45% resueltos), y verificaron que el orden nunca se violó. La misma idea, para
ediciones de programas:

| Nivel | Qué tocás | Ejemplo | ¿Es salto? |
|---|---|---|---|
| 0 | un **número** | cambiar mu | no: es refinar |
| 1 | una **función** | la forma del ruido; `y = f(x)` (M3, M5) | sí, chico |
| 2 | un **símbolo nuevo** (variable, tipo, estado) | M1, M2, M4 | sí, el central |
| 3 | el **cableado** (qué depende de qué; un bucle) | realimentación | sí, grande |

Predicción a registrar antes de correr: **nivel 1 > nivel 2 > nivel 3 en tasa de acierto**, y
dentro del nivel 2, M4 (memoria) más fácil que M1 (tipos) porque el símbolo nuevo tiene menos
grados de libertad. Si el orden se viola, la escalera está mal (eso también es un resultado).

**Cuántas ediciones** (la perilla de NewtonBench): 1 edición = primitiva aislada; 2 ediciones
(p. ej. M1 + M5: dos tipos medidos con un aparato que satura) = compuesta, predicha más difícil que
cualquiera de las dos solas. Fácil / medio / difícil = 1 / 2 / 3 ediciones.

**La firma de Knoblich que nadie probó en agentes**: *transferencia diferencial*. Una vez que
relajaste una restricción, queda relajada: un agente que resolvió M1 en una semilla debería resolver
M1 más rápido en la siguiente, y **no** mejorar en M2. Si la mejora transfiere solo dentro del mismo
tipo de edición, la primitiva es real (Astra: la transferencia selectiva es la evidencia fuerte de
separabilidad, no darles nombre).

## 4. Los controles, por mutación (la ley de dos controles + lo que agregaron Astra y Kaplan & Simon)

Para cada M:
1. **Sin truco te va mal**: la base óptima saca mala nota en el examen de M (headroom material).
2. **Con la idea nombrada te va bien**: "las unidades pueden ser de dos tipos" (no la solución) →
   un agente lo resuelve. Si ni así, el mundo está mal, no el agente.
3. **Gemelo negativo**: la base sin mutación, mismo brief. Castiga al que siempre inventa dos tipos.
4. **Control activo** (Astra): una ayuda de igual esfuerzo/atención que no apunte a la estructura.
5. **Saliencia** (Kaplan & Simon): la misma información mostrada de forma que la agrupación se vea
   (p. ej. filas ordenadas por unidad) sin decir nada. Mide si el problema es *ver* o *usar*.
6. **Menú previo** (Klahr & Dunbar est. 2; Boden): antes de comprar, "listá todas las formas que se te
   ocurren". Es la caja efectiva del agente para este episodio; decide "selectivo vs creativo".

## 5. Qué mediría cada cosa (observables mecánicos, sin rúbrica)

- **¿Salió de la caja?** El programa entregado, ¿tiene el símbolo nuevo (un tipo, una variable, un
  umbral, un rezago, un tope)? Se lee del código, no de la prosa.
- **¿Le pagó?** Log-score fuera de muestra vs la base óptima (la brecha certificada).
- **¿Construyó y descartó?** Detector NazoNazo: ¿algún bloque de código ajustó el símbolo nuevo y la
  entrega no lo tiene?
- **¿Contrastó?** I:C (Failing to Falsify): cada compra, ¿era compatible o incompatible con el modelo
  de trabajo enunciado? Si nunca enunció un modelo, "I:C indefinido" es el dato.
- **¿Estaba en su lista previa?** Selectivo (estaba) vs creativo-en-el-episodio (no estaba y apareció).

## 6. Lo que NO resuelve este boceto (honesto)

- Que el molde ("dos tipos", "una variable escondida") es de los más comunes de la estadística: el
  lado 1 (verdad fresca) tapa el recuerdo del resultado, no del molde. Para eso, mutaciones menos
  canónicas (M5 con formas raras de distorsión) y medir cómo cambia el acierto con la rareza del molde.
- Que "forma vs números" es relativo a la familia: si el agente trae mixturas por defecto, M1 es
  refinar para él. Por eso el menú previo y la caja declarada en el certificado.
- Que la validez ecológica baja: son mundos de juguete. Es el trade-off que Lucas eligió ("ya no
  queremos casos ultra realistas").
- Que cada mutación necesita su propio examen donde la base *pierda por mucho*: M4 (memoria) y M5
  (saturación) pueden ser casi invisibles con pocas mediciones. Headroom primero, siempre.
