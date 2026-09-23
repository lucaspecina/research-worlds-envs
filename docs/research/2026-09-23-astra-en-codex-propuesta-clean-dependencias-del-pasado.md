# Astra en Codex, segundo turno: la propuesta "clean" para el mes — reconstruir dependencias del pasado (2026-09-23, noche)

> **Qué se le mandó** (misma sesión persistente de Codex, `gpt-6-astra`, effort max): la propuesta A de Claude
> (escalera de ediciones + brecha cerrada, estilo NewtonBench), el punto de Lucas sobre el incentivo (lección de
> D1), las tres dudas vivas (listar hipótesis afuera; contradicción de adentro o de afuera; cómo aislar la
> creatividad si es fácil) y la consigna de Lucas: **no otra review, sino UNA idea y UNA propuesta limpias**,
> en diez líneas como el abstract de NewtonBench, con sus tres comprobaciones previas y su resultado que la
> mata. Prompt: `scratch/codex-astra-consulta-2026-09-23b.txt`; transcript: `scratch/codex-astra-respuesta-2026-09-23b.txt`.
> **Nada decidido**; sigue el ida y vuelta con Lucas.
>
> **Resumen de Claude.** Elige **A, restringida a UNA transformación: incorporar dependencias del pasado.**
> Cambia la perilla: no "cantidad de ediciones" (depende de la gramática) sino **cantidad de entradas pasadas que
> afectan necesariamente la salida** (k = 0, 1, 2, 3), verificable sin discutir cómo se escribe el programa.
> Mundo: bits; y_t = b XOR u_t XOR (XOR de las entradas en las posiciones secretas S, entre 8 posibles). La ley
> es fija todo el episodio; el prefijo es compatible con "solo importa la entrada actual" (p. ej. tras
> reiniciar el pasado a cero), sin cambiar el aparato en secreto. **Nota Q = 1 − 4·Brier**: 0 = techo del mejor
> predictor sin pasado (0.25 de Brier para todo k>0, verificado por enumeración de las 512 ventanas; incluso
> conocer todos los rezagos menos uno deja 0.25), 1 = reconstrucción perfecta; brecha absoluta constante 0.25
> (en D1 era 0.014: "normalizar no fabrica la pérdida"). El agente conoce cómo se puntúa y ve sus predicciones
> vs resultados en un lote de comprobación (quedarse cuesta y el costo es visible). Tres comprobaciones antes
> de construir: certificado de necesidad y nota (incluida una tabla que memoriza y un predictor flexible: el
> presupuesto no debe permitir ganar almacenando la tabla de verdad; cualquier solución funcionalmente
> correcta vale); certificado de evidencia y presupuesto (un testigo sin conocer S, b, k recupera la regla
> dentro del presupuesto); calibración de capacidad y techo (microepisodios con y sin pista constante sobre la
> familia — "paridad de entradas presentes y pasadas" — también en el gemelo). **Muerte:** si sin ayuda cierran
> ≥90% de la brecha casi siempre, incluido k=3, y conservan el gemelo → se cierra el anfitrión por techo, sin
> buscar un wording que los haga fallar; si ni con la idea nombrada resuelven, no se lanza la tanda. La firma
> interesante: capacidad asistida alta + pérdida autónoma reproducible al crecer k. Sobrevive solo M4; M1/M2/M3/M5
> quedan afuera este mes. Las dos dudas: "adentro o afuera" → perilla binaria operacional (chequeo automático
> vs iniciado por el agente), fija en automático este mes; "creatividad" → queda en la motivación, no en el
> claim ("descubrir e incorporar dependencias necesarias bajo evidencia suficiente y capacidad comprobada").
> Lo que no le convence: la dicotomía "si cae la curva, can't jump es cierto"; llamar "parche" a cualquier
> solución que no tenga nuestra forma preferida (si un predictor flexible reconstruye la conducta, gana; la
> frontera es funcional: usa o no la información necesaria); y que la familia resulte demasiado fácil — por
> eso los microcasos primero.

---

**[Juicio] Elijo A, restringido a una sola transformación: incorporar dependencias del pasado.** B responde otra pregunta y lo dejaría afuera del mes.

Cambiaría la perilla: **no “cantidad de ediciones de forma”, sino “cantidad de entradas pasadas que afectan necesariamente la salida”.** Eso se puede verificar sin discutir cómo escribimos el programa. No lo llamaría distancia creativa.

