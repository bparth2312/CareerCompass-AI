from io import BytesIO
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet
)
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)


# =========================================================
# COLORS
# =========================================================

PRIMARY_COLOR = colors.HexColor(
    "#0F766E"
)

PRIMARY_DARK = colors.HexColor(
    "#115E59"
)

TEXT_COLOR = colors.HexColor(
    "#0F172A"
)

SECONDARY_TEXT_COLOR = colors.HexColor(
    "#334155"
)

MUTED_COLOR = colors.HexColor(
    "#64748B"
)

LIGHT_BACKGROUND = colors.HexColor(
    "#F8FAFC"
)

BORDER_COLOR = colors.HexColor(
    "#CBD5E1"
)

WHITE = colors.white


# =========================================================
# TEXT CLEANING
# =========================================================

UNICODE_REPLACEMENTS = {
    "\u2022": "-",
    "\u2023": "-",
    "\u25CF": "-",
    "\u25AA": "-",
    "\u25E6": "-",
    "\u2043": "-",
    "\u2219": "-",

    "\u2010": "-",
    "\u2011": "-",
    "\u2012": "-",
    "\u2013": "-",
    "\u2014": "-",
    "\u2015": "-",

    "\u2018": "'",
    "\u2019": "'",
    "\u201A": "'",
    "\u201B": "'",

    "\u201C": '"',
    "\u201D": '"',
    "\u201E": '"',

    "\u2026": "...",
    "\u00A0": " ",
    "\u200B": "",
    "\u200C": "",
    "\u200D": "",
    "\uFEFF": "",

    "\u2713": "",
    "\u2714": "",
    "\u2715": "",
    "\u2716": "",

    "\u25A0": "",
    "\u25A1": "",
    "\uFFFD": ""
}


def clean_string(
    value: Any
) -> str:
    """
    Clean extracted resume text so ReportLab's
    built-in Helvetica font can display it safely.
    """

    if value is None:
        return ""

    text = str(value)

    for old_value, new_value in (
        UNICODE_REPLACEMENTS.items()
    ):
        text = text.replace(
            old_value,
            new_value
        )

    # Replace unsupported remaining characters.
    text = text.encode(
        "latin-1",
        errors="ignore"
    ).decode(
        "latin-1"
    )

    text = " ".join(
        text.split()
    )

    return text.strip()


def clean_list(
    values: Any
) -> list[str]:
    """
    Clean and remove duplicate list items.
    """

    if not isinstance(
        values,
        list
    ):
        return []

    cleaned_values = []
    seen_values = set()

    for value in values:
        clean_value = clean_string(
            value
        )

        normalized_value = (
            clean_value.lower()
        )

        if (
            clean_value
            and normalized_value
            not in seen_values
        ):
            cleaned_values.append(
                clean_value
            )

            seen_values.add(
                normalized_value
            )

    return cleaned_values


def safe_paragraph_text(
    value: Any
) -> str:
    """
    Escape text before placing it inside a ReportLab
    Paragraph.
    """

    return escape(
        clean_string(value)
    )


# =========================================================
# ITEM CLASSIFICATION
# =========================================================

def looks_like_date_line(
    value: str
) -> bool:
    text = clean_string(
        value
    ).lower()

    date_words = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "present"
    ]

    contains_month = any(
        word in text
        for word in date_words
    )

    contains_year = any(
        str(year) in text
        for year in range(
            2000,
            2036
        )
    )

    return (
        contains_month
        and contains_year
    )


def looks_like_heading(
    value: str
) -> bool:
    """
    Detect project titles, job headings, companies
    and date headings.
    """

    text = clean_string(
        value
    )

    if not text:
        return False

    words = text.split()

    if len(words) > 14:
        return False

    if text.endswith(
        (
            ".",
            ";",
            ","
        )
    ):
        return False

    action_starters = {
        "developed",
        "designed",
        "built",
        "implemented",
        "created",
        "engineered",
        "deployed",
        "analyzed",
        "performed",
        "generated",
        "integrated",
        "automated",
        "managed",
        "collaborated",
        "improved",
        "optimized"
    }

    first_word = (
        words[0].lower()
        if words
        else ""
    )

    if first_word in action_starters:
        return False

    if looks_like_date_line(
        text
    ):
        return True

    title_keywords = [
        "intern",
        "developer",
        "engineer",
        "analyst",
        "manager",
        "specialist",
        "consultant",
        "dashboard",
        "analysis",
        "analyzer",
        "application",
        "platform",
        "system",
        "clone",
        "project",
        "website",
        "app"
    ]

    contains_title_keyword = any(
        keyword in text.lower()
        for keyword in title_keywords
    )

    if contains_title_keyword:
        return True

    return (
        len(words) <= 8
        and not text.endswith(".")
    )


