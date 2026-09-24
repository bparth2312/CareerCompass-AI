from typing import Any

from app.domain_detector import (
    detect_resume_domain
)


# =========================================================
# CAREER PROFILES
# =========================================================

CAREER_PROFILES = {
    # =====================================================
    # DATA AND ARTIFICIAL INTELLIGENCE
    # =====================================================

    "Data Analyst": {
        "domain": "Data and Artificial Intelligence",
        "description": (
            "Analyzes business data, prepares reports and "
            "dashboards, and supports data-driven decisions."
        ),
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Pandas",
            "NumPy",
            "Power BI",
            "Tableau",
            "Statistics",
            "Data Visualization",
            "EDA"
        ]
    },

    "Data Scientist": {
        "domain": "Data and Artificial Intelligence",
        "description": (
            "Uses statistics, programming and machine learning "
            "to discover patterns and build predictive solutions."
        ),
        "skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "Statistics",
            "Machine Learning",
            "Scikit-learn",
            "Data Visualization",
            "Deep Learning",
            "EDA"
        ]
    },

    "Machine Learning Engineer": {
        "domain": "Data and Artificial Intelligence",
        "description": (
            "Builds, evaluates and deploys machine-learning "
            "models for production applications."
        ),
        "skills": [
            "Python",
            "Machine Learning",
            "Scikit-learn",
            "TensorFlow",
            "PyTorch",
            "Deep Learning",
            "FastAPI",
            "Docker",
            "Git",
            "AWS"
        ]
    },

    "Business Intelligence Analyst": {
        "domain": "Data and Artificial Intelligence",
        "description": (
            "Creates dashboards, reporting systems and business "
            "insights using analytics and visualization tools."
        ),
        "skills": [
            "SQL",
            "Excel",
            "Power BI",
            "Tableau",
            "Data Analysis",
            "Data Visualization",
            "Statistics",
            "PostgreSQL",
            "MS Office"
        ]
    },

    "AI Engineer": {
        "domain": "Data and Artificial Intelligence",
        "description": (
            "Develops intelligent applications using machine "
            "learning, deep learning and AI deployment methods."
        ),
        "skills": [
            "Python",
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Natural Language Processing",
            "Computer Vision",
            "FastAPI",
            "Docker"
        ]
    },

    # =====================================================
    # TECHNOLOGY
    # =====================================================

    "Full Stack Developer": {
        "domain": "Technology",
        "description": (
            "Develops complete web applications using frontend, "
            "backend and database technologies."
        ),
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express.js",
            "MongoDB",
            "SQL",
            "Git",
            "REST API"
        ]
    },

    "Backend Developer": {
        "domain": "Technology",
        "description": (
            "Builds server-side logic, APIs, authentication "
            "systems and database integrations."
        ),
        "skills": [
            "Python",
            "FastAPI",
            "Node.js",
            "Express.js",
            "SQL",
            "PostgreSQL",
            "MongoDB",
            "REST API",
            "Git",
            "Docker"
        ]
    },

    "Frontend Developer": {
        "domain": "Technology",
        "description": (
            "Creates responsive and interactive user interfaces "
            "for websites and web applications."
        ),
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Bootstrap",
            "Tailwind CSS",
            "Git",
            "TypeScript",
            "REST API"
        ]
    },

    "DevOps Engineer": {
        "domain": "Technology",
        "description": (
            "Automates deployment, infrastructure management "
            "and software delivery processes."
        ),
        "skills": [
            "Linux",
            "Git",
            "Docker",
            "Kubernetes",
            "AWS",
            "CI/CD",
            "Jenkins",
            "Python",
            "Terraform"
        ]
    },

    "Database Developer": {
        "domain": "Technology",
        "description": (
            "Designs, manages and optimizes relational and "
            "NoSQL database systems."
        ),
        "skills": [
            "SQL",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Python",
            "Git"
        ]
    },

    # =====================================================
    # HUMAN RESOURCES
    # =====================================================

    "HR Operations Executive": {
        "domain": "Human Resources",
        "description": (
            "Manages daily HR operations, attendance, payroll, "
            "employee records and workforce coordination."
        ),
        "skills": [
            "HR Operations",
            "Employee Lifecycle Management",
            "Payroll Processing",
            "Attendance Management",
            "Employee Relations",
            "Grievance Handling",
            "Workforce Management",
            "HR Reporting",
            "Excel",
            "MS Office"
        ]
    },

    "HR Generalist": {
        "domain": "Human Resources",
        "description": (
            "Handles recruitment, onboarding, employee relations, "
            "HR operations, compliance and employee engagement."
        ),
        "skills": [
            "HR Operations",
            "Recruitment",
            "Onboarding",
            "Employee Relations",
            "Grievance Handling",
            "Employee Engagement",
            "Performance Management",
            "Statutory Compliance",
            "HR Reporting",
            "Communication"
        ]
    },

    "Payroll and Compliance Executive": {
        "domain": "Human Resources",
        "description": (
            "Manages payroll inputs, attendance, statutory filings "
            "and labour-law compliance activities."
        ),
        "skills": [
            "Payroll Processing",
            "Attendance Management",
            "Statutory Compliance",
            "PF Compliance",
            "ESIC Compliance",
            "ECR Filing",
            "POSH Compliance",
            "Labor Law",
            "Excel",
            "HR Reporting"
        ]
    },

    "Talent Acquisition Executive": {
        "domain": "Human Resources",
        "description": (
            "Sources candidates, coordinates interviews and "
            "supports recruitment and onboarding processes."
        ),
        "skills": [
            "Recruitment",
            "Talent Acquisition",
            "Interviewing",
            "Onboarding",
            "Communication",
            "Interpersonal Skills",
            "HR Operations",
            "MS Office",
            "Excel"
        ]
    },

    "Employee Relations Executive": {
        "domain": "Human Resources",
        "description": (
            "Supports employee relations, grievance resolution, "
            "engagement and workplace discipline."
        ),
        "skills": [
            "Employee Relations",
            "Grievance Handling",
            "Employee Engagement",
            "Communication",
            "Interpersonal Skills",
            "Labor Law",
            "HR Operations",
            "Performance Management"
        ]
    },

    "HR Compliance Executive": {
        "domain": "Human Resources",
        "description": (
            "Ensures statutory compliance, maintains HR records "
            "and supports labour-law and workplace-policy processes."
        ),
        "skills": [
            "Statutory Compliance",
            "PF Compliance",
            "ESIC Compliance",
            "ECR Filing",
            "POSH Compliance",
            "Labor Law",
            "HR Reporting",
            "Excel",
            "MS Office"
        ]
    },

    # =====================================================
    # FINANCE AND ACCOUNTING
    # =====================================================

    "Accountant": {
        "domain": "Finance and Accounting",
        "description": (
            "Maintains financial records, prepares accounts and "
            "supports taxation and reconciliation activities."
        ),
        "skills": [
            "Accounting",
            "Bookkeeping",
            "Bank Reconciliation",
            "Financial Reporting",
            "GST",
            "TDS",
            "Taxation",
            "Tally",
            "Excel",
            "MS Office"
        ]
    },

    "Financial Analyst": {
        "domain": "Finance and Accounting",
        "description": (
            "Analyzes financial performance, budgets, forecasts "
            "and business investment decisions."
        ),
        "skills": [
            "Financial Analysis",
            "Financial Reporting",
            "Budgeting",
            "Financial Forecasting",
            "Excel",
            "Statistics",
            "Power BI",
            "Accounting"
        ]
    },

    "Accounts Executive": {
        "domain": "Finance and Accounting",
        "description": (
            "Manages invoices, payments, receivables, reconciliations "
            "and accounting documentation."
        ),
        "skills": [
            "Accounting",
            "Accounts Payable",
            "Accounts Receivable",
            "Invoice Processing",
            "Bank Reconciliation",
            "Tally",
            "GST",
            "TDS",
            "Excel"
        ]
    },

    "Audit Associate": {
        "domain": "Finance and Accounting",
        "description": (
            "Reviews financial records, verifies compliance and "
            "supports internal and external audit activities."
        ),
        "skills": [
            "Auditing",
            "Accounting",
            "Financial Reporting",
            "Taxation",
            "GST",
            "TDS",
            "Excel",
            "MS Office"
        ]
    },

    # =====================================================
    # MARKETING
    # =====================================================

    "Digital Marketing Executive": {
        "domain": "Marketing",
        "description": (
            "Plans and manages digital campaigns across search, "
            "social media, email and advertising platforms."
        ),
        "skills": [
            "Digital Marketing",
            "Social Media Marketing",
            "SEO",
            "SEM",
            "Google Ads",
            "Meta Ads",
            "Campaign Management",
            "Email Marketing",
            "Content Marketing",
            "Market Research"
        ]
    },

    "SEO Specialist": {
        "domain": "Marketing",
        "description": (
            "Improves website search visibility through keyword, "
            "content and technical optimization."
        ),
        "skills": [
            "SEO",
            "SEM",
            "Content Marketing",
            "Market Research",
            "Google Ads",
            "Data Analysis",
            "Excel"
        ]
    },

    "Content Marketing Executive": {
        "domain": "Marketing",
        "description": (
            "Creates and distributes content to increase brand "
            "awareness, engagement and lead generation."
        ),
        "skills": [
            "Content Marketing",
            "Copywriting",
            "Social Media Marketing",
            "Email Marketing",
            "Brand Management",
            "SEO",
            "Lead Generation",
            "Communication"
        ]
    },

    "Marketing Analyst": {
        "domain": "Marketing",
        "description": (
            "Analyzes campaign and customer data to improve "
            "marketing performance and business decisions."
        ),
        "skills": [
            "Market Research",
            "Data Analysis",
            "Excel",
            "Power BI",
            "Campaign Management",
            "Digital Marketing",
            "Data Visualization"
        ]
    },

    # =====================================================
    # SALES AND BUSINESS DEVELOPMENT
    # =====================================================

    "Sales Executive": {
        "domain": "Sales and Business Development",
        "description": (
            "Generates sales, manages customer relationships and "
            "works toward business revenue targets."
        ),
        "skills": [
            "Sales",
            "Client Acquisition",
            "CRM",
            "Cold Calling",
            "Negotiation",
            "Account Management",
            "Sales Pipeline Management",
            "Revenue Generation",
            "Communication"
        ]
    },

    "Business Development Executive": {
        "domain": "Sales and Business Development",
        "description": (
            "Identifies business opportunities, generates leads "
            "and develops client relationships."
        ),
        "skills": [
            "Business Development",
            "Lead Generation",
            "Client Acquisition",
            "Negotiation",
            "CRM",
            "Account Management",
            "Sales Pipeline Management",
            "Communication"
        ]
    },

    "Account Manager": {
        "domain": "Sales and Business Development",
        "description": (
            "Manages client accounts, builds relationships and "
            "supports customer retention and revenue growth."
        ),
        "skills": [
            "Account Management",
            "CRM",
            "Negotiation",
            "Client Acquisition",
            "Sales",
            "Communication",
            "Customer Satisfaction"
        ]
    },

    # =====================================================
    # OPERATIONS AND SUPPLY CHAIN
    # =====================================================

    "Operations Executive": {
        "domain": "Operations and Supply Chain",
        "description": (
            "Coordinates daily business operations, reporting, "
            "resources and process execution."
        ),
        "skills": [
            "Operations Management",
            "Process Improvement",
            "Vendor Management",
            "Inventory Management",
            "Excel",
            "MS Office",
            "Communication",
            "Problem Solving"
        ]
    },

    "Supply Chain Executive": {
        "domain": "Operations and Supply Chain",
        "description": (
            "Supports procurement, inventory, suppliers and "
            "movement of materials across the supply chain."
        ),
        "skills": [
            "Supply Chain Management",
            "Procurement",
            "Inventory Management",
            "Vendor Management",
            "Logistics",
            "Warehouse Management",
            "Excel"
        ]
    },

    "Logistics Executive": {
        "domain": "Operations and Supply Chain",
        "description": (
            "Coordinates transportation, dispatch, warehouse "
            "activities and delivery operations."
        ),
        "skills": [
            "Logistics",
            "Warehouse Management",
            "Inventory Management",
            "Vendor Management",
            "Operations Management",
            "Excel"
        ]
    },

    "Procurement Executive": {
        "domain": "Operations and Supply Chain",
        "description": (
            "Manages purchasing, suppliers, pricing and procurement "
            "documentation for organizational requirements."
        ),
        "skills": [
            "Procurement",
            "Vendor Management",
            "Negotiation",
            "Supply Chain Management",
            "Inventory Management",
            "Excel"
        ]
    },

    # =====================================================
    # CUSTOMER SERVICE
    # =====================================================

    "Customer Service Executive": {
        "domain": "Customer Service",
        "description": (
            "Handles customer questions, complaints and service "
            "requests through phone, email or chat."
        ),
        "skills": [
            "Customer Service",
            "Complaint Resolution",
            "Call Handling",
            "Email Support",
            "Chat Support",
            "Customer Satisfaction",
            "Communication",
            "Interpersonal Skills"
        ]
    },

    "Customer Support Associate": {
        "domain": "Customer Service",
        "description": (
            "Supports customers, resolves tickets and maintains "
            "positive customer experiences."
        ),
        "skills": [
            "Customer Service",
            "Ticket Management",
            "Complaint Resolution",
            "Email Support",
            "Chat Support",
            "Communication",
            "Problem Solving"
        ]
    },

    # =====================================================
    # EDUCATION AND TRAINING
    # =====================================================

    "Teacher": {
        "domain": "Education and Training",
        "description": (
            "Plans lessons, teaches students and evaluates "
            "academic progress."
        ),
        "skills": [
            "Teaching",
            "Lesson Planning",
            "Student Assessment",
            "Classroom Management",
            "Communication",
            "Mentoring"
        ]
    },

    "Corporate Trainer": {
        "domain": "Education and Training",
        "description": (
            "Designs and delivers employee training programs "
            "for professional skill development."
        ),
        "skills": [
            "Training",
            "Curriculum Development",
            "Communication",
            "Mentoring",
            "Leadership",
            "MS Office"
        ]
    },

    # =====================================================
    # DESIGN AND CREATIVE
    # =====================================================

    "Graphic Designer": {
        "domain": "Design and Creative",
        "description": (
            "Creates visual content for branding, marketing "
            "and digital communication."
        ),
        "skills": [
            "Graphic Design",
            "Adobe Photoshop",
            "Adobe Illustrator",
            "Canva",
            "Brand Management",
            "Communication"
        ]
    },

    "UI Designer": {
        "domain": "Design and Creative",
        "description": (
            "Designs visually clear and usable interfaces for "
            "web and mobile applications."
        ),
        "skills": [
            "UI Design",
            "Figma",
            "Wireframing",
            "Prototyping",
            "Graphic Design",
            "Adobe Photoshop"
        ]
    },

    "UX Designer": {
        "domain": "Design and Creative",
        "description": (
            "Researches user needs and designs usable, accessible "
            "and effective digital experiences."
        ),
        "skills": [
            "UX Design",
            "Figma",
            "Wireframing",
            "Prototyping",
            "Communication",
            "Problem Solving"
        ]
    }
}


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {
    "react.js": "react",
    "reactjs": "react",
    "nodejs": "node.js",
    "express": "express.js",
    "rest apis": "rest api",
    "powerbi": "power bi",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "human resource operations": "hr operations",
    "human resources operations": "hr operations",
    "employee grievances": "grievance handling",
    "recruiting": "recruitment",
    "provident fund": "pf compliance",
    "employee state insurance": "esic compliance",
    "labour law": "labor law",
    "social media campaigns": "social media marketing",
    "customer support": "customer service"
}


