"""Add sharing mechanism

Revision ID: 9337f1451eba
Revises: 9f8cd26e465e
Create Date: 2022-06-07 02:23:46.416492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9337f1451eba'
down_revision = '9f8cd26e465e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('sharinglinks',
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('trip_id', sa.Integer(), nullable=True),
        sa.Column('expiration_date', sa.DateTime(), nullable=False),
        sa.Column('access_type', sa.Enum('Read', 'Write', name='tripaccesstype'), nullable=False),
        sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('uuid')
    )
    op.add_column('tripaccess', sa.Column('access_type',
                                          sa.Enum('Read', 'Write', name='tripaccesstype'),
                                          nullable=False,
                                          server_default='Read'))
    op.alter_column('tripaccess', 'access_type', server_default=None)


def downgrade() -> None:
    op.drop_column('tripaccess', 'access_type')
    op.drop_table('sharinglinks')
