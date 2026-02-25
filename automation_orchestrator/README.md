# Module 6 — Enterprise Automation Orchestrator (FastAPI + CLI)

A production-style simulation of a **GenAI automation workflow** for retail product operations.

## What it does
Given a product JSON, the orchestrator:
1) Generates structured product copy (JSON)
2) Generates a visual prompt for marketing/design
3) Runs governance checks (risk scoring)
4) Produces token & cost estimates
5) Creates a Notion draft (optional)
6) Sends a Slack notification (optional)
7) Applies approval gates (approve/reject/pending)
8) Logs each run to SQLite (`automation_orchestrator/db/runs.sqlite`)

## Run (CLI)
From repo root:

```bash
pip install -r automation_orchestrator/requirements_extra.txt
python3 automation_orchestrator/cli.py --input automation_orchestrator/sample_product.json --approve pending --dry-run
```

## Run (API)
From repo root:

```bash
pip install -r automation_orchestrator/requirements_extra.txt
uvicorn automation_orchestrator.api:app --reload --port 8010
```

Then:
- GET `http://localhost:8010/health`
- POST `http://localhost:8010/run` with body:
```json
{
  "payload": { "name": "..." },
  "approve": true
}
```

## Integrations (optional)
Set these in repo root `.env` to enable real integrations:
- `NOTION_TOKEN`
- `NOTION_PARENT_PAGE_ID`
- `SLACK_WEBHOOK_URL`

Force dry-run mode:
- set `DRY_RUN=1` in `.env`
- or pass `--dry-run` in CLI

## Governance behavior
If governance score < `GOVERNANCE_THRESHOLD` (default 0.85), status becomes:
- `MANUAL_REVIEW_REQUIRED`
and it will not auto-publish even if `approve=true`.
