#!/usr/bin/env python3
import argparse
import logging
import sys
import traceback
from os import PathLike
from pathlib import Path
from typing import IO, Any, Dict, List

import orjson
from zlib_ng import gzip_ng_threaded as gzip

import evaluate.settings as settings
from evaluate.utils import parse_ipal_input
from metrics.utils import get_all_metrics

REQUIRED_KEYS = ["id", "timestamp", "malicious", "ids"]


def open_file(
    filename: str | PathLike | Path,
    mode: str = "r",
    compresslevel: int | None = None,
    force_gzip: bool = False,
) -> IO | None:
    """
    Wrapper to hide .gz files and stdin/stdout

    :param filename: filename to open
    :param mode: file mode
    :param compresslevel: force compresslevel, if None level is taken from settings
    :param force_gzip: if file should be treated as gzip even without .gz ending
    :return: file-like object or None
    """

    # make sure filename is a string and not path-like object
    filename = str(filename)

    if not compresslevel:
        compresslevel = settings.compresslevel

    if filename == "-" and force_gzip:
        # we can give gzip stdin/stdout to read / write from if explicitly wanted
        if "r" in mode:
            filename = sys.stdin
        elif "w" in mode:
            filename = sys.stdout

    if filename is None:
        return None
    elif filename.endswith(".gz") or force_gzip:
        return gzip.open(filename, mode=mode, compresslevel=compresslevel, threads=-1)
    elif (filename == "-" or filename == "stdin") and "r" in mode:
        return sys.stdin
    elif (filename == "-" or filename == "stdout") and "w" in mode:
        return sys.stdout
    else:
        if "b" in mode:
            return open(filename, mode=mode, buffering=0)
        else:
            return open(filename, mode=mode, buffering=1)


# Initialize logger
def initialize_logger(args):
    if args.log:
        settings.log = getattr(logging, args.log.upper(), None)

        if not isinstance(settings.log, int):
            logging.getLogger("ipal-evaluate").error(
                "Option '--log' parameter not found"
            )
            exit(1)

    if args.logfile:
        settings.logfile = args.logfile
        logging.basicConfig(
            filename=settings.logfile, level=settings.log, format=settings.logformat
        )
    else:
        logging.basicConfig(level=settings.log, format=settings.logformat)

    settings.logger = logging.getLogger("ipal-evaluate")


def prepare_arg_parser(parser):
    # Input and output
    parser.add_argument(
        "input",
        metavar="FILE",
        nargs=1,
        help="input file of IPAL messages to evaluate ('-' stdin, '*.gz' compressed) (Default: '-')",
        default="-",
    )

    parser.add_argument(
        "--output",
        dest="output",
        metavar="FILE",
        help="output file to write the evaluation to ('-' stdout, '*.gz' compress) (Default: '-')",
        default="-",
        required=False,
    )
    parser.add_argument(
        "--attacks",
        dest="attacks",
        metavar="FILE",
        help="JSON file containing the attacks from the used dataset ('*.gz' compress) (Default: None)",
        required=False,
    )
    parser.add_argument(
        "--timed-dataset",
        dest="timed",
        metavar="bool",
        help="is the dataset timed? Required by some metrics (True, False) (Default: True)",
        default="True",
        required=False,
    )

    # Logging
    parser.add_argument(
        "--log",
        dest="log",
        metavar="STR",
        help="define logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) (Default: WARNING)",
        required=False,
    )
    parser.add_argument(
        "--logfile",
        dest="logfile",
        metavar="FILE",
        default=False,
        help="file to log to (Default: stderr)",
        required=False,
    )

    # Gzip compress level
    parser.add_argument(
        "--compresslevel",
        dest="compresslevel",
        metavar="INT",
        default=6,
        help="set the gzip compress level (0 no compress, 1 fast/large, ..., 9 slow/tiny) (Default: 6)",
        required=False,
    )

    # Version number
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {settings.version}"
    )


def load_settings(args):
    # Gzip compress level
    if args.compresslevel:
        try:
            settings.compresslevel = int(args.compresslevel)
        except ValueError:
            settings.logger.error(
                "Option '--compresslevel' must be an integer from 0-9"
            )
            exit(1)

        if 9 < settings.compresslevel < 0:
            settings.logger.error(
                "Option '--compresslevel' must be an integer from 0-9"
            )
            exit(1)

    # Parse and open input file
    if args.input:
        settings.input = args.input[0]

    settings.inputfd = open_file(settings.input, "rb")

    # Parse and open output file
    if args.output:
        settings.output = args.output

    settings.outputfd = open_file(settings.output, "wb")

    # Parse attacks
    if args.attacks:
        settings.attacks = args.attacks

    # Parse timed
    if args.timed:
        timed_value = args.timed.lower()
        if timed_value == "true":
            settings.timed_dataset = True
        elif timed_value == "false":
            settings.timed_dataset = False
        else:
            settings.logger.error("Option '--timed-dataset' must be 'true' or 'false'.")
            sys.exit(1)
    else:
        settings.timed_dataset = True


def check_timed_attacks_keys(attacks: List[Dict[str, Any]]) -> bool:
    error = False
    for attack in attacks:
        for key in ["id", "start", "end"]:
            if key not in attack.keys():
                settings.logger.error(
                    f"Invalid attack format {str(attack)}: missing key '{key}'"
                )
                error = True
    return error


