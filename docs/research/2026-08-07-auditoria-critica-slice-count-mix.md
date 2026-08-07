# Auditoría crítica del slice count_mix — qué tiene sentido y qué no

> **Origen:** revisión exigida por Lucas (2026-08-07) tras preguntar qué se le pide exactamente al
> agente. **Confesión de proceso primero:** el brief lo escribí yo (Claude) el 2026-08-06; el
> problema no fue desconocerlo sino no CONFRONTARLO — certifiqué que la información alcanzaba
> (testigo) y que un robot podía ganar, pero nunca apliqué al diseño la pregunta 3/8 del gate
> "un nivel arriba" (¿medimos lo que creemos? ¿el anfitrión produce el fenómeno NATURALMENTE?)
> del lado del INCENTIVO del agente. Las preguntas de Lucas son ese gate, ejecutado tarde.
> Ningún dato se recorre ni se descarta: se RE-LEE con las fallas a la vista.

## A. Lo que NO tiene sentido (tres fallas de diseño confirmadas)

**A1 — El objetivo declarado no requiere el salto (stakes vacíos).** El brief pide "modelo
generativo para planificar inspección y descartes" y el campo de stakes/funcionales — el
mecanismo de la casa para decir "al cliente le importa especialmente X" — quedó `[]`. El modelo
continuo que entregaron sirve razonablemente al objetivo declarado (media 0.90–0.99, varianza ✓,
repeticiones ✓, velocidades no vistas ✓; R = 0.83–0.91). Lo único que pifian —la banda intermedia,
al doble— no le importa a nadie en el mundo. **La rival "no saltó porque no lo necesitaba" está
viva por construcción.**

**A2 — El salto no paga en extrapolación (violación de ADR 0150).** Diseñé la estructura
invariante entre regímenes a propósito (ambas clases escalan igual con `speed`) buscando limpieza…
y eso viola la regla más profunda de los mundos de salto, que la casa ya tenía escrita: *"el
premio del salto vive en la EXTRAPOLACIÓN; si el mundo paga por fit del régimen visitado, el
parche gana siempre"*. En este mundo NO existe régimen —alcanzable ni de examen— donde el modelo
continuo se rompa y el discreto no. Por eso R apenas lo cobra. Doble des-incentivo con A1.

**A3 — El ancla de S era el rival equivocado (el "media-salto" fue parcialmente artefacto).**
S_struct se ancló en el mejor UN-componente **iid** (sin persistencia). Pero el rival real —lo
que de hecho entregaron— es la frailty continua CON persistencia, que captura el ICC
trivialmente (verificado hoy: baseline frailty da valle=0.302, icc=0.783 vs verdad 0.154/0.746).
Contra el rival fuerte, el componente ICC se vuelve ruido de escala y la métrica honesta de
DISCRETITUD queda en el valle solo: **las entregas de los agentes puntúan ≈0–0.36 (mediana ~0.2,
varias ≈0.0)** — es decir, **≈ el rival continuo mismo**. El titular "construyeron la mitad del
salto" mezclaba un componente real (persistencia capturada — dato verdadero e interesante) con
la vara de salto inflada por el ancla débil. ADR 0152 (titulares con alcance) me alcanzó a mí.

## B. Lo que SÍ tiene sentido (sobrevive la crítica, y algo sale fortalecido)

**B1 — El hecho conductual limpio, que ninguna de las tres fallas toca:** en **0 de 11 episodios**
(6 principales + 4 pista + técnico) los agentes corrieron **comparación de modelos alguna** — ni
un ajuste de mezcla-2, ni un BIC frente a frente — incluso cuando verbalizaron la alternativa
("subpopulations via clustering or mixture"), incluso con la pista, siempre con presupuesto
sobrante. Ajustan UNA historia, la chequean contra sí misma, entregan. Esto no depende de
stakes, ni de extrapolación, ni de anclas: es conducta observada en la traza. Y converge con la
línea B (chequean ajuste, no forma) y con agosto (reenvío byte-idéntico).

**B2 — El gemelo funcionó 10/10** (espurio 0; ni la pista induce clases fantasma). El
instrumento bilateral es real: no premiamos paranoia y ellos no fantasean.

**B3 — La conducta de compra fue buena 20/20** (repeats en turnos 2–4, sin señal). El mundo
elicita buen shopping; la falla queda aislada en hipótesis/criticism — localización útil.

**B4 — La infraestructura y la disciplina**: testigo, robots (cazaron 4 choques de contrato antes
del primer dólar), fichas congeladas, seeds quemadas, techo respetado 30×, crudos completos. Y la
revisión misma funcionó: la crítica de Lucas cazó A1/A2; la verificación numérica de hoy cazó A3.

## C. El resultado, re-leído con la vara honesta

| Qué | Lectura re-hecha |
|---|---|
| Persistencia por lote | **Capturada** (ICC ≈ verdad, 10/10) — dato real, se reporta como componente aparte |
| Salto discreto (valle vs rival fuerte) | **≈0 en 10/10 + técnico** — "no abrió", más limpio que el "indeterminado" del ancla vieja |
| Pista nivel-2 | No movió nada (y la frase era absorbible — salvedad ya registrada) |
| Sugestión en el gemelo | No (0/10) |
| Comparación de modelos corrida | **0/11** — candidato a métrica conductual primaria de la v1 |

## D. Qué cambia para la v1 y para la máquina (propuesta, NO ejecutada)

1. **Certificado de necesidad DOBLE** (nueva compuerta del kit, para TODO mundo de salto):
   *epistémica* (testigo + brecha contra la familia rival FUERTE — enumerando explícitamente la
   versión con persistencia/continua del rival) **y teleológica** (el objetivo declarado del
   agente debe REQUERIR el salto: stakes con funcional declarado + el salto debe pagar en
   extrapolación/held-out, ADR 0150).
2. **v1 del mundo**: (a) stake declarado en el brief ("a la gerencia le importa la fracción de
   lotes en la banda de reproceso 4–7" — donde el continuo yerra al doble); (b) estructura que
   PAGUE fuera de soporte (p.ej. el peso de la clase mala crece con `speed`: el frailty ajustado
   a speed=1 extrapola MAL a 1.2 y el examen lo cobra); (c) baseline fuerte congelado en la
   ficha; (d) métrica primaria conductual: ¿corrió alguna comparación de modelos? (computable de
   trazas, cero-LLM) + valle-vs-rival-fuerte como métrica de entrega.
3. **La escalera de ayudas (niveles 3/4)** se corre sobre la v1 — en la v0 respondería "¿pueden?"
   dentro de un mundo que ya sabemos mal-incentivado.
4. **El dossier completo (resultado + esta auditoría) va a Codex** antes de construir la v1.

## E. Meta-lección

El slice costó USD 1.5 y tres días, y produjo: un fenómeno conductual limpio (B1), dos gemelos
certificados reutilizables, cuatro bugs de contrato cazados gratis, y TRES fallas de diseño
detectadas por revisión antes de que contaminaran un claim. Exactamente para esto era la fase de
descubrimiento barata: el mundo v0 era la planta piloto, y la planta piloto enseñó — sobre los
agentes Y sobre nosotros. La regla de Lucas ("contrastar con la realidad lo antes posible") y su
pregunta ("¿qué se le pide exactamente?") son las dos guardias que más valor produjeron esta
semana; la segunda entra al checklist permanente de diseño: **leer el brief con los ojos del
agente racional y preguntarse si el salto le conviene**.
