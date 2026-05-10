from app.utils.skill_db import SKILLS_DB

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))