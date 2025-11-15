# app/application/use_cases/initialize_services_from_config.py
from __future__ import annotations

from app.domain.repository.service_repository import ServiceRepository
from app.infrastructure.config.service_config_loader import ServiceConfigLoader


class InitializeServicesFromConfig:
    """
    Use case: load services from config file and upsert into the repository.
    Intended to run at application startup.
    """

    def __init__(
        self,
        service_repo: ServiceRepository,
        config_loader: ServiceConfigLoader,
    ) -> None:
        self._service_repo = service_repo
        self._config_loader = config_loader

    def execute(self) -> None:
        services = self._config_loader.load()
        if not services:
            # Nothing to seed – that's fine.
            return

        self._service_repo.save_or_update_many(services)
