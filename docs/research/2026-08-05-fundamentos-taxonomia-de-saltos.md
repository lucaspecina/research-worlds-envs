# Fundamentos de la taxonomía de saltos — de dónde salen, cómo se justifican, dónde hay más

> **Estado:** propuesta metodológica para discutir (Lucas ↔ Claude, 2026-08-05; pendiente Codex).
> Responde las preguntas de Lucas: *"¿de dónde sacaste esas 10 naturalezas? ¿cómo lo justificamos?
> ¿cómo sabemos dónde hay más?"* y *"definir las naturalezas de una manera justificada, súper
> inteligente, que nadie antes haya visto"*. Complementa
> [menu-estrategico-y-maquina-de-saltos](2026-08-05-menu-estrategico-y-maquina-de-saltos.md) §3.1.

---

## 0. Confesión de origen (por qué esto hace falta)

La lista de 10 operadores del doc de la máquina fue **destilada en sesión por intuición experta**
(catálogo de ahas + vicio-4 + historia de la ciencia + qué puede cambiar en un programa
generativo). No tiene todavía justificación metodológica. La prueba de que no alcanza: el ejemplo
de Darwin de Lucas (pinzones ↔ criadores) reveló de inmediato un operador AUSENTE — la
transferencia estructural. Una lista que crece cuando alguien recuerda un caso no es una
taxonomía; es una colección. Este doc propone el método para convertirla en taxonomía.

## 1. El marco formal (la parte que nadie tiene): saltos como ediciones ESTRUCTURALES de un programa generativo

En WAGER un mundo ES un programa generativo. Eso permite definir "salto" sin poesía:

> **Refinamiento** = cambiar los NÚMEROS de un programa manteniendo su estructura
> (ajustar parámetros dentro de la familia).
> **Salto** = cambiar la ESTRUCTURA del programa: qué variables existen, cómo se conectan,
> bajo qué restricciones, o cómo el mundo se convierte en datos.

Los componentes sintácticos de un programa generativo son enumerables, y cada uno admite
ediciones estructurales. **La matriz componente × edición ES el espacio de operadores:**

| Componente del programa | Edición estructural | Operador resultante | Ejemplo histórico |
|---|---|---|---|
| Variables (obs./latentes) | + nodo latente | **1. Entidad oculta** | Neptuno |
| Índices de población | unidades → tipos (mezcla) | **2. Heterogeneidad oculta** | Mendel; responders |
| Índice temporal | + índice de régimen | **3. Régimen/fase oculto** | transiciones de fase |
| Coordenadas/representación | reparametrización | **4. Geometría** | Kepler log-log; espacio-tiempo |
| Grafo causal | fusionar mecanismos / causa común | **5. Unificación** | Luna y manzana |
| Restricciones globales | promover un invariante banal a restricción (simetría) | **6. Re-jerarquización de lo banal** | equivalencia (Einstein) |
| Modelo de observación | selección/censura/instrumento | **7. Proceso del observador** | Wald |
| Grafo causal | + ciclo | **8. Feedback oculto** | depredador-presa |
| Restricciones globales | conservación/discretización | **9. Cuantización** | estequiometría; Mendel |
| Estado temporal | + memoria/retardo | **10. Memoria oculta** | histéresis |

Y el ejemplo de Darwin revela que la matriz tiene **dos pisos**:

- **Piso intra-programa** (ops 1–10): ediciones a UN programa.
- **Piso inter-programa** (nuevo): relaciones ENTRE programas.
  **11. Transferencia estructural (isomorfismo)** — reconocer que el sistema actual comparte
  estructura de programa con otro sistema ya conocido, bajo otra piel, y transferir la hipótesis
  (Darwin: variación+selección+cambio en pinzones ≅ en la cría doméstica; el mecanismo faltante
  se importa). Su formalización es exactamente la teoría de **structure-mapping de Gentner**
  (analogía = mapear RELACIONES, no atributos superficiales) — y su gemelo cae solo de la teoría:
  la **analogía falsa** (similitud de superficie SIN isomorfismo relacional; transferir pierde).
  Nota de coherencia con la historia del proyecto: nuestra línea `overgen` (sobre-generalización +
  su gemelo donde generalizar SÍ era correcto) es literalmente el par vicio↔aha de este operador —
  ya construida, ya certificada.

