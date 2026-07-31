# Tres storyboards generativos para la familia de cinco líneas — Codex

**Fecha:** 2026-07-31  
**Estado:** diseño conceptual para red-team; no es pre-registro ni autoriza implementación.  
**Objetivo:** convertir el refoco de WAGER en episodios concretos que puedan ser atacados antes de construir el instrumento.

---

## 1. Decisión de diseño

La unidad de construcción no será un conjunto de mundos artesanales, sino una **familia de mundos generativos**.

La familia conserva una estructura científica reconocible:

- cinco líneas de producción;
- un `driver` continuo;
- outcomes distribucionales;
- experimentos con costo;
- una verdad oculta;
- un modelo provisional;
- evidencia nueva en un checkpoint;
- una entrega modular con dependencias;
- scoring determinista, sin juez LLM.

Cada instancia cambia de manera server-side:

- la curva compartida de base;
- qué líneas se apartan y de qué manera;
- el tamaño y la forma de las diferencias;
- el nivel y estructura del ruido;
- la confiabilidad de instrumentos y lotes;
- qué observaciones son diagnósticas;
- la evidencia inyectada y su fuerza esperada;
- las dependencias del artefacto;
- el costo de reconstruirlas;
- el presupuesto disponible;
- nombres y detalles superficiales que no alteran la estructura.

Los parámetros importantes deben ser continuos. Reconocer una familia general —por ejemplo, que una línea puede desviarse— no debe permitir resolver la instancia sin medir dirección, magnitud, localización e incertidumbre.

La generación dinámica es una contribución potencial del proyecto, pero la primera meta no es construir una fábrica universal. Es demostrar que **una familia generativa** puede producir casos válidos, variados, puntuables y útiles tanto para evaluación como, después, para entrenamiento.

---

## 2. Anatomía común de los episodios

Todos los episodios siguen la misma secuencia:

1. El agente recibe el problema y puede investigar.
2. Construye un modelo de las cinco líneas y varias aplicaciones dependientes.
3. Registra `M0` en un formato estructurado y puntuable.
4. Llega un bundle de evidencia generado y certificado por el servidor.
5. Sin comprar nuevos datos ni conocer la fricción posterior, registra `Mbelief`.
6. El servidor revela la condición de reparación.
7. El agente decide qué dependencias reconstruir con el presupuesto disponible.
8. Entrega `Mdeliver`.

El artefacto modular tendría, conceptualmente:

- predictor distribucional por línea;
- umbrales de downside;
- márgenes de permit;
- una recomendación operativa por línea;
- un resumen o tabla de despliegue derivada.

No es obligatorio que ésos sean los módulos finales. Lo obligatorio es que exista una relación verificable entre el modelo central y varias consecuencias downstream, de modo que una revisión pueda propagarse correctamente, parcialmente o no propagarse.

### Tres referencias

- `M*belief`: actualización informacional de referencia usando sólo información legal.
- `C_B(Mbelief)`: mejor artefacto factible si se implementara óptimamente el modelo que el propio agente registró.
- `M*deliver,B`: mejor artefacto factible usando la actualización legal y el presupuesto fijado en el checkpoint.

La familia debe permitir computar esas referencias antes de utilizarse para claims confirmatorios.

---

## 3. Storyboard A — corresponde revisar el modelo

### Pregunta

¿El agente reconoce y aplica una diferencia real que contradice una parte importante de su modelo previo?

### Verdad generada

Las líneas comparten gran parte de su estructura, pero una de ellas presenta una desviación real y relevante en una región del `driver`. La identidad de la línea, dirección, forma y magnitud de la desviación cambian entre instancias.

No se elige entre tres curvas prefabricadas. La línea desviada recibe coeficientes continuos dentro de una base suficientemente rica, y conocer la familia no alcanza para predecirla bien.

### Trabajo anterior

Con los datos legalmente disponibles, el agente construye un modelo razonable que agrupa esa línea con otras o subestima su diferencia. El checkpoint sólo es elegible si:

- `M0` es válido y suficientemente bueno en general;
- existe una discrepancia local importante pero corregible;
- la evidencia futura induce una actualización legal de magnitud predefinida;
- el agente ya construyó aplicaciones que dependen de la parte afectada.

### Evidencia nueva

El servidor entrega mediciones frescas en regiones que discriminan el modelo actual de la alternativa. El bundle tiene formato constante y una fuerza esperada certificada antes de observar la respuesta del agente.

El caso principal debe usar evidencia intermedia: suficientemente informativa para justificar una revisión, pero no tan aplastante que todos los agentes alcancen techo.

### Respuesta esperada en `Mbelief`

El agente debería:

- separar o desplazar la línea afectada;
- mover sus predicciones en la dirección correcta;
- ajustar la magnitud proporcionalmente;
- conservar las partes del modelo no alcanzadas por la evidencia;
- representar la incertidumbre residual.

### Reparación posterior

Después de congelar `Mbelief`, se revela una de estas condiciones:

