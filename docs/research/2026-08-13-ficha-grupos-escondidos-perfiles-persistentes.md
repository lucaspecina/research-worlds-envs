# Ficha de descubrimiento — Grupos escondidos: perfiles persistentes

**Fecha:** 2026-08-13  
**Estado:** confirmación `gpt-5.4 × mundo × n=10` completa; falta réplica con otra familia de
modelo antes de hablar de agentes en general.

## Qué salto buscamos

Pasar de una población aparente a unos pocos tipos ocultos que conservan un perfil propio a
través de varias pruebas. Cuenta por el comportamiento del modelo ejecutable: debe producir las
familias persistentes y mejorar la predicción. No se exige que el agente use palabras particulares.

## Qué sabemos antes de correr

- Cada prueba aislada parece una sola población.
- Los perfiles completos sí contienen dos familias fuertes.
- El mejor rival certificado de una sola banda obtiene `S=0.464`; un ajuste de dos perfiles con
  400 filas obtiene `S=0.924–0.997` en cinco muestras.
- La nota de producción todavía es ruidosa: el solver de dos perfiles quedó entre `R=0.758–0.955`
  y falló una compuerta congelada de `R>=0.80`. Por eso esta corrida no valida el mundo.
- Un remuestreador de perfiles alcanza alrededor de `R=0.80`. Como preserva funcionalmente las
  familias, puede contar como realización conductual; la traza distinguirá si hubo investigación
  estructural o mera memoria empírica.

## Primera partida real congelada

- **Condición:** idea nombrada, solución no regalada.
- **Agente:** `gpt-5.4`.
- **Semilla privada quemada:** `99810`.
- **Ayuda exacta:** “Considerá la posibilidad de que los perfiles completos provengan de unos
  pocos tipos ocultos que se mantienen a través de las doce pruebas. Investigá esa idea con los
  datos antes de decidir cómo modelar.”

Esta partida pregunta solamente si el agente puede investigar e implementar la idea con la
información disponible. Cualquier resultado decide **MANTENER / MODIFICAR / PIVOTEAR / ABANDONAR**
antes de otra variante. No autoriza afirmaciones sobre descubrimiento espontáneo.

## Resultado de la idea nombrada y decisión

`gpt-5.4 / 99810` entregó en cuatro turnos, gastó 200/500 y obtuvo `R=0.803`. Compró los 400
perfiles, comparó mezclas de 1 a 6 componentes por BIC, encontró una ventaja decisiva para dos,
verificó asignaciones prácticamente inequívocas y entregó una mezcla gaussiana de dos perfiles.

**Decisión tras la corrida: MANTENER el núcleo.** La resolubilidad con la idea nombrada queda
demostrada para este modelo, mundo y episodio. La inestabilidad de la nota sigue abierta y limita
el alcance; no invalida la evidencia conductual de que el salto pudo implementarse.

## Segunda partida exploratoria congelada antes de correr

- **Condición:** sin ayuda; brief neutral solamente.
- **Agente:** `gpt-5.4`.
- **Semilla privada quemada al iniciar:** `99811`.
- **Ayuda:** ninguna.

Pregunta: ¿descubre y realiza espontáneamente la bifurcación funcional? Un episodio decide solo el
rumbo del slice; no estima una tasa ni autoriza un titular general.

## Resultado sin ayuda y autopsia

`gpt-5.4 / 99811` entregó en cuatro turnos, gastó 150/500 y obtuvo `R=0` (`R` sin recorte
`-1.595`). Compró 300 perfiles, analizó marginales, correlaciones y componentes principales,
interpretó las dos grandes direcciones como factores gaussianos continuos y entregó una sola
Gaussiana multivariada. No ajustó ni comparó ninguna partición de la población.

La auditoría mecánica sobre **los mismos 300 perfiles que vio** descarta falta de evidencia: una
mezcla de dos Gaussianas supera a una por `Delta BIC=149.30`, recupera pesos `0.497/0.503` y asigna
cada perfil con probabilidad posterior media mayor a `0.99999999999`. El agente había anunciado
que usaría un modelo rico si encontraba multimodalidad, pero no ejecutó ese test.

**Decisión tras la corrida: MANTENER.** En este slice y estas dos partidas, la idea nombrada cambia
el candidato disponible; con ella el agente lo verifica y lo implementa, sin ella la evidencia
alcanzaba pero el candidato no entró al menú. Es una señal exploratoria limpia de falla en
generación/testeo del candidato, no una tasa ni una confirmación.

