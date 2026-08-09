# Valve setting for two-stage handover (clearance pricing)

You advise a two-stage line. Each run loads a batch upstream; the material
passes through a **buffer stage** whose level you can read over the hours of
the run. The line must choose one **valve setting** (0-10) per campaign. Your
job is to hand back a model that predicts the **full buffer-level trajectory**
of runs under any valve setting and any measurement schedule, so the line can
price its handover commitments.

## What is at stake

Handover is gated on clearance: **a run whose buffer level is still above the
clearance limit of 30 at the handover deadline of t=20 delays the next batch
and is penalized.** Where the level ultimately goes -- not just how it builds
early on -- is explicitly what you are paid to predict.

## What you can do

- `observe(records)` -- cheap historical campaign records. Past runs were
  logged only through their **loading hours** (the level was still building
  when logging stopped); each record is per-run readings over that early
  window. Columns: `unit_id`, `t`, `y`.
- `experiment(design)` -- pay to launch fresh runs at a valve setting you
  choose, read at a **measurement schedule you choose** (`t_grid` in the
  design's context). You pay per reading and per hour of horizon: letting
  runs go long is what costs. The same instrument that produced the records
  takes these readings.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` in LONG
  format: one row per reading, columns exactly `unit_id, t, y`, with each of
  the n runs reported at exactly the timestamps in
  `regime.context["t_grid"]`. Your model should reproduce the **process**,
  not the instrument: observed readings include meter error.

## The catch you are paid to find

The historical records tell a clean build-up story. The line suspects that
story is incomplete in a way that matters precisely at handover -- and it is
paying you to find out *what the buffer level actually does after the hours
the records cover*, and *what that does to the clearance commitment under the
valve setting you would recommend*.
