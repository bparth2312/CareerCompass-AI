import re
from typing import Any


SECTION_PATTERNS = {
    "summary": {
        "summary",
        "professional summary",
        "profile",
        "career profile",
        "career objective",
        "objective",
        "about me"
    },

    "education": {
        "education",
        "academic qualification",
        "academic qualifications",
        "academic background",
        "educational qualification",
        "educational qualifications"
    },

    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship",
        "internships"
    },

    "projects": {
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "technical projects",
        "major projects"
    },

    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "core competencies",
        "technical competencies",
        "tools and technologies"
    },

    "certifications": {
        "certification",
        "certifications",
        "certificates",
        "courses",
        "training",
        "trainings"
    },

    "achievements": {
        "achievement",
        "achievements",
        "awards",
        "awards and achievements"
    },

    "links": {
        "profile links",
        "links",
        "professional links",
        "social links"
    }
}


SECTION_ORDER = [
    "summary",
    "education",
    "experience",
    "projects",
    "skills",
    "certifications",
    "achievements",
    "links"
]


BULLET_PATTERN = re.compile(
    r"^[\s•●▪◦\-–—*]+"
)


DATE_PATTERN = re.compile(
    r"\b("
    r"jan|january|feb|february|mar|march|apr|april|"
    r"may|jun|june|jul|july|aug|august|sep|sept|"
    r"september|oct|october|nov|november|dec|december"
    r")\b.*\b(19|20)\d{2}\b",
    flags=re.IGNORECASE
)


YEAR_RANGE_PATTERN = re.compile(
    r"\b(19|20)\d{2}\b"
    r"\s*[-–—]\s*"
    r"(\b(19|20)\d{2}\b|present|current)",
    flags=re.IGNORECASE
)


def clean_line(
    value: str
) -> str:
    value = str(
        value or ""
    )

    value = value.replace(
        "\u00a0",
        " "
    )

    value = value.replace(
        "\t",
        " "
    )

    value = re.sub(
        r"[ ]+",
        " ",
        value
    )

    return value.strip()


