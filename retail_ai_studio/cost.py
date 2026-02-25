from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CostEstimate:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

def estimate_tokens(model: str, prompt: str, completion: str) -> CostEstimate:
    try:
        import tiktoken  # type: ignore
        enc = tiktoken.encoding_for_model(model)
        pt = len(enc.encode(prompt or ""))
        ct = len(enc.encode(completion or ""))
        return CostEstimate(prompt_tokens=pt, completion_tokens=ct, total_tokens=pt+ct)
    except Exception:
        pt = max(1, int(len(prompt or "") / 4))
        ct = max(1, int(len(completion or "") / 4))
        return CostEstimate(prompt_tokens=pt, completion_tokens=ct, total_tokens=pt+ct)
