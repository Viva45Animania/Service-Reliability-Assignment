from __future__ import annotations

from app.application.dto.service_dto import ServiceDto
from app.domain.model.value_objects import ServiceId
from app.domain.repository.service_repository import ServiceRepository
from app.application.use_cases.service_get_details import ServiceNotFoundError


class SetServiceEnabled:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._service_repo = service_repo

    def execute(self, service_id_str: str, enabled: bool) -> ServiceDto:
        sid = ServiceId(service_id_str)
        service = self._service_repo.find_by_id(sid)
        if service is None:
            raise ServiceNotFoundError(f"Service '{service_id_str}' not found")

        service.enabled = enabled
        self._service_repo.save(service)
        return ServiceDto.from_domain(service)
