import json
import os
import shutil
import re

from io import BytesIO
from pathlib import Path
from uuid import uuid4
from app.resume_rewriter import (
    rewrite_resume_for_career
)
from app.pdf_export import (
    generate_rewritten_resume_pdf
)                                                                                                   
from io import BytesIO
from app.resume_export import (
    generate_rewritten_resume_docx
)
from app.market_trend_service import (
    apply_live_market_trends
)

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status
)
from app.course_recommender import (
    recommend_courses_for_skills
)
from app.job_description_analyzer import (
    analyze_resume_against_job
)
from app.resume_improvement import (
    build_resume_improvements
)
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.ats_analyzer import calculate_ats_score
from app.auth import( create_access_token,
                      get_current_user
)
from app.career_predictor import predict_careers
from app.database import get_db
from app.job_recommender import (
    recommend_jobs_with_live_market
)
from app.learning_recommender import generate_learning_roadmap
from app.models import Resume, User
from app.report_generator import generate_resume_report
from app.resume_parser import extract_resume_text
from app.skill_extractor import extract_skills
from app.skill_gap_analyzer import analyze_skill_gap
from app.utils import( hash_password, 
                       verify_password
)
from app.schemas import (
    ATSAnalysisResponse,
    CareerPredictionResponse,
    JobRecommendationResponse,
    JobDescriptionAnalysisResponse,
    ResumeRewriteRequest,
ResumeRewriteResponse,
    ResumeImprovementResponse,
    JobDescriptionAnalysisRequest,
    ResumeImprovementCareerRequest,
    LearningRoadmapResponse,
    PasswordChangeRequest,
    ResumeAnalysisResponse,
    ResumeResponse,
    SkillExtractionResponse,
    SkillGapAnalysisResponse,
    Token,
    UserCreate,
    UserLogin,
    UserProfileResponse,
    UserProfileUpdate,
    UserResponse
)


router = APIRouter()


# ==========================================
# FILE UPLOAD CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}

MAX_FILE_SIZE = 5 * 1024 * 1024


# ==========================================
# REGISTER API
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==========================================
# LOGIN API
# ==========================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==========================================
# CURRENT USER API
# ==========================================

@router.get(
    "/users/me",
    response_model=UserResponse
)
def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):
    return current_user


# ==========================================
# RESUME UPLOAD API
# ==========================================

@router.post(
    "/resume/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select a resume file"
        )

    original_filename = Path(file.filename).name

    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOC and DOCX files are allowed"
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5 MB"
        )

    unique_filename = (
        f"user_{current_user.id}_{uuid4().hex}{file_extension}"
    )

    saved_file_path = UPLOAD_DIR / unique_filename

    try:
        with open(saved_file_path, "wb") as destination:
            destination.write(file_content)

    except OSError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save resume file"
        )

    new_resume = Resume(
        user_id=current_user.id,
        file_name=original_filename,
        file_path=str(saved_file_path)
    )

    try:
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

    except Exception:
        db.rollback()

        if saved_file_path.exists():
            os.remove(saved_file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save resume information"
        )

    return new_resume


# ==========================================
# GET USER RESUMES
# ==========================================

@router.get(
    "/resume/my-resumes",
    response_model=list[ResumeResponse]
)
def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(
        Resume.uploaded_at.desc()
    ).all()

    return resumes

    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.uploaded_at.desc())
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume analysis found."
        )

    def load_json(value, default):
        if not value:
            return default

        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "ats_score": resume.ats_score,
        "ats_rating": resume.ats_rating,
        "best_career": resume.best_career,
        "career_readiness": resume.career_readiness,
        "readiness_level": resume.readiness_level,
        "best_job": resume.best_job,
        "career_predictions": load_json(
            resume.career_predictions,
            []
        ),
        "skill_gap_analysis": load_json(
            resume.skill_gap_analysis,
            {}
        ),
        "job_recommendations": load_json(
            resume.job_recommendations,
            {}
        )
    }
