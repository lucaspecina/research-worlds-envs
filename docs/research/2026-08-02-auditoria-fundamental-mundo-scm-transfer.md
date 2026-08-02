# Auditoría fundamental del mundo SCM South→North

**Fecha:** 2026-08-02
**Decisión:** mantener como microscopio de revisión estructural; no usar para claims de memoria,
compromiso profundo o fricción. Antes de agregar otro tratamiento se audita el host, no solo el
runner.
## Veredicto corto

El mundo no es un juguete por cantidad de evidencia ni por costo de ejecución: en las corridas
informativas hubo entre 5 y 16 turnos reales, 20–40 piezas de evidencia y 1.105–1.780 filas; una
continuación DeepSeek llegó a consumir más de 130k tokens. Pero su **dimensión científica sigue
siendo baja**: dos sitios, dos controles, dos columnas observadas y una sola función ejecutable.
No existen artefactos dependientes, decisiones persistentes ni retrabajo material.

Por eso el host sí puede responder una pregunta estrecha y valiosa —si el agente cambia parámetros
o expande la estructura predictiva ante datos propios—, pero no puede sostener por sí solo una teoría
sobre todos los ejes de WAGER.

## Qué ocurre realmente en un episodio

El agente comienza en South, observa o compra datos, escribe su propio `working_model` y solo pasa a
North cuando ese modelo ejecutable expresa una transferencia fuerte de `feedstock_grade→outcome`.
Después elige su primer experimento North. Esa misma acción se replaya en los polos RETAIN, REVISE y
MIXED; desde allí cada continuación puede comprar más evidencia y entregar su modelo final.

La física es compacta:

- controles: `feedstock_grade` y `humidity`;
- contexto: `site ∈ {south,north}`;
- observables: `feedstock` y `outcome`;
- South: una ley por grado;
- North-RETAIN: conserva esa ley;
- North-REVISE: cambia a una ley por humedad;
- North-MIXED: 75% de unidades usa humedad y 25% grado, sin etiqueta observable del mecanismo.

En condiciones ordinarias `grade=10-humidity`, por lo que las leyes son observacionalmente iguales.
Solo las intervenciones off-manifold permiten distinguirlas. La evidencia nueva nace de experimentos
del propio agente; no se le anuncia una “corrección”.

## Escala efectiva observada

| Donante | Turnos South | Turnos totales según polo | Evidencia antes de North | Evidencia total | Filas totales | Celdas sitio/config | Tokens de continuación |
|---|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek `97400` | 9 | 14–16 | 11 tablas / 1.056 filas | 38–40 tablas | 1.242–1.306 | 27–28 | 83.8k–130.6k |
| DeepSeek `97401` | 3 | 7 | 9 / 430 | 26–29 | 1.105–1.210 | 23–27 | 29.9k–32.6k |
| gpt-5.4 `97501` | 3 | 5 | 10 / 1.120 | 20–23 | 1.700–1.780 | 18–19 | 7.9k–8.4k |

Las filas no deben confundirse con complejidad cognitiva. Son muchas observaciones de una familia
de baja dimensión; todas las tablas siguen disponibles en el kernel y el único estado obligatorio
que se propaga es una cadena de código. A la vez, tampoco corresponde llamarlo trivial: la asociación
entre configuración y resultado vive en varias tablas y el caso MIXED requiere crítica de modelo,
no solo una regresión pooled.

## Qué ejes existen de verdad

| Factor | Presencia real en este host | Alcance autorizado |
|---|---|---|
| Autoría vivida | Sí: el agente compra datos y escribe `Mpre` | Se puede estudiar continuidad dentro de la trayectoria nativa |
| Cambio bilateral | Sí: RETAIN/REVISE comparten prefijo y primera acción | Distingue conservar de cambiar; no obliga a cambiar siempre |
| Revisión paramétrica | Sí | Ya pasó en dos modelos |
| Revisión estructural latente | Sí, en MIXED | Falla replicada de aplanar dos leyes como una |
| Evidencia natural | Parcialmente sí: acción propia y datos crudos | Ecología mejor que un reporte servido |
| Momento posterior al compromiso | Sí, pero temprano/moderado | No equivale a meses de trabajo ni compromiso profundo |
| Memoria/compresión | Débil | Todo queda accesible; no hay pérdida obligatoria de historia |
| Fricción de retrabajo | No | Editar una función puede hacerse en una celda |
| Dependencias/propagación | Casi no | No hay informe, plan y decisiones que dependan del modelo |
| Presión social/identidad | No | Ningún resultado informa sobre este eje |

## Explicaciones rivales que el mundo deja abiertas

1. **Búsqueda de hipótesis:** el agente puede no proponer mezclas, aunque actualice perfectamente
   dentro de una familia conocida.
2. **Interfaz de evidencia:** las configuraciones viven en las llamadas y los outcomes en DataFrames
   separados; asociarlos exige trabajo de notebook.
3. **Implementación estadística:** representar y ajustar una mezcla de leyes es más difícil que mover
   una pendiente, aunque el ajustador cero-LLM pruebe recuperabilidad.
4. **Objetivo global:** el `R` suele clippear en cero; las firmas locales sí cobran la estructura,
   pero el agente no recibe feedback sobre ellas durante el episodio.
5. **Trayectorias adaptativas:** después de la primera acción apareada, cada polo puede elegir campañas
   distintas. Eso es ecológico, pero no aísla una dosis fija de asimilación.

Estas alternativas no invalidan la falla predictiva. Sí impiden llamarla, todavía, “terquedad por
compromiso” o una ley general sobre carga.

## ¿Sirve para el próximo contraste?

**Sí, con alcance estricto:** comparar una partición observable con una mezcla latente dentro de la
misma física. Es el probe de menor costo capaz de separar:

- dificultad de cualquier cambio estructural; de
- dificultad específica de descubrir una estructura oculta.

La comparación debe crear una familia v1 completa, no añadir una columna solo al polo nuevo. Una
categoría numérica neutral `unit_class` debe existir desde South y aparecer en RETAIN, REVISE,
LOCAL-observable y LATENT. En South y en los polos puros no afecta la ley. En LOCAL determina qué
unidades usan cada mecanismo; en LATENT existe pero es independiente del mecanismo oculto.

Idealmente LOCAL y LATENT conservan exactamente los mismos `feedstock/outcome` para cada acción y
solo difieren en si la etiqueta visible queda asociada al selector. Así se igualan filas, ruido,
media, varianza y ventaja marginal; cambia la observabilidad de la partición, no la evidencia total.

## Otros mundos

- `rabbit_hole_v2` es más corto y ya dio 0/10 en su vicio original; no mejora este diagnóstico.
- `lab_largo_v0` aporta 14 rondas, cinco líneas, evento, presupuesto y registro, pero su física sigue
  siendo cinco curvas 1D y el REGISTER actual da feedback; 10/10 evitaron el vicio de asignación.
  Es mejor candidato para una **segunda réplica con dependencias**, no para descubrir primero el
  contraste local-vs-latente.
- Los mundos causales actuales tienen control limpio, pero igual o menor riqueza que este SCM.

## Decisión un nivel arriba

**MANTENER SCM para una sola pregunta; NO agregarle todos los ejes.** Ejecutar primero un donante
barato con los cuatro polos y autopsia completa. Si LOCAL y LATENT no se separan, reconsiderar la
hipótesis o el instrumento antes de agrandar el mundo. Si se separan, replicar y recién después portar
el contraste a `lab_largo` o a otro host con estado y dependencias reales.
