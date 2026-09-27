# LegalEase

Complete Streamlit + FastAPI + Gemini legal-document drafting application.

## Features

- AI-assisted document generation
- Employment contracts, NDAs, leases, service agreements and custom documents
- Editable preview
- TXT, DOCX and PDF export
- Terms table in DOCX
- API validation with Pydantic
- CORS configuration
- Health endpoint and automatic FastAPI docs
- Deterministic demo mode when no Gemini key is configured
- Automated tests

## VS Code setup

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Put your Gemini API key in `.env`. You can leave it blank for demo mode.

## Run

Terminal 1:
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:
```bash
streamlit run app.py
```

Backend: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs  
Frontend: http://localhost:8501

## Test

```bash
pytest -q
```

## Notes

The original project specification selected Gemini 1.5 Pro. That model is no longer available, so this implementation uses a configurable current Gemini model via `GEMINI_MODEL`. The API key remains backend-only.

LegalEase is an AI drafting aid, not a substitute for qualified legal review.