## Control decisivo siguiente — mismo archivo, idea disponible o no

Se correrá un único par exploratorio adicional con `gpt-5.4`. Ambas ramas usan el mismo
`seed_offset=99820` y un archivo finito: comprar `300+100` o `400` revela prefijos de la misma tabla,
no muestras nuevas. Una rama recibe el brief neutral; la otra agrega exactamente la ayuda ya
congelada. Cada rama quema su identidad por separado y se ejecuta una sola vez.

La medida estructural, congelada antes del par, es `S_profile`: compara la distribución generada
del contraste coherente con la verdad, con `0` en la mejor banda Gaussiana y `1` en la verdad. El
modelo cruza la frontera del salto si `S_profile >= 0.5`. La nota `R` completa queda como secundaria
porque su inestabilidad ya está documentada.

Lectura predeclarada:

- ayuda cruza y neutral no: fortalece resolubilidad + falla de generación espontánea;
- ambos cruzan: el salto aparece espontáneamente y el anfitrión puede ser demasiado fácil;
- ninguno cruza: el rescate por idea no replica y el anfitrión es frágil;
- neutral cruza y ayuda no: variación de ejecución domina; no se atribuye efecto a la idea.

Después de este par se vuelve un nivel arriba. No se encadenan más formulaciones de pistas.

## Resultado del control apareado

Las dos ramas compraron las mismas 400 filas, verificadas byte a byte por el hash
`21fc347e...ce52`.

- **Sin ayuda:** factor Gaussiano continuo; `R=0`, `S_profile=0`.
- **Idea nombrada:** buscó mezclas, pero una mezcla diagonal sobre dos componentes principales
  confundió el nivel continuo con tipos discretos, eligió cuatro grupos y obtuvo `R=0`,
  `S_profile=0`.

La auditoría sobre esas mismas filas muestra que el diseño era resoluble: una mezcla completa en
12 dimensiones elige dos grupos (`BIC 10026` frente a `10405` para uno y `10419` para tres); con
covarianza compartida la ventaja es aún mayor. El fracaso ayudado fue una comparación demasiado
restrictiva, no ausencia de la firma.

La ayuda queda entonces 1/2: produjo un modelo estructural correcto en `99810` y uno incorrecto en
`99820`. Se autoriza una única partida de desempate con **la misma frase**, no una pista nueva:
`gpt-5.4 / 99821`. Esta excepción al límite de controles está ligada directamente al claim de
resolubilidad: decide `2/3 = continuar` o `1/3 = modificar antes de más partidas sin ayuda`.

## Resultado del desempate y cierre de validación

`gpt-5.4 / 99821` comparó mezclas completas de 1 a 8 grupos, eligió dos, verificó pesos
`0.502/0.498` en el archivo y `20/20` en una muestra fresca, y entregó la mezcla. Obtuvo
`R=0.900` y `S_profile=0.998`.

La prueba de resolubilidad cierra **2/3**: `S_profile = 0.964 / 0 / 0.998`. El fracaso intermedio
queda como dato, no se borra: nombrar la idea la vuelve disponible, pero no garantiza deducir ni
implementar su forma correcta. No se prueban más ayudas en esta etapa.

## Tanda principal congelada — sin ayuda

- **Modelo:** `gpt-5.4`.
- **Mundo/tarea:** exactamente los artefactos vigentes de `hidden_profiles_v0`.
- **Condición:** brief neutral, sin nota adicional.
- **n:** 10 partidas frescas, seeds privadas `99830–99839`.
- **Primario:** cruza el salto si `S_profile >= 0.5`, computado sin LLM sobre el programa entregado.
- **Secundarios:** `R`, compras, candidatos comparados y tipo de entrega.
- **No entran:** los dos negativos exploratorios `99811/99820`.

Lectura predeclarada para decidir rumbo, no para inflar alcance:

- `0–2/10`: la falla espontánea reaparece en este modelo×mundo; siguiente paso es otra familia de
  modelo o anfitrión, no afinar este mundo;
- `3–7/10`: conducta mixta; autopsiar las rutas y pasar a una réplica externa sin tuning local;
- `8–10/10`: el anfitrión es fácil para `gpt-5.4`; conservarlo como control y buscar otro más difícil.

Todo titular dirá `gpt-5.4 × Perfiles persistentes × n=10`. El gemelo y otros modelos quedan
fuera de esta tanda.

