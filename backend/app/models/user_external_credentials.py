# app/models/user_external_credentials.py
import uuid
from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import BaseModel
from app.models.enums import ProviderType


class UserExternalCredentials(BaseModel):
    __tablename__ = "user_external_credentials"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider: Mapped[ProviderType] = mapped_column(
        Enum(ProviderType, name="provider_type"),
        nullable=False,
        index=True,
    )

    external_username: Mapped[str] = mapped_column(String, nullable=False)
    external_password: Mapped[str] = mapped_column(String, nullable=False)

    auth_type: Mapped[str] = mapped_column(
        String,
        default="password",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="active",
        nullable=False,
    )

    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
