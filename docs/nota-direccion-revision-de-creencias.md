# WAGER — guía del programa de revisión de creencias

> **Guía conceptual canónica y viva.** Consolidada el 2026-07-31 por pedido de Lucas a
> partir de la nota de dirección original, la anatomía de casos reales y los reassessments.
> Sirve para volver periódicamente un paso arriba y comprobar que mundos, experimentos y
> claims siguen estudiando el mismo objeto.
>
> - Esta guía dice **qué queremos entender y qué debe cubrir el programa**.
> - [`docs/vicios/vicio-1-calibracion-de-creencias.md`](vicios/vicio-1-calibracion-de-creencias.md)
>   conserva la evidencia, cifras y anatomía detallada de los casos.
> - [`docs/roadmap.md`](roadmap.md) dice **dónde estamos y qué sigue**.
> - Los ADR conservan decisiones e historia; un instrumento nunca redefine por sí solo esta guía.

## La pregunta, en una frase

> **¿Cuándo y por qué un agente ajusta correctamente su modelo del mundo a medida que recibe
> evidencia durante una investigación —cambiando, conservando o dudando en la magnitud
> justificada— y en qué punto se pierde esa revisión antes de llegar a sus acciones y entrega?**

No estudiamos “si los modelos cambian de opinión”. Estudiamos si cambian **en proporción al
valor probatorio de lo que observaron**. Cambiar siempre es tan incorrecto como no cambiar
nunca.

La conducta se cobra sobre un **modelo predictivo ejecutable** y sus consecuencias contra la
verdad oculta del mundo, sin un LLM en el reward. La prosa sirve para diagnosticar, no para
decidir si acertó.

## 1. Qué puede exigir racionalmente la evidencia

| Evidencia disponible | Respuesta correcta |
|---|---|
| Refuta la estructura central | **Pivotear** a otro modelo |
| Corrige una parte sin destruir el resto | **Revisar local o parcialmente** |
| No discrimina o confirma lo anterior | **Mantener** el modelo |
| Abre alternativas que los datos no resuelven | **Aumentar incertidumbre** |
| Resuelve una ambigüedad previa | **Reducir incertidumbre** |

La respuesta correcta se define server-side usando únicamente la información legalmente
disponible en ese momento. No se deduce retrospectivamente mirando la verdad.

## 2. Los fenómenos y ejes que debe cubrir el programa

No forman una única escala llamada “carga”. Son mecanismos candidatos que pueden interactuar
y también producir efectos opuestos.

### A. La evidencia que encuentra al agente

1. **Valor probatorio.** Débil, moderado o concluyente: cuánto discrimina realmente entre
   modelos rivales.
2. **Visibilidad.** Limpia; mezclada con datos rutinarios; poco saliente; o llamativa pero sin
   información real. Valor y visibilidad se manipulan por separado.
3. **Origen y adquisición.** Resultado de un experimento elegido por el agente; dato rutinario
   del entorno; evidencia externa; o afirmación sin sustento.

### B. La trayectoria que ya construyó

4. **Autoría/endogeneidad.** Modelo heredado, atribuido como propio o realmente construido
   mediante las decisiones del agente.
5. **Compromiso acumulado.** Cuánto tiempo, trabajo, decisiones y expectativas se apoyan ya en
   el modelo anterior.
6. **Momento y horizonte.** Formación, mitad o cierre; después de cinco pasos o de quinientos.
   El tiempo no es el mecanismo por definición: puede ser un proxy del compromiso acumulado.

### C. La revisión que sería necesaria

7. **Tamaño del cambio.** Retocar un parámetro, separar un componente o reemplazar la
   estructura explicativa central.
8. **Fricción real de revisión.** Cuántas dependencias, análisis, decisiones o partes del
   artefacto deben rehacerse para aplicar correctamente el cambio.
9. **Recursos restantes.** Tiempo, presupuesto y oportunidades de comprobar o implementar.
   Esto condiciona qué reparación es racional, pero no define la fricción.

**Fricción no significa cobrar una tarifa artificial por cambiar de opinión.** Un costo
explícito puede ser una manipulación controlada futura, pero el fenómeno principal es que una
misma corrección puede exigir tocar una pieza o reconstruir una obra entera.

### D. Extensiones importantes, no asumidas como centro

10. **Estacionariedad.** Aprender más sobre un mecanismo fijo frente a detectar que el mundo
    realmente cambió.
11. **Entorno social.** Fuente, autoridad, pares, identidad y consenso.
12. **Orden de llegada.** La misma evidencia en secuencias distintas puede producir otra
    trayectoria.

Estos ejes están registrados para no olvidarlos, no para construir un factorial gigantesco.

## 3. Dónde puede romperse la cadena

