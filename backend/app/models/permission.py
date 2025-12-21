# backend/app/models/permission.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Permission(BaseModel):
    """
    Fine-grained permissions:
    e.g. plant:read, device:write
    """

    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
