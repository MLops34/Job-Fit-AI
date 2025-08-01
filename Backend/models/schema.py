from pydantic import BaseModel, Field
from typing import Optional

class ResumeInput(BaseModel):
    resume_text: str = Field(..., description="Extracted or raw resume text")

class JDInput(BaseModel):
    job_description_text: str = Field(..., description="Job description text")
 
class MatchResponse(BaseModel):
    match_score: float = Field(..., description="Score representing match between resume and JD")
    feedback: Optional[str] = Field(None, description="LLM-generated feedback on the match")
