"""Factory and zero-LLM oracle guards for the frozen plan probe v0."""

import json

import numpy as np
import pytest

from wager.factory.plan_probe_v0 import (
    SCENARIOS,
    VALIDATION_SEED_START,
    ProbeConfig,
    certify_family,
    evaluate_fixed_cohort,
    exact_posterior,
    generate_candidate,
    sample_truth,
    write_factory_report,
)
from wager.reward.decision_oracle import (
    DecisionInstrument,
    NormalMixture,
    exact_optimal_action,
    monte_carlo_optimal_action,
    normal_mixture_energy_distance,
    propagation_fraction,
)


def test_normal_mixture_and_exact_action_are_deterministic():
    mix = NormalMixture(
        np.array([0.25, 0.75]),
        np.array([-1.0, 2.0]),
        np.array([0.5, 1.0]),
    )
    assert mix.quantile(0.1) < mix.mean < mix.quantile(0.9)
    assert np.array_equal(mix.sample(20, 17), mix.sample(20, 17))

    instrument = DecisionInstrument(
        actions=(1.0, 2.0),
        safety_threshold=-10.0,
        risk_penalty=0.0,
        reopen_cost_low=0.1,
        reopen_cost_high=1.0,
    )
    decision = exact_optimal_action(
        lambda action: NormalMixture(
            np.array([1.0]), np.array([action]), np.array([0.2])
        ),
        instrument,
    )
    assert decision.action == 2.0

    with pytest.raises(ValueError, match="at least two"):
        DecisionInstrument(
            actions=(1.0,),
            safety_threshold=0.0,
            risk_penalty=0.0,
            reopen_cost_low=0.1,
            reopen_cost_high=1.0,
        )


def test_normal_mixture_energy_distance_is_exact_and_seed_free():
    left = NormalMixture(
        np.array([1.0]), np.array([0.0]), np.array([1.0])
    )
    right = NormalMixture(
        np.array([0.5, 0.5]), np.array([-2.0, 2.0]), np.array([0.5, 0.5])
    )
    assert normal_mixture_energy_distance(left, left) == pytest.approx(0.0)
    assert normal_mixture_energy_distance(left, right) > 0.0
    assert normal_mixture_energy_distance(left, right, scale=2.0) == pytest.approx(
        normal_mixture_energy_distance(left, right) / 2.0
    )


def test_monte_carlo_reference_marks_unresolved_top_two():
    instrument = DecisionInstrument(
        actions=(1.0, 2.0),
        safety_threshold=-10.0,
        risk_penalty=0.0,
        reopen_cost_low=0.1,
        reopen_cost_high=1.0,
    )

    def tied_sampler(action, n, seed):
        return np.random.default_rng(seed).normal(0.0, 1.0, n)

    decision = monte_carlo_optimal_action(
        tied_sampler, instrument, n=200, bootstrap_reps=50, seed=9
    )
    assert decision.indeterminate


def test_candidate_is_reproducible_and_public_recipe_has_no_answer():
    config = ProbeConfig()
    first = generate_candidate(731_000, config)
    second = generate_candidate(731_000, config)
    other = generate_candidate(731_001, config)
    assert first.prefix_sha256 == second.prefix_sha256
    assert first.hidden_manifest() == second.hidden_manifest()
    assert first.prefix_sha256 != other.prefix_sha256

    public = json.dumps(config.public_recipe(), sort_keys=True).lower()
    for forbidden in ("true_gain", "true_scale", "true_amplitude", "correct_action"):
        assert forbidden not in public


def test_all_precheckpoint_queries_are_byte_identical_across_twins():
    config = ProbeConfig()
    family = generate_candidate(731_000, config)
    for line in config.lines:
        points = config.control_points if line == family.target_line else config.other_prefix_points
        for index, driver in enumerate(points):
            draws = [
                sample_truth(
                    family,
                    scenario,
                    line=line,
                    driver=driver,
                    n=32,
                    seed=80_000 + index,
                    config=config,
                )
                for scenario in SCENARIOS
            ]
            assert np.array_equal(draws[0], draws[1])
            assert np.array_equal(draws[0], draws[2])