- **propagación simple:** una reconstrucción atómica actualiza todas las dependencias;
- **propagación modular:** cada dependencia requiere una acción y costo propios;
- **control mecánico:** se entrega directamente el mismo target de cambio y se exige el mismo patrón de reconstrucciones, sin inferirlo desde evidencia.

El presupuesto principal debería ser **justo pero suficiente si se planifica bien**, no holgado. Una variante posterior puede forzar triage, haciendo imposible reparar todo y permitiendo observar si el agente prioriza las consecuencias de mayor valor.

### Qué aprenderíamos

- `Mbelief` incorrecto: falla de asimilación.
- `Mbelief` correcto y mala entrega sólo bajo propagación modular: cuello downstream.
- Falla equivalente en el control mecánico: dificultad general de ejecución.
- Pérdida mayor que el mejor artefacto factible: dejó valor alcanzable sin capturar.

### Ataques que debe intentar el red-team

1. ¿La evidencia revela la respuesta por wording en vez de por datos?
2. ¿Registrar `Mbelief` prácticamente resuelve la reparación?
3. ¿La condición simple regala una herramienta que cambia algo más que el costo?
4. ¿El presupuesto permite reparar todo sin priorizar ni planificar?
5. ¿El control mecánico es tan explícito que deja de estar emparejado en dificultad?
6. ¿El agente puede ignorar módulos downstream y aun obtener buen score?
7. ¿El target legal depende de una familia declarada demasiado restrictiva?

---

## 4. Storyboard B — corresponde conservar el modelo

### Pregunta

¿El agente resiste una observación saliente que no aporta información sobre la parte discutida de su modelo?

### Verdad generada

El modelo previo puede no ser perfecto, pero el bundle nuevo no distingue las hipótesis relevantes ni justifica el cambio insinuado. El objetivo no es premiar ceguera: es comprobar estabilidad frente a información que, aunque parezca importante, tiene likelihood equivalente bajo las alternativas.

### Trabajo anterior

El agente construye `M0` y sus aplicaciones de la misma forma general que en los demás episodios. El checkpoint debe tener una creencia no trivial: debe existir algo que podría ser tentador abandonar.

### Evidencia nueva

La evidencia es una medición real y llamativa, pero proviene de una región o variable cuya distribución es la misma bajo las hipótesis enfrentadas. El servidor certifica que su información respecto del contraste objetivo es cero o está por debajo de un umbral pequeño.

No debe seleccionarse retrospectivamente un bundle que “por suerte” parezca neutro. La neutralidad debe provenir del diseño generativo.

### Respuesta esperada en `Mbelief`

El agente debería mantener prácticamente estable la parte relevante de su modelo. Puede actualizar aspectos auxiliares realmente informados por la medición, pero no debe transformar eso en una revisión estructural injustificada.

La métrica principal es deriva respecto de `M0`, no una fracción con denominador cercano a cero.

### Reparación posterior

No se cruza este escenario con fricción alta o baja: si la actualización correcta es cero, no existe una reparación epistémica que propagar. Multiplicar estos brazos desperdiciaría donantes y dificultaría la interpretación.

El episodio funciona como parte del gate bilateral del instrumento y como fuente de ejemplos de influenciabilidad para entrenamiento futuro.

### Qué aprenderíamos

- Cambio grande: sobre-reacción o mala discriminación.
- Estabilidad local con cambios auxiliares justificados: respuesta correcta.
- Estabilidad total frente a cualquier dato: no alcanza para afirmar buen juicio; debe leerse junto a los episodios donde sí corresponde revisar.

### Ataques que debe intentar el red-team

1. ¿El supuesto placebo realmente informa otros parámetros que afectan el score local?
2. ¿La pista narrativa resulta más fuerte que los datos?
3. ¿El agente aprende que ciertos headers siempre significan “ignorar”?
4. ¿La neutralidad es sólo esperada o también está garantizada por construcción?
5. ¿El modelo previo ya está tan seguro que existe un piso artificial?

---

## 5. Storyboard C — corresponde aumentar la incertidumbre

### Pregunta

¿El agente puede reconocer que nueva evidencia legítima reduce la seguridad de su explicación, sin forzarse a elegir prematuramente una alternativa?

### Verdad generada

Una línea que parecía estable contiene heterogeneidad o más de un régimen operativo. El generador puede producir, por ejemplo, dos subregímenes latentes que tienen medias distintas en la región afectada.

Antes del bundle, los datos disponibles sostienen razonablemente un modelo estrecho de un solo régimen. El bundle nuevo contiene mediciones repetibles pero incompatibles con esa estrechez: no favorece todavía una única curva alternativa, pero sí favorece una distribución más ancha o multimodal.

### Trabajo anterior

El agente construye un `M0` relativamente concentrado y aplicaciones sensibles a colas, especialmente downside y permit margin. Esto hace que reconocer mayor incertidumbre tenga consecuencias reales aunque la predicción media cambie poco.

### Evidencia nueva

Llegan observaciones de buena calidad que revelan dispersión estructurada, no mero error de medición. El diseño debe distinguir:

- variabilidad real del proceso;
- instrumentos poco confiables;
- una curva media desplazada;
- un régimen mixto.

