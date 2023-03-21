import evaluate.settings as settings

from .metric import Metric


class JaccardIndex(Metric):
    _name = "Jaccard-Index"
    _description = "The Jaccard index measures the similarity between the set of entries deemed to be malicious obtained from the classification and the one obtained from the ground truth. Synonyms: Tanimoto Index."
    _requires = ["tp", "fn", "fp"]
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
        tp, fp, fn = ergs["tp"], ergs["fp"], ergs["fn"]

        # decoupling from f1-errors
        denom = tp + fn + fp

        if denom == 0:
            settings.logger.warning("Jaccard Index is undefined.")
            return {cls._name: 0}
        else:
            return {cls._name: tp / denom}


class JaccardDistance(Metric):
    _name = "Jaccard-Distance"
    _description = "The Jaccard distance is the complement to the Jaccard index, it measures the dissimilarity between the classification and the ground truth."
    _requires = ["Jaccard-Index"]
    _requires_timed_dataset = False
    _requires_attacks = False
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
        assert ergs is not None
        jaccard_index = ergs["Jaccard-Index"]

        return {cls._name: 1 - jaccard_index}
