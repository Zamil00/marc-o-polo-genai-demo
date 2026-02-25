from __future__ import annotations
import argparse
import json
from pathlib import Path
from .config import Settings
from .orchestrator import run_workflow

def main():
    p = argparse.ArgumentParser(description="Module 6 — Enterprise Automation Orchestrator (CLI)")
    p.add_argument("--input", required=True, help="Path to product JSON")
    p.add_argument("--approve", choices=["yes","no","pending"], default="pending", help="Approval simulation")
    p.add_argument("--dry-run", action="store_true", help="Disable Notion/Slack calls even if env vars exist")
    args = p.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    approve = None if args.approve == "pending" else (args.approve == "yes")

    settings = Settings()
    if args.dry_run:
        object.__setattr__(settings, "dry_run", True)  # type: ignore

    result = run_workflow(payload, approve=approve, settings=settings)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
