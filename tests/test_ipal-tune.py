import pytest

from .conftest import check_with_validation_file, tune


def test_tune_empty():
    errno, stdout, stderr = tune([])

    assert errno == 1
    assert stdout == b""
    assert b"ERROR:ipal-tune" in stderr


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
    errno, stdout, stderr = tune(
        [
            "--config",
            file,
            "--restart-experiment",
            "--max-cpus",
            "1",
        ]
    )

    print(stderr.decode("utf-8"))

    assert errno == 0
    check_with_validation_file(
        file.replace("/", "-"), stdout.decode("utf-8"), test_tune_file.__name__
    )
