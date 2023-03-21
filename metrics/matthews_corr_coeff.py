import math

import evaluate.settings as settings

from .metric import Metric


class MCC(Metric):
    _name = "MCC"
    _description = "Matthew's Correlation Coefficient measures the correlation between the IIDS' classification and the ground truth. Its main advantage over the F-score is that it is not affected by over-representation of either benign of malicious entries. Synonyms: Phi coefficient."
    _requires = ["tp", "fp", "tn", "fn"]
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
        tp, fp, tn, fn = ergs["tp"], ergs["fp"], ergs["tn"], ergs["fn"]

        # to prevent overflow split into individual sqrts
        denom = (
            math.sqrt((tp + fp))
            * math.sqrt((tp + fn))
            * math.sqrt((tn + fp))
            * math.sqrt((tn + fn))
        )

        if denom == 0:
            settings.logger.warning("MCC is undefined")
            return {cls._name: 0}
        else:
            return {cls._name: (tp * tn - fp * fn) / denom}
