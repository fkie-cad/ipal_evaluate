from typing import Any, Dict, List

import pytest

from evaluate.evaluate import check_timed_attacks_keys, check_timed_attacks_order


@pytest.mark.parametrize(
    "attacks,result",
    [
        ([{"id": 1, "start": 2, "end": 3}, {"id": 2, "start": 1, "end": 2}], True),
        (
            [
                {"id": 1, "start": 2, "end": 3},
                {"id": 2, "start": 3, "end": 5},
                {"id": 3, "start": 1, "end": 2},
            ],
            True,
        ),
        (
            [
                {"id": 1, "start": 4, "end": 10},
                {"id": 2, "start": 15, "end": 25},
                {"id": 3, "start": 2, "end": 3},
                {"id": 4, "start": 1, "end": 2},
            ],
            True,
        ),
        ([{"id": 1, "start": 2, "end": 3}, {"id": 2, "start": 3, "end": 5}], False),
        ([{"id": 1, "start": 2, "end": 3}], False),
    ],
)
def test_attack_file_order(attacks: List[Dict[str, Any]], result: bool) -> None:
    assert check_timed_attacks_order(attacks) == result


@pytest.mark.parametrize(
    "attacks,result",
    [
        ([{"id": 1, "start": 1}], True),
        ([{"id": 1, "end": 1}], True),
        ([{"start": 1, "end": 1}], True),
        ([{"id": 1, "start": 1, "end": 1}], False),
    ],
)
def test_attack_file_keys(attacks: List[Dict[str, Any]], result: bool) -> None:
    assert check_timed_attacks_keys(attacks) == result
