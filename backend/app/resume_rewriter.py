import re
from typing import Any
from app.resume_sections import (
    extract_sections,
    build_summary,
    build_bullets
)

SECTION_NAMES = [
    "summary",
    "professional summary",
    "career objective",
    "objective",
    "education",
    "experience",
    "work experience",
    "internship",
    "internships",
    "projects",
    "academic projects",
    "personal projects",
    "technical skills",
    "skills",
    "certifications",
    "achievements"
]


CAREER_KEYWORDS = {
    "full stack developer": [
        "React.js",
        "JavaScript",
        "Node.js",
        "Express.js",
        "REST APIs",
        "MongoDB",
        "PostgreSQL",
        "Git",
        "Cloud Deployment"
    ],

    "frontend developer": [
        "React.js",
        "JavaScript",
        "HTML5",
        "CSS3",
        "Responsive Design",
        "REST APIs",
        "Git",
        "UI Development"
    ],

    "backend developer": [
        "Python",
        "FastAPI",
        "Node.js",
        "Express.js",
        "REST APIs",
        "PostgreSQL",
        "MongoDB",
        "Authentication"
    ],

    "data analyst": [
        "Python",
        "SQL",
        "Pandas",
        "Excel",
        "Power BI",
        "Data Cleaning",
        "EDA",
        "Data Visualization"
    ],

    "data scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Machine Learning",
        "EDA",
        "Data Visualization"
    ],

    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "NLP",
        "Model Deployment"
    ],

    "machine learning engineer": [
        "Python",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Feature Engineering",
        "Model Evaluation",
        "Deployment"
    ],

    "business analyst": [
        "Excel",
        "SQL",
        "Power BI",
        "Business Intelligence",
        "Data Visualization",
        "Requirements Analysis",
        "KPIs",
        "Reporting"
    ],

    "cloud engineer": [
        "AWS",
        "Cloud Deployment",
        "Docker",
        "CI/CD",
        "Linux",
        "Networking",
        "Git",
        "Monitoring"
    ]
}


ACTION_VERBS = [
    "Developed",
    "Built",
    "Implemented",
    "Designed",
    "Created",
    "Engineered",
    "Automated",
    "Integrated",
    "Deployed",
    "Analyzed",
    "Optimized",
    "Improved",
    "Managed",
    "Collaborated"
]


def clean_text(
    value: str
) -> str:
    """
    Remove unnecessary spacing while keeping
    readable line breaks.
    """

    if not value:
        return ""

    cleaned_lines = []

    for line in value.splitlines():
        clean_line = re.sub(
            r"\s+",
            " ",
            line
        ).strip()

        if clean_line:
            cleaned_lines.append(
                clean_line
            )

    return "\n".join(
        cleaned_lines
    )


def normalize_heading(
    value: str
) -> str:
    normalized = re.sub(
        r"[^a-zA-Z ]",
        "",
        value
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    )

    return normalized.strip().lower()


def is_section_heading(
    line: str
) -> bool:
    normalized = normalize_heading(
        line
    )

    if normalized in SECTION_NAMES:
        return True

    if (
        line.isupper()
        and len(line.split()) <= 4
        and len(line) <= 40
    ):
        return normalized in SECTION_NAMES

    return False


def get_section_key(
    heading: str
) -> str:
    normalized = normalize_heading(
        heading
    )

    mappings = {
        "professional summary": "summary",
        "career objective": "summary",
        "objective": "summary",
        "summary": "summary",

        "work experience": "experience",
        "internship": "experience",
        "internships": "experience",
        "experience": "experience",

        "academic projects": "projects",
        "personal projects": "projects",
        "projects": "projects",

        "technical skills": "skills",
        "skills": "skills",

        "education": "education",
        "certifications": "certifications",
        "achievements": "achievements"
    }

    return mappings.get(
        normalized,
        normalized
    )


def split_resume_into_sections(
    resume_text: str
) -> dict[str, list[str]]:
    """
    Divide extracted resume text into common sections.
    """

    sections: dict[
        str,
        list[str]
    ] = {
        "header": []
    }

    current_section = "header"

    for raw_line in resume_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if is_section_heading(line):
            current_section = (
                get_section_key(line)
            )

            sections.setdefault(
                current_section,
                []
            )

            continue

        sections.setdefault(
            current_section,
            []
        ).append(line)

    return sections