| Etapa | Failure mode observable |
|---|---|
| **Buscar** | No compra el experimento que podría falsar su hipótesis |
| **Notar** | El dato llega, pero queda como ruido de fondo |
| **Interpretar** | Nota la anomalía, pero le asigna un significado incorrecto |
| **Asimilar** | Entiende o menciona la corrección, pero su modelo predictivo no cambia |
| **Actuar/propagar** | Corrige el modelo, pero no sus decisiones, dependencias o entrega |
| **Persistir** | Actualiza correctamente y después vuelve a la idea inicial |
| **Calibrar el alcance** | Convierte un caso válido pero local en una ley general |

Por eso se observan por separado:

- qué dice;
- qué experimentos compra;
- cómo cambia su modelo ejecutable a lo largo del tiempo;
- qué decisiones toma;
- qué modelo entrega finalmente.

Una mala entrega no se llama automáticamente “terquedad”: primero se localiza dónde se rompió
la cadena.

## 4. Banco compacto de casos que los mundos deben poder reproducir

La tabla no sustituye el dossier detallado de `docs/vicios/`. Es el recordatorio de cobertura
que se consulta antes de diseñar o pivotear un mundo.

| Fenómeno | Caso que lo muestra | Estructura que debe conservar el mundo sintético |
|---|---|---|
| **Dato propio ignorado a mitad del trabajo** | Corral | El agente compra el dato, detecta una discrepancia y aun así entrega la estructura anterior |
| **Modelo que queda viejo durante una trayectoria larga** | KellyBench | Llegan resultados frescos normalmente; diagnostica sus pérdidas pero casi nunca reentrena ni cambia su acción |
| **Información intermedia tratada como fondo** | OSWorld 2.0 | Un dato relevante aparece dentro del flujo ordinario, no como anuncio de “evidencia importante” |
| **Ve lo correcto y vuelve a la primera idea** | RadLE | Los hallazgos intermedios contradicen el diagnóstico inicial, pero la conclusión lo restaura |
| **Evidencia mezclada leída selectivamente** | Xie et al. | Una contradicción limpia se incorpora; la misma tensión mezclada con confirmación produce rigidez |
| **Compromiso con la respuesta propia** | Kumaran et al. | El mismo contenido pesa distinto si el trabajo anterior se vive como propio o ajeno |
| **Sobre-generalización desde un caso chico** | WAGER `[PROPIO]` + `overgen_v0` | Una regla verdadera en un juguete o subdominio se promueve a ley general sin revisar indicios que limitan su alcance |
| **Generalizar sí era correcto** | `overgen_twin_v0` | El gemelo donde la ley realmente transfiere impide aprender “nunca generalices” |
| **Sabe qué debería hacer, pero hace otra cosa** | KellyBench / Pal / Investigator | Separar declaración, modelo vigente, búsqueda y decisión con consecuencias |
| **Persistencia racional** | Xie limpio / gemelos estables | La nueva información no justifica abandonar el modelo; pivotear por reflejo debe perder |
| **Mayor incertidumbre como respuesta correcta** | BeliefTrack/BASIL + mundos cerrados WAGER | Evidencia legítima descarta certeza sin seleccionar todavía una explicación única |

El ejemplo propio “un caso de KellyBench → rediseñemos todo como KellyBench” pertenece a la
misma familia de **alcance mal calibrado**. Es una advertencia de proceso, no evidencia sobre
agentes ni una razón para convertir KellyBench en el centro del proyecto.

## 5. Cómo reproducir los fenómenos con fidelidad

1. **La evidencia aparece como en el caso real.** Si en Corral fue un experimento propio y en
   KellyBench fueron resultados rutinarios, no se reemplaza por una pantalla que anuncia
   “llegó la corrección”.
2. **No se delata el momento importante.** Los checkpoints, si existen, ocurren con un ritmo
   regular idéntico entre brazos; no solamente alrededor del dato que nos interesa.
3. **Adquisición y asimilación se separan.** Una versión garantiza que el mismo dato llegue de
   forma natural para medir incorporación; otra permite que dependa del experimento elegido
   para medir la cadena completa.
4. **Los mundos vienen en pares o tríos.** Ante superficies similares debe existir un polo
   donde cambiar gana, otro donde mantener gana y, cuando corresponda, uno donde la respuesta
   correcta sea parcial o más incierta.
5. **El prefijo y el estado previo se igualan cuando se afirma causalidad.** Los forks parten
   del mismo trabajo y varían una condición. Comparar mundos o horizontes distintos habla de
   generalización, no identifica por sí solo una causa.
6. **La longitud es una perilla.** Ningún número fijo de rondas representa “trayectoria larga”.
7. **La dificultad operativa se controla.** Escribir código inválido, olvidar el protocolo o
   perder contexto no se confunde con juicio epistémico.
8. **Las estrategias reflejas deben perder.** Cambiar siempre, mantener siempre, ensanchar
   siempre y copiar la última señal deben fallar en algún gemelo certificado.

