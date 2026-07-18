from app.utils.skill_db import (
    PROGRAMMING_LANGUAGES,
    FRONTEND,
    BACKEND,
    DATABASES,
    DEVOPS,
    CLOUD,
    AI_ML,
)


def get_category(skill: str) -> str:
    """
    Return the category of a skill.
    """

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

    return "General"


def generate_suggestions(missing_skills):
    """
    Generate natural ATS recommendations.
    """

    if not missing_skills:
        return [
            "Excellent match! Your resume already aligns well with the job description. Focus on presenting your projects and achievements clearly."
        ]

    suggestions = []

    templates = {
        "Programming": [
            "Consider adding experience with '{skill}' if you've used it in projects or coursework.",
            "Highlight any practical work involving '{skill}' to strengthen your programming profile.",
            "If you're familiar with '{skill}', make it more visible in your resume."
        ],

        "Frontend": [
            "Showcase projects or practical experience using '{skill}'.",
            "Adding '{skill}' to relevant project descriptions could improve your match.",
            "Highlight your frontend work involving '{skill}' where applicable."
        ],

        "Backend": [
            "Including backend experience with '{skill}' would strengthen your profile.",
            "If you've built APIs or applications using '{skill}', be sure to mention them.",
            "Consider highlighting projects that demonstrate your knowledge of '{skill}'."
        ],

        "Database": [
            "Experience with '{skill}' would make your resume more competitive for this role.",
            "Mention database work involving '{skill}' if applicable.",
            "Adding projects that use '{skill}' can strengthen your technical profile."
        ],

        "DevOps": [
            "Practical exposure to '{skill}' would add value to your resume.",
            "If you've worked with '{skill}', highlight it in your projects or experience.",
            "Consider building a small project using '{skill}' to strengthen your profile."
        ],

        "Cloud": [
            "Cloud experience with '{skill}' is commonly expected for similar roles.",
            "Highlight any hands-on work involving '{skill}' if you have it.",
            "Adding cloud-based projects using '{skill}' can improve your resume."
        ],

        "AI / ML": [
            "Mention projects demonstrating your experience with '{skill}'.",
            "If you've used '{skill}' in machine learning projects, highlight those achievements.",
            "Adding practical examples involving '{skill}' would strengthen your AI/ML profile."
        ],

        "General": [
            "Consider including experience with '{skill}' if it is relevant to your background.",
            "Highlight any exposure to '{skill}' to better align with the job description.",
            "Adding examples where you've used '{skill}' can improve your resume."
        ]
    }

    for index, skill in enumerate(missing_skills[:5]):

        category = get_category(skill)

        options = templates.get(category, templates["General"])

        suggestion = options[index % len(options)].format(skill=skill)

        suggestions.append(suggestion)

    return suggestions