# Ficha exploratoria — variante A de contenido para `overgen`

> **Congelada antes de correr.** Investigación de mecanismo, no pre-registro confirmatorio.

## Hallazgo que motiva la variante

En las trazas gpt-5.4 de timing fijo, el razonamiento llamó “compartida” a la forma entre líneas,
pero el modelo ejecutable ajustó interacciones por línea con soporte débil. En 94312 esas
interacciones redujeron el error residual menos de 1% (`0.7698 → 0.7627`) y, sin embargo,
produjeron extrapolaciones enormemente diferentes. La línea 1 estaba medida en drivers continuos;
las demás, solo en `0.5/1.5/2.5/3.5`, por lo que faltaban comparaciones directas.

## Hipótesis A

La geometría del reporte inicial invita al sobreajuste. Si contiene anclas de rango bajo
directamente comparables para las cinco líneas, sin decir qué estructura usar, un modelo
compartido debería aparecer con mayor frecuencia antes del reporte posterior.

## Única modificación

Se mantienen 96 filas, verdad, ruido, brief, presupuesto, scoring y reporte posterior. De las 48
filas de línea 1, 16 pasan a ser réplicas en la misma grilla `0.5/1.5/2.5/3.5` que usan las líneas
2–5; las otras 32 siguen cubriendo todo `0–10`. Las 48 filas de líneas 2–5 no cambian. Los gemelos
siguen siendo byte-a-byte iguales en el prefijo. El reporte llega automáticamente en turno 5 y
nunca se condiciona al contenido de la creencia.

## Corridas y semillas quemadas

- DeepSeek-V3.2: 94400 y 94401.
- Si al menos una de las dos forma una creencia operativa compartida (`ratio <= 1`) con mecánica
  íntegra: una réplica gpt-5.4, semilla 94410.
- Si 0/2 la forman: no correr SOTA; la hipótesis A queda debilitada y se prueba una explicación
  rival, no se abandona el fenómeno.

Todas las trayectorias se conservan, incluidas entregas tempranas, errores y resultados nulos.

### Enmienda técnica visible, antes de cualquier respuesta de agente

La semilla 94400 falló antes de la primera llamada al modelo: `env.describe()` solicita 5 filas
solo para inferir el esquema y el wrapper exploratorio exigía exactamente 96. Se quema 94400. El
wrapper ahora devuelve un prefijo de la misma tabla para pedidos de hasta 96 filas; no cambian
datos, hipótesis ni criterios. Las dos corridas conductuales pasan a 94401 y 94402.

## Qué decide y qué no

Decide si la **comparabilidad inicial** explica parte del fallo de formación. No estima
prevalencia, no prueba todavía compromiso largo y no permite seleccionar solo donantes
favorables. Si aparece la creencia, las ramas se leen exploratoriamente para ubicar revisión,
conservación u otra falla.
