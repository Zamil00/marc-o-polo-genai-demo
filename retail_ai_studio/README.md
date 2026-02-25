# Retail AI Studio — GenAI Experimentation & Optimization Platform

A mini internal **GenAI enablement platform** for retail teams.
It demonstrates how to operationalize GenAI with:
- **Prompt versioning** (Prompt Registry)
- **Evaluation** (schema/format checks + quality heuristics)
- **Guardrails** (banned claims, safety checks)
- **Cost tracking** (token estimation + logging)
- **Agent Mode** (auto-select best output across prompt versions / models)

## Quickstart
From repo root:

```bash
pip install -r requirements.txt
pip install -r retail_ai_studio/requirements_extra.txt
streamlit run retail_ai_studio/app.py
```

## Environment
Create a `.env` in repo root:

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

## What to demo (10 minutes)
1. Open the Streamlit UI
2. Choose **Task: Product Copy (JSON)**
3. Run **Prompt v1 vs v2** (Agent Mode)
4. Show evaluation score + guardrail warnings + cost estimate
5. Open `retail_ai_studio/data/logs.db` (logged runs)
