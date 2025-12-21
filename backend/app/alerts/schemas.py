from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AlertCreate(BaseModel):
    company_id: UUID
    plant_id: UUID | None = None
    device_id: UUID | None = None
    alert_type: str
    severity: str
    message: str


class AlertResponse(BaseModel):
    id: UUID
    alert_type: str
    severity: str
    message: str
    triggered_at: datetime
