> Nota de dirección (2026-07-31), guardada VERBATIM por pedido de Lucas — redactada en otra
> sesión (con Codex) y adoptada como presentación del objetivo del proyecto. Complementa los
> ADRs 0153/0154/0155; ante conflicto de detalle experimental, mandan los pre-registros.

# WAGER: mapa causal de la revisión de creencias bajo carga

## Resumen ejecutivo

Este trabajo busca responder una pregunta concreta:

> **¿Bajo qué condiciones un agente actualiza correctamente sus creencias según la evidencia, medido por el modelo que finalmente entrega y no solamente por lo que declara?**

Actualizar correctamente no significa cambiar siempre. A veces la evidencia realmente refuta el modelo anterior y el agente debería pivotear. A veces parece relevante, pero no distingue entre hipótesis, y debería mantenerse firme. En otros casos aporta información parcial y justifica una revisión moderada, no un cambio completo.

El objetivo es construir un **mapa causal de la revisión aplicada**: medir cómo la claridad de la evidencia, la dependencia de la trayectoria previa y la dificultad de reabrir el trabajo afectan la capacidad del agente de decidir cuándo cambiar, cuándo mantenerse y cuánto cambiar.

La creencia no se infiere únicamente de la prosa del modelo. Se operacionaliza mediante un **modelo predictivo ejecutable**, registrado antes y después de recibir nueva evidencia, y puntuado matemáticamente contra la verdad oculta de un mundo sintético. Esto permite distinguir entre lo que el agente dice haber aprendido, las acciones que toma y lo que efectivamente incorpora en su entrega.

---

## 1. Pregunta de investigación

La pregunta principal es:

> **¿Cómo cambia la sensibilidad de los agentes a la evidencia cuando aumenta la "carga" asociada a revisar un modelo previo?**

Por carga entendemos una combinación de:

- dificultad para identificar la señal relevante;
- dependencia de una trayectoria de trabajo previa;
- compromiso acumulado con el modelo existente;
- costo práctico o estructural de corregirlo.

No buscamos demostrar simplemente que los modelos son tercos o influenciables. Buscamos medir si el cambio realizado es **proporcional al valor probatorio de la evidencia**.

Esto incluye tres respuestas normativamente correctas:

| Lo que justifica la evidencia | Respuesta correcta |
|---|---|
| Refuta suficientemente el modelo previo | Revisar o pivotear |
| No discrimina o es compatible con el modelo | Mantenerse |
| Modifica parcialmente el balance entre hipótesis | Revisar parcialmente |

Y, por lo tanto, distintos modos de falla:

| Falla | Descripción |
|---|---|
| Rigidez | Debería cambiar, pero mantiene el modelo |
| Influenciabilidad | No debería cambiar, pero abandona el modelo |
| Subactualización | Cambia en la dirección correcta, pero demasiado poco |
| Sobreactualización | Reacciona más de lo justificado |
| Actualización errónea | Cambia en una dirección que la evidencia no respalda |

Esta simetría es esencial. Un benchmark que premiara solamente pivotear podría enseñar el reflejo "cambiá ante cualquier anomalía"; uno que premiara resistir podría enseñar paranoia frente a toda corrección. El objeto real es la **discriminación calibrada**.

---

## 2. Hipótesis conceptual

La hipótesis general es que la revisión aplicada puede entenderse mediante tres factores principales:

| Factor | Pregunta | Ejemplos de manipulación |
|---|---|---|
| **Señal de la evidencia** | ¿Qué tan fácil es identificar la información que discrimina? | Evidencia limpia, misma evidencia mezclada con relleno, información no diagnóstica |
| **Dependencia de trayectoria** | ¿Cuánto está condicionado el agente por el trabajo anterior? | Modelo heredado, atribuido como propio, construido y registrado durante la trayectoria |
| **Fricción de revisión** | ¿Cuánto trabajo exige actuar sobre la corrección? | Cambiar un parámetro, separar una parte del modelo, reconstruirlo y revisar dependencias |

La expectativa no es necesariamente que cada factor produzca un efecto independiente. Las interacciones pueden ser más importantes.

Por ejemplo:

- La trayectoria propia podría no importar cuando la evidencia es limpia.
- Podría aparecer rigidez solamente cuando la evidencia es ambigua y la corrección es costosa.
- La fricción podría afectar la entrega aunque el agente reconozca verbalmente la evidencia.
- Una trayectoria previa podría proteger contra señales engañosas, pero también dificultar revisiones legítimas.

El momento de llegada —formación, mitad o cierre— también se estudia, pero no se presupone que sea el mecanismo fundamental. Su efecto puede deberse a que, con el tiempo, aumentan el trabajo acumulado, las dependencias y el costo de reabrir.

