# Dryer heat setting for spray-dried powder (reprocessing pricing)

You advise a spray-drying operation that must set one **dryer heat setting**
(0-10) per campaign. Your job is to hand back a model that predicts the
distribution of the **powder stability score** of lots under any setting you
choose to run.

## What is at stake

Reprocessing is the cost driver: **a lot scoring below the rework line of 20
is sent for reprocessing at the plant's cost**. Predicting *how much of the
population lands below the line* under a given setting matters as much as
predicting the average.

The plant's operators are adamant about the shape of the game: **too little
leaves powder damp, too much heat-damages it** -- they are sure there is a
sweet spot, and they suspect the plant has been running below it for years.
The records cluster around the settings the plant actually ran.

## What you can do

- `observe(records)` -- cheap historical production records. Columns:
  `dryer_setting`, `moisture_probe` (inline moisture-related reading),
  `shelf_life` (powder stability).
- `observe(replicas_calibracion)` -- a costlier calibration bench: two
  stability readings per lot (`shelf_life__rep1`, `shelf_life__rep2`).
- `experiment(design)` -- pay to run fresh lots at settings you choose,
  including settings the records never visited. The same instrument takes the
  readings.
- `submit(model)` -- hand back `model(regime, n, seed) -> table` over
  `dryer_setting, moisture_probe, shelf_life`. Model the **process**, not the
  meter.

## The catch you are paid to find

Maybe there is none -- or maybe the operators' story is exactly right and the
money is in *where* the sweet spot sits and *how fast* stability falls off on
either side. The plant pays for the real shape of the response, especially
away from the settings the records cover, and for the reprocessing rate at
the setting you would commit to.