@router.post(
    "/resume/{resume_id}/parse",
    response_model=ResumeAnalysisResponse
)
def parse_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    try:
        extracted_text = extract_resume_text(
            resume.file_path
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception as error:
        print("Resume parsing error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to extract text from resume"
        )

    if not extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No readable text was found in the resume"
        )

    resume.extracted_text = extracted_text

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "extracted_text": extracted_text,
        "character_count": len(extracted_text),
        "word_count": len(extracted_text.split())
    }

# ==========================================
# SKILL EXTRACTION API
# ==========================================

@router.post(
    "/resume/{resume_id}/extract-skills",
    response_model=SkillExtractionResponse
)
def extract_resume_skills(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text has not been extracted yet"
        )

    detected_skills = extract_skills(
        resume.extracted_text
    )

    resume.extracted_skills = json.dumps(
        detected_skills
    )

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "skills": detected_skills,
        "total_skills": len(detected_skills)
    }

# ==========================================
# ATS ANALYSIS API
# ==========================================

@router.post(
    "/resume/{resume_id}/ats-analysis",
    response_model=ATSAnalysisResponse
)
def analyze_resume_ats(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text has not been extracted yet"
        )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills or "[]"
        )
    except json.JSONDecodeError:
        extracted_skills = []

    ats_result = calculate_ats_score(
        resume.extracted_text,
        extracted_skills
    )

    resume.ats_score = ats_result["score"]
    resume.ats_rating = ats_result["rating"]
    resume.ats_analysis = json.dumps(
        ats_result
    )

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "ats_score": ats_result["score"],
        "rating": ats_result["rating"],
        "strengths": ats_result["strengths"],
        "missing_sections": ats_result["missing_sections"],
        "suggestions": ats_result["suggestions"],
        "checks": ats_result["checks"]
    }

# ==========================================
# CAREER PREDICTION API
# ==========================================

@router.post(
    "/resume/{resume_id}/predict-career",
    response_model=CareerPredictionResponse
)
async def predict_resume_career(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    if not resume.extracted_skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Skills have not been extracted from "
                "this resume yet"
            )
        )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stored resume skills are invalid"
        )

    base_predictions = predict_careers(
    extracted_skills=
        extracted_skills,

    limit=5,

    resume_text=
        resume.extracted_text
        or ""
    )

    predictions = await apply_live_market_trends(
    career_predictions=
        base_predictions,

    extracted_skills=
        extracted_skills,

    location=
        "India",

    limit=
        5
    )


    best_career = (
    predictions[0]["career"]
    if predictions
    else None
    )

    resume.best_career = best_career
    resume.career_predictions = json.dumps(
        predictions
    )

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "best_career": best_career,
        "predictions": predictions
    }

# ==========================================
# SKILL GAP ANALYSIS API
# ==========================================

@router.post(
    "/resume/{resume_id}/skill-gap-analysis",
    response_model=SkillGapAnalysisResponse
)
def create_skill_gap_analysis(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    if not resume.extracted_skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Skills have not been extracted from "
                "this resume yet"
            )
        )

    if not resume.best_career:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Career prediction has not been "
                "completed yet"
            )
        )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stored resume skills are invalid"
        )

    try:
        result = analyze_skill_gap(
            extracted_skills=extracted_skills,
            target_career=resume.best_career
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    resume.career_readiness = result[
        "readiness_score"
    ]

    resume.readiness_level = result[
        "readiness_level"
    ]

    resume.skill_gap_analysis = json.dumps(
        result
    )

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        **result
    }

# ==========================================
# LEARNING ROADMAP API
# ==========================================

@router.post(
    "/resume/{resume_id}/learning-roadmap",
    response_model=LearningRoadmapResponse
)
def create_learning_roadmap(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    if not resume.best_career:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Career prediction has not been "
                "completed yet"
            )
        )

    if not resume.skill_gap_analysis:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Skill gap analysis has not been "
                "completed yet"
            )
        )

    try:
        skill_gap_data = json.loads(
            resume.skill_gap_analysis
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stored skill gap analysis is invalid"
        )

    missing_skills = skill_gap_data.get(
        "missing_skills",
        []
    )

    priority_skills = skill_gap_data.get(
        "priority_skills",
        []
    )

    roadmap_result = generate_learning_roadmap(
        missing_skills=missing_skills,
        priority_skills=priority_skills,
        target_career=resume.best_career
    )

    resume.learning_recommendations = json.dumps(
        roadmap_result
    )

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        **roadmap_result
    }

