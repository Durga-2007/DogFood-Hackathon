"""
SQLAlchemy ORM models for the DOGFOOD 2026 portal.
All IDs are strings (fixture-compatible).
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, ForeignKey,
    Table, Integer, JSON
)
from sqlalchemy.orm import relationship
from database import Base


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ── Users ────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # organizer | participant | judge
    is_seeded = Column(Boolean, default=False)   # from fixtures

    # Relations
    team_memberships = relationship("TeamMember", back_populates="user")
    projects = relationship("Project", back_populates="owner")
    tokens = relationship("AuthToken", back_populates="user")


class AuthToken(Base):
    """Simple bearer token auth. One per user for seed accounts."""
    __tablename__ = "auth_tokens"

    token = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="tokens")


# ── Events ───────────────────────────────────────────────────────────────────

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    submissions_close = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utcnow)
    created_by = Column(String, ForeignKey("users.id"), nullable=True)
    is_seeded = Column(Boolean, default=False)

    tracks = relationship("Track", back_populates="event", cascade="all, delete-orphan")
    registrations = relationship("EventRegistration", back_populates="event")


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime, default=utcnow)

    event = relationship("Event", back_populates="registrations")
    user = relationship("User")


# ── Tracks ───────────────────────────────────────────────────────────────────

class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)

    event = relationship("Event", back_populates="tracks")
    projects = relationship("Project", back_populates="track")


# ── Judges ───────────────────────────────────────────────────────────────────

class JudgeTrack(Base):
    """Maps a judge (User with role=judge) to tracks they evaluate."""
    __tablename__ = "judge_tracks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    judge_id = Column(String, nullable=False)   # fixture judge id e.g. jdg_01
    track_id = Column(String, ForeignKey("tracks.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # linked User row


# ── Teams ────────────────────────────────────────────────────────────────────

class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=True)
    created_at = Column(DateTime, default=utcnow)
    is_seeded = Column(Boolean, default=False)

    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String, ForeignKey("teams.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    email = Column(String, nullable=False)   # from fixture: email-only members
    joined_at = Column(DateTime, default=utcnow)

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")


# ── Projects ─────────────────────────────────────────────────────────────────

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"), nullable=False)
    track_id = Column(String, ForeignKey("tracks.id"), nullable=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)  # creating user
    title = Column(String, nullable=False)
    summary = Column(Text, default="")
    repo_url = Column(String, default="")
    status = Column(String, default="draft")  # draft | submitted
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    is_seeded = Column(Boolean, default=False)

    team = relationship("Team", back_populates="projects")
    track = relationship("Track", back_populates="projects")
    owner = relationship("User", back_populates="projects")
    scores = relationship("Score", back_populates="project", cascade="all, delete-orphan")


# ── Scores ───────────────────────────────────────────────────────────────────

class Score(Base):
    """
    Stores judge scores. Retained from fixtures for T2 use.
    criteria stored as JSON dict e.g. {"functionality": 4, "quality": 3}
    """
    __tablename__ = "scores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    judge_fixture_id = Column(String, nullable=False)   # e.g. jdg_01
    judge_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    criteria = Column(JSON, nullable=False, default=dict)
    comment = Column(Text, default="")
    scored_at = Column(DateTime, default=utcnow)

    project = relationship("Project", back_populates="scores")
