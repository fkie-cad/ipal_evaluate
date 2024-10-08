#!/usr/bin/env python3
import argparse
import logging
import os
import sys

import orjson

import evaluate.settings as settings
from evaluate.evaluate import open_file


def validate_fields(obj, fields):
    """Validate that all required fields are present and not empty in a JSON object."""
    for field in fields:
        if field not in obj or not obj[field]:
            return False
    return True


def validate_data(js, fields):
    # Validate fields in each JSON object
    for obj in js:
        if not validate_fields(obj, fields):
            settings.logger.error(f"Missing required fields in an JSON entry: {obj}")
            exit(1)


# Boolean function to check whether a packet is malicious
def is_malicious(attacks, packet):
    for attack in attacks:
        if attack["start"] <= packet["timestamp"] <= attack["end"]:
            return attack["id"]
    return False


def initialize_logger(args):
    if args.log:
        settings.log = getattr(logging, args.log.upper(), None)

        if not isinstance(settings.log, int):
            logging.getLogger("ipal-add-attacks").error(
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

    settings.logger = logging.getLogger("ipal-add-attacks")


def prepare_arg_parser(parser):
    # Add arguments to parser
    parser.add_argument(
        "--attacks",
        metavar="FILE",
        help="Path to attacks.json file of the dataset. ('-' stdin, '*.gz' compressed)",
        required=True,
    )

    parser.add_argument(
        "--input",
        metavar="FILE",
        help="Path to the input file that contains transcribed traffic. ('-' stdin, '*.gz' compressed)",
        required=True,
    )

    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Path to the output file. If file does not exist, it will be created. ('-' stdout, '*.gz' compressed) (Default: '-')",
        default="-",
        required=False,
    )

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

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {settings.version}"
    )


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add arguments to parser
    prepare_arg_parser(parser)

    # Parse the command-line arguments
    args = parser.parse_args()

    initialize_logger(args)

    # Check if the attacks and ipal files exist
    if not os.path.isfile(args.attacks) and not args.attacks == "-":
        settings.logger.error(f"Attack file '{args.attacks}' does not exist.")
        exit(1)

    if not os.path.isfile(args.input) and not args.input == "-":
        settings.logger.error(f"Input IPAL file '{args.input}' does not exist.")
        exit(1)

    # Define required fields for attacks and ipal
    required_attack_fields = ["start", "end"]
    required_ipal_fields = ["timestamp"]

    # Read attack file and store objects in a list
    with open_file(args.attacks, "rb") as f:
        attack_objects = orjson.loads(f.read())
        validate_data(attack_objects, required_attack_fields)

    with open_file(args.input, "rt") as f:
        ipal_objects = [orjson.loads(line) for line in f]
        validate_fields(ipal_objects, required_ipal_fields)

    # Check if packet is malicious and update object
    for packet in ipal_objects:
        packet["malicious"] = is_malicious(attack_objects, packet)

    # Save output
    with open_file(args.output, "wb") as file:
        is_stdout = file == sys.stdout
        for packet in ipal_objects:
            serialized_json = orjson.dumps(
                packet, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
            )
            # need to handle stdout differently, since it expects text output
            if is_stdout:
                file.write(serialized_json.decode("utf-8"))
            else:
                file.write(serialized_json)


if __name__ == "__main__":
    main()
