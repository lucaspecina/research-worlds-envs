"""Corrupted source VIEWS over the clean mechanism (ARCHITECTURE §1/§2.2,
implemented for world 3 -- Decision Log v0.49/v0.50/v0.51/v0.52).

The invariant this module exists to protect: `world.sample()` is ALWAYS the
clean mechanism (the scorer's truth); the agent's `observe()` -- and, for the
measurement channel, `experiment()` too (v0.9: the experiment bypasses the
HISTORICAL SAMPLING, never the measurement channel) -- receive views corrupted
per the source's DECLARED pipeline: selection filter (sampling layer) then
measurement channel (channel layer). Factory rivals train on these same views
(the naive anchor believes the record). Deterministic per (source, seed).
"""

from types import SimpleNamespace
from typing import Callable

import numpy as np
import pandas as pd

from wager.contracts.episode import BatchEffect, MeasurementChannel, SelectionFilter, SourceConfig
from wager.reward.seeds import derive_seed

_SEL_TAG = 811   # rep tags for derived rngs; disjoint from scoring reps (j >= 0)
_CH_TAG = 823
_BATCH_TAG = 829
_OVERSAMPLE = 4
_MAX_TRIES = 8


def apply_batch(df: pd.DataFrame, be: BatchEffect, rng: np.random.Generator,
                historical: bool) -> pd.DataFrame:
    """Per-batch meter offsets (#9, ADR 0078). historical=True applies the
    record's confound: rows chunked along the era's driver ramp (sorted by
    sort_key + sort_noise) and offsets DRIFTING with batch index. Fresh runs
    (experiments) chunk by arrival with idiosyncratic offsets only -- the
    meter's batch structure survives (v0.9), the confound does not."""
    out = df.reset_index(drop=True).copy()
    n = len(out)
    if historical and be.assign == "driver_ramp" and be.sort_key is not None:
        key = out[be.sort_key].to_numpy() + rng.normal(0.0, be.sort_noise, n)
        order = np.argsort(key)
    else:
        order = np.arange(n)
    batch_of = np.empty(n, dtype=int)
    batch_of[order] = np.arange(n) // be.batch_size
    n_batches = int(batch_of.max()) + 1
    offsets = rng.normal(0.0, be.offset_sd, n_batches)
    if historical:
        offsets = offsets + be.drift_per_batch * (np.arange(n_batches) - (n_batches - 1) / 2.0)
    out[be.column] = out[be.column] + offsets[batch_of]
    out[be.id_column] = batch_of.astype(float)
    return out


def apply_selection(df: pd.DataFrame, sel: SelectionFilter) -> pd.DataFrame:
    score = sum(w * df[c] for c, w in sel.weights.items())
    mask = score > sel.threshold if sel.keep == "above" else score < sel.threshold
    return df[mask]


def apply_channel(df: pd.DataFrame, ch: MeasurementChannel, rng: np.random.Generator) -> pd.DataFrame:
    out = df.copy()
    if ch.replicates == 1:
        out[ch.column] = out[ch.column] + rng.normal(0.0, ch.noise_sd, len(out))
        return out
    # replicated readings (v0.51): two independent measurements of the same unit;
    # the true column is REPLACED by the pair (the meter never shows the truth)
    base = out.pop(ch.column)
    for r in range(ch.replicates):
        out[f"{ch.column}__rep{r + 1}"] = base + rng.normal(0.0, ch.noise_sd, len(out))
    return out


