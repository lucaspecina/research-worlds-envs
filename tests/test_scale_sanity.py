"""Scale/anchor sanity suite (Decision Log v0.22, generalizes the std regression).

The scale/anchor family has had three pathologies: the null as a range-inflating
outlier (v0.12), 64-bit seeds crashing legacy RNG (v0.16), and the == 0 std clamp
exploding D_MAX on controlled (constant) columns (v0.21). This suite asserts the
invariants as PROPERTIES over random worlds/regimes, in CI:

- std floors are relative (a constant column -> std clamped, not ~1e-15);
- D_MAX_item is finite and in a sane range (not ~1e16);
- no per-item distance exceeds D_MAX_item (the universal cap holds);
- unclipped anchor order: R(crash) <= R(null) <= R(naive)=0 <= R(truth)=1.
"""

from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from wager.contracts import Battery, BatteryItem, ScoringParams
from wager.contracts.world import Regime
from wager.reward.distance import TruthSide
from wager.reward.scorer import WorldSide, make_anchors, score_callable

COLS = ["x", "marker", "y"]
PARAMS = ScoringParams(lambda_mdl=0.0, n_samples=500, m_reps=2)


def _make_world(a, b, sev_eff):
    def sample(regime, n, seed):
        r = np.random.default_rng(seed)
        ctx = regime.context.get("ctx", 0.0)
        s = r.normal(ctx, 1.0, n)
        if "x" in regime.config:
            x = np.full(n, float(regime.config["x"]))
        else:
            x = np.clip(a * s + r.normal(0, 1, n), 0, 10)
        y = b * (10 * x / (x + 4)) + sev_eff * s + r.normal(0, 0.5, n)
        marker = s + r.normal(0, 1.5, n)
        return pd.DataFrame({"x": x, "marker": marker, "y": y})
    return sample


def _pool(world, n, seed):
    return world(SimpleNamespace(config={}, context={"ctx": 0.0}, horizon=None), n, seed)


def _null_of(pool):
    mu, sd = pool[COLS].mean().to_numpy(), pool[COLS].std().to_numpy()
    def null(regime, n, seed):
        r = np.random.default_rng(seed)
        return pd.DataFrame({c: r.normal(mu[i], sd[i], n) for i, c in enumerate(COLS)})
    return null


def _naive_of(pool):
    mu, cov = pool[COLS].mean().to_numpy(), pool[COLS].cov().to_numpy()
    def naive(regime, n, seed):
        r = np.random.default_rng(seed)
        if "x" in regime.config:
            d = float(regime.config["x"])
            mc = mu[1:] + cov[1:, 0] / cov[0, 0] * (d - mu[0])
            cc = cov[1:, 1:] - np.outer(cov[1:, 0], cov[0, 1:]) / cov[0, 0]
            draw = r.multivariate_normal(mc, cc, n)
            return pd.DataFrame({"x": np.full(n, d), "marker": draw[:, 0], "y": draw[:, 1]})
        draw = r.multivariate_normal(mu, cov, n)
        return pd.DataFrame({"x": draw[:, 0], "marker": draw[:, 1], "y": draw[:, 2]})
    return naive


def _crash(regime, n, seed):
    raise RuntimeError("crash")


def _battery(rng):
    items = []
    for i in range(8):
        if rng.random() < 0.8:
            reg = Regime(config={"x": float(rng.uniform(0, 10))}, context={"ctx": float(rng.uniform(-1.5, 1.5))})
        else:
            reg = Regime(config={}, context={"ctx": float(rng.uniform(-1, 1))})
        items.append(BatteryItem(weight=1.0, regime=reg, seed_world=1000 + i))
    return Battery(items=items)


def test_std_clamp_handles_constant_column():
    # a controlled variable is constant; its std must clamp to ~1, not ~1e-15
    df = pd.DataFrame({"x": np.full(400, 7.3), "marker": np.random.default_rng(0).normal(size=400),
                       "y": np.random.default_rng(1).normal(size=400)})
    ts = TruthSide(df, COLS)
    assert ts.std[0] >= 0.5  # clamped, not 1e-15
    other = pd.DataFrame({"x": np.full(400, 2.0), "marker": np.zeros(400), "y": np.zeros(400)})
    d = ts.distance_to(other)
    assert np.isfinite(d) and d < 100  # bounded, not ~1e16


