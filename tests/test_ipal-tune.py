import pytest

from .conftest import (
    check_command_output,
    check_is_ipal_ids_installed,
    check_is_transcriber_installed,
    check_with_validation_file,
    tune,
)


def test_tune_empty():

    args = []
    errno, stdout, stderr = tune(args)

    check_command_output(
        returncode=errno,
        args=args,
        stdout=stdout,
        stderr=stderr,
        expectedcode=1,
        expected_stderr=[r"ERROR:ipal\-tune"],  # only checks if that string shows up
        expected_stdout=[b""],
    )


TESTFILES = [
    "misc/tests/tune-iids/tune-config.py",
    "misc/tests/tune-combiner/tune-config.py",
]


@pytest.mark.parametrize("file", TESTFILES)
def test_tune_file(file):

    check_is_transcriber_installed()
    check_is_ipal_ids_installed()

    args = [
        "--config",
        file,
        "--restart-experiment",
        "--max-cpus",
        "1",
    ]

    errno, stdout, stderr = tune(args)

    check_command_output(
        returncode=errno,
        args=args,
        stdout=stdout,
        stderr=stderr,
        expectedcode=0,
        check_for=["ERROR"],  # check if an IPAL error appears
    )

    check_with_validation_file(
        file.replace("/", "-"), stdout.decode("utf-8"), test_tune_file.__name__
    )
