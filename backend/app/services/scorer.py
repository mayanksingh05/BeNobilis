from collections import defaultdict

CATEGORY_MAP = {
    "react": "Frontend",
    "html": "Frontend",
    "css": "Frontend",
    "javascript": "Frontend",
    "tailwind css": "Frontend",

    "python": "Backend",
    "fastapi": "Backend",
    "flask": "Backend",
    "node.js": "Backend",
    "sql": "Backend",
    "mongodb": "Backend",
    "rest api": "Backend",

    "aws": "Cloud",
    "docker": "DevOps",
    "git": "DevOps",

    "machine learning": "AI/ML",
    "data analysis": "AI/ML",
}

def calculate_score(resume_skills, job_skills):
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matched) / len(job_skills)) * 100)

    category_scores = defaultdict(lambda: {"matched": 0, "total": 0})

    for skill in job_skills:
        category = CATEGORY_MAP.get(skill, "Other")

        category_scores[category]["total"] += 1

        if skill in matched:
            category_scores[category]["matched"] += 1

    chart_data = []

    for category, values in category_scores.items():
        total = values["total"]
        matched_count = values["matched"]

        percentage = int((matched_count / total) * 100)

        chart_data.append({
            "name": category,
            "score": percentage
        })

    return score, matched, missing, chart_data