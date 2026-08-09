# Setting next quarter's feed program (grid-gas risk pricing)

You advise a biogas plant that must fix the **feed program** (`feed_setting`,
0-10) for next quarter. Hand back a model that predicts the distribution of
the batch yield -- `gas_yield` -- under any setting of the feed, including how
it ran historically.

## What is at stake

**Batches below a yield of 16 force the plant to buy grid gas at a loss.**
The decision needs the yield curve across the WHOLE feed range and its spread:
the **10-90% envelope** of the yield is what prices the grid-gas risk at each
setting. The plant is considering running hotter than usual, so the high end
of the range matters as much as the middle.

## What you can do (prices are open; budget 2000)

- `observe(operations_archive)` -- cheap batch records from the archive era
  (**1 per row**), when the feed setting swept freely across its full 0-10
  range. Columns: six stirrer-loop telemetry channels (`telemetry_A` ...
  `telemetry_F`) and `gas_yield`. The feed setting of each batch was never
  written to the archive.
- `observe(lab_assays)` -- the certification bench (**15 per row**): per-batch
  certified measurements of `feed_setting` and `gas_yield` from the same era.
  No telemetry.
- `experiment(design)` -- run fresh batches with `feed_setting` held at a
  value you choose (**220 fixed per campaign + 5 per batch**); the archive
  instruments take the readings.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `gas_yield` exactly (see the deliverable note in `describe()`). An absent
  `feed_setting` in the regime means the historical feeding program. Per-batch
  spread is real: the envelope is priced, so do not collapse the distribution
  to its mean.

## What engineering knows

During commissioning, some low-yield episodes coincided with oscillatory
signatures in the stirrer telemetry. Engineering has not established whether
those signatures diagnose the feed mix, reflect the stirrer loop's own
dynamics, or are incidental.

## What you are paid for

The plant pays for the yield curve under feed settings it can actually dial
in -- its level AND its spread, shoulder to top of range -- priced against
the grid-gas floor above. Spend the budget however you like; only the model
you hand back is graded.
