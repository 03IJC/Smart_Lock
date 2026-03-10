from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user, require_admin
from ..core.exceptions import NotFoundError, ConflictError, ValidationError
from ..database.session import get_db
from ..models.user import User
from ..schemas.fingerprint import *
from ..services.fingerprint_service import FingerprintService

router = APIRouter(prefix = "/fingerprints", tags = ["Fingerprints"])

@router.get("", response_model = list[FingerprintResponse])
def list_fingerprints(
    enabled: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if enabled is True:
        return FingerprintService(db).list_enabled_fingerprints()
    return FingerprintService(db).list_fingerprints()

@router.post("", response_model = FingerprintResponse, status_code = status.HTTP_201_CREATED)
def create_fingerprint(
    data: FingerprintCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        return FingerprintService(db).create_fingerprint(data)
    except ConflictError as e:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = str(e))

@router.get("/{fingerprint_id}", response_model = FingerprintResponse)
def get_fingerprint(
    fingerprint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return FingerprintService(db).get_fingerprint_by_id(fingerprint_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))

@router.patch("/{fingerprint_id}", response_model = FingerprintResponse)
def update_fingerprint(
    fingerprint_id: int,
    data: FingerprintUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        service = FingerprintService(db)

        if data.enabled is True:
            service.enable_fingerprint(fingerprint_id)
        if data.enabled is False:
            service.disable_fingerprint(fingerprint_id)
        if data.name:
            service.update_name(data.name, fingerprint_id)

        return service.get_fingerprint_by_id(fingerprint_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{fingerprint_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_fingerprint(
    fingerprint_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        FingerprintService(db).soft_delete_fingerprint(fingerprint_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    except ValidationError as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = str(e))