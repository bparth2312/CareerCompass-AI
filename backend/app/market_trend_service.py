from typing import Any
import asyncio

from app.domain_detector import (
    detect_resume_domain
)
from app.job_market_client import (
    analyze_live_job_market
)

# =========================================================
# LOCAL CAREER MARKET TREND DATA
# =========================================================
#
# This local dataset keeps the project stable and usable
# without depending on an external API.
#
# Later, these values can be updated using a real-time
# job-market API and stored in the database.
# =========================================================

CAREER_MARKET_TRENDS = {
    # =====================================================
    # DATA AND ARTIFICIAL INTELLIGENCE
    # =====================================================

    "Data Analyst": {
        "market_demand_score": 88,
        "growth_score": 86,
        "salary_range": "₹4–10 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Hyderabad",
            "Delhi NCR"
        ],
        "trending_skills": [
            "SQL",
            "Excel",
            "Power BI",
            "Python",
            "Data Visualization"
        ]
    },

    "Data Scientist": {
        "market_demand_score": 85,
        "growth_score": 90,
        "salary_range": "₹6–16 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Mumbai",
            "Delhi NCR"
        ],
        "trending_skills": [
            "Python",
            "Machine Learning",
            "Statistics",
            "Scikit-learn",
            "SQL"
        ]
    },

    "Machine Learning Engineer": {
        "market_demand_score": 89,
        "growth_score": 94,
        "salary_range": "₹7–20 LPA",
        "demand_level": "Very High",
        "trend_status": "Fast Growing",
        "top_locations": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Delhi NCR"
        ],
        "trending_skills": [
            "Python",
            "Machine Learning",
            "TensorFlow",
            "PyTorch",
            "Model Deployment"
        ]
    },

    "Business Intelligence Analyst": {
        "market_demand_score": 84,
        "growth_score": 82,
        "salary_range": "₹5–12 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Hyderabad",
            "Delhi NCR"
        ],
        "trending_skills": [
            "Power BI",
            "SQL",
            "Excel",
            "Tableau",
            "Data Visualization"
        ]
    },

    "AI Engineer": {
        "market_demand_score": 92,
        "growth_score": 96,
        "salary_range": "₹8–24 LPA",
        "demand_level": "Very High",
        "trend_status": "Fast Growing",
        "top_locations": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Delhi NCR",
            "Chennai"
        ],
        "trending_skills": [
            "Python",
            "Artificial Intelligence",
            "Deep Learning",
            "NLP",
            "Model Deployment"
        ]
    },

    # =====================================================
    # TECHNOLOGY
    # =====================================================

    "Full Stack Developer": {
        "market_demand_score": 87,
        "growth_score": 84,
        "salary_range": "₹4–14 LPA",
        "demand_level": "High",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Bengaluru",
            "Pune",
            "Hyderabad",
            "Mumbai",
            "Chennai"
        ],
        "trending_skills": [
            "React",
            "Node.js",
            "JavaScript",
            "REST API",
            "Cloud Deployment"
        ]
    },

    "Backend Developer": {
        "market_demand_score": 86,
        "growth_score": 85,
        "salary_range": "₹5–15 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Mumbai"
        ],
        "trending_skills": [
            "Python",
            "Node.js",
            "FastAPI",
            "SQL",
            "Docker"
        ]
    },

    "Frontend Developer": {
        "market_demand_score": 81,
        "growth_score": 78,
        "salary_range": "₹4–12 LPA",
        "demand_level": "High",
        "trend_status": "Stable",
        "top_locations": [
            "Bengaluru",
            "Pune",
            "Mumbai",
            "Hyderabad",
            "Chennai"
        ],
        "trending_skills": [
            "React",
            "JavaScript",
            "TypeScript",
            "Responsive Design",
            "REST API"
        ]
    },

    "DevOps Engineer": {
        "market_demand_score": 90,
        "growth_score": 92,
        "salary_range": "₹7–20 LPA",
        "demand_level": "Very High",
        "trend_status": "Fast Growing",
        "top_locations": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Delhi NCR"
        ],
        "trending_skills": [
            "Docker",
            "Kubernetes",
            "AWS",
            "CI/CD",
            "Terraform"
        ]
    },

    "Database Developer": {
        "market_demand_score": 75,
        "growth_score": 72,
        "salary_range": "₹4–11 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable",
        "top_locations": [
            "Bengaluru",
            "Pune",
            "Mumbai",
            "Hyderabad",
            "Chennai"
        ],
        "trending_skills": [
            "SQL",
            "PostgreSQL",
            "Query Optimization",
            "Data Modeling",
            "MongoDB"
        ]
    },

    # =====================================================
    # HUMAN RESOURCES
    # =====================================================

    "HR Operations Executive": {
        "market_demand_score": 84,
        "growth_score": 80,
        "salary_range": "₹3–8 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Bengaluru",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "HR Operations",
            "Payroll Processing",
            "HRMS",
            "Employee Relations",
            "Excel"
        ]
    },

    "HR Generalist": {
        "market_demand_score": 86,
        "growth_score": 83,
        "salary_range": "₹4–10 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Recruitment",
            "Employee Relations",
            "Onboarding",
            "HR Operations",
            "Performance Management"
        ]
    },

    "Payroll and Compliance Executive": {
        "market_demand_score": 82,
        "growth_score": 78,
        "salary_range": "₹3–8 LPA",
        "demand_level": "High",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Delhi NCR",
            "Bengaluru",
            "Ahmedabad"
        ],
        "trending_skills": [
            "Payroll Processing",
            "PF Compliance",
            "ESIC Compliance",
            "ECR Filing",
            "Excel"
        ]
    },

    "Talent Acquisition Executive": {
        "market_demand_score": 88,
        "growth_score": 85,
        "salary_range": "₹3–9 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Bengaluru",
            "Mumbai",
            "Pune",
            "Hyderabad",
            "Delhi NCR"
        ],
        "trending_skills": [
            "Recruitment",
            "Talent Acquisition",
            "Interviewing",
            "LinkedIn Sourcing",
            "Communication"
        ]
    },

    "Employee Relations Executive": {
        "market_demand_score": 76,
        "growth_score": 75,
        "salary_range": "₹4–9 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Bengaluru",
            "Delhi NCR",
            "Chennai"
        ],
        "trending_skills": [
            "Employee Relations",
            "Grievance Handling",
            "Labor Law",
            "Employee Engagement",
            "Communication"
        ]
    },

    "HR Compliance Executive": {
        "market_demand_score": 79,
        "growth_score": 76,
        "salary_range": "₹3–8 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Delhi NCR",
            "Ahmedabad",
            "Bengaluru"
        ],
        "trending_skills": [
            "Statutory Compliance",
            "PF Compliance",
            "ESIC Compliance",
            "POSH Compliance",
            "Labor Law"
        ]
    },

    # =====================================================
    # FINANCE AND ACCOUNTING
    # =====================================================

    "Accountant": {
        "market_demand_score": 78,
        "growth_score": 72,
        "salary_range": "₹3–8 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Delhi NCR",
            "Bengaluru",
            "Ahmedabad"
        ],
        "trending_skills": [
            "Accounting",
            "GST",
            "TDS",
            "Tally",
            "Excel"
        ]
    },

    "Financial Analyst": {
        "market_demand_score": 87,
        "growth_score": 88,
        "salary_range": "₹5–15 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Financial Analysis",
            "Excel",
            "Power BI",
            "Financial Forecasting",
            "Accounting"
        ]
    },

    "Accounts Executive": {
        "market_demand_score": 80,
        "growth_score": 73,
        "salary_range": "₹3–7 LPA",
        "demand_level": "High",
        "trend_status": "Stable",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Ahmedabad",
            "Delhi NCR",
            "Bengaluru"
        ],
        "trending_skills": [
            "Accounts Payable",
            "Accounts Receivable",
            "GST",
            "Tally",
            "Excel"
        ]
    },

    "Audit Associate": {
        "market_demand_score": 76,
        "growth_score": 74,
        "salary_range": "₹3–9 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable",
        "top_locations": [
            "Mumbai",
            "Delhi NCR",
            "Bengaluru",
            "Pune",
            "Chennai"
        ],
        "trending_skills": [
            "Auditing",
            "Accounting",
            "Taxation",
            "Excel",
            "Financial Reporting"
        ]
    },

    # =====================================================
    # MARKETING
    # =====================================================

    "Digital Marketing Executive": {
        "market_demand_score": 86,
        "growth_score": 88,
        "salary_range": "₹3–10 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "SEO",
            "Social Media Marketing",
            "Google Ads",
            "Content Marketing",
            "Campaign Management"
        ]
    },

    "SEO Specialist": {
        "market_demand_score": 80,
        "growth_score": 82,
        "salary_range": "₹3–9 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Bengaluru",
            "Delhi NCR",
            "Ahmedabad"
        ],
        "trending_skills": [
            "SEO",
            "SEM",
            "Content Marketing",
            "Google Analytics",
            "Keyword Research"
        ]
    },

    "Content Marketing Executive": {
        "market_demand_score": 79,
        "growth_score": 81,
        "salary_range": "₹3–9 LPA",
        "demand_level": "Moderate",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Content Marketing",
            "Copywriting",
            "SEO",
            "Social Media Marketing",
            "Brand Management"
        ]
    },

    "Marketing Analyst": {
        "market_demand_score": 83,
        "growth_score": 84,
        "salary_range": "₹4–12 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Market Research",
            "Excel",
            "Power BI",
            "Data Analysis",
            "Campaign Management"
        ]
    },

    # =====================================================
    # SALES AND BUSINESS DEVELOPMENT
    # =====================================================

    "Sales Executive": {
        "market_demand_score": 88,
        "growth_score": 78,
        "salary_range": "₹3–9 LPA + incentives",
        "demand_level": "High",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Mumbai",
            "Delhi NCR",
            "Bengaluru",
            "Pune",
            "Hyderabad"
        ],
        "trending_skills": [
            "Sales",
            "CRM",
            "Negotiation",
            "Lead Generation",
            "Communication"
        ]
    },

    "Business Development Executive": {
        "market_demand_score": 90,
        "growth_score": 85,
        "salary_range": "₹3–10 LPA + incentives",
        "demand_level": "Very High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Business Development",
            "Lead Generation",
            "CRM",
            "Negotiation",
            "Client Acquisition"
        ]
    },

    "Account Manager": {
        "market_demand_score": 82,
        "growth_score": 81,
        "salary_range": "₹5–14 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Account Management",
            "CRM",
            "Negotiation",
            "Client Relationship",
            "Communication"
        ]
    },

    # =====================================================
    # OPERATIONS
    # =====================================================

    "Operations Executive": {
        "market_demand_score": 82,
        "growth_score": 77,
        "salary_range": "₹3–8 LPA",
        "demand_level": "High",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Bengaluru",
            "Delhi NCR",
            "Chennai"
        ],
        "trending_skills": [
            "Operations Management",
            "Excel",
            "Process Improvement",
            "Vendor Management",
            "Communication"
        ]
    },

    "Supply Chain Executive": {
        "market_demand_score": 84,
        "growth_score": 86,
        "salary_range": "₹4–11 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Chennai",
            "Delhi NCR",
            "Bengaluru"
        ],
        "trending_skills": [
            "Supply Chain Management",
            "Procurement",
            "Inventory Management",
            "Logistics",
            "Excel"
        ]
    },

    "Logistics Executive": {
        "market_demand_score": 80,
        "growth_score": 82,
        "salary_range": "₹3–8 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Chennai",
            "Delhi NCR",
            "Ahmedabad"
        ],
        "trending_skills": [
            "Logistics",
            "Warehouse Management",
            "Inventory Management",
            "Excel",
            "Vendor Management"
        ]
    },

    "Procurement Executive": {
        "market_demand_score": 78,
        "growth_score": 79,
        "salary_range": "₹4–10 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Chennai",
            "Delhi NCR",
            "Bengaluru"
        ],
        "trending_skills": [
            "Procurement",
            "Vendor Management",
            "Negotiation",
            "Supply Chain Management",
            "Excel"
        ]
    },

    # =====================================================
    # CUSTOMER SERVICE
    # =====================================================

    "Customer Service Executive": {
        "market_demand_score": 84,
        "growth_score": 72,
        "salary_range": "₹2.5–6 LPA",
        "demand_level": "High",
        "trend_status": "Stable",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Bengaluru",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Customer Service",
            "Communication",
            "Complaint Resolution",
            "CRM",
            "Email Support"
        ]
    },

    "Customer Support Associate": {
        "market_demand_score": 85,
        "growth_score": 75,
        "salary_range": "₹2.5–7 LPA",
        "demand_level": "High",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Bengaluru",
            "Pune",
            "Hyderabad",
            "Mumbai",
            "Delhi NCR"
        ],
        "trending_skills": [
            "Customer Service",
            "Ticket Management",
            "Communication",
            "Problem Solving",
            "Chat Support"
        ]
    },

    # =====================================================
    # EDUCATION AND TRAINING
    # =====================================================

    "Teacher": {
        "market_demand_score": 74,
        "growth_score": 71,
        "salary_range": "₹3–8 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable",
        "top_locations": [
            "Mumbai",
            "Pune",
            "Delhi NCR",
            "Bengaluru",
            "Hyderabad"
        ],
        "trending_skills": [
            "Teaching",
            "Lesson Planning",
            "Student Assessment",
            "Communication",
            "Digital Learning Tools"
        ]
    },

    "Corporate Trainer": {
        "market_demand_score": 79,
        "growth_score": 82,
        "salary_range": "₹4–12 LPA",
        "demand_level": "Moderate",
        "trend_status": "Growing",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Training",
            "Communication",
            "Curriculum Development",
            "Presentation Skills",
            "Leadership"
        ]
    },

    # =====================================================
    # DESIGN
    # =====================================================

    "Graphic Designer": {
        "market_demand_score": 78,
        "growth_score": 76,
        "salary_range": "₹3–9 LPA",
        "demand_level": "Moderate",
        "trend_status": "Stable Growth",
        "top_locations": [
            "Mumbai",
            "Bengaluru",
            "Pune",
            "Delhi NCR",
            "Hyderabad"
        ],
        "trending_skills": [
            "Graphic Design",
            "Adobe Photoshop",
            "Adobe Illustrator",
            "Canva",
            "Branding"
        ]
    },

    "UI Designer": {
        "market_demand_score": 82,
        "growth_score": 86,
        "salary_range": "₹4–13 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Bengaluru",
            "Pune",
            "Mumbai",
            "Hyderabad",
            "Delhi NCR"
        ],
        "trending_skills": [
            "UI Design",
            "Figma",
            "Wireframing",
            "Prototyping",
            "Design Systems"
        ]
    },

    "UX Designer": {
        "market_demand_score": 84,
        "growth_score": 88,
        "salary_range": "₹5–15 LPA",
        "demand_level": "High",
        "trend_status": "Growing",
        "top_locations": [
            "Bengaluru",
            "Pune",
            "Mumbai",
            "Hyderabad",
            "Delhi NCR"
        ],
        "trending_skills": [
            "UX Design",
            "Figma",
            "User Research",
            "Wireframing",
            "Prototyping"
        ]
    }
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalize_skill(
    skill: str
) -> str:
    return " ".join(
        str(skill).strip().lower().split()
    )


