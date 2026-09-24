import json
import re
from typing import Any


ACTION_VERBS = [
    "developed",
    "built",
    "implemented",
    "designed",
    "created",
    "optimized",
    "automated",
    "deployed",
    "integrated",
    "managed",
    "analyzed",
    "improved",
    "reduced",
    "increased",
    "led",
    "collaborated"
]


# Similar ATS recommendations are mapped to one
# standard suggestion key.
SUGGESTION_ALIASES = {
    "linkedin": [
        "linkedin",
        "linkedin profile",
        "linkedin profile url",
        "linkedin url"
    ],
    "github": [
        "github",
        "github profile",
        "github profile url",
        "github url"
    ],
    "certifications": [
        "certification",
        "certifications",
        "certificate",
        "completed courses"
    ],
    "projects": [
        "project section",
        "projects section",
        "technical projects",
        "academic projects",
        "personal projects"
    ],
    "technical_skills": [
        "technical skills",
        "role-relevant technical skills",
        "sufficient technical skills",
        "skills section"
    ],
    "education": [
        "education",
        "education section",
        "academic qualification",
        "academic background"
    ],
    "experience": [
        "experience",
        "experience section",
        "internship",
        "work experience",
        "practical training"
    ],
    "contact": [
        "contact information",
        "email address",
        "phone number"
    ],
    "metrics": [
        "measurable achievement",
        "measurable achievements",
        "percentages",
        "performance improvements",
        "quantify",
        "numbers"
    ],
    "resume_length": [
        "resume content appears too short",
        "resume appears too short",
        "add more relevant details",
        "sufficient length"
    ]
}


def normalize_list(
    value: Any
) -> list[str]:
    """
    Convert JSON strings or Python lists into a clean,
    unique list of strings.
    """

    if not value:
        return []

    parsed_value = value

    if isinstance(value, str):
        try:
            parsed_value = json.loads(
                value
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):
            return []

    if not isinstance(
        parsed_value,
        list
    ):
        return []

    cleaned_items = []
    seen_items = set()

    for item in parsed_value:
        clean_item = str(
            item
        ).strip()

        normalized_item = (
            clean_item.lower()
        )

        if (
            clean_item
            and normalized_item
            not in seen_items
        ):
            cleaned_items.append(
                clean_item
            )

            seen_items.add(
                normalized_item
            )

    return cleaned_items


def contains_action_verbs(
    resume_text: str
) -> bool:
    text = resume_text.lower()

    return any(
        re.search(
            rf"\b{re.escape(verb)}\b",
            text
        )
        for verb in ACTION_VERBS
    )


def contains_metrics(
    resume_text: str
) -> bool:
    """
    Detect meaningful numbers, counts, percentages
    and measurable outcomes.

    Dates and phone numbers may still contain digits,
    so percentage/count patterns are checked first.
    """

    patterns = [
        r"\b\d+(\.\d+)?\s*%",
        r"\b\d+\+\s*(users|clients|projects|applications|workflows|records|websites|dashboards)",
        r"\b\d+\s+(users|clients|projects|applications|workflows|records|websites|dashboards)",
        r"\b(reduced|increased|improved|saved|processed|served|managed)\s+.*?\d+",
        r"\b\d+\s*(hours?|days?|minutes?)\s+(saved|reduced)",
        r"\b\d+x\b"
    ]

    return any(
        re.search(
            pattern,
            resume_text,
            flags=re.IGNORECASE
        )
        for pattern in patterns
    )


def create_priority(
    severity: str
) -> int:
    priorities = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    return priorities.get(
        severity,
        3
    )


def normalize_text(
    value: str
) -> str:
    """
    Normalize text for duplicate comparison.
    """

    normalized = str(
        value
    ).lower()

    normalized = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        normalized
    )

    normalized = re.sub(
        r"\b(your|the|a|an|relevant|especially|please)\b",
        " ",
        normalized
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    )

    return normalized.strip()


