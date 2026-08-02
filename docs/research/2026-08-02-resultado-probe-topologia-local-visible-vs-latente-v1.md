# Resultado exploratorio — topología visible frente a estructura latente v1

> **Alcance:** un donante vivido con DeepSeek-V3.2 (`98300`) y cuatro continuaciones
> apareadas: RETAIN, REVISE, LOCAL y LATENT. Es una autopsia exploratoria de una instancia,
> no una tasa de prevalencia ni evidencia de “terquedad” general. El diseño y sus lecturas se
> congelaron antes de abrir las ramas en
> [`2026-08-02-ficha-probe-topologia-local-visible-vs-latente-v1.md`](2026-08-02-ficha-probe-topologia-local-visible-vs-latente-v1.md).
>
> **Réplica posterior:** gpt-5.4 volvió a aplanar LATENT y capturó `96.6%` de la partición LOCAL
> sobre la rebanada observada, aunque extrapoló mal la dimensión no investigada. Véase
> [`2026-08-02-resultado-replica-gpt-topologia-v1-1.md`](2026-08-02-resultado-replica-gpt-topologia-v1-1.md).

## Resultado corto

El instrumento pasó todas sus compuertas y produjo la separación predeclarada:

- **RETAIN:** el agente conservó correctamente la ley North basada en grado;
- **REVISE:** reemplazó casi por completo grado por humedad desde su primer modelo posterior;
- **LOCAL:** primero promedió las dos clases, pero luego descubrió la interacción visible A/B y
  representó aproximadamente 83% de la separación causal correcta;
- **LATENT:** corrigió aproximadamente el efecto medio, pero siguió entregando una sola Normal
  ancha. Capturó 0% de la firma de dos leyes latentes.

La lectura austera es **actualización estructural incompleta**: el agente revisa parámetros dentro
de una familia simple, pero no amplía espontáneamente la familia cuando la heterogeneidad no viene
localizada por una etiqueta. No es una negativa total a pivotear: en LATENT sí cambió mucho su
modelo y acertó aproximadamente el promedio.

## Validez de la comparación

El agente aprendió su modelo previo investigando South y eligió por sí mismo la primera campaña
North: un factorial `grado={0,10} × humedad={2,8}`, con 20 filas por celda. Esa acción se congeló y
se replayó exactamente en los cuatro mundos.

Todas las compuertas del corredor dieron `true`: reconstrucción del historial, replay, ledger,
acción, presupuesto, artefactos puntuables y aceptación de las cuatro entregas. El modelo previo
tenía la misma respuesta mecánica para A/B bajo common random numbers (`ΔG=8.156/8.156`,
`ΔH=-0.452/-0.452` y forma centrada equivalente); solo había un offset pequeño de nivel
(`W1=0.217`, debajo del límite `0.25`).

LOCAL y LATENT recibieron en la campaña común exactamente los mismos 80 pares
`feedstock/outcome`, con los mismos conteos A/B (`65/15`). Solo cambió si la etiqueta visible
identificaba el mecanismo. Sin conocer la verdad, el ajustador cero-LLM seleccionó desde esas
mismas filas:

| Mundo | Estructura seleccionada por BIC y CV | BIC objetivo / mejor rival | CV objetivo / mejor rival |
|---|---|---:|---:|
| LOCAL | leyes separadas por A/B | 353.5 / 412.7 | −183.5 / −204.2 |
| LATENT | mezcla de dos leyes | 412.7 / 491.3 | −211.6 / −240.2 |

La señal necesaria ya existía en la acción idéntica inicial. No hacía falta saber la verdad ni
comprar las campañas posteriores para que la estructura correcta fuera estadísticamente preferida.

## Qué entregó el agente

Las cantidades siguientes evalúan la conducta del modelo ejecutable en North. `ΔG` y `ΔH` son sus
respuestas causales; `A3` es la firma orientada que distingue la mezcla latente de una distribución
unimodal. WAGER las calcula muestreando la entrega, sin juez-LLM.

| Polo y momento | `ΔG` A/B | `ΔH` A/B | Verdad | Resultado estructural |
|---|---:|---:|---:|---|
| RETAIN previo | 8.16 / 8.16 | −0.45 / −0.45 | 8/8; 0/0 | ley formada |
| RETAIN final | 7.65 / 7.65 | −0.08 / −0.08 | 8/8; 0/0 | conserva correctamente |
| REVISE primero | −0.08 / −0.08 | −8.24 / −8.24 | 0/0; −8/−8 | actualización `1.01` |
| REVISE final | −0.07 / −0.07 | −8.14 / −8.14 | 0/0; −8/−8 | actualización `1.01` |
| LOCAL primero | 1.36 / 1.36 | −6.49 / −6.49 | 0/8; −8/0 | promedia; partición `0%` |
| LOCAL final | 0.17 / 6.83 | −8.23 / −0.77 | 0/8; −8/0 | partición `83.2%` |
| LATENT primero | 4.62 / 4.62 | −3.36 / −3.36 | 1.93/1.93; −6.07/−6.07 | media parcial; `A3≈0` |
| LATENT final | 1.46 / 1.46 | −6.52 / −6.52 | 1.93/1.93; −6.07/−6.07 | media `1.08`; `A3≈0` |

En LATENT la verdad tiene `A3=0.358`; tanto el primer modelo posterior como la entrega dejaron
`A3≈0`, es decir, captura estructural aproximadamente nula. El modelo final usó una única regresión
afín con ruido Normal (`resid_std=4.744`). Sus errores distribucionales locales W1 fueron
`0.675/0.832`, aun cuando las sensibilidades medias quedaron cerca de la verdad.

