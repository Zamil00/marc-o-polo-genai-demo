from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TokenEstimate:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

def estimate_tokens(model: str, prompt: str, completion: str) -> TokenEstimate:
    try:
        import tiktoken  # type: ignore
        enc = tiktoken.encoding_for_model(model)
        pt = len(enc.encode(prompt or ""))
        ct = len(enc.encode(completion or ""))
        return TokenEstimate(prompt_tokens=pt, completion_tokens=ct, total_tokens=pt+ct)
    except Exception:
        pt = max(1, int(len(prompt or "") / 4))
        ct = max(1, int(len(completion or "") / 4))
        return TokenEstimate(prompt_tokens=pt, completion_tokens=ct, total_tokens=pt+ct)

MODEL_COST_PER_1K_TOKENS_USD = {
    "gpt-4o-mini": 0.003,
    "gpt-4o": 0.015,
}

def estimate_cost_usd(model: str, total_tokens: int) -> float:
    rate = MODEL_COST_PER_1K_TOKENS_USD.get(model, 0.01)
    return round(rate * (total_tokens / 1000.0), 6)
