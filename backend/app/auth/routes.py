# app/auth/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.schemas import LoginRequest, TokenResponse, UserOut
from app.auth.security import verify_password, create_access_token
from app.auth.dependencies import get_current_user
from app.models.user import User

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.schemas import SignupRequest, UserOut
from app.auth.services import signup_user

router = APIRouter(prefix="/auth", tags=["Auth"])
 


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        subject=str(user.id),
        role=user.role.value,
        company_id=str(user.company_id) if user.company_id else None,
    )

    return {"access_token": token}

@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    payload: SignupRequest,
    db: Session = Depends(get_db),
):
    user = signup_user(db, payload)
    return user
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
