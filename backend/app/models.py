from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    resumes = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    file_name = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    extracted_text = Column(
        Text,
        nullable=True
    )

    extracted_skills = Column(
        Text,
        nullable=True
    )

    ats_score = Column(
        Integer,
        nullable=True
    )

    ats_rating = Column(
        String,
        nullable=True
    )

    ats_analysis = Column(
        Text,
        nullable=True
    )

    best_career = Column(
    String,
    nullable=True
    )

    career_predictions = Column(
    Text,
    nullable=True
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    career_readiness = Column(
    Integer,
    nullable=True
    )

    readiness_level = Column(
    String,
    nullable=True
    )

    skill_gap_analysis = Column(
    Text,
    nullable=True
    )

    learning_recommendations = Column(
    Text,
    nullable=True
    )

    best_job = Column(
    String,
    nullable=True
    )

    job_recommendations = Column(
    Text,
    nullable=True
    )

    user = relationship(
        "User",
        back_populates="resumes"
    )
    