@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4])
def test_anchor_order_and_dmax_sanity(seed):
    rng = np.random.default_rng(seed)
    world = _make_world(a=rng.uniform(1, 2), b=rng.uniform(0.7, 1.3), sev_eff=rng.uniform(-2.5, -1.0))
    pool = _pool(world, 3000, 100 + seed)
    null, naive = _null_of(pool), _naive_of(pool)
    battery = _battery(rng)
    ws = WorldSide(world, battery, COLS, PARAMS.n_samples, null_sample=null)

    # D_MAX sane: finite, positive, not exploded
    assert all(np.isfinite(dm) and 0 < dm < 1e4 for dm in ws.d_maxes), ws.d_maxes

    s_truth = score_callable(world, ws, PARAMS)
    s_naive = score_callable(naive, ws, PARAMS)
    s_null = score_callable(null, ws, PARAMS)
    s_crash = score_callable(_crash, ws, PARAMS)
    anchors = make_anchors(s_truth, s_naive, s_null)

    r = lambda s: anchors.r_of(s)[1]  # unclipped
    assert r(s_truth) == pytest.approx(1.0, abs=1e-6)
    assert r(s_naive) == pytest.approx(0.0, abs=1e-6)
    assert r(s_null) < r(s_naive) + 1e-9       # null no better than naive
    assert r(s_crash) <= r(s_null) + 1e-9       # crash no better than the null


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_no_distance_exceeds_dmax(seed):
    from wager.reward.scorer import score_submission

    rng = np.random.default_rng(10 + seed)
    world = _make_world(a=1.5, b=1.0, sev_eff=-2.0)
    pool = _pool(world, 2000, 50 + seed)
    battery = _battery(rng)
    ws = WorldSide(world, battery, COLS, PARAMS.n_samples, null_sample=_null_of(pool))
    code = (
        "import numpy as np, pandas as pd\n"
        "def model(regime, n, seed):\n"
        " r = np.random.default_rng(seed)\n"
        " x = np.full(n, float(regime.config.get('x', 3.0)))\n"
        " return pd.DataFrame({'x': x, 'marker': r.normal(0,1,n)*5, 'y': r.normal(0,1,n)*9})\n"
    )
    rep = score_submission(code, ws, PARAMS)
    for it in rep.items:
        assert it.mean_distance <= it.d_max + 1e-9  # cap holds for every item


# ---- dimensional consistency of gate thresholds (Decision Log v0.36-1b) ------
# Fifth member of the scale family: a threshold expressed as relative CV is
# accidentally valid where rung means sit near 1 (there CV == std) and breaks
# exactly when the instrument works and pushes means down. Gates are ABSOLUTE.


def test_gate_threshold_is_absolute_r_units():
    import inspect

    from wager.factory.calibration import gate_threshold

    # 3 x max of the ABSOLUTE stds across sweep extremes
    assert gate_threshold([0.0092, 0.0124]) == pytest.approx(3 * 0.0124)
    # signature pin: stds only -- no mean/CV parameter can re-enter the API
    params = list(inspect.signature(gate_threshold).parameters)
    assert params == ["stds"]
    # two regimes whose rung MEANS differ x4 but share absolute std produce the
    # SAME threshold (the CV convention would have inflated the small-mean one x4)
    assert gate_threshold([0.012]) == gate_threshold([0.012])


def test_sub_battery_r_renormalizes_and_cancels_mdl():
    from wager.contracts import ItemScore, ScoreReport, ScoringCost
    from wager.factory.calibration import sub_battery_r

    def report(dists, mdl_term):
        items = [
            ItemScore(index=i, weight=0.25, mean_distance=d, d_max=10.0,
                      capped_reps=0, sandbox_errors=0)
            for i, d in enumerate(dists)
        ]
        fid = -sum(0.25 * d for d in dists)
        return ScoreReport(fidelity=fid, mdl_bytes=1, mdl_term=mdl_term,
                           raw_score=fid - mdl_term, items=items,
                           cost=ScoringCost(k_items=len(dists), n_samples=1,
                                            m_reps=1, wall_seconds=0.0))

    # obs sub-battery = items {2, 3}; rung halfway between truth and naive there
    truth = report([0.1, 0.1, 0.2, 0.2], mdl_term=0.5)
    naive = report([1.0, 1.0, 1.0, 1.0], mdl_term=0.0)
    rung = report([0.5, 0.9, 0.6, 0.6], mdl_term=9.9)  # MDL must NOT matter
    r_obs = sub_battery_r(rung, truth, naive, idxs=[2, 3])
    assert r_obs == pytest.approx((-0.6 + 1.0) / (-0.2 + 1.0))  # 0.5 exactly
