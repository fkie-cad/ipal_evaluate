from .metric import Metric, get_alarms


class TruePositiveAlarms(Metric):
    _name = "TPA"
    _description = "True positive alarms (TPA) counts the number of continuous alarms that overlap with at least a single attack."
    _requires = []
    _requires_timed_dataset = True
    _requires_attacks = True
    _higher_is_better = True

    @classmethod
    def calculate(
        cls,
        truth=None,
        predicted=None,
        dataset=None,
        attacks=None,
        ergs=None,
    ):
        assert dataset is not None and attacks is not None
        count = 0

        for start, end in get_alarms(dataset):
            for attack in attacks:
                if start <= attack["end"] and end >= attack["start"]:  # any overlap
                    count += 1
                    break

        return {cls._name: count}


class FalsePositiveAlarms(Metric):
    _name = "FPA"
    _description = "False positive alarms (FPA) counts the number of continuous alarms that do not overlap with any attack."
    _requires = []
    _requires_timed_dataset = True
    _requires_attacks = True
    _higher_is_better = False

    @classmethod
    def calculate(
        cls,
        truth=None,
        predicted=None,
        dataset=None,
        attacks=None,
        ergs=None,
    ):
        assert dataset is not None and attacks is not None
        fpa = set(get_alarms(dataset))

        for start, end in get_alarms(dataset):
            for attack in attacks:
                if start <= attack["end"] and end >= attack["start"]:  # any overlap
                    fpa.remove((start, end))
                    break

        return {cls._name: len(fpa)}