def calculate_trending_skill_match(
    *,
    extracted_skills: list[str],
    trending_skills: list[str]
) -> dict[str, Any]:
    normalized_user_skills = {
        normalize_skill(skill)
        for skill in extracted_skills
        if str(skill).strip()
    }

    matched_trending_skills = []
    missing_trending_skills = []

    for skill in trending_skills:
        if (
            normalize_skill(skill)
            in normalized_user_skills
        ):
            matched_trending_skills.append(
                skill
            )
        else:
            missing_trending_skills.append(
                skill
            )

    total_trending_skills = len(
        trending_skills
    )

    if total_trending_skills == 0:
        trending_skill_score = 0
    else:
        trending_skill_score = round(
            len(matched_trending_skills)
            / total_trending_skills
            * 100
        )

    return {
        "trending_skill_score":
            trending_skill_score,

        "matched_trending_skills":
            matched_trending_skills,

        "missing_trending_skills":
            missing_trending_skills
    }


def get_default_market_trend() -> dict[str, Any]:
    return {
        "market_demand_score": 65,
        "growth_score": 65,
        "salary_range": "Market data unavailable",
        "demand_level": "Moderate",
        "trend_status": "Stable",
        "top_locations": [],
        "trending_skills": []
    }


def enrich_career_with_market_trend(
    *,
    career_prediction: dict[str, Any],
    extracted_skills: list[str]
) -> dict[str, Any]:
    career_name = str(
        career_prediction.get(
            "career",
            ""
        )
    ).strip()

    market_trend = (
        CAREER_MARKET_TRENDS.get(
            career_name,
            get_default_market_trend()
        )
    )

    skill_trend_result = (
        calculate_trending_skill_match(
            extracted_skills=
                extracted_skills,

            trending_skills=
                market_trend.get(
                    "trending_skills",
                    []
                )
        )
    )

    resume_match_score = int(
        career_prediction.get(
            "match_percentage",
            0
        )
        or 0
    )

    market_demand_score = int(
        market_trend.get(
            "market_demand_score",
            65
        )
        or 65
    )

    growth_score = int(
        market_trend.get(
            "growth_score",
            65
        )
        or 65
    )

    trending_skill_score = int(
        skill_trend_result.get(
            "trending_skill_score",
            0
        )
        or 0
    )

    # Resume match remains the most important factor.
    final_career_score = round(
        resume_match_score * 0.55
        + market_demand_score * 0.20
        + trending_skill_score * 0.15
        + growth_score * 0.10
    )

    return {
        **career_prediction,

        "resume_match_score":
            resume_match_score,

        "market_demand_score":
            market_demand_score,

        "growth_score":
            growth_score,

        "trending_skill_score":
            trending_skill_score,

        "final_career_score":
            min(
                max(
                    final_career_score,
                    0
                ),
                100
            ),

        "salary_range":
            market_trend.get(
                "salary_range",
                "Market data unavailable"
            ),

        "demand_level":
            market_trend.get(
                "demand_level",
                "Moderate"
            ),

        "trend_status":
            market_trend.get(
                "trend_status",
                "Stable"
            ),

        "top_locations":
            market_trend.get(
                "top_locations",
                []
            ),

        "trending_skills":
            market_trend.get(
                "trending_skills",
                []
            ),

        "matched_trending_skills":
            skill_trend_result[
                "matched_trending_skills"
            ],

        "missing_trending_skills":
            skill_trend_result[
                "missing_trending_skills"
            ]
    }


