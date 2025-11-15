# app/application/use_cases/run_health_check_cycle.py
from __future__ import annotations

from app.domain.repository.service_repository import ServiceRepository
from app.application.use_cases.run_health_check_for_service import RunHealthCheckForService


class RunHealthCheckCycle:
    """
    Use case: run a health check for all enabled services.
    """

    def __init__(
        self,
        service_repo: ServiceRepository,
        run_health_check_for_service: RunHealthCheckForService,
    ) -> None:
        self._service_repo = service_repo
        self._run_health_check_for_service = run_health_check_for_service

    async def execute(self) -> None:
        services = self._service_repo.find_all_enabled()
        # MVP: simple sequential execution – can be parallelised later if needed
        for service in services:
            await self._run_health_check_for_service.execute(service)
