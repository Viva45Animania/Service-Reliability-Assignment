# app/infrastructure/db/sqlite_health_check_repository.py
from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domain.model.health_check import HealthCheckResult
from app.domain.model.value_objects import ServiceId, HealthStatus, Version
from app.domain.repository.health_check_repository import HealthCheckRepository
from app.infrastructure.db.models import HealthCheckORM


class SQLiteHealthCheckRepository(HealthCheckRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def save(self, result: HealthCheckResult) -> None:
        row = HealthCheckORM(
            service_id=str(result.service_id),
            timestamp=result.timestamp,
            status=result.status.value,
            latency_ms=result.latency_ms,
            version=result.version.value if result.version else None,
            version_matches_expected=result.version_matches_expected,
            error_message=result.error_message,
        )
        self._db.add(row)
        self._db.commit()

    def find_latest_by_service_id(self, service_id: ServiceId) -> Optional[HealthCheckResult]:
        row = (
            self._db.query(HealthCheckORM)
            .filter(HealthCheckORM.service_id == str(service_id))
            .order_by(desc(HealthCheckORM.timestamp))
            .first()
        )
        if not row:
            return None
        return self._to_domain(row)

    def find_latest_for_all_services(self) -> Dict[ServiceId, HealthCheckResult]:
        """
        Simple but not super-optimised implementation:
        - For each distinct service_id, fetch the latest row.
        This is perfectly fine for MVP and small scale.
        """
        results: Dict[ServiceId, HealthCheckResult] = {}

        # Get distinct service_ids
        service_ids = [
            r[0]
            for r in self._db.query(HealthCheckORM.service_id)
            .distinct(HealthCheckORM.service_id)
            .all()
        ]

        for sid in service_ids:
            row = (
                self._db.query(HealthCheckORM)
                .filter(HealthCheckORM.service_id == sid)
                .order_by(desc(HealthCheckORM.timestamp))
                .first()
            )
            if row:
                domain_result = self._to_domain(row)
                results[ServiceId(sid)] = domain_result

        return results

    def find_recent_by_service_id(self, service_id: ServiceId, limit: int = 20) -> List[HealthCheckResult]:
        rows = (
            self._db.query(HealthCheckORM)
            .filter(HealthCheckORM.service_id == str(service_id))
            .order_by(desc(HealthCheckORM.timestamp))
            .limit(limit)
            .all()
        )
        return [self._to_domain(r) for r in rows]

    @staticmethod
    def _to_domain(row: HealthCheckORM) -> HealthCheckResult:
        return HealthCheckResult(
            service_id=ServiceId(row.service_id),
            timestamp=row.timestamp,
            status=HealthStatus(row.status),
            latency_ms=row.latency_ms,
            version=Version(row.version) if row.version else None,
            version_matches_expected=row.version_matches_expected,
            error_message=row.error_message,
        )
