#!/usr/bin/env python3
import argparse
import gzip
import importlib
import logging
import os
import random
import shutil
import sys
import time

import numpy as np
import ray
from ray import air, tune

import evaluate.settings as settings
from evaluate.tuner import IidsTrainable


# Wrapper for hiding .gz files
def open_file(filename, mode):
    if filename is None:
        return None
    elif filename.endswith(".gz"):
        return gzip.open(filename, mode=mode, compresslevel=settings.compresslevel)
    elif filename == "-":
        return sys.stdin
    else:
        return open(filename, mode=mode, buffering=1)


# Initialize logger
def initialize_logger(args):
    if args.log:
        settings.log = getattr(logging, args.log.upper(), None)

        if not isinstance(settings.log, int):
            logging.getLogger("ipal-tune").error("Option '--log' parameter not found")
            exit(1)

    if args.logfile:
        settings.logfile = args.logfile
        logging.basicConfig(
            filename=settings.logfile, level=settings.log, format=settings.logformat
        )
    else:
        logging.basicConfig(level=settings.log, format=settings.logformat)

    settings.logger = logging.getLogger("ipal-tune")


def dump_default_config(name):
    print(
        """from ray import tune

# Configure how the IIDS is evaluated and tuned
config = {
    "name": "Testconfig",

    "seed": 1234,
    "num_samples": 2,
    "cpus_per_trial": 1,
    "gpus_per_trial": 0,

    "train_file": "path/to/training/file",
    "combiner_file": "path/to/combiner/training/file",
    "test_files": ["path/to/test/file(s)"],
    "attack_file": "path/to/attacks.json",

    "file_type": ipal or state,
    "is_timed_dataset": True,
    "extend_alarms": False,
    "keep_output": False,

    "metric": "F1",
    "mode": "max",
}

def postprocess(config):
    # Hacky: Can be used to resolve nested parameter, which can not be handled by
    # some optimizaion algorithms. This methods is called right before the parameters
    # are handed over to ipal-iids
    return config

# Configure the IIDS and the combiner
parameters = {
    # put IIDS config here and define tunable hyperparameters
    # https://docs.ray.io/en/latest/tune/api/search_space.html

    "iids": {
        "NAME": {
            "_type": "<name>",
            "model-file": "model-iids",
            "threshold": tune.uniform(0.0, 5.0)
            ...
        }
    },

    "combiner": {"_type": "Any", "model-file": "model-combiner"},

    "_postprocess": postprocess,
}

# Fine-tuning of the raytune search algorithm
search_alg = tune.search.BasicVariantGenerator() # Default random search
#from ray.tune.search.bayesopt import BayesOptSearch
#search_alg = BayesOptSearch(mode=config["mode"], metric=config["metric"])
#from ray.tune.search.hyperopt import HyperOptSearch
#search_alg = HyperOptSearch(mode=config["mode"], metric=config["metric"])

reporter = tune.CLIReporter(max_progress_rows=15, max_column_length=80, sort_by_metric=True)
# Select specific parameters to monitor with: parameter_columns={"iids/NAME/threshold", "threshold"}
# Select specific metrics to monitor with: reporter.add_metric_column(config["metric"])
"""
    )
    exit(0)


def prepare_arg_parser(parser):
    # Configure tune program
    parser.add_argument(
        "--config",
        dest="config",
        metavar="FILE.py",
        help="load IDS configuration and hyperparameters from the specified file (python file).",
        required=False,
    )

    # Options for continuing experiments
    parser.add_argument(
        "--restart-experiment",
        dest="restart_experiment",
        action="store_true",
        help="Usually experiments are resumed. If this parameter is provided, a new experiment ist started from scratch.",
        required=False,
    )
    parser.add_argument(
        "--resume-errored",
        dest="resume_errored",
        action="store_true",
        help="Usually errored experiments are ignored. If this parameter is provided, errored experiments are rescheduled.",
        required=False,
    )

    # Resource options
    parser.add_argument(
        "--max-cpus",
        dest="max_cpus",
        type=int,
        metavar="INT",
        help="max number of CPUs to use (Default: detected available number of CPUs)",
        required=False,
    )
    parser.add_argument(
        "--max-gpus",
        dest="max_gpus",
        type=int,
        metavar="INT",
        help="max number of GPUs to use (Default: detected available number of GPUs)",
        required=False,
    )

    # Further options
    parser.add_argument(
        "--default.config",
        dest="defaultconfig",
        action="store_true",
        help="dump an exemplary default configuration",
        required=False,
    )

    # Logging
    parser.add_argument(
        "--log",
        dest="log",
        metavar="STR",
        help="define logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) (Default: WARNING).",
        required=False,
    )
    parser.add_argument(
        "--logfile",
        dest="logfile",
        metavar="FILE",
        default=False,
        help="file to log to (Default: stderr).",
        required=False,
    )

    # Gzip compress level
    parser.add_argument(
        "--compresslevel",
        dest="compresslevel",
        metavar="INT",
        default=9,
        help="set the gzip compress level. 0 no compress, 1 fast/large, ..., 9 slow/tiny. (Default: 9)",
        required=False,
    )

    # Version number
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {settings.version}"
    )