def normalize_skill(
    skill: str
) -> str:
    """
    Convert a skill into a normalized form for
    case-insensitive and alias-aware matching.
    """

    normalized = (
        str(skill)
        .strip()
        .lower()
    )

    normalized = " ".join(
        normalized.split()
    )

    return SKILL_ALIASES.get(
        normalized,
        normalized
    )


def get_detected_domain(
    extracted_skills: list[str],
    resume_text: str = ""
) -> dict[str, Any]:
    """
    Detect domain from full resume text when available.

    If resume text is not passed, use extracted skill
    names as the domain-detection input.
    """

    detection_text = (
        resume_text.strip()
        if resume_text
        and resume_text.strip()
        else " ".join(
            extracted_skills
        )
    )

    return detect_resume_domain(
        detection_text
    )


def calculate_career_match(
    *,
    user_skills: set[str],
    career_name: str,
    profile: dict[str, Any],
    detected_domain: str
) -> dict[str, Any]:
    required_skills = (
        profile.get(
            "skills",
            []
        )
    )

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:
        normalized_required_skill = (
            normalize_skill(
                required_skill
            )
        )

        if (
            normalized_required_skill
            in user_skills
        ):
            matched_skills.append(
                required_skill
            )

        else:
            missing_skills.append(
                required_skill
            )

    total_required = len(
        required_skills
    )

    total_matched = len(
        matched_skills
    )

    if total_required == 0:
        skill_match_percentage = 0

    else:
        skill_match_percentage = round(
            total_matched
            / total_required
            * 100
        )

    profile_domain = profile.get(
        "domain",
        "General"
    )

    domain_matches = (
        detected_domain == profile_domain
    )

    # The domain score prevents careers from unrelated
    # fields from appearing above relevant careers.
    domain_bonus = (
        20
        if domain_matches
        else 0
    )

    final_sort_score = min(
        100,
        skill_match_percentage
        + domain_bonus
    )

    return {
        "career":
            career_name,

        "description":
            profile.get(
                "description",
                ""
            ),

        "match_percentage":
            skill_match_percentage,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "matched_skill_count":
            total_matched,

        "required_skill_count":
            total_required,

        "_domain":
            profile_domain,

        "_domain_matches":
            domain_matches,

        "_sort_score":
            final_sort_score
    }


