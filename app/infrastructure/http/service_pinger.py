# app/infrastructure/http/service_pinger.py
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from app.domain.model.service import Service


@dataclass
class PingResult:
    http_status_code: Optional[int]
    latency_ms: Optional[int]
    reported_version: Optional[str]
    error_message: Optional[str] = None


class HttpServicePinger:
    """
    Infrastructure service that pings a given service URL and returns raw data
    for the domain to interpret.
    """

    async def ping(self, service: Service) -> PingResult:
        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(service.url)
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            reported_version = self._extract_version(response)

            return PingResult(
                http_status_code=response.status_code,
                latency_ms=elapsed_ms,
                reported_version=reported_version,
                error_message=None,
            )
        except Exception as exc:  # noqa: BLE001
            # On error, we still consider this a ping result but DOWN
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return PingResult(
                http_status_code=None,
                latency_ms=elapsed_ms,
                reported_version=None,
                error_message=str(exc),
            )

    def _extract_version(self, response: httpx.Response) -> Optional[str]:
        """
        Very simple version extraction:
        - Try JSON body with 'version' key
        - If that fails, try 'X-Service-Version' header
        - Otherwise return None
        """
        # JSON body
        try:
            data = response.json()
            if isinstance(data, dict) and "version" in data:
                return str(data["version"])
        except (json.JSONDecodeError, ValueError):
            pass

        # Header
        version_header = response.headers.get("X-Service-Version")
        if version_header:
            return version_header

        return None
