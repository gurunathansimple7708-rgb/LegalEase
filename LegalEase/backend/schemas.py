from pydantic import BaseModel, Field, field_validator

class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=2, max_length=4000)
    terms: str = Field(min_length=2, max_length=10000)
    dates: str = Field(min_length=2, max_length=200)

    @field_validator("document_type", "parties", "terms", "dates")
    @classmethod
    def strip_input(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty.")
        return value

class GeneratedDocument(BaseModel):
    document_type: str
    content: str
    demo_mode: bool = False

class ExportRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    content: str = Field(min_length=1, max_length=50000)
    terms: str = Field(default="", max_length=10000)