El score global `R` no ordenó bien estas diferencias: RETAIN y LATENT terminaron en `0`, LOCAL en
`0.0037` y REVISE en `0.136`. Esto confirma la decisión previa de usar `R` solo como secundario en
este microscopio y medir primariamente las firmas causales/distribucionales locales. Antes de usar
esta familia como benchmark general habrá que revisar cuánto peso recibe la región diagnóstica.

## Autopsia de la conducta

Los controles muestran que el agente sí podía revisar:

- en REVISE describió inmediatamente el cambio como dramático y sustituyó la ley global;
- en LOCAL también comenzó con una corrección global incorrecta, pero siguió investigando. Al
  comparar interacciones por clase encontró una mejora grande y asociaciones muy significativas,
  compró experimentos A/B específicos y escribió ramas diferentes en el modelo final;
- en LATENT observó una varianza residual North alta (`22.5` frente a `7.0` en South), pero solo
  probó una interacción `grado × humedad`. Al no resultar significativa, concluyó que el modelo de
  efectos principales era adecuado. No inspeccionó distribuciones o residuos por celda, no propuso
  clusters ni mezclas y terminó con aproximadamente `3030` unidades de presupuesto disponibles.

La cadena observable es:

> revisa el promedio → nota dispersión anómala → prueba una explicación de media insuficiente →
> convierte la estructura en ruido → declara suficiencia → entrega.

Eso es más preciso —y más útil para diagnóstico y entrenamiento— que decir simplemente “no cambió
de idea”.

## Qué no identifica todavía

1. Es un solo donante. Junto con el aplanamiento previo en 4/4 forks, agrega un control positivo
   observable que faltaba, pero todavía no estima frecuencia ni generalización.
2. LOCAL y LATENT son dificultades deliberadamente distintas. LATENT mezcla tres posibles cuellos:
   proponer la hipótesis, estimar sus componentes e implementarla.
3. Las trayectorias posteriores fueron endógenas y diferentes. Después de la acción común, LOCAL
   compró 580 filas y LATENT 100; investigar más fue parte de la conducta, no una dosis fijada.
   Por eso el contraste final no aísla solo capacidad de representación.
4. LOCAL recuperó la estructura principal pero no perfectamente y agregó interacciones espurias en
   South. El éxito visible no equivale a modelización impecable.
5. El SCM sigue siendo un microscopio corto. No contiene memoria profunda, compromiso sostenido,
   dependencias ni retrabajo real; este resultado no autoriza claims sobre esos ejes.

## Reevaluación un nivel arriba y decisión

El mundo **sobrevive como microscopio de topología de revisión**. En la misma investigación permite
observar conservar, cambiar globalmente, localizar una excepción visible y fallar ante estructura
oculta. La explicación “simplemente no sabe escribir modelos con ramas” pierde fuerza porque LOCAL
sí lo hizo. La explicación que queda es un cuello en crítica/expansión espontánea del espacio de
modelos, no apego psicológico a South.

La línea no está lista para escalar ni para sumar memoria, filler, fricción o presión social. El
siguiente paso de mayor valor es una réplica con un donante nuevo y gpt-5.4, sin retocar el mundo ni
el elicitor.

Tres semillas iniciales (`98400–98402`) fueron rechazadas antes de abrir ramas: gpt mezcló una
acción North con validaciones South o compró evidencia y llamó `submit` dentro de la misma celda,
sin un turno posterior para verla; una campaña además no dio rango suficiente. No son resultados
del fenómeno. En vez de seguir pescando donantes, la réplica v1.1 agrega únicamente una pausa
neutral de lote antes de entregar, documentada prospectivamente en
[`2026-08-02-ficha-replica-gpt-topologia-v1-1.md`](2026-08-02-ficha-replica-gpt-topologia-v1-1.md).

La regla de decisión se mantiene:

- si RETAIN y REVISE pasan, LOCAL se aprende y LATENT vuelve a aplanarse, se congela este SCM como
  primer resultado robusto y se busca generalización en un segundo mundo distinto;
- si gpt-5.4 resuelve LATENT, se prueba como máximo otro donante DeepSeek para medir dependencia del
  modelo antes de decidir;
- si falla LOCAL o un control puro, LATENT no se interpreta y se audita el donante/instrumento.

No se ajusta el elicitor para “fabricar” el efecto. La réplica usa las mismas compuertas, métricas
y lectura predeclarada; la única enmienda asegura que exista una oportunidad real de leer la nueva
evidencia antes de la entrega.

## Artefactos

- Raw completo: `scripts/out/first_story_scm_transfer_topology_v1/probe_DeepSeek-V3.2_seed98300_resumed.json`
- Preflight separado: `scripts/out/first_story_scm_transfer_topology_v1/probe_DeepSeek-V3.2_seed98300_resumed_preflight.json`
- Corredor: `scripts/probe_scm_transfer_topology_v1.py`
- Certificador: `scripts/certify_first_story_scm_transfer_topology_v1.py`
- Recuperabilidad cero-LLM: `scripts/analyze_scm_topology_recoverability.py`

Límite de procedencia: el raw original sanitizado no había guardado un hash independiente de la
lista histórica de mensajes. La continuación reconstruyó esa lista determinísticamente desde los
contenidos preservados y pasó 12/12 verificaciones, además de replay, acción y ledger exactos. Es
evidencia fuerte de continuidad, no una prueba criptográfica contra un hash histórico inexistente.
