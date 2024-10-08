import pytest

from .conftest import add_attacks, check_with_validation_file


def test_attacks_empty():
    errno, stdout, stderr = add_attacks([])

    assert errno == 2
    assert stdout == b""
    assert b"usage: ipal-add-attacks" in stderr


TESTFILES = [["attacks.json", "test-file.ipal"]]


@pytest.mark.parametrize("file", TESTFILES)
def test_add_attack_file(file):
    errno, stdout, stderr = add_attacks(
        [
            "--log",
            "info",
            "--attacks",
            f"./misc/tests/add-attacks/{file[0]}",
            "--input",
            f"./misc/tests/add-attacks/{file[1]}",
            "--output",
            "-",
        ]
    )

    if errno != 0:
        print(f"{'=' * 20} FAILED {'=' * 20}")
        print(stdout.decode("utf-8"))
        print(stderr.decode("utf-8"))
        assert errno == 0

    check_with_validation_file(
        file[1], stdout.decode("utf-8"), test_add_attack_file.__name__
    )
