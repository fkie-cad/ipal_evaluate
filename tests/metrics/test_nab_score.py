from typing import Any, Dict
from unittest import TestCase

import pytest
from pytest import approx

from evaluate.settings import nab_profiles as profiles
from metrics.nab_score import Nab

# used for validation with results from the original
# implementation. For comparisons, probationary period must
# be set to 0 to ensure same count of events.
_validation_profiles = {
    "default": {
        "nab_atp": 1,
        "nab_afp": -0.11,
        "nab_afn": -1,
    },
    "reward_low_fp": {
        "nab_atp": 1,
        "nab_afp": -0.22,
        "nab_afn": -1,
    },
    "reward_low_fn": {
        "nab_atp": 1,
        "nab_afp": -0.11,
        "nab_afn": -2.0,
    },
}


def _init_scores() -> Dict[str, Dict[str, float]]:
    return {
        name: {"raw": 0.0, "null": 0.0, "perfect": 0.0, "normalized": 0.0}
        for name in profiles.keys()
    }


@pytest.mark.parametrize(
    "entry,attack,result",
    [
        ({"timestamp": 5}, {"start": 1, "end": 5}, -1 / 5),
        ({"timestamp": 1}, {"start": 1, "end": 3}, -1.0),
        ({"timestamp": 1}, {"start": 1, "end": 1}, -1.0),
        ({"timestamp": 2}, {"start": 1, "end": 1}, 1.0),
        ({"timestamp": 9}, {"start": 1, "end": 5}, 1.0),
    ],
)
def test_relative_pos(
    entry: Dict[str, Any], attack: Dict[str, Any], result: float
) -> None:
    assert Nab._relative_pos(entry, attack) == approx(result)


def test_calculate_format() -> None:
    ergs = {"Detected-Scenarios": ["a"]}

    test_data = [
        {"timestamp": 1, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 5, "state": {}, "malicious": True, "metrics": {}, "ids": True},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 1, "end": 5},
    ]
    scores = Nab._compute_scores(
        _init_scores(), test_data, test_attacks, profiles, len(test_attacks), 0
    )
    final_res = Nab.calculate(dataset=test_data, attacks=test_attacks, ergs=ergs)

    # verify that the normalized scores are being returned by the calculate function
    expected = {
        "NAB-score-default": scores["default"]["normalized"],
        "NAB-score-low-fp": scores["reward_low_fp"]["normalized"],
        "NAB-score-low-fn": scores["reward_low_fn"]["normalized"],
    }

    TestCase().assertDictEqual(expected, final_res)


def test_latest_tp_only() -> None:
    test_data = [
        {"timestamp": 1, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 5, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 6, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        {"timestamp": 9, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 12, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 13, "state": {}, "malicious": True, "metrics": {}, "ids": True},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 1, "end": 5},
        {"id": "b", "attack_point": [], "description": "", "start": 9, "end": 13},
    ]

    # compare results with logical expected values
    scores = Nab._compute_scores(
        _init_scores(), test_data, test_attacks, profiles, len(test_attacks), 0
    )
    for name, profile in profiles.items():
        assert scores[name]["null"] == profile["nab_afn"] * len(test_attacks)
        assert scores[name]["perfect"] == profile["nab_atp"] * len(test_attacks)
        # two detections at the right-most edge of 5-entry windows
        # yield two times 1 / window length (because of the off-by-one
        # in the original implementation for relative position computation)
        assert scores[name]["raw"] == approx(
            2 * (Nab._sigma(-1 / 5) / Nab._sigma(-1.0)) * profile["nab_atp"]
        )

    # compare results with values obtained from running the official implementation
    scores = Nab._compute_scores(
        _init_scores(),
        test_data,
        test_attacks,
        _validation_profiles,
        len(test_attacks),
        0,
    )
    raw_score = 0.9367736878045564  # official impl res with the given data and profile

    for profile, score in scores.items():
        assert score["raw"] == approx(raw_score)
        null_score = _validation_profiles[profile]["nab_afn"] * len(test_attacks)
        perfect_score = _validation_profiles[profile]["nab_atp"] * len(test_attacks)
        assert score["normalized"] == approx(
            100 * ((raw_score - null_score) / (perfect_score - null_score))
        )


