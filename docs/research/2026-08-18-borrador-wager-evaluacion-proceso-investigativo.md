# Borrador de dirección — WAGER como instrumento del proceso investigativo

> **Estado:** BORRADOR EN DISCUSIÓN · **Fecha:** 2026-08-18 · **Decide:** Lucas.
>
> Esta nota no cambia el rumbo, no supersede ADRs y no autoriza nuevas corridas. Ordena una
> posibilidad nacida de la conversación sobre Model Discovery Agent y de las autopsias de
> Perfiles persistentes y Partículas bajo una sonda.

## La síntesis propuesta

La pregunta principal de WAGER no cambia:

> **¿El agente descubre y realiza el salto abductivo que hace falta para construir el modelo bueno
> del mundo?**

La vuelta de tuerca es tratar a WAGER no solo como una evaluación del resultado final, sino como un
instrumento para observar **dónde se gana o se pierde ese salto durante una investigación**.

Una entrega incorrecta puede esconder procesos muy distintos: la idea nunca apareció; apareció
como palabra suelta; se volvió una hipótesis concreta pero fue descartada sin probar; ganó la
comparación pero se implementó mal; o llegó al código y se perdió después. Si todo termina reducido
a una sola nota, esos casos parecen iguales aunque científicamente no lo sean.

La identidad propuesta sería:

> **WAGER puntúa mecánicamente acciones y consecuencias de una investigación, y caracteriza sus
> eslabones observables mediante una rúbrica auditada en mundos de verdad conocida.**

Esto no convierte a WAGER en un benchmark de harnesses. El agente con el **harness mínimo
congelado** sigue siendo la celda primaria: ahí medimos lo espontáneo. Un planner, una alarma de
desajuste, memoria externa o un crítico pueden probarse después como factores que cambian el
proceso, igual que cambiar de modelo, mundo, condición o entrenamiento.

## Qué queda fijo y qué se puede enchufar

La idea de matriz sirve como mapa de comparaciones, no como un factorial que haya que llenar.

| Instrumento WAGER — queda fijo dentro de un estudio | Factores que pueden compararse |
|---|---|
| Contrato entre verdad, acciones y score, congelado dentro del estudio | Modelo o agente |
| Acciones legales, presupuesto y datos entregados | Configuración del harness del agente |
| Ledger server-side y capturas que no alteren la tarea | Mundo e instancia, congelados dentro de cada comparación |
| Examen sellado y puntaje cero-LLM | Condición o intervención |
| Rúbrica del proceso congelada para ese caso | Antes/después de entrenamiento |

Hay dos sentidos de “harness” que no conviene mezclar. El **instrumento WAGER** registra y puntúa;
el **harness del agente** es el andamiaje cognitivo bajo prueba. Solo el segundo es una variable de
la matriz.

Cada estudio debe elegir pocos contrastes que respondan una pregunta. La tabla no justifica correr
todas las combinaciones posibles. El mundo puede variar entre estudios, pero el programa concreto
y su scoring quedan congelados dentro de cada comparación.

Registrar evidencia server-side es pasivo. Pedirle al agente que mantenga un `working_model`, haga
checkpoints o declare su creencia puede cambiar su conducta: eso pertenece a la tarea o al harness
bajo prueba y debe mantenerse idéntico entre las condiciones que se comparan.

## Por qué esta formulación apareció ahora

### Perfiles persistentes

El resultado final decía que 9/10 agentes entregaron una sola campana y ninguno escribió el modelo
compacto de dos tipos. La autopsia cambió la atribución: ocho negativos mencionaron mezcla o
multimodalidad y uno encontró los dos grupos exactos, pero los descartó sin compararlos. El endpoint
final medía realización; no demostraba por sí solo ausencia de creatividad.

### Partículas bajo una sonda

Con la idea de dos tipos persistentes nombrada, 3/3 agentes la pusieron en juego y la eligieron;
2/3 conservaron la geometría de los dos tipos en código y solo 1/3 calibró bien toda la distribución.
La nota final mezclaba el salto estructural con errores posteriores sobre el ruido de lectura.

### La planta química

La mejor campana sin estructura obtenía 0.986/1.0. Ahí ninguna rúbrica del proceso podía rescatar el
claim original: si omitir el salto casi no cuesta, el mundo no permite acusar al agente por no
realizarlo. La validación matemática del caso sigue estando antes que toda interpretación.

