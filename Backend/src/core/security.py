import secrets
from typing import Any

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from .config import settings
from .exceptions import TokenValidationError
from ..models.user import User

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_HOURS = settings.access_token_expire_hours
DEVICE_API_KEY = settings.device_api_key

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: User) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours = ACCESS_TOKEN_EXPIRE_HOURS)

    payload = {
        "sub": str(user.id),
        "role": user.role,
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

    return token, int(expire.timestamp())

def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    except JWTError:
        raise TokenValidationError()

def verify_api_key(api_key: str) -> bool:
    if not api_key or not DEVICE_API_KEY:
        return False
    return secrets.compare_digest(api_key, DEVICE_API_KEY)