from datetime import datetime, timezone
from typing import cast

from sqlalchemy.orm import Session
from ..models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.deleted_at.is_(None)
            )
            .first()
        )

    def get_by_username(self, username: str) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.username == username,
                User.deleted_at.is_(None)
            )
            .first()
        )

    def list_all(self) -> list[User]:
        return cast(
            list[User],
            self.db.query(User)
            .filter(User.deleted_at.is_(None))
            .order_by(User.created_at.desc())
            .all()
        )

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def soft_delete(self, user: User) -> None:
        user.deleted_at = datetime.now(timezone.utc)
        self.db.commit()