# Input setting for incoming lots

You advise a process line that must set a single **input level** (0-10) for the
units that arrive. Your job is to hand back a model that predicts the distribution
of the quality **outcome** under any level you choose to set, so the line can
price its policy.

## What is at stake

A poor outcome -- a quality score below the scrap line of -5 -- is far costlier than a forgone gain: scrapping a unit with the wrong input level is the failure the line most wants to avoid. So predicting *where the bad tail sits* under a given level matters as much as predicting the average.

The line also warns you: **the lots that arrive are not the lot in your
records.** The historical data was collected from one standing population of units;
the units you must set the level for may be composed quite differently, and the
operator needs a model that still holds when the population shifts. Unit-to-unit
heterogeneity in how they respond is plausible and worth investigating.

## What you can do

- `observe(records)` -- cheap historical line records. Columns: `dose`, `marker`,
  `outcome`. (The records include a per-unit **sensor** reading, `marker`.)
- `experiment(design)` -- pay to set the input level on a sample and measure outcomes
  (randomization breaks the historical assignment, not the measurement channel).
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `dose, marker, outcome`.

## The catch you are paid to find

The historical input-outcome association is what an untrained eye would price. The
line suspects it is misleading and is paying you to find out *why*, *for which
units*, and *what actually happens to the outcome -- and its scrap tail -- when the
input level is set deliberately for a population unlike the one on record.*
