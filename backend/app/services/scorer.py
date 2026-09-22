import re
from collections import defaultdict
from typing import Dict, Any, List

from app.utils.skill_db import get_skill_category, SKILL_ALIASES
from app.services.ml_scorer import calculate_semantic_similarity


def get_category(skill: str) -> str:
    """
    Return human-readable category for any skill out of 17 supported categories.
    """
    return get_skill_category(skill)


def detect_sections(text: str) -> Dict[str, bool]:
    """
    Detect presence of core resume sections using regex matching on industry synonyms.
    """
    t = text.lower()

    experience_detected = bool(re.search(
        r"(?i)\b(experience|work\s+history|employment|professional\s+background|career\s+history|work\s+experience)\b",
        t
    ))

    education_detected = bool(re.search(
        r"(?i)\b(education|academic|qualifications|degree|degrees|university|college|bachelor|master|phd)\b",
        t
    ))

    projects_detected = bool(re.search(
        r"(?i)\b(projects?|portfolio|key\s+achievements|open\s+source|personal\s+projects)\b",
        t
    ))

    skills_detected = bool(re.search(
        r"(?i)\b(skills?|technical\s+proficiencies|technologies|competencies|tools\s+&\s+technologies|core\s+competencies)\b",
        t
    ))

    return {
        "experience": experience_detected,
        "education": education_detected,
        "projects": projects_detected,
        "skills": skills_detected,
    }


def calculate_score(
    resume_skills: List[str],
    job_skills: List[str],
    resume_text: str,
    job_description: str = ""
) -> Dict[str, Any]:
    """
    Calculates accurate ATS Score using a calibrated Hybrid ML Architecture:
    1. Skill Match Score (50 Marks) - Direct coverage of required technical competencies.
    2. Semantic TF-IDF Score (30 Marks) - Contextual and project alignment via calibrated cosine similarity.
    3. Structural & Section Completeness (20 Marks) - Professional formatting and section presence.
    """
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    extra = sorted(resume_set - job_set)

    # -----------------------------
    # 1. Category Chart Data (17 Categories)
    # -----------------------------
    category_counts = defaultdict(lambda: {"matched": 0, "missing": 0, "extra": 0})

    for skill in matched:
        category_counts[get_category(skill)]["matched"] += 1

    for skill in missing:
        category_counts[get_category(skill)]["missing"] += 1

    for skill in extra:
        category_counts[get_category(skill)]["extra"] += 1

    chart_data = [
        {
            "category": cat,
            "matched": vals["matched"],
            "missing": vals["missing"],
            "extra": vals["extra"],
            "total": vals["matched"] + vals["missing"] + vals["extra"],
        }
        for cat, vals in category_counts.items()
    ]
    chart_data.sort(key=lambda x: x["total"], reverse=True)

    coverage = {
        "matched": len(matched),
        "missing": len(missing),
        "extra": len(extra)
    }

    # -----------------------------
    # 2. Skill Match Score (50 Marks)
    # -----------------------------
    if len(job_set) > 0:
        skill_score = (len(matched) / len(job_set)) * 50.0
    else:
        # Fallback if job description does not specify explicit keywords from DB
        skill_score = 30.0 if len(matched) > 0 else 15.0

    # Extra skills bonus: up to +3 marks for complementary tech
    extra_bonus = min(len(extra) * 0.5, 3.0)

    # -----------------------------
    # 3. Semantic TF-IDF ML Score (30 Marks)
    # -----------------------------
    if job_description.strip():
        sem_result = calculate_semantic_similarity(resume_text, job_description)
        semantic_score = sem_result["semantic_score"]
        raw_similarity = sem_result["raw_similarity"]
    else:
        semantic_score = int(round((len(matched) / max(len(job_set), 1)) * 100))
        raw_similarity = 0.0

    semantic_points = (semantic_score / 100.0) * 30.0

    # -----------------------------
    # 4. Structural Completeness (20 Marks)
    # -----------------------------
    sections = detect_sections(resume_text)
    completeness = 0
    if sections["experience"]:
        completeness += 6
    if sections["education"]:
        completeness += 5
    if sections["projects"]:
        completeness += 5
    if sections["skills"]:
        completeness += 4

    # -----------------------------
    # 5. Proportional Deficit Penalty
    # -----------------------------
    # If the JD specifies at least 3 skills and candidate has less than 35% match, apply penalty
    penalty = 0
    if len(job_set) >= 3 and len(matched) < len(job_set) * 0.35:
        penalty = 5

    # -----------------------------
    # 6. Final Calibrated ATS Score
    # -----------------------------
    ats_score = round(skill_score + extra_bonus + semantic_points + completeness - penalty)
    ats_score = max(0, min(100, ats_score))

    return {
        "ats_score": ats_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "coverage": coverage,
        "chart_data": chart_data,
        "semantic_score": semantic_score,
        "raw_similarity": raw_similarity,
        "sections": sections,
    }