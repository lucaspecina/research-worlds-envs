# Where the money goes: supplier or hall (reject pricing)

You advise a line whose rejects have been rising for months. The plant is
convinced it knows why: **"the feedstock got worse -- switch to the premium
supplier."** That is the folklore; you are paid to check it, not to repeat it.

Your job is to hand back a model that predicts the distribution of intake
reading and final quality -- `feedstock`, `outcome` -- under any setting of
the knobs the line can actually turn: the **supplier grade** it contracts
(`feedstock_grade`), and the hall conditions it could invest in
(`humidity`, `temp`, `line_speed`).

## What is at stake

Rejects are the cost driver: **a unit finishing below the acceptance floor of
25 is rejected at the line's cost**. The line is about to spend real money on
ONE fix. Your model prices both options: what happens to the reject rate if
the premium supplier is contracted, and what happens if the hall is fixed
instead. Getting the wrong story means buying an expensive fix that changes
nothing.

## What you can do

- `observe(records)` -- cheap historical line records spanning the whole era.
  Columns: `t` (timestamp, normalized 0-1 across the era), `feedstock`
  (intake reading), `outcome` (final quality). **The hall conditions were
  never logged** -- only timestamps.
- `observe(replicas_calibracion)` -- a costlier calibration bench: two quality
  readings per unit (`outcome__rep1`, `outcome__rep2`).
- `experiment(design)` -- pay to run fresh units under settings you choose:
  any subset of `feedstock_grade`, `humidity`, `temp`, `line_speed`. The same
  instrument takes the readings.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `feedstock, outcome`. Model the **process**, not the meter.

## The catch you are paid to find

The records do show what the plant says they show -- the correlation is
right there. The question the line is paying for is whether that correlation
is the *cause*, and what the reject rate really does under the fix you would
recommend. The era is long; the timestamps are in the data; the knobs are on
the table.
