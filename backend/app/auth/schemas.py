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

class SignupRequest(BaseModel):
    user: UserSignup
    company: Optional[CompanySignup] = None
    require_otp: bool = True


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
