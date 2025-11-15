# app/domain/repository/service_repository.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional, List

from app.domain.model.service import Service
from app.domain.model.value_objects import ServiceId


class ServiceRepository(ABC):
    """
    Abstraction over how services are stored/retrieved.
    Implemented in infrastructure layer (e.g. SQLiteServiceRepository).
    """

    @abstractmethod
    def find_all_enabled(self) -> List[Service]:
        ...

    @abstractmethod
    def find_by_id(self, service_id: ServiceId) -> Optional[Service]:
        ...

    @abstractmethod
    def list_all(self) -> List[Service]:
        ...

    @abstractmethod
    def save(self, service: Service) -> None:
        """
        Insert or update a single service.
        """
        ...

    def save_or_update_many(self, services: Iterable[Service]) -> None:
        """
        Default implementation in terms of save(); can be overridden.
        """
        for service in services:
            self.save(service)
