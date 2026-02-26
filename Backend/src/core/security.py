from typing import Any

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from .exceptions import TokenValidationError
from ..models.user import User

SECRET_KEY = "CHANGE_THIS_TO_ENV_VARIABLE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

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