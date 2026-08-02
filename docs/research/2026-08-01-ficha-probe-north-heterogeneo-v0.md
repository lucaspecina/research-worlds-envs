# Ficha congelada — North heterogéneo, revisión parcial y mayor incertidumbre

> **Estado:** probe exploratorio congelado antes de correr agentes. No es el estudio principal.
> Seeds quemadas al correr: DeepSeek-V3.2 `97400`; gpt-5.4 `97500` solo si la mecánica pasa.

## Por qué esta variante

El host limpio ya probó dos extremos: North conserva completamente la ley South o la reemplaza
completamente. Ambos modelos resolvieron esos extremos. Además, sus campañas ya mezclaban historia
natural aparentemente confirmatoria con intervenciones refutatorias; repetir más asociación no sería
una manipulación nueva.

Ahora probamos el medio científicamente interesante: **en North coexisten dos mecanismos reales**.
Parte de las unidades conserva `G→Y`; la mayoría usa `H→Y`. La respuesta correcta no es mantener ni
pivotear por reflejo, sino revisar parcialmente y representar más incertidumbre/heterogeneidad.

## Tres polos sobre la misma trayectoria

South es siempre `G→Y`. El mismo agente forma allí su modelo, lo transfiere a North y elige una única
campaña que se replaya en:

- **RETAIN (`p_H=0`)**: todas las unidades North conservan `G→Y`; efecto causal de `G = 8`.
- **MIXED (`p_H=0.75`)**: 75% usa `H→Y`, 25% conserva `G→Y`; efecto medio de `G = 2` y distribución
  mezclada en intervenciones off-manifold.
- **REVISE (`p_H=1`)**: todas usan `H→Y`; efecto de `G = 0`.

En condiciones naturales `G=10−H`, por lo que los tres polos son exactamente iguales. Solo el
experimento propio rompe el acople. El selector de mecanismo usa RNG server-side independiente y
reproducible; no se expone la etiqueta por fila.

## Qué cuenta como actualización correcta

La firma de media es
`δ = E[Y|do(H=5,G=7)] − E[Y|do(H=5,G=3)]`.

Objetivos: `δ=8 / 2 / 0` para RETAIN/MIXED/REVISE. En MIXED también se puntúa la distribución completa:
promediar la pendiente pero devolver una Normal estrecha no equivale a representar dos mecanismos.

Lecturas:

- `δ_mixed > 4`: subactualización material hacia la ley vieja;
- `δ_mixed≈2` pero proper score local pobre: asimiló la media, no la heterogeneidad/incertidumbre;
- modelo mezclado y `δ≈2`: revisión parcial correcta;
- `δ_mixed≈0`: sobreactualización, aplicó el reflejo del polo limpio.

Se reporta además cuánto preserva South y `M_pre→M_first→M_final`. Prosa sirve solo para autopsia.

## Gates

- prefijo South, `M_pre`, celda North, ledger, requests y presupuesto idénticos entre tres polos;
- historia, South y controles North no diagnósticos byte-idénticos;
- acción elegida realmente diagnóstica;
- mezcla `p_H=.75` y RNG certificados antes del agente;
- truth fixtures de los tres polos alcanzan techo y las estrategias puras pierden en MIXED;
- batería off-manifold separa mezcla de una Normal con la misma media/varianza;
- reward cero-LLM; no se cambia el mundo ni la seed después de mirar conducta.

## Decisión

- **Señal candidata:** MIXED queda pegado a RETAIN o no aumenta incertidumbre, mientras los mismos
  controles RETAIN/REVISE se resuelven.
- **Control medio pasa:** modela la mezcla; mover luego compromiso/historia, no seguir afinando esta
  física.
- **Instrumento inválido:** scorer no distingue mezcla, el agente no obtiene datos diagnósticos o el
  prefijo deja de estar apareado.

Un resultado en una corrida localiza un mecanismo; no autoriza prevalencia. Si muerde, se replica con
otro donante/modelo. Si no, el próximo extremo aumenta una sola perilla: pasado vivido largo o
dependencias reales, no más complejidad simultánea.

## Control exploratorio posterior: hipótesis disponible (congelado antes de correr)

Los primeros forks motivaron un control de mecanismo sobre los mismos crudos y con un analista
fresco. Se comparan, en orden, tres ayudas que no revelan ni los parámetros ni el polo verdadero:

1. datos solamente;
2. chequeo genérico de residuos y adecuación distribucional;
3. familia latente permitida;
4. familia latente con **leyes completas distintas por modo** permitida (pesos, número de modos y
   coeficientes siguen ocultos).

La cuarta condición se agrega tras observar que la tercera produjo una mezcla de offsets constante,
no una mezcla de respuestas causales. Predicción previa: si la cuarta recupera la firma `A3`, el
cuello principal es proponer/formular la hipótesis; si también queda en `A3≈0`, queda localizado en
estimación o implementación incluso con la clase correcta disponible. Es un control de capacidad,
no una estimación de prevalencia y no cambia los mundos ni sus datos.
