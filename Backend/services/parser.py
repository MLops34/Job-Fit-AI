import fitz  # PyMuPDF
import docx
import re
from io import BytesIO

def parse_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_docx(file_bytes: bytes) -> str:
    doc = docx.Document(BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def parse_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")

def extract_structured_info(text: str) -> dict:
    name = text.split('\n')[0].strip()
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
    linkedin = re.findall(r'linkedin\.com\/[^\s\|]+', text)
    github = re.findall(r'github\.com\/[^\s\|]+', text)

    return {
        "name": name,
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "linkedin": linkedin[0] if linkedin else "",
        "github": github[0] if github else "",
    }

def parse_resume(file_bytes: bytes, filename: str) -> dict:
    if filename.endswith(".pdf"):
        text = parse_pdf(file_bytes)
    elif filename.endswith(".docx"):
        text = parse_docx(file_bytes)
    elif filename.endswith(".txt"):
        text = parse_txt(file_bytes)
    else:
        return {"error": "Unsupported file format."}

    print("Raw text extracted:", text[:500])  # debug first 500 chars
    structured_info = extract_structured_info(text)
    print("Structured info extracted:", structured_info)

    return {
        "raw_text": text,
        "structured_info": structured_info
    }
