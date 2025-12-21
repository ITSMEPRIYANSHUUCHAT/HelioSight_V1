from sqlalchemy import String, Text,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class Company(BaseModel):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,          # <-- THIS is the fix
        nullable=False,
        default=True,
        index=True,
    )
