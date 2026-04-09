
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class UAVCommand:
    command_type: str
    direction: str
    altitude_action: str
    magnitude: str
    urgency: str
    safety: str
    confidence: float = 1.0


FSC_TO_UAV = {
    # placeholder mappings for proof-of-concept
    ("activate", "lights", "kitchen"): ("move", "forward", "none", "small", "medium", "normal"),
    ("deactivate", "lights", "kitchen"): ("hover", "none", "none", "small", "low", "strict"),
    ("increase", "heat", "bedroom"): ("climb", "up", "up", "medium", "medium", "normal"),
    ("decrease", "heat", "bedroom"): ("descend", "down", "down", "medium", "medium", "normal"),
}


def map_fsc_slots_to_uav(action: str, obj: str, location: str) -> UAVCommand:
    key = (action, obj, location)
    if key in FSC_TO_UAV:
        c = FSC_TO_UAV[key]
        return UAVCommand(*c, confidence=0.95)

    # safe default mapping
    return UAVCommand(
        command_type="hover",
        direction="none",
        altitude_action="none",
        magnitude="small",
        urgency="low",
        safety="strict",
        confidence=0.5,
    )
