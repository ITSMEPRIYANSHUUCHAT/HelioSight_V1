# app/config.py

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -----------------------------
    # App
    # -----------------------------
    APP_NAME: str = "HelioSight"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # -----------------------------
    # Security
    # -----------------------------
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # -----------------------------
    # Database
    # -----------------------------
    DATABASE_URL: str

    # -----------------------------
    # Redis (future)
    # -----------------------------
    REDIS_URL: str | None = None

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