def test_fp_before_any_attack() -> None:
    test_data = [
        {"timestamp": 1, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        {"timestamp": 2, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        {"timestamp": 5, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 8, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 9, "state": {}, "malicious": False, "metrics": {}, "ids": False},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 5, "end": 8},
    ]

    # compare results with logical expected values
    scores = Nab._compute_scores(
        _init_scores(), test_data, test_attacks, profiles, len(test_attacks), 1
    )
    for name, profile in profiles.items():
        assert scores[name]["null"] == profile["nab_afn"] * len(test_attacks)
        assert scores[name]["perfect"] == profile["nab_atp"] * len(test_attacks)
        # one false positive with maximal penalty and a false negative
        assert scores[name]["raw"] == profile["nab_afp"] + profile["nab_afn"]


def test_multiple_tp() -> None:
    test_data = [
        {"timestamp": 1, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        {"timestamp": 2, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 3, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 4, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 5, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 8, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 9, "state": {}, "malicious": False, "metrics": {}, "ids": False},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 2, "end": 8},
    ]

    # compare results with logical expected values
    scores = Nab._compute_scores(
        _init_scores(), test_data, test_attacks, profiles, len(test_attacks), 0
    )
    for name, profile in profiles.items():
        assert scores[name]["null"] == profile["nab_afn"] * len(test_attacks)
        assert scores[name]["perfect"] == profile["nab_atp"] * len(test_attacks)
        # one attack scenario detected multiple times, only the earliest detection
        # at timestamp 3 should count
        assert scores[name]["raw"] == approx(
            (
                Nab._sigma(Nab._relative_pos(test_data[2], test_attacks[0]))
                / Nab._sigma(-1.0)
            )
            * profile["nab_atp"]
        )

    # compare results with values obtained from running the official implementation
    scores = Nab._compute_scores(
        _init_scores(),
        test_data,
        test_attacks,
        _validation_profiles,
        len(test_attacks),
        0,
    )
    raw_score = 0.9860450714481678  # official impl res with the given data and profile

    for profile, score in scores.items():
        assert score["raw"] == approx(raw_score)
        null_score = _validation_profiles[profile]["nab_afn"] * len(test_attacks)
        perfect_score = _validation_profiles[profile]["nab_atp"] * len(test_attacks)
        assert score["normalized"] == approx(
            100 * ((raw_score - null_score) / (perfect_score - null_score))
        )


def test_overlapping_attacks() -> None:
    # fmt: off
    test_data = [
        {"timestamp": 1, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        {"timestamp": 2, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 3, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 4, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 5, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 6, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 7, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 8, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        {"timestamp": 9, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 10, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 11, "state": {}, "malicious": True, "metrics": {}, "ids": True},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 2, "end": 7},
        {"id": "b", "attack_point": [], "description": "", "start": 4, "end": 7},
        {"id": "c", "attack_point": [], "description": "", "start": 5, "end": 6},
        {"id": "d", "attack_point": [], "description": "", "start": 9, "end": 10},
        {"id": "e", "attack_point": [], "description": "", "start": 10, "end": 11},
    ]
    # fmt: on

    # compare results with logical expected values
    scores = Nab._compute_scores(
        _init_scores(), test_data, test_attacks, profiles, len(test_attacks), 0
    )
    for name, profile in profiles.items():
        assert scores[name]["null"] == profile["nab_afn"] * len(test_attacks)
        assert scores[name]["perfect"] == profile["nab_atp"] * len(test_attacks)
        # all attacks are detected as early as possible, no TP matching a new
        # attack should be ignored even if it overlaps ongoing attacks that have already started
        assert scores[name]["raw"] == scores[name]["perfect"]


def test_combined_short() -> None:
    # fmt: off
    test_data = [
        {"timestamp": 1, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        # False positives before any attack
        {"timestamp": 2, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        {"timestamp": 3, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        # First attack, detected at the last possible moment
        {"timestamp": 4, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 8, "state": {}, "malicious": True, "metrics": {}, "ids": True},

        {"timestamp": 9, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        # isolated false positive
        {"timestamp": 54, "state": {}, "malicious": False, "metrics": {}, "ids": True},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 4, "end": 8},
    ]
    # fmt: on

    # compare results with values obtained from running the official implementation
    scores = Nab._compute_scores(
        _init_scores(),
        test_data,
        test_attacks,
        _validation_profiles,
        len(test_attacks),
        0,
    )
    raw_scores = {
        "default": 0.1383868439022781,
        "reward_low_fp": -0.1916131560977219,
        "reward_low_fn": 0.1383868439022781,
    }

    for profile, score in scores.items():
        assert score["raw"] == approx(raw_scores[profile])


def test_combined() -> None:
    # fmt: off
    test_data = [
        {"timestamp": 1, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        # False positives before any attack
        {"timestamp": 2, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        {"timestamp": 3, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        # First attack, detected at the last possible moment
        {"timestamp": 4, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 8, "state": {}, "malicious": True, "metrics": {}, "ids": True},

        {"timestamp": 9, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        # isolated false positive
        {"timestamp": 54, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        # Second attack, detected before the end
        {"timestamp": 123, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 319, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 320, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        {"timestamp": 321, "state": {}, "malicious": True, "metrics": {}, "ids": True},
        # Trailing false positives after attack end
        {"timestamp": 322, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        {"timestamp": 323, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        {"timestamp": 324, "state": {}, "malicious": False, "metrics": {}, "ids": True},
        # Third attack, false negative
        {"timestamp": 444, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 554, "state": {}, "malicious": True, "metrics": {}, "ids": False},
        {"timestamp": 555, "state": {}, "malicious": False, "metrics": {}, "ids": False},
        # Trailing false positive after last attack
        {"timestamp": 556, "state": {}, "malicious": False, "metrics": {}, "ids": True},
    ]
    test_attacks = [
        {"id": "a", "attack_point": [], "description": "", "start": 4, "end": 8},
        {"id": "b", "attack_point": [], "description": "", "start": 123, "end": 321},
        {"id": "c", "attack_point": [], "description": "", "start": 444, "end": 554},
    ]
    # fmt: on

    # compare results with values obtained from running the official implementation
    scores = Nab._compute_scores(
        _init_scores(),
        test_data,
        test_attacks,
        _validation_profiles,
        len(test_attacks),
        1,
    )
    raw_scores = {
        "default": -0.8367586963087265,
        "reward_low_fp": -1.1800859332159153,
        "reward_low_fn": -1.8367586963087263,
    }

    for profile, score in scores.items():
        assert score["raw"] == approx(raw_scores[profile])
