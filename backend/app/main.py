from fastapi import FastAPI
from app.config import settings
from app.database import engine
from app.models import Base
from app.alerts.router import router as alert_router
from app.metrics import router as metrics_router
from app.auth.routes import router as auth_router

from app.bulk_upload.routes import router as bulk_upload_router



app = FastAPI(title=settings.APP_NAME)

 

app.include_router(alert_router)
app.include_router(auth_router)
app.include_router(metrics_router)
app.include_router(bulk_upload_router)


@app.get("/health")
def health():
    return {"status": "ok"}