**Respuestas que este marco da a las preguntas de Lucas:**

- *¿De dónde salen más?* De tres lugares enumerables: (a) celdas vacías de la matriz
  componente × edición; (b) el piso inter-programa (transferencia, especialización,
  generalización); (c) COMPOSICIONES de operadores (entidad oculta + feedback; mezcla + régimen…)
  — el espacio composicional es el argumento de escala de la fábrica.
- *¿Cómo sabemos si la lista está completa?* No lo sabemos — pero ahora la incompletitud es
  DETECTABLE: un salto histórico o de agente que no sea edición de ningún componente **rompe el
  marco, y eso sería un hallazgo en sí** (se registra, se agrega el componente).
- *Límite declarado del marco:* captura saltos de "entender un sistema" (el alcance de WAGER).
  No pretende cubrir toda creatividad (reformular la PREGUNTA, creatividad matemática pura,
  estética). Parcialmente fuera: el "re-encoding" de Ohlsson (cambiar la representación del
  problema, no del modelo).

## 2. Triangulación con tres literaturas independientes (la justificación externa)

Regla propuesta: **un operador entra a la taxonomía si aparece en ≥2 de las 3 columnas, tiene ≥2
casos históricos documentados y, idealmente, ≥1 falla LLM documentada.** Lo que solo tiene una
columna queda etiquetado especulativo.