def get_suggestion_group(
    text: str
) -> str:
    """
    Return a semantic group for similar suggestions.

    Examples:
    - Add LinkedIn profile
    - Add your LinkedIn profile URL

    Both become:
    linkedin
    """

    normalized = normalize_text(
        text
    )

    for group, phrases in (
        SUGGESTION_ALIASES.items()
    ):
        for phrase in phrases:
            if normalize_text(
                phrase
            ) in normalized:
                return group

    return normalized


def get_satisfied_groups(
    checks: dict[str, Any],
    resume_text: str
) -> set[str]:
    """
    Identify recommendations that are already satisfied.
    """

    satisfied = set()

    check_to_group = {
        "linkedin": "linkedin",
        "github": "github",
        "certifications": "certifications",
        "projects": "projects",
        "technical_skills": "technical_skills",
        "education": "education",
        "experience": "experience",
        "sufficient_length": "resume_length"
    }

    for check_name, group in (
        check_to_group.items()
    ):
        if checks.get(
            check_name,
            False
        ):
            satisfied.add(
                group
            )

    if (
        checks.get("email")
        and checks.get("phone")
    ):
        satisfied.add(
            "contact"
        )

    if contains_metrics(
        resume_text
    ):
        satisfied.add(
            "metrics"
        )

    return satisfied


def create_suggestion(
    *,
    category: str,
    title: str,
    description: str,
    severity: str,
    impact: str,
    example: str | None = None,
    group: str | None = None
) -> dict[str, Any]:
    """
    Create one standard suggestion object.
    """

    return {
        "category": category,
        "title": title,
        "description": description,
        "severity": severity,
        "priority": create_priority(
            severity
        ),
        "impact": impact,
        "example": example,
        "_group": (
            group
            or get_suggestion_group(
                title
            )
        )
    }


def clean_missing_sections(
    missing_sections: list[str],
    satisfied_groups: set[str]
) -> list[str]:
    """
    Remove missing sections that are already detected.
    """

    cleaned_sections = []
    seen_groups = set()

    for section in missing_sections:
        group = get_suggestion_group(
            section
        )

        if group in satisfied_groups:
            continue

        if group in seen_groups:
            continue

        cleaned_sections.append(
            section
        )

        seen_groups.add(
            group
        )

    return cleaned_sections


def merge_unique_suggestions(
    suggestions: list[dict[str, Any]],
    satisfied_groups: set[str]
) -> list[dict[str, Any]]:
    """
    Remove semantic duplicates and recommendations
    that are already satisfied.

    When two suggestions belong to the same group,
    the higher-priority suggestion is retained.
    """

    selected_by_group = {}

    for suggestion in suggestions:
        group = (
            suggestion.get("_group")
            or get_suggestion_group(
                suggestion.get(
                    "title",
                    ""
                )
            )
        )

        if group in satisfied_groups:
            continue

        suggestion[
            "_group"
        ] = group

        existing = selected_by_group.get(
            group
        )

        if existing is None:
            selected_by_group[
                group
            ] = suggestion

            continue

        existing_priority = int(
            existing.get(
                "priority",
                3
            )
            or 3
        )

        new_priority = int(
            suggestion.get(
                "priority",
                3
            )
            or 3
        )

        # Keep the suggestion with the higher priority.
        if new_priority < existing_priority:
            selected_by_group[
                group
            ] = suggestion

            continue

        # If priority is equal, keep the one with the
        # more useful description and example.
        if new_priority == existing_priority:
            existing_quality = (
                len(
                    str(
                        existing.get(
                            "description",
                            ""
                        )
                    )
                )
                + len(
                    str(
                        existing.get(
                            "example",
                            ""
                        )
                    )
                )
            )

            new_quality = (
                len(
                    str(
                        suggestion.get(
                            "description",
                            ""
                        )
                    )
                )
                + len(
                    str(
                        suggestion.get(
                            "example",
                            ""
                        )
                    )
                )
            )

            if new_quality > existing_quality:
                selected_by_group[
                    group
                ] = suggestion

    unique_suggestions = list(
        selected_by_group.values()
    )

    unique_suggestions.sort(
        key=lambda item: (
            int(
                item.get(
                    "priority",
                    3
                )
                or 3
            ),
            str(
                item.get(
                    "category",
                    ""
                )
            ).lower(),
            str(
                item.get(
                    "title",
                    ""
                )
            ).lower()
        )
    )

    # Internal group key must not be sent to Pydantic.
    for suggestion in unique_suggestions:
        suggestion.pop(
            "_group",
            None
        )

    return unique_suggestions


