from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text: str, job_description: str) -> float:
    # Basic cleanup, you can use your utils here
    resume_text = resume_text.lower().strip()
    job_description = job_description.lower().strip()

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)


# services/matcher.py

default_jd = """
We are looking for a Data Scientist with expertise in machine learning, data analysis, Python, statistics, and communication skills.
"""

def ats_score_check(resume_text: str) -> dict:
    required_sections = ["skills", "experience", "education"]
    found = sum(1 for sec in required_sections if sec in resume_text.lower())

    structure_score = (found / len(required_sections)) * 100
    readability_score = 100 if len(resume_text) > 300 else 60

    final_score = 0.6 * structure_score + 0.4 * readability_score

    return {
        "structure_score": structure_score,
        "readability_score": readability_score,
        "final_ats_score": round(final_score, 2)
    }

