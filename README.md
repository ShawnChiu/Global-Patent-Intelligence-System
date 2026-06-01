# Global Patent Intelligence System

React + FastAPI patent intelligence analysis system for GPSS patent search, matrix analysis, interactive charts, and PDF report generation.

## Features

- GPSS login and search automation with Playwright.
- Automatic captcha recognition with `ddddocr`.
- Rule-based or LLM-assisted Boolean query and matrix keyword generation.
- Interactive dark-mode React UI built with Vite and Tailwind.
- Plotly chart rendering for IPC, assignee, country, trend, and technology-effect matrix views.
- PDF report generation with ReportLab, including chart redraws, source data tables, and written analysis.
- Local settings persisted under `.data/user_settings.json`.

## Tech Stack

- Frontend: React, Vite, Tailwind, Plotly.js
- Backend: FastAPI, Uvicorn
- Automation: Playwright
- Data processing: Pandas, OpenPyXL, lxml
- OCR: ddddocr
- AI: Google Gemini API or OpenAI-compatible chat completions API
- Reports: ReportLab
- Python dependency management: uv

## LLM Configuration

The AI modes are provider/model configurable.

- `gemini`: uses Google Gemini API through `google-generativeai`.
- `openai-compatible`: uses a `/v1/chat/completions` compatible API with the Python standard library, so it can work with OpenAI, OpenRouter, Groq, vLLM, or Ollama-compatible endpoints.

The frontend exposes:

- Provider
- Model name
- Base URL for OpenAI-compatible providers
- API key

The default model remains `gemini-2.5-flash`, but it is no longer hard-coded in the analysis flow.

## Setup

```powershell
uv sync
uv run playwright install chromium
cd frontend
npm install
```

## Development

From the project root:

```powershell
.\.uv-venv\Scripts\python.exe run_react.py
```

Then open:

```text
http://127.0.0.1:5173
```

The development launcher starts:

- FastAPI backend on `http://127.0.0.1:8000`
- Vite frontend on `http://127.0.0.1:5173`

## Production-Like Local Run

Build the frontend:

```powershell
cd frontend
npm run build
cd ..
.\.uv-venv\Scripts\python.exe -m uvicorn fast_app:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

## Project Structure

```text
.
├── fast_app.py                 # FastAPI API and React static serving
├── run_react.py                # Development launcher
├── config.py                   # Defaults and example topics
├── pyproject.toml              # Python dependencies
├── uv.lock                     # Locked Python dependency graph
├── frontend/
│   ├── src/main.jsx            # React application
│   ├── src/styles.css          # Tailwind styles
│   └── package.json            # Frontend dependencies
├── models/
│   ├── gemini_client.py        # Patent LLM prompt workflow compatibility layer
│   ├── llm_client.py           # Gemini and OpenAI-compatible LLM clients
│   └── gpss_client.py          # GPSS browser automation
└── services/
    ├── analysis_runner.py      # Main analysis workflow
    ├── captcha.py              # Captcha OCR
    ├── chart_data.py           # Plotly chart data extraction
    ├── gen_report.py           # PDF report generation
    ├── parser.py               # GPSS table parsing and Plotly figure creation
    └── settings_manager.py     # User settings persistence
```

## Notes

- Do not commit `.data/`; it may contain local GPSS credentials and API keys.
- `frontend/dist/`, `frontend/node_modules/`, `.uv-venv/`, `.uv-cache/`, and generated output folders are ignored.
- The PDF report redraws charts from Plotly data directly, so it does not depend on Kaleido or Word/Docx image export.
