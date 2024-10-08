import pytest

from .conftest import check_command_output, check_with_validation_file, tune


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
    # "misc/tests/tune-iids/tune-config.py",
    # "misc/tests/tune-combiner/tune-config.py",
    # ignored for now. if use with gitlab-ci add to before_script:
    # - git clone https://github.com/fkie-cad/ipal_ids_framework
    # - sudo pip3 install ipal_ids_framework/
    # - git clone https://github.com/fkie-cad/ipal_transcriber
    # - sudo pip3 install ipal_transcriber/
    # - sudo rm -rf ipal_ids_framework/ ipal_transcriber/
]


@pytest.mark.parametrize("file", TESTFILES)
def test_tune_file(file):

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
