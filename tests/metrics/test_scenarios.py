from unittest import TestCase

from metrics.scenarios import (
    DetectedScenarios,
    DetectedScenariosPercent,
    DetectionDelay,
    ScenarioRecall,
)
from tests.metrics.test_data import test_attacks, test_data


def test_det_scenarios():
    ergs = DetectedScenarios.calculate(dataset=test_data, attacks=test_attacks)

    expected = {"Detected-Scenarios": ["a", "b"]}
    TestCase().assertDictEqual(expected, ergs)


def test_det_scenarios_perc():
    ergs = {"Detected-Scenarios": ["b"]}
    ergs = DetectedScenariosPercent.calculate(
        dataset=test_data, attacks=test_attacks, ergs=ergs
    )

    expected = {"Detected-Scenarios-Percent": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_scenario_recall():
    ergs = ScenarioRecall.calculate(dataset=test_data, attacks=test_attacks)

    expected = {"Scenario-Recall": {"a": 0.0, "b": 1.0}}
    TestCase().assertDictEqual(expected, ergs)


def test_det_delay():
    ergs = {"Detected-Scenarios": ["a", "b"]}
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

    ergs = DetectionDelay.calculate(dataset=test_data, attacks=test_attacks, ergs=ergs)

    expected = {"Detection-Delay": 8}
    TestCase().assertDictEqual(expected, ergs)
