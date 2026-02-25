from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Optional, Tuple, List

from guardrails import run_guardrails
from schemas.product_copy import ProductCopy

@dataclass
class EvalResult:
    score: float
    reasons: List[str]
    json_valid: bool

def _safe_json(text: str) -> Optional[dict]:
    t = (text or "").strip()
    try:
        return json.loads(t)
    except Exception:
        s = t.find("{")
        e = t.rfind("}")
        if s != -1 and e != -1 and e > s:
            try:
                return json.loads(t[s:e+1])
            except Exception:
                return None
        return None

def evaluate_product_copy(output_text: str, sustainability_provided: bool, payload: dict):
    reasons = []
    score = 0.0

    # ---------- INPUT RISK CHECK ----------
    product_name = str(payload.get("name", "")).lower()
    if "guarantee" in product_name or "100%" in product_name:
        reasons.append("Risky marketing claim detected in input product name.")
        score -= 0.05

    # ---------- SAFE JSON PARSE ----------
    parsed = _safe_json(output_text)

    if parsed is None:
        gr = run_guardrails(output_text, sustainability_provided)
        return (
            EvalResult(
                score=0.0,
                reasons=["Output is not valid JSON."] + gr.warnings,
                json_valid=False,
            ),
            "",
            gr.passed,
        )

    json_valid = False

    # ---------- SCHEMA VALIDATION ----------
    try:
        ProductCopy(**parsed)
        json_valid = True
        reasons.append("JSON schema valid.")
        score += 0.65
    except Exception as e:
        reasons.append(f"JSON schema invalid: {e}")
        score += 0.25

    # ---------- OUTPUT OVERCLAIM CHECK ----------
    t = (output_text or "").lower()
    if "guarantee" in t or "100%" in t:
        reasons.append("Potential overclaiming language in output.")
        score -= 0.10

    # ---------- GUARDRAILS ----------
    gr = run_guardrails(output_text, sustainability_provided)

    if gr.passed:
        reasons.append("Guardrails passed.")
        score += 0.25
    else:
        reasons.extend(gr.warnings)
        score -= min(0.25, 0.05 * len(gr.warnings))

    # ---------- FINAL CLAMP ----------
    score = max(0.0, min(1.0, score))

    return (
        EvalResult(score=score, reasons=reasons, json_valid=json_valid),
        json.dumps(parsed, ensure_ascii=False, indent=2),
        gr.passed,
    )