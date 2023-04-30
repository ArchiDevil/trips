"""Add UID for trips

Revision ID: 1daa250ee6c3
Revises: f3b468706c42
Create Date: 2023-04-30 17:21:32.038560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1daa250ee6c3'
down_revision = 'f3b468706c42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('trips', sa.Column('uid', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('trips', 'uid')
