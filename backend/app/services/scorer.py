from collections import defaultdict

from app.utils.skill_db import (
    PROGRAMMING_LANGUAGES,
    FRONTEND,
    BACKEND,
    DATABASES,
    DEVOPS,
    CLOUD,
    AI_ML,
)

CRITICAL_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "fastapi",
    "django",
    "sql",
    "mongodb",
    "mysql",
    "postgresql",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "machine learning",
    "tensorflow",
    "pytorch",
}


def get_category(skill: str):
    if skill in PROGRAMMING_LANGUAGES:
        return "Programming"

    if skill in FRONTEND:
        return "Frontend"

    if skill in BACKEND:
        return "Backend"

    if skill in DATABASES:
        return "Database"

    if skill in DEVOPS:
        return "DevOps"

    if skill in CLOUD:
        return "Cloud"

    if skill in AI_ML:
        return "AI / ML"

    return "Other"


def calculate_score(resume_skills, job_skills, resume_text):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    extra = sorted(resume_set - job_set)

    chart_data = defaultdict(lambda: {
        "matched": 0,
        "missing": 0,
        "extra": 0
    })

    for skill in matched:
        chart_data[get_category(skill)]["matched"] += 1

    for skill in missing:
        chart_data[get_category(skill)]["missing"] += 1

    for skill in extra:
        chart_data[get_category(skill)]["extra"] += 1

    chart_data = [
        {
            "category": category,
            "matched": values["matched"],
            "missing": values["missing"],
            "extra": values["extra"]
        }
        for category, values in chart_data.items()
    ]

    coverage = {
        "matched": len(matched),
        "missing": len(missing),
        "extra": len(extra)
    }

    # -------------------------
    # ATS Score
    # -------------------------

    total_required = max(len(job_set), 1)

    # ----------------------------------
    # ATS Score Calculation
    # ----------------------------------

    text = resume_text.lower()

    # 75 Marks - Required Skill Match
    skill_score = (len(matched) / total_required) * 75

    # 10 Marks - Resume Completeness
    completeness = 0

    if "education" in text:
        completeness += 2

    if "project" in text:
        completeness += 3

    if "skill" in text:
        completeness += 2

    if "experience" in text:
        completeness += 3

    completeness = min(completeness, 10)

    # 10 Marks - Relevant Projects
    project_score = 0

    project_keywords = [
        "react",
        "fastapi",
        "python",
        "api",
        "rest",
        "dashboard",
        "ai",
        "machine learning",
        "resume",
        "file sharing",
        "web application",
    ]

    for keyword in project_keywords:
        if keyword in text:
            project_score += 1.5

    project_score = min(project_score, 10)

    # 5 Marks - Extra Relevant Skills
    extra_bonus = min(len(extra), 5)

    # Penalty for missing important skills
    penalty = 0

    for skill in missing:
        if skill in CRITICAL_SKILLS:
            penalty += 2

    penalty = min(penalty, 5)

    ats_score = round(
        skill_score
        + completeness
        + project_score
        + extra_bonus
        - penalty
    )

    ats_score = max(0, min(100, ats_score))

    return {
        "ats_score": ats_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "coverage": coverage,
        "chart_data": chart_data
    }