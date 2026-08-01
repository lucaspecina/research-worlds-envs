from wager.report.overgen_belief import shared_transfer_phenotype


SHARED = '''
import numpy as np
import pandas as pd
def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    line = int(regime.config["line"])
    d = float(regime.config["driver"])
    return pd.DataFrame({"outcome": rng.normal(line * 0.1 + d * (10-d), 0.7, n)})
'''


FRAGMENTED = '''
import numpy as np
import pandas as pd
def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    line = int(regime.config["line"])
    d = float(regime.config["driver"])
    return pd.DataFrame({"outcome": rng.normal(line * d * 1.5, 0.7, n)})
'''


def test_shared_shape_with_line_intercepts_is_eligible():
    result = shared_transfer_phenotype(SHARED, n=300)
    assert result["eligible"]


def test_line_specific_shapes_are_not_eligible():
    result = shared_transfer_phenotype(FRAGMENTED, n=300)
    assert not result["eligible"]
    assert result["reason"] == "target_belief_absent"
