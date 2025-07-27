resume_store = {}
job_store = {}

def save_resume(user_id: str, text: str):
    resume_store[user_id] = text

def get_resume(user_id: str) -> str:
    return resume_store.get(user_id, "")

def save_job(user_id: str, text: str):
    job_store[user_id] = text

def get_job(user_id: str) -> str:
    return job_store.get(user_id, "")