---

## 3. Qué significa "creencia" en este estudio

No se afirma que un LLM posea creencias en un sentido psicológico fuerte.

En este trabajo, una creencia se define operacionalmente como:

> **El modelo predictivo que el agente utiliza para anticipar el comportamiento del mundo y sobre el cual basa sus decisiones.**

Antes de recibir nueva evidencia, el agente registra un modelo provisional `M0`. Después entrega un modelo `M1`.

La revisión se mide comparando:

- las predicciones de `M0`;
- las predicciones de `M1`;
- la verdad oculta del mundo;
- la actualización que habría sido legalmente alcanzable con la información disponible.

Esto permite hablar con mayor precisión de **revisión del modelo**, **incorporación de evidencia** o **revisión conductual**, evitando depender de interpretaciones antropomórficas de la prosa.

---

## 4. Diseño experimental

Los experimentos ocurren en mundos sintéticos ejecutables con una verdad oculta. El agente investiga el mundo, compra datos o experimentos con un presupuesto y construye un modelo predictivo.

El diseño básico tiene cinco etapas:

1. El agente investiga y construye un modelo provisional.
2. Ese modelo queda registrado y puede puntuarse.
3. Se alcanza un checkpoint donde ya existe algo que revisar.
4. Se introduce evidencia nueva bajo una condición experimental.
5. El agente continúa y entrega su modelo final.

Mediante **forks apareados**, distintas continuaciones parten del mismo estado previo. Entre brazos se modifica una sola condición: por ejemplo, si la evidencia llega limpia o mezclada, si el modelo se presenta como propio o heredado, o si corregirlo tiene consecuencias sobre trabajo ya registrado.

Esto reduce el ruido producido por historias de investigación diferentes: la comparación relevante ocurre entre agentes que parten del mismo modelo, datos y presupuesto.

### Ejemplo conceptual

El agente concluye que cuatro líneas de producción comparten una misma curva.

Se construyen mundos gemelos:

| Mundo | Verdad | Respuesta correcta |
|---|---|---|
| A | Una línea realmente utiliza otra curva | Separarla |
| B | Todas comparten la curva; la diferencia observada es ruido | Mantener el modelo común |
| C | Hay una diferencia moderada, pero la evidencia es limitada | Reducir el pooling o representar incertidumbre |

Desde afuera, los tres mundos deben parecer suficientemente similares. La estrategia "separá siempre" pierde en B; "agrupá siempre" pierde en A; solamente investigar cuánto discrimina la evidencia permite resolverlos correctamente.

---

## 5. Manipulación de la evidencia

La evidencia debe caracterizarse antes de observar la respuesta del agente.

Las condiciones principales son:

| Condición | Contenido |
|---|---|
| **Limpia** | Información diagnóstica presentada de manera directa |
| **Mezclada** | La misma información diagnóstica, acompañada por relleno o datos secundarios |
| **Parcial** | Evidencia real pero insuficiente para decidir completamente |
| **No diagnóstica** | Información saliente que no cambia el balance entre hipótesis |
| **Confirmatoria** | Evidencia que respalda correctamente el modelo previo |

Para aislar el efecto de la mezcla, CLEAN y MIXED deben contener la **misma evidencia diagnóstica**. MIXED agrega relleno; no debe simplemente recibir menos información útil. De lo contrario, no se puede distinguir entre pérdida de señal e interferencia contextual.

La información de cada bundle se cuantifica server-side, por ejemplo mediante KL o likelihood ratios esperados. Esto permite describir la dosis probatoria independientemente de cuánto persuada al modelo.

---

## 6. Cómo se mide la actualización

La métrica primaria compara el cambio del modelo sobre la región del mundo a la que se refiere la evidencia.

Sea:

- `S0`: score del modelo previo;
- `S1`: score del modelo final;
- `S*`: score de un oráculo legal que utiliza únicamente el modelo previo y la evidencia recibida.

Se define la fracción de mejora capturada:

F = (S1 − S0) / (S* − S0)

Interpretación aproximada:

| Valor | Interpretación |
|---|---|
| `F ≈ 1` | Capturó prácticamente toda la mejora disponible |
| `F ≈ 0` | La evidencia no produjo mejora aplicada |
| `F < 0` | El modelo final empeoró |
| `0 < F < 1` | Incorporación parcial |
| `F > 1` | Superó al oráculo de referencia |

`F` no pretende ser una medida directa de una posterior interna. Es una medida conductual de cuánto de la mejora legalmente disponible apareció en el artefacto entregado.

Además se observan tres canales:

| Canal | Pregunta |
|---|---|
| **Declara** | ¿Qué dice el agente que aprendió o debería cambiar? |
| **Compra** | ¿Qué evidencia decide verificar o adquirir? |
| **Entrega** | ¿Qué modifica realmente en el modelo final? |

