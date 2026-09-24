import re


SKILL_KEYWORDS = {
    # =====================================================
    # TECHNOLOGY AND SOFTWARE
    # =====================================================

    "Python": [
        "python"
    ],

    "Java": [
        "java"
    ],

    "C": [
        "c programming",
        "language c"
    ],

    "C++": [
        "c++",
        "cpp"
    ],

    "C#": [
        "c#",
        "c sharp"
    ],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    "TypeScript": [
        "typescript",
        "type script"
    ],

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "React": [
        "react",
        "react.js",
        "reactjs"
    ],

    "Angular": [
        "angular",
        "angular.js",
        "angularjs"
    ],

    "Vue.js": [
        "vue",
        "vue.js",
        "vuejs"
    ],

    "Node.js": [
        "node.js",
        "nodejs"
    ],

    "Express.js": [
        "express.js",
        "expressjs"
    ],

    "FastAPI": [
        "fastapi",
        "fast api"
    ],

    "Flask": [
        "flask"
    ],

    "Django": [
        "django"
    ],

    "Tailwind CSS": [
        "tailwind",
        "tailwind css"
    ],

    "Bootstrap": [
        "bootstrap"
    ],

    "SQL": [
        "sql",
        "structured query language"
    ],

    "MySQL": [
        "mysql",
        "my sql"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres",
        "postgre sql"
    ],

    "MongoDB": [
        "mongodb",
        "mongo db"
    ],

    "SQLite": [
        "sqlite",
        "sqlite3"
    ],

    "Redis": [
        "redis"
    ],

    "REST API": [
        "rest api",
        "restful api",
        "restful services"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github",
        "git hub"
    ],

    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "microsoft azure",
        "azure"
    ],

    "Google Cloud": [
        "google cloud",
        "gcp"
    ],

    "Linux": [
        "linux"
    ],

    "Postman": [
        "postman"
    ],

    "CI/CD": [
        "ci/cd",
        "continuous integration",
        "continuous deployment"
    ],

    "Terraform": [
        "terraform"
    ],

    "Jenkins": [
        "jenkins"
    ],

    # =====================================================
    # DATA AND ARTIFICIAL INTELLIGENCE
    # =====================================================

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Matplotlib": [
        "matplotlib"
    ],

    "Scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "TensorFlow": [
        "tensorflow",
        "tensor flow"
    ],

    "PyTorch": [
        "pytorch",
        "py torch"
    ],

    "Machine Learning": [
        "machine learning"
    ],

    "Deep Learning": [
        "deep learning"
    ],

    "Artificial Intelligence": [
        "artificial intelligence"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics",
        "data analyst"
    ],

    "Data Science": [
        "data science",
        "data scientist"
    ],

    "Natural Language Processing": [
        "natural language processing",
        "nlp"
    ],

    "Computer Vision": [
        "computer vision",
        "opencv"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Tableau": [
        "tableau"
    ],

    "Excel": [
        "microsoft excel",
        "ms excel",
        "advanced excel",
        "excel"
    ],

    "Statistics": [
        "statistics",
        "statistical analysis"
    ],

    "Data Visualization": [
        "data visualization",
        "dashboard",
        "dashboards"
    ],

    "EDA": [
        "exploratory data analysis",
        "eda"
    ],

    "Hadoop": [
        "hadoop"
    ],

    "Spark": [
        "apache spark",
        "pyspark"
    ],

    "MapReduce": [
        "mapreduce",
        "map reduce"
    ],

    # =====================================================
    # HUMAN RESOURCES
    # =====================================================

    "HR Operations": [
        "hr operations",
        "human resource operations",
        "human resources operations"
    ],

    "Employee Lifecycle Management": [
        "employee lifecycle management",
        "employee lifecycle"
    ],

    "Payroll Processing": [
        "payroll processing",
        "payroll inputs",
        "staff payroll",
        "employee payroll",
        "payroll"
    ],

    "Attendance Management": [
        "attendance management",
        "attendance tracking",
        "biometric attendance",
        "attendance"
    ],

    "Employee Relations": [
        "employee relations",
        "employee relationship"
    ],

    "Grievance Handling": [
        "grievance handling",
        "employee grievances",
        "grievance resolution",
        "hr queries"
    ],

    "Recruitment": [
        "recruitment",
        "recruiting",
        "candidate recruitment"
    ],

    "Talent Acquisition": [
        "talent acquisition",
        "talent sourcing"
    ],

    "Interviewing": [
        "conducting interviews",
        "interviews",
        "candidate interviews"
    ],

    "Onboarding": [
        "employee onboarding",
        "onboarding"
    ],

    "Offboarding": [
        "employee offboarding",
        "offboarding",
        "exit formalities"
    ],

    "Statutory Compliance": [
        "statutory compliance",
        "labor compliance",
        "labour compliance"
    ],

    "PF Compliance": [
        "pf compliance",
        "pf challan",
        "pf challans",
        "provident fund",
        "pf transfer"
    ],

    "ESIC Compliance": [
        "esic compliance",
        "esic challan",
        "esic challans",
        "employee state insurance"
    ],

    "ECR Filing": [
        "ecr filing",
        "ecr filings",
        "ecr"
    ],

    "POSH Compliance": [
        "posh compliance",
        "posh",
        "she-box",
        "she box"
    ],

    "Workforce Management": [
        "workforce management",
        "workforce operations",
        "contractual employees"
    ],

    "Performance Management": [
        "performance management",
        "performance appraisal",
        "employee appraisal"
    ],

    "Employee Engagement": [
        "employee engagement",
        "staff engagement"
    ],

    "HRMS": [
        "hrms",
        "human resource management system"
    ],

    "HR Reporting": [
        "hr reporting",
        "compliance reports",
        "hr reports"
    ],

    "Labor Law": [
        "labor law",
        "labour law",
        "labor regulations",
        "labour regulations"
    ],

    # =====================================================
    # FINANCE AND ACCOUNTING
    # =====================================================

    "Accounting": [
        "accounting",
        "accounts"
    ],

    "Bookkeeping": [
        "bookkeeping"
    ],

    "Financial Reporting": [
        "financial reporting",
        "financial reports"
    ],

    "Financial Analysis": [
        "financial analysis",
        "financial analyst"
    ],

    "Accounts Payable": [
        "accounts payable",
        "payables"
    ],

    "Accounts Receivable": [
        "accounts receivable",
        "receivables"
    ],

    "Bank Reconciliation": [
        "bank reconciliation",
        "reconciliation"
    ],

    "GST": [
        "gst",
        "goods and services tax"
    ],

    "TDS": [
        "tds",
        "tax deducted at source"
    ],

    "Taxation": [
        "taxation",
        "tax compliance"
    ],

    "Auditing": [
        "audit",
        "auditing"
    ],

    "Budgeting": [
        "budgeting",
        "budget preparation"
    ],

    "Financial Forecasting": [
        "financial forecasting",
        "forecasting"
    ],

    "Tally": [
        "tally",
        "tally erp"
    ],

    "SAP FICO": [
        "sap fico",
        "fico"
    ],

    "Invoice Processing": [
        "invoice processing",
        "invoice management"
    ],

    # =====================================================
    # MARKETING
    # =====================================================

    "Digital Marketing": [
        "digital marketing"
    ],

    "Social Media Marketing": [
        "social media marketing",
        "social media campaigns"
    ],

    "SEO": [
        "seo",
        "search engine optimization"
    ],

    "SEM": [
        "sem",
        "search engine marketing"
    ],

    "Content Marketing": [
        "content marketing"
    ],

    "Email Marketing": [
        "email marketing"
    ],

    "Google Ads": [
        "google ads",
        "google adwords"
    ],

    "Meta Ads": [
        "facebook ads",
        "meta ads",
        "instagram ads"
    ],

    "Campaign Management": [
        "campaign management",
        "marketing campaigns"
    ],

    "Market Research": [
        "market research",
        "market analysis"
    ],

    "Brand Management": [
        "brand management",
        "branding"
    ],

    "Copywriting": [
        "copywriting",
        "content writing"
    ],

    "Lead Generation": [
        "lead generation",
        "lead generation campaigns"
    ],

    # =====================================================
    # SALES AND BUSINESS DEVELOPMENT
    # =====================================================

    "Sales": [
        "sales",
        "sales executive"
    ],

    "Business Development": [
        "business development",
        "business development executive"
    ],

    "Client Acquisition": [
        "client acquisition",
        "customer acquisition"
    ],

    "CRM": [
        "crm",
        "customer relationship management"
    ],

    "Cold Calling": [
        "cold calling",
        "outbound calling"
    ],

    "Negotiation": [
        "negotiation",
        "client negotiation"
    ],

    "Account Management": [
        "account management",
        "key account management"
    ],

    "Sales Pipeline Management": [
        "sales pipeline",
        "pipeline management"
    ],

    "Revenue Generation": [
        "revenue generation",
        "revenue growth"
    ],

    # =====================================================
    # OPERATIONS AND SUPPLY CHAIN
    # =====================================================

    "Operations Management": [
        "operations management",
        "business operations"
    ],

    "Supply Chain Management": [
        "supply chain",
        "supply chain management"
    ],

    "Logistics": [
        "logistics",
        "logistics management"
    ],

    "Inventory Management": [
        "inventory management",
        "stock management"
    ],

    "Procurement": [
        "procurement",
        "purchasing"
    ],

    "Vendor Management": [
        "vendor management",
        "supplier management"
    ],

    "Warehouse Management": [
        "warehouse management",
        "warehouse operations"
    ],

    "Process Improvement": [
        "process improvement",
        "process optimization"
    ],

    "Quality Management": [
        "quality management",
        "quality control"
    ],

    # =====================================================
    # CUSTOMER SERVICE
    # =====================================================

    "Customer Service": [
        "customer service",
        "customer support"
    ],

    "Complaint Resolution": [
        "complaint resolution",
        "customer complaints"
    ],

    "Ticket Management": [
        "ticket management",
        "support tickets"
    ],

    "Call Handling": [
        "call handling",
        "inbound calls",
        "outbound calls"
    ],

    "Customer Satisfaction": [
        "customer satisfaction",
        "customer experience"
    ],

    "Email Support": [
        "email support"
    ],

    "Chat Support": [
        "chat support"
    ],

    # =====================================================
    # EDUCATION AND TRAINING
    # =====================================================

    "Teaching": [
        "teaching",
        "teacher"
    ],

    "Training": [
        "training",
        "trainer"
    ],

    "Curriculum Development": [
        "curriculum development",
        "curriculum design"
    ],

    "Lesson Planning": [
        "lesson planning"
    ],

    "Student Assessment": [
        "student assessment",
        "student evaluation"
    ],

    "Classroom Management": [
        "classroom management"
    ],

    "Mentoring": [
        "mentoring",
        "student mentoring"
    ],

    # =====================================================
    # DESIGN AND CREATIVE
    # =====================================================

    "Graphic Design": [
        "graphic design",
        "graphic designer"
    ],

    "UI Design": [
        "ui design",
        "user interface design"
    ],

    "UX Design": [
        "ux design",
        "user experience design"
    ],

    "Figma": [
        "figma"
    ],

    "Adobe Photoshop": [
        "adobe photoshop",
        "photoshop"
    ],

    "Adobe Illustrator": [
        "adobe illustrator",
        "illustrator"
    ],

    "Canva": [
        "canva"
    ],

    "Wireframing": [
        "wireframing",
        "wireframes"
    ],

    "Prototyping": [
        "prototyping",
        "prototype design"
    ],

    "Video Editing": [
        "video editing"
    ],

    # =====================================================
    # COMMON PROFESSIONAL SKILLS
    # =====================================================

    "Communication": [
        "communication skills",
        "communication"
    ],

    "Interpersonal Skills": [
        "interpersonal skills"
    ],

    "Teamwork": [
        "teamwork",
        "team collaboration"
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ],

    "Leadership": [
        "leadership",
        "team leadership"
    ],

    "Time Management": [
        "time management"
    ],

    "MS Office": [
        "ms office",
        "microsoft office"
    ]
}


def normalize_text(
    value: str
) -> str:
    if not value:
        return ""

    value = value.lower()

    value = value.replace(
        "\u00a0",
        " "
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def contains_skill(
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

    escaped_keyword = re.escape(
        normalized_keyword
    )

    pattern = (
        rf"(?<![a-zA-Z0-9])"
        rf"{escaped_keyword}"
        rf"(?![a-zA-Z0-9])"
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE
        )
    )


def extract_skills(
    resume_text: str
) -> list[str]:
    """
    Extract technical and non-technical skills from
    the complete resume text.
    """

    if not resume_text:
        return []

    detected_skills = []

    for skill_name, keywords in (
        SKILL_KEYWORDS.items()
    ):
        for keyword in keywords:
            if contains_skill(
                resume_text,
                keyword
            ):
                detected_skills.append(
                    skill_name
                )

                break

    return sorted(
        set(detected_skills)
    )