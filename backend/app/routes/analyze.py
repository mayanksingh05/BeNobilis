from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.parser import extract_text_from_pdf
from app.services.nlp_engine import extract_skills
from app.services.scorer import calculate_score
from app.services.recommender import generate_suggestions

router = APIRouter()

ALLOWED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    if resume.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files allowed"
        )

    content = await resume.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 5MB limit"
        )

    suspicious_extensions = [
        ".exe",
        ".bat",
        ".sh",
        ".js"
    ]

    for ext in suspicious_extensions:
        if resume.filename.endswith(ext):
            raise HTTPException(
                status_code=400,
                detail="Suspicious file detected"
            )

    resume.file.seek(0)

    if resume.content_type == "application/pdf":
        resume_text = extract_text_from_pdf(resume.file)
    else:
        resume_text = "DOCX support coming soon"

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