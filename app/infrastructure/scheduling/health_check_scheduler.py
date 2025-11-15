# app/infrastructure/scheduling/health_check_scheduler.py
from __future__ import annotations

import asyncio
import logging

from app.application.use_cases.run_health_check_for_service import RunHealthCheckForService
from app.application.use_cases.run_health_check_cycle import RunHealthCheckCycle
from app.domain.services.health_evaluation_service import HealthEvaluationService
from app.infrastructure.alerting.alert_notifier import AlertNotifier
from app.infrastructure.db.base import SessionLocal
from app.infrastructure.db.sqlite_service_repository import SQLiteServiceRepository
from app.infrastructure.db.sqlite_health_check_repository import SQLiteHealthCheckRepository
from app.infrastructure.http.service_pinger import HttpServicePinger
from config.settings import settings

logger = logging.getLogger(__name__)


async def health_check_loop() -> None:
    """
    Background loop that runs the health check cycle at a fixed interval.
    """
    interval = settings.health_check_interval_seconds
    logger.info("Starting health check scheduler with interval=%s seconds", interval)

    while True:
        logger.info("Starting health check cycle")
        db = SessionLocal()
        try:
            service_repo = SQLiteServiceRepository(db)
            health_repo = SQLiteHealthCheckRepository(db)
            pinger = HttpServicePinger()
            evaluator = HealthEvaluationService()

            run_single = RunHealthCheckForService(
                pinger=pinger,
                evaluator=evaluator,
                health_repo=health_repo,
            )
            cycle = RunHealthCheckCycle(
                service_repo=service_repo,
                run_health_check_for_service=run_single,
            )

            await cycle.execute()
            logger.info("Completed health check cycle")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error during health check cycle: %s", exc)
        finally:
            db.close()

        await asyncio.sleep(interval)

async def _evaluate_alerts(
    service_repo: SQLiteServiceRepository,
    health_repo: SQLiteHealthCheckRepository,
    notifier: AlertNotifier,
) -> None:
    """
    After a health check cycle, inspect recent results and trigger alerts
    for services that have been DOWN for N consecutive checks.
    """
    threshold = settings.alert_consecutive_failures_threshold
    services = service_repo.find_all_enabled()

    for service in services:
        recent = health_repo.find_recent_by_service_id(service.id, limit=threshold)
        if len(recent) < threshold:
            continue

        # We want the MOST recent 'threshold' checks; our repo returns them desc by timestamp
        # so recent[0] is the latest.
        all_down = all(check.status.name == "DOWN" for check in recent[:threshold])
        if all_down:
            await notifier.service_down_repeatedly(service, recent[:threshold], threshold)

async def health_check_loop() -> None:
    """
    Background loop that runs the health check cycle at a fixed interval.
    """
    interval = settings.health_check_interval_seconds
    logger.info("Starting health check scheduler with interval=%s seconds", interval)

    notifier = AlertNotifier()

    while True:
        logger.info("Starting health check cycle")
        db = SessionLocal()
        try:
            service_repo = SQLiteServiceRepository(db)
            health_repo = SQLiteHealthCheckRepository(db)
            pinger = HttpServicePinger()
            evaluator = HealthEvaluationService()

            run_single = RunHealthCheckForService(
                pinger=pinger,
                evaluator=evaluator,
                health_repo=health_repo,
            )
            cycle = RunHealthCheckCycle(
                service_repo=service_repo,
                run_health_check_for_service=run_single,
            )

            # Run the health checks
            await cycle.execute()

            # Evaluate alerts based on recent results
            await _evaluate_alerts(
                service_repo=service_repo,
                health_repo=health_repo,
                notifier=notifier,
            )

            logger.info("Completed health check cycle")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error during health check cycle: %s", exc)
        finally:
            db.close()

        await asyncio.sleep(interval)


def start_health_check_scheduler() -> None:
    """
    Kick off the background health check loop.
    Should be called from FastAPI startup event.
    """
    asyncio.create_task(health_check_loop())
