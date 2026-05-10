from fastapi import APIRouter, UploadFile, File, Form
from app.services.parser import extract_text_from_pdf
from app.services.nlp_engine import extract_skills
from app.services.scorer import calculate_score
from app.services.recommender import generate_suggestions

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume.file)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    score, matched, missing = calculate_score(
        resume_skills,
        job_skills
    )

    suggestions = generate_suggestions(missing)

    return {
        "ats_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }