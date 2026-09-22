import io
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.models.schemas import AnalysisResponse
from app.services.parser import extract_text
from app.services.nlp_engine import extract_skills
from app.services.scorer import calculate_score
from app.services.recommender import generate_suggestions

router = APIRouter()

ALLOWED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "application/octet-stream",  # Fallback MIME often sent for docx/pdf
]

MIN_FILE_SIZE = 1 * 1024         # 1 KB minimum
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 MB maximum

SUSPICIOUS_EXTENSIONS = [
    ".exe", ".bat", ".cmd", ".com", ".scr", ".js", ".msi", ".sh", ".vbs", ".apk"
]


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # ----------------------------
    # 1. Input Validation
    # ----------------------------
    if not resume:
        raise HTTPException(status_code=400, detail="Resume file is required.")

    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    if len(job_description.strip()) < 30:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short. Please paste at least 30 characters describing the role."
        )

    filename = (resume.filename or "").lower()

    for ext in SUSPICIOUS_EXTENSIONS:
        if filename.endswith(ext):
            raise HTTPException(
                status_code=400,
                detail="Suspicious file type detected. Please upload a legitimate PDF or DOCX resume."
            )

    # Allow if extension is .pdf or .docx even if browser sent generic octet-stream
    has_valid_extension = filename.endswith(".pdf") or filename.endswith(".docx")
    has_valid_content_type = resume.content_type in ALLOWED_TYPES

    if not (has_valid_extension or has_valid_content_type):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # ----------------------------
    # 2. Safe Stream-Chunk Memory Reading (1KB - 30MB)
    # ----------------------------
    total_size = 0
    chunks = []
    chunk_size = 64 * 1024  # 64 KB chunks

    while True:
        chunk = await resume.read(chunk_size)
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds the 30 MB maximum upload limit."
            )
        chunks.append(chunk)

    file_bytes = b"".join(chunks)

    if len(file_bytes) < MIN_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size is below the 1 KB minimum requirement. Please upload a complete resume."
        )

    # ----------------------------
    # 3. Document Parsing (PDF & DOCX)
    # ----------------------------
    file_stream = io.BytesIO(file_bytes)

    try:
        resume_text = extract_text(file_stream, filename=filename, content_type=resume.content_type or "")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process document: {str(e)}")

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Unable to extract text from the uploaded document. Please check the file formatting."
        )

    # ----------------------------
    # 4. Accurate NLP Skill Extraction
    # ----------------------------
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # ----------------------------
    # 5. Hybrid ML Scoring (Skills 50% + TF-IDF ML 30% + Structure 20%)
    # ----------------------------
    result = calculate_score(
        resume_skills=resume_skills,
        job_skills=job_skills,
        resume_text=resume_text,
        job_description=job_description
    )

    score = result["ats_score"]
    matched = result["matched_skills"]
    missing = result["missing_skills"]
    extra = result["extra_skills"]
    coverage = result["coverage"]
    chart_data = result["chart_data"]
    sections = result["sections"]
    semantic_score = result.get("semantic_score", 0)

    # ----------------------------
    # 6. Contextual Suggestions
    # ----------------------------
    suggestions = generate_suggestions(missing, sections=sections)

    # ----------------------------
    # 7. Dynamic Strengths
    # ----------------------------
    strengths = []

    if score >= 80:
        strengths.append("Exceptional overall match with the job description requirements.")
    elif score >= 65:
        strengths.append("Solid overall technical alignment with the target role.")

    if len(matched) >= 5:
        strengths.append(f"Strong alignment across {len(matched)} key technical competencies.")
    elif len(matched) >= 2:
        strengths.append(f"Direct alignment with {len(matched)} core skills required by the role.")

    if matched:
        top_skills = [s.title() for s in matched[:4]]
        strengths.append(f"Verified expertise in key technologies: {', '.join(top_skills)}.")

    if sections.get("experience") and sections.get("projects") and sections.get("education"):
        strengths.append("Comprehensive resume structure with clear experience, project, and academic sections.")

    if not strengths:
        strengths.append("Foundational technical background detected matching role parameters.")

    # ----------------------------
    # 8. Dynamic Weaknesses
    # ----------------------------
    weaknesses = []

    if score < 50:
        weaknesses.append("Low overall similarity score with this specific job description.")

    if len(job_skills) > 0 and len(matched) < (len(job_skills) * 0.5):
        weaknesses.append(
            f"Underrepresentation of required job skills: only {len(matched)} of {len(job_skills)} detected."
        )

    if missing:
        top_missing = [s.title() for s in missing[:4]]
        weaknesses.append(f"Missing core technologies: {', '.join(top_missing)}.")

    if not sections.get("projects"):
        weaknesses.append("No explicit 'Projects' or 'Portfolio' section found to validate hands-on work.")

    if not sections.get("skills"):
        weaknesses.append("Skills are not grouped into a dedicated technical skills section.")

    if not weaknesses:
        weaknesses.append("No major technical skill gaps identified for this role.")

    # ----------------------------
    # 9. Clean up memory
    # ----------------------------
    await resume.close()
    del file_bytes
    del chunks

    # ----------------------------
    # 10. Response
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
        "semantic_score": semantic_score,
    }