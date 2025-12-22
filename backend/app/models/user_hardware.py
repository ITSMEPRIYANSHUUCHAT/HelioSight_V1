import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class UserHardwareProfile(BaseModel):
    __tablename__ = "user_hardware_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    panel_brand: Mapped[str | None] = mapped_column(String, nullable=True)
    panel_capacity_kw: Mapped[str | None] = mapped_column(String, nullable=True)
    panel_type: Mapped[str | None] = mapped_column(String, nullable=True)

    inverter_brand: Mapped[str | None] = mapped_column(String, nullable=True)
    inverter_capacity_kw: Mapped[str | None] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="hardware_profile")
