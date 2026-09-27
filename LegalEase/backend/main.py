from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from backend.routes import router

settings = get_settings()
app = FastAPI(title="LegalEase API", version="1.0.0",
              description="AI-assisted legal document generation and export API.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "LegalEase API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)
