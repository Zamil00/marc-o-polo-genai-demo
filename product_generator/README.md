# Product Description Generator (LLM)

A structured prompt + workflow that generates **brand-consistent, SEO-ready** product copy in **DE/EN** from a small product JSON input.

## What it generates
For each product (per language):
- Short description (≤ 60 words)
- SEO description (~150 words)
- 5 feature bullets
- Meta title (≤ 60 chars)
- Meta description (≤ 155 chars)

## Run locally
From repo root:

```bash
pip install -r requirements.txt
python product_generator/cli.py --input product_generator/sample_products.json --lang DE
python product_generator/cli.py --input product_generator/sample_products.json --lang EN
```

## Notes
- Requires `OPENAI_API_KEY` in a root `.env` file (same as the RAG project).
- Outputs are written to `product_generator/out/` as JSON.
