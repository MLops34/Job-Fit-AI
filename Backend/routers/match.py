from fastapi import APIRouter, UploadFile, File, Form
from Backend.services import parser,storage
from Backend.services import storage, matcher
router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    result = parser.parse_resume(contents, file.filename)

    if "error" in result:
        return {"error": result["error"]}

    user_id = "user123"
    storage.save_resume(user_id, result["raw_text"])

    return {
        "filename": file.filename,
        "stored": True,
        "parsed_text_preview": result["raw_text"][:300],
        "structured_data": result["structured_info"]
    }


@router.post("/upload-job")
async def upload_job(description: str = Form(...)):
    user_id = "user123"
    storage.save_job(user_id, description)
    return {
        "job_description": description[:200],
        "stored": True
    }

@router.post("/match-score")
async def match_score():
    user_id = "user123"
    resume_text = storage.get_resume(user_id)
    job_description = storage.get_job(user_id)

    if not resume_text or not job_description:
        return {"error": "Resume or job description not uploaded."}

    score = matcher.calculate_jobfit_score(resume_text, job_description)

    return {
        "match_score_percent": score,
        "message": f"Resume matches the job description by {score}%"
    }


@router.get("/health")
async def health_check():
    return {"status": "ok"}

