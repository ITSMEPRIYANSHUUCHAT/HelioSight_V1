# app/models/device.py
import uuid
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import BaseModel


class Device(BaseModel):
    __tablename__ = "devices"

    plant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plants.id", ondelete="CASCADE"),
        nullable=False,
    )

    provider_integration_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("provider_integrations.id"),
        nullable=False,
    )

    device_serial: Mapped[str]
    model: Mapped[str | None]

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen: Mapped[datetime | None]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[datetime | None]
