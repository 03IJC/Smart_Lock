from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)

    name: Mapped[str] = mapped_column(String, nullable = False)
    username: Mapped[str] = mapped_column(String, unique = True, nullable = False)
    password_hash: Mapped[str] = mapped_column(String, nullable = False)
    role: Mapped[str] = mapped_column(String, default="admin", nullable = False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )