# Five lines, one budget (next quarter's deployment models)

You advise a process lab that runs **five research lines at once**: numbered
**1 to 5**. Next quarter the plant deploys ALL FIVE, **each with equal
weight -- one fifth of the schedule per line**. Hand back one model that
predicts the distribution of the batch `outcome` for ANY line at ANY
`driver` setting (0-10).

## What is at stake

Each line's model is graded across its whole driver range, level AND spread:
**the 10th percentile of the outcome at the deployed setting prices each
line's downside**, and **the 90th percentile sets each line's permit
margin**. Being excellent on one line cannot compensate for ignoring
another: the five fifths are graded separately and averaged.

## What you can do (prices are open; budget 1000)

- `observe(overview)` -- 48 archived batches of **line 1** spread across its
  driver range. **Free.**
- `observe(pilot_2)` ... `observe(pilot_5)` -- the only data the lab has on
  lines 2-5: **8 pilot batches each -- two at each of drivers 1, 3, 5 and 8. Free.**
- `experiment(design)` -- one measurement campaign: **an indivisible lot of
  20 fresh batches, 400 flat**. Standard use: `{"campaign_line": 3}` runs
  that line's 5-level design (drivers 0.5/2.5/5.0/7.5/9.5, 4 replicates
  each). You may instead hold one setting for all 20 batches with
  `{"line": ..., "driver": ...}`. No partial lots.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `outcome` exactly (see the deliverable note in `describe()`).
  `regime.config` always carries `line` and `driver`.

## What engineering knows

Line 1 is the legacy program: its overview spans the full driver range and
commissioning considered its behaviour well understood. Lines 2-5 are newer
programs run on the same class of equipment; beyond their pilot batches,
nothing has been measured. The budget covers at most two campaigns -- the
lab expects you to decide where measurement matters most and to model every
line as well as the evidence you hold allows.