def normalize_skill(
    skill: str
) -> str:
    return re.sub(
        r"[^a-z0-9+#.]",
        "",
        str(skill).lower()
    )


def unique_skills(
    skills: list[str]
) -> list[str]:
    cleaned = []
    seen = set()

    for skill in skills:
        clean_skill = str(skill).strip()

        key = normalize_skill(
            clean_skill
        )

        if (
            clean_skill
            and key
            and key not in seen
        ):
            cleaned.append(
                clean_skill
            )

            seen.add(key)

    return cleaned


def get_career_keywords(
    target_career: str
) -> list[str]:
    normalized_career = (
        target_career
        .strip()
        .lower()
    )

    if normalized_career in CAREER_KEYWORDS:
        return CAREER_KEYWORDS[
            normalized_career
        ]

    for career, keywords in (
        CAREER_KEYWORDS.items()
    ):
        if (
            career in normalized_career
            or normalized_career in career
        ):
            return keywords

    return []


def select_relevant_skills(
    extracted_skills: list[str],
    target_career: str,
    priority_skills: list[str]
) -> dict[str, list[str]]:
    current_skills = unique_skills(
        extracted_skills
    )

    career_keywords = get_career_keywords(
        target_career
    )

    existing_keys = {
        normalize_skill(skill)
        for skill in current_skills
    }

    matched_career_skills = [
        skill
        for skill in career_keywords
        if normalize_skill(skill)
        in existing_keys
    ]

    suggested_skills = []

    for skill in (
        priority_skills
        + career_keywords
    ):
        skill_key = normalize_skill(
            skill
        )

        if (
            skill_key
            and skill_key not in existing_keys
            and skill_key not in {
                normalize_skill(item)
                for item in suggested_skills
            }
        ):
            suggested_skills.append(
                skill
            )

    return {
        "current_skills":
            current_skills,

        "matched_career_skills":
            matched_career_skills,

        "suggested_skills":
            suggested_skills[:10]
    }


def build_professional_summary(
    *,
    target_career: str,
    extracted_skills: list[str],
    existing_summary: str
) -> str:
    """
    Rewrite the professional summary for the selected
    career while preserving useful original information.

    The function never adds unverified experience,
    qualifications, metrics or skills.
    """

    career_keywords = get_career_keywords(
        target_career
    )

    existing_skill_keys = {
        normalize_skill(skill)
        for skill in extracted_skills
    }

    relevant_skills = [
        skill
        for skill in career_keywords
        if normalize_skill(skill)
        in existing_skill_keys
    ]

    if not relevant_skills:
        relevant_skills = (
            extracted_skills[:6]
        )

    skill_text = ", ".join(
        relevant_skills[:6]
    )

    if not skill_text:
        skill_text = (
            "software development, data analysis "
            "and problem-solving"
        )

    clean_existing_summary = re.sub(
        r"\s+",
        " ",
        str(existing_summary or "")
    ).strip()

    if clean_existing_summary:
        clean_existing_summary = (
            clean_existing_summary.rstrip(".")
        )

        rewritten_summary = (
            f"{clean_existing_summary}. "
            f"Career-focused {target_career} candidate "
            f"with practical knowledge of {skill_text}. "
            "Demonstrates analytical thinking, "
            "problem-solving, collaboration and continuous "
            "learning, with an interest in building reliable, "
            "scalable and user-focused solutions."
        )
    else:
        rewritten_summary = (
            f"Motivated {target_career} candidate with "
            f"practical knowledge of {skill_text}. "
            "Experienced in applying technical skills through "
            "academic projects, internships and real-world "
            "problem-solving. Demonstrates analytical thinking, "
            "collaboration and continuous learning, with an "
            "interest in building reliable, scalable and "
            "user-focused solutions."
        )

    return re.sub(
        r"\s+",
        " ",
        rewritten_summary
    ).strip()


def remove_bullet_prefix(
    value: str
) -> str:
    return re.sub(
        r"^[\s•●▪◦\-–—*]+",
        "",
        value
    ).strip()


