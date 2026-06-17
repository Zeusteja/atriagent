import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__) + "/..")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agentforge.pipeline.orchestrator import Pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SprintRequest(BaseModel):
    title: str
    description: str


@app.get("/api/health")
def health():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    return {"status": "ok", "api_key_set": bool(key)}


@app.post("/api/chat")
def run_sprint(req: SprintRequest):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY is not set in environment variables.")

    try:
        pipeline = Pipeline(verbose=False)
        outputs = pipeline.run(title=req.title, description=req.description)
        return {
            "outputs": [
                {"role": o.role.value, "summary": o.summary, "approved": o.approved}
                for o in outputs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")
