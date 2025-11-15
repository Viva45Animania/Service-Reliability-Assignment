# app/application/dto/service_details_dto.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.domain.model.health_check import HealthCheckResult
from app.domain.model.service import Service


class HealthCheckItemDto(BaseModel):
    timestamp: datetime
    status: str
    latencyMs: Optional[int] = None
    version: Optional[str] = None
    versionMatchesExpected: Optional[bool] = None
    errorMessage: Optional[str] = None

    @classmethod
    def from_domain(cls, check: HealthCheckResult) -> "HealthCheckItemDto":
        return cls(
            timestamp=check.timestamp,
            status=check.status.value,
            latencyMs=check.latency_ms,
            version=str(check.version) if check.version else None,
            versionMatchesExpected=check.version_matches_expected,
            errorMessage=check.error_message,
        )


class ServiceDetailsDto(BaseModel):
    serviceId: str
    name: str
    environment: str
    url: str
    checks: List[HealthCheckItemDto]

    @classmethod
    def from_domain(
        cls,
        service: Service,
        checks: List[HealthCheckResult],
    ) -> "ServiceDetailsDto":
        return cls(
            serviceId=str(service.id),
            name=service.name,
            environment=service.environment.value,
            url=service.url,
            checks=[HealthCheckItemDto.from_domain(c) for c in checks],
        )