def source_view(world_sample: Callable, source: SourceConfig, n: int, seed: int) -> pd.DataFrame:
    """The agent-facing draw from one source, per the DECLARED pipeline_order
    (v0.53-1): select_then_measure (survivorship: filter sees TRUE values; v0
    default) or measure_then_select (admission by recorded symptom: filter sees
    MEASURED values -- with replicates, the FIRST reading). Selection
    oversamples deterministically until n rows survive."""
    ns = SimpleNamespace(config=dict(source.config), context=dict(source.context), horizon=None)
    measure_first = source.pipeline_order == "measure_then_select"

    def measured(df, rng):
        return apply_channel(df, source.channel, rng) if source.channel is not None else df

    def filter_frame(df):
        if source.selection is None:
            return df
        if not measure_first:
            return apply_selection(df, source.selection)
        # filter on MEASURED values; a replicated column resolves to the FIRST
        # reading (the admission measurement, v0.53-1)
        sel = source.selection
        scored = pd.DataFrame({
            c: df[c] if c in df.columns else df[f"{c}__rep1"] for c in sel.weights
        }, index=df.index)
        return df.loc[apply_selection(scored, sel).index]

    def archived(df):
        # per-batch offsets (#9, ADR 0078) with the HISTORICAL confound, then
        # archival censoring (#7, ADR 0077): the RECORD format clips one column
        # at the old bench's limit -- applied last (post-channel: what gets
        # clipped is the recorded value; with replicates, every rep). Records
        # only: experiment_view applies the meter's batch offsets WITHOUT the
        # confound and never censors.
        if source.batch is not None:
            df = apply_batch(df, source.batch,
                             np.random.default_rng(derive_seed(seed, _BATCH_TAG)),
                             historical=True)
        cen = source.censoring
        if cen is None:
            return _visible(df, source)
        cols = [c for c in df.columns if c == cen.column or c.startswith(f"{cen.column}__rep")]
        out = df.copy()
        for c in cols:
            out[c] = out[c].clip(upper=cen.limit) if cen.side == "above" else out[c].clip(lower=cen.limit)
        return _visible(out, source)

    if source.selection is None and not measure_first:
        df = measured(world_sample(ns, n, seed), np.random.default_rng(derive_seed(seed, _CH_TAG)))
        return archived(df).reset_index(drop=True)

    frames, got, s = [], 0, seed
    for _ in range(_MAX_TRIES):
        draw = world_sample(ns, n * _OVERSAMPLE, s)
        if measure_first:
            draw = measured(draw, np.random.default_rng(derive_seed(s, _CH_TAG)))
        kept = filter_frame(draw)
        frames.append(kept)
        got += len(kept)
        if got >= n:
            break
        s = derive_seed(s, _SEL_TAG)
    df = pd.concat(frames, ignore_index=True)
    if len(df) < n:
        raise ValueError(
            f"selection filter too harsh: {len(df)}/{n} rows after {_MAX_TRIES} tries"
        )
    df = df.head(n)
    if not measure_first and source.channel is not None:
        rng = np.random.default_rng(derive_seed(seed, _CH_TAG))
        df = apply_channel(df, source.channel, rng)
    return archived(df).reset_index(drop=True)


def _visible(df: pd.DataFrame, source: SourceConfig) -> pd.DataFrame:
    """Drop the columns the instrument/record never reports (D2, ADR 0081) --
    the LAST step of every view."""
    hidden = [c for c in source.hidden_columns if c in df.columns]
    return df.drop(columns=hidden) if hidden else df


def experiment_view(world_sample: Callable, regime, source_channel: MeasurementChannel | None,
                    n: int, seed: int, source_batch: BatchEffect | None = None,
                    hidden_columns: tuple[str, ...] = ()) -> pd.DataFrame:
    """Experimental draw: randomization bypasses the historical SELECTION (that
    is what it buys) but NEVER the measurement channel (v0.9 rule -- the
    thermometer is still the same thermometer; test asserts this). The meter's
    per-batch offsets (#9) apply too -- fresh batches, arrival order, NO
    historical drift/ramp (the confound is what randomization buys off)."""
    df = world_sample(regime, n, seed)
    if source_channel is not None:
        rng = np.random.default_rng(derive_seed(seed, _CH_TAG))
        df = apply_channel(df, source_channel, rng)
    if source_batch is not None:
        df = apply_batch(df, source_batch,
                         np.random.default_rng(derive_seed(seed, _BATCH_TAG)),
                         historical=False)
    hidden = [c for c in hidden_columns if c in df.columns]
    if hidden:
        df = df.drop(columns=hidden)
    return df.reset_index(drop=True)
