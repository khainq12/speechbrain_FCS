
from dataclasses import asdict
from typing import Dict


MAGNITUDE_ORDER = {
    "very-small": 1,
    "small": 2,
    "medium": 3,
    "large": 4,
    "very-large": 5,
}

URGENCY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "very-high": 4,
}

SAFETY_ORDER = {
    "strict": 1,
    "normal": 2,
    "relaxed": 3,
}


def normalize_with_ha(command) -> Dict:
    """
    Phase-1 HA placeholder.
    Replace later with full Hedge Algebra module.
    """
    d = asdict(command)
    d["magnitude_rank"] = MAGNITUDE_ORDER.get(d["magnitude"], 2)
    d["urgency_rank"] = URGENCY_ORDER.get(d["urgency"], 2)
    d["safety_rank"] = SAFETY_ORDER.get(d["safety"], 1)
    return d
