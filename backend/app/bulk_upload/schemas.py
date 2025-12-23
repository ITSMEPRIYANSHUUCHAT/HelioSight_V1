from pydantic import BaseModel
from typing import List, Optional


class BulkUserRow(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None

    provider_type: str  # solis / solarman / shinemonitor
    provider_username: str
    provider_password: str

    whatsapp_number: Optional[str] = None
    address_line_1: Optional[str] = None

    panel_brand: Optional[str] = None
    panel_capacity_kw: Optional[str] = None
    panel_type: Optional[str] = None

    inverter_brand: Optional[str] = None
    inverter_capacity_kw: Optional[str] = None


class BulkUploadPreview(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: List[str]


class BulkUploadResult(BaseModel):
    created_users: int
    skipped_users: int
    created_external_credentials: int
