from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.company import Company
from app.models.user_profile import UserProfile
from app.models.user_hardware import UserHardwareProfile
from app.models.enums import UserRole
from app.auth.security import hash_password
from app.auth.schemas import SignupRequest


def signup_user(db: Session, data: SignupRequest):
    user_data = data.user

    # ---------------------------
    # 1️⃣ Uniqueness checks
    # ---------------------------
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # ---------------------------
    # 2️⃣ Company creation (OPTIONAL)
    # ---------------------------
    company = None
    role = UserRole.end_user

    if data.company is not None:
        # Create company
        company = Company(
            name=data.company.name,
            description=data.company.description,
            is_active=True,
        )
        db.add(company)
        db.flush()  # get company.id

        role = UserRole.company_admin

    # ---------------------------
    # 3️⃣ Create user
    # ---------------------------
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.fullname,
        hashed_password=hash_password(user_data.password),
        role=role,
        company_id=company.id if company else None,
        is_active=True,
    )
    db.add(user)
    db.flush()  # get user.id

    # ---------------------------
    # 4️⃣ Create user profile
    # ---------------------------
    profile = UserProfile(
        user_id=user.id,
        whatsapp_number=data.whatsapp_number,
        address_line_1=data.address,
        city=None,
        state=None,
        country=None,
        pincode=None,
    )
    db.add(profile)

    # ---------------------------
    # 5️⃣ Create hardware profile (optional fields OK)
    # ---------------------------
    hardware = UserHardwareProfile(
        user_id=user.id,
        panel_brand=data.panel_brand,
        panel_capacity_kw=data.panel_capacity,
        panel_type=data.panel_type,
        inverter_brand=data.inverter_brand,
        inverter_capacity_kw=data.inverter_capacity,
    )
    db.add(hardware)

    # ---------------------------
    # 6️⃣ Commit
    # ---------------------------
    db.commit()
    db.refresh(user)

    return user
