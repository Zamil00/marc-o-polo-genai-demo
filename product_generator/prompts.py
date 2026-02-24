from __future__ import annotations
from schemas import Product, Lang

BRAND_VOICE = """You are a brand copywriter for a premium, modern fashion brand.
Brand voice:
- Minimalistic and clear
- Natural and refined
- Confident but not loud
- Sustainability-aware (when applicable)
- Avoid exaggeration and hard selling
- Keep claims factual; if uncertain, use neutral wording (e.g., "designed for", "typically").
"""

def build_prompt(product: Product, lang: Lang) -> str:
    language_instruction = "German (DE)" if lang == "DE" else "English (EN)"

    return f"""{BRAND_VOICE}

TASK:
Generate structured, SEO-ready product copy for the product below.

OUTPUT FORMAT (strict JSON, no markdown, no extra text):
{{
  \"short_description\": \"string (max 60 words)\",
  \"seo_description\": \"string (~150 words)\",
  \"features\": [\"string\", \"string\", \"string\", \"string\", \"string\"],
  \"meta_title\": \"string (max 60 characters)\",
  \"meta_description\": \"string (max 155 characters)\"
}}

RULES:
- Output must be valid JSON.
- Do not invent certifications or guarantees.
- If sustainability info is empty, do not force sustainability claims.
- Features must be concrete (material, fit, feel, usage, care hints).
- Use a premium tone, but stay concise.
- Language: {language_instruction}.

PRODUCT DATA:
Name: {product.name}
Material: {product.material}
Fit: {product.fit}
Color: {product.color}
Sustainability: {product.sustainability or "N/A"}
Additional details: {product.additional_details or "N/A"}
"""
