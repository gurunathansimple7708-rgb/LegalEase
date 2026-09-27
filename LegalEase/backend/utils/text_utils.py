import html
import re

def sanitize_text(text: str) -> str:
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def terms_to_list(terms: str) -> list[str]:
    return [x.strip() for x in terms.split(";") if x.strip()]

def html_escape(text: str) -> str:
    return html.escape(text)
