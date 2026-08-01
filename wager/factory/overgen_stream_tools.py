"""Build/certification helpers for the longitudinal overgen pair (ADR 0162).

This module is researcher-side only.  The two case world.py files remain
self-contained because world source is also the sandboxed truth anchor.
"""

from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from wager.contracts import Battery, BatteryItem, ExperimentDesign
from wager.contracts.world import Regime
from wager.harness.case_episode import build_world_server
from wager.reward.sandbox import SandboxedSubmission

LINES = (1, 2, 3, 4, 5)
GRID = np.round(np.arange(0.0, 10.001, 0.1), 3)
LEVELS_LOW = (0.5, 1.5, 2.5, 3.5)
LEVELS_HIGH = (5.0, 6.2, 7.4, 8.6, 9.6)
REPORT_TURN = 5


def _ns(config):
    return SimpleNamespace(config=dict(config), context={}, horizon=None)


def _law_fit(df):
    d = df["driver"].to_numpy(float)
    y = df["outcome"].to_numpy(float)
    x = d * (10.0 - d) / 25.0
    X = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    return float(coef[0]), float(coef[1]), float(max(np.std(resid), 0.55))


def _law_values(a, b, d):
    d = np.asarray(d, float)
    return a + b * d * (10.0 - d) / 25.0


def _pchip_values(df):
    from scipy.interpolate import PchipInterpolator

    d = df["driver"].to_numpy(float)
    y = df["outcome"].to_numpy(float)
    rounded = np.round(d, 3)
    xs = np.unique(rounded)
    means = np.array([np.mean(y[rounded == x]) for x in xs])
    if xs.size < 3:
        return np.interp(GRID, xs, means)
    fit = PchipInterpolator(xs, means, extrapolate=True)
    values = fit(np.clip(GRID, xs[0], xs[-1]))
    return values


def _submission(tables, sds):
    entries = []
    xs = ", ".join(f"{x:g}" for x in GRID)
    for line in LINES:
        ys = ", ".join(f"{y:.4f}" for y in tables[line])
        entries.append(
            f"    {line}: (np.array([{xs}]), np.array([{ys}]), {float(sds[line]):.4f}),"
        )
    return f'''import numpy as np
import pandas as pd

T = {{
{chr(10).join(entries)}
}}

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    X, Y, sd = T[int(regime.config["line"])]
    d = np.full(n, float(regime.config["driver"]))
    return pd.DataFrame({{"outcome": np.interp(d, X, Y) + rng.normal(0.0, sd, n)}})
'''


def _read_prefix(server):
    return server.observe("qualification_report", 96)


def _receive_report(server):
    payloads = []
    for turn in range(1, REPORT_TURN + 1):
        server.begin_turn(turn)
        payloads.extend(server.pop_deliveries())
    found = [df for name, df in payloads if name == "commissioning_report"]
    if len(found) != 1:
        raise RuntimeError(f"expected one commissioning report, got {len(found)}")
    return found[0]


def _base_model(prefix, sd_scale=1.0):
    line1 = prefix[prefix["line"] == 1]
    a, b, sd = _law_fit(line1)
    tables = {line: _law_values(a, b, GRID) for line in LINES}
    sds = {line: sd * sd_scale for line in LINES}
    return a, b, sd, tables, sds


def run_never_update(server):
    prefix = _read_prefix(server)
    _receive_report(server)  # delivered and ignored, as the reflex specifies
    _, _, _, tables, sds = _base_model(prefix)
    server.submit(_submission(tables, sds))


def run_fragment_all(server):
    prefix = _read_prefix(server)
    report = _receive_report(server)
    a, b, sd, tables, sds = _base_model(prefix)
    del a, b
    for line in (2, 3, 4, 5):
        local = np_concat_rows(prefix[prefix["line"] == line], report[report["line"] == line])
        tables[line] = _pchip_values(local)
        sds[line] = sd
    server.submit(_submission(tables, sds))