def is_recommended_skill_note(
    value: str
) -> bool:
    text = clean_string(
        value
    ).lower()

    return any(
        phrase in text
        for phrase in [
            "recommended",
            "learn",
            "missing",
            "priority",
            "add after",
            "gain practical"
        ]
    )


# =========================================================
# STYLES
# =========================================================

def build_styles() -> dict[str, ParagraphStyle]:
    sample_styles = getSampleStyleSheet()

    return {
        "name": ParagraphStyle(
            "ResumeName",
            parent=sample_styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            alignment=TA_CENTER,
            textColor=TEXT_COLOR,
            spaceAfter=2
        ),

        "career": ParagraphStyle(
            "ResumeCareer",
            parent=sample_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=PRIMARY_DARK,
            spaceAfter=5
        ),

        "contact": ParagraphStyle(
            "ResumeContact",
            parent=sample_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            textColor=MUTED_COLOR,
            spaceAfter=8
        ),

        "section": ParagraphStyle(
            "ResumeSection",
            parent=sample_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            alignment=TA_LEFT,
            textColor=PRIMARY_DARK,
            spaceBefore=7,
            spaceAfter=3
        ),

        "summary": ParagraphStyle(
            "ResumeSummary",
            parent=sample_styles["Normal"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=14,
            alignment=TA_LEFT,
            textColor=SECONDARY_TEXT_COLOR,
            spaceAfter=5
        ),

        "item_heading": ParagraphStyle(
            "ResumeItemHeading",
            parent=sample_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.2,
            leading=13,
            textColor=TEXT_COLOR,
            spaceBefore=4,
            spaceAfter=1
        ),

        "date": ParagraphStyle(
            "ResumeDate",
            parent=sample_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=SECONDARY_TEXT_COLOR,
            spaceAfter=2
        ),

        "bullet": ParagraphStyle(
            "ResumeBullet",
            parent=sample_styles["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13,
            leftIndent=0,
            firstLineIndent=0,
            textColor=SECONDARY_TEXT_COLOR,
            spaceAfter=1.5
        ),

        "skill_label": ParagraphStyle(
            "SkillLabel",
            parent=sample_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=12,
            textColor=PRIMARY_DARK
        ),

        "skill_value": ParagraphStyle(
            "SkillValue",
            parent=sample_styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.5,
            textColor=SECONDARY_TEXT_COLOR
        ),

        "note": ParagraphStyle(
            "ResumeNote",
            parent=sample_styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=7.5,
            leading=10,
            textColor=MUTED_COLOR
        ),

        "page_number": ParagraphStyle(
            "PageNumber",
            parent=sample_styles["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            alignment=TA_CENTER,
            textColor=MUTED_COLOR
        )
    }


# =========================================================
# PAGE HEADER AND FOOTER
# =========================================================

def add_page_number(
    canvas,
    document
) -> None:
    canvas.saveState()

    page_number = canvas.getPageNumber()

    page_width, _ = A4

    canvas.setFont(
        "Helvetica",
        7
    )

    canvas.setFillColor(
        MUTED_COLOR
    )

    canvas.drawCentredString(
        page_width / 2,
        0.28 * inch,
        f"Page {page_number}"
    )

    canvas.restoreState()


# =========================================================
# DOCUMENT SECTIONS
# =========================================================

def add_section_heading(
    story: list,
    title: str,
    styles: dict
) -> None:
    heading = Paragraph(
        safe_paragraph_text(
            title.upper()
        ),
        styles["section"]
    )

    story.append(
        heading
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=PRIMARY_COLOR,
            spaceBefore=0,
            spaceAfter=4
        )
    )


def create_wrapped_contact_text(
    contact_items: list[str],
    max_width: float,
    font_name: str = "Helvetica",
    font_size: float = 8.5
) -> list[str]:
    """
    Wrap contact details into multiple centered lines
    when URLs are too long.
    """

    lines = []
    current_line = ""

    for item in contact_items:
        clean_item = clean_string(
            item
        )

        if not clean_item:
            continue

        candidate = (
            f"{current_line} | {clean_item}"
            if current_line
            else clean_item
        )

        candidate_width = stringWidth(
            candidate,
            font_name,
            font_size
        )

        if (
            candidate_width <= max_width
            or not current_line
        ):
            current_line = candidate

        else:
            lines.append(
                current_line
            )

            current_line = clean_item

    if current_line:
        lines.append(
            current_line
        )

    return lines


def add_resume_header(
    story: list,
    *,
    user_name: str,
    user_email: str,
    phone: str,
    linkedin: str,
    github: str,
    target_career: str,
    styles: dict
) -> None:
    story.append(
        Paragraph(
            safe_paragraph_text(
                user_name.upper()
                or "PROFESSIONAL RESUME"
            ),
            styles["name"]
        )
    )

    if target_career:
        story.append(
            Paragraph(
                safe_paragraph_text(
                    target_career
                ),
                styles["career"]
            )
        )

    contact_items = [
        phone,
        user_email,
        linkedin,
        github
    ]

    contact_items = [
        clean_string(item)
        for item in contact_items
        if clean_string(item)
    ]

    contact_lines = (
        create_wrapped_contact_text(
            contact_items,
            max_width=7.05 * inch
        )
    )

    for contact_line in contact_lines:
        story.append(
            Paragraph(
                safe_paragraph_text(
                    contact_line
                ),
                styles["contact"]
            )
        )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=PRIMARY_COLOR,
            spaceBefore=1,
            spaceAfter=5
        )
    )


