# Intensity setting under a drifting record (reject pricing)

You advise a process line that must set one **process intensity** (0-10) per
campaign. Your job is to hand back a model that predicts the distribution of
the final **quality score** of units under any intensity you choose to set.

## What is at stake

The line scraps what fails: **a unit whose quality lands below the reject line
of 15 is scrapped at the line's cost**. Scrap is far costlier than the margin
on a good unit, so predicting *how much of the population lands below the
line* under a given intensity matters as much as predicting the average.

The line also tells you its history plainly: over the era its records cover,
**both the meter's calibration and the operating intensity changed over
time**. It suspects the records overstate what intensity buys.

## What you can do

- `observe(records)` -- cheap historical line records, taken in measurement
  batches. Columns: `driver`, `signal`, `outcome`, `batch_id` (the run the
  reading belongs to).
- `observe(replicas_calibracion)` -- a costlier calibration bench: two quality
  readings per unit (`outcome__rep1`, `outcome__rep2`).
- `experiment(design)` -- pay to run fresh units at intensities you choose.
  The same instrument takes the readings: they arrive in fresh batches
  (`batch_id`), each batch with its own meter state.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `driver, signal, outcome`. Model the **process**, not the meter.

## The catch you are paid to find

The records show a generous return to intensity. The line is paying you to
find out *how much of that return is real*, *what part of the spread you see
is the instrument rather than the product*, and *what the reject rate really
is at the intensity you would recommend*.
