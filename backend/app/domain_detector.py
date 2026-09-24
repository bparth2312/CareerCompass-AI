import re
from typing import Any


DOMAIN_KEYWORDS = {
    "Human Resources": {
        "keywords": [
            "human resources",
            "human resource",
            "hr executive",
            "hr operations",
            "hr generalist",
            "hr manager",
            "hr intern",
            "employee relations",
            "employee engagement",
            "employee lifecycle",
            "payroll",
            "payroll processing",
            "attendance management",
            "workforce management",
            "recruitment",
            "talent acquisition",
            "onboarding",
            "offboarding",
            "grievance handling",
            "performance management",
            "statutory compliance",
            "labor law",
            "labour law",
            "pf",
            "esic",
            "ecr",
            "posh",
            "she-box",
            "hrms",
            "interviews",
            "employee records",
            "benefits administration"
        ],
        "title_keywords": [
            "hr executive",
            "hr intern",
            "hr manager",
            "hr generalist",
            "human resources",
            "talent acquisition",
            "recruiter",
            "payroll executive"
        ]
    },

    "Technology": {
        "keywords": [
            "software developer",
            "software engineer",
            "frontend",
            "backend",
            "full stack",
            "web developer",
            "application developer",
            "python",
            "java",
            "javascript",
            "react",
            "node.js",
            "express.js",
            "fastapi",
            "django",
            "flask",
            "html",
            "css",
            "rest api",
            "mongodb",
            "postgresql",
            "mysql",
            "git",
            "github",
            "docker",
            "kubernetes",
            "cloud",
            "aws",
            "azure",
            "devops"
        ],
        "title_keywords": [
            "software developer",
            "software engineer",
            "frontend developer",
            "backend developer",
            "full stack developer",
            "web developer",
            "devops engineer"
        ]
    },

    "Data and Artificial Intelligence": {
        "keywords": [
            "data analyst",
            "data scientist",
            "machine learning",
            "artificial intelligence",
            "deep learning",
            "data analytics",
            "data analysis",
            "business intelligence",
            "power bi",
            "tableau",
            "pandas",
            "numpy",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "statistics",
            "data visualization",
            "eda",
            "predictive modeling",
            "natural language processing",
            "computer vision"
        ],
        "title_keywords": [
            "data analyst",
            "data scientist",
            "machine learning engineer",
            "ai engineer",
            "business intelligence analyst"
        ]
    },

    "Finance and Accounting": {
        "keywords": [
            "finance",
            "accounting",
            "accounts payable",
            "accounts receivable",
            "financial analysis",
            "financial reporting",
            "bookkeeping",
            "audit",
            "auditing",
            "taxation",
            "gst",
            "tds",
            "balance sheet",
            "profit and loss",
            "cash flow",
            "budgeting",
            "forecasting",
            "reconciliation",
            "ledger",
            "invoice processing",
            "tally",
            "sap fico",
            "investment analysis"
        ],
        "title_keywords": [
            "accountant",
            "financial analyst",
            "finance executive",
            "audit associate",
            "accounts executive"
        ]
    },

    "Marketing": {
        "keywords": [
            "marketing",
            "digital marketing",
            "social media marketing",
            "content marketing",
            "seo",
            "sem",
            "google ads",
            "facebook ads",
            "campaign management",
            "brand management",
            "market research",
            "email marketing",
            "content creation",
            "copywriting",
            "analytics",
            "lead generation",
            "customer engagement"
        ],
        "title_keywords": [
            "marketing executive",
            "digital marketing executive",
            "marketing manager",
            "seo specialist",
            "content marketer"
        ]
    },

    "Sales and Business Development": {
        "keywords": [
            "sales",
            "business development",
            "lead generation",
            "client acquisition",
            "customer acquisition",
            "sales target",
            "revenue generation",
            "negotiation",
            "crm",
            "cold calling",
            "sales pipeline",
            "account management",
            "client relationship",
            "market expansion",
            "product demonstration"
        ],
        "title_keywords": [
            "sales executive",
            "business development executive",
            "account manager",
            "sales manager",
            "relationship manager"
        ]
    },

    "Operations and Supply Chain": {
        "keywords": [
            "operations",
            "business operations",
            "supply chain",
            "logistics",
            "inventory management",
            "procurement",
            "vendor management",
            "warehouse management",
            "process improvement",
            "quality management",
            "production planning",
            "resource planning",
            "dispatch",
            "order processing",
            "coordination",
            "operational efficiency"
        ],
        "title_keywords": [
            "operations executive",
            "operations manager",
            "supply chain executive",
            "logistics executive",
            "procurement executive"
        ]
    },

    "Customer Service": {
        "keywords": [
            "customer service",
            "customer support",
            "client support",
            "customer queries",
            "complaint resolution",
            "call handling",
            "ticket management",
            "service desk",
            "customer satisfaction",
            "relationship management",
            "technical support",
            "chat support",
            "email support"
        ],
        "title_keywords": [
            "customer service executive",
            "customer support executive",
            "support associate",
            "service desk executive"
        ]
    },

    "Education and Training": {
        "keywords": [
            "teaching",
            "teacher",
            "lecturer",
            "trainer",
            "training",
            "curriculum",
            "lesson planning",
            "student assessment",
            "classroom management",
            "education",
            "academic",
            "instruction",
            "mentoring",
            "faculty",
            "learning and development"
        ],
        "title_keywords": [
            "teacher",
            "trainer",
            "lecturer",
            "faculty",
            "academic coordinator"
        ]
    },

    "Design and Creative": {
        "keywords": [
            "graphic design",
            "ui design",
            "ux design",
            "user experience",
            "user interface",
            "figma",
            "adobe photoshop",
            "illustrator",
            "canva",
            "visual design",
            "branding",
            "wireframing",
            "prototyping",
            "video editing",
            "animation"
        ],
        "title_keywords": [
            "graphic designer",
            "ui designer",
            "ux designer",
            "ui ux designer",
            "visual designer"
        ]
    }
}


