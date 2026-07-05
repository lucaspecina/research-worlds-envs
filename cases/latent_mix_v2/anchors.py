"""v2 anchors and reference players (factory side; Decision Log v0.63).

- bayes_ceiling: THE R=1 anchor -- the best LEGAL player. Posterior over the
  hidden mix from the calibration window (declared grid x declared prior,
  likelihood = the marker mixture law), then POSTERIOR-PREDICTIVE generation:
  each draw samples mix ~ posterior (never a mean/MAP plug-in; canonical by
  convention, v0.63-1).
- plugin_player: the mandatory ladder member the TRUE theory gap is measured
  against -- window mean -> point estimate of mix -> generate at that point.
- pooled_naive: the R=0 anchor -- believes the pooled record, ignores the window.
- oracle_with_mix: DIAGNOSTIC bound (an ILLEGAL player: reads the lot's true
  mix). Scored via the same per-item pipeline by the certify script; R_uncl > 1
  expected -- the ceiling<->oracle distance is the tax of the unknowable.

Zero-LLM, numpy only. Everything parametric is DECLARED in meta
(window_protocol.posterior_grid / prior); nothing hidden here.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

WK = "cal_window"


def _grid(meta):
    g = meta.window_protocol["posterior_grid"]
    return np.linspace(g["lo"], g["hi"], int(g["points"]))


def _log_prior(grid, meta):
    pr = meta.window_protocol["prior"]
    return -0.5 * ((grid - pr["mu"]) / pr["sd"]) ** 2


def posterior_weights(window, grid, meta):
    """P(mix | window) on the declared grid. Likelihood per reading: the
    marker mixture  (1-s)N(0,mn) + sN(sep,mn), s = sigmoid(mix)."""
    p = world.PARAMS
    s = 1.0 / (1.0 + np.exp(-grid))                      # (G,)
    w = np.asarray(window, dtype=float)                  # (K,)
    mn2 = p["marker_noise"] ** 2
    a = np.exp(-0.5 * (w[None, :] ** 2) / mn2)           # component z=0
    b = np.exp(-0.5 * ((w[None, :] - p["marker_sep"]) ** 2) / mn2)
    ll = np.log((1 - s)[:, None] * a + s[:, None] * b + 1e-300).sum(axis=1)
    logp = ll + _log_prior(grid, meta)
    logp -= logp.max()
    wts = np.exp(logp)
    return wts / wts.sum()


def bayes_ceiling(meta):
    grid = _grid(meta)

    def sample(regime, n, seed):
        # POSTERIOR PREDICTIVE per the signed spec (v0.63-1, verbatim: "genera
        # cada FILA muestreando mix ~ posterior") -- row-level mixing: each row
        # draws its own mix from the posterior, i.e. rows are iid from the
        # marginal predictive. Never a per-table draw (extra between-rep
        # variance) and never a mean/MAP plug-in.
        rng = np.random.default_rng(seed)
        wts = posterior_weights(regime.context[WK], grid, meta)
        p = world.PARAMS
        s_row = 1.0 / (1.0 + np.exp(-rng.choice(grid, size=n, p=wts)))
        z = (rng.random(n) < s_row).astype(float)
        marker = p["marker_sep"] * z + rng.normal(0.0, p["marker_noise"], n)
        if "dose" in regime.config:
            dose = np.full(n, float(regime.config["dose"]))
        else:
            raw = p["dose_base"] + p["class_coef_dose"] * z + rng.normal(0.0, p["dose_noise"], n)
            dose = np.clip(raw, world.DOSE_MIN, world.DOSE_MAX)
        effect = np.where(z > 0.5, p["slope_b"], p["slope_a"])
        outcome = effect * dose + rng.normal(0.0, p["outcome_noise"], n)
        return pd.DataFrame({"dose": dose, "marker": marker, "outcome": outcome})

    return sample


def plugin_player(meta):
    """Window mean -> sigmoid-inverse point estimate -> generate there."""
    p = world.PARAMS

    def sample(regime, n, seed):
        m = float(np.mean(regime.context[WK]))
        s_hat = float(np.clip(m / p["marker_sep"], 0.02, 0.98))
        mix_hat = float(np.log(s_hat / (1.0 - s_hat)))
        return world.mechanism_given_mix(p, mix_hat, regime, n, seed)

    return sample


POOL_N, POOL_SEED0 = 4000, 97001


def _pool_stats(n_pool=POOL_N, seed0=POOL_SEED0):
    """Deterministic historical-record stats -- shared by the in-process
    callables AND the committed code fixtures (parity by construction). The
    bare regime IS the multi-lot archive (each row its own hidden lot)."""
    pool = world.sample(__import__("types").SimpleNamespace(config={}, context={}, horizon=None),
                        n_pool, seed0)
    cols = list(world.COLUMNS)
    return {
        "mu": pool[cols].mean().to_numpy(),
        "cov": pool[cols].cov().to_numpy(),
        "marg": {c: (float(pool[c].mean()), float(pool[c].std())) for c in cols},
    }


def pooled_naive(n_pool=POOL_N, seed0=POOL_SEED0):
    """Joint Gaussian of the pooled historical record; ignores the window."""
    stats = _pool_stats(n_pool, seed0)
    mu, cov = stats["mu"], stats["cov"]

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        if "dose" in regime.config:
            d = float(regime.config["dose"])
            mu_c = mu[1:] + cov[1:, 0] / cov[0, 0] * (d - mu[0])
            cov_c = cov[1:, 1:] - np.outer(cov[1:, 0], cov[0, 1:]) / cov[0, 0]
            draw = rng.multivariate_normal(mu_c, cov_c, n)
            return pd.DataFrame({"dose": np.full(n, d), "marker": draw[:, 0], "outcome": draw[:, 1]})
        draw = rng.multivariate_normal(mu, cov, n)
        return pd.DataFrame({"dose": np.clip(draw[:, 0], 0, 10), "marker": draw[:, 1], "outcome": draw[:, 2]})

    return sample


def null_marginals(n_pool=POOL_N, seed0=POOL_SEED0):
    stats = _pool_stats(n_pool, seed0)["marg"]

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        out = {}
        for c, (m, s) in stats.items():
            v = rng.normal(m, s, n)
            out[c] = np.clip(v, 0, 10) if c == "dose" else v
        return pd.DataFrame(out)

    return sample


def enrich(ns, seed_world):
    """THE choke point hook (v0.63-4): materialize the lot's window from the
    persisted scalar n_cal. Never persisted; every consumer crosses here."""
    n_cal = int(ns.context.get("n_cal", 8))
    ns.context = dict(ns.context)
    ns.context[WK] = world.make_window(seed_world, n_cal)
    return ns


# --- committed code fixtures (episode anchors as CODE, v0.63) ----------------
# The episode path scores CODE in the sandbox; for a window world the R=1
# anchor is the LEGAL bayes ceiling (world.py is the ILLEGAL player), committed
# as truth_code.py. Generators bake the declared grid/prior/PARAMS as literals
# and mirror the in-process callables' RNG call order exactly -- the parity
# test (same seeds => identical draws) is the contract.

def bayes_ceiling_code(meta):
    g = meta.window_protocol["posterior_grid"]
    pr = meta.window_protocol["prior"]
    p = world.PARAMS
    return f'''"""truth_code -- the LEGAL R=1 anchor of {meta.case_id} (Decision Log v0.63).

