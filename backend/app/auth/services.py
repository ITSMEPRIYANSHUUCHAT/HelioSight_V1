import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.company import Company
from app.models.enums import UserRole
from app.auth.security import hash_password


def signup_user(db: Session, data):
    """
    Creates:
    1. Company
    2. Company admin user
    """

    # -------------------------
    # 1️⃣ Check email uniqueness
    # -------------------------
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # -------------------------
    # 2️⃣ Create company
    # -------------------------
    company = Company(
        name=data.company_name,
        description=data.company_description,
        is_active=True,
    )
    db.add(company)
    db.flush()  # get company.id without commit

    # -------------------------
    # 3️⃣ Create user
    # -------------------------
    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=UserRole.company_admin,
        company_id=company.id,
        is_active=True,
    )
    db.add(user)

    # -------------------------
    # 4️⃣ Commit transaction
    # -------------------------
    db.commit()
    db.refresh(user)

    return user