def check_timed_attacks_order(attacks: List[Dict[str, Any]]) -> bool:
    error_detected = False
    warnings = []

    sorted_attacks = sorted(attacks, key=lambda x: x["start"])

    # Check if attacks are in the correct chronological order
    for i, attack in enumerate(attacks):
        if attack != sorted_attacks[i]:
            original_index = attacks.index(sorted_attacks[i])
            warnings.append(
                f"Attack {i} with id '{attack['id']}' is out of order: "
                f"starts {'after' if sorted_attacks[i]['start'] < attack['start'] else 'before'} "
                f"attack {original_index} with id '{sorted_attacks[i]['id']}'."
            )
            error_detected = True

    if error_detected:
        settings.logger.error(
            f"Attacks must be sorted chronologically. {' '.join(warnings)} "
            "Fix the attack file to ensure that metrics are computed correctly."
        )

    # Check for overlapping attacks
    overlap_warnings = []
    for i in range(1, len(sorted_attacks)):
        if sorted_attacks[i]["start"] <= sorted_attacks[i - 1]["end"]:
            overlap_warnings.append(
                f"Attack with id '{sorted_attacks[i]['id']}' starts at timestamp {sorted_attacks[i]['start']} "
                f"before attack with id '{sorted_attacks[i - 1]['id']}' "
                f"ends at timestamp {sorted_attacks[i - 1]['end']}."
            )

    if overlap_warnings:
        settings.logger.warning(
            f"Attacks must be non-overlapping. {' '.join(overlap_warnings)} "
            "Some metrics might not be computed correctly."
        )

    return error_detected


def evaluate(
    attacks: List[Dict[str, Any]], truth, predicted, dataset
) -> Dict[str, Any]:
    ergs = {}
    metrics = get_all_metrics()

    for name, metric in metrics.items():
        if metric.check_requirements(ergs, attacks, settings.timed_dataset):
            try:
                # Update ergs with the new calculated values
                ergs.update(metric.calculate(truth, predicted, dataset, attacks, ergs))
                settings.logger.info(f"Calculated '{name}' metric.")
            except Exception as e:
                settings.logger.error(f"Failed calculating the '{name}' metric!")
                settings.logger.debug(traceback.format_exc())
                settings.logger.error(str(e))

                # Ensure that all metric results are set to None if an error occurs
                for real_name in metric.defines():
                    ergs[real_name] = None
        else:
            # If requirements aren't met, set all expected metric results to None
            ergs.update({real_name: None for real_name in metric.defines()})

    return ergs


def main():
    # Argument parser and settings
    parser = argparse.ArgumentParser()
    prepare_arg_parser(parser)
    args = parser.parse_args()
    initialize_logger(args)
    load_settings(args)

    # 1) Load attacks
    if args.attacks:
        settings.logger.info(f"Loading attacks from {settings.attacks}")
        with open_file(settings.attacks, "rb") as f:
            attacks = orjson.loads(f.read())

    else:
        settings.logger.warning("No attack file provided! Some metrics may be skipped")
        attacks = None

    # 1.5) If dataset is timed, check attack order and overlap
    if settings.timed_dataset and attacks is not None:
        if check_timed_attacks_keys(attacks) or check_timed_attacks_order(attacks):
            sys.exit(1)

    # 2) Load IDS classification results
    settings.logger.info(f"Loading dataset from {settings.input}")

    dataset = []
    _first = True

    for line in settings.inputfd:
        js = orjson.loads(line)

        if _first:  # Forward transcriber/ipal_iids parameters
            configs = {k: v for k, v in js.items() if k.startswith("_")}
            _first = False

        # Avoid loading the entire dataset into memory
        js = {key: js[key] for key in REQUIRED_KEYS if key in js}

        dataset.append(js)

    # 3) Test if dataset is sorted by timestamp
    settings.logger.info("Validating dataset")

    if settings.timed_dataset and not all("timestamp" in d for d in dataset):
        settings.logger.error(
            "'timestamp' is not in dataset, but timed-dataset was set"
        )
        exit(1)

    if settings.timed_dataset and not all(
        dataset[i]["timestamp"] <= dataset[i + 1]["timestamp"]
        for i in range(len(dataset) - 1)
    ):
        settings.logger.error("Dataset is not strictly ordered by timestamp")
        exit(1)

    # 4) Evaluate
    settings.logger.info("Evaluation started")

    truth, predicted = parse_ipal_input(dataset)
    ergs = evaluate(attacks, truth, predicted, dataset)
    ergs["_evaluation-config"] = settings.evaluation_settings_to_dict()

    # 5) json export
    settings.logger.info(f"Writing evaluation files to {settings.output}")
    serialized_json = orjson.dumps(
        {**ergs, **configs},
        option=orjson.OPT_SERIALIZE_NUMPY
        | orjson.OPT_INDENT_2
        | orjson.OPT_APPEND_NEWLINE
        | orjson.OPT_NON_STR_KEYS,
    )

    # need to handle stdout differently, since it expects text output
    if settings.outputfd == sys.stdout:
        settings.outputfd.write(serialized_json.decode("utf-8"))
    else:
        settings.outputfd.write(serialized_json)

    # Finalize and close
    if settings.output and settings.outputfd != sys.stdout:
        settings.outputfd.close()
    if settings.input:
        settings.inputfd.close()


if __name__ == "__main__":
    main()
