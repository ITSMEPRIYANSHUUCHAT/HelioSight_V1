from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import uuid


class PlantUserAssignment(Base):
    __tablename__ = "plant_user_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False, default="viewer")

    __table_args__ = (
        UniqueConstraint("plant_id", "user_id", name="uq_plant_user"),
    )
