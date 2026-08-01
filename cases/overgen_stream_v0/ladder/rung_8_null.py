import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"outcome": rng.normal(18.73125783511101, 2.5443422505307676, n)})
