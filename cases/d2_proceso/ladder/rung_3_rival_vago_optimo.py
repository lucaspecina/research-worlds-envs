"""EL ANCLA CERO (rung-0 pattern, ADR 0175): el mejor rival SIN el salto —
gaussiana momento-matcheada por T, coeficientes CONGELADOS en certificación."""
import numpy as np
import pandas as pd

CM = [91.58120366944584, -3.441996766037518, 0.022149541243315186]    # mu(T)      = CM[0] + CM[1]*(T-1) + CM[2]*(T-1)**2
CS = [0.583983380143015, 0.7782445385725985, -1.134683695693752]    # log sd(T)  = CS[0] + CS[1]*(T-1) + CS[2]*(T-1)**2


def model(regime, n, seed):
    config = getattr(regime, "config", None) or {}
    T = min(max(float(config.get("T", 1.0)), 0.6), 1.4)
    mu = CM[0] + CM[1] * (T - 1.0) + CM[2] * (T - 1.0) ** 2
    sd = min(max(float(np.exp(CS[0] + CS[1] * (T - 1.0) + CS[2] * (T - 1.0) ** 2)),
                 0.3), 6.0)
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                          "y": mu + rng.normal(0, sd, int(n))})
