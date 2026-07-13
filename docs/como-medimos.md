# Cómo medimos — registro y reflexión sobre métodos de MEDICIÓN del juicio

> **Por qué existe este doc (Lucas, 2026-07-10).** El problema más difícil e importante del proyecto
> es **CÓMO MEDIR**: cómo medimos cada vicio, cómo medimos los aha / las formas de generar ideas e
> hipótesis. Cuando aparece un paper que MIDE alguna de estas cosas, acá anotamos **cómo lo mide** (el
> método concreto, no el hallazgo — el hallazgo va a `lectura-de-fuentes.md`) y **reflexionamos** sobre
> qué podemos robar, qué evitar, y qué nos dice sobre nuestra propia medición.
>
> **La distinción que ordena todo: MEDIR-PARA-DESCRIBIR vs MEDIR-PARA-PREMIAR.**
> - *Describir* (caracterizar una población, un modelo, una distribución): un juez-LLM VALIDADO
>   está bien — no hay presión de optimización que lo engañe, porque nadie entrena contra él.
> - *Premiar* (dar reward para entrenar/rankear): **debe ser cero-LLM** — bajo presión de
>   optimización, cualquier juez-LLM se gamea (se actúa la forma sin el fondo). Esta es la regla dura
>   de WAGER.
>
> Casi todos los papers de la literatura miden PARA DESCRIBIR. WAGER mide PARA PREMIAR. Por eso muchos
> métodos lindísimos de la literatura NO se pueden portar al reward path — pero **sí** se pueden usar
> como instrumento DESCRIPTIVO para VALIDAR que un mundo elicita el vicio (off-reward). Tenerlo claro
> evita dos errores: copiar un juez-LLM al reward (prohibido), y descartar un método útil solo porque
> usa un LLM (sirve para describir/validar, no para premiar).

---

## 1. Chen, Zhao & Cohan 2026 — "Measuring the Gap..." (2607.01233) — cómo midieron la generación de ideas

**Qué miden**: no la calidad de UNA idea, sino la **distribución de "movidas de investigación"** que
un modelo produce vs la que producen los humanos, sobre el mismo contexto. Es medición de *generación
de ideas/hipótesis* — justo el polo aha que a nosotros nos cuesta puntuar.

### El método, paso a paso (la anatomía de la medición)

1. **Anclaje al MISMO input (el truco de comparabilidad)**: por cada paper humano real, reconstruyen
   4-8 trabajos previos que "razonablemente precedieron" a la idea (de la sección related-work del
   paper), y dan SOLO esos títulos+abstracts como input. La idea HUMANA = la que realizó el paper; la
   idea LLM = la que el modelo genera desde ese mismo contexto. Así, cualquier diferencia no es por
   elegir otro tema — es por **cómo cada uno enmarca el hueco y construye la contribución**.
   → *espejo de lo nuestro*: nosotros anclamos naive/canónico/agente al MISMO mundo. Misma jugada de
   comparabilidad, distinto objeto.
2. **Descomponer la salida en partes estructuradas**: cada idea = (motivación, método). No prosa
   libre: dos casilleros. → *espejo*: nuestra submission es un programa con contrato (estructura fija).
3. **Etiquetar con una TAXONOMÍA de 2 ejes, construida con rigor** (esto es lo más transferible):
   - *Opportunity Pattern* (POR QUÉ vale la idea; 7 etiquetas): puzzle/contradicción · hueco de
     explicación · desajuste de alcance · hueco de evidencia · **oportunidad-puente** · hueco de
     falla/riesgo · cuello de botella de recursos.
   - *Method Paradigm* (CÓMO se convierte en contribución; 7 etiquetas): **síntesis/unificación** ·
     relajar/extender alcance · robustificación · derivación formal · mapeo empírico · artefacto/
     sistema · optimización/búsqueda.
   - **Cómo construyeron la taxonomía** (la receta de rigor): partieron de las guías de formulación de
     proyectos de **NSF, NIH, AHRQ y DARPA** → 11 patrones + 9 métodos iniciales → los **refinaron
     sobre 150 papers held-out** (hasta 2 etiquetas por eje + "otro"; fusionaron duplicados, separaron
     etiquetas que mezclaban motivación con método, sacaron las atadas a un dominio) → final 7×7. Tres
     requisitos: que sean marcos recurrentes, generalizables entre dominios, sin colapso sistemático
     de categorías.
4. **Anotador automático = un LLM, VALIDADO contra humanos** (el punto clave de método, y el límite):
   GPT-5.4-mini recibe la taxonomía + el contexto + (motivación, método) y devuelve etiqueta primaria
   y secundaria por eje + scores. **Validación**: sobre los 150 held-out, dos autores auditaron;
   **Cohen's κ entre el LLM y cada humano = 0.84, 0.81, 0.93** (acuerdo alto); revisaron matrices de
   confusión para asegurar que los errores caen en etiquetas ADYACENTES, no en colapso de categorías.
   → *acá está la línea*: es un JUEZ-LLM. Legítimo porque MIDE-PARA-DESCRIBIR (nadie entrena contra
   él) y está validado. **NO portable a nuestro reward** (se gamearía). SÍ portable como instrumento
   descriptivo para validar mundos (ver §2).
