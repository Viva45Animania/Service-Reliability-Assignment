# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Service Reliability Monitor"
    db_url: str = "sqlite:///./health.db"
    health_check_interval_seconds: int = 60
    services_config_path: str = "config/services.json"

    alert_consecutive_failures_threshold: int = 3
    alert_webhook_url: str | None = None  # optional; if not set, log-only alerts

    class Config:
        env_file = ".env"

settings = Settings()
