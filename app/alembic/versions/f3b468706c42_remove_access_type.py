"""Remove access type

Revision ID: f3b468706c42
Revises: dbfec4efa1d5
Create Date: 2023-04-30 19:21:35.637943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b468706c42'
down_revision = 'dbfec4efa1d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('tripaccess', 'access_type')
    op.drop_column('sharinglinks', 'access_type')
    op.execute('DROP TYPE tripaccesstype')


def downgrade() -> None:
    tatype = sa.Enum('Read', 'Write', name='tripaccesstype')
    tatype.create(op.get_bind())

    op.add_column('sharinglinks', sa.Column('access_type',
                                            tatype,
                                            nullable=False))
    op.add_column('tripaccess', sa.Column('access_type',
                                          tatype,
                                          nullable=False))
