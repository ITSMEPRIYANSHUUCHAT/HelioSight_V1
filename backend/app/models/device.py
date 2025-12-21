import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Device(BaseModel):
    __tablename__ = "devices"

    plant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider_integration_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("provider_integrations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ✅ MUST MATCH schema.sql
    device_serial: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    plant = relationship("Plant", lazy="joined")