# ==========================================
# JOB RECOMMENDATION API
# ==========================================

@router.post(
    "/resume/{resume_id}/job-recommendations",
    response_model=JobRecommendationResponse
)
async def create_job_recommendations(
    resume_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,

            detail="Resume not found"
        )

    if not resume.extracted_skills:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,

            detail=(
                "Resume skills have not been "
                "extracted yet"
            )
        )

    if not resume.career_predictions:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,

            detail=(
                "Career prediction has not been "
                "completed yet"
            )
        )

    if resume.career_readiness is None:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,

            detail=(
                "Skill gap analysis has not been "
                "completed yet"
            )
        )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
        )

        career_predictions = json.loads(
            resume.career_predictions
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        raise HTTPException(
            status_code=
                status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=(
                "Stored resume analysis data "
                "is invalid"
            )
        )

    result = (
        await recommend_jobs_with_live_market(
            extracted_skills=
                extracted_skills,

            predicted_careers=
                career_predictions,

            readiness_score=
                resume.career_readiness,

            limit=6,

            location="India"
        )
    )

    resume.best_job = result[
        "best_job"
    ]

    resume.job_recommendations = (
        json.dumps(result)
    )

    db.commit()
    db.refresh(resume)

    return {
        "resume_id":
            resume.id,

        "file_name":
            resume.file_name,

        **result
    }

# ==========================================
# PDF REPORT DOWNLOAD API
# ==========================================

@router.get(
    "/resume/{resume_id}/download-report",
    response_class=StreamingResponse
)
def download_resume_report(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    required_fields = {
        "extracted_skills": resume.extracted_skills,
        "ats_analysis": resume.ats_analysis,
        "career_predictions": resume.career_predictions,
        "skill_gap_analysis": resume.skill_gap_analysis,
        "learning_recommendations":
            resume.learning_recommendations,
        "job_recommendations":
            resume.job_recommendations
    }

    missing_fields = [
        field_name
        for field_name, value in required_fields.items()
        if not value
    ]

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Complete resume analysis before generating "
                "the PDF report. Missing: "
                + ", ".join(missing_fields)
            )
        )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
        )

        ats_analysis = json.loads(
            resume.ats_analysis
        )

        career_predictions = json.loads(
            resume.career_predictions
        )

        skill_gap_analysis = json.loads(
            resume.skill_gap_analysis
        )

        learning_recommendations = json.loads(
            resume.learning_recommendations
        )

        job_recommendations = json.loads(
            resume.job_recommendations
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Stored resume analysis data is invalid. "
                "Please analyze the resume again."
            )
        )

    try:
        pdf_buffer = generate_resume_report(
            resume=resume,
            user=current_user,
            extracted_skills=extracted_skills,
            ats_analysis=ats_analysis,
            career_predictions=career_predictions,
            skill_gap_analysis=skill_gap_analysis,
            learning_recommendations=
                learning_recommendations,
            job_recommendations=
                job_recommendations
        )
    except Exception as error:
        print("PDF generation error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate the PDF report"
        )

    original_name = resume.file_name.rsplit(
        ".",
        1
    )[0]

    safe_file_name = "".join(
        character
        if character.isalnum()
        or character in ("-", "_")
        else "_"
        for character in original_name
    )

    report_file_name = (
        f"{safe_file_name}_CareerCompass_Report.pdf"
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{report_file_name}"'
            )
        }
    )

# ==========================================
# GET USER RESUME HISTORY
# ==========================================

@router.get(
    "/resumes/history",
    response_model=list[ResumeResponse]
)
def get_resume_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.id.desc())
        .all()
    )

    return resumes

# ==========================================
# DASHBOARD STATISTICS
# ==========================================

