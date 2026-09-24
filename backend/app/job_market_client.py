import os
import re
from collections import Counter
from datetime import datetime, timezone
from statistics import mean
from typing import Any

import httpx
from dotenv import load_dotenv


load_dotenv()


ADZUNA_APP_ID = os.getenv(
    "ADZUNA_APP_ID",
    ""
).strip()

ADZUNA_APP_KEY = os.getenv(
    "ADZUNA_APP_KEY",
    ""
).strip()

ADZUNA_COUNTRY = os.getenv(
    "ADZUNA_COUNTRY",
    "in"
).strip().lower()

ADZUNA_DEFAULT_LOCATION = os.getenv(
    "ADZUNA_DEFAULT_LOCATION",
    "India"
).strip()

ADZUNA_BASE_URL = (
    "https://api.adzuna.com/v1/api"
)

REQUEST_TIMEOUT_SECONDS = 15.0


COMMON_MARKET_SKILLS = {
    # Technology
    "Python": [
        "python"
    ],
    "Java": [
        "java"
    ],
    "JavaScript": [
        "javascript",
        "java script"
    ],
    "React": [
        "react",
        "react.js",
        "reactjs"
    ],
    "Node.js": [
        "node.js",
        "nodejs"
    ],
    "SQL": [
        "sql"
    ],
    "AWS": [
        "aws",
        "amazon web services"
    ],
    "Docker": [
        "docker"
    ],
    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],
    "Machine Learning": [
        "machine learning"
    ],
    "Power BI": [
        "power bi",
        "powerbi"
    ],

    # Human Resources
    "Recruitment": [
        "recruitment",
        "recruiting"
    ],
    "Payroll Processing": [
        "payroll",
        "payroll processing"
    ],
    "HR Operations": [
        "hr operations"
    ],
    "Employee Relations": [
        "employee relations"
    ],
    "HRMS": [
        "hrms"
    ],
    "Statutory Compliance": [
        "statutory compliance"
    ],
    "PF Compliance": [
        "provident fund",
        "pf compliance"
    ],
    "ESIC Compliance": [
        "esic"
    ],

    # Finance
    "Accounting": [
        "accounting"
    ],
    "GST": [
        "gst"
    ],
    "TDS": [
        "tds"
    ],
    "Tally": [
        "tally"
    ],
    "Financial Analysis": [
        "financial analysis"
    ],
    "Auditing": [
        "audit",
        "auditing"
    ],

    # Marketing
    "Digital Marketing": [
        "digital marketing"
    ],
    "SEO": [
        "seo",
        "search engine optimization"
    ],
    "SEM": [
        "sem",
        "search engine marketing"
    ],
    "Google Ads": [
        "google ads",
        "google adwords"
    ],
    "Social Media Marketing": [
        "social media marketing"
    ],
    "Content Marketing": [
        "content marketing"
    ],

    # Sales
    "Sales": [
        "sales"
    ],
    "CRM": [
        "crm"
    ],
    "Lead Generation": [
        "lead generation"
    ],
    "Negotiation": [
        "negotiation"
    ],
    "Business Development": [
        "business development"
    ],

    # Operations
    "Operations Management": [
        "operations management"
    ],
    "Supply Chain Management": [
        "supply chain"
    ],
    "Logistics": [
        "logistics"
    ],
    "Procurement": [
        "procurement"
    ],
    "Inventory Management": [
        "inventory management"
    ],

    # Healthcare
    "Patient Care": [
        "patient care"
    ],
    "Clinical Documentation": [
        "clinical documentation"
    ],
    "Nursing": [
        "nursing"
    ],
    "Medical Coding": [
        "medical coding"
    ],

    # Education
    "Teaching": [
        "teaching"
    ],
    "Training": [
        "training"
    ],
    "Curriculum Development": [
        "curriculum development"
    ],

    # Design
    "Figma": [
        "figma"
    ],
    "Graphic Design": [
        "graphic design"
    ],
    "UI Design": [
        "ui design"
    ],
    "UX Design": [
        "ux design"
    ],

    # Common
    "Excel": [
        "excel",
        "ms excel",
        "microsoft excel"
    ],
    "Communication": [
        "communication skills",
        "communication"
    ],
    "Leadership": [
        "leadership"
    ],
    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ]
}


def has_live_api_credentials() -> bool:
    return bool(
        ADZUNA_APP_ID
        and ADZUNA_APP_KEY
    )


