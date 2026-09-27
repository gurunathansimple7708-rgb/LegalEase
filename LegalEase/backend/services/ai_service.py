from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.config import get_settings

def get_generator() -> GeminiDocumentGenerator:
    settings = get_settings()
    return GeminiDocumentGenerator(api_key=settings.gemini_api_key, model=settings.gemini_model)
