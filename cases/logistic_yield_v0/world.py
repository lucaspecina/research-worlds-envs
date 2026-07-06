"""logistic_yield_v0 -- the first dynamic (ODE) world: saturating batch yield.

The truth of the case. Server-side only: the agent never sees this file.

E1-matrix slot #11 (spec: docs/mundos-dinamicos.md). A batch process whose
cumulative yield grows and SATURATES (closed-form logistic -- no integrator,
perfect determinism). Its job is to validate that the exam machinery survives
the change of formalism (photos -> movies), not to produce headroom.

Mechanism per unit (population heterogeneity makes distributions meaningful):

    r_i  = (r0 + r_slope * feed) * exp(N(0, r_disp))   # growth rate; feed-settable
    K_i  ~ N(K0, K_sd), clipped >= K_min               # capacity; feed-INDEPENDENT
    x0_i ~ N(x0, x0_sd), clipped >= x0_min             # initial state (no degenerate
                                                       # early column -- scale family)
    y_i(t) = K_i / (1 + ((K_i - x0_i)/x0_i) * exp(-r_i t))

The epistemic structure (spec 2/4.5): early points inform r; K is INVISIBLE
until saturation starts. The historical source is truncated at horizon t<=6
(growth phase only) -> in the cheap pool the data says "this grows without a
ceiling". Because K does not depend on feed, a good investigator can buy a
HIGH-feed experiment (saturates sooner -> cheaper horizon) and transfer K to
the operating regimes -- the manual move this world exists to price.

Deliverable format (trajectory contract, ADR 0068-R1): LONG -- one row per
reading, columns (unit_id, t, y); the item's grid arrives DECLARED in
regime.context["t_grid"]; n counts UNITS. world.sample() is the CLEAN truth:
truncation and sensor noise live in the declared sources, never here.
"""

import numpy as np
import pandas as pd

COLUMNS = ["unit_id", "t", "y"]

PARAMS = {
    "r0": 0.15,          # base growth rate at feed=0
    "r_slope": 0.05,     # feed -> growth rate (feed is the settable knob)
    "r_disp": 0.10,      # lognormal dispersion of r across units
    "K0": 100.0,         # population capacity center (feed-independent)
    "K_sd": 8.0,
    "K_min": 20.0,
    "x0": 2.0,           # initial yield level
    "x0_sd": 0.4,
    "x0_min": 0.5,
}
FEED_MIN, FEED_MAX = 0.0, 10.0
HIST_FEED = 4.0          # the line's historical operating feed


def mechanism(params, regime, n, seed):
    p = params
    grid = regime.context.get("t_grid")
    if grid is None:
        raise ValueError("logistic_yield_v0: every regime must declare context['t_grid']")
    t = np.asarray(tuple(grid), dtype=float)
    feed = float(regime.config.get("feed", HIST_FEED))
    rng = np.random.default_rng(seed)

    r = (p["r0"] + p["r_slope"] * feed) * np.exp(rng.normal(0.0, p["r_disp"], n))
    K = np.clip(rng.normal(p["K0"], p["K_sd"], n), p["K_min"], None)
    x0 = np.clip(rng.normal(p["x0"], p["x0_sd"], n), p["x0_min"], None)

    a = (K - x0) / x0                                   # (n,)
    y = K[:, None] / (1.0 + a[:, None] * np.exp(-r[:, None] * t[None, :]))  # (n, k)

    k = t.size
    return pd.DataFrame({
        "unit_id": np.repeat(np.arange(n, dtype=float), k),
        "t": np.tile(t, n),
        "y": y.ravel(),
    })


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
