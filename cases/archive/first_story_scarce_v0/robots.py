"""The robot pair of first_story_v0 (ADR 0080-1 / 0081): scripted EPISODE agents.

The first scripted harness agents: both run through the REAL episode pipeline
(describe/observe/experiment/submit, budget charged, smoke validated -- no
factory shortcuts). Their R comes from server.result like any solver's.

- TERCO (vicious; choice rule DECLARED: seduced-by-design -- in this world the
  seduction points deterministically at Historia X: the record's correlation +
  the folklore. Rationale: the world is built so X is the first thing any
  naive fit finds). Policy: buys the record, fits y~feedstock, executes
  everything else competently, never tries to break its own story. Its model:
  grade moves feedstock moves outcome; humidity does not exist.
- CUIDADOSO (careful; the adaptivity-certificate proxy). Policy: forms X, then
  spends a declared slice trying to REFUTE it -- stratifies the record by
  time (cheap escape) and runs the discriminating experiments over the FULL
  declared knob menu (dear escape) -- then models Historia Y, deconvolving
  the meter via the replicas source.

Zero-LLM. Deterministic given the server's seed_offset.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402

GBAR = 5.0  # the record's implicit grade center (both robots read it from the brief's scale)


def _fit_line(x, y):
    b, a = np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)
    return float(a), float(b)


def run_terco(server) -> None:
    df = server.observe("registros_linea", 1500)
    f, y = df["feedstock"].to_numpy(float), df["outcome"].to_numpy(float)
    a, b = _fit_line(f, y)
    resid = float(np.std(y - (a + b * f)))
    f_mean, f_sd = float(f.mean()), float(f.std())
    code = f'''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    g = float(regime.config.get("feedstock_grade", {GBAR}))
    f = {f_mean} + (g - {GBAR}) + rng.normal(0.0, {f_sd}, n)
    y = {a} + {b} * f + rng.normal(0.0, {resid}, n)
    return pd.DataFrame({{"feedstock": f, "outcome": y}})
'''
    server.submit(code)


def run_cuidadoso(server) -> None:
    df = server.observe("registros_linea", 1500)
    f, y, t = (df["feedstock"].to_numpy(float), df["outcome"].to_numpy(float),
               df["t"].to_numpy(float))

    # (1) cheap escape: stratify by time -- within-window the X-effect evaporates
    order = np.argsort(t)
    within = []
    for chunk in np.array_split(order, 8):
        if len(chunk) >= 30:
            a_w, b_w = _fit_line(f[chunk], y[chunk])
            within.append(b_w)
    b_within = float(np.median(within))  # ~0: X refuted inside the record itself

    # (2) dear escape: discriminating experiments over the FULL declared menu
    knob_effect = {}
    for knob in ("humidity", "temp", "line_speed"):
        lo = server.experiment(ExperimentDesign(config={knob: 3.0}, n=60))
        hi = server.experiment(ExperimentDesign(config={knob: 7.0}, n=60))
        knob_effect[knob] = {
            "dy": float(hi["outcome"].mean() - lo["outcome"].mean()),
            "df": float(hi["feedstock"].mean() - lo["feedstock"].mean()),
            "y_lo": float(lo["outcome"].mean()), "y_sd": float(np.std(
                np.concatenate([lo["outcome"], hi["outcome"]
                                - float(hi["outcome"].mean() - lo["outcome"].mean())]))),
            "f_sd": float(np.std(np.concatenate([lo["feedstock"], hi["feedstock"]
                                                 - float(hi["feedstock"].mean() - lo["feedstock"].mean())]))),
        }
    driver = max(knob_effect, key=lambda k: abs(knob_effect[k]["dy"]))
    eff = knob_effect[driver]
    yh = eff["dy"] / 4.0                       # outcome slope per unit of the real knob
    fh = eff["df"] / 4.0                       # feedstock slope per unit
    y0 = eff["y_lo"] - yh * 3.0 + yh * 5.0     # centered at knob=5
    f0 = float(np.mean([knob_effect[driver]["f_sd"]]))  # placeholder, recomputed below

    # (3) the supplier counterfactual: does grade move outcome? (it moves f only)
    lo_g = server.experiment(ExperimentDesign(config={"feedstock_grade": 2.0, driver: 5.0}, n=60))
    hi_g = server.experiment(ExperimentDesign(config={"feedstock_grade": 8.0, driver: 5.0}, n=60))
    g_coef_f = float((hi_g["feedstock"].mean() - lo_g["feedstock"].mean()) / 6.0)
    f_at5 = float(np.mean([lo_g["feedstock"].mean() + g_coef_f * 3.0,
                           hi_g["feedstock"].mean() - g_coef_f * 3.0]))

    # (4) meter sigma via replicas -> deconvolved outcome residual
    reps = server.observe("replicas_calibracion", 60)
    sigma = float(np.sqrt(max((reps["outcome__rep1"] - reps["outcome__rep2"]).var() / 2.0, 1e-4)))
    y_res_true = float(np.sqrt(max(eff["y_sd"] ** 2 - sigma ** 2, 0.25)))
    f_res = float(np.sqrt(max(eff["f_sd"] ** 2, 0.25)))

    # (5) the historical regime, PARAMETRICALLY (no empirical payload: the MDL
    # term prices embedded data -- the v2 payload lesson, re-learned by our own
    # robot): the era structure it already discovered (trends in t) + the
    # JOINT de-trended residual covariance, meter-deconvolved on outcome.
    af_t = np.polyfit(t, f, 1)
    ay_t = np.polyfit(t, y, 1)
    rf = f - np.polyval(af_t, t)
    ry = y - np.polyval(ay_t, t)
    cov = np.cov(np.column_stack([rf, ry]), rowvar=False)
    cov[1, 1] = max(cov[1, 1] - sigma ** 2, 0.25)
    code = f'''
import numpy as np
import pandas as pd

COV = np.array({[[float(v) for v in row] for row in cov]!r})

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    g = regime.config.get("feedstock_grade")
    h = regime.config.get("{driver}")
    if h is None:
        t = rng.uniform(0.0, 1.0, n)
        eps = rng.multivariate_normal([0.0, 0.0], COV, n)
        f = {float(af_t[1])} + {float(af_t[0])} * t + eps[:, 0]
        y = {float(ay_t[1])} + {float(ay_t[0])} * t + eps[:, 1]
        if g is not None:
            f = f + {g_coef_f} * (float(g) - {GBAR})
        return pd.DataFrame({{"feedstock": f, "outcome": y}})
    h = float(h)
    gg = {GBAR} if g is None else float(g)
    f = {f_at5} + {fh} * (h - 5.0) + {g_coef_f} * (gg - {GBAR}) + rng.normal(0.0, {f_res}, n)
    y = {y0} + {yh} * (h - 5.0) + rng.normal(0.0, {y_res_true}, n)
    return pd.DataFrame({{"feedstock": f, "outcome": y}})
'''
    server.submit(code)


def run_terco_noticia(server) -> None:
    """The stubborn under NEWS (D4 pair): same seduced policy, but it PLAYS
    THROUGH the event turn -- the notice fires, the HVAC log is available, and
    it ignores both (declared: not-incorporating is the vice under test)."""
    server.begin_turn(1)
    df = server.observe("registros_linea", 1500)
    for turn in (2, 3, 4):
        server.begin_turn(turn)  # turn 4: the notice fires; ignored
    f, y = df["feedstock"].to_numpy(float), df["outcome"].to_numpy(float)
    a, b = _fit_line(f, y)
    resid = float(np.std(y - (a + b * f)))
    f_mean, f_sd = float(f.mean()), float(f.std())
    code = f'''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    g = float(regime.config.get("feedstock_grade", {GBAR}))
    f = {f_mean} + (g - {GBAR}) + rng.normal(0.0, {f_sd}, n)
    y = {a} + {b} * f + rng.normal(0.0, {resid}, n)
    return pd.DataFrame({{"feedstock": f, "outcome": y}})
'''
    server.submit(code)


def run_cuidadoso_noticia(server) -> None:
    """Incorporates the news (D4 pair): headed to Historia X (it did NOT
    stratify on its own -- this robot isolates pure incorporation), the turn-4
    notice fires, it reads the HVAC log, maps the record's time trends into
    ambient space, re-estimates, and ships Historia Y with what remains."""
    server.begin_turn(1)
    df = server.observe("registros_linea", 1500)
    f, y, t = (df["feedstock"].to_numpy(float), df["outcome"].to_numpy(float),
               df["t"].to_numpy(float))
    server.begin_turn(2)
    server.begin_turn(3)
    notices = server.begin_turn(4)
    if not notices:
        raise RuntimeError("expected the sealed notice at turn 4")
    log = server.observe("log_hvac", 800)
    a_amb, b_amb = _fit_line(log["t"].to_numpy(float), log["ambient"].to_numpy(float))
    amb_rec = a_amb + b_amb * t                      # the record rows' implied ambient
    ay, by = _fit_line(amb_rec, y)                   # y in AMBIENT space (Historia Y)
    af, bf = _fit_line(amb_rec, f)
    reps = server.observe("replicas_calibracion", 60)
    sigma = float(np.sqrt(max((reps["outcome__rep1"] - reps["outcome__rep2"]).var() / 2.0, 1e-4)))
    y_res = float(np.sqrt(max(np.var(y - (ay + by * amb_rec)) - sigma ** 2, 0.25)))
    f_res_all = float(np.std(f - (af + bf * amb_rec)))
    lo_g = server.experiment(ExperimentDesign(config={"feedstock_grade": 2.0, "humidity": 5.0}, n=60))
    hi_g = server.experiment(ExperimentDesign(config={"feedstock_grade": 8.0, "humidity": 5.0}, n=60))
    g_coef = float((hi_g["feedstock"].mean() - lo_g["feedstock"].mean()) / 6.0)
    amb_sd_hist = float(np.std(amb_rec))
    code = f'''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    g = regime.config.get("feedstock_grade")
    h = regime.config.get("humidity")
    if h is None:
        amb = rng.uniform({float(a_amb)}, {float(a_amb + b_amb)}, n) + rng.normal(0.0, 0.4, n)
    else:
        amb = float(h) + rng.normal(0.0, 0.5, n)
    gg = {GBAR} if g is None else float(g)
    f = {af} + {bf} * amb + {g_coef} * (gg - {GBAR}) + rng.normal(0.0, {f_res_all}, n)
    y = {ay} + {by} * amb + rng.normal(0.0, {y_res}, n)
    return pd.DataFrame({{"feedstock": f, "outcome": y}})
'''
    server.submit(code)


ROBOTS = {
    "terco": run_terco,
    "cuidadoso": run_cuidadoso,
    "terco_noticia": run_terco_noticia,
    "cuidadoso_noticia": run_cuidadoso_noticia,
}


def run_robot(case_dir, robot: str, seed_offset: int) -> dict:
    from wager.harness.case_episode import build_world_server

    server = build_world_server(case_dir, seed_offset=seed_offset)
    ROBOTS[robot](server)
    if server.result is None:
        raise RuntimeError(f"robot {robot} (seed {seed_offset}): submission rejected by smoke")
    return {"robot": robot, "seed_offset": seed_offset,
            "R": server.result["R"], "R_uncl": server.result["R_unclipped"],
            "spent": server.budget_remaining}
