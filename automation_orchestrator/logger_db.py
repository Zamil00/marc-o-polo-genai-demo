from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict

DB_PATH = Path(__file__).parent / "db" / "runs.sqlite"

def log_run(row: Dict[str, Any]) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO runs (
          ts, run_id, status, approval, governance_score, governance_warnings,
          model_copy, model_visual, prompt_tokens, completion_tokens, total_tokens, est_cost_usd,
          notion_page_id, slack_message_ts, payload_json, outputs_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["ts"],
            row["run_id"],
            row["status"],
            row["approval"],
            float(row["governance_score"]),
            row.get("governance_warnings",""),
            row.get("model_copy",""),
            row.get("model_visual",""),
            row.get("prompt_tokens"),
            row.get("completion_tokens"),
            row.get("total_tokens"),
            row.get("est_cost_usd"),
            row.get("notion_page_id"),
            row.get("slack_message_ts"),
            json.dumps(row.get("payload",{}), ensure_ascii=False),
            json.dumps(row.get("outputs",{}), ensure_ascii=False),
        ),
    )
    conn.commit()
    conn.close()
