# services/storage.py

# In-memory storage for resumes and job descriptions
store = {
    "resumes": {},  # {user_id: resume_text}
    "job_descriptions": {}  # {user_id: jd_text}
}

def save_resume(user_id: str, resume_text: str):
    """Save resume text for a given user ID."""
    store["resumes"][user_id] = resume_text

def save_job_description(user_id: str, jd_text: str):
    """Save job description text for a given user ID."""
    store["job_descriptions"][user_id] = jd_text

def get_resume(user_id: str, default_value: str = ""):
    """Retrieve resume text for a given user ID."""
    return store["resumes"].get(user_id, default_value)

def get_job_description(user_id: str, default_value: str = ""):
    """Retrieve job description text for a given user ID."""
    return store["job_descriptions"].get(user_id, default_value)
