"""Zero-LLM certifier for the ODE second-wave structural-opening arms (v0).

Default command certifies and exits nonzero on any failed gate:

    python scripts/certify_ode_second_wave_v0.py [--seed-offset N]

Gates (ficha 2026-08-02-ficha-probe-ode-apertura-estructural-v0):
  G1 surface identity      brief/battery/ladder byte-identical; meta identical
                           except case_id + truth knobs; describe() identical.
  G2 line-A identity       clean truth and noisy source views byte-identical
                           across arms on Line A.
  G3 report form/noise     the delivered commissioning report has the same
                           shape/grid/units in every arm, the SAME noise
                           realization, and struct - retain equals the second
                           wave exactly.
  G4 dose calibration      PARAM and STRUCT sit at comparable distance from
                           the A-law forecast; per-unit plateaus match.
  G5 phase selection       BIC + unit-CV + unit-holdout pick 1 phase in
                           RETAIN/PARAM and 2 phases in STRUCT on exactly the
                           served report rows.
  G6 single-phase loss     the best single-phase fit loses materially only in
                           STRUCT.
  G7 reward headroom       the real reward path scores the frozen A-law
                           transfer reference: near-ceiling in RETAIN,
                           materially punished in PARAM/STRUCT; a legal
                           mean-curve fit recovers most of the gap.

No LLM anywhere. No agent runner in this phase (ADR 0173 discovery slice).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.factory.case_loader import load_meta, load_world_module  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.source_view import source_view  # noqa: E402
from wager.reward.episode_score import score_episode_submission  # noqa: E402

from cases import ode_second_wave_v0_common as physics  # noqa: E402

ARM_DIRS = {
    "retain": ROOT / "cases" / "ode_second_wave_retain_v0",
    "param": ROOT / "cases" / "ode_second_wave_param_v0",
    "struct": ROOT / "cases" / "ode_second_wave_struct_v0",
}
OUT = ROOT / "scripts" / "out" / "ode_second_wave_v0"

DOSE_GAP_REL_MAX = 0.10
RETAIN_DOSE_MAX = 0.5
PHASES_EXPECTED = {"retain": 1, "param": 1, "struct": 2}
STRUCT_LOSS_RATIO_MIN = 1.10
OTHER_LOSS_RATIO_MAX = 1.10
R_REF_RETAIN_MIN = 0.60
R_REF_GAP_MIN = 0.12
REWARD_DOSE_REL_GAP_MAX = 0.25
CROSS_TOPOLOGY_GAP_MIN = 0.03
ORACLE_RECOVERY_MAX = 0.30
RETAIN_REF_CURVE_ERR_MAX = 1.0

# The mechanical M_pre reference: Line A's law applied to every line (the
# transfer forecast). Frozen; doubles as the dose anchor.
TRANSFER_REF_CODE = '''
import numpy as np
import pandas as pd

K0, K_SD, K_MIN = 100.0, 8.0, 20.0
X0, X0_SD, X0_MIN = 2.0, 0.4, 0.5
R, R_DISP = 0.55, 0.10


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    K = np.clip(rng.normal(K0, K_SD, n), K_MIN, None)[:, None]
    x0 = np.clip(rng.normal(X0, X0_SD, n), X0_MIN, None)[:, None]
    r = (R * np.exp(rng.normal(0.0, R_DISP, n)))[:, None]
    a = (K - x0) / x0
    y = K / (1.0 + a * np.exp(-r * t[None, :]))
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), t.size),
                         "t": np.tile(t, n), "y": y.ravel()})
'''


def _ns(config: dict, context: dict) -> SimpleNamespace:
    return SimpleNamespace(config=dict(config), context=dict(context), horizon=None)


def _meta_core(meta_dict: dict) -> dict:
    """Meta minus the fields that legitimately differ per arm."""
    core = dict(meta_dict)
    core.pop("case_id", None)
    core.pop("operators", None)
    return core


def gate_surface_identity() -> dict:
    briefs = {a: (d / "brief.md").read_bytes() for a, d in ARM_DIRS.items()}
    batteries = {a: (d / "battery.json").read_bytes() for a, d in ARM_DIRS.items()}
    ladders = {
        a: {p.name: p.read_bytes() for p in sorted((d / "ladder").glob("rung_*.py"))}
        for a, d in ARM_DIRS.items()
    }
    metas = {
        a: json.loads((d / "meta.json").read_text(encoding="utf-8"))
        for a, d in ARM_DIRS.items()
    }
    describes = {
        a: build_world_server(d).describe() for a, d in ARM_DIRS.items()
    }
    reference = "retain"
    checks = {
        "briefs_identical": all(b == briefs[reference] for b in briefs.values()),
        "batteries_identical": all(b == batteries[reference] for b in batteries.values()),
        "ladders_identical": all(l == ladders[reference] for l in ladders.values()),
        "meta_identical_except_truth": all(
            _meta_core(m) == _meta_core(metas[reference]) for m in metas.values()
        ),
        "case_ids_distinct": len({m["case_id"] for m in metas.values()}) == 3,
        "describe_identical": all(d == describes[reference] for d in describes.values()),
    }
    return {"checks": checks, "all": all(checks.values())}


def gate_line_a_identity(seed_offset: int) -> dict:
    worlds = {a: load_world_module(d) for a, d in ARM_DIRS.items()}
    meta = load_meta(ARM_DIRS["retain"])
    history = meta.episode.observe_sources["line_a_history"]
    grids = [physics.HISTORY_GRID, (0.0, 4.0, 8.0, 12.0, 16.0)]
    seeds = [910_100 + seed_offset, 910_101 + seed_offset]
    clean_equal, view_equal = [], []
    for seed in seeds:
        for grid in grids:
            regime = _ns({}, {"line": "A", "t_grid": tuple(grid)})
            frames = {a: w.sample(regime, 40, seed) for a, w in worlds.items()}
            clean_equal.append(
                all(frames[a].equals(frames["retain"]) for a in frames)
            )
        views = {
            a: source_view(w.sample, history, 40, seed) for a, w in worlds.items()
        }
        view_equal.append(all(views[a].equals(views["retain"]) for a in views))
    checks = {
        "clean_line_a_identical": all(clean_equal),
        "history_view_identical": all(view_equal),
    }
    return {"checks": checks, "all": all(checks.values())}


def _fire_report(arm: str, seed_offset: int):
    server = build_world_server(ARM_DIRS[arm], seed_offset=seed_offset)
    notices = server.fire_event(0, turn_idx=8)
    deliveries = server.pop_deliveries()
    if len(deliveries) != 1:
        raise RuntimeError(f"{arm}: expected exactly one delivery, got {len(deliveries)}")
    variable, frame = deliveries[0]
    return server, notices, variable, frame


def gate_report_identity(seed_offset: int) -> dict:
    meta = load_meta(ARM_DIRS["retain"])
    event = meta.episode.events[0]
    n_units = event.auto_deliver_n
    grid = tuple(float(v) for v in event.source.context["t_grid"])
    reports, notices, variables = {}, {}, {}
    for arm in ARM_DIRS:
        _, notice, variable, frame = _fire_report(arm, seed_offset)
        reports[arm], notices[arm], variables[arm] = frame, notice, variable

    # The event is the server's first seed consumer: its draw seed is exact.
    seed_event = 740_000 + seed_offset * 100_000 + 1
    worlds = {a: load_world_module(d) for a, d in ARM_DIRS.items()}
    expected = {
        a: source_view(w.sample, event.source, n_units, seed_event)
        for a, w in worlds.items()
    }
    clean = {
        a: w.sample(_ns(event.source.config, dict(event.source.context)), n_units, seed_event)
        for a, w in worlds.items()
    }
    noise = {
        a: reports[a]["y"].to_numpy() - clean[a]["y"].to_numpy() for a in ARM_DIRS
    }
    wave2 = physics.struct_second_wave_component(n_units, seed_event, grid).ravel()

    reference = reports["retain"]
    checks = {
        "notices_identical": all(n == notices["retain"] for n in notices.values()),
        "delivery_variable_identical": all(
            v == variables["retain"] for v in variables.values()
        ),
        "columns_and_shape_identical": all(
            list(r.columns) == list(reference.columns) and r.shape == reference.shape
            for r in reports.values()
        ),
        "grid_and_units_identical": all(
            r["t"].equals(reference["t"]) and r["unit_id"].equals(reference["unit_id"])
            for r in reports.values()
        ),
        "delivery_matches_declared_source_view": all(
            reports[a].equals(expected[a]) for a in ARM_DIRS
        ),
        "noise_realization_identical": all(
            float(np.max(np.abs(noise[a] - noise["retain"]))) < 1e-9 for a in ARM_DIRS
        ),
        "struct_minus_retain_is_second_wave_exactly": bool(
            float(
                np.max(
                    np.abs(
                        reports["struct"]["y"].to_numpy()
                        - reports["retain"]["y"].to_numpy()
                        - wave2
                    )
                )
            )
            < 1e-8
        ),
    }
    return {
        "checks": checks,
        "report_rows": int(reference.shape[0]),
        "report_units": int(n_units),
        "seed_event": seed_event,
        "all": all(checks.values()),
    }


def gate_dose_calibration() -> dict:
    doses = {arm: physics.dose_from_transfer(arm) for arm in physics.ARMS}
    gap = abs(doses["param"] - doses["struct"])
    rel_gap = gap / max((doses["param"] + doses["struct"]) / 2.0, 1e-9)

    z = physics._draws_b(20_000, physics._MC_SEED)
    p_param = physics._b_components("param", z)
    p_struct = physics._b_components("struct", z)
    plateau_gap = float(
        np.max(np.abs(p_param["K"] - (p_struct["K1"] + p_struct["K2"])))
    )
    checks = {
        "retain_dose_zero": doses["retain"] <= RETAIN_DOSE_MAX,
        "param_struct_dose_comparable": rel_gap <= DOSE_GAP_REL_MAX,
        "per_unit_plateaus_match": plateau_gap < 1e-9,
    }
    return {
        "doses_from_transfer": {k: float(v) for k, v in doses.items()},
        "relative_gap_param_vs_struct": float(rel_gap),
        "per_unit_plateau_max_gap": plateau_gap,
        "checks": checks,
        "all": all(checks.values()),
    }


def gate_phase_selection(reports: dict) -> dict:
    fits = {arm: physics.fit_phase_selection(frame) for arm, frame in reports.items()}
    checks = {
        f"{arm}_selects_{expected}_phase": fits[arm]["phases_selected"] == expected
        for arm, expected in PHASES_EXPECTED.items()
    }
    return {"fits": fits, "checks": checks, "all": all(checks.values())}


def gate_single_phase_loss(fits: dict) -> dict:
    ratios = {arm: fits[arm]["single_phase_holdout_ratio"] for arm in fits}
    checks = {
        "struct_single_phase_loses_materially": ratios["struct"] >= STRUCT_LOSS_RATIO_MIN,
        "retain_single_phase_adequate": ratios["retain"] <= OTHER_LOSS_RATIO_MAX,
        "param_single_phase_adequate": ratios["param"] <= OTHER_LOSS_RATIO_MAX,
    }
    return {"holdout_ratios_1p_over_2p": ratios, "checks": checks, "all": all(checks.values())}


def _score(server, code: str) -> dict:
    try:
        result = score_episode_submission(
            code=code,
            world_sample=server.world_sample,
            world_source=server.scoring.world_source,
            naive_code=server.scoring.naive_code,
            null_code=server.scoring.null_code,
            battery=server.scoring.battery,
            columns=server.columns,
            params=server.scoring.params,
            functionals=server.scoring.functionals,
            truth_code=server.scoring.truth_code,
            enrich_regime=server.scoring.enrich_regime,
            sample_transform=server.scoring.sample_transform,
        )
        return {"scoreable": True, "R": float(result["R"])}
    except Exception as exc:  # noqa: BLE001 -- certifier preserves raw failure
        return {"scoreable": False, "error": repr(exc)}


def _mean_curve_error(arm: str, curve: np.ndarray) -> float:
    truth = physics.mean_curve(arm, "B", physics.DOSE_GRID)
    return float(np.mean(np.abs(curve - truth)))


def gate_reward_headroom(fits: dict, seed_offset: int) -> dict:
    grid = np.asarray(physics.DOSE_GRID, dtype=float)
    transfer_curve = physics.transfer_mean_curve(physics.DOSE_GRID)
    scores, ref_err, legal_err = {}, {}, {}
    for arm, case_dir in ARM_DIRS.items():
        server = build_world_server(case_dir, seed_offset=seed_offset)
        scores[arm] = _score(server, TRANSFER_REF_CODE)
        ref_err[arm] = _mean_curve_error(arm, transfer_curve)
        fit = fits[arm]
        if fit["phases_selected"] == 2:
            legal_curve = physics._predict_2p(np.asarray(fit["theta_2p"]), grid)
        else:
            legal_curve = physics._predict_1p(np.asarray(fit["theta_1p"]), grid)
        legal_err[arm] = _mean_curve_error(arm, legal_curve)

    # Cross the two legal ceilings.  PARAM-in-STRUCT is the decisive
    # scoreable one-phase counterfactual: it reaches the same final plateau
    # and has matched update dose, but never opens a second phase.
    truth_codes = {
        arm: (case_dir / "truth_code.py").read_text(encoding="utf-8")
        for arm, case_dir in ARM_DIRS.items()
    }
    truth_scores = {
        arm: _score(build_world_server(case_dir, seed_offset=seed_offset), truth_codes[arm])
        for arm, case_dir in ARM_DIRS.items()
    }
    cross_scores = {
        "param_code_in_struct_world": _score(
            build_world_server(ARM_DIRS["struct"], seed_offset=seed_offset),
            truth_codes["param"],
        ),
        "struct_code_in_param_world": _score(
            build_world_server(ARM_DIRS["param"], seed_offset=seed_offset),
            truth_codes["struct"],
        ),
    }

    r = {arm: scores[arm].get("R") for arm in scores}
    reward_gains = {
        arm: (None if r[arm] is None else 1.0 - float(r[arm]))
        for arm in ("param", "struct")
    }
    reward_gain_rel_gap = (
        abs(reward_gains["param"] - reward_gains["struct"])
        / max(np.mean(list(reward_gains.values())), 1e-9)
        if all(value is not None for value in reward_gains.values())
        else None
    )
    cross_param_struct_r = cross_scores["param_code_in_struct_world"].get("R")
    checks = {
        "reward_path_runs_in_every_arm": all(s["scoreable"] for s in scores.values()),
        "transfer_ref_near_ceiling_in_retain": (
            r["retain"] is not None and r["retain"] >= R_REF_RETAIN_MIN
        ),
        "transfer_ref_punished_in_param": (
            None not in (r["retain"], r["param"])
            and r["retain"] - r["param"] >= R_REF_GAP_MIN
        ),
        "transfer_ref_punished_in_struct": (
            None not in (r["retain"], r["struct"])
            and r["retain"] - r["struct"] >= R_REF_GAP_MIN
        ),
        "reward_update_dose_comparable": (
            bool(
                reward_gain_rel_gap is not None
                and reward_gain_rel_gap <= REWARD_DOSE_REL_GAP_MAX
            )
        ),
        "truth_code_scores_at_ceiling_all": all(
            row.get("scoreable") and row.get("R", 0.0) >= 0.999
            for row in truth_scores.values()
        ),
        "wrong_one_phase_topology_is_penalized_in_struct": (
            cross_param_struct_r is not None
            and 1.0 - cross_param_struct_r >= CROSS_TOPOLOGY_GAP_MIN
        ),
        "legal_fit_recovers_param": legal_err["param"] <= ORACLE_RECOVERY_MAX * ref_err["param"],
        "legal_fit_recovers_struct": legal_err["struct"] <= ORACLE_RECOVERY_MAX * ref_err["struct"],
        "transfer_ref_already_right_in_retain": ref_err["retain"] <= RETAIN_REF_CURVE_ERR_MAX,
    }
    return {
        "R_transfer_reference": r,
        "scores_raw": scores,
        "truth_scores": truth_scores,
        "cross_topology_scores": cross_scores,
        "reward_gain_from_transfer": reward_gains,
        "reward_gain_relative_gap_param_vs_struct": reward_gain_rel_gap,
        "mean_curve_error_transfer": {k: float(v) for k, v in ref_err.items()},
        "mean_curve_error_legal_fit": {k: float(v) for k, v in legal_err.items()},
        "checks": checks,
        "all": all(checks.values()),
    }


def run_certificates(seed_offset: int) -> dict:
    report = {"kind": "ode_second_wave_v0_certificate", "seed_offset": seed_offset}
    report["G1_surface_identity"] = gate_surface_identity()
    report["G2_line_a_identity"] = gate_line_a_identity(seed_offset)
    report["G3_report_identity"] = gate_report_identity(seed_offset)
    report["G4_dose_calibration"] = gate_dose_calibration()

    reports = {arm: _fire_report(arm, seed_offset)[3] for arm in ARM_DIRS}
    g5 = gate_phase_selection(reports)
    report["G5_phase_selection"] = g5
    report["G6_single_phase_loss"] = gate_single_phase_loss(g5["fits"])
    report["G7_reward_headroom"] = gate_reward_headroom(g5["fits"], seed_offset)

    gates = [k for k in report if k.startswith("G")]
    report["gates_passed"] = {k: report[k]["all"] for k in gates}
    report["all"] = all(report[k]["all"] for k in gates)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    report = run_certificates(args.seed_offset)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"certificate_seed{args.seed_offset}.json"
    path.write_text(json.dumps(report, indent=2, default=float), encoding="utf-8")

    for gate, passed in report["gates_passed"].items():
        print(f"{'PASS' if passed else 'FAIL'}  {gate}")
    print(f"\ncertificate -> {path}")
    print("ALL GATES PASS" if report["all"] else "CERTIFICATE FAILED")
    return 0 if report["all"] else 1


if __name__ == "__main__":
    sys.exit(main())
