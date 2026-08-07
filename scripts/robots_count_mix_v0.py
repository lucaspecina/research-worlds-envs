"""G2 (robots) + G3 (value map) certifier for the count-mixture pair.

Every robot plays through the REAL WorldServer (build_world_server) — this
doubles as the G5 interface smoke. Deliveries are CODE STRINGS submitted via
server.submit (sandboxed acceptance) and re-executed locally to compute the
primary instruments (S_struct on MIX / S_clean + espurio on SINGLE).

Robots (inference reflexes vs shopping reflexes, per ficha G2 + amendment):
  nunca_mezcla   archive 300 -> best single component -> deliver iid single
  siempre_mezcla archive 300 -> DOGMATIC forced two-component split (w=0.5,
                 separation 2.2*sqrt(mean)) regardless of the data
  todo_barato    archive to the cap, honest lattice fit
  azar           random menu actions (seeded) to ~70% budget, honest fit
  compra_caro    maximizes cost-per-row: n=1 experiments until budget floor
  cuidadoso      canonical script (plan §solución canónica): archive 300,
                 dispersion check, lattice fit, confirm with a repeats
                 experiment when mixture wins, deliver accordingly

Value map (G3): exact symmetric per-row KL between the two live hypotheses
(frozen MIX params vs mean-paired SINGLE) for iid actions; Monte Carlo
per-unit symmetric LLR for repeated-measures actions. Zero-LLM throughout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scipy.stats import poisson  # noqa: E402

from cases.count_mix_v0_common import (  # noqa: E402
    _DictRegime, _fit_mix2, _fit_negbin, _fit_poisson, forced_mix_program,
    load_instance, program_functionals, s_clean, s_struct,
    single_baseline_program, spurious_mixture_flag,
)
from wager.contracts import ExperimentDesign  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402

POLES = {"mix": "count_mix_v0", "single": "count_mix_twin_v0"}
ROBOT_SEED_BASE = 99280  # inside burned family, outside witness/battery/episode seeds


# --- delivery code templates (what a robot submits) --------------------------

SINGLE_POISSON_CODE = """import numpy as np
import pandas as pd
LAM = {lam!r}
def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 1]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    y = rng.poisson(LAM * speed, n).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
"""

SINGLE_NEGBIN_CODE = """import numpy as np
import pandas as pd
M, R = {m!r}, {r!r}
def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 2]))
    p = R / (R + M * speed)
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    y = rng.negative_binomial(R, p, n).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
"""

MIX_UNIT_CODE = """import numpy as np
import pandas as pd
W_HI, LAM_LO, LAM_HI = {w_hi!r}, {lam_lo!r}, {lam_hi!r}
def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 3]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    n_units = int(ids[-1]) + 1 if n else 0
    hi = rng.random(n_units) < W_HI
    lam_unit = np.where(hi, LAM_HI, LAM_LO) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
