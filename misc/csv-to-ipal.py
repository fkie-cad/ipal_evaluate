#!/usr/bin/env python3
import argparse
from argparse import Namespace
from typing import Any, Dict, List

import orjson

from evaluate.evaluate import open_file


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
        metavar="FILE",
        nargs=1,
        help="input file in CSV format to convert to IPAL ('-' stdin, '*.gz' compressed)",
    )

    parser.add_argument(
        "output",
        metavar="FILE",
        nargs=1,
        help="output file to write the generated IPAL to ('-' stdout, '*.gz' compress)",
    )

    parser.add_argument(
        "--compresslevel",
        metavar="INT",
        type=int,
        default=6,
        help="set the gzip compress level (0 no compress, 1 fast/large, ..., 9 slow/tiny) (Default: 6)",
    )

    parser.add_argument(
        "--timestamp",
        metavar="INT",
        type=int,
        required=False,
        help="index of the column containing timestamps (index starts at 0)",
    )

    parser.add_argument(
        "--groundtruth",
        metavar="INT",
        type=int,
        required=True,
        help="index of the column containing the ground truth (index starts at 0)",
    )

    parser.add_argument(
        "--ids",
        metavar="INT",
        type=int,
        required=True,
        help="index of the column containing the IIDS classification output (index starts at 0)",
    )

    parser.add_argument(
        "--separator",
        metavar="STR",
        default=",",
        required=False,
        help="character used to separate cells (Default: ',')",
    )

    parser.add_argument(
        "--skip",
        metavar="INT",
        type=int,
        default=1,
        required=False,
        help="how many rows at the start of the file should be skipped (Default: 1, skip the header)",
    )

    parser.add_argument(
        "--header",
        metavar="INT",
        type=int,
        default=0,
        required=False,
        help=(
            "index of the row containing column headers, used to derive column names, "
            "must be less than the value provided to --skip (Default: 0)"
        ),
    )

    parser.add_argument(
        "--attacks",
        metavar="FILE",
        required=False,
        help=(
            "path under which the attacks file corresponding to the dataset should be written,"
            " requires the timestamp column to have been specified using --timestamp"
        ),
    )

    parser.add_argument(
        "--scores",
        metavar="STR",
        type=str,
        required=False,
        help=(
            "comma-separated list of <metric name>:<column index> pairs, e.g. "
            "'S1:4,S2:5,S3:8' indicates that the outputs of IIDS scores S1, S2, S3 "
            "are in columns 4, 5 and 8 respectively (index starts at 0)"
        ),
    )

    args = parser.parse_args()

    return args


def strip_quotes(val: str) -> str:
    if len(val) < 2:
        return val
    output = val
    if val[0] == "'" and val[-1] == "'":
        output = val.strip("'")
    elif val[0] == '"' and val[-1] == '"':
        output = val.strip('"')
    return output


def try_to_convert(val: str, t: type) -> Any:
    try:
        return t(val)
    except ValueError:
        return val


def main() -> None:
    args = parse_args()
    input_fd = open_file(args.input[0], mode="rt", compresslevel=args.compresslevel)
    output_fd = open_file(args.output[0], mode="wt", compresslevel=args.compresslevel)

    separator = args.separator
    index_ts = args.timestamp
    index_gt = args.groundtruth
    index_id = args.ids

    scores = (
        {int(m.split(":")[1]): m.split(":")[0] for m in args.scores.split(",")}
        if args.scores is not None
        else None
    )

    headers = None

    skipped = 0

    attack = False
    attacks: List[Dict[str, Any]] = []
    attack_start = 0
    previous_timestamp = 0

    for line in input_fd:
        line = line.rstrip()

        if skipped < args.skip:
            if skipped == args.header:
                # determine column names
                headers = [strip_quotes(token) for token in line.split(separator)]
            skipped += 1
            continue

        if headers is None:
            headers = [f"val_{i}" for i in range(len(line.split(separator)))]

        ipal = {}
        tokens = line.split(separator)

        # parse each cell according to the defined column type
        for i in range(len(tokens)):
            if index_ts is not None and i == index_ts:
                ipal["timestamp"] = int(tokens[i])
            elif i == index_gt:
                malicious = int(tokens[i])
                ipal["malicious"] = malicious != 0
            elif i == index_id:
                ids = int(tokens[i])
                ipal["ids"] = ids == 1
            elif scores is not None and i in scores.keys():
                if "scores" not in ipal.keys():
                    ipal["scores"] = {}
                metric_name = scores[i] if scores[i] != "" else headers[i]
                ipal["scores"][metric_name] = float(tokens[i])
            else:
                stripped = strip_quotes(tokens[i])
                if stripped != tokens[i]:
                    # definitely a string
                    ipal[headers[i]] = stripped
                elif "." in stripped:
                    # maybe a float?
                    ipal[headers[i]] = try_to_convert(stripped, float)
                else:
                    ipal[headers[i]] = try_to_convert(stripped, int)

        # determine attack boundaries
        if args.attacks and "timestamp" in ipal.keys():
            if attack and ipal["malicious"] is False:
                attack_obj = {
                    "id": len(attacks) + 1,
                    "start": attack_start,
                    "end": previous_timestamp,
                }
                attack = False
                attacks.append(attack_obj)
            elif not attack and ipal["malicious"] is True:
                attack = True
                attack_start = ipal["timestamp"]

            previous_timestamp = ipal["timestamp"]
        output_fd.write(orjson.dumps(ipal, option=orjson.OPT_APPEND_NEWLINE).decode("utf-8"))

    input_fd.close()
    output_fd.close()
    if index_ts is not None and args.attacks is not None:
        if attack:
            attack_obj = {
                "id": len(attacks) + 1,
                "start": attack_start,
                "end": previous_timestamp,
            }
            attacks.append(attack_obj)

        with open_file(args.attacks, mode="wt", compresslevel=args.compresslevel) as f:
            f.write(orjson.dumps(attacks, option=orjson.OPT_INDENT_2).decode("utf-8"))


if __name__ == "__main__":
    main()
