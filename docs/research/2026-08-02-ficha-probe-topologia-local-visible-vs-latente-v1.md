# Ficha exploratoria congelada — revisión local visible vs estructura latente v1

**Fecha:** 2026-08-02
**Estado:** diseño exploratorio congelado; no es un pre-registro confirmatorio ni estima
prevalencia. La familia v1 y sus compuertas cero-LLM ya fueron construidas. **Enmienda visible
pre-rama tras el piloto `98300`:** el donante llegó hasta el gate de `Mpre`, pero el corredor se
detuvo antes de abrir cualquiera de las cuatro ramas por un gate A/B demasiado estricto. No se vio
ningún resultado de tratamiento. La corrección de abajo se hizo contra esa causa mecánica, no contra
un efecto observado; el prefijo, la acción congelada y la semilla `98300` se preservan.
**Auditoría del host:** `docs/research/2026-08-02-auditoria-fundamental-mundo-scm-transfer.md`.

**Ejecución posterior:** el donante `98300` fue reanudado después de la enmienda y completó las
cuatro ramas con todas las compuertas en verde. El resultado se documenta, sin modificar esta
lectura previa, en
`docs/research/2026-08-02-resultado-probe-topologia-local-visible-vs-latente-v1.md`.

## Enmienda pre-rama tras `98300`

La pregunta identificable no es si el agente **menciona por primera vez** A/B ni si su código ya
contiene una rama textual por clase. `batch_class` existe desde South y un modelo puede incluirla
por precaución, o absorber pequeños offsets muestrales, sin haber localizado un mecanismo nuevo.
El estimando correcto es conductual:

> ¿La evidencia North hace aparecer una **localización mecánica por clase** —respuestas distintas
> de `outcome` ante cambios de `feedstock_grade` y `humidity`— donde el modelo previo trataba esas
> respuestas como equivalentes?

Por eso, el gate previo A/B deja de exigir igualdad de niveles o de código. Se permiten offsets
pequeños entre A y B en South si se cumplen simultáneamente:

- `ΔG` es equivalente entre clases;
- `ΔH` es equivalente entre clases;
- la forma de la distribución, después de centrar cada clase, es equivalente.

Todas estas comparaciones usan **common random numbers (CRN)**: mismo código, mismos regímenes,
mismos seeds y draws apareados entre A/B. La equivalencia se decide con la tolerancia instrumental
predeclarada del corredor (la vara de bases dobles de la casa), no mirando el tratamiento. Un offset
de nivel por sí solo no excluye al donante; una diferencia material de respuesta o de forma sí.

El intento `98300` fue detenido exclusivamente por la antigua regla de igualdad A/B, antes de
RETAIN/REVISE/LOCAL/LATENT. Por lo tanto no se quema ni se reemplaza: se conserva el mismo donante y
se continúa desde el snapshot congelado, sujeto al gate mecánico corregido. Cualquier replay previo
a las ramas debe ser exacto y no puede sumar evidencia.

## Pregunta

En el SCM South→North los agentes frontier ya conservaron una ley correcta y cambiaron una ley
global incorrecta, pero aplanaron dos mecanismos latentes en 4/4 forks. Este probe pregunta qué
explica esa separación:

> ¿El agente puede expandir su modelo cuando la partición relevante es observable, y falla solo
> cuando debe descubrirla; o falla ante cualquier revisión estructural aunque la división esté a la
> vista?

No se interpretará el resultado como una escala psicológica única de “distancia”. Agregar una rama
observable e inferir mecanismos latentes son operaciones cualitativamente distintas.

## Familia de cuatro polos

Se crean casos v1 nuevos; los v0 y sus raws no se modifican. Todos comparten brief, controles,
presupuesto, batería y una columna de **vista** `batch_class ∈ {A,B}` presente desde South. La entrega
sigue siendo `model(regime,n,seed) → DataFrame(['feedstock','outcome'])`; para evaluación, el contexto
puede fijar `batch_class`. La clasificación es logística y rutinaria; el brief no afirma que afecte
el mecanismo.

| Polo | Verdad North | Revisión correcta |
|---|---|---|
| RETAIN | A y B usan grado | conservar |
| REVISE | A y B usan humedad | cambiar mecanismo global |
| LOCAL | A usa humedad; B usa grado | agregar una rama observable |
| LATENT | 75% humedad / 25% grado, independiente de A/B | descubrir y representar mezcla latente |

South usa grado para todos y `batch_class` es irrelevante en los cuatro polos. Prevalencia A/B =
75/25, igual al peso marginal de mecanismos en LOCAL y LATENT.

## Igualación LOCAL–LATENT

El generador usa un selector de mecanismo común `z` y una etiqueta visible:

- LOCAL reporta `batch_class=z`;
- LATENT genera los mismos `feedstock/outcome` con el mismo `z`, pero reporta una permutación
  determinística e independiente de las etiquetas, conservando exactamente sus conteos;
- cuando `regime.context['batch_class']` está fijado, LOCAL fija también el mecanismo y LATENT
  mantiene el selector independiente; en ambos polos todas las filas devueltas deben llevar la
  clase solicitada, porque la semántica pública del contexto no cambia entre mundos.