def add_summary_section(
    story: list,
    summary: str,
    styles: dict
) -> None:
    summary_text = clean_string(
        summary
    )

    if not summary_text:
        return

    add_section_heading(
        story,
        "Professional Summary",
        styles
    )

    story.append(
        Paragraph(
            safe_paragraph_text(
                summary_text
            ),
            styles["summary"]
        )
    )


def add_resume_items(
    story: list,
    items: list[str],
    styles: dict
) -> None:
    """
    Add job/project headings and bullets with clean
    formatting.
    """

    safe_items = clean_list(
        items
    )

    pending_bullets = []

    def flush_bullets() -> None:
        nonlocal pending_bullets

        if not pending_bullets:
            return

        bullet_items = []

        for bullet_text in pending_bullets:
            bullet_items.append(
                ListItem(
                    Paragraph(
                        safe_paragraph_text(
                            bullet_text
                        ),
                        styles["bullet"]
                    ),
                    leftIndent=10
                )
            )

        story.append(
            ListFlowable(
                bullet_items,
                bulletType="bullet",
                start="circle",
                leftIndent=13,
                bulletFontName="Helvetica",
                bulletFontSize=5.5,
                bulletOffsetY=1.5,
                spaceBefore=1,
                spaceAfter=3
            )
        )

        pending_bullets = []

    for item in safe_items:
        if looks_like_heading(
            item
        ):
            flush_bullets()

            selected_style = (
                styles["date"]
                if looks_like_date_line(item)
                else styles["item_heading"]
            )

            story.append(
                Paragraph(
                    safe_paragraph_text(
                        item
                    ),
                    selected_style
                )
            )

        else:
            pending_bullets.append(
                item
            )

    flush_bullets()


def add_experience_section(
    story: list,
    experience: list[str],
    styles: dict
) -> None:
    safe_experience = clean_list(
        experience
    )

    if not safe_experience:
        return

    add_section_heading(
        story,
        "Experience",
        styles
    )

    add_resume_items(
        story,
        safe_experience,
        styles
    )


def add_projects_section(
    story: list,
    projects: list[str],
    styles: dict
) -> None:
    safe_projects = clean_list(
        projects
    )

    if not safe_projects:
        return

    add_section_heading(
        story,
        "Projects",
        styles
    )

    add_resume_items(
        story,
        safe_projects,
        styles
    )


# =========================================================
# SKILLS
# =========================================================

def categorize_skills(
    skills: list[str]
) -> dict[str, list[str]]:
    categories = {
        "Programming":
            [],

        "Frontend":
            [],

        "Backend":
            [],

        "Data and AI":
            [],

        "Databases":
            [],

        "Tools and Cloud":
            [],

        "Other":
            []
    }

    programming = {
        "python",
        "java",
        "c",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "sql"
    }

    frontend = {
        "html",
        "html5",
        "css",
        "css3",
        "react",
        "react.js",
        "bootstrap",
        "tailwind",
        "tailwind css"
    }

    backend = {
        "node.js",
        "nodejs",
        "express",
        "express.js",
        "fastapi",
        "flask",
        "django",
        "rest api",
        "rest apis",
        "api"
    }

    data_ai = {
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "sklearn",
        "natural language processing",
        "nlp",
        "power bi",
        "tableau",
        "excel",
        "data analysis",
        "data analytics",
        "data visualization",
        "eda"
    }

    databases = {
        "mongodb",
        "postgresql",
        "mysql",
        "sqlite",
        "redis",
        "sql server"
    }

    tools_cloud = {
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "gcp",
        "cloud deployment",
        "ci/cd",
        "n8n",
        "hadoop",
        "vs code",
        "postman",
        "replit"
    }

    for skill in clean_list(
        skills
    ):
        normalized_skill = (
            skill.lower().strip()
        )

        if normalized_skill in programming:
            category = "Programming"

        elif normalized_skill in frontend:
            category = "Frontend"

        elif normalized_skill in backend:
            category = "Backend"

        elif normalized_skill in data_ai:
            category = "Data and AI"

        elif normalized_skill in databases:
            category = "Databases"

        elif normalized_skill in tools_cloud:
            category = "Tools and Cloud"

        else:
            category = "Other"

        categories[
            category
        ].append(
            skill
        )

    return {
        category: values
        for category, values in (
            categories.items()
        )
        if values
    }


