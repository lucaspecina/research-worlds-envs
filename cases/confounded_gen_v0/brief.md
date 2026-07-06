# injection molding of medical syringe barrels -- setting policy under a suspect record

The agent advises molding settings for upcoming syringe barrel runs and must hand back a recommended pack_pressure level. It can inspect historical production records with inline readings and final QA results, then propose the best setting for future output.

## What is at stake

The line scraps what fails: a scrap -- clarity_seal_score below the acceptance line of 16.8 -- is far costlier than a forgone gain. Predicting how much of the population lands below the line under a given pack_pressure matters as much as the average.

## What you can do

- `observe(records)` -- cheap historical records (`pack_pressure`, `cavity_fill_time`, `clarity_seal_score`).
- `experiment(design)` -- pay to run fresh units at a `pack_pressure` you choose (randomization breaks the historical assignment).
- `submit(model)` -- hand back `model(regime, n, seed)` over `pack_pressure, cavity_fill_time, clarity_seal_score`.

## The catch you are paid to find

The catch is that resin_dryness was not directly logged in the main table, even though it affected both the chosen pressure setting and the final quality. Operators often pushed pressure differently when the material was flowing unusually well or poorly, so the apparent benefit of the knob may be confounded.
