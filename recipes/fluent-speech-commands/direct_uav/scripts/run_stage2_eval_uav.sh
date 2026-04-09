#!/usr/bin/env bash
set -e
python - <<'PY'
from speechbrain_uav.uav_mapping import map_fsc_slots_to_uav
from speechbrain_uav.ha_normalizer import normalize_with_ha
from speechbrain_uav.semantic_packet import SemanticPacket
from speechbrain_uav.uav_validator import validate_and_correct

cmd = map_fsc_slots_to_uav("activate", "lights", "kitchen")
norm = normalize_with_ha(cmd)
pkt = SemanticPacket(
    command_type=norm["command_type"],
    direction=norm["direction"],
    altitude_action=norm["altitude_action"],
    magnitude_rank=norm["magnitude_rank"],
    urgency_rank=norm["urgency_rank"],
    safety_rank=norm["safety_rank"],
    confidence=norm["confidence"],
)
print("TOKENS:", pkt.to_token_sequence())
print("SERIALIZED:", pkt.serialize())
print("VALIDATED:", validate_and_correct({
    "command_type": pkt.command_type,
    "direction": pkt.direction,
    "altitude_action": pkt.altitude_action,
    "magnitude_rank": pkt.magnitude_rank,
    "urgency_rank": pkt.urgency_rank,
    "safety_rank": pkt.safety_rank,
    "confidence": pkt.confidence,
}))
PY
