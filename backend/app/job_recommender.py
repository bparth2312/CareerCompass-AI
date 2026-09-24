from __future__ import annotations

import asyncio
from typing import Any

from app.job_market_client import analyze_live_job_market


CAREER_JOB_VARIANTS: dict[str, list[dict[str, Any]]] = {
    "Data Analyst": [
        {"job_title": "Junior Data Analyst", "experience_level": "Entry Level", "minimum_readiness": 30},
        {"job_title": "Business Intelligence Analyst", "experience_level": "Entry to Intermediate", "minimum_readiness": 45},
    ],
    "Data Scientist": [
        {"job_title": "Junior Data Scientist", "experience_level": "Entry Level", "minimum_readiness": 40},
    ],
    "Machine Learning Engineer": [
        {"job_title": "Machine Learning Intern", "experience_level": "Internship", "minimum_readiness": 30},
        {"job_title": "Junior Machine Learning Engineer", "experience_level": "Entry Level", "minimum_readiness": 50},
    ],
    "Full Stack Developer": [
        {"job_title": "Full Stack Developer Intern", "experience_level": "Internship", "minimum_readiness": 25},
        {"job_title": "Junior Full Stack Developer", "experience_level": "Entry Level", "minimum_readiness": 40},
    ],
    "Frontend Developer": [
        {"job_title": "Frontend Developer Intern", "experience_level": "Internship", "minimum_readiness": 25},
        {"job_title": "Junior Frontend Developer", "experience_level": "Entry Level", "minimum_readiness": 40},
    ],
    "Backend Developer": [
        {"job_title": "Backend Developer Intern", "experience_level": "Internship", "minimum_readiness": 25},
        {"job_title": "Junior Backend Developer", "experience_level": "Entry Level", "minimum_readiness": 40},
    ],
    "DevOps Engineer": [
        {"job_title": "Cloud and DevOps Intern", "experience_level": "Internship", "minimum_readiness": 25},
        {"job_title": "Junior DevOps Engineer", "experience_level": "Entry Level", "minimum_readiness": 45},
    ],
    "Database Developer": [
        {"job_title": "Database Developer Intern", "experience_level": "Internship", "minimum_readiness": 25},
        {"job_title": "Junior Database Developer", "experience_level": "Entry Level", "minimum_readiness": 40},
    ],
    "HR Operations Executive": [
        {"job_title": "HR Operations Executive", "experience_level": "Entry to Intermediate", "minimum_readiness": 35},
        {"job_title": "HR Operations Coordinator", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "HR Generalist": [
        {"job_title": "HR Generalist", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
        {"job_title": "Junior HR Generalist", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "Payroll and Compliance Executive": [
        {"job_title": "Payroll Executive", "experience_level": "Entry to Intermediate", "minimum_readiness": 35},
        {"job_title": "Payroll and Compliance Executive", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "Talent Acquisition Executive": [
        {"job_title": "Talent Acquisition Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
        {"job_title": "Recruitment Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "Employee Relations Executive": [
        {"job_title": "Employee Relations Executive", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "HR Compliance Executive": [
        {"job_title": "HR Compliance Executive", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "Accountant": [
        {"job_title": "Junior Accountant", "experience_level": "Entry Level", "minimum_readiness": 30},
        {"job_title": "Accountant", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "Financial Analyst": [
        {"job_title": "Junior Financial Analyst", "experience_level": "Entry Level", "minimum_readiness": 40},
        {"job_title": "Financial Analyst", "experience_level": "Entry to Intermediate", "minimum_readiness": 50},
    ],
    "Accounts Executive": [
        {"job_title": "Accounts Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "Audit Associate": [
        {"job_title": "Audit Associate", "experience_level": "Entry Level", "minimum_readiness": 35},
    ],
    "Digital Marketing Executive": [
        {"job_title": "Digital Marketing Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "SEO Specialist": [
        {"job_title": "SEO Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
        {"job_title": "SEO Specialist", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "Content Marketing Executive": [
        {"job_title": "Content Marketing Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "Marketing Analyst": [
        {"job_title": "Marketing Analyst", "experience_level": "Entry Level", "minimum_readiness": 40},
    ],
    "Sales Executive": [
        {"job_title": "Sales Executive", "experience_level": "Entry Level", "minimum_readiness": 25},
    ],
    "Business Development Executive": [
        {"job_title": "Business Development Executive", "experience_level": "Entry Level", "minimum_readiness": 25},
    ],
    "Account Manager": [
        {"job_title": "Junior Account Manager", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "Operations Executive": [
        {"job_title": "Operations Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "Supply Chain Executive": [
        {"job_title": "Supply Chain Executive", "experience_level": "Entry Level", "minimum_readiness": 35},
    ],
    "Logistics Executive": [
        {"job_title": "Logistics Executive", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "Procurement Executive": [
        {"job_title": "Procurement Executive", "experience_level": "Entry Level", "minimum_readiness": 35},
    ],
    "Customer Service Executive": [
        {"job_title": "Customer Service Executive", "experience_level": "Entry Level", "minimum_readiness": 20},
    ],
    "Customer Support Associate": [
        {"job_title": "Customer Support Associate", "experience_level": "Entry Level", "minimum_readiness": 20},
    ],
    "Teacher": [
        {"job_title": "Teacher", "experience_level": "Entry to Intermediate", "minimum_readiness": 35},
    ],
    "Corporate Trainer": [
        {"job_title": "Corporate Trainer", "experience_level": "Entry to Intermediate", "minimum_readiness": 40},
    ],
    "Graphic Designer": [
        {"job_title": "Junior Graphic Designer", "experience_level": "Entry Level", "minimum_readiness": 30},
    ],
    "UI Designer": [
        {"job_title": "Junior UI Designer", "experience_level": "Entry Level", "minimum_readiness": 35},
    ],
    "UX Designer": [
        {"job_title": "Junior UX Designer", "experience_level": "Entry Level", "minimum_readiness": 35},
    ],
}


def normalize_skill(skill: str) -> str:
    return " ".join(str(skill or "").strip().lower().split())


def normalize_live_skill_items(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    output: list[str] = []
    for item in items:
        value = str(item.get("skill", "") if isinstance(item, dict) else item).strip()
        if value and value not in output:
            output.append(value)
    return output


def normalize_named_items(items: Any, key: str) -> list[str]:
    if not isinstance(items, list):
        return []
    output: list[str] = []
    for item in items:
        value = str(item.get(key, "") if isinstance(item, dict) else item).strip()
        if value and value not in output:
            output.append(value)
    return output


def format_indian_salary(value: Any) -> str:
    try:
        salary = float(value)
    except (TypeError, ValueError):
        return "Salary data unavailable"
    if salary <= 0:
        return "Salary data unavailable"
    return f"₹{salary / 100000:.1f} LPA"


def build_job_candidates(predicted_careers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()

    for prediction in predicted_careers:
        career_name = str(prediction.get("career", "")).strip()
        if not career_name:
            continue

        variants = CAREER_JOB_VARIANTS.get(
            career_name,
            [{"job_title": career_name, "experience_level": "Entry to Intermediate", "minimum_readiness": 35}],
        )

        for variant in variants:
            title = str(variant.get("job_title", "")).strip()
            if not title or title.lower() in seen:
                continue
            seen.add(title.lower())

            matched = list(prediction.get("matched_skills", []))
            missing = list(prediction.get("missing_skills", []))

            candidates.append({
                "job_title": title,
                "career_category": career_name,
                "experience_level": variant.get("experience_level", "Entry Level"),
                "minimum_readiness": int(variant.get("minimum_readiness", 30) or 30),
                "description": prediction.get("description", ""),
                "career_match_percentage": int(prediction.get("match_percentage", prediction.get("resume_match_score", 0)) or 0),
                "career_final_score": int(prediction.get("final_career_score", prediction.get("match_percentage", 0)) or 0),
                "required_skills": matched + missing,
            })

    return candidates


def calculate_job_skill_match(*, extracted_skills: list[str], required_skills: list[str]) -> dict[str, Any]:
    user_skills = {normalize_skill(skill) for skill in extracted_skills if str(skill).strip()}
    matched: list[str] = []
    missing: list[str] = []

    for skill in required_skills:
        if normalize_skill(skill) in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    score = round(len(matched) / len(required_skills) * 100) if required_skills else 0
    return {"matched_skills": matched, "missing_skills": missing, "match_percentage": score}


def calculate_trending_skill_match(*, extracted_skills: list[str], trending_skills: list[str]) -> dict[str, Any]:
    user_skills = {normalize_skill(skill) for skill in extracted_skills if str(skill).strip()}
    matched: list[str] = []
    missing: list[str] = []

    for skill in trending_skills:
        if normalize_skill(skill) in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    score = round(len(matched) / len(trending_skills) * 100) if trending_skills else 0
    return {"score": score, "matched": matched, "missing": missing}


def get_application_status(*, final_score: int, readiness_score: int, minimum_readiness: int) -> str:
    if final_score >= 75 and readiness_score >= minimum_readiness:
        return "Strong Match"
    if final_score >= 55 and readiness_score >= minimum_readiness:
        return "Good Match"
    if final_score >= 35:
        return "Potential Match"
    return "Needs Preparation"


def get_preparation_advice(*, status: str, missing_skills: list[str]) -> str:
    if status == "Strong Match":
        return "You can start applying for this role. Customize your resume for each vacancy and prepare role-specific interview examples."
    if status == "Good Match":
        return "You are suitable for this role. Strengthen the remaining skills and add relevant evidence to your resume."

    priority_text = ", ".join(missing_skills[:3]) or "the main missing skills"
    if status == "Potential Match":
        return f"Build stronger practical knowledge before applying. Focus first on: {priority_text}."
    return f"Complete the recommended learning roadmap before applying. Important skills: {priority_text}."


async def enrich_job_with_live_market(*, candidate: dict[str, Any], extracted_skills: list[str], readiness_score: int, location: str) -> dict[str, Any]:
    job_title = candidate["job_title"]
    skill_result = calculate_job_skill_match(
        extracted_skills=extracted_skills,
        required_skills=candidate.get("required_skills", []),
    )

    try:
        live_result = await analyze_live_job_market(
            role=job_title,
            location=location,
            results_per_page=50,
        )
    except Exception as error:
        print(f"Live job-market error for {job_title}:", error)
        live_result = {
            "success": False,
            "market_demand_score": 0,
            "demand_level": "Unavailable",
            "job_count": 0,
            "average_salary": None,
            "top_locations": [],
            "top_companies": [],
            "trending_skills": [],
            "fetched_at": None,
        }

    live_available = bool(live_result.get("success"))
    trending_skills = normalize_live_skill_items(live_result.get("trending_skills", []))
    trend_result = calculate_trending_skill_match(
        extracted_skills=extracted_skills,
        trending_skills=trending_skills,
    )

    resume_match = int(skill_result["match_percentage"] or candidate.get("career_match_percentage", 0) or 0)
    career_score = int(candidate.get("career_final_score", 0) or 0)
    market_score = int(live_result.get("market_demand_score", 0) or 0)
    trend_score = int(trend_result["score"] or 0)
    readiness = min(max(int(readiness_score or 0), 0), 100)

    if live_available:
        final_score = round(
            resume_match * 0.45
            + market_score * 0.20
            + trend_score * 0.15
            + readiness * 0.10
            + career_score * 0.10
        )
    else:
        final_score = round(resume_match * 0.60 + readiness * 0.20 + career_score * 0.20)

    final_score = min(max(final_score, 0), 100)
    status = get_application_status(
        final_score=final_score,
        readiness_score=readiness,
        minimum_readiness=int(candidate.get("minimum_readiness", 30) or 30),
    )
    average_salary = live_result.get("average_salary")

    return {
        "job_title": job_title,
        "career_category": candidate["career_category"],
        "experience_level": candidate["experience_level"],
        "description": candidate.get("description", ""),
        "match_percentage": resume_match,
        "recommendation_score": final_score,
        "application_status": status,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "required_skill_count": len(candidate.get("required_skills", [])),
        "matched_skill_count": len(skill_result["matched_skills"]),
        "preparation_advice": get_preparation_advice(status=status, missing_skills=skill_result["missing_skills"]),
        "resume_match_score": resume_match,
        "market_demand_score": market_score,
        "trending_skill_score": trend_score,
        "career_score": career_score,
        "readiness_score": readiness,
        "live_job_count": int(live_result.get("job_count", 0) or 0),
        "average_salary": average_salary,
        "salary_range": format_indian_salary(average_salary) if average_salary else "Salary data unavailable",
        "demand_level": live_result.get("demand_level", "Unavailable"),
        "top_locations": normalize_named_items(live_result.get("top_locations", []), "location"),
        "top_companies": normalize_named_items(live_result.get("top_companies", []), "company"),
        "trending_skills": trending_skills,
        "matched_trending_skills": trend_result["matched"],
        "missing_trending_skills": trend_result["missing"],
        "market_data_source": live_result.get("source", "Adzuna") if live_available else "Local calculation",
        "live_data_available": live_available,
        "market_data_updated_at": live_result.get("fetched_at"),
    }


async def recommend_jobs_with_live_market(
    *,
    extracted_skills: list[str],
    predicted_careers: list[dict[str, Any]],
    readiness_score: int,
    limit: int = 6,
    location: str = "India",
) -> dict[str, Any]:
    candidates = build_job_candidates(predicted_careers)
    if not candidates:
        return {"best_job": None, "total_recommendations": 0, "recommendations": []}

    candidate_limit = max(min(limit * 2, 10), limit)
    selected = candidates[:candidate_limit]

    recommendations = list(await asyncio.gather(*[
        enrich_job_with_live_market(
            candidate=candidate,
            extracted_skills=extracted_skills,
            readiness_score=readiness_score,
            location=location,
        )
        for candidate in selected
    ]))

    recommendations.sort(
        key=lambda item: (
            item["recommendation_score"],
            item["match_percentage"],
            item["market_demand_score"],
            item["live_job_count"],
        ),
        reverse=True,
    )

    top = recommendations[:limit]
    return {
        "best_job": top[0]["job_title"] if top else None,
        "total_recommendations": len(top),
        "recommendations": top,
    }


def recommend_jobs(
    extracted_skills: list[str],
    predicted_careers: list[dict[str, Any]],
    readiness_score: int,
    limit: int = 6,
) -> dict[str, Any]:
    """Backward-compatible local fallback."""
    candidates = build_job_candidates(predicted_careers)
    recommendations: list[dict[str, Any]] = []

    for candidate in candidates:
        skill_result = calculate_job_skill_match(
            extracted_skills=extracted_skills,
            required_skills=candidate.get("required_skills", []),
        )
        resume_match = int(skill_result["match_percentage"] or candidate.get("career_match_percentage", 0) or 0)
        readiness = min(max(int(readiness_score or 0), 0), 100)
        career_score = int(candidate.get("career_final_score", 0) or 0)
        final_score = min(max(round(resume_match * 0.65 + readiness * 0.20 + career_score * 0.15), 0), 100)
        status = get_application_status(
            final_score=final_score,
            readiness_score=readiness,
            minimum_readiness=candidate["minimum_readiness"],
        )

        recommendations.append({
            "job_title": candidate["job_title"],
            "career_category": candidate["career_category"],
            "experience_level": candidate["experience_level"],
            "description": candidate.get("description", ""),
            "match_percentage": resume_match,
            "recommendation_score": final_score,
            "application_status": status,
            "matched_skills": skill_result["matched_skills"],
            "missing_skills": skill_result["missing_skills"],
            "required_skill_count": len(candidate.get("required_skills", [])),
            "matched_skill_count": len(skill_result["matched_skills"]),
            "preparation_advice": get_preparation_advice(status=status, missing_skills=skill_result["missing_skills"]),
        })

    recommendations.sort(
        key=lambda item: (item["recommendation_score"], item["match_percentage"], item["matched_skill_count"]),
        reverse=True,
    )
    top = recommendations[:limit]
    return {
        "best_job": top[0]["job_title"] if top else None,
        "total_recommendations": len(top),
        "recommendations": top,
    }