def apply_market_trends(
    *,
    career_predictions: list[
        dict[str, Any]
    ],
    extracted_skills: list[str],
    limit: int = 5
) -> list[dict[str, Any]]:
    """
    Combine resume-based career predictions with
    current local market-trend data.
    """

    enriched_predictions = []

    for prediction in career_predictions:
        enriched_prediction = (
            enrich_career_with_market_trend(
                career_prediction=
                    prediction,

                extracted_skills=
                    extracted_skills
            )
        )

        enriched_predictions.append(
            enriched_prediction
        )

    enriched_predictions.sort(
        key=lambda item: (
            item.get(
                "final_career_score",
                0
            ),
            item.get(
                "resume_match_score",
                0
            ),
            item.get(
                "market_demand_score",
                0
            )
        ),
        reverse=True
    )

    return enriched_predictions[:limit]

# =========================================================
# LIVE MARKET TREND INTEGRATION
# =========================================================

def normalize_live_skill_items(
    live_skills: Any
) -> list[str]:
    """
    Convert live API skill objects into a simple list
    of skill names.

    Example:
        [{"skill": "Excel", "frequency": 10}]

    Becomes:
        ["Excel"]
    """

    if not isinstance(
        live_skills,
        list
    ):
        return []

    normalized_skills = []

    for item in live_skills:
        if isinstance(
            item,
            dict
        ):
            skill_name = str(
                item.get(
                    "skill",
                    ""
                )
            ).strip()

        else:
            skill_name = str(
                item
            ).strip()

        if (
            skill_name
            and skill_name
            not in normalized_skills
        ):
            normalized_skills.append(
                skill_name
            )

    return normalized_skills


