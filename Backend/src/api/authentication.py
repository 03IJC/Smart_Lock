from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user
from ..core.exceptions import AuthenticationError
from ..database.session import get_db
from ..models.log import EventType
from ..models.user import User
from ..schemas.authentication import LoginRequest, TokenResponse
from ..schemas.user import UserResponse
from ..services.authentication_service import AuthenticationService
from ..services.log_service import LogService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model = TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        auth_service = AuthenticationService(db)
        token, expires_at = auth_service.login(data.username, data.password)
        user = auth_service.get_user_from_token(token)

        LogService(db).log(
            event_type = EventType.ADMIN_LOGIN,
            success = True,
            user_id = user.id
        )

        return TokenResponse(
            access_token = token,
            expires_at = expires_at
        )
    except AuthenticationError:
        LogService(db).log(
            event_type = EventType.ADMIN_LOGIN,
            success = False
        )

        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )


@router.get("/me", response_model = UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user