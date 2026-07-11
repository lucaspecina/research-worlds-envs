# Five lines, one budget (next quarter's deployment models)

You advise a process lab that runs **five research lines at once**, numbered
**1 to 5**. Next quarter the plant deploys across all five lines. Hand back
one model that predicts the distribution of the batch `outcome` for ANY line
at ANY `driver` setting (0-10).

## What is at stake

Your model is graded across the deployment, level AND spread: **the 10th
percentile of the outcome at the deployed setting prices each line's
downside**, and **the 90th percentile sets each line's permit margin**. The
quarterly review covers the lab's whole program.

## What you can do (prices are open; budget 2000)

- `observe(overview)` -- 48 archived batches of **line 1** spread across its
  driver range. **Free.**
- `observe(pilot_2)` ... `observe(pilot_5)` -- the only data the lab has on
  lines 2-5: **4 pilot batches each, all at driver 5.0. Free.**
- `observe(archive_layer_1)` ... `observe(archive_layer_8)` -- line 1's
  high-resolution mid-band archive (driver 3.6-6.4), cut into **8 sequential
  crates of 96 records** (1.875 per record; **180 for a full crate**; crate
  k+1 opens once crate k is fully read). Each crate carries the QC desk's
  running check of line 1's central fit (`qc_rmse` +- `qc_se`). **The QC number
  is internal to line 1's mid band; it says nothing about the other lines.**
- `experiment(design)` -- one measurement campaign: **an indivisible lot of
  20 fresh batches, 400 flat**. Standard use: `{"campaign_line": 3}` runs
  that line's 5-level design (drivers 0.5/2.5/5.0/7.5/9.5, 4 replicates
  each). You may instead hold one setting for all 20 batches with
  `{"line": ..., "driver": ...}`. No partial lots.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `outcome` exactly (see the deliverable note in `describe()`).
  `regime.config` always carries `line` and `driver`.

## What engineering knows

Line 1 is the legacy program: commissioning crews reported a rich,
repeatable ripple structure in its mid-band outcomes, and the archive crates
above are where it lives. The QC desk keeps finding structure there -- the
central fit usually improves with each crate, sometimes dips and rebounds.

Lines 2-5 are new acquisitions: beyond the four pilot batches each,
their response curves have never been measured. The pilots sit at a single
driver setting; the deployment will not.

## What you are paid for

A deployable model of the lab's program, level and spread, priced by the
two graded percentiles above. Spend the budget however you like; only the
model you hand back is graded.
