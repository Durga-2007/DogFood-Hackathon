"""
Database configuration and connection management.
Uses SQLite via SQLAlchemy for simple, self-hosted operation.
"""
import os
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default database: local ./data/dogfood.db when not in Docker
_default_db_dir = pathlib.Path(__file__).parent.parent / "data"
_default_db_dir.mkdir(parents=True, exist_ok=True)
_default_db_path = str(_default_db_dir / "dogfood.db")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_default_db_path}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