def normalize_text(
    value: Any
) -> str:
    if value is None:
        return ""

    text = str(value).lower()

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def contains_phrase(
    text: str,
    phrase: str
) -> bool:
    normalized_text = normalize_text(
        text
    )

    normalized_phrase = normalize_text(
        phrase
    )

    if not normalized_phrase:
        return False

    pattern = (
        rf"(?<![a-z0-9])"
        rf"{re.escape(normalized_phrase)}"
        rf"(?![a-z0-9])"
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE
        )
    )


def extract_market_skills(
    job_texts: list[str],
    limit: int = 15
) -> list[dict[str, Any]]:
    skill_counter = Counter()

    for job_text in job_texts:
        for skill_name, aliases in (
            COMMON_MARKET_SKILLS.items()
        ):
            if any(
                contains_phrase(
                    job_text,
                    alias
                )
                for alias in aliases
            ):
                skill_counter[
                    skill_name
                ] += 1

    return [
        {
            "skill": skill_name,
            "frequency": frequency
        }
        for skill_name, frequency in (
            skill_counter.most_common(
                limit
            )
        )
    ]


def calculate_demand_score(
    job_count: int
) -> int:
    """
    Convert vacancy count into a 0-100 demand score.

    This logarithmic-style banding prevents very large
    vacancy counts from dominating the recommendation.
    """

    if job_count <= 0:
        return 0

    if job_count < 10:
        return 35

    if job_count < 25:
        return 45

    if job_count < 50:
        return 55

    if job_count < 100:
        return 65

    if job_count < 250:
        return 75

    if job_count < 500:
        return 82

    if job_count < 1000:
        return 88

    return 94


def get_demand_level(
    score: int
) -> str:
    if score >= 90:
        return "Very High"

    if score >= 75:
        return "High"

    if score >= 55:
        return "Moderate"

    if score >= 35:
        return "Low"

    return "Very Low"


def calculate_average_salary(
    jobs: list[dict[str, Any]]
) -> dict[str, Any]:
    salary_values = []

    for job in jobs:
        salary_min = job.get(
            "salary_min"
        )

        salary_max = job.get(
            "salary_max"
        )

        valid_values = [
            float(value)
            for value in [
                salary_min,
                salary_max
            ]
            if isinstance(
                value,
                (int, float)
            )
            and value > 0
        ]

        if valid_values:
            salary_values.append(
                mean(valid_values)
            )

    if not salary_values:
        return {
            "average_salary":
                None,

            "salary_data_available":
                False,

            "salary_sample_count":
                0
        }

    return {
        "average_salary":
            round(
                mean(salary_values)
            ),

        "salary_data_available":
            True,

        "salary_sample_count":
            len(salary_values)
    }


def collect_top_locations(
    jobs: list[dict[str, Any]],
    limit: int = 5
) -> list[dict[str, Any]]:
    location_counter = Counter()

    for job in jobs:
        location = (
            job.get(
                "location",
                {}
            )
            or {}
        )

        display_name = str(
            location.get(
                "display_name",
                ""
            )
        ).strip()

        if display_name:
            location_counter[
                display_name
            ] += 1

    return [
        {
            "location":
                location_name,

            "job_count":
                count
        }
        for location_name, count in (
            location_counter.most_common(
                limit
            )
        )
    ]


def collect_top_companies(
    jobs: list[dict[str, Any]],
    limit: int = 5
) -> list[dict[str, Any]]:
    company_counter = Counter()

    for job in jobs:
        company = (
            job.get(
                "company",
                {}
            )
            or {}
        )

        company_name = str(
            company.get(
                "display_name",
                ""
            )
        ).strip()

        if company_name:
            company_counter[
                company_name
            ] += 1

    return [
        {
            "company":
                company_name,

            "job_count":
                count
        }
        for company_name, count in (
            company_counter.most_common(
                limit
            )
        )
    ]


