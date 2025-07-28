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
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else ""

    # Improved regex patterns
    email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.findall(r'(\+?\d[\d\s\-\(\)]{7,}\d)', text)
    linkedin = re.findall(r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+', text)
    github = re.findall(r'(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+', text)

    return {
        "name": name,
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "linkedin": linkedin[0] if linkedin else "",
        "github": github[0] if github else "",
    }

def extract_sections(text: str) -> dict:
    sections = {}
    current_section = "Header"
    sections[current_section] = []

    # Define common section headers, case-insensitive
    section_headers = [
        "education",
        "experience",
        "projects",
        "certificates & achievements",
        "technical skills",
        "skills",
        "summary",
        "objective",
        "contact",
    ]

    for line in text.split('\n'):
        line_strip = line.strip()
        if not line_strip:
            continue
        # Check if line matches any section header (case-insensitive)
        if any(line_strip.lower().startswith(h) for h in section_headers):
            current_section = line_strip.title()
            sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line_strip)

    # Join lines back to strings
    for key in sections:
        sections[key] = "\n".join(sections[key])

    return sections

def parse_resume(file_bytes: bytes, filename: str) -> dict:
    if filename.lower().endswith(".pdf"):
        text = parse_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        text = parse_docx(file_bytes)
    elif filename.lower().endswith(".txt"):
        text = parse_txt(file_bytes)
    else:
        return {"error": "Unsupported file format."}

    print("Raw text extracted:", text[:500])  # debug first 500 chars
    structured_info = extract_structured_info(text)
    sections = extract_sections(text)
    print("Structured info extracted:", structured_info)

    return {
        "raw_text": text,
        "structured_info": structured_info,
        "sections": sections
    }
