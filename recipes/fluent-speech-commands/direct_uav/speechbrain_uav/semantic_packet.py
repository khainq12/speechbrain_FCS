
import json
from dataclasses import dataclass, asdict


@dataclass
class SemanticPacket:
    command_type: str
    direction: str
    altitude_action: str
    magnitude_rank: int
    urgency_rank: int
    safety_rank: int
    confidence: float

    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def deserialize(cls, s: str):
        return cls(**json.loads(s))

    def to_token_sequence(self):
        return [
            self.command_type,
            self.direction,
            self.altitude_action,
            f"MAG_{self.magnitude_rank}",
            f"URG_{self.urgency_rank}",
            f"SAFE_{self.safety_rank}",
        ]
