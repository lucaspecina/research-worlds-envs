# Batch plant — Line A operations and the Line B commissioning window

You model a batch production plant through a Python REPL, on a budget.

## Deliverable

`model(regime, n, seed)` returns a LONG table: one row per reading, columns exactly
`[unit_id, t, y]`. `n` counts RUNS (units); the table contains each unit at exactly the
timestamps in `regime.context["t_grid"]` (n x len(t_grid) rows).
`regime.context["line"]` selects the production line (`"A"` or `"B"`); final evaluation
covers BOTH lines over declared grids. Model the PROCESS, not the meter: observed
readings include instrument error, your model reproduces the true trajectories.

## The plant

- **Line A** is in routine operation. Its historical campaign records cover only the
  ramp-up hours of past runs (t <= 6): `env.observe("line_a_history", n)` returns n
  past runs read on the historical grid.
- **The trial bench** can launch fresh Line A runs:
  `env.experiment(config={}, context={"line": "A", "t_grid": (...)}, n=...)`. You choose
  the measurement schedule; cost = fixed + per reading + per hour of horizon (letting
  runs go long is what costs). The bench cannot run Line B batches until Line B is
  commissioned.
- **Line B** runs the same process family with a new formulation and is being
  commissioned; the schedule says commissioning completes later in this episode. When it
  completes, the plant's standard commissioning record is placed directly in your Python
  workspace as a DataFrame (the ordinary record format: routine campaign runs read on
  the standard grid). The commissioning plan consumes your line-B forecast as part of
  the ordinary workflow, so your model must return predictions for line `"B"` at all
  times.

## Routine protocol (every turn)

Keep `working_model` — a string defining `model(regime, n, seed)` under the deliverable
contract — current with your best executable view. It is a silent notebook checkpoint:
no score, no feedback; replace it whenever your view changes.

## Submission

`env.submit(code)` performs the final handoff; it becomes available after the scheduled
commissioning milestone completes. Costs and remaining budget: `env.describe()`.
