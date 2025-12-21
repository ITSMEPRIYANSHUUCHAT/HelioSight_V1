from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

from app.models.enums import UserRole


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================
# SIGNUP
# =========================

class SignupRequest(BaseModel):
    # ---- Step 1: User ----
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str

    # ---- Step 2: Company ----
    company_name: str
    company_description: Optional[str] = None

    # ---- Role ----
    role: UserRole = UserRole.company_admin


# =========================
# OUTPUT
# =========================

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str]
    role: UserRole
    company_id: Optional[UUID]

    class Config:
        from_attributes = True
