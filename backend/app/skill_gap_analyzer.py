from typing import Any

from app.career_predictor import CAREER_PROFILES


# Skills that should usually be learned first
SKILL_PRIORITY = {
    "Python": 10,
    "JavaScript": 10,
    "SQL": 10,
    "HTML": 9,
    "CSS": 9,
    "Git": 9,
    "React": 8,
    "Node.js": 8,
    "FastAPI": 8,
    "Express.js": 8,
    "PostgreSQL": 8,
    "MongoDB": 8,
    "Pandas": 8,
    "NumPy": 8,
    "Statistics": 8,
    "Machine Learning": 7,
    "Scikit-learn": 7,
    "REST API": 7,
    "Docker": 6,
    "AWS": 6,
    "Power BI": 6,
    "Tableau": 6,
    "TensorFlow": 5,
    "PyTorch": 5,
    "Deep Learning": 5,
    "Kubernetes": 4,
    "Terraform": 4
}


def normalize_skill(skill: str) -> str:
    """
    Convert a skill to lowercase and remove extra spaces.
    """

    return skill.strip().lower()


def get_readiness_level(score: int) -> str:
    """
    Return the user's career-readiness level.
    """

    if score >= 85:
        return "Job Ready"

    if score >= 70:
        return "Advanced"

    if score >= 50:
        return "Intermediate"

    if score >= 30:
        return "Beginner"

    return "Foundation Level"


def get_learning_time(missing_skill_count: int) -> str:
    """
    Estimate learning time from the number of missing skills.
    """

    if missing_skill_count == 0:
        return "No major learning gap"

    if missing_skill_count <= 2:
        return "2-4 weeks"

    if missing_skill_count <= 4:
        return "4-8 weeks"

    if missing_skill_count <= 6:
        return "8-12 weeks"

    return "12-20 weeks"


def sort_priority_skills(
    missing_skills: list[str]
) -> list[str]:
    """
    Sort missing skills according to their learning priority.
    """

    return sorted(
        missing_skills,
        key=lambda skill: SKILL_PRIORITY.get(skill, 1),
        reverse=True
    )


def analyze_skill_gap(
    extracted_skills: list[str],
    target_career: str
) -> dict[str, Any]:
    """
    Compare extracted resume skills with the selected
    career profile.
    """

    if not target_career:
        raise ValueError("Target career is required")

    career_profile = CAREER_PROFILES.get(target_career)

    if not career_profile:
        raise ValueError(
            f"Career profile not found: {target_career}"
        )

    normalized_user_skills = {
        normalize_skill(skill)
        for skill in extracted_skills
    }

    required_skills = career_profile["skills"]

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:
        normalized_required_skill = normalize_skill(
            required_skill
        )

        if normalized_required_skill in normalized_user_skills:
            matched_skills.append(required_skill)
        else:
            missing_skills.append(required_skill)

    total_required = len(required_skills)
    total_matched = len(matched_skills)

    if total_required == 0:
        readiness_score = 0
    else:
        readiness_score = round(
            (total_matched / total_required) * 100
        )

    readiness_level = get_readiness_level(
        readiness_score
    )

    sorted_missing_skills = sort_priority_skills(
        missing_skills
    )

    priority_skills = sorted_missing_skills[:3]

    estimated_learning_time = get_learning_time(
        len(missing_skills)
    )

    if readiness_score >= 85:
        summary = (
            f"You are well prepared for the "
            f"{target_career} role."
        )
    elif readiness_score >= 60:
        summary = (
            f"You have a strong foundation for the "
            f"{target_career} role, but should improve "
            f"a few important skills."
        )
    elif readiness_score >= 40:
        summary = (
            f"You have some relevant skills for the "
            f"{target_career} role, but additional "
            f"preparation is required."
        )
    else:
        summary = (
            f"You are at the beginning of the "
            f"{target_career} learning path. Focus on "
            f"the priority skills first."
        )

    return {
        "target_career": target_career,
        "career_description": career_profile["description"],
        "readiness_score": readiness_score,
        "readiness_level": readiness_level,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "priority_skills": priority_skills,
        "estimated_learning_time": estimated_learning_time,
        "matched_skill_count": total_matched,
        "missing_skill_count": len(missing_skills),
        "required_skill_count": total_required,
        "summary": summary
    }