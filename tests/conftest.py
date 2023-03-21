from pathlib import Path
from subprocess import PIPE, Popen
from typing import List, Tuple

# Exclude output paths
collect_ignore = ["snapshots"]

EVALUATE = "./ipal-evaluate"
TUNE = "./ipal-tune"
CSVTOIPAL = "./misc/csv-to-ipal.py"

########################
# Helper methods
########################


def evaluate(args):
    p = Popen([EVALUATE] + args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr


def tune(args):
    p = Popen([TUNE] + args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr


def csvtoipal(args: List[str], stdin: bytes) -> Tuple[int, bytes, bytes]:
    p = Popen([CSVTOIPAL] + args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(stdin)
    return p.returncode, stdout, stderr


def assert_file_contents_equal(validation_path: Path, output_path: Path):
    validation_content = validation_path.read_text().splitlines()
    output_content = output_path.read_text().splitlines()

    assert len(validation_content) == len(output_content)

    for val, out in zip(validation_content, output_content):
        assert "###IGNORE-LINE###" in val or val == out


def calculate_and_create_paths(filename: str, prefix: str):
    if prefix:
        prefix += "_"
    base_path = Path(__file__).parent / "snapshots"
    output_path = base_path / "output" / f"{prefix}{filename}"
    validation_path = base_path / "validation" / f"{prefix}{filename}"
    output_path.parent.mkdir(exist_ok=True)
    validation_path.parent.mkdir(exist_ok=True)
    return output_path, validation_path


def check_with_validation_file(filename: str, raw_content: str, prefix: str = ""):
    output_path, validation_path = calculate_and_create_paths(filename, prefix)

    output_path.write_text(raw_content)
    if not validation_path.is_file():
        validation_path.write_text("== new file ==\n" + raw_content)

    assert_file_contents_equal(validation_path, output_path)
