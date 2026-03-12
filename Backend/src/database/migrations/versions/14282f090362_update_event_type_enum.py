"""update event_type enum

Revision ID: 14282f090362
Revises: 3c98b26c3748
Create Date: 2026-03-12 21:07:47.431720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14282f090362'
down_revision: Union[str, Sequence[str], None] = '3c98b26c3748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'LOCK_CREATED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'LOCK_DELETED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'LOCK_LOCKED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'LOCK_UNLOCKED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'USER_CREATED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'USER_DELETED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'USER_UPDATED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'USER_PASSWORD_CHANGED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'FINGERPRINT_ENABLED'")
    op.execute("ALTER TYPE event_type ADD VALUE IF NOT EXISTS 'FINGERPRINT_DISABLED'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
