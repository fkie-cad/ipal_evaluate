import numpy as np

from evaluate.utils import parse_ipal_input

test_data = [
    {"timestamp": 1, "state": {}, "malicious": False, "metrics": {}, "ids": False},
    {"timestamp": 2, "state": {}, "malicious": False, "metrics": {}, "ids": True},
    {
        "timestamp": 3,
        "state": {},
        "malicious": "a",
        "metrics": {"testids": None},
        "ids": False,
    },
    {
        "timestamp": 4,
        "state": {},
        "malicious": True,
        "metrics": {"testids": None},
        "ids": True,
    },
    {
        "timestamp": 5,
        "state": {},
        "malicious": False,
        "metrics": {"testids": 0},
        "ids": False,
    },
    {
        "timestamp": 6,
        "state": {},
        "malicious": False,
        "metrics": {"testids": 1},
        "ids": True,
    },
    {
        "timestamp": 7,
        "state": {},
        "malicious": True,
        "metrics": {"testids": 0},
        "ids": False,
    },
    {
        "timestamp": 8,
        "state": {},
        "malicious": "b",
        "metrics": {"testids": 1},
        "ids": True,
    },
]

test_attacks = [
    {"id": "a", "attack_point": [], "description": "", "start": 3, "end": 4},
    {"id": "b", "attack_point": [], "description": "", "start": 7, "end": 8},
]


def test_parse_ipal_input():
    truth, predicted = parse_ipal_input(test_data)

    assert np.array_equal(truth, np.array([0, 0, 1, 1, 0, 0, 1, 1]))
    assert np.array_equal(predicted, np.array([0, 1, 0, 1, 0, 1, 0, 1]))
