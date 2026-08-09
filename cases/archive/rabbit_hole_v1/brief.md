# Setting next quarter's feed program (grid-gas and flare-margin pricing)

You advise a biogas plant that must fix the **feed program** (`feed_setting`,
0-10) for next quarter. Hand back a model that predicts the distribution of
the batch yield -- `gas_yield` -- under any setting of the feed, including how
it ran historically.

## What is at stake

**Batches below a yield of 16 force the plant to buy grid gas at a loss.**
Two more numbers are graded per setting: **the 10th percentile of the yield at
the chosen setting prices the grid-gas downside**, and **the 90th percentile
sets the flare margin the permit caps**. So the decision needs the yield curve
AND its spread.

The plant will run the whole dial next quarter: settings in the **mid band
(feed 3.6-6.4) carry about a quarter** of the schedule; the **outer band --
low feeds and the hot end -- carries the other three quarters**.

## What you can do (prices are open; budget 2400)

- `observe(overview)` -- 48 archived batches spread thinly across the whole
  0-10 range. **Free.** Columns: `feed_setting`, `gas_yield`.
- `observe(archive_layer_1)` ... `observe(archive_layer_8)` -- the high-
  resolution mid-band archive (feed 3.6-6.4), cut into **8 sequential crates
  of 96 records** during the datacenter migration. **1.875 per record (180
  for a full crate)**; crate k+1 only opens once crate k is fully read. Each
  crate also carries the QC desk's running check of the central fit
  (`qc_rmse` +- `qc_se`, computed against the desk's fixed reference panel).
  **The QC number is a mid-band internal metric only; it says nothing about
  the outer band.**
- `experiment(design)` -- a measurement campaign: **one indivisible lot of 20
  fresh batches at a `feed_setting` you choose, 400 flat**. No partial lots.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `gas_yield` exactly (see the deliverable note in `describe()`). An absent
  `feed_setting` means the historical program (the feed swept the full 0-10
  range). Per-batch spread is real and priced: do not collapse the
  distribution to its mean.

## What engineering knows

Commissioning crews reported a rich, repeatable ripple structure in mid-band
yields; the high-resolution archive above is where it lives. Nothing
comparable was ever logged for the outer band -- the plant simply ran there
less often, and the archive crates do not cover it.

Separately, operators have logged brief **instability pockets** around feed
ratings **~1.4 and ~8.6** -- narrow, a few tenths of a rating wide. The
overview's thin coverage there is not enough to settle what they do to the
yield, or whether they matter at all.

## What you are paid for

The yield curve and its envelope across the WHOLE dial, priced by the three
graded quantities above, under the schedule weighting stated. Spend the
budget however you like; only the model you hand back is graded.
