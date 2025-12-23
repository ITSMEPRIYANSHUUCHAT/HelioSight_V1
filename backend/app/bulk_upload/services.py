from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.enums import UserRole
from app.models.user_external_credentials import UserExternalCredentials
from app.auth.security import hash_password

from app.bulk_upload.schemas import BulkUploadRequest


def bulk_create_users_and_creds(
    db: Session,
    payload: BulkUploadRequest,
    company_id,
):
    created_users = {}
    results = {
        "users_created": 0,
        "external_credentials_created": 0,
    }

    # -------------------------
    # CREATE USERS
    # -------------------------
    for row in payload.users:
        existing = (
            db.query(User)
            .filter(
                User.username == row.username,
                User.company_id == company_id,
            )
            .first()
        )

        if existing:
            created_users[row.username] = existing
            continue

        user = User(
            username=row.username,
            email=row.email or f"{row.username}@placeholder.local",
            full_name=row.fullname,
            hashed_password=hash_password(row.password),  # temp password
            role=UserRole.end_user,
            company_id=company_id,
            is_active=True,
        )

        db.add(user)
        db.flush()
        created_users[row.username] = user
        results["users_created"] += 1

    # -------------------------
    # CREATE EXTERNAL CREDS
    # -------------------------
    for row in payload.external_credentials:
        user = created_users[row.username]

        exists = (
            db.query(UserExternalCredentials)
            .filter(
                UserExternalCredentials.user_id == user.id,
                UserExternalCredentials.provider == row.provider,
            )
            .first()
        )

        if exists:
            continue

        cred = UserExternalCredentials(
            user_id=user.id,
            provider=row.provider,
            external_username=row.external_username,
            external_password=row.external_password,
        )

        db.add(cred)
        results["external_credentials_created"] += 1

    db.commit()
    return results
