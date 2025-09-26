"""fix transcription type to text

Revision ID: 45473ffe89a7
Revises: 6f3b48afb30e
Create Date: 2025-09-25 18:09:09.936494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45473ffe89a7'
down_revision: Union[str, Sequence[str], None] = '6f3b48afb30e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'recordings',
        'transcription',
        existing_type=sa.Integer(),
        type_=sa.Text(),
        postgresql_using='transcription::text',
        existing_nullable=True
    )
    # pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'recordings',
        'transcription',
        existing_type=sa.Text(),
        type_=sa.Integer(),
        postgresql_using='transcription::integer',
        existing_nullable=False
    )
    # pass
