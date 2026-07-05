# Conditioning intensity for the batch line

You advise a batch conditioning line that must set one **conditioning
intensity** (0-10) per run. Your job is to hand back a model that predicts the
distribution of the final **quality** score under any intensity you choose to
set, so the line can price its policy.

## What is at stake

Getting the tail right is the money: a unit whose quality lands below the cull line of 2 is far costlier than a forgone gain. So predicting *where the culled tail sits* under a given intensity matters as much as predicting the average.

One thing the lab is upfront about: **your model should reproduce the system's
true behavior; your measurements include instrument error.** The quality meter
is imperfect -- its readings scatter around the true value -- and the line pays
you for the process, not for the meter.

## What you can do

- `observe(records)` -- cheap historical line records. Columns: `driver`,
  `signal`, `outcome`, `ambient`.
- `observe(replicas_calibracion)` -- dearer: fresh units, each measured
  **twice** on the same quality meter (`outcome__rep1`, `outcome__rep2`).
- `experiment(design)` -- pay to set the intensity on fresh units and measure
  quality (randomization breaks the historical record-keeping, not the
  measurement channel).
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `driver, signal, outcome, ambient` -- the system's true behavior.

## The catch you are paid to find

The historical association between the gauge, the intensity and the quality is
what an untrained eye would price. The line suspects its records flatter the
gauge and is paying you to find out *why*, *what the intensity really does*,
and *where the culled tail actually sits when you set the intensity
deliberately* -- for runs like and unlike the ones on record.
