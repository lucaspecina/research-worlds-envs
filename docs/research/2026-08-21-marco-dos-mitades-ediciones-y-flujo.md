# El marco de las dos mitades: EDICIONES × FLUJO — el enunciado maestro (Lucas + Claude, 2026-08-21)

> **Qué es este doc**: la formulación del marco teórico tal como la entendemos hoy, armada en
> conversación (la propuesta de Lucas + tres ajustes discutidos y aceptados). Escrita para
> re-leerse y para que cualquiera la entienda fácil. Es la referencia canónica del enunciado;
> las wikis apuntan acá. Decisión asociada: ADR 0187.

## La separación central (la propuesta de Lucas)

Un descubrimiento tiene DOS mitades que veníamos mezclando:

1. **LA MODIFICACIÓN** (el objeto): qué edición se le hizo al modelo — el salto propiamente
   dicho. De esto hay TIPOS (postular una entidad, partir una población en dos, cambiar de
   régimen…): nuestra taxonomía de 11.
2. **EL FLUJO** (el proceso): todo lo que rodea y produce esa edición — darse cuenta de que
   hace falta un cambio (o no darse cuenta), decidir qué mirar y qué hacer, la generación del
   candidato (el "aha"), probarlo, elegirlo, implementarlo, sostenerlo.

**Los saltos no viven aislados ni son una sola cosa**: son ediciones de la forma del modelo
actual, y el fenómeno que estudiamos es el FLUJO que las produce (o las mata).

## Los tres ajustes (la crítica que afinó la propuesta)

**Ajuste 1 — al generalizar, no disolver LA distinción.** No todo cambio de modelo es un
salto. La piedra fundacional sigue: **refinar** (mover los números dentro de la misma forma)
vs **saltar** (cambiar la forma). Y la definición precisa es RELACIONAL (Boden, Magnani): *un
salto no es un tipo de edición — es una edición relativa al espacio de búsqueda del que
busca*. La misma edición es salto para un agente y consulta de memoria para otro. Dos
consecuencias directas: el test de contaminación es constitutivo del claim de creatividad, y
**los tipos son secundarios por construcción** — lo que hace salto a un salto no es su tipo,
es su relación con el repertorio del agente.

**Ajuste 2 — "creatividad": elegimos el sentido estricto, con razón empírica.** El campo está
partido: la vista estrecha (Ohlsson, la tradición del insight; Wallas 1926 ya aislaba la
"iluminación") pone la creatividad en el momento de generación; la vista amplia (Weisberg,
en parte Dunbar) dice que es cognición común distribuida en todo el flujo y que el "momento
aha" es en parte artefacto narrativo. Nuestra elección: **"creatividad" (estricta) = el
eslabón de generación del candidato; "rendimiento creativo" = propiedad del flujo entero.**
La razón es de nuestros propios datos: las etapas se DISOCIAN (menús sin hipótesis; un
candidato construido en código sin narrarlo; ejecución correcta cuando la idea viene
nombrada). Si creatividad = todo, perdemos la capacidad de decir DÓNDE se rompió — que es
justo lo que el instrumento logra.

**Ajuste 3 — la comparativa histórica, degradada con honestidad.** La idea "100 casos:
descubridor vs contemporáneos con los mismos datos" no se sostiene como estudio (la historia
documenta rico al que saltó y casi nada a los que no; el descubridor difería en mil cosas a
la vez; la atribución contrafáctica es opinión). Su valor real: los pocos contrastes bien
documentados (Priestley/Lavoisier vía Thagard; el equipo de Onnes) son **pruebas de
existencia** de condiciones — mina de hipótesis, no evidencia. Y el reframe operativo: **la
comparativa que la historia no permite, nuestros mundos la fabrican** — el mismo agente, el
mismo mundo, con y sin la condición, es el experimento Priestley/Lavoisier hecho bien. Para
eso son los gemelos y las condiciones.

## El flujo, en dos resoluciones

**Versión de bolsillo (5 etapas, para conversar):**

1. Medir con resolución suficiente para **VER** que algo no cierra.
2. Que lo que no cierra te **MOLESTE** (la norma que vuelve intolerable el residuo).
3. **GENERAR** el candidato estructural (la creatividad estricta; el "aha").
4. Correr el **TEST barato que discrimina** (el contraste).
5. **JUGARSE**: reconstruir sobre la estructura nueva y sostenerla.

**Versión instrumental (la cadena de 9 eslabones del Protocolo v1, que es la que se mide):**
evidencia → grieta → creatividad → puesta en juego → desarrollo → contraste → selección →
realización → propagación. Mapeo: etapa 1-2 ≈ evidencia+grieta · etapa 3 ≈ creatividad ·
etapa 4 ≈ puesta en juego+desarrollo+contraste · etapa 5 ≈ selección+realización+propagación.
El marco que este doc enuncia **ya está operacionalizado** en esa ficha — no hay que
construirlo, hay que reconocer que es el centro.

## La hipótesis anti-romántica (abierta, con su pregunta honesta)

La vista romántica pone la magia en la etapa 3. **Nunca encontramos el cadáver ahí.** Los
cadáveres aparecen antes (renombran la señal para no dudar; no les molesta el residuo) y
después (no corren el test; no se juegan). Y con la idea nombrada, la desarrollan. Para un
LLM con repertorio gigante, generar puede ser lo barato; lo caro parece ser **la economía
alrededor**: notar, que te importe, chequear, comprometerte. **Pregunta abierta que aún no
podemos separar**: ¿generar es difícil, o generar nunca recibe sus precondiciones? (En
Perfiles: 0/10 hipótesis específica — pero también 0/10 duda expresada y 0/10 contraste. ¿La
semilla o la tierra?)

Candidatos a "lo que realmente importa", compitiendo sin favorito: resolución del
instrumento · norma interna (Rayleigh vs Priestley) · **memoria/incubación** (candidata de
Lucas — los episodios de 4 turnos ni la instancian) · hábito del test barato · costo de
jugarse · capa social · tiempo.

## La apuesta falsable que el marco hace

**Los fallos viven en el FLUJO y son independientes del TIPO de edición; los tipos importan
solo para diseñar mundos.** Evidencia a favor hasta hoy: mundos de tipos distintos
(count_mix, Perfiles, la planta) rompen la cadena en los mismos eslabones. Si algún día un
tipo muestra un perfil de falla propio, la apuesta se rompe — y eso también sería un
hallazgo. Las pruebas siguientes se derivan del marco: forzar el eslabón señalado (contraste)
debería destrabar la cadena (el experimento del validador; el mundo de Partículas).

## Qué cambia en la casa (operativo)

- **La cadena + el instrumento (Protocolo v1) pasan a ser el centro del programa.**
- **La taxonomía de 11 saltos baja a BIBLIOTECA DE DISEÑO** (catálogo de verdades ocultas
  para construir mundos; sigue viva para eso). La nomenclatura por salto (ADR 0179) se
  conserva: cada experimento sigue nombrando su salto objetivo — lo que cambia es el nivel
  de ANÁLISIS de las fallas (por eslabón, no por tipo).
- La palabra "creatividad" en docs y fichas = sentido estricto (el eslabón); para el todo se
  dice "flujo de descubrimiento" / "rendimiento creativo".
- El linaje intelectual queda declarado: Darden (lado ediciones) × Wallas/Ohlsson/Klein/
  Nersessian (lado flujo); lo que no existía y es nuestro: el instrumento de medición
  mecánico del flujo, con gemelos.