def normalize_live_locations(
    live_locations: Any
) -> list[str]:
    """
    Convert live API location objects into strings.
    """

    if not isinstance(
        live_locations,
        list
    ):
        return []

    normalized_locations = []

    for item in live_locations:
        if isinstance(
            item,
            dict
        ):
            location_name = str(
                item.get(
                    "location",
                    ""
                )
            ).strip()

        else:
            location_name = str(
                item
            ).strip()

        if (
            location_name
            and location_name
            not in normalized_locations
        ):
            normalized_locations.append(
                location_name
            )

    return normalized_locations


def normalize_live_companies(
    live_companies: Any
) -> list[str]:
    """
    Convert live API company objects into strings.
    """

    if not isinstance(
        live_companies,
        list
    ):
        return []

    normalized_companies = []

    for item in live_companies:
        if isinstance(
            item,
            dict
        ):
            company_name = str(
                item.get(
                    "company",
                    ""
                )
            ).strip()

        else:
            company_name = str(
                item
            ).strip()

        if (
            company_name
            and company_name
            not in normalized_companies
        ):
            normalized_companies.append(
                company_name
            )

    return normalized_companies


def format_indian_salary(
    annual_salary: Any
) -> str:
    """
    Convert annual salary into an Indian LPA string.

    Example:
        576923 -> ₹5.8 LPA
    """

    try:
        salary_value = float(
            annual_salary
        )

    except (
        TypeError,
        ValueError
    ):
        return "Salary data unavailable"

    if salary_value <= 0:
        return "Salary data unavailable"

    salary_lpa = salary_value / 100000

    return f"₹{salary_lpa:.1f} LPA"


