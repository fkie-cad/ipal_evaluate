import os
import tempfile

from eTaPR_pkg import etapr
from eTaPR_pkg.DataManage import File_IO

import evaluate.settings as settings

from .basic_metrics import FScore
from .metric import Metric


class eTaPR(Metric):
    _name = "TaPR"
    _description = "Hwang et al. proposed their (enhanced) time series-aware variants for classical point-based metrics, i.e., precision, recall, and F1, addressing known issues when adopting point-based metrics for time series-aware evaluations. For instance, while point-based recall weights long attacks as more important, the new time series-aware recall variant (eTaR) treats all consecutive attacks equally. To replace precision, eTaP implements diminishing returns for long-lasting alarms. Lastly, the new proposed eTaF score is defined in the same way as the regular F score but leverages the substitute eTaP and eTaR metrics."
    _requires = []
    _requires_timed_dataset = True
    _requires_attacks = False
    _higher_is_better = True

    @classmethod
    def _list_to_eTaPr_list(cls, inlist):
        fd, path = tempfile.mkstemp()

        with os.fdopen(fd, "w") as tmp:
            tmp.write("\n".join([str(x) for x in inlist]) + "\n")

        erg = File_IO.load_file(path, "stream")
        os.remove(path)

        return erg

    @classmethod
    def defines(cls):
        return ["eTaP", "eTaR"] + [
            "eTaF{}".format(beta) for beta in settings.fscore_betas
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
        assert truth is not None and predicted is not None
        if all([x == 0 for x in predicted]) or all([x == 0 for x in truth]):
            # eTaR/eTaP undefined for empty truth/prediction list, set everything to 0
            return {x: 0 for x in cls.defines()}

        truth = cls._list_to_eTaPr_list([-1 if x == 1 else 1 for x in truth])
        predicted = cls._list_to_eTaPr_list([-1 if x == 1 else 1 for x in predicted])

        result = etapr.evaluate_w_ranges(
            truth,
            predicted,
            settings.eTaPR_theta_p,
            settings.eTaPR_theta_r,
            settings.eTaPR_delta,
        )

        output = {
            "eTaR": result["eTaR"],
            "eTaP": result["eTaP"],
            # "eTaF1": result["f1"], # calculated below
        }

        fscores = FScore.calculate(
            ergs={"Precision": result["eTaP"], "Recall": result["eTaR"]}
        )
        for fscore, score in fscores.items():
            output["eTa{}".format(fscore)] = score

        assert abs(fscores["F1"] - result["f1"]) < 0.001

        return output