def test_known_triplet_certifies_all_four_cases():
    config = ProbeConfig()
    family = generate_candidate(731_000, config)
    certificate = certify_family(family, config)
    assert certificate["all"], [
        name for name, gate in certificate["gates"].items() if not gate["passed"]
    ]

    revise = certificate["scenarios"]["revise"]
    maintain = certificate["scenarios"]["maintain"]
    doubt = certificate["scenarios"]["doubt"]
    assert revise["post_action"] < revise["pre_action"]
    assert revise["reopen_low"] and not revise["reopen_high"]
    assert maintain["post_action"] == maintain["pre_action"]
    assert not maintain["reopen_low"] and not maintain["reopen_high"]
    assert doubt["post_action"] < doubt["pre_action"]
    assert doubt["assimilation_detail"]["width_ratio"] >= config.doubt_width_ratio_min


def test_posterior_uses_prefix_and_only_the_selected_twin_evidence():
    config = ProbeConfig()
    family = generate_candidate(731_000, config)
    pre = exact_posterior(family, config)
    revise = exact_posterior(family, config, evidence="revise")
    doubt = exact_posterior(family, config, evidence="doubt")
    assert revise.scenario_probability("revise") > pre.scenario_probability("revise")
    assert doubt.scenario_probability("doubt") > pre.scenario_probability("doubt")


def test_propagation_fraction_distinguishes_sterile_and_complete_repair():
    instrument = DecisionInstrument(
        actions=(1.0, 2.0, 3.0),
        safety_threshold=-10.0,
        risk_penalty=0.0,
        reopen_cost_low=0.1,
        reopen_cost_high=2.0,
    )
    decision = exact_optimal_action(
        lambda action: NormalMixture(
            np.array([1.0]), np.array([action]), np.array([0.1])
        ),
        instrument,
    )
    sterile = propagation_fraction(
        committed_action=1.0,
        final_action=1.0,
        own_decision=decision,
        epsilon=0.1,
    )
    complete = propagation_fraction(
        committed_action=1.0,
        final_action=3.0,
        own_decision=decision,
        epsilon=0.1,
    )
    assert sterile.sterile and sterile.fraction == 0.0
    assert not complete.sterile and np.isclose(complete.fraction, 1.0)


def test_fixed_cohort_is_consecutive_and_never_rejection_selected():
    cohort = evaluate_fixed_cohort(count=4)
    seeds = [family.candidate_seed for family, _ in cohort]
    assert seeds == list(range(VALIDATION_SEED_START, VALIDATION_SEED_START + 4))
    assert len(cohort) == 4


def test_factory_writes_separate_private_and_agent_safe_manifests(tmp_path):
    report = write_factory_report(tmp_path, count=4)
    private_path = tmp_path / "private" / "factory_certification.json"
    public_path = tmp_path / "public" / "manifest.json"
    assert private_path.exists() and public_path.exists()
    assert report["fixed_cohort"]["consecutive_no_skips"]
    assert not report["fixed_cohort"]["selection_on_realized_evidence"]
    assert report["batch_gates"]["cost_only_accuracy_is_chance"]["passed"]
    assert report["batch_gates"]["scenario_cost_mutual_information_zero"]["passed"]

    public = json.loads(public_path.read_text(encoding="utf-8"))

    def keys(value):
        if isinstance(value, dict):
            for key, child in value.items():
                yield key
                yield from keys(child)
        elif isinstance(value, list):
            for child in value:
                yield from keys(child)

    forbidden = {
        "candidate_seed",
        "true_gain",
        "true_scale",
        "true_amplitude",
        "evidence_sha256",
        "seed_manifest",
        "action_utilities",
        "pre_action",
        "post_action",
        "gross_gain",
        "truth_utility_at_reference_action",
    }
    assert forbidden.isdisjoint(set(keys(public)))
    assert "candidate_seed" in set(keys(json.loads(
        private_path.read_text(encoding="utf-8")
    )))