def predict_careers(
    extracted_skills: list[str],
    limit: int = 5,
    resume_text: str = ""
) -> list[dict[str, Any]]:
    """
    Predict the top careers from the candidate's
    detected professional domain.

    Existing calls remain compatible:

        predict_careers(skills, limit=5)

    For stronger domain detection, routes can later use:

        predict_careers(
            extracted_skills=skills,
            limit=5,
            resume_text=resume.extracted_text
        )
    """

    if not extracted_skills:
        return []

    normalized_user_skills = {
        normalize_skill(
            skill
        )
        for skill in extracted_skills
        if str(skill).strip()
    }

    domain_result = get_detected_domain(
        extracted_skills=
            extracted_skills,

        resume_text=
            resume_text
    )

    detected_domain = (
        domain_result.get(
            "detected_domain"
        )
        or "General"
    )

    all_predictions = []

    for career_name, profile in (
        CAREER_PROFILES.items()
    ):
        prediction = (
            calculate_career_match(
                user_skills=
                    normalized_user_skills,

                career_name=
                    career_name,

                profile=
                    profile,

                detected_domain=
                    detected_domain
            )
        )

        all_predictions.append(
            prediction
        )

    domain_predictions = [
        item
        for item in all_predictions
        if item["_domain_matches"]
    ]

    # If domain detection returns a supported domain,
    # show only careers belonging to that domain.
    if domain_predictions:
        selected_predictions = (
            domain_predictions
        )

    else:
        # Safe fallback for mixed or unknown resumes.
        selected_predictions = (
            all_predictions
        )

    selected_predictions.sort(
        key=lambda prediction: (
            prediction["_sort_score"],
            prediction[
                "match_percentage"
            ],
            prediction[
                "matched_skill_count"
            ]
        ),
        reverse=True
    )

    cleaned_predictions = []

    for prediction in (
        selected_predictions[:limit]
    ):
        cleaned_predictions.append({
            "career":
                prediction["career"],

            "description":
                prediction[
                    "description"
                ],

            "match_percentage":
                prediction[
                    "match_percentage"
                ],

            "matched_skills":
                prediction[
                    "matched_skills"
                ],

            "missing_skills":
                prediction[
                    "missing_skills"
                ],

            "matched_skill_count":
                prediction[
                    "matched_skill_count"
                ],

            "required_skill_count":
                prediction[
                    "required_skill_count"
                ]
        })

    return cleaned_predictions