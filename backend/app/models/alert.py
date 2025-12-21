from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from datetime import datetime
import uuid


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)

    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)

    triggered_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
