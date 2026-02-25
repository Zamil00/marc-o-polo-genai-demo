from __future__ import annotations
import os
import json
from typing import Any, Dict, Tuple
from openai import OpenAI

COPY_SCHEMA_HINT = {
  "short_description": "string (<= 60 words)",
  "seo_description": "string (~150 words)",
  "features": ["string","string","string","string","string"],
  "meta_title": "string (<= 60 chars)",
  "meta_description": "string (<= 155 chars)"
}

def generate_copy(payload: Dict[str, Any], model: str, temperature: float) -> Tuple[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user = (
        "Generate premium fashion product copy as STRICT JSON only (no markdown).\n\n"
        f"JSON schema: {json.dumps(COPY_SCHEMA_HINT)}\n\n"
        "Rules: avoid unverifiable claims, avoid certifications not provided, keep brand tone minimal and premium.\n\n"
        "Input product JSON:\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "You are a premium fashion brand copywriter. Output valid JSON only."},
            {"role": "user", "content": user},
        ],
    )
    return user, (resp.choices[0].message.content or "").strip()

def generate_visual_prompt(payload: Dict[str, Any], model: str, temperature: float) -> Tuple[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user = (
        "Create ONE safe text-to-image prompt for a premium fashion e-commerce product photo.\n"
        "Constraints: photorealistic, clean background, natural lighting, minimal style.\n"
        "Do not mention certifications unless explicitly present. Avoid any guarantee language.\n\n"
        "Input product JSON:\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "You produce safe, concise visual prompts for fashion retail."},
            {"role": "user", "content": user},
        ],
    )
    return user, (resp.choices[0].message.content or "").strip()
