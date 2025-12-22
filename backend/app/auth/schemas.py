from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.enums import UserRole


# ---------- USER CORE ----------

class UserSignup(BaseModel):
    username: str = Field(..., min_length=3)
    fullname: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    is_installer: bool = False
    role: UserRole = UserRole.end_user

    whatsapp_number: Optional[str] = None


# ---------- COMPANY CORE ----------

class CompanySignup(BaseModel):
    name: str
    description: Optional[str] = None


# ---------- MAIN SIGNUP ----------

class UserSignup(BaseModel):
    email: str
    username: str
    fullname: Optional[str]
    password: str
    confirm_password: str


class SignupRequest(BaseModel):
    user: UserSignup

    whatsapp_number: Optional[str] = Field(None, alias="whatsappNumber")
    address: Optional[str]

    panel_brand: Optional[str] = Field(None, alias="panelBrand")
    panel_capacity: Optional[str] = Field(None, alias="panelCapacity")
    panel_type: Optional[str] = Field(None, alias="panelType")

    inverter_brand: Optional[str] = Field(None, alias="inverterBrand")
    inverter_capacity: Optional[str] = Field(None, alias="inverterCapacity")

    class Config:
        populate_by_name = True


# ---------- LOGIN ----------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- RESPONSES ----------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: UserRole
    company_id: Optional[str]
