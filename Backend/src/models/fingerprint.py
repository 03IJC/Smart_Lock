from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Fingerprint(Base):
    __tablename__ = "fingerprints"

    id: Mapped[int] = mapped_column(primary_key = True)

    name: Mapped[str] = mapped_column(String, nullable = False)
    template_id: Mapped[str] = mapped_column(String, unique = True, nullable = False)
    enabled: Mapped[bool] = mapped_column(Boolean, default = False, nullable = False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )