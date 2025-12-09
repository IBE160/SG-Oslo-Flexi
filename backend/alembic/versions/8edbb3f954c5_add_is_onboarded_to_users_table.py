"""Add is_onboarded to users table

Revision ID: 8edbb3f954c5
Revises: 7edbb3f954c4
Create Date: 2025-12-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8edbb3f954c5'
down_revision: Union[str, None] = '7edbb3f954c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_onboarded', sa.Boolean(), nullable=True))
    op.execute("UPDATE users SET is_onboarded = false")
    op.alter_column('users', 'is_onboarded', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'is_onboarded')
