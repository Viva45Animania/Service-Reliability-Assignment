# app/infrastructure/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.infrastructure.db.base import Base

class ServiceORM(Base):
    __tablename__ = "services"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    expected_version = Column(String, nullable=True)
    environment = Column(String, nullable=True)
    enabled = Column(Boolean, default=True)


class HealthCheckORM(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    latency_ms = Column(Integer, nullable=True)
    version = Column(String, nullable=True)
    version_matches_expected = Column(Boolean, nullable=True)
    error_message = Column(String, nullable=True)
