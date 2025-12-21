from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import SignupRequest, LoginRequest, TokenResponse, UserOut
from app.auth.services import signup_user
from app.auth.security import authenticate_user, create_access_token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = signup_user(db, payload)
    return UserOut(
        id=str(user.id),
        email=user.email,
        role=user.role,
        company_id=str(user.company_id) if user.company_id else None,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    token = create_access_token(user)
    return TokenResponse(access_token=token)
