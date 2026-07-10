# Codex ronda 5 — diagnostico y rediseno del metodo de pistas (GPT-5.6 Sol, max) — 2026-07-10

> Consulta pedida por Lucas: que pasa con las pistas y como hacerlo mas honesto. Veredicto: la intuicion de Lucas (pista dirigida = valida el mundo) es SALVABLE pero solo como pieza de triangulacion, no como prueba autosuficiente; formulacion honesta de 3 eslabones + control epistemico activo (no placebo de estilo) + metricas de tasa + protocolo de 3 fases. Diagnostico de los ceros: mas probable un atractor catastrofico preexistente de DeepSeek amplificado por la pista, que sobre-incorporacion (a confirmar con trazas). Crudo:

codex
Diagnóstico central: la sobre-incorporación es plausible, pero hoy hay una explicación más conservadora: **DeepSeek tiene un atractor catastrófico preexistente y cualquier cambio de prompt altera la probabilidad de caer ahí**. Hay R≈−1.3 en libre, pista y placebo; la pista parece aumentar esa probabilidad bajo escasez, pero no necesariamente inventa un fallo nuevo.

## (a) Mecanismo de los ceros

Hipótesis priorizadas:

1. **Template malo recurrente amplificado por la pista.** Los R_uncl cercanos a −1.3 en varios brazos sugieren una misma arquitectura equivocada: defaults, rama observacional/do, signo o tratamiento del confounding.

2. **Sobre-incorporación:** usa asociaciones históricas como causales o fuerza toda evidencia comprada dentro de la maqueta.

3. **Reescritura final destructiva:** tenía una interpretación razonable, pero “check every part/incorporate” induce complejidad o una última reimplementación.

4. **Cambio de estrategia de compras:** la advertencia sobre presupuesto altera qué evidencia adquiere, no solo cómo la integra.

Miraría exactamente:

- Secuencia de compras, costos y momento de terminación.
- Hipótesis antes y después de cada evidencia.
- Qué relaciones declara causales y con qué respaldo.
- Si distingue registros observacionales de experimentos.
- Código final:

  - rama `decision set` vs. no-set;
  - defaults de knobs;
  - coeficientes y signos;
  - uso de correlación histórica bajo `do()`;
  - proceso vs. ruido de medición;
  - última reescritura.

- Score descompuesto por:

  - observacional;
  - intervenciones supplier;
  - intervenciones hall;
  - contexto;
  - energía vs. funcional de rechazo.

Confirmaría sobre-incorporación solo si los ceros:

1. compran evidencia relevante;
2. reconocen su naturaleza;
3. trasladan asociaciones observacionales a la rama causal o agregan términos no identificados;
4. fallan específicamente en `do()`.

Si fallan en todas las particiones por defaults/código, es implementation drift, no sobre-incorporación.

## (b) ¿Es salvable la intuición de Lucas?

Sí, pero como **evidencia de sensibilidad causal del ítem**, no como prueba autosuficiente de validez.

La formulación honesta sería:

> Una intervención dirigida cambia la conducta epistémica objetivo y mejora selectivamente el outcome en mundos donde esa conducta es necesaria.

Tiene tres eslabones, no uno:

1. La pista cambia la conducta objetivo en la traza.
2. Esa conducta mejora el score en el mundo-vicio.
3. No mueve controles ni ejecución general.

Si solo observan el punto 2, puede ser instruction-following, leak o ayuda de código.

Además, hay una tensión doctrinal inevitable: si una instrucción arregla el fallo, por el criterio actual “¿lo arregla un scaffold?”, parece OPERACIÓN. Para salvar el método deben decir:

> La pista es una manipulación diagnóstica del proceso, no evidencia de que el fallo sea intrínsecamente no-scaffoldeable.

No puede validar por sí sola el corte operación/juicio.

### Pista más limpia

- Contextualmente neutra.
- Sin presupuesto, código, entrega ni “usá todo”.
- Un principio epistémico, no checklist operativo.
- Reutilizable en varias estructuras del mismo vicio.

Ejemplo:

> “Treat your current leading explanation as provisional: evidence should be allowed to change which explanation you prefer.”

### Control más limpio

