from typing import cast

from sqlalchemy.orm import Session

from ..core.exceptions import AuthenticationError
from ..core.security import verify_password, create_access_token, decode_token
from ..models.user import User
from ..repositories.user_repository import UserRepository


class AuthenticationService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def login(self, username: str, password: str) -> tuple[str, int]:
        user = self.repo.get_by_username(username)

        if not user or not verify_password(password, cast(str, user.password_hash)):
            raise AuthenticationError("Invalid credentials")

        token, exp = create_access_token(user)

        return token, exp

    def get_user_from_token(self, token: str) -> User:
        payload = decode_token(token)

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Invalid token")

        try:
            user_id = user_id
        except ValueError:
            raise AuthenticationError("Invalid token")

        user = self.repo.get_by_id(user_id)

        if not user or user.deleted_at:
            raise AuthenticationError("Invalid token")

        return user