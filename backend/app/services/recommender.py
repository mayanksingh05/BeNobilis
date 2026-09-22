from typing import List, Dict, Optional
from app.utils.skill_db import get_skill_category


TEMPLATES = {
    "Programming": [
        "Consider adding coursework, certifications, or projects highlighting '{skill}' to strengthen your core coding background.",
        "Feature any practical applications or repositories involving '{skill}' prominently in your technical skills section.",
        "Demonstrate how you solved real-world problems using '{skill}' in your project bullet points."
    ],
    "Frontend": [
        "Showcase user-interface or interactive web applications built with '{skill}'.",
        "Highlight your experience with modern UI/UX patterns using '{skill}'.",
        "Mention state management or component design involving '{skill}'."
    ],
    "Backend": [
        "Highlight API design, microservices, or server architecture implemented using '{skill}'.",
        "If you have built backend services or endpoints with '{skill}', specify their throughput or business impact.",
        "Demonstrate server-side architecture and data flow using '{skill}'."
    ],
    "Database": [
        "Include hands-on experience designing schemas, queries, or indexing in '{skill}'.",
        "Mention performance optimization or data migrations carried out with '{skill}'.",
        "Adding practical database projects using '{skill}' will significantly improve alignment."
    ],
    "DevOps": [
        "Highlight CI/CD pipelines, container orchestration, or automation involving '{skill}'.",
        "Showcase how you automated deployments or monitoring with '{skill}'.",
        "Demonstrate infrastructure reliability or workflow efficiency achieved through '{skill}'."
    ],
    "Cloud": [
        "Mention any cloud architecture, hosting, or resource management using '{skill}'.",
        "Highlight cloud security, scaling, or storage services utilized within '{skill}'.",
        "Add relevant cloud-native deployments using '{skill}' to your experience."
    ],
    "AI / ML": [
        "Highlight machine learning models, feature engineering, or training pipelines built with '{skill}'.",
        "Mention model metrics (accuracy, latency, F1-score) achieved using '{skill}'.",
        "Showcase practical AI/ML projects or research utilizing '{skill}'."
    ],
    "Data Science": [
        "Demonstrate data analysis, visualization, or ETL workflows created with '{skill}'.",
        "Highlight actionable insights derived from data processing using '{skill}'.",
        "Feature analytics dashboards or statistical modeling involving '{skill}'."
    ],
    "APIs & Services": [
        "Detail web services or third-party integrations developed using '{skill}'.",
        "Mention API documentation, authentication, or contract testing with '{skill}'.",
        "Showcase secure, RESTful or event-driven communication utilizing '{skill}'."
    ],
    "Security": [
        "Highlight security audits, encryption, or authentication protocols implemented with '{skill}'.",
        "Mention compliance, vulnerability prevention, or secure coding practices in '{skill}'.",
        "Feature experience securing distributed systems against common threats using '{skill}'."
    ],
    "Testing & QA": [
        "Highlight automated test suites, unit tests, or end-to-end testing written using '{skill}'.",
        "Mention code coverage improvements or bug reduction achieved through '{skill}'.",
        "Demonstrate quality assurance workflows or regression suites using '{skill}'."
    ],
    "Mobile": [
        "Showcase native or cross-platform mobile apps deployed using '{skill}'.",
        "Highlight mobile responsiveness, lifecycle management, or store publication using '{skill}'.",
        "Mention offline storage or push notification systems built with '{skill}'."
    ],
    "Version Control": [
        "Highlight collaboration workflows (feature branching, code reviews, PRs) using '{skill}'.",
        "Mention repository governance or release management using '{skill}'."
    ],
    "Operating Systems": [
        "Mention system administration, scripting, or environment configuration in '{skill}'.",
        "Highlight server deployment and CLI proficiency within '{skill}'."
    ],
    "Developer Tools": [
        "Highlight proficiency with modern engineering toolchains like '{skill}'.",
        "Showcase development speed or debugging efficiency gained through '{skill}'."
    ],
    "Software Architecture": [
        "Detail how you applied '{skill}' to improve system maintainability and scalability.",
        "Highlight architectural patterns or modular design using '{skill}'."
    ],
    "Networking": [
        "Mention protocol understanding, reverse proxying, or network configurations using '{skill}'.",
        "Highlight socket programming or low-latency networking with '{skill}'."
    ],
    "Other": [
        "Consider including exposure to '{skill}' if it aligns with your technical background.",
        "Highlight any hands-on experience involving '{skill}' to better match the job description."
    ]
}


def generate_suggestions(
    missing_skills: List[str],
    sections: Optional[Dict[str, bool]] = None
) -> List[str]:
    """
    Generate tailored, natural ATS improvement recommendations
    based on missing skills across all 17 categories and resume structure.
    """
    suggestions = []

    # 1. Structural advice if critical resume sections are missing
    if sections:
        if not sections.get("projects", True):
            suggestions.append(
                "Add a dedicated 'Projects' or 'Portfolio' section showcasing 2-3 key technical builds."
            )
        if not sections.get("skills", True):
            suggestions.append(
                "Create a distinct 'Technical Skills' section organized by category for faster ATS parsing."
            )

    # 2. Skill-specific recommendations
    if not missing_skills and not suggestions:
        return [
            "Excellent match! Your resume already captures the required technical skills. "
            "Ensure your bullet points quantify your business impact (e.g. percentages, metrics, scale)."
        ]

    for index, skill in enumerate(missing_skills[:5]):
        category = get_skill_category(skill)
        options = TEMPLATES.get(category, TEMPLATES["Other"])
        suggestion = options[index % len(options)].format(skill=skill)
        suggestions.append(suggestion)

    return suggestions