No usaría placebo de estilo. Usaría otra pista epistémica igualmente sustantiva, dirigida a un vicio ortogonal. Idealmente:

- mundo de actualización + pista de actualización / pista de calibración;
- mundo de calibración + pista de actualización / pista de calibración.

Cada pista funciona como control activo de la otra. Es mucho más informativo que “nombres claros”.

El control del mundo debe ser un gemelo estructural con headroom, no una variante saturada por presupuesto.

### Métrica

Por la bimodalidad:

- Primaria: tasa de éxito `R ≥ τ`, con τ fijado desde robots/bandas antes de correr.
- Secundaria: tasa catastrófica `R_uncl < 0`.
- Secundaria: distribución completa de R_uncl.
- Interacción principal: diferencia de tasas entre pista dirigida y control activo, target vs. gemelo.

No medianas de ocho episodios.

## (c) Juicio vs. ejecución

No alcanza con conducta nombrada + seeds apareadas + temperatura + n grande. Eso mejora precisión, no identificación causal.

Necesitan medir tres resultados separados:

- **Conducta epistémica:** ¿buscó alternativa, revisó creencia, distinguió obs/do?
- **Ejecución:** aceptación, contrato, ramas, errores numéricos, terminación, tokens.
- **Outcome científico:** R y particiones.

La evidencia fuerte es:

> cambia conducta epistémica → mejora outcome → ejecución permanece estable.

Si mejora outcome sin cambiar la conducta, es prompt effect inespecífico. Si cambia conducta pero no outcome, el mundo no la vuelve necesaria o el reward no la ve.

Idealmente agregaría una condición de ejecución común/oracular. Como mínimo, un control con la misma arquitectura de código y sin el vicio.

Temperatura fija no garantiza determinismo. Hay que:

- fijar versión del deployment;
- randomizar e intercalar celdas;
- bloquear por seed;
- distribuir episodios en varios batches/días;
- modelar batch como fuente de variación.

Dato importante: aunque P3 falló formalmente, los efectos placebo apareados fueron aproximadamente +0.109 en scarce y −0.010 en pleno, bastante menos dramáticos que la diferencia de medianas. “Cualquier consejo mueve” tampoco está todavía demostrado con estabilidad.

## (d) Protocolo mínimo creíble

### Fase 1: autopsia, no confirmatoria

1. Repetir pista actual y libre con trazas, submissions y score por partición.
2. N fijo; no detenerse cuando aparezcan suficientes ceros.
3. Taxonomía de fallos escrita antes de leer.
4. Clasificación ciega de todos los episodios.
5. Determinar si los ceros comparten un template causal/código concreto.

Estos datos no cuentan para validar la pista v2.

### Fase 2: desarrollo separado

6. Diseñar pista v2 sobre mundos/trazas de desarrollo.
7. Verificar que no permite inferir la respuesta sin datos.
8. Elegir control epistémico activo de longitud, tono y esfuerzo comparables.
9. Congelar ambos textos.

### Fase 3: confirmatorio

10. Target y gemelo/control con:

   - misma fachada y carga de implementación;
   - headroom basal 30–70%;
   - misma pista congruente;
   - estructura congelada.

11. Factorial mínimo:

   - target/control;
   - pista dirigida/control epistémico;
   - orden randomizado e intercalado;
   - varios batches;
   - trazas completas.

12. Power formal sobre diferencia de tasas; probablemente decenas por celda, no ocho.

13. Preregistrar:

   - τ de éxito;
   - tasa catastrófica;
   - interacción mínima;
   - análisis ITT;
   - manipulación de conducta;
   - métricas de ejecución;
   - tratamiento de fallos.

### Lectura cerrada

- Pista no cambia conducta → falló la manipulación; no juzga al mundo.
- Cambia conducta, no outcome → mundo/reward no vuelve causal al vicio.
- Mejora outcome también en control → ayuda general.
- Empeora o induce otro vicio → pista inválida.
- Cambia conducta objetivo, mejora solo target y no afecta ejecución → evidencia de validez.
- Recién al replicar en otra estructura y otro modelo → claim serio de constructo.

La intuición de Lucas es salvable, pero solo como una pieza de triangulación. Si “la pista levanta el score” vuelve a ser todo el argumento, van a repetir el mismo error con más n.
