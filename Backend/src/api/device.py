from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..core.dependencies import require_device
from ..core.exceptions import NotFoundError, ValidationError
from ..database.session import get_db
from ..models.log import EventType
from ..schemas.device import *
from ..services.access_service import AccessService
from ..services.lock_service import LockService
from ..services.log_service import LogService


router = APIRouter(prefix = "/device", tags = ["Device"])

@router.post("/heartbeat/{lock_id}", status_code = status.HTTP_204_NO_CONTENT)
def lock_heartbeat(
    lock_id: int,
    data: LockHeartbeat,
    _: None = Depends(require_device),
    db: Session = Depends(get_db)
):
    LockService(db).heartbeat(lock_id, data.status)
    LogService(db).log(
        event_type = EventType.LOCK_HEARTBEAT,
        success = True,
        lock_id = lock_id,
    )


@router.post("/access", response_model = AccessResponse)
def lock_access_attempt(
    data: AccessAttempt,
    _: None = Depends(require_device),
    db: Session = Depends(get_db)
):
    try:
        LockService(db).get_lock_by_id(data.lock_id)
        fingerprint = AccessService(db).verify_fingerprint(data.template_id)

        LogService(db).log(
            event_type = EventType.UNLOCK_SUCCESS,
            success = True,
            lock_id = data.lock_id,
            fingerprint_id = fingerprint.id
        )

        return AccessResponse(granted=True)
    except (NotFoundError, ValidationError):
        LogService(db).log(
            event_type = EventType.UNLOCK_FAILURE,
            success = False,
            lock_id = data.lock_id,
        )

        return AccessResponse(granted=False)
