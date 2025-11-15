from __future__ import annotations

from app.application.dto.service_dto import ServiceDto, CreateServiceRequest
from app.domain.model.service import Service
from app.domain.repository.service_repository import ServiceRepository


class CreateService:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._service_repo = service_repo

    def execute(self, req: CreateServiceRequest) -> ServiceDto:
        service = Service.from_primitives(
            id=req.serviceId,
            name=req.name,
            url=req.url,
            expected_version=req.expectedVersion,
            environment=req.environment,
            enabled=req.enabled,
        )
        self._service_repo.save(service)
        return ServiceDto.from_domain(service)
