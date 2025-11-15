# app/application/use_cases/get_health_history_for_service.py
from __future__ import annotations

from typing import Optional

from app.application.dto.service_details_dto import ServiceDetailsDto
from app.domain.model.value_objects import ServiceId
from app.domain.repository.health_check_repository import HealthCheckRepository
from app.domain.repository.service_repository import ServiceRepository


class ServiceNotFoundError(Exception):
    pass


class GetHealthHistoryForService:
    """
    Use case: retrieve recent health checks for a single service.
    """

    def __init__(
        self,
        service_repo: ServiceRepository,
        health_repo: HealthCheckRepository,
    ) -> None:
        self._service_repo = service_repo
        self._health_repo = health_repo

    def execute(self, service_id_str: str, limit: int = 20) -> ServiceDetailsDto:
        sid = ServiceId(service_id_str)
        service = self._service_repo.find_by_id(sid)
        if service is None:
            raise ServiceNotFoundError(f"Service '{service_id_str}' not found")

        checks = self._health_repo.find_recent_by_service_id(sid, limit=limit)
        return ServiceDetailsDto.from_domain(service, checks)
