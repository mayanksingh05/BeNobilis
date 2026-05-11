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

    score, matched, missing, chart_data = calculate_score(
        resume_skills,
        job_skills
    )

    suggestions = generate_suggestions(missing)

    strengths = []

    if len(matched) >= 5:
        strengths.append("Strong technical skill alignment")

    if "react" in matched:
        strengths.append("Good frontend development skills")

    if "python" in matched:
        strengths.append("Strong backend programming foundation")

    weaknesses = []

    if "aws" in missing:
        weaknesses.append("Missing cloud platform experience")

    if "docker" in missing:
        weaknesses.append("Containerization knowledge missing")

    if len(missing) > 5:
        weaknesses.append("Large skill gap with job requirements")

    return {
        "ats_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "chart_data": chart_data
    }