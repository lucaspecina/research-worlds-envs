# Cure intensity for the finishing line (rework pricing)

You advise a curing line that must set one **cure intensity** (0-10) per
campaign. Your job is to hand back a model that predicts the distribution of
the **finish quality score** of units under any intensity you choose to set.

## What is at stake

Rework is the cost driver: **a unit finishing below the rework line of 20 is
reworked at the line's cost**. Predicting *how much of the population lands
below the line* under a given intensity matters as much as predicting the
average.

The line's veterans are adamant about the shape of the game: **too little
cures poorly, too much scorches** -- they are sure there is a sweet spot,
and they suspect the line has been running below it for years. The records
cluster around the intensities the line actually ran.

## What you can do

- `observe(records)` -- cheap historical line records. Columns: `driver`,
  `signal` (inline material reading), `outcome` (finish quality).
- `observe(replicas_calibracion)` -- a costlier calibration bench: two quality
  readings per unit (`outcome__rep1`, `outcome__rep2`).
- `experiment(design)` -- pay to run fresh units at intensities you choose,
  including intensities the records never visited. The same instrument takes
  the readings.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `driver, signal, outcome`. Model the **process**, not the meter.

## The catch you are paid to find

Maybe there is none -- or maybe the veterans' story is exactly right and the
money is in *where* the sweet spot sits and *how fast* quality falls off on
either side. The line pays for the real shape of the response, especially
away from the intensities the records cover, and for the rework rate at the
intensity you would commit to.
