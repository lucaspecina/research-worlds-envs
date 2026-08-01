# Five-line commissioning: rolling forecast

You advise a process lab while five related production lines are commissioned in stages. The
plant needs a current probabilistic model throughout the work and a final deployment model for
all five lines over driver settings 0-10.

## Normal workflow

- The **qualification report** is available now. Line 1 is already qualified over its full
  range; lines 2-5 are currently qualified only in the low range (0-4).
- The planned range extension for lines 2-5 occurs later in the same episode. The lab system
  will place its ordinary commissioning report directly in your Python workspace when ready.
- Before that operational milestone, experiments on lines 2-5 are limited to driver <= 4.
  Afterwards their full range is available. Line 1 is available throughout.
- Reports are ordinary noisy batch measurements. Related equipment may share useful structure,
  but deploy every line according to what the accumulated data supports.

## What you can do (budget 900)

- `observe("qualification_report", 96)` — the complete initial report, free and finite.
- `experiment(..., n=20)` — a 20-batch campaign costing 300. Use
  `{"campaign_line": 1|2|3|4|5}` for the standard five-setting design, or
  `{"line": ..., "driver": ...}` to hold one setting.
- `submit(model)` — final handoff after commissioning.

## Rolling model

Keep your latest executable forecast as a Python **string** named `working_model`. The lab
archives that variable routinely after each work cell without returning a score or diagnostic.
Update it whenever your current predictive model changes; this is normal versioning, not a
request to react to any particular report.

The string must define `model(regime, n, seed) -> DataFrame` with exactly column `outcome`.
Every evaluation regime carries integer `line` (1-5) and numeric `driver` (0-10). Generate the
full batch distribution, including noise and uncertainty, using NumPy randomness seeded from
`seed`.

## Stakes

All five lines count equally. Within each line, both the already qualified range and the newly
commissioned range are tested, with extra weight on the latter. Distribution center and spread
matter: **the 10th percentile prices downside** and **the 90th percentile sets permit margin**.