def build_resume_improvements(
    *,
    resume_text: str,
    extracted_skills: list[str],
    ats_analysis: dict[str, Any],
    target_career: str | None,
    skill_gap_analysis: dict[str, Any]
) -> dict[str, Any]:
    if not resume_text.strip():
        raise ValueError(
            "Resume text is empty."
        )

    suggestions = []

    if not isinstance(
        ats_analysis,
        dict
    ):
        ats_analysis = {}

    if not isinstance(
        skill_gap_analysis,
        dict
    ):
        skill_gap_analysis = {}

    checks = ats_analysis.get(
        "checks",
        {}
    )

    if not isinstance(
        checks,
        dict
    ):
        checks = {}

    try:
        ats_score = int(
            ats_analysis.get(
                "score",
                0
            )
            or 0
        )

    except (
        TypeError,
        ValueError
    ):
        ats_score = 0

    ats_score = min(
        max(
            ats_score,
            0
        ),
        100
    )

    missing_sections = normalize_list(
        ats_analysis.get(
            "missing_sections"
        )
    )

    existing_suggestions = normalize_list(
        ats_analysis.get(
            "suggestions"
        )
    )

    missing_skills = normalize_list(
        skill_gap_analysis.get(
            "missing_skills"
        )
    )

    priority_skills = normalize_list(
        skill_gap_analysis.get(
            "priority_skills"
        )
    )

    satisfied_groups = (
        get_satisfied_groups(
            checks,
            resume_text
        )
    )

    missing_sections = (
        clean_missing_sections(
            missing_sections,
            satisfied_groups
        )
    )

    # ------------------------------------------
    # Professional links
    # ------------------------------------------

    if not checks.get(
        "linkedin",
        False
    ):
        suggestions.append(
            create_suggestion(
                category=(
                    "Contact and Professional "
                    "Presence"
                ),
                title=(
                    "Add your LinkedIn profile"
                ),
                description=(
                    "Include a complete LinkedIn URL "
                    "near your email and phone number. "
                    "Keep the profile headline and "
                    "skills consistent with your resume."
                ),
                severity="high",
                impact=(
                    "Improves recruiter trust and ATS "
                    "profile completeness."
                ),
                example=(
                    "LinkedIn: "
                    "linkedin.com/in/your-profile"
                ),
                group="linkedin"
            )
        )

    if not checks.get(
        "github",
        False
    ):
        suggestions.append(
            create_suggestion(
                category="Technical Profile",
                title="Add your GitHub profile",
                description=(
                    "Include a GitHub URL and pin "
                    "projects that are relevant to "
                    "your selected career."
                ),
                severity="high",
                impact=(
                    "Demonstrates practical technical "
                    "ability to recruiters."
                ),
                example=(
                    "GitHub: "
                    "github.com/your-username"
                ),
                group="github"
            )
        )

    # ------------------------------------------
    # Main resume sections
    # ------------------------------------------

    if not checks.get(
        "certifications",
        False
    ):
        suggestions.append(
            create_suggestion(
                category="Certifications",
                title=(
                    "Add a certifications section"
                ),
                description=(
                    "Include relevant certifications "
                    "and completed courses with the "
                    "provider and completion year."
                ),
                severity="medium",
                impact=(
                    "Strengthens credibility for "
                    "fresher and entry-level roles."
                ),
                example=(
                    "AWS Cloud Practitioner — "
                    "Amazon Web Services, 2026"
                ),
                group="certifications"
            )
        )

    if not checks.get(
        "projects",
        False
    ):
        suggestions.append(
            create_suggestion(
                category="Projects",
                title=(
                    "Add relevant technical projects"
                ),
                description=(
                    "Include two or three projects "
                    "with the technology stack, your "
                    "contribution, the problem solved "
                    "and a measurable result."
                ),
                severity="high",
                impact=(
                    "Shows practical application of "
                    "your technical skills."
                ),
                example=(
                    "Built a FastAPI career-analysis "
                    "platform using React, PostgreSQL "
                    "and JWT authentication."
                ),
                group="projects"
            )
        )

    # ------------------------------------------
    # Writing quality
    # ------------------------------------------

    if not contains_action_verbs(
        resume_text
    ):
        suggestions.append(
            create_suggestion(
                category="Writing Quality",
                title=(
                    "Start bullet points with "
                    "strong action verbs"
                ),
                description=(
                    "Use strong action verbs instead "
                    "of passive sentences. Explain "
                    "what you built, improved, "
                    "automated or delivered."
                ),
                severity="medium",
                impact=(
                    "Makes achievements clearer and "
                    "more persuasive."
                ),
                example=(
                    "Developed, automated, "
                    "implemented, deployed, "
                    "optimized and analyzed."
                ),
                group="action_verbs"
            )
        )

    if not contains_metrics(
        resume_text
    ):
        suggestions.append(
            create_suggestion(
                category="Achievements",
                title=(
                    "Add measurable achievements"
                ),
                description=(
                    "Quantify your work using "
                    "percentages, counts, users, time "
                    "saved, workflows automated or "
                    "performance improvements."
                ),
                severity="high",
                impact=(
                    "Makes your experience more "
                    "credible and results-focused."
                ),
                example=(
                    "Automated 5 business workflows "
                    "and reduced manual processing "
                    "time by 40%."
                ),
                group="metrics"
            )
        )

    # ------------------------------------------
    # Technical skills
    # ------------------------------------------

    if len(extracted_skills) < 8:
        suggestions.append(
            create_suggestion(
                category="Technical Skills",
                title=(
                    "Expand and organize your "
                    "technical skills"
                ),
                description=(
                    "Group skills into programming "
                    "languages, frameworks, databases, "
                    "cloud platforms and tools."
                ),
                severity="medium",
                impact=(
                    "Helps ATS systems identify more "
                    "role-relevant keywords."
                ),
                example=(
                    "Programming: Python, JavaScript | "
                    "Frameworks: React, FastAPI | "
                    "Databases: PostgreSQL, MongoDB"
                ),
                group="technical_skills"
            )
        )

    if priority_skills:
        skill_text = ", ".join(
            priority_skills[:6]
        )

        suggestions.append(
            create_suggestion(
                category="Career Alignment",
                title=(
                    "Develop the priority skills for "
                    f"{target_career or 'your target career'}"
                ),
                description=(
                    "The most important missing "
                    f"skills are: {skill_text}."
                ),
                severity="high",
                impact=(
                    "Improves career readiness and "
                    "job-description compatibility."
                ),
                example=(
                    "Complete practical projects "
                    "demonstrating these skills before "
                    "adding them to your resume."
                ),
                group="career_skills"
            )
        )

    elif missing_skills:
        skill_text = ", ".join(
            missing_skills[:6]
        )

        suggestions.append(
            create_suggestion(
                category="Career Alignment",
                title=(
                    "Address the remaining career "
                    "skill gaps"
                ),
                description=(
                    "Consider learning and "
                    f"demonstrating: {skill_text}."
                ),
                severity="medium",
                impact=(
                    "Improves alignment with your "
                    "recommended career."
                ),
                example=(
                    "Add these skills only after "
                    "completing practical work."
                ),
                group="career_skills"
            )
        )

    # ------------------------------------------
    # Career-focused summary
    # ------------------------------------------

    if target_career:
        suggestions.append(
            create_suggestion(
                category="Professional Summary",
                title=(
                    "Customize your professional "
                    "summary"
                ),
                description=(
                    "Align your summary with the "
                    f"{target_career} role. Mention "
                    "your strongest skills, practical "
                    "experience and career objective."
                ),
                severity="medium",
                impact=(
                    "Creates a clear role-focused "
                    "first impression."
                ),
                example=(
                    f"Entry-level {target_career} "
                    "with practical experience in "
                    "building scalable and "
                    "data-driven applications."
                ),
                group="professional_summary"
            )
        )

    # ------------------------------------------
    # Resume length
    # ------------------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count > 900:
        suggestions.append(
            create_suggestion(
                category="Resume Length",
                title=(
                    "Reduce unnecessary resume "
                    "content"
                ),
                description=(
                    "Remove repetitive or low-value "
                    "details and retain the most "
                    "relevant experience."
                ),
                severity="medium",
                impact=(
                    "Makes the resume easier for "
                    "recruiters to scan."
                ),
                example=(
                    "Keep fresher resumes close to "
                    "one page where practical."
                ),
                group="resume_length"
            )
        )

    elif word_count < 250:
        suggestions.append(
            create_suggestion(
                category="Resume Content",
                title=(
                    "Add more relevant resume detail"
                ),
                description=(
                    "Add project contributions, "
                    "technical responsibilities, "
                    "achievements and relevant "
                    "coursework."
                ),
                severity="high",
                impact=(
                    "Provides sufficient information "
                    "for recruiters and ATS systems."
                ),
                example=(
                    "Add two to four "
                    "achievement-focused bullets "
                    "under every project or "
                    "internship."
                ),
                group="resume_length"
            )
        )

    # ------------------------------------------
    # ATS recommendations
    # ------------------------------------------

    for existing in existing_suggestions:
        group = get_suggestion_group(
            existing
        )

        # Ignore advice already satisfied by the
        # updated ATS checks.
        if group in satisfied_groups:
            continue

        suggestions.append(
            create_suggestion(
                category="ATS Recommendation",
                title=existing,
                description=(
                    "This recommendation was "
                    "identified during your ATS "
                    "resume analysis."
                ),
                severity="medium",
                impact=(
                    "Improves ATS compatibility and "
                    "resume completeness."
                ),
                example=None,
                group=group
            )
        )

    unique_suggestions = (
        merge_unique_suggestions(
            suggestions,
            satisfied_groups
        )
    )

    high_priority_count = sum(
        1
        for item in unique_suggestions
        if item["severity"] == "high"
    )

    medium_priority_count = sum(
        1
        for item in unique_suggestions
        if item["severity"] == "medium"
    )

    low_priority_count = sum(
        1
        for item in unique_suggestions
        if item["severity"] == "low"
    )

    potential_score = min(
        100,
        ats_score
        + high_priority_count * 5
        + medium_priority_count * 2
        + low_priority_count
    )

    if ats_score >= 80:
        summary = (
            "Your resume is already strong. "
            "Focus on role-specific keywords, "
            "measurable achievements and targeted "
            "career improvements."
        )

    elif ats_score >= 60:
        summary = (
            "Your resume has a good foundation, "
            "but several targeted improvements can "
            "increase ATS compatibility and "
            "recruiter impact."
        )

    else:
        summary = (
            "Your resume requires important "
            "structural and content improvements "
            "before applying to competitive roles."
        )

    return {
        "current_ats_score":
            ats_score,

        "potential_ats_score":
            potential_score,

        "target_career":
            target_career,

        "summary":
            summary,

        "total_suggestions":
            len(unique_suggestions),

        "high_priority_count":
            high_priority_count,

        "medium_priority_count":
            medium_priority_count,

        "low_priority_count":
            low_priority_count,

        "missing_sections":
            missing_sections,

        "priority_skills":
            priority_skills,

        "suggestions":
            unique_suggestions
    }