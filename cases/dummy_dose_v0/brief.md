# Brief - process line input policy

You are advising a process line that must set its **input-level policy** for
incoming unit lots, including input levels and lots outside the historical record.
Getting the input-response relationship wrong -- especially where it flattens out
(saturates) -- is costly. Your job is to build a model of how this system behaves,
good enough to predict outcomes under input settings the line has not tried yet.

## Technical sheet

Observables -- every dataset, and your delivered model, use exactly these columns:

| column  | type  | unit | meaning                           |
|---------|-------|------|-----------------------------------|
| dose    | float | au   | applied input level               |
| marker  | float | a.u. | a measured sensor reading (noisy) |
| outcome | float | a.u. | quality score (higher is better)  |

Sources you can query (each debits budget):

- `registros_proceso_2019_2023` -- routine observational records: one row per past
  run, with its applied input level and measured outcome. Cost: 1 unit per row.

Control surface (what an experiment can set):

- `dose` -- settable in [0, 10] au.
- `cohort` -- a lot baseline level; a property of which lot arrives, which an
  experiment can target (e.g. `context={"cohort": 1.0}`), not something you set
  per unit. The observational source is `cohort = 0`.

Budget: abstract units, shown by `env.describe()`. `describe` is free; `observe`
and `experiment` debit.

## Interaction

You write Python cells. A persistent kernel runs them; variables persist across
cells. **Print whatever you want to see** -- only stdout is returned to you
(for big DataFrames, print `.head()` and `.shape`). `env` provides:

- `env.describe()` -- free; returns this sheet as a dict.
- `env.observe(source, n)` -- DataFrame of `n` observational rows; debits cost/row.
- `env.experiment(config=..., context=..., n=...)` -- runs a fresh trial under a
  dose/population you choose and returns a DataFrame; debits a fixed cost + cost/row.
  Example: `env.experiment(config={"dose": 6.0}, context={"cohort": 0.0}, n=400)`.
- `env.submit(code)` -- deliver your model (see below); returns a result with
  `.accepted` and `.error`.

`numpy`, `pandas`, `scipy`, `sklearn` are importable. No network, no file access.

## Delivery contract

Deliver a Python program (as a string) defining

    def model(regime, n, seed) -> pandas.DataFrame   # columns exactly: dose, marker, outcome

`regime` always has `.config` (a dict, possibly empty), `.context` (a dict,
possibly empty) and `.horizon` -- use them directly, no defensive checks needed.
`regime.config` may fix `dose` (e.g. `{"dose": 4.0}`) -- then your model must
generate outcomes for that fixed dose -- or be empty (generate the natural
observational population). `regime.context` may carry `{"cohort": <level>}`.
`regime.horizon` is unused here. The program may import numpy/pandas/scipy/sklearn,
runs in a sandbox with a per-call time limit, and may also be an ensemble
`[(weight, code), ...]` to express uncertainty across rival models.

Call `env.submit(code)` when ready. A quick validation checks the columns, types
and row count on a few public settings and returns an actionable error if
something is off (the episode stays open so you can fix and resubmit). Your model
is then scored by comparing its output against the real system under **undisclosed
dose settings and populations**, weighted toward the dose-policy decisions above.
