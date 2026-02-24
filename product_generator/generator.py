from __future__ import annotations
import json
from typing import Any, Dict, Optional
from openai import OpenAI
from config import Settings

class LLMJsonGenerator:
    def __init__(self, settings: Settings):
        settings.validate()
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def _safe_json_loads(self, text: str) -> Dict[str, Any]:
        text = (text or "").strip()
        try:
            return json.loads(text)
        except Exception:
            pass

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start:end+1])

        raise ValueError("Model output was not valid JSON.")

    def generate_json(self, prompt: str, max_retries: int = 2) -> Dict[str, Any]:
        last_err: Optional[Exception] = None
        for _ in range(max_retries + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=self.settings.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.settings.temperature,
                )
                content = resp.choices[0].message.content or ""
                return self._safe_json_loads(content)
            except Exception as e:
                last_err = e
        raise last_err or RuntimeError("Unknown error generating JSON.")
