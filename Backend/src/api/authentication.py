from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user
from ..core.exceptions import AuthenticationError
from ..database.session import get_db
from ..models.user import User
from ..schemas.authentication import LoginRequest, TokenResponse
from ..services.authentication_service import AuthenticationService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model = TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        auth_service = AuthenticationService(db)
        token, expires_at = auth_service.login(data.username, data.password)

        return TokenResponse(
            access_token = token,
            expires_at = expires_at
        )
    except AuthenticationError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return current_user