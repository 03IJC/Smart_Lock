from typing import Optional

from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, ConflictError, ValidationError
from ..core.security import hash_password
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..repositories.user_repository import UserRepository


def _validate_user(user: Optional[User]) -> None:
    if not user:
        raise NotFoundError("User not found")

    if user.deleted_at is not None:
        raise ValidationError("User has been deleted prior")

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreate) -> User:
        if self.repo.get_by_username(data.username):
            raise ConflictError("Username already exists")

        user = User(
            name = data.name,
            username = data.username,
            password_hash = hash_password(data.password),
            role = data.role
        )

        return self.repo.create(user)

    def change_password(self, user_id: int, new_password: str) -> None:
        user = self.get_user_by_id(user_id)

        user.password_hash = hash_password(new_password)

        self.repo.save(user)

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)

        if data.name is not None:
            user.name = data.name

        if data.role is not None:
            user.role = data.role

        self.repo.save(user)

        return user

    def soft_delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)

        self.repo.soft_delete(user)

    def list_users(self) -> list[User]:
        return self.repo.list_all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)

        _validate_user(user)

        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.repo.get_by_username(username)

        _validate_user(user)

        return user