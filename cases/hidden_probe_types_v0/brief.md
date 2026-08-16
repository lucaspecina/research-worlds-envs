# Calibration particles: response under a directional probe

You inherit a routine log from a lab that characterizes visually identical particles. Each routine
row is a different particle measured once at one probe orientation. The lab also keeps a bank of
192 labelled particles that can be measured repeatedly without destroying them.

Your job is to return a generative model for the complete response curve of **new particles** at
any requested set of orientations. The downstream calibration routine subtracts each particle's
own mean response before using the curve, so your model is judged on that centered curve shape.
Matching each orientation's separate mean and spread is not enough; preserve their joint pattern.

## Normal workflow

Keep your latest executable forecast in a Python string named `working_model`. The lab archives it
after every work cell without returning a score. This is ordinary model versioning: update it when
your current account of the population changes.

## What you can do

- `observe("routine_snapshots", n)` buys up to 200 routine rows. Their particle IDs never repeat.
- A calibration-bank experiment measures the same 192 persistent IDs at one orientation. Call
  `experiment(config={}, context={"panel": "calibration", "t_grid": (theta,)}, n=192)`, with
  `0 <= theta < 2*pi`. Each call may contain exactly one orientation; results arrive immediately.
- `submit(code)` hands back the final executable model.

The budget permits reading the complete routine log and scanning the calibration bank at five
orientations. You choose the orientations and their order.

## What you submit

Define `model(regime, n, seed) -> DataFrame` in long format with columns exactly
`unit_id, t, y`. Here `n` means new particles and `regime.context["t_grid"]` is the requested
orientation grid. Return one row per `(unit_id, orientation)` and keep each generated particle's
identity coherent across its complete curve. The evaluator applies the stated within-particle
centering before comparison. Hidden evaluation uses new particles and is entirely mathematical;
no language model reads or grades the answer.
