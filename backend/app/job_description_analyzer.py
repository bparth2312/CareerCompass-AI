import re
from collections import Counter
from typing import Any

from app.skill_extractor import extract_skills


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "that",
    "the",
    "their",
    "this",
    "to",
    "we",
    "will",
    "with",
    "you",
    "your",
    "candidate",
    "job",
    "role",
    "position",
    "work",
    "working",
    "responsible",
    "responsibilities",
    "requirements",
    "required",
    "preferred",
    "looking"
}


IMPORTANT_JOB_TERMS = {
    "develop",
    "design",
    "build",
    "maintain",
    "deploy",
    "test",
    "debug",
    "optimize",
    "integrate",
    "analyze",
    "manage",
    "implement",
    "monitor",
    "collaborate",
    "scalable",
    "security",
    "performance",
    "database",
    "frontend",
    "backend",
    "api",
    "cloud",
    "automation",
    "machine learning",
    "data analysis",
    "problem solving",
    "communication",
    "teamwork",
    "leadership"
}


def normalize_skill(skill: str) -> str:
    """
    Normalize skill names for case-insensitive matching.
    """

    return re.sub(
        r"\s+",
        " ",
        str(skill).strip().lower()
    )


def clean_skill_list(
    skills: list[str]
) -> list[str]:
    """
    Remove empty and duplicate skill names.
    """

    cleaned_skills = []
    seen_skills = set()

    for skill in skills:
        clean_skill = str(skill).strip()
        normalized_skill = normalize_skill(
            clean_skill
        )

        if (
            clean_skill
            and normalized_skill
            not in seen_skills
        ):
            cleaned_skills.append(
                clean_skill
            )

            seen_skills.add(
                normalized_skill
            )

    return cleaned_skills


def extract_keywords(
    text: str,
    limit: int = 20
) -> list[str]:
    """
    Extract frequently occurring meaningful words
    from a job description.
    """

    words = re.findall(
        r"[A-Za-z][A-Za-z0-9+#.\-]{2,}",
        text.lower()
    )

    filtered_words = [
        word
        for word in words
        if word not in STOP_WORDS
        and not word.isdigit()
    ]

    word_counts = Counter(
        filtered_words
    )

    return [
        word
        for word, _ in
        word_counts.most_common(limit)
    ]


def find_matching_keywords(
    resume_text: str,
    job_keywords: list[str]
) -> tuple[list[str], list[str]]:
    """
    Compare important job keywords with resume text.
    """

    normalized_resume = (
        resume_text.lower()
    )

    matched_keywords = []
    missing_keywords = []

    for keyword in job_keywords:
        if keyword.lower() in normalized_resume:
            matched_keywords.append(
                keyword
            )
        else:
            missing_keywords.append(
                keyword
            )

    return (
        matched_keywords,
        missing_keywords
    )


