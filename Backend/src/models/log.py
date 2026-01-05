from datetime import datetime, timezone
from typing import Optional
from enum import Enum

from sqlalchemy import String, DateTime, Enum as SQLEnum, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class EventType(str, Enum):
    UNLOCK_ATTEMPT = "unlock_attempt"
    UNLOCK_SUCCESS = "unlock_success"
    UNLOCK_FAILURE = "unlock_failure"

    FINGERPRINT_ADDED = "fingerprint_added"
    FINGERPRINT_REMOVED = "fingerprint_removed"

    ADMIN_LOGIN = "admin_login"
    MANUAL_UNLOCK = "manual_unlock"

    LOCK_HEARTBEAT = "lock_heartbeat"

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key = True)
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name = "event_type"),
        nullable = False)

    lock_id: Mapped[Optional[int]] = mapped_column(nullable = True)
    fingerprint_id: Mapped[Optional[int]] = mapped_column(nullable = True)
    user_id: Mapped[Optional[int]] = mapped_column(nullable = True)

    success: Mapped[bool] = mapped_column(Boolean, default = False, nullable = False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )

    event_metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )