from __future__ import annotations
import os
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")

SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  task TEXT NOT NULL,
  model TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  temperature REAL NOT NULL,
  input_json TEXT,
  prompt_text TEXT NOT NULL,
  output_text TEXT NOT NULL,
  score REAL NOT NULL,
  guardrail_passed INTEGER NOT NULL,
  guardrail_warnings TEXT,
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  total_tokens INTEGER
);
'''

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.execute(SCHEMA_SQL)
    c.commit()
    return c

def log_run(
    task: str,
    model: str,
    prompt_version: str,
    temperature: float,
    input_json: Optional[str],
    prompt_text: str,
    output_text: str,
    score: float,
    guardrail_passed: bool,
    guardrail_warnings: str,
    tokens: Optional[Dict[str, Any]] = None,
) -> None:
    ts = datetime.utcnow().isoformat()
    t = tokens or {}
    with _conn() as c:
        c.execute(
            '''
            INSERT INTO runs (ts, task, model, prompt_version, temperature, input_json, prompt_text, output_text, score,
                             guardrail_passed, guardrail_warnings, prompt_tokens, completion_tokens, total_tokens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                ts, task, model, prompt_version, temperature, input_json, prompt_text, output_text, float(score),
                1 if guardrail_passed else 0, guardrail_warnings,
                t.get("prompt_tokens"), t.get("completion_tokens"), t.get("total_tokens"),
            )
        )
        c.commit()
