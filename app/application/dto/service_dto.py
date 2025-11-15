from typing import Optional

from pydantic import BaseModel

from app.domain.model.service import Service


class ServiceDto(BaseModel):
    serviceId: str
    name: str
    url: str
    expectedVersion: Optional[str] = None
    environment: str
    enabled: bool

    @classmethod
    def from_domain(cls, service: Service) -> "ServiceDto":
        return cls(
            serviceId=str(service.id),
            name=service.name,
            url=service.url,
            expectedVersion=service.expected_version.value if service.expected_version else None,
            environment=service.environment.value,
            enabled=service.enabled,
        )


class CreateServiceRequest(BaseModel):
    serviceId: str
    name: str
    url: str
    expectedVersion: Optional[str] = None
    environment: Optional[str] = "unknown"
    enabled: bool = True
