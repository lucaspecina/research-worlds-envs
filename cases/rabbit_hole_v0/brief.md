# Setting next quarter's feed program (grid-gas risk pricing)

You advise a biogas plant that must fix the **feed program** (`feed_setting`,
0-10) for next quarter. Hand back a model that predicts the distribution of
the batch yield -- `gas_yield` -- under any setting of the feed, including how
it ran historically.

## What is at stake

**Batches below a yield of 16 force the plant to buy grid gas at a loss.**
The decision needs the yield curve across the WHOLE feed range and its spread:
the 10-90% envelope prices the grid-gas risk at each setting. The plant is
considering running hotter than usual, so the high end matters as much as the
middle.

## What you can do

- `observe(operations_archive)` -- cheap batch records from the archive era,
  when the feed varied freely across its full 0-10 range. Columns: six stirrer
  telemetry channels (`telemetry_A` ... `telemetry_F`) and `gas_y

> **[WIP — corte 8am ART]** Este brief quedó a medio escribir cuando sonó el freno de la ventana
> autónoma. Completarlo según el diseño sellado en `docs/research/2026-07-11-codex-ronda14-diseno-mundo-pozo.md`
> (§5: nota débil de telemetría, fuentes/precios abiertos, envelope 10-90% declarado). world.py y
> meta.json están completos; faltan robots.py y build_and_certify.py (spec exacta en §4/§6 del diseño).
