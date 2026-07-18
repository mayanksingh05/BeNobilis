from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.parser import extract_text_from_pdf
from app.services.nlp_engine import extract_skills
from app.services.scorer import calculate_score
from app.services.recommender import generate_suggestions

router = APIRouter()

ALLOWED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

MAX_FILE_SIZE = 5 * 1024 * 1024

SUSPICIOUS_EXTENSIONS = [
    ".exe",
    ".bat",
    ".cmd",
    ".com",
    ".scr",
    ".js",
    ".msi",
    ".sh",
]


@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # ----------------------------
    # Input Validation
    # ----------------------------

    if not resume:
        raise HTTPException(
            status_code=400,
            detail="Resume file is required."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    if len(job_description.strip()) < 30:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short."
        )

    if resume.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    filename = (resume.filename or "").lower()

    for ext in SUSPICIOUS_EXTENSIONS:
        if filename.endswith(ext):
            raise HTTPException(
                status_code=400,
                detail="Suspicious file detected."
            )

    file_bytes = await resume.read()

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 5 MB."
        )

    # Reset pointer after validation
    resume.file.seek(0)

    # ----------------------------
    # Resume Parsing
    # ----------------------------

    if resume.content_type == "application/pdf":
        resume_text = extract_text_from_pdf(resume.file)
    else:
        raise HTTPException(
            status_code=400,
            detail="DOCX support will be added soon."
        )

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Unable to extract text from the resume."
        )

    # ----------------------------
    # Skill Extraction
    # ----------------------------

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    result = calculate_score(
        resume_skills,
        job_skills,
        resume_text
    )

    score = result["ats_score"]
    matched = result["matched_skills"]
    missing = result["missing_skills"]
    extra = result["extra_skills"]
    coverage = result["coverage"]
    chart_data = result["chart_data"]

    suggestions = generate_suggestions(missing)

    # ----------------------------
    # Strengths
    # ----------------------------

    strengths = []

    if score >= 80:
        strengths.append(
            "Resume has a strong overall match with the job description."
        )

    if len(matched) >= 5:
        strengths.append(
            "Good alignment with the required technical skills."
        )

    if "react" in matched:
        strengths.append(
            "Frontend development skills detected."
        )

    if "python" in matched:
        strengths.append(
            "Python programming experience detected."
        )

    # ----------------------------
    # Weaknesses
    # ----------------------------

    weaknesses = []

    if score < 50:
        weaknesses.append(
            "Resume has a low similarity with the job description."
        )

    if "docker" in missing:
        weaknesses.append(
            "Containerization experience is missing."
        )

    if "aws" in missing:
        weaknesses.append(
            "Cloud platform experience is missing."
        )

    if len(missing) >= 5:
        weaknesses.append(
            "Several important job skills are missing."
        )

    # ----------------------------
    # Privacy Cleanup
    # ----------------------------

    await resume.close()

    del file_bytes
    del resume_text
    del resume_skills
    del job_skills

    # ----------------------------
    # Response
    # ----------------------------

    return {
        "ats_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "coverage": coverage,
        "suggestions": suggestions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "chart_data": chart_data,
    }