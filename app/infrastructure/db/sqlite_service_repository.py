# app/infrastructure/db/sqlite_service_repository.py
from __future__ import annotations

from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from app.domain.model.service import Service
from app.domain.model.value_objects import ServiceId
from app.domain.repository.service_repository import ServiceRepository
from app.infrastructure.db.models import ServiceORM


class SQLiteServiceRepository(ServiceRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_all_enabled(self) -> List[Service]:
        rows = (
            self._db.query(ServiceORM)
            .filter(ServiceORM.enabled == True)  # noqa: E712
            .all()
        )
        return [self._to_domain(row) for row in rows]

    def find_by_id(self, service_id: ServiceId) -> Optional[Service]:
        row = self._db.query(ServiceORM).filter(ServiceORM.id == str(service_id)).first()
        if not row:
            return None
        return self._to_domain(row)

    def save(self, service: Service) -> None:
        existing = (
            self._db.query(ServiceORM)
            .filter(ServiceORM.id == str(service.id))
            .first()
        )
        if existing:
            existing.name = service.name
            existing.url = service.url
            existing.expected_version = (
                service.expected_version.value if service.expected_version else None
            )
            existing.environment = service.environment.value
            existing.enabled = service.enabled
        else:
            row = ServiceORM(
                id=str(service.id),
                name=service.name,
                url=service.url,
                expected_version=service.expected_version.value if service.expected_version else None,
                environment=service.environment.value,
                enabled=service.enabled,
            )
            self._db.add(row)
        self._db.commit()

    def save_or_update_many(self, services: Iterable[Service]) -> None:
        for service in services:
            self.save(service)

    def list_all(self) -> List[Service]:
        rows = self._db.query(ServiceORM).all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(row: ServiceORM) -> Service:
        return Service.from_primitives(
            id=row.id,
            name=row.name,
            url=row.url,
            expected_version=row.expected_version,
            environment=row.environment,
            enabled=row.enabled,
        )
