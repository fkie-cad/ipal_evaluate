from ray import tune

# Configure how the IIDS is evaluated and tuned
config = {
    "name": "Testconfig",
    "seed": 1234,
    "num_samples": 4,
    "cpus_per_trial": 1,
    "gpus_per_trial": 0,
    "train_file": "./train.ipal",
    "combiner_file": "<none>",
    "test_files": ["./test.ipal"],
    "attack_file": "./attacks.json",
    "file_type": "state",
    "is_timed_dataset": True,
    "extend_alarms": False,
    "keep_output": False,
    "metric": "F1",
    "mode": "max",
}

# Configure the IIDS and the combiner
parameters = {
    # put IIDS config here and define tunable hyperparameters with, e.g.:
    "iids": {
        "MinMax": {
            "_type": "MinMax",
            "model-file": "./model-minmax",
            "features": [
                "state;1",
                "state;2",
                "state;3",
                "state;4",
                "state;5",
                "state;6",
                "state;7",
                "state;8",
                "state;9",
                "state;10",
                "state;11",
                "state;12",
                "state;13",
                "state;14",
                "state;15",
                "state;16",
                "state;17",
                "state;18",
                "state;19",
                "state;20",
                "state;21",
                "state;22",
                "state;23",
                "state;24",
                "state;25",
                "state;26",
                "state;27",
                "state;28",
                "state;29",
                "state;30",
                "state;31",
                "state;32",
                "state;33",
                "state;34",
                "state;35",
                "state;36",
                "state;37",
                "state;38",
                "state;39",
                "state;40",
                "state;41",
            ],
            "preprocessors": [],
            "allow-none": False,
            "save-training": None,
            "trainon": 1.0,
            "threshold": tune.quniform(0, 2, 1e-1),
        }
    },
    "combiner": {"_type": "Any", "model-file": "model-combiner"},
}

search_alg = tune.search.BasicVariantGenerator()

reporter = tune.CLIReporter(
    max_progress_rows=15,
    max_column_length=80,
    sort_by_metric=True,
    parameter_columns={"iids/MinMax/threshold": "threshold"},
    max_report_frequency=3600,
)
reporter.add_metric_column(config["metric"])
