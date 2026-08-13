"""Decision and distributional functionals scored ON TOP of energy distance
(ARCHITECTURE §9.3).

ZERO-LLM ZONE. Pure numpy/pandas. A functional `F` maps a sample DataFrame to a
scalar; the per-item contribution to the combined distance is

    Σ_F  c_F · S_F( |F(pred) − F(real)| )

standardized BY TYPE so c_F is dimensionless and transferable across functionals
and suites (Decision Log v0.28 — the null-relative per-item normalization that
explodes at F(truth)≈F(null) is FORBIDDEN in the metric):

    exceedance     -> |ΔP|                     (raw; native [0,1])
    quantile       -> |Δ| / σ_truth(column)    (same play as energy standardization)
    subgroup_mean  -> |Δ| / σ_truth(column)
    expected_loss  -> |ΔL| / declared loss range
    projection_energy -> energy distance between standardized projected samples

An empty functional list -> zero extra distance: the combined score is then
IDENTICAL to the energy score of §9 (identity by construction, the dummy suite).
"""

import numpy as np
import pandas as pd

from wager.contracts import FunctionalSpec
from wager.reward.distance import energy_distance


def functional_value(spec: FunctionalSpec, df: pd.DataFrame) -> float:
    """F(samples) for one declared functional. Computed from samples, not params."""
    col = df[spec.column].to_numpy(dtype=float)
    if spec.name == "exceedance":
        hit = col < spec.threshold if spec.direction == "below" else col > spec.threshold
        return float(np.mean(hit))
    if spec.name == "quantile":
        return float(np.quantile(col, spec.tau))
    if spec.name == "subgroup_mean":
        raise NotImplementedError(
            "subgroup_mean needs a declared subgroup filter; add when a case requires it"
        )
    if spec.name == "expected_loss":
        raise NotImplementedError(
            "expected_loss needs a declared loss rule + range; add when a case requires it"
        )
    if spec.name == "projection_energy":
        raise TypeError("projection_energy is distribution-valued, not a scalar functional")
    raise ValueError(f"unknown functional: {spec.name}")


class FunctionalScorer:
    """Per-item functional contribution, built once from the truth sample.

    Holds F(real) and the truth column σ's; `extra_distance(pred)` returns the
    standardized, c_F-weighted sum added to the energy distance. Built with the
    SAME truth sample (CRN) the TruthSide standardizes against.
    """

    def __init__(
        self,
        specs: list[FunctionalSpec],
        truth_df: pd.DataFrame,
        columns: list[str],
        truth_std: np.ndarray,
        c_f: float | dict[str, float] = 1.0,
    ) -> None:
        # Trajectory worlds (spec docs/mundos-dinamicos.md 4.2): a time-indexed
        # functional (column "y@16") prices exactly the items whose DECLARED
        # grid carries that timestamp -- on other items it is inert, never a
        # crash. Static worlds are unaffected (their columns always exist).
        self.specs = [
            s
            for s in specs
            if (
                s.name == "projection_energy"
                and s.projection is not None
                and set(s.projection).issubset(columns)
            )
            or (s.name != "projection_energy" and s.column in columns)
        ]
        self.c_f = c_f
        self.col_std = {c: float(truth_std[i]) for i, c in enumerate(columns)}
        self.f_real: list[float | None] = []
        self.projected_real: list[np.ndarray | None] = []
        self.projected_std: list[float | None] = []
        for spec in self.specs:
            if spec.name == "projection_energy":
                projected = self._project(spec, truth_df)
                scale = float(projected.std())
                self.f_real.append(None)
                self.projected_real.append(projected)
                self.projected_std.append(scale if scale > 1e-12 else 1.0)
            else:
                self.f_real.append(functional_value(spec, truth_df))
                self.projected_real.append(None)
                self.projected_std.append(None)

    @staticmethod
    def _project(spec: FunctionalSpec, df: pd.DataFrame) -> np.ndarray:
        assert spec.projection is not None
        columns = list(spec.projection)
        weights = np.asarray([spec.projection[c] for c in columns], dtype=float)
        return df[columns].to_numpy(dtype=float) @ weights

    def _weight(self, spec: FunctionalSpec) -> float:
        return self.c_f.get(spec.name, 1.0) if isinstance(self.c_f, dict) else float(self.c_f)

    def _standardize(self, spec: FunctionalSpec, delta: float) -> float:
        if spec.name in ("quantile", "subgroup_mean"):
            return delta / (self.col_std.get(spec.column, 1.0) or 1.0)
        # exceedance (and 0-1 expected_loss): raw, already dimensionless in [0,1]
        return delta

    def extra_distance(self, pred: pd.DataFrame) -> float:
        """Σ c_F · S_F(|F(pred) − F(real)|). 0.0 when no functionals are declared
        (identity by construction)."""
        total = 0.0
        for spec, f_real, projected_real, projected_std in zip(
            self.specs, self.f_real, self.projected_real, self.projected_std
        ):
            if spec.name == "projection_energy":
                assert projected_real is not None and projected_std is not None
                projected_pred = self._project(spec, pred)
                distance = energy_distance(
                    (projected_real / projected_std)[:, None],
                    (projected_pred / projected_std)[:, None],
                )
                total += self._weight(spec) * max(distance, 0.0)
                continue
            assert f_real is not None
            f_pred = functional_value(spec, pred)
            total += self._weight(spec) * self._standardize(spec, abs(f_pred - f_real))
        return total
