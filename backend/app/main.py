# app/main.py

from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/docs" if settings.ENV != "prod" else None,
    redoc_url="/redoc" if settings.ENV != "prod" else None,
)


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "env": settings.ENV,
    }
