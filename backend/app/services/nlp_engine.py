import re

from app.utils.skill_db import SKILLS_DB, SKILL_ALIASES
from app.utils.text_cleaner import clean_text


def normalize_text(text: str) -> str:
    """
    Normalize text before skill extraction.
    """

    text = clean_text(text)

    text = text.replace("/", " ")
    text = text.replace("\\", " ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill(skill: str) -> str:
    """
    Convert aliases into one canonical skill.
    """

    skill = skill.lower().strip()

    return SKILL_ALIASES.get(skill, skill)


def extract_skills(text: str):
    """
    Extract technical skills from resume or job description.

    Returns:
        List[str]
    """

    if not text:
        return []

    normalized_text = normalize_text(text)

    found = set()

    # -----------------------------
    # Match predefined skills
    # -----------------------------

    for skill in SKILLS_DB:

        normalized_skill = normalize_skill(skill)

        pattern = (
            r"\b"
            + re.escape(skill.lower())
                .replace(r"\ ", r"\s+")
                .replace(r"\-", r"[-\s]?")
                .replace(r"\.", r"\.?")
            + r"\b"
        )

        if re.search(pattern, normalized_text):
            found.add(normalized_skill)

    # -----------------------------
    # Match aliases
    # -----------------------------

    for alias, canonical in SKILL_ALIASES.items():

        pattern = (
            r"\b"
            + re.escape(alias.lower())
                .replace(r"\ ", r"\s+")
                .replace(r"\-", r"[-\s]?")
                .replace(r"\.", r"\.?")
            + r"\b"
        )

        if re.search(pattern, normalized_text):
            found.add(canonical)

    return sorted(found)