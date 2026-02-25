from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .config import Settings
from .governance import evaluate_payload
from .cost_tracker import estimate_tokens, estimate_cost_usd
from .llm_services import generate_copy, generate_visual_prompt
from .integrations.notion_client import create_notion_draft
from .integrations.slack_client import send_slack_webhook
from .logger_db import log_run

def run_workflow(payload: Dict[str, Any], approve: Optional[bool], settings: Settings) -> Dict[str, Any]:
    settings.validate()
    run_id = str(uuid.uuid4())[:8]
    ts = datetime.now(timezone.utc).isoformat()

    gov = evaluate_payload(payload)
    approval = "PENDING" if approve is None else ("APPROVED" if approve else "REJECTED")

    copy_prompt, copy_out = generate_copy(payload, model=settings.model_copy, temperature=settings.temperature)
    visual_in, visual_out = generate_visual_prompt(payload, model=settings.model_visual_prompt, temperature=settings.temperature)

    tok = estimate_tokens(settings.model_copy, copy_prompt, copy_out)
    est_cost = estimate_cost_usd(settings.model_copy, tok.total_tokens)

    requires_manual_review = gov.score < settings.governance_threshold

    notion_page_id = None
    slack_ts = None

    if not settings.dry_run:
        # Notion draft
        try:
            md = f"""Run: {run_id}
Governance score: {gov.score:.2f}

### Copy (raw JSON)
{copy_out}

### Visual prompt
{visual_out}
"""
            notion_page_id = create_notion_draft(
                token=settings.notion_token,
                parent_page_id=settings.notion_parent_page_id,
                title=f"[AI Draft] {payload.get('name','Product')}",
                properties={},
                content_markdown=md,
            )
        except Exception:
            notion_page_id = None

        # Slack notify
        try:
            msg = (
                f"🧠 *AI Draft Ready* (run {run_id})\n"
                f"- Governance score: {gov.score:.2f}{' ⚠️ manual review required' if requires_manual_review else ''}\n"
                f"- Approval: {approval}\n"
                f"- Notion draft: {notion_page_id or 'N/A'}"
            )
            slack_ts = send_slack_webhook(settings.slack_webhook_url, msg)
        except Exception:
            slack_ts = None

    # Final status
    if requires_manual_review:
        status = "MANUAL_REVIEW_REQUIRED"
    else:
        if approve is True:
            status = "PUBLISHED"
        elif approve is False:
            status = "REJECTED"
        else:
            status = "AWAITING_APPROVAL"

    outputs = {
        "copy_json_raw": copy_out,
        "visual_prompt": visual_out,
        "notion_page_id": notion_page_id,
    }

    log_run({
        "ts": ts,
        "run_id": run_id,
        "status": status,
        "approval": approval,
        "governance_score": gov.score,
        "governance_warnings": "; ".join(gov.warnings),
        "model_copy": settings.model_copy,
        "model_visual": settings.model_visual_prompt,
        "prompt_tokens": tok.prompt_tokens,
        "completion_tokens": tok.completion_tokens,
        "total_tokens": tok.total_tokens,
        "est_cost_usd": est_cost,
        "notion_page_id": notion_page_id,
        "slack_message_ts": slack_ts,
        "payload": payload,
        "outputs": outputs,
    })

    return {
        "run_id": run_id,
        "status": status,
        "approval": approval,
        "governance": {"score": gov.score, "warnings": gov.warnings},
        "cost_estimate": {"total_tokens": tok.total_tokens, "est_cost_usd": est_cost},
        "outputs": outputs,
        "dry_run": settings.dry_run,
    }