Así, para cada experimento ordinario apareado, LOCAL y LATENT deben tener `feedstock/outcome`
byte-idénticos y la misma cantidad A/B. Solo cambia si la etiqueta permite localizar la ley. No se
exige igualdad del DataFrame completo porque esa columna es el tratamiento.

## Trayectoria

Se reutiliza el corredor vivido South→North:

1. el mismo agente investiga South y escribe un `Mpre` ejecutable;
2. se habilita North de forma neutral;
3. el primer experimento North elegido por el agente se congela y replaya en los cuatro polos;
4. cada rama continúa de forma nativa, puede comprar evidencia y finalmente entrega;
5. se guardan `Mpre`, primer modelo posterior y entrega, más todo el ledger y las acciones.

La unidad es el donante, no cada rama. Seed exploratorio inicial: `98300`, modelo
`DeepSeek-V3.2`. Semillas de esta sonda se queman y no entran en una confirmación posterior.

## Compuertas cero-LLM antes de correr

1. South, prompts, costos, presupuesto y superficie agente-facing son iguales en los cuatro polos.
2. `batch_class` aparece desde la primera evidencia South y su distribución es idéntica.
3. South es byte-idéntico en todas las columnas visibles. En condiciones North no diagnósticas,
   `feedstock/outcome` son byte-idénticos y los conteos A/B coinciden; no se exige igualdad de la
   etiqueta fila por fila porque su asociación con el mecanismo es precisamente el tratamiento.
4. En North off-manifold, LOCAL y LATENT tienen `feedstock/outcome` byte-idénticos y conteos A/B
   idénticos; la asociación clase↔mecanismo es fuerte en LOCAL y nula dentro de tolerancia en LATENT.
5. Verdad por clase: RETAIN `ΔG_A≈ΔG_B≈8`; REVISE `≈0/0`; LOCAL `≈0/8`; LATENT `≈2/2`.
6. La batería pesa A y B explícitamente, sin permitir que la minoría desaparezca en el promedio.
7. El modelo previo tiene margen material y comparable para mejorar en LOCAL/LATENT. Su conducta
   mecánica previa debe ser equivalente para A y B bajo CRN: `ΔG`, `ΔH` y forma centrada equivalentes.
   Pequeños offsets South son admisibles y una rama textual A/B no constituye por sí misma una
   localización. Si antes de North ya difieren materialmente las respuestas o la forma, el donante
   no identifica la aparición de una nueva localización.
8. Sobre exactamente las filas del protocolo, un ajustador cero-LLM selecciona la partición A/B en
   LOCAL y dos leyes latentes en LATENT por BIC y CV; un modelo que ignora A/B pierde en LOCAL.
9. Robots `siempre conservar`, `siempre cambiar`, `siempre dividir por A/B` y `siempre mezclar`
   pierden en al menos un polo.

Si 1–7 no pasan, no se abren ramas. El control de recuperabilidad 8 se ejecuta sobre las filas
reales de cada campaña antes de interpretar comportamiento; si no hay cobertura suficiente por
clase/celda, la rama se declara no informativa sin aumentar datos post hoc.

La recuperabilidad real usa selección de folds **automática, target-blind y congelada**: intenta
`k=5,4,3,2` y toma el mayor `k` que los conteos `configuración × clase` y el rango de las matrices de
entrenamiento permiten. Esta decisión usa solo requests, etiquetas y conteos, nunca outcomes, el
nombre del polo ni cuál estructura debería ganar. Con `k<2`, BIC/CV en desacuerdo o diseño afín sin
rango suficiente, el resultado es `informative=false`. Recién después se compara el ganador
BIC+CV con LOCAL o LATENT. El certificado sintético mantiene `k=5` fijo porque su protocolo
predeclarado (cuatro celdas, 60 filas por celda) lo soporta holgadamente; no se usa para elegir el
`k` de una rama real.

## Métricas y lectura previa

Primarias, siempre por clase y en regiones North diagnósticas:

- `ΔG_A`, `ΔG_B` y error distribucional;
- fracción de mejora legal capturada por clase;
- captura de la separación A/B en LOCAL;
- firma de mezcla orientada y captura estructural en LATENT;
- daño a South;
- modelo, acciones y entrega. El `R` global es secundario.

Lecturas predeclaradas:

- LOCAL pasa y LATENT falla → cuello de descubrimiento, estimación o representación de estructura
  latente frente a una partición observable; esta sonda no separa esos tres subprocesos;
- LOCAL y LATENT fallan → barrera más general de revisión estructural o implementación;
- ambos pasan → el 4/4 anterior era específico de la instancia/interfaz;
- controles puros fallan → instrumento/familia v1 inválidos; no interpretar topología.

## Secuencia de gasto

1. construir mundos, batería, robots, certificado y análisis; cero LLM;
2. certificar física y emparejamiento;
3. correr un único donante DeepSeek `98300` con cuatro polos;
4. autopsia completa antes de cualquier réplica;
5. gpt-5.4 y segundo donante solo si el instrumento pasa y el contraste es interpretable.

No se agregan memoria larga, fricción, planes ni artefactos dependientes en este probe. Esos ejes no
existen en este host y requerirán una segunda familia si la separación estructural sobrevive.