## 6. Cómo se mide sin leer la mente del agente

La creencia operacional es el **modelo predictivo ejecutable vigente**. Idealmente se conserva
una trayectoria `M0, M1, …, Mt`, no solamente un antes y un después. El registro puede modificar
la conducta, por lo que debe ser rutinario, constante entre brazos y declarado como parte del
protocolo estudiado.

Cada versión se compara con:

- la verdad oculta, para medir consecuencias;
- la actualización legal alcanzable con la información disponible;
- la versión anterior, para medir dirección y magnitud del cambio;
- las acciones y la entrega posterior, para medir propagación y persistencia.

Las métricas deben distinguir al menos:

- no actualización;
- subactualización;
- actualización proporcional;
- sobreactualización;
- movimiento en dirección incorrecta;
- aumento o reducción apropiados de incertidumbre;
- reversión posterior;
- modelo actualizado que no llega a la acción o entrega.

La fracción `F` de mejora capturada puede seguir como resumen secundario donde su denominador
esté bien resuelto. No reemplaza este diagnóstico por etapas.

## 7. Programa de mundos, no “el mundo definitivo”

Ningún escenario debe intentar representar todo. El programa necesita pocos mundos
complementarios y muchas instancias generables:

1. **Compuerta bilateral controlada:** verifica que el instrumento distingue cambiar,
   conservar y aumentar incertidumbre.
2. **Sobre-generalización + gemelo:** caso simple válido que puede o no transferir a un dominio
   amplio (`overgen_v0` / `overgen_twin_v0`).
3. **Dato propio a mitad del flujo:** una investigación produce evidencia sutil contra su propia
   hipótesis (estructura Corral).
4. **Trayectoria prolongada:** el modelo puede quedar obsoleto a lo largo de muchos resultados
   ordinarios (estructura KellyBench), sin convertir esa estructura en todo WAGER.
5. **Formación y cierre:** una creencia temprana puede curvar la búsqueda; una corrección tardía
   puede reconocerse pero no llegar a la entrega.
6. **Fricción estructural:** la misma fuerza de evidencia exige una corrección local o un pivote
   que invalida dependencias.

La fábrica dinámica es una contribución potencial importante: cada familia debe parametrizar
mecanismos, fuerza de evidencia, trayectoria y alcance del cambio para producir muchas
instancias certificadas. Primero se valida el fenómeno en pocos mundos; después se escala.

## 8. Qué sería un resultado científico importante

No alcanza con catalogar errores. Buscamos una regularidad compacta que sobreviva a modelos y
familias de mundos, por ejemplo:

> Con evidencia igualmente diagnóstica, la incorporación cae cuando la señal es poco visible
> y la corrección exige un pivote estructural sobre trabajo endógeno acumulado.

También sería importante descubrir que esa hipótesis es falsa: que solamente importa la
calidad de la señal, que la autoría no agrega nada, que diferentes modelos fallan en etapas
distintas o que no existe una teoría compacta entre mundos.

Los mundos sintéticos también pueden convertirse después en tareas de entrenamiento para
agentes, pero esa contribución es secundaria hasta demostrar que los instrumentos reproducen
fallas reales y no enseñan un reflejo superficial.

## 9. Guardia de alineación y anti-rabbit-hole

Antes de firmar un mundo, interpretar una corrida o pivotear el programa, responder:

1. ¿Qué caso real y qué fila de esta guía estamos reproduciendo?
2. ¿Cómo apareció realmente la evidencia: propia, rutinaria, externa, limpia o mezclada?
3. ¿Qué respuesta debería ser correcta y qué gemelo derrota el reflejo opuesto?
4. ¿Estamos midiendo búsqueda, atención, interpretación, asimilación o propagación?
5. ¿La fricción surge del trabajo que debe rehacerse o la inventamos como señal artificial?
6. ¿El horizonte reproduce el fenómeno o elegimos una cantidad cómoda de rondas?
7. ¿El resultado generaliza o estamos convirtiendo el último caso observado en todo el proyecto?
8. ¿Después de esta etapa conviene mantener, modificar o abandonar la hipótesis?

Una discrepancia entre mundos se interpreta primero como **falta de generalización**, no como
prueba automática de un eje nuevo. Una idea no queda protegida por el trabajo ya invertido.

## Síntesis final

WAGER busca medir la **calibración de la revisión aplicada** dentro de investigaciones reales o
sintéticas de trayectoria: cuándo el agente debe pivotear, corregir parcialmente, mantenerse o
dudar más; cómo influyen evidencia, trayectoria y alcance del cambio; y dónde se corta el camino
entre observar un dato y entregar un modelo que realmente lo incorporó.

La guía gobierna el programa. Los casos reales gobiernan los mundos. Los experimentos deciden
qué hipótesis sobrevive.
