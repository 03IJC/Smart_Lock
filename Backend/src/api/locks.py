from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user, require_admin
from ..core.exceptions import NotFoundError, ConflictError, ValidationError
from ..database.session import get_db
from ..models.user import User
from ..models.lock import LockStatus
from ..schemas.lock import *
from ..services.lock_service import LockService

router = APIRouter(prefix = "/locks", tags = ["Locks"])

@router.get("", response_model = list[LockResponse])
def list_locks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return LockService(db).list_locks()

@router.post("", response_model = LockResponse, status_code = status.HTTP_201_CREATED)
def create_lock(
    data: LockCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        return LockService(db).create_lock(data)
    except ConflictError as e:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = str(e))

@router.get("/{lock_id}", response_model = LockResponse)
def get_lock(
    lock_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return LockService(db).get_lock_by_id(lock_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))

@router.post("/{lock_id}/unlock", response_model = LockResponse)
def unlock_lock(
    lock_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        return LockService(db).unlock(lock_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{lock_id}/lock", response_model = LockResponse)
def lock_lock(
    lock_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        return LockService(db).lock(lock_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{lock_id}/state", response_model = LockStatus)
def get_lock_state(
    lock_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return LockService(db).get_state(lock_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))


@router.delete("/{lock_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_lock(
    lock_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        LockService(db).delete_lock(lock_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))