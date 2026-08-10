"""INSTRUMENTO (B) — polo del par D1 (server-side; el agente jamás lo ve).
El proceso sigue limpio; el autosampler encaja mal ciertos viales (falla intermitente a nivel vial): mismas lecturas rutinarias.
Física compartida: cases/d1_calibracion_common.py."""

from cases.d1_calibracion_common import load_instance, pole_truth_program, refresh_cache

POLE = "instrumento"
_params = load_instance()["params"]
refresh_cache(_params)
_prog = pole_truth_program(POLE, _params)


def sample(regime, n, seed):
    return _prog(regime, n, seed)


model = sample
