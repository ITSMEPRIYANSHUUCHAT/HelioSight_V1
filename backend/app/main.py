# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database import engine, Base  # Will be defined in Phase 2
from app.middleware import tenant_middleware
from app.logging import setup_logging
from app.auth.router import router as auth_router
# Import other routers in later phases, e.g., from app.companies.router import router as companies_router

setup_logging()

app = FastAPI(title="Solar SaaS Dashboard API", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tenant isolation middleware
app.middleware("http")(tenant_middleware)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Include routers (add more in later phases)
app.include_router(auth_router, prefix="/api/auth")

# Exception handler for production
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# In Phase 2, add: Base.metadata.create_all(bind=engine) if not using Alembic