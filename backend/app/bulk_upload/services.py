from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_hardware import UserHardwareProfile
from app.models.user_external_credentials import UserExternalCredentials
from app.models.enums import UserRole, ProviderType
from app.auth.security import hash_password

from .schemas import BulkUserRow


def process_bulk_upload(
    db: Session,
    company_id,
    rows: list[BulkUserRow],
):
    created_users = 0
    skipped_users = 0
    created_creds = 0

    for row in rows:
        # 1️⃣ User
        user = (
            db.query(User)
            .filter(
                User.username == row.username,
                User.company_id == company_id,
            )
            .first()
        )

        if not user:
            user = User(
                username=row.username,
                email=row.email or f"{row.username}@placeholder.local",
                full_name=row.fullname,
                hashed_password=hash_password(row.provider_password),
                role=UserRole.end_user,
                company_id=company_id,
                is_active=True,
            )
            db.add(user)
            db.flush()
            created_users += 1
        else:
            skipped_users += 1

        # 2️⃣ Profile
        if row.whatsapp_number or row.address_line_1:
            db.merge(
                UserProfile(
                    user_id=user.id,
                    whatsapp_number=row.whatsapp_number,
                    address_line_1=row.address_line_1,
                )
            )

        # 3️⃣ Hardware
        if row.panel_brand or row.inverter_brand:
            db.merge(
                UserHardwareProfile(
                    user_id=user.id,
                    panel_brand=row.panel_brand,
                    panel_capacity_kw=row.panel_capacity_kw,
                    panel_type=row.panel_type,
                    inverter_brand=row.inverter_brand,
                    inverter_capacity_kw=row.inverter_capacity_kw,
                )
            )

        # 4️⃣ External credentials (MANDATORY)
        provider_enum = ProviderType(row.provider_type)

        existing_cred = (
            db.query(UserExternalCredentials)
            .filter(
                UserExternalCredentials.user_id == user.id,
                UserExternalCredentials.provider == provider_enum,
            )
            .first()
        )

        if not existing_cred:
            cred = UserExternalCredentials(
                user_id=user.id,
                provider=provider_enum,
                external_username=row.provider_username,
                external_password=row.provider_password,
            )
            db.add(cred)
            created_creds += 1

    db.commit()

    return {
        "created_users": created_users,
        "skipped_users": skipped_users,
        "created_external_credentials": created_creds,
    }
