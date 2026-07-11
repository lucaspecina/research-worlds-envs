DELIVERY CONTRACT (v1) -- read carefully; every clause is graded.

Deliver ONE python code string defining:  model(regime, n, seed) -> pandas.DataFrame

1. OUTPUT: a DataFrame with columns exactly ['feedstock', 'outcome'], exactly n rows,
   finite floats. `regime.config` is a dict; `seed` is an integer.
2. WHAT model() MUST GENERATE: the PROCESS distribution -- the true per-unit values,
   BEFORE any measurement instrument. Do NOT add instrument/meter error to the output.
   (Instrument error exists only in the readings served by observe()/experiment()
   during an investigation; the deliverable models the plant, not the meter.)
3. KNOB SEMANTICS: regime.config may contain any subset of
   {feedstock_grade, humidity, temp, line_speed}.
   - If a knob IS present: the process runs with that knob held at the given value
     for all n units.
   - If a knob is ABSENT: that knob is NOT held -- the process runs with that factor
     behaving as it does historically/ambiently (its natural distribution across
     units, as described in the belief you are implementing).
   - An EMPTY config means: the historical/observational process, exactly as the era
     that produced the records.
4. RANDOMNESS: use ONLY numpy randomness seeded from `seed`
   (np.random.default_rng(seed) or equivalent). Same (regime, n, seed) -> same table.
5. Per-unit heterogeneity is real: units differ by process noise and by any
   historically-varying factors. Do not collapse distributions to their means.
6. Implement EXACTLY the belief specified in the MODEL SPEC you were given -- even
   where you would personally disagree. Fidelity to the spec is what is graded.