def run_adaptive(server):
    prefix = _read_prefix(server)
    report = _receive_report(server)
    a, b, sd, tables, sds = _base_model(prefix)
    for line in (2, 3, 4, 5):
        rows = report[report["line"] == line]
        residual = rows["outcome"].to_numpy(float) - _law_values(
            a, b, rows["driver"].to_numpy(float)
        )
        # Mean absolute standardized residual: ~0.8 under transfer, well above
        # 1.35 for the certified deviations. This is a legal recipe, not truth.
        evidence = float(np.mean(np.abs(residual)) / max(sd, 1e-6))
        if evidence >= 1.35:
            local = np_concat_rows(prefix[prefix["line"] == line], rows)
            tables[line] = _pchip_values(local)
            sds[line] = sd
    server.submit(_submission(tables, sds))


def np_concat_rows(a, b):
    return pd.concat([a, b], ignore_index=True)


def _ledger_frame(record):
    """Reconstruct one agent-visible DataFrame from a JSON-safe ledger row."""
    payload = record["data"]
    return pd.DataFrame(payload["data"], columns=payload["columns"])


def _prior_moments(code, lines, *, n=2000):
    moments = {}
    with SandboxedSubmission(code, ["outcome"], timeout_s=10.0) as submission:
        for line in lines:
            means = []
            spreads = []
            for j, driver in enumerate(GRID):
                frame = submission.run(
                    Regime(config={"line": line, "driver": float(driver)}, context={}),
                    n,
                    970_000 + 1000 * line + j,
                )
                values = frame["outcome"].to_numpy(float)
                means.append(float(np.mean(values)))
                spreads.append(float(np.std(values, ddof=1)))
            moments[line] = (
                np.asarray(means, dtype=float),
                np.asarray(spreads, dtype=float),
            )
    return moments


def _correction_wrapper(prior_code, corrections):
    """Rename the prior model and append local mean/spread updates."""
    tree = ast.parse(prior_code)
    models = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "model"
    ]
    if len(models) != 1 or isinstance(models[0], ast.AsyncFunctionDef):
        raise ValueError("prior artifact must define exactly one top-level synchronous model")
    models[0].name = "_prior_model"
    renamed = ast.unparse(ast.fix_missing_locations(tree))
    entries = []
    xs = ", ".join(f"{x:g}" for x in GRID)
    for line, (prior_mean, delta, scale) in corrections.items():
        ms = ", ".join(f"{value:.8f}" for value in prior_mean)
        ys = ", ".join(f"{value:.8f}" for value in delta)
        ss = ", ".join(f"{value:.8f}" for value in scale)
        entries.append(
            f"    {line}: (np.array([{xs}]), np.array([{ms}]), "
            f"np.array([{ys}]), np.array([{ss}])),"
        )
    return renamed + f'''

import numpy as np

_REFERENCE_CORRECTIONS = {{
{chr(10).join(entries)}
}}

def model(regime, n, seed):
    frame = _prior_model(regime, n, seed)
    line = int(regime.config["line"])
    if line not in _REFERENCE_CORRECTIONS:
        return frame
    driver = float(regime.config["driver"])
    if driver <= 4.0:
        return frame
    X, PRIOR_MEAN, DELTA, SCALE = _REFERENCE_CORRECTIONS[line]
    out = frame.copy()
    prior_mean = float(np.interp(driver, X, PRIOR_MEAN))
    target_mean = prior_mean + float(np.interp(driver, X, DELTA))
    scale = float(np.interp(driver, X, SCALE))
    out["outcome"] = target_mean + (out["outcome"] - prior_mean) * scale
    return out
'''


