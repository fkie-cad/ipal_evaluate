import sys

import evaluate.settings as settings

from .basic_metrics import FScore
from .metric import Metric


class AffiliationMetric(Metric):
    _name = "Affiliation"
    _description = "The [Affiliation Metric](https://dl.acm.org/doi/pdf/10.1145/3534678.3539339) implements two variants of precision and recall to solve the insufficiencies of their point-based counterparts. Moreover, this metric claims to be more resilient against adversarial algorithms and random predictions."
    _requires = []
    _requires_timed_dataset = True
    _requires_attacks = False
    _higher_is_better = True

    @classmethod
    def defines(cls):
        return ["Affiliation-Precision", "Affiliation-Recall"] + [
            f"Affiliation-F{beta}" for beta in settings.fscore_betas
        ]

    @classmethod
    def calculate(
        cls,
        truth=None,
        predicted=None,
        dataset=None,
        attacks=None,
        ergs=None,
    ):
        try:  # Load modules
            from affiliation.generics import convert_vector_to_events
            from affiliation.metrics import pr_from_events
        except ModuleNotFoundError:
            settings.logger.error("Please install affiliation-metrics-py")
            sys.exit(1)

        assert truth is not None and predicted is not None

        # Cf. https://github.com/ahstat/affiliation-metrics-py#usage
        events_pred = convert_vector_to_events(predicted)
        events_gt = convert_vector_to_events(truth)
        Trange = (0, len(predicted))
        result = pr_from_events(events_pred, events_gt, Trange)

        output = {
            "Affiliation-Precision": result["precision"],
            "Affiliation-Recall": result["recall"],
        }

        fscores = FScore.calculate(
            ergs={"Precision": result["precision"], "Recall": result["recall"]}
        )
        for fscore, score in fscores.items():
            output[f"Affiliation-{fscore}"] = score

        return output
