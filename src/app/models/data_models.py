from enum import Enum as PyEnum
from uuid import uuid4

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class UserRole(str, PyEnum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default="user")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    created_mcqs = relationship(
        "MCQ", back_populates="creator", cascade="all, delete-orphan"
    )
    history = relationship(
        "UserHistory", back_populates="user", cascade="all, delete-orphan"
    )
    submissions = relationship(
        "Submission", back_populates="user", cascade="all, delete-orphan"
    )


class UserHistory(Base):
    __tablename__ = "user_history"

    history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    total_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    total_attempts = Column(Integer, nullable=False)
    attempted_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    submission_id = Column(
        UUID, ForeignKey("submissions.submission_id"), nullable=False
    )
    certificate = Column(String, nullable=False)

    user = relationship("User", back_populates="history")
    details = relationship(
        "UserHistoryDetail", back_populates="user_history", cascade="all, delete-orphan"
    )
    submission = relationship("Submission", back_populates="histories")


class UserHistoryDetail(Base):
    __tablename__ = "user_history_details"

    detail_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    history_id = Column(UUID, ForeignKey("user_history.history_id"), nullable=False)
    mcq_id = Column(UUID, ForeignKey("mcqs.mcq_id"), nullable=False)
    user_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    user_history = relationship("UserHistory", back_populates="details")
    mcq = relationship("MCQ")


class MCQ(Base):
    __tablename__ = "mcqs"

    mcq_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String, nullable=False)
    question = Column(String, nullable=False, unique=True)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)
    created_by = Column(UUID, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    creator = relationship("User", back_populates="created_mcqs")


class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    total_questions = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="submissions")
    histories = relationship("UserHistory", back_populates="submission")