def build_reference_from_ledger(ledger, *, update_threshold=1.35, prior_code=None):
    """Build the frozen v0 legal reference using only agent-visible rows.

    This deliberately implements the already-certified adaptive recipe.  It is
    a reference updater, not a claim of a unique Bayesian posterior: learn the
    shared law from the qualification report, then specialize a line only when
    later high-range residuals clear the prospectively fixed threshold.
    """
    qualification = [
        _ledger_frame(record)
        for record in ledger
        if record.get("kind") == "observe"
        and record.get("source") == "qualification_report"
    ]
    if not qualification:
        raise ValueError("ledger has no qualification_report observation")
    prefix = pd.concat(qualification, ignore_index=True)
    required = {"line", "driver", "outcome"}
    if not required <= set(prefix.columns):
        raise ValueError("qualification ledger rows lack line/driver/outcome")

    later = [
        _ledger_frame(record)
        for record in ledger
        if not (
            record.get("kind") == "observe"
            and record.get("source") == "qualification_report"
        )
        and required <= set(record.get("data", {}).get("columns", []))
    ]
    post = (
        pd.concat(later, ignore_index=True)
        if later else pd.DataFrame(columns=list(required))
    )

    a, b, sd, tables, sds = _base_model(prefix)
    evidence_by_line = {}
    updated_lines = []
    for line in (2, 3, 4, 5):
        diagnostic = post[(post["line"] == line) & (post["driver"] > 4.0)]
        if diagnostic.empty:
            evidence = None
        else:
            residual = diagnostic["outcome"].to_numpy(float) - _law_values(
                a, b, diagnostic["driver"].to_numpy(float)
            )
            evidence = float(np.mean(np.abs(residual)) / max(sd, 1e-6))
        evidence_by_line[str(line)] = evidence
        if evidence is not None and evidence >= update_threshold:
            local = pd.concat(
                [prefix[prefix["line"] == line], post[post["line"] == line]],
                ignore_index=True,
            )
            tables[line] = _pchip_values(local)
            sds[line] = sd
            updated_lines.append(line)

    diagnostics = {
        "kind": "frozen_v0_reference_not_unique_posterior",
        "ledger_records": len(ledger),
        "qualification_rows": int(len(prefix)),
        "later_rows": int(len(post)),
        "update_threshold": float(update_threshold),
        "standardized_mean_abs_residual": evidence_by_line,
        "updated_lines": updated_lines,
    }
    rebuilt = _submission(tables, sds)
    if prior_code is None:
        return rebuilt, diagnostics

    diagnostics["kind"] = "prior_preserving_v1_reference_not_unique_posterior"
    if not updated_lines:
        diagnostics["prior_preserved_byte_exact"] = True
        diagnostics["correction_max_abs"] = {}
        return prior_code, diagnostics

    prior_moments = _prior_moments(prior_code, updated_lines)
    corrections = {}
    for line in updated_lines:
        prior_mean, prior_sd = prior_moments[line]
        delta = np.asarray(tables[line], dtype=float) - prior_mean
        scale = np.full_like(delta, float(sds[line])) / np.maximum(prior_sd, 1e-6)
        delta[GRID <= 4.0] = 0.0
        scale[GRID <= 4.0] = 1.0
        corrections[line] = (prior_mean, delta, scale)
    diagnostics["prior_preserved_byte_exact"] = False
    diagnostics["preserved_lines"] = [line for line in LINES if line not in updated_lines]
    diagnostics["preserved_region"] = "driver<=4 for every line"
    diagnostics["correction_max_abs"] = {
        str(line): float(np.max(np.abs(delta)))
        for line, (_, delta, _) in corrections.items()
    }
    diagnostics["spread_scale_range"] = {
        str(line): [float(np.min(scale)), float(np.max(scale))]
        for line, (_, _, scale) in corrections.items()
    }
    return _correction_wrapper(prior_code, corrections), diagnostics


ROBOTS = {
    "adaptive": run_adaptive,
    "never_update": run_never_update,
    "fragment_all": run_fragment_all,
}


def run_robot(case_dir, robot, seed_offset):
    server = build_world_server(case_dir, seed_offset=seed_offset)
    ROBOTS[robot](server)
    if server.result is None:
        raise RuntimeError(f"robot {robot} did not submit")
    return {"R": server.result["R"], "left": server.budget_remaining}


