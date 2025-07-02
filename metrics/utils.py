from .affiliation import AffiliationMetric
from .alarms import FalsePositiveAlarms, TruePositiveAlarms
from .basic_metrics import (
    Accuracy,
    Confusion,
    Fallout,
    FScore,
    Informedness,
    InversePrecision,
    InverseRecall,
    Markedness,
    MissRate,
    Precision,
    Recall,
)
from .batadal import Batadal, BatadalCLF, BatadalTTD
from .jaccard import JaccardDistance, JaccardIndex
from .matthews_corr_coeff import MCC
from .nab_score import Nab
from .scenarios import (
    AverageTimeToDetection,
    DetectedScenarios,
    DetectedScenariosPercent,
    DetectionDelay,
    PenaltyScore,
    ScenarioRecall,
)
from .tapr import eTaPR

metrics = [
    # Basic Metrics
    Confusion,
    Accuracy,
    Precision,
    InversePrecision,
    Recall,
    InverseRecall,
    Fallout,
    MissRate,
    Informedness,
    Markedness,
    FScore,
    # Further basic point-based metrics
    MCC,
    JaccardIndex,
    JaccardDistance,
    # Scenario and Alarm Metrics
    DetectedScenarios,
    DetectedScenariosPercent,
    ScenarioRecall,
    PenaltyScore,
    DetectionDelay,
    AverageTimeToDetection,
    TruePositiveAlarms,
    FalsePositiveAlarms,
    # Time-Aware metrics
    eTaPR,
    BatadalTTD,
    BatadalCLF,
    Batadal,
    Nab,
    AffiliationMetric,
]


def get_all_metrics():
    return {metric._name: metric for metric in metrics}