5. **Métricas DISTRIBUCIONALES, no puntuales** (la lección grande para nosotros): por cada modelo y
   eje estiman la distribución empírica de etiquetas y la comparan con la humana con **TVD** (cuánta
   masa de etiquetas habría que mover para igualar al humano), **JSD** (divergencia acotada simétrica)
   y **entropía normalizada** (qué tan concentrado está — bajo = pocos movimientos repetidos). El
   argumento explícito: *"una sola idea puede parecer novedosa y coherente, mientras que el conjunto
   de ideas de la misma fuente refleja un rango angosto de taste."*
6. **Análisis de mecanismo (cómo abren la caja)**:
   - *Archetype clustering*: reescriben cada propuesta a una frase-arquetipo de una línea (un LLM,
     abstrae el dominio), la clusterizan (TF-IDF + MiniBatchKMeans, k=30) y **normalizan el verbo
     principal a una "familia de operación"** (integrar, unificar, reemplazar, desacoplar,
     formalizar...). Después: log-odds modelo-vs-humano por operación (integrar 34.2% vs 2.35% →
     log-odds 3.07). → una forma de medir "¿QUÉ MOVIDA hizo?" desde salida libre.
   - *Representación*: embeddings compartidos (Qwen3-Embedding-4B) → similitud modelo-modelo 0.83 vs
     humano-modelo 0.72-0.78 (los modelos se parecen entre sí más que a un humano), + una métrica de
     cuán difusamente se posiciona la propuesta respecto de sus trabajos previos.
7. **Scores diagnósticos ordinales (0-3)** del anotador: *surface stitching* (¿es combinación
   superficial?), **bottleneck specificity** (¿identifica el mecanismo/factor limitante preciso?),
   *boilerplate* (fraseo genérico). → conceptos medibles que nos importan, aunque acá salgan de un LLM.

### Reflexión — qué nos enseña sobre CÓMO MEDIMOS

- **Robamos: pensar DISTRIBUCIONALMENTE.** Nuestra crisis de la semana (medianas de n=8 son ruido, la
  varianza corrida-a-corrida ahogó la señal) es EXACTAMENTE lo que este paper resuelve mirando la
  distribución completa, no puntos. Para el rediseño del experimento de pistas y para E1: reportar
  **distribuciones de R + tasas con intervalos**, no medianas sueltas; y pensar el perfil de un modelo
  como una **distribución de movidas/firmas** entre muchos mundos, no un número por mundo.
- **Robamos: la receta de taxonomía con rigor.** Nuestra taxonomía de vicios/ahas se construyó de
  papers; su método (fuentes autoritativas → refinar en held-out → validar con κ contra humanos → sin
  colapso de categorías) es un estándar que podemos adoptar/citar cuando formalicemos la nuestra.
- **Robamos (para DESCRIBIR, no premiar): la abstracción a "familia de operación".** Medir "¿qué
  movida hizo el agente?" (integrar vs desacoplar vs reemplazar) desde su traza/entrega, con un LLM
  anotador OFF-reward, es una forma legítima de **validar que un mundo elicita el vicio** — sin tocar
  la nota. Es el complemento descriptivo de nuestro certificado (que es operacional).
- **La diferencia de fondo: MOVIDA vs CONSECUENCIA.** El paper mide la movida upstream (qué idea
  proponés) directamente del texto. WAGER mide la consecuencia downstream (¿tu modelo reproduce el
  mundo en regímenes no vistos?). Son complementarios: ellos ven "sobre-produce síntesis" sin correr
  ningún experimento; nosotros vemos "su modelo se cae fuera de soporte" sin nombrar la movida. El
  ideal a futuro: **medir las dos** — la consecuencia con el reward cero-LLM (para premiar), la movida
  con un anotador descriptivo (para validar/diagnosticar que el mundo pega donde debe).
- **Lo que NO copiamos: el juez-LLM en la nota.** Toda su medición pasa por un LLM (anota las
  etiquetas, extrae la idea humana del paper, reescribe los arquetipos). Impecable para describir una
  población; imposible para nuestro reward. Es la confirmación por contraste de por qué WAGER es
  cero-LLM: ellos pueden porque nadie optimiza contra su anotador.
- **Un caveat honesto de su método** (no es crítica destructiva, es límite): la "idea humana" también
  la extrae un LLM del paper, y las etiquetas las pone un LLM. Validaron con κ alto, pero la medición
  es LLM-mediada de punta a punta. Para nuestra tesis eso refuerza el valor de tener AL MENOS un lado
  (la nota) que no dependa de ningún LLM.

---

