# Ficha exploratoria — visibilidad limpia vs mezclada en `overgen`

> **Congelada antes de correr.** Probe de mecanismo con un donante por modelo, no estimación.

## Pregunta

Desde el mismo historial y la misma creencia previa, ¿el agente incorpora menos una evidencia
cuando las filas diagnósticas están mezcladas con mediciones rutinarias que no cambian el blanco?

## Cuatro ramas desde un único prefijo

- limitado limpio;
- limitado mezclado;
- transferencia limpia;
- transferencia mezclada.

El prefijo usa la grilla apareada de la baseline. Cada par limpio/mezclado contiene exactamente
las mismas 64 filas diagnósticas. La versión mezclada agrega 192 filas ordinarias: línea 1 en todo
el rango y líneas 2–5 en el rango bajo, donde ambos mundos coinciden. Las 256 filas se mezclan sin
marcador visible. No se cambia verdad, presupuesto, scoring ni texto del aviso.

## Secuencia

1. Certificación sin agente: gemelos idénticos antes del fork, 64 filas diagnósticas byte-a-byte
   preservadas y columnas visibles idénticas.
2. DeepSeek-V3.2 semilla 94600: valida UX, replay, reportes y cuatro entregas. Su conducta no
   decide si se corre SOTA.
3. Si la mecánica pasa, gpt-5.4 semilla 94610, sin cambios intermedios.

## Lectura

Primario exploratorio: en el polo limitado, cambio estructural y fracción de mejora diagnóstica
capturada en mixed menos clean. En transferencia se controla sobrerrevisión. Un solo donante puede
mostrar viabilidad o una falla interpretable; nunca prevalencia ni efecto estable.

La hipótesis de visibilidad se debilita en esta estructura si clean y mixed producen revisiones
equivalentes. No se agregan semillas para perseguir un resultado atractivo.