"""


def _exec_model(code: str):
    ns: dict = {}
    exec(code, ns)  # server-side robot code, ours
    return ns["model"]


def _honest_lattice_code(y: np.ndarray) -> str:
    """Fit the lattice honestly; deliver mixture-with-persistence if mix2 wins
    by BIC, else the best single component."""
    fits = [_fit_poisson(y), _fit_negbin(y), _fit_mix2(y)]
    n = len(y)
    bic = {f["name"]: f["k"] * np.log(n) - 2 * f["loglik"] for f in fits}
    best = min(bic, key=bic.get)
    if best == "mix2":
        p = [f for f in fits if f["name"] == "mix2"][0]["params"]
        return MIX_UNIT_CODE.format(w_hi=p["w_high"], lam_lo=p["lam_low"], lam_hi=p["lam_high"])
    if best == "negbin":
        p = [f for f in fits if f["name"] == "negbin"][0]["params"]
        return SINGLE_NEGBIN_CODE.format(m=p["mean"], r=1.0 / p["alpha"])
    return SINGLE_POISSON_CODE.format(lam=float(y.mean()))


# --- robots ------------------------------------------------------------------

def robot_nunca_mezcla(srv):
    y = srv.observe("archivo", 300)["y"].to_numpy(float)
    fits = [_fit_poisson(y), _fit_negbin(y)]
    best = max(fits, key=lambda f: f["loglik"])
    if best["name"] == "negbin":
        p = best["params"]
        return SINGLE_NEGBIN_CODE.format(m=p["mean"], r=1.0 / p["alpha"])
    return SINGLE_POISSON_CODE.format(lam=float(y.mean()))


def robot_siempre_mezcla(srv):
    y = srv.observe("archivo", 300)["y"].to_numpy(float)
    m = float(y.mean())
    sep = 2.2 * np.sqrt(max(m, 1e-9))
    return MIX_UNIT_CODE.format(w_hi=0.5, lam_lo=max(m - sep / 2, 0.05), lam_hi=m + sep / 2)


def robot_todo_barato(srv):
    y = srv.observe("archivo", 400)["y"].to_numpy(float)
    return _honest_lattice_code(y)


def robot_azar(srv, rng_seed: int):
    rng = np.random.default_rng(rng_seed)
    ys = []
    while (srv.budget_remaining if not callable(srv.budget_remaining) else srv.budget_remaining()) > 300:
        if rng.random() < 0.5:
            try:
                ys.append(srv.observe("archivo", int(rng.integers(20, 80)))["y"].to_numpy(float))
            except Exception:
                break
        else:
            d = ExperimentDesign(config={"speed": float(rng.uniform(0.8, 1.2)),
                                          "repeats_per_unit": float(rng.integers(1, 5))},
                                 n=int(rng.integers(10, 40)))
            ys.append(srv.experiment(d)["y"].to_numpy(float))
    y = np.concatenate(ys) if ys else np.array([0.0])
    return _honest_lattice_code(y)


def robot_compra_caro(srv):
    """Price-chaser: maximizes cost-per-row -> n=1 experiments only."""
    ys = []
    while (srv.budget_remaining if not callable(srv.budget_remaining) else srv.budget_remaining()) >= 41:
        d = ExperimentDesign(config={"speed": 1.2, "repeats_per_unit": 1.0}, n=1)
        ys.append(srv.experiment(d)["y"].to_numpy(float))
    y = np.concatenate(ys) if ys else np.array([0.0])
    # honest fit on its (tiny, off-speed) sample
    return _honest_lattice_code(y)


def robot_cuidadoso(srv):
    """Canonical script (plan): fit level, CHECK dispersion, open only if the
    data demand it, confirm with the discriminating repeats purchase."""
    y = srv.observe("archivo", 300)["y"].to_numpy(float)
    mean = float(y.mean())
    fano = float(y.var() / max(mean, 1e-9))
    fits = [_fit_poisson(y), _fit_negbin(y), _fit_mix2(y)]
    n = len(y)
    bic = {f["name"]: f["k"] * np.log(n) - 2 * f["loglik"] for f in fits}
    if bic["mix2"] < min(bic["poisson"], bic["negbin"]) and fano > 1.5:
        rep = srv.experiment(ExperimentDesign(config={"speed": 1.0, "repeats_per_unit": 3.0}, n=60))
        g = rep.groupby("unit_id")["y"].mean()
        between = float(g.var())
        within = float(rep.groupby("unit_id")["y"].var().mean())
        if between > within:  # unit-level heterogeneity confirmed
            p = [f for f in fits if f["name"] == "mix2"][0]["params"]
            return MIX_UNIT_CODE.format(w_hi=p["w_high"], lam_lo=p["lam_low"], lam_hi=p["lam_high"])
    best = max([f for f in fits if f["name"] != "mix2"], key=lambda f: f["loglik"])
    if best["name"] == "negbin":
        p = best["params"]
        return SINGLE_NEGBIN_CODE.format(m=p["mean"], r=1.0 / p["alpha"])
    return SINGLE_POISSON_CODE.format(lam=mean)


ROBOTS = {
    "nunca_mezcla": robot_nunca_mezcla,
    "siempre_mezcla": robot_siempre_mezcla,
    "todo_barato": robot_todo_barato,
    "azar": lambda srv: robot_azar(srv, ROBOT_SEED_BASE),
    "compra_caro": robot_compra_caro,
    "cuidadoso": robot_cuidadoso,
}


# --- instruments -------------------------------------------------------------

def build_instruments(inst):
    params, geo, tail_at = inst["params"], inst["geometry"], inst["tail_at"]
    from cases.count_mix_v0_common import _sample_counts

    def truth_mix(regime, n, seed):
        return _sample_counts("mix", params, regime, n, seed)

    def truth_single(regime, n, seed):
        return _sample_counts("single", params, regime, n, seed)

    truth_f = program_functionals(truth_mix, geo, tail_at)
    single_truth_f = program_functionals(truth_single, geo, tail_at)
    y_train = truth_mix(_DictRegime({"speed": 1.0}), inst["witness_n"],
                        inst["witness_sample_seed"])["y"].to_numpy(float)
    base_prog, _ = single_baseline_program(y_train)
    base_f = program_functionals(base_prog, geo, tail_at)
    forced_f = program_functionals(forced_mix_program(params["lam0"]), geo, tail_at)
    return {"geo": geo, "tail_at": tail_at, "truth_f": truth_f,
            "single_truth_f": single_truth_f, "base_f": base_f, "forced_f": forced_f}


def score_delivery(code: str, pole: str, instruments) -> dict:
    prog = _exec_model(code)
    f = program_functionals(prog, instruments["geo"], instruments["tail_at"])
    out = {"functionals": f}
    if pole == "mix":
        out.update(s_struct(f, instruments["truth_f"], instruments["base_f"]))
        out["F_mean"] = float(np.clip(
            1 - abs(f["mean"] - instruments["truth_f"]["mean"]) / instruments["truth_f"]["mean"], 0, 1))
    else:
        out.update(s_clean(f, instruments["single_truth_f"], instruments["forced_f"]))
        y_model = prog(_DictRegime({"speed": 1.0}), 2000, 777)["y"].to_numpy(float)
        out["espurio"] = spurious_mixture_flag(f, instruments["single_truth_f"], y_model)
    return out


# --- value map (G3) ----------------------------------------------------------

def _sym_kl_per_row(params, speed: float) -> float:
    la, lb, w, l0 = (params["lam_a"] * speed, params["lam_b"] * speed,
                     params["w"], params["lam0"] * speed)
    ymax = int(lb + 8 * np.sqrt(lb) + 8)
    ks = np.arange(ymax + 1)
    p_mix = (1 - w) * poisson.pmf(ks, la) + w * poisson.pmf(ks, lb)
    p_single = poisson.pmf(ks, l0)
    p_mix, p_single = p_mix / p_mix.sum(), p_single / p_single.sum()
    kl_ms = float(np.sum(p_mix * (np.log(p_mix + 1e-300) - np.log(p_single + 1e-300))))
    kl_sm = float(np.sum(p_single * (np.log(p_single + 1e-300) - np.log(p_mix + 1e-300))))
    return 0.5 * (kl_ms + kl_sm)


def _sym_llr_per_unit(params, speed: float, repeats: int, n_mc: int = 4000, seed: int = 5) -> float:
    rng = np.random.default_rng(seed)
    la, lb, w, l0 = (params["lam_a"] * speed, params["lam_b"] * speed,
                     params["w"], params["lam0"] * speed)

    def unit_llr(y_unit):
        ll_mix = logsumexp_pair(
            np.log(1 - w) + poisson.logpmf(y_unit, la).sum(),
            np.log(w) + poisson.logpmf(y_unit, lb).sum())
        ll_single = poisson.logpmf(y_unit, l0).sum()
        return ll_mix - ll_single

    def logsumexp_pair(a, b):
        m = max(a, b)
        return m + np.log(np.exp(a - m) + np.exp(b - m))

    # E_mix[llr] - E_single[llr], symmetric discriminability per unit
    tot_mix = 0.0
    for _ in range(n_mc):
        lam = lb if rng.random() < w else la
        tot_mix += unit_llr(rng.poisson(lam, repeats))
    tot_single = 0.0
    for _ in range(n_mc):
        tot_single += unit_llr(rng.poisson(l0, repeats))
    return 0.5 * (tot_mix / n_mc - tot_single / n_mc)


def value_map(params) -> dict:
    actions = {
        "observe_archivo_100": {"cost": 50.0, "value": 100 * _sym_kl_per_row(params, 1.0)},
        "exp_speed1.0_n50": {"cost": 90.0, "value": 50 * _sym_kl_per_row(params, 1.0)},
        "exp_speed1.2_n50": {"cost": 90.0, "value": 50 * _sym_kl_per_row(params, 1.2)},
        "exp_repeats3_n20": {"cost": 60.0, "value": 20 * _sym_llr_per_unit(params, 1.0, 3)},
        "exp_repeats4_n20": {"cost": 60.0, "value": 20 * _sym_llr_per_unit(params, 1.0, 4)},
    }
    for a in actions.values():
        a["value_per_cost"] = a["value"] / a["cost"]
    vpc = [a["value_per_cost"] for a in actions.values()]
    vals = [a["value"] for a in actions.values()]
    costs = [a["cost"] for a in actions.values()]
    ratio = max(vpc) / max(min(vpc), 1e-9)
    corr = float(np.corrcoef(costs, vals)[0, 1])
    return {"actions": actions, "hetero_ratio": float(ratio),
            "price_value_corr": corr,
            "discriminant_cost_frac": 60.0 / 1000.0}


# --- main --------------------------------------------------------------------

def main() -> int:
    inst = load_instance()
    instruments = build_instruments(inst)
    results: dict = {}
    for pole, case in POLES.items():
        results[pole] = {}
        for i, (name, fn) in enumerate(ROBOTS.items()):
            srv = build_world_server(ROOT / "cases" / case, seed_offset=ROBOT_SEED_BASE + i)
            code = fn(srv)
            sub = srv.submit(code)
            rem = srv.budget_remaining
            rem = rem() if callable(rem) else rem
            sc = score_delivery(code, pole, instruments)
            entry = {"accepted": bool(sub.accepted), "spent": float(1000.0 - rem)}
            if pole == "mix":
                entry.update({"S_struct": sc["S_struct"], "F_mean": sc["F_mean"]})
            else:
                entry.update({"S_clean": sc["S_clean"],
                              "espurio": sc["espurio"]["spurious"]})
            results[pole][name] = entry

    vm = value_map(inst["params"])

    g2 = {
        "nunca_mezcla_pierde_en_MIX": results["mix"]["nunca_mezcla"]["S_struct"] <= 0.10,
        "siempre_mezcla_pierde_en_SINGLE": (results["single"]["siempre_mezcla"]["S_clean"] <= 0.10
                                            and results["single"]["siempre_mezcla"]["espurio"]),
        "cuidadoso_gana_MIX": results["mix"]["cuidadoso"]["S_struct"] >= 0.90,
        "cuidadoso_gana_SINGLE": (results["single"]["cuidadoso"]["S_clean"] >= 0.90
                                  and not results["single"]["cuidadoso"]["espurio"]),
        "cuidadoso_presupuesto_le_70pct": max(results["mix"]["cuidadoso"]["spent"],
                                              results["single"]["cuidadoso"]["spent"]) <= 700.0,
        "compra_caro_pierde_en_algun_polo": (results["mix"]["compra_caro"]["S_struct"] <= 0.60
                                             or results["mix"]["compra_caro"]["F_mean"] < 0.60
                                             or results["single"]["compra_caro"]["S_clean"] <= 0.60
                                             or results["single"]["compra_caro"]["espurio"]),
        "todos_aceptados": all(e["accepted"] for pole in results.values() for e in pole.values()),
    }
    g3 = {
        "hetero_vpc_ratio_ge_3": vm["hetero_ratio"] >= 3.0,
        "discriminante_pagable": vm["discriminant_cost_frac"] <= 0.30,
        "precio_no_chivato": abs(vm["price_value_corr"]) < 0.95,
    }
    notes = {
        "todo_barato_vs_cuidadoso": {
            "S_struct_todo_barato": results["mix"]["todo_barato"]["S_struct"],
            "nota": ("en este host nivel-1 el archivo ALCANZA por diseño (la señal se sirve "
                     "barata); el reflejo de shopping empata con el cuidadoso en MIX y la "
                     "compuerta de shopping se vuelve vinculante recién en hosts nivel-2+ "
                     "(señal en residuos/condicional). Se reporta, no se fuerza."),
        },
        "pricing": "per-ROW (n = mediciones; enmienda consolidada de ficha 2026-08-07)",
    }
    verdict = "PASS" if all(g2.values()) and all(g3.values()) else "REVIEW"
    out = {"robots": results, "value_map": vm, "G2": g2, "G3": g3,
           "notes": notes, "verdict": verdict}

    # merge into certificates.json (both poles)
    for case in POLES.values():
        path = ROOT / "cases" / case / "certificates.json"
        cert = json.loads(path.read_text())
        cert["G2_G3_G5"] = out
        cert["gates"].update({f"G2_{k}": bool(v) for k, v in g2.items()})
        cert["gates"].update({f"G3_{k}": bool(v) for k, v in g3.items()})
        cert["gates"]["G5_interface_smoke"] = bool(g2["todos_aceptados"])
        cert["pending_gates"] = ["smoke con agentes reales (paso 5, necesita .env)"]
        cert["verdict"] = ("PASS" if all(cert["gates"].values()) else "REVIEW")
        path.write_text(json.dumps(cert, indent=2))

    print(json.dumps(out, indent=2, default=str))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
