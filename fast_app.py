import base64
import json
import threading
import time
import uuid
from pathlib import Path

import plotly.io as pio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from config import EXAMPLE_CONFIG
from services.analysis_runner import AnalysisInputs, run_patent_analysis
from services.settings_manager import setmgr


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app = FastAPI(title="Global Patent Intelligence System")
if (FRONTEND_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

jobs = {}
jobs_lock = threading.Lock()


class AnalyzeRequest(BaseModel):
    topic_select: str = "自訂"
    topic: str = ""
    gpss_id: str = ""
    gpss_pw: str = ""
    gemini_api_key: str = ""
    llm_provider: str = "gemini"
    llm_model: str = "gemini-2.5-flash"
    llm_base_url: str = "https://api.openai.com/v1"
    login_mode: str = "自動辨識驗證碼"
    search_mode: str = "搜尋布林檢索式"
    matrix_mode: str = "關鍵字規則 (Rule-based)"
    query: str = ""
    source: str = ""
    conf_source: str = ""
    matrix: dict = Field(default_factory=dict)


def _default_state():
    return {
        "topic": "",
        "gpss_id": setmgr.settings.gpss_id,
        "gpss_pw": setmgr.settings.gpss_pw,
        "gemini_api_key": setmgr.settings.gemini_api_key,
        "llm_provider": setmgr.settings.llm_provider,
        "llm_model": setmgr.settings.llm_model,
        "llm_base_url": setmgr.settings.llm_base_url,
        "login_mode": "自動辨識驗證碼",
        "search_mode": "搜尋布林檢索式",
        "matrix_mode": "關鍵字規則 (Rule-based)",
        "query": setmgr.settings.query,
        "source": "",
        "conf_source": "",
        "matrix": setmgr.settings.matrix,
    }


def _figure_payload(figures):
    payload = {}
    for key, fig in figures.items():
        payload[key] = json.loads(pio.to_json(fig))
    return payload


def _binary_payload(buffer):
    if hasattr(buffer, "seek"):
        buffer.seek(0)
    data = buffer.read() if hasattr(buffer, "read") else bytes(buffer)
    return base64.b64encode(data).decode("ascii")


def _run_job(job_id, request: AnalyzeRequest):
    def progress(level, message):
        with jobs_lock:
            job = jobs[job_id]
            job["messages"].append(
                {
                    "level": level,
                    "message": message,
                    "time": time.strftime("%H:%M:%S"),
                }
            )

    try:
        with jobs_lock:
            jobs[job_id]["status"] = "running"

        inputs = AnalysisInputs(**request.model_dump())
        result = run_patent_analysis(inputs, progress)
        payload = {
            "query": result["query"],
            "matrix": result["matrix"],
            "figures": _figure_payload(result["fig"]),
            "pdf": _binary_payload(result["pdf"]),
            "search_result": result["search_result"],
        }

        with jobs_lock:
            jobs[job_id]["status"] = "done"
            jobs[job_id]["result"] = payload
    except Exception as e:
        progress("error", str(e))
        with jobs_lock:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = str(e)


@app.get("/", response_class=HTMLResponse)
def index():
    if (FRONTEND_DIST / "index.html").exists():
        return (FRONTEND_DIST / "index.html").read_text(encoding="utf-8")
    return "<p>React frontend is not built. Run <code>cd frontend && npm run dev</code>.</p>"


@app.get("/plotly.js")
def plotly_js():
    return Response(content=pio.get_plotlyjs(), media_type="application/javascript")


@app.get("/api/bootstrap")
def bootstrap():
    return {
        "defaults": _default_state(),
        "examples": list(EXAMPLE_CONFIG.keys()),
        "example_config": EXAMPLE_CONFIG,
    }


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    job_id = uuid.uuid4().hex
    with jobs_lock:
        jobs[job_id] = {
            "status": "queued",
            "messages": [],
            "result": None,
            "error": None,
        }

    thread = threading.Thread(target=_run_job, args=(job_id, request), daemon=True)
    thread.start()
    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job


@app.get("/{full_path:path}", response_class=HTMLResponse)
def frontend_fallback(full_path: str):
    if (FRONTEND_DIST / "index.html").exists():
        return (FRONTEND_DIST / "index.html").read_text(encoding="utf-8")
    raise HTTPException(status_code=404, detail="Not found")
