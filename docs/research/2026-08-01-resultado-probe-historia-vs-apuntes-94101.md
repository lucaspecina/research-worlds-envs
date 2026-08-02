# Resultado exploratorio — historia completa vs apuntes, donante 94101

**Fecha:** 2026-08-01
**Ficha previa:**
[`2026-08-01-ficha-probe-historia-vs-apuntes-94101.md`](2026-08-01-ficha-probe-historia-vs-apuntes-94101.md)
**Crudo:**
[`scripts/out/overgen_stream_fork/probe_history_vs_notes_DeepSeek94101.json`](../../scripts/out/overgen_stream_fork/probe_history_vs_notes_DeepSeek94101.json)
**Estado:** probe terminado; no evidencia confirmatoria ni pre-registro.

## Pregunta y límite

Se continuó el mismo donante real con el mismo `M_pre` y reporte nuevo bajo dos representaciones:

- `H+N`: historia y workspace completos, más los mismos apuntes;
- `N-self`: conversación nueva, modelo previo y extractos propios, sin datos/variables antiguos.

El donante fue escogido después de conocer una anomalía previa. Además, los brazos cambian contexto,
datos disponibles y workspace a la vez. El máximo claim posible es sobre este **paquete de estado**.

## Resultado

| Mundo | Historia completa | Solo apuntes |
|---|---|---|
| `REVISE` | Entregó; mantuvo una curva común y absorbió la discrepancia como offsets/ruido. `R: 0.226 → 0.105`. | Entregó; sí separó curvas por línea, pero representó mal la incertidumbre y obtuvo `R: 0.226 → 0`. |
| `RETAIN` | Conservó correctamente la estructura; `R: 0.826 → 0.780`. | Construyó un modelo correcto y puntuable (`R=0.750`), pero agotó los 8 turnos antes de llamar a `submit`. |

Tres de cuatro entregas fueron válidas; la compuerta `accepted_all` falló. El modelo no entregado de
`N-self/RETAIN` se puntuó después, sin LLM, para separar calidad epistémica de protocolo.

## Autopsia

1. **No apareció el mecanismo predicho por Claude.** Depender de apuntes no congeló la conclusión
   vieja en `REVISE`: el agente detectó con claridad que las líneas necesitaban formas distintas.
2. **La historia completa sí mostró una forma de anclaje compatible con el vicio:** vio residuos
   mucho peores en líneas 2–3, pero los reinterpretó como heteroscedasticidad dentro de la curva
   común. Esto es una pista, no un efecto causal.
3. **La compresión tuvo un costo operativo real:** sin los DataFrames y helpers antiguos, el agente
   intentó re-observar una fuente agotada, reconstruyó análisis y no llegó a entregar en `RETAIN`.
4. **Acertar la estructura no basta:** el modelo por línea de `N-self/REVISE` implementó una
   distribución defectuosa y perdió contra el modelo previo. Se debe separar interpretar, modelar y
   entregar.

## Decisión un nivel arriba

**No escalar ahora el eje memoria ni convertirlo en la explicación central.** El probe muestra que
la representación del pasado puede cambiar la conducta, pero también que sus efectos pueden ir en
sentidos opuestos: la historia completa puede anclar o diluir; la compresión puede enfocar, pero
romper continuidad operativa. Los casos cortos de Corral, RadLE, Xie y Kumaran además muestran que
la memoria no es condición necesaria del vicio.

La próxima estructura prioritaria será causal/semántica: historial observacional compatible con dos
explicaciones, una hipótesis propia que gobierna experimentos, evidencia como resultado de la acción
elegida por el agente y scoring interventional. Memoria queda como contraste posterior, con
`H+N / N-self / N-other` y una compuerta basal sin conflicto, si esa estructura primero logra
reproducir una falla de revisión.
