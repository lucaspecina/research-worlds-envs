"""PROCESO (A) — polo del par D2 (server-side; el agente jamás lo ve).
La reaccion lateral degrada una fraccion de lotes que CRECE con T (pi(T)); el espectrometro esta sano.
Física: cases/d2_decision_common.py (pi(T)) sobre cases/d1_calibracion_common.py."""

import json
from pathlib import Path

from cases.d1_calibracion_common import refresh_cache
from cases.d2_decision_common import pole_truth_program_d2

POLE = "proceso"
_params = json.loads((Path(__file__).resolve().parents[1] / "d2_proceso"
                      / "instance.json").read_text())["params"]
refresh_cache(_params)
_prog = pole_truth_program_d2(POLE, _params)


def sample(regime, n, seed):
    return _prog(regime, n, seed)


model = sample
