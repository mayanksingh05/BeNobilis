def generate_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"Consider adding experience or projects related to {skill}."
        )

    if not suggestions:
        suggestions.append("Your resume matches the job description well.")

    return suggestions