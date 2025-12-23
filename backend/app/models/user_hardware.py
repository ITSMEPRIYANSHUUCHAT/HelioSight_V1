# app/models/user_hardware.py
import uuid
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import BaseModel


class UserHardwareProfile(BaseModel):
    __tablename__ = "user_hardware_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    panel_brand: Mapped[str | None]
    panel_capacity_kw: Mapped[str | None]
    panel_type: Mapped[str | None]

    inverter_brand: Mapped[str | None]
    inverter_capacity_kw: Mapped[str | None]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[datetime | None]
