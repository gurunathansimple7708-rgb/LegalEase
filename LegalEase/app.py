import html
import os
import requests
import streamlit as st

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.markdown("""
<style>
.main-title{text-align:center;font-size:2.6rem;font-weight:800;margin-bottom:0}
.subtitle{text-align:center;color:#777;margin-bottom:1.5rem}
.preview{background:#111827;color:#f9fafb;padding:1.25rem;border-radius:14px;
max-height:620px;overflow:auto;white-space:pre-wrap;font-family:Georgia,serif;line-height:1.55}
.notice{padding:.8rem 1rem;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa;margin-bottom:1rem}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered legal document drafting, editing and export</div>', unsafe_allow_html=True)
st.markdown('<div class="notice"><b>Review notice:</b> LegalEase creates AI-assisted drafts. Check the facts and applicable jurisdiction before signing or relying on a document.</div>', unsafe_allow_html=True)

if "document" not in st.session_state:
    st.session_state.document = ""
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

left, right = st.columns([0.9, 1.1], gap="large")

with left:
    st.subheader("Document details")
    document_type = st.selectbox("Document type", [
        "Employment Contract", "Non-Disclosure Agreement (NDA)", "Lease Agreement",
        "Freelance Work Contract", "Service Agreement", "General Agreement", "Custom Legal Document"
    ])
    if document_type == "Custom Legal Document":
        document_type = st.text_input("Custom document type", placeholder="e.g. Consulting Agreement")

    parties = st.text_area("Parties involved", height=120,
                           placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)")
    terms = st.text_area("Terms & Conditions", height=190,
                         placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
                         help="Separate individual terms with semicolons.")
    dates = st.text_input("Effective date", placeholder="April 10, 2026")

    if st.button("Generate Document", type="primary", use_container_width=True):
        payload = {"document_type": document_type, "parties": parties, "terms": terms, "dates": dates}
        try:
            with st.spinner("Generating draft..."):
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=120)
            if response.ok:
                data = response.json()
                st.session_state.document = data["content"]
                st.session_state.demo_mode = data.get("demo_mode", False)
                st.success("Document generated.")
                if st.session_state.demo_mode:
                    st.info("Demo mode is active because GEMINI_API_KEY is not configured.")
            else:
                st.error(f"Backend error: {response.text}")
        except requests.RequestException as exc:
            st.error(f"Could not reach FastAPI backend: {exc}")

with right:
    st.subheader("Editable preview")
    edited = st.text_area("Document text", value=st.session_state.document, height=520,
                           label_visibility="collapsed", placeholder="Your generated document will appear here.")
    st.session_state.document = edited

    if st.session_state.document:
        st.markdown("#### Styled preview")
        st.markdown(f'<div class="preview">{html.escape(st.session_state.document)}</div>', unsafe_allow_html=True)

        st.markdown("#### Download")
        c1, c2, c3 = st.columns(3)
        payload = {"document_type": document_type, "content": st.session_state.document, "terms": terms}

        with c1:
            if st.button("Prepare TXT", use_container_width=True):
                r = requests.post(f"{BACKEND_URL}/export/txt", json=payload, timeout=60)
                if r.ok: st.download_button("Download TXT", r.content, "legalease_document.txt", "text/plain", use_container_width=True)
                else: st.error(r.text)
        with c2:
            if st.button("Prepare DOCX", use_container_width=True):
                r = requests.post(f"{BACKEND_URL}/export/docx", json=payload, timeout=60)
                if r.ok: st.download_button("Download DOCX", r.content, "legalease_document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                else: st.error(r.text)
        with c3:
            if st.button("Prepare PDF", use_container_width=True):
                r = requests.post(f"{BACKEND_URL}/export/pdf", json=payload, timeout=60)
                if r.ok: st.download_button("Download PDF", r.content, "legalease_document.pdf", "application/pdf", use_container_width=True)
                else: st.error(r.text)

st.divider()
st.caption("LegalEase • FastAPI + Streamlit + Gemini • AI-assisted drafting")