def normalize_text(value: str) -> str:
    if not value:
        return ""

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9+#.\-/\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def keyword_exists(
    resume_text: str,
    keyword: str
) -> bool:
    normalized_text = normalize_text(
        resume_text
    )

    normalized_keyword = normalize_text(
        keyword
    )

    if not normalized_keyword:
        return False

    pattern = (
        rf"(?<![a-z0-9])"
        rf"{re.escape(normalized_keyword)}"
        rf"(?![a-z0-9])"
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE
        )
    )


def calculate_domain_score(
    resume_text: str,
    domain_profile: dict[str, Any]
) -> dict[str, Any]:
    matched_keywords = []

    score = 0

    for keyword in domain_profile.get(
        "keywords",
        []
    ):
        if keyword_exists(
            resume_text,
            keyword
        ):
            matched_keywords.append(
                keyword
            )

            score += 2

    for title_keyword in domain_profile.get(
        "title_keywords",
        []
    ):
        if keyword_exists(
            resume_text,
            title_keyword
        ):
            if (
                title_keyword
                not in matched_keywords
            ):
                matched_keywords.append(
                    title_keyword
                )

            # Job titles are stronger domain evidence.
            score += 8

    return {
        "score": score,
        "matched_keywords": matched_keywords
    }


def detect_resume_domain(
    resume_text: str
) -> dict[str, Any]:
    """
    Identify the most suitable professional domain
    from the complete resume text.
    """

    if not resume_text or not resume_text.strip():
        return {
            "detected_domain": "General",
            "confidence": 0,
            "matched_keywords": [],
            "domain_scores": []
        }

    domain_results = []

    for domain_name, domain_profile in (
        DOMAIN_KEYWORDS.items()
    ):
        result = calculate_domain_score(
            resume_text,
            domain_profile
        )

        domain_results.append({
            "domain": domain_name,
            "score": result["score"],
            "matched_keywords":
                result["matched_keywords"]
        })

    domain_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    best_result = (
        domain_results[0]
        if domain_results
        else {
            "domain": "General",
            "score": 0,
            "matched_keywords": []
        }
    )

    total_positive_score = sum(
        item["score"]
        for item in domain_results
        if item["score"] > 0
    )

    if best_result["score"] == 0:
        confidence = 0
        detected_domain = "General"

    elif total_positive_score == 0:
        confidence = 0
        detected_domain = (
            best_result["domain"]
        )

    else:
        confidence = round(
            best_result["score"]
            / total_positive_score
            * 100
        )

        # A clear title or many domain terms should
        # receive a stronger minimum confidence.
        if best_result["score"] >= 20:
            confidence = max(
                confidence,
                80
            )

        elif best_result["score"] >= 10:
            confidence = max(
                confidence,
                65
            )

        confidence = min(
            confidence,
            100
        )

        detected_domain = (
            best_result["domain"]
        )

    return {
        "detected_domain":
            detected_domain,

        "confidence":
            confidence,

        "matched_keywords":
            best_result[
                "matched_keywords"
            ],

        "domain_scores": [
            {
                "domain":
                    item["domain"],

                "score":
                    item["score"]
            }
            for item in domain_results
        ]
    }