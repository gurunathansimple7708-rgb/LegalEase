from __future__ import annotations
from io import BytesIO
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF
from backend.utils.text_utils import sanitize_text, terms_to_list

def _markdown_lines(text: str) -> list[str]:
    return [x.rstrip() for x in sanitize_text(text).splitlines()]

def format_txt(text: str) -> bytes:
    return sanitize_text(text).encode("utf-8")

def format_docx(text: str, doc_type: str, terms: str = "") -> bytes:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(doc_type.upper())
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr = subtitle.add_run("LegalEase - AI-Assisted Draft")
    rr.italic = True
    rr.font.size = Pt(9)

    for line in _markdown_lines(text):
        if not line:
            doc.add_paragraph()
        elif line.startswith("# "):
            p = doc.add_paragraph()
            r = p.add_run(line[2:].strip()); r.bold = True; r.font.size = Pt(15)
        elif line.startswith("## "):
            p = doc.add_paragraph()
            r = p.add_run(line[3:].strip()); r.bold = True; r.font.size = Pt(12)
        elif re.match(r"^\d+\.\s+", line):
            doc.add_paragraph(re.sub(r"^\d+\.\s+", "", line), style="List Number")
        elif line.startswith("- "):
            doc.add_paragraph(line[2:].strip(), style="List Bullet")
        else:
            doc.add_paragraph(line)

    term_items = terms_to_list(terms)
    if term_items:
        h = doc.add_paragraph()
        r = h.add_run("Terms supplied by user"); r.bold = True
        table = doc.add_table(rows=1, cols=2); table.style = "Table Grid"
        table.rows[0].cells[0].text = "No."
        table.rows[0].cells[1].text = "Term"
        for i, term in enumerate(term_items, 1):
            cells = table.add_row().cells
            cells[0].text = str(i); cells[1].text = term

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("LegalEase | AI-assisted draft | Review before use").font.size = Pt(8)

    out = BytesIO(); doc.save(out); return out.getvalue()

class LegalEasePDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 8, self.doc_type.upper(), align="C")
        self.ln(8)
        self.line(10, 18, 200, 18)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", size=8)
        self.cell(0, 8, "LegalEase | AI-assisted draft | Review before use", align="C")

def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalEasePDF(doc_type)
    pdf.set_title(doc_type)
    pdf.add_page()
    for line in _markdown_lines(text):
        if not line:
            pdf.ln(3); continue
        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 15); pdf.multi_cell(0, 8, line[2:].strip()); pdf.ln(2)
        elif line.startswith("## "):
            pdf.set_font("Helvetica", "B", 12); pdf.multi_cell(0, 7, line[3:].strip()); pdf.ln(1)
        elif line.startswith("- "):
            pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 6, "- " + line[2:].strip())
        else:
            pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 6, line)
    return bytes(pdf.output())
