# app/models/metric.py
import uuid
from sqlalchemy import String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import Base


class Metric(Base):
    __tablename__ = "metrics"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        primary_key=True,
    )

    plant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plants.id"),
        primary_key=True,
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("devices.id"),
        primary_key=True,
    )

    provider: Mapped[str]
    metric_type: Mapped[str]

    value: Mapped[float]
    unit: Mapped[str | None]

    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
