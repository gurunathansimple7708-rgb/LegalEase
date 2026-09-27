from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from backend.schemas import DocumentRequest, ExportRequest, GeneratedDocument
from backend.services.ai_service import get_generator
from backend.services.document_service import format_docx, format_pdf, format_txt

router = APIRouter()

@router.post("/generate", response_model=GeneratedDocument)
def generate_document(request: DocumentRequest) -> GeneratedDocument:
    try:
        generator = get_generator()
        content = generator.generate_document(request.document_type, request.parties, request.terms, request.dates)
        return GeneratedDocument(document_type=request.document_type, content=content, demo_mode=generator.demo_mode)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Document generation failed: {exc}") from exc

@router.post("/export/txt")
def export_txt(request: ExportRequest):
    return Response(format_txt(request.content), media_type="text/plain; charset=utf-8",
                    headers={"Content-Disposition": 'attachment; filename="legalease_document.txt"'})

@router.post("/export/docx")
def export_docx(request: ExportRequest):
    return Response(format_docx(request.content, request.document_type, request.terms),
                    media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    headers={"Content-Disposition": 'attachment; filename="legalease_document.docx"'})

@router.post("/export/pdf")
def export_pdf(request: ExportRequest):
    return Response(format_pdf(request.content, request.document_type), media_type="application/pdf",
                    headers={"Content-Disposition": 'attachment; filename="legalease_document.pdf"'})
