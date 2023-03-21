from unittest import TestCase

from evaluate.utils import parse_ipal_input
from metrics.tapr import eTaPR
from tests.metrics.test_data import test_data


def test_eTaPR():
    truth, predicted = parse_ipal_input(test_data)
    ergs = eTaPR.calculate(truth, predicted)

    expected = {
        "eTaR": 0.75,
        "eTaP": 0.5,
        "eTaF0.1": 0.5016556291390729,
        "eTaF0.5": 0.5357142857142857,
        "eTaF1": 0.6,
        "eTaF2": 0.6818181818181818,
        "eTaF10": 0.7463054187192119,
    }
    TestCase().assertDictEqual(expected, ergs)
