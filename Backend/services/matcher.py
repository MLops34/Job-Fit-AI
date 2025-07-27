from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute the cosine similarity percentage between two texts using TF-IDF vectors.

    Args:
        text1 (str): First text (e.g., resume text).
        text2 (str): Second text (e.g., job description).

    Returns:
        float: Similarity score as a percentage (0 to 100).
    """

    # Handle empty inputs gracefully
    if not text1.strip() or not text2.strip():
        return 0.0

    # Initialize TF-IDF vectorizer with English stop words
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform both texts into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Compute cosine similarity between the two vectors
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Return as percentage rounded to 2 decimal places
    return round(similarity * 100, 2)
