# app/interfaces/ui/dashboard_router.py
from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.application.dto.service_health_summary_dto import ServiceHealthSummaryDto
from app.application.use_cases.get_latest_health_status import GetLatestHealthStatusForAllServices
from app.infrastructure.db.base import get_db
from app.infrastructure.db.sqlite_service_repository import SQLiteServiceRepository
from app.infrastructure.db.sqlite_health_check_repository import SQLiteHealthCheckRepository

router = APIRouter()

# Point Jinja2 at the templates directory (relative to project root)
templates = Jinja2Templates(directory="app/interfaces/ui/templates")


def get_latest_health_use_case(
    db: Session = Depends(get_db),
) -> GetLatestHealthStatusForAllServices:
    service_repo = SQLiteServiceRepository(db)
    health_repo = SQLiteHealthCheckRepository(db)
    return GetLatestHealthStatusForAllServices(service_repo, health_repo)


@router.get(
    "/",
    summary="Service health dashboard",
    include_in_schema=False,  # hide from /docs; it's a human-facing page
)
async def dashboard(
    request: Request,
    use_case: GetLatestHealthStatusForAllServices = Depends(get_latest_health_use_case),
):
    services: List[ServiceHealthSummaryDto] = use_case.execute()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "services": services,
        },
    )
