from unittest import TestCase

from metrics.matthews_corr_coeff import MCC


def test_accuracy():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = MCC.calculate(ergs=test_ergs)

    expected = {"MCC": 0.0}
    TestCase().assertDictEqual(expected, ergs)
