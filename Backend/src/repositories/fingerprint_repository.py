from datetime import datetime, timezone
from typing import cast

from sqlalchemy.orm import Session
from ..models.fingerprint import Fingerprint


class FingerprintRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, fingerprint_id: int) -> Fingerprint | None:
        return (
            self.db.query(Fingerprint)
            .filter(
                Fingerprint.id == fingerprint_id,
                Fingerprint.deleted_at.is_(None)
            )
            .first()
        )

    def get_by_name(self, name: str) -> Fingerprint | None:
        return (
            self.db.query(Fingerprint)
            .filter(
                Fingerprint.name == name,
                Fingerprint.deleted_at.is_(None)
            )
            .first()
        )

    def get_by_template_id(self, template_id: str) -> Fingerprint | None:
        return (
            self.db.query(Fingerprint)
            .filter(
                Fingerprint.template_id == template_id,
                Fingerprint.deleted_at.is_(None)
            )
            .first()
        )

    def get_enabled(self) -> list[Fingerprint]:
        return cast(
            list[Fingerprint],
            self.db.query(Fingerprint)
            .filter(
                Fingerprint.enabled.is_(True),
                Fingerprint.deleted_at.is_(None)
            )
            .order_by(Fingerprint.created_at.desc())
            .all()
        )

    def list_all(self) -> list[Fingerprint]:
        return cast(
            list[Fingerprint],
            self.db.query(Fingerprint)
            .filter(Fingerprint.deleted_at.is_(None))
            .order_by(Fingerprint.created_at.desc())
            .all()
        )

    def create(self, fingerprint: Fingerprint) -> Fingerprint:
        self.db.add(fingerprint)
        self.db.commit()
        self.db.refresh(fingerprint)
        return fingerprint

    def soft_delete(self, fingerprint: Fingerprint) -> None:
        fingerprint.deleted_at = datetime.now(timezone.utc)
        self.db.commit()