Estos tres ejemplos sostienen una posibilidad metodológica, todavía no una generalización sobre
los LLMs:

> **Una nota final puede confundir fallas investigativas distintas; un perfil de eslabones puede
> separarlas, siempre que sus observables sean confiables y estén definidos antes de correr.**

## Qué podemos medir realmente

No todo el proceso es mecánico. La formulación defendible es **instrumento mecánicamente anclado**,
no “lector mecánico de todo el razonamiento”.

| Parte del proceso | Qué puede observar WAGER | Naturaleza de la lectura |
|---|---|---|
| Evidencia | Qué compró y qué información recibió | Mecánica |
| Grieta | Si el modelo vigente quedó objetivamente en tensión; si el agente lo expresó | Mecánica + descripción de traza |
| Creatividad | Si expresó una hipótesis estructural específica o construyó un candidato | Traza citada + artefacto cuando existe |
| Puesta en juego | Si trató la hipótesis como rival vivo | Traza, plan o candidato registrado |
| Desarrollo | Si dedujo una consecuencia que separa rivales | Traza o predicción ejecutable |
| Contraste | Si corrió una prueba con poder real para discriminar | Mecánica |
| Selección | Qué alternativa favorecía la evidencia y cuál eligió | Resultado mecánico + decisión registrada |
| Realización | Qué forma implementó y cuán bien calibró el modelo | Mecánica |
| Propagación | Si el cambio sobrevivió en entregas y decisiones posteriores | Mecánica cuando el mundo lo instancia |
| Resultado | Ganancia real contra el rival fuerte sin salto | Mecánica y cero-LLM |

La traza permite decir “expresó esta hipótesis”; no permite afirmar qué creyó internamente. Las
anotaciones descriptivas jamás entran al reward. Cada casillero admite `incierto` y `N/A`.

La secuencia tampoco debe tratarse como una escalera psicológica universal. Una investigación puede
volver atrás, generar antes de notar una grieta o no instanciar propagación. Es un **perfil de
eslabones observables**, no una teoría de que toda mente avanza linealmente por nueve estaciones.

## Relación con Model Discovery Agent

Model Discovery Agent construye deliberadamente un descubridor híbrido: la matemática detecta que
el modelo no alcanza, obliga a reabrir el menú, compara las formas y elige experimentos; el LLM
propone candidatos dentro de un vocabulario bastante guiado.

WAGER hace la pregunta complementaria: **¿qué partes de ese proceso realiza el agente sin ese
exoesqueleto?**

Los componentes estilo MDA pueden servir como una sonda diagnóstica ocasional: por ejemplo, agregar
solo una alarma de desajuste después de un negativo y observar si reaparece la investigación. No son
el producto principal ni deben recorrer una escalera automática. El endpoint primario sigue siendo
el proceso con harness mínimo congelado.

La ablación de MDA es motivación externa, no una réplica directa de WAGER: sus mundos, prompts,
gramática de modelos y división del trabajo son distintos.

## Claim candidato y límites

Una formulación publicable posible, si la validamos, sería:

> **Las evaluaciones basadas solo en el resultado final confunden fallas investigativas diferentes.
> WAGER combina puntuación ejecutable cero-LLM, mundos de verdad conocida y artefactos auditables
> para distinguir perfiles observables compatibles con distintos quiebres entre la aparición de
> una hipótesis estructural y su uso funcional.**

Esta nota no autoriza todavía a afirmar que:

- WAGER observa todo el razonamiento;
- los nueve eslabones son una cadena causal universal;
- ya conocemos una tasa general de creatividad de los LLMs;
- un score bajo identifica por sí solo el vicio;
- los harnesses son la identidad o el leaderboard principal del proyecto;
- las evidencias retrospectivas ya validan el instrumento.

La novedad potencial no está en una pieza aislada. Está en juntar verdad programática conocida,
evidencia legal por partida, modelos ejecutables intermedios, pruebas con poder calculable,
consecuencias selladas y un reward sin juez-LLM.

## Guardarraíles si esta dirección avanza

