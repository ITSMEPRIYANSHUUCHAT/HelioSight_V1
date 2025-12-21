# app/metrics/schemas.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class MetricIn(BaseModel):
    company_id: UUID
    plant_id: UUID
    device_id: UUID

    provider: str
    metric_type: str
    value: float
    unit: Optional[str] = None
    timestamp: datetime
