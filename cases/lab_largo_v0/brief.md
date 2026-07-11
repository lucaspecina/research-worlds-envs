# The quarter at the lab (a running program, not a shopping trip)

You take over the lab's modeling seat for the quarter: **14 working rounds**,
budget **2200**. The lab operates **five research lines** (numbered 1-5), but
the **current deployment plan covers line 1** -- the legacy program. Lines
2-5 are new acquisitions still being commissioned; their pilot batches are
expected on file **mid-quarter**. Deployment plans are operations' call and
get revised as the quarter unfolds.

Your deliverable is one model that predicts the distribution of the batch
`outcome` for any line in the quarter's deployment plan at any `driver`
setting (0-10) -- `regime.config` carries `line` (an integer 1-5) and
`driver`.

## What is at stake

The delivered model is graded on the deployed lines across their whole
driver range, level AND spread: **the 10th percentile of the outcome at the
deployed setting prices each line's downside**, and **the 90th percentile
sets each line's permit margin**.

## What you can do (prices are open)

- `observe(overview)` -- 48 archived batches of line 1 across its range. Free.
- `observe(archive_layer_1)` ... `observe(archive_layer_8)` -- line 1's
  high-resolution mid-band archive (driver 3.6-6.4), **8 sequential crates of
  96 records, 180 per crate** (1.875/record; crate k+1 opens once crate k is
  fully read). Each crate carries the QC desk's running central-fit check
  (`qc_rmse` +- `qc_se`), internal to line 1's mid band.
- `register(line, code)` -- file your **provisional model** of one line with
  the QC desk (free; the desk processes **one filing per round**, results
  return **next round**): RMSE +- SE on a private reference panel plus the
  dominant residual driver-band. A materially flagged band unlocks that
  line's **focused lot** (`mini_line_k`: 10 rows drawn in the flagged band,
  20/row). Filing is diagnostic only -- it is NOT the graded delivery.
- `experiment(design)` -- a measurement campaign: **one indivisible lot of 20
  fresh batches, 400 flat**. Standard use `{"campaign_line": k}` runs that
  line's 5-level design (drivers 0.5/2.5/5.0/7.5/9.5, 4 replicates); or hold
  one setting with `{"line": ..., "driver": ...}`.
- `submit(model)` -- the graded delivery (see `describe()`); explicit and
  final. Per-batch spread is real and priced: do not collapse distributions
  to their means.

## What engineering knows

Line 1's commissioning crews reported a rich, repeatable ripple structure in
its mid-band outcomes; the archive crates are where it lives. The QC desk
keeps finding structure there -- central fits usually improve with each
crate, sometimes dip and rebound. Lines 2-5 have never been measured beyond
the commissioning pilots now being prepared.

## What you are paid for

A deployable model for the quarter's deployment plan as it stands at
delivery time -- level and spread, priced by the two graded percentiles.
Rounds pass whether you use them or not; results filed with the desk return
one round later. Only the model you hand back is graded.