## 2. Implicancia para WAGER — CÓMO medimos cada cosa (el marco, informado por lo de arriba)

- **Cómo medimos un VICIO (hoy, operacional/reward)**: mundo donde el vicio es la jugada perdedora →
  la entrega ejecutable se puntúa contra el mundo verdadero en regímenes no mostrados → R baja = vicio
  presente. *Debilidad recién aprendida*: R por-episodio es ruidoso (bimodal) → hay que medir
  DISTRIBUCIONALMENTE (tasa de caída, no mediana). *Complemento descriptivo posible*: anotar la
  distribución de movidas del agente (off-reward) para validar que el mundo elicita ESE vicio.
- **Cómo medimos un AHA (hoy)**: mundo donde la operación-aha es la ÚNICA vía a R=1 (el naive/
  incremental toca techo); el que llega arriba hizo el salto. Firmas de trace observadas, JAMÁS
  premiadas (construye una variable no dada; compra la evidencia discriminante; un mecanismo cubre
  ambas anomalías). *Lo que el paper agrega*: una forma de MEDIR la movida generativa (qué operación)
  a nivel distribución — útil para validar que nuestros mundos-aha piden la operación que decimos.
- **La pregunta abierta que este doc deja viva**: ¿cuál es el instrumento DESCRIPTIVO cero-costo-de-
  gaming que valida que un mundo pega donde debe? Candidatos: (a) la pista dirigida (en rediseño,
  ADR 0122); (b) los robots hábito/juicio (certificado del par); (c) un anotador de movidas off-reward
  estilo §1.6. Los tres son descriptivos; ninguno toca la nota. Elegir/combinar es trabajo de diseño.

*(Doc vivo. Cada paper nuevo que MIDA juicio/vicios/ideas entra acá con su método + reflexión, además
de a `lectura-de-fuentes.md` con su hallazgo.)*

## 3. Los que miden la ACTUALIZACIÓN DE CREENCIAS (el cluster del foco — 3ª oleada, 2026-07-13)

Métodos robables (todos DESCRIBEN; ninguno entra al reward — cero-LLM intacto). Links y
estado de lectura en `lectura-de-fuentes.md`; hallazgos en `vicios/vicio-1`.

- **Oráculo normativo + destilación** ([Qiu, 2503.17523](https://arxiv.org/abs/2503.17523)):
  computa la posterior bayesiana exacta del setting y mide la distancia del modelo; después
  ENTRENA imitando al normativo (y generaliza). Robable como VALIDADOR en mundos con posterior
  tractable; imposible como reward general — en investigación abierta no hay oráculo (nuestro
  lugar: fidelidad en held-out).
- **El piso sin hablante como brazo de control** ([Hu, 2607.05545](https://arxiv.org/abs/2607.05545)):
  mismo payload con y sin fuente — separa contenido de social. Obligatorio en toda sonda
  nuestra del canal social (sin ese brazo, "social" mide contenido).
- **Probe de creencia interna + steering causal** ([Yang, 2505.16170](https://arxiv.org/abs/2505.16170)):
  mide la creencia aparte de la salida y la manipula para probar causalidad. Necesita pesos →
  descriptivo puro, útil en E2 con modelos abiertos.
- **Creencia declarada vs ACCIÓN** ([Pal, 2511.13240](https://arxiv.org/abs/2511.13240)):
  confidencias elicitadas vs conducta (apostar, buscar info, defender bajo desafío) — la
  brecha reconocer→actuar como métrica separada de la creencia.
- **El predictor de crossover** ([Vigraham, 2605.04361](https://arxiv.org/abs/2605.04361)):
  la exploración de base SIN material predice si el material mostrado ayuda o daña (r=−0.82) —
  barato en nuestros mundos (correr la base sin material primero).
- **La lección del distractor auditado** ([Sturgeon 2026, LessWrong](https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail)):
  la celda "irrelevante" NO se certifica por juicio (a dos frontiers les dio κ=0.32) — en
  WAGER se certifica COMPUTABLE desde la verdad del mundo: condicionar en el material no
  cambia la posterior sobre mecanismos ni el score alcanzable. Diferencial nuestro; va al
  certificado del mundo del canal contenido.
- **Del dossier externo (vía B)**: puntuar la actualización en LOG-ODDS contra el generativo
  del mundo (rigidez = cambio < normativo · sobre-reacción = > · deriva = cambio con LR≈1 ·
  testimonio virtuoso = cambio ∝ confiabilidad demostrada de la fuente); verbo
  `registrar_creencia({H: p})` en checkpoints (la prosa no puntúa) contrastado con la creencia
  REVELADA (predicciones held-out + elección del próximo experimento bajo costo); confiabilidad
  del par ENSEÑADA programáticamente (historial 50% vs 80%, misma frase); y la nota del par
  por el mínimo de MEDIAS APAREADAS por subfamilia — jamás mínimo por episodio (amplifica
  ruido).

