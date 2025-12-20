# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    DATABASE_URL: str
    REDIS_URL: Optional[str] = "redis://redis:6379/0"
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:3000"
    COMPANY_KEY: str  # For any tenant-specific encryption if needed
    ENCRYPTION_KEY: Optional[str] = None  # For provider creds encryption
    BATCH_SIZE: int = 1000  # For ingestion batches
    # Provider-specific (e.g., for adapters)
    SOLARMAN_EMAIL: Optional[str] = None
    SOLARMAN_PASSWORD_SHA256: Optional[str] = None
    SOLARMAN_APP_ID: Optional[str] = None
    SOLARMAN_APP_SECRET: Optional[str] = None
    LOG_LEVEL: str = "INFO"

settings = Settings()