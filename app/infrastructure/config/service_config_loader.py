# app/infrastructure/config/service_config_loader.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from app.domain.model.service import Service


@dataclass
class ServiceConfig:
    id: str
    name: str
    url: str
    expectedVersion: Optional[str]
    environment: Optional[str]
    enabled: bool = True


class ServiceConfigLoader:
    """
    Loads monitored service definitions from a JSON config file and
    converts them into domain Service entities.
    """

    def __init__(self, config_path: str) -> None:
        self._path = Path(config_path)

    def load(self) -> List[Service]:
        if not self._path.exists():
            # No config file: return empty list instead of crashing.
            return []

        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        services_data = data.get("services", [])
        services: List[Service] = []

        for raw in services_data:
            cfg = ServiceConfig(
                id=raw["id"],
                name=raw["name"],
                url=raw["url"],
                expectedVersion=raw.get("expectedVersion"),
                environment=raw.get("environment"),
                enabled=raw.get("enabled", True),
            )

            service = Service.from_primitives(
                id=cfg.id,
                name=cfg.name,
                url=cfg.url,
                expected_version=cfg.expectedVersion,
                environment=cfg.environment,
                enabled=cfg.enabled,
            )
            services.append(service)

        return services
