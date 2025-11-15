from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dto.service_dto import ServiceDto, CreateServiceRequest
from app.application.use_cases.service_list_services import ListServices
from app.application.use_cases.service_get_details import GetServiceDetails, ServiceNotFoundError
from app.application.use_cases.service_create import CreateService
from app.application.use_cases.service_set_enabled import SetServiceEnabled
from app.infrastructure.db.base import get_db
from app.infrastructure.db.sqlite_service_repository import SQLiteServiceRepository

router = APIRouter()


def get_service_repo(db: Session = Depends(get_db)) -> SQLiteServiceRepository:
    return SQLiteServiceRepository(db)


def get_list_services_uc(
    repo: SQLiteServiceRepository = Depends(get_service_repo),
) -> ListServices:
    return ListServices(repo)


def get_get_details_uc(
    repo: SQLiteServiceRepository = Depends(get_service_repo),
) -> GetServiceDetails:
    return GetServiceDetails(repo)


def get_create_service_uc(
    repo: SQLiteServiceRepository = Depends(get_service_repo),
) -> CreateService:
    return CreateService(repo)


def get_set_enabled_uc(
    repo: SQLiteServiceRepository = Depends(get_service_repo),
) -> SetServiceEnabled:
    return SetServiceEnabled(repo)


@router.get(
    "/",
    summary="List all monitored services",
    response_model=List[ServiceDto],
)
async def list_services(
    use_case: ListServices = Depends(get_list_services_uc),
) -> List[ServiceDto]:
    return use_case.execute()


@router.get(
    "/{service_id}",
    summary="Get details of a single service",
    response_model=ServiceDto,
)
async def get_service(
    service_id: str,
    use_case: GetServiceDetails = Depends(get_get_details_uc),
) -> ServiceDto:
    try:
        return use_case.execute(service_id_str=service_id)
    except ServiceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/",
    summary="Create or register a new service to monitor",
    response_model=ServiceDto,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    req: CreateServiceRequest,
    use_case: CreateService = Depends(get_create_service_uc),
) -> ServiceDto:
    return use_case.execute(req)


@router.patch(
    "/{service_id}/enable",
    summary="Enable health checks for a service",
    response_model=ServiceDto,
)
async def enable_service(
    service_id: str,
    use_case: SetServiceEnabled = Depends(get_set_enabled_uc),
) -> ServiceDto:
    try:
        return use_case.execute(service_id_str=service_id, enabled=True)
    except ServiceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch(
    "/{service_id}/disable",
    summary="Disable health checks for a service",
    response_model=ServiceDto,
)
async def disable_service(
    service_id: str,
    use_case: SetServiceEnabled = Depends(get_set_enabled_uc),
) -> ServiceDto:
    try:
        return use_case.execute(service_id_str=service_id, enabled=False)
    except ServiceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
