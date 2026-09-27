from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)

def test_demo_generation():
    payload = {
        "document_type": "Freelance Work Contract",
        "parties": "Jane Doe (Freelancer), Example Corp (Client)",
        "terms": "Payment within 30 days; Confidentiality applies",
        "dates": "April 10, 2026",
    }
    r = client.post("/generate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["document_type"] == payload["document_type"]
    assert "Jane Doe" in data["content"]
    assert "Confidentiality applies" in data["content"]
