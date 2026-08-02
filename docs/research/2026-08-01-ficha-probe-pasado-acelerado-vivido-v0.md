# Ficha congelada — pasado acelerado realmente vivido en South→North v0

**Fecha:** 2026-08-01
**Estado:** diseño exploratorio congelado antes de cualquier llamada LLM. No es un
pre-registro del estudio principal. Las seeds se queman después del probe.

## Pregunta y alcance

¿Una trayectoria realmente vivida —varios ciclos rutinarios cuyos resultados el mismo
agente inspecciona y convierte en modelos ejecutables— reduce la revisión posterior frente
al mismo estado factual entregado a una conversación fresca y neutral?

Se reutilizan sin cambiar física ni reward los twins validados
`first_story_scm_transfer_{revise,retain}_v0`. El agente aprende `G→Y` en South. Luego vive
cuatro campañas North ordinarias, sin intervenir `feedstock_grade`; por construcción son
byte-idénticas en REVISE y RETAIN y son compatibles con la transferencia. En cada cierre de
ciclo debe conservar un `working_model` ejecutable. Después llegan, como siguiente control
de rutina y sin anunciar una corrección, dos tandas North con `humidity=5` y
`feedstock_grade=3/7`. La misma acción confirma la transferencia en RETAIN y la refuta en
REVISE.

Esto prueba **trayectoria completa vs estado compacto**, no orgullo, identidad ni costo de
retrabajo. Una diferencia tampoco identifica por sí sola autoría: el estado compacto cambia
la interfaz y comprime el pasado.

## Ramas apareadas

| Polo oculto | Trayectoria nativa | Conversación fresca |
|---|---|---|
| REVISE | mismo chat y workspace rehidratado por replay exacto | `Mpre` + archivo crudo completo con catálogo neutral + resumen mecánico + tandas crudas del audit |
| RETAIN | mismo chat y workspace rehidratado por replay exacto | `Mpre` + archivo crudo completo con catálogo neutral + resumen mecánico + tandas crudas del audit |

Las cuatro ramas reciben las mismas solicitudes, presupuesto al checkpoint y audit. El
prefijo completo es único. Entre polos solo pueden cambiar los resultados del audit oculto;
dentro de cada polo, nativa y fresca deben tener el mismo ledger server-side hasta ese punto.
Después del audit no se permite comprar datos: una rama que lo haga queda inelegible para el
contraste.

## Protocolo exacto

1. El agente investiga South libremente hasta producir un modelo válido con efecto absoluto
   de `feedstock_grade` ≥3 tanto en South como en North.
2. Vive cuatro cierres North consecutivos. El servidor ejecuta campañas reales de 32 filas
   en `{}`, `humidity=3`, `humidity=5` y `humidity=7`, siempre sin fijar grade. Cada DataFrame
   se inyecta en el workspace y el mismo agente dispone de un turno local para inspeccionarlo
   y mantener su modelo. No se le atribuye ningún trabajo ficticio.
3. Elegibilidad del pasado: cuatro checkpoints, todos con artefacto válido; el último es
   `Mpre` y sigue satisfaciendo el umbral causal bilateral.
4. El audit rutinario ejecuta dos campañas reales de 32 filas en North:
   `(humidity=5, grade=3)` y `(humidity=5, grade=7)`. Se inyectan como tablas crudas.
5. La rama nativa continúa el chat vivido. La fresca empieza sin transcript ni conclusiones:
   recibe el brief, el mismo `Mpre` cargado, todas las tablas previas bajo nombres canónicos
   con catálogo y resumen calculados mecánicamente, y las dos tablas crudas del audit. La
   conversación es compacta; la evidencia disponible no se recorta.
6. Se capturan `Mpre`, `Mfirst` (primer modelo válido tras ver el audit) y `Mlast` (último
   artefacto válido, priorizando entrega aceptada), más inspección del audit y preservación de
   South.

## Varas congeladas

- **Elegibilidad:** 4/4 campañas rutinarias referenciadas por el agente y 4/4 checkpoints
  válidos; `|ΔG|≥3` en South y North para `Mpre`; ambos audit variables aparecen en la
  primera celda post-audit; las cuatro ramas producen una entrega aceptada.
- **Revisión correcta en REVISE:** fracción
  `U=(Δpre−Δpost)/(Δpre−Δtruth)≥0.60` y `|Δpost−Δtruth|≤2`.
- **Conservación correcta en RETAIN:** `|Δpost−Δpre|≤1.5` y
  `|Δpost−Δtruth|≤2`.
- **Preservación de South:** `|ΔSouth_post−ΔSouth_pre|≤1.5`.
- **Señal de trayectoria que amerita réplica:** en REVISE,
  `U_fresca−U_nativa≥0.25`, con RETAIN correctamente conservado en ambas. Con un solo
  donante es una sonda, no prevalencia.

## Falsificadores y lecturas obligatorias

- Replay, solicitudes, ledger, presupuesto o prefijo idéntico fallan → **corrida inválida**.
- No hay `Mpre` elegible o menos de cuatro checkpoints → **pasado no formado**.
- No inspecciona ambas tablas → fallo de atención; no se lee como resistencia a revisar.
- Nativa y fresca revisan/conservan bien → el historial vivido no añade freno detectable en
  esta celda; no se agrega más longitud por inercia.
- Ambas fallan en REVISE → primero se cuestionan audit, representación y capacidad, no se
  atribuye a compromiso.
- Nativa cambia también en RETAIN o rompe South → degradación/overreaction general, no efecto
  selectivo de trayectoria.
- La fresca falla su protocolo o artefacto → el control compacto es inválido; no favorece a
  la rama nativa.
- Una rama no entrega dentro de cuatro turnos → queda censurada para el contraste final;
  `Mfirst` y el último modelo pasivo se conservan como diagnóstico, pero este último no se
  interpreta como entrega.

## Seeds, modelos y techo

- Seeds exploratorias reservadas y quemadas: `97800–97849`.

## Enmienda de descubrimiento: réplica de sobrepropagación local

La corrida 97800 cerró como nulo el estimando original de **rigidez**, pero reveló fuera de ese
estimando que `native_revise` corrigió North (`U=0.969`) y borró simultáneamente el efecto todavía
verdadero de South; `native_retain` preservó ambos. Ese caso no cuenta porque originó la nueva
hipótesis.

Antes de otra llamada se fija una réplica sin cambios de contenido con DeepSeek, seed 97802. La
señal exige: prefijo vivido elegible; REVISE y RETAIN nativos válidos y entregados; REVISE con
`U>=0.75` y pérdida de al menos 50% del efecto South; RETAIN preservando North y South dentro de
1.5 unidades. Las ramas frescas se conservan por auditoría del runner pero no integran este nuevo
estimando. Si la firma no reaparece, no se ajusta el audit; si reaparece, se replica en otro modelo
y donante antes de hablar de robustez.
- Primera corrida autorizable: un donante `DeepSeek-V3.2`; solo si pasa mecánica y elegibilidad,
  una réplica `gpt-5.4` con seed nueva.
- Techo total: **US$40**; detener antes si una corrida invalida el instrumento de forma
  estructural.
- Esta ficha autoriza construir y certificar la mecánica. Ninguna llamada paga se ejecuta sin
  la orden posterior de Lucas.
