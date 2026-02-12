from typing import cast
from sqlalchemy.orm import Session

from ..models.log import Log
from ..schemas.log import LogFilter

class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, log: Log) -> Log:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def query(
        self,
        filters: LogFilter,
        limit: int,
        offset: int,
    ) -> tuple[list[Log], int]:

        query = self.db.query(Log)

        if filters.event_type is not None:
            query = query.filter(Log.event_type == filters.event_type)

        if filters.lock_id is not None:
            query = query.filter(Log.lock_id == filters.lock_id)

        if filters.user_id is not None:
            query = query.filter(Log.user_id == filters.user_id)

        if filters.success is not None:
            query = query.filter(Log.success == filters.success)

        if filters.start_time:
            query = query.filter(Log.timestamp >= filters.start_time)

        if filters.end_time:
            query = query.filter(Log.timestamp <= filters.end_time)

        total = query.count()

        items = cast(
            list[Log],
            query
                .order_by(Log.timestamp.desc())
                .limit(limit)
                .offset(offset)
                .all()
        )

        return items, total