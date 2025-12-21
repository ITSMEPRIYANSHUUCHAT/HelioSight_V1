from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from datetime import datetime


class Metric(Base):
    __tablename__ = "metrics"

    # ✅ COMPOSITE PRIMARY KEY
    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("devices.id"),
        primary_key=True,
        nullable=False,
    )

    metric_type = Column(
        String,
        primary_key=True,
        nullable=False,
    )

    timestamp = Column(
        DateTime(timezone=True),
        primary_key=True,
        nullable=False,
    )

    # Other dimensions
    company_id = Column(UUID(as_uuid=True), nullable=False)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)

    provider = Column(String, nullable=False)

    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("idx_metric_device_time", "device_id", "timestamp"),
        Index("idx_metric_plant_time", "plant_id", "timestamp"),
        Index("idx_metric_company_time", "company_id", "timestamp"),
    )