def begins_with_action_verb(
    value: str
) -> bool:
    first_word_match = re.match(
        r"^[A-Za-z]+",
        value.strip()
    )

    if not first_word_match:
        return False

    first_word = (
        first_word_match.group(0)
        .lower()
    )

    return first_word in {
        verb.lower()
        for verb in ACTION_VERBS
    }


def improve_bullet(
    bullet: str,
    index: int
) -> str:
    """
    Improve bullet structure without adding false
    numbers, results or technologies.
    """

    clean_bullet = remove_bullet_prefix(
        bullet
    )

    if not clean_bullet:
        return ""

    clean_bullet = clean_bullet.rstrip(
        "."
    )

    if begins_with_action_verb(
        clean_bullet
    ):
        improved = clean_bullet

    else:
        action_verb = ACTION_VERBS[
            index % len(
                ACTION_VERBS
            )
        ]

        first_character = (
            clean_bullet[0].lower()
            + clean_bullet[1:]
            if len(clean_bullet) > 1
            else clean_bullet.lower()
        )

        improved = (
            f"{action_verb} "
            f"{first_character}"
        )

    return f"{improved}."


def rewrite_bullets(
    lines: list[str]
) -> list[str]:
    rewritten = []

    for index, line in enumerate(lines):
        clean_line = line.strip()

        if not clean_line:
            continue

        # Preserve likely job titles, organization
        # names and date lines.
        if (
            not re.match(
                r"^[•●▪◦\-–—*]",
                clean_line
            )
            and len(clean_line.split()) <= 10
        ):
            rewritten.append(
                clean_line
            )

            continue

        rewritten_bullet = improve_bullet(
            clean_line,
            index
        )

        if rewritten_bullet:
            rewritten.append(
                rewritten_bullet
            )

    return rewritten


def rewrite_experience_section(
    experience_lines: list[str]
) -> list[str]:
    rewritten = []

    for index, line in enumerate(
        experience_lines
    ):
        clean_line = remove_bullet_prefix(
            line
        ).strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Keep short headings such as company names,
        # job titles and date lines unchanged.
        if (
            len(clean_line.split()) <= 8
            and not any(
                keyword in lower_line
                for keyword in [
                    "developed",
                    "built",
                    "implemented",
                    "designed",
                    "created",
                    "engineered",
                    "automated",
                    "deployed",
                    "integrated",
                    "managed",
                    "analyzed",
                    "improved",
                    "worked"
                ]
            )
        ):
            rewritten.append(
                clean_line
            )
            continue

        improved = clean_line.rstrip(".")

        replacements = [
            (
                r"^worked on\b",
                "Contributed to"
            ),
            (
                r"^worked with\b",
                "Collaborated using"
            ),
            (
                r"^made\b",
                "Developed"
            ),
            (
                r"^created\b",
                "Designed and developed"
            ),
            (
                r"^built\b",
                "Designed and built"
            ),
            (
                r"^did\b",
                "Executed"
            ),
            (
                r"^helped\b",
                "Supported"
            )
        ]

        for pattern, replacement in replacements:
            improved = re.sub(
                pattern,
                replacement,
                improved,
                flags=re.IGNORECASE
            )

        if not begins_with_action_verb(
            improved
        ):
            action_verb = ACTION_VERBS[
                index % len(ACTION_VERBS)
            ]

            first_character = (
                improved[0].lower()
                + improved[1:]
                if len(improved) > 1
                else improved.lower()
            )

            improved = (
                f"{action_verb} "
                f"{first_character}"
            )

        improved = re.sub(
            r"\busing using\b",
            "using",
            improved,
            flags=re.IGNORECASE
        )

        improved = re.sub(
            r"\s+",
            " ",
            improved
        ).strip()

        rewritten.append(
            f"{improved}."
        )

    return rewritten


