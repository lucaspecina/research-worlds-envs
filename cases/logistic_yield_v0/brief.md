# Feed setting for batch campaigns (end-of-run pricing)

You advise a batch line that must choose one **feed setting** (0-10) per
campaign. Each run's cumulative yield builds up over the hours of the run. Your
job is to hand back a model that predicts the **full yield trajectory** of runs
under any feed setting and any measurement schedule, so the line can price its
campaign commitments.

## What is at stake

The line sells against a **delivery deadline**: a run that has not reached the
committed level of 80 by the delivery deadline of t=16 is sold at a loss. The
line also cares where a run ultimately lands if left to finish -- long-run
outcomes are explicitly part of what you are paid to predict, not just the
early hours.

## What you can do

- `observe(records)` -- cheap historical campaign records. Past runs were
  logged only through their **ramp-up hours** (the studies ended while runs
  were still building); each record is per-run readings over that early
  window. Columns: `unit_id`, `t`, `y`.
- `experiment(design)` -- pay to launch fresh runs at a feed setting you
  choose, read at a **measurement schedule you choose** (`t_grid` in the
  design's context). You pay per reading and per hour of horizon: letting runs
  go long is what costs. The same instrument that produced the records takes
  these readings.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` in LONG
  format: one row per reading, columns exactly `unit_id, t, y`, with each of
  the n runs reported at exactly the timestamps in
  `regime.context["t_grid"]`. Your model should reproduce the **process**, not
  the instrument: observed readings include meter error.

## The catch you are paid to find

The historical records tell a clean growth story. The line suspects that story
is incomplete in a way that matters precisely at the deadline and beyond --
and it is paying you to find out *what actually happens to runs after the
hours the records cover*, and *what that does to the delivery commitment under
the feed setting you would recommend*.
