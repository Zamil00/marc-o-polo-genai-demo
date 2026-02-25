from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

from registry import load_prompt, render_user
from llm_client import LLMClient
from eval_engine import evaluate_product_copy
from cost import estimate_tokens

@dataclass
class Candidate:
    prompt_version: str
    model: str
    output_text: str
    score: float
    reasons: List[str]
    tokens: dict

def run_agent_product_copy(
    llm: LLMClient,
    payload: Dict[str, Any],
    prompt_versions: List[str],
    models: List[str],
    temperature: float,
) -> Tuple[Candidate, List[Candidate]]:
    candidates: List[Candidate] = []
    sustainability_provided = bool(str(payload.get("sustainability", "")).strip())

    for v in prompt_versions:
        p = load_prompt(task="product_copy", version=v)
        user = render_user(p.user_template, payload)
        for model in models:
            out = llm.chat(system=p.system, user=user, model=model, temperature=temperature)
            ev, _, _ = evaluate_product_copy(
            out,
            sustainability_provided=sustainability_provided,
            payload=payload)
            tok = estimate_tokens(model, user, out).__dict__
            candidates.append(Candidate(
                prompt_version=v,
                model=model,
                output_text=out,
                score=ev.score,
                reasons=ev.reasons,
                tokens=tok,
            ))

    best = sorted(candidates, key=lambda c: c.score, reverse=True)[0]
    return best, candidates
