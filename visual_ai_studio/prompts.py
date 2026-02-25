from __future__ import annotations
import json
from typing import Dict

PROMPT_V1 = """You are a fashion retail visual prompt engineer.
Create ONE concise text-to-image prompt for a studio product photo.

Requirements:
- clean e-commerce studio background
- premium, minimal, brand-safe
- no brand logos unless explicitly present in the product JSON
- do not claim certifications not given

Output only the final prompt as plain text.

Product JSON:
{product_json}
"""

PROMPT_V2 = """You are a senior art director for premium fashion e-commerce.
Create ONE text-to-image prompt for a hero product shot that is:
- photorealistic, natural lighting, premium feel
- clean studio background, subtle shadow
- consistent with the brand style in JSON
- avoid any medical/guarantee/certification claims

Output only the final prompt as plain text.

Product JSON:
{product_json}
"""

def render_prompt(template: str, product: Dict) -> str:
    return template.format(product_json=json.dumps(product, ensure_ascii=False, indent=2))
