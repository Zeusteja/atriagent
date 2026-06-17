import os
import sys

sys.path.insert(0, os.path.dirname(__file__) + "/..")

from fastapi import FastAPI
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
    return {"status": "ok"}


@app.post("/api/chat")
def run_sprint(req: SprintRequest):
    pipeline = Pipeline(verbose=False)
    outputs = pipeline.run(title=req.title, description=req.description)
    return {
        "outputs": [
            {"role": o.role.value, "summary": o.summary, "approved": o.approved}
            for o in outputs
        ]
    }
