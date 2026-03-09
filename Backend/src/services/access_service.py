from sqlalchemy.orm import Session

from ..core.exceptions import ValidationError, NotFoundError
from ..models.fingerprint import Fingerprint
from ..repositories.fingerprint_repository import FingerprintRepository


class AccessService:
    def __init__(self, db: Session):
        self.repo = FingerprintRepository(db)

    def verify_fingerprint(self, template_id: str) -> Fingerprint:
        fingerprint = self.repo.get_by_template_id(template_id)

        if not fingerprint:
            raise NotFoundError("Fingerprint not registered")

        if not fingerprint.enabled:
            raise ValidationError("Fingerprint is disabled")

        return fingerprint