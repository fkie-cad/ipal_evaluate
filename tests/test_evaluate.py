import pytest

from .conftest import check_with_validation_file, evaluate


def test_evaluate_empty():
    errno, stdout, stderr = evaluate([])

    assert errno == 2
    assert stdout == b""
    assert b"usage: ipal-evaluate" in stderr


TESTFILES = [
    ("testfile-1.ipal.gz", "attacks-1.json"),
    ("testfile-2.ipal.gz", "attacks-2.json"),
    ("testfile-3.ipal.gz", "attacks-3.json"),
    ("testfile-4.ipal.gz", "attacks-1.json"),
]


@pytest.mark.parametrize("file", TESTFILES)
def test_test_file(file):
    errno, stdout, stderr = evaluate(
        [
            "--attacks",
            f"misc/tests/{file[1]}",
            "--timed-dataset",
            "true",
            f"misc/tests/{file[0]}",
        ]
    )

    if errno != 0:
        print(f"{'=' * 20} FAILED {'=' * 20}")
        print(stdout.decode("utf-8"))
        print(stderr.decode("utf-8"))
        assert errno == 0

    assert stderr == "" or b"ERROR" not in stderr
    check_with_validation_file(file[0], stdout.decode("utf-8"), test_test_file.__name__)
