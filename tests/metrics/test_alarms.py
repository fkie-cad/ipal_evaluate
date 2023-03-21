from unittest import TestCase

from metrics.alarms import FalsePositiveAlarms, TruePositiveAlarms
from tests.metrics.test_data import test_attacks, test_data


def test_true_positive_alarms():
    ergs = TruePositiveAlarms.calculate(dataset=test_data, attacks=test_attacks)

    expected = {"TPA": 2}
    TestCase().assertDictEqual(expected, ergs)


def test_false_positive_alarms():
    ergs = FalsePositiveAlarms.calculate(dataset=test_data, attacks=test_attacks)

    expected = {"FPA": 2}
    TestCase().assertDictEqual(expected, ergs)
