# app/infrastructure/alerting/alert_notifier.py
from __future__ import annotations

import json
import logging
from typing import Sequence

import httpx

from app.domain.model.health_check import HealthCheckResult
from app.domain.model.service import Service
from config.settings import settings

logger = logging.getLogger(__name__)


class AlertNotifier:
    """
    Sends alerts when certain conditions are met.
    MVP: log to console; optionally POST to a webhook if configured.
    """

    def __init__(self, webhook_url: str | None = None) -> None:
        self._webhook_url = webhook_url or settings.alert_webhook_url

    async def service_down_repeatedly(
        self,
        service: Service,
        recent_checks: Sequence[HealthCheckResult],
        threshold: int,
    ) -> None:
        """
        Called when a service has been DOWN for `threshold` consecutive checks.
        """
        message = (
            f"ALERT: Service '{service.name}' ({service.id}) has been DOWN for "
            f"{threshold} consecutive checks. Last status at {recent_checks[0].timestamp}."
        )

        # Always log
        logger.warning(message)

        # Optionally send webhook
        if self._webhook_url:
            payload = {
                "serviceId": str(service.id),
                "name": service.name,
                "url": service.url,
                "environment": service.environment.value,
                "consecutiveFailures": threshold,
                "lastStatus": recent_checks[0].status.value,
                "lastCheckedAt": recent_checks[0].timestamp.isoformat(),
            }
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    await client.post(
                        self._webhook_url,
                        headers={"Content-Type": "application/json"},
                        content=json.dumps(payload),
                    )
            except Exception as exc:  # noqa: BLE001
                logger.exception(
                    "Failed to send alert webhook for service %s: %s", service.id, exc
                )
