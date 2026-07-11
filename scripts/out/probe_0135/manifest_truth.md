MODEL SPEC ('truth') -- implement EXACTLY this belief.

Outputs (the DataFrame columns): feedstock, outcome

Per-unit generative process:
  t: era position; historically t ~ Uniform(0,1) per unit; under ANY config that sets humidity, t = 0 for all units
  ambient: hall condition; historically ambient = 2.0 + 6.0*t + Normal(0, 0.5) per unit; if humidity is set: ambient = humidity + Normal(0, 0.5) per unit
  u: unit-level latent quality factor; u ~ Normal(0, 1) per unit, ALWAYS (every regime)
  grade: supplier grade; if feedstock_grade is set: grade = that exact value (no noise); historically grade ~ Normal(5, 1) clipped to [0, 10] per unit

  feedstock = 6.0 + 1.0*(grade - 5.0) - 0.9*(ambient - 5.0) + Normal(0, 0.9)
  outcome = 30.0 - 2.5*(ambient - 5.0) + 3.0*u + Normal(0, 2.0)

NOTE: feedstock_grade does NOT enter the outcome equation at all (no direct or indirect effect on outcome).
NOTE: temp and line_speed affect NOTHING (no equation reads them).
NOTE: all Normal(mu, sd) noises are fresh independent per-unit draws.