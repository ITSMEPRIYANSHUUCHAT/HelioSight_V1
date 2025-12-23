# app/models/enums.py
from enum import Enum


class UserRole(str, Enum):
    super_admin = "super_admin"
    company_admin = "company_admin"
    end_user = "end_user"


class ProviderType(str, Enum):
    solis = "solis"
    solarman = "solarman"
    shinemonitor = "shinemonitor"
    other = "other"
