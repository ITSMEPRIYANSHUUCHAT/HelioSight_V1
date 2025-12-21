from fastapi import Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.config import settings


def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise Exception
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
