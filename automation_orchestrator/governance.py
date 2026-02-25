from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List

RISKY_TERMS = [
    "100% guaranteed", "guarantee", "guaranteed", "clinically proven", "cure", "medical",
    "certified", "officially certified", "gots", "oeko-tex", "fair trade", "bluesign"
]

@dataclass
class GovernanceResult:
    score: float
    warnings: List[str]

def evaluate_payload(payload: Dict[str, Any]) -> GovernanceResult:
    score = 1.0
    warnings: List[str] = []

    name = str(payload.get("name", "")).lower()
    sustainability = str(payload.get("sustainability", "")).lower()

    for term in RISKY_TERMS:
        if term in name:
            score -= 0.10
            warnings.append(f"Risky marketing claim in product name: '{term}'")

    if not sustainability.strip():
        score -= 0.05
        warnings.append("Sustainability missing/empty → enforce no certification claims.")

    if not sustainability.strip():
        for cert in ["gots", "oeko-tex", "fair trade", "bluesign"]:
            if cert in name:
                score -= 0.10
                warnings.append("Certification-like term appears but sustainability field is empty.")

    score = max(0.0, min(1.0, score))
    return GovernanceResult(score=score, warnings=warnings)