@router.get("/dashboard/statistics")
def get_dashboard_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.id.desc())
        .all()
    )

    total_resumes = len(resumes)

    ats_scores = [
        resume.ats_score
        for resume in resumes
        if resume.ats_score is not None
    ]

    readiness_scores = [
        resume.career_readiness
        for resume in resumes
        if resume.career_readiness is not None
    ]

    average_ats_score = (
        round(sum(ats_scores) / len(ats_scores))
        if ats_scores
        else 0
    )

    average_readiness = (
        round(
            sum(readiness_scores)
            / len(readiness_scores)
        )
        if readiness_scores
        else 0
    )

    best_ats_score = (
        max(ats_scores)
        if ats_scores
        else 0
    )

    career_counts = {}

    for resume in resumes:
        if resume.best_career:
            career_counts[resume.best_career] = (
                career_counts.get(
                    resume.best_career,
                    0
                ) + 1
            )

    most_recommended_career = None

    if career_counts:
        most_recommended_career = max(
            career_counts,
            key=career_counts.get
        )

    latest_resume = resumes[0] if resumes else None

    return {
        "total_resumes": total_resumes,
        "average_ats_score": average_ats_score,
        "best_ats_score": best_ats_score,
        "average_readiness": average_readiness,
        "most_recommended_career":
            most_recommended_career,
        "latest_resume": {
            "id": latest_resume.id,
            "file_name": latest_resume.file_name,
            "ats_score": latest_resume.ats_score,
            "best_career": latest_resume.best_career,
            "best_job": latest_resume.best_job
        } if latest_resume else None
    }

@router.get("/resume/latest-analysis")
def get_latest_resume_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume analysis found."
        )

    def load_json(value, default):
        if not value:
            return default

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "ats_score": resume.ats_score,
        "ats_rating": resume.ats_rating,
        "best_career": resume.best_career,
        "career_readiness": resume.career_readiness,
        "readiness_level": resume.readiness_level,
        "best_job": resume.best_job,
        "career_predictions": load_json(
            resume.career_predictions,
            []
        ),
        "skill_gap_analysis": load_json(
            resume.skill_gap_analysis,
            {}
        ),
        "job_recommendations": load_json(
            resume.job_recommendations,
            {}
        )
    }

# ==========================================
# DELETE RESUME
# ==========================================

@router.delete("/resume/{resume_id}")
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    file_path = getattr(
        resume,
        "file_path",
        None
    )

    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass

    db.delete(resume)
    db.commit()

    return {
        "message": "Resume deleted successfully",
        "resume_id": resume_id
    }

# ==========================================
# GET CURRENT USER PROFILE
# ==========================================

@router.get(
    "/profile",
    response_model=UserProfileResponse
)
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# ==========================================
# UPDATE CURRENT USER PROFILE
# ==========================================

@router.put(
    "/profile",
    response_model=UserProfileResponse
)
def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clean_name = profile_data.full_name.strip()

    if len(clean_name) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Full name must contain at least "
                "2 characters."
            )
        )

    current_user.full_name = clean_name

    db.commit()
    db.refresh(current_user)

    return current_user


# ==========================================
# CHANGE USER PASSWORD
# ==========================================

@router.put("/profile/change-password")
def change_user_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(
        password_data.current_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect."
        )

    if (
        password_data.new_password
        != password_data.confirm_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "New password and confirm password "
                "do not match."
            )
        )

    if (
        password_data.current_password
        == password_data.new_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "New password must be different "
                "from the current password."
            )
        )

    current_user.password = hash_password(
        password_data.new_password
    )

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Password changed successfully."
    }

# ==========================================
# RESUME VS JOB DESCRIPTION ANALYZER
# ==========================================

