"""Add passwords reset

Revision ID: dbfec4efa1d5
Revises: 9337f1451eba
Create Date: 2022-06-21 02:28:51.309205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbfec4efa1d5'
down_revision = '9337f1451eba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('passwordlinks',
                    sa.Column('uuid', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('expiration_date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('uuid'))


def downgrade() -> None:
    op.drop_table('passwordlinks')