def calculate_live_trending_skill_match(
    *,
    extracted_skills: list[str],
    live_trending_skills: list[str]
) -> dict[str, Any]:
    """
    Compare resume skills with skills frequently
    mentioned in current job advertisements.
    """

    normalized_resume_skills = {
        normalize_skill(skill)
        for skill in extracted_skills
        if str(skill).strip()
    }

    matched_skills = []
    missing_skills = []

    for skill in live_trending_skills:
        if (
            normalize_skill(skill)
            in normalized_resume_skills
        ):
            matched_skills.append(
                skill
            )

        else:
            missing_skills.append(
                skill
            )

    total_skills = len(
        live_trending_skills
    )

    if total_skills == 0:
        score = 0

    else:
        score = round(
            len(matched_skills)
            / total_skills
            * 100
        )

    return {
        "score":
            score,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills
    }
DOMAIN_ALLOWED_SKILLS = {
    "Human Resources": {
        "HR Operations",
        "Recruitment",
        "Payroll Processing",
        "Employee Relations",
        "HRMS",
        "Statutory Compliance",
        "PF Compliance",
        "ESIC Compliance",
        "ECR Filing",
        "POSH Compliance",
        "Attendance Management",
        "Workforce Management",
        "Grievance Handling",
        "Talent Acquisition",
        "Interviewing",
        "Onboarding",
        "Performance Management",
        "Employee Engagement",
        "Labor Law",
        "HR Reporting",
        "Excel",
        "Communication",
        "Interpersonal Skills",
        "Leadership",
        "Training"
    },

    "Technology": {
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "React",
        "Node.js",
        "SQL",
        "AWS",
        "Docker",
        "Kubernetes",
        "REST API",
        "FastAPI",
        "Git",
        "GitHub",
        "CI/CD",
        "Terraform",
        "Linux",
        "PostgreSQL",
        "MongoDB",
        "Problem Solving",
        "Communication"
    },

    "Data and Artificial Intelligence": {
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Power BI",
        "Tableau",
        "Statistics",
        "Data Visualization",
        "EDA",
        "Excel",
        "Communication"
    },

    "Finance and Accounting": {
        "Accounting",
        "Bookkeeping",
        "Financial Reporting",
        "Financial Analysis",
        "Accounts Payable",
        "Accounts Receivable",
        "Bank Reconciliation",
        "GST",
        "TDS",
        "Taxation",
        "Auditing",
        "Budgeting",
        "Financial Forecasting",
        "Tally",
        "SAP FICO",
        "Invoice Processing",
        "Excel",
        "MS Office",
        "Communication"
    },

    "Marketing": {
        "Digital Marketing",
        "Social Media Marketing",
        "SEO",
        "SEM",
        "Content Marketing",
        "Email Marketing",
        "Google Ads",
        "Meta Ads",
        "Campaign Management",
        "Market Research",
        "Brand Management",
        "Copywriting",
        "Lead Generation",
        "Excel",
        "Communication"
    },

    "Sales and Business Development": {
        "Sales",
        "Business Development",
        "Client Acquisition",
        "CRM",
        "Cold Calling",
        "Negotiation",
        "Account Management",
        "Sales Pipeline Management",
        "Revenue Generation",
        "Lead Generation",
        "Communication",
        "Interpersonal Skills"
    },

    "Operations and Supply Chain": {
        "Operations Management",
        "Supply Chain Management",
        "Logistics",
        "Inventory Management",
        "Procurement",
        "Vendor Management",
        "Warehouse Management",
        "Process Improvement",
        "Quality Management",
        "Excel",
        "MS Office",
        "Communication",
        "Problem Solving"
    },

    "Customer Service": {
        "Customer Service",
        "Complaint Resolution",
        "Ticket Management",
        "Call Handling",
        "Customer Satisfaction",
        "Email Support",
        "Chat Support",
        "CRM",
        "Communication",
        "Interpersonal Skills",
        "Problem Solving"
    },

    "Education and Training": {
        "Teaching",
        "Training",
        "Curriculum Development",
        "Lesson Planning",
        "Student Assessment",
        "Classroom Management",
        "Mentoring",
        "Communication",
        "Leadership",
        "MS Office"
    },

    "Design and Creative": {
        "Graphic Design",
        "UI Design",
        "UX Design",
        "Figma",
        "Adobe Photoshop",
        "Adobe Illustrator",
        "Canva",
        "Wireframing",
        "Prototyping",
        "Video Editing",
        "Communication",
        "Problem Solving"
    }
}


