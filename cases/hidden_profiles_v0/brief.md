# Assignment — forecast complete qualification profiles

A laboratory qualifies material specimens with twelve standardized, non-destructive tests. Every
row in a returned table is one specimen measured under all twelve tests; the columns are
`response_01` through `response_12`.

Your job is to return a generative model of the **complete profile of a new specimen**. Preserving
each test's average and spread is not enough: readings from the same specimen may move together in
ways that affect qualification.

The qualification plan depends on the distribution of complete within-specimen profiles, not
merely on twelve separate marginals.

## What you can do

- `observe("profile_archive", n)` buys up to 400 archived complete profiles.
- `experiment(n=n)` produces `n` fresh complete profiles. There are no treatment knobs in this
  first world; a fresh run is simply more independently sampled specimens.
- `submit(code)` hands back your executable model.

The budget is finite. You choose how much evidence is worth buying and how to analyse the joint
profiles.

## What you submit

Define `model(regime, n, seed) -> DataFrame` with exactly the twelve response columns, in order, and
exactly `n` rows. Each generated row must be the complete profile of one new specimen. The hidden
evaluation uses fresh specimens and judges the joint distribution mathematically; no language
model reads or grades your answer.
