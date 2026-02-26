from typing import Optional

from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate
from ..schemas.user import UserUpdate
from ..repositories.user_repository import UserRepository
from ..core.security import hash_password


def _validate_user(user: Optional[User]) -> None:
    if not user:
        raise ValueError("User not found")

    if user.deleted_at is not None:
        raise ValueError("User has been deleted prior")

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreate) -> User:
        if self.repo.get_by_username(data.username):
            raise ValueError("Username already exists")

        user = User(
            name = data.name,
            username = data.username,
            password_hash = hash_password(data.password),
            role = data.role
        )

        return self.repo.create(user)

    def change_password(self, user_id: int, new_password: str) -> None:
        user = self.repo.get_by_id(user_id)

        _validate_user(user)

        user.password_hash = hash_password(new_password)

        self.repo.save(user)

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.repo.get_by_id(user_id)

        _validate_user(user)

        if data.name is not None:
            user.name = data.name

        if data.role is not None:
            user.role = data.role

        self.repo.save(user)

        return user

    def soft_delete_user(self, user_id: int) -> None:
        user = self.repo.get_by_id(user_id)

        _validate_user(user)

        self.repo.soft_delete(user)
