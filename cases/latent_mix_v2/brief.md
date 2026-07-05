# Input setting for incoming lots (unlabeled composition)

You advise a process line that must set a single **input level** (0-10) for each
incoming lot. Your job is to hand back a model that predicts the distribution of
the quality **outcome** for a given lot under any level you choose to set, so the
line can price its policy lot by lot.

## What is at stake

A poor outcome -- a quality score below the reject line of -5 -- is far costlier than a forgone gain: rejecting a unit with the wrong input level is the failure the line most wants to avoid. So predicting *where the bad tail sits* under a given level matters as much as predicting the average.

The line also warns you: **lots are not labeled and they are not alike.** The
material composition of each incoming lot varies, is nowhere recorded, and may
lie well outside anything in your historical records. Unit-to-unit heterogeneity
in how units respond is plausible and worth investigating.

What you get for each lot is a **small calibration sample**: before committing to
an input level, the line pulls a handful of units from the lot and runs the
per-unit **sensor** on them. Those unlabeled readings are all you ever see of a
lot before your model must speak.

## What you can do

- `observe(records)` -- cheap historical line records: past lots of varying,
  unrecorded composition. Columns: `dose`, `marker`, `outcome`.
- `experiment(design)` -- pay to run a trial on **one fresh lot per call**: you
  set the input level and how many units to draw from that single lot
  (randomization breaks the historical assignment, not the measurement
  channel). Lots differ -- to cover several fresh lots, run several
  experiments. You cannot choose or see a lot's composition.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `dose, marker, outcome`. Each evaluation regime carries that lot's
  **calibration readings** in `regime.context["cal_window"]`: unlabeled sensor
  readings from the target lot, **variable length** (some lots come with 2,
  some with 64). Your model answers for THAT lot.

## The catch you are paid to find

The historical input-outcome association is what an untrained eye would price.
The line suspects it is misleading and is paying you to find out *why*, *for
which lots*, and *what actually happens to the outcome -- and its reject tail --
when the input level is set deliberately for a lot you have only a handful of
sensor readings from.*
