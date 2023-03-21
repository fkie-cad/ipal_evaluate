from sklearn.metrics import confusion_matrix

import evaluate.settings as settings

from .metric import Metric


class Confusion(Metric):
    _name = "Confusion-Matrix"
    _description = "Calculates the confusion metrix including tn, fp, fn, tp"
    _requires = []
    _requires_timed_dataset = False
    _requires_attacks = False
    _higher_is_better = False

    @classmethod
    def defines(cls):
        return ["tn", "fp", "fn", "tp"]

    @classmethod
    def calculate(
        cls,
        truth=None,
        predicted=None,
        dataset=None,
        attacks=None,
        ergs=None,
    ):
        assert truth is not None and predicted is not None

        tn, fp, fn, tp = confusion_matrix(truth, predicted, labels=[0, 1]).ravel()

        return {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        }


class Accuracy(Metric):
    _name = "Accuracy"
    _description = "Accuracy captures the overall proportion of correct classifications. The higher the accuracy score is, the more reliable the predictions of the IIDS are. Synonyms: Rand Index."
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
        return {cls._name: (tp + tn) / (tp + tn + fp + fn)}


class Precision(Metric):
    _name = "Precision"
    _description = "Precision is the proportion of correct classifications among all positive classifications (entries classified as malicious). It captures the validness of positive classifications. Synonyms: PPV, Confidence."
    _requires = ["tp", "fp"]
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
        tp, fp = ergs["tp"], ergs["fp"]
        return {cls._name: 0 if tp + fp == 0 else tp / (tp + fp)}


class InversePrecision(Metric):
    _name = "Inverse-Precision"
    _description = "In contrast to precision, inverse precision is the proportion of benign entries correctly classified as benign. Synonyms: NPV, TNA."
    _requires = ["tn", "fn"]
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
        tn, fn = ergs["tn"], ergs["fn"]
        return {cls._name: 0 if tn + fn == 0 else tn / (tn + fn)}


class Recall(Metric):
    _name = "Recall"
    _description = "Recall states how many malicious entries of the dataset are actually detected by an IIDS. It captures the completeness of positive classifications. Synonyms: TPR, Sensitivity, Hit Rate."
    _requires = ["tp", "fn"]
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
        tp, fn = ergs["tp"], ergs["fn"]
        return {cls._name: 0 if tp + fn == 0 else tp / (tp + fn)}


class InverseRecall(Metric):
    _name = "Inverse-Recall"
    _description = "Inverse recall is the proportion of classifications as benign behavior that are correct. Synonyms: TNR, Specificity, Selectivity."
    _requires = ["tn", "fp"]
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
        tn, fp = ergs["tn"], ergs["fp"]
        return {cls._name: 0 if tn + fp == 0 else tn / (tn + fp)}


class Fallout(Metric):
    _name = "Fallout"
    _description = "Fallout calculates the fraction of false alarms across the dataset. Synonyms: FPR."
    _requires = ["fp", "tp", "fn"]
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
        fp, tp, fn = ergs["fp"], ergs["tp"], ergs["fn"]
        return {cls._name: 1 if fp + fn == 0 else fp / (tp + fn)}


class MissRate(Metric):
    _name = "Missrate"
    _description = (
        "Missrate measures the fraction of missed malicious entries. Synonyms: FNR."
    )
    _requires = ["fn", "tn", "fp"]
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
        fn, tn, fp = ergs["fn"], ergs["tn"], ergs["fp"]
        return {cls._name: 1 if tn + fp == 0 else fn / (tn + fp)}


class Informedness(Metric):
    _name = "Informedness"
    _description = "Informedness aggregates recall and inverse recall, measuring how informed the IIDS is, i.e. the completeness of both positive and negative classifications. Synonyms: Youden's J statistic."
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
        recall, inverse_recall = ergs["Recall"], ergs["Inverse-Recall"]
        return {cls._name: recall + inverse_recall - 1}


class Markedness(Metric):
    _name = "Markedness"
    _description = "Markedness aggregates precision and inverse precision, measuring the reliability of the IIDS, i.e. the validness of both positive and negative classifications."
    _requires = ["Precision", "Inverse-Precision"]
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
        precision, inverse_precision = ergs["Precision"], ergs["Inverse-Precision"]
        return {cls._name: precision + inverse_precision - 1}


class FScore(Metric):
    _name = "F-Score"
    _description = "Usually, an inherent tradeoff between achieving a maximal number of detected attacks (recall) while reducing false positives (precision) exists. The F-score combines both design goals into a single metric. F1 is the harmonic mean between precision and recall."
    _requires = ["Precision", "Recall"]
    _requires_timed_dataset = False
    _requires_attacks = False
    _higher_is_better = True

    @classmethod
    def defines(cls):
        return ["F{}".format(beta) for beta in settings.fscore_betas]

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
        precision, recall = ergs["Precision"], ergs["Recall"]

        result = {}

        for beta in settings.fscore_betas:
            if beta == float("inf"):
                score = recall

            elif beta == 0:
                score = precision

            elif precision == recall == 0:
                score = 0

            elif 0 <= beta:
                score = (
                    (1 + beta**2)
                    * (precision * recall)
                    / (beta**2 * precision + recall)
                )

            else:
                raise ValueError(f"Invalid {beta=}")

            result["F{}".format(beta)] = score

        return result
