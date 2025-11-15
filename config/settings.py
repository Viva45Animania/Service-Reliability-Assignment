# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Service Reliability Monitor"
    db_url: str = "sqlite:///./health.db"
    health_check_interval_seconds: int = 60
    services_config_path: str = "config/services.json"

    class Config:
        env_file = ".env"

settings = Settings()
