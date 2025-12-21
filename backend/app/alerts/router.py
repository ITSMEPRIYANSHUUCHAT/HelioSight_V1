from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.alerts.schemas import AlertCreate, AlertResponse
from app.alerts.service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/", response_model=AlertResponse)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    alert = AlertService.raise_alert(db, payload)
    return alert
