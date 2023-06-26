#!/usr/bin/env python3
import argparse
import gzip
import json
import logging
import sys
import traceback
from typing import Any, Dict, List

import evaluate.settings as settings
from evaluate.utils import parse_ipal_input
from metrics.utils import get_all_metrics

REQUIRED_KEYS = ["id", "timestamp", "malicious", "ids"]


# Wrapper for hiding .gz files
def open_file(filename, mode):
    if filename.endswith(".gz"):
        return gzip.open(filename, mode=mode, compresslevel=settings.compresslevel)
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
        default=9,
        help="set the gzip compress level (0 no compress, 1 fast/large, ..., 9 slow/tiny) (Default: 9)",
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

        if settings.compresslevel < 0 or 9 < settings.compresslevel:
            settings.logger.error(
                "Option '--compresslevel' must be an integer from 0-9"
            )
            exit(1)

    # Parse and open input file
    if args.input:
        settings.input = args.input[0]

    if settings.input != "stdout" and settings.input != "-":
        settings.inputfd = open_file(settings.input, "r")
    else:
        settings.inputfd = sys.stdin

    # Parse and open output file
    if args.output:
        settings.output = args.output

    if settings.output != "stdout" and settings.output != "-":
        # clear the file we are about to write to
        open_file(settings.output, "wt").close()
        settings.outputfd = open_file(settings.output, "wt")
    else:
        settings.outputfd = sys.stdout

    # Parse attacks
    if args.attacks:
        settings.attacks = args.attacks

    # Parse timed
    if args.timed:
        if args.timed in ["True", "true"]:
            settings.timed_dataset = True
        elif args.timed in ["False", "false"]:
            settings.timed_dataset = False
        else:
            settings.logger.error("Option '--timed-dataset' must be true or false")
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
    error = False

    sorted_attacks = sorted(attacks, key=lambda x: x["start"])
    warning = []
    for i, attack in enumerate(attacks):
        if attack != sorted_attacks[i]:
            other_index = 0
            for j, other_attack in enumerate(attacks):
                if sorted_attacks[i] == other_attack:
                    other_index = j
                    break
            warning.append(f", attack {i} with id '{attack['id']}' starts ")
            warning.append(
                f"{'after' if sorted_attacks[i]['start'] < attack['start'] else 'before'} "
            )
            warning.append(f"attack {other_index} with id '{sorted_attacks[i]['id']}'")
            error = True

    if len(warning) > 0:
        settings.logger.error(
            "".join(
                ["Attacks must be sorted chronologically, yet"]
                + warning
                + [
                    ". Fix the attack file to ensure that metrics are computed correctly"
                ]
            )
        )
    warning = []
    for i in range(1, len(sorted_attacks)):
        if sorted_attacks[i]["start"] <= sorted_attacks[i - 1]["end"]:
            warning.append(f", attack with id '{sorted_attacks[i]['id']}' starts at ")
            warning.append(f"timestamp {sorted_attacks[i]['start']} before ")
            warning.append(f"attack with id '{sorted_attacks[i-1]['id']}' ends at ")
            warning.append(f"timestamp {sorted_attacks[i-1]['end']}")
    if len(warning) > 0:
        settings.logger.warning(
            "".join(
                ["Attacks must be non-overlapping, yet"]
                + warning
                + [". Some metrics might not be computed correctly"]
            )
        )
    return error


def evaluate(attacks, truth, predicted, dataset):
    ergs = {}

    # Evaluate point based metrics
    for name, metric in get_all_metrics().items():
        if metric.check_requirements(ergs, attacks, settings.timed_dataset):
            try:
                ergs = {
                    **ergs,
                    **metric.calculate(truth, predicted, dataset, attacks, ergs),
                }
                settings.logger.info("Calculated '{}'".format(name))

            except Exception as e:
                settings.logger.error(
                    "Failed calculating the '{}' metric!".format(name)
                )
                settings.logger.debug(traceback.format_exc())
                settings.logger.error(str(e))

                for real_name in metric.defines():
                    ergs[real_name] = None

        else:
            dummy = {real_name: None for real_name in metric.defines()}
            ergs = {**ergs, **dummy}

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
        settings.logger.info("Loading attacks from {}".format(settings.attacks))
        with open_file(settings.attacks, "r") as f:
            attacks = json.load(f)

    else:
        settings.logger.warning("No attack file provided! Some metrics may be skipped")
        attacks = None

    # 1.5) If dataset is timed, check attack order and overlap
    if settings.timed_dataset and attacks is not None:
        if check_timed_attacks_keys(attacks) or check_timed_attacks_order(attacks):
            sys.exit(1)

    # 2) Load IDS classification results
    settings.logger.info("Loading dataset from {}".format(settings.input))

    dataset = []
    _first = True

    for line in settings.inputfd.readlines():
        js = json.loads(line)

        if _first:  # Forward transcriber/ipal_iids parameters
            configs = {k: v for k, v in js.items() if k.startswith("_")}
            _first = False

        # Avoid loading the entire dataset into memory
        for rm in [key for key in js if key not in REQUIRED_KEYS]:
            del js[rm]

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
    settings.logger.info("Writing evaluation files to {}".format(settings.output))
    settings.outputfd.write(json.dumps({**ergs, **configs}, indent=4) + "\n")

    # Finalize and close
    if settings.output and settings.outputfd != sys.stdout:
        settings.outputfd.close()
    if settings.input:
        settings.inputfd.close()


if __name__ == "__main__":
    main()
