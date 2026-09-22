import re
from typing import List, Set

from app.utils.skill_db import SKILLS_DB, SKILL_ALIASES
from app.utils.text_cleaner import normalize_text_for_nlp

# Precompiled specialized regex patterns for skills with punctuation, single chars, or ambiguous words
SPECIAL_PATTERNS = {
    "c++": (re.compile(r"(?<!\w)c\+\+(?!\w)", re.IGNORECASE), "c++"),
    "c#": (re.compile(r"(?<!\w)c\#(?!\w)", re.IGNORECASE), "c#"),
    "c": (re.compile(r"(?<!\w)C(?!\w)"), "c"),
    "r": (re.compile(r"(?<!\w)R(?!\w)"), "r"),
    "go": (re.compile(r"\b(?:golang|go\s+lang|go\s+programming)\b|\bGo\b"), "go"),
    ".net": (re.compile(r"(?<!\w)\.net(?!\w)|\bdotnet\b", re.IGNORECASE), ".net"),
    "asp.net": (re.compile(r"(?<!\w)asp\.net(?!\w)", re.IGNORECASE), "asp.net"),
    "node.js": (re.compile(r"\bnode(?:\.|\s*)js\b", re.IGNORECASE), "node.js"),
    "next.js": (re.compile(r"\bnext(?:\.|\s*)js\b", re.IGNORECASE), "next.js"),
    "vue.js": (re.compile(r"\bvue(?:\.|\s*)js\b", re.IGNORECASE), "vue"),
    "express.js": (re.compile(r"\bexpress(?:\.|\s*)js\b", re.IGNORECASE), "express.js"),
    "ci/cd": (re.compile(r"\bci[\s\/\-]cd\b", re.IGNORECASE), "ci/cd"),
    "tcp/ip": (re.compile(r"\btcp[\s\/\-]ip\b", re.IGNORECASE), "tcp/ip"),
    "rest api": (re.compile(r"\b(?:rest\s*api|restful|rest\s*apis)\b", re.IGNORECASE), "rest api"),
}

# Ambiguous words to exclude from generic matching because they cause false positives
AMBIGUOUS_SKILLS = {
    "c", "r", "go", "c++", "c#", ".net", "asp.net", "node.js", "next.js",
    "vue.js", "express.js", "ci/cd", "tcp/ip", "rest", "rest api", "ip"
}

# Precompile standard skill patterns once at import time
_COMPILED_SKILLS = []
for skill in SKILLS_DB:
    if skill in AMBIGUOUS_SKILLS:
        continue
    escaped = re.escape(skill).replace(r"\ ", r"\s+").replace(r"\-", r"[-\s]?")
    pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
    _COMPILED_SKILLS.append((pattern, skill))

# Precompile alias patterns once at import time
_COMPILED_ALIASES = []
for alias, canonical in SKILL_ALIASES.items():
    if alias in AMBIGUOUS_SKILLS or canonical in AMBIGUOUS_SKILLS:
        continue
    escaped = re.escape(alias).replace(r"\ ", r"\s+").replace(r"\-", r"[-\s]?")
    pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
    _COMPILED_ALIASES.append((pattern, canonical))


def normalize_skill(skill: str) -> str:
    """
    Convert any skill name or alias into its canonical database form.
    """
    s = skill.lower().strip()
    return SKILL_ALIASES.get(s, s)


def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from resume or job description with high accuracy,
    protecting single-letter languages, special characters, and compound terms.
    """
    if not text:
        return []

    normalized_text = normalize_text_for_nlp(text)
    found: Set[str] = set()

    # 1. Specialized regex matching (C++, C#, C, R, Go, .NET, Node.js, Next.js, CI/CD, etc.)
    for key, (pattern, canonical) in SPECIAL_PATTERNS.items():
        if pattern.search(normalized_text):
            found.add(canonical)

    # 2. Standard skill matching across the master database
    for pattern, canonical in _COMPILED_SKILLS:
        if pattern.search(normalized_text):
            found.add(canonical)

    # 3. Alias mapping matching
    for pattern, canonical in _COMPILED_ALIASES:
        if pattern.search(normalized_text):
            found.add(canonical)

    # Clean up redundant nested overlaps (e.g. if 'react native' is found, both are kept or distinct)
    return sorted(found)