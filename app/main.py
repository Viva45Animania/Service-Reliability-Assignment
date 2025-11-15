# app/main.py
from fastapi import FastAPI

from app.interfaces.api.health_router import router as health_router
from app.infrastructure.db.base import Base, engine, SessionLocal
from app.infrastructure.scheduling.health_check_scheduler import start_health_check_scheduler
from app.infrastructure.db.sqlite_service_repository import SQLiteServiceRepository
from app.infrastructure.config.service_config_loader import ServiceConfigLoader
from app.application.use_cases.initialize_services_from_config import InitializeServicesFromConfig
from config.settings import settings

def service_reliability_app() -> FastAPI:
    app = FastAPI(
        title="Service Reliability Monitor",
        version="0.1.0",
        description="Lightweight service reliability monitor.",
    )

    # Create DB tables on startup (for MVP; you can move to migrations later)
    @app.on_event("startup")
    async def on_startup():
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()
        try:
            service_repo = SQLiteServiceRepository(db)
            loader = ServiceConfigLoader(settings.services_config_path)
            init_uc = InitializeServicesFromConfig(service_repo, loader)
            init_uc.execute()
        finally:
            db.close()

        start_health_check_scheduler()

    # Routers
    app.include_router(health_router, prefix="/health", tags=["health"])

    @app.get("/ping")
    async def ping():
        return {"status": "ok"}

    return app

app = service_reliability_app()
