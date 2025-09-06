from time import timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    PARTICIPANT = "participant"
    RESEARCH_ASSISTANT = "research_assistant"
    STUDY_COORDINATOR = "study_coordinator"
    ADMIN = "admin"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    users = relationship("User", back_populates="organization")
    studies = relationship("Study", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    client_id = Column(String, unique=True, nullable=False)
    client_secret_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    org_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    participant_sessions = relationship(
        "Session", foreign_keys="Session.participant_id", back_populates="participant"
    )


class Study(Base):
    __tablename__ = "studies"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    org_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    organization = relationship("Organization", back_populates="studies")
    sessions = relationship("Session", back_populates="study")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    study_id = Column(String, ForeignKey("studies.id"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    study = relationship("Study", back_populates="sessions")
    participant = relationship(
        "User", foreign_keys=[participant_id], back_populates="participant_sessions"
    )
