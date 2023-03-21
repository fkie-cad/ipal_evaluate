from unittest import TestCase

from metrics.jaccard import JaccardDistance, JaccardIndex


def test_jaccard_index():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = JaccardIndex.calculate(ergs=test_ergs)

    expected = {"Jaccard-Index": 1 / 3}
    TestCase().assertDictEqual(expected, ergs)


def test_jaccard_distance():
    test_ergs = {"Jaccard-Index": 1}
    ergs = JaccardDistance.calculate(ergs=test_ergs)

    expected = {"Jaccard-Distance": 0.0}
    TestCase().assertDictEqual(expected, ergs)
