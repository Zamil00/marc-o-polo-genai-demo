# Module 5 — Visual AI Studio (Product Image Prompting + Generation)

A lightweight Streamlit app to demonstrate **Text-to-Image** use cases in fashion retail.

## What it does
- Takes a **product JSON** as input
- Generates **brand-safe visual prompts** (Prompt v1 / v2)
- Calls the OpenAI **Images API** to generate product visuals
- Saves outputs to `visual_ai_studio/out/` and displays them in the UI

## Run
From repo root:

```bash
pip install -r visual_ai_studio/requirements_extra.txt
streamlit run visual_ai_studio/app.py
```

## Notes
- Requires `OPENAI_API_KEY` in your repo root `.env`
- Default image model: `gpt-image-1.5`
