"""add ai message intelligence fields

Revision ID: 79b384e5ac08
Revises: eb169b2bf7ac
Create Date: 2026-08-02 15:33:20.879201
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79b384e5ac08"
down_revision: Union[str, Sequence[str], None] = "eb169b2bf7ac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    pass

    # ai_processed already exists in the database.
    # Do NOT add it again here.


def downgrade() -> None:
    """Downgrade schema."""

    pass