# app/domain/model/health_check.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .value_objects import ServiceId, HealthStatus, Version


@dataclass
class HealthCheckResult:
    """
    Domain representation of a single health check measurement.
    """
    service_id: ServiceId
    timestamp: datetime
    status: HealthStatus
    latency_ms: int | None
    version: Version | None
    version_matches_expected: bool | None
    error_message: str | None = None
