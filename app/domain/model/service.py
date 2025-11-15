# app/domain/model/service.py
from __future__ import annotations

from dataclasses import dataclass

from .value_objects import ServiceId, Version, Environment


@dataclass
class Service:
    """
    Domain entity representing a monitored service.
    """
    id: ServiceId
    name: str
    url: str
    expected_version: Version | None
    environment: Environment
    enabled: bool = True

    @staticmethod
    def from_primitives(
        id: str,
        name: str,
        url: str,
        expected_version: str | None,
        environment: str | None,
        enabled: bool = True,
    ) -> "Service":
        """
        Helper factory to construct a Service from basic types (e.g. config/DB row).
        """
        from .value_objects import Version, Environment, ServiceId

        env = Environment(environment) if environment is not None else Environment.UNKNOWN
        version_obj = Version(expected_version) if expected_version is not None else None

        return Service(
            id=ServiceId(id),
            name=name,
            url=url,
            expected_version=version_obj,
            environment=env,
            enabled=enabled,
        )
