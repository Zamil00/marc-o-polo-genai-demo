from __future__ import annotations
import argparse
import json
import os
from typing import List, Dict, Any
from config import Settings
from schemas import Product, Lang
from generator import LLMJsonGenerator
from pipeline import generate_copy_for_product

def load_products(path: str) -> List[Product]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of products")
    return [Product.from_dict(item) for item in data]

def main():
    parser = argparse.ArgumentParser(description="Generate product descriptions with an LLM (DE/EN).")
    parser.add_argument("--input", required=True, help="Path to JSON file with product list")
    parser.add_argument("--lang", required=True, choices=["DE", "EN"], help="Output language")
    args = parser.parse_args()

    settings = Settings()
    llm = LLMJsonGenerator(settings)

    products = load_products(args.input)
    lang: Lang = args.lang  # type: ignore

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)

    results: List[Dict[str, Any]] = []
    for p in products:
        copy = generate_copy_for_product(llm, p, lang)
        results.append({"product": p.__dict__, "lang": lang, "copy": copy.to_dict()})

    out_path = os.path.join(out_dir, f"generated_copy_{lang}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Done. Wrote: {out_path}")

if __name__ == "__main__":
    main()
