"""Kill test para una firma funcional de dos tipos persistentes.

Este script NO construye un mundo, no certifica un diseño ni llama agentes. Prueba un esqueleto
matemático exploratorio:

* cada unidad tiene un tipo oculto z en {-1, +1};
* la misma unidad responde bajo k condiciones;
* cada respuesta aislada parece venir de una sola población;
* el vector completo cae en una de dos trayectorias separadas.

La verdad se enfrenta, con acceso oráculo, a rivales de una sola banda continua. El rival más
fuerte es una envolvente no paramétrica: la mejor densidad simétrica y unimodal posible sobre la
dirección que separa las trayectorias. Si esa envolvente queda cerca de la verdad, el diseño muere.

Uso:
    .venv/bin/python scripts/design_hidden_groups_signature.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize
from scipy.stats import gennorm, norm, t


# Línea exploratoria para ordenar el barrido, no gate científico congelado. Antes de elegir una
# instancia hay que fijar qué diferencia cuenta como material y volver a correr el barrido.
PROVISIONAL_GAP_NATS_PER_UNIT = 0.10
GRID_DX = 0.0025
EPS = 1e-300


@dataclass(frozen=True)
class Candidate:
    conditions: int
    signal_per_condition: float

    @property
    def projected_signal(self) -> float:
        return self.signal_per_condition * np.sqrt(self.conditions)


def truth_pdf(x: np.ndarray, separation: float) -> np.ndarray:
    """Proyección suficiente: mezcla 50/50 de N(-m,1) y N(+m,1)."""
    return 0.5 * norm.pdf(x, -separation, 1.0) + 0.5 * norm.pdf(x, separation, 1.0)


def _grid(separation: float) -> tuple[np.ndarray, np.ndarray, float]:
    limit = max(10.0, separation + 8.0)
    x = np.arange(-limit + GRID_DX / 2.0, limit, GRID_DX)
    p = truth_pdf(x, separation)
    p /= float(np.sum(p) * GRID_DX)
    return x, p, GRID_DX


def kl_on_grid(p: np.ndarray, q: np.ndarray, dx: float) -> float:
    q = np.maximum(q, EPS)
    q /= float(np.sum(q) * dx)
    return float(np.sum(p * (np.log(np.maximum(p, EPS)) - np.log(q))) * dx)


def gaussian_gap(separation: float) -> float:
    x, p, dx = _grid(separation)
    sd = np.sqrt(1.0 + separation**2)
    return kl_on_grid(p, norm.pdf(x, 0.0, sd), dx)


def student_t_gap(separation: float) -> tuple[float, dict]:
    x, p, dx = _grid(separation)

    def objective(theta: np.ndarray) -> float:
        scale = np.exp(theta[0])
        df = 2.0 + np.exp(theta[1])
        return kl_on_grid(p, t.pdf(x / scale, df=df) / scale, dx)

    starts = [
        np.log([np.sqrt(1 + separation**2), 3.0]),
        np.log([max(separation, 0.5), 10.0]),
        np.log([max(separation / 2, 0.5), 1.0]),
    ]
    best = min(
        (minimize(objective, start, method="L-BFGS-B", bounds=[(-4, 4), (-6, 8)])
         for start in starts),
        key=lambda fit: fit.fun,
    )
    return float(best.fun), {
        "scale": float(np.exp(best.x[0])),
        "df": float(2.0 + np.exp(best.x[1])),
        "optimizer_success": bool(best.success),
    }


def generalized_normal_gap(separation: float) -> tuple[float, dict]:
    x, p, dx = _grid(separation)

    def objective(theta: np.ndarray) -> float:
        scale = np.exp(theta[0])
        shape = np.exp(theta[1])
        return kl_on_grid(p, gennorm.pdf(x, beta=shape, scale=scale), dx)

    starts = [
        np.log([np.sqrt(1 + separation**2), 2.0]),
        np.log([max(separation, 0.5), 8.0]),
        np.log([max(separation, 0.5), 1.0]),
    ]
    best = min(
        (minimize(objective, start, method="L-BFGS-B", bounds=[(-4, 4), (-4, np.log(30.0))])
         for start in starts),
        key=lambda fit: fit.fun,
    )
    return float(best.fun), {
        "scale": float(np.exp(best.x[0])),
        "shape": float(np.exp(best.x[1])),
        "optimizer_success": bool(best.success),
    }


def uniform_latent_gap(separation: float) -> tuple[float, dict]:
    """U~Uniform(-width,width), X=U+Normal(0, noise): una banda continua."""
    x, p, dx = _grid(separation)

    def density(width: float, noise: float) -> np.ndarray:
        if width < 1e-6:
            return norm.pdf(x, 0.0, noise)
        return (
            norm.cdf((x + width) / noise) - norm.cdf((x - width) / noise)
        ) / (2.0 * width)

    def objective(theta: np.ndarray) -> float:
        width, noise = np.exp(theta)
        return kl_on_grid(p, density(width, noise), dx)

    starts = [
        np.log([max(separation, 0.25), 1.0]),
        np.log([max(1.5 * separation, 0.5), 0.5]),
        np.log([max(0.5 * separation, 0.25), 1.5]),
    ]
    best = min(
        (minimize(objective, start, method="L-BFGS-B", bounds=[(-7, 5), (-5, 4)])
         for start in starts),
        key=lambda fit: fit.fun,
    )
    return float(best.fun), {
        "half_width": float(np.exp(best.x[0])),
        "noise": float(np.exp(best.x[1])),
        "optimizer_success": bool(best.success),
    }


def _pava_nonincreasing(values: np.ndarray) -> np.ndarray:
    """KL/MLE projection of probabilities onto a non-increasing sequence."""
    blocks: list[list[float]] = []
    for value in values:
        blocks.append([float(value), 1.0])
        while len(blocks) >= 2:
            prev_mean = blocks[-2][0] / blocks[-2][1]
            last_mean = blocks[-1][0] / blocks[-1][1]
            if prev_mean >= last_mean:
                break
            right = blocks.pop()
            left = blocks.pop()
            blocks.append([left[0] + right[0], left[1] + right[1]])
    out = np.empty(len(values), dtype=float)
    cursor = 0
    for total, count in blocks:
        size = int(count)
        out[cursor:cursor + size] = total / count
        cursor += size
    return out


def unimodal_oracle_gap(separation: float) -> tuple[float, dict]:
    """Best arbitrary symmetric unimodal density, discretized on |x|.

    This is deliberately stronger than any named one-band family above. It may use a flat
    plateau and arbitrary tails, but its density cannot rise again away from the center.
    """
    limit = max(10.0, separation + 8.0)
    radius = np.arange(GRID_DX / 2.0, limit, GRID_DX)
    folded_mass = 2.0 * truth_pdf(radius, separation) * GRID_DX
    folded_mass /= float(np.sum(folded_mass))
    fitted_mass = _pava_nonincreasing(folded_mass)
    fitted_mass /= float(np.sum(fitted_mass))
    gap = float(np.sum(
        folded_mass * (
            np.log(np.maximum(folded_mass, EPS))
            - np.log(np.maximum(fitted_mass, EPS))
        )
    ))
    plateau_bins = 1
    while (
        plateau_bins < len(fitted_mass)
        and np.isclose(fitted_mass[plateau_bins], fitted_mass[0], rtol=1e-10, atol=1e-15)
    ):
        plateau_bins += 1
    return gap, {
        "plateau_half_width": float(plateau_bins * GRID_DX),
        "grid_dx": GRID_DX,
        "class": "oracle symmetric unimodal density on separating projection",
    }


def evaluate(candidate: Candidate) -> dict:
    m = candidate.projected_signal
    student_gap, student_params = student_t_gap(m)
    gennorm_gap, gennorm_params = generalized_normal_gap(m)
    uniform_gap, uniform_params = uniform_latent_gap(m)
    oracle_gap, oracle_meta = unimodal_oracle_gap(m)
    gaps = {
        "matched_full_gaussian": gaussian_gap(m),
        "optimized_student_t": student_gap,
        "optimized_generalized_normal": gennorm_gap,
        "optimized_uniform_continuous_latent": uniform_gap,
        "unimodal_nonparametric_oracle": oracle_gap,
    }
    strongest_named = min(
        (name for name in gaps if name != "unimodal_nonparametric_oracle"),
        key=gaps.get,
    )
    return {
        "conditions_per_unit": candidate.conditions,
        "signal_per_condition_in_noise_sd": candidate.signal_per_condition,
        "each_single_condition_is_unimodal": bool(candidate.signal_per_condition <= 1.0),
        "projected_signal_in_noise_sd": float(m),
        "gaps_nats_per_new_unit": gaps,
        "strongest_named_rival": strongest_named,
        "strongest_named_gap": float(gaps[strongest_named]),
        "oracle_gate": {
            "provisional_line": PROVISIONAL_GAP_NATS_PER_UNIT,
            "observed": float(oracle_gap),
            "above_provisional_line": bool(
                oracle_gap >= PROVISIONAL_GAP_NATS_PER_UNIT
            ),
        },
        "fit_details": {
            "student_t": student_params,
            "generalized_normal": gennorm_params,
            "uniform_continuous_latent": uniform_params,
            "unimodal_oracle": oracle_meta,
        },
    }


def main() -> int:
    candidates = [
        Candidate(k, signal)
        for k in (2, 3, 4, 6, 8, 10)
        for signal in (0.50, 0.65, 0.75, 0.85, 0.95)
    ]
    rows = [evaluate(candidate) for candidate in candidates]
    passing = [
        row
        for row in rows
        if row["oracle_gate"]["above_provisional_line"]
    ]
    selected = min(
        passing,
        key=lambda row: (row["conditions_per_unit"], row["signal_per_condition_in_noise_sd"]),
        default=None,
    )
    payload = {
        "construct": (
            "two separated persistent response trajectories on new units; literal class names "
            "in code are irrelevant"
        ),
        "does_not_count": [
            "independent wide noise per condition",
            "one continuous band of intermediate trajectories",
            "memorizing unit identifiers",
        ],
        "truth": (
            "z in {-1,+1}; response vector y = z*a*s + iid N(0,1), with a<1 so every "
            "single-condition marginal remains unimodal"
        ),
        "evaluation": "joint log-score per response vector of a previously unseen unit",
        "selection_rule": (
            "smallest number of conditions, then smallest per-condition signal, that leaves "
            f">={PROVISIONAL_GAP_NATS_PER_UNIT} nats/new-unit against the nonparametric unimodal "
            "oracle; this line is exploratory, not a certification gate"
        ),
        "first_candidate_above_provisional_line": selected,
        "all_candidates": rows,
        "status": (
            "exploratory mathematical skeleton only; no frozen materiality threshold, "
            "world, story, task UI, certification, or agent run"
        ),
    }
    print(json.dumps(payload, indent=2))
    return 0 if selected is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
