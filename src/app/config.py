"""Configuración por variables de entorno (spec: architecture.md, RN-04, RN-05, RNF-03)."""
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./tutorias.db"
    business_timezone: str = "America/Panama"
    session_minutes: int = 60          # RN-05
    min_notice_minutes: int = 60       # RN-04
    admin_token: str = "cambia-este-token-admin"


settings = Settings()


def local_now() -> datetime:
    """Hora actual en la zona del negocio, como datetime naive (criterio único, RNF-03)."""
    return datetime.now(ZoneInfo(settings.business_timezone)).replace(tzinfo=None)
