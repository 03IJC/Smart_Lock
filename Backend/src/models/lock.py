from datetime import datetime, timezone
from typing import Optional
from enum import Enum

from sqlalchemy import String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class LockStatus(str, Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    OFFLINE = "offline"

class Lock(Base):
    __tablename__ = "locks"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String, unique = True, nullable = False)

    status: Mapped[LockStatus] = mapped_column(
        SQLEnum(LockStatus, name = "lock_status"),
        default = LockStatus.OFFLINE,
        nullable = False
    )
    last_heartbeat: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )