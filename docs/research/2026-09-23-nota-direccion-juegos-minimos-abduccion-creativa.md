# Nota de dirección (NO DECIDIDA): reducir WAGER a juegos mínimos que aíslen la abducción creativa

> **Estado:** idea en discusión, escrita a pedido de Lucas (2026-09-23) para que la revise GPT Astra
> y después él decida. No cambia ningún ADR, ningún mundo ni ninguna regla. Si se adopta, llevará su
> ADR propio con checklist de supersesión.

## 1. La propuesta, en las palabras de Lucas

Benchmarks de descubrimiento hay un montón: un mundo con datos e interacción donde hay que descubrir
(y a veces arreglar) algo que no está claro al principio. Los de ingeniería de software son eso también.
Son juegos con la misma estructura. **Lo que queremos es reducir a lo mínimo indispensable para probar
UN componente de todo ese proceso: la abducción creativa / la creatividad**, con casos básicos de
juguete donde esa capacidad se aísle lo mejor posible, siguiendo la filosofía de ARC-AGI (simplificar y
probar los casos más simples, en vez de mezclar muchas cosas en entornos amplios). Ya no queremos
construir casos ultra realistas de investigación: queremos ir a lo más profundo y preguntar qué es
realmente descubrir / inventar / dar un salto, qué es en lo más primitivo, si se puede aislar, de qué
depende, y si existe o es un mito y resulta ser todo memoria asociativa.

## 2. De dónde sale (el hilo de las últimas tres semanas)

1. La re-anotación de Perfiles: la cadena no se corta en la "chispa" sino antes (no dejan que la
   anomalía moleste) y después (no testean; construyen el candidato y lo descartan).
2. Codex (review, MODIFICAR): retirar "medimos el salto creativo" y "ya localizamos el cuello" hasta
   tener evidencia causal; la taxonomía como variable medida.
3. Lucas: "¿el aha es un mito? ¿el salto importa? ¿cuáles son las primitivas del descubrimiento?"
4. Astra (segunda opinión): mantener WAGER pero definir el producto como *medir cuándo un agente usa
   evidencia para mejorar un modelo ejecutable*; cinco "capacidades locales" en micromundos con
   controles; congelar un mes la expansión conceptual.
5. Las definiciones lado a lado: lo nuestro es la capa del medio — descubrimientos que exigen cambiar
   la FORMA del modelo = abducción creativa (Magnani) = creatividad transformacional (Boden) = "jump".
6. Las lecturas a texto completo: Knoblich (dificultad predicha por alcance), Kaplan & Simon
   (saliencia; notar ≠ perseguir), Klahr & Dunbar (enumerar antes; el poder de un test depende del
   espacio de hipótesis), NewtonBench (un generador por mutaciones).
7. El boceto: una base y cinco mutaciones al programa generador; cada mutación = un salto = una
   primitiva. [Boceto](2026-09-23-boceto-generador-una-base-cinco-mutaciones.md).

## 3. Qué cambiaría (si se adopta)

- **La identidad**: de "banco de mundos realistas de investigación" a **"laboratorio de juegos mínimos
  para una capacidad: salir de la caja"**. El "ARC de la abducción creativa", con una diferencia
  esencial respecto de ARC: ARC aísla captar una regla con pocos ejemplos; nosotros aislamos
  *abandonar una familia de explicaciones que falla* — para eso el juego necesita una **caja de partida**
  que el agente trae y que falla a la vista. Sin caja no hay abducción, hay inducción.
- **La unidad de trabajo**: de "un mundo a mano por salto" a **"una base + una mutación"**. Gemelos
  gratis; certificación por tipo de mutación; cien instancias frescas por semilla.
- **El blanco**: la abducción creativa en sentido de Magnani (fabricar lo que no estaba en el
  repertorio), medida solo como **P-creatividad relativa al episodio** (Boden; Astra).
- **Dos niveles, ambos chicos**: (a) la primitiva sola — con la sorpresa servida y los tests listos, ¿aparece
  un candidato fuera de la caja con predicciones distintas?; (b) el flujo en miniatura — sin nada
  servido. La distancia entre (a) y (b) es el dato, no un defecto.

## 4. Qué NO cambia

Reward cero-LLM; gemelos; la ley de dos controles (mejor rival sin salto optimizado; idea nombrada
como compuerta); reglas congeladas antes de correr; ADRs append-only; la operativa Codex/Claude
(Astra como tercera voz externa); nada se construye sin el GO de Lucas.

## 5. Anatomía del caso mínimo (cinco piezas)

1. **Caja de partida**: la familia que el agente va a suponer (se la das, se la inducís, o la elicitás).
2. **Verdad a UN paso fuera de la caja**: una sola edición de forma la alcanza. Ese paso es la primitiva.
3. **Sorpresa visible y que duela**: la caja falla en algo que el agente puede comprobar por sí mismo.
4. **Examen donde la caja óptima pierde por mucho**: fuera de muestra o bajo intervención.
5. **Gemelo donde la verdad está en la caja**: castiga al que salta siempre.
Más: control activo de igual esfuerzo (Astra), saliencia (Kaplan & Simon), menú previo (Klahr & Dunbar).

## 6. El problema de la caja en un LLM, y cómo rodearlo (tres lados; el tercero es propuesta nuestra)

1. Verdad fabricada (no existe en ningún libro) — tapa el recuerdo del resultado, no del molde.
2. Vaciar la caja antes de ver datos ("listá todas las formas posibles") — la caja efectiva del episodio.
3. Dos pistas como sonda: "¿te recuerda a algo conocido?" (memoria) vs "mirá qué cambia entre filas"
   (estructura). Si solo la primera destraba, es memoria. **Esta sonda no está en la literatura leída.**

## 7. La prueba que decide si las primitivas son reales (Knoblich, 1999)

Knoblich predijo la dificultad de cada insight por el alcance de la restricción a soltar y verificó
además la **transferencia diferencial**: soltar una restricción en un problema hace fáciles los
problemas que exigen soltar *esa misma* restricción, y no otros. Traducido: un agente que resolvió
"partir en dos tipos" en una semilla debería resolver "partir" más rápido en la siguiente y **no**
mejorar en "memoria". Si la mejora transfiere solo dentro del mismo tipo de edición, la primitiva es
real; si transfiere a todo (o a nada), son nombres. Es el resultado que convierte los juguetes en
ciencia, y nadie lo midió en agentes.

## 8. Objeciones que ya conocemos (para no olvidarlas)

- Un juego mínimo con la respuesta mal recordada mide "abandonar la respuesta recordada", no
  necesariamente creatividad (Astra Q4: los dos controles prueban una dificultad asistible).
- El molde ("dos tipos") es de los más comunes de la estadística: el lado 1 no lo tapa.
- Cinco juegos no demuestran cinco módulos (Astra): solo la transferencia selectiva lo haría.
- "Forma vs números" es relativo a la familia: definir la caja en el certificado y elicitarla.
- Validez ecológica: baja por diseño; es el trade-off elegido.
- Cero-LLM no es cero-Goodhart (Astra): batería estrecha, fugas, normalización.

## 9. Qué resultado mataría esta dirección

- La caja óptima empata al modelo verdadero en todas las mutaciones (no hay headroom en los juguetes).
- Con la idea nombrada nadie resuelve ninguna mutación (los juegos son irresolubles, no difíciles).
- Solo la pista de memoria destraba, en todas las mutaciones y modelos (es memoria; publicable igual).
- No hay transferencia diferencial: la mejora es general o nula (las "primitivas" no separan nada).

## 10. Qué se le pide a Astra

Revisión crítica de §3, §5, §6 y §7; comparación con ARC, NazoNazo, BoxingGym, DiscoveryWorld y
"Knoblich para LLMs" si existe; y su plan de 2-4 semanas bajo este reencuadre (¿cambia lo que propuso
el 23-09?). Después decide Lucas.

---

## Addendum (mismo día, tras la review de Astra — [respuesta completa](2026-09-23-segunda-opinion-gpt-astra-b-nota-direccion.md))

Astra **adoptaría la reducción a juegos mínimos como programa de un mes**, pero no la identidad "ARC de
la abducción creativa" ni "cinco mutaciones = cinco primitivas". Cuatro frases de esta nota que pide
corregir (quedan marcadas, no borradas, hasta que Lucas decida):
1. §3 "sin caja no hay abducción, hay inducción" → es una delimitación de *nuestro paradigma* (revisión
   ante anomalías), no una definición de abducción.
2. §6 "no estaba en la lista previa → creativo" → registrar como **"no expresado previamente"**; la lista
   es una cota inferior bajo esa consigna y además cambia el episodio.
3. §6 la tercera sonda (pista de memoria vs de estructura) → **no separa recuperación de construcción**;
   son dos ayudas distintas; la literatura de analogía (Gick & Holyoak; Gentner; MAC/FAC) motiva manipular
   recuperación y estructura pero no un clasificador binario. Reformulación posible: ¿aprovecha
   correspondencias estructurales cuando no coinciden con la semejanza superficial? (2×2 fuente-objetivo).
4. §7 "transferencia diferencial = las primitivas son reales" → es **evidencia de especificidad del
   aprendizaje**, compatible con plantilla, reutilización de código, prior actualizado; la prueba correcta es
   comparar predicciones de explicaciones rivales sobre la matriz de transferencia (dos operaciones × dos
   anfitriones, exposición por demostraciones en contexto, índice S, gemelos).
Además: la caja debe demostrarse **operativa** (predicciones consistentes con la familia antes de la
evidencia crítica); "una edición" = distancia en una gramática declarada, no átomo cognitivo; el gemelo
negativo no castiga automáticamente al que "salta siempre" (la familia ampliada contiene a la base); I:C
no aplica a densidades continuas; M2/M3/M5 tal como están escritas pueden reabsorberse en la distribución
latente; "una base universal" puede ser camisa de fuerza (prefiere contrato común + dos bases). Formulación
provisional que propone: *"WAGER estudia cuándo un agente revisa una familia de modelos ante evidencia que la
vuelve insuficiente, mediante tareas mínimas y controles contrafácticos."*
