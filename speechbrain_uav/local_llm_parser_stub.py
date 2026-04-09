
from typing import Dict


def parse_semantics_stub(semantics_text: str) -> Dict[str, str]:
    """
    Placeholder for local LLM / parser.
    For phase 1, keep deterministic and inspectable.
    """
    parts = semantics_text.strip().split("|")
    out = {
        "action": parts[0].strip() if len(parts) > 0 else "none",
        "object": parts[1].strip() if len(parts) > 1 else "none",
        "location": parts[2].strip() if len(parts) > 2 else "none",
        "confidence": "0.90",
    }
    return out
