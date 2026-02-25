from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_copy: str = os.getenv("OPENAI_MODEL_COPY", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    model_visual_prompt: str = os.getenv("OPENAI_MODEL_VISUAL_PROMPT", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

    # Integrations (optional)
    notion_token: str = os.getenv("NOTION_TOKEN", "")
    notion_parent_page_id: str = os.getenv("NOTION_PARENT_PAGE_ID", "")
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")

    # Behavior
    dry_run: bool = os.getenv("DRY_RUN", "0") in ("1", "true", "True", "yes", "YES")
    governance_threshold: float = float(os.getenv("GOVERNANCE_THRESHOLD", "0.85"))

    def validate(self) -> None:
        if not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to repo root .env")
