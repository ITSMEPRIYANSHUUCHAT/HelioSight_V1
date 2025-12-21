from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class NormalizedMetric(BaseModel):
    timestamp: datetime

    company_id: Optional[str] = None
    plant_external_id: str
    device_external_id: Optional[str]

    power_kw: Optional[float]
    energy_kwh: Optional[float]
    voltage_v: Optional[float]
    current_a: Optional[float]
    frequency_hz: Optional[float]

    provider: str
    raw_payload: Dict[str, Any]
