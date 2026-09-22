import logging
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.text_cleaner import clean_text_for_tfidf

logger = logging.getLogger(__name__)


def calculate_semantic_similarity(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Computes semantic similarity using TF-IDF and Cosine Similarity,
    with sublinear term frequency and n-gram analysis.

    Applies non-linear calibration to adjust for the inherent length asymmetry
    between comprehensive resumes and concise job descriptions.
    """
    cleaned_resume = clean_text_for_tfidf(resume_text)
    cleaned_job = clean_text_for_tfidf(job_description)

    if not cleaned_resume or not cleaned_job:
        return {"raw_similarity": 0.0, "semantic_score": 0}

    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            norm="l2",
            stop_words="english",
            max_features=5000,
        )

        tfidf_matrix = vectorizer.fit_transform([
            cleaned_resume,
            cleaned_job
        ])

        raw_similarity = float(
            cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        )

        # Calibrated scaling for asymmetric document retrieval:
        # In IR, raw cosine between a 600-word resume and a 60-word JD rarely exceeds 0.40.
        # Power-scaling appropriately maps genuine domain relevance to a 0-100 scale.
        if raw_similarity <= 0.02:
            semantic_score = 0
        else:
            scaled = (raw_similarity ** 0.55) * 160.0 - 15.0
            semantic_score = int(round(max(0.0, min(100.0, scaled))))

    except Exception as e:
        logger.error(f"Error computing TF-IDF similarity: {e}")
        raw_similarity = 0.0
        semantic_score = 0

    return {
        "raw_similarity": round(raw_similarity, 4),
        "semantic_score": semantic_score,
    }