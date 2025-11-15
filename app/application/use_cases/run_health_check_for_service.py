# app/application/use_cases/run_health_check_for_service.py
from __future__ import annotations

from datetime import datetime

from app.domain.model.service import Service
from app.domain.repository.health_check_repository import HealthCheckRepository
from app.domain.services.health_evaluation_service import (
    HealthEvaluationService,
    HealthCheckInput,
)
from app.infrastructure.http.service_pinger import HttpServicePinger


class RunHealthCheckForService:
    """
    Use case: run a single health check for one service.
    """

    def __init__(
        self,
        pinger: HttpServicePinger,
        evaluator: HealthEvaluationService,
        health_repo: HealthCheckRepository,
    ) -> None:
        self._pinger = pinger
        self._evaluator = evaluator
        self._health_repo = health_repo

    async def execute(self, service: Service) -> None:
        ping_result = await self._pinger.ping(service)

        input_data = HealthCheckInput(
            http_status_code=ping_result.http_status_code,
            latency_ms=ping_result.latency_ms,
            reported_version=ping_result.reported_version,
            error_message=ping_result.error_message,
        )

        health_check = self._evaluator.evaluate(
            service=service,
            data=input_data,
            timestamp=datetime.utcnow(),
        )

        self._health_repo.save(health_check)