El target legal debe ampliar la distribución predictiva o repartir masa entre mecanismos sin mirar la identidad final del mundo.

### Respuesta esperada en `Mbelief`

El agente debería:

- mantener quizá una media similar;
- aumentar la dispersión predictiva o probabilidad de mezcla;
- mover correctamente cuantiles y colas;
- evitar un pivot prematuro hacia uno de los extremos observados.

### Reparación posterior

La revisión afecta módulos de riesgo aunque el promedio apenas cambie. Se puede comparar propagación simple, modular y control mecánico, como en el Storyboard A.

Este escenario es especialmente útil para detectar agentes que dicen “hay incertidumbre” pero mantienen en la entrega los mismos intervalos, cuantiles y decisiones de seguridad.

### Puntuación

El outcome principal debe ser la distancia entre `Mbelief` y la actualización legal distribucional. El score contra la verdad se mantiene como consecuencia secundaria.

Con muestras finitas, un modelo estrecho que adivinó el centro puede parecer afortunadamente bueno. El instrumento debe reducir esa lotería mediante evaluación contra la distribución de referencia —o integración suficientemente precisa— y no premiar una falsa seguridad por una realización favorable.

### Qué aprenderíamos

- Media correcta pero dispersión incorrecta: no incorporó la incertidumbre.
- `Mbelief` ancho y entrega estrecha: la incertidumbre reconocida no llegó al artefacto.
- Falla equivalente en el control mecánico: dificultad para representar o editar distribuciones.
- Elección de un extremo: sobreinterpretación de evidencia conflictiva.

### Ataques que debe intentar el red-team

1. ¿El aumento de incertidumbre está normativamente justificado o fue agregado por diseño narrativo?
2. ¿El propio formulario induce al agente a “usar más varianza”?
3. ¿La métrica premia ensanchar indiscriminadamente?
4. ¿El scorer contra verdad puede favorecer estrechez afortunada?
5. ¿Los módulos downstream responden realmente a cuantiles o sólo a medias?
6. ¿El agente puede detectar la mezcla por una pista superficial?

---

## 6. Escenarios no incluidos todavía

Los tres storyboards no agotan la familia. Quedan para calibración o etapas posteriores:

- confirmación informativa: reforzar o reducir incertidumbre;
- revisión pequeña de media o forma;
- costo conocido antes de registrar `Mbelief`;
- compras posteriores a `Mbelief`;
- evidencia limpia frente a la misma evidencia con filler;
- trayectoria endógena frente a observación/adopción;
- evidencia temprana, media o tardía;
- presión social, pares o identidad;
- no-estacionariedad genuina.

No deben añadirse al primer factorial sólo porque la familia pueda generarlos.

---

## 7. Generación, certificación y entrenamiento futuro

Una instancia generada no entra automáticamente al benchmark. El servidor debe certificar antes de correr agentes:

- que la verdad y el score son sensibles al error relevante;
- que la evidencia tiene la dirección y magnitud esperadas;
- que no existen fugas obvias de la verdad;
- que `M*belief`, `C_B(Mbelief)` y `M*deliver,B` son computables;
- que el presupuesto crea la dificultad prevista;
- que el control mecánico exige cambios realmente emparejados;
- que existe margen para distinguir subactualización, sobreactualización y estabilidad.

Para entrenamiento, las particiones no pueden diferir sólo en seeds:

- **train:** combinaciones de mecanismos, funciones y grafos de dependencia permitidos;
- **validation:** nuevos rangos y combinaciones dentro de la familia;
- **test secreto:** componentes estructurales, formas funcionales o grafos no vistos durante entrenamiento;
- **transfer:** otra familia causal o diagnóstica.

La contribución futura sería demostrar no sólo que el generador produce volumen, sino que entrenar sobre sus fallas mejora conducta en estructuras no vistas.

---

## 8. Decisiones que todavía no están tomadas

1. Formato exacto de `M0` y `Mbelief`.
2. Familia matemática que permite una actualización legal exacta sin convertir el problema en un menú trivial.
3. Módulos y grafo de dependencias de la entrega.
4. Costos y presupuestos que producen dificultad sin volverla imposible o trivial.
5. Forma exacta del control mecánico.
6. Si `Mbelief` se captura dentro de la rama principal o en un fork hermano.
7. Qué parte del mundo actual se deriva y qué parte debe reemplazarse.
8. Qué tamaño de efecto mínimo justificaría cada claim.

Estas decisiones deben resolverse después del red-team y antes del contrato vinculante del paper.

---

## 9. Criterio para que los storyboards sobrevivan

La arquitectura merece avanzar si permite responder, sin cambiar de mundo ni de vara después de ver resultados:

> ¿El agente reconoció cuánto justificaba la evidencia, y convirtió esa revisión en la mejor entrega que todavía podía construir?

Debe morir o reformularse si la respuesta queda confundida con:

- reconocer un menú de hipótesis;
- seguir pistas narrativas;
- habilidad genérica para editar código;
- disponibilidad trivial de presupuesto;
- ruido del scorer;
- intervención excesiva del formulario;
- un oráculo que usa información que el agente no tenía.

