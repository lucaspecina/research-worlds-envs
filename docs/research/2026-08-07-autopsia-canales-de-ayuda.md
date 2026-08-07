# Autopsia: por qué "ayuda fuerte" rindió peor que "ayuda media" (gpt-5.4)

> **Origen:** Lucas (2026-08-07): "es rarísimo esto de ayuda fuerte peor que ayuda media... no
> tiene sentido para mí. Debe haber algo que no estamos viendo." Releí las 8 trayectorias con
> ayuda de la escalera v0.2 (mix), turno por turno, con citas textuales.
>
> **Alcance del titular:** 2 modelos (gpt-5.4, DeepSeek-V3.2) × 1 mundo (count_mix_v0 v0.2) ×
> n=2 seeds por celda × las dos frases congeladas de la escalera. El mecanismo se lee en el
> TEXTO de las 8 trazas (consistente 8/8), no solo en los scores.

## El resultado que parecía absurdo

| Celda (mix) | DeepSeek | gpt-5.4 |
|---|---|---|
| nivel3 — "considerá la posibilidad de que los lotes vengan en unos pocos tipos distintos" | 0.0 · 0.0 | **0.87 · 0.97** |
| nivel4 — "considerá probar un modelo de mezcla finita: 2 o 3 grupos de lotes, cada grupo con su propia tasa" | **1.0** (+1 censura max_tokens) | 0.17 · 0.0 |

Leído como "dosis de ayuda", es una paradoja: más ayuda, peor. Leído en las trazas, no hay
paradoja: **las dos frases no son dosis de la misma droga — son drogas distintas que entran por
órganos distintos.**

## Qué hace cada modelo con cada frase (evidencia textual)

**nivel3 es una afirmación sobre el MUNDO** ("los lotes vienen en tipos"). gpt la convierte en
una instrucción de mirada — va a los datos a BUSCAR el patrón:

- 99366 t4: *"the unit means seem to cluster into low and high levels... fit a rough 2-type split"*
- 99366 t5: *"The unit means are very cleanly bimodal, which strongly supports a small discrete mixture"*
- 99367 t5: *"estimate whether the baseline marginal at speed 1.0 is obviously multimodal in lot means"*
- 99367 t6: *"strikingly clustered into a low group around 1–3 and a high group around 7–14"*

Mira las medias por lote → la bimodalidad es innegable → entrega mezcla. **La frase le cambió
QUÉ mirar; una vez mirado, ver = creer.**

**nivel4 es una afirmación sobre una HERRAMIENTA** ("probá el modelo de mezcla"). gpt NO la
lleva a los datos: la archiva en su menú de familias de modelos, junto a Poisson y NegBin, y
sigue su rutina de siempre — momentos, varianza dentro/entre lotes, escalado con velocidad.
Ninguno de esos resúmenes distingue mezcla de gamma continua. Al final, el default gana "por
parsimonia" **sin que la mezcla se haya ajustado ni una vez**:

- 99370 t3: *"decide between plain Poisson, gamma-Poisson/negative-binomial, or a finite mixture"* (la lista)
- 99370 t5: *"using a gamma distribution for lot rates is a **parsimonious continuous alternative
  to a finite mixture**"* — la frase espécimen: parsimonia invocada EN LUGAR del test, no después.
- 99371 t5: *"the estimated NB size stays roughly stable around 2–3 despite noise, which is
  exactly what gamma mixing... predicts"* — chequeo que la mezcla también pasa (no discrimina).

**El detalle brutal:** en ambas corridas nivel4, gpt IMPRIMIÓ la evidencia discriminante y los
ojos le pasaron por encima. En 99371 t2 imprimió el histograma de y (0..20): 46-49 casos en
y=1-3, caída a 8 en y=5, retorno a 23-27 en y=7-8 — el valle, en pantalla. En 99370 t3 imprimió
los cuartiles de las medias por lote: 25%=2.0, 50%=5.25, 75%=11.0 — dos nubes, en pantalla.
Cero comentarios en ambos casos. **Miró los datos a través de los estadísticos que su modelo
default sabe explicar (media, varianza, ICC, k de NB) — y esos estadísticos son exactamente los
que no pueden refutarlo.**

**DeepSeek es el espejo exacto.** Con nivel3 (afirmación sobre el mundo) la registra, PLANEA el
test — 99365 t5: *"I can... fit a two-component Poisson mixture via EM"* — y el plan se muere en
el camino: 5 turnos después (t10) cierra con *"I could extend the model to a mixture of two
Gamma distributions, **but that adds complexity**. Given the data, a single Gamma may be
sufficient"*. Episodios largos (11-19 turnos), el plan del turno 5 no sobrevive al turno 10.
Con nivel4 (herramienta) la trata como spec y la EJECUTA: 99368 t7: *"scipy is available, so I
can properly fit a Poisson mixture. I'll fit a two-component mixture... using EM"* — ajusta,
contrasta ICC y varianzas simuladas contra las observadas, entrega. 1.0. La única celda de toda
la era v0.2 con un ajuste formal de la mezcla.

