import evaluate.settings as settings

from .metric import Metric


# https://par.nsf.gov/servlets/purl/10104860
class BatadalTTD(Metric):
    # Cf. https://par.nsf.gov/servlets/purl/10104860 equation (3)
    _name = "BATADAL-TTD"
    _description = (
        "BATADAL time-to-detection. Normalized time until an attack is detected."
    )
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
        assert dataset is not None
        attackCount = 0
        score = 0

        attack_start = None
        prev_timestamp = None
        detection = None

        for d in dataset:
            if attack_start is None and d["malicious"]:  # Start of attack
                attack_start = d["timestamp"]
                detection = None

            elif attack_start is not None and not d["malicious"]:  # End of attack
                if prev_timestamp == attack_start:  # attack only one timestep
                    score += 0 if detection else 1
                else:
                    if (
                        detection is None
                    ):  # attack not detected. Assign maximum TTD (cf paper)
                        detection = prev_timestamp

                    ttd = detection - attack_start
                    score += ttd / (prev_timestamp - attack_start)

                attack_start = None
                attackCount += 1

            if d["ids"] and detection is None:  # Store earliest detection
                detection = d["timestamp"]
            prev_timestamp = d["timestamp"]

        # End of dataset
        if attack_start is not None:
            if detection is None:
                detection = prev_timestamp

            ttd = detection - attack_start
            score += ttd / (prev_timestamp - attack_start)
            attackCount += 1

        return {cls._name: 1 - score / attackCount}


class BatadalCLF(Metric):
    # Cf. https://par.nsf.gov/servlets/purl/10104860 equation (6)
    _name = "BATADAL-CLF"
    _description = "BATADAL classification performance. Mean between TNR and TPR"
    _requires = ["Recall", "Inverse-Recall"]
    _requires_timed_dataset = False
    _requires_attacks = False
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
        assert ergs is not None
        tpr, tnr = ergs["Recall"], ergs["Inverse-Recall"]

        return {cls._name: (tpr + tnr) / 2}


class Batadal(Metric):
    # Cf. https://par.nsf.gov/servlets/purl/10104860 equation (6)
    _name = "BATADAL"
    _description = "BATADAL ranking. Weighted BATADAL-TTD and BATADAL-CLF"
    _requires = ["BATADAL-TTD", "BATADAL-CLF"]
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
        assert ergs is not None
        ttd, clf = ergs["BATADAL-TTD"], ergs["BATADAL-CLF"]
        gamma = settings.batadal_gamma

        return {cls._name: gamma * ttd + (1 - gamma) * clf}
