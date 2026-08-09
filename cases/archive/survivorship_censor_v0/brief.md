# Treatment intensity for the unscreened line (warranty pricing)

You advise a treatment line that must set one **treatment intensity** (0-10)
per campaign and price its warranty exposure. Your job is to hand back a model
that predicts the distribution of the **endurance score** of treated units
under any intensity you choose to set.

## What is at stake

The exposure is simple: **a unit whose endurance lands below the warranty
floor of 25 is a claim the line pays**. Claims are far costlier than the
margin on a good unit, so predicting *how much of the population lands below
the floor* under a given intensity matters as much as predicting the average.

One more thing the line tells you plainly: to cut cost, it is **removing the
intake screen** that used to run before treatment. Your model must answer for
**every incoming unit**, screened or not.

## What you can do

- `observe(records)` -- cheap historical line records from the screened era.
  Columns: `driver`, `stress` (intake reading), `outcome` (endurance).
- `observe(replicas_calibracion)` -- a costlier calibration bench: two
  endurance readings per unit (`outcome__rep1`, `outcome__rep2`).
- `experiment(design)` -- pay to treat fresh, unscreened units at intensities
  you choose (randomization breaks the historical intake practice, not the
  measurement instrument). You cannot hand-pick units.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `driver, stress, outcome` for the full production population.

## The catch you are paid to find

The historical records look reassuring. The line suspects they flatter the
product in more ways than one -- and it is paying you to find out *why*, *by
how much*, and *what the warranty exposure really is at the intensity you
would recommend, once the screen is gone.*
