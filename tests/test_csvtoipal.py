from itertools import product

import pytest

from .conftest import calculate_and_create_paths, check_with_validation_file, csvtoipal


@pytest.mark.parametrize(
    "separator,quote,line_end", product([",", ";"], ['"', "'", ""], ["\n", "\r\n"])
)
def test_csv_to_ipal(separator: str, quote: str, line_end: str) -> None:
    csv = (
        f"{separator}{quote}actuators{quote}{separator}{separator}{separator}{quote}classifications{quote}{separator}{separator}{quote}scores{quote}{separator}{separator}{separator}{line_end}"
        f"{quote}timestamp{quote}{separator}{quote}PUMP_A{quote}{separator}{quote}VALVE_A{quote}{separator}{quote}VALVE_B{quote}{separator}{quote}malicious{quote}{separator}{quote}ids{quote}{separator}{quote}Gradient{quote}{separator}{quote}Histogram{quote}{separator}{quote}MinMax{quote}{separator}{quote}Steadytime{quote}{line_end}"
        f"1451293200{separator}1{separator}{quote}OPEN{quote}{separator}0.01{separator}1{separator}1{separator}21{separator}0{separator}0{separator}0{line_end}"
        f"1451293201{separator}1{separator}{quote}OPEN{quote}{separator}0.01{separator}0{separator}1{separator}12{separator}-1{separator}0{separator}0{line_end}"
        f"1451293202{separator}0{separator}{quote}CLOSED{quote}{separator}-0.14985{separator}0{separator}0{separator}0{separator}-1{separator}0{separator}-0.00003{line_end}"
        f"1451293203{separator}0{separator}{quote}CLOSED{quote}{separator}0.324368{separator}1{separator}0{separator}0{separator}1{separator}0{separator}0{line_end}"
        f"1451293204{separator}0{separator}{quote}OPEN{quote}{separator}0.57523{separator}1{separator}0{separator}0{separator}-1{separator}0{separator}0{line_end}"
        f"1451293205{separator}1{separator}{quote}OPEN{quote}{separator}0.58942{separator}1{separator}1{separator}32{separator}-1{separator}0{separator}3.33{line_end}"
        f"1451293206{separator}1{separator}{quote}CLOSED{quote}{separator}-0.559348{separator}0{separator}1{separator}423{separator}0{separator}0{separator}221.32{line_end}"
        f"1451293207{separator}1{separator}{quote}CLOSED{quote}{separator}0.5352{separator}1{separator}1{separator}5345{separator}0{separator}0{separator}0{line_end}"
        f"1451293208{separator}0{separator}{quote}OPEN{quote}{separator}0.543123{separator}1{separator}0{separator}0{separator}0{separator}0{separator}0{line_end}"
    )

    attack_file, _ = calculate_and_create_paths(
        "attacks.json", test_csv_to_ipal.__name__
    )
    errno, stdout, _ = csvtoipal(
        [
            "-",
            "-",
            "--separator",
            f"{separator}",
            "--timestamp",
            "0",
            "--groundtruth",
            "4",
            "--ids",
            "5",
            "--scores",
            "Gradient:6,Histogram:7,MinMax:8,:9",
            "--attacks",
            f"{attack_file}",
            "--skip",
            "2",
            "--header",
            "1",
        ],
        bytes(csv, "UTF-8"),
    )

    assert errno == 0
    raw_attacks = open(attack_file, "rt").read()
    check_with_validation_file(
        "output.state.json",
        stdout.decode("utf-8"),
        test_csv_to_ipal.__name__,
    )

    check_with_validation_file(
        "attacks.json",
        raw_attacks,
        test_csv_to_ipal.__name__,
    )
