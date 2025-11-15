# app/domain/services/health_evaluation_service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.model.health_check import HealthCheckResult
from app.domain.model.service import Service
from app.domain.model.value_objects import HealthStatus, Version, ServiceId


@dataclass
class HealthCheckInput:
    """
    Data passed from the infrastructure HTTP pinger into the domain.
    This keeps HTTP/client-specific details out of the domain.
    """
    http_status_code: int | None
    latency_ms: int | None
    reported_version: str | None
    error_message: str | None = None


class HealthEvaluationService:
    """
    Domain service that converts raw ping data into a HealthCheckResult.
    MVP logic: simple UP/DOWN + version match.
    """

    def evaluate(self, service: Service, data: HealthCheckInput, timestamp: datetime | None = None) -> HealthCheckResult:
        ts = timestamp or datetime.utcnow()

        # --- Determine status (MVP logic) ---
        if data.http_status_code is None:
            status = HealthStatus.DOWN
        elif 200 <= data.http_status_code < 300:
            status = HealthStatus.UP
        else:
            status = HealthStatus.DOWN

        # --- Version handling ---
        version_obj: Version | None = None
        version_matches: bool | None = None

        if data.reported_version is not None:
            version_obj = Version(data.reported_version)
            if service.expected_version is not None:
                version_matches = service.expected_version.is_same_as(version_obj)
            else:
                version_matches = None  # we don't know what to expect
        else:
            version_obj = None
            version_matches = None

        return HealthCheckResult(
            service_id=ServiceId(service.id),  # ensure it's the right type
            timestamp=ts,
            status=status,
            latency_ms=data.latency_ms,
            version=version_obj,
            version_matches_expected=version_matches,
            error_message=data.error_message,
        )
