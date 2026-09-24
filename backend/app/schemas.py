from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str
    extracted_text: str | None = None
    extracted_skills: str | None = None
    ats_score: int | None = None
    ats_rating: str | None = None
    ats_analysis: str | None = None
    best_career: str | None = None
    career_predictions: str | None = None
    career_readiness: int | None = None
    readiness_level: str | None = None
    skill_gap_analysis: str | None = None
    learning_recommendations: str | None = None
    best_job: str | None = None
    job_recommendations: str | None = None
    uploaded_at: datetime
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    file_name: str
    extracted_text: str
    character_count: int
    word_count: int


class SkillExtractionResponse(BaseModel):
    resume_id: int
    file_name: str
    skills: list[str]
    total_skills: int


class ATSAnalysisResponse(BaseModel):
    resume_id: int
    file_name: str
    ats_score: int
    rating: str
    strengths: list[str]
    missing_sections: list[str]
    suggestions: list[str]
    checks: dict[str, bool]


class CareerPredictionItem(BaseModel):
    career: str
    description: str
    match_percentage: int
    matched_skills: list[str]
    missing_skills: list[str]
    matched_skill_count: int
    required_skill_count: int
    resume_match_score: int
    market_demand_score: int
    growth_score: int
    trending_skill_score: int
    final_career_score: int

    salary_range: str
    demand_level: str
    trend_status: str

    top_locations: list[str]
    trending_skills: list[str]
    matched_trending_skills: list[str]
    missing_trending_skills: list[str]
    live_job_count: int = 0

    average_salary: float | int | None = None

    top_companies: list[str] = []

    market_data_source: str = "Local fallback"

    live_data_available: bool = False

    market_data_updated_at: str | None = None

class CareerPredictionResponse(BaseModel):
    resume_id: int
    file_name: str
    best_career: str | None
    predictions: list[
        CareerPredictionItem
    ]


class SkillGapAnalysisResponse(BaseModel):
    resume_id: int
    file_name: str
    target_career: str
    career_description: str
    readiness_score: int
    readiness_level: str
    matched_skills: list[str]
    missing_skills: list[str]
    priority_skills: list[str]
    estimated_learning_time: str
    matched_skill_count: int
    missing_skill_count: int
    required_skill_count: int
    summary: str


class LearningResourceItem(BaseModel):
    title: str
    provider: str
    type: str
    url: str


class LearningRoadmapItem(BaseModel):
    order: int
    skill: str
    is_priority: bool
    difficulty: str
    duration: str
    resources: list[
        LearningResourceItem
    ]
    mini_project: str
    certification: str | None = None


class LearningRoadmapResponse(BaseModel):
    resume_id: int
    file_name: str
    target_career: str
    total_recommendations: int
    roadmap: list[
        LearningRoadmapItem
    ]
    message: str


class JobRecommendationItem(
    BaseModel
):
    job_title: str
    career_category: str
    experience_level: str
    description: str

    match_percentage: int
    recommendation_score: int
    application_status: str

    matched_skills: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )

    required_skill_count: int
    matched_skill_count: int

    preparation_advice: str

    resume_match_score: int = 0
    market_demand_score: int = 0
    trending_skill_score: int = 0
    career_score: int = 0
    readiness_score: int = 0

    live_job_count: int = 0

    average_salary: float | int | None = None

    salary_range: str = (
        "Salary data unavailable"
    )

    demand_level: str = (
        "Unavailable"
    )

    top_locations: list[str] = Field(
        default_factory=list
    )

    top_companies: list[str] = Field(
        default_factory=list
    )

    trending_skills: list[str] = Field(
        default_factory=list
    )

    matched_trending_skills: list[str] = Field(
        default_factory=list
    )

    missing_trending_skills: list[str] = Field(
        default_factory=list
    )

    market_data_source: str = (
        "Local calculation"
    )

    live_data_available: bool = False

    market_data_updated_at: str | None = None


class JobRecommendationResponse(BaseModel):
    resume_id: int
    file_name: str
    best_job: str | None
    total_recommendations: int
    recommendations: list[
        JobRecommendationItem
    ]


class UserProfileResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(
        ...,
        min_length=6,
        max_length=72
    )

    new_password: str = Field(
        ...,
        min_length=6,
        max_length=72
    )

    confirm_password: str = Field(
        ...,
        min_length=6,
        max_length=72
    )


class JobDescriptionAnalysisRequest(
    BaseModel
):
    job_title: str | None = Field(
        default=None,
        max_length=150
    )

    job_description: str = Field(
        ...,
        min_length=50,
        max_length=20_000
    )


class JobDescriptionAnalysisResponse(
    BaseModel
):
    resume_id: int
    file_name: str
    job_title: str
    overall_match_score: int
    match_level: str
    application_status: str
    skill_match_percentage: int
    keyword_match_percentage: int
    resume_quality_score: int
    resume_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    important_keywords: list[str]
    matched_keywords: list[str]
    missing_keywords: list[str]
    experience_requirement: str | None
    strengths: list[str]
    suggestions: list[str]
    matched_skill_count: int
    missing_skill_count: int
    required_skill_count: int


class ResumeImprovementSuggestion(
    BaseModel
):
    category: str
    title: str
    description: str
    severity: str
    priority: int
    impact: str
    example: str | None = None


class ResumeImprovementCareerItem(
    BaseModel
):
    career: str
    match_percentage: int
    description: str = ""
class ResumeImprovementCareerRequest(
    BaseModel
):
    target_career: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

class ResumeImprovementResponse(
    BaseModel
):
    resume_id: int
    file_name: str
    current_ats_score: int
    potential_ats_score: int
    target_career: str | None

    recommended_careers: list[
        ResumeImprovementCareerItem
    ]

    summary: str
    total_suggestions: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    missing_sections: list[str]
    priority_skills: list[str]

    suggestions: list[
        ResumeImprovementSuggestion
    ]

class ResumeRewriteRequest(
    BaseModel
):
    target_career: str = Field(
        ...,
        min_length=2,
        max_length=150
    )


class ResumeRewriteOriginalContent(
    BaseModel
):
    summary: str
    experience: list[str]
    projects: list[str]
    skills: list[str]


class ResumeRewriteContent(
    BaseModel
):
    summary: str
    experience: list[str]
    projects: list[str]
    verified_skills: list[str]
    recommended_skills: list[str]

class ResumeQualityAnalysis(
    BaseModel
):
    readability: int
    professional_language: int
    ats_optimization: int
    action_verbs: int
    overall_improvement: int
    original_word_count: int
    rewritten_word_count: int

class ResumeRewriteResponse(
    BaseModel
):
    resume_id: int
    file_name: str
    target_career: str
    original_content:ResumeRewriteOriginalContent
    rewritten_content:ResumeRewriteContent
    quality_analysis:ResumeQualityAnalysis
    rewrite_notes: list[str]
    disclaimer: str