Bayes posterior-predictive ceiling: posterior over the hidden lot mix from
regime.context["cal_window"] (declared grid x declared prior, marker mixture
likelihood), then EACH ROW samples its own mix ~ posterior (v0.63-1 verbatim;
never a per-table draw, never a mean/MAP plug-in). world.py itself is the
ILLEGAL player here (it reads the lot's hidden state) and is never scored as
an anchor. GENERATED by anchors.bayes_ceiling_code -- do not hand-edit.
"""
import numpy as np
import pandas as pd

PARAMS = {dict(p)!r}
GRID = np.linspace({g["lo"]!r}, {g["hi"]!r}, {int(g["points"])!r})
PRIOR_MU, PRIOR_SD = {pr["mu"]!r}, {pr["sd"]!r}
DOSE_MIN, DOSE_MAX = {world.DOSE_MIN!r}, {world.DOSE_MAX!r}


def _posterior_weights(window):
    p = PARAMS
    s = 1.0 / (1.0 + np.exp(-GRID))
    w = np.asarray(window, dtype=float)
    mn2 = p["marker_noise"] ** 2
    a = np.exp(-0.5 * (w[None, :] ** 2) / mn2)
    b = np.exp(-0.5 * ((w[None, :] - p["marker_sep"]) ** 2) / mn2)
    ll = np.log((1 - s)[:, None] * a + s[:, None] * b + 1e-300).sum(axis=1)
    logp = ll + (-0.5 * ((GRID - PRIOR_MU) / PRIOR_SD) ** 2)
    logp -= logp.max()
    wts = np.exp(logp)
    return wts / wts.sum()


def model(regime, n, seed):
    p = PARAMS
    rng = np.random.default_rng(seed)
    wts = _posterior_weights(regime.context["cal_window"])
    s_row = 1.0 / (1.0 + np.exp(-rng.choice(GRID, size=n, p=wts)))
    z = (rng.random(n) < s_row).astype(float)
    marker = p["marker_sep"] * z + rng.normal(0.0, p["marker_noise"], n)
    if "dose" in regime.config:
        dose = np.full(n, float(regime.config["dose"]))
    else:
        raw = p["dose_base"] + p["class_coef_dose"] * z + rng.normal(0.0, p["dose_noise"], n)
        dose = np.clip(raw, DOSE_MIN, DOSE_MAX)
    effect = np.where(z > 0.5, p["slope_b"], p["slope_a"])
    outcome = effect * dose + rng.normal(0.0, p["outcome_noise"], n)
    return pd.DataFrame({{"dose": dose, "marker": marker, "outcome": outcome}})
'''


def pooled_naive_code():
    f = _pool_stats()
    mu = [float(v) for v in f["mu"]]
    cov = [[float(v) for v in row] for row in f["cov"]]
    return f'''"""Rung 7 -- naive pooled fit of the historical record (S_naive anchor, R=0).

Joint Gaussian of the pooled multi-lot record; believes the historical record,
ignores the calibration window entirely. GENERATED by anchors.pooled_naive_code
(POOL_SEED0={POOL_SEED0}, POOL_N={POOL_N}) -- do not hand-edit.
"""
import numpy as np
import pandas as pd

MU = np.array({mu!r})
COV = np.array({cov!r})


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    if "dose" in regime.config:
        d = float(regime.config["dose"])
        mu_c = MU[1:] + COV[1:, 0] / COV[0, 0] * (d - MU[0])
        cov_c = COV[1:, 1:] - np.outer(COV[1:, 0], COV[0, 1:]) / COV[0, 0]
        draw = rng.multivariate_normal(mu_c, cov_c, n)
        return pd.DataFrame({{"dose": np.full(n, d), "marker": draw[:, 0], "outcome": draw[:, 1]}})
    draw = rng.multivariate_normal(MU, COV, n)
    return pd.DataFrame({{"dose": np.clip(draw[:, 0], 0.0, 10.0), "marker": draw[:, 1], "outcome": draw[:, 2]}})
'''


def null_marginals_code():
    marg = _pool_stats()["marg"]
    return f'''"""Rung 8 -- null model: independent pool marginals (S_null / D_MAX reference).

GENERATED by anchors.null_marginals_code (POOL_SEED0={POOL_SEED0},
POOL_N={POOL_N}) -- do not hand-edit.
"""
import numpy as np
import pandas as pd

MARG = {marg!r}


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {{}}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == "dose" else v
    return pd.DataFrame(out)
'''


def write_fixtures():
    from wager.contracts import CaseMeta
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    (CASE / "truth_code.py").write_text(bayes_ceiling_code(meta), encoding="utf-8", newline="\n")
    ladder = CASE / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_7_naive_pooled.py").write_text(pooled_naive_code(), encoding="utf-8", newline="\n")
    (ladder / "rung_8_null.py").write_text(null_marginals_code(), encoding="utf-8", newline="\n")
    print("wrote truth_code.py, ladder/rung_7_naive_pooled.py, ladder/rung_8_null.py")


if __name__ == "__main__":
    write_fixtures()
