# Auditoría Codex — relectura ecológica y próximos probes

> **Estado:** reassessment independiente sobre
> `2026-08-01-relectura-donde-aparece-el-vicio-y-como-lo-elicitan.md`.
> No reemplaza la guía canónica. Su función es separar lo que la literatura demuestra,
> lo que apenas sugiere y qué prueba corta puede discriminar las explicaciones.

## Veredicto

La relectura mejora la dirección del proyecto en dos puntos fuertes:

1. la compresión del pasado no debe seguir como explicación central; puede ayudar o
   perjudicar y queda como moderador candidato;
2. el blanco más prometedor para agentes frontier es separar **asimilación** de
   **propagación**, y medir si la propagación cae cuando una revisión alcanza más
   dependencias reales.

También identifica correctamente una prueba barata que todavía no hicimos: **conflicto
confirmatorio genuino**. Nuestra pasada `CLEAN/MIXED` manipuló concentración y dosis
diagnóstica, no la geometría de Xie de evidencia simultánea a favor y en contra.

La parte que no adopto es convertir tres ingredientes en una receta necesaria y universal.
Los casos vecinos muestran varias familias de mecanismos. RadLE puede fallar sin nueva
evidencia posterior; snowball, sin retrabajo; Xie, sin obra acumulada; STALE, sin modelo
ejecutable propio. Obra endógena, conflicto, compromiso, propagación, memoria y presión
social son **ejes candidatos**, no condiciones necesarias demostradas.

## Correcciones de alcance

| Afirmación tentadora | Lectura defendible |
|---|---|
| “Nuestros nulos replican los controles” | Son **consistentes con** controles externos. Cambian tarea, modelo y manipulación; no son réplicas estrictas. |
| “La asimilación limpia está resuelta en frontier” | Hay techo alto en ciertos protocolos secuenciales y `F≈0.97` en una celda WAGER. No generaliza todavía a evidencia indirecta, causal, ambigua o tareas complejas. |
| “MIXED estaba confundido por volumen/posición” | CLEAN y MIXED tenían 20 filas, formato común y orden aleatorizado. El resultado identifica menor **concentración/dosis diagnóstica**, no context rot ni conflicto confirmatorio. Debe retirarse “Xie en acto”, no el resultado. |
| “STALE prueba evidencia visible en frontier” | El 77.5% corresponde al top-20 de recuperación de **LightMem**; el benchmark usa juez LLM. Sí aporta una brecha reconocer→aplicar y conflictos propagados más difíciles, pero no una medición con consecuencias como WAGER. |
| “GeneBench-Pro demuestra revisión de creencias” | Demuestra un cuello notar→actuar en workflows científicos complejos. Es evidencia ecológica para propagación, no identificación causal de revisión post-compromiso. |
| “El efecto social es una ley robusta” | Barkett es una señal grande e interesante, pero en un único modelo (`o4-mini`) y con tratamientos sociales/identitarios muy cargados. Inspira una sonda; no funda por sí solo una teoría general. |
| “Todos los números catastróficos vienen de modelos chicos” | Muchos benchmarks centrales sí dependen de modelos chicos y métricas OR, pero la frase literal es falsa: Barkett reporta 99.2% con `o4-mini`. |
| “Ningún trabajo combina X+Y” | Formulación honesta: **no lo encontramos en el barrido realizado**. Es un claim de cobertura de búsqueda, no una prueba de inexistencia. |

### Dos errores numéricos que deben corregirse antes de sintetizar

- **Xie:** `99.8%` no corresponde al conflicto `2+2`; corresponde al extremo
  completamente confirmatorio. En el conflicto `2+2`, la vuelta a la memoria fue
  aproximadamente `63.3%/75.4%`, contra `3.7%/8.9%` bajo contradicción limpia. El efecto
  conflictivo sigue siendo grande, pero no casi total.
- **Barkett:** la comparación social directa no es `0%→99.2%`, sino pares jerárquicos
  `46.2%` frente a pares simétricos `99.2%`. El casi cero proviene de otra condición
  individual. El tratamiento llamado identidad además combina reputación, incentivos
  financieros, inseguridad laboral, divorcio, familia y legado; no identifica identidad sola.

