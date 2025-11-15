from __future__ import annotations

from typing import List

from app.application.dto.service_dto import ServiceDto
from app.domain.repository.service_repository import ServiceRepository


class ListServices:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._service_repo = service_repo

    def execute(self) -> List[ServiceDto]:
        services = self._service_repo.list_all()
        return [ServiceDto.from_domain(s) for s in services]
