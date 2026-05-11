def generate_suggestions(missing_skills):

    suggestions = []

    if "aws" in missing_skills:
        suggestions.append(
            "Add cloud deployment experience using AWS or GCP."
        )

    if "docker" in missing_skills:
        suggestions.append(
            "Learn Docker containerization for deployment workflows."
        )

    if "git" in missing_skills:
        suggestions.append(
            "Include version control tools like Git and GitHub."
        )

    if "react" in missing_skills:
        suggestions.append(
            "Improve frontend development skills using React.js."
        )

    if "sql" in missing_skills:
        suggestions.append(
            "Strengthen database concepts and SQL query skills."
        )

    if len(suggestions) == 0:
        suggestions.append(
            "Resume aligns well with the provided job description."
        )

    return suggestions