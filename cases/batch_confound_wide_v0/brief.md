# Intensity setting under a drifting record — the full instrument panel

You advise a process line that must set one **process intensity** (0-10) per
campaign. Your job is to hand back a model that predicts the joint
distribution of **everything the line logs per unit** -- nineteen signals:
the settings (`driver`, `pressure`, `flow_rate`, `torque`, `rpm`), the
material readings (`signal`, `surface_gloss`, `density`, `weight`, `grain`),
the hall conditions (`hall_temp`, `hall_rh`, `vibration`, `noise_db`), the
maintenance panel (`wear_index`, `feed_counter`, `supply_age`, `op_tenure`)
and the final `outcome` -- under any intensity you choose to set.

## What is at stake

The line scraps what fails: **a unit whose quality lands below the reject line
of 15 is scrapped at the line's cost**. Scrap is far costlier than the margin
on a good unit, so predicting *how much of the population lands below the
line* under a given intensity matters as much as predicting the average.

The line also tells you its history plainly: over the era its records cover,
**both the meter's calibration and the operating intensity changed over
time**. It suspects the records overstate what intensity buys. And it warns
you about its own logging habit: they record everything that has a plug --
most of those nineteen signals are bystanders to the money question.

## What you can do

- `observe(records)` -- cheap historical line records, taken in measurement
  batches (`batch_id` included).
- `observe(replicas_calibracion)` -- a costlier calibration bench: two quality
  readings per unit (`outcome__rep1`, `outcome__rep2`).
- `experiment(design)` -- pay to run fresh units at intensities you choose.
  The same instrument takes the readings, in fresh batches.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over all
  nineteen columns. Model the **process**, not the meter.

## The catch you are paid to find

The records show a generous return to intensity, and nineteen columns each
willing to tell you a story. The line is paying you to find out *how much of
that return is real*, *which of the many signals actually matter for the
reject rate*, and *what the reject rate really is at the intensity you would
recommend*.
