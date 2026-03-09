from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from sqlalchemy.orm import Session

from ..core.security import verify_api_key
from ..core.exceptions import AuthenticationError, TokenValidationError
from ..database.session import get_db
from ..models.user import User
from ..services.authentication_service import AuthenticationService

bearer_scheme = HTTPBearer()
api_key_header = APIKeyHeader(name="X-Device-API-Key")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        auth_service = AuthenticationService(db)
        return auth_service.get_user_from_token(credentials.credentials)
    except (AuthenticationError, TokenValidationError):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token"
        )


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Admin access required"
        )
    return user


def require_device(api_key: str = Security(api_key_header)) -> None:
    if not verify_api_key(api_key):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid API key"
        )