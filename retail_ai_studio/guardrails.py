from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List

BANNED_CLAIMS_PATTERNS = [
    r"\b100%\s+guarantee\b",
    r"\bclinically\s+proven\b",
    r"\bguaranteed\b",
    r"\bcertified\b(?!\s+organic\b)",
]

SUSTAINABILITY_HALLUCINATION = [
    r"\bGOTS\b",
    r"\bFair\s*Trade\b",
    r"\bOEKO[-\s]?TEX\b",
    r"\bbluesign\b",
]

@dataclass
class GuardrailResult:
    passed: bool
    warnings: List[str]

def run_guardrails(text: str, sustainability_provided: bool) -> GuardrailResult:
    warnings: List[str] = []
    t = text or ""

    for pat in BANNED_CLAIMS_PATTERNS:
        if re.search(pat, t, flags=re.IGNORECASE):
            warnings.append(f"Banned/unsafe claim pattern detected: {pat}")

    if not sustainability_provided:
        for pat in SUSTAINABILITY_HALLUCINATION:
            if re.search(pat, t, flags=re.IGNORECASE):
                warnings.append("Possible sustainability certification hallucination (not provided in input).")

    return GuardrailResult(passed=len(warnings) == 0, warnings=warnings)
