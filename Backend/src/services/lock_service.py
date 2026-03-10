from typing import Optional

from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, ConflictError, ValidationError
from ..models.lock import Lock, LockStatus
from ..repositories.lock_repository import LockRepository
from ..schemas.lock import LockCreate


def _validate_lock(lock: Optional[Lock]) -> None:
    if not lock:
        raise NotFoundError("Lock not found")

    if lock.deleted_at is not None:
        raise ValidationError("Lock has been deleted")

def _validate_online_lock(lock: Optional[Lock]) -> None:
    if lock.status == LockStatus.OFFLINE:
        raise ValidationError("Lock is offline and cannot be commanded")

class LockService:
    def __init__(self, db: Session):
        self.repo = LockRepository(db)

    def create_lock(self, data: LockCreate) -> Lock:
        if self.repo.get_by_name(data.name):
            raise ConflictError("Lock name already exists")

        lock = Lock(name = data.name)

        return self.repo.create(lock)

    def delete_lock(self, lock_id: int) -> None:
        lock = self.get_lock_by_id(lock_id)

        self.repo.soft_delete(lock)

    def list_locks(self) -> list[Lock]:
        return self.repo.list_all()

    def get_lock_by_id(self, lock_id: int) -> Lock:
        lock = self.repo.get_by_id(lock_id)

        _validate_lock(lock)

        return lock

    def get_lock_by_name(self, lock_name: str) -> Lock:
        lock = self.repo.get_by_name(lock_name)

        _validate_lock(lock)

        return lock

    def get_state(self, lock_id: int) -> LockStatus:
        return self.get_lock_by_id(lock_id).status

    def unlock(self, lock_id: int) -> Lock:
        lock = self.get_lock_by_id(lock_id)

        _validate_online_lock(lock)

        self.repo.update_status(lock, LockStatus.UNLOCKED)

        return lock

    def lock(self, lock_id: int) -> Lock:
        lock = self.get_lock_by_id(lock_id)

        _validate_online_lock(lock)

        self.repo.update_status(lock, LockStatus.LOCKED)

        return lock

    def heartbeat(self, lock_id: int, status: LockStatus) -> Lock:
        lock = self.get_lock_by_id(lock_id)

        self.repo.record_heartbeat(lock, status)

        return lock