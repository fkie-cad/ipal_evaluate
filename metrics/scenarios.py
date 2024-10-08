import evaluate.settings as settings

from .metric import Metric


class DetectedScenarios(Metric):
    _name = "Detected-Scenarios"
    _description = "Detected scenarios lists the attack scenarios detected by at least a single alarm."
    _requires = []
    _requires_timed_dataset = False
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
        scenarios = set()

        attackids = {att["ipalid"]: att["id"] for att in attacks if "ipalid" in att}

        for d in dataset:
            if d["ids"]:  # if there is an alert
                if "ipalid" in d and d["ipalid"] in attackids:  # detected by ipalid
                    scenarios.add((attackids[d["ipalid"]], None, None))

                for att in attacks:  # detected time range
                    if "start" in att and "end" in att:
                        if (
                            att["start"] - settings.alarm_gracetime
                            <= d["timestamp"]
                            <= att["end"] + settings.alarm_gracetime
                        ):
                            scenarios.add((att["id"], att["start"], att["end"]))

        return {cls._name: sorted([s[0] for s in scenarios])}


class DetectedScenariosPercent(Metric):
    _name = "Detected-Scenarios-Percent"
    _description = "Proportion of attack scenarios that were detected by the IIDS."
    _requires = ["Detected-Scenarios"]
    _requires_timed_dataset = False
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
        assert attacks is not None and ergs is not None
        scenarios = set(ergs["Detected-Scenarios"])
        uniqueattacks = set([a["id"] for a in attacks])

        return {cls._name: len(scenarios) / len(uniqueattacks)}


class ScenarioRecall(Metric):
    _name = "Scenario-Recall"
    _description = "Recall measurement on a per-attack-scenario basis."
    _requires = []
    _requires_timed_dataset = False
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
        assert attacks is not None and dataset is not None
        scenarios = {a["id"]: {"tp": 0, "fn": 0} for a in attacks}

        for d in dataset:
            if not d["malicious"]:
                continue

            if d["malicious"] not in scenarios:
                settings.logger.warning(f"Scenario '{d['malicious']}' not found!")
                continue

            if d["ids"]:
                scenarios[d["malicious"]]["tp"] += 1
            else:
                scenarios[d["malicious"]]["fn"] += 1

        for k, v in scenarios.items():
            if v["tp"] + v["fn"] == 0:
                scenarios[k] = 0
            else:
                scenarios[k] = v["tp"] / (v["tp"] + v["fn"])

        return {cls._name: scenarios}


class PenaltyScore(Metric):
    _name = "Penalty-Score"
    _description = "Penalty Score (PS) is the length of detection results outside their overlap with attack scenarios (cf. TABOR paper)."
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
        assert attacks is not None and dataset is not None
        ps = 0
        prev = dataset[0]["timestamp"]

        for d in dataset:
            if d["ids"]:
                for attack in attacks:
                    if attack["start"] <= d["timestamp"] <= attack["end"]:
                        break
                else:
                    ps += d["timestamp"] - prev

            prev = d["timestamp"]

        return {cls._name: ps}


class DetectionDelay(Metric):
    _name = "Detection-Delay"
    _description = "The detection delay aggregates the time intervals between the start of an attack and the time of the first detection."
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
        assert dataset is not None and attacks is not None and ergs is not None
        dd = 0

        detected_scenarios = set(ergs["Detected-Scenarios"])
        detected = set()
        detected_amount = 0
        detected_before_amount = 0
        prev = dataset[0]["timestamp"]

        # Filter attacks once before iterating over dataset
        active_attacks = [
            attack for attack in attacks if attack["id"] in detected_scenarios
        ]

        for d in dataset:

            # Filter out already detected attacks
            # for efficiency only filter if change occurred
            if detected_amount != detected_before_amount:
                detected_before_amount = detected_amount
                active_attacks = [
                    attack for attack in active_attacks if attack["id"] not in detected
                ]

            for attack in active_attacks:
                # overlapping now
                if attack["start"] <= d["timestamp"] <= attack["end"]:
                    dd += d["timestamp"] - max(prev, attack["start"])
                    if d["ids"]:  # attack detected
                        detected.add(attack["id"])
                        detected_amount = len(detected)

            prev = d["timestamp"]

        return {cls._name: dd}
