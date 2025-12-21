from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey

from app.models.base import BaseModel
import uuid


class ProviderIntegration(BaseModel):
    __tablename__ = "provider_integrations"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    # ✅ MATCHES DB
    config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