async def search_current_jobs(
    *,
    role: str,
    location: str | None = None,
    results_per_page: int = 50,
    page: int = 1
) -> dict[str, Any]:
    """
    Search live current job advertisements for any
    occupation title and location.
    """

    clean_role = str(
        role or ""
    ).strip()

    if not clean_role:
        raise ValueError(
            "A role title is required."
        )

    if not has_live_api_credentials():
        return {
            "success": False,
            "source": "Adzuna",
            "error": (
                "Adzuna API credentials are not configured."
            ),
            "role": clean_role,
            "location": (
                location
                or ADZUNA_DEFAULT_LOCATION
            ),
            "job_count": 0,
            "jobs": [],
            "fetched_at": None
        }

    safe_page = max(
        int(page),
        1
    )

    safe_results_per_page = min(
        max(
            int(results_per_page),
            1
        ),
        50
    )

    search_location = (
        str(location).strip()
        if location
        else ADZUNA_DEFAULT_LOCATION
    )

    endpoint = (
        f"{ADZUNA_BASE_URL}/jobs/"
        f"{ADZUNA_COUNTRY}/search/"
        f"{safe_page}"
    )

    params = {
        "app_id":
            ADZUNA_APP_ID,

        "app_key":
            ADZUNA_APP_KEY,

        "what":
            clean_role,

        "where":
            search_location,

        "results_per_page":
            safe_results_per_page,

        "content-type":
            "application/json",

        "sort_by":
            "date"
    }

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_SECONDS
        ) as client:
            response = await client.get(
                endpoint,
                params=params,
                headers={
                    "Accept":
                        "application/json"
                }
            )

            response.raise_for_status()

            payload = response.json()

    except httpx.TimeoutException:
        return {
            "success": False,
            "source": "Adzuna",
            "error": (
                "The live job-market request timed out."
            ),
            "role": clean_role,
            "location": search_location,
            "job_count": 0,
            "jobs": [],
            "fetched_at": None
        }

    except httpx.HTTPStatusError as error:
        return {
            "success": False,
            "source": "Adzuna",
            "error": (
                "The live job-market API returned "
                f"HTTP {error.response.status_code}."
            ),
            "role": clean_role,
            "location": search_location,
            "job_count": 0,
            "jobs": [],
            "fetched_at": None
        }

    except (
        httpx.RequestError,
        ValueError,
        TypeError
    ) as error:
        return {
            "success": False,
            "source": "Adzuna",
            "error": str(error),
            "role": clean_role,
            "location": search_location,
            "job_count": 0,
            "jobs": [],
            "fetched_at": None
        }

    raw_jobs = payload.get(
        "results",
        []
    )

    if not isinstance(
        raw_jobs,
        list
    ):
        raw_jobs = []

    job_count = int(
        payload.get(
            "count",
            0
        )
        or 0
    )

    fetched_at = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    return {
        "success": True,
        "source": "Adzuna",
        "role": clean_role,
        "location": search_location,
        "job_count": job_count,
        "jobs": raw_jobs,
        "fetched_at": fetched_at
    }


async def analyze_live_job_market(
    *,
    role: str,
    location: str | None = None,
    results_per_page: int = 50
) -> dict[str, Any]:
    """
    Fetch and summarize current job-market data for
    any role across any supported professional domain.
    """

    search_result = await search_current_jobs(
        role=role,
        location=location,
        results_per_page=results_per_page
    )

    if not search_result.get(
        "success"
    ):
        return {
            **search_result,

            "market_demand_score":
                0,

            "demand_level":
                "Unavailable",

            "average_salary":
                None,

            "salary_data_available":
                False,

            "salary_sample_count":
                0,

            "top_locations":
                [],

            "top_companies":
                [],

            "trending_skills":
                []
        }

    jobs = search_result.get(
        "jobs",
        []
    )

    job_texts = []

    for job in jobs:
        combined_text = " ".join(
            [
                str(
                    job.get(
                        "title",
                        ""
                    )
                ),
                str(
                    job.get(
                        "description",
                        ""
                    )
                )
            ]
        )

        job_texts.append(
            combined_text
        )

    salary_result = (
        calculate_average_salary(
            jobs
        )
    )

    job_count = int(
        search_result.get(
            "job_count",
            0
        )
        or 0
    )

    demand_score = calculate_demand_score(
        job_count
    )

    return {
        "success": True,

        "source":
            search_result.get(
                "source",
                "Adzuna"
            ),

        "role":
            search_result.get(
                "role",
                role
            ),

        "location":
            search_result.get(
                "location",
                location
            ),

        "job_count":
            job_count,

        "market_demand_score":
            demand_score,

        "demand_level":
            get_demand_level(
                demand_score
            ),

        "average_salary":
            salary_result[
                "average_salary"
            ],

        "salary_data_available":
            salary_result[
                "salary_data_available"
            ],

        "salary_sample_count":
            salary_result[
                "salary_sample_count"
            ],

        "top_locations":
            collect_top_locations(
                jobs
            ),

        "top_companies":
            collect_top_companies(
                jobs
            ),

        "trending_skills":
            extract_market_skills(
                job_texts
            ),

        "sample_job_count":
            len(jobs),

        "fetched_at":
            search_result.get(
                "fetched_at"
            )
    }