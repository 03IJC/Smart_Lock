from typing import Optional

from sqlalchemy.orm import Session

from ..models.log import Log, EventType
from ..repositories.log_repository import LogRepository
from ..schemas.log import LogFilter


class LogService:
    def __init__(self, db: Session):
        self.repo = LogRepository(db)

    def log(
        self,
        event_type: EventType,
        success: bool,
        lock_id: Optional[int] = None,
        fingerprint_id: Optional[int] = None,
        user_id: Optional[int] = None,
        event_metadata: Optional[dict] = None,
    ) -> Log:
        log = Log(
            event_type = event_type,
            success = success,
            lock_id = lock_id,
            fingerprint_id = fingerprint_id,
            user_id = user_id,
            event_metadata = event_metadata,
        )

        return self.repo.create(log)

    def query_logs(
        self,
        filters: LogFilter,
        limit: int,
        offset: int,
    ) -> tuple[list[Log], int]:
        return self.repo.query(filters, limit, offset)