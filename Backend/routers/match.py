from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from Backend.services import parser,storage
from Backend.services import storage, matcher
from ..services.parser import parse_resume
import re
router = APIRouter()

import logging

from Backend.services import storage

def is_valid_resume(text: str) -> bool:
    """
    Checks whether the text contains common resume sections/keywords.
    """
    resume_keywords = [
        'experience', 'education', 'skills', 'projects',
        'summary', 'certifications', 'objective', 'achievements'
    ]
    text = text.lower()
    matches = [kw for kw in resume_keywords if kw in text]
    return len(matches) >= 2  # Require at least 2 matches to consider it a resume

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    logging.info(f"Received file: {file.filename}, size: {len(contents)} bytes")

    result = parser.parse_resume(contents, file.filename)
    logging.info(f"Parser result keys: {list(result.keys())}")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    raw_text = result["raw_text"]
    
    # ✅ Check if it's a valid resume
    if not is_valid_resume(raw_text):
        raise HTTPException(status_code=400, detail="❌ Uploaded document is not a valid resume. Please upload a proper resume.")

    # Save resume
    user_id = "user123"  # Replace this with actual session/auth-based user_id if needed
    storage.save_resume(user_id, raw_text)

    return {
        "filename": file.filename,
        "stored": True,
        "parsed_text_full": raw_text,
        "structured_data": result["structured_info"]
    }


@router.post("/upload-job")
async def upload_job(description: str = Form(...)):
    user_id = "user123"  
    resume_text = storage.get_resume(user_id)
    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="❌ Please upload resume first before uploading job description."
        )
    storage.save_job_description(user_id, description)

    return {
        "job_description": description[:200],
        "stored": True
    }

@router.post("/match-score")
def match_score():
    resume_text = storage.get_resume(user_id="user123", default_value="")
    job_description = storage.get_job_description(user_id="user123", default_value="")

    if not resume_text or not job_description:
        raise HTTPException(status_code=400, detail="Resume or job description not found.")

    match_score = matcher.calculate_match_score(resume_text, job_description)

    return { 
        "match_score_percent": match_score,
        "message": "Match score calculated successfully."
    }

@router.post("/ats-check")

def ats_check(data: dict = None):
    # Get resume text (from data or storage)
    resume_text = data.get("resume_text") if data and "resume_text" in data else storage.get_resume("user123")
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text not found.")
    ats_report = {}

    # 1. Check for important resume sections
    sections = ["education", "experience", "skills", "projects", "certifications", "summary", "objective"]
    found_sections = [sec for sec in sections if sec in resume_text.lower()]
    section_score = round(len(found_sections) / len(sections) * 100, 2)
    ats_report["sections_found"] = found_sections
    ats_report["section_score"] = section_score
    ats_report["keyword_match"] = None  # Since JD is not provided, make it explicit
    ats_report["resume_text_length"] = len(resume_text)


    # 2. Bullet points score
    bullet_points = resume_text.count("•") + resume_text.count("- ")
    bullet_point_score = 100 if bullet_points >= 5 else bullet_points * 20  # Max 100 if >=5
    ats_report["bullet_points"] = bullet_points
    ats_report["bullet_point_score"] = bullet_point_score

    # 3. Length score based on word count
    word_count = len(resume_text.split())
    length_score = 100 if 300 <= word_count <= 800 else 60 if word_count > 800 else 40
    ats_report["length"] = word_count
    ats_report["length_score"] = length_score

    # 4. Contact Info
    has_email = bool(re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resume_text))
    has_phone = bool(re.search(r"\+?\d[\d\s\-()]{7,}\d", resume_text))
    ats_report["has_email"] = has_email
    ats_report["has_phone"] = has_phone
    contact_score = 50 if has_email else 0
    contact_score += 50 if has_phone else 0

    # 5. Final ATS Score (out of 100)
    final_score = (
        (section_score * 0.4) +
        (length_score * 0.3) +
        (bullet_point_score * 0.2) +
        (contact_score * 0.1)
    )
    ats_report["final_ats_score"] = round(final_score, 2)

    return {
    "keyword_match": ats_report["keyword_match"],
    "sections_found": found_sections,
    "section_score": section_score,
    "bullet_points": bullet_points,
    "bullet_point_score": bullet_point_score,
    "length": word_count,
    "length_score": length_score,
    "has_email": has_email,
    "has_phone": has_phone,
    "final_ats_score": final_score
}




@router.get("/health")
async def health_check():
    return {"status": "ok"}