| Columna | Qué aporta | Mapeos principales |
|---|---|---|
| **A. Ciencia cognitiva de la creatividad/insight** | Boden: creatividad combinacional / exploratoria / **transformacional** (cambiar el espacio mismo = nuestras ediciones estructurales). Ohlsson (cambio representacional): relajar restricciones ↔ ops 6/9; descomponer chunks ↔ ops 2/3. **Gentner** (structure-mapping) ↔ op 11. Klahr & Dunbar (búsqueda dual: espacio de hipótesis × espacio de experimentos — nuestro juego es exactamente eso) | ops 2,3,4,6,9,11 |
| **B. Historia y filosofía de la ciencia** | Peirce/Hanson: abducción como lógica del descubrimiento (la familia entera). Nersessian (razonamiento basado en modelos): analogía ↔ 11, experimentos mentales, casos límite ↔ 4/6. Darden (estrategias de cambio de teoría en genética): agregar variable ↔ 1, dividir ↔ 2/3, alterar observación ↔ 7. Thagard (revoluciones conceptuales): reclasificación ↔ 2. Dunbar (labs in vivo): analogías locales vs distantes ↔ 11 | ops 1,2,3,4,6,7,11 |
| **C. Empírica era-LLM** | Chen/Zhao/Cohan ([2607.01233](https://arxiv.org/abs/2607.01233), **el paper que Lucas linkeó — ya extraído en `como-medimos.md` §1**): familias de operación validadas con κ; los LLMs evitan justo **replace / decouple / formalize** (decouple ↔ 2/8; formalize ↔ 4/9). Can't-jump: parche-Vulcano ↔ anti-1; camino anti-MDL. [Einstein's Footsteps 2607.27794](https://arxiv.org/abs/2607.27794): los grandes saltos parten de PRINCIPIOS de simetría y abducen la teoría ↔ ops 6/9 primero, verificación después. DiscoverPhysics: fallan en especies/materia oscura ↔ 1/2. Nuestro A3 ↔ 2. Lewis & Mitchell (tareas contrafactuales): la analogía LLM es frágil fuera de lo familiar ↔ 11 | ops 1,2,4,6,8,9,11 |

## 3. La receta de validación (robada del paper que Lucas linkeó)

[Chen/Zhao/Cohan 2607.01233](https://arxiv.org/abs/2607.01233) construyó su taxonomía así — y
`como-medimos.md` §1 ya lo registró como "la receta de rigor" a copiar:

1. Partir de **fuentes autoritativas** (ellos: NSF/NIH/DARPA; nosotros: las tres columnas de §2).
2. **Refinar sobre un held-out de casos** (ellos: 150 papers; nosotros: un corpus de casos
   históricos de descubrimiento + fallas LLM documentadas, etiquetados por operador).
3. **Validar con anotadores independientes** (κ alto; matrices de confusión sin colapso de
   categorías — errores solo entre operadores adyacentes).
4. **El agregado que nadie puede copiar:** cada operador debe además **COMPILAR** — existir como
   transformador ejecutable con sus certificados (necesidad/alcanzabilidad/gemelo). Una taxonomía
   donde cada categoría es una transformación de programa es falsable y construible; las
   taxonomías puramente verbales (Boden, Nersessian) no pueden decir "este mundo instancia el
   operador 7 con brecha certificada de 0.4". **Ésa es la novedad**: la taxonomía de saltos
   operacionalizada como álgebra de ediciones de programas generativos, con certificados por
   instancia.

## 4. Tipos de fenómeno (aclaración pedida — ya estaban codificados en la nota de dirección §6)

Cada tipo es un POLO; su gemelo es obligatorio (doctrina de pares — nada se mide sin el mundo
donde el reflejo opuesto pierde):

| Eje | Polo vicio | Polo espejo |
|---|---|---|
| Magnitud paramétrica | no actualiza / sub-actualiza | sobre-actualiza / dirección equivocada |
| Incertidumbre | no la sube cuando la evidencia abre alternativas | no la baja cuando la evidencia resuelve |
| **Estructura (los saltos)** | **no abre cuando debe (aplanamiento)** | **abre cuando no debe (apofenia / entidad fantasma / analogía falsa)** |
| Tiempo | actualiza y después REVIERTE | — |
| Propagación | el modelo cambia pero acción/entrega no | cambia la entrega sin cambiar el modelo (moda) |
| Parada | cierra antes del chequeo barato | no cierra nunca / re-verifica sin fin |

## 5. Las palancas del mundo (qué variar para reproducir robustamente) — tres baldes según evidencia

**Baldes con evidencia PROPIA de que mueven el fenómeno:**
1. **Dónde vive la señal** (media → varianza → forma → régimen → solo-intervención): la palanca
   más fuerte que tenemos — con señal en la media revisan (ODE); en la forma, aplanan (SCM).
2. **Visibilidad de la partición** (etiqueta presente/ausente): 83–96% vs ~0%.
3. **Menú de hipótesis** (familia declarada legal vs no declarada): intenta-mal vs jamás-intenta.
4. **Re-entrada del propio output antes del cierre** (el rescate de ODE).
5. **Modelo** (perfiles por modelo son reales: DeepSeek se casa con la primera historia donde gpt
   pivotea — ADR 0111).

**Muertas a NUESTRA escala (no globalmente — alcance en el titular):**
6. Autoridad social sin evidencia (4.3%) · 7. filler/longitud moderada · 8. costo hundido
individual con contabilidad visible (0/60) · 9. multiplicar casilleros de edición (6/6 propagó).

**Sin probar (el blanco de D y de la máquina):**
10. **Estacionariedad** — el mundo que cambia debajo (anatomía KellyBench). ·
11. **Costo de re-trabajo real** (re-modelar vs editar una celda). ·
12. **Horizonte largo real** (>100k tokens útiles sin re-anclaje). ·
13. Mezcla confirmación+contradicción en formato Xie (nuestro conflicto-firmado usó otro formato). ·
14. Bundle identidad+pares (Big-Muddy: la escalada vive ahí, no en lo individual).

## 6. Modelos chicos (pregunta de Lucas: ¿probamos con más chicos?)

Sí — y ya es doctrina: [estrategia-modelos-chicos](2026-08-02-estrategia-modelos-chicos-para-mineria.md)
(escalera: interfaz nano/Phi-4 → minería gpt-5.4-mini → puente DeepSeek → confirmación frontier),
con el **gate** para no confundir incapacidad con fenómeno (el chico debe pasar el control
limpio/etiquetado para que su falla en el salto informe algo).

**Uso NUEVO que la máquina habilita — rango dinámico:** ordenar los mundos del archivo por "quién
logra el salto" (nadie / solo frontier / también chicos). Un mundo donde todos empatan no
discrimina ni entrena (OQ #17: sin varianza no hay gradiente); el archivo sano cubre el espectro.
Y para los fenómenos de REVISIÓN (línea D) los chicos son mejores canarios: DeepSeek ya mostró
first-story-vice donde gpt no. Regla intacta: claims sobre frontier exigen frontier e instancias
frescas.

## 7. Nombre

Propuesta: **"saltos" (jumps)** como término del programa y del paper — conecta con la literatura
(can't-jump, Boden transformacional, Einstein-test) y es auto-explicativo. "Aha" queda como nombre
histórico interno del catálogo (`ahas.md`). Operadores = "operadores de salto". Decide Lucas.

## 8. Cola de lectura nueva (antes de firmar la taxonomía — ADR 0115)

- [The Einstein Test (arXiv 2501.06948)](https://arxiv.org/abs/2501.06948) + versión
  [CACM](https://cacm.acm.org/opinion/the-einstein-test-a-test-of-ais-ability-to-generate-transformative-science/) —
  re-descubrir breakthroughs desde el corpus PRE-descubrimiento (probable candidato al paper que
  Lucas recuerda).
- [Can AI Follow in Einstein's Footsteps? (arXiv 2607.27794)](https://arxiv.org/abs/2607.27794) —
  los grandes saltos no fueron inductivos ni deductivos: principios de simetría → abducción →
  verificación; y el cuello real es el "taste" (estimar el payoff de la idea nueva, no producirla).
- [Gentner, "Analogy" — Open Encyclopedia of Cognitive Science 2025](https://groups.psych.northwestern.edu/gentner/papers/Gentner-Analogy-OECS2025.pdf) (fuente autoritativa op 11).
- Webb, Holyoak & Lu (NHB 2023, analogía emergente) + [respuesta](https://arxiv.org/abs/2308.16118) +
  Lewis & Mitchell (tareas contrafactuales) — el debate completo de op 11 en LLMs.
- Boden (*The Creative Mind*), Ohlsson (cambio representacional), Klahr & Dunbar (SDDS), Nersessian
  (*Creating Scientific Concepts*), Darden (*Theory Change in Science*) — clásicos, columnas A/B.
- [Analogy mining — Hope, Chan, Kittur, Shahaf (KDD 2017)](https://arxiv.org/abs/1706.05585) y
  [Scaling analogical innovation (PNAS 2019)](https://www.pnas.org/doi/abs/10.1073/pnas.1807185116) —
  cómo ENCONTRAR isomorfismos estructurales a escala (generador de pares op-11).
- [DreamCoder (wake-sleep library learning)](https://dl.acm.org/doi/10.1145/3453483.3454080) y
  [LILO (arXiv 2310.19791)](https://arxiv.org/abs/2310.19791) — el modelo formal de "inventar
  conceptos" = agregar primitivas al lenguaje; referencia del residuo R5 y candidato a
  descubrimiento de operadores por compresión.
- [AI-Descartes (arXiv 2109.01634 / Nat. Comm. Sci.)](https://arxiv.org/abs/2109.01634) y
  [AI-Hilbert (Nature Communications 2024)](https://www.nature.com/articles/s41467-024-50074-w) —
  datos + axiomas de fondo: derivabilidad como desempate de candidatas empíricamente empatadas,
  con pruebas formales, cero-LLM. La referencia del canal biblioteca (§12).
- [MOOSE-Chem (ICLR 2025, arXiv 2410.07076)](https://arxiv.org/abs/2410.07076) y
  [ResearchBench (arXiv 2503.21248)](https://arxiv.org/pdf/2503.21248) — hipótesis =
  `background + inspiraciones` sobre papers reales; el antecedente del mundo Swanson.
- Ya en cola de la máquina: NewtonBench y LLM-SRBench completos.

## 9. La objeción de los trucos estadísticos (Lucas, mismo día) — doctrina de diseño

> *"Mi miedo es que todos los supuestos saltos que queramos hacer emerger terminen siendo
> simplemente trucos estadísticos de distintos tipos, porque es con lo que contamos en la
> maquinaria, ¿no?"*

Cinco reglas que responden — y el punto donde el miedo tiene razón:

**R1 — El salto es relativo al MARCO, no al contenido.** La misma matemática es ejercicio o salto
según el espacio de búsqueda que el agente trae. Detectar una mezcla es un ejercicio si el
brief/menú la sugiere; es un salto si todo el marco (vocabulario, herramientas, ejemplos, historia)
vive en "una ley + ruido". El marco es una perilla REAL y MEDIDA por nosotros: familia declarada →
intenta (mal) / no declarada → jamás; etiqueta visible → 83–96% / sin etiqueta → ~0%. El
certificado de necesidad garantiza que el mejor modelo dentro del marco sugerido toca techo.

**R2 — La estadística es el JUEZ, no el juego.** Que la nota sea distancia distribucional no
vuelve estadística la habilidad, igual que el juez-compilador de AtCoder no vuelve la programación
"trucos de compilación". La habilidad vive en qué hipótesis genera y qué experimento compra; la
estadística cobra la consecuencia. Y por ADR 0150 el pago vive en la EXTRAPOLACIÓN (held-out de
régimen): la astucia sobre lo observado paga cero por construcción; solo paga la estructura que
transporta.

**R3 — Donde el miedo TIENE razón: el checklist (red-team #2/#14).** Si el alfabeto es chico y
público, "probá los 11 operadores" es una estrategia y el salto muere en checklist. Mitigaciones:
(a) los operadores COMPONEN — el espacio compuesto es combinatorio y el presupuesto lo vuelve
incomprable por enumeración; (b) la relación firma-de-anomalía → operador se diseña
MUCHAS-A-MUCHAS: varias estructuras producen anomalías superficiales parecidas y separarlas exige
comprar el experimento discriminante (aha A4) — la habilidad pasa de enumerar a *leer la firma y
priorizar*, que es abducción operacionalizada (Peirce: del carácter de la sorpresa, inferir el
TIPO de causa); (c) operadores held-out jamás usados en iteración; (d) para evaluar frontier HOY
el punto es empíricamente discutible — no corren ni un ítem del checklist (A3≈0 aun con turno
extra y criticism pedido). Para RL es la carrera armamentista ya declarada.

**R4 — No todos los operadores son estadísticos ni en su mecánica.** Transferencia (11) =
reconocimiento de isomorfismo entre sistemas; unificación (5) = notar que dos corrientes comparten
programa; re-jerarquización (6) = promover el invariante aburrido a restricción. Ahí lo
estadístico es rutina y el cuello es el reconocimiento.

**R5 — El residuo honesto, declarado.** Saltos que esta máquina NO puede exigir: inventar un
LENGUAJE de representación nuevo (no elegir/combinar dentro del lenguaje de programas
generativos), re-concebir qué cuenta como fenómeno (Kuhn completo), y el caso duro del can't-jump
(loss≈0 en todo régimen alcanzable). Se declara como alcance en el paper — ningún benchmark
existente llega ahí tampoco. Referencia formal de qué significaría cruzarlo: library learning
(DreamCoder/LILO) = agregar primitivas al lenguaje; candidato a largo plazo para descubrir
operadores por compresión en vez de autoría nuestra.

## 10. ¿Qué puede expresar la maquinaria actual? Inventario honesto + el mundo Darwin

| Operadores | Estado |
|---|---|
| 2 mezcla · 3 régimen · 7 observador | **Ya expresables** — mundos existentes los rozan (`latent_mix`, `ode_second_wave`, `survivorship_censor`/`selection_bias`) |
| 1 entidad · 4 geometría · 6 invariante · 9 conservación · 10 memoria | Expresables con maquinaria de un-mundo; construcción media |
| 5 unificación | Episodios multi-corriente (dos fenómenos, un mecanismo) — mundo "consiliencia" en cartera |
| 8 feedback | Parcial (SCM + intervenciones) |
| **11 transferencia (Darwin)** | **NO expresable hoy** — episodio de DOS sistemas; boceto abajo |

**El mundo Darwin (boceto).** El episodio contiene el sistema A — barato, familiar, totalmente
instrumentado (el análogo de la cría doméstica; puede venir como documentación en el brief, como
Darwin conocía a los criadores) — y el sistema B — caro, piel distinta (otro dominio, otras
variables), que comparte la estructura profunda del programa salvo un mecanismo observable en A y
oculto en B. El salto: reconocer el isomorfismo, transferir la hipótesis del mecanismo, y COMPRAR
en B el experimento que la pone a prueba. Entrega y nota como siempre (modelo ejecutable de B,
cero-LLM).

**Los gemelos salen solos de la teoría de Gentner** (cuadrante similitud-superficial ×
similitud-estructural): B' con mucha superficie compartida y otra estructura — transferir PIERDE
(analogía falsa); B'' con cero superficie y verdadero isomorfismo — transferir GANA. Nuestro par
`overgen`/`overgen_twin` ya es la versión intra-dominio de este cuadrante.

**Certificado nuevo que este mundo exige — el valor-de-la-analogía:** el testigo se vuelve
CONDICIONAL. Con solo los datos comprables de B (presupuesto dado), la estructura NO es
recuperable (o cuesta ≫ presupuesto); con la estructura de A como candidata, se recupera barato.
La diferencia — en presupuesto o en bits — ES el valor informacional de la analogía, computable
cero-LLM. Que sepamos, nadie tiene ese certificado.

**Maquinaria externa robable para GENERAR pares del 11:** analogy-mining de
Hope/Chan/Kittur/Shahaf ([KDD 2017](https://arxiv.org/abs/1706.05585),
[PNAS 2019](https://www.pnas.org/doi/abs/10.1073/pnas.1807185116)) — representaciones de
propósito/mecanismo para encontrar analogías estructurales a escala; nuestra versión: esqueleto
estructural del programa vs piel.

## 11. El caso duro del can't-jump, descompuesto en escalera (+ el mundo Einstein)

El caso histórico: hacia 1900 la gravedad de Newton estaba verificada a ~10⁻⁹ en TODO lo medible.
La única anomalía (43″/siglo del perihelio de Mercurio) se leía como entidad oculta (Vulcano) —
la MISMA movida que había triunfado con Neptuno en 1846. Einstein no construyó la Relatividad
General desde datos: partió de una tensión CONCEPTUAL (Newton instantáneo vs relatividad especial;
la coincidencia "banal" masa inercial = masa gravitatoria promovida a principio) y el pago
empírico llegó décadas después. Para un benchmark que puntúa predicción: **sin discrepancia no hay
gradiente** — el que no salta puntúa perfecto igual.

**La descomposición (nueva, de esta sesión):**

- **Peldaño 1 — anomalía en los datos.** Lo que ya hacemos. El truco de OQ #24: aunque el episodio
  no muestre error (loss≈0 en lo observado, como Newton), el EXAMEN cobra en regímenes no vistos →
  el gradiente existe en la nota aunque no en la experiencia del agente.
- **Peldaño 2 — sin anomalía en ningún dato; la tensión vive ENTRE los modelos del propio
  agente.** Dos dominios/instrumentos, cada uno con su ley localmente PERFECTA; las dos leyes se
  contradicen en una frontera que ningún experimento comprable alcanza; el examen cobra la
  frontera. El salto = notar la inconsistencia de los propios artefactos y unificar (composición
  de operadores 5+6: unificación + invariante promovido). Gemelo: mundo donde los dos mecanismos
  son GENUINAMENTE distintos y forzar la unificación pierde. **ESTO ES EXPRESABLE con episodios
  multi-corriente y no lo tiene nadie** — el "mundo Einstein" como instancia insignia del tier
  nuevo. El disparador no es un dato: es la coherencia interna del portafolio de modelos del
  agente — medible porque los modelos son ejecutables.
- **Peldaño 3 — el residuo puro: ni datos ni tensión interna detectable.** El salto solo por
  gusto/estética, pagando en regímenes inalcanzables. **Argumento de imposibilidad (para
  cualquier benchmark, no solo el nuestro):** para premiar el salto, el examen debe distinguir
  las teorías. Si nada alcanzable las distingue y el examen tampoco → empatan, no hay nada que
  premiar. Si el examen sí distingue → el mundo (con stakes declarados "serás evaluado fuera de
  soporte") vuelve racional buscar robustez extrapolativa → colapsa al peldaño 2 o 1. Y probar
  "gusto" con teorías empíricamente empatadas = testear si el prior del agente coincide con el
  prior de NUESTRO generador — no hay habilidad que premiar, solo base-rate. El estado epistémico
  real de Einstein (sin examen prometido) es irreproducible por definición dentro de cualquier
  cosa que puntúe: **puntuar ES prometer un examen.** Se declara como límite conceptual del campo,
  no como debilidad nuestra.

## 12. Similitud de modelo — las dos formas honestas (doctrina de score; GO de Lucas 2026-08-05)

Pregunta original de Lucas: además de la predicción, ¿podemos premiar que el MODELO se parezca al
verdadero? **Leer el código queda prohibido**: es gameable (se puede escribir código que PARECE la
estructura correcta sin serlo) y rompe el contrato conductual ("por dentro puede tener lo que
quiera"). Las dos formas que sí:

**Forma 1 — La estructura ES conducta bajo intervención y simetría.** *(Entra al diseño v1: no
depende de nada nuevo.)* Dos programas empatados en lo observacional se separan muestreándolos
bajo: (a) **do()-probes** — fijar/forzar variables y comparar las distribuciones resultantes
contra la verdad; (b) **tests de invariancia** — transformar la entrada según la simetría
verdadera y verificar que las predicciones se transforman como corresponde; (c) **funcionales
orientados** tipo `A3` (firma de mezcla), ya probados en agosto. Todo entra a la BATERÍA como
regímenes nuevos: la nota sigue siendo "¿qué tan bien predice tu modelo?", solo que en las
coordenadas donde la estructura es visible. Implicancia para certificados: la brecha de teoría
(certificado de necesidad) se computa TAMBIÉN sobre estas sondas — la lección del ataque #5 del
red-team (energía ciega a multimodalidad), sistematizada.

**Forma 2 — Consistencia/derivabilidad con teoría declarada (la movida AI-Descartes).** Con
axiomas de fondo declarados, el empate empírico se rompe por derivabilidad, chequeable
mecánicamente (lógica/optimización, cero LLM). **Depende del canal biblioteca → DEMARCADA FUTURO
con él (§13).**

**Métrica descriptiva secundaria (jamás reward):** match simbólico canónico
(canonicalización tipo LLM-SRBench) para describir entregas — frágil/gameable; solo diagnóstico.

## 13. El canal biblioteca (teoría como insumo) — FUTURO, EXPLÍCITAMENTE DEMARCADO (Lucas 2026-08-05)

Decisión de Lucas: añade mucha complejidad ("no se me ocurre cómo podríamos crear teoría bien");
se acota y se demarca. **El canal biblioteca** (documentos de confiabilidad mixta), **la forma 2
de §12** (derivabilidad), y los mundos que dependen de él — **Einstein (peldaños 2/2.5), Swanson,
Darwin-con-documentación** — quedan **documentados pero FUERA del alcance v1**. No se construyen
ni se prototipan.

Costos reales que justifican demarcarlo: autoría de teoría por mundo = disciplina anti-leak nueva
(el escritor de la biblioteca debe ser ciego a batería/rivales); superficie de contaminación
textual; y el pipeline base todavía no está validado.

**Condiciones de retoma:** (a) alcance v1 (§14) validado con yield decente; o (b) un caso real
del catálogo cuya reproducción fiel EXIJA teoría como insumo; o (c) decisión explícita de
Lucas/Codex. Los bocetos no se pierden: viven en §10–§12 de este doc.

## 14. Alcance v1 propuesto: el subconjunto inicial de saltos

Criterios, en orden: (1) maquinaria existente; (2) evidencia previa de que el mundo elicita falla
real; (3) **diversidad de componente formal dentro del subconjunto** — que el prototipo pruebe la
generalidad del pipeline, no un solo tipo; (4) novedad frente a vecinos; (5) conexión con el
fenómeno ya confirmado (anclar el programa en evidencia).

| Estado | Operadores | Razón |
|---|---|---|
| **V1 — construir ya** | **2 mezcla · 3 régimen · 7 observador** | Semillas existentes (`latent_mix`/SCM; `ode_second_wave`; `survivorship_censor`/`selection_bias`); tres componentes formales DISTINTOS (población / tiempo / observación); el 2 ancla el fenómeno confirmado (A3); el 7 es nicho que nadie ocupa como benchmark de salto y el más "ciencia real" (sesgo de supervivencia/selección — Wald) |
| **HELD-OUT — no tocar hasta confirmación** | 1 entidad · 9 conservación | Construibles con maquinaria de un-mundo; se reservan FRESCOS para probar la generalidad del alfabeto sin contaminación de iteración (E3 a nivel operador) |
| **BANCO** | 4 geometría · 8 feedback · 10 memoria | Un-mundo, construcción media; entran cuando v1 valide el pipeline |
| **FUTURO DEMARCADO** | 5 unificación · 6 invariante · 11 Darwin · mundos Einstein/Swanson · canal biblioteca | Exigen episodios multi-corriente/multi-sistema o biblioteca (§13) |

Nota sobre el 7 (observador): sus mundos semilla existen desde la época 1, pero NUNCA pasaron por
certificados de salto (necesidad/testigo/gemelo) ni tienen — que conste — evidencia agéntica
registrada como mundos de salto. Correr el 7 por el pipeline ES el test de que la máquina
generaliza más allá de lo ya explorado: cumple el rol de "operador genuinamente nuevo" del
prototipo (§3.7 del doc de la máquina) con costo mínimo.

## 15. Siguiente paso concreto propuesto

1. **Corpus held-out de casos** (~30–50: históricos + fallas LLM documentadas) → receta §3 →
   congelar el alfabeto v1. *(Puede correr en paralelo a 2.)*
2. **Prototipo del pipeline sobre el alcance v1 (§14):** transformador + 5 certificados + gemelo +
   robots para los operadores 2/3/7. Construible sin `.env`; smokes con agentes al recuperar
   credenciales.
3. Las lecturas de §8 alimentan el paso 1; NewtonBench y LLM-SRBench completos alimentan el 2.
4. **Cruce con Codex** del paquete completo antes de construir en serio (ADR 0172).
