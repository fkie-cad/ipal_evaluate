from enum import IntEnum, unique

import numpy as np


@unique
class ADLabels(IntEnum):
    # Default 2-class scenario
    ANOMALY = 1
    NON_ANOMALOUS = 0

    @staticmethod
    def from_is_malicious(malicious: bool):
        return ADLabels.ANOMALY if malicious else ADLabels.NON_ANOMALOUS

    @staticmethod
    def default_order():
        return [ADLabels.ANOMALY.value, ADLabels.NON_ANOMALOUS.value]

    @staticmethod
    def reverse_order():
        return [ADLabels.NON_ANOMALOUS.value, ADLabels.ANOMALY.value]


def parse_ipal_input(dataset):
    """Extracts truth labels (from the dataset), and the IDS' classification result

    Args:
        dataset: a list of IPAL messages

    Returns:
        (truth, ids-classification)
    """

    truth = np.empty(len(dataset), dtype=int)
    predicted = np.empty(len(dataset), dtype=int)

    for i, ipal in enumerate(dataset):
        truth[i] = ADLabels.from_is_malicious(ipal["malicious"]).value
        predicted[i] = ADLabels.from_is_malicious(ipal["ids"]).value

    return truth, predicted