La brecha entre estos canales es una parte central del objeto. Un agente puede escribir que la evidencia refuta su hipótesis, comprar el chequeo correcto y aun así entregar un modelo prácticamente idéntico.

El reward primario se calcula matemáticamente contra la verdad oculta, sin utilizar otro LLM como juez.

---

## 7. Posicionamiento científico

La literatura actual cubre distintos extremos del problema:

- Estudios controlados de pocos turnos muestran sesgos de compromiso y sobreponderación de consejos contradictorios, pero sin trabajo acumulado ni consecuencias sobre una entrega. [Kumaran et al.](https://arxiv.org/abs/2507.03120)
- Belief-R y Bayesian Teaching miden revisión frente a evidencia con tareas donde existe una actualización normativa conocida. [Belief-R](https://aclanthology.org/2024.emnlp-main.586/), [Bayesian Teaching](https://arxiv.org/abs/2503.17523)
- Corral encuentra evidencia ignorada y poca revisión refutacional en agentes científicos reales, pero principalmente mediante análisis observacional de trayectorias. [Corral](https://arxiv.org/abs/2604.18805)
- KellyBench muestra adaptación fallida en tareas extensas y no estacionarias, sin aislar causalmente qué componente de la trayectoria genera la falla. [KellyBench](https://arxiv.org/abs/2604.27865)
- BoxingGym y DiscoverPhysics ya utilizan mundos generativos, experimentación y evaluación predictiva. La existencia de mundos ocultos o modelos ejecutables no constituye por sí sola la novedad. [BoxingGym](https://arxiv.org/abs/2501.01540), [DiscoverPhysics](https://arxiv.org/abs/2605.26087)

La contribución buscada por WAGER es conectar ambos extremos:

> **Una medición causal y apareada de la revisión de modelos en agentes con trayectoria, evidencia cuantificada y consecuencias verificables sobre la entrega.**

---

## 8. Qué constituiría un resultado importante

El objetivo no es llenar todas las combinaciones posibles. El mapa es un instrumento para buscar una regularidad compacta.

Un resultado fuerte sería demostrar, entre diferentes modelos y familias de mundos, algo como:

> La incorporación de evidencia se mantiene ante refutaciones limpias, pero cae cuando se combinan baja señal, dependencia de trayectoria y alta fricción de revisión.

También sería importante encontrar que:

- solo importa la señal y no existe un efecto especial de autoría;
- la trayectoria afecta la entrega, pero no la declaración;
- la carga produce rigidez frente a evidencia legítima e influenciabilidad frente a señales aparentes;
- distintos modelos poseen perfiles de revisión cualitativamente diferentes;
- la zona intermedia —evidencia genuina pero no concluyente— revela fallas que los extremos no muestran.

Esta última zona puede ser especialmente informativa. Con evidencia aplastante, actualizar es fácil; con cero evidencia, mantenerse también puede ser fácil. El juicio aparece cuando hay que decidir cuánto peso merece una señal incompleta.

---

## 9. Alcance y criterio anti-rabbit hole

Los ejes son candidatos, no una ontología definitiva. El proyecto no debe agregar una nueva dimensión cada vez que dos resultados difieran.

La estrategia es:

1. probar pocas celdas altamente informativas;
2. replicar en otra familia de mundos;
3. comparar varios modelos;
4. buscar si señal, trayectoria y fricción explican los resultados;
5. abandonar o reducir la teoría si cada mundo exige una explicación distinta.

El enfoque pierde interés si los efectos:

- aparecen solamente con un wording;
- no replican entre mundos;
- se explican por longitud de contexto o dificultad de escribir código;
- requieren una taxonomía cada vez más grande;
- no distinguen revisión epistémica de simples fallas operativas.

El resultado buscado no es una enciclopedia de fallas, sino una teoría pequeña y comprobable sobre la revisión aplicada.

---

## Síntesis final

WAGER estudia si los agentes ajustan sus modelos proporcionalmente a la evidencia cuando ya existe una trayectoria de trabajo comprometida.

La pregunta incluye tres capacidades:

> **Saber cuándo pivotear, cuándo mantenerse y cuánto cambiar.**

Estas capacidades se estudian bajo variaciones controladas de:

> **señal de la evidencia, dependencia de trayectoria y fricción de revisión.**

La conducta se mide en tres niveles:

> **lo que el agente declara, la evidencia que busca y el modelo que entrega.**

La meta científica es encontrar una regularidad causal, reproducible entre modelos y mundos, que explique por qué agentes capaces de reconocer evidencia pueden no incorporarla correctamente cuando la revisión ocurre dentro de un flujo de trabajo con consecuencias.
