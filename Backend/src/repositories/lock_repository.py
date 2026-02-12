from datetime import datetime, timezone
from typing import cast

from sqlalchemy.orm import Session
from ..models.lock import Lock, LockStatus


class LockRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lock_id: int) -> Lock | None:
        return (
            self.db.query(Lock)
            .filter(
                Lock.id == lock_id,
                Lock.deleted_at.is_(None)
            )
            .first()
        )

    def get_by_name(self, lock_name: str) -> Lock | None:
        return (
            self.db.query(Lock)
            .filter(
                Lock.name == lock_name,
                Lock.deleted_at.is_(None)
            )
            .first()
        )

    def update_status(self, lock: Lock, status: LockStatus) -> None:
        lock.status = status
        self.db.commit()

    def record_heartbeat(self, lock: Lock, status: LockStatus) -> None:
        lock.status = status
        lock.last_heartbeat = datetime.now(timezone.utc)
        self.db.commit()

    def list_all(self) -> list[Lock]:
        return cast(
            list[Lock],
            self.db.query(Lock)
            .filter(Lock.deleted_at.is_(None))
            .order_by(Lock.created_at.desc())
            .all()
        )

    def create(self, lock: Lock) -> Lock:
        self.db.add(lock)
        self.db.commit()
        self.db.refresh(lock)
        return lock

    def soft_delete(self, lock: Lock) -> None:
        lock.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
