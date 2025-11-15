# app/infrastructure/db/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config.settings import settings
from typing import Generator

# For SQLite, check_same_thread=False is needed for use in async context with FastAPI
engine = create_engine(
    settings.db_url,
    connect_args={"check_same_thread": False} if settings.db_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session and ensures it's closed
    after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()