def detect_experience_requirement(
    job_description: str
) -> str | None:
    """
    Detect experience requirements such as:
    2 years, 3+ years, 1-2 years.
    """

    patterns = [
        r"\b\d+\s*\+\s*years?\b",
        r"\b\d+\s*-\s*\d+\s*years?\b",
        r"\b\d+\s+to\s+\d+\s+years?\b",
        r"\bminimum\s+of\s+\d+\s+years?\b",
        r"\bat\s+least\s+\d+\s+years?\b",
        r"\b\d+\s+years?\s+of\s+experience\b"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            job_description,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(0)

    return None


def calculate_percentage(
    matched_count: int,
    total_count: int
) -> int:
    if total_count <= 0:
        return 0

    return round(
        matched_count
        / total_count
        * 100
    )


def get_match_level(
    score: int
) -> str:
    if score >= 80:
        return "Excellent Match"

    if score >= 65:
        return "Good Match"

    if score >= 50:
        return "Moderate Match"

    if score >= 35:
        return "Low Match"

    return "Poor Match"


def get_application_status(
    score: int
) -> str:
    if score >= 75:
        return "Ready to Apply"

    if score >= 55:
        return "Apply After Improvements"

    return "More Preparation Required"


def build_suggestions(
    *,
    missing_skills: list[str],
    missing_keywords: list[str],
    resume_text: str,
    experience_requirement: str | None
) -> list[str]:
    suggestions = []

    if missing_skills:
        skill_text = ", ".join(
            missing_skills[:6]
        )

        suggestions.append(
            "Add or learn the following job-relevant "
            f"skills: {skill_text}."
        )

    if missing_keywords:
        keyword_text = ", ".join(
            missing_keywords[:6]
        )

        suggestions.append(
            "Use relevant job-description keywords "
            f"naturally in your resume: {keyword_text}."
        )

    if experience_requirement:
        suggestions.append(
            "The job description mentions an experience "
            f"requirement of '{experience_requirement}'. "
            "Highlight internships, projects and practical "
            "experience that support this requirement."
        )

    if not re.search(
        r"\b\d+([.,]\d+)?%?\b",
        resume_text
    ):
        suggestions.append(
            "Add measurable achievements using numbers, "
            "percentages, performance improvements or "
            "project results."
        )

    if "project" not in resume_text.lower():
        suggestions.append(
            "Add relevant projects that demonstrate the "
            "skills required by this job."
        )

    if not suggestions:
        suggestions.append(
            "Your resume aligns well with this role. "
            "Customize your professional summary and most "
            "relevant project descriptions before applying."
        )

    return suggestions


def analyze_resume_against_job(
    *,
    resume_text: str,
    resume_skills: list[str],
    job_description: str,
    job_title: str | None = None
) -> dict[str, Any]:
    """
    Compare an analyzed resume against a job description.

    Score distribution:
    - Skills match: 70%
    - Keyword match: 20%
    - Resume quality and experience relevance: 10%
    """

    if not resume_text.strip():
        raise ValueError(
            "Resume text is empty."
        )

    if not job_description.strip():
        raise ValueError(
            "Job description is required."
        )

    clean_resume_skills = clean_skill_list(
        resume_skills
    )

    job_skills = clean_skill_list(
        extract_skills(
            job_description
        )
    )

    resume_skill_map = {
        normalize_skill(skill): skill
        for skill in clean_resume_skills
    }

    job_skill_map = {
        normalize_skill(skill): skill
        for skill in job_skills
    }

    matched_skill_keys = (
        set(resume_skill_map)
        & set(job_skill_map)
    )

    missing_skill_keys = (
        set(job_skill_map)
        - set(resume_skill_map)
    )

    matched_skills = sorted(
        job_skill_map[key]
        for key in matched_skill_keys
    )

    missing_skills = sorted(
        job_skill_map[key]
        for key in missing_skill_keys
    )

    skill_match_percentage = (
        calculate_percentage(
            len(matched_skills),
            len(job_skills)
        )
        if job_skills
        else 0
    )

    extracted_keywords = extract_keywords(
        job_description,
        limit=20
    )

    important_keywords = []

    for keyword in extracted_keywords:
        if (
            keyword in IMPORTANT_JOB_TERMS
            or len(keyword) >= 5
        ):
            important_keywords.append(
                keyword
            )

    important_keywords = (
        important_keywords[:12]
    )

    (
        matched_keywords,
        missing_keywords
    ) = find_matching_keywords(
        resume_text,
        important_keywords
    )

    keyword_match_percentage = (
        calculate_percentage(
            len(matched_keywords),
            len(important_keywords)
        )
        if important_keywords
        else 0
    )

    experience_requirement = (
        detect_experience_requirement(
            job_description
        )
    )

    quality_score = 0

    if len(resume_text.split()) >= 250:
        quality_score += 4

    if re.search(
        r"\b\d+([.,]\d+)?%?\b",
        resume_text
    ):
        quality_score += 3

    if any(
        section in resume_text.lower()
        for section in [
            "experience",
            "internship",
            "projects"
        ]
    ):
        quality_score += 3

    overall_score = round(
        skill_match_percentage * 0.70
        + keyword_match_percentage * 0.20
        + quality_score
    )

    overall_score = min(
        max(overall_score, 0),
        100
    )

    suggestions = build_suggestions(
        missing_skills=missing_skills,
        missing_keywords=missing_keywords,
        resume_text=resume_text,
        experience_requirement=
            experience_requirement
    )

    strengths = []

    if matched_skills:
        strengths.append(
            f"{len(matched_skills)} required technical "
            "skills were found in the resume."
        )

    if keyword_match_percentage >= 60:
        strengths.append(
            "The resume contains several important "
            "keywords from the job description."
        )

    if quality_score >= 7:
        strengths.append(
            "The resume contains sufficient detail, "
            "experience or measurable information."
        )

    if not strengths:
        strengths.append(
            "The resume provides a base profile that can "
            "be improved for this job."
        )

    return {
        "job_title": (
            job_title.strip()
            if job_title
            and job_title.strip()
            else "Selected Job"
        ),
        "overall_match_score":
            overall_score,
        "match_level":
            get_match_level(
                overall_score
            ),
        "application_status":
            get_application_status(
                overall_score
            ),
        "skill_match_percentage":
            skill_match_percentage,
        "keyword_match_percentage":
            keyword_match_percentage,
        "resume_quality_score":
            quality_score,
        "resume_skills":
            clean_resume_skills,
        "required_skills":
            job_skills,
        "matched_skills":
            matched_skills,
        "missing_skills":
            missing_skills,
        "important_keywords":
            important_keywords,
        "matched_keywords":
            matched_keywords,
        "missing_keywords":
            missing_keywords,
        "experience_requirement":
            experience_requirement,
        "strengths":
            strengths,
        "suggestions":
            suggestions,
        "matched_skill_count":
            len(matched_skills),
        "missing_skill_count":
            len(missing_skills),
        "required_skill_count":
            len(job_skills)
    }