## El mecanismo unificador (lo que no estábamos viendo)

En TODAS las celdas falladas — con ayuda y sin ayuda — el acto ausente es el mismo: **nadie corre
el test que discrimina** (ajustar la alternativa y compararla contra el default). La hipótesis
correcta puede estar EN LA LISTA (con ayuda, la pusimos nosotros); entre la lista y la entrega
hay un filtro — "¿necesito más estructura?" — y ese filtro corre con evidencia que el default
siempre sobrevive (momentos, "parsimonia", "adds complexity"). La ayuda cambia POR DÓNDE entra
la hipótesis; no cambia el filtro:

- Si entra por la **percepción** (afirmación sobre el mundo + el modelo va y mira): el patrón
  visto con los ojos es tan fuerte que saltea el filtro. Camino de gpt en nivel3.
- Si entra por el **menú de métodos** (sugerencia de herramienta): cae justo en el filtro roto y
  muere por parsimonia-sin-test. Camino de gpt en nivel4.
- Si entra como **spec a ejecutar** (para un modelo obediente-ejecutor como DeepSeek): saltea el
  filtro por obediencia. Camino de DeepSeek en nivel4.
- Si requiere **sostener un plan propio** muchos turnos (DeepSeek en nivel3): el plan decae antes
  de ejecutarse.

Corolario re-leído del hallazgo B1 (0 comparaciones espontáneas en 11 episodios; 1 sola celda con
ajuste formal en toda la era): el cuello de botella del salto en este mundo no es solo GENERAR la
hipótesis — es que aun REGALADA, solo prospera si llega en el formato que el órgano sano de cada
modelo sabe usar.

## Explicaciones rivales (estado)

1. **Ruido de n=2.** Viva para los scores; débil para el mecanismo: el patrón textual es 8/8
   coherente (2/2 nivel3-gpt miran la forma de las medias por lote; 2/2 nivel4-gpt no la miran
   nunca; 2/2 nivel4-DS ajustan EM u operan como spec; 2/2 nivel3-DS planean-y-abandonan).
   Barata de matar con +2 seeds por celda.
2. **Confusión de wording, no de canal.** nivel3 AFIRMA un hecho; nivel4 INVITA a probar
   ("considerá probar") — quizá lo que mata no es el canal (mundo vs herramienta) sino el modo
   verbal (afirmación vs invitación). Discriminable con una frase nueva (abajo).
3. **Recursos/presupuesto.** Descartada: gpt entregó con 200-400 de presupuesto sobrante en
   ambas nivel4.

## Qué se propone (pendiente de GO de Lucas — nada corrido)

1. **Des-ruido del 2×2**: +2 seeds por celda de ayuda (8 corridas, ~USD 1.5).
2. **Frase nueva "nivel4b — comparación mandada"** (congelada antes de correr, una-frase-una-
   corrida): en vez de regalar el modelo, mandar el ACTO ausente — p.ej. *"Nota del encargo:
   antes de entregar, ajustá al menos dos familias candidatas y quedate con la que gane en una
   comparación directa sobre los datos."* Predicción pre-registrada: gpt salta (la frase fuerza
   la comparación que su filtro nunca corre) sin que le hayamos nombrado la mezcla; si aun así
   no salta, el filtro es más profundo que el wording. Nota: esta frase no nombra "tipos" ni
   "mezcla" — es ayuda de PROCEDIMIENTO puro, un peldaño genuinamente distinto de la escalera.
3. **Reencuadre del instrumento**: dejar de leer la escalera como DOSIS y leerla como CANALES
   (percepción / método / procedimiento). El objeto medible pasa a ser "¿en qué órgano muere la
   hipótesis regalada?" por modelo — la localización del quiebre dentro de las etapas del salto
   (ver-patrón → postular-estructura → testear → adoptar). Candidato fuerte a pieza central del
   dossier para Codex.

## Nivel arriba

- **Aprendizaje real:** la variable activa de la ayuda no es su fuerza sino su CANAL; el déficit
  común de fondo es un filtro de necesidad que corre con chequeos sin poder de refutación
  ("parsimonious continuous alternative to a finite mixture" — sin haber ajustado la mezcla).
- **Límite del claim:** 2 modelos, 1 mundo, n=2 por celda, 2 frases; el mecanismo es textual y
  consistente pero el diseño no separa aún canal de modo-verbal (rival 2).
- **Explicación rival más fuerte:** wording (afirmación vs invitación), no canal.
- **¿Sigue siendo este mundo el uso de mayor valor?** Sí: acaba de convertirse en un
  localizador de QUÉ etapa del salto se rompe por modelo — más fino que "salta/no salta".