def add_skills_section(
    story: list,
    verified_skills: list[str],
    recommended_skills: list[str],
    styles: dict
) -> None:
    """
    Add only verified skills to the exported resume.

    Recommended skills remain available on the
    website but are excluded from the PDF because
    they are not yet verified candidate skills.
    """

    verified = clean_list(
        verified_skills
    )

    if not verified:
        return

    add_section_heading(
        story,
        "Technical Skills",
        styles
    )

    categorized_skills = (
        categorize_skills(
            verified
        )
    )

    rows = []

    for category, category_skills in (
        categorized_skills.items()
    ):
        rows.append(
            [
                Paragraph(
                    safe_paragraph_text(
                        category
                    ),
                    styles["skill_label"]
                ),
                Paragraph(
                    safe_paragraph_text(
                        ", ".join(
                            category_skills
                        )
                    ),
                    styles["skill_value"]
                )
            ]
        )

    if not rows:
        return

    skills_table = Table(
        rows,
        colWidths=[
            1.25 * inch,
            5.75 * inch
        ],
        hAlign="LEFT"
    )

    skills_table.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    LIGHT_BACKGROUND
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -2),
                    0.3,
                    BORDER_COLOR
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER_COLOR
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ]
        )
    )

    story.append(
        skills_table
    )


# =========================================================
# MAIN PDF GENERATOR
# =========================================================

def generate_rewritten_resume_pdf(
    *,
    user_name: str,
    user_email: str,
    file_name: str,
    target_career: str,
    rewritten_content: dict[str, Any],
    phone: str = "",
    linkedin: str = "",
    github: str = ""
) -> bytes:
    """
    Generate a clean, professional and ATS-friendly
    rewritten resume PDF.
    """

    if not isinstance(
        rewritten_content,
        dict
    ):
        raise ValueError(
            "Rewritten resume content is invalid."
        )

    summary = clean_string(
        rewritten_content.get(
            "summary"
        )
    )

    experience = clean_list(
        rewritten_content.get(
            "experience"
        )
    )

    projects = clean_list(
        rewritten_content.get(
            "projects"
        )
    )

    verified_skills = clean_list(
        rewritten_content.get(
            "verified_skills"
        )
    )

    recommended_skills = clean_list(
        rewritten_content.get(
            "recommended_skills"
        )
    )

    if (
        not summary
        and not experience
        and not projects
        and not verified_skills
    ):
        raise ValueError(
            "No rewritten resume content is available."
        )

    output_buffer = BytesIO()

    pdf_document = SimpleDocTemplate(
        output_buffer,
        pagesize=A4,

        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.48 * inch,

        title=(
            f"{clean_string(user_name)} - "
            f"{clean_string(target_career)} Resume"
        ),

        author=(
            clean_string(user_name)
            or "CareerCompass AI"
        ),

        subject=(
            "ATS-friendly rewritten resume"
        ),

        creator="CareerCompass AI"
    )

    styles = build_styles()

    story = []

    add_resume_header(
        story,
        user_name=clean_string(
            user_name
        ),
        user_email=clean_string(
            user_email
        ),
        phone=clean_string(
            phone
        ),
        linkedin=clean_string(
            linkedin
        ),
        github=clean_string(
            github
        ),
        target_career=clean_string(
            target_career
        ),
        styles=styles
    )

    add_summary_section(
        story,
        summary,
        styles
    )

    add_experience_section(
        story,
        experience,
        styles
    )

    add_projects_section(
        story,
        projects,
        styles
    )

    add_skills_section(
        story,
        verified_skills,
        recommended_skills,
        styles
    )

    pdf_document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    output_buffer.seek(0)

    return output_buffer.getvalue()