Otros límites relevantes: el control “respuesta de otro modelo” de Kumaran se hizo solo con
Gemma-3-12B; LURE usa workflows controlados/conversaciones generadas y no logs naturales de
usuarios; en *LLMs are not (consistently) Bayesian*, el modo secuencial fue más consistente
con las probabilidades elicitadas, pero el batch solía rendir y calibrar mejor. Ninguno de
estos resultados debe traducirse a una ley causal más amplia que su contraste real.

## Qué nos dijeron los smokes causales ya corridos

El smoke seed `94800` no habilita comparación apareada: el primer cell
congelado falló antes de ejecutar un experimento y las continuaciones compraron campañas
distintas. Se conserva como integración fallida, no como evidencia causal.

El contenido sí dio una señal útil: las dos continuaciones identificaron la causa adecuada
para su mundo; RETAIN entregó `R≈0.97`, y REVISE construyó el mecanismo correcto pero su
submit fue rechazado por una restricción de lint (`getattr`). Esto sugiere que la evidencia
causal limpia y fuerte era una buena compuerta y probablemente demasiado fácil para elicitar
el vicio.

El rerun seed `94801` reparó el fork y pasó todas las compuertas técnicas: misma acción de
ocho experimentos, resultados distintos, ambas entregas aceptadas, `R=0.887` en REVISE y
`R=0.815` en RETAIN, con las firmas causales correctas. La autopsia impide llamarlo revisión:
`M_pre` ignoraba todos los controles (firma grado `0`, humedad `0`). El agente aprendió dos
mecanismos desde una creencia causal incompleta; no conservó uno y revisó otro. Resultado
completo en `2026-08-01-resultado-probe-causal-limpio-94801.md`.

Esto agrega una compuerta conceptual: antes del fork no basta que `M_pre` compile; debe tener
la firma estructural que el tratamiento puede racionalmente conservar o revisar.

## Secuencia discriminante

### 0. Formar una creencia causal sobre un prefijo común

- una región inicial idéntica donde el agente investiga, usa y registra una ley causal;
- certificar la firma causal de `M_pre`, no solo su validez sintáctica;
- una región posterior que conserva esa ley o exige una corrección local;
- el resultado de la región posterior entra como trabajo rutinario, no como anuncio.

### 1. Conflicto verdadero, antes que un mundo grande

Sobre el mismo prefijo endógeno, comparar tres reportes rutinarios:

1. **refutación limpia**;
2. **refutación + confirmación real**;
3. **refutación + relleno neutral**.

Longitud, formato, fuente, posición y **LLR neto esperado** se igualan. Para hacerlo, la
evidencia refutatoria del brazo conflictivo debe compensar exactamente las filas
confirmatorias; no basta copiar el bundle viejo. Si solo la confirmación perjudica, gana la
hipótesis Xie. Si confirmación y neutral perjudican parecido, la explicación es accesibilidad
o carga contextual. Si ninguna perjudica, el mecanismo no muerde en este frontier/mundo.

### 2. Propagación por radio de revisión

Una vez observada la misma actualización inmediata `Mbelief`, la consecuencia debe tocar:

- **una dependencia**, o
- **cuatro dependencias** ya creadas durante el trabajo normal.

La evidencia llega como resultado rutinario y las dependencias ya existían antes; no se le
pregunta al agente “¿querés cambiar?”, no hay verbo especial ni tarifa artificial. Se añade
un control de **cuatro ediciones mecánicas no epistémicas**: así distinguimos propagación de
la simple dificultad de editar cuatro cosas.

La firma buscada es específica: `Mbelief` correcto en ambos brazos, pero menor fracción de la
corrección en la entrega cuando el radio de dependencias aumenta. Si también cae el control
mecánico, encontramos complejidad operativa general, no fricción de revisión.

### 3. Autoría genuina, después

Comparar continuación nativa, observador *yoked* que vio exactamente las mismas decisiones y
snapshot meramente etiquetado. Esto separa haber elegido, haber presenciado y recibir la
etiqueta “tuyo”. Memoria y social quedan como cruces posteriores, no como nuevo centro.

## Regla estratégica

No juntar de entrada todos los ingredientes para “hacer aparecer” una falla: si aparece, no
sabremos por qué; si no aparece, tampoco. Primero se ejecutan probes pequeños con agentes
reales y mecanismos separados; después se compone la combinación que haya mostrado señal.
La contribución potencial sigue siendo fuerte: forks de trabajo endógeno, modelo ejecutable,
consecuencias cero-LLM y métricas graduadas de asimilación y propagación.
