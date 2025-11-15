# app/domain/repository/health_check_repository.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.domain.model.health_check import HealthCheckResult
from app.domain.model.value_objects import ServiceId


class HealthCheckRepository(ABC):
    """
    Abstraction over persisted health check results.
    Implemented in infrastructure layer (e.g. SQLiteHealthCheckRepository).
    """

    @abstractmethod
    def save(self, result: HealthCheckResult) -> None:
        ...

    @abstractmethod
    def find_latest_by_service_id(self, service_id: ServiceId) -> Optional[HealthCheckResult]:
        ...

    @abstractmethod
    def find_latest_for_all_services(self) -> Dict[ServiceId, HealthCheckResult]:
        """
        Should return at most one HealthCheckResult per service.
        """
        ...

    @abstractmethod
    def find_recent_by_service_id(self, service_id: ServiceId, limit: int = 20) -> List[HealthCheckResult]:
        ...
