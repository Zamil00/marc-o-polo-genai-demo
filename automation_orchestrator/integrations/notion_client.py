from __future__ import annotations
import requests
from typing import Any, Dict, Optional

NOTION_API = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

def create_notion_draft(
    token: str,
    parent_page_id: str,
    title: str,
    properties: Dict[str, Any],
    content_markdown: str,
) -> Optional[str]:
    if not token or not parent_page_id:
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]},
            **properties,
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content_markdown[:1900]}}]
                },
            },
        ],
    }

    r = requests.post(NOTION_API, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data.get("id")
