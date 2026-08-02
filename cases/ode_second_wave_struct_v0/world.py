"""STRUCT arm of the ODE second-wave probe: Line B = A's logistic + a second,
delayed wave.

Server-side truth. The agent never sees this file. Physics shared with the
other arms via cases/ode_second_wave_v0_common.py; Line A and every
pre-commissioning surface are byte-identical across arms.
"""

from cases.ode_second_wave_v0_common import arm_sample

ARM = "struct"


def sample(regime, n, seed):
    return arm_sample(ARM, regime, n, seed)


model = sample


def experiment_guard(design, turn, fired_events):
    """Operational availability (server-side, same text in every arm)."""
    line = str(design.context.get("line", "A")).upper()
    if not fired_events:
        if line == "B":
            raise ValueError(
                "line B is not commissioned yet: the trial bench cannot run line-B batches"
            )
        return
    raise ValueError(
        "commissioning window: the trial bench is reserved for line-B integration "
        "for the remainder of this episode; consolidate the model from existing records"
    )
