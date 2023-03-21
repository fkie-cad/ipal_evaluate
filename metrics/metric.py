import evaluate.settings as settings


class Metric:
    _name = ""  # the name of the metric
    _description = ""  # a short description about the metric
    _requires = []  # a list of other metric names required for the calculation
    _requires_timed_dataset = False  # whether the metric requires a timed dataset
    _requires_attacks = False  # whether the metric requires the attack file
    _higher_is_better = True  # is a higher score in that metric better?

    @classmethod
    def defines(cls):
        # By default a metric returns its own metric as calculation. However, this
        # may not be true for, e.g., the F-Score which can yield F1 F0.5 etc.
        return [cls._name]

    @classmethod
    def check_requirements(cls, ergs, attacks, timed_dataset):
        # Check if datset is timed
        if cls._requires_timed_dataset and not timed_dataset:
            settings.logger.warning(
                "'{}' requires timed dataset (skipped)".format(cls._name)
            )
            return False

        # Check attack requirements
        if cls._requires_attacks and (attacks is None or len(attacks) == 0):
            settings.logger.warning("'{}' requires attacks (skipped)".format(cls._name))
            return False

        # Check required metrics if needed
        if len(cls._requires) > 0:
            if ergs is None:  # No metrics provided
                settings.logger.warning(
                    "'{}' requires '{}' (skipped)".format(
                        cls._name, ",".join(cls._requires)
                    )
                )
                return False

            for req in cls._requires:  # check if all are provided
                if req not in ergs:
                    settings.logger.warning(
                        "'{}' requires '{}' (skipped)".format(cls._name, req)
                    )
                    return False

        # All requirements passed
        return True

    @classmethod
    def calculate(
        cls,
        truth=None,
        predicted=None,
        dataset=None,
        attacks=None,
        ergs=None,
    ):
        raise NotImplementedError
        # return {cls._name: the-score}


# Helper


# Get start and end of consecutive alarms as tuples
def get_alarms(dataset):
    alarms = []

    START = None
    END = None

    for d in dataset:
        if d["ids"]:  # IDS Alarm
            END = d["timestamp"]
            if START is None:
                START = d["timestamp"]

        else:
            if START is not None:
                alarms.append((START, END))
                START = None
                END = None

    if START is not None:  # Add alarm, which is not finished at the end
        alarms.append((START, END))

    return alarms
