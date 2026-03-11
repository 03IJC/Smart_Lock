from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..core.dependencies import require_device
from ..core.exceptions import NotFoundError, ValidationError
from ..database.session import get_db
from ..schemas.device import *
from ..services.access_service import AccessService
from ..services.lock_service import LockService


router = APIRouter(prefix = "/device", tags = ["Device"])

@router.post("/heartbeat/{lock_id}", status_code = status.HTTP_204_NO_CONTENT)
def lock_heartbeat(
    lock_id: int,
    data: LockHeartbeat,
    _: None = Depends(require_device),
    db: Session = Depends(get_db)
):
    LockService(db).heartbeat(lock_id, data.status)


@router.post("/access", response_model = AccessResponse)
def lock_access_attempt(
    data: AccessAttempt,
    _: None = Depends(require_device),
    db: Session = Depends(get_db)
):
    try:
        LockService(db).get_lock_by_id(data.lock_id)
        AccessService(db).verify_fingerprint(data.template_id)

        return AccessResponse(granted=True)
    except (NotFoundError, ValidationError):
        return AccessResponse(granted=False)
