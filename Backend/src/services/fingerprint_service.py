from typing import Optional

from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, ConflictError, ValidationError
from ..models.fingerprint import Fingerprint
from ..repositories.fingerprint_repository import FingerprintRepository
from ..schemas.fingerprint import FingerprintCreate


def _validate_fingerprint(fingerprint: Optional[Fingerprint]) -> None:
    if not fingerprint:
        raise NotFoundError("Fingerprint not found")

    if fingerprint.deleted_at is not None:
        raise ValidationError("Fingerprint has been deleted prior")

class FingerprintService:
    def __init__(self, db: Session):
        self.repo = FingerprintRepository(db)

    def create_fingerprint(self, data: FingerprintCreate) -> Fingerprint:
        if self.repo.get_by_template_id(data.template_id):
            raise ConflictError("Template ID already registered")

        fingerprint = Fingerprint(
            name = data.name,
            template_id = data.template_id,
        )

        return self.repo.create(fingerprint)

    def update_name(self, fingerprint_name: str,  fingerprint_id: int) -> None:
        fingerprint = self.get_fingerprint_by_id(fingerprint_id)

        self.repo.update_name(fingerprint_name, fingerprint)

    def enable_fingerprint(self, fingerprint_id: int) -> None:
        fingerprint = self.get_fingerprint_by_id(fingerprint_id)

        self.repo.enable(fingerprint)

    def disable_fingerprint(self, fingerprint_id: int) -> None:
        fingerprint = self.get_fingerprint_by_id(fingerprint_id)

        self.repo.disable(fingerprint)

    def soft_delete_fingerprint(self, fingerprint_id: int) -> None:
        fingerprint = self.get_fingerprint_by_id(fingerprint_id)

        self.repo.soft_delete(fingerprint)

    def list_fingerprints(self) -> list[Fingerprint]:
        return self.repo.list_all()

    def list_enabled_fingerprints(self) -> list[Fingerprint]:
        return self.repo.get_enabled()

    def get_fingerprint_by_id(self, fingerprint_id: int) -> Fingerprint:
        fingerprint = self.repo.get_by_id(fingerprint_id)

        _validate_fingerprint(fingerprint)

        return fingerprint

