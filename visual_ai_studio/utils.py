from __future__ import annotations

import base64
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class ImageGenResult:
    prompt: str
    image_paths: List[Path]
    raw_response: Dict[str, Any]
    score: float
    reasons: List[str]

def risk_score_input(product: Dict[str, Any]) -> Tuple[float, List[str]]:
    """Simple governance scoring for risky marketing claims in product input."""
    score = 1.0
    reasons: List[str] = []

    name = str(product.get("name", "")).lower()
    sustainability = str(product.get("sustainability", product.get("brand_style", ""))).lower()

    risky_terms = ["guarantee", "guaranteed", "100% guaranteed", "cure", "medical", "certified", "officially certified"]
    for t in risky_terms:
        if t in name:
            score -= 0.10
            reasons.append(f"Risky claim detected in product name: '{t}'")

    if not sustainability.strip():
        score -= 0.05
        reasons.append("Sustainability field missing/empty: avoid overclaiming in output.")

    return max(0.0, score), reasons

def generate_visual_prompt(prompt_text: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You produce safe, concise image-generation prompts for fashion e-commerce."},
            {"role": "user", "content": prompt_text},
        ],
    )
    return (resp.choices[0].message.content or "").strip()

def call_images_api(prompt: str, *, model: str = "gpt-image-1.5", n: int = 1, size: str = "1024x1024", quality: str = "auto") -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file in repo root.")

    url = "https://api.openai.com/v1/images/generations"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"model": model, "prompt": prompt, "n": int(n), "size": size, "quality": quality}

    r = requests.post(url, headers=headers, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()

def save_b64_images(resp: Dict[str, Any], out_dir: Path, prefix: str) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    for i, item in enumerate(resp.get("data", []) or []):
        b64 = item.get("b64_json")
        if not b64:
            continue
        img_bytes = base64.b64decode(b64)
        p = out_dir / f"{prefix}_{i}.png"
        p.write_bytes(img_bytes)
        paths.append(p)

    (out_dir / f"{prefix}_meta.json").write_text(json.dumps(resp, indent=2), encoding="utf-8")
    return paths

def run_image_generation(
    product: Dict[str, Any],
    prompt_version: str,
    rendered_prompt: str,
    *,
    llm_model: str = "gpt-4o-mini",
    image_model: str = "gpt-image-1.5",
    n: int = 1,
    size: str = "1024x1024",
    quality: str = "auto",
    out_dir: Path,
) -> ImageGenResult:
    score, reasons = risk_score_input(product)

    visual_prompt = generate_visual_prompt(rendered_prompt, model=llm_model)

    if score < 0.9:
        visual_prompt = visual_prompt + " | Avoid any guarantee/certification claims. Keep it purely visual and factual."

    raw = call_images_api(visual_prompt, model=image_model, n=n, size=size, quality=quality)

    prefix = f"{int(time.time())}_{prompt_version}"
    img_paths = save_b64_images(raw, out_dir, prefix)

    return ImageGenResult(prompt=visual_prompt, image_paths=img_paths, raw_response=raw, score=score, reasons=reasons)