def _load_world(case_dir):
    spec = importlib.util.spec_from_file_location(f"stream_world_{case_dir.name}", case_dir / "world.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_battery():
    items = []
    seed = 88001
    for line in LINES:
        for driver in LEVELS_LOW:
            items.append(BatteryItem(
                weight=0.012,
                seed_world=seed,
                regime=Regime(config={"line": line, "driver": driver}, context={}),
            ))
            seed += 1
        for driver in LEVELS_HIGH:
            items.append(BatteryItem(
                weight=0.028,
                seed_world=seed,
                regime=Regime(config={"line": line, "driver": driver}, context={}),
            ))
            seed += 1
    return Battery(items=items)


def _write_truth(case_dir, world):
    dense = np.round(np.arange(0.0, 10.001, 0.05), 3)
    rows = []
    xs = ", ".join(f"{x:g}" for x in dense)
    for line in LINES:
        ys = ", ".join(f"{y:.5f}" for y in world.curve(line, dense))
        rows.append(f"    {line}: (np.array([{xs}]), np.array([{ys}])),")
    code = f'''import numpy as np
import pandas as pd

T = {{
{chr(10).join(rows)}
}}

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    X, Y = T[int(regime.config["line"])]
    d = np.full(n, float(regime.config["driver"]))
    return pd.DataFrame({{"outcome": np.interp(d, X, Y) + rng.normal(0.0, {world.NOISE!r}, n)}})
'''
    (case_dir / "truth_code.py").write_text(code, encoding="utf-8", newline="\n")


def _write_ladder(case_dir, world):
    prefix = world.sample(_ns({"__qualification": 1}), 96, 81001)
    _, _, _, tables, sds = _base_model(prefix, sd_scale=1.8)
    naive = _submission(tables, sds)
    mean = float(prefix["outcome"].mean())
    spread = float(max(prefix["outcome"].std(), 1.0))
    null = f'''import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({{"outcome": rng.normal({mean!r}, {spread!r}, n)}})
'''
    ladder = case_dir / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_7_coarse_shared.py").write_text(naive, encoding="utf-8", newline="\n")
    (ladder / "rung_8_null.py").write_text(null, encoding="utf-8", newline="\n")


def _prefix_identity(case_dir, world):
    sibling_name = "overgen_stream_twin_v0" if world.POLE == "limited" else "overgen_stream_v0"
    sibling_dir = case_dir.parent / sibling_name
    if not sibling_dir.exists():
        return False
    other = _load_world(sibling_dir)
    queries = [
        ({"__qualification": 1}, 96, 81001),
        ({"line": 1, "driver": 9.0}, 20, 81002),
        ({"line": 3, "driver": 2.5}, 20, 81003),
    ]
    for config, n, seed in queries:
        a = world.sample(_ns(config), n, seed)
        b = other.sample(_ns(config), n, seed)
        if not a.equals(b):
            return False
    return True


def build_and_check(case_dir):
    case_dir = Path(case_dir)
    world = _load_world(case_dir)
    _build_battery().to_json_file(case_dir / "battery.json")
    _write_truth(case_dir, world)
    _write_ladder(case_dir, world)

    checks = {
        "pole": world.POLE,
        "prefix_byte_identical": _prefix_identity(case_dir, world),
    }
    report = world.sample(_ns({"__commissioning": 1}), 64, 82001)
    signal = {}
    for line in (2, 3, 4, 5):
        rows = report[(report["line"] == line) & (report["driver"] > 4.0)]
        delta = world.curve(line, rows["driver"].to_numpy(float)) - world.law(
            rows["driver"].to_numpy(float)
        )
        signal[str(line)] = round(float(np.sqrt(np.mean(delta ** 2)) / world.NOISE), 3)
    checks["diagnostic_signal_rms_noise"] = signal

    server = build_world_server(case_dir, seed_offset=3)
    accepted = server.submit((case_dir / "truth_code.py").read_text(encoding="utf-8"))
    checks["contract_runs"] = bool(accepted.accepted)
    checks["truth_R"] = round(float(server.result["R"]), 4)

    scores = {}
    for robot in ROBOTS:
        vals = []
        for seed_offset in (20, 21, 22):
            vals.append(round(float(run_robot(case_dir, robot, seed_offset)["R"]), 4))
        scores[robot] = vals
    checks["robots"] = scores

    a = np.asarray(scores["adaptive"])
    never = np.asarray(scores["never_update"])
    fragment = np.asarray(scores["fragment_all"])
    if world.POLE == "limited":
        checks["behavior_gates"] = {
            "adaptive_reaches": bool(a.min() >= 0.72),
            "never_update_loses": bool(np.min(a - never) >= 0.12),
            "selective_beats_change_all": bool(np.min(a - fragment) >= 0.02),
        }
    else:
        checks["behavior_gates"] = {
            "maintain_reaches": bool(never.min() >= 0.80),
            "adaptive_reaches": bool(a.min() >= 0.80),
            "fragment_all_loses": bool(np.min(a - fragment) >= 0.03),
            "adaptive_matches_maintain": bool(np.max(np.abs(a - never)) <= 0.06),
        }
    checks["all"] = bool(
        checks["prefix_byte_identical"]
        and checks["contract_runs"]
        and checks["truth_R"] >= 0.999
        and all(checks["behavior_gates"].values())
    )
    (case_dir / "check.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, indent=2))
    return checks
