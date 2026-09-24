import re


SECTION_KEYWORDS = {
    "education": [
        "education",
        "academic qualification",
        "academic background"
    ],
    "experience": [
        "experience",
        "work experience",
        "employment",
        "internship"
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects"
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies"
    ],
    "certifications": [
        "certification",
        "certifications",
        "certificate"
    ]
}


def contains_any(text: str, keywords: list[str]) -> bool:
    text_lower = text.lower()

    return any(
        keyword.lower() in text_lower
        for keyword in keywords
    )


def has_email(text: str) -> bool:
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    return bool(
        re.search(email_pattern, text)
    )


def has_phone(text: str) -> bool:
    phone_pattern = r"(\+?\d[\d\s\-()]{8,}\d)"

    return bool(
        re.search(phone_pattern, text)
    )


def has_linkedin(text: str) -> bool:
    """
    Detect LinkedIn even when the PDF contains only
    the visible hyperlink text.
    """

    text_lower = text.lower()

    linkedin_patterns = [
        r"linkedin\.com",
        r"linkedin\.com/in/",
        r"www\.linkedin\.com",
        r"\blinkedin\b",
        r"linkedin profile",
        r"linkedin url"
    ]

    return any(
        re.search(pattern, text_lower)
        for pattern in linkedin_patterns
    )


def has_github(text: str) -> bool:
    """
    Detect GitHub even when only the visible hyperlink
    text exists.
    """

    text_lower = text.lower()

    github_patterns = [
        r"github\.com",
        r"www\.github\.com",
        r"\bgithub\b",
        r"github profile",
        r"github url"
    ]

    return any(
        re.search(pattern, text_lower)
        for pattern in github_patterns
    )


def has_numbers_or_metrics(text: str) -> bool:
    metrics_pattern = r"\b\d+([.,]\d+)?%?\b"

    return bool(
        re.search(metrics_pattern, text)
    )


def calculate_ats_score(
    resume_text: str,
    extracted_skills: list[str]
) -> dict:
    if not resume_text:
        return {
            "score": 0,
            "checks": {},
            "strengths": [],
            "missing_sections": [],
            "suggestions": []
        }

    checks = {
        "email": has_email(resume_text),
        "phone": has_phone(resume_text),
        "linkedin": has_linkedin(resume_text),
        "github": has_github(resume_text),
        "education": contains_any(
            resume_text,
            SECTION_KEYWORDS["education"]
        ),
        "experience": contains_any(
            resume_text,
            SECTION_KEYWORDS["experience"]
        ),
        "projects": contains_any(
            resume_text,
            SECTION_KEYWORDS["projects"]
        ),
        "skills_section": contains_any(
            resume_text,
            SECTION_KEYWORDS["skills"]
        ),
        "certifications": contains_any(
            resume_text,
            SECTION_KEYWORDS["certifications"]
        ),
        "technical_skills": len(extracted_skills) >= 5,
        "measurable_achievements": has_numbers_or_metrics(
            resume_text
        ),
        "sufficient_length": len(
            resume_text.split()
        ) >= 250
    }

    weights = {
        "email": 5,
        "phone": 5,
        "linkedin": 5,
        "github": 5,
        "education": 10,
        "experience": 15,
        "projects": 10,
        "skills_section": 10,
        "certifications": 5,
        "technical_skills": 15,
        "measurable_achievements": 10,
        "sufficient_length": 5
    }

    score = sum(
        weights[key]
        for key, passed in checks.items()
        if passed
    )

    strengths = []
    missing_sections = []
    suggestions = []

    if checks["email"] and checks["phone"]:
        strengths.append(
            "Contact information is available"
        )
    else:
        missing_sections.append(
            "Complete contact information"
        )
        suggestions.append(
            "Add a valid email address and phone number."
        )

    if checks["linkedin"]:
        strengths.append(
            "LinkedIn profile is included"
        )
    else:
        missing_sections.append(
            "LinkedIn profile"
        )
        suggestions.append(
            "Add your LinkedIn profile URL."
        )

    if checks["github"]:
        strengths.append(
            "GitHub profile is included"
        )
    else:
        missing_sections.append(
            "GitHub profile"
        )
        suggestions.append(
            "Add your GitHub profile, especially for technical roles."
        )

    if checks["education"]:
        strengths.append(
            "Education section is present"
        )
    else:
        missing_sections.append(
            "Education section"
        )
        suggestions.append(
            "Add your education details with degree, institute and year."
        )

    if checks["experience"]:
        strengths.append(
            "Experience or internship section is present"
        )
    else:
        missing_sections.append(
            "Experience section"
        )
        suggestions.append(
            "Add internships, work experience or practical training."
        )

    if checks["projects"]:
        strengths.append(
            "Project section is present"
        )
    else:
        missing_sections.append(
            "Projects section"
        )
        suggestions.append(
            "Add relevant academic or personal projects."
        )

    if checks["technical_skills"]:
        strengths.append(
            f"{len(extracted_skills)} technical skills were detected"
        )
    else:
        missing_sections.append(
            "Sufficient technical skills"
        )
        suggestions.append(
            "Add more role-relevant technical skills."
        )

    if checks["certifications"]:
        strengths.append(
            "Certifications are included"
        )
    else:
        missing_sections.append(
            "Certifications section"
        )
        suggestions.append(
            "Add relevant certifications or completed courses."
        )

    if checks["measurable_achievements"]:
        strengths.append(
            "Resume contains measurable results"
        )
    else:
        suggestions.append(
            "Use measurable achievements such as percentages, counts or performance improvements."
        )

    if not checks["sufficient_length"]:
        suggestions.append(
            "Add more relevant details. The resume content appears too short."
        )

    if score >= 80:
        rating = "Excellent"
    elif score >= 65:
        rating = "Good"
    elif score >= 50:
        rating = "Average"
    else:
        rating = "Needs Improvement"

    return {
        "score": score,
        "rating": rating,
        "checks": checks,
        "strengths": strengths,
        "missing_sections": missing_sections,
        "suggestions": suggestions
    }