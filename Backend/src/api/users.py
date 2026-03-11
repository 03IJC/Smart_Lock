from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user, require_admin
from ..core.exceptions import NotFoundError, ConflictError, ValidationError
from ..database.session import get_db
from ..models.log import EventType
from ..models.user import User
from ..schemas.user import *
from ..services.log_service import LogService
from ..services.user_service import UserService

router = APIRouter(prefix = "/users", tags = ["Users"])


@router.get("", response_model = list[UserResponse])
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UserService(db).list_users()


@router.post("", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        user = UserService(db).create_user(data)

        LogService(db).log(
            event_type = EventType.USER_CREATED,
            success = True,
            user_id = user.id
        )

        return user
    except ConflictError as e:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = str(e))


@router.get("/{user_id}", response_model = UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return UserService(db).get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))


@router.patch("/{user_id}", response_model = UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        user = UserService(db).update_user(user_id, data)

        LogService(db).log(
            event_type = EventType.USER_UPDATED,
            success = True,
            user_id = user_id
        )

        return user
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    except ValidationError as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = str(e))


@router.patch("/{user_id}/password", status_code = status.HTTP_204_NO_CONTENT)
def change_password(
    user_id: int,
    data: ChangePassword,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        UserService(db).change_password(user_id, data.new_password)
        LogService(db).log(
            event_type = EventType.USER_PASSWORD_CHANGED,
            success = True,
            user_id = user_id
        )
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    except ValidationError as e:
        raise HTTPException(status_code  =status.HTTP_400_BAD_REQUEST, detail = str(e))


@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        UserService(db).soft_delete_user(user_id)

        LogService(db).log(
            event_type = EventType.USER_DELETED,
            success = True,
            user_id = user_id
        )
    except NotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    except ValidationError as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = str(e))