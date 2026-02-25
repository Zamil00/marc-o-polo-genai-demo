from __future__ import annotations
from openai import OpenAI
from config import Settings

class LLMClient:
    def __init__(self, settings: Settings):
        settings.validate()
        self.settings = settings
        self.client = OpenAI(api_key=settings.api_key)

    def chat(self, system: str, user: str, model: str | None = None, temperature: float | None = None) -> str:
        m = model or self.settings.default_model
        t = temperature if temperature is not None else self.settings.temperature
        resp = self.client.chat.completions.create(
            model=m,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=t,
        )
        return (resp.choices[0].message.content or "").strip()
