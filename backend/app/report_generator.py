from io import BytesIO
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)


def safe_text(value: Any, default: str = "Not available") -> str:
    """
    Convert a value into safe text for the PDF.
    """

    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return escape(text)


def create_skill_badges(
    skills: list[str],
    style: ParagraphStyle
) -> Table:
    """
    Create a wrapped table containing skills.
    """

    if not skills:
        return Table(
            [[Paragraph("No skills available.", style)]],
            colWidths=[6.7 * inch]
        )

    skill_cells = []

    for skill in skills:
        skill_cells.append(
            Paragraph(
                f"<b>{safe_text(skill)}</b>",
                style
            )
        )

    rows = []
    skills_per_row = 3

    for index in range(0, len(skill_cells), skills_per_row):
        row = skill_cells[index:index + skills_per_row]

        while len(row) < skills_per_row:
            row.append("")

        rows.append(row)

    table = Table(
        rows,
        colWidths=[2.2 * inch] * skills_per_row,
        hAlign="LEFT"
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#EEF2FF")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.HexColor("#3730A3")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#C7D2FE")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.white
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    return table


def add_page_number(canvas, document):
    """
    Add page number and footer on every page.
    """

    canvas.saveState()

    page_number = canvas.getPageNumber()

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(
        colors.HexColor("#64748B")
    )

    canvas.drawString(
        40,
        25,
        "CareerCompass AI - Resume Analysis Report"
    )

    canvas.drawRightString(
        A4[0] - 40,
        25,
        f"Page {page_number}"
    )

    canvas.restoreState()


def generate_resume_report(
    resume: Any,
    user: Any,
    extracted_skills: list[str],
    ats_analysis: dict[str, Any],
    career_predictions: list[dict[str, Any]],
    skill_gap_analysis: dict[str, Any],
    learning_recommendations: dict[str, Any],
    job_recommendations: dict[str, Any]
) -> BytesIO:
    """
    Generate the complete CareerCompass PDF report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45,
        title="CareerCompass AI Resume Analysis Report",
        author="CareerCompass AI"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1E1B4B"),
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#312E81"),
        spaceBefore=14,
        spaceAfter=10
    )

    subsection_style = ParagraphStyle(
        "SubsectionHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceBefore=8,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    small_style = ParagraphStyle(
        "Small",
        parent=body_style,
        fontSize=8,
        leading=11
    )

    badge_style = ParagraphStyle(
        "Badge",
        parent=body_style,
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#3730A3")
    )

    white_heading_style = ParagraphStyle(
        "WhiteHeading",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.white
    )

    story = []

    # ======================================
    # TITLE PAGE
    # ======================================

    story.append(Spacer(1, 0.6 * inch))

    story.append(
        Paragraph(
            "CareerCompass AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Complete Resume, Career and Skill Analysis Report",
            subtitle_style
        )
    )

    summary_table = Table(
        [
            [
                Paragraph(
                    "<b>Candidate</b>",
                    body_style
                ),
                Paragraph(
                    safe_text(
                        getattr(user, "full_name", None)
                        or getattr(user, "name", None)
                        or getattr(user, "username", None)
                        or getattr(user, "email", None)
                    ),
                    body_style
                )
            ],
            [
                Paragraph(
                    "<b>Email</b>",
                    body_style
                ),
                Paragraph(
                    safe_text(
                        getattr(user, "email", None)
                    ),
                    body_style
                )
            ],
            [
                Paragraph(
                    "<b>Resume</b>",
                    body_style
                ),
                Paragraph(
                    safe_text(resume.file_name),
                    body_style
                )
            ],
            [
                Paragraph(
                    "<b>ATS Score</b>",
                    body_style
                ),
                Paragraph(
                    (
                        f"{safe_text(resume.ats_score, '0')}% - "
                        f"{safe_text(resume.ats_rating)}"
                    ),
                    body_style
                )
            ],
            [
                Paragraph(
                    "<b>Best Career</b>",
                    body_style
                ),
                Paragraph(
                    safe_text(resume.best_career),
                    body_style
                )
            ],
            [
                Paragraph(
                    "<b>Best Job Match</b>",
                    body_style
                ),
                Paragraph(
                    safe_text(resume.best_job),
                    body_style
                )
            ]
        ],
        colWidths=[1.6 * inch, 5.0 * inch]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#E0E7FF")
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                colors.HexColor("#F8FAFC")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#CBD5E1")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#E2E8F0")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            )
        ])
    )

    story.append(summary_table)
    story.append(Spacer(1, 20))

    disclaimer = (
        "This report is generated from resume content and "
        "predefined skill-matching rules. Recommendations should "
        "be used as career guidance and not as a guaranteed hiring result."
    )

    story.append(
        Paragraph(
            disclaimer,
            small_style
        )
    )

    story.append(PageBreak())

    # ======================================
    # EXECUTIVE SUMMARY
    # ======================================

    story.append(
        Paragraph(
            "1. Executive Summary",
            section_style
        )
    )

    readiness_score = skill_gap_analysis.get(
        "readiness_score",
        resume.career_readiness or 0
    )

    readiness_level = skill_gap_analysis.get(
        "readiness_level",
        resume.readiness_level or "Not available"
    )

    executive_data = [
        [
            Paragraph(
                "<b>Metric</b>",
                body_style
            ),
            Paragraph(
                "<b>Result</b>",
                body_style
            )
        ],
        [
            Paragraph(
                "ATS Score",
                body_style
            ),
            Paragraph(
                f"{resume.ats_score or 0}%",
                body_style
            )
        ],
        [
            Paragraph(
                "ATS Rating",
                body_style
            ),
            Paragraph(
                safe_text(resume.ats_rating),
                body_style
            )
        ],
        [
            Paragraph(
                "Technical Skills Detected",
                body_style
            ),
            Paragraph(
                str(len(extracted_skills)),
                body_style
            )
        ],
        [
            Paragraph(
                "Recommended Career",
                body_style
            ),
            Paragraph(
                safe_text(resume.best_career),
                body_style
            )
        ],
        [
            Paragraph(
                "Career Readiness",
                body_style
            ),
            Paragraph(
                f"{readiness_score}% - {safe_text(readiness_level)}",
                body_style
            )
        ],
        [
            Paragraph(
                "Recommended Job",
                body_style
            ),
            Paragraph(
                safe_text(resume.best_job),
                body_style
            )
        ]
    ]

    executive_table = Table(
        executive_data,
        colWidths=[3.2 * inch, 3.4 * inch],
        repeatRows=1
    )

    executive_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#312E81")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#F8FAFC")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.7,
                colors.HexColor("#CBD5E1")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#E2E8F0")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    story.append(executive_table)

    summary = skill_gap_analysis.get(
        "summary",
        "No summary is available."
    )

    story.append(Spacer(1, 15))
    story.append(
        Paragraph(
            f"<b>Career Summary:</b> {safe_text(summary)}",
            body_style
        )
    )

    # ======================================
    # EXTRACTED SKILLS
    # ======================================

    story.append(
        Paragraph(
            "2. Extracted Technical Skills",
            section_style
        )
    )

    story.append(
        Paragraph(
            (
                f"The system detected <b>{len(extracted_skills)}</b> "
                "technical skills in the uploaded resume."
            ),
            body_style
        )
    )

    story.append(Spacer(1, 6))
    story.append(
        create_skill_badges(
            extracted_skills,
            badge_style
        )
    )

    # ======================================
    # ATS ANALYSIS
    # ======================================

    story.append(
        Paragraph(
            "3. ATS Resume Analysis",
            section_style
        )
    )

    score_table = Table(
        [
            [
                Paragraph(
                    "ATS SCORE",
                    white_heading_style
                ),
                Paragraph(
                    (
                        f"<b>{ats_analysis.get('score', 0)}%</b><br/>"
                        f"{safe_text(ats_analysis.get('rating'))}"
                    ),
                    white_heading_style
                )
            ]
        ],
        colWidths=[3.3 * inch, 3.3 * inch]
    )

    score_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#4F46E5")
            ),
            (
                "ALIGN",
                (1, 0),
                (1, 0),
                "RIGHT"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                14
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                14
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                12
            )
        ])
    )

    story.append(score_table)

    ats_sections = [
        (
            "Strengths",
            ats_analysis.get("strengths", [])
        ),
        (
            "Missing Sections",
            ats_analysis.get("missing_sections", [])
        ),
        (
            "Improvement Suggestions",
            ats_analysis.get("suggestions", [])
        )
    ]

    for title, items in ats_sections:
        story.append(
            Paragraph(
                title,
                subsection_style
            )
        )

        if items:
            for item in items:
                story.append(
                    Paragraph(
                        f"- {safe_text(item)}",
                        body_style
                    )
                )
        else:
            story.append(
                Paragraph(
                    "No items available.",
                    body_style
                )
            )

    story.append(PageBreak())

    # ======================================
    # CAREER PREDICTIONS
    # ======================================

    story.append(
        Paragraph(
            "4. Career Predictions",
            section_style
        )
    )

    if career_predictions:
        career_rows = [
            [
                Paragraph(
                    "<b>Career</b>",
                    small_style
                ),
                Paragraph(
                    "<b>Match</b>",
                    small_style
                ),
                Paragraph(
                    "<b>Matched Skills</b>",
                    small_style
                ),
                Paragraph(
                    "<b>Skills to Learn</b>",
                    small_style
                )
            ]
        ]

        for prediction in career_predictions:
            career_rows.append([
                Paragraph(
                    safe_text(
                        prediction.get("career")
                    ),
                    small_style
                ),
                Paragraph(
                    f"{prediction.get('match_percentage', 0)}%",
                    small_style
                ),
                Paragraph(
                    safe_text(
                        ", ".join(
                            prediction.get(
                                "matched_skills",
                                []
                            )
                        ),
                        "None"
                    ),
                    small_style
                ),
                Paragraph(
                    safe_text(
                        ", ".join(
                            prediction.get(
                                "missing_skills",
                                []
                            )
                        ),
                        "None"
                    ),
                    small_style
                )
            ])

        career_table = Table(
            career_rows,
            colWidths=[
                1.35 * inch,
                0.65 * inch,
                2.3 * inch,
                2.3 * inch
            ],
            repeatRows=1
        )

        career_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#312E81")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC")
                    ]
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CBD5E1")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
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
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(career_table)
    else:
        story.append(
            Paragraph(
                "No career predictions are available.",
                body_style
            )
        )

    # ======================================
    # SKILL GAP ANALYSIS
    # ======================================

    story.append(
        Paragraph(
            "5. Skill Gap Analysis",
            section_style
        )
    )

    story.append(
        Paragraph(
            (
                f"<b>Target Career:</b> "
                f"{safe_text(skill_gap_analysis.get('target_career'))}"
            ),
            body_style
        )
    )

    story.append(
        Paragraph(
            (
                f"<b>Career Readiness:</b> "
                f"{skill_gap_analysis.get('readiness_score', 0)}% - "
                f"{safe_text(skill_gap_analysis.get('readiness_level'))}"
            ),
            body_style
        )
    )

    story.append(
        Paragraph(
            (
                f"<b>Estimated Learning Time:</b> "
                f"{safe_text(skill_gap_analysis.get('estimated_learning_time'))}"
            ),
            body_style
        )
    )

    gap_rows = [
        [
            Paragraph(
                "<b>Skills Already Available</b>",
                body_style
            ),
            Paragraph(
                "<b>Missing Skills</b>",
                body_style
            ),
            Paragraph(
                "<b>Priority Skills</b>",
                body_style
            )
        ],
        [
            Paragraph(
                safe_text(
                    ", ".join(
                        skill_gap_analysis.get(
                            "matched_skills",
                            []
                        )
                    ),
                    "None"
                ),
                body_style
            ),
            Paragraph(
                safe_text(
                    ", ".join(
                        skill_gap_analysis.get(
                            "missing_skills",
                            []
                        )
                    ),
                    "None"
                ),
                body_style
            ),
            Paragraph(
                safe_text(
                    ", ".join(
                        skill_gap_analysis.get(
                            "priority_skills",
                            []
                        )
                    ),
                    "None"
                ),
                body_style
            )
        ]
    ]

    gap_table = Table(
        gap_rows,
        colWidths=[
            2.2 * inch,
            2.2 * inch,
            2.2 * inch
        ]
    )

    gap_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, 0),
                colors.HexColor("#DCFCE7")
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, 0),
                colors.HexColor("#FEE2E2")
            ),
            (
                "BACKGROUND",
                (2, 0),
                (2, 0),
                colors.HexColor("#FEF3C7")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#CBD5E1")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    story.append(Spacer(1, 8))
    story.append(gap_table)

    story.append(PageBreak())

    # ======================================
    # LEARNING ROADMAP
    # ======================================

    story.append(
        Paragraph(
            "6. Personalized Learning Roadmap",
            section_style
        )
    )

    story.append(
        Paragraph(
            safe_text(
                learning_recommendations.get(
                    "message"
                )
            ),
            body_style
        )
    )

    roadmap = learning_recommendations.get(
        "roadmap",
        []
    )

    if roadmap:
        for item in roadmap:
            priority_label = (
                " - Priority Skill"
                if item.get("is_priority")
                else ""
            )

            story.append(
                Paragraph(
                    (
                        f"{item.get('order', '')}. "
                        f"{safe_text(item.get('skill'))}"
                        f"{priority_label}"
                    ),
                    subsection_style
                )
            )

            details = [
                [
                    Paragraph(
                        "<b>Difficulty</b>",
                        small_style
                    ),
                    Paragraph(
                        safe_text(
                            item.get("difficulty")
                        ),
                        small_style
                    ),
                    Paragraph(
                        "<b>Duration</b>",
                        small_style
                    ),
                    Paragraph(
                        safe_text(
                            item.get("duration")
                        ),
                        small_style
                    )
                ]
            ]

            details_table = Table(
                details,
                colWidths=[
                    1.0 * inch,
                    2.1 * inch,
                    1.0 * inch,
                    2.5 * inch
                ]
            )

            details_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#F5F3FF")
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#DDD6FE")
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            story.append(details_table)
            story.append(Spacer(1, 6))

            story.append(
                Paragraph(
                    (
                        f"<b>Mini Project:</b> "
                        f"{safe_text(item.get('mini_project'))}"
                    ),
                    body_style
                )
            )

            story.append(
                Paragraph(
                    (
                        f"<b>Suggested Certification:</b> "
                        f"{safe_text(item.get('certification'))}"
                    ),
                    body_style
                )
            )

            resources = item.get(
                "resources",
                []
            )

            if resources:
                story.append(
                    Paragraph(
                        "<b>Learning Resources:</b>",
                        body_style
                    )
                )

                for resource in resources:
                    resource_text = (
                        f"- {safe_text(resource.get('title'))} "
                        f"({safe_text(resource.get('provider'))}, "
                        f"{safe_text(resource.get('type'))})"
                    )

                    story.append(
                        Paragraph(
                            resource_text,
                            small_style
                        )
                    )

            story.append(Spacer(1, 8))
    else:
        story.append(
            Paragraph(
                (
                    "No major learning gaps were found. "
                    "Focus on projects and interview preparation."
                ),
                body_style
            )
        )

    # ======================================
    # JOB RECOMMENDATIONS
    # ======================================

    story.append(
        Paragraph(
            "7. Job Recommendations",
            section_style
        )
    )

    recommendations = job_recommendations.get(
        "recommendations",
        []
    )

    if recommendations:
        for index, job in enumerate(
            recommendations,
            start=1
        ):
            story.append(
                Paragraph(
                    (
                        f"{index}. "
                        f"{safe_text(job.get('job_title'))}"
                    ),
                    subsection_style
                )
            )

            job_info = [
                [
                    Paragraph(
                        "<b>Career Category</b>",
                        small_style
                    ),
                    Paragraph(
                        safe_text(
                            job.get("career_category")
                        ),
                        small_style
                    ),
                    Paragraph(
                        "<b>Experience Level</b>",
                        small_style
                    ),
                    Paragraph(
                        safe_text(
                            job.get("experience_level")
                        ),
                        small_style
                    )
                ],
                [
                    Paragraph(
                        "<b>Skill Match</b>",
                        small_style
                    ),
                    Paragraph(
                        f"{job.get('match_percentage', 0)}%",
                        small_style
                    ),
                    Paragraph(
                        "<b>Status</b>",
                        small_style
                    ),
                    Paragraph(
                        safe_text(
                            job.get("application_status")
                        ),
                        small_style
                    )
                ]
            ]

            job_table = Table(
                job_info,
                colWidths=[
                    1.2 * inch,
                    2.0 * inch,
                    1.2 * inch,
                    2.2 * inch
                ]
            )

            job_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#EFF6FF")
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#BFDBFE")
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            story.append(job_table)
            story.append(Spacer(1, 6))

            story.append(
                Paragraph(
                    safe_text(job.get("description")),
                    body_style
                )
            )

            story.append(
                Paragraph(
                    (
                        f"<b>Matched Skills:</b> "
                        f"{safe_text(', '.join(job.get('matched_skills', [])), 'None')}"
                    ),
                    body_style
                )
            )

            story.append(
                Paragraph(
                    (
                        f"<b>Skills to Improve:</b> "
                        f"{safe_text(', '.join(job.get('missing_skills', [])), 'None')}"
                    ),
                    body_style
                )
            )

            story.append(
                Paragraph(
                    (
                        f"<b>Application Advice:</b> "
                        f"{safe_text(job.get('preparation_advice'))}"
                    ),
                    body_style
                )
            )

            story.append(Spacer(1, 10))
    else:
        story.append(
            Paragraph(
                "No job recommendations are available.",
                body_style
            )
        )

    # ======================================
    # FINAL ACTION PLAN
    # ======================================

    story.append(
        Paragraph(
            "8. Final Action Plan",
            section_style
        )
    )

    priority_skills = skill_gap_analysis.get(
        "priority_skills",
        []
    )

    final_steps = [
        (
            "Improve the priority skills: "
            + (
                ", ".join(priority_skills)
                if priority_skills
                else "continue advanced skill practice"
            )
        ),
        "Complete the recommended mini projects.",
        "Update the resume with measurable achievements.",
        "Create or improve LinkedIn and GitHub profiles.",
        (
            "Apply for suitable roles such as "
            f"{job_recommendations.get('best_job') or resume.best_job or 'entry-level roles'}."
        ),
        "Practice technical, aptitude and HR interview questions."
    ]

    for index, step in enumerate(
        final_steps,
        start=1
    ):
        story.append(
            Paragraph(
                f"{index}. {safe_text(step)}",
                body_style
            )
        )

    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            (
                "<b>End of Report</b><br/>"
                "Generated by CareerCompass AI"
            ),
            subtitle_style
        )
    )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)

    return buffer