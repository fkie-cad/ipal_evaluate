from math import exp
from typing import Any, Dict, List

import evaluate.settings as settings

from .metric import Metric


class Nab(Metric):
    _name = "nab-score"
    _description = "The NAB score weighs the evaluation of classification results based on their relative position to attack scenarios. Rewards (for true positives) and penalties (for false positives) are scaled by the sigmoid function centered around the end of attack windows. This ensures that early detections are rewarded, while trailing false positives are only gradually penalized."
    _requires = ["Detected-Scenarios"]
    _requires_timed_dataset = True
    _higher_is_better = True

    @classmethod
    def _sigma(cls, relative_distance) -> float:
        # scale by two to ensure that _sigma(0) == 0
        if relative_distance >= 10:
            return -1
        return 2 * (1 / (1 + exp(5 * relative_distance))) - 1

    @classmethod
    def defines(cls) -> List[str]:
        return ["NAB-score-default, NAB-score-low-fp, NAB-score-low-fn"]

    @classmethod
    def _relative_pos(cls, entry: Dict[str, Any], attack: Dict[str, Any]) -> float:
        # relative position as calculated in the NAB project
        # negative position is off-by-one in that the computed position can
        # never be 0, but is instead 1 / window_len at the right-most position
        w_end = attack["end"]
        w_start = attack["start"]
        t = entry["timestamp"]

        if t <= w_end:
            return (t - w_end - 1) / (w_end - w_start + 1)

        return (t - w_end) / (w_end - w_start) if w_end - w_start != 0 else t - w_end

    @classmethod
    def _compute_scores(
        cls,
        scores: Dict[str, Dict[str, float]],
        dataset: List[Dict],
        attacks: List[Dict],
        profiles: Dict[str, Dict],
        scenario_count: int,
        false_negatives: int,
    ) -> Dict[str, Dict[str, float]]:
        ignore_until = 0
        a_index = 0
        max_end = 0
        for entry in dataset:
            if entry["ids"]:
                if entry["timestamp"] <= ignore_until:
                    continue
                # find the earliest attack that starts after the current timestamp (false positive)
                # or ends before the current timestamp (true positive)
                while a_index < len(attacks):
                    if attacks[a_index]["start"] > entry["timestamp"]:
                        a_index -= 1
                        break
                    else:
                        if attacks[a_index]["end"] >= entry["timestamp"]:
                            break
                    a_index += 1

                if a_index < 0:
                    # no attack before the alarm, scored as false positive with maximal penalty
                    for name, profile in profiles.items():
                        scores[name]["raw"] += profile["nab_afp"]
                    a_index = 0
                    continue
                else:
                    # handle false positives after the last attack
                    a_index = min(len(attacks) - 1, a_index)

                attack = attacks[a_index]
                rel_pos = cls._relative_pos(entry, attack)
                if rel_pos <= 0:
                    # true positive: the alarm is before the end of the attack
                    # ignore all following entries until the furthest end of all detected attacks so far,
                    # or the start of the following attack if it overlaps with the current attack
                    max_end = max(attack["end"], max_end)
                    ignore_until = max_end
                    if (
                        a_index + 1 < len(attacks)
                        and ignore_until >= attacks[a_index + 1]["start"]
                    ):
                        ignore_until = attacks[a_index + 1]["start"] - 1
                        a_index += 1
                    score = cls._sigma(rel_pos) / cls._sigma(-1.0)
                    for name, profile in profiles.items():
                        scores[name]["raw"] += score * profile["nab_atp"]
                else:
                    # false positive: sigmoidally increasing penalty for missing the attack
                    score = abs(cls._sigma(rel_pos))
                    for name, profile in profiles.items():
                        scores[name]["raw"] += score * profile["nab_afp"]

        for name, profile in profiles.items():
            scores[name]["raw"] += profile["nab_afn"] * false_negatives
            scores[name]["null"] = profile["nab_afn"] * scenario_count
            scores[name]["perfect"] = profile["nab_atp"] * scenario_count
            scores[name]["normalized"] = (
                100
                * (scores[name]["raw"] - scores[name]["null"])
                / (scores[name]["perfect"] - scores[name]["null"])
            )

        return scores

    @classmethod
    def calculate(
        cls, truth=None, predicted=None, dataset=None, attacks=None, ergs=None
    ) -> Dict[str, float]:
        assert ergs is not None and attacks is not None and dataset is not None

        scenario_count = len(attacks)
        false_negatives = scenario_count - len(ergs["Detected-Scenarios"])

        profiles = settings.nab_profiles
        scores: Dict[str, Dict[str, float]] = {
            name: {"raw": 0.0, "null": 0.0, "perfect": 0.0, "normalized": 0.0}
            for name in profiles.keys()
        }

        if len(attacks) == 0:
            return {
                "NAB-score-default": 0,
                "NAB-score-low-fp": 0,
                "NAB-score-low-fn": 0,
            }

        scores = cls._compute_scores(
            scores, dataset, attacks, profiles, scenario_count, false_negatives
        )

        return {
            "NAB-score-default": scores["default"]["normalized"],
            "NAB-score-low-fp": scores["reward_low_fp"]["normalized"],
            "NAB-score-low-fn": scores["reward_low_fn"]["normalized"],
        }
