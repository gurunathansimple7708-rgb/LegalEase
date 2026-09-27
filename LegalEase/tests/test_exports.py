from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)

payload = {
    "document_type": "General Agreement",
    "content": "# General Agreement\n\n## 1. Parties\nJane Doe and Example Corp.\n\n1. Payment within 30 days.",
    "terms": "Payment within 30 days; Confidentiality applies",
}

def test_txt_export():
    r = client.post("/export/txt", json=payload)
    assert r.status_code == 200
    assert r.content.startswith(b"# General Agreement")

def test_docx_export():
    r = client.post("/export/docx", json=payload)
    assert r.status_code == 200
    assert r.content[:2] == b"PK"

def test_pdf_export():
    r = client.post("/export/pdf", json=payload)
    assert r.status_code == 200
    assert r.content.startswith(b"%PDF")