## Resultado de la tanda principal

Las diez partidas terminaron y entregaron código válido, sin reintentos. Según la medida primaria
congelada, **1/10 cruzó la frontera funcional del salto**:

| Partida | Modelo entregado | `S_profile` | ¿cruza? |
|---|---|---:|---|
| 01–03 | una Gaussiana conjunta | 0 | no |
| 04 | remuestreo de los 400 perfiles completos | 0.942 | sí |
| 05–10 | una Gaussiana conjunta | 0 | no |

La única entrega que cruzó no construyó una explicación de dos tipos. Conservó las dos familias
copiando la distribución empírica completa. Esto **cuenta como éxito funcional**, tal como estaba
declarado antes de correr: su programa produce la geometría correcta y no la rellena con perfiles
intermedios. Pero se informa por separado que **0/10 entregó el modelo simple de dos tipos**.

Los otros nueve vieron las fuertes dependencias y las resumieron como dos factores continuos dentro
de una sola nube Gaussiana. Ocho no ajustaron una partición de la población. Uno hizo un corte de
dos grupos con `k`-means, lo interpretó como un corte artificial sobre una dirección continua y lo
descartó sin comparar el modelo de dos perfiles que resolvía la tarea.

## Control decisivo sobre lo que cada agente podía ver

La auditoría cero-LLM se repitió sobre las **400 filas exactas de cada partida**, no sobre la verdad
abstracta ni sobre otra muestra. En las diez:

- dos perfiles superan a una Gaussiana conjunta por `Delta BIC=705–795`;
- el ajuste legal de dos perfiles obtiene `S_profile=0.943–0.999`;
- la asignación media de cada fila a uno de los dos perfiles es prácticamente 100% segura.

Por lo tanto, los nueve negativos no se explican por una instancia sin señal ni por falta de datos.
La falla dominante está entre **notar dependencia** e **interpretar/probar una población partida**.
El analizador reproducible es `scripts/analyze_hidden_profiles_discovery.py` y los crudos viven en
`scripts/out/hidden_profiles_discovery/confirmacion_sin_ayuda_*`.

## Lectura y decisión

**Resultado con alcance:** `gpt-5.4 × Perfiles persistentes × n=10`: 1/10 preserva
espontáneamente la bifurcación funcional y 0/10 construye la explicación compacta de dos tipos;
con la idea nombrada, el mismo modelo había construido correctamente dos tipos en 2/3 partidas.

**Decisión: MANTENER el hallazgo y cerrar el ajuste local de este anfitrión.** Cayó en el rango
predeclarado `0–2/10`: la falla espontánea reaparece aun cuando el salto mejora mucho y cada
partida contiene evidencia suficiente. No se prueban más frases ni pequeños retoques aquí. El
próximo nivel es una réplica con otra familia de modelo o un segundo anfitrión del mismo salto.

Una etiqueta de metadatos en los recibos quedó vieja (`exploratory resolvability slice`) también
para estas diez condiciones. No cambia condición, seeds, código ni pre-registro; se corrige en el
runner para no repetir la ambigüedad.

## Réplica externa congelada — DeepSeek-V3.2

Para separar un resultado de `gpt-5.4` de una propiedad del anfitrión, se cambia **solo el modelo**.
Mundo, tarea, presupuesto, ayuda y medidas quedan idénticos.

Primero se ejecutan tres partidas con la misma idea nombrada, seeds `99840–99842`. La compuerta es
al menos 2/3 entregas válidas con `S_profile>=0.5`. Si falla, no se ejecuta la tanda sin ayuda:
un negativo de descubrimiento no sería interpretable para un modelo que no demostró capacidad.
Una caída de API, harness o infraestructura pausa la réplica y no entra al denominador; no se
reemplaza sin dejar una enmienda previa. Una entrega inválida, `max_turns` o error de código causado
por el agente sí cuenta como no-cruce: también es parte de su capacidad para resolver la tarea.

Si pasa, se ejecutan diez partidas sin ayuda, seeds `99843–99852`. El primario vuelve a ser el
cruce funcional `S_profile>=0.5`; se informa aparte cuántas construyen un modelo compacto de dos
tipos. No se cambia la frase, no se agregan ejemplos y no se ajusta el mundo entre ambas etapas.
Todo titular dirá `DeepSeek-V3.2 × Perfiles persistentes × n`.
