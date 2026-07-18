from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.text_cleaner import clean_text
from app.services.nlp_engine import extract_skills


def calculate_similarity_score(resume_text: str, job_description: str) -> int:
    """
    ML-powered ATS Scoring

    Final Score =
        70% TF-IDF Cosine Similarity
      + 30% Skill Match Score

    This keeps the ATS score primarily ML-based while also
    rewarding resumes that contain the required technologies.
    """

    # ----------------------------
    # Clean text
    # ----------------------------

    cleaned_resume = clean_text(resume_text)
    cleaned_job = clean_text(job_description)

    if not cleaned_resume or not cleaned_job:
        return 0

    # ----------------------------
    # TF-IDF + Cosine Similarity
    # ----------------------------

    try:

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            norm="l2"
        )

        tfidf_matrix = vectorizer.fit_transform([
            cleaned_resume,
            cleaned_job
        ])

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        ml_score = similarity * 100

    except Exception:
        ml_score = 0

    # ----------------------------
    # Skill Match Score
    # ----------------------------

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    if len(job_skills) == 0:
        skill_score = 0
    else:
        matched = len(
            set(resume_skills).intersection(job_skills)
        )

        skill_score = (matched / len(job_skills)) * 100

    # ----------------------------
    # Hybrid ATS Score
    # ----------------------------

    final_score = (0.70 * ml_score) + (0.30 * skill_score)

    final_score = round(final_score)

    final_score = max(0, min(100, final_score))

    return final_score