1. El agente con harness mínimo congelado sigue siendo el resultado primario.
2. Primero se certifica el mundo: el salto debe ser posible, necesario, visible y materialmente útil.
3. Las ayudas sirven para capacidad o diagnóstico; nunca se rebautizan como creatividad espontánea.
4. La matriz es un esquema de metadatos y contrastes selectivos, no un factorial obligatorio.
5. El gemelo se agrega cuando derrota un falso positivo concreto; no vuelve a ser obligatorio ahora.
6. La ficha se congela antes de una tanda confirmatoria y conserva `incierto`/`N/A`.
7. Ninguna lectura textual entra al reward ni reemplaza al comportamiento ejecutable.
8. Descubrimiento y confirmación usan episodios frescos separados.

El “umbral de reestructuración” puede ser una salida futura interesante, pero no debe venderse como
un número universal de cada modelo. La cantidad relevante sería una **curva condicionada**: ante
qué magnitud y visibilidad de desajuste, en qué mundo y con qué harness, el agente reabre su forma de
modelar.

## Piloto mínimo para saber si la idea sirve

### 1. Prueba retrospectiva barata

Reanotar las diez trazas de Perfiles persistentes usando la ficha v1:

- dos anotadores independientes;
- sin mirar el score final mientras clasifican;
- reglas congeladas y una cita o artefacto por casillero;
- `incierto` cuando la traza no alcanza;
- desacuerdos conservados, no resueltos conociendo la verdad.

El piloto estima, sin gate inventado después, qué fracción de cada casillero resulta observable y
cuánto acuerdo hay por eslabón, con incertidumbre y una medida apropiada de concordancia. Sirve para
descubrir qué campos son ambiguos; no valida causalmente la rúbrica.

“Primer quiebre” no significa tomar el primer `no` de una escalera lineal. Para un candidato
estructural específico, es la primera transición observable que no ocurre pese a existir la
oportunidad y la evidencia necesarias. Si el candidato nunca aparece en traza o artefactos, solo se
puede registrar `sin señal observable`, no afirmar que nunca existió internamente.

Si generación, puesta en juego y selección no se pueden distinguir, o las etiquetas se deducen
simplemente de la entrega final, la propuesta queda falsada como instrumento de proceso. Seguiría
siendo una buena narrativa de autopsia, pero no el producto prometido.

### 2. Validación prospectiva posterior

En un anfitrión futuro, congelar la ficha y los registros antes de correr. Después de negativos,
usar como máximo un fork desde el mismo estado: ayuda dirigida al quiebre observable diagnosticado
contra un mensaje neutral equivalente.

La rúbrica gana validez si el diagnóstico predice qué intervención rescata el **siguiente artefacto
mecánico** y mejora después la consecuencia funcional. Si no predice nada, solo está contando una
historia retrospectiva convincente.

Esto no habilita esa corrida ahora. Primero debe funcionar la prueba barata sobre las trazas ya
existentes.

## Decisiones que siguen abiertas

- Si esta formulación describe la identidad de WAGER o solo una aplicación secundaria.
- Si la ficha v1 tiene suficiente acuerdo y observabilidad para sostenerla.
- Qué eslabones deben ser comunes a todos los mundos y cuáles pueden quedar `N/A`.
- Cuándo un harness externo merece entrar como contraste científico.
- Qué validación prospectiva mínima convertiría el borrador en dirección adoptada.

Hasta resolverlas, el rumbo operativo vigente no cambia: terminar la reanotación metodológica y
modificar una sola vez el anfitrión de Partículas para que el ruido de lectura no se confunda con el
salto estructural.

## Documentos relacionados

- [Protocolo v1 — validar el caso y leer la trayectoria](../adr/0186-protocolo-v1-validacion-y-trayectoria-del-salto.md)
- [Cómo medimos §2.1](../como-medimos.md#21-protocolo-v1--validar-el-caso-y-leer-la-trayectoria-del-agente)
- [MDA en la lectura de fuentes](../lectura-de-fuentes.md#mda-model-discovery-agent-arxiv-260809696)
- [MDA explicado en el marco de indagación](../../WIKI-INDAGACION.md#un-vecino-muy-cercano-model-discovery-agent-mda)
- [Perfiles persistentes](2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md)
- [Fallas de la indagación](../../WIKI-FALLAS.md)
