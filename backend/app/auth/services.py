from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.auth.schemas import SignupRequest
from app.auth.security import hash_password
from app.models.user import User
from app.models.company import Company


def signup_user(db: Session, data: SignupRequest) -> User:
    user_data = data.user
    company_data = data.company

    # ---------- validations ----------
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    # ---------- company (optional) ----------
    company = None
    if company_data:
        company = Company(
            name=company_data.name,
            description=company_data.description,
        )
        db.add(company)
        db.flush()  # get company.id

    # ---------- user ----------
    user = User(
        email=user_data.email,
        full_name=user_data.fullname,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        company_id=company.id if company else None,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