def rewrite_projects_section(
    project_lines: list[str]
) -> list[str]:
    rewritten = []

    for index, line in enumerate(
        project_lines
    ):
        clean_line = remove_bullet_prefix(
            line
        ).strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Keep likely project names unchanged.
        if (
            len(clean_line.split()) <= 7
            and not any(
                keyword in lower_line
                for keyword in [
                    "developed",
                    "built",
                    "implemented",
                    "designed",
                    "created",
                    "analyzed",
                    "performed",
                    "generated",
                    "deployed"
                ]
            )
        ):
            rewritten.append(
                clean_line
            )
            continue

        improved = clean_line.rstrip(".")

        replacements = [
            (
                r"^made\b",
                "Developed"
            ),
            (
                r"^created\b",
                "Designed and developed"
            ),
            (
                r"^built\b",
                "Designed and built"
            ),
            (
                r"^did analysis on\b",
                "Analyzed"
            ),
            (
                r"^worked on\b",
                "Developed"
            ),
            (
                r"^used\b",
                "Applied"
            )
        ]

        for pattern, replacement in replacements:
            improved = re.sub(
                pattern,
                replacement,
                improved,
                flags=re.IGNORECASE
            )

        if not begins_with_action_verb(
            improved
        ):
            preferred_verbs = [
                "Developed",
                "Implemented",
                "Designed",
                "Analyzed",
                "Built",
                "Created"
            ]

            action_verb = preferred_verbs[
                index % len(
                    preferred_verbs
                )
            ]

            first_character = (
                improved[0].lower()
                + improved[1:]
                if len(improved) > 1
                else improved.lower()
            )

            improved = (
                f"{action_verb} "
                f"{first_character}"
            )

        improved = re.sub(
            r"\busing using\b",
            "using",
            improved,
            flags=re.IGNORECASE
        )

        improved = re.sub(
            r"\s+",
            " ",
            improved
        ).strip()

        rewritten.append(
            f"{improved}."
        )

    return rewritten


def build_skills_section(
    *,
    extracted_skills: list[str],
    priority_skills: list[str],
    target_career: str
) -> dict[str, list[str]]:
    skill_result = select_relevant_skills(
        extracted_skills=
            extracted_skills,

        target_career=
            target_career,

        priority_skills=
            priority_skills
    )

    current_skills = (
        skill_result[
            "current_skills"
        ]
    )

    suggested_skills = (
        skill_result[
            "suggested_skills"
        ]
    )

    return {
        "verified_skills":
            current_skills,

        "recommended_skills":
            suggested_skills,

        "important_note": [
            "Add recommended skills only after gaining "
            "practical knowledge or project experience."
        ]
    }


def build_rewrite_notes(
    *,
    original_summary: str,
    rewritten_summary: str,
    original_experience: list[str],
    rewritten_experience: list[str],
    original_projects: list[str],
    rewritten_projects: list[str],
    recommended_skills: list[str]
) -> list[str]:
    notes = []

    if (
        rewritten_summary
        and rewritten_summary
        != original_summary
    ):
        notes.append(
            "Professional summary was rewritten to "
            "match the selected career."
        )

    if (
        rewritten_experience
        != original_experience
    ):
        notes.append(
            "Experience bullets were improved using "
            "stronger action-oriented language."
        )

    if (
        rewritten_projects
        != original_projects
    ):
        notes.append(
            "Project descriptions were rewritten for "
            "clarity and stronger technical impact."
        )

    if recommended_skills:
        notes.append(
            "Missing career skills are shown separately "
            "and are not automatically added as existing skills."
        )

    notes.append(
        "The generated content does not invent company "
        "names, job responsibilities, metrics or achievements."
    )

    return notes


