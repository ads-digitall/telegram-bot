"""add interests

Revision ID: 73659cce0457
Revises: 3csdv5a5sefg
Create Date: 2025-04-12 13:29:09.523826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73659cce0457'
down_revision: Union[str, None] = '3csdv5a5sefg'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