@router.post(
    "/resume/job-description-analysis",
    response_model=
        JobDescriptionAnalysisResponse
)
def analyze_job_description(
    request_data:
        JobDescriptionAnalysisRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,
            detail=(
                "No uploaded resume was found."
            )
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The latest resume has not been "
                "parsed yet. Analyze the resume "
                "before comparing it with a job "
                "description."
            )
        )

    try:
        resume_skills = json.loads(
            resume.extracted_skills
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        resume_skills = []

    if not resume_skills:
        resume_skills = extract_skills(
            resume.extracted_text
        )

    try:
        analysis = (
            analyze_resume_against_job(
                resume_text=
                    resume.extracted_text,

                resume_skills=
                    resume_skills,

                job_description=
                    request_data.job_description,

                job_title=
                    request_data.job_title
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        **analysis
    }

@router.get(
    "/resume/latest-learning-resources"
)
async def get_latest_learning_resources(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "No analyzed resume was found."
            )
        )

    missing_skills = []

    if resume.skill_gap_analysis:
        try:
            skill_gap = json.loads(
                resume.skill_gap_analysis
            )

            missing_skills = (
                skill_gap.get(
                    "priority_skills"
                )
                or skill_gap.get(
                    "missing_skills"
                )
                or []
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):
            missing_skills = []

    if not missing_skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "No missing skills were found "
                "for the latest resume."
            )
        )

    recommendations = (
        await recommend_courses_for_skills(
            missing_skills
        )
    )

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "target_career": (
            resume.best_career
        ),
        "skills_count": len(
            recommendations
        ),
        "recommendations": recommendations
    }

# ==========================================
# AI RESUME IMPROVEMENT SUGGESTIONS
# ==========================================

