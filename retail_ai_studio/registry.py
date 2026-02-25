from __future__ import annotations
import os
import json
from dataclasses import dataclass
from typing import Dict, Any, List

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")

@dataclass(frozen=True)
class PromptTemplate:
    version: str
    task: str
    system: str
    user_template: str

def list_prompts(task: str) -> List[str]:
    versions: List[str] = []
    for fn in os.listdir(PROMPT_DIR):
        if fn.startswith(f"{task}__") and fn.endswith(".json"):
            versions.append(fn.split("__", 1)[1].replace(".json", ""))
    return sorted(versions)

def load_prompt(task: str, version: str) -> PromptTemplate:
    path = os.path.join(PROMPT_DIR, f"{task}__{version}.json")
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    return PromptTemplate(
        version=d["version"],
        task=d["task"],
        system=d["system"],
        user_template=d["user_template"],
    )

def render_user(template: str, payload: Dict[str, Any]) -> str:
    text = template
    for k, v in payload.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text