def normalize_skill_name(
    value: str
) -> str:
    return " ".join(
        str(value or "")
        .strip()
        .lower()
        .split()
    )


def detect_career_domain(
    *,
    career_name: str,
    career_description: str = "",
    extracted_skills: list[str] | None = None
) -> str:
    """
    Detect the most suitable domain for one career.
    """

    detection_text = " ".join(
        [
            career_name,
            career_description,
            " ".join(
                extracted_skills or []
            )
        ]
    )

    result = detect_resume_domain(
        detection_text
    )

    return (
        result.get(
            "detected_domain"
        )
        or "General"
    )


def filter_trending_skills_by_domain(
    *,
    skills: list[str],
    domain: str
) -> list[str]:
    """
    Keep only market skills relevant to the selected
    career domain.
    """

    allowed_skills = DOMAIN_ALLOWED_SKILLS.get(
        domain
    )

    if not allowed_skills:
        return skills

    normalized_allowed = {
        normalize_skill_name(skill)
        for skill in allowed_skills
    }

    filtered = []

    for skill in skills:
        normalized_skill = normalize_skill_name(
            skill
        )

        if (
            normalized_skill
            in normalized_allowed
            and skill not in filtered
        ):
            filtered.append(
                skill
            )

    return filtered

async def enrich_career_with_live_market(
    *,
    career_prediction: dict[str, Any],
    extracted_skills: list[str],
    location: str = "India"
) -> dict[str, Any]:
    """
    Try to enrich one career using live Adzuna data.

    If the API fails, use the existing local market
    trend values instead.
    """

    career_name = str(
        career_prediction.get(
            "career",
            ""
        )
    ).strip()

    # Local result is always prepared first so it can
    # be used safely as a fallback.
    local_result = (
        enrich_career_with_market_trend(
            career_prediction=
                career_prediction,

            extracted_skills=
                extracted_skills
        )
    )

    if not career_name:
        return {
            **local_result,

            "market_data_source":
                "Local fallback",

            "live_data_available":
                False,

            "live_job_count":
                0,

            "average_salary":
                None,

            "top_companies":
                [],

            "market_data_updated_at":
                None
        }

    try:
        live_result = (
            await analyze_live_job_market(
                role=
                    career_name,

                location=
                    location,

                results_per_page=
                    50
            )
        )

    except Exception as error:
        print(
            "Live market API error "
            f"for {career_name}:",
            error
        )

        return {
            **local_result,

            "market_data_source":
                "Local fallback",

            "live_data_available":
                False,

            "live_job_count":
                0,

            "average_salary":
                None,

            "top_companies":
                [],

            "market_data_updated_at":
                None
        }

    if not live_result.get(
        "success"
    ):
        return {
            **local_result,

            "market_data_source":
                "Local fallback",

            "live_data_available":
                False,

            "live_job_count":
                0,

            "average_salary":
                None,

            "top_companies":
                [],

            "market_data_updated_at":
                None
        }

    raw_live_trending_skills = (
        normalize_live_skill_items(
            live_result.get(
                "trending_skills",
                []
            )
        )
    )

    career_domain = detect_career_domain(
        career_name=career_name,
        career_description=str(
            career_prediction.get(
                "description",
                ""
            )
        ),
        extracted_skills=extracted_skills
    )

    live_trending_skills = (
        filter_trending_skills_by_domain(
            skills=raw_live_trending_skills,
            domain=career_domain
        )
    )

    skill_match_result = (
        calculate_live_trending_skill_match(
            extracted_skills=
                extracted_skills,

            live_trending_skills=
                live_trending_skills
        )
    )

    resume_match_score = int(
        career_prediction.get(
            "match_percentage",
            0
        )
        or 0
    )

    live_market_demand_score = int(
        live_result.get(
            "market_demand_score",
            0
        )
        or 0
    )

    trending_skill_score = int(
        skill_match_result.get(
            "score",
            0
        )
        or 0
    )

    # Growth score is currently taken from the local
    # structured trend dataset because the job-search
    # result does not directly provide future growth.
    growth_score = int(
        local_result.get(
            "growth_score",
            65
        )
        or 65
    )

    final_career_score = round(
        resume_match_score * 0.55
        + live_market_demand_score * 0.20
        + trending_skill_score * 0.15
        + growth_score * 0.10
    )

    average_salary = (
        live_result.get(
            "average_salary"
        )
    )

    salary_range = (
        format_indian_salary(
            average_salary
        )
        if average_salary
        else local_result.get(
            "salary_range",
            "Salary data unavailable"
        )
    )

    return {
        **career_prediction,

        "career_domain":
            career_domain,

        "resume_match_score":
            resume_match_score,

        "market_demand_score":
            live_market_demand_score,

        "growth_score":
            growth_score,

        "trending_skill_score":
            trending_skill_score,

        "final_career_score":
            min(
                max(
                    final_career_score,
                    0
                ),
                100
            ),

        "salary_range":
            salary_range,

        "demand_level":
            live_result.get(
                "demand_level",
                local_result.get(
                    "demand_level",
                    "Moderate"
                )
            ),

        "trend_status":
            local_result.get(
                "trend_status",
                "Current Market"
            ),

        "top_locations":
            normalize_live_locations(
                live_result.get(
                    "top_locations",
                    []
                )
            ),

        "top_companies":
            normalize_live_companies(
                live_result.get(
                    "top_companies",
                    []
                )
            ),

        "trending_skills":
            live_trending_skills,

        "matched_trending_skills":
            skill_match_result[
                "matched_skills"
            ],

        "missing_trending_skills":
            skill_match_result[
                "missing_skills"
            ],

        "live_job_count":
            int(
                live_result.get(
                    "job_count",
                    0
                )
                or 0
            ),

        "average_salary":
            average_salary,

        "market_data_source":
            live_result.get(
                "source",
                "Adzuna"
            ),

        "live_data_available":
            True,

        "market_data_updated_at":
            live_result.get(
                "fetched_at"
            )
    }


async def apply_live_market_trends(
    *,
    career_predictions: list[
        dict[str, Any]
    ],
    extracted_skills: list[str],
    location: str = "India",
    limit: int = 5
) -> list[dict[str, Any]]:
    """
    Enrich multiple predicted careers concurrently
    using live job-market data.

    Local values are automatically used when a live
    request fails.
    """

    if not career_predictions:
        return []

    tasks = [
        enrich_career_with_live_market(
            career_prediction=
                prediction,

            extracted_skills=
                extracted_skills,

            location=
                location
        )
        for prediction in career_predictions
    ]

    enriched_predictions = (
        await asyncio.gather(
            *tasks
        )
    )

    enriched_predictions.sort(
        key=lambda item: (
            item.get(
                "final_career_score",
                0
            ),
            item.get(
                "resume_match_score",
                0
            ),
            item.get(
                "market_demand_score",
                0
            )
        ),
        reverse=True
    )

    return enriched_predictions[:limit]