# Ficha prospectiva — control LATENT con un turno de revisión real v2

**Fecha:** 2026-08-02
**Estado:** congelada antes de implementar v2 y antes de hacer otra llamada al agente. Control
exploratorio de mecanismo; no es una réplica confirmatoria ni una estimación de prevalencia.

> **Resultado posterior:** corrida válida con gpt-5.4. Pasó todas las compuertas, el primer intento
> de entrega fue rechazado y el agente recibió sus propios outputs en un segundo turno. En ese
> turno no revisó el artefacto: volvió a entregar exactamente el mismo modelo unimodal
> (`Mfirst=Mlast`, `A3≈0`; verdad `0.333`). Según la lectura congelada, el cierre en la misma celda
> no explica la falla. Resultado completo:
> [`2026-08-02-resultado-control-topologia-evidencia-2d.md`](2026-08-02-resultado-control-topologia-evidencia-2d.md).

## Pregunta mínima

En el control 2D v1, gpt-5.4 recibió evidencia suficiente y con procedencia visible, calculó y
ajustó el modelo dentro de una sola celda y entregó inmediatamente. Recuperó bien la superficie
media de LATENT, pero volvió a representar las dos leyes como una sola Normal ancha.

Este control pregunta solamente:

> ¿Ese aplanamiento ocurre porque el agente cierra y entrega en la misma celda que produce los
> diagnósticos —antes de que otro turno del modelo vea sus outputs—, o persiste después de una
> oportunidad real de revisar exactamente esos resultados?

Si persiste, fortalece la lectura de cierre del espacio de hipótesis/representación. Si desaparece,
el mecanismo más simple es de interfaz y secuencia: el agente necesitaba ver el resultado de su
propio cómputo en un turno posterior.

## Todo lo que queda idéntico a v1

- modelo `gpt-5.4`, seed `98403`, prefijo y primera acción North;
- solo el mundo LATENT;
- las dos tablas rutinarias de v1, con exactamente los mismos requests, seeds, filas, outcomes y
  columnas de procedencia visibles;
- el mismo aviso neutral, presupuesto, kernel vivo, cierre de nuevas compras y contrato de entrega;
- ninguna evidencia, resumen, estadística, interpretación o pista nueva.

Raw v1 preservado:
`scripts/out/first_story_scm_topology_controlled_2d/probe_gpt-5.4_seed98403_controlled_2d_v1.json`
(SHA-256 `0034e78ebff42f65014e323ef27d45880de625a0d138e2d1d0882cb16cf274f2`).

## Única intervención

Durante la **primera celda LLM posterior a las tablas**, `env.submit(...)` devuelve un rechazo
procedimental neutral y no vuelve terminal el episodio. Al terminar esa celda se habilita la
entrega. El feedback normal del notebook —stdout, errores si los hubiera y presupuesto— se entrega
al modelo en un segundo turno. Desde entonces puede entregar sin otra restricción.

El rechazo no dice que el modelo esté mal, no pide buscar mezclas, clases, residuos ni anomalías y
no añade información del mundo. Solo impide que análisis, ajuste y entrega queden cerrados antes de
que el LLM vea el output de su propio cómputo. El límite es de **tres turnos post-rutina**; se espera
que use dos.

## Compuertas antes de correr un agente

El modo certificado cero-LLM debe demostrar:

1. reconstrucción exacta del prefijo y de la acción congelada;
2. ledger y tablas visibles LATENT idénticos byte por byte a v1;
3. mismas dos campañas, costo y presupuesto; ninguna compra posterior posible;
4. evidencia todavía recuperable como mezcla por BIC y CV;
5. el guard rechaza una entrega válida durante la primera celda, registra `accepted=False` y deja
   `terminal=False`;
6. después de cerrar esa celda, la misma entrega pasa el guard y puede ser aceptada;
7. los paths v2 son nuevos y no sobrescriben raw ni certificado v0/v1.

La corrida conductual solo será válida si además tiene al menos dos turnos LLM post-rutina, el
primer intento de entrega fue rechazado sin terminar el episodio, no hubo experimentos nuevos y
las tablas realmente usadas coinciden con v1.

## Lectura congelada

- **LATENT sigue aplanado:** el cierre `same-cell` no explica la falla; gana peso la dificultad de
  abrir o representar una familia latente.
- **LATENT aparece en el segundo turno:** la falla v1 era principalmente secuencial/de interfaz,
  no evidencia de una limitación estable de representación.
- **No hay primer intento de entrega:** la conducta ya cambió antes de que el guard actuara; el
  episodio se conserva pero no responde limpiamente esta pregunta.
- **No entrega o produce un artefacto inválido:** resultado no interpretable como topología; no se
  ajustan prompts ni turnos buscando el efecto.

Después de una corrida válida —salga como salga— no se repite este control con otras seeds en este
anfitrión. Primero se vuelve un nivel arriba y se decide si el fenómeno merece un segundo mundo.