@router.get(
    "/resume/latest-improvement-suggestions",
    response_model=ResumeImprovementResponse
)
def get_resume_improvement_suggestions(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,
            detail=(
                "No uploaded resume was found."
            )
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The latest resume has not been "
                "parsed yet."
            )
        )

    # ------------------------------------------
    # Load extracted resume skills
    # ------------------------------------------

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        extracted_skills = []

    if not isinstance(
        extracted_skills,
        list
    ):
        extracted_skills = []

    if not extracted_skills:
        extracted_skills = extract_skills(
            resume.extracted_text
        )

    # ------------------------------------------
    # Load ATS analysis
    # ------------------------------------------

    try:
        ats_analysis = json.loads(
            resume.ats_analysis
            or "{}"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        ats_analysis = {}

    if not isinstance(
        ats_analysis,
        dict
    ):
        ats_analysis = {}

    if not ats_analysis:
        ats_analysis = calculate_ats_score(
            resume.extracted_text,
            extracted_skills
        )

    # ------------------------------------------
    # Load skill-gap analysis
    # ------------------------------------------

    try:
        skill_gap_analysis = json.loads(
            resume.skill_gap_analysis
            or "{}"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        skill_gap_analysis = {}

    if not isinstance(
        skill_gap_analysis,
        dict
    ):
        skill_gap_analysis = {}

    # ------------------------------------------
    # Load top five predicted careers
    # ------------------------------------------

    try:
        career_predictions = json.loads(
            resume.career_predictions
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        career_predictions = []

    if not isinstance(
        career_predictions,
        list
    ):
        career_predictions = []

    recommended_careers = []
    seen_careers = set()

    for prediction in career_predictions:
        if not isinstance(
            prediction,
            dict
        ):
            continue

        career_name = str(
            prediction.get(
                "career",
                ""
            )
        ).strip()

        if not career_name:
            continue

        normalized_career = (
            career_name.lower()
        )

        if normalized_career in seen_careers:
            continue

        try:
            match_percentage = int(
                prediction.get(
                    "match_percentage",
                    0
                )
                or 0
            )

        except (
            TypeError,
            ValueError
        ):
            match_percentage = 0

        match_percentage = min(
            max(
                match_percentage,
                0
            ),
            100
        )

        recommended_careers.append({
            "career":
                career_name,

            "match_percentage":
                match_percentage,

            "description": str(
                prediction.get(
                    "description",
                    ""
                )
                or ""
            ).strip()
        })

        seen_careers.add(
            normalized_career
        )

    recommended_careers.sort(
        key=lambda item:
            item["match_percentage"],
        reverse=True
    )

    recommended_careers = (
        recommended_careers[:5]
    )

    # Fallback when stored predictions are missing.
    if (
        not recommended_careers
        and resume.best_career
    ):
        recommended_careers.append({
            "career":
                resume.best_career,

            "match_percentage":
                0,

            "description":
                "The most suitable career based "
                "on your latest resume analysis."
        })

    # ------------------------------------------
    # Generate improvement suggestions
    # ------------------------------------------

    try:
        result = build_resume_improvements(
            resume_text=
                resume.extracted_text,

            extracted_skills=
                extracted_skills,

            ats_analysis=
                ats_analysis,

            target_career=
                resume.best_career,

            skill_gap_analysis=
                skill_gap_analysis
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    # ------------------------------------------
    # Final API response
    # ------------------------------------------

    return {
        "resume_id":
            resume.id,

        "file_name":
            resume.file_name,

        "recommended_careers":
            recommended_careers,

        **result
    }
# ==========================================
# RESUME IMPROVEMENT BY SELECTED CAREER
# ==========================================

@router.post(
    "/resume/improvement-by-career",
    response_model=ResumeImprovementResponse
)
def get_resume_improvement_by_career(
    request_data:
        ResumeImprovementCareerRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,
            detail=(
                "No uploaded resume was found."
            )
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The latest resume has not been "
                "parsed yet."
            )
        )

    target_career = (
        request_data.target_career
        .strip()
    )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        extracted_skills = []

    if not isinstance(
        extracted_skills,
        list
    ):
        extracted_skills = []

    if not extracted_skills:
        extracted_skills = extract_skills(
            resume.extracted_text
        )

    try:
        ats_analysis = json.loads(
            resume.ats_analysis
            or "{}"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        ats_analysis = {}

    if not isinstance(
        ats_analysis,
        dict
    ):
        ats_analysis = {}

    if not ats_analysis:
        ats_analysis = calculate_ats_score(
            resume.extracted_text,
            extracted_skills
        )

    try:
        career_predictions = json.loads(
            resume.career_predictions
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        career_predictions = []

    if not isinstance(
        career_predictions,
        list
    ):
        career_predictions = []

    available_careers = []

    recommended_careers = []

    for prediction in career_predictions:
        if not isinstance(
            prediction,
            dict
        ):
            continue

        career_name = str(
            prediction.get(
                "career",
                ""
            )
        ).strip()

        if not career_name:
            continue

        available_careers.append(
            career_name.lower()
        )

        try:
            match_percentage = int(
                prediction.get(
                    "match_percentage",
                    0
                )
                or 0
            )

        except (
            TypeError,
            ValueError
        ):
            match_percentage = 0

        recommended_careers.append({
            "career":
                career_name,

            "match_percentage":
                min(
                    max(
                        match_percentage,
                        0
                    ),
                    100
                ),

            "description": str(
                prediction.get(
                    "description",
                    ""
                )
                or ""
            ).strip()
        })

    if (
        available_careers
        and target_career.lower()
        not in available_careers
    ):
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The selected career is not part "
                "of the predicted career list."
            )
        )

    recommended_careers.sort(
        key=lambda item:
            item["match_percentage"],
        reverse=True
    )

    recommended_careers = (
        recommended_careers[:5]
    )

    try:
        selected_skill_gap = (
            analyze_skill_gap(
                extracted_skills=
                    extracted_skills,

                target_career=
                    target_career
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    try:
        result = build_resume_improvements(
            resume_text=
                resume.extracted_text,

            extracted_skills=
                extracted_skills,

            ats_analysis=
                ats_analysis,

            target_career=
                target_career,

            skill_gap_analysis=
                selected_skill_gap
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    return {
        "resume_id":
            resume.id,

        "file_name":
            resume.file_name,

        "recommended_careers":
            recommended_careers,

        **result
    }

# ==========================================
# RESUME REWRITE BY SELECTED CAREER
# ==========================================

@router.post(
    "/resume/rewrite-by-career",
    response_model=ResumeRewriteResponse
)
def rewrite_latest_resume_by_career(
    request_data: ResumeRewriteRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,
            detail=(
                "No uploaded resume was found."
            )
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The latest resume has not been "
                "parsed yet."
            )
        )

    target_career = (
        request_data.target_career
        .strip()
    )

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        extracted_skills = []

    if not isinstance(
        extracted_skills,
        list
    ):
        extracted_skills = []

    if not extracted_skills:
        extracted_skills = extract_skills(
            resume.extracted_text
        )

    try:
        skill_gap_analysis = json.loads(
            resume.skill_gap_analysis
            or "{}"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        skill_gap_analysis = {}

    if not isinstance(
        skill_gap_analysis,
        dict
    ):
        skill_gap_analysis = {}

    stored_target_career = str(
        skill_gap_analysis.get(
            "target_career",
            ""
        )
        or ""
    ).strip()

    if (
        stored_target_career.lower()
        == target_career.lower()
    ):
        priority_skills = (
            skill_gap_analysis.get(
                "priority_skills"
            )
            or []
        )

    else:
        try:
            selected_skill_gap = (
                analyze_skill_gap(
                    extracted_skills=
                        extracted_skills,

                    target_career=
                        target_career
                )
            )

        except ValueError as error:
            raise HTTPException(
                status_code=
                    status.HTTP_400_BAD_REQUEST,
                detail=str(error)
            )

        priority_skills = (
            selected_skill_gap.get(
                "priority_skills"
            )
            or []
        )

    if not isinstance(
        priority_skills,
        list
    ):
        priority_skills = []

    try:
        result = rewrite_resume_for_career(
            resume_text=
                resume.extracted_text,

            extracted_skills=
                extracted_skills,

            target_career=
                target_career,

            priority_skills=
                priority_skills
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    return {
        "resume_id":
            resume.id,

        "file_name":
            resume.file_name,

        **result
    }

# ==========================================
# DOWNLOAD REWRITTEN RESUME AS DOCX
# ==========================================

@router.post(
    "/resume/download-rewritten-docx"
)
def download_rewritten_resume_docx(
    request_data: ResumeRewriteRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,
            detail=(
                "No uploaded resume was found."
            )
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The latest resume has not been "
                "parsed yet."
            )
        )

    target_career = (
        request_data.target_career
        .strip()
    )

    # ------------------------------------------
    # Load extracted skills
    # ------------------------------------------

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        extracted_skills = []

    if not isinstance(
        extracted_skills,
        list
    ):
        extracted_skills = []

    if not extracted_skills:
        extracted_skills = extract_skills(
            resume.extracted_text
        )

    # ------------------------------------------
    # Generate skill gap for selected career
    # ------------------------------------------

    try:
        selected_skill_gap = (
            analyze_skill_gap(
                extracted_skills=
                    extracted_skills,

                target_career=
                    target_career
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    priority_skills = (
        selected_skill_gap.get(
            "priority_skills"
        )
        or []
    )

    if not isinstance(
        priority_skills,
        list
    ):
        priority_skills = []

    # ------------------------------------------
    # Rewrite resume
    # ------------------------------------------

    try:
        rewrite_result = (
            rewrite_resume_for_career(
                resume_text=
                    resume.extracted_text,

                extracted_skills=
                    extracted_skills,

                target_career=
                    target_career,

                priority_skills=
                    priority_skills
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    rewritten_content = (
        rewrite_result.get(
            "rewritten_content",
            {}
        )
    )

    # ------------------------------------------
    # Extract basic contact information
    # ------------------------------------------

    resume_text = (
        resume.extracted_text
        or ""
    )

    phone_match = re.search(
        r"(\+?\d[\d\s\-()]{8,}\d)",
        resume_text
    )

    phone = (
        phone_match.group(0).strip()
        if phone_match
        else ""
    )

    linkedin_match = re.search(
        r"https?://(?:www\.)?linkedin\.com/[^\s]+",
        resume_text,
        flags=re.IGNORECASE
    )

    linkedin = (
        linkedin_match.group(0).strip()
        if linkedin_match
        else ""
    )

    github_match = re.search(
        r"https?://(?:www\.)?github\.com/[^\s]+",
        resume_text,
        flags=re.IGNORECASE
    )

    github = (
        github_match.group(0).strip()
        if github_match
        else ""
    )

    # ------------------------------------------
    # Generate DOCX bytes
    # ------------------------------------------

    try:
        docx_bytes = (
            generate_rewritten_resume_docx(
                user_name=
                    current_user.full_name,

                user_email=
                    current_user.email,

                file_name=
                    resume.file_name,

                target_career=
                    target_career,

                rewritten_content=
                    rewritten_content,

                phone=
                    phone,

                linkedin=
                    linkedin,

                github=
                    github
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    safe_career_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        target_career
    ).strip("_")

    if not safe_career_name:
        safe_career_name = (
            "Improved_Resume"
        )

    download_name = (
        f"{current_user.full_name}_"
        f"{safe_career_name}_Resume.docx"
    )

    download_name = re.sub(
        r"\s+",
        "_",
        download_name
    )

    return StreamingResponse(
        BytesIO(
            docx_bytes
        ),
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.wordprocessingml.document"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="{download_name}"'
            )
        }
    )

# ==========================================
# DOWNLOAD REWRITTEN RESUME AS PDF
# ==========================================

@router.post(
    "/resume/download-rewritten-pdf"
)
def download_rewritten_resume_pdf(
    request_data: ResumeRewriteRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id
            == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=
                status.HTTP_404_NOT_FOUND,
            detail=(
                "No uploaded resume was found."
            )
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=(
                "The latest resume has not been "
                "parsed yet."
            )
        )

    target_career = (
        request_data.target_career
        .strip()
    )

    # ------------------------------------------
    # Load extracted skills
    # ------------------------------------------

    try:
        extracted_skills = json.loads(
            resume.extracted_skills
            or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):
        extracted_skills = []

    if not isinstance(
        extracted_skills,
        list
    ):
        extracted_skills = []

    if not extracted_skills:
        extracted_skills = extract_skills(
            resume.extracted_text
        )

    # ------------------------------------------
    # Generate skill gap for selected career
    # ------------------------------------------

    try:
        selected_skill_gap = (
            analyze_skill_gap(
                extracted_skills=
                    extracted_skills,

                target_career=
                    target_career
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    priority_skills = (
        selected_skill_gap.get(
            "priority_skills"
        )
        or []
    )

    if not isinstance(
        priority_skills,
        list
    ):
        priority_skills = []

    # ------------------------------------------
    # Rewrite resume
    # ------------------------------------------

    try:
        rewrite_result = (
            rewrite_resume_for_career(
                resume_text=
                    resume.extracted_text,

                extracted_skills=
                    extracted_skills,

                target_career=
                    target_career,

                priority_skills=
                    priority_skills
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    rewritten_content = (
        rewrite_result.get(
            "rewritten_content",
            {}
        )
    )

    # ------------------------------------------
    # Extract contact information
    # ------------------------------------------

    resume_text = (
        resume.extracted_text
        or ""
    )

    phone_match = re.search(
        r"(\+?\d[\d\s\-()]{8,}\d)",
        resume_text
    )

    phone = (
        phone_match.group(0).strip()
        if phone_match
        else ""
    )

    linkedin_match = re.search(
        r"https?://(?:www\.)?linkedin\.com/[^\s]+",
        resume_text,
        flags=re.IGNORECASE
    )

    linkedin = (
        linkedin_match.group(0).strip()
        if linkedin_match
        else ""
    )

    github_match = re.search(
        r"https?://(?:www\.)?github\.com/[^\s]+",
        resume_text,
        flags=re.IGNORECASE
    )

    github = (
        github_match.group(0).strip()
        if github_match
        else ""
    )

    # ------------------------------------------
    # Generate PDF bytes
    # ------------------------------------------

    try:
        pdf_bytes = (
            generate_rewritten_resume_pdf(
                user_name=
                    current_user.full_name,

                user_email=
                    current_user.email,

                file_name=
                    resume.file_name,

                target_career=
                    target_career,

                rewritten_content=
                    rewritten_content,

                phone=
                    phone,

                linkedin=
                    linkedin,

                github=
                    github
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=
                status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    safe_career_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        target_career
    ).strip("_")

    if not safe_career_name:
        safe_career_name = (
            "Improved_Resume"
        )

    download_name = (
        f"{current_user.full_name}_"
        f"{safe_career_name}_Resume.pdf"
    )

    download_name = re.sub(
        r"\s+",
        "_",
        download_name
    )

    return StreamingResponse(
        BytesIO(
            pdf_bytes
        ),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{download_name}"'
            )
        }
    )