def load_settings(args):
    if args.defaultconfig:
        dump_default_config(args.defaultconfig)

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

    # Load configuration file
    if not args.config:
        settings.logger.error("no tune configuration provided, exiting")
        exit(1)

    try:
        settings.configfile = args.config
        spec = importlib.util.spec_from_file_location("module.name", args.config)
        settings.config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings.config)
    except Exception as e:
        settings.logger.error("Could not load rule file!")
        settings.logger.error(e)
        exit(1)

    # Forward log-level
    if args.log:
        settings.config.config["log-level"] = args.log
    else:
        settings.config.config["log-level"] = "WARNING"

    if args.max_cpus:
        settings.max_cpus = int(args.max_cpus)
        settings.logger.info(f"Using {settings.max_cpus} CPUs only")
    if args.max_gpus:
        settings.max_gpus = int(args.max_gpus)
        settings.logger.info(f"Using {settings.max_gpus} GPUs only")
    if args.restart_experiment:
        settings.restart = True
    if args.resume_errored:
        settings.resume_errored = True


def main():
    # Argument parser and settings
    parser = argparse.ArgumentParser(prog="ipal-tune")
    prepare_arg_parser(parser)
    args = parser.parse_args()
    initialize_logger(args)
    load_settings(args)

    # Shortcut
    config = settings.config.config

    # Set seeds
    random.seed(config["seed"])
    np.random.seed(config["seed"])

    # Prepare directory and paths
    os.chdir(os.path.dirname("./" + args.config))

    # Adjust training/test/attack files' paths
    config["train_file"] = os.path.abspath(config["train_file"])
    if config["attack_file"] is not None:
        config["attack_file"] = os.path.abspath(config["attack_file"])
    if config["combiner_file"] is not None:
        config["combiner_file"] = os.path.abspath(config["combiner_file"])
    config["test_files"] = [os.path.abspath(f) for f in config["test_files"]]

    # Configuring ray tune
    ray.init(num_cpus=settings.max_cpus, num_gpus=settings.max_gpus)

    # Tune
    t1 = time.time()
    settings.logger.info(f"Tuning started at {t1}")

    if not settings.restart and os.path.exists(config["name"]):
        settings.logger.info("Resuming experiment")
        # TODO test if the config file has not changed in between and warn the user if so
        tuner = tune.Tuner.restore(
            path=config["name"], resume_errored=settings.resume_errored
        )

    else:
        settings.logger.info("Starting experiment from scratch")

        try:
            shutil.rmtree(config["name"])  # remove old experiment data
        except FileNotFoundError:
            pass

        tune_config = tune.TuneConfig(
            metric=config["metric"],
            mode=config["mode"],
            num_samples=config["num_samples"],
            search_alg=settings.config.search_alg,
        )

        run_config = air.RunConfig(
            name=config["name"],
            local_dir="./",
            stop={"training_iteration": 1},  # we only have one iteration
            checkpoint_config=air.CheckpointConfig(checkpoint_at_end=False),
            progress_reporter=settings.config.reporter,
        )

        trainable_with_resources = tune.with_resources(
            IidsTrainable,
            {"cpu": config["cpus_per_trial"], "gpu": config["gpus_per_trial"]},
        )

        settings.config.parameters["tune_config"] = config

        tuner = tune.Tuner(
            trainable_with_resources,
            param_space=settings.config.parameters,
            run_config=run_config,
            tune_config=tune_config,
        )

    results = tuner.fit()

    t2 = time.time()
    settings.logger.info(f"Tuning ended at {t2} ({t2-t1}s)")

    print(
        "best result for {}:".format(config["metric"])
        + str(
            results.get_best_result(metric=config["metric"], mode=config["mode"]).config
        )
    )


if __name__ == "__main__":
    main()
