# app/application/dto/service_health_summary_dto.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.domain.model.health_check import HealthCheckResult
from app.domain.model.service import Service


class ServiceHealthSummaryDto(BaseModel):
    serviceId: str
    name: str
    environment: str
    status: str
    latencyMs: Optional[int] = None
    version: Optional[str] = None
    versionMatchesExpected: Optional[bool] = None
    lastCheckedAt: datetime

    @classmethod
    def from_domain(cls, service: Service, check: HealthCheckResult) -> "ServiceHealthSummaryDto":
        return cls(
            serviceId=str(service.id),
            name=service.name,
            environment=service.environment.value,
            status=check.status.value,
            latencyMs=check.latency_ms,
            version=str(check.version) if check.version else None,
            versionMatchesExpected=check.version_matches_expected,
            lastCheckedAt=check.timestamp,
        )
