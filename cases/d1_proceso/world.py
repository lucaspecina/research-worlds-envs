"""PROCESO (A) — polo del par D1 (server-side; el agente jamás lo ve).
Una fraccion PI de los lotes nuevos nace degradada (mezcla real a nivel lote); el espectrometro esta sano.
Física compartida: cases/d1_calibracion_common.py."""

from cases.d1_calibracion_common import load_instance, pole_truth_program, refresh_cache

POLE = "proceso"
_params = load_instance()["params"]
refresh_cache(_params)
_prog = pole_truth_program(POLE, _params)


def sample(regime, n, seed):
    return _prog(regime, n, seed)


model = sample
