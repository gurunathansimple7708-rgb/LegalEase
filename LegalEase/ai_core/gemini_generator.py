from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """
You are LegalEase, an AI-assisted legal-document drafting engine.

Create a professional legal document draft from the user's supplied facts.
Do not invent names, dates, monetary values, addresses, or obligations.
Use clear headings and numbered sections.
Preserve every material user-provided term.
If information is missing, write a neutral placeholder such as [DETAIL REQUIRED]
rather than guessing.
Return Markdown only.

This is a drafting assistant, not a lawyer. Do not claim that a generated
document is guaranteed legally valid or appropriate for a particular jurisdiction.
Include a short final note stating that the draft should be reviewed for the
applicable jurisdiction before signing.
"""

@dataclass
class GeminiDocumentGenerator:
    api_key: str = ""
    model: str = "gemini-3.8-flash"

    def __post_init__(self) -> None:
        self.client: Optional[genai.Client] = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    @property
    def demo_mode(self) -> bool:
        return self.client is None

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        if self.demo_mode:
            return self._demo_document(document_type, parties, terms, dates)

        prompt = f"""
Draft a {document_type}.

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{dates}

Requirements:
- Start with a clear document title.
- Include parties and effective date.
- Organize supplied terms into sensible numbered clauses.
- Add standard boilerplate only when generic and when it does not invent facts.
- Preserve user-provided facts exactly where possible.
- Use Markdown headings and numbered sections.
- Finish with a jurisdiction-review disclaimer.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=5000,
            ),
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned no text.")
        return text.strip()

    @staticmethod
    def _demo_document(document_type: str, parties: str, terms: str, dates: str) -> str:
        clauses = [x.strip() for x in terms.split(";") if x.strip()]
        bullets = "\n".join(f"{i}. {item}" for i, item in enumerate(clauses, 1))
        if not bullets:
            bullets = "1. [DETAIL REQUIRED]"
        return f"""# {document_type}

## 1. Parties
{parties}

## 2. Effective Date
{dates}

## 3. Terms and Conditions
{bullets}

## 4. General Provisions
The parties intend this document to record the terms identified above. Any
additional provisions should be reviewed and completed before execution.

## Review Notice
This is a demonstration AI-assisted draft. Review the document for the
applicable jurisdiction and facts before signing or relying on it.
"""
