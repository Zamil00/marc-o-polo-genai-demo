from __future__ import annotations
from typing import Dict, Any
from schemas import Product, CopyOutput, Lang
from prompts import build_prompt
from generator import LLMJsonGenerator

def _validate_output(d: Dict[str, Any]) -> CopyOutput:
    required = ["short_description", "seo_description", "features", "meta_title", "meta_description"]
    missing = [k for k in required if k not in d]
    if missing:
        raise ValueError(f"Missing keys in output JSON: {missing}")

    features = d["features"]
    if not isinstance(features, list) or len(features) != 5:
        raise ValueError("features must be a list of exactly 5 items")

    features = [str(x).strip() for x in features]

    return CopyOutput(
        short_description=str(d["short_description"]).strip(),
        seo_description=str(d["seo_description"]).strip(),
        features=features,
        meta_title=str(d["meta_title"]).strip(),
        meta_description=str(d["meta_description"]).strip(),
    )

def generate_copy_for_product(llm: LLMJsonGenerator, product: Product, lang: Lang) -> CopyOutput:
    prompt = build_prompt(product, lang)
    raw = llm.generate_json(prompt)
    return _validate_output(raw)