## La propuesta, en diez líneas

**[Juicio — abstract de un experimento propuesto, no de resultados obtenidos]**

1. Evaluamos si agentes reconstruyen dependencias omitidas cuando su modelo inicial falla visiblemente.
2. Usamos dispositivos binarios deterministas cuya salida depende de la entrada actual y, eventualmente, de entradas anteriores.
3. La única perilla del mundo es el número de dependencias pasadas relevantes: cero, una, dos o tres.
4. El horizonte disponible, presupuesto, interfaz y magnitud de la pérdida evitable permanecen equiparados.
5. Un prefijo permite predecir correctamente sin usar el pasado; después aparecen pruebas que distinguen las alternativas.
6. El agente recibe automáticamente los errores de su predictor provisional sobre datos visibles, sin diagnóstico estructural.
7. Puede experimentar y entregar cualquier predictor ejecutable, sin enumerar previamente hipótesis.
8. La nota mide cuánto mejora respecto del mejor predictor posible sin pasado, con una brecha absoluta constante.
9. El caso sin dependencias controla revisiones perjudiciales; la idea nombrada controla capacidad de resolución.
10. El resultado es una curva de rendimiento frente al número de dependencias, con y sin ayuda estructural.

## El mundo concreto y la nota

**[Juicio] Tomaría la familia:**

\[
y_t=b\oplus u_t\oplus\bigoplus_{j\in S}u_{t-j},
\qquad k=|S|\in\{0,1,2,3\}.
\]

Las entradas son bits; \(\oplus\) significa XOR. Hay ocho posiciones pasadas disponibles. El conjunto \(S\) y el bit \(b\) son secretos.

En palabras: **algunas entradas anteriores invierten la respuesta; el agente debe descubrir cuáles y cómo combinarlas.**

La ley permanece fija durante todo el episodio. El prefijo usa historias compatibles con el predictor sin pasado —por ejemplo, pruebas después de reiniciar las entradas previas a cero—; **no cambiamos secretamente el dispositivo después del compromiso**.

Las instancias se aparean conservando también el mayor rezago relevante: aumentar \(k\) no debe convertirse accidentalmente en recordar más atrás.

### Por qué acá el default pierde realmente

La familia de base no es una fórmula débil elegida a mano. Es **cualquier predictor probabilístico que use solamente la entrada actual**.

Bajo una distribución uniforme de las ventanas de entrada:

- Para cualquier \(k>0\), su mejor Brier posible es **0.25**.
- La regla verdadera obtiene **0**.
- Incluso conocer todos los rezagos relevantes menos uno deja Brier óptimo **0.25**: el bit faltante mantiene incierta la paridad.

**[Juicio — cálculo propio]** Comprobé esta propiedad por enumeración de las 512 ventanas posibles, además del argumento anterior. Es una propiedad matemática del diseño, todavía no una certificación del entorno ni de capacidad del agente.

Usaría una única nota:

\[
Q=1-4\,\mathrm{Brier}.
\]

Para \(k>0\), **0 es el techo del predictor sin pasado y 1 es reconstrucción perfecta**. Se permiten notas negativas; no las recortaría.

Para \(k=0\), la misma nota sigue funcionando: la base correcta obtiene 1. Ahí no hablamos de “brecha cerrada”, porque la brecha contra la base es cero.

**[Paquete]** Esto conserva la lección de [ADR 0175](/Users/lucaspecina/Desktop/dev/ai/lucaspecina/research-worlds-envs/docs/adr/0175-headroom-contra-el-mejor-rival-sin-salto.md): la base optimizada debe perder materialmente. **Normalizar no fabrica esa pérdida.** En D1 no alcanzaba con reescalar 0.014; acá la diferencia absoluta es 0.25.

El agente conocería cómo se puntúa y vería predicciones propias frente a resultados reales en un lote de comprobación. El examen final no se usa para darle feedback. Así, quedarse cuesta **y ese costo es visible**.

## Las tres comprobaciones antes de construir el entorno

**[Juicio] Las haría con cálculo y microcasos estáticos; no requieren desarrollar una fábrica. El control con agentes requiere el GO correspondiente.**