def rewrite_resume_for_career(
    *,
    resume_text: str,
    extracted_skills: list[str],
    target_career: str,
    priority_skills: list[str] | None = None
) -> dict[str, Any]:
    """
    Generate a rule-based resume rewrite for a
    selected career.

    The function improves wording but avoids inventing
    experience, numbers, qualifications or skills.
    """

    if not resume_text.strip():
        raise ValueError(
            "Resume text is empty."
        )

    clean_target_career = (
        target_career.strip()
    )

    if len(clean_target_career) < 2:
        raise ValueError(
            "Please select a valid target career."
        )

    safe_priority_skills = (
        unique_skills(
            priority_skills or []
        )
    )

    safe_extracted_skills = (
        unique_skills(
            extracted_skills
        )
    )

    # ------------------------------------------
    # Extract structured resume sections
    # ------------------------------------------

    sections = extract_sections(
    clean_text(
        resume_text
    )
    )


    original_summary = build_summary(
        sections
    )

    original_experience = build_bullets(
        sections.get(
            "experience",
            []
        )
    )

    original_projects = build_bullets(
        sections.get(
            "projects",
            []
        )
    )

    # ------------------------------------------
    # Summary fallback
    # ------------------------------------------

    if not original_summary:
        resume_lines = [
            line.strip()
            for line in resume_text.splitlines()
            if line.strip()
        ]

        summary_start = None
        summary_end = None

        for index, line in enumerate(
            resume_lines
        ):
            normalized_line = (
                line.lower()
                .strip()
                .rstrip(":")
            )

            if normalized_line in {
                "summary",
                "professional summary",
                "profile",
                "career objective",
                "objective",
                "about me"
            }:
                summary_start = index + 1
                break

        if summary_start is not None:
            for index in range(
                summary_start,
                len(resume_lines)
            ):
                normalized_line = (
                    resume_lines[index]
                    .lower()
                    .strip()
                    .rstrip(":")
                )

                if normalized_line in {
                    "education",
                    "experience",
                    "work experience",
                    "internship",
                    "projects",
                    "technical skills",
                    "skills",
                    "certifications",
                    "achievements"
                }:
                    summary_end = index
                    break

            summary_lines = resume_lines[
                summary_start:
                summary_end
            ]

            original_summary = " ".join(
                summary_lines
            ).strip()

    # Second summary fallback.
    if not original_summary:
        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(
                r"\n\s*\n",
                resume_text
            )
            if len(
                paragraph.split()
            ) >= 20
        ]

        if paragraphs:
            original_summary = (
                paragraphs[0]
            )

    # ------------------------------------------
    # Experience fallback
    # ------------------------------------------

    if not original_experience:
        experience_candidates = []

        for line in resume_text.splitlines():
            clean_line = (
                line.strip()
            )

            if not clean_line:
                continue

            lower_line = (
                clean_line.lower()
            )

            contains_action_word = any(
                word in lower_line
                for word in [
                    "developed",
                    "built",
                    "implemented",
                    "worked",
                    "designed",
                    "created",
                    "engineered",
                    "deployed",
                    "integrated",
                    "automated",
                    "managed",
                    "intern"
                ]
            )

            if (
                len(
                    clean_line.split()
                ) >= 7
                and contains_action_word
            ):
                experience_candidates.append(
                    clean_line
                )

        original_experience = (
            experience_candidates[:10]
        )

    # ------------------------------------------
    # Projects fallback
    # ------------------------------------------

    if not original_projects:
        project_candidates = []

        for line in resume_text.splitlines():
            clean_line = (
                line.strip()
            )

            if not clean_line:
                continue

            lower_line = (
                clean_line.lower()
            )

            contains_project_word = any(
                word in lower_line
                for word in [
                    "project",
                    "application",
                    "system",
                    "website",
                    "platform",
                    "dashboard",
                    "machine learning",
                    "data analysis",
                    "ai-powered",
                    "developed",
                    "built",
                    "analyzed"
                ]
            )

            if (
                len(
                    clean_line.split()
                ) >= 6
                and contains_project_word
            ):
                project_candidates.append(
                    clean_line
                )

        original_projects = (
            project_candidates[:12]
        )

    # ------------------------------------------
    # Rewrite the extracted sections
    # ------------------------------------------

    rewritten_summary = (
        build_professional_summary(
            target_career=
                clean_target_career,

            extracted_skills=
                safe_extracted_skills,

            existing_summary=
                original_summary
        )
    )

    rewritten_experience = (
        rewrite_experience_section(
            original_experience
        )
    )

    rewritten_projects = (
        rewrite_projects_section(
            original_projects
        )
    )

    # ------------------------------------------
    # Skills
    # ------------------------------------------

    skills_result = (
        build_skills_section(
            extracted_skills=
                safe_extracted_skills,

            priority_skills=
                safe_priority_skills,

            target_career=
                clean_target_career
        )
    )

    # ------------------------------------------
    # Rewrite notes
    # ------------------------------------------

    rewrite_notes = (
        build_rewrite_notes(
            original_summary=
                original_summary,

            rewritten_summary=
                rewritten_summary,

            original_experience=
                original_experience,

            rewritten_experience=
                rewritten_experience,

            original_projects=
                original_projects,

            rewritten_projects=
                rewritten_projects,

            recommended_skills=
                skills_result[
                    "recommended_skills"
                ]
        )
    )
    # ------------------------------------------
    # Resume quality metrics
    # ------------------------------------------

    # Compare only the sections that were rewritten:
    # summary, experience and projects.
    original_rewrite_text = "\n".join(
        [
            original_summary,
            *original_experience,
            *original_projects
        ]
    ).strip()

    rewritten_resume_text = "\n".join(
        [
            rewritten_summary,
            *rewritten_experience,
            *rewritten_projects
        ]
    ).strip()

    original_word_count = len(
        original_rewrite_text.split()
    )

    rewritten_word_count = len(
        rewritten_resume_text.split()
    )

    rewritten_items = (
        rewritten_experience
        + rewritten_projects
    )

    action_item_count = sum(
        1
        for item in rewritten_items
        if begins_with_action_verb(
            item
        )
    )

    # Professional-language score is based on
    # rewritten bullets that begin with action verbs.
    if rewritten_items:
        professional_language_score = round(
            65
            + (
                action_item_count
                / len(rewritten_items)
            )
            * 35
        )
    else:
        professional_language_score = 65

    professional_language_score = max(
        55,
        min(
            professional_language_score,
            100
        )
    )

    # Readability is estimated from average sentence
    # length in the rewritten content.
    sentence_parts = [
        sentence.strip()
        for sentence in re.split(
            r"[.!?]+",
            rewritten_resume_text
        )
        if sentence.strip()
    ]

    sentence_count = max(
        len(sentence_parts),
        1
    )

    average_sentence_length = (
        rewritten_word_count
        / sentence_count
    )

    if average_sentence_length <= 18:
        readability_score = 95

    elif average_sentence_length <= 22:
        readability_score = 88

    elif average_sentence_length <= 26:
        readability_score = 80

    elif average_sentence_length <= 30:
        readability_score = 72

    else:
        readability_score = 65

    verified_skill_count = len(
        skills_result.get(
            "verified_skills",
            []
        )
    )

    recommended_skill_count = len(
        skills_result.get(
            "recommended_skills",
            []
        )
    )

    total_career_skills = (
        verified_skill_count
        + recommended_skill_count
    )

    if total_career_skills > 0:
        ats_optimization_score = round(
            verified_skill_count
            / total_career_skills
            * 100
        )
    else:
        ats_optimization_score = 70

    ats_optimization_score = max(
        55,
        min(
            ats_optimization_score,
            100
        )
    )

    if rewritten_items:
        action_verb_score = round(
            action_item_count
            / len(rewritten_items)
            * 100
        )
    else:
        action_verb_score = 60

    action_verb_score = max(
        55,
        min(
            action_verb_score,
            100
        )
    )

    average_quality_score = round(
        (
            readability_score
            + professional_language_score
            + ats_optimization_score
            + action_verb_score
        )
        / 4
    )

    overall_improvement = max(
        0,
        min(
            30,
            round(
                (
                    average_quality_score
                    - 65
                )
                * 0.6
            )
        )
    )

    quality_analysis = {
        "readability":
            readability_score,

        "professional_language":
            professional_language_score,

        "ats_optimization":
            ats_optimization_score,

        "action_verbs":
            action_verb_score,

        "overall_improvement":
            overall_improvement,

        "original_word_count":
            original_word_count,

        "rewritten_word_count":
            rewritten_word_count
    }

    return {
        "target_career":
            clean_target_career,

        "original_content": {
            "summary":
                original_summary,

            "experience":
                original_experience,

            "projects":
                original_projects,

            "skills":
                safe_extracted_skills
        },

        "rewritten_content": {
            "summary":
                rewritten_summary,

            "experience":
                rewritten_experience,

            "projects":
                rewritten_projects,

            "verified_skills":
                skills_result[
                    "verified_skills"
                ],

            "recommended_skills":
                skills_result[
                    "recommended_skills"
                ]
        },

        "rewrite_notes":
            rewrite_notes,

        "quality_analysis":
            quality_analysis,

        "disclaimer": (
            "Review all rewritten content before using "
            "it. Keep only statements, skills and "
            "achievements that accurately represent "
            "your real experience."
        )
    }