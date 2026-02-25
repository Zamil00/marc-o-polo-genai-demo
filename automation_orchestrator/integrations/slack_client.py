from __future__ import annotations
import requests
from typing import Optional

def send_slack_webhook(webhook_url: str, text: str) -> Optional[str]:
    if not webhook_url:
        return None
    payload = {"text": text}
    r = requests.post(webhook_url, json=payload, timeout=30)
    r.raise_for_status()
    return None
