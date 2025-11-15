# app/application/use_cases/get_latest_health_status.py
from __future__ import annotations

from typing import List

from app.application.dto.service_health_summary_dto import ServiceHealthSummaryDto
from app.domain.repository.service_repository import ServiceRepository
from app.domain.repository.health_check_repository import HealthCheckRepository


class GetLatestHealthStatusForAllServices:
    def __init__(self, service_repo: ServiceRepository, health_repo: HealthCheckRepository) -> None:
        self._service_repo = service_repo
        self._health_repo = health_repo

    def execute(self) -> List[ServiceHealthSummaryDto]:
        services = self._service_repo.find_all_enabled()
        latest_checks = self._health_repo.find_latest_for_all_services()

        result: List[ServiceHealthSummaryDto] = []

        for service in services:
            check = latest_checks.get(service.id)
            if not check:
                # For MVP, you can either skip or show UNKNOWN entries.
                # Here we'll skip services with no health checks yet.
                continue

            dto = ServiceHealthSummaryDto.from_domain(service, check)
            result.append(dto)

        return result
