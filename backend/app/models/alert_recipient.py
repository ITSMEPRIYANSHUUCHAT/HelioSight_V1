from sqlalchemy import Column, ForeignKey, Boolean, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from datetime import datetime
import uuid


class AlertRecipient(Base):
    __tablename__ = "alert_recipients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    recipient_type = Column(String, nullable=False)  # epc | user
    delivered = Column(Boolean, default=False)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
