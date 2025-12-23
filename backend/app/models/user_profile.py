# app/models/user_profile.py
import uuid
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import BaseModel


class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    whatsapp_number: Mapped[str | None]

    address_line_1: Mapped[str | None]
    address_line_2: Mapped[str | None]
    city: Mapped[str | None]
    state: Mapped[str | None]
    country: Mapped[str | None]
    pincode: Mapped[str | None]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[datetime | None]
