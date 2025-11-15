# app/interfaces/api/health_router.py
# from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.application.dto.service_health_summary_dto import ServiceHealthSummaryDto
from app.application.dto.service_details_dto import ServiceDetailsDto
from app.application.use_cases.get_latest_health_status import GetLatestHealthStatusForAllServices
from app.application.use_cases.get_health_history_for_service import (GetHealthHistoryForService,ServiceNotFoundError)
from app.infrastructure.db.base import get_db
from app.infrastructure.db.sqlite_service_repository import SQLiteServiceRepository
from app.infrastructure.db.sqlite_health_check_repository import SQLiteHealthCheckRepository


router = APIRouter()


# class ServiceHealthStub(BaseModel):
#     serviceId: str
#     name: str
#     environment: str
#     status: str
#     latencyMs: Optional[int] = None
#     version: Optional[str] = None
#     versionMatchesExpected: Optional[bool] = None
#     lastCheckedAt: datetime


# @router.get(
#     "/",
#     summary="Get latest health status for all services",
#     response_model=List[ServiceHealthStub],
# )
# async def get_all_health() -> List[ServiceHealthStub]:
#     # MVP stub – later this will call the GetLatestHealthStatusForAllServices use case
#     now = datetime.utcnow()
#     return [
#         ServiceHealthStub(
#             serviceId="example-service",
#             name="Example Service",
#             environment="production",
#             status="UNKNOWN",
#             latencyMs=None,
#             version=None,
#             versionMatchesExpected=None,
#             lastCheckedAt=now,
#         )
#     ]

# def get_latest_health_use_case(db: Session = Depends(get_db)) -> GetLatestHealthStatusForAllServices:
#     service_repo = SQLiteServiceRepository(db)
#     health_repo = SQLiteHealthCheckRepository(db)
#     return GetLatestHealthStatusForAllServices(service_repo, health_repo)

#functions
def get_repositories(db: Session = Depends(get_db)):
    service_repo = SQLiteServiceRepository(db)
    health_repo = SQLiteHealthCheckRepository(db)
    return service_repo, health_repo

def get_latest_health_use_case(repos = Depends(get_repositories)) -> GetLatestHealthStatusForAllServices:
    service_repo, health_repo = repos
    return GetLatestHealthStatusForAllServices(service_repo, health_repo)

def get_health_history_use_case(
    repos = Depends(get_repositories),
) -> GetHealthHistoryForService:
    service_repo, health_repo = repos
    return GetHealthHistoryForService(service_repo, health_repo)

#routes
@router.get("/",summary="Get latest health status for all services",response_model=List[ServiceHealthSummaryDto])
async def get_all_health(
    use_case: GetLatestHealthStatusForAllServices = Depends(get_latest_health_use_case),
) -> List[ServiceHealthSummaryDto]:
    return use_case.execute()

@router.get("/{service_id}",summary="Get recent health history for a single service",response_model=ServiceDetailsDto)
async def get_health_for_service(
    service_id: str,
    limit: int = Query(20, ge=1, le=100),
    use_case: GetHealthHistoryForService = Depends(get_health_history_use_case),
) -> ServiceDetailsDto:
    try:
        return use_case.execute(service_id_str=service_id, limit=limit)
    except ServiceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
