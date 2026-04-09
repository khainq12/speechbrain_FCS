
from copy import deepcopy


def validate_and_correct(packet_dict: dict, conf_threshold: float = 0.6):
    out = deepcopy(packet_dict)
    issues = []

    if out.get("confidence", 0.0) < conf_threshold:
        issues.append("low_confidence")

    if out.get("direction") is None or out.get("direction") == "":
        out["direction"] = "none"
        issues.append("missing_direction")

    if out.get("magnitude_rank", 0) < 1:
        out["magnitude_rank"] = 1
        issues.append("invalid_magnitude_low")
    if out.get("magnitude_rank", 0) > 5:
        out["magnitude_rank"] = 5
        issues.append("invalid_magnitude_high")

    if out.get("command_type", "none") == "none":
        out["command_type"] = "hover"
        issues.append("fallback_hover")

    out["issues"] = issues
    out["accepted"] = len(issues) == 0 or issues == ["low_confidence"]
    return out