1. **Certificado de necesidad y nota.** Verificar la influencia efectiva de cada entrada, el óptimo de la base y la brecha constante. Probar también una tabla que memoriza observaciones y un predictor flexible: el presupuesto no debe permitir ganar simplemente almacenando toda la tabla de verdad. La evaluación debe aceptar cualquier solución funcionalmente correcta.

2. **Certificado de evidencia y presupuesto.** Un testigo recibe exactamente las observaciones y acciones legales, sin conocer \(S\), \(b\) ni \(k\), y recupera la regla dentro del presupuesto común. Verificar que el prefijo y las pruebas posteriores provienen de la misma ley. Mantener comparable la longitud del historial, el horizonte y la evidencia servida.

3. **Calibración de capacidad y techo.** Microepisodios frescos, con y sin una pista constante sobre la familia de reglas —paridad de entradas presentes y pasadas—, sin revelar posiciones ni cantidades. La pista también se prueba en el gemelo: debe permitir descubrir que ningún rezago interviene.

**Resultado que mata esta propuesta como siguiente inversión:** si sin ayuda cierran al menos el 90% de la brecha prácticamente siempre, incluido \(k=3\), y conservan el gemelo, **cerramos este anfitrión por techo**. No buscaría un wording que los haga fallar.

Si ni con la idea nombrada resuelven, tampoco lanzamos la tanda principal: falla la calibración necesaria para interpretar el descubrimiento autónomo.

La firma interesante sería **capacidad asistida alta y una pérdida autónoma reproducible al aumentar \(k\)**. No la doy por descontada.

## Qué queda de las mutaciones de A

**[Juicio] Este mes sobrevive solamente M4, modificada a esta familia determinista.** M1, M2, M3 y M5 quedan afuera; no intentaría salvarlas simultáneamente.

Eso resuelve los tres problemas señalados:

- **Reabsorción:** una distribución latente o un ruido más flexible, mientras no use el pasado, sigue limitado a Brier 0.25. Si empieza a condicionar en el pasado, ya abandonó funcionalmente la base.
- **Gramática:** \(k\) no cuenta instrucciones. Cuenta entradas cuya intervención puede cambiar la salida manteniendo las otras fijas. Reescribir el programa no cambia ese número. Está definido respecto de las entradas físicas del dispositivo, no como propiedad de la mente del agente.
- **Gemelo:** agregar una dependencia de paridad falsa produce errores y pierde nota. Un programa más general que deja sus coeficientes temporales en cero **no debe perder**: representa correctamente el gemelo.

**[Literatura]** NewtonBench también define sus mutaciones respecto de una representación concreta y pone restricciones para evitar que varias se reduzcan a una. Eso es una decisión de ingeniería del benchmark, no una escala psicológica universal. Además, su equivalencia simbólica usa un juez LLM; nosotros no necesitamos copiar esa parte. [NewtonBench, apéndices A.3–A.4](https://arxiv.org/html/2510.07172v1).

## Las dos dudas pendientes

**[Juicio] “Contradicción interior o exterior” la convertiría en una perilla binaria operacional: chequeo automático versus chequeo por iniciativa del agente.** Mismos datos, restricciones y predictor; en una condición el sistema ejecuta y presenta la comparación, en la otra el agente debe iniciarla con el mismo verificador disponible. No afirmaría que eso manipula el origen psicológico del insight.

**En este experimento la dejaría fija en automático.** Comprar evidencia nueva sería otra intervención y queda afuera.

**[Juicio] “Creatividad” queda en la motivación, no en el resultado certificado.** El claim es descubrir e incorporar dependencias necesarias bajo evidencia suficiente y capacidad comprobada. Puede hacerse recuperando un esquema conocido, construyéndolo o combinando ambos. El experimento no necesita resolver esa disputa para producir un resultado interpretable.

## Lo que NO me convence

**[Juicio]** No acepto la dicotomía “si la curva cae, *can’t jump* es cierto; si no, es falso”. La curva caracteriza esta tarea y sus ayudas.

Tampoco acepto llamar “parche” a cualquier solución que no tenga nuestra forma preferida. **Si un predictor flexible reconstruye correctamente el comportamiento, gana.** La frontera defendible es funcional: usa o no la información necesaria.

Y esta familia puede resultar demasiado fácil. Precisamente por eso propongo intentar descartarla con microcasos antes de comprometer el mes. **Mi apuesta concreta es ésta: dependencias necesarias, pérdida constante y fallo visible; no cinco mutaciones ni una teoría general de creatividad.**
