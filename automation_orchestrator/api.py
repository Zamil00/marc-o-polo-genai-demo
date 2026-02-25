from __future__ import annotations
from typing import Any, Dict, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from .config import Settings
from .orchestrator import run_workflow

app = FastAPI(title="Automation Orchestrator", version="1.0.0")

class RunRequest(BaseModel):
    payload: Dict[str, Any]
    approve: Optional[bool] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(req: RunRequest):
    settings = Settings()
    return run_workflow(req.payload, approve=req.approve, settings=settings)