def normalize_heading(
    value: str
) -> str:
    value = clean_line(
        value
    ).lower()

    value = value.rstrip(
        ":"
    )

    value = re.sub(
        r"[^a-z ]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def get_section_name(
    line: str
) -> tuple[str | None, str]:
    """
    Detect a section heading even when the PDF parser
    places the heading and its first content on the
    same line.

    Example:
    SUMMARY Final-year student...

    Returns:
    ("summary", "Final-year student...")
    """

    clean_value = clean_line(
        line
    )

    if not clean_value:
        return None, ""

    lower_value = (
        clean_value
        .lower()
        .strip()
    )

    # Check longer aliases first so that
    # "technical skills" is matched before "skills".
    heading_candidates = []

    for section_name, aliases in (
        SECTION_PATTERNS.items()
    ):
        for alias in aliases:
            heading_candidates.append(
                (
                    alias.lower(),
                    section_name
                )
            )

    heading_candidates.sort(
        key=lambda item:
            len(item[0]),
        reverse=True
    )

    for alias, section_name in (
        heading_candidates
    ):
        pattern = (
            rf"^\s*"
            rf"{re.escape(alias)}"
            rf"\s*:?\s*"
        )

        match = re.match(
            pattern,
            lower_value,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        # Prevent accidental matches such as
        # "project management" being treated as PROJECT.
        remaining_lower = (
            lower_value[
                match.end():
            ].strip()
        )

        remaining_original = (
            clean_value[
                match.end():
            ].strip()
        )

        if (
            alias in {
                "project",
                "skills",
                "experience",
                "education",
                "summary"
            }
            and remaining_lower
            and len(
                alias.split()
            ) == 1
        ):
            # Single-word headings should normally be
            # uppercase or followed by resume content.
            first_token = (
                clean_value
                .split()[0]
                .rstrip(":")
            )

            if (
                not first_token.isupper()
                and normalize_heading(
                    clean_value
                ) != alias
            ):
                continue

        return (
            section_name,
            remaining_original
        )

    return None, ""

def is_section_heading(
    line: str
) -> bool:
    section_name, _ = (
        get_section_name(
            line
        )
    )

    return section_name is not None


def split_into_lines(
    resume_text: str
) -> list[str]:
    if not resume_text:
        return []

    normalized_text = (
        resume_text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    lines = []

    for raw_line in (
        normalized_text.split("\n")
    ):
        line = clean_line(
            raw_line
        )

        if line:
            lines.append(
                line
            )

    return lines


def extract_sections(
    resume_text: str
) -> dict[str, list[str]]:
    """
    Extract resume sections using strict section
    boundaries.

    It supports both:

    SUMMARY
    Final-year student...

    and:

    SUMMARY Final-year student...
    """

    lines = split_into_lines(
        resume_text
    )

    sections: dict[
        str,
        list[str]
    ] = {
        "header": []
    }

    for section_name in SECTION_ORDER:
        sections[
            section_name
        ] = []

    current_section = "header"

    for line in lines:
        (
            detected_section,
            remaining_content
        ) = get_section_name(
            line
        )

        if detected_section:
            current_section = (
                detected_section
            )

            # When the PDF merges the heading and the
            # first content line, keep the remaining text.
            if remaining_content:
                sections[
                    current_section
                ].append(
                    remaining_content
                )

            continue

        sections.setdefault(
            current_section,
            []
        ).append(
            line
        )

    return sections

def remove_bullet_prefix(
    value: str
) -> str:
    return BULLET_PATTERN.sub(
        "",
        clean_line(value)
    ).strip()


def is_bullet_line(
    value: str
) -> bool:
    return bool(
        BULLET_PATTERN.match(
            str(value or "")
        )
    )


def is_date_line(
    value: str
) -> bool:
    line = clean_line(
        value
    )

    return bool(
        DATE_PATTERN.search(line)
        or YEAR_RANGE_PATTERN.search(line)
    )


def looks_like_title(
    value: str
) -> bool:
    """
    Detect short project names, role names,
    organization names or headings.
    """

    line = clean_line(
        value
    )

    if not line:
        return False

    word_count = len(
        line.split()
    )

    if word_count > 12:
        return False

    if is_bullet_line(line):
        return False

    if line.endswith("."):
        return False

    return True


def build_summary(
    sections: dict[
        str,
        list[str]
    ]
) -> str:
    summary_lines = sections.get(
        "summary",
        []
    )

    if not isinstance(
        summary_lines,
        list
    ):
        return ""

    cleaned = []

    for line in summary_lines:
        clean_value = (
            remove_bullet_prefix(
                line
            )
        )

        if clean_value:
            cleaned.append(
                clean_value
            )

    return " ".join(
        cleaned
    ).strip()


def join_wrapped_lines(
    lines: list[str]
) -> list[str]:
    """
    Join text that was wrapped across multiple PDF
    lines into complete sentences.
    """

    results = []
    current_parts = []

    for line in lines:
        clean_value = clean_line(
            line
        )

        if not clean_value:
            continue

        if (
            is_bullet_line(clean_value)
            or looks_like_title(clean_value)
            or is_date_line(clean_value)
        ):
            if current_parts:
                results.append(
                    " ".join(
                        current_parts
                    ).strip()
                )

                current_parts = []

            results.append(
                clean_value
            )

            continue

        current_parts.append(
            clean_value
        )

        if clean_value.endswith(
            (
                ".",
                "!",
                "?"
            )
        ):
            results.append(
                " ".join(
                    current_parts
                ).strip()
            )

            current_parts = []

    if current_parts:
        results.append(
            " ".join(
                current_parts
            ).strip()
        )

    return results


def build_bullets(
    section_lines: list[str]
) -> list[str]:
    """
    Convert a section into structured items while
    preserving titles, companies and date lines.

    Bullet lines are kept as complete bullets instead
    of being split into individual words.
    """

    if not isinstance(
        section_lines,
        list
    ):
        return []

    prepared_lines = join_wrapped_lines(
        section_lines
    )

    results = []
    current_bullet_parts = []

    def flush_bullet() -> None:
        nonlocal current_bullet_parts

        if not current_bullet_parts:
            return

        combined = " ".join(
            current_bullet_parts
        ).strip()

        combined = remove_bullet_prefix(
            combined
        )

        if combined:
            results.append(
                combined
            )

        current_bullet_parts = []

    for line in prepared_lines:
        clean_value = clean_line(
            line
        )

        if not clean_value:
            continue

        if is_bullet_line(
            clean_value
        ):
            flush_bullet()

            current_bullet_parts = [
                remove_bullet_prefix(
                    clean_value
                )
            ]

            continue

        if (
            looks_like_title(clean_value)
            or is_date_line(clean_value)
        ):
            flush_bullet()

            results.append(
                clean_value
            )

            continue

        if current_bullet_parts:
            current_bullet_parts.append(
                clean_value
            )

        else:
            results.append(
                clean_value
            )

    flush_bullet()

    cleaned_results = []
    seen = set()

    for item in results:
        clean_item = re.sub(
            r"\s+",
            " ",
            clean_line(item)
        ).strip()

        if not clean_item:
            continue

        normalized_item = (
            clean_item.lower()
        )

        if normalized_item in seen:
            continue

        seen.add(
            normalized_item
        )

        cleaned_results.append(
            clean_item
        )

    return cleaned_results


def separate_titles_and_bullets(
    section_lines: list[str]
) -> list[dict[str, Any]]:
    """
    Build grouped records for projects or experience.

    Example output:

    [
        {
            "title": "Netflix Data Analysis",
            "details": [
                "Analyzed Netflix dataset...",
                "Performed EDA..."
            ]
        }
    ]
    """

    structured_items = []
    current_item: dict[
        str,
        Any
    ] | None = None

    parsed_items = build_bullets(
        section_lines
    )

    for item in parsed_items:
        if looks_like_title(
            item
        ):
            if current_item:
                structured_items.append(
                    current_item
                )

            current_item = {
                "title": item,
                "details": []
            }

            continue

        if current_item is None:
            current_item = {
                "title": "",
                "details": []
            }

        current_item[
            "details"
        ].append(
            item
        )

    if current_item:
        structured_items.append(
            current_item
        )

    return structured_items


def extract_resume_structure(
    resume_text: str
) -> dict[str, Any]:
    """
    Return complete structured resume data.
    """

    sections = extract_sections(
        resume_text
    )

    return {
        "header":
            sections.get(
                "header",
                []
            ),

        "summary":
            build_summary(
                sections
            ),

        "education":
            build_bullets(
                sections.get(
                    "education",
                    []
                )
            ),

        "experience":
            build_bullets(
                sections.get(
                    "experience",
                    []
                )
            ),

        "projects":
            build_bullets(
                sections.get(
                    "projects",
                    []
                )
            ),

        "skills":
            build_bullets(
                sections.get(
                    "skills",
                    []
                )
            ),

        "certifications":
            build_bullets(
                sections.get(
                    "certifications",
                    []
                )
            ),

        "achievements":
            build_bullets(
                sections.get(
                    "achievements",
                    []
                )
            ),

        "links":
            build_bullets(
                sections.get(
                    "links",
                    []
                )
            ),

        "structured_experience":
            separate_titles_and_bullets(
                sections.get(
                    "experience",
                    []
                )
            ),

        "structured_projects":
            separate_titles_and_bullets(
                sections.get(
                    "projects",
                    []
                )
            )
    }