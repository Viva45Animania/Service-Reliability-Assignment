# app/domain/model/value_objects.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NewType


# Strongly-typed wrapper around a string ID
ServiceId = NewType("ServiceId", str)


class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    UAT = "uat"
    DEV = "dev"
    UNKNOWN = "unknown"


class HealthStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"
    # You can add DEGRADED later as a stretch


@dataclass(frozen=True)
class Version:
    """
    Simple value object for a service version.
    For now it's just a string wrapper; later you can add parsing/comparison logic if needed.
    """
    value: str

    def __str__(self) -> str:
        return self.value

    def is_same_as(self, other: "Version | None") -> bool:
        if other is None:
            return False
        return self.value == other.value
