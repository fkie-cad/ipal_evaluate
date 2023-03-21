from unittest import TestCase

import evaluate.settings as settings
from evaluate.utils import parse_ipal_input
from metrics.basic_metrics import (
    Accuracy,
    Confusion,
    Fallout,
    FScore,
    Informedness,
    InversePrecision,
    InverseRecall,
    Markedness,
    MissRate,
    Precision,
    Recall,
)
from tests.metrics.test_data import test_data


def test_confusion():
    truth, predicted = parse_ipal_input(test_data)
    ergs = Confusion.calculate(truth, predicted)

    expected = {"tn": 2, "fp": 2, "fn": 2, "tp": 2}
    TestCase().assertDictEqual(expected, ergs)


def test_accuracy():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = Accuracy.calculate(ergs=test_ergs)

    expected = {"Accuracy": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_precision():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = Precision.calculate(ergs=test_ergs)

    expected = {"Precision": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_inverse_precision():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = InversePrecision.calculate(ergs=test_ergs)

    expected = {"Inverse-Precision": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_recall():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = Recall.calculate(ergs=test_ergs)

    expected = {"Recall": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_inverse_recall():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = InverseRecall.calculate(ergs=test_ergs)

    expected = {"Inverse-Recall": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_fallout():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = Fallout.calculate(ergs=test_ergs)

    expected = {"Fallout": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test__missrate():
    test_ergs = {"tp": 1, "fp": 1, "fn": 1, "tn": 1}
    ergs = MissRate.calculate(ergs=test_ergs)

    expected = {"Missrate": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_informedness():
    test_ergs = {"Recall": 0.5, "Inverse-Recall": 0.5}
    ergs = Informedness.calculate(ergs=test_ergs)

    expected = {"Informedness": 0.0}
    TestCase().assertDictEqual(expected, ergs)


def test_markedness():
    test_ergs = {"Precision": 0.5, "Inverse-Precision": 0.5}
    ergs = Markedness.calculate(ergs=test_ergs)

    expected = {"Markedness": 0.0}
    TestCase().assertDictEqual(expected, ergs)


def test_fdefaultscore():
    test_ergs = {"Precision": 0.5, "Recall": 0.5}
    ergs = FScore.calculate(ergs=test_ergs)

    expected = {"F0.1": 0.5, "F0.5": 0.5, "F1": 0.5, "F2": 0.5, "F10": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_f1score():
    test_ergs = {"Precision": 0.5, "Recall": 0.5}
    bak = settings.fscore_betas
    settings.fscore_betas = [1]
    ergs = FScore.calculate(ergs=test_ergs)

    settings.fscore_betas = bak
    expected = {"F1": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_f0score():
    test_ergs = {"Precision": 0.5, "Recall": 0.5}
    bak = settings.fscore_betas
    settings.fscore_betas = [0]
    ergs = FScore.calculate(ergs=test_ergs)

    settings.fscore_betas = bak
    expected = {"F0": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_f05score():
    test_ergs = {"Precision": 0.5, "Recall": 0.5}
    bak = settings.fscore_betas
    settings.fscore_betas = [0.5]
    ergs = FScore.calculate(ergs=test_ergs)

    settings.fscore_betas = bak
    expected = {"F0.5": 0.5}
    TestCase().assertDictEqual(expected, ergs)


def test_f2score():
    test_ergs = {"Precision": 0.5, "Recall": 0.5}
    bak = settings.fscore_betas
    settings.fscore_betas = [2]
    ergs = FScore.calculate(ergs=test_ergs)

    settings.fscore_betas = bak
    expected = {"F2": 0.5}
    TestCase().assertDictEqual(expected, ergs)
